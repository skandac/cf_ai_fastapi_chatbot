import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Configuration ---
# Load environment variables. Create a .env file in the same directory
# with your credentials (see README.md).
# Example:
# CF_ACCOUNT_ID="your_account_id_here"
# CF_API_TOKEN="your_api_token_here"

CLOUDFLARE_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CF_API_TOKEN")

# Ensure environment variables are set before starting
if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
    raise RuntimeError(
        "Missing Cloudflare credentials. Please set CF_ACCOUNT_ID and "
        "CF_API_TOKEN environment variables."
    )

# You can swap this with other models available in Workers AI
LLM_MODEL = "@cf/meta/llama-3-8b-instruct"
CLOUDFLARE_API_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}"
    f"/ai/run/{LLM_MODEL}"
)

# --- FastAPI App ---
app = FastAPI(
    title="Cloudflare AI Chatbot",
    description="A simple FastAPI backend to chat with a Cloudflare Workers AI model.",
    version="1.0.0",
)

# In-memory conversation storage.
# In a production environment, you would replace this with a database
# like Redis, PostgreSQL, or Firestore to persist conversations.
conversations = {}

# --- Pydantic Models (Data Validation) ---
class ChatRequest(BaseModel):
    conversation_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    conversation_history: list

# --- API Endpoint ---
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request_body: ChatRequest):
    """
    Receives a message, sends it to Cloudflare's AI,
    and returns the model's response.
    """
    cid = request_body.conversation_id
    user_message = {"role": "user", "content": request_body.message}

    # Initialize conversation history if it's a new conversation
    if cid not in conversations:
        conversations[cid] = []

    # Add the new user message to the history
    conversations[cid].append(user_message)

    # --- Call Cloudflare Workers AI ---
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
    
    # Chat/instruct models expect a list of messages, not a single "input" string.
    payload = {
        "messages": conversations[cid]
    }

    try:
        response = requests.post(CLOUDFLARE_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error calling Cloudflare API: {e}")
        raise HTTPException(status_code=500, detail="Failed to communicate with AI service.")

    # --- Process Response ---
    response_data = response.json()
    
    if not response_data.get("success"):
        errors = response_data.get("errors", [])
        raise HTTPException(status_code=500, detail=f"AI service returned an error: {errors}")

    ai_reply_content = response_data.get("result", {}).get("response", "").strip()

    if not ai_reply_content:
        raise HTTPException(status_code=500, detail="Received an empty response from the AI service.")

    # Save AI's response to the conversation history
    assistant_message = {"role": "assistant", "content": ai_reply_content}
    conversations[cid].append(assistant_message)

    return {
        "reply": ai_reply_content,
        "conversation_history": conversations[cid]
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chatbot API. Send a POST request to /chat to begin."}
