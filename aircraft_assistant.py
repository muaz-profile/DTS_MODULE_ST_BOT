from functools import lru_cache
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

CONTEXT_PATH = Path(__file__).parent / "packages" / "dtsense-rag" / "dtsense_rag" / "data" / "sample.txt"
DEFAULT_MODEL = "llama-3.1-8b-instant"

@lru_cache(maxsize=1)
def load_context() -> str:
    text = CONTEXT_PATH.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("The aircraft cooling reference document is empty.")
    return text

def build_chain(api_key: str, model_name: str = DEFAULT_MODEL):
    if not api_key.strip():
        raise ValueError("A GROQ API key is required.")
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an aircraft cooling-system knowledge assistant.
Answer only from the reference text below. Clearly state when the reference does not contain enough information.
Separate facts from general explanation, avoid safety or certification claims, and reply in the same language as the question.

REFERENCE TEXT:
{context}"""),
        ("human", "{question}"),
    ]).partial(context=load_context())
    model = ChatGroq(groq_api_key=api_key, model=model_name, temperature=0)
    return prompt | model | StrOutputParser()

def answer_question(question: str, api_key: str, model_name: str = DEFAULT_MODEL) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Question must not be empty.")
    return build_chain(api_key, model_name).invoke({"question": question})
