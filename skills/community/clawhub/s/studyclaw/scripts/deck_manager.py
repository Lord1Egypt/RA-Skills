#!/usr/bin/env python3
"""
Study Buddy - Deck Manager
Manages flashcard decks with spaced repetition (SM-2 algorithm).

License: MIT

Usage:
    deck_manager.py create <deck_name> --cards '<json_array>'
    deck_manager.py add <deck_name> --cards '<json_array>'
    deck_manager.py list
    deck_manager.py stats <deck_name>
    deck_manager.py review <deck_name>
    deck_manager.py quiz <deck_name> [--count N]
    deck_manager.py exam <deck_name> [--questions N] [--types types]
    deck_manager.py record <deck_name> --card-id <id> --result <correct|partial|missed>
    deck_manager.py due
    deck_manager.py export <deck_name>
    deck_manager.py import <file_path>
    deck_manager.py delete <deck_name>
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

__all__ = [
    "DECKS_DIR",
    "ensure_dir",
    "deck_path",
    "load_deck",
    "save_deck",
    "new_card",
    "sm2_update",
    "cmd_create",
    "cmd_add",
    "cmd_list",
    "cmd_stats",
    "cmd_review",
    "cmd_quiz",
    "cmd_exam",
    "cmd_record",
    "cmd_due",
    "cmd_export",
    "cmd_import",
    "cmd_delete",
    "main",
]

# --- Named constants ---
MASTERY_THRESHOLD = 5          # Repetitions needed to consider a card mastered
DEFAULT_EASE = 2.5             # Starting ease factor for new cards
MIN_EASE = 1.3                 # Minimum ease factor (SM-2 floor)
EASE_BONUS_CORRECT = 0.1      # Ease increase on correct answer
EASE_PENALTY_PARTIAL = -0.15   # Ease decrease on partial answer
EASE_PENALTY_MISSED = -0.2    # Ease decrease on missed answer
DEFAULT_QUIZ_COUNT = 10        # Default number of quiz questions
DEFAULT_EXAM_QUESTIONS = 20    # Default number of exam questions

DECKS_DIR = Path.home() / ".openclaw" / "study-buddy" / "decks"


def ensure_dir() -> None:
    """Create the decks directory if it does not exist."""
    DECKS_DIR.mkdir(parents=True, exist_ok=True)


def deck_path(name: str) -> Path:
    """Return the filesystem path for a deck given its name."""
    safe = name.lower().replace(" ", "_").replace("/", "_")
    return DECKS_DIR / f"{safe}.json"


def load_deck(name: str) -> dict:
    """Load a deck from disk by name, exiting if not found."""
    path = deck_path(name)
    if not path.exists():
        logger.error("Deck '%s' not found.", name)
        print(f"Error: Deck '{name}' not found.", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def save_deck(deck: dict) -> None:
    """Persist a deck dictionary to its JSON file on disk."""
    ensure_dir()
    path = deck_path(deck["name"])
    with open(path, "w") as f:
        json.dump(deck, f, indent=2, ensure_ascii=False)


def new_card(card_id: int, question: str, answer: str) -> dict:
    """Create a new flashcard with default SM-2 scheduling values."""
    return {
        "id": card_id,
        "q": question,
        "a": answer,
        "interval": 0,
        "ease": DEFAULT_EASE,
        "repetitions": 0,
        "next_review": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
    }


def sm2_update(card: dict, result: str) -> dict:
    """Apply the SM-2 spaced repetition algorithm to update a card's scheduling."""
    ease = card.get("ease", DEFAULT_EASE)
    interval = card.get("interval", 0)
    reps = card.get("repetitions", 0)

    if result == "correct":
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 3
        else:
            interval = int(interval * ease)
        reps += 1
        ease = max(MIN_EASE, ease + EASE_BONUS_CORRECT)
    elif result == "partial":
        ease = max(MIN_EASE, ease + EASE_PENALTY_PARTIAL)
    elif result == "missed":
        reps = 0
        interval = 1
        ease = max(MIN_EASE, ease + EASE_PENALTY_MISSED)

    card["interval"] = interval
    card["ease"] = round(ease, 2)
    card["repetitions"] = reps
    card["next_review"] = (datetime.now() + timedelta(days=max(interval, 1))).isoformat()
    return card


