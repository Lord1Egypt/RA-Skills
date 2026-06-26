"""LLM-backed WhatsApp agent for Zim using OpenRouter API.

Replaces the rigid keyword-parsing flow with a conversational AI agent
that understands natural language, asks clarifying questions, and
executes tool calls against Zim's search APIs.

Environment variables
---------------------
OPENROUTER_API_KEY   Required. OpenRouter API key.
ZIM_LLM_MODEL        Optional. Model to use via OpenRouter.
                     Default: anthropic/claude-3-haiku
ZIM_STATE_DB         SQLite path for conversation state.
                     Default: /tmp/zim_state.db
ZIM_TRAVELER_ID      Default traveler ID for policy lookups.
                     Default: "default"
"""

from __future__ import annotations

import json
import logging
import os
import random
from datetime import date, datetime, timedelta
from typing import Any
import re

import httpx

from zim.state_store import InMemoryStateStore, SQLiteStateStore, StateStore

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-3-haiku"
DEFAULT_SPEND_LIMIT = 2000.0  # USD — bookings above this need human approval

# Keep at most this many messages in stored history (excludes system prompt).
MAX_HISTORY = 30
# Max LLM → tool → LLM iterations per inbound message.
MAX_TOOL_ROUNDS = 6

# Conversation log path
CONVO_LOG_DB = os.environ.get("ZIM_CONVO_LOG_DB", "/var/lib/zim/conversations.db")


# ---------------------------------------------------------------------------
# Conversation logger — logs all messages for product feedback
# ---------------------------------------------------------------------------

import sqlite3
import time


class ConversationLogger:
    """Logs all WhatsApp conversations for product analytics.

    Tracks: user messages, agent responses, tool calls, errors,
    and flags unhandled/failed interactions for review.
    """

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path or CONVO_LOG_DB
        self._init_db()

    def _init_db(self) -> None:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp REAL NOT NULL,
                        user_id TEXT NOT NULL,
                        direction TEXT NOT NULL,
                        message TEXT NOT NULL,
                        tool_calls TEXT,
                        error TEXT,
                        category TEXT
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS feedback_flags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp REAL NOT NULL,
                        user_id TEXT NOT NULL,
                        flag_type TEXT NOT NULL,
                        detail TEXT,
                        user_message TEXT
                    )
                """)
        except Exception:
            logger.warning("Could not initialize conversation log DB at %s", self._db_path)

    def log_message(self, user_id: str, direction: str, message: str,
                    tool_calls: list[str] | None = None, error: str | None = None,
                    category: str | None = None) -> None:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    "INSERT INTO conversation_log (timestamp, user_id, direction, message, tool_calls, error, category) VALUES (?,?,?,?,?,?,?)",
                    (time.time(), user_id, direction, message,
                     json.dumps(tool_calls) if tool_calls else None, error, category),
                )
        except Exception:
            logger.warning("Failed to log conversation message")

    def flag(self, user_id: str, flag_type: str, detail: str, user_message: str = "") -> None:
        """Flag an interaction for review.

        flag_type: 'unhandled', 'error', 'frustration', 'feature_request', 'spend_limit'
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    "INSERT INTO feedback_flags (timestamp, user_id, flag_type, detail, user_message) VALUES (?,?,?,?,?)",
                    (time.time(), user_id, flag_type, detail, user_message),
                )
        except Exception:
            logger.warning("Failed to flag conversation")

    def get_summary(self, hours: int = 24) -> dict[str, Any]:
        """Generate a product feedback summary for the last N hours."""
        cutoff = time.time() - (hours * 3600)
        summary: dict[str, Any] = {"period_hours": hours, "flags": [], "stats": {}}
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.row_factory = sqlite3.Row
                # Total messages
                row = conn.execute(
                    "SELECT COUNT(*) as cnt FROM conversation_log WHERE timestamp > ? AND direction='inbound'",
                    (cutoff,),
                ).fetchone()
                summary["stats"]["total_user_messages"] = row["cnt"] if row else 0

                row = conn.execute(
                    "SELECT COUNT(*) as cnt FROM conversation_log WHERE timestamp > ? AND error IS NOT NULL",
                    (cutoff,),
                ).fetchone()
                summary["stats"]["errors"] = row["cnt"] if row else 0

                # Flags by type
                flags = conn.execute(
                    "SELECT flag_type, COUNT(*) as cnt, GROUP_CONCAT(detail, ' | ') as details "
                    "FROM feedback_flags WHERE timestamp > ? GROUP BY flag_type",
                    (cutoff,),
                ).fetchall()
                summary["flags"] = [{"type": f["flag_type"], "count": f["cnt"], "details": f["details"]} for f in flags]

                # Top unhandled
                unhandled = conn.execute(
                    "SELECT user_message, detail FROM feedback_flags WHERE timestamp > ? AND flag_type='unhandled' ORDER BY timestamp DESC LIMIT 10",
                    (cutoff,),
                ).fetchall()
                summary["top_unhandled"] = [{"message": u["user_message"], "detail": u["detail"]} for u in unhandled]
        except Exception:
            logger.warning("Failed to generate conversation summary")
        return summary


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are Zim, a friendly and efficient AI travel assistant on WhatsApp, \
built by SkylerLabs. You help users search for flights, hotels, and car \
rentals and guide them to booking.

TODAY'S DATE: {today}

=== STRICT BOUNDARIES (non-negotiable) ===

