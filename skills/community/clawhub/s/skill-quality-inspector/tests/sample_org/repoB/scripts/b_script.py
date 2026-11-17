#!/usr/bin/env python3
"""b_script.py — fixture。"""
import argparse
import sys


def main():
    argparse.ArgumentParser(description="b").parse_args()
    return 0


if __name__ == "__main__":
    sys.exit(main())
