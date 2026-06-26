#!/usr/bin/env python3
import json
import sys
import time
from datetime import datetime, timezone


def parse_json(raw, fallback):
    try:
        return json.loads(raw)
    except Exception:
        return fallback


def has_pr(deliverables):
    if not isinstance(deliverables, list):
        return False
    for d in deliverables:
        if not isinstance(d, dict):
            continue
        if d.get("type") == "pr":
            return True
        if "/pull/" in str(d.get("url") or ""):
            return True
    return False


def parse_ts(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value if value >= 1e12 else value * 1000)
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return None
        if s.isdigit():
            n = float(s)
            return n if n >= 1e12 else n * 1000
        try:
            if s.endswith("Z"):
                dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
            else:
                dt = datetime.fromisoformat(s)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
            return dt.timestamp() * 1000
        except Exception:
            return None
    return None


def build_envelope(pending_raw, review_raw, working_raw, now_ms=None):
    pending = parse_json(pending_raw, {"tasks": []})
    review = parse_json(review_raw, {"tasks": []})
    working = parse_json(working_raw, {"tasks": []})

    pending_tasks = pending.get("tasks", []) if isinstance(pending, dict) else []
    review_tasks_all = review.get("tasks", []) if isinstance(review, dict) else []
    working_tasks_all = working.get("tasks", []) if isinstance(working, dict) else []

    review_tasks = [
        t for t in review_tasks_all if has_pr(t.get("deliverables", [])) and not t.get("pickedUpAt")
    ]

    if now_ms is None:
        now_ms = time.time() * 1000
    stuck_threshold_ms = 30 * 60 * 1000
    activity_grace_ms = 15 * 60 * 1000

    stuck_tasks = []
    for t in working_tasks_all:
        if not has_pr(t.get("deliverables", [])):
            continue

        started_at = parse_ts(t.get("startedAt"))
        if started_at is None or now_ms - started_at <= stuck_threshold_ms:
            continue

        activity_candidates = [
            t.get("updatedAt"),
            t.get("lastActivityAt"),
            t.get("lastThreadMessageAt"),
            t.get("pickedUpAt"),
        ]
        activity_ts = max((parse_ts(v) for v in activity_candidates if v is not None), default=None)
        if activity_ts is not None and (now_ms - activity_ts) <= activity_grace_ms:
            continue

        stuck_tasks.append(t)

    return {
        "generatedAt": int(now_ms),
        "pending": pending,
        "review": {"tasks": review_tasks},
        "stuck": {"tasks": stuck_tasks},
        "counts": {
            "pending": len(pending_tasks),
            "review": len(review_tasks),
            "stuck": len(stuck_tasks),
        },
    }


def main():
    if len(sys.argv) == 4:
        envelope = build_envelope(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            print("Usage: poll-parser.py <pending_json> <review_json> <working_json> OR stdin JSON with pending/review/working", file=sys.stderr)
            sys.exit(2)
        bundle = parse_json(raw, {})
        if not isinstance(bundle, dict):
            print("Invalid stdin JSON bundle", file=sys.stderr)
            sys.exit(2)
        envelope = build_envelope(
            json.dumps(bundle.get("pending", {"tasks": []})),
            json.dumps(bundle.get("review", {"tasks": []})),
            json.dumps(bundle.get("working", {"tasks": []})),
        )
    if envelope["counts"]["pending"] == 0 and envelope["counts"]["review"] == 0 and envelope["counts"]["stuck"] == 0:
        print("HEARTBEAT_OK")
        return

    print("POLL_RESULT:")
    print(json.dumps(envelope))


if __name__ == "__main__":
    main()
