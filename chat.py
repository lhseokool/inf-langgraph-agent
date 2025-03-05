from dotenv import load_dotenv
import streamlit as st
from trading_graph import graph 


import streamlit as st

# Import your build_graph function from your module
# from your_module import build_graph
st.set_page_config(page_title="LangGraph + Streamlit", page_icon=":robot:")


# Streamlit UI
st.title("Stock Analysis Multi-Agent System")
st.markdown("""
This app uses a multi-agent system to analyze stocks. Enter a ticker symbol and a question about the stock to get a comprehensive analysis.
""")
load_dotenv()

if 'message_list' not in st.session_state:
    st.session_state.message_list = []

for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get user input
user_input = st.chat_input("Enter a stock ticker and question (e.g., 'Should I invest in AAPL?')")
config = {
    'configurable': {
        'thread_id': '1234'
    }
}

if user_input:
    st.session_state.message_list.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    with st.spinner("Generating response..."):
        # Display assistant response with streaming
        with st.chat_message("assistant"):
            try:
                ai_message = graph.invoke(
                    {"messages": [("user", user_input)]}, stream_mode="messages", config=config
                );
                
                ai_message = graph.get_state(config).values['messages'][-1].content
                st.write(ai_message)
            
                st.session_state.message_list.append({"role": "assistant", "content": ai_message})
            
            except Exception as e:
                st.error(f"Error during streaming: {str(e)}")
                st.info("This may be due to API rate limits. Please wait a minute and try again with a simpler query.")


