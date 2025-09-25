FastAPI Chatbot with Cloudflare Workers AI

This project is a simple backend service built with Python and FastAPI that provides a chat interface to a Large Language Model (LLM) hosted on Cloudflare Workers AI. It maintains conversation history in memory for follow-up questions.

Features
FastAPI Backend: A modern, fast (high-performance) web framework for building APIs.

Cloudflare Workers AI Integratioin: Connects to Cloudflare's serverless AI platform to run powerful LLMs like Llama 3.

Conversation Memory: Remembers the context of the current conversation using a unique conversation_id.

Environment-based Configuration: Securely manages API keys and account IDs using environment variables.

Interactive API Docs: Automatically generates interactive documentation (via Swagger UI) for easy testing.

Project Setup
Prerequisites
Python 3.8+

A Cloudflare account with access to Workers AI.

Your Cloudflare Account ID and a Workers AI API Token.

1. Clone or Download the Project
First, get the project files onto your local machine. This includes main.py, this README.md, and PROMPTS.md.

2. Install Dependencies
Navigate to the project directory in your terminal and install the required Python packages using pip.

pip install "fastapi[all]" requests python-dotenv

fastapi[all]: Installs FastAPI and the uvicorn web server.

requests: Used to make HTTP requests to the Cloudflare API.

python-dotenv: A library to load environment variables from a .env file.

3. Configure Your Credentials
For the application to connect to your Cloudflare account, you must provide your credentials.

Create a new file in the project's root directory named .env.

Open the .env file and add your credentials in the following format:

# .env file
CF_ACCOUNT_ID="your_cloudflare_account_id_here"
CF_API_TOKEN="your_cloudflare_workers_ai_api_token_here"

The application is coded to read this file on startup. Never commit your .env file to a public repository.

Running the Application
Once the setup is complete, you can run the web server.

Open your terminal in the project's root directory.

Execute the following command:

uvicorn main:app --reload

main: The name of the Python file (main.py).

app: The FastAPI object created in main.py (app = FastAPI()).

--reload: Automatically restarts the server whenever you save a change to the code.

The server will start, and you'll see a message indicating it's running on http://127.0.0.1:8000.

How to Test the API
You can interact with your running chatbot in two primary ways.

1. Using the Interactive Docs (Recommended for Beginners)
FastAPI provides a beautiful, interactive testing environment.

With the server running, open your web browser and navigate to http://127.0.0.1:8000/docs.

Click on the /chat endpoint to expand its details.

Click the "Try it out" button.

In the Request body field, provide a JSON object with a conversation_id and your message.

{
  "conversation_id": "test-convo-123",
  "message": "Explain what a neural network is in simple terms."
}

Click the blue "Execute" button to send the request. The API response will appear below.

2. Using curl (Command-Line)
For a more traditional approach, you can use curl in a new terminal window.

curl -X POST "[http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)" \
-H "Content-Type: application/json" \
-d '{
    "conversation_id": "test-convo-123",
    "message": "What is the capital of Canada?"
}'

This will print the JSON response directly to your terminal.