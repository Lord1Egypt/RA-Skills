#!/usr/bin/env python3
"""
memory_compact.py — Memory tier compaction and lifecycle management.

Memory Tiers:
  HOT  — Actively used, high access frequency. Stored in state/memory/hot/
  WARM — Accessed within last 7 days. Stored in state/memory/warm/
  COLD — Not accessed in 7+ days. Stored in state/memory/cold/
  ARCHIVE — Compressed and moved to state/memory/archive/

Promotion/Demotion Rules:
  - HOT → WARM:  No access in 3 days
  - WARM → COLD: No access in 7 days
  - COLD → ARCHIVE: No access in 30 days
  - Any tier → HOT: Accessed within last 24h

Merge Rules:
  - Entries with >80% similarity in the same tier are merged
  - Merged entry retains the most recent timestamp

Usage:
  python3 memory_compact.py [--state-dir DIR] [--dry-run] [--tier TIER]
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_STATE_DIR = os.path.expanduser("~/self-smarter/state")
TIERS = ["hot", "warm", "cold", "archive"]

# Promotion/demotion thresholds (days)
HOT_TO_WARM_DAYS = 3
WARM_TO_COLD_DAYS = 7
COLD_TO_ARCHIVE_DAYS = 30
PROMOTE_TO_HOT_DAYS = 1

# Similarity threshold for merging (0-1)
MERGE_SIMILARITY_THRESHOLD = 0.80

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def days_since(timestamp_str: str) -> float:
    """Calculate days since a timestamp string."""
    try:
        ts = datetime.fromisoformat(timestamp_str)
        return (datetime.now() - ts).total_seconds() / 86400
    except (ValueError, TypeError):
        return float("inf")

def load_entries(tier_dir: Path) -> list:
    """Load all memory entries from a tier directory."""
    entries = []
    if not tier_dir.exists():
        return entries
    for entry_file in tier_dir.glob("*.json"):
        try:
            with open(entry_file, "r") as f:
                entry = json.load(f)
                entry["_file"] = str(entry_file)
                entries.append(entry)
        except (json.JSONDecodeError, OSError):
            continue
    return entries

def save_entry(entry: dict, target_dir: Path):
    """Save a memory entry to a tier directory."""
    target_dir.mkdir(parents=True, exist_ok=True)
    entry_id = entry.get("id", f"entry_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    target_file = target_dir / f"{entry_id}.json"
    entry_clean = {k: v for k, v in entry.items() if k != "_file"}
    entry_clean["last_compacted"] = datetime.now().isoformat()
    with open(target_file, "w") as f:
        json.dump(entry_clean, f, indent=2)

def simple_similarity(a: str, b: str) -> float:
    """Simple word-overlap similarity (Jaccard-like)."""
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)

# ---------------------------------------------------------------------------
# Compaction logic
# ---------------------------------------------------------------------------
def apply_lifecycle(state_dir: Path, dry_run: bool, logger_func) -> dict:
    """Move entries between tiers based on age rules."""
    state_memory = state_dir / "memory"
    stats = {"promoted": 0, "demoted": 0, "archived": 0, "skipped": 0}

    for i, tier in enumerate(TIERS[:-1]):  # skip archive
        tier_dir = state_memory / tier
        entries = load_entries(tier_dir)
        next_tier = TIERS[i + 1]
        next_dir = state_memory / next_tier

        # Determine threshold
        if tier == "hot":
            threshold = HOT_TO_WARM_DAYS
        elif tier == "warm":
            threshold = WARM_TO_COLD_DAYS
        else:
            threshold = COLD_TO_ARCHIVE_DAYS

        for entry in entries:
            last_access = entry.get("last_accessed", entry.get("created", ""))
            age_days = days_since(last_access)

            if age_days >= threshold:
                if not dry_run:
                    save_entry(entry, next_dir)
                    # Remove from current tier
                    entry_file = entry.pop("_file", None)
                    if entry_file and os.path.exists(entry_file):
                        os.remove(entry_file)
                stats["demoted"] += 1
                logger_func(f"  {tier} → {next_tier}: {entry.get('id', '?')} ({age_days:.1f}d old)")
            else:
                stats["skipped"] += 1

    # Check for promotions (cold/warm → hot if accessed recently)
    for tier in ["warm", "cold"]:
        tier_dir = state_memory / tier
        hot_dir = state_memory / "hot"
        entries = load_entries(tier_dir)
        for entry in entries:
            last_access = entry.get("last_accessed", "")
            if days_since(last_access) <= PROMOTE_TO_HOT_DAYS:
                if not dry_run:
                    save_entry(entry, hot_dir)
                    entry_file = entry.pop("_file", None)
                    if entry_file and os.path.exists(entry_file):
                        os.remove(entry_file)
                stats["promoted"] += 1
                logger_func(f"  {tier} → hot: {entry.get('id', '?')} (recent access)")

    return stats

def merge_similar(state_dir: Path, dry_run: bool, logger_func) -> dict:
    """Merge similar entries within the same tier."""
    state_memory = state_dir / "memory"
    stats = {"merged_pairs": 0}

    for tier in TIERS[:-1]:  # skip archive
        tier_dir = state_memory / tier
        entries = load_entries(tier_dir)
        merged = set()

        for i, entry_a in enumerate(entries):
            if i in merged:
                continue
            content_a = entry_a.get("content", entry_a.get("summary", ""))
            for j, entry_b in enumerate(entries[i + 1:], start=i + 1):
                if j in merged:
                    continue
                content_b = entry_b.get("content", entry_b.get("summary", ""))
                sim = simple_similarity(content_a, content_b)
                if sim >= MERGE_SIMILARITY_THRESHOLD:
                    # Merge: keep entry_a, absorb entry_b
                    entry_a["merged_from"] = entry_a.get("merged_from", [])
                    entry_a["merged_from"].append(entry_b.get("id", f"entry_{j}"))
                    entry_a["last_accessed"] = max(
                        entry_a.get("last_accessed", ""),
                        entry_b.get("last_accessed", "")
                    )
                    if not dry_run:
                        save_entry(entry_a, tier_dir)
                        entry_b_file = entry_b.get("_file")
                        if entry_b_file and os.path.exists(entry_b_file):
                            os.remove(entry_b_file)
                    merged.add(j)
                    stats["merged_pairs"] += 1
                    logger_func(f"  Merged in {tier}: {entry_a.get('id', '?')} ← {entry_b.get('id', '?')} (sim={sim:.2f})")

    return stats

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Memory tier compaction")
    parser.add_argument("--state-dir", type=str, default=DEFAULT_STATE_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--tier", type=str, choices=TIERS, help="Process specific tier only")
    args = parser.parse_args()

    state_dir = Path(args.state_dir)
    state_memory = state_dir / "memory"

    def log(msg):
        prefix = "[DRY-RUN] " if args.dry_run else ""
        print(f"{prefix}{msg}")

    print("\n=== Memory Compaction ===")
    print(f"State dir: {state_dir}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'LIVE'}\n")

    # Ensure tier directories exist
    for tier in TIERS:
        (state_memory / tier).mkdir(parents=True, exist_ok=True)

    # Phase 1: Lifecycle promotion/demotion
    print("Phase 1: Lifecycle transitions")
    lifecycle_stats = apply_lifecycle(state_dir, args.dry_run, log)
    print(f"  → Promoted: {lifecycle_stats['promoted']}, Demoted: {lifecycle_stats['demoted']}, "
          f"Skipped: {lifecycle_stats['skipped']}\n")

    # Phase 2: Merge similar entries
    print("Phase 2: Similarity merging")
    merge_stats = merge_similar(state_dir, args.dry_run, log)
    print(f"  → Merged pairs: {merge_stats['merged_pairs']}\n")

    # Summary
    total_entries = 0
    for tier in TIERS:
        count = len(load_entries(state_memory / tier))
        total_entries += count
        print(f"  {tier.upper():8s}: {count} entries")
    print(f"  {'TOTAL':8s}: {total_entries} entries")
    print("\n=== Compaction Complete ===\n")

if __name__ == "__main__":
    main()
