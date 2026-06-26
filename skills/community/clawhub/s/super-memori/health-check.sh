#!/usr/bin/env python3
# Exit codes: 0=OK, 2=WARN, 3=FAIL, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from super_memori_common import (
    DB_PATH,
    MEMORY_DIR,
    QUEUE_DIR,
    audit_memory_integrity,
    canonical_memory_files,
    ensure_db,
    host_profile_status,
    lexical_index_stale,
    qdrant_collection_info,
    qdrant_ok,
    read_state,
    semantic_index_stale,
    semantic_runtime_status,
    skill_operational_memory_status,
    system_hygiene_status,
    audit_change_memory,
    query_current_known_state,
    hot_buffer_health_status,
)


class MemoriArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(message, file=sys.stderr)
        raise SystemExit(4)


def main() -> int:
    p = MemoriArgumentParser(description="Check health of super_memori")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    state = read_state()
    profile = host_profile_status()
    checks = []

    checks.append({"name": "memory_dir", "ok": MEMORY_DIR.exists(), "detail": str(MEMORY_DIR)})
    checks.append({"name": "canonical_files", "ok": len(canonical_memory_files()) > 0, "detail": len(canonical_memory_files())})
    checks.append({"name": "host_profile", "ok": True, "detail": profile})

    db_ok = False
    db_err = None
    fts_ok = False
    fts_err = None
    try:
        conn = ensure_db()
        conn.execute("SELECT 1")
        db_ok = True
        conn.execute("SELECT chunk_id FROM chunks_fts WHERE chunks_fts MATCH 'memory' LIMIT 1").fetchall()
        fts_ok = True
    except Exception as e:
        if not db_ok:
            db_err = str(e)
        else:
            fts_err = str(e)
    checks.append({"name": "lexical_db", "ok": db_ok, "detail": db_err or str(DB_PATH)})
    checks.append({"name": "lexical_fts", "ok": fts_ok, "detail": fts_err or "queryable"})

    qdrant_ready = qdrant_ok()
    qdrant_info = qdrant_collection_info() if qdrant_ready else None
    semantic_status = semantic_runtime_status(state)
    audit = audit_memory_integrity()
    checks.append({"name": "qdrant", "ok": qdrant_ready, "detail": "reachable" if qdrant_ready else "unreachable"})
    checks.append({"name": "qdrant_collection", "ok": bool(qdrant_info), "detail": qdrant_info.get("points_count") if qdrant_info else None})
    checks.append({"name": "semantic_dependencies", "ok": all(semantic_status["deps"].values()), "detail": semantic_status["deps"]})
    checks.append({"name": "local_embedding_model", "ok": semantic_status["model_ready"], "detail": semantic_status["model_error"] or "ready"})
    checks.append({"name": "semantic_vectors", "ok": semantic_status["indexed_vectors"] > 0, "detail": semantic_status["indexed_vectors"]})
    checks.append({"name": "integrity_audit", "ok": audit["status"] == "ok", "detail": audit})

    queue_count = len(list(QUEUE_DIR.glob("*.json"))) if QUEUE_DIR.exists() else 0
    checks.append({"name": "queue_backlog", "ok": queue_count < int(profile.get("queue_backlog_warn") or 500), "detail": queue_count})
    skill_status = skill_operational_memory_status()
    checks.append({"name": "skill_operational_memory", "ok": skill_status["fresh"], "detail": skill_status})
    hygiene_status = system_hygiene_status()
    checks.append({"name": "system_hygiene", "ok": hygiene_status["fresh"], "detail": hygiene_status})
    change_audit = audit_change_memory()
    checks.append({"name": "agent_change_memory", "ok": change_audit["status"] in {"ok", "warn"}, "detail": change_audit})
    hot_buffer = hot_buffer_health_status()
    checks.append({"name": "hot_change_buffer", "ok": hot_buffer["hot_buffer_integrity"] == "ok", "detail": hot_buffer})

    lexical_fresh = bool(state.get("lexical_last_indexed_at")) and not lexical_index_stale(state)
    semantic_fresh = bool(state.get("semantic_last_indexed_at")) and not semantic_index_stale(state)
    checks.append({"name": "lexical_freshness", "ok": lexical_fresh, "detail": state.get("lexical_last_indexed_at")})
    checks.append({"name": "semantic_freshness", "ok": semantic_fresh, "detail": state.get("semantic_last_indexed_at")})

    warnings = []
    if profile.get("detected_profile") == "max" and not semantic_status["model_ready"]:
        warnings.append("max profile requested but semantic stack not equipped on this host")
    if not qdrant_ready or not all(semantic_status["deps"].values()) or not semantic_status["model_ready"]:
        warnings.append("semantic layer degraded or unavailable")
    elif qdrant_info:
        reported_vectors = int(qdrant_info.get("indexed_vectors_count", 0) or qdrant_info.get("points_count", 0) or 0)
        if reported_vectors == 0:
            warnings.append("semantic backend reachable but no indexed vectors reported")
    if not state.get("lexical_last_indexed_at"):
        warnings.append("lexical index has not been built yet")
    elif not lexical_fresh:
        warnings.append("lexical index is stale; run index-memory.sh to refresh")
    if state.get("semantic_last_indexed_at") and not semantic_fresh:
        warnings.append("semantic index is stale; run index-memory.sh --rebuild-vectors to refresh")
    if audit["status"] != "ok":
        warnings.append("memory integrity drift detected; run index-memory.sh --audit and repair before trusting hybrid quality")
    if queue_count:
        warnings.append(f"queue backlog present: {queue_count}")
    if hot_buffer.get("hot_buffer_pressure", 0.0) >= 0.9:
        warnings.append("hot-change-buffer pressure is high; compaction/eviction is active")

    overall = "OK"
    if any(not c["ok"] for c in checks if c["name"] in {"memory_dir", "canonical_files", "lexical_db", "lexical_fts"}):
        overall = "FAIL"
    elif warnings:
        overall = "WARN"

    payload = {"status": overall, "warnings": warnings, "checks": checks}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"status: {overall}")
        for c in checks:
            print(f"- {c['name']}: {'ok' if c['ok'] else 'fail'} ({c['detail']})")
        if warnings:
            print("warnings:")
            for w in warnings:
                print(f"- {w}")
    return 0 if overall == "OK" else 2 if overall == "WARN" else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"health-check internal error: {exc}", file=sys.stderr)
        raise SystemExit(5)
