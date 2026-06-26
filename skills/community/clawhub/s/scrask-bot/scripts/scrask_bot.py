#!/usr/bin/env python3
"""
scrask_bot.py
Scrask Bot — Screenshot to Intent Parser

Parses screenshots (from any chat transport — Telegram, iMessage, Slack, etc.)
using Gemini or Claude vision, and emits structured intent JSON. Scrask does
not write to any calendar or task store directly — the OpenClaw agent delegates
to the user's installed destination skills (calctl, apple-reminders, things-mac,
brainz-calendar, etc.) based on the intent type.

Usage:
  python scrask_bot.py --image-path <path> [--provider auto|claude|gemini] [--timezone <tz>]
  python scrask_bot.py --image-base64 <base64> [--provider auto|claude|gemini]

Env vars:
  GEMINI_API_KEY            — optional; enables Gemini-first 'auto' routing and 'gemini' mode
  ANTHROPIC_API_KEY         — optional; enables Claude fallback and 'claude' mode
  OPENCLAW_VISION_PROVIDER  — injected by OpenClaw; 'anthropic' or 'google'
  OPENCLAW_VISION_KEY       — injected by OpenClaw; key for the platform-configured LLM
  OPENCLAW_VISION_MODEL     — injected by OpenClaw; optional model name override
  VISION_PROVIDER           — 'auto' (default), 'openclaw', 'claude', or 'gemini' (overridden by --provider)

Requirements:
  pip install -r requirements.txt
"""

import argparse
import base64
import json
import os
import sys
from datetime import date
from pathlib import Path

try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# ─── Constants ─────────────────────────────────────────────────────────────────

MIME_TYPES = {
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png":  "image/png",
    ".gif":  "image/gif",
    ".webp": "image/webp",
}

DEFAULT_CONFIDENCE_THRESHOLD = 0.75   # legacy per-item gate (kept for backward compat)
FALLBACK_THRESHOLD           = 0.60   # Gemini→Claude fallback trigger (worst per-field score)
FALLBACK_IMPROVEMENT_MIN     = 0.05

ACTIONABLE_THRESHOLD         = 0.70   # below → emit a top-level "is this actionable?" clarification
TYPE_THRESHOLD               = 0.70   # below → emit a "calendar or task list?" clarification
FIELD_THRESHOLD              = 0.70   # below (or value=null) for a mandatory field → field clarification

# Mandatory field lists per item type — drive clarification generation in shape_intent.
MANDATORY_FIELDS_BY_TYPE = {
    "event":    ["title", "date", "time"],
    "reminder": ["title", "date", "time"],
    "task":     ["title"],
}

# Templates for clarification questions, keyed by field name. {title} is the item title
# (or "this item" if title is missing/empty).
CLARIFICATION_QUESTIONS = {
    "title":        "What should I call this?",
    "date":         "What date is {title}?",
    "time":         "What time is {title}?",
    "end_time":     "When does {title} end?",
    "location":     "Where is {title}?",
    "participants": "Who is going to {title}?",
    "description":  "Any details I should add for {title}?",
    "priority":     "How urgent is {title}?",
    "type":         "Should {title} go on your calendar or task list?",
}

CLAUDE_MODEL = "claude-opus-4-6"
GEMINI_MODEL = "gemini-2.0-flash"


# ─── Shared prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a structured data extraction assistant. "
    "Your only job is to analyze screenshots and return valid JSON — nothing else. "
    "No preamble, no explanation, no markdown fences. Only raw JSON."
)

