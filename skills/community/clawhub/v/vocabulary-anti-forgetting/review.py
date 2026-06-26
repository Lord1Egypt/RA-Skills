#!/usr/bin/env python3
"""Ebbinghaus spaced-repetition vocabulary review script.

Selects words from the vocabulary bank based on the forgetting curve,
displays them as a study session, and tracks progress in a review log.
"""

import argparse
import os
import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

INTERVALS = {0: 0, 1: 1, 2: 2, 3: 4, 4: 7, 5: 15, 6: 30, 7: 60}
MAX_LEVEL = 7

SKILL_DIR = Path(__file__).parent
WORKSPACE_DIR = SKILL_DIR.parent.parent  # .../skills/vocabulary-anti-forgetting/ -> .../workspace-root/
MEMORY_DIR = Path(os.environ.get("REVIEW_MEMORY_DIR", "")) or WORKSPACE_DIR / "memory"
LOG_PATH = MEMORY_DIR / "review_log.md"
BANK_PATH = SKILL_DIR / "asset" / "vocabulary_bank.md"

INITIAL_LOG = """\
# Vocabulary Review Log

> **Total sessions:** 0
> **Last session date:** —

| id | vocabulary | level | review_count | last_reviewed | next_review_date |
|---|---|---|---|---|---|
"""


@dataclass
class Word:
    id: int
    vocabulary: str
    chinese: str


@dataclass
class ReviewEntry:
    id: int
    vocabulary: str
    level: int = 0
    review_count: int = 0
    last_reviewed: Optional[date] = None
    next_review_date: Optional[date] = None


@dataclass
class ReviewLog:
    total_sessions: int = 0
    last_session_date: str = "—"
    entries: Dict[int, ReviewEntry] = field(default_factory=dict)


def parse_vocabulary_bank() -> List[Word]:
    text = BANK_PATH.read_text(encoding="utf-8")
    words = []
    for m in re.finditer(
        r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
        text,
        re.MULTILINE,
    ):
        word_id = int(m.group(1))
        vocabulary = m.group(2).strip()
        chinese = m.group(3).strip()
        if chinese and chinese != "Chinese Translation":
            words.append(Word(id=word_id, vocabulary=vocabulary, chinese=chinese))
    return words


def parse_review_log() -> ReviewLog:
    if not LOG_PATH.exists():
        return ReviewLog()

    text = LOG_PATH.read_text(encoding="utf-8")
    log = ReviewLog()

    m = re.search(r"Total sessions:\*\*\s*(\d+)", text)
    if m:
        log.total_sessions = int(m.group(1))

    m = re.search(r"Last session date:\*\*\s*(.+)", text)
    if m:
        log.last_session_date = m.group(1).strip()

    for m in re.finditer(
        r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|",
        text,
        re.MULTILINE,
    ):
        entry = ReviewEntry(
            id=int(m.group(1)),
            vocabulary=m.group(2).strip(),
            level=int(m.group(3)),
            review_count=int(m.group(4)),
            last_reviewed=_parse_date(m.group(5)),
            next_review_date=_parse_date(m.group(6)),
        )
        log.entries[entry.id] = entry

    return log


def _parse_date(s: str) -> Optional[date]:
    s = s.strip()
    if not s or s == "—":
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def ensure_log_exists():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.write_text(INITIAL_LOG, encoding="utf-8")


def select_words(
    bank: List[Word], log: ReviewLog, count: int = 10
) -> List[Tuple[Word, Optional[ReviewEntry]]]:
    """Return up to `count` words: due reviews first, then new words."""
    today = date.today()

    due = []
    for entry in log.entries.values():
        if entry.next_review_date and entry.next_review_date <= today:
            word = next((w for w in bank if w.id == entry.id), None)
            if word:
                due.append((word, entry))
    due.sort(key=lambda x: x[1].next_review_date or today)

    reviewed_ids = set(log.entries.keys())
    new_words = [w for w in bank if w.id not in reviewed_ids]

    min_new = min(3, len(new_words), count)
    max_due = count - min_new

    selected: List[Tuple[Word, Optional[ReviewEntry]]] = []
    selected.extend(due[:max_due])

    remaining = count - len(selected)
    if remaining > 0:
        selected.extend((w, None) for w in new_words[:remaining])

    if len(selected) < count:
        extra_due = [d for d in due[max_due:] if d not in selected]
        selected.extend(extra_due[: count - len(selected)])

    return selected[:count]


