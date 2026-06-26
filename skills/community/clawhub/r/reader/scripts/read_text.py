#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.text_utils import load_input

def main():
    parser = argparse.ArgumentParser(description="Read and normalize text")
    parser.add_argument("--file", help="Path to local file")
    parser.add_argument("--text", help="Direct text input")
    args = parser.parse_args()

    text = load_input(file_path=args.file, text=args.text)
    print(text)

if __name__ == "__main__":
    main()
