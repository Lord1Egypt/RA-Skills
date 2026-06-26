#!/usr/bin/env python3
"""Search 100 udon recipes by keyword, ingredient, category, or number."""

import codecs
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows

RECIPES_FILE = Path(__file__).parent.parent / "references" / "recipes.md"

CATEGORY_KEYWORDS = {
    "grilled": ["grilled", "yaki"],
    "cold": ["cold", "hiyashi", "zaru"],
    "simmered": ["simmered", "nabeyaki", "nabe"],
    "curry": ["curry"],
    "miso": ["miso"],
    "egg": ["egg", "tamago"],
    "meat": ["meat", "pork", "beef", "chicken", "bacon", "ham"],
    "seafood": ["salmon", "tuna", "saba", "mentaiko", "tarako", "shrimp", "seafood"],
    "natto": ["natto"],
    "kimchi": ["kimchi"],
    "vegetable": ["vegetable", "cabbage", "spinach", "mushroom", "tomato"],
    "quick": ["easy", "quick", "minute", "no measuring"],
}


def parse_recipes(text: str) -> list[dict]:
    """Parse recipes.md into a list of recipe dicts."""
    results = []
    # Split by ## heading
    blocks = re.split(r"(?=^## \d+\.)", text, flags=re.MULTILINE)
    for block in blocks:
        m = re.match(r"^## (\d+)\.\s*(.+)$", block, re.MULTILINE)
        if not m:
            continue
        num = int(m.group(1))
        title = m.group(2).strip()
        # Extract ingredients from bullet points
        ingredients = re.findall(r"^\*\s*(.+)$", block, re.MULTILINE)
        # Extract link
        links = re.findall(r"\[View Recipe\]\(([^)]+)\)", block)
        results.append({
            "num": num,
            "title": title,
            "ingredients": ingredients,
            "link": links[0] if links else "",
        })
    return results


def search(query: str, recipes: list[dict]) -> list[dict]:
    """Filter recipes by keyword/ingredient."""
    q = query.lower()
    matches = []
    for r in recipes:
        score = 0
        searchable = (r["title"] + " " + " ".join(r["ingredients"])).lower()
        # Check each token in query
        for token in q.split():
            if token in searchable:
                score += 1
        if score > 0:
            matches.append((score, r))
    # Sort by match score descending
    matches.sort(key=lambda x: -x[0])
    return [r for _, r in matches]


def format_recipe(r: dict) -> str:
    """Format a single recipe for display."""
    lines = [f"## {r['num']}. {r['title']}"]
    if r["link"]:
        lines.append(f"  Link: {r['link']}")
    if r["ingredients"]:
        lines.append(f"  Ingredients: {', '.join(r['ingredients'])}")
    return "\n".join(lines)


def main():
    if not RECIPES_FILE.exists():
        print(f"Error: recipes file not found at {RECIPES_FILE}", file=sys.stderr)
        sys.exit(1)

    text = RECIPES_FILE.read_text(encoding="utf-8")
    recipes = parse_recipes(text)

    # No args: show all recipe numbers and titles
    if len(sys.argv) < 2:
        print(f"100 Udon Recipes — quick index:\n")
        for r in recipes:
            print(f"  {r['num']:>3}. {r['title']}")
        print(f"\nUsage: search_udon.py <keyword>")
        print("  e.g.: search_udon.py curry")
        print("        search_udon.py egg")
        print("        search_udon.py cold")
        print("        search_udon.py 42")
        return

    query = " ".join(sys.argv[1:])

    # If query is just a number, show that single recipe
    if query.isdigit():
        num = int(query)
        for r in recipes:
            if r["num"] == num:
                print(format_recipe(r))
                return
        print(f"Recipe #{num} not found.")
        return

    matches = search(query, recipes)
    if not matches:
        print(f"No recipes found matching '{query}'.")
        return

    print(f"Found {len(matches)} recipe(s) matching '{query}':\n")
    for r in matches:
        print(format_recipe(r))
        print()


if __name__ == "__main__":
    main()
