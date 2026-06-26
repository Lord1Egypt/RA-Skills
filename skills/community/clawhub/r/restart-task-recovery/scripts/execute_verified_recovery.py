#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: execute_verified_recovery.py <recover-verified.json>", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1]).expanduser()
    data = json.loads(src.read_text(encoding="utf-8"))
    verified = data.get("verified", [])

    send = [v for v in verified if v.get("decision") == "send"]
    hold = [v for v in verified if v.get("decision") == "hold"]

    # This script outputs execution plan only; caller executes tool calls.
    out = {
        "sendCount": len(send),
        "holdCount": len(hold),
        "sendActions": [
            {
                "tool": "sessions_send",
                "params": {
                    "sessionKey": v.get("sessionKey"),
                    "message": v.get("message"),
                },
            }
            for v in send
        ],
        "holdForManualConfirm": [
            {
                "sessionKey": v.get("sessionKey"),
                "reason": v.get("reason", "Potential non-idempotent write"),
                "message": v.get("message"),
            }
            for v in hold
        ],
    }

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
