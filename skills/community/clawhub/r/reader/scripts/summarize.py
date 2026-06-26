#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.text_utils import load_input, summarize_simple
from lib.storage import load_history, save_history

def main():
    parser = argparse.ArgumentParser(description="Summarize text")
    parser.add_argument("--file", help="Path to local file")
    parser.add_argument("--text", help="Direct text input")
    parser.add_argument("--style", choices=["concise", "executive", "study"], default="concise")
    args = parser.parse_args()

    text = load_input(file_path=args.file, text=args.text)

    if args.style == "concise":
        summary = summarize_simple(text, max_sentences=2)
    elif args.style == "executive":
        summary = summarize_simple(text, max_sentences=4)
    else:
        summary = summarize_simple(text, max_sentences=5)

    history = load_history()
    history["sessions"].append({
        "type": "summary",
        "style": args.style,
        "file": args.file,
        "created_at": datetime.now().isoformat()
    })
    save_history(history)

    print("SUMMARY")
    print(summary)

if __name__ == "__main__":
    main()
