#!/usr/bin/env python3
"""
Goal Hierarchy Generator

Creates a 10-year → 1-year → 1-month → 1-week → daily goal hierarchy
from user's vision statement and anti-vision.
"""

import sys


def get_anti_vision():
    """Gather anti-vision (what user doesn't want)"""
    print("\n" + "=" * 60)
    print("ANTI-VISION EXERCISE")
    print("=" * 60)
    print("\nWrite out what you DON'T want in your life.")
    print("Be specific. Feel the discomfort. Don't stop until you feel it.\n")

    print("Consider these areas:")
    print("- Career/Work: What job or work situation would be terrible?")
    print("- Relationships: What kind of connections drain you?")
    print("- Health: What would your body look like if you neglected it?")
    print("- finances: What would financial stress look like for you?")
    print("- Daily life: What would a typical day look like that you hate?")

    print("\nType your anti-vision (press Enter twice when done, or 'skip' to move on):")

    lines = []
    while True:
        try:
            line = input()
            if line.lower() == 'skip':
                break
            if line == '' and lines:
                break
            lines.append(line)
        except EOFError:
            break

    return '\n'.join(lines)


def get_vision():
    """Gather vision (what user wants)"""
    print("\n" + "=" * 60)
    print("VISION EXERCISE")
    print("=" * 60)
    print("\nWrite out your ideal future. Be petty. Think big.")
    print("Ignore what's 'rational.' If friends/family think you can't do it, even better.\n")

    print("Consider these areas:")
    print("- Career: What work would you do for free?")
    print("- Impact: What problem would you solve for millions of people?")
    print("- Lifestyle: Where do you live? How do you spend your days?")
    print("- Relationships: Who surrounds you? What connections do you have?")
    print("- Health: How does your body feel? What can you do?")
    print("- finances: What does abundance look like for you?")
    print("- Legacy: What would you be remembered for?")

    print("\nType your vision (press Enter twice when done, or 'skip' to move on):")

    lines = []
    while True:
        try:
            line = input()
            if line.lower() == 'skip':
                break
            if line == '' and lines:
                break
            lines.append(line)
        except EOFError:
            break

    return '\n'.join(lines)


def get_distractions():
    """Gather distractions standing between user and their vision"""
    print("\n" + "=" * 60)
    print("DISTRACTIONS AUDIT")
    print("=" * 60)
    print("\nWhat stands between you and your vision?\n")

    print("People: Who drains your energy or holds you back?")
    print("Activities: What do you do that doesn't serve your vision?")
    print("Apps/Consumption: What content do you consume that doesn't help?")
    print("Habits: What patterns repeat that you want to change?")
    print("Commitments: What are you saying yes to that you should no?")

    print("\nType your distractions (press Enter twice when done, or 'skip' to move on):")

    lines = []
    while True:
        try:
            line = input()
            if line.lower() == 'skip':
                break
            if line == '' and lines:
                break
            lines.append(line)
        except EOFError:
            break

    return '\n'.join(lines)


def generate_10_year():
    """Generate 10-year goal from vision"""
    print("\n" + "=" * 60)
    print("10-YEAR GOAL")
    print("=" * 60)
    print("\nBased on your vision, what is your 10-year destination?")
    print("Think big. This is your north star.\n")

    print("Example: 'I will be the founder of a global education company")
    print("         impacting 10 million students annually.'")

    goal = input("Your 10-year goal: ")
    return goal


def generate_1_year(ten_year):
    """Generate 1-year goal from 10-year goal"""
    print("\n" + "=" * 60)
    print("1-YEAR GOAL")
    print("=" * 60)
    print(f"\nYour 10-year goal: {ten_year}")
    print("\nWhat milestone must you achieve in 1 year to stay on track?")
    print("Be specific and measurable.\n")

    print("Example: 'I will launch my MVP and acquire 1,000 paid subscribers'")

    goal = input("Your 1-year goal: ")
    return goal


def generate_1_month(one_year):
    """Generate 1-month goal from 1-year goal"""
    print("\n" + "=" * 60)
    print("1-MONTH GOAL")
    print("=" * 60)
    print(f"\nYour 1-year goal: {one_year}")
    print("\nWhat must you accomplish this month to stay on track?")
    print("This should be a concrete deliverable.\n")

    print("Example: 'I will create the minimum viable course product with 5 lessons'")

    goal = input("Your 1-month goal: ")
    return goal


