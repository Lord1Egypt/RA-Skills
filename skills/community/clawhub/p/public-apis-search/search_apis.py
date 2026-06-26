#!/usr/bin/env python3
"""Search public APIs by keyword, category, or filters."""

import json
import sys
import re
import io
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def load_db():
    db_path = Path(__file__).parent / 'apis.json'
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def score_match(api, keywords):
    """Score an API entry against search keywords. Higher = better match."""
    score = 0
    name_lower = api['name'].lower()
    desc_lower = api['description'].lower()
    cat_lower = api['category'].lower()

    for kw in keywords:
        # Exact name match: highest priority
        if kw == name_lower:
            score += 100
        elif name_lower.startswith(kw):
            score += 80
        elif kw in name_lower:
            score += 50
        # Description match
        if kw in desc_lower:
            score += 20
        # Category match
        if kw in cat_lower:
            score += 30

    return score

def format_api(api):
    """Format a single API entry for display."""
    auth_str = f"Auth: {api['auth']}"
    https_str = f"HTTPS: {api['https']}"
    cors_str = f"CORS: {api['cors']}"
    return f"- {api['name']}\n  {api['description']}\n  Category: {api['category']} | {auth_str} | {https_str} | {cors_str}\n  URL: {api['url']}"

def search(query, category=None, auth=None, https_only=False, limit=15):
    apis = load_db()
    keywords = re.findall(r'[\w\-]+', query.lower())

    # Filter by category
    if category:
        cat_lower = category.lower()
        apis = [a for a in apis if cat_lower in a['category'].lower()]

    # Filter by auth
    if auth:
        auth_lower = auth.lower()
        if auth_lower == 'free' or auth_lower == 'no':
            apis = [a for a in apis if a['auth'] == 'No']
        else:
            apis = [a for a in apis if auth_lower in a['auth'].lower()]

    # Filter HTTPS only
    if https_only:
        apis = [a for a in apis if a['https'] == 'Yes']

    # Score and sort
    scored = [(score_match(a, keywords), a) for a in apis]
    scored = [(s, a) for s, a in scored if s > 0]
    scored.sort(key=lambda x: -x[0])

    results = scored[:limit]

    if not results:
        # If no keyword match, show all matching filters
        if not keywords:
            results = [(0, a) for a in apis[:limit]]
        return []

    return results

def list_categories():
    apis = load_db()
    cats = {}
    for api in apis:
        cat = api['category']
        cats[cat] = cats.get(cat, 0) + 1
    for cat, count in sorted(cats.items()):
        print(f"  {cat} ({count})")

def main():
    if len(sys.argv) < 2:
        print("Usage: search_apis.py <query> [--category CAT] [--auth free|apiKey|OAuth] [--https] [--limit N]")
        print("       search_apis.py --categories    # List all categories")
        print("       search_apis.py --random [N]    # Show N random APIs (default 5)")
        sys.exit(1)

    query = sys.argv[1]

    # --categories
    if query == '--categories':
        print("Available categories:")
        list_categories()
        return

    # --random
    if query == '--random':
        import random
        apis = load_db()
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        sample = random.sample(apis, min(n, len(apis)))
        print(f"\n🎲 Random APIs ({n}):\n")
        for i, api in enumerate(sample, 1):
            print(f"{i}. {format_api(api)}\n")
        return

    # Parse args
    category = None
    auth = None
    https_only = False
    limit = 15

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == '--category' and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == '--auth' and i + 1 < len(args):
            auth = args[i + 1]
            i += 2
        elif args[i] == '--https':
            https_only = True
            i += 1
        elif args[i] == '--limit' and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            query += ' ' + args[i]
            i += 1

    results = search(query, category=category, auth=auth, https_only=https_only, limit=limit)

    if not results:
        print(f"No APIs found for: {query}")
        return

    print(f"Found {len(results)} APIs for: {query}\n")
    # Group by category
    by_cat = {}
    for score, api in results:
        cat = api['category']
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append((score, api))

    for cat, entries in sorted(by_cat.items()):
        print(f"【{cat}】")
        for score, api in entries:
            print(format_api(api))
            print()

if __name__ == '__main__':
    main()
