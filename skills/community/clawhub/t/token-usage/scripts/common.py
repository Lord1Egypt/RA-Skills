"""Shared session parsing and model handling for token-usage reports."""

import gzip
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL_TZ_NAME = "Asia/Calcutta"
LOCAL_TZ = ZoneInfo(LOCAL_TZ_NAME)


def normalize_model(model):
    """Return a stable provider/model name for pricing and reports."""
    value = (model or "unknown").strip().lower()
    aliases = {
        # Kimi models
        "k2.6": "kimi/k2.6", "k2.7": "kimi/k2.7", "k2.7-code": "kimi/k2.7-code",
        "k3": "kimi/k3", "k3-1m": "kimi/k3-1m",
        # OpenAI/GPT models (session logs often store bare names)
        "gpt-5.6-luna": "openai/gpt-5.6-luna",
        "gpt-5.6-luna-pro": "openai/gpt-5.6-luna-pro",
        "gpt-5.6-terra": "openai/gpt-5.6-terra",
        "gpt-5.6-terra-pro": "openai/gpt-5.6-terra-pro",
        "gpt-5.6-sol-pro": "openai/gpt-5.6-sol-pro",
        "gpt-5.4": "openai/gpt-5.4",
        "gpt-5.4-mini": "openai/gpt-5.4-mini",
        "gpt-5.4-nano": "openai/gpt-5.4-nano",
        "gpt-4o": "openai/gpt-4o",
        "gpt-4o-mini": "openai/gpt-4o-mini",
        # Anthropic models
        "claude-sonnet-4.5": "anthropic/claude-sonnet-4.5",
        "claude-opus-5": "anthropic/claude-opus-5",
        # Google models
        "gemini-3.7-flash": "google/gemini-3.7-flash",
        "gemini-3.6-flash": "google/gemini-3.6-flash",
        "gemini-3.5-flash": "google/gemini-3.5-flash",
        # DeepSeek
        "deepseek-v4": "deepseek/deepseek-v4",
        "deepseek-v4-pro": "deepseek/deepseek-v4-pro",
        # Qwen
        "qwen3.8-max": "qwen/qwen3.8-max",
        "qwen3.8-27b": "qwen/qwen3.8-27b",
    }
    return aliases.get(value, value)


def local_timestamp(timestamp):
    """Return a timestamp in local time for grouping and filtering."""
    if not timestamp:
        return ""
    try:
        value = timestamp.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(LOCAL_TZ).replace(tzinfo=None).isoformat(timespec="seconds")
    except ValueError:
        return timestamp


def local_date(timestamp):
    return local_timestamp(timestamp)[:10] if timestamp else "unknown"


def find_sessions():
    roots = [
        Path.home() / ".openclaw" / "agents" / "main" / "sessions",
        Path.home() / ".openclaw" / "agents" / "sub" / "sessions",
        Path.home() / ".openclaw" / "agents" / "main" / "agent" / "codex-home" / "sessions",
    ]
    files = []
    for root in roots:
        if root.exists():
            files.extend(root.rglob("*.jsonl"))
            files.extend(root.rglob("*.jsonl.gz"))
            files.extend(root.rglob("*.jsonl.*.zst"))
    return sorted(set(files))


def _model_from_context(payload):
    return payload.get("model", "") or ""


def _zstd_open(path, mode="rt", encoding="utf-8", errors="replace"):
    """Open a zstd-compressed file for text reading via subprocess."""
    import io
    proc = subprocess.Popen(
        ["zstd", "-dc", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return io.TextIOWrapper(proc.stdout, encoding=encoding, errors=errors)


def parse_session(path):
    """Yield timestamp, normalized model, and per-turn token usage."""
    path_str = str(path)
    if path_str.endswith(".zst"):
        opener = _zstd_open
    elif path_str.endswith(".gz"):
        opener = gzip.open
    else:
        opener = open
    codex_model = ""
    try:
        with opener(path, "rt", encoding="utf-8", errors="replace") as stream:
            for raw in stream:
                try:
                    record = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if record.get("type") == "turn_context":
                    codex_model = _model_from_context(record.get("payload", {})) or codex_model
                    continue
                if record.get("type") == "event_msg":
                    payload = record.get("payload", {})
                    if payload.get("type") != "token_count":
                        continue
                    usage = (payload.get("info") or {}).get("last_token_usage") or {}
                    if usage:
                        yield record.get("timestamp", ""), normalize_model(codex_model or "openai/gpt-5.6-luna"), {
                            "input": usage.get("input_tokens", 0),
                            "output": usage.get("output_tokens", 0),
                            "cacheRead": usage.get("cached_input_tokens", 0),
                            "cacheWrite": usage.get("cache_write_input_tokens", 0),
                        }
                    continue
                if record.get("type") != "message":
                    continue
                message = record.get("message", {})
                if message.get("role") != "assistant":
                    continue
                usage = message.get("usage") or record.get("usage")
                if usage:
                    model = message.get("model") or record.get("model") or record.get("api")
                    yield record.get("timestamp", ""), normalize_model(model), usage
    except (FileNotFoundError, OSError):
        return


def estimate_cost(usage, model, pricing):
    """Estimate cost; return None when the model has no known price."""
    rates = pricing.get(normalize_model(model))
    if rates is None:
        return None
    total = usage.get("input", 0) * (rates.get("input") or 0)
    total += usage.get("output", 0) * (rates.get("output") or 0)
    total += usage.get("cacheRead", 0) * (rates.get("cache_read") or 0)
    total += usage.get("cacheWrite", 0) * (rates.get("cache_write") or 0)
    return total / 1e6
