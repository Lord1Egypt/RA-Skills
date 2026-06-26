#!/usr/bin/env python3
"""
review.py — Process a card review: update FSRS state + next review date.

Usage:
    python review.py <card_file> <card_title_or_partial> <rating>

    rating: 1=Again (forgot), 2=Hard, 3=Good, 4=Easy

Example:
    python review.py ~/algo-spaced-repetition.md "Two Sum" 3
    python review.py ~/algo-spaced-repetition.md "rotate matrix" 4

The card file is updated in-place. The FSRS line and History line are modified.
"""

import re
import sys
import os
from datetime import date

# Allow running from any directory
sys.path.insert(0, os.path.dirname(__file__))
from fsrs import FSRSState, process_review

RATING_LABELS = {1: "Again", 2: "Hard", 3: "Good", 4: "Easy"}
DESIRED_RETENTION = 0.9


# ---------------------------------------------------------------------------
# Card file parsing
# ---------------------------------------------------------------------------

def parse_cards(text: str) -> list[dict]:
    """
    Parse a markdown card file into a list of card dicts.

    Each card dict has:
        title (str), start_line (int), end_line (int),
        raw_lines (list[str]), fsrs_state (FSRSState or None),
        fsrs_line_idx (int or None), history_line_idx (int or None),
        priority (str)
    """
    lines = text.splitlines(keepends=True)
    cards = []
    current = None

    for i, line in enumerate(lines):
        m = re.match(r'^#{1,4}\s+(.+)$', line.rstrip())
        if m:
            if current is not None:
                current["end_line"] = i
                current["raw_lines"] = lines[current["start_line"]:i]
                cards.append(current)
            current = {
                "title": m.group(1).strip(),
                "start_line": i,
                "end_line": None,
                "raw_lines": [],
                "fsrs_state": None,
                "fsrs_line_idx": None,      # index within raw_lines
                "history_line_idx": None,
                "priority": "P3",
            }

    if current is not None:
        current["end_line"] = len(lines)
        current["raw_lines"] = lines[current["start_line"]:len(lines)]
        cards.append(current)

    # Parse each card's metadata
    for card in cards:
        for j, line in enumerate(card["raw_lines"]):
            s = line.strip()

            # FSRS state line
            m = re.match(r'-\s+\*\*FSRS:\*\*\s+(.+)', s)
            if m:
                card["fsrs_state"] = parse_fsrs_line(m.group(1))
                card["fsrs_line_idx"] = j
                continue

            # Priority
            m = re.match(r'-\s+\*\*Priority:\*\*\s+(P[123])', s)
            if m:
                card["priority"] = m.group(1)
                continue

            # History line
            if re.match(r'-\s+\*\*History:\*\*', s):
                card["history_line_idx"] = j

    return cards, lines


def parse_fsrs_line(fsrs_str: str) -> FSRSState:
    """Parse `d=5.50 s=2.00 reps=1 lapses=0 last=2026-03-11 next=2026-03-12`."""
    state = FSRSState()
    pairs = dict(re.findall(r'(\w+)=([^\s]+)', fsrs_str))
    state.difficulty = float(pairs.get("d", 5.0))
    state.stability = float(pairs.get("s", 1.0))
    state.reps = int(pairs.get("reps", 0))
    state.lapses = int(pairs.get("lapses", 0))
    last_str = pairs.get("last") or pairs.get("last_review")
    next_str = pairs.get("next") or pairs.get("next_review")
    if last_str and last_str != "None":
        from datetime import date as _date
        state.last_review = _date.fromisoformat(last_str)
    if next_str and next_str != "None":
        from datetime import date as _date
        state.next_review = _date.fromisoformat(next_str)
    return state


def format_fsrs_line(state: FSRSState) -> str:
    """Format FSRS state as a compact inline string."""
    last = state.last_review.isoformat() if state.last_review else "None"
    nxt = state.next_review.isoformat() if state.next_review else "None"
    return (
        f"- **FSRS:** d={state.difficulty:.2f} s={state.stability:.2f} "
        f"reps={state.reps} lapses={state.lapses} "
        f"last={last} next={nxt}"
    )


# ---------------------------------------------------------------------------
# Card matching
# ---------------------------------------------------------------------------

