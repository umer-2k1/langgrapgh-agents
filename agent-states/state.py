from typing import TypedDict, List, Annotated
from langgraph.graph import END, StateGraph
from IPython.display import display, Image
import operator
import os


class SimpleState(TypedDict):
    count: int
    sum: Annotated[int, operator.add]
    history: Annotated[List[str], operator.concat]


def increment(state: SimpleState) -> SimpleState:
    count = state["count"] + 1
    return {"count": count, "sum": count, "history": [count]}


def should_continue(state):
    if state["count"] < 5:
        return "continue"
    else:
        return "stop"


graph = StateGraph(SimpleState)

graph.add_node("increment", increment)
graph.set_entry_point("increment")
graph.add_conditional_edges(
    "increment", should_continue, {"continue": "increment", "stop": END}
)

graph = graph.compile()

# View
png_data = graph.get_graph().draw_mermaid_png()

# Make sure the diagram directory exists
os.makedirs("diagram", exist_ok=True)
 
image_path = os.path.join("diagram", "graph.png")
 
with open(image_path, "wb") as f:
    f.write(png_data)
 
state = {"count": 0, "sum": 0, "history": []}

result = graph.invoke(state)
print(result)
