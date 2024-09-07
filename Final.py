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

# Initialize session state to save the conversation history and context
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'context' not in st.session_state:
    st.session_state.context = ""

# Display the conversation history first with spacing between prompts
for i, entry in enumerate(st.session_state.conversation):
    if i > 0:
        st.markdown("<hr style='margin: 24px 0;'>", unsafe_allow_html=True)  # Add a horizontal line with margin

    st.write("**You:**", entry["prompt"])
    st.write("**Lawrence Bot:**", entry["response"])

# Input prompt and submit button below the conversation
st.markdown("<hr style='margin: 24px 0;'>", unsafe_allow_html=True)  # Add a separator before the input box
prompt_input = st.text_area("Enter your prompt:")

submit_button = st.button("Submit")

if submit_button and prompt_input:
    try:
        # Append the current prompt to the context
        st.session_state.context += " " + prompt_input
        
        # Generate response from LLM with context
        response = llm.invoke(st.session_state.context)
        st.session_state.conversation.append({"prompt": prompt_input, "response": response.content})
        
        # Refresh the page to show updated conversation and input box below
        st.experimental_rerun()

    except Exception as e:
        st.error(f"An Error Occurred: {e}")

# If you want to clear the conversation history and context
if st.button("Clear Conversation"):
    st.session_state.conversation = []
    st.session_state.context = ""
    st.experimental_rerun()
