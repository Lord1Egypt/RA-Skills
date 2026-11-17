"""
memory.py — BlueColumn Voice Memory Helpers
Manages pre-call recall, post-call storage, and mid-call notes.
Uses name-based queries for better recall (phone numbers are weak semantic signals).
"""
import os
import json
import logging
import httpx
from typing import Optional
from pathlib import Path

logger = logging.getLogger('uvicorn.memory')

# Config from environment
BLUECOLUMN_API_KEY = os.getenv("BLUECOLUMN_API_KEY", "")
BLUECOLUMN_BASE = os.getenv("BLUECOLUMN_BASE", "https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1")

# Contacts file path (for name lookup)
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTACTS_FILE = os.path.join(SKILL_DIR, "contacts.json")


def _lookup_caller_name(caller_number: str) -> str:
    """Look up the caller's name from contacts.json for better semantic queries."""
    try:
        with open(CONTACTS_FILE) as f:
            contacts = json.load(f)
        info = contacts.get(caller_number, {})
        return info.get("name", "")
    except (FileNotFoundError, json.JSONDecodeError):
        return ""


def _build_recall_query(caller_number: str) -> str:
    """
    Build an effective recall query using name if available.
    BlueColumn semantic search works much better with names than phone numbers.
    """
    name = _lookup_caller_name(caller_number)
    if name:
        return f"past conversations with {name} ({caller_number}) history context preferences"
    return f"caller {caller_number} past conversations history context preferences"


async def recall_caller(caller_number: str, timeout: float = 2.0) -> str:
    """
    Recall everything BlueColumn knows about a caller.
    Called BEFORE the agent speaks — injected into the system prompt.
    
    Uses name-based queries for better recall. Falls back to phone number.
    
    Args:
        caller_number: Phone number in E.164 format (e.g., +12065550123)
        timeout: Max seconds to wait (default 2.0s — voice needs speed)
    
    Returns:
        Synthesized answer string, or empty string if no memory / timeout
    """
    if not BLUECOLUMN_API_KEY:
        logger.warning("No BlueColumn API key configured — skipping recall")
        return ""
    
    if not caller_number:
        return ""
    
    query = _build_recall_query(caller_number)
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                f"{BLUECOLUMN_BASE}/agent-recall",
                headers={
                    "Authorization": f"Bearer {BLUECOLUMN_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"q": query}
            )
            
            if resp.status_code == 200:
                data = resp.json()
                answer = data.get("answer", "")
                sources = data.get("sources", [])
                
                if answer and sources:
                    logger.info(f"✅ BlueColumn recall: {len(answer)} chars from {len(sources)} sources for {caller_number}")
                elif answer:
                    logger.info(f"ℹ️ BlueColumn recall: answer only (no sources) for {caller_number}")
                else:
                    logger.info(f"❓ No BlueColumn memory found for {caller_number}")
                
                return answer[:3000]  # Cap at 3000 chars for prompt injection
            else:
                logger.warning(f"BlueColumn recall status {resp.status_code} for {caller_number}: {resp.text[:200]}")
                return ""
                
    except httpx.TimeoutException:
        logger.warning(f"BlueColumn recall timed out ({timeout}s) for {caller_number}")
        return ""
    except Exception as e:
        logger.warning(f"BlueColumn recall error for {caller_number}: {type(e).__name__}: {e}")
        return ""


async def store_conversation(transcript: str, caller_number: str, title: Optional[str] = None) -> Optional[str]:
    """
    Store a call transcript/conversation into BlueColumn memory.
    Called AFTER the call ends (fire-and-forget).
    
    Args:
        transcript: The conversation text
        caller_number: Phone number in E.164 format
        title: Optional title (auto-generated if not provided)
    
    Returns:
        session_id if stored successfully, None otherwise
    """
    if not BLUECOLUMN_API_KEY:
        logger.warning("No BlueColumn API key configured — skipping memory storage")
        return None
    
    if not transcript or len(transcript.strip()) < 10:
        logger.warning("Transcript too short to store")
        return None
    
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    name = _lookup_caller_name(caller_number)
    caller_label = f"{name} ({caller_number})" if name else caller_number
    effective_title = title or f"Voice call - {caller_label} - {today}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{BLUECOLUMN_BASE}/agent-remember",
                headers={
                    "Authorization": f"Bearer {BLUECOLUMN_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "text": transcript[:5000],  # Cap at 5000 chars
                    "title": effective_title[:200]
                }
            )
            
            if resp.status_code == 200:
                data = resp.json()
                session_id = data.get("session_id")
                summary = data.get("summary", "")
                action_items = data.get("action_items", [])
                logger.info(f"✅ Stored {caller_number} call in BlueColumn: session={session_id}, actions={len(action_items)}")
                return session_id
            else:
                logger.warning(f"BlueColumn store failed: {resp.status_code} — {resp.text[:200]}")
                return None
                
    except Exception as e:
        logger.warning(f"BlueColumn store error: {type(e).__name__}: {e}")
        return None


async def save_note(text: str, tags: list = None) -> bool:
    """
    Save a quick agent observation to BlueColumn.
    Called mid-call when the agent learns something about the caller.
    """
    if not BLUECOLUMN_API_KEY:
        return False
    
    if not text or len(text.strip()) < 5:
        return False
    
    payload = {"text": text[:500]}
    if tags:
        payload["tags"] = tags[:10]
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{BLUECOLUMN_BASE}/agent-note",
                headers={
                    "Authorization": f"Bearer {BLUECOLUMN_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            return resp.status_code == 200
    except Exception as e:
        logger.warning(f"BlueColumn note error: {e}")
        return False


async def recall_query(query: str, top_k: int = 5) -> dict:
    """
    General-purpose BlueColumn recall query.
    Used by the agent mid-conversation to look up specific facts.
    
    Returns full response dict with answer + sources.
    """
    if not BLUECOLUMN_API_KEY:
        return {"answer": "BlueColumn not configured", "sources": []}
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{BLUECOLUMN_BASE}/agent-recall",
                headers={
                    "Authorization": f"Bearer {BLUECOLUMN_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"q": query[:500]}
            )
            
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"answer": f"Recall failed ({resp.status_code})", "sources": []}
                
    except Exception as e:
        return {"answer": f"Recall error: {e}", "sources": []}
