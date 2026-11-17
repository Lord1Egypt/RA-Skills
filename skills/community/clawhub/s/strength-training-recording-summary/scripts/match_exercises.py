#!/usr/bin/env python3
"""Fuzzy-match workout exercise names against hasaneyldrm/exercises-dataset.

The helper intentionally returns compact top matches, not the whole dataset.
It uses only the Python standard library so a future agent can run it without
installing dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

DEFAULT_DATASET_URL = (
    "https://raw.githubusercontent.com/hasaneyldrm/"
    "exercises-dataset/main/data/exercises.json"
)
DEFAULT_CACHE = Path.home() / ".cache" / "strength-training-recording-summary" / "exercises.json"
LANGS = ("en", "es", "it", "tr", "ru", "zh", "hi", "pl", "ko")
ZH_ALIASES = {
    "哑铃": "dumbbell",
    "杠铃": "barbell",
    "壶铃": "kettlebell",
    "弹力带": "band",
    "绳索": "cable",
    "史密斯": "smith",
    "深蹲": "squat",
    "硬拉": "deadlift",
    "卧推": "bench press",
    "推举": "press",
    "肩推": "shoulder press",
    "划船": "row",
    "弓步": "lunge",
    "箭步": "lunge",
    "俯卧撑": "push up",
    "引体向上": "pull up",
    "卷腹": "crunch",
    "平板支撑": "plank",
    "臀桥": "glute bridge",
    "侧平举": "lateral raise",
    "侧举": "lateral raise",
    "前平举": "front raise",
    "平举": "raise",
    "二头弯举": "biceps curl",
    "弯举": "curl",
    "三头": "triceps",
}


def normalize(text: Any) -> str:
    raw = unicodedata.normalize("NFKC", str(text or "")).casefold()
    # Keep word characters and CJK ranges; turn punctuation into spaces.
    raw = re.sub(r"[^\w\u3400-\u9fff]+", " ", raw)
    return re.sub(r"\s+", " ", raw).strip()


def expand_aliases(text: str, lang: str) -> str:
    if lang != "zh":
        return text
    aliases = [english for zh, english in ZH_ALIASES.items() if zh in text]
    return f"{text} {' '.join(aliases)}" if aliases else text


def compact_steps(record: dict[str, Any], lang: str, limit: int) -> list[str]:
    steps = record.get("instruction_steps", {})
    if not isinstance(steps, dict):
        steps = {}
    selected = steps.get(lang) or steps.get("en") or []
    if isinstance(selected, str):
        selected = [selected]
    return [str(s).strip() for s in selected[:limit] if str(s).strip()]


def instruction_text(record: dict[str, Any], lang: str) -> str:
    instructions = record.get("instructions", {})
    if not isinstance(instructions, dict):
        return ""
    value = instructions.get(lang) or instructions.get("en") or ""
    if isinstance(value, list):
        return " ".join(str(v) for v in value)
    return str(value)


def search_blob(record: dict[str, Any], lang: str) -> str:
    fields: list[str] = [
        record.get("name"),
        record.get("category"),
        record.get("body_part"),
        record.get("equipment"),
        record.get("target"),
        record.get("muscle_group"),
    ]
    fields.extend(record.get("secondary_muscles") or [])
    fields.extend(compact_steps(record, lang, 3))
    fields.append(instruction_text(record, lang)[:500])
    return normalize(" ".join(str(f) for f in fields if f))


def score_candidate(query: str, record: dict[str, Any], lang: str) -> tuple[float, list[str]]:
    expanded_query = expand_aliases(query, lang)
    q = normalize(expanded_query)
    name = normalize(record.get("name"))
    equipment = normalize(record.get("equipment"))
    target = normalize(record.get("target"))
    body_part = normalize(record.get("body_part") or record.get("category"))
    blob = search_blob(record, lang)

    if not q:
        return 0.0, []

    name_ratio = SequenceMatcher(None, q, name).ratio()
    blob_ratio = SequenceMatcher(None, q, blob[: max(120, len(q) * 4)]).ratio()

    q_tokens = set(q.split())
    name_tokens = set(name.split())
    blob_tokens = set(blob.split())
    token_overlap = len(q_tokens & name_tokens) / max(1, len(q_tokens))
    blob_overlap = len(q_tokens & blob_tokens) / max(1, len(q_tokens))
    extra_name_tokens = max(0, len(name_tokens - q_tokens))

    substring_bonus = 0.0
    reasons: list[str] = []
    if q and q in name:
        # A raw substring can over-rank narrow variants, e.g. "barbell squat
        # (on knees)" for the generic query "barbell squat". Keep the bonus,
        # but scale it down when the dataset name has many extra qualifiers.
        substring_bonus += max(0.08, 0.20 - 0.025 * extra_name_tokens)
        reasons.append("query_in_name")
    elif q and q in blob:
        substring_bonus += 0.08
        reasons.append("query_in_metadata")
    elif q_tokens and q_tokens <= name_tokens:
        substring_bonus += max(0.04, 0.12 - 0.02 * extra_name_tokens)
        reasons.append("query_tokens_in_name")

    score = (
        name_ratio * 0.50
        + token_overlap * 0.25
        + blob_ratio * 0.10
        + blob_overlap * 0.10
        + substring_bonus
    )

    if token_overlap:
        reasons.append("name_token_overlap")
    if expanded_query != query and token_overlap:
        reasons.append("translated_alias")
    if blob_overlap and not token_overlap:
        reasons.append("metadata_token_overlap")
    if equipment and equipment in q:
        score += 0.04
        reasons.append("equipment_context")
    if target and target in q:
        score += 0.04
        reasons.append("target_context")
    if body_part and body_part in q:
        score += 0.03
        reasons.append("body_part_context")

    if extra_name_tokens >= 3:
        score -= min(0.10, 0.015 * extra_name_tokens)
        reasons.append("variant_penalty")
    if "(" in str(record.get("name") or ""):
        score -= 0.03
        reasons.append("parenthetical_variant_penalty")

    return max(0.0, min(score, 1.0)), reasons


def load_dataset(path: Path | None, url: str, cache: Path) -> list[dict[str, Any]]:
    if path and path.exists():
        source = path
    else:
        source = cache
        if not source.exists():
            source.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(url, timeout=30) as res:
                source.write_bytes(res.read())

    with source.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise SystemExit(f"dataset must be a JSON array: {source}")
    return [r for r in data if isinstance(r, dict)]


def read_candidates(args: argparse.Namespace) -> list[str]:
    candidates = list(args.candidates or [])
    if args.candidates_file:
        text = Path(args.candidates_file).read_text(encoding="utf-8")
        if args.candidates_file.endswith(".json"):
            data = json.loads(text)
            if isinstance(data, list):
                candidates.extend(str(x) for x in data)
            else:
                raise SystemExit("--candidates-file JSON must be an array")
        else:
            candidates.extend(line.strip() for line in text.splitlines() if line.strip())
    return [c for c in candidates if c.strip()]


def match_all(
    records: list[dict[str, Any]], candidates: list[str], lang: str, top_k: int, steps: int
) -> dict[str, Any]:
    results = []
    for candidate in candidates:
        scored = []
        for record in records:
            score, reasons = score_candidate(candidate, record, lang)
            if score <= 0:
                continue
            scored.append((score, reasons, record))
        scored.sort(key=lambda x: x[0], reverse=True)
        matches = []
        for score, reasons, record in scored[:top_k]:
            matches.append(
                {
                    "id": record.get("id"),
                    "name": record.get("name"),
                    "score": round(score, 4),
                    "reasons": reasons,
                    "category": record.get("category") or record.get("body_part"),
                    "equipment": record.get("equipment"),
                    "target": record.get("target"),
                    "muscle_group": record.get("muscle_group"),
                    "secondary_muscles": record.get("secondary_muscles") or [],
                    "instruction_steps": compact_steps(record, lang, steps),
                }
            )
        results.append({"candidate": candidate, "matches": matches})
    return {"language": lang, "count": len(results), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", nargs="*", help="exercise names or short phrases")
    parser.add_argument("--candidates-file", help="newline text or JSON array of candidates")
    parser.add_argument("--dataset", type=Path, help="path to data/exercises.json")
    parser.add_argument("--dataset-url", default=DEFAULT_DATASET_URL)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--lang", choices=LANGS, default="en")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--steps", type=int, default=3, help="instruction steps per match")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    candidates = read_candidates(args)
    if not candidates:
        parser.error("provide candidates as arguments or --candidates-file")

    records = load_dataset(args.dataset, args.dataset_url, args.cache)
    output = match_all(records, candidates, args.lang, max(1, args.top_k), max(0, args.steps))
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
