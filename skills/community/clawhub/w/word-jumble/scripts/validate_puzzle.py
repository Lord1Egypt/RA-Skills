#!/usr/bin/env python3
"""
Validate a Word Jumble puzzle JSON against all invariants.
Exit 0 = valid, exit 1 = invalid (errors printed to stderr).
"""

import json
import sys


def validate(puzzle: dict) -> list[str]:
    errors = []
    all_circled = []

    for i, word in enumerate(puzzle.get("scrambles", [])):
        tag = f"Word {i+1} ({(''.join(word.get('unscrambled', []))))}"

        scrambled = word.get("scrambled", [])
        unscrambled = word.get("unscrambled", [])

        # 1. Anagram check
        if sorted(scrambled) != sorted(unscrambled):
            errors.append(f"{tag}: scrambled is not an anagram of unscrambled")

        # 2. circled positions extract the right letters
        circled = word.get("circled", [])
        clue_letters = word.get("clue_letters", [])
        extracted = [unscrambled[pos - 1] for pos in circled if pos - 1 < len(unscrambled)]
        if extracted != clue_letters:
            errors.append(
                f"{tag}: clue_letters {clue_letters} don't match "
                f"letters at circled positions {circled} → {extracted}"
            )

        all_circled.extend(extracted)

    # 3. All circled letters match the solution (excluding spaces)
    solution = puzzle.get("final_puzzle", {}).get("solution", [])
    solution_letters = [c for c in solution if c != " "]

    if sorted(all_circled) != sorted(solution_letters):
        errors.append(
            f"Final: circled letters {sorted(all_circled)} "
            f"don't match solution letters {sorted(solution_letters)}"
        )

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_puzzle.py <puzzle.json>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        puzzle = json.load(f)

    errors = validate(puzzle)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print("✅ Puzzle valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
