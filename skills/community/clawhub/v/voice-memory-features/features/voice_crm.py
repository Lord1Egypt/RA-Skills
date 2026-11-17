"""
voice_crm.py — Feature 4: Voice CRM
Remember customer conversations and preferences. Voice-driven CRM.
"""
import logging
from .voice_memory import remember, note, recall, today

logger = logging.getLogger("voice_crm")


async def log_customer_interaction(customer: str, summary: str, outcome: str = None) -> str:
    """Log a customer conversation. Returns session_id."""
    text = f"Customer: {customer}. {summary}"
    if outcome:
        text += f" Outcome: {outcome}."
    return await remember(text, title=f"CRM - {customer} - {today()}", tags=["voice-crm", customer])


async def log_preference(customer: str, preference: str) -> bool:
    """Remember a customer preference."""
    return await note(f"{customer} prefers {preference}", tags=["voice-crm", customer, "preference"])


async def customer_profile(customer: str) -> str:
    """Full customer history + preferences before a call."""
    r = await recall(f"What do we know about customer {customer}? conversations, preferences, history, open items")
    return r.get("answer", "")


async def open_followups(customer: str = None) -> str:
    """Recall open follow-up items."""
    q = "What follow-ups and open items are pending?"
    if customer:
        q = f"What follow-ups are pending for {customer}?"
    r = await recall(q)
    return r.get("answer", "")
