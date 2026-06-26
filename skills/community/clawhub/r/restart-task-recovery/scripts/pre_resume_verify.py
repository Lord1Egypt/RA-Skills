#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: pre_resume_verify.py <recover-actions.json> [out.json]", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1]).expanduser()
    out = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else None

    data = json.loads(src.read_text(encoding="utf-8"))
    actions = data.get("actions", [])

    verified = []
    for a in actions:
        params = a.get("params", {})
        msg = params.get("message", "")
        # Heuristic risk gate: if message hints external write/retry, require manual confirm first.
        risky = any(k in msg.lower() for k in ["retry", "write", "create", "update", "delete", "payment", "transfer"])
        verified.append(
            {
                "sessionKey": params.get("sessionKey"),
                "message": msg,
                "risk": "high" if risky else "normal",
                "requiresManualConfirm": bool(risky),
                "decision": "hold" if risky else "send",
                "reason": "Potential non-idempotent external write" if risky else "Safe to resume",
            }
        )

    result = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "source": str(src),
        "count": len(verified),
        "verified": verified,
    }

    txt = json.dumps(result, ensure_ascii=False, indent=2)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(txt, encoding="utf-8")
        print(str(out))
    else:
        print(txt)


if __name__ == "__main__":
    main()
