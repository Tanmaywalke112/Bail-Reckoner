import streamlit as st
from langchain_groq import ChatGroq
import requests
from bs4 import BeautifulSoup

# Initialize the LLM model
llm = ChatGroq(
    temperature=0, 
    groq_api_key='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', 
    model_name="llama-3.1-70b-versatile"
)

# Streamlit app setup
st.title("Lawrence Legal Bot")

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
prompt_input = st.text_area("Enter your legal query:")

submit_button = st.button("Submit")

def fetch_legal_information(query):
    search_url = f"https://www.indiankanoon.org/search/?formInput={query.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Extracting relevant case summaries or law sections
    case_summaries = soup.find_all('div', class_='result_title')
    relevant_cases = []
    
    for case in case_summaries:
        case_title = case.get_text().strip()
        case_link = "https://www.indiankanoon.org" + case.find('a')['href']
        relevant_cases.append((case_title, case_link))
    
    return relevant_cases

if submit_button and prompt_input:
    try:
        # Create the combined prompt
        combined_prompt = prompt_input + " List of relevant cases and laws in the past"
        
        # Append the current combined prompt to the context
        st.session_state.context += " " + combined_prompt
        
        # Fetch relevant legal information from Indian Kanoon
        legal_info = fetch_legal_information(combined_prompt)
        
        # Generate response from LLM with context and legal information
        response = llm.invoke(st.session_state.context)
        response_text = response.content
        
        # Format and display the fetched legal information
        if legal_info:
            response_text += "\n\n### Relevant Cases and Laws:\n"
            for title, link in legal_info:
                # Properly format the links to avoid issues
                response_text += f"- [{title}]({link})\n"
        else:
            response_text += "\n\nThough Chances of such cases had been minimal in the past past"
        
        st.session_state.conversation.append({"prompt": prompt_input, "response": response_text})
        
        # Refresh the page to show updated conversation and input box below
        st.experimental_rerun()

    except Exception as e:
        st.error(f"An Error Occurred: {e}")

# If you want to clear the conversation history and context
if st.button("Clear Conversation"):
    st.session_state.conversation = []
    st.session_state.context = ""
    st.experimental_rerun()
