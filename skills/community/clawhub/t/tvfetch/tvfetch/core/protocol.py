"""
TradingView WebSocket framing protocol.

Every message uses this custom format:
    ~m~<byte_length>~m~<payload>

Multiple messages may arrive in one WebSocket frame, concatenated:
    ~m~42~m~{"m":"foo","p":[]}~m~15~m~{"m":"bar","p":[]}

Heartbeat pings look like:
    ~m~3~m~~h~0
These must be echoed back immediately or TV closes the connection.
"""

from __future__ import annotations

import json
import re

_FRAME_PATTERN = re.compile(r"~m~\d+~m~(.*?)(?=~m~\d+~m~|$)", re.DOTALL)
_HEARTBEAT_PATTERN = re.compile(r"~m~\d+~m~(~h~\d+)")


def encode(payload: str) -> str:
    """Wrap a string payload in TradingView's ~m~ framing."""
    return f"~m~{len(payload)}~m~{payload}"


def encode_json(obj: dict) -> str:
    """Serialise a dict to JSON, then wrap in ~m~ framing."""
    return encode(json.dumps(obj))


def decode(raw: str) -> list[str]:
    """
    Extract all payload strings from a raw WebSocket frame.
    Returns a list — one entry per embedded ~m~ packet.
    """
    return [m.group(1) for m in _FRAME_PATTERN.finditer(raw) if m.group(1).strip()]


def decode_json(raw: str) -> list[dict]:
    """
    Extract and parse all JSON payloads from a raw WebSocket frame.
    Non-JSON payloads (heartbeats) are silently skipped.
    """
    result: list[dict] = []
    for payload in decode(raw):
        try:
            result.append(json.loads(payload))
        except json.JSONDecodeError:
            pass
    return result


def is_heartbeat(raw: str) -> bool:
    """Return True if the raw frame contains a heartbeat ping."""
    return "~h~" in raw


def extract_heartbeat(raw: str) -> str | None:
    """Return the heartbeat payload to echo back, or None if not a heartbeat."""
    m = _HEARTBEAT_PATTERN.search(raw)
    return encode(m.group(1)) if m else None
