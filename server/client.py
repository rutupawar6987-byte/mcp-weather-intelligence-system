'''import asyncio
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient


async def main():
    load_dotenv()

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY") )
    

    # ✅ SIMPLE CLIENT (no experimental modules)
    client = MCPClient()

    # ✅ Attach server in runtime mode
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=5
    )

    print("🌦️ MCP Weather Agent Started\n")

    while True:
        query = input("👉 Ask: ")

        if query.lower() in ["exit", "quit"]:
            break

        try:
            response = await agent.run(query)
            print("\n🤖", response, "\n")
        except Exception as e:
            print("❌ Error:", e)


if __name__ == "__main__":
    asyncio.run(main()) '''


from server.weather import get_forecast, get_alerts

async def fetch_forecast(lat, lon):
    return await get_forecast(lat, lon)

async def fetch_alerts(lat, lon):
    return await get_alerts(lat, lon)