"""
voice_journal.py — Feature 3: Voice Journal
Store every spoken thought as searchable memories. Speak it, it's saved.
"""
import logging
from .voice_memory import remember, note, recall, today

logger = logging.getLogger("voice_journal")


async def journal_entry(thought: str, mood: str = None, date: str = None) -> str:
    """Store a spoken journal entry. Returns session_id."""
    text = thought
    if mood:
        text = f"[mood: {mood}] {text}"
    sid = await remember(text, title=f"Voice Journal - {date or today()}", tags=["voice-journal"])
    return sid


async def today_entries() -> str:
    """Recall what you journaled today."""
    r = await recall(f"Voice journal entries from today {today()}")
    return r.get("answer", "")


async def search_journal(topic: str) -> str:
    """Semantic search over journal entries."""
    r = await recall(f"Journal entries about {topic}")
    return r.get("answer", "")
