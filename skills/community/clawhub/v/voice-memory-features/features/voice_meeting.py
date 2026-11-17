"""
voice_meeting.py — Feature 5: Voice Meeting Memory
Record, transcribe, summarize, and remember meetings. Every meeting becomes searchable.
"""
import logging
from .voice_memory import remember, recall, today

logger = logging.getLogger("voice_meeting")


async def record_meeting(meeting_title: str, transcript: str) -> str:
    """Store a meeting transcript. Returns session_id."""
    return await remember(
        transcript,
        title=f"Meeting - {meeting_title} - {today()}",
        tags=["voice-meeting", meeting_title],
    )


async def summarize_meeting(meeting_title: str) -> str:
    """Recall a meeting's summary, action items, and decisions."""
    r = await recall(f"Meeting '{meeting_title}': what was decided, action items, owners, next steps?")
    return r.get("answer", "")


async def action_items(project: str = None) -> str:
    """Recall open action items across meetings."""
    q = "What are the open action items and owners from meetings?"
    if project:
        q = f"What action items are open for project {project}?"
    r = await recall(q)
    return r.get("answer", "")
