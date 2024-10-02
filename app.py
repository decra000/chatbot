import streamlit as st
import openai

# Set up the Streamlit app layout
st.title("Legal Chatbot")
st.write("Ask me any legal question!")

# Initialize session state to hold past chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get a response from OpenAI's GPT model
def get_legal_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error communicating with OpenAI: {e}")
        return "Sorry, I couldn't get a response."

# Chat Interface
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You: ")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    response = get_legal_response(user_input)
    st.session_state.chat_history.append({"user": user_input, "bot": response})

# Display Chat History
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.write(f"You: {chat['user']}")
        st.write(f"Bot: {chat['bot']}")
