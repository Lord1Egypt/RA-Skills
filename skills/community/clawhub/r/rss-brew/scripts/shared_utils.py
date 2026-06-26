#!/usr/bin/env python3
"""Shared helpers for RSS-Brew v2 orchestration scripts."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from urllib import request
import subprocess
from uuid import uuid4


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def parse_dt(value: str) -> datetime:
    if not value:
        return datetime.min
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return datetime.min


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "")).strip()
    return text


def truncate_cn_note(text: str, min_len: int = 160, max_len: int = 220) -> str:
    s = clean_text(text)
    if not s:
        return "（无可用摘要）"
    if len(s) <= max_len:
        return s
    clipped = s[:max_len].rstrip(" ，,。.!?；;:")
    if len(clipped) < min_len and len(s) > min_len:
        clipped = s[:min_len]
    return clipped + "…"


def slugify(title: str) -> str:
    s = (title or "untitled").lower().strip()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80] or "untitled"


def _extract_last_json_object(text: str) -> str:
    """Extract the last complete top-level JSON object from mixed stdout."""

    objects: List[str] = []
    depth = 0
    start = -1
    in_str = False
    escaped = False

    for i, ch in enumerate(text):
        if in_str:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_str = False
            continue

        if ch == '"':
            in_str = True
            continue

        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    objects.append(text[start : i + 1])
                    start = -1

    if not objects:
        raise RuntimeError("Could not isolate final JSON object from openclaw output")
    return objects[-1]


def _vertex_completion(model_id: str, system_prompt: str, user_prompt: str) -> str:
    """Direct Vertex AI SDK call. Bypasses openclaw agent entirely."""
    import vertexai
    from vertexai.generative_models import GenerativeModel, Content, Part
    import os

    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=project, location=location)

    model = GenerativeModel(
        model_id,
        system_instruction=system_prompt,
    )
    resp = model.generate_content(user_prompt + "\n\nReturn ONLY the JSON.")
    return resp.text


def openclaw_agent_completion(model_alias: str, system_prompt: str, user_prompt: str, timeout: int = 600) -> str:
    """Call the appropriate LLM backend based on model alias.

    Vertex models are called directly via SDK (avoids openclaw agent limitations).
    Other models fall through to openclaw agent CLI.
    """
    # Route Vertex models directly to SDK — openclaw /model routing is broken for these
    _VERTEX_MODELS = {
        "VERTEX_PRO": "gemini-2.5-pro",
        "VERTEX_FAST": "gemini-2.5-flash",
        "VERTEX_FLASH_LITE": "gemini-2.5-flash-lite",
    }
    if model_alias in _VERTEX_MODELS:
        return _vertex_completion(_VERTEX_MODELS[model_alias], system_prompt, user_prompt)

    # For non-Vertex models, use openclaw agent CLI (two-step: switch then prompt)
    session_id = f"rss-brew-{model_alias.lower()}-{int(datetime.utcnow().timestamp())}-{uuid4().hex[:8]}"

    def _run(message: str, t: int) -> str:
        cmd = [
            "/usr/bin/openclaw", "agent", "--local",
            "--session-id", session_id,
            "--message", message,
            "--json", "--timeout", str(t),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=t + 30)
        if res.returncode != 0:
            raise RuntimeError(f"openclaw agent failed ({res.returncode}): {res.stderr.strip()[:400]}")
        return (res.stdout + res.stderr).strip()

    # Step 1: switch model
    _run(f"/model {model_alias}", 30)
    # Step 2: actual prompt
    out = _run(f"SYSTEM:\n{system_prompt}\n\nUSER:\n{user_prompt}\n\nReturn ONLY the JSON.", timeout)

    payload = json.loads(_extract_last_json_object(out))
    payloads = payload.get("payloads") or []
    if not payloads or not isinstance(payloads, list):
        raise RuntimeError("openclaw agent returned no text payload")
    text = None
    for p in payloads:
        t = p.get("text", "").strip()
        if t:
            text = t
            break
    if not text:
        raise RuntimeError("openclaw agent returned no text payload")
    return text


# Backward compat: keep old name used by Phase-A/B scripts.
chat_completion = openclaw_agent_completion


def latest_run_stats(run_stats_dir: Path) -> Dict[str, Any]:
    if not run_stats_dir.exists():
        return {}
    files = sorted(run_stats_dir.glob("run-stats-*.json"))
    if not files:
        return {}
    return load_json(files[-1], {})


def sort_by_score_then_published(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        items,
        key=lambda x: (int(x.get("score", 0)), parse_dt(x.get("published", ""))),
        reverse=True,
    )
