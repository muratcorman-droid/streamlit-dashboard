import streamlit as st
import pandas as pd
import plotly.express as px
    
st.set_page_config(page_title="Dashboard", layout="wide")

# ---- LOAD DATA ----
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSm-RCknFcNTfdxfpgwkxFZenuIQfLORE5kXDTyKF_FeW6CXCvQffk9RFrM2Ptcf2S-icK_mPOSw6_U/pub?output=csv"

def load_data():
    return pd.read_csv(CSV_URL)

df = load_data()
df.columns = df.columns.str.lower()

st.title("📊 Operasyon Dashboard")

# ---- KPIs ----
k1, k2, k3 = st.columns(3)

k1.metric("Toplam Satır", len(df))

if "order_id" in df.columns:
    k2.metric("Toplam Sipariş", df["order_id"].nunique())
else:
    k2.metric("Toplam Sipariş", "-")

if {"price", "quantity"}.issubset(df.columns):
    df["gmv"] = df["price"] * df["quantity"]
    k3.metric("Toplam GMV", f"{df['gmv'].sum():,.0f}")
else:
    k3.metric("Toplam GMV", "-")

st.divider()

# ---- FILTERS ----
with st.sidebar:
    st.header("Filtreler")

    if "status" in df.columns:
        status = st.multiselect(
            "Status",
            df["status"].unique(),
            default=df["status"].unique()
        )
        df = df[df["status"].isin(status)]

# ---- CHART ----
if "order_date" in df.columns and "gmv" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    daily = df.groupby("order_date")["gmv"].sum().reset_index()

    fig = px.line(
        daily,
        x="order_date",
        y="gmv",
        title="Günlük GMV"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---- TABLE ----
st.subheader("Detay Tablo")
st.dataframe(df, use_container_width=True)
