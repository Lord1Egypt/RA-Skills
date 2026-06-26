#!/usr/bin/env python3
"""
Query Vidau model list and capability config (scaleList, durationList, resolutionList).
Reads API key from env VIDAU_API_KEY or OpenClaw config ~/.openclaw/openclaw.json. Caches response for 10 minutes (env VIDAU_MODELS_CACHE or ~/.vidau_models_cache.json).
Prints full API JSON to stdout; use data[] and each item's model, scaleList, durationList, resolutionList, generateAudio for validation before create_task.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client
from typing import Optional
from urllib.error import URLError

API_BASE = "https://api.superaiglobal.com/v1"
MODELS_URL = f"{API_BASE}/models"
CACHE_TTL_SECONDS = 600  # 10 minutes


def _cache_path() -> str:
    return os.environ.get("VIDAU_MODELS_CACHE", os.path.expanduser("~/.vidau_models_cache.json"))


def _load_cached() -> Optional[dict]:
    p = _cache_path()
    if not os.path.isfile(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            obj = json.load(f)
        cached_at = obj.get("cachedAt", 0)
        if time.time() - cached_at > CACHE_TTL_SECONDS:
            return None
        return obj.get("response")
    except (OSError, json.JSONDecodeError, TypeError):
        return None


def _save_cache(response: dict) -> None:
    p = _cache_path()
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"cachedAt": time.time(), "response": response}, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query Vidau model list and capabilities. Cached 10 min. Requires env VIDAU_API_KEY."
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore cache and force refresh from API",
    )
    args = parser.parse_args()

    api_key = api_client.get_api_key()
    if not api_key:
        print(
            "Error: VIDAU_API_KEY is not set. Register at https://www.superaiglobal.com/ to get an API key, then configure apiKey or env.VIDAU_API_KEY in OpenClaw skills.entries.vidau.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.no_cache:
        cached = _load_cached()
        if cached is not None:
            print(json.dumps(cached, ensure_ascii=False))
            return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        raw, _ = api_client.api_request("GET", MODELS_URL, headers=headers, timeout=30)
        raw_str = raw.decode("utf-8")
        out = json.loads(raw_str)
        if out.get("code") != "200":
            print(
                f"API returned non-success: code={out.get('code')}, message={out.get('message', '')}",
                file=sys.stderr,
            )
            sys.exit(1)
        _save_cache(out)
        print(json.dumps(out, ensure_ascii=False))
    except api_client.APIError as e:
        try:
            err_json = json.loads(e.body)
            msg = err_json.get("message", e.body)
        except Exception:
            msg = e.body or str(e)
        print(f"HTTP {e.code}: {msg}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Response is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
