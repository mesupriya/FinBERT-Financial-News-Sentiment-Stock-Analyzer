# 📈 FinBERT Financial News Sentiment & Stock Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.2-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)
![Transformers](https://img.shields.io/badge/Hugging%20Face-Transformers-F9AB00.svg?style=flat&logo=HuggingFace&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A modern, machine learning-powered web application that analyzes real-time financial news sentiment and correlates it with stock price movements. 

## 🚀 Overview

This project was built to explore the intersection of Natural Language Processing (NLP) and quantitative finance. By scraping the latest news headlines for any given stock ticker and passing them through **FinBERT** (a pre-trained NLP model specifically tuned for financial text), the application classifies market sentiment as `Positive`, `Negative`, or `Neutral`. It then displays these insights alongside an interactive candlestick chart of the stock's recent price history.

## ✨ Features

- **Real-Time Market Data**: Fetches the latest 1-month historical price data using the `yfinance` API.
- **Automated News Aggregation**: Retrieves the most recent news headlines relevant to the requested company.
- **AI-Powered Sentiment Analysis**: Utilizes the `ProsusAI/finbert` Hugging Face model to accurately gauge the sentiment of financial news.
- **Interactive Visualizations**: Beautiful, responsive candlestick charts powered by `Plotly`.
- **Sleek UI**: Built entirely in Python using `Streamlit`.

## 🛠️ Technology Stack

- **Frontend / Web Framework**: [Streamlit](https://streamlit.io/)
- **Data Acquisition**: [yfinance](https://pypi.org/project/yfinance/)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
- **Machine Learning / NLP**: [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) & [PyTorch](https://pytorch.org/)
- **Visualization**: [Plotly](https://plotly.com/python/)

## 💻 Local Setup & Installation

Follow these steps to run the project locally on your machine.

### Prerequisites
- Python 3.8 or higher installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/financial-sentiment-analyzer.git
cd financial-sentiment-analyzer
```

### 2. Create a Virtual Environment (Recommended)
**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```
**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: Installing PyTorch and Transformers may take a few minutes depending on your internet connection.)*

### 4. Run the Application
```bash
streamlit run app.py
```
The dashboard will automatically open in your default web browser at `http://localhost:8501`.

## 📊 Usage

1. Open the web dashboard.
2. Enter a stock ticker symbol into the search bar (e.g., `AAPL` for Apple, `TSLA` for Tesla, `NVDA` for NVIDIA).
3. The app will fetch the latest price data and generate a candlestick chart.
4. Below the chart, the AI will process the latest news headlines and display the sentiment breakdown (Positive, Neutral, Negative) along with confidence scores and direct links to the articles.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/YOUR_USERNAME/financial-sentiment-analyzer/issues).

## 📝 License

This project is open-source and available under the MIT License.
