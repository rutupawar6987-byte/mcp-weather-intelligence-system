# 🌦️ MCP Weather Server

An MCP (Model Context Protocol) based weather server built using Python and FastMCP.
This project exposes real-time weather alerts and forecasts as AI-callable tools, enabling dynamic tool usage by AI systems like Cursor.

---

## 🚀 Features

* 🌍 Get real-time weather alerts by US state
* 📍 Fetch weather forecasts using latitude & longitude
* 🤖 AI tool integration using MCP
* ⚡ Asynchronous API handling with httpx

---

## 🛠️ Tech Stack

* Python
* FastMCP
* httpx
* MCP (Model Context Protocol)

---

## 📂 Project Structure

```
mcp_crashcourse/
│── server/
│   └── weather.py
│── .gitignore
│── pyproject.toml
│── README.md
```

---

## ⚙️ How to Run

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/mcp-weather-server.git
cd mcp-weather-server
```

### 2️⃣ Install dependencies

```
pip install httpx mcp
```

### 3️⃣ Run the server

```
python server/weather.py
```

---

## 🔗 MCP Tools

### 📌 get_alerts(state)

* Input: US state code (e.g., CA, NY)
* Output: Active weather alerts

---

### 📌 get_forecast(latitude, longitude)

* Input: Coordinates
* Output: 5-period weather forecast

---

## 🔄 How it Works

```
User → Cursor (Client) → MCP Server → Weather API → Response
```

---

## 📌 Use Case

This project demonstrates how AI can dynamically interact with external tools using MCP instead of hardcoded logic.

---

## 🎯 Future Improvements

* 🌏 Add support for global weather APIs
* 📊 Add visualization (charts/graphs)
* 🔐 Add API key security

---

## 👩‍💻 Author

**Rutuja Pawar**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
