#!/usr/bin/env python3
"""good_script.py — fixture 示例脚本（仅用于测试 --help 检查）。"""
import argparse
import sys


def main():
    ap = argparse.ArgumentParser(description="示例脚本")
    ap.add_argument("--hello", default="world", help="问候对象")
    args = ap.parse_args()
    print("hello", args.hello)
    return 0


if __name__ == "__main__":
    sys.exit(main())
