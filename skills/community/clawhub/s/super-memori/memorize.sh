#!/usr/bin/env python3
# Exit codes: 0=written/duplicate, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from super_memori_common import LEARNINGS_DIR, QUEUE_DIR, VALID_LEARNING_TYPES, MAX_LEARNING_CHARS, ensure_dirs, learning_text_exists, now_iso, validate_relation_target

VALID_CONFLICT_STATUS = {"none", "active", "superseded", "contradicted", "stale"}


class MemoriArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(message, file=sys.stderr)
        raise SystemExit(4)


def normalize_list_arg(value: str) -> list[str]:
    items = []
    for piece in value.replace(";", ",").split(","):
        cleaned = piece.strip()
        if cleaned:
            items.append(cleaned)
    return items


def derive_signature(text: str, learning_type: str, tags: list[str], source: str) -> str:
    head = " ".join(text.strip().split())[:180].casefold()
    payload = json.dumps({"type": learning_type, "source": source.casefold(), "tags": sorted(tag.casefold() for tag in tags), "head": head}, ensure_ascii=False)
    import hashlib
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    p = MemoriArgumentParser(description="Record a useful learning entry")
    p.add_argument("text")
    p.add_argument("type", nargs="?", default="lesson")
    p.add_argument("--pending", action="store_true")
    p.add_argument("--reviewed", action="store_true")
    p.add_argument("--tags", default="")
    p.add_argument("--source", default="agent")
    p.add_argument("--signature", default="")
    p.add_argument("--source-confidence", type=float)
    p.add_argument("--conflict-status", default="none")
    p.add_argument("--supersedes", default="")
    p.add_argument("--contradicts", default="")
    p.add_argument("--confirms", default="")
    p.add_argument("--refines", default="")
    p.add_argument("--extends", dest="extends_rel", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.type not in VALID_LEARNING_TYPES:
        print(f"invalid learning type: {args.type}", file=sys.stderr)
        return 4
    if args.conflict_status not in VALID_CONFLICT_STATUS:
        print(f"invalid conflict status: {args.conflict_status}", file=sys.stderr)
        return 4
    if args.source_confidence is not None and not (0.0 <= args.source_confidence <= 1.0):
        print("source confidence must be between 0.0 and 1.0", file=sys.stderr)
        return 4

    ensure_dirs()
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    day = time.strftime("%Y-%m-%d")
    target = LEARNINGS_DIR / f"{day}.md"
    status = "reviewed" if args.reviewed else "pending"
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    text = args.text.strip()
    truncated = False
    if len(text) > MAX_LEARNING_CHARS:
        text = text[:MAX_LEARNING_CHARS].rstrip() + "\n[truncated]"
        truncated = True

    signature = args.signature.strip() or derive_signature(text, args.type, tags, args.source)
    duplicate_path = learning_text_exists(text, signature=signature)
    if duplicate_path:
        payload = {
            "status": "duplicate",
            "file": str(duplicate_path),
            "type": args.type,
            "review_status": status,
            "signature": signature,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"duplicate skipped: {duplicate_path}")
        return 0

    if not target.exists():
        target.write_text(f"# Learnings — {day}\n\n", encoding="utf-8")

    relation_map = {
        "supersedes": normalize_list_arg(args.supersedes),
        "contradicts": normalize_list_arg(args.contradicts),
        "confirms": normalize_list_arg(args.confirms),
        "refines": normalize_list_arg(args.refines),
        "extends": normalize_list_arg(args.extends_rel),
    }
    for rel_key, targets in relation_map.items():
        for target in targets:
            ok, reason = validate_relation_target(rel_key, target)
            if not ok:
                print(f"invalid relation target for {rel_key}: {target} ({reason})", file=sys.stderr)
                return 4
    relation_lines = []
    for key, values in relation_map.items():
        if values:
            relation_lines.append(f"- {key}: {', '.join(values)}")
    source_confidence = args.source_confidence if args.source_confidence is not None else (0.7 if status == "reviewed" else 0.45)

    block = (
        f"## {args.type} — {now_iso()}\n"
        f"- status: {status}\n"
        f"- source: {args.source}\n"
        f"- tags: {', '.join(tags) if tags else 'none'}\n"
        f"- signature: {signature}\n"
        f"- source_confidence: {source_confidence:.2f}\n"
        f"- conflict_status: {args.conflict_status}\n"
        + ("\n".join(relation_lines) + "\n" if relation_lines else "")
        + f"\n{text}\n\n"
    )
    existing_text = target.read_text(encoding="utf-8", errors="ignore") if target.exists() else f"# Learnings — {day}\n\n"
    merged_text = existing_text + block
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(target.parent), prefix=f"{target.name}.", suffix=".tmp") as tmp:
        tmp.write(merged_text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, target)

    queue_item = QUEUE_DIR / f"learn-{int(time.time())}.json"
    queue_item.write_text(json.dumps({
        "kind": "learning",
        "file": str(target),
        "type": args.type,
        "review_status": status,
        "source": args.source,
        "tags": tags,
        "signature": signature,
        "source_confidence": source_confidence,
        "conflict_status": args.conflict_status,
        "relations": relation_map,
        "created_at": now_iso(),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = {
        "status": "written",
        "file": str(target),
        "queue_item": str(queue_item),
        "type": args.type,
        "review_status": status,
        "truncated": truncated,
        "signature": signature,
        "source_confidence": source_confidence,
        "conflict_status": args.conflict_status,
        "relations": relation_map,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"written: {target}\nqueued: {queue_item}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"memorize internal error: {exc}", file=sys.stderr)
        raise SystemExit(5)