USER_PROMPT_TEMPLATE = """Analyze this screenshot carefully. It may be a WhatsApp forward,
email screenshot, social media post, chat message, event flyer, or booking confirmation.

Extract ALL actionable information — calendar events AND task-like asks — and return a single JSON object:

{{
  "actionable_confidence": 0.0-1.0,
  "items": [
    {{
      "type": "event" | "reminder" | "task",
      "type_confidence": 0.0-1.0,
      "title": "concise title in English (max 60 chars)",
      "date": "YYYY-MM-DD or null",
      "time": "HH:MM (24h) or null",
      "end_time": "HH:MM (24h) or null",
      "end_date": "YYYY-MM-DD or null (multi-day events only; null if same day as date)",
      "timezone_hint": "IANA timezone or offset string, or null",
      "location": "physical address or venue name or null",
      "online_link": "Zoom/Meet/Teams URL or null",
      "participants": ["string", ...] or null,
      "recurrence": "none | daily | weekly | monthly | yearly",
      "recurrence_day": "e.g. Tuesday or null",
      "description": "1-2 sentence context summary in English or null",
      "priority": "high | medium | low",
      "source_type": "whatsapp | email | social_media | chat | flyer | booking | other",
      "language": "ISO 639-1 code of the screenshot text",
      "already_in_calendar_hint": true | false,
      "confidences": {{
        "title":        0.0-1.0,
        "date":         0.0-1.0,
        "time":         0.0-1.0,
        "end_time":     0.0-1.0,
        "location":     0.0-1.0,
        "participants": 0.0-1.0,
        "description":  0.0-1.0,
        "priority":     0.0-1.0
      }}
    }}
  ],
  "screenshot_summary": "one sentence describing what this screenshot shows",
  "no_actionable_content": true | false,
  "parse_notes": "edge cases, ambiguities, or things to flag to the user"
}}

Classification rules:
- "event"    → scheduled gathering with a date (time optional if all-day), OR a venue/link with an
               inferred date. Social meetups, invites, flights, hotel check-ins. Goes to a calendar.
- "reminder" → personal action with a deadline or due date (date required; time optional).
               Bills, submissions, prep steps before an event ("book the table", "buy a gift").
               Goes to a task list with a due date.
- "task"     → action item with no date at all (e.g. "send me your resume"). Goes to a task list.

Date and time inference (anchor on Current date and User timezone below):
- Resolve relative phrases: tomorrow, next Friday, this Sunday, in 2 weeks, next month, etc.
- If month/day already passed this year, assume next year unless context implies otherwise.
- Default to User timezone when none is stated; put explicit or detected zones in timezone_hint.
- All-day: date present, no specific time → type "event", time null, end_time null.
- Reminder with due time: type "reminder", set both date and time.
- Time ranges ("2–4 pm"): time = start, end_time = end on the same date.
- Approximate times ("around 7", "7ish"): pick best guess, lower confidence, note in parse_notes.
- Dual timezone ("3 pm EST / 12 pm PST"): use the time matching User timezone; note the other in parse_notes.
- Vague deadlines ("EOD", "end of week", "ASAP"): infer best date/time, lower confidence, explain in parse_notes.

Per source type:
- whatsapp / chat: informal wording; "lets meet fri" may need date inference — lower confidence accordingly.
- email: look for structured invite blocks, organizer, venue, Meet/Zoom links — often high confidence.
- social_media / flyer: poster dates may lack year; venue-heavy → event even without time (lower confidence).
- booking: flights, trains, hotels — extract the primary actionable datetime (departure, check-in);
           put confirmation numbers and secondary times in description.
- Reschedule or cancellation notices: extract the NEW date/time if rescheduled; type "event" or "reminder"
  as appropriate; note "reschedule" or "cancellation" in parse_notes.

Translation:
- If screenshot text is not English, set language to its ISO 639-1 code.
- Always write title and description in English regardless of source language.

already_in_calendar_hint:
- Set true when the screenshot IS a calendar app view, agenda, or existing event listing — not a new invite.

Multi-item rules:
- One screenshot may yield multiple items. Split when actions, dates, or intents differ.
  Do not merge unrelated items into one.

Event + implied prep (always emit BOTH when the pattern applies):
- When a social plan at a venue implies a prep step the user must do beforehand, emit TWO items:
  1) type "event" — the gathering itself (date, time, location from the message)
  2) type "reminder" — the prep action, due BEFORE the event (see timing below)
- Trigger when the plan implies prep even if not stated explicitly:
  • restaurant / bar / cafe dinner or drinks → book a table or reservation
  • travel (flight, train, trip) → check in, pack, arrange transport
  • party, wedding, hosted event → RSVP, buy gift, arrange outfit
  • meeting with external person at a venue → confirm or book if needed
- Do NOT split when prep is unnecessary or already done:
  • casual "come over to my place" — event only
  • message already includes a confirmation number or "booked" / "confirmed"
  • explicit single intent ("see you at 7" with no venue booking implied)

Prep reminder timing:
- Due date = day before the event, OR same day several hours before event time — whichever
  is more realistic for the prep type. Restaurant reservations → due day before or morning of.
- Copy venue and event date into the reminder title. Reference the event in description.
- Prep reminders are inferred — set type_confidence and the relevant field confidences in
  the 0.65–0.80 band, and note the inference in parse_notes.

Participants:
- Extract named people the screenshot mentions as attending/invited (e.g. "lunch with Priya and Anika"
  → ["Priya", "Anika"]). Do NOT invent names. If no one is named, set participants to null.
- The sender of a chat message is a participant only if the message implies they will attend (e.g.
  "Priya: let's grab coffee" → Priya is a participant; "Priya: don't forget the meeting" is not).
- Participants are NEVER mandatory; missing participants is normal.

Examples (always two items for these patterns):
- "lets grab coffee at Pegasus on friday" →
    event:    "Coffee at Pegasus" — date Friday, time inferred or null
    reminder: "Book table at Pegasus" — due Thursday (or Friday morning)
- "lets go for dinner at Olive Garden on friday evening" →
    event:    "Dinner at Olive Garden" — date Friday, time ~19:00, location Olive Garden
    reminder: "Book reservation at Olive Garden" — due Thursday (or Friday before 17:00)

no_actionable_content:
- true only when there is no event, reminder, or task. Memes, scenery, pure venting with no ask,
  code/error screenshots, and shopping lists with no dates are not actionable.
- "Send me your resume" IS actionable — it is a task.

Confidence scoring (per-field + two decisions):

Score each confidence on this scale:
- 0.9–1.0  Directly visible in the screenshot, no inference needed
- 0.75–0.9 Minor inference (relative date resolved, year inferred from context)
- 0.5–0.75 Meaningful guesswork (vague phrasing, partial info, approximate values)
- < 0.5    Very little usable info — emit the field anyway if you have a best guess

actionable_confidence (top-level, 0.0–1.0):
- How sure are you the screenshot contains AT LEAST one actionable event/reminder/task.
- 0.9+ for clear invites, bookings, explicit asks. 0.6–0.8 for ambiguous chat that might
  imply a plan. < 0.5 when the screenshot looks like content with no real ask. Pair a low
  score here with no_actionable_content=true only when you are confident there is nothing.

type_confidence (per item, 0.0–1.0):
- How sure are you about the type (event vs reminder vs task) for THIS item.
- High when the screenshot makes the distinction obvious (clear time + venue → event).
- Low (0.5–0.7) when the line between reminder and task is fuzzy, or between event and
  reminder is unclear (e.g. "lunch with mom tomorrow" — event or reminder?).

confidences (per field, 0.0–1.0 each):
- title:        was the title obvious in the text, or did you summarize/translate heavily?
- date:         explicit date → high; relative ("next Friday") → 0.75–0.9; vague → 0.5–0.75.
- time:         explicit time → high; "around 7" / "7ish" → 0.55–0.7; "evening" → 0.5–0.65.
- end_time:     present in source → high; inferred from duration → 0.6–0.8; absent → 0.0.
- location:     full address → high; venue name only → 0.7–0.85; absent or guessed → low.
- participants: names directly mentioned → high; inferred from group context → 0.6–0.75;
                no participants found → 0.0.
- description:  rephrased from source → 0.8+; heavily inferred → 0.5–0.7; absent → 0.0.
- priority:     explicit ("urgent", "ASAP") → high; tone-inferred → 0.5–0.7; absent → 0.0.

Only include a key in `confidences` for fields you actually extracted. Omit keys for fields
you set to null AND did not attempt to infer. A field with a non-null value MUST have a
confidence entry.

Current date: {today}
User timezone: {timezone}

Return only JSON. No markdown. No explanation."""


