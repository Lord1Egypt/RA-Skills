#!/usr/bin/env python3
# Exit codes: 0=OK, 2=WARN/degraded, 3=FAIL, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


class StartupArgParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(message, file=sys.stderr)
        raise SystemExit(4)


def run_json_command(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        args,
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    payload = None
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = {"_raw_stdout": stdout}
    return {
        "command": args,
        "exit_code": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "payload": payload,
    }


def check_ok(health: dict[str, Any] | None, name: str) -> bool | None:
    if not isinstance(health, dict):
        return None
    checks = health.get("checks") or []
    for item in checks:
        if item.get("name") == name:
            return bool(item.get("ok"))
    return None


def should_attempt_repair(health_payload: dict[str, Any]) -> tuple[bool, str]:
    status = str(health_payload.get("status") or "FAIL")
    if status == "WARN":
        return True, "warn-state safe self-heal"
    if status != "FAIL":
        return False, "healthy"
    memory_dir_ok = check_ok(health_payload, "memory_dir")
    canonical_ok = check_ok(health_payload, "canonical_files")
    lexical_db_ok = check_ok(health_payload, "lexical_db")
    lexical_fts_ok = check_ok(health_payload, "lexical_fts")
    if memory_dir_ok and canonical_ok and (lexical_db_ok is False or lexical_fts_ok is False):
        return True, "fail-state lexical repair"
    return False, "fail-state not safely repairable"


def build_summary(report: dict[str, Any]) -> str:
    final_status = report.get("final_status") or "FAIL"
    repair_attempted = bool(report.get("repair_attempted"))
    smoke = report.get("smoke_query") or {}
    smoke_mode = (smoke.get("payload") or {}).get("mode_used")
    parts = [f"final_status={final_status}"]
    if repair_attempted:
        parts.append("repair_attempted=true")
    if smoke_mode:
        parts.append(f"smoke_mode={smoke_mode}")
    if smoke.get("exit_code") is not None:
        parts.append(f"smoke_exit={smoke['exit_code']}")
    return ", ".join(parts)


def main() -> int:
    parser = StartupArgParser(description="Startup health-check and safe self-heal for super-memori")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--repair", dest="repair", action="store_true")
    parser.add_argument("--no-repair", dest="repair", action="store_false")
    parser.add_argument("--report-file")
    parser.set_defaults(repair=True)
    args = parser.parse_args()

    started_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    health_before = run_json_command(["./health-check.sh", "--json"])
    before_payload = health_before.get("payload") if isinstance(health_before.get("payload"), dict) else None
    if not isinstance(before_payload, dict):
        report = {
            "started_at": started_at,
            "final_status": "FAIL",
            "repair_enabled": bool(args.repair),
            "repair_attempted": False,
            "health_before": health_before,
            "error": "health-check did not return JSON",
        }
        if args.report_file:
            path = Path(args.report_file).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print("startup self-check failed: health-check did not return JSON", file=sys.stderr)
        return 5

    repair_attempted = False
    repair_reason = "disabled"
    maintenance = None
    if args.repair:
        do_repair, repair_reason = should_attempt_repair(before_payload)
        if do_repair:
            repair_attempted = True
            maintenance = run_json_command(["./index-memory.sh", "--full", "--rebuild-vectors", "--audit", "--json"])

    health_after = run_json_command(["./health-check.sh", "--json"])
    after_payload = health_after.get("payload") if isinstance(health_after.get("payload"), dict) else None
    if not isinstance(after_payload, dict):
        after_payload = {"status": "FAIL", "warnings": ["health-check post-pass did not return JSON"]}

    smoke_query = None
    final_status = str(after_payload.get("status") or "FAIL")
    if final_status != "FAIL":
        smoke_query = run_json_command(["./query-memory.sh", "test query", "--mode", "auto", "--json", "--limit", "1"])

    report = {
        "started_at": started_at,
        "skill_root": str(ROOT),
        "repair_enabled": bool(args.repair),
        "repair_attempted": repair_attempted,
        "repair_reason": repair_reason,
        "health_before": health_before,
        "maintenance": maintenance,
        "health_after": health_after,
        "smoke_query": smoke_query,
        "final_status": final_status,
        "summary": "",
    }
    report["summary"] = build_summary(report)

    if args.report_file:
        path = Path(args.report_file).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(report["summary"])
        warnings = (after_payload.get("warnings") or []) if isinstance(after_payload, dict) else []
        if warnings:
            print("remaining warnings:")
            for item in warnings:
                print(f"- {item}")

    smoke_exit = smoke_query.get("exit_code") if isinstance(smoke_query, dict) else None
    if final_status == "OK" and smoke_exit not in {3, 4, 5}:
        return 0
    if final_status == "WARN":
        return 2
    return 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"startup-self-check internal error: {exc}", file=sys.stderr)
        raise SystemExit(5)
