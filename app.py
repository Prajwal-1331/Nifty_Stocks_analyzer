import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Stocks_2025.csv")

# Drop unwanted column if it exists
if "Unnamed: 0" in df.columns:
    df = df.drop("Unnamed: 0", axis=1)

# --- Safe Date conversion ---
if "Date" in df.columns:
    try:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", infer_datetime_format=True)
        df = df.dropna(subset=["Date"])
    except Exception as e:
        st.error(f"❌ Date conversion failed: {e}")
        st.stop()
else:
    st.error("❌ No 'Date' column found in the dataset")
    st.stop()

# Clean Stock column (remove spaces)
if "Stock" in df.columns:
    df["Stock"] = df["Stock"].replace(" ", "", regex=True)
else:
    st.error("❌ No 'Stock' column found in the dataset")
    st.stop()

# --- Compute Moving Averages ---
df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()

# --- Streamlit UI ---
st.title("📈 Nifty Stocks Interactive Dashboard")

# Category selection
if "Category" in df.columns:
    categories = df["Category"].unique()
    category = st.selectbox("Select Category", categories)
    d = df[df["Category"] == category]
else:
    st.error("❌ No 'Category' column found in the dataset")
    st.stop()

# Stock selection
stocks = d["Stock"].unique()
stock = st.selectbox("Select Stock", stocks)
r = d[d["Stock"] == stock]

# --- Plot Chart ---
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

# --- Optional Debug Info ---
if st.checkbox("Show raw data"):
    st.write(r.head(20))
