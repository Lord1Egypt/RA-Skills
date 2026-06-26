#!/usr/bin/env python3
"""Analyze the reply corpus to extract persona patterns.

Queries the reply_pairs table and produces a structured report plus
configs/persona_analysis.json with real observed patterns.
"""

from __future__ import annotations

import json
import re
import sqlite3
import statistics
from collections import Counter
from pathlib import Path

from app.core.config import get_internal_domains, get_user_names
from app.core.settings import get_var_dir

ROOT_DIR = Path(__file__).resolve().parents[1]


def _build_signature_patterns() -> list[re.Pattern]:
    """Build signature patterns from config user names plus common closings."""
    patterns: list[re.Pattern] = []
    # Add user-name-based signature patterns from config
    for name in get_user_names():
        if name.strip():
            patterns.append(re.compile(rf"^{re.escape(name)}", re.MULTILINE))
    # Common signature separators and closings
    patterns.extend(
        [
            re.compile(r"^-- $", re.MULTILINE),
            re.compile(r"^--$", re.MULTILINE),
            re.compile(r"^Best,\s*$", re.MULTILINE),
            re.compile(r"^Cheers,\s*$", re.MULTILINE),
            re.compile(r"^Regards,\s*$", re.MULTILINE),
            re.compile(r"^Kind regards,\s*$", re.MULTILINE),
            re.compile(r"^Thanks,\s*$", re.MULTILINE),
            re.compile(r"^Thank you,\s*$", re.MULTILINE),
            re.compile(r"^Sent from my iPhone", re.MULTILINE),
            re.compile(r"^Sent from my iPad", re.MULTILINE),
        ]
    )
    return patterns


# Signature patterns — truncate at first match
_SIGNATURE_PATTERNS = _build_signature_patterns()


def strip_signature(text: str) -> str:
    """Strip signature from reply text."""
    earliest_pos = len(text)
    found = False
    for pattern in _SIGNATURE_PATTERNS:
        match = pattern.search(text)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()
            found = True
    if found:
        return text[:earliest_pos].rstrip()
    return text


def _extract_greeting(text: str) -> str | None:
    """Extract the greeting pattern from first line."""
    first_line = text.strip().split("\n")[0].strip()
    if not first_line:
        return None
    # Normalize
    lower = first_line.lower()
    if lower.startswith("hi ") or lower == "hi":
        return "Hi X"
    if lower.startswith("hey ") or lower == "hey":
        return "Hey X"
    if lower.startswith("hello ") or lower == "hello":
        return "Hello X"
    if lower.startswith("dear "):
        return "Dear X"
    if lower.startswith("thanks") or lower.startswith("thank you"):
        return "Thanks opener"
    if lower.startswith("sure") or lower.startswith("yes") or lower.startswith("no"):
        return "Direct answer"
    return "Direct start"


def _extract_closer(text: str) -> str | None:
    """Extract the closing pattern from last meaningful line."""
    lines = [ln.strip() for ln in text.strip().split("\n") if ln.strip()]
    if not lines:
        return None
    last = lines[-1].lower()
    if last.startswith("cheers"):
        return "Cheers"
    if last.startswith("best"):
        return "Best"
    if last.startswith("thanks"):
        return "Thanks"
    if last.startswith("regards"):
        return "Regards"
    if last.startswith("let me know"):
        return "Let me know"
    if "?" in last:
        return "Question"
    return "Statement"


def _classify_sender_type(author: str | None) -> str:
    """Sender classification using configured internal domains."""
    if not author:
        return "unknown"
    lower = author.lower()
    internal_domains = get_internal_domains()
    for domain in internal_domains:
        if f"@{domain}" in lower:
            return "internal"
    personal_domains = {"gmail.com", "yahoo.com", "hotmail.com", "icloud.com", "outlook.com"}
    for d in personal_domains:
        if f"@{d}" in lower:
            return "personal"
    return "external_client"


