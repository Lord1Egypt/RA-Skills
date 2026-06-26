#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.text_utils import load_input, sentence_split
from lib.storage import load_history, save_history

def main():
    parser = argparse.ArgumentParser(description="Compare two texts")
    parser.add_argument("--file_a", required=True, help="First file")
    parser.add_argument("--file_b", required=True, help="Second file")
    args = parser.parse_args()

    text_a = load_input(file_path=args.file_a)
    text_b = load_input(file_path=args.file_b)

    set_a = set(sentence_split(text_a))
    set_b = set(sentence_split(text_b))

    only_a = sorted(set_a - set_b)[:10]
    only_b = sorted(set_b - set_a)[:10]
    shared = sorted(set_a & set_b)[:10]

    history = load_history()
    history["sessions"].append({
        "type": "compare",
        "file_a": args.file_a,
        "file_b": args.file_b,
        "created_at": datetime.now().isoformat()
    })
    save_history(history)

    print("SHARED")
    for x in shared:
        print(f"- {x}")
    print()
    print("ONLY IN A")
    for x in only_a:
        print(f"- {x}")
    print()
    print("ONLY IN B")
    for x in only_b:
        print(f"- {x}")

if __name__ == "__main__":
    main()
