import streamlit as st
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

# Set up the Streamlit app layout
st.title("Legal Chatbot")
st.write("Ask me any legal question!")

# Initialize session state to hold past chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load LegalBERT or GPT model and tokenizer from Hugging Face
@st.cache_resource
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    return pipeline('question-answering', model=model, tokenizer=tokenizer)

# Function to handle user input and generate response
def get_legal_response(question, context):
    qa_pipeline = load_model("deepset/legal-bert-base-uncased")  # Using LegalBERT
    answer = qa_pipeline({'question': question, 'context': context})
    return answer['answer']

# Example context for the legal chatbot (This can be dynamic, or you can use external data)
context = """
In the US, the legal structure of a Limited Liability Company (LLC) provides liability protection for its owners while allowing the flexibility of a pass-through tax structure.
A sole proprietorship is the simplest and most common structure chosen to start a business, and it's not considered a separate legal entity.
"""

# Chat Interface
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You: ")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    response = get_legal_response(user_input, context)
    st.session_state.chat_history.append({"user": user_input, "bot": response})

# Display Chat History
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.write(f"You: {chat['user']}")
        st.write(f"Bot: {chat['bot']}")