# ─── Provider: Claude ──────────────────────────────────────────────────────────

def parse_with_claude(
    image_base64: str,
    media_type: str,
    api_key: str,
    timezone: str = "UTC",
    model: str | None = None,
) -> dict:
    if not CLAUDE_AVAILABLE:
        raise RuntimeError("anthropic package not installed. Run: pip install anthropic")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model or CLAUDE_MODEL,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_base64}},
                {"type": "text",  "text": USER_PROMPT_TEMPLATE.format(today=date.today().isoformat(), timezone=timezone)},
            ],
        }],
    )
    raw = message.content[0].text if message.content else ""
    return _clean_and_parse_json(raw)


# ─── Provider: Gemini ──────────────────────────────────────────────────────────

def parse_with_gemini(
    image_base64: str,
    media_type: str,
    api_key: str,
    timezone: str = "UTC",
    model: str | None = None,
) -> dict:
    if not GEMINI_AVAILABLE:
        raise RuntimeError("google-generativeai package not installed. Run: pip install google-generativeai")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=model or GEMINI_MODEL, system_instruction=SYSTEM_PROMPT)

    image_bytes = base64.standard_b64decode(image_base64)
    image_part  = {"mime_type": media_type, "data": image_bytes}
    prompt      = USER_PROMPT_TEMPLATE.format(today=date.today().isoformat(), timezone=timezone)

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT:        HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH:       HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    response = model.generate_content(
        [image_part, prompt],
        safety_settings=safety_settings,
        generation_config=genai.GenerationConfig(max_output_tokens=1500, temperature=0.1),
    )

    raw = response.text if response.text else ""
    return _clean_and_parse_json(raw)


