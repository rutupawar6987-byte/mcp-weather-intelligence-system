'''import streamlit as st
import httpx

st.set_page_config(page_title="Weather App", page_icon="🌦️", layout="centered")

st.title("🌦️ Smart Weather App")
st.markdown("Get real-time weather updates instantly")

city = st.text_input("📍 Enter City Name", placeholder="e.g. Pune, Mumbai")

API_KEY = "83d9b889304340418b0112935261504"  # ⚠️ replace with correct key

if st.button("Get Weather"):

    if city:
        with st.spinner("Fetching weather data... ⏳"):
            try:
                url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
                response = httpx.get(url)
                data = response.json()

                # st.write("STATUS CODE:", response.status_code)
                # st.write("RAW RESPONSE:", response.text)

                # ✅ handle error safely
                if response.status_code != 200 or "error" in data:
                    st.error(data.get("error", {}).get("message", "Something went wrong"))
                else:
                    temp = data["current"]["temp_c"]
                    condition = data["current"]["condition"]["text"]
                    humidity = data["current"]["humidity"]
                    wind = data["current"]["wind_kph"]

                    st.success(f"Weather in {city}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("🌡️ Temperature", f"{temp} °C")
                        st.metric("💧 Humidity", f"{humidity}%")

                    with col2:
                        st.metric("🌬️ Wind Speed", f"{wind} km/h")
                        st.metric("☁️ Condition", condition)

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning("⚠️ Please enter a city name")

st.markdown("---")
st.caption("Built using Streamlit + MCP Concept")  '''

import streamlit as st
import asyncio
from geopy.geocoders import Nominatim

from server.client import fetch_forecast, fetch_alerts

st.set_page_config(page_title="MCP Weather AI", page_icon="🌦️")

st.title("🌦️ MCP Weather Intelligence System")
st.markdown("End-to-end AI + MCP + Weather API Project")

geolocator = Nominatim(user_agent="weather-app")


def get_coordinates(city):
    location = geolocator.geocode(city)
    return (location.latitude, location.longitude) if location else (None, None)


city = st.text_input("Enter City (Global Supported)")

if st.button("Get Weather"):

    if not city:
        st.warning("Please enter a city")

    else:
        lat, lon = get_coordinates(city)

        if not lat:
            st.error("City not found")

        else:
            with st.spinner("Fetching MCP Weather Data..."):

                forecast = asyncio.run(fetch_forecast(lat, lon))
                alerts = asyncio.run(fetch_alerts(lat, lon))

            st.subheader("🌤️ Forecast")
            st.text(forecast)

            st.subheader("⚠️ Alerts")
            st.text(alerts)