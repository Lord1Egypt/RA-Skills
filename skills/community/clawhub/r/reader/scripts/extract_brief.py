#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.text_utils import load_input, summarize_simple, extract_key_points, extract_action_items, extract_questions
from lib.storage import load_history, save_history

def main():
    parser = argparse.ArgumentParser(description="Extract a reading brief")
    parser.add_argument("--file", help="Path to local file")
    parser.add_argument("--text", help="Direct text input")
    args = parser.parse_args()

    text = load_input(file_path=args.file, text=args.text)

    summary = summarize_simple(text, max_sentences=3)
    key_points = extract_key_points(text, limit=5)
    actions = extract_action_items(text)
    questions = extract_questions(text)

    history = load_history()
    history["sessions"].append({
        "type": "brief",
        "file": args.file,
        "created_at": datetime.now().isoformat()
    })
    save_history(history)

    print("SUMMARY")
    print(summary)
    print()
    print("KEY POINTS")
    for point in key_points:
        print(f"- {point}")
    print()
    print("ACTION ITEMS")
    if actions:
        for item in actions:
            print(f"- {item}")
    else:
        print("- None detected")
    print()
    print("OPEN QUESTIONS")
    if questions:
        for q in questions:
            print(f"- {q}")
    else:
        print("- None detected")

if __name__ == "__main__":
    main()
