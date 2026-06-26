#!/usr/bin/env python3
"""Memory Pipeline: Candidate -> Learning -> Promotion -> Dashboard.

This gives the self-improving system an observable queue between raw transcript
context and durable SQLite/skill promotion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.cwd()))
DEFAULT_SESSIONS_DIR = Path(os.environ.get("OPENCLAW_SESSIONS_DIR", Path.home() / ".openclaw" / "agents" / "main" / "sessions"))
DEFAULT_SESSION_KEY = os.environ.get("SELF_IMPROVING_MAIN_SESSION_KEY", "")
DEFAULT_BASE = DEFAULT_WORKSPACE / "learning" / "pipeline"
DEFAULT_CONTEXT_DIR = Path(os.environ.get("SELF_IMPROVING_PIPELINE_CONTEXT_DIR", DEFAULT_WORKSPACE / "learning" / "pipeline" / "context"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, item: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                rows.append({"status": "corrupt", "raw": line})
    return rows


def rewrite_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def text_from_content(content: Any, role: str) -> str:
    parts: list[str] = []
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    for item in content:
        if not isinstance(item, dict):
            continue
        typ = item.get("type")
        if typ == "text" and isinstance(item.get("text"), str):
            parts.append(item["text"])
        elif role == "user" and typ in {"image", "file", "audio", "video"}:
            parts.append(f"[{typ} attachment]")
    return "\n".join(p.strip() for p in parts if p and p.strip()).strip()


def resolve_session_file(sessions_dir: Path, session_key: str) -> tuple[str | None, Path | None, str | None]:
    sessions_json = sessions_dir / "sessions.json"
    sessions = load_json(sessions_json, {})
    if not isinstance(sessions, dict) or not sessions:
        return None, None, f"sessions_index_missing_or_empty: {sessions_json}"

    entry = sessions.get(session_key) if session_key else None
    if entry is None and not session_key:
        # Portable fallback: choose the most recent direct-message style session if available,
        # otherwise the most recently updated session. Operators can avoid ambiguity by setting
        # SELF_IMPROVING_MAIN_SESSION_KEY.
        items = list(sessions.items())
        direct = [(k, v) for k, v in items if isinstance(k, str) and ":direct:" in k and isinstance(v, dict)]
        candidates = direct or [(k, v) for k, v in items if isinstance(v, dict)]
        if candidates:
            session_key, entry = max(candidates, key=lambda kv: int(kv[1].get("updatedAtMs") or kv[1].get("lastActivityAtMs") or 0))
    if not entry:
        return None, None, f"session_key_not_found: {session_key or '<unset>'}"
    session_id = entry.get("sessionId")
    session_file = Path(entry.get("sessionFile") or (sessions_dir / f"{session_id}.jsonl"))
    if not session_file.exists():
        return session_id, session_file, f"session_file_missing: {session_file}"
    return session_id, session_file, None


def collect_messages(session_file: Path) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    with session_file.open("r", encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f, 1):
            raw = line.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if obj.get("type") != "message":
                continue
            msg = obj.get("message") or {}
            role = msg.get("role")
            if role not in {"user", "assistant"}:
                continue
            text = text_from_content(msg.get("content"), role)
            if not text:
                continue
            messages.append({
                "role": role,
                "text": text,
                "timestamp": obj.get("timestamp") or msg.get("timestamp"),
                "line": line_no,
                "id": obj.get("id"),
            })
    return messages


def clip(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + f"\n...[truncated {len(text)-max_chars} chars]"


def cmd_collect(args: argparse.Namespace) -> int:
    base = args.base
    context_dir = args.context_dir
    cursor_path = base / "cursor.json"
    out_json = context_dir / "incremental-context.json"
    out_md = context_dir / "incremental-context.md"
    session_id, session_file, err = resolve_session_file(args.sessions_dir, args.session_key)
    payload: dict[str, Any] = {
        "status": "blocked" if err else "ok",
        "generated_at": now_iso(),
        "session_key": args.session_key,
        "session_id": session_id,
        "session_file": str(session_file) if session_file else None,
        "messages": [],
    }
    if err:
        payload["error"] = err
        write_json(out_json, payload)
        write_incremental_md(out_md, payload, args.max_chars_per_message)
        print(json.dumps({"status": "blocked", "error": err, "out_json": str(out_json), "out_md": str(out_md)}, ensure_ascii=False))
        return 2

    assert session_file is not None
    cursor = load_json(cursor_path, {})
    same_file = cursor.get("session_file") == str(session_file)
    last_line = int(cursor.get("last_line", 0) or 0) if same_file else 0
    messages = [m for m in collect_messages(session_file) if int(m.get("line") or 0) > last_line]
    if args.limit and len(messages) > args.limit:
        messages = messages[-args.limit:]
    all_messages = collect_messages(session_file)
    current_last_line = max([int(m.get("line") or 0) for m in all_messages], default=0)
    payload.update({
        "cursor_path": str(cursor_path),
        "previous_last_line": last_line,
        "current_last_line": current_last_line,
        "new_messages": len(messages),
        "messages": messages,
        "out_json": str(out_json),
        "out_md": str(out_md),
    })
    write_json(out_json, payload)
    write_incremental_md(out_md, payload, args.max_chars_per_message)
    print(json.dumps({
        "status": payload["status"],
        "new_messages": len(messages),
        "previous_last_line": last_line,
        "current_last_line": current_last_line,
        "out_json": str(out_json),
        "out_md": str(out_md),
        "cursor_path": str(cursor_path),
    }, ensure_ascii=False))
    return 0


def write_incremental_md(path: Path, payload: dict[str, Any], max_chars: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Incremental Memory Pipeline Context",
        "",
        f"- status: `{payload.get('status')}`",
        f"- generated_at: `{payload.get('generated_at')}`",
        f"- session_key: `{payload.get('session_key')}`",
        f"- session_file: `{payload.get('session_file')}`",
        f"- previous_last_line: `{payload.get('previous_last_line', 0)}`",
        f"- current_last_line: `{payload.get('current_last_line', 0)}`",
        f"- new_messages: `{len(payload.get('messages', []))}`",
    ]
    if payload.get("error"):
        lines.append(f"- error: `{payload['error']}`")
    lines += ["", "## New Messages", ""]
    for idx, m in enumerate(payload.get("messages", []), 1):
        lines += [f"### {idx}. {m.get('role')} — line {m.get('line')} — {m.get('timestamp') or ''}", "", clip(str(m.get("text") or ""), max_chars), ""]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def cmd_commit_cursor(args: argparse.Namespace) -> int:
    payload = load_json(args.context_json, {})
    if payload.get("status") != "ok":
        print(json.dumps({"status": "blocked", "error": "context_not_ok"}, ensure_ascii=False))
        return 2
    cursor = {
        "updated_at": now_iso(),
        "session_key": payload.get("session_key"),
        "session_id": payload.get("session_id"),
        "session_file": payload.get("session_file"),
        "last_line": payload.get("current_last_line", 0),
        "last_context_json": str(args.context_json),
    }
    write_json(args.base / "cursor.json", cursor)
    print(json.dumps({"status": "ok", "cursor": cursor}, ensure_ascii=False))
    return 0


def stable_id(prefix: str, fields: list[str]) -> str:
    h = hashlib.sha256("\n".join(fields).encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{h}"


def cmd_add_candidate(args: argparse.Namespace) -> int:
    if args.json_stdin:
        data = json.load(sys.stdin)
    else:
        data = {
            "kind": args.kind,
            "summary": args.summary,
            "details": args.details,
            "evidence": args.evidence,
            "source": args.source,
            "confidence": args.confidence,
            "promotion_target": args.promotion_target,
            "search_terms": args.search_terms,
        }
    summary = str(data.get("summary") or "").strip()
    if not summary:
        print(json.dumps({"status": "blocked", "error": "missing_summary"}, ensure_ascii=False))
        return 2
    item = {
        "id": data.get("id") or stable_id("CAND", [summary, str(data.get("evidence") or "")]),
        "created_at": data.get("created_at") or now_iso(),
        "updated_at": now_iso(),
        "status": data.get("status") or "new",
        "kind": data.get("kind") or "learning",
        "summary": summary,
        "details": data.get("details") or "",
        "evidence": data.get("evidence") or "",
        "source": data.get("source") or "unknown",
        "confidence": float(data.get("confidence") or 0.5),
        "promotion_target": data.get("promotion_target") or "",
        "search_terms": data.get("search_terms") or [],
        "linked_entry": data.get("linked_entry") or "",
    }
    candidates_path = args.base / "candidates.jsonl"
    rows = read_jsonl(candidates_path)
    if any(r.get("id") == item["id"] for r in rows):
        print(json.dumps({"status": "duplicate", "id": item["id"]}, ensure_ascii=False))
        return 0
    append_jsonl(candidates_path, item)
    print(json.dumps({"status": "ok", "id": item["id"], "path": str(candidates_path)}, ensure_ascii=False))
    return 0


def cmd_mark_candidate(args: argparse.Namespace) -> int:
    path = args.base / "candidates.jsonl"
    rows = read_jsonl(path)
    found = False
    for row in rows:
        if row.get("id") == args.id:
            row["status"] = args.status
            row["updated_at"] = now_iso()
            if args.linked_entry:
                row["linked_entry"] = args.linked_entry
            if args.note:
                row["note"] = args.note
            found = True
    rewrite_jsonl(path, rows)
    print(json.dumps({"status": "ok" if found else "not_found", "id": args.id}, ensure_ascii=False))
    return 0 if found else 2


def cmd_add_promotion(args: argparse.Namespace) -> int:
    if args.json_stdin:
        data = json.load(sys.stdin)
    else:
        data = {
            "source": args.source,
            "target": args.target,
            "reason": args.reason,
            "patch_summary": args.patch_summary,
            "confidence": args.confidence,
        }
    source = str(data.get("source") or "").strip()
    target = str(data.get("target") or "").strip()
    if not source or not target:
        print(json.dumps({"status": "blocked", "error": "missing_source_or_target"}, ensure_ascii=False))
        return 2
    item = {
        "id": data.get("id") or stable_id("PROMO", [source, target, str(data.get("reason") or "")]),
        "created_at": data.get("created_at") or now_iso(),
        "updated_at": now_iso(),
        "status": data.get("status") or "pending_review",
        "source": source,
        "target": target,
        "reason": data.get("reason") or "",
        "patch_summary": data.get("patch_summary") or "",
        "confidence": float(data.get("confidence") or 0.5),
    }
    path = args.base / "promotion-queue.json"
    rows = load_json(path, [])
    if not isinstance(rows, list):
        rows = []
    if any(r.get("id") == item["id"] for r in rows):
        print(json.dumps({"status": "duplicate", "id": item["id"]}, ensure_ascii=False))
        return 0
    rows.append(item)
    write_json(path, rows)
    print(json.dumps({"status": "ok", "id": item["id"], "path": str(path)}, ensure_ascii=False))
    return 0


def cmd_mark_promotion(args: argparse.Namespace) -> int:
    path = args.base / "promotion-queue.json"
    rows = load_json(path, [])
    if not isinstance(rows, list):
        rows = []
    found = False
    for row in rows:
        if row.get("id") == args.id:
            row["status"] = args.status
            row["updated_at"] = now_iso()
            if args.note:
                row["note"] = args.note
            found = True
    write_json(path, rows)
    print(json.dumps({"status": "ok" if found else "not_found", "id": args.id}, ensure_ascii=False))
    return 0 if found else 2


def cmd_dashboard(args: argparse.Namespace) -> int:
    base = args.base
    candidates = read_jsonl(base / "candidates.jsonl")
    promotions = load_json(base / "promotion-queue.json", [])
    if not isinstance(promotions, list):
        promotions = []
    cursor = load_json(base / "cursor.json", {})
    # Best-effort current line check.
    _sid, session_file, err = resolve_session_file(args.sessions_dir, args.session_key)
    current_last_line = None
    if not err and session_file:
        current_last_line = max([int(m.get("line") or 0) for m in collect_messages(session_file)], default=0)
    last_line = int(cursor.get("last_line", 0) or 0)
    unprocessed = max(0, (current_last_line or last_line) - last_line)
    cand_counts: dict[str, int] = {}
    for c in candidates:
        cand_counts[c.get("status", "unknown")] = cand_counts.get(c.get("status", "unknown"), 0) + 1
    promo_counts: dict[str, int] = {}
    for p in promotions:
        promo_counts[p.get("status", "unknown")] = promo_counts.get(p.get("status", "unknown"), 0) + 1
    status = {
        "generated_at": now_iso(),
        "cursor": cursor,
        "current_last_line": current_last_line,
        "unprocessed_messages": unprocessed,
        "candidates": {"total": len(candidates), "by_status": cand_counts},
        "promotions": {"total": len(promotions), "by_status": promo_counts},
        "paths": {
            "cursor": str(base / "cursor.json"),
            "candidates": str(base / "candidates.jsonl"),
            "promotions": str(base / "promotion-queue.json"),
            "dashboard": str(base / "dashboard.md"),
        },
    }
    write_json(base / "status.json", status)
    write_dashboard_md(base / "dashboard.md", status, candidates, promotions)
    # Convenience top-level dashboard for quick inspection from workspace/learning/.
    if base.name == "pipeline" and base.parent.name == "learning":
        write_dashboard_md(base.parent / "dashboard.md", status, candidates, promotions)
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0


def write_dashboard_md(path: Path, status: dict[str, Any], candidates: list[dict[str, Any]], promotions: list[dict[str, Any]]) -> None:
    lines = [
        "# Memory Pipeline Dashboard",
        "",
        f"Generated: `{status['generated_at']}`",
        "",
        "## Coverage",
        "",
        f"- last processed line: `{status.get('cursor', {}).get('last_line', 0)}`",
        f"- current last line: `{status.get('current_last_line')}`",
        f"- unprocessed messages: `{status.get('unprocessed_messages')}`",
        "",
        "## Candidates",
        "",
        f"- total: `{status['candidates']['total']}`",
    ]
    for k, v in sorted(status["candidates"]["by_status"].items()):
        lines.append(f"- {k}: `{v}`")
    lines += ["", "### Open candidates", ""]
    open_candidates = [c for c in candidates if c.get("status") in {"new", "duplicate_pending", "learning_pending"}]
    if not open_candidates:
        lines.append("_None._")
    for c in open_candidates[-20:]:
        lines.append(f"- `{c.get('id')}` [{c.get('kind')}/{c.get('status')}] {c.get('summary')}")
    lines += ["", "## Promotions", "", f"- total: `{status['promotions']['total']}`"]
    for k, v in sorted(status["promotions"]["by_status"].items()):
        lines.append(f"- {k}: `{v}`")
    lines += ["", "### Pending promotions", ""]
    pending = [p for p in promotions if p.get("status") in {"pending", "pending_review"}]
    if not pending:
        lines.append("_None._")
    for p in pending[-20:]:
        lines.append(f"- `{p.get('id')}` {p.get('source')} → `{p.get('target')}`: {p.get('patch_summary') or p.get('reason')}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Memory Pipeline: Candidate -> Learning -> Promotion")
    ap.add_argument("--base", type=Path, default=DEFAULT_BASE)
    ap.add_argument("--sessions-dir", type=Path, default=DEFAULT_SESSIONS_DIR)
    ap.add_argument("--session-key", default=DEFAULT_SESSION_KEY)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("collect-incremental")
    p.add_argument("--context-dir", type=Path, default=DEFAULT_CONTEXT_DIR)
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--max-chars-per-message", type=int, default=5000)
    p.set_defaults(func=cmd_collect)

    p = sub.add_parser("commit-cursor")
    p.add_argument("--context-json", type=Path, default=DEFAULT_CONTEXT_DIR / "incremental-context.json")
    p.set_defaults(func=cmd_commit_cursor)

    p = sub.add_parser("add-candidate")
    p.add_argument("--json-stdin", action="store_true")
    p.add_argument("--kind", default="learning")
    p.add_argument("--summary", default="")
    p.add_argument("--details", default="")
    p.add_argument("--evidence", default="")
    p.add_argument("--source", default="unknown")
    p.add_argument("--confidence", type=float, default=0.5)
    p.add_argument("--promotion-target", default="")
    p.add_argument("--search-terms", nargs="*", default=[])
    p.set_defaults(func=cmd_add_candidate)

    p = sub.add_parser("mark-candidate")
    p.add_argument("id")
    p.add_argument("--status", required=True)
    p.add_argument("--linked-entry", default="")
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_mark_candidate)

    p = sub.add_parser("add-promotion")
    p.add_argument("--json-stdin", action="store_true")
    p.add_argument("--source", default="")
    p.add_argument("--target", default="")
    p.add_argument("--reason", default="")
    p.add_argument("--patch-summary", default="")
    p.add_argument("--confidence", type=float, default=0.5)
    p.set_defaults(func=cmd_add_promotion)

    p = sub.add_parser("mark-promotion")
    p.add_argument("id")
    p.add_argument("--status", required=True)
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_mark_promotion)

    p = sub.add_parser("dashboard")
    p.set_defaults(func=cmd_dashboard)

    args = ap.parse_args()
    args.base.mkdir(parents=True, exist_ok=True)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
