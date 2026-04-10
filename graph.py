from langgraph.graph import StateGraph
from llm_utils import detect_intent, model
from rag import generate_rag_response
from typing import TypedDict

class AgentState(TypedDict, total=False):
    user_input: str
    history: str
    intent: str
    response: str
    vectorstore: object
    model: object

builder = StateGraph(AgentState)

#adding the nodes
def detect_intent_node(state):
    user_input = state.get("user_input", "")
    history = state.get("history", "")

    intent = detect_intent(user_input,history)

    return {**state, "intent": intent}

def handle_greeting(state):
    return {**state, "response": "Hey! How can I help you?"}

def handle_inquiry(state):
    response = generate_rag_response(
        state['user_input'],
        state['vectorstore'],
        state['model']
    )
    return {**state, 'response': response}

def handle_high_intent(state):
    return {**state, 'response':"Let's get your details! "}

def handle_irrelevant(state):
    return {**state, 'response': 'Got it.'}

#adding nodes to the graph
builder.add_node("intent", detect_intent_node)
builder.add_node("greeting", handle_greeting)
builder.add_node("inquiry", handle_inquiry)
builder.add_node("high_intent", handle_high_intent)
builder.add_node("irrelevant", handle_irrelevant)

#adding routing logic
def route_intent(state):
    return state['intent']

builder.add_conditional_edges(
    'intent',
    route_intent,
    {
        'greeting': 'greeting',
        'inquiry': 'inquiry',
        'high_intent':'high_intent',
        'irrelevant':'irrelevant'
    }
)

#setting entry and end

builder.set_entry_point('intent')
builder.set_finish_point('greeting')
builder.set_finish_point('inquiry')
builder.set_finish_point('high_intent')
builder.set_finish_point('irrelevant')

graph = builder.compile()

