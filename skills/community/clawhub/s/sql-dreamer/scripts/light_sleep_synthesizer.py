"""
scripts/light_sleep_synthesizer.py — SQL-native light sleep synthesizer

Generates DreamLight entries directly in SQL (no .md file dependency).

What it does:
1. Reads short-term-recall.json and phase-signals.json from memory/.dreams/
2. Loads config from config/config.yml (walks up to find it)
3. Filters entries: within lookback_days, skip pure stopword snippets
4. Scores each entry using OpenClaw's formula:
   - avgScore = totalScore / max(1, recallCount)
   - recallStrength = min(1, log1p(recallCount) / log1p(6))
   - consolidation = min(1, len(recallDays) / 3)
   - conceptual = 0.5 if len(conceptTags) > 0 else 0.0
   - confidence = avgScore*0.45 + recallStrength*0.25 + consolidation*0.20 + conceptual*0.10
5. Takes top N candidates (configurable, default 50)
6. Writes to dreams.DreamLight table (idempotent — clears existing for cycle_date)
7. ALSO writes memory/dreaming/light/YYYY-MM-DD.md for backward compat
8. Supports --dry-run, --date YYYY-MM-DD, --config flags

Usage:
    python scripts/light_sleep_synthesizer.py
    python scripts/light_sleep_synthesizer.py --dry-run
    python scripts/light_sleep_synthesizer.py --date 2026-04-25
    python scripts/light_sleep_synthesizer.py --config /path/to/config.yml
"""

import sys
import os
import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from math import log1p
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from src.sql_connector import SQLDreamerConnector

# Common stopword-only patterns (very short, mostly common words)
STOPWORD_ONLY_PATTERNS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "is", "are", "was", "were", "be", "been", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might",
    "must", "can", "shall", "with", "from", "by", "as", "about", "into",
    "through", "during", "before", "after", "above", "below", "up", "down",
    "out", "off", "over", "under", "so", "just", "only", "more", "most",
    "no", "not", "yes", "ok", "okay", "thanks", "please", "hi", "hello"
}


def find_config(start_path: str = ".") -> str:
    """
    Walk up directory tree to find config/config.yml.
    Start from start_path and work toward root.
    """
    current = Path(start_path).resolve()
    while current != current.parent:
        config_file = current / "config" / "config.yml"
        if config_file.exists():
            return str(config_file)
        current = current.parent
    
    raise FileNotFoundError("config/config.yml not found walking up from current directory")


