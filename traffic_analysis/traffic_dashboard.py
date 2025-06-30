# Your Streamlit dashboard code here
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(layout="wide", page_title="Traffic Pattern Dashboard")

st.title("🚦 Traffic Pattern Analysis Dashboard")
st.markdown("Analyze traffic volume, weather effects, incident trends, and fatality stats interactively.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("traffic_data.csv", parse_dates=["date"])
    fatalities = pd.read_csv("fatalities_data.csv")
    return df, fatalities

df, fatal_df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
weather_option = st.sidebar.radio("Weather Filter:", ["All Days", "Bad Weather Only", "Normal Days Only"])

if weather_option == "Bad Weather Only":
    df = df[df["is_bad_weather_day"] == True]
elif weather_option == "Normal Days Only":
    df = df[df["is_bad_weather_day"] == False]

# --- Section 1: Hourly Traffic Volume ---
st.subheader("📊 Hourly Traffic Volume")
hourly_traffic = df.groupby("hour")["Traffic Volume"].sum().reset_index()
fig1, ax1 = plt.subplots()
sns.lineplot(data=hourly_traffic, x="hour", y="Traffic Volume", marker='o', ax=ax1)
ax1.set_title("Traffic Volume by Hour")
st.pyplot(fig1)

# --- Section 2: Traffic by Day of Week ---
st.subheader("📅 Traffic by Day of Week")
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_traffic = df["day_of_week"].value_counts().reindex(dow_order).reset_index()
dow_traffic.columns = ['Day', 'Traffic Volume']
fig2, ax2 = plt.subplots()
sns.barplot(data=dow_traffic, x='Day', y='Traffic Volume', palette='viridis', ax=ax2)
ax2.set_title("Total Traffic by Day of Week")
st.pyplot(fig2)

# --- Section 3: Incident Reports per Year ---
st.subheader("🚨 Incident Reports Per Year")
yearly_incidents = df.groupby(df['date'].dt.year)["Incident Reports"].sum().reset_index()
yearly_incidents.columns = ['Year', 'Incident Reports']
fig3, ax3 = plt.subplots()
sns.barplot(data=yearly_incidents, x='Year', y='Incident Reports', palette='flare', ax=ax3)
ax3.set_title("Yearly Incident Reports")
st.pyplot(fig3)

# --- Section 4: Road Fatalities Per Year ---
st.subheader("⚰️ Road Fatalities Per Year")
fig4, ax4 = plt.subplots()
sns.lineplot(data=fatal_df, x="year", y="Total_Deaths", marker="o", color="red", ax=ax4)
ax4.set_title("Yearly Road Fatalities")
ax4.set_ylabel("Number of Deaths")
st.pyplot(fig4)

# --- Section 5: Insights ---
st.subheader("🧠 Insights Summary")
peak_hour = df['hour'].value_counts().idxmax()
busiest_day = df['day_of_week'].value_counts().idxmax()
weather_days = df['is_bad_weather_day'].sum()

st.markdown(f"""
- **Peak Hour:** {peak_hour}:00 hrs  
- **Busiest Day:** {busiest_day}  
- **Bad Weather Days in Dataset:** {weather_days} days  
""")
