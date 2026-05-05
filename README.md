# Financial News Sentiment & Stock Analyzer

This project is a web-based dashboard built with Streamlit that analyzes the sentiment of recent financial news for a given stock ticker and displays it alongside the stock's recent price movements.

## Features
- **Real-Time Data**: Fetches 1-month historical price data using `yfinance`.
- **News Aggregation**: Retrieves the latest news headlines for the specified company.
- **NLP Sentiment Analysis**: Uses the `ProsusAI/finbert` model via Hugging Face Transformers to classify news headlines as `positive`, `negative`, or `neutral`.
- **Interactive UI**: Built with Streamlit, featuring Plotly candlestick charts.

## Setup Instructions

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

## How to push this to GitHub
1. Create a new empty repository on GitHub.
2. Link your local repo to GitHub and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```
