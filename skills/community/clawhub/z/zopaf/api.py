"""FastAPI backend for the Negotiation Coach web app.

Thin wrapper around coach.py — manages sessions and exposes chat endpoint.
"""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from coach import NegotiationCoach
from session_store import (
    save_session,
    load_session,
    set_unlocked,
    is_unlocked,
)

app = FastAPI(title="Negotiation Coach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateSessionResponse(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    issues_count: int
    elicitations_count: int
    gated: bool = False


class SessionInfo(BaseModel):
    session_id: str
    issues: list[dict]
    learned_weights: dict[str, float]
    message_count: int


@app.post("/sessions", response_model=CreateSessionResponse)
def create_session():
    """Create a new coaching session."""
    session_id = str(uuid.uuid4())[:8]
    coach = NegotiationCoach()
    save_session(session_id, coach)
    return CreateSessionResponse(session_id=session_id)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Send a message to the coach and get a response."""
    coach = load_session(request.session_id)
    if coach is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Reset the premium flag before each chat turn
    coach.used_premium_tool = False
    response = coach.chat(request.message)

    # Paywall disabled — free for launch period
    is_gated = False

    # Save updated state
    save_session(request.session_id, coach)

    return ChatResponse(
        response=response if not is_gated else (
            "I've analyzed your negotiation and have personalized counteroffers ready for you. "
            "Unlock your strategy to see them."
        ),
        issues_count=len(coach.issues),
        elicitations_count=len(coach.elicitation_choices),
        gated=is_gated,
    )


@app.get("/sessions/{session_id}", response_model=SessionInfo)
def get_session(session_id: str):
    """Get session state."""
    coach = load_session(session_id)
    if coach is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionInfo(
        session_id=session_id,
        issues=coach.issues,
        learned_weights=coach.learned_weights,
        message_count=len(coach.messages),
    )


class UnlockRequest(BaseModel):
    session_id: str


@app.post("/unlock")
def unlock_session(request: UnlockRequest):
    """Unlock premium features for a session (called after payment)."""
    set_unlocked(request.session_id)
    return {"status": "unlocked"}


@app.get("/sessions/{session_id}/history")
def get_history(session_id: str):
    """Get chat history for a session (used to restore UI after redirect)."""
    coach = load_session(session_id)
    if coach is None:
        return {"messages": [], "unlocked": is_unlocked(session_id)}
    return {
        "messages": coach.chat_history,
        "unlocked": is_unlocked(session_id),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
