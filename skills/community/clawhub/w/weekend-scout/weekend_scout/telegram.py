"""Telegram message formatting and sending for Weekend Scout.

Uses the Telegram Bot API directly via the requests library.
No async, no python-telegram-bot dependency.

Message length limit: 4096 characters per Telegram message.
If the message is longer, it is split at section boundaries.

Formatting: HTML parse_mode (not Markdown/MarkdownV2).
Only <, >, & need escaping via html.escape().
Supports: <b>bold</b>, <i>italic</i>, <a href="url">text</a>
"""

from __future__ import annotations

import datetime
import html
import re
from urllib.parse import quote
from typing import Any

import requests

TELEGRAM_MAX_LENGTH = 4096
TELEGRAM_API_BASE = "https://api.telegram.org"
DELIVERY_SEPARATOR = "--------------------"

# Hardcoded English month names — avoids locale-dependent strftime on Windows.
_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_TRIP_PREFIX_RE = re.compile(r"^(?:[A-Z]|\d+)\.\s+")
_ROUTE_ARROW_RE = re.compile(r"\s*(?:->|→)\s*")


def _day_abbr(iso_date: str) -> str:
    """Return short weekday abbreviation for an ISO date string."""
    d = datetime.date.fromisoformat(iso_date)
    return _DAYS[d.weekday()]


def _normalize_trip_name(name: str) -> str:
    """Strip any pre-numbered trip prefix so the formatter owns labeling."""
    return _TRIP_PREFIX_RE.sub("", name).strip()


def _date_range_label(saturday: str, sunday: str) -> str:
    sat = datetime.date.fromisoformat(saturday)
    sun = datetime.date.fromisoformat(sunday)
    month = _MONTHS[sat.month - 1]
    if sat.month == sun.month:
        return f"{month} {sat.day}-{sun.day}, {sat.year}"
    sun_month = _MONTHS[sun.month - 1]
    return f"{month} {sat.day} - {sun_month} {sun.day}, {sat.year}"


