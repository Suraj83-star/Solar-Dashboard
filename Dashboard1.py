# 📊 Solar GHI Forecast Dashboard for Farmers (Multilingual + Enhanced UI)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the forecast results (ensure this file is generated from your model)
df = pd.read_csv("3day_forecast_results.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# LANGUAGE OPTIONS
LANGUAGES = {
    'English': {
        'title': "🌞 Solar Forecast for Smart Irrigation",
        'ghi_label': "Global Horizontal Irradiance (GHI) Forecast",
        'alert_title': "🚨 Irrigation Recommendations",
        'pump_on': "✅ Turn on the Pump",
        'pump_off': "❌ Do not Pump",
        'chart_title': "Forecast vs Actual GHI",
        'lang_label': "Select Language"
    },
    'Marathi': {
        'title': "🌞 शहाण्या सिंचनासाठी सौर अंदाज",
        'ghi_label': "संपूर्ण क्षैतिज विकिरण (GHI) चा अंदाज",
        'alert_title': "🚨 सिंचनासाठी सूचना",
        'pump_on': "✅ पंप चालू करा",
        'pump_off': "❌ पंप चालू करू नका",
        'chart_title': "GHI अंदाज विरुद्ध वास्तविक",
        'lang_label': "भाषा निवडा"
    },
    'Hindi': {
        'title': "🌞 स्मार्ट सिंचाई के लिए सौर पूर्वानुमान",
        'ghi_label': "ग्लोबल हॉरिजॉन्टल इरैडिएंस (GHI) का पूर्वानुमान",
        'alert_title': "🚨 सिंचाई की सिफारिशें",
        'pump_on': "✅ पंप चालू करें",
        'pump_off': "❌ पंप चालू न करें",
        'chart_title': "अनुमानित बनाम वास्तविक GHI",
        'lang_label': "भाषा चुनें"
    }
}

# SIDEBAR CONFIG
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3514/3514491.png", width=60)
selected_lang = st.sidebar.selectbox("🌐 Language / भाषा / भाषा", list(LANGUAGES.keys()))
labels = LANGUAGES[selected_lang]

st.set_page_config(page_title="Smart Irrigation Dashboard", layout="wide")
st.title(labels['title'])

# GHI FORECAST PLOT
st.subheader(labels['ghi_label'])
fig = px.line(df, x='timestamp', y=['forecasted_ghi', 'actual_ghi'], labels={'value': 'GHI (W/m²)', 'timestamp': 'Time'},
              title=labels['chart_title'])
st.plotly_chart(fig, use_container_width=True)

# IRRIGATION ALERTS
df['alert_text'] = df['irrigation_alert'].map({1: labels['pump_on'], 0: labels['pump_off']})
st.subheader(labels['alert_title'])
st.dataframe(df[['timestamp', 'forecasted_ghi', 'alert_text']].rename(columns={
    'timestamp': '🕒 Time',
    'forecasted_ghi': '🔆 Predicted GHI',
    'alert_text': '🚜 Action'
}))

# METRICS
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("📆 Days Forecasted", "3")
col2.metric("🌤️ Max GHI", f"{df['forecasted_ghi'].max():.0f} W/m²")
col3.metric("🔄 Alerts Issued", f"{df['irrigation_alert'].sum()} times")

# FOOTER
st.markdown("""
<style>
footer {visibility: hidden;}
.css-18e3th9 {padding-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

st.info("Developed for rural empowerment using solar forecasting and AI")
