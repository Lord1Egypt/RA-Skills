#!/usr/bin/env python3
"""
context_guard.py

Default OpenClaw compatible session rotate trigger.
No memory system required.

Behavior:
- When used/max >= threshold (default 0.8), print a NEW_SESSION trigger line.
- By default, no cooldown, so every qualifying check can trigger.
"""

from __future__ import annotations

import argparse
import sys


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Trigger new session when context usage reaches threshold")
    p.add_argument("used_tokens", type=int, help="Current context used tokens")
    p.add_argument("max_tokens", type=int, help="Current context max tokens")
    p.add_argument("--threshold", type=float, default=0.8, help="Trigger threshold ratio, default 0.8")
    p.add_argument("--channel", default="boss", help="Channel label for message text")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if args.max_tokens <= 0:
        print("[ROTATE_ERROR] invalid max_tokens")
        return 1

    ratio = args.used_tokens / args.max_tokens
    if ratio < args.threshold:
        print(f"[ROTATE_NOT_NEEDED] ratio={ratio:.3f} < {args.threshold:.3f}")
        return 0

    pct = int(round(args.threshold * 100))
    print("[ROTATE_NEEDED]")
    print(f"[NEW_SESSION] 上下文达到{pct}%（{args.used_tokens}/{args.max_tokens}），自动切换新会话")
    print("[HANDOFF_HINT] 在旧会话保留3行交接：当前目标、已完成、下一步")
    return 0


if __name__ == "__main__":
    sys.exit(main())