def _truncate_description(description: str, limit: int = 120) -> str:
    text = str(description or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _escape_markdown_text(text: str) -> str:
    return re.sub(r"([\\`*_{}\[\]()#+\-.!|>])", r"\\\1", text)


def _escape_markdown_link_url(url: str) -> str:
    return quote(url, safe=":/#?&=@[]!$&'*,;%-._~")


def _render_text(value: object, *, html_mode: bool) -> str:
    text = str(value or "")
    return html.escape(text) if html_mode else _escape_markdown_text(text)


def _render_title(text: str, *, html_mode: bool) -> str:
    rendered = _render_text(text, html_mode=html_mode)
    return f"<b>{rendered}</b>" if html_mode else f"**{rendered}**"


def _normalize_route(route: str) -> str:
    text = str(route or "").strip()
    if not text:
        return ""
    return _ROUTE_ARROW_RE.sub(" → ", text)


def _trip_route_summary(route: str) -> str:
    normalized = _normalize_route(route)
    if not normalized:
        return ""
    parts = [part.strip() for part in normalized.split(" → ") if part.strip()]
    if len(parts) >= 2:
        return parts[1]
    return normalized


def _event_day_time(event: dict[str, Any]) -> str:
    start_date = event.get("start_date") or ""
    end_date = event.get("end_date") or ""
    time_info = str(event.get("time_info") or "").strip()

    day_str = ""
    if start_date:
        day_str = _day_abbr(start_date)
        if end_date and end_date != start_date:
            day_str = f"{day_str}-{_day_abbr(end_date)}"

    return " ".join(part for part in (day_str, time_info) if part).strip()


def _normalize_free_entry(value: object) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if value == 1:
            return True
        if value == 0:
            return False

    text = str(value).strip().lower()
    if not text:
        return None

    if text in {"true", "yes", "y", "free", "gratis", "free entry", "free entrance"}:
        return True
    if text in {"false", "no", "n", "paid", "ticketed", "paid entry", "paid entrance"}:
        return False

    if "free" in text and "not free" not in text and "paid" not in text:
        return True
    if any(token in text for token in ("paid", "ticket", "bilet", "platn", "płatn")):
        return False
    return None


def _event_price_label(free_entry: object) -> str | None:
    normalized = _normalize_free_entry(free_entry)
    if normalized is True:
        return "✅ Free entrance"
    if normalized is False:
        return "💰 Paid entrance"
    return None


def _render_link_line(url: str, *, html_mode: bool) -> str | None:
    clean_url = str(url or "").strip()
    if not clean_url:
        return None
    if html_mode:
        return f'   🔗 <a href="{html.escape(clean_url)}">Details</a>'
    return f"   🔗 [Details]({_escape_markdown_link_url(clean_url)})"


def _build_event_lines(
    event: dict[str, Any],
    *,
    html_mode: bool,
    index: int | None = None,
) -> list[str]:
    lines: list[str] = []

    title_text = str(event.get("event_name") or "")
    if html_mode:
        if index is not None:
            title_text = f"{index}. {title_text}"
        title = _render_title(title_text, html_mode=True)
    else:
        if index is not None:
            title_text = f"{index}. {title_text}"
        title = _render_title(title_text, html_mode=False)
    lines.append(title)

    venue = str(event.get("location_name") or "").strip()
    if venue:
        lines.append(f"   📍 {_render_text(venue, html_mode=html_mode)}")

    schedule_parts: list[str] = []
    day_time = _event_day_time(event)
    if day_time:
        schedule_parts.append(_render_text(day_time, html_mode=html_mode))
    price = _event_price_label(event.get("free_entry"))
    if price:
        schedule_parts.append(price)
    if schedule_parts:
        lines.append(f"   🗓 {' • '.join(schedule_parts)}")

    description = _truncate_description(str(event.get("description") or ""))
    if description:
        lines.append(f"   {_render_text(description, html_mode=html_mode)}")

    link_line = _render_link_line(str(event.get("source_url") or ""), html_mode=html_mode)
    if link_line:
        lines.append(link_line)

    return lines


def _build_trip_lines(
    trip: dict[str, Any],
    *,
    html_mode: bool,
    index: int,
) -> list[str]:
    trip_name = _normalize_trip_name(str(trip.get("name") or ""))
    if html_mode:
        title = _render_title(f"{index:02d}. {trip_name}", html_mode=True)
    else:
        title = _render_title(f"{index:02d}. {trip_name}", html_mode=False)
    lines = [title]

    route = _trip_route_summary(str(trip.get("route") or ""))
    if route:
        lines.append(f"   📍 {_render_text(route, html_mode=html_mode)}")

    events_text = str(trip.get("events") or "").strip()
    if events_text:
        lines.append(f"   🎉 {_render_text(events_text, html_mode=html_mode)}")

    timing = str(trip.get("timing") or "").strip()
    if timing:
        lines.append(f"   🕒 {_render_text(timing, html_mode=html_mode)}")

    link_line = _render_link_line(str(trip.get("url") or ""), html_mode=html_mode)
    if link_line:
        lines.append(link_line)

    return lines


def _low_results_block(
    total: int,
    *,
    low_results_hint: bool,
    hint_max_searches: int,
    hint_max_fetches: int,
    html_mode: bool,
) -> str | None:
    if not low_results_hint:
        return None
    text = (
        f"Only {total} event(s) found. To discover more, increase your search budget:\n"
        f"python -m weekend_scout config max_searches {hint_max_searches}\n"
        f"python -m weekend_scout config max_fetches {hint_max_fetches}"
    )
    if html_mode:
        return f"<i>{text}</i>"
    return "\n".join(f"_{_escape_markdown_text(line)}_" for line in text.splitlines())


def _render_freeform_block(
    lines: list[str] | None,
    *,
    html_mode: bool,
    italic: bool = False,
) -> str | None:
    if not lines:
        return None
    rendered_lines: list[str] = []
    for line in lines:
        rendered = _render_text(line, html_mode=html_mode)
        if italic:
            rendered = f"<i>{rendered}</i>" if html_mode else f"_{rendered}_"
        rendered_lines.append(rendered)
    return "\n".join(rendered_lines)


def _compose_digest(
    home_city: str,
    saturday: str,
    sunday: str,
    city_events: list[dict[str, Any]],
    trip_options: list[dict[str, Any]],
    *,
    low_results_hint: bool,
    hint_max_searches: int,
    hint_max_fetches: int,
    html_mode: bool,
) -> str:
    date_range = _date_range_label(saturday, sunday)
    header = f"🗓 <b>Weekend Scout | {date_range}</b>" if html_mode else f"🗓 Weekend Scout | {date_range}"
    footer = "✨ <i>Scouted by Weekend Scout</i>" if html_mode else "✨ Scouted by Weekend Scout"

    sections: list[str] = [header]
    total = len(city_events) + len(trip_options)

    if not city_events and not trip_options:
        sections.append("No events found for this weekend.")
        hint = _low_results_block(
            0,
            low_results_hint=low_results_hint,
            hint_max_searches=hint_max_searches,
            hint_max_fetches=hint_max_fetches,
            html_mode=html_mode,
        )
        if hint:
            sections.append(hint)
        sections.append(footer)
        return "\n\n".join(sections)

    if city_events:
        home_section = f"🏙 In {_render_text(home_city, html_mode=html_mode)}"
        sections.append(f"<b>{home_section}</b>" if html_mode else home_section)
        for index, event in enumerate(city_events, 1):
            sections.append("\n".join(_build_event_lines(event, html_mode=html_mode, index=index)))

    if trip_options:
        trip_section = "🚗 Road Trips"
        sections.append(f"<b>{trip_section}</b>" if html_mode else trip_section)
        for index, trip in enumerate(trip_options, 1):
            sections.append("\n".join(_build_trip_lines(trip, html_mode=html_mode, index=index)))

    hint = _low_results_block(
        total,
        low_results_hint=low_results_hint,
        hint_max_searches=hint_max_searches,
        hint_max_fetches=hint_max_fetches,
        html_mode=html_mode,
    )
    if hint:
        sections.append(hint)

    sections.append(footer)
    return "\n\n".join(sections)


def _compose_markdown_preview(
    home_city: str,
    saturday: str,
    sunday: str,
    city_events: list[dict[str, Any]],
    trip_options: list[dict[str, Any]],
    *,
    low_results_hint: bool,
    hint_max_searches: int,
    hint_max_fetches: int,
) -> str:
    date_range = _date_range_label(saturday, sunday)
    header = f"**\U0001F5D3 Weekend Scout | {_escape_markdown_text(date_range)}**"
    footer = "_\U0001F331 Scouted by Weekend Scout_"

    sections: list[str] = [header]
    total = len(city_events) + len(trip_options)

    if not city_events and not trip_options:
        sections.append(_escape_markdown_text("No events found for this weekend."))
        hint = _low_results_block(
            0,
            low_results_hint=low_results_hint,
            hint_max_searches=hint_max_searches,
            hint_max_fetches=hint_max_fetches,
            html_mode=False,
        )
        if hint:
            sections.append(hint)
        sections.append(footer)
        return "\n\n".join(sections)

    if city_events:
        home_section = f"\U0001F3D9 In {_render_text(home_city, html_mode=False)}"
        sections.append(f"**{home_section}**")
        for index, event in enumerate(city_events, 1):
            sections.append("\n".join(_build_event_lines(event, html_mode=False, index=index)))

    if trip_options:
        trip_section = "\U0001F697 Road Trips"
        sections.append(f"**{trip_section}**")
        for index, trip in enumerate(trip_options, 1):
            sections.append("\n".join(_build_trip_lines(trip, html_mode=False, index=index)))

    hint = _low_results_block(
        total,
        low_results_hint=low_results_hint,
        hint_max_searches=hint_max_searches,
        hint_max_fetches=hint_max_fetches,
        html_mode=False,
    )
    if hint:
        sections.append(hint)

    sections.append(footer)
    return "\n\n".join(sections)


def split_message(message: str, max_length: int = TELEGRAM_MAX_LENGTH) -> list[str]:
    """Split a long message into parts at section boundaries.

    Splits prefer double-newline paragraph breaks, falling back to
    single newlines if necessary.

    Args:
        message: Full message text.
        max_length: Maximum character length per part.

    Returns:
        List of message part strings, each <= max_length characters.
    """
    if not message:
        return [""]
    if len(message) <= max_length:
        return [message]

    window = message[:max_length]

    # Prefer splitting at a paragraph break
    split_at = window.rfind("\n\n")
    if split_at == -1:
        # Fall back to any line break
        split_at = window.rfind("\n")
    if split_at == -1:
        # Hard split as last resort
        split_at = max_length

    head = message[:split_at].rstrip()
    tail = message[split_at:].lstrip()

    parts = [head] if head else []
    if tail:
        parts.extend(split_message(tail, max_length))
    return parts if parts else [""]


def _safe_error_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if len(text) > 200:
        return text[:197] + "..."
    return text


def _telegram_response_description(resp: object) -> str | None:
    json_reader = getattr(resp, "json", None)
    if callable(json_reader):
        try:
            payload = json_reader()
        except ValueError:
            payload = None
        if isinstance(payload, dict):
            description = _safe_error_text(payload.get("description"))
            if description:
                return description
    text = _safe_error_text(getattr(resp, "text", None))
    return text


def _network_error_code(exc: requests.RequestException) -> str:
    message = str(exc).lower()
    if isinstance(exc, requests.Timeout):
        return "telegram_timeout"
    if "10013" in message or "access permissions" in message:
        return "telegram_network_blocked"
    return "telegram_network_error"


def send_telegram(config: dict[str, Any], message: str) -> dict[str, Any]:
    """Send a message to the configured Telegram chat.

    Automatically splits messages longer than 4096 characters.

    Args:
        config: Loaded configuration dictionary (must contain
                telegram_bot_token and telegram_chat_id).
        message: Formatted message text (HTML).

    Returns:
        Structured send result with authoritative reason and safe diagnostics.
    """
    token = config.get("telegram_bot_token", "")
    chat_id = config.get("telegram_chat_id", "")

    if not token or not chat_id:
        missing = []
        if not token:
            missing.append("telegram_bot_token")
        if not chat_id:
            missing.append("telegram_chat_id")
        return {
            "sent": False,
            "reason": "telegram_not_configured",
            "error_code": "telegram_not_configured",
            "status_code": None,
            "error": f"Missing config: {', '.join(missing)}",
            "parts_sent": 0,
        }

    url = f"{TELEGRAM_API_BASE}/bot{token}/sendMessage"
    parts = split_message(message)
    parts_sent = 0

    try:
        for part in parts:
            resp = requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": part,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
                timeout=30,
            )
            if resp.status_code != 200:
                return {
                    "sent": False,
                    "reason": "send_failed",
                    "error_code": "telegram_http_error",
                    "status_code": resp.status_code,
                    "error": _telegram_response_description(resp) or f"HTTP {resp.status_code}",
                    "parts_sent": parts_sent,
                }
            json_reader = getattr(resp, "json", None)
            if callable(json_reader):
                try:
                    payload = json_reader()
                except ValueError:
                    return {
                        "sent": False,
                        "reason": "send_failed",
                        "error_code": "telegram_bad_response",
                        "status_code": resp.status_code,
                        "error": "Telegram returned a non-JSON success response",
                        "parts_sent": parts_sent,
                    }
                if isinstance(payload, dict) and payload.get("ok") is False:
                    return {
                        "sent": False,
                        "reason": "send_failed",
                        "error_code": "telegram_bad_response",
                        "status_code": resp.status_code,
                        "error": _safe_error_text(payload.get("description")) or "Telegram returned ok=false",
                        "parts_sent": parts_sent,
                    }
            parts_sent += 1
    except requests.RequestException as exc:
        return {
            "sent": False,
            "reason": "send_failed",
            "error_code": _network_error_code(exc),
            "status_code": None,
            "error": _safe_error_text(exc) or type(exc).__name__,
            "parts_sent": parts_sent,
        }

    return {
        "sent": True,
        "reason": "sent",
        "error_code": None,
        "status_code": None,
        "error": None,
        "parts_sent": len(parts),
    }


