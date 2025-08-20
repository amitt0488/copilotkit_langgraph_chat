import os
from typing import Annotated,TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph.message import AnyMessage
from langgraph.graph import START,END,StateGraph
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

def chat_node(state:State)->State:
    synapse_api_key = os.environ.get("SYNAPSE_API_KEY")
    from chat_completion_api_proxy import ChatCompletionProxy
    api_url = os.environ.get(
        "SYNAPSE_CHAT_COMPLETION_API_URL",
        "https://llm.synapse.thalescloud.io/v1/chat/completions",
    )
    model_name = os.environ.get("LLM_MODEL", "gpt-4o")

    # Build plain text messages from state
    user_messages = [
        m for m in state["messages"]
        if getattr(m, "type", "") == "human" or getattr(m, "role", "") == "user"
    ]
    messages_payload = []
    for m in user_messages:
        role = getattr(m, "role", None) or ("user" if getattr(m, "type", "") == "human" else "user")
        content = getattr(m, "content", "")
        messages_payload.append({"role": role, "content": content})

    proxy = ChatCompletionProxy(api_url=api_url, api_key=synapse_api_key, model=model_name)
    state["messages"] = proxy.chat(messages_payload)
    return state
    
graph_builder=StateGraph(State)
graph_builder.add_node("chat_node",chat_node)
graph_builder.add_edge(START,"chat_node")
graph_builder.add_edge("chat_node",END)
graph = graph_builder.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    config={"configurable":{"thread_id":"test"}}
    response = graph.invoke({"messages":[{"role":"user","content":"Hello, how are you?"}]},config=config)
    print(response)





