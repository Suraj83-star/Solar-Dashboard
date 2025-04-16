# ✅ Enhanced GHI Forecasting Code (3-Day Version) with Feature Engineering for Dashboard Use

# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor

# 2. Load and Prepare Data
df = pd.read_csv("dnidata.csv", parse_dates=['period_end'])
df.rename(columns={"period_end": "timestamp"}, inplace=True)
df.set_index("timestamp", inplace=True)
df.sort_index(inplace=True)

# Filter recent years to improve speed and relevance
df = df.loc['2022':]

# Drop non-numeric columns (prevent errors on resample)
df = df.select_dtypes(include=[np.number])

# Downsample to 30-minute intervals
df = df.resample('30T').mean().interpolate()

# Clean GHI values
df['ghi'] = np.where(df['ghi'] > 1000, np.nan, df['ghi'])
df['ghi'] = df['ghi'].interpolate()
df.dropna(subset=['ghi', 'air_temp', 'relative_humidity', 'cloud_opacity'], inplace=True)

# 3. Feature Engineering
df['HTI'] = df['relative_humidity'] * (df['air_temp'] / 30)
df['hour'] = df.index.hour
df['cloud_impact'] = df['cloud_opacity'] * np.sin(np.deg2rad(90 - df['hour'] * 15))
df['is_daylight'] = np.where(df['hour'].between(6, 18), 1, 0)
for lag in range(1, 4):
    df[f"ghi_lag_{lag}"] = df['ghi'].shift(lag)
df['ghi_roll_mean'] = df['ghi'].rolling(4).mean()
df['ghi_roll_std'] = df['ghi'].rolling(4).std()
fft_vals = np.abs(np.fft.fft(df['ghi'].fillna(0)))
df['fft_mean'] = np.mean(fft_vals)
df['fft_std'] = np.std(fft_vals)
df.dropna(inplace=True)

# 4. Train-Test Split
train_data = df.loc['2022':'2023']
test_data = df.loc['2024'].iloc[:144]  # 72 hours of 30-minute intervals

# 5. SARIMA Modeling
exog_cols = ['HTI', 'cloud_impact', 'is_daylight']
model = SARIMAX(train_data['ghi'], order=(2, 1, 1), seasonal_order=(1, 0, 1, 48), exog=train_data[exog_cols])
result = model.fit(disp=False)
sarima_forecast = result.predict(start=test_data.index[0], end=test_data.index[-1], exog=test_data[exog_cols])

# 6. Residual Correction with XGBoost
residuals = train_data['ghi'] - result.fittedvalues
xgb = XGBRegressor(n_estimators=50, max_depth=3, tree_method='hist', random_state=42)
xgb_features = ['HTI', 'cloud_impact', 'ghi_lag_1']
xgb.fit(train_data[xgb_features].iloc[-len(residuals):], residuals[-len(residuals):])
xgb_resid = xgb.predict(test_data[xgb_features])
final_forecast = sarima_forecast + xgb_resid

# Set GHI to zero during night
night_mask = (test_data.index.hour < 6) | (test_data.index.hour > 18)
final_forecast[night_mask] = 0

# 7. Irrigation Alert Logic
alerts = np.where(final_forecast > 500, 1, 0)

# 8. Evaluation
actual = test_data['ghi']
rmse = mean_squared_error(actual, final_forecast, squared=False)
mae = mean_absolute_error(actual, final_forecast)
accuracy = np.mean((actual > 500) == (final_forecast > 500))

print(f"3-Day Forecast Evaluation:")
print(f"Pump Activation Accuracy: {accuracy:.2%}")
print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")

# 9. Save for Dashboard
forecast_df = pd.DataFrame({
    'timestamp': test_data.index,
    'forecasted_ghi': final_forecast,
    'actual_ghi': actual,
    'irrigation_alert': alerts
})
forecast_df.to_csv("3day_forecast_results.csv", index=False)
forecast_df.head()