def analyze(db_path: Path, *, recent_days: int | None = None) -> dict:
    """Run corpus analysis and return findings.

    Args:
        recent_days: If set, weight pairs from last N days 3x in style metrics.
                     If None (--full mode), all pairs are weighted equally.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("SELECT reply_text, inbound_text, inbound_author, reply_author, metadata_json, paired_at FROM reply_pairs").fetchall()
    finally:
        conn.close()

    if not rows:
        return {"error": "No reply pairs found", "total_pairs": 0}

    # Compute recency weights
    import math
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    weights: list[float] = []
    for row in rows:
        paired_at = row["paired_at"] if "paired_at" in row.keys() else None
        weight = 1.0
        if recent_days is not None and paired_at:
            try:
                dt = datetime.fromisoformat(str(paired_at).replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                days_ago = (now - dt).days
                if days_ago <= recent_days:
                    weight = 3.0
            except (ValueError, TypeError):
                pass
        weights.append(weight)

    word_counts = []
    greeting_counter: Counter = Counter()
    closer_counter: Counter = Counter()
    signature_counter: Counter = Counter()
    tone_by_type: dict[str, list[int]] = {"internal": [], "external_client": [], "personal": [], "unknown": []}

    # New style metrics accumulators
    sentence_lengths: list[float] = []
    bullet_count = 0
    question_counts: list[int] = []
    hedge_count = 0
    emoji_count = 0
    paragraph_counts: list[int] = []

    _HEDGE_WORDS = re.compile(r"\b(perhaps|might|could|maybe|possibly|i think|i believe)\b", re.IGNORECASE)
    _BULLET_PATTERN = re.compile(r"(^- |^\* |^\d+[\.\)] )", re.MULTILINE)
    _EMOJI_PATTERN = re.compile(
        "["
        "\U0001f600-\U0001f64f"
        "\U0001f300-\U0001f5ff"
        "\U0001f680-\U0001f6ff"
        "\U0001f1e0-\U0001f1ff"
        "\U00002702-\U000027b0"
        "\U000024c2-\U0001f251"
        "\U0001f900-\U0001f9ff"
        "\U0001fa00-\U0001fa6f"
        "\U0001fa70-\U0001faff"
        "\U00002600-\U000026ff"
        "]"
    )

    for row in rows:
        reply_raw = row["reply_text"] or ""
        stripped = strip_signature(reply_raw)

        # Detect which signature was found
        for pattern in _SIGNATURE_PATTERNS:
            if pattern.search(reply_raw):
                sig_name = pattern.pattern.replace("^", "").replace("\\s*$", "").replace("$", "").strip()
                signature_counter[sig_name] += 1
                break
        else:
            signature_counter["(none)"] += 1

        words = stripped.split()
        wc = len(words)
        word_counts.append(wc)

        greeting = _extract_greeting(stripped)
        if greeting:
            greeting_counter[greeting] += 1

        closer = _extract_closer(stripped)
        if closer:
            closer_counter[closer] += 1

        sender_type = _classify_sender_type(row["inbound_author"])
        tone_by_type.setdefault(sender_type, []).append(wc)

        # Sentence length
        sentences = [s.strip() for s in re.split(r"[.!?]+", stripped) if s.strip()]
        if sentences:
            avg_sent = statistics.mean(len(s.split()) for s in sentences)
            sentence_lengths.append(avg_sent)

        # Bullet points
        if _BULLET_PATTERN.search(stripped):
            bullet_count += 1

        # Questions
        question_counts.append(stripped.count("?"))

        # Hedge words
        if _HEDGE_WORDS.search(stripped):
            hedge_count += 1

        # Emoji
        if _EMOJI_PATTERN.search(stripped):
            emoji_count += 1

        # Paragraphs (split on double newline)
        paragraphs = [p.strip() for p in stripped.split("\n\n") if p.strip()]
        paragraph_counts.append(len(paragraphs))

    # Compute stats
    word_counts_sorted = sorted(word_counts)
    _n = len(word_counts_sorted)

    def percentile(data: list[int], p: float) -> int:
        idx = int(len(data) * p)
        return data[min(idx, len(data) - 1)]

    total = len(rows)
    bullet_point_pct = round(bullet_count / total, 4) if total else 0
    hedge_word_pct = round(hedge_count / total, 4) if total else 0

    # Per-intent average word counts
    from app.core.intent import classify_intent as _classify_intent

    intent_word_buckets: dict[str, list[int]] = {}
    for row in rows:
        reply_raw = row["reply_text"] or ""
        stripped_reply = strip_signature(reply_raw)
        wc = len(stripped_reply.split())
        inbound = row["inbound_text"] if "inbound_text" in row.keys() else None
        if inbound:
            intent = _classify_intent(inbound)
        else:
            intent = "general"
        intent_word_buckets.setdefault(intent, []).append(wc)

    intent_avg_words: dict[str, int] = {}
    for intent_key, wcs in intent_word_buckets.items():
        if wcs:
            intent_avg_words[intent_key] = round(statistics.mean(wcs))

    # EWMA avg_reply_words with 60-day half-life
    ewma_avg_words = 0.0
    if word_counts:
        # Sort pairs by paired_at for temporal ordering
        paired_wc: list[tuple[str | None, int]] = []
        for row_idx, row in enumerate(rows):
            paired_at_str = row["paired_at"] if "paired_at" in row.keys() else None
            paired_wc.append((paired_at_str, word_counts[row_idx]))
        paired_wc.sort(key=lambda x: x[0] or "")

        # Compute EWMA: weight = exp(-0.693 * days_ago / 60)
        ewma_weights = []
        ewma_values = []
        for paired_at_str, wc in paired_wc:
            days_ago = 365.0  # default for unknown dates
            if paired_at_str:
                try:
                    dt = datetime.fromisoformat(str(paired_at_str).replace("Z", "+00:00"))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    days_ago = max(0, (now - dt).days)
                except (ValueError, TypeError):
                    pass
            w = math.exp(-0.693 * days_ago / 60)
            ewma_weights.append(w)
            ewma_values.append(wc)

        total_weight = sum(ewma_weights)
        if total_weight > 0:
            ewma_avg_words = round(sum(w * v for w, v in zip(ewma_weights, ewma_values, strict=True)) / total_weight, 1)
        else:
            ewma_avg_words = round(statistics.mean(word_counts), 1)
    else:
        ewma_avg_words = 0.0

    # Confidence interval stats for avg_reply_words
    avg_reply_words_p25 = percentile(word_counts_sorted, 0.25) if word_counts_sorted else 0
    avg_reply_words_p75 = percentile(word_counts_sorted, 0.75) if word_counts_sorted else 0
    avg_reply_words_stddev = round(statistics.stdev(word_counts), 1) if len(word_counts) >= 2 else 0.0

    findings = {
        "total_pairs": total,
        "reply_length": {
            "avg_words": ewma_avg_words,
            "p25": avg_reply_words_p25,
            "p50": percentile(word_counts_sorted, 0.50),
            "p75": avg_reply_words_p75,
            "p95": percentile(word_counts_sorted, 0.95),
            "min": word_counts_sorted[0] if word_counts_sorted else 0,
            "max": word_counts_sorted[-1] if word_counts_sorted else 0,
        },
        "avg_reply_words_p25": avg_reply_words_p25,
        "avg_reply_words_p75": avg_reply_words_p75,
        "avg_reply_words_stddev": avg_reply_words_stddev,
        "greeting_patterns": dict(greeting_counter.most_common(20)),
        "closing_patterns": dict(closer_counter.most_common(20)),
        "signature_patterns": dict(signature_counter.most_common(20)),
        "tone_by_sender_type": {
            k: {
                "count": len(v),
                "avg_words": round(statistics.mean(v), 1) if v else 0,
                "p50": percentile(sorted(v), 0.50) if v else 0,
            }
            for k, v in tone_by_type.items()
            if v
        },
        "sentence_length_avg": round(statistics.mean(sentence_lengths), 2) if sentence_lengths else 0,
        "bullet_point_pct": bullet_point_pct,
        "question_frequency": round(statistics.mean(question_counts), 2) if question_counts else 0,
        "hedge_word_pct": hedge_word_pct,
        "directness_score": round(1.0 - hedge_word_pct, 4),
        "emoji_pct": round(emoji_count / total, 4) if total else 0,
        "avg_paragraphs": round(statistics.mean(paragraph_counts), 2) if paragraph_counts else 0,
        "intent_avg_words": intent_avg_words,
    }

    return findings


def print_report(findings: dict) -> None:
    """Print a human-readable report."""
    print("=" * 60)
    print("YouOS Persona Corpus Analysis")
    print("=" * 60)

    if "error" in findings:
        print(f"\n{findings['error']}")
        return

    print(f"\nTotal reply pairs analyzed: {findings['total_pairs']}")

    rl = findings["reply_length"]
    print("\n--- Reply Length Distribution ---")
    print(f"  Average words: {rl['avg_words']}")
    print(f"  p25: {rl['p25']}  p50: {rl['p50']}  p75: {rl['p75']}  p95: {rl['p95']}")
    print(f"  Range: {rl['min']} - {rl['max']}")

    print("\n--- Greeting Patterns (top 20) ---")
    for pattern, count in findings["greeting_patterns"].items():
        print(f"  {pattern}: {count}")

    print("\n--- Closing Patterns (top 20) ---")
    for pattern, count in findings["closing_patterns"].items():
        print(f"  {pattern}: {count}")

    print("\n--- Signature Detection ---")
    for sig, count in findings["signature_patterns"].items():
        print(f"  {sig}: {count}")

    print("\n--- Tone by Sender Type ---")
    for stype, stats in findings["tone_by_sender_type"].items():
        print(f"  {stype}: {stats['count']} replies, avg {stats['avg_words']} words, p50 {stats['p50']}")

    print("\n" + "=" * 60)


def main() -> None:
    import argparse
    import sys

    sys.path.insert(0, str(ROOT_DIR))

    parser = argparse.ArgumentParser(description="Analyze persona patterns from corpus")
    parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing")
    parser.add_argument("--recent-days", type=int, default=None, help="Weight pairs from last N days 3x (default: 90)")
    parser.add_argument("--full", action="store_true", help="Process all pairs with equal weight")
    args = parser.parse_args()

    # Determine recent_days: --full → None (equal weight), --recent-days → value, default → 90
    recent_days: int | None = None
    if not args.full:
        recent_days = args.recent_days if args.recent_days is not None else 90

    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)

    findings = analyze(db_path, recent_days=recent_days)
    print_report(findings)

    if args.dry_run:
        print("\n[DRY RUN] Would write findings to configs/persona_analysis.json")
        # Show what persona merge would do
        from scripts.analyze_persona_merge import merge_persona_analysis

        merge_persona_analysis(
            analysis_path=None,
            persona_path=ROOT_DIR / "configs" / "persona.yaml",
            log_path=get_var_dir() / "persona_merge.log",
            dry_run=True,
            findings_dict=findings,
        )
    else:
        output_path = ROOT_DIR / "configs" / "persona_analysis.json"
        output_path.write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nFindings written to {output_path}")

        # Append drift entry
        from datetime import datetime, timezone

        drift_path = get_var_dir() / "persona_drift.jsonl"
        drift_path.parent.mkdir(parents=True, exist_ok=True)
        drift_entry = {
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "avg_reply_words": findings.get("reply_length", {}).get("avg_words", 0),
            "directness_score": findings.get("directness_score", 0),
            "bullet_point_pct": findings.get("bullet_point_pct", 0),
            "avg_paragraphs": findings.get("avg_paragraphs", 0),
        }
        with open(drift_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(drift_entry, ensure_ascii=False) + "\n")
        print(f"Drift entry appended to {drift_path}")


if __name__ == "__main__":
    main()
