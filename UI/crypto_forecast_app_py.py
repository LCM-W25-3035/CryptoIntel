import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

# Set page config
st.set_page_config(page_title="Crypto Price Forecast", layout="centered")
st.title("📈 LSTM-based Crypto Forecast – 7 Day Close Price Prediction")

# Paths to models
model_paths = {
    "Bitcoin": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Bitcoin.h5",
    "Ethereum": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Ethereum.h5",
    "Cardano": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Cardano.h5",
    "Ripple": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Ripple.h5",
    "Solana": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Solana.h5",
    "Litecoin": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Litecoin.h5",
    "Polkadot": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Polkadot.h5",
    "Polygon": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Polygon.h5",
    "Chainlink": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Chainlink.h5",
    "Dogecoin": "/Users/anand/Documents/Capstone Files Dump/Test case 1/models/LSTM_Dogecoin.h5"
}

# Select currency
selected_crypto = st.selectbox("Choose a Cryptocurrency", list(model_paths.keys()))

# Load your FINAL_DATA.csv
df = pd.read_csv("C:/Users/anand/Documents/Capstone Files Dump/Test case 1/separatemodeltraining/FINAL_DATA.csv")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Filter for selected crypto
crypto_df = df[df['Crypto'] == selected_crypto].copy()
crypto_df.drop(columns=["Crypto"], inplace=True)
crypto_df.dropna(inplace=True)

# Features used
features = ['Open', 'High', 'Low', 'Volume', 'VWAP', 'Volatility', 'Price_Change',
            'RSI', 'MACD', 'MA_7', 'MA_14', 'EMA_7', 'EMA_14', 'Rolling_Std_7',
            'Rolling_Std_14', 'Day_of_Week', 'Month', 'Week_of_Year',
            'Close_Lag_1', 'Close_Lag_2', 'Close_Lag_3']

target = 'Close'
sequence_length = 10

# Scale input
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(crypto_df[features])
y_scaled = scaler_y.fit_transform(crypto_df[[target]])

# Create sequence
X_seq = []
for i in range(sequence_length, len(X_scaled)):
    X_seq.append(X_scaled[i-sequence_length:i])
X_seq = np.array(X_seq)

# Last 20% as test
split = int(0.8 * len(X_seq))
X_test = X_seq[split:]
y_test = y_scaled[split + sequence_length:]

# Load model
model = load_model(model_paths[selected_crypto])

# Predict
y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_test_inv = scaler_y.inverse_transform(y_test)

# Predict next 7 days
last_seq = X_scaled[-sequence_length:].reshape(1, sequence_length, len(features))
next_preds = []

for _ in range(7):
    next_price_scaled = model.predict(last_seq)[0]
    next_price = scaler_y.inverse_transform(next_price_scaled.reshape(1, -1))[0][0]
    next_preds.append(next_price)

    # Create next input seq
    new_row = np.append(last_seq[0, -1, :-1], next_price_scaled).reshape(1, -1)
    last_seq = np.append(last_seq[:, 1:, :], new_row.reshape(1, 1, -1), axis=1)

# Create future forecast DataFrame
future_dates = pd.date_range(start=crypto_df['Timestamp'].iloc[-1] + pd.Timedelta(days=1), periods=7)
forecast_df = pd.DataFrame({'Date': future_dates, 'Forecasted Close': next_preds})

# Plot actual vs forecast
st.subheader(f"📊 Forecast for {selected_crypto} (Next 7 Days)")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(crypto_df['Timestamp'].iloc[-100:], crypto_df['Close'].iloc[-100:], label="Actual")
ax.plot(forecast_df['Date'], forecast_df['Forecasted Close'], label="Forecast", linestyle='--', marker='o', color='orange')
ax.set_title(f"{selected_crypto} – Forecast vs Actual (Close Price)")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price (USD)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Display forecast table
st.dataframe(forecast_df.style.format({"Forecasted Close": "${:,.2f}"}))