# ─── Provider: OpenClaw (use whatever vision LLM the platform has configured) ──

# OpenClaw injects these env vars into skill subprocesses so individual skills
# can call the user's configured vision LLM without each shipping its own keys.
# The skill stays vision-provider-agnostic; the platform decides which model
# (Claude / Gemini / future providers) is actually used.
OPENCLAW_PROVIDER_ENV = "OPENCLAW_VISION_PROVIDER"   # "anthropic" | "google" | future
OPENCLAW_KEY_ENV      = "OPENCLAW_VISION_KEY"        # API key for that provider
OPENCLAW_MODEL_ENV    = "OPENCLAW_VISION_MODEL"      # optional model override


def _openclaw_vision_available() -> bool:
    """True iff the platform has injected both a provider name and a key."""
    return bool(
        os.environ.get(OPENCLAW_PROVIDER_ENV)
        and os.environ.get(OPENCLAW_KEY_ENV)
    )


def parse_with_openclaw(image_base64: str, media_type: str, timezone: str = "UTC") -> dict:
    """
    Use OpenClaw's configured vision LLM. The platform injects the provider
    name, key, and optional model override via env vars; we route to the
    matching provider function.

    No skill-level API key needed when this path is used — that is the whole
    point of openclaw mode.
    """
    provider_name = (os.environ.get(OPENCLAW_PROVIDER_ENV) or "").lower().strip()
    api_key       = os.environ.get(OPENCLAW_KEY_ENV)
    model_name    = os.environ.get(OPENCLAW_MODEL_ENV) or None

    if not provider_name or not api_key:
        raise RuntimeError(
            "OpenClaw has no vision-capable LLM configured for skills. "
            f"Either configure one at the platform level (which sets "
            f"{OPENCLAW_PROVIDER_ENV} and {OPENCLAW_KEY_ENV}), or set "
            f"GEMINI_API_KEY / ANTHROPIC_API_KEY and pick that provider "
            f"explicitly via --provider."
        )

    if provider_name == "anthropic":
        return parse_with_claude(image_base64, media_type, api_key, timezone, model=model_name)

    if provider_name == "google":
        return parse_with_gemini(image_base64, media_type, api_key, timezone, model=model_name)

    raise RuntimeError(
        f"OpenClaw vision provider '{provider_name}' is not supported by Scrask. "
        "Supported values: 'anthropic', 'google'."
    )


# ─── Provider router ───────────────────────────────────────────────────────────

def parse_screenshot(
    image_base64: str,
    media_type: str,
    provider: str,
    timezone: str = "UTC",
    claude_api_key: str | None = None,
    gemini_api_key: str | None = None,
) -> dict:
    provider = (provider or "auto").lower().strip()

    if provider == "openclaw":
        result = parse_with_openclaw(image_base64, media_type, timezone)
        result["_provider_used"]      = "openclaw"
        result["_fallback_triggered"] = False
        return result

    if provider == "claude":
        result = parse_with_claude(image_base64, media_type, claude_api_key, timezone)
        result["_provider_used"]      = "claude"
        result["_fallback_triggered"] = False
        return result

    if provider == "gemini":
        result = parse_with_gemini(image_base64, media_type, gemini_api_key, timezone)
        result["_provider_used"]      = "gemini"
        result["_fallback_triggered"] = False
        return result

    if provider == "auto":
        return _parse_with_auto(
            image_base64, media_type, timezone,
            gemini_api_key=gemini_api_key,
            claude_api_key=claude_api_key,
        )

    raise ValueError(
        f"Unknown provider '{provider}'. Choose 'auto', 'openclaw', 'claude', or 'gemini'."
    )


