#!/usr/bin/env python3
"""Build a source-indexed, reasoning-safe atlas index from a Claude JSONL session."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def compact(text: str, limit: int = 280) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1] + "…"


def content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "text":
            parts.append(str(block.get("text", "")))
    return "\n".join(part for part in parts if part)


def classify_prompt(record: dict[str, Any], text: str) -> str:
    origin = record.get("origin") or {}
    if origin.get("kind") == "human":
        return "human"
    if text.startswith("<task-notification>"):
        return "task-notification"
    if "Another Claude session sent a message:" in text:
        return "peer-message"
    if text.startswith("<codex-monitor") or "codex-monitor observation" in text:
        return "monitor-message"
    if text:
        return "external-message"
    return "none"


def summarize_tool_input(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raw = json.dumps(value, sort_keys=True, ensure_ascii=False)
        return {"summary": compact(raw), "sha256": sha256_text(raw), "bytes": len(raw)}

    summary: dict[str, Any] = {}
    for key in (
        "description",
        "command",
        "file_path",
        "path",
        "pattern",
        "query",
        "skill",
        "task_id",
        "prompt",
    ):
        if key in value:
            raw = str(value[key])
            summary[key] = raw if key in {"file_path", "path", "skill", "task_id"} else compact(raw, 500)

    if name == "Write" and "content" in value:
        raw = str(value["content"])
        summary["content_bytes"] = len(raw.encode("utf-8"))
        summary["content_sha256"] = sha256_text(raw)
    if name == "Edit":
        for key in ("old_string", "new_string"):
            if key in value:
                raw = str(value[key])
                summary[f"{key}_bytes"] = len(raw.encode("utf-8"))
                summary[f"{key}_sha256"] = sha256_text(raw)

    raw_json = json.dumps(value, sort_keys=True, ensure_ascii=False)
    summary["input_sha256"] = sha256_text(raw_json)
    summary["input_bytes"] = len(raw_json.encode("utf-8"))
    return summary


def result_content(block: dict[str, Any]) -> str:
    value = block.get("content", "")
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def prompt_anchor(record: dict[str, Any]) -> tuple[str, str] | None:
    if record.get("type") != "user":
        return None
    text = content_text((record.get("message") or {}).get("content"))
    if not text:
        return None
    content = (record.get("message") or {}).get("content")
    if isinstance(content, list) and all(
        isinstance(block, dict) and block.get("type") == "tool_result" for block in content
    ):
        return None
    return classify_prompt(record, text), text


def iter_blocks(record: dict[str, Any], kind: str) -> Iterable[dict[str, Any]]:
    if record.get("type") != kind:
        return []
    content = (record.get("message") or {}).get("content")
    return content if isinstance(content, list) else []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument(
        "--snapshot-label",
        default=None,
        help="Stable human label; defaults to session id and the final timestamp.",
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    out_dir = args.out_dir.expanduser().absolute()
    if out_dir.exists() or out_dir.is_symlink():
        raise SystemExit("Refusing existing output path; choose a fresh private directory")

    raw = source.read_bytes()
    records: list[dict[str, Any]] = []
    parse_errors: list[dict[str, Any]] = []
    for line_no, line in enumerate(raw.splitlines(), start=1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            parse_errors.append({"line": line_no, "error": str(exc)})
            continue
        if not isinstance(item, dict):
            parse_errors.append({"line": line_no, "error": "expected JSON object"})
            continue
        item["_atlas_line"] = line_no
        records.append(item)

    if parse_errors:
        raise SystemExit(f"Refusing partial index: {len(parse_errors)} JSON parse errors")

    type_counts = collections.Counter(str(record.get("type", "unknown")) for record in records)
    block_counts: collections.Counter[str] = collections.Counter()
    prompt_counts: collections.Counter[str] = collections.Counter()
    tool_counts: collections.Counter[str] = collections.Counter()
    timestamps = [str(r["timestamp"]) for r in records if r.get("timestamp")]
    session_ids = sorted({str(r["sessionId"]) for r in records if r.get("sessionId")})

    tool_calls: dict[str, dict[str, Any]] = {}
    tool_results: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    thinking_hashes: list[dict[str, Any]] = []

    for record in records:
        for block in iter_blocks(record, "assistant"):
            block_type = str(block.get("type", "unknown"))
            block_counts[f"assistant:{block_type}"] += 1
            if block_type == "tool_use":
                tool_id = str(block.get("id", ""))
                name = str(block.get("name", "unknown"))
                tool_counts[name] += 1
                tool_calls[tool_id] = {
                    "id": tool_id,
                    "name": name,
                    "line": record["_atlas_line"],
                    "timestamp": record.get("timestamp"),
                    "input": summarize_tool_input(name, block.get("input")),
                }
            elif block_type == "thinking":
                # Never reproduce private chain-of-thought. Hashing proves coverage.
                text = str(block.get("thinking", ""))
                thinking_hashes.append(
                    {
                        "line": record["_atlas_line"],
                        "bytes": len(text.encode("utf-8")),
                        "sha256": sha256_text(text),
                    }
                )
        for block in iter_blocks(record, "user"):
            block_type = str(block.get("type", "unknown"))
            block_counts[f"user:{block_type}"] += 1
            if block_type == "tool_result":
                tool_id = str(block.get("tool_use_id", ""))
                text = result_content(block)
                tool_results[tool_id].append(
                    {
                        "line": record["_atlas_line"],
                        "timestamp": record.get("timestamp"),
                        "is_error": bool(block.get("is_error", False)),
                        "bytes": len(text.encode("utf-8")),
                        "sha256": sha256_text(text),
                        "preview": compact(text, 500),
                    }
                )

    turns: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    def finish_turn(end_line: int) -> None:
        nonlocal current
        if current is None:
            return
        current["end_line"] = end_line
        current["assistant_text_bytes"] = sum(
            len(text.encode("utf-8")) for text in current["assistant_text"]
        )
        current["tool_counts"] = dict(collections.Counter(current.pop("_tool_names")))
        turns.append(current)
        current = None

    for record in records:
        anchor = prompt_anchor(record)
        if anchor:
            finish_turn(record["_atlas_line"] - 1)
            prompt_kind, text = anchor
            prompt_counts[prompt_kind] += 1
            current = {
                "turn": len(turns) + 1,
                "kind": prompt_kind,
                "start_line": record["_atlas_line"],
                "end_line": record["_atlas_line"],
                "timestamp": record.get("timestamp"),
                "uuid": record.get("uuid"),
                "prompt": text,
                "prompt_sha256": sha256_text(text),
                "assistant_text": [],
                "tool_calls": [],
                "_tool_names": [],
            }

        if current is None:
            continue

        if record.get("type") == "assistant":
            for block in iter_blocks(record, "assistant"):
                if block.get("type") == "text":
                    current["assistant_text"].append(str(block.get("text", "")))
                elif block.get("type") == "tool_use":
                    tool_id = str(block.get("id", ""))
                    call = dict(tool_calls.get(tool_id, {}))
                    call["results"] = tool_results.get(tool_id, [])
                    current["tool_calls"].append(call)
                    current["_tool_names"].append(str(block.get("name", "unknown")))

    finish_turn(records[-1]["_atlas_line"] if records else 0)

    label = args.snapshot_label
    if not label:
        session = session_ids[0] if len(session_ids) == 1 else "mixed-session"
        tail = timestamps[-1] if timestamps else "undated"
        label = f"{session}@{tail}"

    manifest = {
        "schema_version": 1,
        "snapshot_label": label,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": str(source),
        "source_bytes": len(raw),
        "source_lines": len(raw.splitlines()),
        "source_sha256": sha256_bytes(raw),
        "session_ids": session_ids,
        "first_timestamp": timestamps[0] if timestamps else None,
        "last_timestamp": timestamps[-1] if timestamps else None,
        "record_count": len(records),
        "record_type_counts": dict(type_counts),
        "content_block_counts": dict(block_counts),
        "prompt_kind_counts": dict(prompt_counts),
        "tool_counts": dict(tool_counts),
        "semantic_turns": len(turns),
        "tool_calls": len(tool_calls),
        "tool_results": sum(len(items) for items in tool_results.values()),
        "unmatched_tool_calls": sorted(tool_id for tool_id in tool_calls if tool_id not in tool_results),
        "orphan_tool_results": sorted(tool_id for tool_id in tool_results if tool_id not in tool_calls),
        "thinking_policy": "Counted and hashed for coverage; private reasoning text is not reproduced.",
        "thinking_blocks": len(thinking_hashes),
        "parse_errors": parse_errors,
    }

    # A fresh private directory prevents truncating prior indexes or following their links.
    # Require its parent to exist so intermediate directories are never made permissive.
    out_dir.mkdir(mode=0o700)
    os.umask(0o077)
    (out_dir / "snapshot-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with (out_dir / "turn-index.jsonl").open("w", encoding="utf-8") as handle:
        for turn in turns:
            handle.write(json.dumps(turn, sort_keys=True, ensure_ascii=False) + "\n")
    with (out_dir / "thinking-coverage.jsonl").open("w", encoding="utf-8") as handle:
        for item in thinking_hashes:
            handle.write(json.dumps(item, sort_keys=True) + "\n")

    summary_lines = [
        "# Claude session source index",
        "",
        f"- Snapshot: `{label}`",
        f"- Source SHA-256: `{manifest['source_sha256']}`",
        f"- Bounds: `{manifest['first_timestamp']}` → `{manifest['last_timestamp']}`",
        f"- Coverage: {manifest['record_count']} JSONL records; {len(turns)} semantic turns",
        f"- Tool evidence: {manifest['tool_calls']} calls; {manifest['tool_results']} results",
        "- Private reasoning: covered by count/hash only; not reproduced",
        "",
        "| Turn | Time | Kind | Source | Prompt | Tools |",
        "|---:|---|---|---|---|---|",
    ]
    for turn in turns:
        tools = ", ".join(
            f"{name}×{count}" for name, count in sorted(turn["tool_counts"].items())
        )
        prompt = compact(turn["prompt"], 180).replace("|", "\\|")
        summary_lines.append(
            f"| {turn['turn']} | {turn['timestamp'] or ''} | {turn['kind']} | "
            f"L{turn['start_line']}–L{turn['end_line']} | {prompt} | {tools} |"
        )
    (out_dir / "source-index.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
