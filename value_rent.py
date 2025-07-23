import streamlit as st
import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Configuration
API_KEY = "bc87829e1d2d4ee68dcbb775c90b598a"
VALUE_URL = "https://api.rentcast.io/v1/avm/value"
RENT_URL = "https://api.rentcast.io/v1/avm/rent/long-term"

headers = {
    "X-Api-Key": API_KEY
}

def fetch_property_value(address):
    params = {"address": address}
    response = requests.get(VALUE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Value API Error {response.status_code}: {response.text}")
        return None

def fetch_rent_estimate(address):
    params = {"address": address}
    response = requests.get(RENT_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Rent API Error {response.status_code}: {response.text}")
        return None

def generate_trend(current_value, growth_rate=0.03, years=10):
    dates = [datetime.now() - timedelta(days=365 * i) for i in reversed(range(years))]
    values = [current_value / ((1 + growth_rate) ** (years - i - 1)) for i in range(years)]
    return pd.DataFrame({'Year': [d.year for d in dates], 'Value': values})

def main():
    st.title("🏡 Property Valuation & Rent Insights Dashboard")

    address = st.text_input("Enter Full Property Address", "3821 Hargis St, Austin, TX 78723")

    if address.strip() and address != "Your address here":
        st.info(f"📡 Fetching data for **{address}**...")

        value_data = fetch_property_value(address)
        rent_data = fetch_rent_estimate(address)

        if value_data is None or rent_data is None:
            st.error("Failed to retrieve property or rent data.")
            return

        st.markdown("---")

        tab1, tab2, tab3 = st.tabs(["🏠 Current Valuation", "📊 Trends Over 10 Years", "📄 Raw API Responses"])

        with tab1:
            price = value_data.get("price")
            price_low = value_data.get("priceRangeLow")
            price_high = value_data.get("priceRangeHigh")

            st.subheader("🏷️ Property Value")
            st.metric("Current Estimated Value", f"${price:,.0f}")
            st.caption(f"Value Range: ${price_low:,.0f} - ${price_high:,.0f}")

            rent = rent_data.get("rent")
            rent_low = rent_data.get("rentRangeLow")
            rent_high = rent_data.get("rentRangeHigh")

            st.subheader("💰 Expected Monthly Rent")
            st.metric("Current Rent Estimate", f"${rent:,.0f} /mo")
            st.caption(f"Rent Range: ${rent_low:,.0f} - ${rent_high:,.0f}")

        with tab2:
            st.subheader("📈 Historical Trends (Simulated)")
            value_trend = generate_trend(price, growth_rate=0.035)
            rent_trend = generate_trend(rent, growth_rate=0.025)

            st.markdown("#### Home Value Over Last 10 Years")
            st.line_chart(value_trend.set_index('Year'))

            st.markdown("#### Rent Estimate Over Last 10 Years")
            st.line_chart(rent_trend.set_index('Year'))

            st.caption("Note: Historical trends are modeled based on assumed average appreciation rates.")

        with tab3:
            st.subheader("📄 Raw API Responses")
            st.markdown("**Property Value API Response:**")
            st.json(value_data)

            st.markdown("**Rent Estimate API Response:**")
            st.json(rent_data)

    else:
        st.warning("⚠️ Please enter a valid address to get started.")

def health_check():
    st.write("ok")

if __name__ == "__main__":
    selected_value = st.query_params.get("key", "default")
    if "healthz" in query_params:
        health_check()
    else:
        main()
