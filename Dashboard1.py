# 📊 Smart Irrigation Dashboard (Multilingual + Forecast + Enhanced UI)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Smart Irrigation Dashboard", layout="wide")

# Load forecast data
df = pd.read_csv("3day_forecast_results.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# LANGUAGE SUPPORT
LANGUAGES = {
    'English': {
        'title': "🌞 Solar Forecast for Smart Irrigation",
        'ghi_label': "Global Horizontal Irradiance (GHI) Forecast",
        'alert_title': "🚨 Irrigation Recommendations",
        'pump_on': "✅ Turn on the Pump",
        'pump_off': "❌ Do not Pump",
        'chart_title': "Forecast vs Actual GHI",
        'metrics': ["📆 Days Forecasted", "🌤️ Max GHI", "🔄 Alerts Issued"],
        'download': "📥 Download Forecast CSV",
        'best_time': "🕓 Best Time to Irrigate: 11 AM – 2 PM",
        'energy_saving': "⚡ Estimated energy saved: ₹340",
        'lang_label': "Select Language"
    },
    'Marathi': {
        'title': "🌞 शहाण्या सिंचनासाठी सौर अंदाज",
        'ghi_label': "संपूर्ण क्षैतिज विकिरण (GHI) चा अंदाज",
        'alert_title': "🚨 सिंचनासाठी सूचना",
        'pump_on': "✅ पंप चालू करा",
        'pump_off': "❌ पंप चालू करू नका",
        'chart_title': "GHI अंदाज विरुद्ध वास्तविक",
        'metrics': ["📆 अंदाजाचे दिवस", "🌤️ जास्तीत जास्त GHI", "🔄 दिलेले अलर्ट"],
        'download': "📥 CSV डाउनलोड करा",
        'best_time': "🕓 सर्वोत्तम सिंचन वेळ: सकाळी 11 – दुपारी 2",
        'energy_saving': "⚡ बचत झालेली ऊर्जा: ₹340",
        'lang_label': "भाषा निवडा"
    },
    'Hindi': {
        'title': "🌞 स्मार्ट सिंचाई के लिए सौर पूर्वानुमान",
        'ghi_label': "ग्लोबल हॉरिजॉन्टल इरैडिएंस (GHI) का पूर्वानुमान",
        'alert_title': "🚨 सिंचाई की सिफारिशें",
        'pump_on': "✅ पंप चालू करें",
        'pump_off': "❌ पंप चालू न करें",
        'chart_title': "अनुमानित बनाम वास्तविक GHI",
        'metrics': ["📆 पूर्वानुमान अवधि", "🌤️ अधिकतम GHI", "🔄 अलर्ट की संख्या"],
        'download': "📥 CSV डाउनलोड करें",
        'best_time': "🕓 सिंचाई का सर्वोत्तम समय: सुबह 11 – दोपहर 2",
        'energy_saving': "⚡ ऊर्जा की बचत: ₹340",
        'lang_label': "भाषा चुनें"
    }
}

# Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3514/3514491.png", width=60)
selected_lang = st.sidebar.selectbox("🌐 Language / भाषा / भाषा", list(LANGUAGES.keys()))
labels = LANGUAGES[selected_lang]

# Title
st.title(labels['title'])

# GHI Forecast Plot with Confidence Intervals
st.subheader(labels['ghi_label'])

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['forecasted_ghi'], mode='lines+markers', name='Forecasted GHI', line=dict(color='blue')))
if 'actual_ghi' in df.columns:
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['actual_ghi'], mode='lines', name='Actual GHI', line=dict(color='gray')))
fig.add_trace(go.Scatter(x=df['timestamp'], y=[500]*len(df), mode='lines', name='Threshold (500)', line=dict(color='red', dash='dash')))
fig.update_layout(title=labels['chart_title'], xaxis_title='Timestamp', yaxis_title='GHI (W/m²)', template='plotly_white')
st.plotly_chart(fig, use_container_width=True)

# Irrigation Alert Table
df['alert_text'] = df['irrigation_alert'].map({1: labels['pump_on'], 0: labels['pump_off']})
st.subheader(labels['alert_title'])
st.dataframe(df[['timestamp', 'forecasted_ghi', 'alert_text']].rename(columns={
    'timestamp': '🕒 Time',
    'forecasted_ghi': '🔆 Predicted GHI',
    'alert_text': '🚜 Action'
}))

# Summary Insights
st.success(labels['best_time'])
st.warning(labels['energy_saving'])

# Key Metrics
col1, col2, col3 = st.columns(3)
col1.metric(labels['metrics'][0], "3")
col2.metric(labels['metrics'][1], f"{df['forecasted_ghi'].max():.0f} W/m²")
col3.metric(labels['metrics'][2], f"{df['irrigation_alert'].sum()}")

# Download Button
st.download_button(
    label=labels['download'],
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="ghi_forecast.csv",
    mime='text/csv'
)

# Footer
st.markdown("""
<style>
footer {visibility: hidden;}
.css-18e3th9 {padding-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

st.info("💡 Developed by Suraj Shah for rural solar irrigation planning – April 2025")