def display_words(selected: List[Tuple[Word, Optional[ReviewEntry]]]):
    print("\n" + "=" * 60)
    print("  TODAY'S VOCABULARY REVIEW")
    print("=" * 60)

    id_width = 6
    en_width = max(len(w.vocabulary) for w, _ in selected)
    en_width = max(en_width, 10)

    print(f"\n  {'#':<{id_width}}  {'English':<{en_width}}  Chinese")
    print(f"  {'—' * id_width}  {'—' * en_width}  {'—' * 20}")

    for i, (word, entry) in enumerate(selected, 1):
        level_tag = "NEW" if entry is None else f"L{entry.level}"
        print(
            f"  {word.id:<{id_width}}  {word.vocabulary:<{en_width}}  {word.chinese}  [{level_tag}]"
        )

    print(f"\n  Total: {len(selected)} words")
    print("=" * 60)


def update_review_log(
    selected: List[Tuple[Word, Optional[ReviewEntry]]], log: ReviewLog
):
    today = date.today()

    new_count = 0
    review_count = 0

    for word, entry in selected:
        if entry is None:
            new_count += 1
            entry = ReviewEntry(id=word.id, vocabulary=word.vocabulary)
            log.entries[word.id] = entry
        else:
            review_count += 1

        entry.level = min(entry.level + 1, MAX_LEVEL)
        entry.review_count += 1
        entry.last_reviewed = today
        interval = INTERVALS.get(entry.level, 60)
        entry.next_review_date = today + timedelta(days=interval)

    log.total_sessions += 1
    log.last_session_date = today.isoformat()

    write_review_log(log)

    due_tomorrow = sum(
        1
        for e in log.entries.values()
        if e.next_review_date and e.next_review_date <= today + timedelta(days=1)
    )
    due_week = sum(
        1
        for e in log.entries.values()
        if e.next_review_date and e.next_review_date <= today + timedelta(days=7)
    )

    print(f"\n  Session #{log.total_sessions} complete!")
    print(f"  New words studied: {new_count}")
    print(f"  Review words studied: {review_count}")
    print(f"  Due tomorrow: {due_tomorrow}")
    print(f"  Due this week: {due_week}")
    print()


def write_review_log(log: ReviewLog):
    lines = [
        "# Vocabulary Review Log\n",
        "\n",
        f"> **Total sessions:** {log.total_sessions}\n",
        f"> **Last session date:** {log.last_session_date}\n",
        "\n",
        "| id | vocabulary | level | review_count | last_reviewed | next_review_date |\n",
        "|---|---|---|---|---|---|\n",
    ]
    for entry in sorted(log.entries.values(), key=lambda e: e.id):
        last = entry.last_reviewed.isoformat() if entry.last_reviewed else "—"
        nxt = entry.next_review_date.isoformat() if entry.next_review_date else "—"
        lines.append(
            f"| {entry.id} | {entry.vocabulary} | {entry.level} "
            f"| {entry.review_count} | {last} | {nxt} |\n"
        )
    LOG_PATH.write_text("".join(lines), encoding="utf-8")


def show_stats(bank: List[Word], log: ReviewLog):
    today = date.today()
    total_bank = len(bank)
    total_reviewed = len(log.entries)
    never_seen = total_bank - total_reviewed

    mastered = sum(1 for e in log.entries.values() if e.level >= 6)
    reviewing = sum(1 for e in log.entries.values() if 3 <= e.level < 6)
    learning = sum(1 for e in log.entries.values() if 1 <= e.level < 3)

    due_today = sum(
        1
        for e in log.entries.values()
        if e.next_review_date and e.next_review_date <= today
    )
    due_tomorrow = sum(
        1
        for e in log.entries.values()
        if e.next_review_date and e.next_review_date == today + timedelta(days=1)
    )

    print("\n" + "=" * 40)
    print("  VOCABULARY STATS")
    print("=" * 40)
    print(f"  Total in bank:     {total_bank}")
    print(f"  Never seen:        {never_seen}")
    print(f"  Total sessions:    {log.total_sessions}")
    print()
    print(f"  Learning (L1-L2):  {learning}")
    print(f"  Reviewing (L3-L5): {reviewing}")
    print(f"  Mastered (L6-L7):  {mastered}")
    print()
    print(f"  Due today:         {due_today}")
    print(f"  Due tomorrow:      {due_tomorrow}")
    print("=" * 40 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Ebbinghaus spaced-repetition vocabulary review"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of words per session (default: 10)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show review statistics and exit",
    )
    args = parser.parse_args()

    ensure_log_exists()
    bank = parse_vocabulary_bank()
    log = parse_review_log()

    if args.stats:
        show_stats(bank, log)
        return

    selected = select_words(bank, log, count=args.count)

    if not selected:
        print("\nNo words to review! All words mastered and none are due.")
        print("Run with --stats to see your progress.\n")
        return

    display_words(selected)
    update_review_log(selected, log)


if __name__ == "__main__":
    main()
