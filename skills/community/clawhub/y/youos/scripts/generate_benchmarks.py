#!/usr/bin/env python3
"""Generate benchmark cases from the email corpus.

Usage:
    python3 scripts/generate_benchmarks.py           # generate 15 cases
    python3 scripts/generate_benchmarks.py --count 20
    python3 scripts/generate_benchmarks.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

FIXTURES_DIR = ROOT_DIR / "fixtures"
BENCHMARK_FILE = FIXTURES_DIR / "benchmark_cases.yaml"
CONFIG_PATH = ROOT_DIR / "youos_config.yaml"

# Common English stop words
STOP_WORDS = frozenset(
    "a an the and or but is are was were be been being have has had do does did "
    "will would shall should can could may might must not no nor so if then than "
    "that this these those it its i me my we our you your he him his she her they "
    "them their what which who whom how when where why all any each every some few "
    "many much more most other another such very too also just only still even again "
    "here there about above after before between from into through with for at by on "
    "in to of up out off over under down".split()
)


def _classify_sender_type(author: str, metadata_json: str) -> str:
    """Derive sender_type from metadata or heuristics."""
    try:
        meta = json.loads(metadata_json) if metadata_json else {}
    except (json.JSONDecodeError, TypeError):
        meta = {}

    if meta.get("sender_type"):
        return meta["sender_type"]

    if not author:
        return "unknown"

    email_match = re.search(r"[\w.+-]+@([\w.-]+)", author or "")
    if not email_match:
        return "unknown"

    domain = email_match.group(1).lower()
    personal_domains = {"gmail.com", "yahoo.com", "hotmail.com", "icloud.com", "outlook.com"}
    if domain in personal_domains:
        return "personal"
    return "external_client"


def _extract_keywords(text: str, max_keywords: int = 3) -> list[str]:
    """Extract non-stopword nouns/verbs from text."""
    words = re.findall(r"[a-zA-Z]{5,}", text)
    freq: dict[str, int] = {}
    for w in words:
        w_lower = w.lower()
        if w_lower not in STOP_WORDS:
            freq[w_lower] = freq.get(w_lower, 0) + 1

    # Sort by frequency, take top N with freq > 1 (or just top N if not enough)
    candidates = sorted(freq.items(), key=lambda x: -x[1])
    keywords = [w for w, c in candidates if c > 1][:max_keywords]
    if len(keywords) < max_keywords:
        keywords = [w for w, _ in candidates[:max_keywords]]
    return keywords


def _make_case_key(subject: str | None, inbound_text: str) -> str:
    """Generate a case_key from subject or first words of inbound."""
    source = subject or inbound_text
    words = re.findall(r"[a-zA-Z0-9]+", source)[:5]
    key = "_".join(w.lower() for w in words)
    return key[:50] if key else "case"


def generate_cases(db_path: Path, count: int = 15, sample_size: int = 30, seed: int | None = None) -> list[dict]:
    """Sample reply pairs and generate benchmark cases.

    Args:
        count: Number of benchmark cases to generate.
        sample_size: Size of random sample pool from reply_pairs.
        seed: Random seed for reproducibility. If None, uses hash of current ISO week.
    """
    import random

    if seed is None:
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        seed = hash(now.isocalendar()[:2])  # (year, week_number)

    rng = random.Random(seed)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # Stratified sampling: try to get a mix of sender types
        target = {
            "external_client": max(1, int(count * 0.53)),  # ~8 of 15
            "internal": max(1, int(count * 0.27)),  # ~4 of 15
            "personal": max(1, int(count * 0.13)),  # ~2 of 15
            "edge": 1,  # 1 edge case
        }

        all_rows = conn.execute(
            "SELECT id, inbound_text, reply_text, inbound_author, metadata_json FROM reply_pairs WHERE reply_text IS NOT NULL AND LENGTH(reply_text) > 20"
        ).fetchall()

        # Shuffle using our seeded RNG instead of SQL RANDOM()
        all_rows = list(all_rows)
        rng.shuffle(all_rows)
        # Limit to sample_size for random rotation
        if sample_size and len(all_rows) > sample_size:
            all_rows = all_rows[:sample_size]

        if not all_rows:
            return []

        # Classify all rows
        classified: dict[str, list] = {"external_client": [], "internal": [], "personal": [], "automated": [], "unknown": []}
        for row in all_rows:
            st = _classify_sender_type(row["inbound_author"], row["metadata_json"])
            classified.setdefault(st, []).append(row)

        selected: list = []

        # Sample from each category
        for cat, needed in [
            ("external_client", target["external_client"]),
            ("internal", target["internal"]),
            ("personal", target["personal"]),
        ]:
            pool = classified.get(cat, [])
            selected.extend(pool[:needed])

        # Edge case: shortest or longest inbound
        if all_rows:
            edge_row = min(all_rows, key=lambda r: len(r["inbound_text"] or ""))
            if edge_row not in selected:
                selected.append(edge_row)

        # Fill remaining with random
        used_ids = {r["id"] for r in selected}
        remaining = [r for r in all_rows if r["id"] not in used_ids]
        needed = count - len(selected)
        if needed > 0:
            selected.extend(remaining[:needed])

        # Build cases
        cases = []
        seen_keys: set[str] = set()
        for _i, row in enumerate(selected[:count]):
            inbound = (row["inbound_text"] or "")[:500]
            reply = row["reply_text"] or ""

            # Strip quoted text from inbound
            inbound_clean = re.split(r"(?i)(on\s+.{5,40}\s+wrote:|from:\s|---+\s*forwarded)", inbound)[0].strip()
            if len(inbound_clean) < 30:
                inbound_clean = inbound

            meta = {}
            try:
                meta = json.loads(row["metadata_json"]) if row["metadata_json"] else {}
            except (json.JSONDecodeError, TypeError):
                pass

            subject = meta.get("subject")
            case_key = _make_case_key(subject, inbound_clean)

            # Ensure unique keys
            base_key = case_key
            suffix = 1
            while case_key in seen_keys:
                case_key = f"{base_key}_{suffix}"
                suffix += 1
            seen_keys.add(case_key)

            sender_type = _classify_sender_type(row["inbound_author"], row["metadata_json"])
            keywords = _extract_keywords(reply, max_keywords=3)
            max_words = int(len(reply.split()) * 1.5)

            cases.append(
                {
                    "case_key": case_key,
                    "category": sender_type,
                    "prompt_text": inbound_clean,
                    "expected_properties": {
                        "should_contain_keywords": keywords,
                        "mode": "personal" if sender_type == "personal" else "work",
                        "max_words": max(20, max_words),
                    },
                }
            )

        return cases
    finally:
        conn.close()


def write_fixtures(cases: list[dict]) -> Path:
    """Write benchmark cases to fixtures/benchmark_cases.yaml."""
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    BENCHMARK_FILE.write_text(
        yaml.dump(cases, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    return BENCHMARK_FILE


def seed_to_db(cases: list[dict], db_path: Path) -> int:
    """Insert benchmark cases into the database."""
    conn = sqlite3.connect(db_path)
    try:
        inserted = 0
        for case in cases:
            expected_json = json.dumps(case["expected_properties"])
            conn.execute(
                """INSERT OR REPLACE INTO benchmark_cases
                   (case_key, category, prompt_text, expected_properties_json)
                   VALUES (?, ?, ?, ?)""",
                (case["case_key"], case["category"], case["prompt_text"], expected_json),
            )
            inserted += 1
        conn.commit()
        return inserted
    finally:
        conn.close()


def update_refresh_count(reply_pair_count: int) -> None:
    """Update last_benchmark_refresh_count in youos_config.yaml."""
    if CONFIG_PATH.exists():
        config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    else:
        config = {}
    config.setdefault("benchmarks", {})["last_refresh_count"] = reply_pair_count
    CONFIG_PATH.write_text(
        yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate benchmark cases from email corpus")
    parser.add_argument("--count", type=int, default=15, help="Number of cases to generate")
    parser.add_argument("--sample-size", type=int, default=30, help="Random sample pool size (default: 30)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    args = parser.parse_args()

    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)

    if not db_path.exists():
        print("No database found. Run 'youos setup' first.")
        sys.exit(1)

    cases = generate_cases(db_path, count=args.count, sample_size=args.sample_size)
    if not cases:
        print("Not enough reply pairs to generate benchmarks.")
        sys.exit(1)

    if args.dry_run:
        print(f"Would generate {len(cases)} benchmark cases:\n")
        for c in cases:
            kw = ", ".join(c["expected_properties"]["should_contain_keywords"])
            print(f"  {c['case_key']:30s}  [{c['category']:18s}]  keywords: {kw}")
        return

    fixture_path = write_fixtures(cases)
    print(f"Wrote {len(cases)} cases to {fixture_path}")

    inserted = seed_to_db(cases, db_path)
    print(f"Seeded {inserted} benchmark cases into database")

    # Update refresh count
    conn = sqlite3.connect(db_path)
    try:
        pair_count = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
    finally:
        conn.close()
    update_refresh_count(pair_count)

    print(f"Generated {len(cases)} benchmark cases from your corpus")


if __name__ == "__main__":
    main()
