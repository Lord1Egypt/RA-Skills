"""Zopaf Coach — Conversational negotiation coaching interface.

Just talk. The math happens in the background.

Usage:
    python3 coach_cli.py
"""
from __future__ import annotations

import sys

from coach import NegotiationCoach


def main():
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║           Z O P A F   C O A C H             ║")
    print("  ║     Your AI negotiation coach.               ║")
    print("  ║     Just tell me what you're negotiating.    ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()
    print("  Type 'quit' to exit.\n")

    coach = NegotiationCoach()

    while True:
        try:
            user_input = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Good luck with your negotiation!\n")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("\n  Good luck with your negotiation!\n")
            break

        print()
        try:
            response = coach.chat(user_input)
            # Wrap long lines for terminal readability
            for line in response.split("\n"):
                print(f"  Coach: {line}" if line else "")
        except Exception as e:
            print(f"  [Error: {e}]")
        print()


if __name__ == "__main__":
    main()
