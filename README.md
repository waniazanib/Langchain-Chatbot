# Llama 3 ChatBot

A conversational chatbot interface built using Streamlit and LangChain, integrated with Meta's `meta-llama/Meta-Llama-3-8B-Instruct` model hosted on the Hugging Face Serverless Inference API.

This project is configured to require user-provided API keys on deployment, allowing users to interact with Llama 3 using their own Hugging Face accounts.

## Features

- **Llama 3 Integration**: Uses the `meta-llama/Meta-Llama-3-8B-Instruct` model.
- **Modern UI**: Built using Streamlit's native chat elements (`st.chat_message` and `st.chat_input`) for a responsive chat interface.
- **Memory Context**: Keeps track of active conversational history to allow natural, multi-turn dialogue.
- **Robust Wrapper Implementation**: Employs LangChain's `ChatHuggingFace` wrapper to properly format inputs for the Llama 3 conversational template.
- **Secure Key Management**: Allows users to input their own Hugging Face Token directly into the sidebar without exposing host credentials.

## Project Structure

```text
├── app.py                 # Streamlit web application
├── requirements.txt       # Project dependencies
├── .env.example           # Reference for local environment variables
└── .gitignore             # Git ignore configuration
```

## Setup Instructions
**Prerequisites**
- Make sure you have Python 3.9 or higher installed.
- Clone the repository: git clone https://github.com/waniazanib/Langchain-Chatbot.git
- Set up a virtual environment:

  ```bash
  #Windows
  python -m venv venv
  .\venv\Scripts\activate

  #macOS/Linux
  python3 -m venv venv
  source venv/bin/activate
  ```
    
**Install dependencies:**
```bash
pip install -r requirements.txt
```
**Environment Configuration:**
Copy .env.example to .env and paste your Hugging Face token:
```bash
cp .env.example .env
```
Note: If you leave the .env file empty or omit it, you can still paste your Hugging Face token directly into the running web interface sidebar.

## Running the Project
**Running the Web App (Streamlit)**

To start the application locally:
```bash
streamlit run app.py
```
Open the local URL displayed in the terminal (usually http://localhost:8501) in your web browser.

