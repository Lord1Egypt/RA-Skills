#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List
from urllib import error, request

TAVILY_URL = "https://api.tavily.com/search"


def _load_api_key() -> str | None:
    key = (os.environ.get("TAVILY_API_KEY") or "").strip()
    if key:
        return key

    env_path = Path.home() / ".openclaw" / ".env"
    if not env_path.exists():
        return None

    try:
        txt = env_path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^\s*TAVILY_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
        if not m:
            return None
        v = m.group(1).strip().strip('"').strip("'")
        return v or None
    except Exception:
        return None


def search(query: str, max_results: int = 5, timeout: float = 20.0) -> List[Dict[str, str]]:
    """Search Tavily and return [{title, url, snippet}].

    Never raises; returns [] on any failure.
    """
    q = (query or "").strip()
    if not q:
        return []

    key = _load_api_key()
    if not key:
        return []

    payload = {
        "api_key": key,
        "query": q,
        "max_results": max(1, min(int(max_results or 5), 10)),
        "search_depth": "basic",
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        TAVILY_URL,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )

    # Light retry for transient network/server/rate-limit failures.
    last_body = ""
    for attempt in range(3):
        try:
            with request.urlopen(req, timeout=max(1.0, float(timeout or 20.0))) as resp:
                last_body = resp.read().decode("utf-8", errors="replace")
            break
        except error.HTTPError as exc:
            status = int(getattr(exc, "code", 0) or 0)
            body = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
            last_body = body
            if status in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(0.8 * (attempt + 1))
                continue
            return []
        except (error.URLError, TimeoutError):
            if attempt < 2:
                time.sleep(0.8 * (attempt + 1))
                continue
            return []
        except Exception:
            return []

    try:
        obj = json.loads(last_body or "{}")
    except Exception:
        return []

    # Tavily sometimes returns explicit error payloads with HTTP 200.
    if obj.get("error") or obj.get("detail"):
        return []

    out: List[Dict[str, str]] = []
    for item in (obj.get("results") or [])[: payload["max_results"]]:
        out.append(
            {
                "title": str(item.get("title") or "").strip(),
                "url": str(item.get("url") or "").strip(),
                "snippet": str(item.get("content") or "").strip(),
            }
        )
    return out
