import json
from llm_utils import model
from rag import create_vector_store, generate_rag_response
from graph import graph

#initializing vector score once
vectorstore=create_vector_store()

#loading knowledge base
with open("knowledge.json") as f:
    knowledge = json.load(f)

#Mock lead capture func
def mock_lead_capture(name, email, platform):
    print(f'\nLead captures successfully: {name}, {email}, {platform}')

#Chat Logic
def chat():
    print("AutoStream agent ready! Type 'exit' to quit.\n")
    history = ''

    lead = {
        "name":None,
        "email":None,
        "platform": None
    }
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break
        
        history += f"user: {user_input}\n"

        state = {
            "user_input": user_input,
            "history": history,
            "vectorstore": vectorstore,
            "model": model
        }

        result = graph.invoke(state)
        response = result['response']
        intent = result.get("intent")
        
        #handling high intent leads
        if intent == "high_intent":
            if not lead["name"]:
                lead['name']=input("What is your name? ")
            if not lead['email']:
                lead['email']=input("Your Email? ")
            if not lead['platform']:
                lead['platform']=input("Which platform do you use? ")
            mock_lead_capture(
                lead['name'],
                lead['email'],
                lead['platform']
            )

            lead = {
                "name":None,
                "email":None,
                "platform": None
            }   
            
            continue
        print(f"\n AutoStream: {response}\n")
        history += f"Bot: {response}\n"

if __name__=='__main__':
    chat() 