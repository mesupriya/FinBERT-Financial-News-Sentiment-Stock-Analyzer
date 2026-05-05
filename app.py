import streamlit as st
import yfinance as yf
import pandas as pd
from transformers import pipeline
import plotly.graph_objects as go

st.set_page_config(page_title="Financial Sentiment Analyzer", layout="wide")

@st.cache_resource
def load_sentiment_model():
    # FinBERT is specifically trained on financial text
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

st.title("📈 Financial News Sentiment & Stock Analyzer")
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
                    title = article.get('title', '')
                    link = article.get('link', '')
                    publisher = article.get('publisher', '')
                    
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
