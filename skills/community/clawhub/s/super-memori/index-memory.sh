#!/usr/bin/env python3
# Exit codes: 0=OK, 2=degraded/partial, 3=FAIL, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from super_memori_common import (
    DB_PATH,
    QUEUE_DIR,
    audit_memory_integrity,
    ensure_db,
    host_profile_status,
    rebuild_lexical_index,
    rebuild_semantic_index,
    read_state,
    semantic_runtime_status,
    refresh_skill_operational_memory,
    scan_system_hygiene,
    plan_hygiene_cleanup,
    record_agent_change,
    reconcile_routine_change_history,
    compact_hot_buffer,
)


class MemoriArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(message, file=sys.stderr)
        raise SystemExit(4)


def main() -> int:
    p = MemoriArgumentParser(description="Maintain super_memori indexes")
    p.add_argument("--incremental", action="store_true")
    p.add_argument("--full", action="store_true")
    p.add_argument("--rebuild-fts", action="store_true")
    p.add_argument("--rebuild-vectors", action="store_true")
    p.add_argument("--stats", action="store_true")
    p.add_argument("--vacuum", action="store_true")
    p.add_argument("--audit", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    state = read_state()
    profile = host_profile_status()
    payload = {"actions": [], "warnings": [], "host_profile": profile}

    if args.stats:
        conn = ensure_db()
        payload["lexical_entries"] = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
        payload["lexical_chunks"] = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        payload["db_path"] = str(DB_PATH)
        payload["state"] = state
        payload["semantic"] = semantic_runtime_status(state)
        payload["audit"] = audit_memory_integrity()
        if payload["audit"]["status"] != "ok":
            payload["warnings"].append("integrity audit reported drift or orphans")
    else:
        if args.full or args.incremental or args.rebuild_fts or not any([args.full, args.incremental, args.rebuild_fts, args.rebuild_vectors, args.vacuum, args.audit]):
            stats = rebuild_lexical_index(full=bool(args.full or args.rebuild_fts))
            payload["actions"].append({"lexical_index": stats})

        queue_processed = 0
        queue_errors = 0
        processed_dir = QUEUE_DIR / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)
        if QUEUE_DIR.exists():
            for item in sorted(QUEUE_DIR.glob("*.json")):
                try:
                    data = json.loads(item.read_text(encoding="utf-8"))
                    target = processed_dir / item.name
                    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                    item.unlink()
                    queue_processed += 1
                except Exception:
                    queue_errors += 1
            if queue_processed:
                payload["actions"].append({"queue_processed": queue_processed})
            if queue_errors:
                payload["warnings"].append(f"queue items with processing errors: {queue_errors}")

        if args.rebuild_vectors:
            try:
                stats = rebuild_semantic_index(recreate=bool(args.full), limit=None)
                payload["actions"].append({"semantic_rebuild": stats})
            except Exception as exc:
                payload["warnings"].append(f"semantic rebuild not executed: {exc}")

        if args.audit:
            audit = audit_memory_integrity()
            payload["actions"].append({"audit": audit})
            if audit["status"] != "ok":
                payload["warnings"].append("integrity audit reported drift or orphans")

        maintenance_record = record_agent_change(
            status="applied_but_unverified",
            target_scope="openclaw",
            action_type="reindex",
            exact_paths=[str(DB_PATH)],
            why_change_was_made="Refresh index state during maintenance",
            expected_effect="keep lexical indexes and operational memories current",
            risk_level="low",
            rollback_possible=True,
            rollback_method="git restore / db vacuum rollback",
            verification_steps=["run health-check.sh", "run audit-memory.sh"],
            verification_state="unverified",
            command_or_patch_summary="index-memory maintenance path",
            related_skills=["super-memori"],
        )
        payload["actions"].append({"agent_change_memory": maintenance_record})

        hot_buffer_compaction = compact_hot_buffer()
        payload["actions"].append({"hot_change_buffer": hot_buffer_compaction})
        hygiene_scan = scan_system_hygiene()
        payload["actions"].append({"system_hygiene_scan": hygiene_scan})
        hygiene_plan = plan_hygiene_cleanup(allow_destructive=False)
        payload["actions"].append({"system_hygiene_cleanup_plan": hygiene_plan})

        skill_refresh = refresh_skill_operational_memory()
        payload["actions"].append({"skill_operational_memory": skill_refresh})

        post_audit = audit_memory_integrity()
        payload["actions"].append({"post_audit": post_audit})
        if post_audit["status"] != "ok":
            payload["warnings"].append("integrity audit reported drift or orphans after maintenance")
        state_after = read_state()
        post_semantic = semantic_runtime_status(state_after)
        if not all(post_semantic["deps"].values()) or not post_semantic["model_ready"]:
            payload["warnings"].append("semantic layer degraded or unavailable after maintenance")

        if not payload["warnings"]:
            reconciled = reconcile_routine_change_history(
                target_scope="openclaw",
                action_type="reindex",
                exact_paths=[str(DB_PATH)],
                command_or_patch_summary="index-memory maintenance path",
                risk_level="low",
                related_skill="super-memori",
                observed_effect="maintenance completed successfully; health/audit verification passed",
                verification_steps=["run health-check.sh", "run audit-memory.sh"],
            )
            payload["actions"].append({"agent_change_memory_reconciled": reconciled})

        if args.vacuum:
            conn = ensure_db()
            conn.execute("VACUUM")
            payload["actions"].append({"vacuum": "done"})

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload)
    if payload["warnings"]:
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except sqlite3.Error as exc:
        print(f"index-memory failure: {exc}", file=sys.stderr)
        raise SystemExit(3)
    except Exception as exc:
        print(f"index-memory internal error: {exc}", file=sys.stderr)
        raise SystemExit(5)
