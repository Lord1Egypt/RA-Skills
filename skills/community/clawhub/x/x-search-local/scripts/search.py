#!/usr/bin/env python3
"""Search X (Twitter) posts using the xAI Grok API."""

import json
import os
import re
import sys
from datetime import datetime
import signal
from urllib.request import Request, HTTPRedirectHandler, build_opener
from urllib.error import URLError, HTTPError


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise HTTPError(newurl, code, f"Redirect to {newurl} blocked (auth safety)", headers, fp)

API_URL = "https://api.x.ai/v1/responses"
MODEL = "grok-4.20-reasoning"
TIMEOUT_S = 120
MAX_HANDLES = 10
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HANDLE_RE = re.compile(r"^[a-zA-Z0-9_]{1,15}$")
FLAGS_WITH_VALUES = {"--handles", "--exclude", "--from", "--to"}


def die(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_args(argv: list[str]) -> dict:
    args = argv[1:]
    options: dict = {
        "handles": None,
        "exclude": None,
        "from_date": None,
        "to_date": None,
        "images": False,
        "video": False,
        "query": [],
    }

    if not args or args[0] in ("-h", "--help"):
        print(
            'Usage: python3 search.py [--handles h1,h2] [--exclude h1,h2] [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--images] [--video] "<query>"',
            file=sys.stderr,
        )
        sys.exit(0 if args else 1)

    # Expand --flag=value into --flag value
    expanded: list[str] = []
    for a in args:
        if "=" in a and a.split("=", 1)[0] in FLAGS_WITH_VALUES:
            expanded.extend(a.split("=", 1))
        else:
            expanded.append(a)

    i = 0
    flags_done = False
    while i < len(expanded):
        arg = expanded[i]

        if arg == "--" and not flags_done:
            flags_done = True
            i += 1
            continue

        if not flags_done and arg in FLAGS_WITH_VALUES and (i + 1 >= len(expanded) or expanded[i + 1].startswith("--")):
            die(f"{arg} requires a value.")

        if not flags_done and arg == "--handles":
            i += 1
            options["handles"] = [h.strip().lstrip("@") for h in expanded[i].split(",") if h.strip().lstrip("@")]
        elif not flags_done and arg == "--exclude":
            i += 1
            options["exclude"] = [h.strip().lstrip("@") for h in expanded[i].split(",") if h.strip().lstrip("@")]
        elif not flags_done and arg == "--from":
            i += 1
            options["from_date"] = expanded[i]
        elif not flags_done and arg == "--to":
            i += 1
            options["to_date"] = expanded[i]
        elif not flags_done and arg == "--images":
            options["images"] = True
        elif not flags_done and arg == "--video":
            options["video"] = True
        elif not flags_done and arg.startswith("--"):
            die(f'Unknown flag "{arg}". Use --help for usage.')
        else:
            options["query"].append(arg)

        i += 1

    return options


def validate(options: dict) -> None:
    handles = options["handles"]
    exclude = options["exclude"]
    from_date = options["from_date"]
    to_date = options["to_date"]

    if handles is not None and exclude is not None:
        die("--handles and --exclude cannot be used together.")

    if handles is not None and len(handles) == 0:
        die("--handles value is empty.")

    if exclude is not None and len(exclude) == 0:
        die("--exclude value is empty.")

    for h in (handles or []) + (exclude or []):
        if not HANDLE_RE.match(h):
            die(f'"{h}" is not a valid X handle (letters, numbers, underscores, max 15 chars).')

    if handles and len(handles) > MAX_HANDLES:
        die(f"--handles accepts at most {MAX_HANDLES} handles, got {len(handles)}.")

    if exclude and len(exclude) > MAX_HANDLES:
        die(f"--exclude accepts at most {MAX_HANDLES} handles, got {len(exclude)}.")

    if from_date and not DATE_RE.match(from_date):
        die(f'--from must be YYYY-MM-DD format, got "{from_date}".')

    if to_date and not DATE_RE.match(to_date):
        die(f'--to must be YYYY-MM-DD format, got "{to_date}".')

    if from_date:
        try:
            datetime.strptime(from_date, "%Y-%m-%d")
        except ValueError:
            die(f'--from date "{from_date}" is not a valid date.')

    if to_date:
        try:
            datetime.strptime(to_date, "%Y-%m-%d")
        except ValueError:
            die(f'--to date "{to_date}" is not a valid date.')

    if from_date and to_date and from_date > to_date:
        die(f"--from date ({from_date}) must be before --to date ({to_date}).")


def build_tool_config(options: dict) -> dict:
    tool: dict = {"type": "x_search"}

    if options["handles"]:
        tool["allowed_x_handles"] = options["handles"]
    if options["exclude"]:
        tool["excluded_x_handles"] = options["exclude"]
    if options["from_date"]:
        tool["from_date"] = options["from_date"]
    if options["to_date"]:
        tool["to_date"] = options["to_date"]
    if options["images"]:
        tool["enable_image_understanding"] = True
    if options["video"]:
        tool["enable_video_understanding"] = True

    return tool


def _safe_get(obj: object, key: str, default: object = None) -> object:
    """Safely get a key from a dict-like object, returning default if obj is not a dict."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return default


def format_response(data: dict, query: str) -> dict:
    outputs = _safe_get(data, "output", [])
    if not isinstance(outputs, list):
        outputs = []
    usage = _safe_get(data, "usage", {})
    if not isinstance(usage, dict):
        usage = {}
    tool_details = _safe_get(usage, "server_side_tool_usage_details", {})
    if not isinstance(tool_details, dict):
        tool_details = {}

    message = next((o for o in outputs if isinstance(o, dict) and o.get("type") == "message"), None)
    content_blocks = _safe_get(message, "content", [])
    if not isinstance(content_blocks, list):
        content_blocks = []

    text = "\n\n".join(
        c.get("text", "")
        for c in content_blocks
        if isinstance(c, dict) and c.get("text")
    )
    annotations = [
        a
        for c in content_blocks if isinstance(c, dict)
        for a in (c.get("annotations") or []) if isinstance(a, dict)
    ]

    citations = [
        {"text": a.get("title", ""), "url": a["url"]}
        for a in annotations
        if a.get("type") == "url_citation" and a.get("url")
    ]

    status = _safe_get(data, "status", "unknown") or "unknown"
    if status not in ("completed", "unknown"):
        error = _safe_get(data, "error", {})
        error_msg = error.get("message", "") if isinstance(error, dict) else str(error)
        text = f"Search {status}" + (f": {error_msg}" if error_msg else "") + ("\n\n" + text if text else "")

    return {
        "status": status,
        "query": query,
        "text": text,
        "citations": citations,
        "searches": tool_details.get("x_search_calls", 0),
        "tokens": {
            "input": usage.get("input_tokens", 0),
            "output": usage.get("output_tokens", 0),
        },
    }


def search(options: dict) -> None:
    api_key = os.environ.get("XAI_API_KEY", "").strip()
    if not api_key:
        die("XAI_API_KEY environment variable is not set.")

    query = " ".join(w for w in options["query"] if w).strip()
    if not query:
        print("Error: No search query provided.", file=sys.stderr)
        print(
            'Usage: python3 search.py [--handles h1,h2] [--exclude h1,h2] [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--images] [--video] "<query>"',
            file=sys.stderr,
        )
        sys.exit(1)

    body = json.dumps({
        "model": MODEL,
        "input": [{"role": "user", "content": query}],
        "tools": [build_tool_config(options)],
    }).encode()

    req = Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "OpenClaw/x-search",
        },
        method="POST",
    )

    opener = build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except HTTPError as e:
        try:
            error_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        except Exception:
            error_body = ""
        die(f"API error ({e.code}): {error_body}")
    except URLError as e:
        die(f"Network request failed: {e.reason}")
    except TimeoutError:
        die(f"Request timed out after {TIMEOUT_S}s.")
    except json.JSONDecodeError:
        die("Failed to parse API response as JSON.")
    except OSError as e:
        die(f"Connection error: {e}")

    output = format_response(data, query)
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda *_: (print("\nInterrupted.", file=sys.stderr), sys.exit(130)))
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    options = parse_args(sys.argv)
    validate(options)
    search(options)
