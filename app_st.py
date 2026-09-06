import os

import streamlit as st

from aircraft_assistant import DEFAULT_MODEL, answer_question

st.set_page_config(page_title="Aircraft Cooling Knowledge Assistant", page_icon="✈️")
st.title("Aircraft Cooling Knowledge Assistant")
st.caption("A document-grounded demonstration covering engine, cabin, avionics and fuel cooling concepts.")

with st.sidebar:
    api_key = st.text_input("GROQ API key", value=os.getenv("GROQ_API_KEY", ""), type="password")
    model_name = st.text_input("Groq model", value=os.getenv("GROQ_MODEL", DEFAULT_MODEL))
    st.link_button("Create a Groq API key", "https://console.groq.com/keys")

question = st.text_area("Question", value="How does an aircraft environmental control system cool cabin air?", height=120)

if st.button("Generate grounded answer", type="primary"):
    if not api_key:
        st.warning("Enter a Groq API key in the sidebar.")
    elif not question.strip():
        st.warning("Enter a question.")
    else:
        try:
            with st.spinner("Reading the reference and generating an answer..."):
                st.markdown(answer_question(question, api_key, model_name))
        except Exception as exc:
            st.error(f"Unable to generate an answer: {exc}")

with st.expander("Scope and limitations"):
    st.write("Answers are grounded in one demonstration reference document. This is not approved aircraft maintenance, design or certification data.")
