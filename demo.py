from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools import execute_query,get_schema,list_tables

model = ChatOllama(model='qwen3:8b')

tools = [execute_query,get_schema,list_tables]
# response = model.invoke("whats apache spark in 20 words")

# print(response.text)

agent = create_agent(
    model=model,
    system_prompt="You are a PostgreSQL expert. Use the available tools when needed.",
    tools=tools,
)


if __name__ == "__main__":
    user_input = input("ask question: ")
    response = agent.invoke(input={"messages": [user_input]})
    print(response["messages"][-1].text)
