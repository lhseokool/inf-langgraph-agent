from dotenv import load_dotenv
import streamlit as st
from trading_graph import graph 
from typing import Callable, TypeVar
import inspect

from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from streamlit.delta_generator import DeltaGenerator

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler


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



# Define a function to wrap and add context to Streamlit's integration with LangGraph
def get_streamlit_cb(parent_container: DeltaGenerator) -> BaseCallbackHandler:
    """
    Creates a Streamlit callback handler that integrates fully with any LangChain ChatLLM integration,
    updating the provided Streamlit container with outputs such as tokens, model responses,
    and intermediate steps. This function ensures that all callback methods run within
    the Streamlit execution context, fixing the NoSessionContext() error commonly encountered
    in Streamlit callbacks.

    Args:
        parent_container (DeltaGenerator): The Streamlit container where the text will be rendered
                                           during the LLM interaction.
    Returns:
        BaseCallbackHandler: An instance of StreamlitCallbackHandler configured for full integration
                             with ChatLLM, enabling dynamic updates in the Streamlit app.
    """

    # Define a type variable for generic type hinting in the decorator, ensuring the original
    # function and wrapped function maintain the same return type.
    fn_return_type = TypeVar('fn_return_type')

    # Decorator function to add Streamlit's execution context to a function
    def add_streamlit_context(fn: Callable[..., fn_return_type]) -> Callable[..., fn_return_type]:
        """
        Decorator to ensure that the decorated function runs within the Streamlit execution context.
        This is necessary for interacting with Streamlit components from within callback functions
        and prevents the NoSessionContext() error by adding the correct session context.

        Args:
            fn (Callable[..., fn_return_type]): The function to be decorated, typically a callback method.
        Returns:
            Callable[..., fn_return_type]: The decorated function that includes the Streamlit context setup.
        """
        # Retrieve the current Streamlit script execution context.
        # This context holds session information necessary for Streamlit operations.
        ctx = get_script_run_ctx()

        def wrapper(*args, **kwargs) -> fn_return_type:
            """
            Wrapper function that adds the Streamlit context and then calls the original function.
            If the Streamlit context is not set, it can lead to NoSessionContext() errors, which this
            wrapper resolves by ensuring that the correct context is used when the function runs.

            Args:
                *args: Positional arguments to pass to the original function.
                **kwargs: Keyword arguments to pass to the original function.
            Returns:
                fn_return_type: The result from the original function.
            """
            # Add the previously captured Streamlit context to the current execution.
            # This step fixes NoSessionContext() errors by ensuring that Streamlit knows which session
            # is executing the code, allowing it to properly manage session state and updates.
            add_script_run_ctx(ctx=ctx)
            return fn(*args, **kwargs)  # Call the original function with its arguments

        return wrapper

    # Create an instance of Streamlit's StreamlitCallbackHandler with the provided Streamlit container
    st_cb = StreamlitCallbackHandler(parent_container)

    # Iterate over all methods of the StreamlitCallbackHandler instance
    for method_name, method_func in inspect.getmembers(st_cb, predicate=inspect.ismethod):
        if method_name.startswith('on_'):  # Identify callback methods that respond to LLM events
            # Wrap each callback method with the Streamlit context setup to prevent session errors
            setattr(st_cb, method_name,
                    add_streamlit_context(method_func))  # Replace the method with the wrapped version

    # Return the fully configured StreamlitCallbackHandler instance, now context-aware and integrated with any ChatLLM
    return st_cb

# Function to invoke the compiled graph externally
def invoke_our_graph(st_messages, callables):
    config = {
        'configurable': {
            'thread_id': '1234'
        },
        "callbacks": callables,
    }
    # Ensure the callables parameter is a list as you can have multiple callbacks
    if not isinstance(callables, list):
        raise TypeError("callables must be a list")
    # Invoke the graph with the current messages and callback configuration
    return graph.invoke({"messages": st_messages}, config=config)

if user_input:
    st.session_state.message_list.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    # Process the AI's response and handles graph events using the callback mechanism
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()  # Placeholder for visually updating AI's response after events end
        # create a new placeholder for streaming messages and other events, and give it context
        st_callback = get_streamlit_cb(st.empty())
        response = invoke_our_graph(st.session_state.message_list, [st_callback])
        last_msg = response["messages"][-1].content
        st.session_state.message_list.append({"role": "assistant", "content":last_msg})  # Add that last message to the st_message_state
        msg_placeholder.write(last_msg) # visually refresh the complete response after the callback container
    