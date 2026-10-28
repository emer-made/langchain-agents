from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool


load_dotenv(override=True)


# Need to add dependency on langchain-anthropic.
MODEL = "anthropic:claude-sonnet-5"


@tool
def get_weather(city: str) -> str:
    """This tool returns the weather in a given city, e.g. rome."""
    return "Cloudy with rain showers in the afternoon."


@tool
def get_population(city: str) -> float:
    """Return the population in a given city in millions, e.g. Rome."""
    return 6.5


agent = create_agent(
    model=MODEL,
    system_prompt="You are a travel assistant. Use your tools to answer questions regarding cities.",
    tools=[get_population, get_weather]
)
response = agent.invoke({"messages": [{"role": "user", "content": "What the weather in Paris and how many is its population."}]})
print(response["messages"][-1].content)
