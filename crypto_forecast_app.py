import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Replace this with your actual prediction logic
def mock_forecast(currency, days):
    dates = pd.date_range(start=pd.Timestamp.today(), periods=days)
    prices = np.random.uniform(low=100, high=5000, size=days)
    return pd.DataFrame({"Date": dates, "Predicted Price": prices})

# List of 10 cryptocurrencies
crypto_list = [
    "Bitcoin (BTC)", "Ethereum (ETH)", "Binance Coin (BNB)", "Ripple (XRP)",
    "Cardano (ADA)", "Solana (SOL)", "Polkadot (DOT)", "Litecoin (LTC)",
    "Avalanche (AVAX)", "Chainlink (LINK)"
]

# Streamlit UI
st.set_page_config(page_title="Crypto Price Forecast", layout="wide")

st.title("📈 Cryptocurrency Price Forecasting Dashboard")

# Sidebar
st.sidebar.header("Configuration")
selected_crypto = st.sidebar.selectbox("Select Cryptocurrency", crypto_list)

forecast_days = st.sidebar.slider("Days to Forecast", min_value=1, max_value=30, value=7)

# Predict button
if st.sidebar.button("Run Forecast"):
    st.subheader(f"Predicted Prices for {selected_crypto} - Next {forecast_days} Days")
    
    # Forecast data
    forecast_df = mock_forecast(selected_crypto, forecast_days)

    # Display as table
    st.dataframe(forecast_df.style.format({"Predicted Price": "${:,.2f}"}), use_container_width=True)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(forecast_df["Date"], forecast_df["Predicted Price"], marker='o', linestyle='-')
    ax.set_title(f"{selected_crypto} Price Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Predicted Price (USD)")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("👈 Choose your options from the sidebar and click **Run Forecast**.")

# Footer
st.markdown("---")
st.markdown("Made with using Streamlit")
