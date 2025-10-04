import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Stocks_2025.csv")
df = df.drop('Unnamed: 0', axis=1)

# Compute SMAs
df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()

# Convert columns
df["Date"] = pd.to_datetime(df["Date"])
df["Stock"] = df["Stock"].replace(" ", "", regex=True)

# Streamlit UI
st.title("📈 Nifty Stocks Interactive Dashboard")

# Category selection
categories = df["Category"].unique()
category = st.selectbox("Select Category", categories)

# Filter by category
d = df[df["Category"] == category]

# Stock selection
stocks = d["Stock"].unique()
stock = st.selectbox("Select Stock", stocks)

# Filter by stock
r = d[d["Stock"] == stock]

# Plot
fig, ax = plt.subplots(figsize=(12, 5))
sb.lineplot(x=r["Date"], y=r["Close"], color='g', marker='d', label="Close", ax=ax)
sb.lineplot(x=r["Date"], y=r["SMA_50"], color='b', label="SMA 50", ax=ax)
sb.lineplot(x=r["Date"], y=r["SMA_200"], color='r', label="SMA 200", ax=ax)

ax.set_title(f"{stock} Price with SMA50 & SMA200")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.xticks(rotation=90)
plt.legend()

st.pyplot(fig)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", infer_datetime_format=True)
