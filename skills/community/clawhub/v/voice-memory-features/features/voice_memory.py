"""
voice_memory.py — Voice Memory Engine (Core)
Feature 1: Voice Memory — automatically remember every conversation.

Shared async client + helpers used by all voice memory features.
Extends the voice-agent-memory bridge (bridge/memory.py) with typed feature modules.
"""
import os
import json
import logging
import httpx
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger("voice_memory")

API_KEY = os.getenv("BLUECOLUMN_API_KEY", "")
BASE = os.getenv("BLUECOLUMN_BASE", "https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1")


def _headers():
    return {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


async def remember(text: str, title: str = None, tags: list = None, timeout: float = 10.0) -> Optional[str]:
    """Store a conversation/memory. Returns session_id. Feature 1 core."""
    if not API_KEY or not text or len(text.strip()) < 5:
        return None
    payload = {"text": text[:8000]}
    if title:
        payload["title"] = title[:200]
    if tags:
        payload["tags"] = tags[:10]
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(f"{BASE}/agent-remember", headers=_headers(), json=payload)
            if r.status_code == 200:
                data = r.json()
                logger.info("Stored session=%s title=%s", data.get("session_id"), title)
                return data.get("session_id")
            logger.warning("remember failed %s: %s", r.status_code, r.text[:200])
    except Exception as e:
        logger.warning("remember error: %s", e)
    return None


async def recall(q: str, timeout: float = 5.0) -> dict:
    """Query memory. Feature 2 core: recall relevant memories before answering."""
    if not API_KEY:
        return {"answer": "", "sources": []}
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(f"{BASE}/agent-recall", headers=_headers(), json={"q": q[:500]})
            if r.status_code == 200:
                return r.json()
    except Exception as e:
        logger.warning("recall error: %s", e)
    return {"answer": "", "sources": []}


async def note(text: str, tags: list = None, timeout: float = 5.0) -> bool:
    """Save a quick observation. Used by journal/CRM/coaching/sales features."""
    if not API_KEY or not text or len(text.strip()) < 5:
        return False
    payload = {"text": text[:500]}
    if tags:
        payload["tags"] = tags[:10]
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(f"{BASE}/agent-note", headers=_headers(), json=payload)
            return r.status_code == 200
    except Exception as e:
        logger.warning("note error: %s", e)
    return False


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")
