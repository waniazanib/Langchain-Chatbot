import streamlit as st
import os
from dotenv import load_dotenv

# Import LangChain components
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

# Load environment variables from .env
load_dotenv()

# Page configuration
st.set_page_config(page_title="Llama 3 ChatBot", page_icon="🤖", layout="wide")
st.title("🤖 Llama 3 ChatBot")
st.write("An assistant powered by LangChain and Meta-Llama-3-8B-Instruct.")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("Configuration")

# 1. Model Selection (Locked to Llama 3)
selected_model = "meta-llama/Meta-Llama-3-8B-Instruct"
st.sidebar.text_input("Active Model", value=selected_model, disabled=True)

# 2. Generation Parameters
temperature = st.sidebar.slider("Temperature (Randomness)", min_value=0.1, max_value=1.0, value=0.7, step=0.1)

# 3. API Key Input
env_key = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
api_key = st.sidebar.text_input(
    "Hugging Face Token", 
    value=env_key, 
    type="password",
    placeholder="Paste your HF Read Token here"
)

# 4. Clear Conversation Button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# --- INITIALIZE CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if user_input := st.chat_input("Ask Llama 3 anything..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check for API key
    if not api_key:
        st.warning("Please provide a Hugging Face Token in the sidebar.")
    else:
        try:
            # 1. Initialize the base endpoint
            huggingface_endpoint = HuggingFaceEndpoint(
                repo_id=selected_model,
                temperature=temperature,
                huggingfacehub_api_token=api_key,
            )
            # 2. Wrap it with ChatHuggingFace to support conversational routing
            llm = ChatHuggingFace(llm=huggingface_endpoint)

            # 3. Construct Prompt Template with Memory
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful and polite conversational assistant."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])

            # 4. Convert message history to LangChain message formats
            chain_history = []
            for msg in st.session_state.messages[:-1]:  # exclude the current message
                if msg["role"] == "user":
                    chain_history.append(HumanMessage(content=msg["content"]))
                else:
                    chain_history.append(AIMessage(content=msg["content"]))

            # 5. Create the sequence
            chain = prompt_template | llm | StrOutputParser()

            # 6. Generate and display response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                
                # Invoke the chain to get the full answer
                full_response = chain.invoke({"chat_history": chain_history, "input": user_input})
                response_placeholder.markdown(full_response)
            
            # Save response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"An error occurred while communicating with Hugging Face: {e}")