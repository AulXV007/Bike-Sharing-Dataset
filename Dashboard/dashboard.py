import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Pengaturan awal
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")
st.title("🚲 Dashboard Penyewaan Sepeda")
st.markdown("Visualisasi tren dan analisis faktor yang mempengaruhi penyewaan sepeda.")

# Load data
def load_data():
    df = pd.read_csv("main_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Sidebar filter
st.sidebar.header("🎚️ Filter Data")
min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input("Rentang tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

filtered_df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

# Statistik Ringkas
st.subheader("📌 Statistik Umum")
col1, col2, col3 = st.columns(3)
col1.metric("Total Hari", filtered_df["date"].nunique())
col2.metric("Total Penyewaan", int(filtered_df["count"].sum()))
col3.metric("Rata-rata Harian", round(filtered_df["count"].mean(), 2))

# Line Chart Penyewaan Harian
st.subheader("📈 Tren Penyewaan Sepeda per Hari")
fig1, ax1 = plt.subplots()
ax1.plot(filtered_df["date"], filtered_df["count"], color="tab:blue")
ax1.set_xlabel("Tanggal")
ax1.set_ylabel("Jumlah Penyewaan")
ax1.set_title("Tren Harian")
st.pyplot(fig1)

# Rata-rata Penyewaan Berdasarkan Kategori
st.subheader("📊 Rata-rata Penyewaan berdasarkan Kategori")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Musim**")
    seasonal_avg = filtered_df.groupby("season")["count"].mean().sort_values()
    st.bar_chart(seasonal_avg)

with col2:
    st.markdown("**Cuaca**")
    weather_avg = filtered_df.groupby("weather")["count"].mean().sort_values()
    st.bar_chart(weather_avg)

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Hari Kerja vs Libur**")
    workingday_avg = filtered_df.groupby("workingday")["count"].mean()
    st.bar_chart(workingday_avg.rename(index={0: "Libur", 1: "Hari Kerja"}))

with col4:
    st.markdown("**Hari Libur Nasional**")
    holiday_avg = filtered_df.groupby("holiday")["count"].mean()
    st.bar_chart(holiday_avg.rename(index={0: "Bukan Libur", 1: "Hari Libur"}))

# Scatter Plot: Cuaca dan Penyewaan
st.subheader("🌡️ Korelasi Faktor Cuaca dan Jumlah Penyewaan")

col1, col2 = st.columns(2)

with col1:
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=filtered_df, x="temp", y="count", ax=ax2)
    ax2.set_title("Suhu vs Penyewaan")
    st.pyplot(fig2)

with col2:
    fig3, ax3 = plt.subplots()
    sns.scatterplot(data=filtered_df, x="hum", y="count", ax=ax3)
    ax3.set_title("Kelembapan vs Penyewaan")
    st.pyplot(fig3)