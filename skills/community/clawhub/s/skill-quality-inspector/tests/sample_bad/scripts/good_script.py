#!/usr/bin/env python3
"""good_script.py — fixture 示例脚本（坏样本中用于让内置脚本引用不悬空）。"""
import argparse
import sys


def main():
    ap = argparse.ArgumentParser(description="示例脚本")
    ap.add_argument("--hello", default="world")
    args = ap.parse_args()
    print("hello", args.hello)
    return 0


if __name__ == "__main__":
    sys.exit(main())