def _parse_with_auto(image_base64, media_type, timezone, gemini_api_key, claude_api_key):
    """
    Smart routing based on which credentials are available at runtime.

    Priority order:
      1. GEMINI_API_KEY set → Gemini-first with Claude fallback (the cheap+fast path).
         This is the existing v4.1 behaviour. Users who set up Gemini explicitly
         keep getting it.
      2. ANTHROPIC_API_KEY set (and no Gemini key) → Claude only. No point routing
         through OpenClaw if the user has already paid for direct Claude access.
      3. Neither → OpenClaw's configured vision LLM. Works out of the box for any
         user who has set up OpenClaw with a vision-capable LLM.
    """
    if gemini_api_key:
        return _parse_with_gemini_claude_fallback(
            image_base64, media_type, timezone,
            gemini_api_key=gemini_api_key,
            claude_api_key=claude_api_key,
        )

    if claude_api_key:
        result = parse_with_claude(image_base64, media_type, claude_api_key, timezone)
        result["_provider_used"]      = "claude"
        result["_fallback_triggered"] = False
        return result

    # No skill-level keys configured — defer to the platform.
    result = parse_with_openclaw(image_base64, media_type, timezone)
    result["_provider_used"]      = "openclaw"
    result["_fallback_triggered"] = False
    return result


def _parse_with_gemini_claude_fallback(image_base64, media_type, timezone, gemini_api_key, claude_api_key):
    gemini_result = parse_with_gemini(image_base64, media_type, gemini_api_key, timezone)
    gemini_items  = gemini_result.get("items", [])
    gemini_min    = _min_confidence(gemini_items)
    gemini_avg    = _avg_confidence(gemini_items)

    fallback_triggered = gemini_min < FALLBACK_THRESHOLD and bool(claude_api_key)

    if not fallback_triggered:
        gemini_result["_provider_used"]      = "gemini"
        gemini_result["_fallback_triggered"] = False
        gemini_result["_gemini_avg_conf"]    = round(gemini_avg, 3)
        return gemini_result

    try:
        claude_result = parse_with_claude(image_base64, media_type, claude_api_key, timezone)
        claude_avg    = _avg_confidence(claude_result.get("items", []))
    except Exception as e:
        gemini_result["_provider_used"]      = "gemini"
        gemini_result["_fallback_triggered"] = True
        gemini_result["_fallback_error"]     = f"Claude fallback failed: {e}"
        gemini_result["_gemini_avg_conf"]    = round(gemini_avg, 3)
        return gemini_result

    improvement = claude_avg - gemini_avg

    if improvement >= FALLBACK_IMPROVEMENT_MIN:
        claude_result["_provider_used"]      = "claude"
        claude_result["_fallback_triggered"] = True
        claude_result["_gemini_avg_conf"]    = round(gemini_avg, 3)
        claude_result["_claude_avg_conf"]    = round(claude_avg, 3)
        claude_result["_confidence_gain"]    = round(improvement, 3)
        return claude_result

    gemini_result["_provider_used"]      = "gemini"
    gemini_result["_fallback_triggered"] = True
    gemini_result["_fallback_outcome"]   = "gemini_retained"
    gemini_result["_gemini_avg_conf"]    = round(gemini_avg, 3)
    gemini_result["_claude_avg_conf"]    = round(claude_avg, 3)
    return gemini_result


def _item_confidence_values(item: dict) -> list[float]:
    """
    Collect every confidence-style score associated with one item:
    per-field `confidences{}` values, `type_confidence`, and the legacy
    item-level `confidence` if present. Used to compute min/avg across an
    entire parse result for auto-fallback decisions.
    """
    values: list[float] = []
    confidences = item.get("confidences") or {}
    for v in confidences.values():
        if isinstance(v, (int, float)):
            values.append(float(v))
    for key in ("type_confidence", "confidence"):
        v = item.get(key)
        if isinstance(v, (int, float)):
            values.append(float(v))
    return values


def _min_confidence(items: list[dict]) -> float:
    """Worst per-field (or per-decision) score across all items. Defaults to 1.0 if nothing is scored."""
    all_scores: list[float] = []
    for item in items:
        all_scores.extend(_item_confidence_values(item))
    return min(all_scores) if all_scores else 1.0


def _avg_confidence(items: list[dict]) -> float:
    """Average across every per-field and per-decision score in the result."""
    all_scores: list[float] = []
    for item in items:
        all_scores.extend(_item_confidence_values(item))
    if not all_scores:
        return 0.0
    return sum(all_scores) / len(all_scores)


def _clean_and_parse_json(raw: str) -> dict:
    cleaned = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(cleaned)


# ─── Intent shaping ────────────────────────────────────────────────────────────

