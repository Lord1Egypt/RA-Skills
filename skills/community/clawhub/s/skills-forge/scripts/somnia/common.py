#!/usr/bin/env python3
import datetime as dt
import json
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR.parent
DEFAULT_TARGET_ROOT = Path.home() / ".openclaw" / "workspace" / "skills"
DEFAULT_FEEDBACK_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-feedback.jsonl"
DEFAULT_REPLAY_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-replay-cases.jsonl"
DEFAULT_REPORT_ROOT = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-forge-nightly"
DEFAULT_UPDATE_ROOT = Path.home() / ".openclaw" / "workspace" / "skill-forge-updates"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def date_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def run_json(command: list[str], check: bool = False) -> dict:
    completed = subprocess.run(command, text=True, capture_output=True, check=check)
    if not completed.stdout.strip():
        return {"status": "no-output", "returncode": completed.returncode, "stderr": completed.stderr.strip()}
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        payload = {"status": "invalid-json", "stdout": completed.stdout, "stderr": completed.stderr}
    payload.setdefault("returncode", completed.returncode)
    return payload


def load_env_file(path: str) -> None:
    if not path:
        return
    env_path = Path(path).expanduser()
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_manifest(target_root: Path) -> dict:
    path = target_root / ".skill-forge-installs.json"
    if not path.exists():
        return {"installs": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"installs": {}, "manifest_error": "invalid-json"}

