#!/usr/bin/env python3
"""
micro_rest.py — Waking neural replay for AI agents (v2)

Based on Eichenlaub et al. 2020: replay occurs during waking rest, not just sleep.
Quick append to daily log. No LLM call for --note mode.
Uses Claude only for --flush (pre-compaction extraction).

Usage:
  # Append a single memory note
  python scripts/micro_rest.py --note "User prefers TypeScript" --type O --workspace ~/.agent_workspace

  # Pipe from stdin
  echo "Fixed auth bug in session.py" | python scripts/micro_rest.py --type B

  # Pre-compaction flush: extract durable memories from context dump
  python scripts/micro_rest.py --flush --context-dump "$(cat session.txt)" --workspace ~/.agent_workspace
"""

import argparse
import json
import os
import sys
import http.client
from datetime import date
from pathlib import Path


FLUSH_SYSTEM = """You are performing a pre-compaction memory flush for an AI agent.
Extract all facts, decisions, preferences, and observations worth retaining long-term.

Use type prefixes:
  W  — world fact (objective)
  B  — biographical/experience (what the agent did)
  O(c=N) — opinion/preference with confidence 0–1
  S  — summary (synthesized observation)

Be selective. Prefer concrete over vague. Skip small talk and irrelevant details.

Respond ONLY with valid JSON, no markdown fences:
{
  "retain": [
    {"type": "W|B|O|S", "confidence": 0.9, "text": "single sentence"}
  ]
}"""


def call_claude_flush(context_dump: str, model: str) -> list[dict]:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not set")
    payload = json.dumps({
        "model": model,
        "max_tokens": 800,
        "system": FLUSH_SYSTEM,
        "messages": [{"role": "user", "content": f"Session context to flush:\n\n{context_dump[:8000]}"}],
    }).encode()
    conn = http.client.HTTPSConnection("api.anthropic.com")
    conn.request("POST", "/v1/messages", payload, {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    })
    resp = conn.getresponse()
    body = json.loads(resp.read().decode())
    conn.close()
    if "error" in body:
        raise RuntimeError(f"API error: {body['error']['message']}")
    raw = body["content"][0]["text"].strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(raw).get("retain", [])
    except Exception:
        return []


def append_to_daily_log(workspace: Path, entries: list[str], source: str = "micro-rest"):
    log_file = workspace / "memory" / f"{date.today()}.md"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = __import__("datetime").datetime.now().strftime("%H:%M")
    block = f"\n### {timestamp} [{source}]\n## Retain\n" + "\n".join(f"- {e}" for e in entries) + "\n"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(block)

    return log_file


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--note", "-n", type=str, help="Note to append (single entry)")
    p.add_argument("--type", "-t", default="W", choices=["W", "B", "O", "S"],
                   help="Memory type: W=world, B=experience, O=opinion, S=summary")
    p.add_argument("--confidence", "-c", type=float, default=0.9,
                   help="Confidence for O-type entries (0–1)")
    p.add_argument("--workspace", "-w", default="~/.agent_workspace")
    p.add_argument("--flush", action="store_true",
                   help="Pre-compaction flush: extract durable memories from context dump")
    p.add_argument("--context-dump", type=str, help="Raw context text for --flush mode")
    p.add_argument("--model", default="claude-sonnet-4-20250514")
    args = p.parse_args()

    workspace = Path(args.workspace).expanduser()

    if args.flush:
        # Pre-compaction flush mode
        context = args.context_dump or ""
        if not context and not sys.stdin.isatty():
            context = sys.stdin.read()
        if not context.strip():
            print("Error: --flush requires --context-dump or stdin", file=sys.stderr)
            sys.exit(1)

        print("  [flush] Extracting durable memories from context...", file=sys.stderr)
        items = call_claude_flush(context, args.model)
        if not items:
            print("  [flush] Nothing worth retaining extracted.", file=sys.stderr)
            return

        entries = []
        for item in items:
            t = item.get("type", "W")
            c = item.get("confidence", 0.9)
            text = item.get("text", "")
            if t == "O":
                entries.append(f"O(c={c:.2f}): {text}")
            else:
                entries.append(f"{t}: {text}")

        log_file = append_to_daily_log(workspace, entries, source="compaction-flush")
        print(f"  [flush] Wrote {len(entries)} item(s) to {log_file}", file=sys.stderr)

    else:
        # Direct note mode
        note_text = args.note
        if not note_text and not sys.stdin.isatty():
            note_text = sys.stdin.read().strip()
        if not note_text:
            print("Error: provide --note or pipe text via stdin", file=sys.stderr)
            sys.exit(1)

        t = args.type
        if t == "O":
            entry = f"O(c={args.confidence:.2f}): {note_text}"
        else:
            entry = f"{t}: {note_text}"

        log_file = append_to_daily_log(workspace, [entry], source="micro-rest")
        print(f"  [micro-rest] Appended to {log_file}")


if __name__ == "__main__":
    main()
