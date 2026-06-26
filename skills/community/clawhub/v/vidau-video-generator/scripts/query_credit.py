#!/usr/bin/env python3
"""
Query current Vidau account credits. Reads API key from env VIDAU_API_KEY or OpenClaw config.
Prints API JSON to stdout with data.userId, data.availableCredit.
"""
import argparse
import json
import os
import sys

# Ensure api_client in same directory can be imported when script is run directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client
from urllib.error import HTTPError, URLError

API_BASE = "https://api.superaiglobal.com/v1"
QUERY_CREDIT_URL = f"{API_BASE}/queryCredit"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query Vidau account credits. Requires env VIDAU_API_KEY."
    )
    parser.parse_args()

    api_key = api_client.get_api_key()
    if not api_key:
        print(
            "Error: VIDAU_API_KEY is not set. Register at https://www.superaiglobal.com/ to get an API key, then configure apiKey or env.VIDAU_API_KEY in OpenClaw skills.entries.vidau.",
            file=sys.stderr,
        )
        sys.exit(1)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        raw, _ = api_client.api_request(
            "GET", QUERY_CREDIT_URL, headers=headers, timeout=30
        )
        raw_str = raw.decode("utf-8")
        print(raw_str)
        out = json.loads(raw_str)
        if out.get("code") != "200":
            print(f"API returned non-success: code={out.get('code')}, message={out.get('message', '')}", file=sys.stderr)
            sys.exit(1)
    except api_client.APIError as e:
        try:
            err_json = json.loads(e.body)
            print(f"HTTP {e.code}: {err_json.get('message', e.body)}", file=sys.stderr)
        except Exception:
            print(f"HTTP {e.code}: {e.body or e}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Response is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
