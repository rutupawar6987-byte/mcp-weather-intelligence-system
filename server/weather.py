'''from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """echo a meeag as resources"""
    return f"resourse echo: {message}"


if __name__ == "__main__":
    mcp.run()
'''


'''from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# =========================
# MCP SERVER INITIALIZATION
# =========================
mcp = FastMCP("weather")

# =========================
# API CONFIG
# =========================
NWS_API_BASE = "https://api.weather.gov"  # US alerts only

WEATHER_API_KEY = "83d9b889304340418b0112935261504"    # replace with your key


# =========================
# UTILITY FUNCTION (US ALERTS)
# =========================
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make request to US weather API (alerts)."""
    headers = {
        "User-Agent": "weather-app/1.0",
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


# =========================
# FORMAT ALERT
# =========================
def format_alert(feature: dict) -> str:
    props = feature["properties"]

    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""


# =========================
# TOOL 1: WEATHER ALERTS (US ONLY)
# =========================
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state (e.g. CA, NY)."""

    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


# =========================
# TOOL 2: GLOBAL WEATHER FORECAST (FIXED)
# =========================
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get GLOBAL weather forecast using WeatherAPI."""

    url = (
        f"http://api.weatherapi.com/v1/forecast.json"
        f"?key={WEATHER_API_KEY}&q={latitude},{longitude}&days=3"
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            data = response.json()

            # API error handling
            if "error" in data:
                return data["error"]["message"]

            forecast_days = data["forecast"]["forecastday"]

            result = []
            for day in forecast_days:
                result.append(f"""
📅 Date: {day['date']}
🌡️ Avg Temp: {day['day']['avgtemp_c']} °C
🌥️ Condition: {day['day']['condition']['text']}
💧 Humidity: {day['day']['avghumidity']}%
🌬️ Max Wind: {day['day']['maxwind_kph']} km/h
""")

            return "\n---\n".join(result)

        except Exception as e:
            return f"Error fetching forecast: {str(e)}"


# =========================
# TOOL 3: SIMPLE RESOURCE (FIXED TYPO)
# =========================
@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as MCP resource."""
    return f"resource echo: {message}"


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    mcp.run()'''



from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

mcp = FastMCP("weather")


# =========================
# SAFE API CALL
# =========================
async def safe_get(url: str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, timeout=30.0)

            if res.status_code != 200:
                return {"error": f"HTTP {res.status_code}: {res.text}"}

            return res.json()

        except Exception as e:
            return {"error": str(e)}


# =========================
# FORECAST TOOL
# =========================
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:

    query = f"{latitude:.4f},{longitude:.4f}"

    url = (
        f"https://api.weatherapi.com/v1/forecast.json"
        f"?key={WEATHER_API_KEY}&q={query}&days=3"
    )

    data = await safe_get(url)

    if "error" in data:
        return f"❌ Forecast Error: {data['error']}"

    result = []

    for day in data["forecast"]["forecastday"]:
        result.append(f"""
📅 {day['date']}
🌡️ Temp: {day['day']['avgtemp_c']}°C
🌥️ Condition: {day['day']['condition']['text']}
💧 Humidity: {day['day']['avghumidity']}%
🌬️ Wind: {day['day']['maxwind_kph']} km/h
""")

    return "\n---\n".join(result)


# =========================
# ALERT TOOL
# =========================
@mcp.tool()
async def get_alerts(latitude: float, longitude: float) -> str:

    query = f"{latitude:.4f},{longitude:.4f}"

    url = (
        f"https://api.weatherapi.com/v1/alerts.json"
        f"?key={WEATHER_API_KEY}&q={query}"
    )

    data = await safe_get(url)

    # SAFE FALLBACK
    if "error" in data:
        return "🟢 No active alerts (or service not available for this region)."

    alerts = data.get("alerts", {}).get("alert", [])

    if not alerts:
        return "🟢 Safe: No active weather alerts for this location."

    result = []

    for a in alerts:
        result.append(f"""
⚠️ Event: {a.get('event')}
📍 Area: {a.get('areas')}
📝 Details: {a.get('desc')}
""")

    return "\n---\n".join(result)


# =========================
# RESOURCE
# =========================
@mcp.resource("echo://{msg}")
def echo(msg: str) -> str:
    return f"echo: {msg}"


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    mcp.run()