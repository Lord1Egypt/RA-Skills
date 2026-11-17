"""
voice_coaching.py — Feature 6: Voice Coaching Memory
Track goals and progress across coaching sessions.
"""
import logging
from .voice_memory import remember, note, recall, today

logger = logging.getLogger("voice_coaching")


async def set_goal(goal: str, deadline: str = None) -> str:
    """Record a coaching goal."""
    text = f"Coaching goal: {goal}"
    if deadline:
        text += f" Deadline: {deadline}."
    return await remember(text, title=f"Coaching Goal - {today()}", tags=["voice-coaching", "goal"])


async def log_checkin(goal: str, progress: str, risk: str = None) -> bool:
    """Log progress on a goal."""
    text = f"Check-in on goal '{goal}': {progress}"
    if risk:
        text += f" Risk: {risk}."
    return await note(text, tags=["voice-coaching", "check-in"])


async def goal_status() -> str:
    """Current status of all coaching goals."""
    r = await recall("What are the coaching goals, latest progress, and risks?")
    return r.get("answer", "")
