"""Build sender profiles from reply_pairs corpus."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path

from app.core.sender import _PERSONAL_DOMAINS, classify_sender, extract_domain
from app.core.settings import get_settings
from app.db.bootstrap import resolve_sqlite_path

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.\w+")
_STOPWORDS = frozenset(
    {
        "re",
        "fw",
        "fwd",
        "the",
        "and",
        "for",
        "you",
        "your",
        "our",
        "are",
        "was",
        "were",
        "will",
        "can",
        "has",
        "have",
        "had",
        "not",
        "but",
        "this",
        "that",
        "with",
        "from",
        "about",
        "just",
        "new",
        "all",
        "get",
        "got",
        "one",
        "two",
        "also",
        "been",
        "more",
        "some",
        "any",
        "out",
        "its",
        "let",
        "may",
        "how",
        "who",
        "what",
        "when",
        "where",
        "which",
        "would",
        "could",
        "should",
        "into",
        "than",
        "then",
        "them",
        "they",
        "their",
        "there",
        "here",
        "very",
        "much",
        "many",
        "each",
        "other",
        "only",
        "over",
        "such",
        "like",
        "well",
        "back",
        "even",
        "still",
        "after",
        "before",
        "between",
        "make",
        "made",
        "take",
        "need",
        "want",
        "know",
        "think",
        "see",
        "use",
        "way",
        "time",
        "please",
        "thanks",
        "thank",
        "dear",
        "hello",
        "hi",
    }
)
_WORD_RE = re.compile(r"[a-z]{3,}")


def extract_email(author: str) -> str | None:
    """Extract email from author string."""
    m = _EMAIL_RE.search(author or "")
    return m.group().lower() if m else None


def extract_display_name(author: str) -> str | None:
    """Extract display name from 'Display Name <email>' format."""
    if "<" in (author or ""):
        name = author.split("<")[0].strip().strip('"').strip("'")
        return name if name else None
    return None


def company_from_domain(domain: str | None) -> str | None:
    """Infer company name from domain."""
    if not domain or domain in _PERSONAL_DOMAINS:
        return None
    parts = domain.split(".")
    if len(parts) >= 2:
        name = parts[-2]
        return name.replace("-", " ").replace("_", " ").title()
    return None


def extract_topics(subjects: list[str], top_n: int = 3) -> list[str]:
    """Extract top N topic keywords from subject lines."""
    counter: Counter[str] = Counter()
    for subj in subjects:
        cleaned = re.sub(r"^(re|fw|fwd)\s*:\s*", "", subj.lower(), flags=re.IGNORECASE)
        words = _WORD_RE.findall(cleaned)
        for w in words:
            if w not in _STOPWORDS:
                counter[w] += 1
    return [w for w, _ in counter.most_common(top_n)]


def _compute_avg_response_hours(timestamps: list[str]) -> float | None:
    """Compute median hours between consecutive paired_at timestamps.

    Returns None if fewer than 3 data points.
    """
    if len(timestamps) < 3:
        return None

    parsed: list[datetime] = []
    for ts in timestamps:
        if not ts:
            continue
        try:
            normalized = ts.strip()
            if normalized.endswith("Z"):
                normalized = normalized[:-1] + "+00:00"
            parsed.append(datetime.fromisoformat(normalized))
        except (ValueError, TypeError):
            continue

    if len(parsed) < 3:
        return None

    parsed.sort()
    intervals = []
    for i in range(1, len(parsed)):
        delta = (parsed[i] - parsed[i - 1]).total_seconds() / 3600.0
        if delta > 0:
            intervals.append(delta)

    if not intervals:
        return None

    return round(statistics.median(intervals), 1)


def build_profiles(
    db_path: Path,
    *,
    limit: int | None = None,
    dry_run: bool = False,
    sender_email: str | None = None,
) -> tuple[int, int]:
    """Build sender profiles from reply_pairs. Returns (new_count, updated_count)."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # Get unique inbound authors
        if sender_email:
            rows = conn.execute(
                "SELECT DISTINCT inbound_author FROM reply_pairs WHERE inbound_author IS NOT NULL AND inbound_author LIKE ?",
                (f"%{sender_email}%",),
            ).fetchall()
        else:
            rows = conn.execute("SELECT DISTINCT inbound_author FROM reply_pairs WHERE inbound_author IS NOT NULL").fetchall()
        authors = [r["inbound_author"] for r in rows]
        if limit:
            authors = authors[:limit]

        new_count = 0
        updated_count = 0

        for author in authors:
            email = extract_email(author)
            if not email:
                continue

            # Gather stats for this sender
            pairs = conn.execute(
                "SELECT reply_text, paired_at FROM reply_pairs WHERE inbound_author = ?",
                (author,),
            ).fetchall()

            reply_count = len(pairs)
            word_counts = [len((r["reply_text"] or "").split()) for r in pairs]
            avg_reply_words = round(sum(word_counts) / len(word_counts), 1) if word_counts else None

            timestamps = [r["paired_at"] for r in pairs if r["paired_at"]]
            first_seen = min(timestamps) if timestamps else None
            last_seen = max(timestamps) if timestamps else None
            avg_response_hours = _compute_avg_response_hours(timestamps)

            # Get subjects for topic extraction
            subject_rows = conn.execute(
                "SELECT d.title FROM reply_pairs rp LEFT JOIN documents d ON d.id = rp.document_id WHERE rp.inbound_author = ? AND d.title IS NOT NULL",
                (author,),
            ).fetchall()
            subjects = [r["title"] for r in subject_rows if r["title"]]
            topics = extract_topics(subjects)

            display_name = extract_display_name(author)
            domain = extract_domain(author)
            company = company_from_domain(domain)
            sender_type = classify_sender(author)

            if dry_run:
                print(f"  Would upsert: {email} ({display_name or 'no name'}) — {sender_type}, {reply_count} replies")
                new_count += 1
                continue

            # Upsert
            existing = conn.execute("SELECT id FROM sender_profiles WHERE email = ?", (email,)).fetchone()

            if existing:
                conn.execute(
                    """UPDATE sender_profiles SET
                        display_name = ?, domain = ?, company = ?, sender_type = ?,
                        reply_count = ?, avg_reply_words = ?, avg_response_hours = ?,
                        first_seen = ?, last_seen = ?,
                        topics_json = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE email = ?""",
                    (
                        display_name,
                        domain,
                        company,
                        sender_type,
                        reply_count,
                        avg_reply_words,
                        avg_response_hours,
                        first_seen,
                        last_seen,
                        json.dumps(topics),
                        email,
                    ),
                )
                updated_count += 1
            else:
                conn.execute(
                    """INSERT INTO sender_profiles
                        (email, display_name, domain, company, sender_type,
                         reply_count, avg_reply_words, avg_response_hours, first_seen, last_seen, topics_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        email,
                        display_name,
                        domain,
                        company,
                        sender_type,
                        reply_count,
                        avg_reply_words,
                        avg_response_hours,
                        first_seen,
                        last_seen,
                        json.dumps(topics),
                    ),
                )
                new_count += 1

        if not dry_run:
            conn.commit()

        return new_count, updated_count
    finally:
        conn.close()


def annotate_intents(db_path: Path) -> int:
    """Annotate reply_pairs with predicted_intent in metadata_json.

    Only annotates pairs that don't already have predicted_intent set.
    Returns number of pairs annotated.
    """
    from app.core.intent import classify_intent

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("SELECT id, inbound_text, metadata_json FROM reply_pairs WHERE inbound_text IS NOT NULL").fetchall()
        count = 0
        for row in rows:
            meta = json.loads(row["metadata_json"]) if row["metadata_json"] else {}
            if meta.get("predicted_intent"):
                continue
            intent = classify_intent(row["inbound_text"] or "")
            meta["predicted_intent"] = intent
            conn.execute(
                "UPDATE reply_pairs SET metadata_json = ? WHERE id = ?",
                (json.dumps(meta), row["id"]),
            )
            count += 1
        conn.commit()
        return count
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build sender profiles from reply_pairs corpus.")
    parser.add_argument("--limit", type=int, default=None, help="Only process N senders.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created.")
    parser.add_argument("--db-path", type=Path, default=None, help="SQLite database path override.")
    args = parser.parse_args()

    settings = get_settings()
    db_path = args.db_path or resolve_sqlite_path(settings.database_url)

    new_count, updated_count = build_profiles(db_path, limit=args.limit, dry_run=args.dry_run)
    total = new_count + updated_count
    if args.dry_run:
        print(f"Dry run: would build {total} sender profiles")
    else:
        print(f"Built {total} sender profiles ({new_count} new, {updated_count} updated)")

    # Annotate reply_pairs with predicted_intent
    if not args.dry_run:
        annotated = annotate_intents(db_path)
        if annotated:
            print(f"Annotated {annotated} reply pairs with predicted_intent")


if __name__ == "__main__":
    main()