def find_card(cards: list[dict], query: str) -> dict | None:
    """Find card by exact or case-insensitive partial title match."""
    query_lower = query.lower()
    # Exact match first
    for card in cards:
        if card["title"].lower() == query_lower:
            return card
    # Partial match
    matches = [c for c in cards if query_lower in c["title"].lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        titles = [m["title"] for m in matches]
        print(f"Ambiguous query '{query}' matches: {titles}", file=sys.stderr)
        print("Provide a more specific title.", file=sys.stderr)
        sys.exit(1)
    return None


# ---------------------------------------------------------------------------
# File update
# ---------------------------------------------------------------------------

def update_card_in_file(
    all_lines: list[str],
    card: dict,
    new_state: FSRSState,
    rating: int,
    review_date: date,
) -> str:
    """
    Return updated file content with the card's FSRS and History lines updated.
    """
    raw = card["raw_lines"]
    offset = card["start_line"]
    fsrs_indent = _detect_indent(raw)

    new_fsrs_line = fsrs_indent + format_fsrs_line(new_state) + "\n"
    rating_entry = f"{review_date.isoformat()} G={rating}({RATING_LABELS[rating]})"

    # Update or insert FSRS line
    if card["fsrs_line_idx"] is not None:
        abs_idx = offset + card["fsrs_line_idx"]
        all_lines[abs_idx] = new_fsrs_line
    else:
        # Insert FSRS line before History line (or at end of card)
        insert_at = _find_insert_position(raw, offset)
        all_lines.insert(insert_at, new_fsrs_line)
        # Adjust history index after insertion
        if card["history_line_idx"] is not None and offset + card["history_line_idx"] >= insert_at:
            card["history_line_idx"] += 1

    # Update History line
    if card["history_line_idx"] is not None:
        abs_idx = offset + card["history_line_idx"]
        hist_line = all_lines[abs_idx].rstrip("\n")
        # Append to existing history
        if hist_line.rstrip().endswith("]"):
            hist_line = hist_line.rstrip()[:-1] + f", {rating_entry}]"
        else:
            hist_line = hist_line + f", {rating_entry}"
        all_lines[abs_idx] = hist_line + "\n"

    return "".join(all_lines)


def _detect_indent(raw_lines: list[str]) -> str:
    """Detect indentation used by bullet points in the card."""
    for line in raw_lines[1:]:
        m = re.match(r'^(\s*)[-*]', line)
        if m:
            return m.group(1)
    return ""


def _find_insert_position(raw_lines: list[str], offset: int) -> int:
    """Find the best line to insert FSRS state (before History, else after heading)."""
    for j, line in enumerate(raw_lines[1:], 1):
        if re.match(r'\s*-\s+\*\*History:\*\*', line):
            return offset + j
    # Insert just before the first blank line or at end
    for j, line in enumerate(raw_lines[1:], 1):
        if line.strip() == "":
            return offset + j
    return offset + len(raw_lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    card_file = os.path.expanduser(sys.argv[1])
    query = sys.argv[2]
    try:
        rating = int(sys.argv[3])
        assert rating in (1, 2, 3, 4)
    except (ValueError, AssertionError):
        print("Rating must be 1 (Again), 2 (Hard), 3 (Good), or 4 (Easy).", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(card_file):
        print(f"File not found: {card_file}", file=sys.stderr)
        sys.exit(1)

    with open(card_file, "r") as f:
        text = f.read()

    cards, all_lines = parse_cards(text)

    card = find_card(cards, query)
    if card is None:
        print(f"Card not found: '{query}'", file=sys.stderr)
        print("Available cards:")
        for c in cards:
            print(f"  - {c['title']}")
        sys.exit(1)

    # Get current state (initialize if new card)
    old_state = card["fsrs_state"] or FSRSState()
    today = date.today()

    new_state = process_review(old_state, rating, review_date=today,
                               desired_retention=DESIRED_RETENTION)

    # Write updated file
    new_text = update_card_in_file(all_lines, card, new_state, rating, today)
    with open(card_file, "w") as f:
        f.write(new_text)

    # Summary output
    interval = (new_state.next_review - today).days
    r_label = RATING_LABELS[rating]
    print(f"[{r_label}] {card['title']}")
    print(f"  Stability: {old_state.stability:.2f} → {new_state.stability:.2f} days")
    print(f"  Difficulty: {old_state.difficulty:.2f} → {new_state.difficulty:.2f}")
    print(f"  Next review: {new_state.next_review} (in {interval} day{'s' if interval != 1 else ''})")
    if rating == 1:
        print(f"  *** LAPSE #{new_state.lapses} — card reset ***")


if __name__ == "__main__":
    main()
