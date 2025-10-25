# btc_gods_correlation_dashboard.py
# Author: Joey Bolkovatz + Seshat
# Description: Dark-themed Streamlit dashboard showing price correlation between BTC and GODS

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date, timedelta

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="BTC vs GODS Correlation Dashboard",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------ DARK MODE STYLE ------------------
dark_css = """
<style>
body {
    background-color: #0e1117;
    color: #c7d5e0;
    font-family: 'Segoe UI', sans-serif;
}
.sidebar .sidebar-content {
    background-color: #111418;
}
[data-testid="stHeader"] {
    background: #0e1117;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #00ffe5;
    text-shadow: 0px 0px 8px #00ffe5;
}
.metric-label, .stMetricLabel {
    color: #c7d5e0 !important;
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.title("🪙 BTC vs GODS Correlation Dashboard")
st.caption("Analyze whether Bitcoin and Gods Unchained move together or in opposite directions")

# ------------------ DATA FETCH ------------------
end_date = date.today()
start_date = end_date - timedelta(days=90)

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    data["Daily_Return"] = data["Close"].pct_change()
    return data.dropna()

btc = load_data("BTC-USD")
gods = load_data("GODS-USD")

# ------------------ CORRELATION ------------------
corr_value = btc["Daily_Return"].corr(gods["Daily_Return"])
relation = "move together 🔼" if corr_value > 0 else "move opposite 🔽"

# ------------------ METRICS ------------------
col1, col2, col3 = st.columns(3)

# Safely extract numeric values as floats
btc_last_price = float(btc["Close"].iloc[-1].item() if hasattr(btc["Close"].iloc[-1], "item") else btc["Close"].iloc[-1])
gods_last_price = float(gods["Close"].iloc[-1].item() if hasattr(gods["Close"].iloc[-1], "item") else gods["Close"].iloc[-1])
corr_display = f"{corr_value:.3f}"

# Display metrics with formatted values
col1.metric("BTC Last Price", f"${btc_last_price:,.2f}")
col2.metric("GODS Last Price", f"${gods_last_price:,.4f}")
col3.metric("Correlation (90d)", corr_display, relation)

# ------------------ PRICE CHART ------------------
st.subheader("📈 Price Comparison")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(btc.index, btc["Close"], label="BTC", color="#00ffe5")
ax1.plot(gods.index, gods["Close"] * (btc["Close"].iloc[-1] / gods["Close"].iloc[-1]),
         label="GODS (scaled)", color="#ff00aa")
ax1.set_facecolor("#111418")
ax1.legend(facecolor="#111418", labelcolor="white")
st.pyplot(fig1)

# ------------------ RETURNS CHART ------------------
st.subheader("📊 Daily % Change Comparison")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.scatter(btc["Daily_Return"], gods["Daily_Return"], color="#00ffe5", alpha=0.7)
ax2.set_xlabel("BTC Daily Return")
ax2.set_ylabel("GODS Daily Return")
ax2.set_facecolor("#111418")
st.pyplot(fig2)

# ------------------ INTERPRETATION ------------------
st.markdown(f"""
### 🔍 Interpretation
The **correlation coefficient** of **{corr_value:.3f}** indicates that BTC and GODS {relation}.
- **Positive (> 0)** → they generally rise and fall together.  
- **Negative (< 0)** → when one rises, the other tends to drop.  
- **Close to 0** → little to no relationship.  
""")

st.markdown("---")
st.caption("Data source: Yahoo Finance | Built with 💜 by Joey + Seshat")

