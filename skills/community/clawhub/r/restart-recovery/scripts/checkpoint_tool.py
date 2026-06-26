#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path.cwd() / "memory" / "checkpoints"
ROOT.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def cp_path(workflow_id: str) -> Path:
    return ROOT / f"{workflow_id}.json"


def lock_path(workflow_id: str) -> Path:
    return ROOT / f"{workflow_id}.lock"


def calc_hash(obj: dict) -> str:
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def atomic_write(path: Path, obj: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    tmp.replace(path)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_start(args):
    p = cp_path(args.workflow)
    if p.exists() and not args.force:
        raise SystemExit(f"checkpoint exists: {p} (use --force)")
    obj = {
        "schemaVersion": "1.0",
        "workflowId": args.workflow,
        "agentId": args.agent,
        "status": "in_progress",
        "currentStep": args.step,
        "completedSteps": [],
        "remainingSteps": args.remaining,
        "handoffTo": args.handoff,
        "notes": args.notes or "",
        "idempotencyKey": args.idempotency,
        "updatedAt": now_iso(),
        "expiresAt": (datetime.now(timezone.utc) + timedelta(days=args.ttl_days)).isoformat(),
    }
    obj["checkpointHash"] = calc_hash({k: v for k, v in obj.items() if k != "checkpointHash"})
    atomic_write(p, obj)
    print(p)


def cmd_update(args):
    p = cp_path(args.workflow)
    obj = load(p)
    if args.complete:
        if args.complete not in obj["completedSteps"]:
            obj["completedSteps"].append(args.complete)
        obj["remainingSteps"] = [s for s in obj["remainingSteps"] if s != args.complete]
    if args.step:
        obj["currentStep"] = args.step
    if args.status:
        obj["status"] = args.status
    if args.notes is not None:
        obj["notes"] = args.notes
    obj["updatedAt"] = now_iso()
    obj["checkpointHash"] = calc_hash({k: v for k, v in obj.items() if k != "checkpointHash"})
    atomic_write(p, obj)
    print(p)


def cmd_complete(args):
    p = cp_path(args.workflow)
    obj = load(p)
    obj["status"] = "done"
    obj["remainingSteps"] = []
    obj["updatedAt"] = now_iso()
    obj["checkpointHash"] = calc_hash({k: v for k, v in obj.items() if k != "checkpointHash"})
    atomic_write(p, obj)
    print(p)


def cmd_list(_args):
    for p in sorted(ROOT.glob("*.json")):
        if p.name == "CHECKPOINT_SCHEMA.json":
            continue
        try:
            obj = load(p)
            print(f"{obj.get('workflowId')}\t{obj.get('status')}\t{obj.get('currentStep')}\t{obj.get('updatedAt')}")
        except Exception:
            print(f"{p.name}\tINVALID")


def cmd_resume(args):
    now = datetime.now(timezone.utc)
    for p in sorted(ROOT.glob("*.json")):
        if p.name == "CHECKPOINT_SCHEMA.json":
            continue
        obj = load(p)
        if obj.get("status") not in {"in_progress", "blocked"}:
            continue
        exp = obj.get("expiresAt")
        if exp:
            try:
                if datetime.fromisoformat(exp) < now:
                    continue
            except Exception:
                pass
        l = lock_path(obj["workflowId"])
        if l.exists() and not args.steal_lock:
            continue
        l.write_text(now_iso(), encoding="utf-8")
        print(json.dumps(obj, indent=2))
        return
    print("NO_CHECKPOINT")


def main():
    ap = argparse.ArgumentParser(description="Checkpoint helper for restart-safe workflows")
    sp = ap.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("start")
    s.add_argument("--workflow", required=True)
    s.add_argument("--agent", required=True)
    s.add_argument("--step", required=True)
    s.add_argument("--remaining", nargs="*", default=[])
    s.add_argument("--idempotency", required=True)
    s.add_argument("--handoff", default=None)
    s.add_argument("--notes", default="")
    s.add_argument("--ttl-days", type=int, default=7)
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_start)

    u = sp.add_parser("update")
    u.add_argument("--workflow", required=True)
    u.add_argument("--step")
    u.add_argument("--complete")
    u.add_argument("--status", choices=["in_progress", "blocked", "done", "failed"])
    u.add_argument("--notes")
    u.set_defaults(func=cmd_update)

    c = sp.add_parser("complete")
    c.add_argument("--workflow", required=True)
    c.set_defaults(func=cmd_complete)

    l = sp.add_parser("list")
    l.set_defaults(func=cmd_list)

    r = sp.add_parser("resume")
    r.add_argument("--steal-lock", action="store_true")
    r.set_defaults(func=cmd_resume)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
