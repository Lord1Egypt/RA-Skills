#!/usr/bin/env python3
"""
Token Audit for memory-bank
Measures the actual token cost of your MEMORY.md file.

Usage:
  python token-audit.py                    # audits ./MEMORY.md
  python token-audit.py path/to/MEMORY.md  # audits a specific file

Requires: pip install tiktoken
"""

import sys
import os

def count_tokens(text):
    """Count tokens using tiktoken (closest to Claude's tokenizer)."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        # Fallback: estimate ~3.5 chars per token for Claude
        return int(len(text) / 3.5)

def audit_memory(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        print("Run this script in a directory with a MEMORY.md file.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.strip().split("\n")
    total_tokens = count_tokens(content)
    total_lines = len(lines)

    # Parse sections
    sections = {}
    current_section = "Header"
    current_lines = []

    for line in lines:
        if line.startswith("## "):
            if current_lines:
                sections[current_section] = "\n".join(current_lines)
            current_section = line.strip("# ").strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines:
        sections[current_section] = "\n".join(current_lines)

    # Tier classification
    tier1_names = ["Project Overview", "Where We Left Off", "Blockers"]
    tier2_names = ["Key Decisions", "Key Files", "Architecture", "Architecture Notes", "Active Work"]
    tier3_names = ["Session Log", "User Preferences", "External Context", "Completed", "Known Issues", "Notes"]

    tier1_tokens = 0
    tier2_tokens = 0
    tier3_tokens = 0
    other_tokens = 0

    print()
    print("=" * 55)
    print("  MEMORY.MD TOKEN AUDIT")
    print("=" * 55)
    print()
    print(f"  File: {filepath}")
    print(f"  Lines: {total_lines} | Tokens: {total_tokens}")
    print()
    print("-" * 55)
    print(f"  {'Section':<30} {'Lines':>6} {'Tokens':>8}")
    print("-" * 55)

    for name, text in sections.items():
        t = count_tokens(text)
        l = len(text.strip().split("\n"))

        tier = ""
        if name in tier1_names:
            tier1_tokens += t
            tier = " [T1]"
        elif name in tier2_names:
            tier2_tokens += t
            tier = " [T2]"
        elif name in tier3_names:
            tier3_tokens += t
            tier = " [T3]"
        else:
            other_tokens += t

        print(f"  {name:<30} {l:>6} {t:>8}{tier}")

    print("-" * 55)
    print(f"  {'TOTAL':<30} {total_lines:>6} {total_tokens:>8}")
    print()

    # Tier summary
    print("  Progressive Loading Tiers:")
    print(f"    Tier 1 (always load):    {tier1_tokens:>6} tokens")
    print(f"    Tier 2 (on demand):      {tier2_tokens:>6} tokens")
    print(f"    Tier 3 (rarely needed):  {tier3_tokens:>6} tokens")
    print(f"    Other:                   {other_tokens:>6} tokens")
    print()

    # Health checks
    print("  Health Checks:")
    if total_tokens <= 400:
        print("    [PASS] Token count is excellent (under 400)")
    elif total_tokens <= 700:
        print("    [PASS] Token count is good (under 700)")
    elif total_tokens <= 1200:
        print("    [WARN] Token count is high (over 700). Consider compressing.")
    else:
        print("    [FAIL] Token count is too high (over 1200). Compress now.")

    if total_lines <= 80:
        print("    [PASS] Line count is good (under 80)")
    elif total_lines <= 150:
        print("    [WARN] Line count is high (over 80). Review for bloat.")
    else:
        print("    [FAIL] Line count exceeds 150. Compress immediately.")

    if tier1_tokens > 250:
        print("    [WARN] Tier 1 is heavy (over 250 tokens). Keep overview concise.")
    else:
        print("    [PASS] Tier 1 is lean (under 250 tokens)")

    # Comparison
    print()
    print("  Comparison:")
    print(f"    Your warm-up cost:       ~{total_tokens + 60} tokens (memory + greeting)")
    print(f"    Without memory-bank:     ~1,200 tokens (re-explain + file reads)")
    saved = 1200 - (total_tokens + 60)
    if saved > 0:
        pct = int(saved / 1200 * 100)
        print(f"    You save:                ~{saved} tokens per session ({pct}%)")
    else:
        print(f"    Your memory is LARGER than re-explaining. Compress it!")
    print()
    print("=" * 55)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "MEMORY.md"
    audit_memory(path)
