"""Streamlit chat interface for the Ollama PostgreSQL agent."""

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from demo import agent


st.set_page_config(page_title="PostgreSQL Assistant", page_icon="🗃️")
st.title("PostgreSQL Assistant")
st.caption("Ask questions about your PostgreSQL database.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = "assistant" if isinstance(message, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(message.content)

if prompt := st.chat_input("Ask a question about your database"):
    user_message = HumanMessage(content=prompt)
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = agent.invoke(
                    {"messages": st.session_state.messages}
                )
                # Keep the full LangChain message sequence so follow-up turns
                # retain tool calls and their results in the conversation.
                st.session_state.messages = result["messages"]
                answer = result["messages"][-1].text
                st.markdown(answer)
            except Exception as error:
                st.error(f"The agent could not answer: {error}")
