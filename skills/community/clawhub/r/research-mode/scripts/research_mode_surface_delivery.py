from __future__ import annotations

from typing import Any

DELIVERY_CHANNEL_ADDRESSING_ERROR = "delivery_channel_addressing_failed"
DELIVERY_NOTIFICATION_ERROR = "delivery_notification_failed"


CHANNEL_LIMITS = {
    "telegram": {
        "message_chars": 4096,
        "summary_first": True,
        "max_inline_items": 10,
    },
    "discord": {
        "message_chars": 2000,
        "summary_first": True,
        "max_inline_items": 15,
    },
    "mattermost": {
        "message_chars": 4000,
        "summary_first": True,
        "max_inline_items": 15,
    },
    "email": {
        "message_chars": None,
        "summary_first": False,
        "max_inline_items": None,
    },
    "file": {
        "message_chars": None,
        "summary_first": False,
        "max_inline_items": None,
    },
}

DELIVERY_PRESETS = {
    "telegram": {
        "strategy": "summary_first",
        "recommendations": [
            "Provide concise summary (2-3 sentences)",
            "If deliverable is a file, say 'see attached'",
            "Use bullets sparingly (max 5-7 items inline)",
            "If longer content needed, suggest '/path/to/file'",
        ],
    },
    "discord": {
        "strategy": "summary_first",
        "recommendations": [
            "Use Discord markdown formatting",
            "Prefer compact blocks with key info",
            "Link to full report as attachment or file",
            "Use spoilers for lengthy details",
        ],
    },
    "mattermost": {
        "strategy": "summary_first",
        "recommendations": [
            "Use concise Mattermost markdown",
            "Lead with the current status and next useful action",
            "Keep inline updates compact and link or attach full artifacts",
            "Avoid fragmented multi-message updates unless splitting is required",
        ],
    },
    "email": {
        "strategy": "report_first",
        "recommendations": [
            "Start with brief intro/context",
            "Include structured sections",
            "Executive summary at top",
            "Attach supporting files if large",
        ],
    },
    "file": {
        "strategy": "file_first",
        "recommendations": [
            "Full report as primary artifact",
            "Include metadata and provenance",
            "Keep human-readable structure",
            "Consider appendices for detail",
        ],
    },
}


def classify_delivery_error(error: str | None) -> str | None:
    text = str(error or "").strip().lower()
    if not text:
        return None
    return DELIVERY_NOTIFICATION_ERROR


def notification_target_shape(target: dict[str, Any] | None) -> dict[str, Any]:
    target = target or {}
    return {
        "channel": target.get("channel"),
        "has_chat_id": bool(target.get("chat_id")),
        "has_thread_id": bool(target.get("thread_id")),
        "has_topic_id": bool(target.get("topic_id")),
    }


def get_channel_profile(channel: str) -> dict[str, Any]:
    channel_lower = str(channel).lower().strip()
    return DELIVERY_PRESETS.get(channel_lower, DELIVERY_PRESETS["file"])


def get_channel_limits(channel: str) -> dict[str, Any]:
    channel_lower = str(channel).lower().strip()
    return CHANNEL_LIMITS.get(channel_lower, CHANNEL_LIMITS["file"])


def needs_splitting(content: str, channel: str) -> bool:
    limits = get_channel_limits(channel)
    max_chars = limits.get("message_chars")
    if max_chars is None:
        return False
    return len(content) > max_chars


def split_for_channel(content: str, channel: str) -> list[str]:
    limits = get_channel_limits(channel)
    max_chars = limits.get("message_chars")
    max_items = limits.get("max_inline_items")

    if max_chars is None:
        return [content]

    if len(content) <= max_chars:
        return [content]

    lines = content.split("\n")
    chunks: list[str] = []
    current_chunk = ""
    truncated = False

    def append_chunk(chunk: str) -> bool:
        nonlocal truncated
        if not chunk:
            return True
        if max_items and len(chunks) >= max_items:
            truncated = True
            return False
        chunks.append(chunk.rstrip())
        return True

    for line in lines:
        line_len = len(line) + 1
        if line_len > max_chars:
            if current_chunk:
                if not append_chunk(current_chunk):
                    break
                current_chunk = ""
            remaining = line
            while remaining:
                if not append_chunk(remaining[:max_chars]):
                    break
                remaining = remaining[max_chars:]
            if truncated:
                break
            continue
        if len(current_chunk) + line_len > max_chars:
            if current_chunk:
                if not append_chunk(current_chunk):
                    break
            if truncated:
                break
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk and not truncated:
        append_chunk(current_chunk)

    if truncated:
        chunks.append("[...] (content truncated)")

    return chunks


def format_for_channel(
    content: str,
    channel: str,
    *,
    summary: str | None = None,
    deliverable_path: str | None = None,
) -> dict[str, Any]:
    profile = get_channel_profile(channel)
    strategy = profile.get("strategy", "file_first")

    needs_split = needs_splitting(content, channel)
    chunks = split_for_channel(content, channel) if needs_split else [content]

    result: dict[str, Any] = {
        "channel": channel,
        "strategy": strategy,
        "needs_splitting": needs_split,
        "chunks": chunks,
        "chunk_count": len(chunks),
        "recommendations": profile.get("recommendations", []),
    }

    if summary and strategy == "summary_first":
        result["summary"] = summary[:500]
        result["has_summary"] = True

    if deliverable_path:
        result["deliverable_path"] = deliverable_path
        result["delivery_hint"] = f"See attached: {deliverable_path}"

    return result


def suggest_channel_strategy(deliverable_type: str | None) -> str:
    return "file_first"
