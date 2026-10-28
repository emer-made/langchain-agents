from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver


load_dotenv(override=True)


# Need to add dependency on langchain-anthropic.
MODEL = "anthropic:claude-sonnet-5"


@tool
def get_weather(city: str) -> str:
    """This tool returns the weather in a given city, e.g. rome."""
    return "Cloudy with rain showers in the afternoon."


# Call without memory.
# agent = create_agent(
#     model=MODEL,
#     tools=[get_weather],
#     system_prompt="You are a travel assistant. Use your tools to answer questions about cities."
# )
# agent.invoke({"messages": [{"role": "user", "content": "I am planning a trip to Paris."}]})
# no_mem = agent.invoke({"messages": [{"role": "user", "content": "What is the weather in my destination?"}]})
# print(no_mem["messages"][-1].content)


# Call with memory
config = {"configurable": {"thread_id": "trip-planning"}}
mem_agent = create_agent(
    model=MODEL,
    tools=[get_weather],
    system_prompt="You are a travel assistant. Use your tools to answer questions about cities.",
    checkpointer=MemorySaver()
)
response = mem_agent.invoke({"messages": [{"role": "user", "content": "I am planning a trip to Paris."}]}, config=config)
response = mem_agent.invoke({"messages": [{"role": "user", "content": "What is the weather in my destination?"}]}, config)
print(response["messages"][-1].content)