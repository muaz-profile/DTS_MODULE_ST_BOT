# Aircraft Cooling Knowledge Assistant

A document-grounded engineering knowledge assistant that turns a technical reference on aircraft cooling systems into concise, traceable answers. The project provides both an interactive Streamlit interface and a FastAPI endpoint.

## Why this project matters

Engineering information is useful only when people can retrieve and understand it consistently. This project demonstrates a small digital workflow that connects a controlled source document with a user-facing application while explicitly limiting answers to the available source.

## Features

- answers questions about engine, cabin, avionics and fuel cooling concepts;
- grounds every answer in the included reference document;
- states when the available information is insufficient;
- supports German, English and other question languages through the model;
- exposes a Streamlit interface and a typed FastAPI endpoint;
- keeps credentials outside the repository;
- includes health checks, input validation and error handling.

## Architecture

```text
Reference document -> Prompt template -> Groq-hosted language model -> Streamlit UI / FastAPI response
```

This is intentionally described as a **document-grounded assistant**, not a full retrieval-augmented generation system: the current demonstration uses one controlled source document rather than a vector search pipeline.

## Installation

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `GROQ_API_KEY` in `.env` or enter it directly in the Streamlit sidebar.

### Streamlit

```bash
streamlit run app_st.py
```

### FastAPI

```bash
uvicorn app.server:app --reload
```

Open `http://localhost:8000/docs` for the interactive API documentation.

### Docker

```bash
docker build -t aircraft-cooling-assistant .
docker run --env-file .env -p 8000:8000 aircraft-cooling-assistant
```

## Limitations

The included reference is a general educational overview, not controlled OEM data or approved maintenance and certification documentation. The application must not be used for operational aircraft decisions.

## Acknowledgement

Initially developed during a DTSense FastAPI/LangChain learning module and subsequently restructured, completed and documented by Muhammad Aziz.