def format_event_block(event: dict[str, Any]) -> str:
    """Format a single event as a Telegram HTML message block.

    Args:
        event: Event dict from the cache (or with the same keys).

    Returns:
        Formatted HTML string block for the event (no leading number/letter).
    """
    return "\n".join(_build_event_lines(event, html_mode=True))


def format_scout_message(
    home_city: str,
    saturday: str,
    sunday: str,
    city_events: list[dict[str, Any]],
    trip_options: list[dict[str, Any]],
    stats_lines: list[str] | None = None,
    notes_lines: list[str] | None = None,
    low_results_hint: bool = False,
    hint_max_searches: int = 50,
    hint_max_fetches: int = 50,
) -> str:
    """Format the full Weekend Scout message as HTML.

    Args:
        home_city: Name of the home city.
        saturday: ISO date string of target Saturday.
        sunday: ISO date string of target Sunday.
        city_events: Top-ranked home city events (caller controls count).
        trip_options: Road trip option dicts (caller controls count).
            Each trip dict should have keys:
              name (str), route (str), events (str), timing (str).
            Optional: url (str) appended as [link] on the events line.
        stats_lines: Optional plain-text lines appended after the digest.
        notes_lines: Optional plain-text lines appended after the stats block.
        low_results_hint: When True, appends a hint suggesting the user
            increase the search budget.

    Returns:
        Fully formatted HTML message string.
    """
    sections: list[str] = [_compose_digest(
        home_city,
        saturday,
        sunday,
        city_events,
        trip_options,
        low_results_hint=low_results_hint,
        hint_max_searches=hint_max_searches,
        hint_max_fetches=hint_max_fetches,
        html_mode=True,
    )]
    stats_block = _render_freeform_block(stats_lines, html_mode=True, italic=True)
    if stats_block:
        sections.append(DELIVERY_SEPARATOR)
        sections.append(stats_block)
    notes_block = _render_freeform_block(notes_lines, html_mode=True, italic=True)
    if notes_block:
        sections.append(DELIVERY_SEPARATOR)
        sections.append(notes_block)
    return "\n\n".join(sections)


def format_scout_preview(
    home_city: str,
    saturday: str,
    sunday: str,
    city_events: list[dict[str, Any]],
    trip_options: list[dict[str, Any]],
    stats_lines: list[str] | None = None,
    notes_lines: list[str] | None = None,
    low_results_hint: bool = False,
    hint_max_searches: int = 50,
    hint_max_fetches: int = 50,
) -> str:
    """Format a markdown-ish preview of the scout digest for CLI/chat display."""
    sections: list[str] = [_compose_markdown_preview(
        home_city,
        saturday,
        sunday,
        city_events,
        trip_options,
        low_results_hint=low_results_hint,
        hint_max_searches=hint_max_searches,
        hint_max_fetches=hint_max_fetches,
    )]
    stats_block = _render_freeform_block(stats_lines, html_mode=False, italic=True)
    if stats_block:
        sections.append(DELIVERY_SEPARATOR)
        sections.append(stats_block)
    notes_block = _render_freeform_block(notes_lines, html_mode=False, italic=True)
    if notes_block:
        sections.append(DELIVERY_SEPARATOR)
        sections.append(notes_block)
    return "\n\n".join(sections)
