# AutoStream AI Agent

An AI-powered conversational agent built using LLMs, RAG, and LangGraph.

## Features
- Intent Detection using Gemini API
- RAG (Retrieval-Augmented Generation) using FAISS
- LangGraph-based workflow (state machine)
- Conversational memory
- Lead capture simulation

## Tech Stack
- Python
- LangGraph
- FAISS
- Sentence Transformers
- Google Gemini API
- 
## Architecture Explanation

This project uses LangGraph to design the conversational agent as a state machine, instead of relying on traditional if-else logic. LangGraph was chosen because it enables structured, modular workflows where each step (intent detection, retrieval, response generation) is represented as a node, and transitions are handled through conditional edges. This makes the system scalable, easier to debug, and closer to real-world AI agent architectures.

The agent flow begins with an intent detection node powered by a LLM. Based on the detected intent, the graph routes execution to the appropriate handler node. For inquiries, a RAG pipeline is used, where relevant documents are retrieved using FAISS and sentence embeddings, and then passed to the LLM to generate grounded responses.

State is managed using a shared dictionary (AgentState) that is passed between nodes. It stores key information such as user input, conversation history, detected intent, and generated response. Conversation memory is maintained by appending user and bot messages to a history string, which is included in each LLM call. This ensures context-aware, multi-turn interactions while keeping the system stateless at the model level.

## WhatsApp Deployment (Using Webhooks)

To integrate this agent with WhatsApp, the system can be connected using the WhatsApp Business API (via providers like Twilio or Meta Cloud API). Incoming user messages from WhatsApp are sent to a backend server through a webhook.

The backend extracts the user message and passes it to the LangGraph agent by invoking the graph with the appropriate state (user_input, history, etc.). The agent processes the request (intent detection, RAG or response generation) and returns a response.

This response is then sent back to the WhatsApp API using an outbound API call, which delivers the message to the user in real time.

Additionally, conversation history can be stored using a database (such as PostgreSQL) keyed by the user’s phone number, enabling persistent multi-turn conversations across sessions.

Future improvements could include adding persistent memory using vector databases, implementing user authentication, and deploying the system using Docker for scalability.

## Setup

```bash
git clone https://github.com/Ekam334/autostream-agent.git
cd autostream-ai-agent
pip install -r requirements.txt
```
After cloning the repository, create a .env file inside the repository, and use your own google gemini api key as:
``` bash
GOOGLE_API_KEY=your_api_key_here
```
