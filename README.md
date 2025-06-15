# Stock Volatility Analyzer
While titled 'Stock Volatility Analyzer', this project takes a deep-dive into stock insights and displays them through charts and tables.

This project aims to interactively demonstrate the volatility behind stocks and future plans include inforporating the sentiment analysis of a stock at the current moment.

It is to be determined if I will develop my own NLP model or utilize an existing one. I also intend to expand to incorporating industry specific trends and comparing similarities and differences between different industries.

## 📦 Requirements
- Python 3.8+
- `streamlit`
- `yfinance`
- `pandas`
- `plotly`
- `numpy`
- `pandas_market_calendars`

## ⚙️ Installation


### 1. Clone the repo
```bash
git clone https://github.com/disbh/stock-dashboard.git
cd stock-dashboard
```
### 2. Create a virtual environment (This is optional)
```bash
python3 -m venv venv\
```
On Mac:
```bash
source venv/bin/activate
```
On Windows:
```bash
or venv\Scripts\activate on Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Running Application

To run the application, utilize the following snippet:
```bash
streamlit run app.py
```