def generate_1_week(one_month):
    """Generate 1-week goal from 1-month goal"""
    print("\n" + "=" * 60)
    print("1-WEEK GOAL")
    print("=" * 60)
    print(f"\nYour 1-month goal: {one_month}")
    print("\nWhat specific actions will you take this week?")
    print("Break it down into tangible tasks.\n")

    print("Example: 'Record 3 video lessons and set up the payment system'")

    goal = input("Your 1-week goal: ")
    return goal


def generate_daily(week):
    """Generate daily lever-moving tasks from 1-week goal"""
    print("\n" + "=" * 60)
    print("DAILY LEVER-MOVING TASKS")
    print("=" * 60)
    print(f"\nYour 1-week goal: {week}")
    print("\nWhat is ONE task you can do today that moves the needle?")
    print("If you could only do ONE thing today, what would it be?\n")

    print("Format: [Task] ([time duration])")

    task = input("Today's lever-moving task: ")
    return task


def generate_hierarchy():
    """Generate complete goal hierarchy"""
    print("=" * 60)
    print("GOAL HIERARCHY GENERATOR")
    print("=" * 60)
    print("\nThis tool helps you build a clear mental frame for your goals.")
    print("It creates a hierarchy: 10-year → 1-year → 1-month → 1-week → daily")

    # Get foundations
    anti_vision = get_anti_vision()
    vision = get_vision()
    distractions = get_distractions()

    # Generate hierarchy
    ten_year = generate_10_year()
    one_year = generate_1_year(ten_year)
    one_month = generate_1_month(one_year)
    one_week = generate_1_week(one_month)
    daily = generate_daily(one_week)

    # Output hierarchy
    print("\n" + "=" * 60)
    print("YOUR GOAL HIERARCHY")
    print("=" * 60)

    hierarchy = {
        "10-Year Goal": ten_year,
        "1-Year Goal": one_year,
        "1-Month Goal": one_month,
        "1-Week Goal": one_week,
        "Today's Lever-Moving Task": daily,
    }

    for level, goal in hierarchy.items():
        print(f"\n{level}:")
        print(f"  {goal}")

    print("\n" + "-" * 60)
    print("THE HIERARCHY:")
    print("-" * 60)
    print("""
    10-Year Goal → Where you want to be
        ↓
    1-Year Goal → Milestone to reach this year
        ↓
    1-Month Goal → What you must achieve this month
        ↓
    1-Week Goal → Actionable tasks this week
        ↓
    Lever-Moving Tasks → Daily 1-3 priorities that move the needle
    """)

    print("-" * 60)
    print("USAGE:")
    print("-" * 60)
    print("""
    DAILY PROTOCOL:
    1. Each morning, review your hierarchy
    2. Identify ONE lever-moving task for today
    3. Work on that for 60 minutes (no multitasking)
    4. At day's end, identify tomorrow's task
    5. Weekly, assess progress against 1-week goal
    6. Monthly, assess progress against 1-month goal
    7. Annually, reassess and adjust all goals
    """)

    # Store for potential export
    return hierarchy


def export_to_file(hierarchy):
    """Export hierarchy to a file"""
    filename = "goal_hierarchy.md"

    with open(filename, 'w') as f:
        f.write("# My Goal Hierarchy\n\n")
        f.write("## Anti-Vision\n")
        f.write(hierarchy.get('anti_vision', 'Not defined') + "\n\n")
        f.write("## Vision\n")
        f.write(hierarchy.get('vision', 'Not defined') + "\n\n")
        f.write("## Distractions to Remove\n")
        f.write(hierarchy.get('distractions', 'Not defined') + "\n\n")
        f.write("---\n\n")
        f.write("## Goals\n\n")
        for level, goal in hierarchy.items():
            if level not in ['anti_vision', 'vision', 'distractions']:
                f.write(f"### {level}\n{goal}\n\n")

    print(f"\nHierarchy exported to {filename}")


def main():
    hierarchy = generate_hierarchy()

    # Ask about export
    print("\n" + "=" * 60)
    export = input("Export to goal_hierarchy.md? (y/n): ")
    if export.lower() == 'y':
        # Add foundations to hierarchy for export
        anti_vision = get_anti_vision()
        vision = get_vision()
        distractions = get_distractions()
        hierarchy['anti_vision'] = anti_vision
        hierarchy['vision'] = vision
        hierarchy['distractions'] = distractions
        export_to_file(hierarchy)


if __name__ == "__main__":
    main()
