from dotenv import load_dotenv
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchain_core.tools import tool


load_dotenv(override=True)


# Need to add dependency on langchain-anthropic.
MODEL = "anthropic:claude-sonnet-5"


class CityReport(BaseModel):
    city: str = Field(description="The name of the city.")
    population: str = Field(description="The population of the city.")
    weather: str = Field(description="The weather in the city.")


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
    system_prompt="You are an expert travel assistant. Use your tools to answer questions about cities in a structured way.",
    tools=[get_weather, get_population],
    response_format=CityReport
)
result = agent.invoke({"messages": [{"role": "user", "content": "Give me a report on London."}]})
report = result["structured_response"]
print(report)
print("Just the weather:", report.weather)