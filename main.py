import streamlit as st
from langchain_groq import ChatGroq

# Initialize the LLM model
llm = ChatGroq(
    temperature=0, 
    groq_api_key='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', 
    model_name="llama-3.1-70b-versatile"
)

# Streamlit app setup
st.title("Lawrence Bot")

# Initialize session state to save the conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Input prompt
prompt_input = st.text_area("Enter your prompt:")

# Submit button
submit_button = st.button("Submit")

if submit_button and prompt_input:
    try:
        # Generate response from LLM
        response = llm.invoke(prompt_input)
        st.session_state.conversation.append({"prompt": prompt_input, "response": response.content})
        
        # Display the conversation history
        for entry in st.session_state.conversation:
            st.write("**You:**", entry["prompt"])
            st.write("**Lawrence Bot:**", entry["response"])
    except Exception as e:
        st.error(f"An Error Occurred: {e}")

# If you want to clear the conversation history
if st.button("Clear Conversation"):
    st.session_state.conversation = []