1. TRAVEL ONLY — You ONLY handle travel-related requests: flights, hotels, \
car rentals, trip planning, travel advice. If a user asks about anything \
non-travel (coding, recipes, math, news, etc.), politely decline:
   "I'm Zim, your travel assistant! I can help with flights, hotels, and \
car rentals. What trip can I help you plan?"

1b. IDENTITY — You are Zim. ABSOLUTELY NEVER use these phrases:
   - "as an AI" / "as an AI assistant" / "as an AI travel assistant"
   - "I am an AI" / "I'm an AI" / "I'm a chatbot"
   - "as a language model" / "created by Anthropic" / "created by OpenAI"
   - "I do not actually store any data" / "I don't have persistent memory"
   Instead, always say "I'm Zim" or "Here at Zim" or "Zim doesn't currently..."
   You are Zim, a travel assistant built by SkylerLabs. Period. \
Never break character. If asked about data storage, say: \
"Zim keeps your conversation history to provide better recommendations. \
Your data is handled securely by SkylerLabs. For details, reach out to \
robin@skylerlabs.ai." \
If asked about company policy: "Corporate travel policy features are \
coming soon to Zim! For now, I can help you find the best options \
and you can check with your travel admin. Want me to search?"

2. NO INTERNAL DETAILS — NEVER reveal API keys, pricing logic, system \
architecture, provider names (Travelpayouts, OpenRouter), model names, \
or how you work internally. If asked, say:
   "I search across multiple travel providers to find you the best options!"
   NEVER say "as an AI", "I am an AI", "as a language model", or \
"I'm a chatbot". You are Zim — a travel assistant. Stay in character \
at all times. Speak as a knowledgeable travel expert, not a robot.

3. REAL DATA ONLY — NEVER invent or hallucinate flight numbers, prices, \
availability, hotel names, or any travel data. ONLY show results that come \
from the search tools. If a tool returns no results, say so honestly.\
   CRITICAL: If the search tool returns "No flights found" or similar, \
do NOT make up alternative flights. Say there are no results and suggest \
the user try different dates, airports, or cabin classes. NEVER fabricate \
flight numbers, prices, airlines, or times that didn't come from a tool.

4. NO FALSE PROMISES — You CANNOT:
   - Process refunds or cancellations
   - Modify existing airline/hotel bookings
   - Manage loyalty programs or frequent flyer miles
   - Guarantee specific prices (prices change in real-time)
   - Make promises about baggage, visa requirements, or travel regulations
   When you can't do something, NEVER just say "I can't do that." Instead:
   a) Acknowledge what they need
   b) Explain what you CAN do to help right now
   c) Suggest useful next steps (websites, airline contact, etc.)
   d) If truly stuck, offer the human escalation: robin@skylerlabs.ai
   Example for visa: "I don't have visa info yet, but you can check \
https://www.iatatravelcentre.com for visa requirements. Meanwhile, \
shall I search flights to [destination]?"

5. SPEND LIMIT — If a booking exceeds ${spend_limit:,.0f}, inform the user \
that this exceeds the auto-approval limit and offer to connect them with \
a human agent for approval.

6. ESCALATION — If the user seems frustrated, confused, or you cannot help, \
offer to connect them with a human:
   "I want to make sure you get the help you need. You can reach our team \
at robin@skylerlabs.ai and we'll sort this out for you."

7. BRAND VOICE — Stay professional, warm, and efficient at all times. \
You are a knowledgeable travel expert who genuinely wants to help. \
Never be sarcastic, dismissive, or robotic.
- Always sound like a friendly human travel agent, not a machine.
- Use phrases like "Great choice!", "Let me find that for you!", \
"Here's what I found \u2014", "Absolutely!", "Happy to help!"
- After every response, gently guide toward the next action \
(booking, searching more, refining results).
- Your goal is to get the user to a booking. Every interaction \
should move closer to a booking or keep them engaged.

8. FEATURES COMING SOON — When asked about corporate policy, \
approvals, payment processing, flight tracking, or loyalty programs, \
respond warmly:
   "That feature is coming very soon! For now, I can help you find \
and compare the best options. Want me to search for [relevant thing]?"
   Always redirect to what you CAN do. Never leave the user empty-handed.

=== FORMATTING (WhatsApp) ===
- No markdown tables or code blocks — WhatsApp doesn't render them.
- Keep messages short and readable on a phone screen.
- Use numbered lists (1. 2. 3.) when showing search results so users can \
pick by number.
- *bold* with asterisks is fine for WhatsApp.
- Avoid walls of text. Break into short paragraphs.

=== BEHAVIOR ===
- Be warm, concise, and conversational — you're texting with the user.
- When showing search results always number them (1, 2, 3) so users can \
reply "option 2", "I'll take 2", "number 3", etc.
- When a user picks an option number (1, 2, 3) or says "book option 2", \
"I'll take the second one", "number 3 please" after seeing search results, \
call book_option IMMEDIATELY with the category and option_number. \
NEVER ask "are you sure?" or "would you like to proceed?" — just do it.
- When the user says YES / confirm / go ahead / book it / sounds good \
after seeing a booking summary, call confirm_booking IMMEDIATELY. \
No confirmation questions — just send the payment link.
- Keep booking messages SHORT — this is WhatsApp, not a webpage.
- ALWAYS show the Zim service fee as a separate line item. Never hide it.
- Ask one clarifying question at a time when required info is missing.
- For flights, origin + destination + departure date are enough for a one-way search.
- Do NOT ask for a return date unless the user explicitly asks for a round trip or mentions a return.
- IMPORTANT: When the user modifies a previous search (e.g. "business class", \
"make it Saturday", "what about direct flights only", "cheaper options"), \
immediately re-run the search with the updated parameters. Do NOT ask for \
confirmation — just search and show new results.
- If a user says "next Friday" or "tomorrow", interpret relative to today's \
date above.
- After showing flight results, briefly offer to also search for a hotel or \
car rental if it seems useful.
- If a search returns no results, say so and suggest alternatives \
(different dates, nearby airports, etc.).
- CRITICAL: When a search tool returns results, you MUST include the full \
numbered list of results from the tool response in your message to the user. \
Do NOT summarize or skip the results. Copy the formatted results exactly \
and add a brief intro/outro around them.

