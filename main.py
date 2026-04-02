from langchain.agents import create_agent
import requests

def get_weather(city: str) -> str:
    """Get real weather for a given city."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url).text

agent = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=[get_weather],
    system_prompt="You are a helpful assistant. Use tools when needed.",
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in Bangalore?"}]}
)

print(response["messages"][-1].content)

