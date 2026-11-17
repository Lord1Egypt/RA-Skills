"""
voice_sales.py — Feature 7: Voice Sales Memory
Remember objections, follow-ups, and customer history. Never lose a deal detail.
"""
import logging
from .voice_memory import remember, note, recall, today

logger = logging.getLogger("voice_sales")


async def log_call(contact: str, summary: str, objection: str = None, next_step: str = None) -> str:
    """Log a sales call with objection + next step. Returns session_id."""
    text = f"Sales call with {contact}. {summary}"
    if objection:
        text += f" Objection: {objection}."
    if next_step:
        text += f" Next step: {next_step}."
    return await remember(text, title=f"Sales call - {contact} - {today()}", tags=["voice-sales", contact])


async def log_objection(contact: str, objection: str) -> bool:
    """Remember an objection raised by a prospect."""
    return await note(f"{contact} raised objection: {objection}", tags=["voice-sales", contact, "objection"])


async def log_followup(contact: str, followup: str) -> bool:
    """Remember a promised follow-up."""
    return await note(f"Follow-up for {contact}: {followup}", tags=["voice-sales", contact, "follow-up"])


async def deal_context(contact: str) -> str:
    """Everything about a deal before a call."""
    r = await recall(f"What do we know about {contact}? objections, follow-ups, customer history, stage")
    return r.get("answer", "")


async def pipeline() -> str:
    """Open deals, next steps, and who to call next."""
    r = await recall("What deals are open, what are the next steps, and who needs follow-up?")
    return r.get("answer", "")