def shape_intent(
    item: dict,
    confidence_threshold: float,
    type_threshold: float = TYPE_THRESHOLD,
    field_threshold: float = FIELD_THRESHOLD,
) -> dict:
    """
    Turn one raw model item into a normalized intent the OpenClaw agent can
    route to a destination skill.

    `destination` is the *kind* of skill needed, not a specific provider:
      - "calendar"  → calctl / accli / brainz-calendar / etc.
      - "task"      → apple-reminders / things-mac / notion / etc.

    Confidence handling:
      - Per-field confidences come from `item["confidences"]`.
      - The legacy per-item `confidence` (if the model emits one) is honoured;
        otherwise we synthesize it as `min(confidences.values())`.
      - `needs_confirmation` is now driven by the clarifications list: any
        outstanding clarification flips it true. `confidence_threshold` is kept
        as a final fallback for callers that pass an item with neither a
        `confidences` block nor a `confidence` value.
      - `clarifications` lists the specific things to ask the user about.
    """
    item_type   = item.get("type", "task")
    destination = "calendar" if item_type == "event" else "task"
    confidences = item.get("confidences") or {}

    # Legacy per-item confidence: honour model-emitted value, else derive.
    if "confidence" in item and isinstance(item["confidence"], (int, float)):
        confidence = float(item["confidence"])
    elif confidences:
        confidence = min(confidences.values())
    else:
        confidence = 0.0

    type_confidence = float(item.get("type_confidence", confidence))

    title = item.get("title") or "this item"
    clarifications: list[dict] = []

    # Type-level clarification first (so it leads the list in the bot UI).
    if type_confidence < type_threshold:
        clarifications.append({
            "field":    "type",
            "question": CLARIFICATION_QUESTIONS["type"].format(title=title),
            "reason":   "low_type_confidence",
        })

    # Per mandatory-field clarifications.
    mandatory = MANDATORY_FIELDS_BY_TYPE.get(item_type, MANDATORY_FIELDS_BY_TYPE["task"])
    for field in mandatory:
        value = item.get(field)
        is_missing = value is None or value == ""
        field_conf = confidences.get(field)

        if is_missing:
            reason = "missing"
        elif field_conf is not None and field_conf < field_threshold:
            reason = "low_confidence"
        else:
            continue

        template = CLARIFICATION_QUESTIONS.get(field, f"What is the {field}?")
        clarifications.append({
            "field":    field,
            "question": template.format(title=title),
            "reason":   reason,
        })

    # Final fallback: legacy per-item gate (only kicks in if no per-field info exists).
    needs_confirmation = bool(clarifications) or (
        not confidences and confidence < confidence_threshold
    )

    return {
        "type":                     item_type,
        "destination":              destination,
        "confidence":               confidence,
        "type_confidence":          type_confidence,
        "confidences":              confidences,
        "needs_confirmation":       needs_confirmation,
        "clarifications":           clarifications,
        "title":                    item.get("title"),
        "date":                     item.get("date"),
        "time":                     item.get("time"),
        "end_time":                 item.get("end_time"),
        "end_date":                 item.get("end_date"),
        "timezone_hint":            item.get("timezone_hint"),
        "location":                 item.get("location"),
        "online_link":              item.get("online_link"),
        "participants":             item.get("participants"),
        "recurrence":               item.get("recurrence", "none"),
        "recurrence_day":           item.get("recurrence_day"),
        "description":              item.get("description"),
        "priority":                 item.get("priority", "medium"),
        "source_type":              item.get("source_type"),
        "language":                 item.get("language"),
        "already_in_calendar_hint": item.get("already_in_calendar_hint", False),
    }


# ─── Human-readable summary ────────────────────────────────────────────────────

