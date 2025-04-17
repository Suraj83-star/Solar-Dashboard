# 🌞 Smart Solar Irrigation Dashboard for Farmers

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- Page Setup ---
st.set_page_config(page_title="Smart Irrigation Dashboard", layout="wide")

# --- Load Data ---
df = pd.read_csv("3day_forecast_results.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# --- Language Settings ---
LANGUAGES = {
    'English': {
        'title': "🌞 Smart Irrigation Forecast Dashboard",
        'live_tab': "Live Forecast",
        'history_tab': "History",
        'settings_tab': "Settings",
        'ghi_label': "Global Horizontal Irradiance (GHI)",
        'alert_title': "🚨 Irrigation Recommendations",
        'pump_on': "✅ Irrigate Now",
        'pump_off': "❌ Delay Irrigation",
        'best_window': "Best GHI Window: 11 AM – 2 PM",
        'savings': "Energy Saved: ₹42 (Est.)",
        'compare_with': "Compare with",
        'language': "Language",
        'alerts_issued': "🔄 Alerts Issued",
        'days_forecasted': "📆 Days Forecasted",
        'max_ghi': "🌤️ Max GHI"
    },
    'Marathi': {
        'title': "🌞 शहाण्या सिंचन डॅशबोर्ड",
        'live_tab': "थेट अंदाज",
        'history_tab': "इतिहास",
        'settings_tab': "सेटिंग्ज",
        'ghi_label': "संपूर्ण क्षैतिज विकिरण (GHI)",
        'alert_title': "🚨 सिंचनासाठी सूचना",
        'pump_on': "✅ पंप चालू करा",
        'pump_off': "❌ पंप सुरू करू नका",
        'best_window': "सर्वोत्तम वेळ: सकाळी ११ – दुपारी २",
        'savings': "ऊर्जा बचत: ₹४२ (अंदाजित)",
        'compare_with': "याची तुलना करा",
        'language': "भाषा",
        'alerts_issued': "🔄 दिलेल्या सूचना",
        'days_forecasted': "📆 अंदाजाचे दिवस",
        'max_ghi': "🌤️ कमाल GHI"
    }
}

# --- Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3514/3514491.png", width=60)
lang = st.sidebar.selectbox("🌐 Language / भाषा", list(LANGUAGES.keys()))
labels = LANGUAGES[lang]

# --- Tabs ---
tab1, tab2, tab3 = st.tabs([labels['live_tab'], labels['history_tab'], labels['settings_tab']])

# --- Tab 1: Live Forecast ---
with tab1:
    st.title(labels['title'])

    # Forecast Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['forecasted_ghi'], mode='lines', name='Forecasted GHI'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['actual_ghi'], mode='lines', name='Actual GHI'))

    # Confidence band example (±100 W/m²)
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['forecasted_ghi'] + 100,
        mode='lines', line=dict(width=0), name='Upper Bound', showlegend=False))
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['forecasted_ghi'] - 100,
        fill='tonexty', mode='lines', line=dict(width=0), name='Lower Bound', showlegend=False,
        fillcolor='rgba(0,100,80,0.2)'))

    # Threshold line
    fig.add_hline(y=500, line_dash="dash", line_color="red")
    fig.update_layout(title=labels['ghi_label'], xaxis_title="Time", yaxis_title="GHI (W/m²)",
                      height=400, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # Recommendations
    st.subheader(labels['alert_title'])
    alert_now = (df['forecasted_ghi'] > 500).rolling(2).sum().max() >= 2
    if alert_now:
        st.success(labels['pump_on'])
    else:
        st.warning(labels['pump_off'])

    st.markdown(f"**{labels['best_window']}**")
    st.markdown(f"**{labels['savings']}**")

    # Metrics row
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric(labels['days_forecasted'], "3")
    col2.metric(labels['max_ghi'], f"{df['forecasted_ghi'].max():.0f} W/m²")
    col3.metric(labels['alerts_issued'], f"{df['irrigation_alert'].sum()} times")

# --- Tab 2: History ---
with tab2:
    view = st.selectbox(labels['compare_with'], ["Last Week", "Last Month", "Monsoon Season"])
    st.write(f"📊 Comparison not implemented in this version. Placeholder for: {view}")

# --- Tab 3: Settings ---
with tab3:
    st.markdown("### 🌍 Region Selector")
    region = st.selectbox("Select your district", ["Aurangabad", "Jalna", "Beed", "Latur"])

    st.markdown("### 🔔 Notifications")
    sms_opt = st.checkbox("Enable SMS Alerts")
    rain_alert = st.checkbox("Notify me before monsoon rain")

    st.markdown("### 🗣️ Voice Feedback (Coming Soon)")
    st.button("🔊 Speak Today's Recommendation")

# --- Footer ---
st.markdown("""
<style>
footer {visibility: hidden;}
.css-18e3th9 {padding-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

st.info("Built with ❤️ for Indian farmers using solar AI forecasting")