=== AVAILABLE TOOLS ===
- search_flights: Search for flights between cities or airports.
- search_hotels: Search for hotels at a destination.
- search_cars: Search for car rentals at a location.
- book_option: Initiate booking for a search result the user selected. \
Call this when the user picks a numbered option from search results.
- confirm_booking: Confirm a pending booking and generate a Stripe payment \
link. Call this when the user says YES to a booking summary.
- get_booking_link: Fallback only — retrieve a direct provider link. \
Prefer book_option + confirm_booking for the in-WhatsApp flow.

Call search tools as soon as you have enough info. If a required field is \
missing, ask for it before calling the tool.\
"""


# ---------------------------------------------------------------------------
# Tool definitions (OpenAI function-calling format, supported by OpenRouter)
# ---------------------------------------------------------------------------

_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": (
                "Search for available flights between two cities or airports. "
                "Call this when the user asks about flights, airfare, or flying."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": (
                            "Origin city or IATA airport code "
                            "(e.g. 'Dubai', 'DXB', 'London', 'LHR')."
                        ),
                    },
                    "destination": {
                        "type": "string",
                        "description": (
                            "Destination city or IATA airport code "
                            "(e.g. 'Copenhagen', 'CPH', 'Paris', 'CDG')."
                        ),
                    },
                    "departure_date": {
                        "type": "string",
                        "description": "Departure date in YYYY-MM-DD format.",
                    },
                    "return_date": {
                        "type": "string",
                        "description": (
                            "Return date in YYYY-MM-DD format "
                            "(for round trips only — omit for one-way)."
                        ),
                    },
                    "cabin_class": {
                        "type": "string",
                        "enum": ["economy", "business", "first"],
                        "description": "Cabin class (default: economy).",
                    },
                    "travelers": {
                        "type": "integer",
                        "description": "Number of travelers (default: 1).",
                    },
                },
                "required": ["origin", "destination", "departure_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": (
                "Search for hotels at a destination. "
                "Call this when the user asks about hotels, accommodation, "
                "or a place to stay."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City or location to search hotels in.",
                    },
                    "checkin": {
                        "type": "string",
                        "description": "Check-in date in YYYY-MM-DD format.",
                    },
                    "checkout": {
                        "type": "string",
                        "description": "Check-out date in YYYY-MM-DD format.",
                    },
                    "guests": {
                        "type": "integer",
                        "description": "Number of guests (default: 1).",
                    },
                    "stars_min": {
                        "type": "integer",
                        "description": "Minimum star rating, 0–5 (default: 0).",
                    },
                },
                "required": ["location", "checkin", "checkout"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_cars",
            "description": (
                "Search for car rentals at a location. "
                "Call this when the user asks about renting a car or SUV."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City or location for car pickup.",
                    },
                    "pickup_date": {
                        "type": "string",
                        "description": "Pickup date in YYYY-MM-DD format.",
                    },
                    "dropoff_date": {
                        "type": "string",
                        "description": "Drop-off date in YYYY-MM-DD format.",
                    },
                    "car_class": {
                        "type": "string",
                        "description": (
                            "Vehicle class: economy, compact, suv, luxury, van, any."
                        ),
                    },
                },
                "required": ["location", "pickup_date", "dropoff_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_option",
            "description": (
                "Initiate booking for a previously shown search result. "
                "Call this when the user wants to book a specific option."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["flight", "hotel", "car"],
                        "description": "Type of booking.",
                    },
                    "option_number": {
                        "type": "integer",
                        "description": "1-based option number from the search results.",
                    },
                },
                "required": ["category", "option_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_booking",
            "description": (
                "Confirm a pending booking and generate a Stripe payment link. "
                "Call this when the user says YES to a booking summary."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_booking_link",
            "description": (
                "Get the booking link for a search result the user wants to book. "
                "Call this when the user selects a numbered option "
                "(e.g. 'book option 2', 'I'll take #1', 'the third one please')."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["flight", "hotel", "car"],
                        "description": "The type of result to retrieve.",
                    },
                    "index": {
                        "type": "integer",
                        "description": (
                            "1-based index of the result shown to the user "
                            "(e.g. 1 for the first result, 2 for the second)."
                        ),
                    },
                },
                "required": ["category", "index"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Result formatters (WhatsApp-friendly plain text)
# ---------------------------------------------------------------------------

def _fmt_flight(r: dict[str, Any], idx: int) -> str:
    def _hhmm(v: Any) -> str:
        """Extract HH:MM from a datetime object or ISO string."""
        if v is None:
            return ""
        if hasattr(v, "strftime"):
            return v.strftime("%H:%M")
        s = str(v)
        return s[11:16] if len(s) > 10 else s

    depart = r.get("depart_at")
    arrive = r.get("arrive_at")
    d_str = _hhmm(depart)
    a_str = _hhmm(arrive)
    timing = f"{d_str} / {a_str}" if d_str and a_str else (d_str or a_str)

    origin = r.get("origin", "")
    dest = r.get("destination", "")
    airline = r.get("airline") or "Airline"
    fn = r.get("flight_number") or ""
    cabin = r.get("cabin") or "economy"
    transfers = r.get("transfers", 0)
    price = r.get("price_usd", 0)
    policy = r.get("policy_status", "approved")

    note = ""
    if policy == "out_of_policy":
        note = " ⚠️ exceeds policy"
    elif policy == "approval_required":
        note = " ⚠️ approval needed"

    parts = [
        f"{idx}. {airline} {fn}".strip(),
        f"   {origin} → {dest}" + (f" | {timing}" if timing else " | Time TBC"),
        f"   {cabin.capitalize()} · {transfers} stop(s) · ${price:,.2f}{note}",
    ]
    return "\n".join(parts)


def _fmt_hotel(r: dict[str, Any], idx: int) -> str:
    name = r.get("name", "Hotel")
    stars = r.get("stars", 0)
    stars_str = "★" * stars if stars else ""
    location = r.get("location", "")
    rate = r.get("nightly_rate_usd", 0)
    policy = r.get("policy_status", "approved")
    refundable = r.get("refundable", False)

    note = ""
    if policy == "out_of_policy":
        note = " ⚠️ exceeds policy"
    elif policy == "approval_required":
        note = " ⚠️ approval needed"

    price_str = f"${rate:,.2f}/night" if rate else "price on request"
    cancel_str = " · Free cancellation" if refundable else ""

    parts = [
        f"{idx}. {name} {stars_str}".strip(),
        f"   {location}",
        f"   {price_str}{cancel_str}{note}",
    ]
    return "\n".join(parts)


def _fmt_car(r: dict[str, Any], idx: int) -> str:
    provider = r.get("provider", "Provider")
    cls = r.get("vehicle_class") or "vehicle"
    location = r.get("pickup_location", "")
    total = r.get("price_usd_total", 0)
    free_cancel = r.get("free_cancellation", False)
    policy = r.get("policy_status", "approved")

    note = ""
    if policy == "approval_required":
        note = " ⚠️ approval needed"

    price_str = f"${total:,.2f} est. total" if total else "see link for price"
    cancel_str = " · Free cancellation" if free_cancel else ""

    parts = [
        f"{idx}. {provider} — {cls.capitalize()}",
        f"   Pickup: {location}",
        f"   {price_str}{cancel_str}{note}",
    ]
    return "\n".join(parts)


def _format_results(category: str, results: list[dict[str, Any]], limit: int = 3) -> str:
    lines: list[str] = []
    for i, r in enumerate(results[:limit], start=1):
        if category == "flight":
            lines.append(_fmt_flight(r, i))
        elif category == "hotel":
            lines.append(_fmt_hotel(r, i))
        elif category == "car":
            lines.append(_fmt_car(r, i))
    return "\n\n".join(lines)


def _resolve_relative_date(text: str, today: date | None = None) -> tuple[str, date | None]:
    """Resolve simple relative weekday/date phrases into YYYY-MM-DD.

    Handles: tomorrow, next sunday, sunday, friday, next friday,
    in N days, in N weeks, this weekend, end of month,
    early/mid/late <Month>.
    Returns updated text and resolved date if any.
    """
    import calendar
    today = today or date.today()
    lower = text.lower()
    weekdays = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6,
    }

    if 'tomorrow' in lower:
        d = today + timedelta(days=1)
        return re.sub(r'\btomorrow\b', d.isoformat(), text, flags=re.I), d

    # 'in N days'
    m = re.search(r'\bin\s+(\d+)\s+days?\b', lower)
    if m:
        d = today + timedelta(days=int(m.group(1)))
        return re.sub(re.escape(m.group(0)), d.isoformat(), text, flags=re.I), d

    # 'in N weeks'
    m = re.search(r'\bin\s+(\d+)\s+weeks?\b', lower)
    if m:
        d = today + timedelta(weeks=int(m.group(1)))
        return re.sub(re.escape(m.group(0)), d.isoformat(), text, flags=re.I), d

    # 'this weekend' → next Saturday
    m = re.search(r'\bthis\s+weekend\b', lower)
    if m:
        delta = (5 - today.weekday()) % 7
        if delta == 0:
            delta = 7
        d = today + timedelta(days=delta)
        return re.sub(re.escape(m.group(0)), d.isoformat(), text, flags=re.I), d

    # 'end of month'
    m = re.search(r'\bend\s+of\s+(?:the\s+)?month\b', lower)
    if m:
        last_day = calendar.monthrange(today.year, today.month)[1]
        d = today.replace(day=last_day)
        return re.sub(re.escape(m.group(0)), d.isoformat(), text, flags=re.I), d

    # 'early/mid/late <Month>'
    _months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12,
    }
    m = re.search(
        r'\b(early|mid|late)\s+'
        r'(january|february|march|april|may|june|july|august|september|october|november|december)\b',
        lower,
    )
    if m:
        period_day = {'early': 5, 'mid': 15, 'late': 25}[m.group(1)]
        month_num = _months[m.group(2)]
        year = today.year
        d = date(year, month_num, period_day)
        if d < today:
            d = date(year + 1, month_num, period_day)
        phrase = m.group(0)
        return re.sub(re.escape(phrase), d.isoformat(), text, flags=re.I), d

    m = re.search(r'\b(next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', lower)
    if m:
        is_next = bool(m.group(1))
        wd_name = m.group(2)
        target = weekdays[wd_name]
        delta = (target - today.weekday()) % 7
        if delta == 0:
            delta = 7
        if is_next:
            delta += 7
        d = today + timedelta(days=delta)
        phrase = m.group(0)
        return re.sub(re.escape(phrase), d.isoformat(), text, flags=re.I), d

    return text, None


# ---------------------------------------------------------------------------
# LLM-backed WhatsApp agent
# ---------------------------------------------------------------------------


class LLMWhatsAppAgent:
    """WhatsApp agent for Zim — delegates to ZimOrchestrator for stateful flow.

    The orchestrator handles NLU (via LLM structured output), state machine
    transitions, search execution, result formatting, and payment creation.
    This class preserves the original interface and adds conversation logging.

    Args:
        api_key:            OpenRouter API key. Falls back to
                            ``OPENROUTER_API_KEY`` env var.
        model:              OpenRouter model string.
                            Falls back to ``ZIM_LLM_MODEL`` env var,
                            then ``anthropic/claude-3-haiku``.
        default_traveler_id: Used for policy lookups.
        state_store:        Where conversation state is persisted.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        default_traveler_id: str = "default",
        state_store: StateStore | None = None,
        spend_limit: float | None = None,
    ) -> None:
        from zim.orchestrator import ZimOrchestrator

        self._api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self._model = (
            model
            or os.environ.get("ZIM_LLM_MODEL", "")
            or DEFAULT_MODEL
        )
        self.default_traveler_id = default_traveler_id
        self._store: StateStore = state_store or SQLiteStateStore()
        self._spend_limit = spend_limit or float(os.environ.get("ZIM_SPEND_LIMIT", str(DEFAULT_SPEND_LIMIT)))
        self._logger = ConversationLogger()
        self._orchestrator = ZimOrchestrator(
            store=self._store,
            api_key=self._api_key,
            model=self._model,
        )

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def handle_message(self, message: str, user_id: str) -> str:
        """Process an inbound WhatsApp message and return a text reply."""
        self._logger.log_message(user_id, "inbound", message)

        if not self._api_key:
            logger.error("OPENROUTER_API_KEY is not set")
            self._logger.flag(user_id, "error", "OPENROUTER_API_KEY not set", message)
            return (
                "Zim's AI layer isn't configured yet "
                "(missing OPENROUTER_API_KEY). Please contact support."
            )

        error_log: str | None = None
        try:
            reply = self._orchestrator.handle_message(message.strip(), user_id)
        except httpx.TimeoutException:
            logger.warning("OpenRouter request timed out for user %s", user_id[:12])
            reply = "The request took too long. Please try again in a moment."
            error_log = "timeout"
            self._logger.flag(user_id, "error", "OpenRouter timeout", message)
        except httpx.HTTPStatusError as exc:
            logger.error(
                "OpenRouter API error %s for user %s",
                exc.response.status_code,
                user_id[:12],
            )
            reply = "I'm having trouble reaching the AI service. Please try again shortly."
            error_log = f"http_{exc.response.status_code}"
            self._logger.flag(user_id, "error", f"OpenRouter HTTP {exc.response.status_code}", message)
        except Exception:
            logger.exception("Unhandled error in LLM agent for user %s", user_id[:12])
            reply = "Something went wrong. Please try again."
            error_log = "unhandled_exception"
            self._logger.flag(user_id, "error", "Unhandled exception", message)

        # Sanitize: strip any "as an AI" character breaks that may slip through
        _ai_phrases = [
            "as an ai travel assistant", "as an ai assistant", "as an ai",
            "i am an ai", "i'm an ai", "as a language model",
            "created by anthropic", "created by openai",
            "i do not actually store any data",
        ]
        reply_lower = reply.lower()
        for phrase in _ai_phrases:
            if phrase in reply_lower:
                idx = reply_lower.index(phrase)
                reply = reply[:idx] + "here at Zim" + reply[idx + len(phrase):]
                reply_lower = reply.lower()

        self._logger.log_message(user_id, "outbound", reply, error=error_log)

        # Detect frustration signals
        lower_msg = message.lower()
        frustration_signals = [
            "this doesn't work", "useless", "terrible", "speak to a human",
            "real person", "agent please", "not helpful", "frustrated",
        ]
        if any(sig in lower_msg for sig in frustration_signals):
            self._logger.flag(user_id, "frustration", f"User message: {message[:200]}", message)

        return reply

    def _normalize_with_context(self, message: str, pending_search: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Resolve relative dates and carry over missing context from prior turn.

        This is a deterministic pre-processor so the LLM receives fully grounded
        context like concrete dates and prior origin/destination when the user says
        just "Friday" or similar.
        """
        original = message
        resolved_message, resolved_date = _resolve_relative_date(message)
        lower = resolved_message.lower()

        # Track likely flight-search context from the current/previous turn.
        ctx = dict(pending_search or {})
        if 'flight' in lower or 'fly' in lower:
            ctx['category'] = 'flight'

        # crude city extraction for common phrasing: from X to Y
        m = re.search(r'from\s+([A-Za-z\-\s]+?)\s+to\s+([A-Za-z\-\s]+?)(?:\s|$)', resolved_message, re.I)
        if m:
            ctx['origin'] = m.group(1).strip(' ,.')
            ctx['destination'] = m.group(2).strip(' ,.')
        else:
            m2 = re.search(r'from\s+([A-Za-z\-\s]+?)(?:\s|$)', resolved_message, re.I)
            if m2 and 'origin' not in ctx:
                ctx['origin'] = m2.group(1).strip(' ,.')

        if resolved_date:
            ctx['departure_date'] = resolved_date.isoformat()

        # If user sends just a relative date / weekday, expand with saved context.
        looks_like_date_only = bool(re.fullmatch(r'\s*(tomorrow|next\s+\w+|monday|tuesday|wednesday|thursday|friday|saturday|sunday|\d{4}-\d{2}-\d{2})\s*', original, re.I))
        if looks_like_date_only and ctx.get('category') == 'flight' and ctx.get('origin') and ctx.get('destination'):
            dep = ctx.get('departure_date') or (resolved_date.isoformat() if resolved_date else None)
            if dep:
                resolved_message = f"I need a one-way flight from {ctx['origin']} to {ctx['destination']} on {dep}"

        # If user says things like "Need a flight from Stockholm to London Friday after my meeting",
        # ensure the resolved date becomes explicit before it reaches the LLM.
        if ctx.get('category') == 'flight' and ctx.get('origin') and ctx.get('destination') and ctx.get('departure_date'):
            if 'from' in lower and 'to' in lower:
                resolved_message = f"I need a one-way flight from {ctx['origin']} to {ctx['destination']} on {ctx['departure_date']}"
            elif 'flight' in lower and 'from' in lower and 'to' not in lower:
                resolved_message = f"I need a one-way flight from {ctx['origin']} to {ctx['destination']} on {ctx['departure_date']}"

        return resolved_message, ctx

    # ------------------------------------------------------------------
    # Agentic loop
    # ------------------------------------------------------------------

    def _run_agent_loop(
        self,
        full_messages: list[dict[str, Any]],
        last_results: dict[str, list[dict[str, Any]]],
    ) -> tuple[str, dict[str, list[dict[str, Any]]], list[str]]:
        """Call the LLM, handle tool calls, repeat until a final reply."""
        tool_calls_log: list[str] = []
        _last_tool_results: list[str] = []  # track formatted search results
        for _round in range(MAX_TOOL_ROUNDS):
            response = self._call_llm(full_messages)
            choice = response["choices"][0]
            assistant_msg: dict[str, Any] = choice["message"]

            # Ensure content is always a string (some models return None)
            if assistant_msg.get("content") is None:
                assistant_msg["content"] = ""

            full_messages.append(assistant_msg)

            tool_calls: list[dict[str, Any]] = assistant_msg.get("tool_calls") or []
            finish_reason = choice.get("finish_reason", "")

            if not tool_calls or finish_reason == "stop":
                # If the LLM omitted search results, prepend them
                reply_text = assistant_msg.get("content", "")
                if _last_tool_results and reply_text:
                    # Check if the LLM actually included the results with prices
                    has_numbered_list = any(x in reply_text for x in ["1.", "1)"])
                    has_prices = any(x in reply_text for x in ["$", "€", "/night", "stop(s)"])
                    if not (has_numbered_list and has_prices):
                        # LLM skipped the results — prepend them
                        combined = "\n\n".join(_last_tool_results)
                        reply_text = f"{combined}\n\n{reply_text}"
                return reply_text, last_results, tool_calls_log

            # Execute each tool call and append results
            _last_tool_results = []
            for tc in tool_calls:
                tool_name = tc["function"]["name"]
                try:
                    raw_args = tc["function"].get("arguments", "{}")
                    tool_args = json.loads(raw_args) if raw_args else {}
                except json.JSONDecodeError:
                    tool_args = {}

                logger.info(
                    "Executing tool %s with args %s",
                    tool_name,
                    json.dumps(tool_args)[:200],
                )

                tool_result = self._execute_tool(tool_name, tool_args, last_results)
                tool_calls_log.append(f"{tool_name}({json.dumps(tool_args)[:100]})")

                # Track search results for fallback inclusion
                if tool_name.startswith("search_") and len(tool_result) > 50:
                    _last_tool_results.append(tool_result)

                full_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": tool_result,
                    }
                )

        # Safety fallback: extract last assistant text if any
        for msg in reversed(full_messages):
            if msg.get("role") == "assistant" and msg.get("content"):
                return msg["content"], last_results, tool_calls_log

        return "Sorry, I couldn't complete that request. Please try again.", last_results, tool_calls_log

    # ------------------------------------------------------------------
    # OpenRouter API call
    # ------------------------------------------------------------------

    def _call_llm(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        """POST to OpenRouter chat completions endpoint."""
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "HTTP-Referer": "https://zim.travel",
                    "X-Title": "Zim Travel Assistant",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self._model,
                    "messages": messages,
                    "tools": _TOOLS,
                    "tool_choice": "auto",
                },
            )
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Tool dispatch
    # ------------------------------------------------------------------

    def _execute_tool(
        self,
        name: str,
        args: dict[str, Any],
        last_results: dict[str, list[dict[str, Any]]],
    ) -> str:
        """Route tool call to the appropriate handler and return a text result."""
        try:
            if name == "search_flights":
                return self._tool_search_flights(args, last_results)
            elif name == "search_hotels":
                return self._tool_search_hotels(args, last_results)
            elif name == "search_cars":
                return self._tool_search_cars(args, last_results)
            elif name == "book_option":
                return self._tool_book_option(args, last_results)
            elif name == "confirm_booking":
                return self._tool_confirm_booking(last_results)
            elif name == "get_booking_link":
                return self._tool_get_booking_link(args, last_results)
            else:
                return f"Unknown tool: {name}"
        except httpx.TimeoutException:
            logger.warning("Search timed out in tool %s", name)
            return "Search timed out. Please try again."
        except httpx.HTTPStatusError as exc:
            logger.warning("Search API error %s in tool %s", exc.response.status_code, name)
            return f"Search provider returned an error ({exc.response.status_code}). Please try again."
        except EnvironmentError:
            logger.error("Missing API token in tool %s", name)
            return "Search API is not configured. Please contact support."
        except ValueError as exc:
            logger.warning("Value error in tool %s: %s", name, exc)
            return f"Could not parse the location or date: {exc}. Please try rephrasing."
        except Exception:
            logger.exception("Unhandled error in tool %s", name)
            return "An error occurred while searching. Please try again."

    def _tool_search_flights(
        self,
        args: dict[str, Any],
        last_results: dict[str, list[dict[str, Any]]],
    ) -> str:
        from zim.trip import plan_trip

        origin: str = args["origin"]
        destination: str = args["destination"]
        departure_str: str = args["departure_date"]
        return_str: str | None = args.get("return_date")

        departure = date.fromisoformat(departure_str)
        return_date = date.fromisoformat(return_str) if return_str else None

        itinerary = plan_trip(
            origin=origin,
            destination=destination,
            departure=departure,
            return_date=return_date,
            mode="personal",
            traveler_id=self.default_traveler_id,
        )

        flights = itinerary.flights
        last_results["flight"] = [f.model_dump() for f in flights]

        if not flights:
            return (
                f"No flights found from {origin} to {destination} "
                f"on {departure_str}. Try different dates or nearby airports."
            )

        formatted = _format_results("flight", last_results["flight"])

        shown = min(len(flights), 3)
        extra = len(flights) - shown
        header = f"Here are the top {shown} flights from {origin} to {destination}:"
        footer = f"\n\n({extra} more options available — ask to see more)" if extra > 0 else ""

        return (
            f"{header}\n\n"
            f"{formatted}{footer}"
        )

    def _tool_search_hotels(
        self,
        args: dict[str, Any],
        last_results: dict[str, list[dict[str, Any]]],
    ) -> str:
        from zim import hotel_search

        location: str = args["location"]
        checkin_str: str = args["checkin"]
        checkout_str: str = args["checkout"]
        guests: int = int(args.get("guests") or 1)
        stars_min: int = int(args.get("stars_min") or 0)

        checkin = date.fromisoformat(checkin_str)
        checkout = date.fromisoformat(checkout_str)

        results = hotel_search.search(
            location=location,
            checkin=checkin,
            checkout=checkout,
            adults=guests,
            stars_min=stars_min,
        )

        last_results["hotel"] = [h.model_dump() for h in results]

        if not results:
            return f"No hotels found in {location} for those dates. Try a different location."

        formatted = _format_results("hotel", last_results["hotel"])
        nights = max((checkout - checkin).days, 1)

        shown = min(len(results), 3)
        extra = len(results) - shown
        header = f"Here are the top {shown} hotels in {location}"
        footer = f"\n\n({extra} more options available — ask to see more)" if extra > 0 else ""

        return (
            f"{header} "
            f"({checkin_str} → {checkout_str}, {nights} night(s)):\n\n"
            f"{formatted}{footer}"
        )

    def _tool_search_cars(
        self,
        args: dict[str, Any],
        last_results: dict[str, list[dict[str, Any]]],
    ) -> str:
        from zim import car_search

        location: str = args["location"]
        pickup_str: str = args["pickup_date"]
        dropoff_str: str = args["dropoff_date"]
        car_class: str | None = args.get("car_class")

        pickup = date.fromisoformat(pickup_str)
        dropoff = date.fromisoformat(dropoff_str)

        results = car_search.search(
            location=location,
            pickup=pickup,
            dropoff=dropoff,
            car_class=car_class,
        )

        last_results["car"] = [c.model_dump() for c in results]

        if not results:
            return f"No car rentals found in {location} for those dates."

        formatted = _format_results("car", last_results["car"])
        days = max((dropoff - pickup).days, 1)

        return (
            f"Found {len(results)} car rental option(s) in {location} "
            f"({pickup_str} → {dropoff_str}, {days} day(s)):\n\n"
            f"{formatted}"
        )

    def _tool_book_option(
        self,
        args: dict[str, Any],
        last_results: dict[str, Any],
    ) -> str:
        from zim.fees import calculate_fee

        category: str = args["category"]
        option_number: int = int(args["option_number"])

        results = last_results.get(category, [])
        if not results:
            return (
                f"No {category} results in memory. "
                "Please run a search first and then select an option."
            )
        if option_number < 1 or option_number > len(results):
            return (
                f"Option {option_number} is out of range — I have {len(results)} "
                f"{category} result(s). Please choose 1–{len(results)}."
            )

        item = results[option_number - 1]

        # Extract base price and build a human-readable description
        if category == "flight":
            base_price = float(item.get("price_usd", 0))
            airline = item.get("airline", "")
            fn = item.get("flight_number", "")
            origin = item.get("origin", "")
            dest = item.get("destination", "")
            cabin = (item.get("cabin") or "economy").capitalize()
            # Try to extract a readable date from depart_at
            depart_raw = item.get("depart_at")
            if depart_raw:
                try:
                    dt = datetime.fromisoformat(str(depart_raw)[:19])
                    date_str = dt.strftime("%b %d, %Y")
                except (ValueError, TypeError):
                    date_str = str(depart_raw)[:10]
            else:
                date_str = ""
            desc_line = f"✈️ *Booking Summary*\n{airline} {fn} | {origin} → {dest}".strip()
            if date_str:
                desc_line += f"\n{date_str} | {cabin}"
            else:
                desc_line += f"\n{cabin}"
        elif category == "hotel":
            base_price = float(item.get("nightly_rate_usd", 0))
            name = item.get("name", "Hotel")
            location = item.get("location", "")
            stars = item.get("stars", 0)
            stars_str = ("★" * stars) if stars else ""
            desc_line = f"🏨 *Booking Summary*\n{name} {stars_str}".strip()
            if location:
                desc_line += f"\n{location}"
            desc_line += "\n(price per night)"
        else:  # car
            base_price = float(item.get("price_usd_total", 0))
            provider = item.get("provider", "")
            cls = (item.get("vehicle_class") or "vehicle").capitalize()
            pickup = item.get("pickup_location", "")
            desc_line = f"🚗 *Booking Summary*\n{provider} — {cls}".strip()
            if pickup:
                desc_line += f"\nPickup: {pickup}"

        breakdown = calculate_fee(base_price)
        booking_id = f"ZIM-{date.today().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

        # Store the pending booking
        last_results["pending_booking"] = {
            "booking_id": booking_id,
            "category": category,
            "item": item,
            "base_price": base_price,
            "fee": breakdown.fee_amount_usd,
            "total_price": breakdown.total_usd,
        }

        return (
            f"{desc_line}\n\n"
            f"Base fare: ${base_price:,.2f}\n"
            f"Zim service fee: ${breakdown.fee_amount_usd:,.2f}\n"
            f"*Total: ${breakdown.total_usd:,.2f}*\n\n"
            "Reply YES to confirm and receive your payment link.\n"
            "Reply NO to go back to results."
        )

    def _tool_confirm_booking(
        self,
        last_results: dict[str, Any],
    ) -> str:
        pending = last_results.get("pending_booking")
        if not pending:
            return (
                "No pending booking found. "
                "Please select an option from the search results first."
            )

        booking_id: str = pending["booking_id"]
        category: str = pending["category"]
        item: dict[str, Any] = pending["item"]
        base_price: float = pending["base_price"]
        fee: float = pending["fee"]

        # Build line items description for Stripe
        if category == "flight":
            desc = (
                f"Flight: {item.get('origin', '?')} → {item.get('destination', '?')} "
                f"({item.get('airline', '')} {item.get('flight_number', '')})".strip()
            )
        elif category == "hotel":
            desc = f"Hotel: {item.get('name', 'Hotel')} (per night)"
        else:
            desc = f"Car rental: {item.get('provider', 'Rental')} {item.get('vehicle_class', '')}".strip()

        try:
            from zim.payment import CheckoutLineItem, StripeConfig, create_checkout_session

            cfg = StripeConfig.from_env()
            if not cfg.is_configured:
                raise EnvironmentError("STRIPE_SECRET_KEY not set")

            line_items = [
                CheckoutLineItem(
                    description=desc,
                    amount_cents=int(round(base_price * 100)),
                    category=category,
                ),
                CheckoutLineItem(
                    description="Zim Service Fee",
                    amount_cents=int(round(fee * 100)),
                    category="service_fee",
                ),
            ]

            result = create_checkout_session(
                booking_id=booking_id,
                line_items=line_items,
            )
            checkout_url = result.checkout_url

            return (
                "Payment link ready! 💳\n\n"
                f"Click here to complete your booking:\n{checkout_url}\n\n"
                "This link expires in 30 minutes.\n"
                f"Your booking reference: {booking_id}\n\n"
                "Once payment is confirmed, I'll send you the booking details!"
            )

        except Exception as exc:
            logger.warning("Stripe checkout failed for %s: %s", booking_id, exc)
            # Graceful fallback to deeplink
            deeplink = item.get("link", "")
            if deeplink:
                return (
                    "Booking is almost ready! Our payment system is being set up. "
                    f"In the meantime, here's a link to book directly: {deeplink}"
                )
            return (
                "Booking is almost ready! Our payment system is being set up. "
                "Please try again in a moment or contact robin@skylerlabs.ai for help."
            )

    def _tool_get_booking_link(
        self,
        args: dict[str, Any],
        last_results: dict[str, list[dict[str, Any]]],
    ) -> str:
        category: str = args["category"]
        index: int = int(args["index"])

        results = last_results.get(category, [])
        if not results:
            return (
                f"No {category} results in memory. "
                "Please run a search first and then select an option."
            )

        if index < 1 or index > len(results):
            return (
                f"Index {index} is out of range — I have {len(results)} {category} result(s). "
                f"Please choose a number between 1 and {len(results)}."
            )

        result = results[index - 1]
        link = result.get("link", "")

        if category == "flight":
            r = result
            summary = (
                f"{r.get('airline', '')} {r.get('flight_number', '')} "
                f"{r.get('origin', '')} → {r.get('destination', '')} "
                f"({r.get('cabin', 'economy')}) · ${r.get('price_usd', 0):,.2f}"
            )
        elif category == "hotel":
            r = result
            rate = r.get("nightly_rate_usd", 0)
            summary = f"{r.get('name', 'Hotel')} · ${rate:,.2f}/night"
        else:  # car
            r = result
            total = r.get("price_usd_total", 0)
            summary = (
                f"{r.get('provider', '')} {r.get('vehicle_class', '')} "
                f"· ${total:,.2f} est."
            )

        link_line = f"\nBook here: {link}" if link else "\n(No direct link — visit the provider's site.)"
        return f"Selected: {summary.strip()}{link_line}"

