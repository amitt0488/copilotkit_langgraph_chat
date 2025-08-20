import os
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph.message import AnyMessage
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def chat_node(state: State) -> State:
    synapse_api_key = os.environ.get("SYNAPSE_API_KEY")
    from chat_completion_api_proxy import ChatCompletionProxy
    api_url = os.environ.get(
        "SYNAPSE_CHAT_COMPLETION_API_URL",
        "https://llm.synapse.thalescloud.io/v1/chat/completions",
    )
    model_name = os.environ.get("LLM_MODEL", "gpt-4o")

    # Normalize all messages (user/assistant/system) into role/content pairs
    messages_payload = []
    for m in state.get("messages", []):
        if isinstance(m, dict):
            msg_type = m.get("type")
            role = m.get("role")
            if not role:
                if msg_type == "human":
                    role = "user"
                elif msg_type == "ai":
                    role = "assistant"
                elif msg_type == "system":
                    role = "system"
                else:
                    role = "user"
            content = m.get("content", "")
        else:
            msg_type = getattr(m, "type", None)
            role = getattr(m, "role", None)
            if not role:
                if msg_type == "human":
                    role = "user"
                elif msg_type == "ai":
                    role = "assistant"
                elif msg_type == "system":
                    role = "system"
                else:
                    role = "user"
            content = getattr(m, "content", "")

        if content:
            messages_payload.append({"role": role, "content": content})

    proxy = ChatCompletionProxy(api_url=api_url, api_key=synapse_api_key, model=model_name)
    assistant_content = proxy.chat(messages_payload)

    # Append the assistant response; LangGraph will merge via add_messages
    return {
        "messages": [
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
graph_builder = StateGraph(State)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)
graph = graph_builder.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "test"}}
    response = graph.invoke({"messages": [{"role": "user", "content": "Hello, how are you?"}]}, config=config)
    print(response)





