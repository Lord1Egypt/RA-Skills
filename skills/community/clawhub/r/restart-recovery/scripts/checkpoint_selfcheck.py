#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


def parse_args():
    ap = argparse.ArgumentParser(description="No-LLM stale-checkpoint detector")
    ap.add_argument("--root", default=str(Path.cwd()), help="Workspace root")
    ap.add_argument("--stale-min", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    return ap.parse_args()


def main():
    args = parse_args()
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=args.stale_min)
    root = Path(args.root)

    roots = [root / "memory" / "checkpoints"]
    agents_dir = root / "agents"
    if agents_dir.exists():
        for d in agents_dir.iterdir():
            roots.append(d / "memory" / "checkpoints")

    findings = []
    for chk_root in roots:
        if not chk_root.exists():
            continue
        for p in chk_root.glob("*.json"):
            if p.name == "CHECKPOINT_SCHEMA.json":
                continue
            try:
                obj = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            if obj.get("status") not in {"in_progress", "blocked"}:
                continue
            ts = obj.get("updatedAt")
            if not ts:
                continue
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except Exception:
                continue
            if dt <= cutoff:
                findings.append({
                    "workflowId": obj.get("workflowId", p.stem),
                    "agentId": obj.get("agentId", "unknown"),
                    "file": p.as_posix(),
                    "ageMinutes": int((now - dt).total_seconds() / 60),
                })

    if args.json:
        print(json.dumps({"status": "ok" if not findings else "alert", "count": len(findings), "findings": findings}, indent=2))
        return

    if not findings:
        print("OK")
        return

    print(f"ALERT stale_checkpoints={len(findings)} threshold_min={args.stale_min}")
    for f in findings[:50]:
        print(f"- {f['agentId']}:{f['workflowId']} age={f['ageMinutes']}m file={f['file']}")


if __name__ == "__main__":
    main()
