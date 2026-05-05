import streamlit as st
import yfinance as yf
import pandas as pd
from transformers.pipelines import pipeline
import plotly.graph_objects as go

st.set_page_config(page_title="FinBERT Financial Sentiment Analyzer", layout="wide")

@st.cache_resource
def load_sentiment_model():
    # FinBERT is specifically trained on financial text
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

st.title("📈 FinBERT Financial News Sentiment & Stock Analyzer")
st.markdown("Analyze recent news sentiment for a stock and see its recent price movements.")

ticker_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)", "AAPL").upper()

if ticker_symbol:
    # 1. Fetch Data
    st.subheader(f"Data for {ticker_symbol}")
    ticker = yf.Ticker(ticker_symbol)
    
    with st.spinner("Fetching stock data..."):
        hist_data = ticker.history(period="1mo")
        
    if hist_data.empty:
        st.error("No data found for this ticker. Please try another one.")
    else:
        # Plot Stock Price
        st.write("**1-Month Price History**")
        fig = go.Figure(data=[go.Candlestick(x=hist_data.index,
                        open=hist_data['Open'],
                        high=hist_data['High'],
                        low=hist_data['Low'],
                        close=hist_data['Close'])])
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=400)
        st.plotly_chart(fig, use_container_width=True)

        # 2. Fetch News
        st.write("**Recent News & Sentiment**")
        with st.spinner("Fetching news & analyzing sentiment (this may take a moment)..."):
            # yfinance returns a list of dictionaries for news
            news = ticker.news
            
            if not news:
                st.warning("No recent news found for this ticker via Yahoo Finance.")
            else:
                analyzer = load_sentiment_model()
                
                news_data = []
                for article in news:
                    content = article.get('content', article)
                    title = content.get('title', '')
                    
                    url_obj = content.get('clickThroughUrl', {})
                    link = url_obj.get('url', '') if isinstance(url_obj, dict) else article.get('link', '')
                        
                    provider = content.get('provider', {})
                    publisher = provider.get('displayName', '') if isinstance(provider, dict) else article.get('publisher', '')
                    
                    if title:
                        # Analyze sentiment of the headline
                        result = analyzer(title)[0]
                        sentiment = result['label']
                        score = result['score']
                        
                        news_data.append({
                            "Title": title,
                            "Publisher": publisher,
                            "Sentiment": sentiment,
                            "Confidence": f"{score:.2%}",
                            "Link": link
                        })
                
                df_news = pd.DataFrame(news_data)
                
                # Display summary metrics
                if not df_news.empty:
                    col1, col2, col3 = st.columns(3)
                    pos_count = len(df_news[df_news['Sentiment'] == 'positive'])
                    neg_count = len(df_news[df_news['Sentiment'] == 'negative'])
                    neu_count = len(df_news[df_news['Sentiment'] == 'neutral'])
                    
                    col1.metric("Positive News", pos_count)
                    col2.metric("Neutral News", neu_count)
                    col3.metric("Negative News", neg_count)
                    
                    st.markdown("---")
                    st.markdown("### 🤖 AI Trading Signal")
                    
                    total_news = len(df_news)
                    sentiment_score = 0
                    if total_news > 0:
                        sentiment_score = (pos_count - neg_count) / total_news
                    
                    # Calculate simple price momentum (last 5 days vs today)
                    price_change = 0
                    if len(hist_data) >= 5:
                        current_price = hist_data['Close'].iloc[-1]
                        past_price = hist_data['Close'].iloc[-5]
                        price_change = (current_price - past_price) / past_price
                    
                    signal = "HOLD 😐"
                    reasoning = ""
                    
                    if sentiment_score > 0.2 and price_change > 0:
                        signal = "STRONG BUY 🚀"
                        reasoning = "Both AI news sentiment and recent price momentum are highly positive."
                    elif sentiment_score > 0.1:
                        signal = "BUY 📈"
                        reasoning = "AI news sentiment is generally positive, suggesting a favorable outlook."
                    elif sentiment_score < -0.2 and price_change < 0:
                        signal = "STRONG SELL 🚨"
                        reasoning = "Both AI news sentiment and recent price momentum are heavily negative."
                    elif sentiment_score < -0.1:
                        signal = "SELL 📉"
                        reasoning = "AI news sentiment is leaning negative. Caution is advised."
                    else:
                        signal = "HOLD 😐"
                        reasoning = "AI news sentiment is mixed or neutral. No clear directional signal."
                        
                    st.info(f"**Recommendation:** {signal}  \n**Reasoning:** {reasoning}")
                    st.markdown("---")
                    
                    # Apply color coding to sentiment
                    def color_sentiment(val):
                        color = 'green' if val == 'positive' else 'red' if val == 'negative' else 'gray'
                        return f'color: {color}'
                    
                    # Display the dataframe
                    st.dataframe(
                        df_news.style.map(color_sentiment, subset=['Sentiment']),
                        column_config={
                            "Link": st.column_config.LinkColumn("Read Article")
                        },
                        hide_index=True,
                        use_container_width=True
                    )