def format_summary(
    items: list[dict],
    parse_data: dict,
    provider: str,
    needs_actionable_confirmation: bool = False,
    actionable_confidence: float | None = None,
) -> str:
    """
    Chat-agnostic preview the agent can relay back to the user via whatever
    transport they came in on. The agent should send this verbatim.

    For confirm items, render the specific clarification questions emitted by
    shape_intent rather than a generic "is this right?" prompt.
    """
    if not items:
        return (
            "🤷 I couldn't find any event, reminder, or task in that screenshot.\n"
            "Could you describe what you'd like to add?"
        )

    lines = []

    if needs_actionable_confirmation:
        pct = f" ({int(actionable_confidence * 100)}% sure)" if actionable_confidence is not None else ""
        lines.append(f"🤔 Is this actually an event or task?{pct}")
        lines.append("Reply **yes** to continue, or **no** to skip.\n")

    silent  = [i for i in items if not i["needs_confirmation"]]
    confirm = [i for i in items if i["needs_confirmation"]]

    for i in silent:
        if i["destination"] == "calendar":
            when = f"{i.get('date', '')} at {i['time']}" if i.get("time") else i.get("date", "")
            lines.append(f"📅 Event: **{i['title']}** — {when}")
        else:
            due  = f" (due {i['date']})" if i.get("date") else ""
            icon = "🔔" if i.get("date") else "✅"
            lines.append(f"{icon} Task: **{i['title']}**{due}")

    for i in confirm:
        lines.append(f"\n🤔 Need a quick check on **{i['title'] or 'this one'}**")

        # Show what we got so far so the user has context.
        if i["destination"] == "calendar":
            lines.append("📅 Event so far:")
            lines.append(f"  Title: {i['title'] or '?'}")
            lines.append(f"  Date:  {i.get('date') or '?'}")
            lines.append(f"  Time:  {i.get('time') or '?'}")
            if i.get("location"):
                lines.append(f"  Where: {i['location']}")
            if i.get("online_link"):
                lines.append(f"  Link:  {i['online_link']}")
            if i.get("participants"):
                lines.append(f"  With:  {', '.join(i['participants'])}")
        else:
            icon  = "🔔" if i.get("date") else "✅"
            label = "Reminder" if i.get("date") else "Task"
            lines.append(f"{icon} {label} so far:")
            lines.append(f"  Title: {i['title'] or '?'}")
            if i.get("date"):
                lines.append(f"  Due:   {i['date']}")

        if i.get("description"):
            lines.append(f"  Note:  {i['description']}")

        # The actual clarification questions.
        clarifications = i.get("clarifications") or []
        if clarifications:
            lines.append("\nI need to confirm:")
            for c in clarifications:
                lines.append(f"  • {c['question']}")
            lines.append("\nReply with the details, or **skip** to drop this one.")
        else:
            lines.append("\nSave it? Reply **yes**, **edit**, or **skip**.")

    if parse_data.get("parse_notes"):
        lines.append(f"\n_ℹ️ {parse_data['parse_notes']}_")

    lines.append(f"\n_Parsed by Scrask using {provider.capitalize()}_")
    return "\n".join(lines).strip()


