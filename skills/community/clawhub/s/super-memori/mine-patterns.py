#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = Path.home() / ".openclaw" / "workspace"
LEARNINGS_DIR = WORKSPACE / ".learnings"
OUT_DIR = ROOT / "reports"
OUT_PATH = OUT_DIR / "pattern-report.json"

STOP = {
    "the", "and", "for", "with", "that", "this", "from", "into", "after", "before",
    "ошибка", "ошибки", "error", "failed", "failure", "lesson", "insight", "correction",
}


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\w\s-]", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokens(text: str) -> list[str]:
    toks = [t for t in normalize(text).split() if len(t) > 2 and t not in STOP]
    return toks[:32]


def representative_key(text: str) -> str:
    toks = tokens(text)
    if not toks:
        return "misc"
    return " ".join(toks[:10])


def parse_ts(text: str) -> date | None:
    try:
        return datetime.strptime(text.strip(), "%Y-%m-%dT%H:%M:%S%z").date()
    except Exception:
        return None


def read_learning_blocks() -> list[dict]:
    blocks: list[dict] = []
    if not LEARNINGS_DIR.exists():
        return blocks
    for path in sorted(LEARNINGS_DIR.rglob("*.md")):
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if path.name.isupper() or path.stem.isupper():
            continue
        current = None
        body_lines: list[str] = []
        for line in raw.splitlines():
            if line.startswith("## "):
                if current:
                    current["body"] = "\n".join(body_lines).strip()
                    blocks.append(current)
                title = line[3:].strip()
                current = {
                    "path": str(path),
                    "title": title,
                    "type": title.split("—", 1)[0].strip().casefold(),
                    "timestamp": title.split("—", 1)[1].strip() if "—" in title else None,
                    "status": "unknown",
                    "source": "unknown",
                    "tags": [],
                    "signature": None,
                    "source_confidence": None,
                    "conflict_status": "none",
                    "relations": {},
                }
                body_lines = []
                continue
            if not current:
                continue
            low = line.strip().lower()
            if low.startswith("- status:"):
                current["status"] = line.split(":", 1)[1].strip().casefold()
            elif low.startswith("- source:"):
                current["source"] = line.split(":", 1)[1].strip()
            elif low.startswith("- tags:"):
                current["tags"] = [t.strip() for t in line.split(":", 1)[1].split(",") if t.strip() and t.strip().lower() != "none"]
            elif low.startswith("- signature:"):
                sig = line.split(":", 1)[1].strip()
                current["signature"] = None if sig.lower() == "none" else sig
            elif low.startswith("- source_confidence:"):
                try:
                    current["source_confidence"] = float(line.split(":", 1)[1].strip())
                except Exception:
                    pass
            elif low.startswith("- conflict_status:"):
                current["conflict_status"] = line.split(":", 1)[1].strip().casefold()
            elif any(low.startswith(f"- {key}:") for key in ["supersedes", "contradicts", "confirms", "refines", "extends"]):
                key = low.split(":", 1)[0].replace("-", "").strip()
                values = [v.strip() for v in line.split(":", 1)[1].replace(";", ",").split(",") if v.strip()]
                current["relations"][key] = values
            else:
                body_lines.append(line)
        if current:
            current["body"] = "\n".join(body_lines).strip()
            blocks.append(current)
    return blocks


def reuse_signal(items: list[dict]) -> str:
    combined = normalize(" ".join((item.get("body") or "") for item in items))
    hits = sum(
        1
        for needle in [
            "reused successfully", "worked again", "still valid", "repeated use",
            "успешно переиспользовано", "работает повторно", "повторно сработало",
        ]
        if needle in combined
    )
    if hits >= 3:
        return "high"
    if hits == 2:
        return "moderate"
    if hits == 1:
        return "low"
    return "none"


def suggested_target(key: str, items: list[dict]) -> str:
    if any(item.get("type") == "correction" for item in items):
        return "procedural"
    if any(item.get("conflict_status") in {"superseded", "contradicted", "stale"} for item in items):
        return "lessons"
    if any(word in key for word in ["command", "script", "restart", "fix", "debug"]):
        return "procedural"
    if any(word in key for word in ["prefer", "always", "never", "infrastructure", "host"]):
        return "semantic"
    if any(word in key for word in ["mistake", "failure", "anti", "wrong"]):
        return "lessons"
    return "review-only"


def retrieval_signal(items: list[dict]) -> str:
    combined = normalize(" ".join((item.get("body") or "") + " " + " ".join(item.get("tags") or []) for item in items))
    if any(word in combined for word in ["fallback", "lexical", "semantic down", "degraded"]):
        return "lexical-fallback"
    if any(word in combined for word in ["no result", "miss", "not found", "missing knowledge"]):
        return "miss-cluster"
    if any(word in combined for word in ["stale", "reindex", "fragment", "orphan", "drift"]):
        return "index-fragmentation"
    return "review-needed" if len(items) >= 3 else "none"


def group_key(item: dict) -> str:
    return item.get("signature") or representative_key((item.get("body") or "") + " " + item.get("title", ""))


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in read_learning_blocks():
        body = (item.get("body") or "").strip()
        if not body:
            continue
        groups[group_key(item)].append(item)

    clusters = []
    for idx, (key, items) in enumerate(sorted(groups.items(), key=lambda kv: len(kv[1]), reverse=True), start=1):
        if key == "misc" and len(items) == 1:
            continue
        counts = Counter(tokens(" ".join((i.get("body") or "") for i in items)))
        confidence = "high" if len(items) >= 5 else "medium" if len(items) >= 3 else "low"
        days = [parse_ts(i.get("timestamp") or "") for i in items if parse_ts(i.get("timestamp") or "")]
        first_seen = min(days).isoformat() if days else None
        last_seen = max(days).isoformat() if days else None
        active_window_days = (max(days) - min(days)).days if len(days) >= 2 else 0
        recency_weight = "current"
        if days:
            age_days = (date.today() - max(days)).days
            if age_days > 90:
                recency_weight = "stale"
            elif age_days > 30:
                recency_weight = "cooling"
        reuse = reuse_signal(items)
        stale_success_candidate = bool(reuse in {"moderate", "high"} and recency_weight == "stale")
        source_files = sorted({i["path"] for i in items})
        relation_summary = defaultdict(int)
        for item in items:
            for rel_key, rel_values in (item.get("relations") or {}).items():
                relation_summary[rel_key] += len(rel_values)
        clusters.append({
            "cluster_id": f"pattern-{idx:03d}",
            "frequency": len(items),
            "representative_title": items[0]["title"],
            "normalized_key": key,
            "signature": items[0].get("signature"),
            "top_terms": [w for w, _ in counts.most_common(10)],
            "suggested_target": suggested_target(key, items),
            "retrieval_audit_signal": retrieval_signal(items),
            "reuse_signal": reuse,
            "confidence": confidence,
            "first_seen": first_seen,
            "last_seen": last_seen,
            "active_window_days": active_window_days,
            "recency_weight": recency_weight,
            "stale_success_candidate": stale_success_candidate,
            "source_files": source_files,
            "conflict_states": Counter(item.get("conflict_status", "none") for item in items),
            "relation_summary": dict(relation_summary),
            "review_status_mix": Counter(item.get("status", "unknown") for item in items),
        })

    report = {
        "status": "ok",
        "learnings_dir": str(LEARNINGS_DIR),
        "cluster_count": len(clusters),
        "clusters": clusters,
        "note": "Review-only report. Do not auto-promote without human approval.",
    }
    OUT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=lambda x: dict(x)), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, default=lambda x: dict(x)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
