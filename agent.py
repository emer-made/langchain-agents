from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv(override=True)

# Need to add dependency on langchain-anthropic.
MODEL = "anthropic:claude-sonnet-5"

agent = create_agent(
    model=MODEL,
    system_prompt="You are a helpful assistant that answers questions concisely."
    )

result = agent.invoke({"messages": [{"role": "user", "content": "Describe agent to agent protocol in 2 sentences."}]})
print(result)
print(result["messages"][-1].content)