#!/usr/bin/env python3
"""
Save the Cat beat sheet generator.
Calculates word count targets for each of the 15 beats.
"""

import argparse
import json
import sys

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# Save the Cat beats with approximate percentages
BEATS = [
    ("1. Opening Image", 0.00),
    ("2. Theme Stated", 0.05),
    ("3. Set-Up", 0.10),
    ("4. Catalyst", 0.12),
    ("5. Debate", 0.12),
    ("6. Break into Two", 0.20),
    ("7. B Story", 0.22),
    ("8. Fun and Games", 0.20),
    ("9. Midpoint", 0.50),
    ("10. Bad Guys Close In", 0.50),
    ("11. All Is Lost", 0.75),
    ("12. Dark Night of the Soul", 0.75),
    ("13. Break into Three", 0.80),
    ("14. Finale", 0.80),
    ("15. Final Image", 1.00),
]


def generate_beat_sheet(total_words: int) -> list:
    """Generate beat sheet with word count targets."""
    sheet = []
    for i, (beat_name, pct) in enumerate(BEATS):
        word_target = int(total_words * pct)
        
        # Calculate beat length (difference from previous)
        if i > 0:
            prev_pct = BEATS[i-1][1]
            beat_length = int(total_words * (pct - prev_pct))
        else:
            beat_length = 0
        
        sheet.append({
            "beat": beat_name,
            "cumulative_word": word_target,
            "beat_length": beat_length,
            "percentage": f"{pct * 100:.0f}%"
        })
    
    return sheet


def print_beat_sheet(sheet: list, total_words: int):
    """Print formatted beat sheet."""
    print("\n" + "=" * 60)
    print("🐱 SAVE THE CAT - BEAT SHEET")
    print(f"   Target: {total_words:,} words")
    print("=" * 60)
    print(f"\n{'Beat':<30} {'At Word':>10} {'Length':>10} {'%':>6}")
    print("-" * 60)
    
    for item in sheet:
        length_str = f"{item['beat_length']:,}" if item['beat_length'] > 0 else "-"
        print(f"{item['beat']:<30} {item['cumulative_word']:>10,} {length_str:>10} {item['percentage']:>6}")
    
    print("-" * 60)
    print("\n📝 Beat Descriptions:")
    print("""
1. Opening Image   - Visual snapshot of hero before the journey
2. Theme Stated    - Someone mentions the theme/lesson
3. Set-Up          - Introduce hero, world, and what's missing
4. Catalyst        - Inciting incident that changes everything
5. Debate          - Hero hesitates, considers the call
6. Break into Two  - Hero commits to the journey
7. B Story         - Relationship story (love, mentor, friend)
8. Fun and Games   - Promise of the premise, exploration
9. Midpoint        - False victory or false defeat, stakes raised
10. Bad Guys Close In - Pressure mounts, internal/external threats
11. All Is Lost    - Lowest point, death (literal or symbolic)
12. Dark Night     - Hero processes the loss, finds new resolve
13. Break into Three - Solution found, plan formed
14. Finale         - Final confrontation, transformation proven
15. Final Image    - Visual proof of change (opposite of opening)
""")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generate Save the Cat beat sheet")
    parser.add_argument("--target", type=int, required=True, help="Total word count target")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    sheet = generate_beat_sheet(args.target)
    
    if args.json:
        print(json.dumps({
            "total_words": args.target,
            "beats": sheet
        }, indent=2))
    else:
        print_beat_sheet(sheet, args.target)


if __name__ == "__main__":
    main()
