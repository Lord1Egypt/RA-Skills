#!/usr/bin/env python3
"""Query Synero council endpoint and parse SSE output.

Examples:
  python3 synero-council.py "How should we prioritize roadmap items?"
  python3 synero-council.py --raw "Give me a 3-way strategic take on X"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

API_URL = os.environ.get("SYNERO_API_URL", "https://synero.ai/api/query")
REQUEST_TIMEOUT_SECONDS = int(os.environ.get("SYNERO_TIMEOUT", "120"))

ADVISOR_KEYS = {
    "architect",
    "philosopher",
    "explorer",
    "maverick",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ask Synero council a question")
    p.add_argument("prompt", help="Question or prompt")
    p.add_argument("--raw", action="store_true", help="Print raw SSE events")
    p.add_argument("--thread-id", help="Optional thread ID for conversation continuity")
    p.add_argument("--parent-query-id", help="Optional parent query ID")
    p.add_argument(
        "--advisor-model",
        action="append",
        default=[],
        metavar="SLOT=MODEL",
        help="Override advisor model (e.g. architect=gpt-5.2). Repeat up to 4 times.",
    )
    p.add_argument(
        "--synthesizer-model",
        help="Optional synthesizer model override (e.g. gpt-4.1)",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress extra status lines and print only the final synthesis in normal mode",
    )
    return p.parse_args()


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {"prompt": args.prompt}
    if args.thread_id:
        payload["threadId"] = args.thread_id
    if args.parent_query_id:
        payload["parentQueryId"] = args.parent_query_id

    cfg: dict[str, Any] = {}
    advisor_models = {
        "architect": os.environ.get("SYNERO_MODEL_ARCHITECT"),
        "philosopher": os.environ.get("SYNERO_MODEL_PHILOSOPHER"),
        "explorer": os.environ.get("SYNERO_MODEL_EXPLORER"),
        "maverick": os.environ.get("SYNERO_MODEL_MAVERICK"),
    }
    advisor_models = {k: v for k, v in advisor_models.items() if v}

    for item in args.advisor_model:
        if "=" not in item:
            raise SystemExit(f"Invalid --advisor-model value '{item}'. Use slot=model format.")
        slot, model = item.split("=", 1)
        slot = slot.strip()
        model = model.strip()
        if slot not in ADVISOR_KEYS:
            raise SystemExit(f"Invalid advisor slot '{slot}'. Must be one of {sorted(ADVISOR_KEYS)}")
        if not model:
            raise SystemExit(f"Invalid model override for slot '{slot}'.")
        advisor_models[slot] = model

    if advisor_models:
        cfg["advisorModels"] = advisor_models

    if args.synthesizer_model:
        cfg["synthesizerModel"] = args.synthesizer_model
    else:
        synth_model = os.environ.get("SYNERO_MODEL_SYNTHESIZER")
        if synth_model:
            cfg["synthesizerModel"] = synth_model

    if cfg:
        payload["config"] = cfg

    return payload


def print_synthesis(text: str, quiet: bool = False) -> None:
    synthesis = text.strip()
    if not synthesis:
        raise RuntimeError("No synthesis content was returned.")
    if quiet:
        print(synthesis)
        return
    print("\n## Synero Synthesis\n")
    print(synthesis)


def parse_sse_line(line: str):
    if not line.startswith("data:"):
        return None

    payload = line.split(":", 1)[1].strip()
    if not payload:
        return None

    try:
        envelope = json.loads(payload)
    except Exception:
        return None

    event = envelope.get("event")
    data = envelope.get("data")
    if not event:
        return None

    if event == "synthesis":
        token = data.get("token") if isinstance(data, dict) else None
        return ("synthesis", token, data)
    if event == "advisor":
        token = data.get("token") if isinstance(data, dict) else None
        return ("advisor", token, data)
    if event in {"synthesis-complete", "complete", "advisor-complete", "advisor-error", "error"}:
        return (event, None, data)
    return (event, None, data)


def query_council(args: argparse.Namespace) -> None:
    api_key = os.environ.get("SYNERO_API_KEY")
    if not api_key:
        raise SystemExit(
            "SYNERO_API_KEY not set. Get an API key from https://synero.ai, then export it first: "
            "export SYNERO_API_KEY=sk_live_..."
        )

    payload = json.dumps(build_payload(args), ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "text/event-stream")
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36",
    )
    req.add_header("Authorization", f"Bearer {api_key}")

    events: dict[str, Any] = {"synthesis": "", "advisor": {}, "complete": None}

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
            if resp.status != 200:
                body = resp.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"HTTP {resp.status}: {body[:400]}")

            if not args.raw and not args.quiet:
                print(f"HTTP {resp.status} {resp.reason}")

            for raw in resp:
                line = raw.decode("utf-8", errors="replace").rstrip("\n")
                if not line.strip():
                    continue

                parsed = parse_sse_line(line)
                if not parsed:
                    if args.raw:
                        print(line)
                    continue

                event, token, payload_data = parsed
                if args.raw:
                    print(line)

                if event == "advisor" and token:
                    slot = payload_data.get("id") if isinstance(payload_data, dict) else None
                    key = f"advisor:{slot}" if slot else "advisor"
                    events["advisor"].setdefault(key, "")
                    events["advisor"][key] += str(token)
                elif event == "synthesis" and token:
                    events["synthesis"] += str(token)
                elif event == "complete":
                    events["complete"] = payload_data
                elif event == "error":
                    raise RuntimeError(f"Synero error event: {payload_data}")

            if not args.raw:
                print_synthesis(events["synthesis"], quiet=args.quiet)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error talking to Synero: {exc}") from exc


def main() -> int:
    args = parse_args()
    if not args.prompt.strip():
        raise SystemExit("Prompt is required")
    query_council(args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        raise SystemExit(130)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
