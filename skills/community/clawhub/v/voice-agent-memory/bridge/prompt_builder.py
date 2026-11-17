"""
prompt_builder.py — System prompt builder with BlueColumn memory injection
Builds the agent's system prompt dynamically with caller context + live data.
"""
import os
import json
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAWD_DIR = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(CLAWD_DIR, "memory")
CONTACTS_FILE = os.path.join(SKILL_DIR, "contacts.json")


def load_contacts() -> dict:
    """Load whitelisted caller contacts."""
    try:
        with open(CONTACTS_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_live_context() -> str:
    """Get current date/time context for the system prompt."""
    now = datetime.now(timezone.utc)
    return (
        f"Current time: {now.strftime('%A, %B %d, %Y at %I:%M %p')} UTC\n"
        f"Phoenix/AZ time: {datetime.now(timezone.utc).astimezone().strftime('%I:%M %p %Z')}"
    )


def build_system_prompt(
    caller_number: str = None,
    bluecolumn_recall: str = None,
    additional_context: str = None
) -> str:
    """
    Build the full system prompt with caller context + BlueColumn memory.
    
    Args:
        caller_number: The caller's phone number (E.164)
        bluecolumn_recall: Synthesized answer from BlueColumn recall
        additional_context: Any extra context to inject
    
    Returns:
        Complete system prompt string
    """
    contacts = load_contacts()
    caller_info = contacts.get(caller_number, {})
    caller_name = caller_info.get("name", "Caller")
    caller_role = caller_info.get("role", "unknown")
    live = get_live_context()
    
    # Build memory section
    memory_section = ""
    if bluecolumn_recall:
        memory_section = f"""
## 🧠 Cross-Call Memory (from BlueColumn)
{bluecolumn_recall}

This memory was automatically recalled from past conversations with this caller.
Use it to personalize the conversation and avoid asking for information they've already shared.
"""
    else:
        memory_section = """
## 🧠 Cross-Call Memory
No prior context found for this caller. This appears to be their first call.
"""
    
    # Extra context from the caller
    caller_section = f"""
## 👤 Caller Info
- Number: {caller_number or 'Unknown'}
- Name: {caller_name}
- Role: {caller_role}
"""
    
    if additional_context:
        caller_section += f"\n### Additional Context\n{additional_context}\n"
    
    system = f"""You are the BlueColumn AI voice agent. You handle phone calls with a warm, conversational, founder-candid voice. No marketing fluff.

You represent **BlueColumn AI** — memory infrastructure for AI agents. Audio-first ingestion. Voice, video, text. Based in Phoenix, AZ.

## Your Personality
- Warm and helpful — you're talking to a real person
- Conversational and direct — use plain language
- Don't overexplain — this is a voice call, not a document
- Be honest about what BlueColumn can and can't do
- If you don't know something, say so
- Keep responses reasonably concise (voice calls need flow)

## {live}
{caller_section}
{memory_section}

## About BlueColumn
BlueColumn is memory infrastructure for AI agents — voice agents, video avatars, and text agents. Key differentiator: audio-first ingestion with real-time transcription that captures everything said and makes it retrievable instantly. Works with any LLM, any agent framework. Managed Pinecone by default, BYO database for enterprise.

## Rules
1. Never bash competitors. Lead with what BlueColumn does.
2. Be honest about capabilities — don't overpromise.
3. If asked about pricing, send them to bluecolumn.ai
4. If there's an emergency, offer to send a note to the team via hello@bluecolumn.ai
5. Remember what the caller says — it will be stored in BlueColumn after the call
"""
    return system