def load_config(config_path: str) -> dict:
    """Load YAML config file."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def is_stopword_only(text: str) -> bool:
    """Check if text is only stopwords (after lowercasing and splitting)."""
    if not text or len(text) < 3:
        return True
    
    words = text.lower().split()
    return all(w in STOPWORD_ONLY_PATTERNS for w in words)


def score_entry(entry: dict) -> float:
    """
    Calculate confidence score for a recall entry using OpenClaw formula.
    
    Formula (from OpenClaw dreamer):
        avgScore = totalScore / max(1, recallCount)
        recallStrength = min(1, log1p(recallCount) / log1p(6))
        consolidation = min(1, len(recallDays) / 3)
        conceptual = 0.5 if len(conceptTags) > 0 else 0.0
        confidence = avgScore*0.45 + recallStrength*0.25 + consolidation*0.20 + conceptual*0.10
    """
    recall_count = entry.get("recallCount", 0)
    total_score = entry.get("totalScore", 0.0)
    recall_days = entry.get("recallDays", [])
    concept_tags = entry.get("conceptTags", [])
    
    # avgScore
    avg_score = total_score / max(1, recall_count)
    
    # recallStrength
    recall_strength = min(1.0, log1p(recall_count) / log1p(6))
    
    # consolidation
    consolidation = min(1.0, len(recall_days) / 3.0)
    
    # conceptual
    conceptual = 0.5 if len(concept_tags) > 0 else 0.0
    
    # confidence (weighted sum)
    confidence = (
        avg_score * 0.45 +
        recall_strength * 0.25 +
        consolidation * 0.20 +
        conceptual * 0.10
    )
    
    return confidence


def load_short_term_recall(json_path: str, lookback_days: int) -> list[dict]:
    """
    Load short-term-recall.json and filter by lookback_days.
    Skip pure stopword snippets.
    """
    with open(json_path) as f:
        data = json.load(f)
    
    entries_dict = data.get("entries", {})
    entries_list = []
    
    cutoff_date = datetime.now(timezone.utc).date() - timedelta(days=lookback_days)
    
    for key, entry in entries_dict.items():
        # Skip if no snippet or pure stopwords
        snippet = entry.get("snippet", "").strip()
        if not snippet or is_stopword_only(snippet):
            continue
        
        # Filter by recallDays
        recall_days = entry.get("recallDays", [])
        if not recall_days:
            continue
        
        # Check if any recall date is within lookback window
        found_recent = False
        for day_str in recall_days:
            try:
                day = datetime.fromisoformat(day_str).date()
                if day >= cutoff_date:
                    found_recent = True
                    break
            except (ValueError, TypeError):
                continue
        
        if not found_recent:
            continue
        
        # Add to candidates with score
        entry_copy = dict(entry)
        entry_copy["score"] = score_entry(entry)
        entries_list.append(entry_copy)
    
    return entries_list


def build_markdown_content(entries: list[dict], cycle_date: str) -> str:
    """
    Format entries as memory/dreaming/light/YYYY-MM-DD.md
    Same format as native dreamer for backward compat.
    """
    lines = [
        "# Light Sleep",
        "",
    ]
    
    for entry in entries:
        snippet = entry.get("snippet", "")[:2000]
        confidence = entry.get("score", 0.0)
        key = entry.get("key", "")
        recall_count = entry.get("recallCount", 0)
        
        lines.append(f"- Candidate: {snippet}")
        lines.append(f"  - confidence: {confidence:.2f}")
        lines.append(f"  - evidence: {key}")
        lines.append(f"  - recalls: {recall_count}")
        lines.append(f"  - status: staged")
        lines.append("")
    
    return "\n".join(lines)


def run(
    config_path: str,
    cycle_date: Optional[str] = None,
    dry_run: bool = False,
) -> None:
    """
    Main entry point.
    
    Args:
        config_path: Path to config/config.yml
        cycle_date: ISO date string (YYYY-MM-DD), default today
        dry_run: Preview without writing
    """
    cfg = load_config(config_path)
    
    if cycle_date is None:
        cycle_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    workspace_dir = cfg["dreaming"]["workspace_dir"]
    lookback_days = cfg["corpus"]["lookback_days"]
    
    # Default top N candidates (add to config if needed)
    top_n = cfg.get("light_sleep", {}).get("top_candidates", 50)
    
    # Paths
    short_term_recall_path = Path(workspace_dir) / "memory" / ".dreams" / "short-term-recall.json"
    output_dir = Path(workspace_dir) / "memory" / "dreaming" / "light"
    output_file = output_dir / f"{cycle_date}.md"
    
    print(f"light_sleep_synthesizer: {cycle_date}")
    print(f"  Config: {config_path}")
    print(f"  Lookback: {lookback_days} days")
    print(f"  Top candidates: {top_n}")
    print(f"  Source: {short_term_recall_path}")
    print(f"  Output MD: {output_file}")
    
    # Check if source exists
    if not short_term_recall_path.exists():
        print(f"  ⚠️  Source file not found: {short_term_recall_path}")
        return
    
    # Load and filter entries
    print("  Loading short-term-recall.json...")
    entries = load_short_term_recall(str(short_term_recall_path), lookback_days)
    print(f"  Entries loaded: {len(entries)}")
    
    # Sort by score descending, take top N
    entries.sort(key=lambda e: e.get("score", 0.0), reverse=True)
    entries = entries[:top_n]
    print(f"  Top candidates after filtering: {len(entries)}")
    
    if not entries:
        print("  ⚠️  No entries passed filters — skipping write")
        return
    
    # Build markdown for backward compat
    md_content = build_markdown_content(entries, cycle_date)
    
    if dry_run:
        print("\n--- DRY RUN: would write ---")
        print(f"MD file ({len(md_content)} chars):")
        print(md_content[:1500])
        if len(md_content) > 1500:
            print(f"... [{len(md_content) - 1500} more chars]")
        
        print(f"\nSQL writes:")
        for i, entry in enumerate(entries[:3]):
            print(f"  [{i+1}] key={entry.get('key', '?')[:50]}")
            print(f"       confidence={entry.get('score', 0):.2f}")
        if len(entries) > 3:
            print(f"  ... and {len(entries) - 3} more")
        
        return
    
    # Write markdown
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  ✅ Wrote {len(md_content)} chars to {output_file}")
    
    # Write to SQL
    try:
        with SQLDreamerConnector.from_config(config_path) as conn:
            # Clear existing entries for this cycle_date
            conn.execute("DELETE FROM dreams.DreamLight WHERE cycle_date = ?", (cycle_date,))
            print(f"  ✅ Cleared existing DreamLight entries for {cycle_date}")
            
            # Prepare SQL rows
            sql = """
                INSERT INTO dreams.DreamLight
                    (cycle_date, entry_key, snippet, confidence, evidence_path,
                     recall_count, status, ingested_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            from datetime import datetime as dt
            now = dt.now(timezone.utc)
            
            rows = [
                (
                    cycle_date,
                    e.get("key", ""),
                    e.get("snippet", "")[:2000],
                    e.get("score", 0.0),
                    e.get("key", ""),  # evidence_path = key
                    e.get("recallCount", 0),
                    "staged",
                    now,
                )
                for e in entries
            ]
            
            conn.executemany(sql, rows)
            print(f"  ✅ Wrote {len(rows)} entries to dreams.DreamLight")
    except Exception as e:
        print(f"  ❌ SQL error: {e}")
        print("  (MD file was still written for backward compat)")


def main():
    parser = argparse.ArgumentParser(
        description="SQL-native light sleep synthesizer"
    )
    parser.add_argument(
        "--config",
        help="Path to config.yml (default: walks up to find config/config.yml)"
    )
    parser.add_argument(
        "--date",
        help="Cycle date in YYYY-MM-DD format (default: today)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without writing"
    )
    
    args = parser.parse_args()
    
    # Find config if not provided
    config_path = args.config
    if not config_path:
        try:
            config_path = find_config()
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    run(config_path, cycle_date=args.date, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
