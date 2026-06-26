#!/usr/bin/env python3
"""
due_cards.py — List flashcards due for review today or overdue.

Usage:
    python due_cards.py <card_file> [--all] [--date YYYY-MM-DD]

    --all          Show all cards (including future) with their next review dates.
    --date         Override today's date (for testing or planning ahead).

Example:
    python due_cards.py ~/algo-spaced-repetition.md
    python due_cards.py ~/algo-spaced-repetition.md --all
    python due_cards.py ~/algo-spaced-repetition.md --date 2026-03-20

Output:
    Cards sorted by priority (P1 → P2 → P3), then by overdue-ness (most overdue first).
    New cards (no FSRS state) always appear first within their priority group.
"""

import os
import re
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from fsrs import FSRSState, retrievability
from review import parse_cards


PRIORITY_ORDER = {"P1": 0, "P2": 1, "P3": 2}


_CARD_FIELDS = re.compile(
    r'\*\*(Prompt|Answer|Priority|FSRS|History|Added|Interrogate|When to reach):\*\*',
    re.IGNORECASE
)


def _is_flashcard(card: dict) -> bool:
    """Return True if the section looks like an actual flashcard (not a header section)."""
    text = "".join(card["raw_lines"])
    return bool(_CARD_FIELDS.search(text))


def load_cards(card_file: str) -> list[dict]:
    with open(card_file, "r") as f:
        text = f.read()
    cards, _ = parse_cards(text)
    return [c for c in cards if _is_flashcard(c)]


def days_overdue(card: dict, today: date) -> int:
    """How many days overdue is this card? Negative = not yet due."""
    state = card["fsrs_state"]
    if state is None or state.next_review is None:
        return 999  # New cards are maximally "overdue" (always show first)
    return (today - state.next_review).days


def format_card_row(card: dict, today: date) -> str:
    """Format a single card row for display."""
    state = card["fsrs_state"]
    prio = card["priority"]
    title = card["title"]

    if state is None or state.next_review is None:
        return f"  [{prio}] {title}  (NEW — not yet initialized)"

    overdue = days_overdue(card, today)

    if overdue >= 0:
        days_label = f"overdue {overdue}d" if overdue > 0 else "due today"
    else:
        days_label = f"due in {-overdue}d"

    r = retrievability(state.stability, max(0, (today - state.last_review).days)) if state.last_review else None
    r_str = f"R={r:.0%}" if r is not None else "R=?"
    s_str = f"S={state.stability:.1f}d"
    d_str = f"D={state.difficulty:.1f}"

    return f"  [{prio}] {title}  ({days_label} | {r_str} {s_str} {d_str})"


def main():
    # --- Argument parsing (manual, no argparse dep) ---
    args = sys.argv[1:]
    show_all = "--all" in args
    date_override = None

    args_clean = []
    i = 0
    while i < len(args):
        if args[i] == "--all":
            i += 1
        elif args[i] == "--date" and i + 1 < len(args):
            date_override = date.fromisoformat(args[i + 1])
            i += 2
        else:
            args_clean.append(args[i])
            i += 1

    if not args_clean:
        print(__doc__)
        sys.exit(1)

    card_file = os.path.expanduser(args_clean[0])
    if not os.path.exists(card_file):
        print(f"File not found: {card_file}", file=sys.stderr)
        sys.exit(1)

    today = date_override or date.today()
    cards = load_cards(card_file)

    # --- Separate due vs future ---
    due_cards = []
    future_cards = []
    new_cards = []

    for card in cards:
        state = card["fsrs_state"]
        if state is None or state.next_review is None:
            new_cards.append(card)
        elif state.next_review <= today:
            due_cards.append(card)
        else:
            future_cards.append(card)

    # Sort by priority then overdue-ness
    sort_key = lambda c: (PRIORITY_ORDER.get(c["priority"], 9), -days_overdue(c, today))
    due_cards.sort(key=sort_key)
    new_cards.sort(key=lambda c: PRIORITY_ORDER.get(c["priority"], 9))

    # --- Output ---
    print(f"Date: {today}  |  Card file: {os.path.basename(card_file)}")
    print()

    total_due = len(due_cards) + len(new_cards)
    if total_due == 0 and not show_all:
        print("No cards due today.")
        if future_cards:
            next_date = min(c["fsrs_state"].next_review for c in future_cards)
            days_until = (next_date - today).days
            print(f"Next review: {next_date} (in {days_until} day{'s' if days_until != 1 else ''})")
        return

    if new_cards:
        print(f"=== NEW ({len(new_cards)}) ===")
        for card in new_cards:
            print(format_card_row(card, today))
        print()

    if due_cards:
        print(f"=== DUE ({len(due_cards)}) ===")
        for card in due_cards:
            print(format_card_row(card, today))
        print()

    if show_all and future_cards:
        future_cards.sort(key=lambda c: (
            c["fsrs_state"].next_review,
            PRIORITY_ORDER.get(c["priority"], 9)
        ))
        print(f"=== UPCOMING ({len(future_cards)}) ===")
        for card in future_cards:
            print(format_card_row(card, today))
        print()

    # Summary stats
    print(f"Total due: {total_due}  |  Total cards: {len(cards)}")
    if due_cards:
        lapses = sum(c["fsrs_state"].lapses for c in due_cards if c["fsrs_state"])
        avg_stability = sum(
            c["fsrs_state"].stability for c in due_cards if c["fsrs_state"]
        ) / len(due_cards)
        print(f"Avg stability (due): {avg_stability:.1f}d  |  Total lapses in queue: {lapses}")


if __name__ == "__main__":
    main()
