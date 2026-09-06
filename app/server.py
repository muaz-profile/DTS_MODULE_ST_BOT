import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from aircraft_assistant import DEFAULT_MODEL, answer_question

app = FastAPI(title="Aircraft Cooling Knowledge Assistant API", version="1.0.0")

class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2_000)
    model: str = DEFAULT_MODEL

class AnswerResponse(BaseModel):
    answer: str
    grounded_in: str = "aircraft cooling reference document"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/answer", response_model=AnswerResponse)
def answer(request: QuestionRequest):
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=503, detail="GROQ_API_KEY is not configured.")
    try:
        result = answer_question(request.question, api_key, request.model)
        return AnswerResponse(answer=result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Model request failed: {exc}") from exc
