import json
import os
import sys
from pathlib import Path


def read_payload(path=None):
    if path:
        raw = Path(path).read_bytes()
    else:
        raw = sys.stdin.buffer.read()
    if not raw.strip():
        return {}
    return json.loads(raw.decode("utf-8-sig", errors="replace"))


def envelope(result=None):
    base = {
        "success": True,
        "processedSources": [],
        "createdPages": [],
        "updatedPages": [],
        "archivedFiles": [],
        "skippedSources": [],
        "errors": [],
        "commitId": "",
    }
    base.update(result or {})
    return base


def write_result(path, result):
    data = envelope(result)
    if path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(f".{target.name}.{os.getpid()}.tmp")
        try:
            temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
    return data


def print_json(data):
    text = json.dumps(data or {}, ensure_ascii=False, indent=2) + "\n"
    sys.stdout.buffer.write(text.encode("utf-8"))
