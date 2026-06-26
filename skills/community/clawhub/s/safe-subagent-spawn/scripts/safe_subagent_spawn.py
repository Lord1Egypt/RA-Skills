#!/usr/bin/env python3
"""Generate a spawn payload for an existing subagent context file.

Takes a context file path and outputs a JSON spawn payload to stdout.
Use create_context.py to create the context file first.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def build_spawn_payload(context_path: Path, timeout: int, child_model: str, agent_id: str) -> dict:
    child_prompt = (
        "You are a delegated subagent. Before doing any work, read this file first: "
        f"{context_path}\n\n"
        "That file is the canonical conversation context for this task. "
        "After reading it, execute the task described in the latest directive section "
        "and return your results."
    )
    payload = {
        "runtime": "subagent",
        "mode": "run",
        "thread": False,
        "task": child_prompt,
        "cleanup": "keep",  # Force keeping all sessions to expose sub-agent issues
        "timeoutSeconds": timeout,
        # Intentionally omit streamTo.
    }
    if child_model:
        payload["model"] = child_model
    if agent_id:
        payload["agentId"] = agent_id
    return payload


def main():
    ap = argparse.ArgumentParser(description="Generate spawn payload for a subagent context file.")
    ap.add_argument("--context-file", required=True, help="Path to the context file")
    ap.add_argument("--child-model", default="", help="Optional model override for the child")
    ap.add_argument("--agent-id", default="", help="Optional agent id (from agents.list[].id)")
    ap.add_argument("--timeout-seconds", type=int, default=300, help="Timeout in seconds")
    args = ap.parse_args()

    context_path = Path(args.context_file).expanduser().resolve()
    if not context_path.is_file():
        print(f"Error: context file not found: {context_path}", file=sys.stderr)
        sys.exit(1)

    content = context_path.read_text(encoding="utf-8")
    if not re.search(r"^## Directive — Round \d+", content, re.MULTILINE):
        print(
            "Error: context file has no Directive section. "
            "Append a directive with append_to_context.py before spawning a subagent.",
            file=sys.stderr,
        )
        sys.exit(1)

    payload = build_spawn_payload(context_path, args.timeout_seconds, args.child_model, args.agent_id)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
