from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
import os


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

memory = MemorySaver()


class ChatState(TypedDict):
    messages: Annotated[list[AIMessage], add_messages]


def chatbot(state: ChatState):
    return {"messages": [llm.invoke(state["messages"])]}


graph = StateGraph(ChatState)

graph.add_node("chatbot", chatbot)

graph.add_edge("chatbot", END)

graph.set_entry_point("chatbot")

app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": 1}}


while True:
    user_input = input("User: ")
    if user_input in ["exit", "end"]:
        break
    else:
        result = app.invoke(
            {"messages": [HumanMessage(content=user_input)]}, config=config
        )

        print("AI: " + result["messages"][-1].content)
