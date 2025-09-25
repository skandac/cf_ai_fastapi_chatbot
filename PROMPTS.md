AI Prompts Used in Project Development
This file documents the key prompts that were used to guide the AI-assisted coding process for the FastAPI Chatbot application.

Prompt 1: Initial Code Generation and Error Diagnosis
User Query:

i am running a fast api python app and i get this error when i run

{
"detail": "Not Found"
}

This was followed by the user providing their initial Python script.

AI Action:

Diagnosed the "Not Found" error as a mismatch between the expected POST request and the user likely trying to access the URL with a GET request (e.g., in a browser).

Corrected the Cloudflare API payload structure from {"input": context} to the correct {"messages": [...]} format required by instruct models.

Generated a more robust and well-documented main.py file with proper error handling.

Generated an initial README.md file with clear instructions on how to run the server and test the endpoint correctly using curl to avoid the "Not Found" error.

Prompt 2: Request for Complex Test Case
User Query:

give me some complex thing to ask using interactive API docs

AI Action:

Provided a multi-part prompt designed to test the AI's role-playing, analogy-making, and creative abilities.

Provided a follow-up prompt to test the application's conversation memory feature.

Prompt 3: Request for Formal Documentation
User Query:

include a README.md file with project documentation and clear running instructions to try out components (either locally or via deployed link). AI-assisted coding is encouraged, but you must include AI prompts used in PROMPTS.md

AI Action:

Created this PROMPTS.md file to log the development history.

Generated a more formal and comprehensive README.md file, structuring it with sections for features, setup, configuration, and testing, suitable for a project repository.