#!/usr/bin/env python3
"""smart-message-plus: send log (JSONL, rolling) + recall routing index."""
from __future__ import annotations

import json
import time
from datetime import datetime

from . import config as C

MAX_ENTRIES = 500


def _path():
    return C.data_dir() / "send_log.jsonl"


def record(
    provider: str,
    account: str,
    msg_id: str,
    send_mode: str,  # p2p | group | broadcast
    target: str,
    preview: str,
    chat_id: str = "",
    extra: dict | None = None,
) -> None:
    entry = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "epoch": time.time(),
        "provider": provider,
        "account": account,
        "msg_id": msg_id,
        "send_mode": send_mode,
        "target": target,
        "chat_id": chat_id,
        "preview": preview[:80],
    }
    if extra:
        entry.update(extra)
    p = _path()
    lines = []
    if p.exists():
        with open(p, encoding="utf-8") as f:
            lines = f.read().splitlines()
    lines.append(json.dumps(entry, ensure_ascii=False))
    if len(lines) > MAX_ENTRIES:
        lines = lines[-MAX_ENTRIES:]
    tmp = p.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    tmp.replace(p)


def find(msg_id: str) -> dict | None:
    p = _path()
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        for line in f.read().splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if e.get("msg_id") == msg_id:
                return e
    return None


def recent(n: int = 20) -> list[dict]:
    p = _path()
    if not p.exists():
        return []
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f.read().splitlines()[-n:]:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def broadcast_audit(
    sender: str, provider: str, mode: str, count: int, preview: str, targets_sample: list
) -> None:
    """Audit log for large sends (> warn threshold)."""
    p = C.data_dir() / "broadcast_log.jsonl"
    entry = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender": sender,
        "provider": provider,
        "mode": mode,
        "count": count,
        "preview": preview[:100],
        "targets_sample": targets_sample[:10],
    }
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