def _validate_cards_json(cards_json: str) -> list[dict]:
    """Parse and validate a JSON string of cards, ensuring each has 'q' and 'a' keys."""
    try:
        cards_data = json.loads(cards_json)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON for cards: %s", exc)
        print(f"Error: Invalid JSON for cards: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(cards_data, list):
        logger.error("Cards must be a JSON array.")
        print("Error: Cards must be a JSON array.", file=sys.stderr)
        sys.exit(1)

    for i, card in enumerate(cards_data):
        if "q" not in card or "a" not in card:
            logger.error("Card at index %d is missing required 'q' and/or 'a' keys.", i)
            print(
                f"Error: Card at index {i} is missing required 'q' and/or 'a' keys.",
                file=sys.stderr,
            )
            sys.exit(1)

    return cards_data


def cmd_create(args: argparse.Namespace) -> None:
    """Create a new flashcard deck from a JSON array of cards."""
    ensure_dir()
    path = deck_path(args.deck_name)
    if path.exists():
        logger.error("Deck '%s' already exists. Use 'add' to add cards.", args.deck_name)
        print(f"Error: Deck '{args.deck_name}' already exists. Use 'add' to add cards.", file=sys.stderr)
        sys.exit(1)

    cards_data = _validate_cards_json(args.cards)
    cards = [new_card(i + 1, c["q"], c["a"]) for i, c in enumerate(cards_data)]

    deck = {
        "name": args.deck_name,
        "cards": cards,
        "next_id": len(cards) + 1,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    save_deck(deck)
    print(json.dumps({"status": "created", "deck": args.deck_name, "cards": len(cards)}, indent=2))


def cmd_add(args: argparse.Namespace) -> None:
    """Add new cards to an existing deck."""
    deck = load_deck(args.deck_name)
    cards_data = _validate_cards_json(args.cards)
    next_id = deck.get("next_id", len(deck["cards"]) + 1)

    new_cards = []
    for i, c in enumerate(cards_data):
        new_cards.append(new_card(next_id + i, c["q"], c["a"]))

    deck["cards"].extend(new_cards)
    deck["next_id"] = next_id + len(new_cards)
    deck["updated_at"] = datetime.now().isoformat()
    save_deck(deck)
    print(json.dumps({"status": "added", "deck": args.deck_name, "new_cards": len(new_cards), "total_cards": len(deck["cards"])}, indent=2))


def cmd_list(args: argparse.Namespace) -> None:
    """List all decks with card counts and due counts."""
    ensure_dir()
    decks: list[dict] = []
    for f in sorted(DECKS_DIR.glob("*.json")):
        with open(f) as fh:
            d = json.load(fh)
            now = datetime.now()
            due = sum(1 for c in d["cards"] if datetime.fromisoformat(c["next_review"]) <= now)
            decks.append({
                "name": d["name"],
                "cards": len(d["cards"]),
                "due": due,
                "created": d.get("created_at", "unknown"),
            })
    print(json.dumps({"decks": decks}, indent=2))


def cmd_stats(args: argparse.Namespace) -> None:
    """Show statistics for a specific deck."""
    deck = load_deck(args.deck_name)
    now = datetime.now()
    cards = deck["cards"]
    due = [c for c in cards if datetime.fromisoformat(c["next_review"]) <= now]
    mastered = [c for c in cards if c.get("repetitions", 0) >= MASTERY_THRESHOLD]
    learning = [c for c in cards if 0 < c.get("repetitions", 0) < MASTERY_THRESHOLD]
    new = [c for c in cards if c.get("repetitions", 0) == 0]

    print(json.dumps({
        "deck": args.deck_name,
        "total_cards": len(cards),
        "due_now": len(due),
        "mastered": len(mastered),
        "learning": len(learning),
        "new": len(new),
        "average_ease": round(sum(c.get("ease", DEFAULT_EASE) for c in cards) / max(len(cards), 1), 2),
    }, indent=2))


def cmd_review(args: argparse.Namespace) -> None:
    """Return due cards for review, shuffled randomly."""
    deck = load_deck(args.deck_name)
    now = datetime.now()
    due = [c for c in deck["cards"] if datetime.fromisoformat(c["next_review"]) <= now]

    if not due:
        next_reviews = sorted(deck["cards"], key=lambda c: c["next_review"])
        next_time = next_reviews[0]["next_review"] if next_reviews else "never"
        print(json.dumps({"status": "no_cards_due", "next_review": next_time}, indent=2))
        return

    random.shuffle(due)
    cards_out = [{"id": c["id"], "q": c["q"], "a": c["a"], "repetitions": c.get("repetitions", 0)} for c in due]
    print(json.dumps({"deck": args.deck_name, "due_count": len(due), "cards": cards_out}, indent=2))


def cmd_quiz(args: argparse.Namespace) -> None:
    """Generate a random quiz from the deck's cards."""
    deck = load_deck(args.deck_name)
    count = min(args.count or DEFAULT_QUIZ_COUNT, len(deck["cards"]))
    selected = random.sample(deck["cards"], count)
    cards_out = [{"id": c["id"], "q": c["q"], "a": c["a"]} for c in selected]
    print(json.dumps({"deck": args.deck_name, "quiz_count": count, "cards": cards_out}, indent=2))


def cmd_exam(args: argparse.Namespace) -> None:
    """Generate a structured exam with multiple question types."""
    deck = load_deck(args.deck_name)
    count = min(args.questions or DEFAULT_EXAM_QUESTIONS, len(deck["cards"]))
    types = (args.types or "multiple_choice,short_answer,true_false").split(",")
    selected = random.sample(deck["cards"], count)
    all_answers = [c["a"] for c in deck["cards"]]

    questions: list[dict] = []
    for i, card in enumerate(selected):
        q_type = types[i % len(types)]
        q: dict = {"number": i + 1, "type": q_type, "question": card["q"], "card_id": card["id"]}

        if q_type == "multiple_choice":
            distractors = [a for a in all_answers if a != card["a"]]
            random.shuffle(distractors)
            options = [card["a"]] + distractors[:3]
            random.shuffle(options)
            q["options"] = options
            q["correct"] = card["a"]
        elif q_type == "true_false":
            use_true = random.choice([True, False])
            if use_true:
                q["statement"] = card["a"]
                q["correct"] = True
            else:
                if distractors := [a for a in all_answers if a != card["a"]]:
                    q["statement"] = random.choice(distractors)
                else:
                    q["statement"] = card["a"]
                    use_true = True
                q["correct"] = use_true
        else:
            q["correct"] = card["a"]

        questions.append(q)

    print(json.dumps({"deck": args.deck_name, "exam": questions}, indent=2))


def cmd_record(args: argparse.Namespace) -> None:
    """Record a review result for a specific card and update its schedule."""
    deck = load_deck(args.deck_name)
    card_id = args.card_id

    for card in deck["cards"]:
        if card["id"] == card_id:
            sm2_update(card, args.result)
            deck["updated_at"] = datetime.now().isoformat()
            save_deck(deck)
            print(json.dumps({
                "status": "recorded",
                "card_id": card_id,
                "result": args.result,
                "next_review": card["next_review"],
                "interval_days": card["interval"],
                "ease": card["ease"],
            }, indent=2))
            return

    logger.error("Card ID %d not found in deck '%s'.", card_id, args.deck_name)
    print(f"Error: Card ID {card_id} not found in deck '{args.deck_name}'.", file=sys.stderr)
    sys.exit(1)


def cmd_due(args: argparse.Namespace) -> None:
    """List all decks that have cards due for review."""
    ensure_dir()
    now = datetime.now()
    results: list[dict] = []
    for f in sorted(DECKS_DIR.glob("*.json")):
        with open(f) as fh:
            d = json.load(fh)
            due = [c for c in d["cards"] if datetime.fromisoformat(c["next_review"]) <= now]
            if due:
                results.append({"deck": d["name"], "due_count": len(due)})
    print(json.dumps({"due_decks": results, "total_due": sum(r["due_count"] for r in results)}, indent=2))


def cmd_export(args: argparse.Namespace) -> None:
    """Export a deck as formatted JSON to stdout."""
    deck = load_deck(args.deck_name)
    print(json.dumps(deck, indent=2, ensure_ascii=False))


def cmd_import(args: argparse.Namespace) -> None:
    """Import a deck from a JSON file on disk."""
    ensure_dir()
    try:
        with open(args.file_path) as f:
            deck = json.load(f)
    except FileNotFoundError:
        logger.error("File not found: %s", args.file_path)
        print(f"Error: File not found: {args.file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in file '%s': %s", args.file_path, exc)
        print(f"Error: Invalid JSON in file '{args.file_path}': {exc}", file=sys.stderr)
        sys.exit(1)

    if "name" not in deck or "cards" not in deck:
        logger.error("Invalid deck format. Must have 'name' and 'cards'.")
        print("Error: Invalid deck format. Must have 'name' and 'cards'.", file=sys.stderr)
        sys.exit(1)
    save_deck(deck)
    print(json.dumps({"status": "imported", "deck": deck["name"], "cards": len(deck["cards"])}, indent=2))


def cmd_delete(args: argparse.Namespace) -> None:
    """Delete a deck file from disk."""
    path = deck_path(args.deck_name)
    if not path.exists():
        logger.error("Deck '%s' not found.", args.deck_name)
        print(f"Error: Deck '{args.deck_name}' not found.", file=sys.stderr)
        sys.exit(1)
    path.unlink()
    print(json.dumps({"status": "deleted", "deck": args.deck_name}, indent=2))


def main() -> None:
    """Entry point: parse CLI arguments and dispatch to the appropriate command."""
    parser = argparse.ArgumentParser(description="Study Buddy - Flashcard Deck Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create")
    p.add_argument("deck_name")
    p.add_argument("--cards", required=True)

    p = sub.add_parser("add")
    p.add_argument("deck_name")
    p.add_argument("--cards", required=True)

    sub.add_parser("list")

    p = sub.add_parser("stats")
    p.add_argument("deck_name")

    p = sub.add_parser("review")
    p.add_argument("deck_name")

    p = sub.add_parser("quiz")
    p.add_argument("deck_name")
    p.add_argument("--count", type=int, default=10)

    p = sub.add_parser("exam")
    p.add_argument("deck_name")
    p.add_argument("--questions", type=int, default=20)
    p.add_argument("--types", default="multiple_choice,short_answer,true_false")

    p = sub.add_parser("record")
    p.add_argument("deck_name")
    p.add_argument("--card-id", type=int, required=True)
    p.add_argument("--result", required=True, choices=["correct", "partial", "missed"])

    sub.add_parser("due")

    p = sub.add_parser("export")
    p.add_argument("deck_name")

    p = sub.add_parser("import")
    p.add_argument("file_path")

    p = sub.add_parser("delete")
    p.add_argument("deck_name")

    args = parser.parse_args()

    commands: dict[str, callable] = {
        "create": cmd_create, "add": cmd_add, "list": cmd_list,
        "stats": cmd_stats, "review": cmd_review, "quiz": cmd_quiz,
        "exam": cmd_exam, "record": cmd_record, "due": cmd_due,
        "export": cmd_export, "import": cmd_import, "delete": cmd_delete,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
