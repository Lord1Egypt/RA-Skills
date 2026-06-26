#!/usr/bin/env python3
# Exit codes: 0=OK, 2=drift/orphans found, 3=audit unavailable, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from super_memori_common import audit_memory_integrity, skill_operational_memory_audit, system_hygiene_status, audit_change_memory, hot_buffer_health_status, detect_interrupted_change_sequence, query_unverified_recent_changes


class AuditArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(message, file=sys.stderr)
        raise SystemExit(4)


def main() -> int:
    p = AuditArgumentParser(description="Audit lexical/semantic integrity for super_memori")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    result = audit_memory_integrity()
    skill_audit = skill_operational_memory_audit()
    result["skill_operational_memory"] = skill_audit
    result["system_hygiene"] = system_hygiene_status()
    result["agent_change_memory"] = audit_change_memory()
    result["hot_change_buffer"] = hot_buffer_health_status()
    result["hot_interrupted_sequences"] = detect_interrupted_change_sequence(limit=16)
    result["hot_unverified_recent"] = query_unverified_recent_changes(limit=16)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"lexical_chunk_count: {result['lexical_chunk_count']}")
        print(f"vector_point_count: {result['vector_point_count']}")
        if result['orphan_chunks']:
            print("orphan_chunks:")
            for item in result['orphan_chunks']:
                print(f"- {item}")
        if result['orphan_fts_chunks']:
            print("orphan_fts_chunks:")
            for item in result['orphan_fts_chunks']:
                print(f"- {item}")
        if result['orphan_vectors']:
            print("orphan_vectors:")
            for item in result['orphan_vectors']:
                print(f"- {item}")
        if result['missing_vectors']:
            print("missing_vectors:")
            for item in result['missing_vectors']:
                print(f"- {item}")
        if result['broken_relations']:
            print("broken_relations:")
            for item in result['broken_relations']:
                print(f"- {item}")
    return 0 if result["status"] == "ok" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"audit-memory internal error: {exc}", file=sys.stderr)
        raise SystemExit(5)
