#!/usr/bin/env python3
"""video-insight LLM module: opt-in summarization via OpenClaw Gateway."""

import os
import json
from typing import Optional

from utils import progress, load_settings, get_setting

SETTINGS = load_settings()

# ──────────────────────────────────────────────
# Summary prompt — loadable from external file
# ──────────────────────────────────────────────

DEFAULT_PROMPT = """You are a professional content analyst. Generate a structured, in-depth summary for this video transcript.

Video Title: {title}
Channel: {channel}
Duration: {duration}

Transcript:
{transcript}

Output format:

### 🎯 Core Topic
- What problem/topic does this video address?

### 💡 Key Points (2-3 sentences each)
1. **Point 1**: ...
2. **Point 2**: ...
3. **Point 3**: ...

### 🛠️ Actionable Takeaways
1. ...
2. ...

### ⚠️ Caveats & Limitations
- ...

### 📊 One-line Summary
- ..."""


def _load_prompt_template() -> str:
    """Load prompt from external file if exists, else use default."""
    from pathlib import Path
    skill_root = Path(__file__).resolve().parent.parent
    prompt_file = skill_root / "config" / "prompt.md"
    if prompt_file.exists():
        try:
            return prompt_file.read_text(encoding="utf-8")
        except Exception:
            pass
    return DEFAULT_PROMPT


def _call_llm(api_url: str, api_key: str, model: str, prompt: str, timeout: int = 120) -> Optional[str]:
    """Call an OpenAI-compatible chat API."""
    try:
        import requests
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        response = requests.post(
            api_url,
            headers=headers,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000,
            },
            timeout=timeout,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        progress(f"  ⚠️  LLM API error: {response.status_code} {response.text[:200]}")
    except Exception as e:
        progress(f"  ⚠️  LLM call error: {e}")
    return None


def generate_summary(
    title: str,
    channel: str,
    duration_seconds: int,
    transcript: str,
) -> Optional[str]:
    """Generate summary using LLM (single backend: env-configured or OpenClaw Gateway).

    This is opt-in only (--summarize flag). By default the agent does its own summarization.

    Backend resolution:
      1. LLM_API_URL + LLM_API_KEY env vars
      2. OPENCLAW_GATEWAY_TOKEN → localhost gateway
      3. Give up (no multi-fallback chain)
    """
    template = _load_prompt_template()

    # Format duration
    mins = duration_seconds // 60
    secs = duration_seconds % 60
    duration_str = f"{mins}:{secs:02d}" if duration_seconds > 0 else "unknown"

    prompt = template.format(
        title=title,
        channel=channel,
        duration=duration_str,
        transcript=transcript,  # Full transcript, no truncation
    )

    # Backend 1: explicit env
    env_url = os.environ.get("LLM_API_URL")
    env_key = os.environ.get("LLM_API_KEY")
    env_model = os.environ.get("LLM_MODEL", "gpt-4o-mini")

    if env_url and env_key:
        progress(f"  🔑 LLM: {env_url}")
        result = _call_llm(env_url, env_key, env_model, prompt)
        if result:
            return result

    # Backend 2: OpenClaw Gateway
    oc_token = os.environ.get("OPENCLAW_GATEWAY_TOKEN")
    if oc_token:
        gw_url = env_url or "http://localhost:18789/v1/chat/completions"
        progress(f"  🔑 LLM: OpenClaw Gateway → {gw_url}")
        result = _call_llm(gw_url, oc_token, env_model, prompt)
        if result:
            return result

    progress("  ⚠️  No LLM backend available. Skipping summary.")
    return None
