"""X (Twitter) source for SCRY skill.

Supports two backends:
1. Bird CLI (vendored) — uses browser cookies (AUTH_TOKEN/CT0)
2. xAI API — uses XAI_API_KEY with x_search tool

Bird is preferred (free, no API key). xAI is fallback.
"""

import json
import os
import re
import signal
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..source_base import Source, SourceMeta
from .. import http, query, dates

# Path to vendored Bird search
_BIRD_SEARCH_MJS = Path(__file__).resolve().parents[3] / "vendor" / "bird-search" / "bird-search.mjs"

# xAI endpoint
XAI_RESPONSES_URL = "https://api.x.ai/v1/responses"

DEPTH_CONFIG = {
    "quick": {"count": 12, "timeout": 30},
    "default": {"count": 30, "timeout": 45},
    "deep": {"count": 60, "timeout": 60},
}

XAI_DEPTH = {
    "quick": (8, 12),
    "default": (20, 30),
    "deep": (40, 60),
}

X_SEARCH_PROMPT = """You have access to real-time X (Twitter) data. Search for posts about: {topic}

Focus on posts from {from_date} to {to_date}. Find {min_items}-{max_items} high-quality, relevant posts.

IMPORTANT: Return ONLY valid JSON in this exact format, no other text:
{{
  "items": [
    {{
      "text": "Post text content (truncated if long)",
      "url": "https://x.com/user/status/...",
      "author_handle": "username",
      "date": "YYYY-MM-DD or null if unknown",
      "engagement": {{
        "likes": 100,
        "reposts": 25,
        "replies": 15,
        "quotes": 5
      }},
      "why_relevant": "Brief explanation of relevance",
      "relevance": 0.85
    }}
  ]
}}

Rules:
- relevance is 0.0 to 1.0 (1.0 = highly relevant)
- date must be YYYY-MM-DD format or null
- engagement can be null if unknown
- Include diverse voices/accounts if applicable
- Prefer posts with substantive content, not just links"""


def _log(msg: str):
    sys.stderr.write(f"[X] {msg}\n")
    sys.stderr.flush()


class XTwitterSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="x_twitter",
            display_name="X (Twitter)",
            tier=2,
            emoji="\U0001f535",
            id_prefix="XT",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["general", "tech", "news"],
        )

    def is_available(self, config):
        # Bird available if vendored .mjs exists + node installed
        if _BIRD_SEARCH_MJS.exists() and config.get("_has_node", False):
            return True
        # xAI API available if key set
        if config.get("XAI_API_KEY"):
            return True
        # Browser cookies
        if config.get("AUTH_TOKEN"):
            return True
        return False

    def _build_bird_env(self, config):
        """Build env dict for Bird subprocess with credentials."""
        env = os.environ.copy()
        if config.get("AUTH_TOKEN"):
            env["AUTH_TOKEN"] = config["AUTH_TOKEN"]
        if config.get("CT0"):
            env["CT0"] = config["CT0"]
        return env

    def _bird_search(self, search_query, count, timeout, config):
        """Run Bird vendored search. Returns list of raw tweet dicts."""
        cmd = [
            "node", str(_BIRD_SEARCH_MJS),
            search_query,
            "--count", str(count),
            "--json",
        ]

        preexec = os.setsid if hasattr(os, 'setsid') else None
        env = self._build_bird_env(config)

        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, preexec_fn=preexec, env=env,
            )
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                except (ProcessLookupError, PermissionError, OSError):
                    proc.kill()
                proc.wait(timeout=5)
                return {"error": f"Bird timeout after {timeout}s", "items": []}

            if proc.returncode != 0:
                error = stderr.strip() if stderr else "Bird search failed"
                return {"error": error, "items": []}

            output = stdout.strip() if stdout else ""
            if not output:
                return {"items": []}

            return json.loads(output)

        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON: {e}", "items": []}
        except Exception as e:
            return {"error": str(e), "items": []}

    def _parse_bird_response(self, response):
        """Parse Bird response into normalized item dicts."""
        items = []
        if "error" in response and response["error"]:
            _log(f"Bird error: {response['error']}")
            return items

        raw_items = response if isinstance(response, list) else response.get("items", response.get("tweets", []))
        if not isinstance(raw_items, list):
            return items

        for i, tweet in enumerate(raw_items):
            if not isinstance(tweet, dict):
                continue

            url = tweet.get("permanent_url") or tweet.get("url", "")
            if not url and tweet.get("id"):
                author_data = tweet.get("author", {}) or tweet.get("user", {})
                screen_name = author_data.get("username") or author_data.get("screen_name", "")
                if screen_name:
                    url = f"https://x.com/{screen_name}/status/{tweet['id']}"

            if not url:
                continue

            # Parse date
            item_date = None
            created_at = tweet.get("createdAt") or tweet.get("created_at", "")
            if created_at:
                try:
                    if len(created_at) > 10 and created_at[10] == "T":
                        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    else:
                        dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                    item_date = dt.strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    pass

            author_data = tweet.get("author", {}) or tweet.get("user", {})
            author_handle = (author_data.get("username") or
                             author_data.get("screen_name", "") or
                             tweet.get("author_handle", ""))

            engagement = {
                "likes": tweet.get("likeCount") or tweet.get("like_count") or tweet.get("favorite_count"),
                "reposts": tweet.get("retweetCount") or tweet.get("retweet_count"),
                "replies": tweet.get("replyCount") or tweet.get("reply_count"),
                "quotes": tweet.get("quoteCount") or tweet.get("quote_count"),
            }
            for key in engagement:
                if engagement[key] is not None:
                    try:
                        engagement[key] = int(engagement[key])
                    except (ValueError, TypeError):
                        engagement[key] = None

            items.append({
                "title": str(tweet.get("text", tweet.get("full_text", ""))).strip()[:500],
                "url": url,
                "author": author_handle.lstrip("@"),
                "date": item_date,
                "engagement": engagement if any(v is not None for v in engagement.values()) else None,
                "relevance": 0.7,
                "snippet": "",
            })

        return items

    def _xai_search(self, topic, from_date, to_date, depth, config):
        """Search via xAI API with x_search tool."""
        api_key = config.get("XAI_API_KEY", "")
        min_items, max_items = XAI_DEPTH.get(depth, XAI_DEPTH["default"])

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        timeout = 90 if depth == "quick" else 120 if depth == "default" else 180

        payload = {
            "model": "grok-3-mini",
            "tools": [{"type": "x_search"}],
            "input": [{
                "role": "user",
                "content": X_SEARCH_PROMPT.format(
                    topic=topic, from_date=from_date, to_date=to_date,
                    min_items=min_items, max_items=max_items,
                ),
            }],
        }

        response = http.post(XAI_RESPONSES_URL, payload, headers=headers, timeout=timeout)
        return self._parse_xai_response(response)

    def _parse_xai_response(self, response):
        """Parse xAI API response into normalized items."""
        items = []

        if "error" in response and response["error"]:
            error = response["error"]
            err_msg = error.get("message", str(error)) if isinstance(error, dict) else str(error)
            _log(f"xAI error: {err_msg}")
            return items

        output_text = ""
        if "output" in response:
            output = response["output"]
            if isinstance(output, str):
                output_text = output
            elif isinstance(output, list):
                for item in output:
                    if isinstance(item, dict):
                        if item.get("type") == "message":
                            for c in item.get("content", []):
                                if isinstance(c, dict) and c.get("type") == "output_text":
                                    output_text = c.get("text", "")
                                    break
                        elif "text" in item:
                            output_text = item["text"]
                    elif isinstance(item, str):
                        output_text = item
                    if output_text:
                        break

        if not output_text and "choices" in response:
            for choice in response["choices"]:
                if "message" in choice:
                    output_text = choice["message"].get("content", "")
                    break

        if not output_text:
            return items

        json_match = re.search(r'\{[\s\S]*"items"[\s\S]*\}', output_text)
        if json_match:
            try:
                data = json.loads(json_match.group())
                raw_items = data.get("items", [])
            except json.JSONDecodeError:
                return items
        else:
            return items

        for i, item in enumerate(raw_items):
            if not isinstance(item, dict):
                continue
            url = item.get("url", "")
            if not url:
                continue

            eng = None
            eng_raw = item.get("engagement")
            if isinstance(eng_raw, dict):
                eng = {
                    "likes": int(eng_raw["likes"]) if eng_raw.get("likes") else None,
                    "reposts": int(eng_raw["reposts"]) if eng_raw.get("reposts") else None,
                    "replies": int(eng_raw["replies"]) if eng_raw.get("replies") else None,
                    "quotes": int(eng_raw["quotes"]) if eng_raw.get("quotes") else None,
                }

            date_val = item.get("date")
            if date_val and not re.match(r'^\d{4}-\d{2}-\d{2}$', str(date_val)):
                date_val = None

            items.append({
                "title": str(item.get("text", "")).strip()[:500],
                "url": url,
                "author": str(item.get("author_handle", "")).strip().lstrip("@"),
                "date": date_val,
                "engagement": eng,
                "relevance": min(1.0, max(0.0, float(item.get("relevance", 0.5)))),
                "snippet": str(item.get("why_relevant", "")),
            })

        return items

    def search(self, topic, from_date, to_date, depth, config):
        dc = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
        core = query.extract_core_subject(topic)

        # Strategy 1: Bird (vendored, free, no API key)
        if _BIRD_SEARCH_MJS.exists() and shutil.which("node"):
            search_query = f"{core} since:{from_date}"
            _log(f"Bird search: {search_query}")
            response = self._bird_search(search_query, dc["count"], dc["timeout"], config)
            items = self._parse_bird_response(response)

            # Retry with fewer keywords if 0 results
            core_words = core.split()
            if not items and len(core_words) > 2:
                shorter = ' '.join(core_words[:2])
                _log(f"Retrying with: {shorter}")
                response = self._bird_search(f"{shorter} since:{from_date}", dc["count"], dc["timeout"], config)
                items = self._parse_bird_response(response)

            if items:
                return items

        # Strategy 2: xAI API
        if config.get("XAI_API_KEY"):
            _log("Falling back to xAI API")
            return self._xai_search(topic, from_date, to_date, depth, config)

        return []


def get_source():
    return XTwitterSource()
