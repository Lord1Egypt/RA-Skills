from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.execution import preflight_action, run_x_action
from core.storage import LocalStateStore
from common import load_json, utc_now_iso


def main() -> int:
    parser = argparse.ArgumentParser(description="Record execution of an approved X action.")
    parser.add_argument("--mission", default="data/mission.json", help="Mission JSON path.")
    parser.add_argument("--action", default="data/action.json", help="Action JSON path.")
    parser.add_argument("--log", default="data/execution_log.jsonl", help="Execution log JSONL path.")
    parser.add_argument("--approved", action="store_true", help="Mark the action as user approved.")
    parser.add_argument("--mode", choices=["dry-run", "record-only", "x-api"], default="dry-run", help="Execution mode.")
    parser.add_argument("--skip-preflight", action="store_true", help="Skip interaction preflight checks for reply or quote actions.")
    args = parser.parse_args()

    mission = load_json(args.mission)
    action = load_json(args.action)
    action_store = LocalStateStore(Path(args.action).parent)
    log_store = LocalStateStore(Path(args.log).parent)

    if action.get("requires_approval", True) and not args.approved:
        raise SystemExit("Refusing to execute without --approved.")

    execution_output = None
    if args.mode == "x-api":
        preflight_output = None
        if action.get("action_type") in {"reply", "quote_post"} and not args.skip_preflight:
            preflight_result = preflight_action(action)
            preflight_output = json.dumps(preflight_result, ensure_ascii=False)
            if preflight_result.get("decision") == "block":
                raise SystemExit(preflight_output)

        execution_output = run_x_action(action)

    result = {
        "executed_at": utc_now_iso(),
        "mode": args.mode,
        "mission_name": mission.get("name", ""),
        "action_id": action.get("id"),
        "action_type": action.get("action_type"),
        "target_url": action.get("target_url"),
        "target_account": action.get("target_account"),
        "draft_text": action.get("draft_text"),
        "status": "recorded" if args.mode == "record-only" else "executed" if args.mode == "x-api" else "dry_run_executed",
    }
    if execution_output:
        try:
            result["provider_result"] = json.loads(execution_output)
        except json.JSONDecodeError:
            result["provider_result_raw"] = execution_output
    if args.mode == "x-api" and action.get("action_type") in {"reply", "quote_post"} and not args.skip_preflight:
        try:
            result["preflight"] = json.loads(preflight_output) if preflight_output else None
        except json.JSONDecodeError:
            result["preflight_raw"] = preflight_output
    log_store.append_execution_event(result, Path(args.log).name)

    action["status"] = "executed"
    action["executed_at"] = result["executed_at"]
    action["execution_mode"] = args.mode
    action_store.save_action(action, Path(args.action).name)

    print(f"Execution recorded for {action.get('id')} in {args.mode} mode")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
