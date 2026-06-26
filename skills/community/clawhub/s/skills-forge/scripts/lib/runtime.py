import json
import subprocess


def run_json(command: list[str], check: bool = True) -> dict:
    completed = subprocess.run(command, check=check, text=True, capture_output=True)
    if not completed.stdout.strip():
        return {
            "status": "no-output",
            "returncode": completed.returncode,
            "stderr": completed.stderr.strip(),
        }
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "invalid-json",
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip()[:1024],
            "stderr": completed.stderr.strip()[:1024],
            "error": str(exc),
        }
    if isinstance(payload, dict):
        payload.setdefault("returncode", completed.returncode)
    return payload


def run_text(command: list[str]) -> str:
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    return completed.stdout.strip()
