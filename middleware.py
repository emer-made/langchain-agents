from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain.agents.middleware import wrap_tool_call


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


# Middleware are like guardrails, it runs code at fixed point in the loop, e.g. during tool call or model invocation.
# There are many built in middle ware.


@wrap_tool_call
def log_tool_call(request, handler):
    call = request.tool_call
    print(f"Middleware calling tool {call['name']} with arguments {call['args']}")
    return handler(request)


agent = create_agent(
    model=MODEL,
    system_prompt="You are a helpful travel assistant. Answer questions about cities using your tools.",
    tools=[get_population, get_weather],
    middleware=[log_tool_call]
)
result = agent.invoke({"messages": [{"role": "user", "content": "What is the weather and population of London and Rome."}]})
print(result["messages"][-1].content)