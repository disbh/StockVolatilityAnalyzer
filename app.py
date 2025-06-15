import streamlit as st

import yfinance as yf

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from scipy.signal import find_peaks

# -----------------
# Data Fetching
# -----------------
def get_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

# ----------------------------
# Data Insights with Graphs
# ----------------------------
def stock_insights(df):
    df['Net Change'] = df['Close'].diff()
    df['Max Change'] = df['High'] - df['Low']
    df['Pct Change'] = df['Close'].pct_change()
    df['Gap'] = df['Open'] - df['Close'].shift(1)

    return {
        "Total Days": len(df),
        "Volatility (std dev)": round(df['Pct Change'].std(), 4),
        "Cumulative Return (%)": round(((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100, 2),
        "High": round(df['High'].max()),
        "Low": round(df['Low'].min())
    }
def stock_insights_advanced(df):
    df['Net Change'] = df['Close'].diff()
    df['Max Change'] = df['High'] - df['Low']
    df['Pct Change'] = df['Close'].pct_change()
    df['Gap'] = df['Open'] - df['Close'].shift(1)

    return {
        "Total Days": len(df),
        "Up Days": (df['Net Change'] > 0).sum(),
        "Down Days": (df['Net Change'] < 0).sum(),
        "Max Daily % Gain": round(df['Pct Change'].max() * 100, 2),
        "Max Daily % Loss": round(df['Pct Change'].min() * 100, 2),
        "Average Daily Range ($)": round(df['Max Change'].mean(), 2),
        "Volatility (std dev)": round(df['Pct Change'].std(), 4),
        "Cumulative Return (%)": round(((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100, 2),
        "Max Gap Up ($)": round(df['Gap'].max(), 2),
        "Max Gap Down ($)": round(df['Gap'].min(), 2),
        "Big Move Days (>2%)": (abs(df['Pct Change']) > 0.02).sum()
}
def plot_all_graphs(df, ticker):
    df['Rolling Volatility'] = df['Pct Change'].rolling(20).std()
    df['Cumulative Return'] = (1 + df['Pct Change']).cumprod()

    st.markdown("### 📊 Interactive Charts")

    def plot_fig(y, title, color, yaxis_label):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[y],
            mode='lines',
            name=title,
            line=dict(color=color)
        ))
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title=yaxis_label,
            hovermode='x unified',
            template='plotly_white'
        )
        return fig

    # Layout: 3 rows × 2 columns
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_fig('Close', f'{ticker.upper()} - Closing Price', '#1f77b4', 'Price ($)'), use_container_width=True)
    with col2:
        st.plotly_chart(plot_fig('Volume', 'Daily Volume', '#2ca02c', 'Volume'), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(plot_fig('Pct Change', 'Daily % Change', '#ff7f0e', 'Percent Change'), use_container_width=True)
    with col4:
        st.plotly_chart(plot_fig('Rolling Volatility', '20-Day Rolling Volatility', '#9467bd', 'Volatility'), use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(plot_fig('Max Change', 'Max Daily Price Change', '#8c564b', 'Range ($)'), use_container_width=True)
    with col6:
        st.plotly_chart(plot_fig('Cumulative Return', 'Cumulative Return (Normalized)', '#d62728', 'Cumulative Return'), use_container_width=True)

# ----------------------------
# Streamlit UI Formatting
# ----------------------------
st.set_page_config(page_title="📈 Stock Insights", layout="wide")

# Inject custom CSS
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            color: #4CAF50;
            font-weight: 700;
            text-align: center;
            padding: 10px 0;
        }
        .metric-box {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 10px;
        }
        .stMetric {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Stock Insights Dashboard</div>", unsafe_allow_html=True)

ticker = st.text_input("Enter stock ticker:", "AAPL")
period = st.selectbox("Select period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"])

if ticker:
    df = get_stock_data(ticker, period)
    if df.empty:
        st.warning("⚠️ No data found. Try another ticker or shorter time period.")
    else:
        insights = stock_insights_advanced(df)

        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            st.metric("Cumulative Return (%)", f"{insights['Cumulative Return (%)']}%")
        with col2:
            st.metric("Volatility (std dev)", insights['Volatility (std dev)'])
        with col3:
            st.metric("Avg Daily Range ($)", insights['Average Daily Range ($)'])

        with col4:
            st.metric("Up Days", insights['Up Days'])
        with col5:
            st.metric("Down Days", insights['Down Days'])
        with col6:
            st.metric("Big Move Days (>2%)", insights['Big Move Days (>2%)'])

        st.markdown("---")
        st.subheader("📈 Price Chart with Detected Peaks")
        plot_all_graphs(df, ticker)
