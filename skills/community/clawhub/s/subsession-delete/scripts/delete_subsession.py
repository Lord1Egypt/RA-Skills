#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Optional

SESSION_KEY_RE = re.compile(r"^agent:(?P<agent>[^:]+):")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Delete an OpenClaw child session cleanly.")
    p.add_argument("--session-key", help="Full session key, e.g. agent:subtest2:subagent:...")
    p.add_argument("--session-id", help="Session id UUID")
    p.add_argument("--agent-id", help="Required with --session-id when agent cannot be inferred")
    p.add_argument("--execute", action="store_true", help="Actually delete files and rewrite sessions.json")
    return p.parse_args()


def infer_agent_id(session_key: Optional[str], agent_id: Optional[str]) -> str:
    if agent_id:
        return agent_id
    if session_key:
        m = SESSION_KEY_RE.match(session_key)
        if m:
            return m.group("agent")
    raise SystemExit("Could not determine agent id; pass --agent-id.")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def find_session_id(data: Any, session_key: Optional[str], session_id: Optional[str]) -> str:
    if session_id:
        return session_id
    if not session_key:
        raise SystemExit("Provide --session-key or --session-id.")
    entry = data.get(session_key)
    if not isinstance(entry, dict) or not entry.get("sessionId"):
        raise SystemExit(f"Session key not found in sessions.json: {session_key}")
    return entry["sessionId"]


def prune(obj: Any, remove_id: str, remove_key: Optional[str]) -> Any:
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            if remove_key and k == remove_key:
                continue
            if k == "sessionId" and v == remove_id:
                return None
            if k == "sessionFile" and isinstance(v, str) and remove_id in v:
                return None
            pruned = prune(v, remove_id, remove_key)
            if pruned is not None:
                new[k] = pruned
        return new
    if isinstance(obj, list):
        out = []
        for item in obj:
            pruned = prune(item, remove_id, remove_key)
            if pruned is not None:
                out.append(pruned)
        return out
    return obj


def main() -> None:
    args = parse_args()
    agent_id = infer_agent_id(args.session_key, args.agent_id)
    sessions_dir = Path.home() / ".openclaw" / "agents" / agent_id / "sessions"
    sessions_json = sessions_dir / "sessions.json"
    if not sessions_json.exists():
        raise SystemExit(f"sessions.json not found: {sessions_json}")

    data = load_json(sessions_json)
    target_session_id = find_session_id(data, args.session_key, args.session_id)

    file_candidates = [
        sessions_dir / f"{target_session_id}.jsonl",
        sessions_dir / f"{target_session_id}.trajectory.jsonl",
        sessions_dir / f"{target_session_id}.trajectory-path.json",
    ]

    existing = [str(p) for p in file_candidates if p.exists()]
    missing = [str(p) for p in file_candidates if not p.exists()]
    pruned = prune(data, target_session_id, args.session_key)
    index_changed = pruned != data

    result = {
        "agentId": agent_id,
        "sessionKey": args.session_key,
        "sessionId": target_session_id,
        "existingFiles": existing,
        "missingFiles": missing,
        "indexChanged": index_changed,
        "mode": "execute" if args.execute else "dry-run",
    }

    if args.execute:
        for path in file_candidates:
            if path.exists():
                path.unlink()
        if index_changed:
            sessions_json.write_text(json.dumps(pruned, ensure_ascii=False, indent=2) + "\n")
        result["deletedFiles"] = existing
        fresh = load_json(sessions_json)
        dumped = json.dumps(fresh, ensure_ascii=False)
        result["verified"] = target_session_id not in dumped and (args.session_key not in dumped if args.session_key else True)
    else:
        result["deletedFiles"] = []
        result["verified"] = False

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
