def main():
    st.title("🏡 Property Valuation & Rent Insights Dashboard")

    address = st.text_input("Enter Full Property Address", "Your address here")

    if st.button("Analyze Property"):
        if not address.strip() or address == "Your address here":
            st.warning("⚠️ Please enter a valid address.")
            return

        st.info(f"📡 Fetching data for **{address}**...")

        value_data = fetch_property_value(address)
        rent_data = fetch_rent_estimate(address)

        st.markdown("---")

        # Display in Tabs
        tab1, tab2, tab3 = st.tabs(["🏠 Current Valuation", "📊 Trends Over 10 Years", "📄 Raw API Responses"])

        with tab1:
            if value_data:
                price = value_data.get("price")
                price_low = value_data.get("priceRangeLow")
                price_high = value_data.get("priceRangeHigh")

                st.subheader("🏷️ Property Value")
                st.metric("Current Estimated Value", f"${price:,.0f}")
                st.caption(f"Value Range: ${price_low:,.0f} - ${price_high:,.0f}")

            if rent_data:
                rent = rent_data.get("rent")
                rent_low = rent_data.get("rentRangeLow")
                rent_high = rent_data.get("rentRangeHigh")

                st.subheader("💰 Expected Monthly Rent")
                st.metric("Current Rent Estimate", f"${rent:,.0f} /mo")
                st.caption(f"Rent Range: ${rent_low:,.0f} - ${rent_high:,.0f}")

        with tab2:
            st.subheader("📈 Historical Trends (Simulated)")
            if value_data and rent_data:
                value_trend = generate_trend(price, growth_rate=0.035)
                rent_trend = generate_trend(rent, growth_rate=0.025)

                st.markdown("#### Home Value Over Last 10 Years")
                st.line_chart(value_trend.set_index('Year'))

                st.markdown("#### Rent Estimate Over Last 10 Years")


if __name__ == "__main__":
    main()
