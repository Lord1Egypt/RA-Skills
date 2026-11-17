"""
voice_context.py — Feature 2: Voice Context
Recall relevant memories BEFORE answering. Inject context into any voice response.
"""
import logging
from .voice_memory import recall, API_KEY

logger = logging.getLogger("voice_context")


async def get_context(question: str, persona: str = None, top_k: int = 5) -> dict:
    """Recall relevant memories before answering. Returns {context, sources}."""
    q = question
    if persona:
        q = f"{persona} — {question}"
    result = await recall(q)
    ctx = result.get("answer", "")
    sources = result.get("sources", [])[:top_k]
    return {"context": ctx, "sources": sources}


def build_context_block(context: str) -> str:
    """Format recall context for injection into a system prompt."""
    if not context:
        return ""
    return f"\n## 🧠 Voice Context (recalled)\n{context}\n"


async def context_for_caller(caller_number: str, name: str = "") -> str:
    """Convenience: recall everything about a caller before answering."""
    label = name or caller_number
    result = await recall(f"What do we know about {label} ({caller_number})? preferences, history, open items")
    return result.get("answer", "")
