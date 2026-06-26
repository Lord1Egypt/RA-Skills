#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent
COLLECT = ROOT / "collect_from_session.py"


class ExportError(Exception):
    def __init__(self, status: str, message: str, payload: dict = None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.payload = payload or {}


def run_json(cmd: List[str]) -> dict:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    payload = None
    for candidate in (proc.stdout, proc.stderr):
        if not candidate or not candidate.strip():
            continue
        try:
            payload = json.loads(candidate)
            break
        except Exception:
            continue
    if proc.returncode != 0:
        if isinstance(payload, dict):
            raise ExportError(payload.get("status", "QUERY_FAILED"), payload.get("message", "command failed"), payload)
        raise ExportError("QUERY_FAILED", proc.stderr.strip() or proc.stdout.strip() or "command failed")
    if not isinstance(payload, dict):
        raise ExportError("QUERY_FAILED", "failed to parse JSON output from group collector")
    return payload


def load_existing(path: Path) -> Dict[str, dict]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ExportError("QUERY_FAILED", "existing groups config must be a JSON array")
    out = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        group_id = item.get("group_id")
        if group_id is None:
            continue
        out[str(group_id)] = item
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a starter groups.json config from a live zsxq token")
    parser.add_argument("--token-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--disable-group-id", action="append", default=[])
    args = parser.parse_args()

    try:
        payload = run_json([
            sys.executable,
            str(COLLECT),
            "--token-file",
            args.token_file,
            "--mode",
            "groups",
        ])
        existing = load_existing(Path(args.output))
        disabled = {str(x) for x in args.disable_group_id}
        groups = payload.get("groups") or []
        result = []
        for group in groups:
            if not isinstance(group, dict):
                continue
            group_id = str(group.get("group_id"))
            current = existing.get(group_id, {})
            enabled_default = group_id not in disabled
            enabled = current.get("enabled", enabled_default)
            if group_id in disabled:
                enabled = False
            status = current.get("status") or ("ignored" if not enabled else "active")
            note = current.get("note") or ("set enabled=false if expired or intentionally ignored" if enabled else "disabled locally")
            result.append({
                "group_id": int(group_id) if group_id.isdigit() else group_id,
                "name": group.get("name") or group_id,
                "enabled": bool(enabled),
                "status": status,
                "note": note,
            })

        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({
            "status": "ok",
            "count": len(result),
            "output": str(out_path),
            "disabled_group_ids": sorted(disabled),
        }, ensure_ascii=False, indent=2))
    except ExportError as e:
        print(json.dumps({
            "status": e.status,
            "message": e.message,
            "mode": "export-groups-config",
            "details": e.payload,
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