# ─── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrask Bot — parse screenshots into structured calendar/task intent."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--image-path",   help="Path to the screenshot file")
    group.add_argument("--image-base64", help="Base64-encoded image data")

    parser.add_argument(
        "--provider",
        choices=["auto", "openclaw", "claude", "gemini"],
        default=os.environ.get("VISION_PROVIDER", "auto"),
        help=(
            "'auto' (default) routes by what you have: GEMINI_API_KEY → "
            "Gemini-first with Claude fallback; else ANTHROPIC_API_KEY → "
            "Claude only; else 'openclaw' (the platform's configured vision "
            "LLM). 'openclaw' / 'claude' / 'gemini' pin a specific provider."
        ),
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Override API key. Defaults to ANTHROPIC_API_KEY / GEMINI_API_KEY env vars.",
    )
    parser.add_argument(
        "--timezone",
        default=os.environ.get("USER_TIMEZONE", "UTC"),
        help="IANA timezone (e.g. Asia/Kolkata)",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        help="Legacy per-item gate (default 0.75). The new behaviour uses field/type/actionable "
             "thresholds below — this one is kept for backward-compatible callers.",
    )
    parser.add_argument(
        "--actionable-threshold",
        type=float,
        default=ACTIONABLE_THRESHOLD,
        help="Below this top-level actionable_confidence the parser asks 'is this actually an "
             "event/task?' (default 0.70).",
    )
    parser.add_argument(
        "--type-threshold",
        type=float,
        default=TYPE_THRESHOLD,
        help="Below this per-item type_confidence the parser asks 'calendar or task list?' "
             "(default 0.70).",
    )
    parser.add_argument(
        "--field-threshold",
        type=float,
        default=FIELD_THRESHOLD,
        help="Per mandatory field: below this confidence (or null value) the parser asks a "
             "targeted clarification question for that field (default 0.70).",
    )
    parser.add_argument(
        "--media-type",
        default=None,
        help="Override media type (auto-detected from file extension if omitted)",
    )

    args = parser.parse_args()

    claude_api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    gemini_api_key = args.api_key or os.environ.get("GEMINI_API_KEY")

    openclaw_available = _openclaw_vision_available()

    if args.provider == "claude" and not claude_api_key:
        exit_error("Missing ANTHROPIC_API_KEY for Claude provider.")
    if args.provider == "gemini" and not gemini_api_key:
        exit_error("Missing GEMINI_API_KEY for Gemini provider.")
    if args.provider == "openclaw" and not openclaw_available:
        exit_error(
            "OpenClaw provider needs the platform to inject "
            f"{OPENCLAW_PROVIDER_ENV} and {OPENCLAW_KEY_ENV}. "
            "Either configure a vision LLM at the platform level, or pick "
            "a different --provider."
        )
    if args.provider == "auto" and not (gemini_api_key or claude_api_key or openclaw_available):
        exit_error(
            "Auto mode requires at least one of: GEMINI_API_KEY, "
            "ANTHROPIC_API_KEY, or a vision LLM configured at the OpenClaw "
            "platform level."
        )
    if args.provider == "auto" and gemini_api_key and not claude_api_key:
        print(
            "ℹ️  ANTHROPIC_API_KEY not set. Auto mode will use Gemini only (no Claude fallback).",
            file=sys.stderr,
        )
    if args.provider == "auto" and not gemini_api_key and not claude_api_key and openclaw_available:
        print(
            "ℹ️  Using OpenClaw's configured vision LLM. Set GEMINI_API_KEY for cheap+fast "
            "Gemini routing, or ANTHROPIC_API_KEY for direct Claude.",
            file=sys.stderr,
        )

    try:
        if args.image_path:
            p = Path(args.image_path)
            if not p.exists():
                exit_error(f"Image not found: {args.image_path}")
            media_type   = args.media_type or MIME_TYPES.get(p.suffix.lower(), "image/png")
            image_base64 = base64.standard_b64encode(p.read_bytes()).decode()
        else:
            image_base64 = args.image_base64
            media_type   = args.media_type or "image/png"
    except Exception as e:
        exit_error(f"Failed to load image: {e}")

    try:
        parse_data = parse_screenshot(
            image_base64, media_type, args.provider, args.timezone,
            claude_api_key=claude_api_key,
            gemini_api_key=gemini_api_key,
        )
    except json.JSONDecodeError as e:
        exit_error(f"Provider returned invalid JSON: {e}")
    except Exception as e:
        exit_error(f"Error during parsing: {e}")

    provider_used         = parse_data.get("_provider_used", args.provider)
    raw_items             = parse_data.get("items", [])
    actionable_confidence = parse_data.get("actionable_confidence")
    if not isinstance(actionable_confidence, (int, float)):
        actionable_confidence = None

    if parse_data.get("no_actionable_content") or not raw_items:
        print(json.dumps({
            "success":                       True,
            "no_actionable_content":         True,
            "provider":                      provider_used,
            "fallback_triggered":            parse_data.get("_fallback_triggered", False),
            "screenshot_summary":            parse_data.get("screenshot_summary", ""),
            "actionable_confidence":         actionable_confidence,
            "needs_actionable_confirmation": False,
            "items":                         [],
            "summary_text": (
                "🤷 I couldn't find any event, reminder, or task in that screenshot.\n"
                "Could you describe what you'd like to add?"
            ),
        }, indent=2, ensure_ascii=False))
        return

    items = [
        shape_intent(
            it,
            args.confidence_threshold,
            type_threshold=args.type_threshold,
            field_threshold=args.field_threshold,
        )
        for it in raw_items
    ]

    # Top-level "is this actually actionable?" gate. If the model emitted items
    # but is unsure the screenshot is actionable at all, flag it so the bot can
    # confirm before dispatching.
    needs_actionable_confirmation = (
        actionable_confidence is not None
        and actionable_confidence < args.actionable_threshold
    )

    print(json.dumps({
        "success":                       True,
        "no_actionable_content":         False,
        "provider":                      provider_used,
        "fallback_triggered":            parse_data.get("_fallback_triggered", False),
        "gemini_avg_confidence":         parse_data.get("_gemini_avg_conf"),
        "claude_avg_confidence":         parse_data.get("_claude_avg_conf"),
        "confidence_gain":               parse_data.get("_confidence_gain"),
        "screenshot_summary":            parse_data.get("screenshot_summary", ""),
        "actionable_confidence":         actionable_confidence,
        "needs_actionable_confirmation": needs_actionable_confirmation,
        "items_found":                   len(items),
        "items_needing_confirmation":    sum(1 for i in items if i["needs_confirmation"]),
        "items":                         items,
        "summary_text":                  format_summary(
            items, parse_data, provider_used,
            needs_actionable_confirmation=needs_actionable_confirmation,
            actionable_confidence=actionable_confidence,
        ),
        "parse_notes":                   parse_data.get("parse_notes"),
    }, indent=2, ensure_ascii=False))


def exit_error(message: str) -> None:
    sys.stderr.write(
        json.dumps({
            "success":      False,
            "error":        True,
            "message":      message,
            "summary_text": f"⚠️ Something went wrong: {message}",
        }) + "\n"
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
