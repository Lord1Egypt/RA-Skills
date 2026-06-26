#!/usr/bin/env python3
"""
ClawHub Skill Search Rank Checker

Query the search ranking of a specific skill across one or more keywords
on ClawHub's public search API.

Usage:
    python3 rank_checker.py <skill_slug> <keyword1> [keyword2] [keyword3] ...

Options:
    --top N         Show top N results for each keyword (default: show only rank)
    --verbose       Show detailed output including scores and all ranked results
    --competitors   Also show competitors around the target skill
    --json          Output in JSON format

Examples:
    python3 rank_checker.py stock-price-query "stock price" "stock query" "股票"
    python3 rank_checker.py stock-price-query "stock price" --top 5
    python3 rank_checker.py stock-price-query "stock" --verbose
    python3 rank_checker.py stock-price-query "stock price" --competitors
    python3 rank_checker.py stock-price-query "stock price" "finance" --json
"""

import sys
import json
import re
import time
import urllib.request
import urllib.parse
import urllib.error


def validate_input(slug, keywords):
    """Validate input parameters for safety."""
    # Slug: alphanumeric, hyphens, underscores only
    if not re.match(r'^[a-zA-Z0-9_-]+$', slug):
        print(json.dumps({"error": f"Invalid slug format: {slug}"}))
        sys.exit(1)

    # Keywords: reasonable length, no control characters
    for kw in keywords:
        if len(kw) > 200:
            print(json.dumps({"error": f"Keyword too long (max 200 chars): {kw[:50]}..."}))
            sys.exit(1)
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', kw):
            print(json.dumps({"error": f"Keyword contains invalid characters: {kw}"}))
            sys.exit(1)


def search_clawhub(keyword, max_retries=2):
    """Search ClawHub API and return results list."""
    encoded_kw = urllib.parse.quote(keyword)
    url = f"https://clawhub.ai/api/search?q={encoded_kw}"

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'clawhub-skill-rank/1.0',
                'Accept': 'application/json'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get('results', [])
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                time.sleep(1.5)
                continue
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except urllib.error.URLError as e:
            return {"error": f"Network error: {str(e.reason)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    return {"error": "Max retries exceeded (rate limited)"}


def find_rank(results, target_slug):
    """Find the rank of target_slug in search results."""
    if isinstance(results, dict) and "error" in results:
        return None, results["error"]

    for i, r in enumerate(results, 1):
        slug = r.get('slug', '')
        if slug == target_slug:
            return i, None

    return None, None  # Not found, but no error


def format_rank(rank, total, error=None):
    """Format rank for display."""
    if error:
        return f"ERROR: {error}"
    if rank is None:
        return f"Not in top {total}"
    if rank == 1:
        return f"🥇 #{rank}/{total}"
    elif rank == 2:
        return f"🥈 #{rank}/{total}"
    elif rank == 3:
        return f"🥉 #{rank}/{total}"
    elif rank <= 5:
        return f"#{rank}/{total}"
    else:
        return f"#{rank}/{total}"


def get_competitors(results, target_slug, target_rank):
    """Get skills ranked around the target skill."""
    if isinstance(results, dict) or not results:
        return []

    competitors = []
    total = len(results)

    # Show 1 above and 1 below
    for i, r in enumerate(results, 1):
        slug = r.get('slug', '')
        if target_rank is not None:
            if abs(i - target_rank) <= 1:
                competitors.append({
                    "rank": i,
                    "slug": slug,
                    "displayName": r.get('displayName', slug),
                    "summary": r.get('summary', ''),
                    "score": r.get('score', 0),
                    "is_target": slug == target_slug
                })
        else:
            # Target not found, show top 3
            if i <= 3:
                competitors.append({
                    "rank": i,
                    "slug": slug,
                    "displayName": r.get('displayName', slug),
                    "summary": r.get('summary', ''),
                    "score": r.get('score', 0),
                    "is_target": False
                })

    return competitors


def main():
    args = sys.argv[1:]

    if len(args) < 2 or args[0] in ('-h', '--help'):
        print(__doc__.strip())
        sys.exit(0)

    # Parse options
    show_top = 0
    verbose = False
    show_competitors = False
    output_json = False

    slug = args[0]
    keywords = []

    i = 1
    while i < len(args):
        if args[i] == '--top':
            i += 1
            if i < len(args):
                try:
                    show_top = int(args[i])
                except ValueError:
                    print(json.dumps({"error": f"Invalid --top value: {args[i]}"}))
                    sys.exit(1)
        elif args[i] == '--verbose':
            verbose = True
        elif args[i] == '--competitors':
            show_competitors = True
        elif args[i] == '--json':
            output_json = True
        else:
            keywords.append(args[i])
        i += 1

    if not keywords:
        print(json.dumps({"error": "No keywords provided"}))
        sys.exit(1)

    validate_input(slug, keywords)

    # Collect results
    all_results = []

    for kw in keywords:
        results = search_clawhub(kw)
        rank, error = find_rank(results, slug)
        total = len(results) if isinstance(results, list) else 0

        entry = {
            "keyword": kw,
            "rank": rank,
            "total": total,
            "error": error,
            "rank_display": format_rank(rank, total, error)
        }

        if show_competitors or verbose:
            entry["competitors"] = get_competitors(results, slug, rank)

        if show_top > 0 and isinstance(results, list):
            top_results = []
            for j, r in enumerate(results[:show_top], 1):
                top_results.append({
                    "rank": j,
                    "slug": r.get('slug', '?'),
                    "displayName": r.get('displayName', '?'),
                    "summary": (r.get('summary', '') or '')[:80],
                    "score": round(r.get('score', 0), 2),
                    "is_target": r.get('slug', '') == slug
                })
            entry["top_results"] = top_results

        all_results.append(entry)

        # Rate limit between requests
        if len(keywords) > 1:
            time.sleep(0.3)

    # Output
    if output_json:
        output = {
            "skill": slug,
            "checked_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": all_results
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"=== ClawHub Search Rank: {slug} ===")
        print(f"Checked: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Summary table
        max_kw_len = max(len(kw) for kw in keywords)
        header_kw = "Keyword".ljust(max_kw_len)
        print(f"  {header_kw}  Rank")
        print(f"  {'─' * max_kw_len}  {'─' * 20}")

        for entry in all_results:
            kw_display = entry['keyword'].ljust(max_kw_len)
            print(f"  {kw_display}  {entry['rank_display']}")

        # Detailed sections
        for entry in all_results:
            if entry.get('top_results') or entry.get('competitors'):
                print(f"\n--- [{entry['keyword']}] ---")

                if entry.get('top_results'):
                    print(f"  Top {len(entry['top_results'])} results:")
                    for tr in entry['top_results']:
                        marker = " ◀ TARGET" if tr['is_target'] else ""
                        print(f"    #{tr['rank']} {tr['slug']} (score: {tr['score']}){marker}")
                        if verbose and tr['summary']:
                            print(f"       {tr['summary']}")

                if entry.get('competitors') and not entry.get('top_results'):
                    print(f"  Nearby competitors:")
                    for c in entry['competitors']:
                        marker = " ◀ TARGET" if c['is_target'] else ""
                        print(f"    #{c['rank']} {c['slug']} (score: {round(c['score'], 2)}){marker}")
                        if verbose and c['summary']:
                            print(f"       {c['summary']}")

        # Summary stats
        print()
        ranked = [e for e in all_results if e['rank'] is not None]
        unranked = [e for e in all_results if e['rank'] is None and e['error'] is None]
        errors = [e for e in all_results if e['error'] is not None]

        print(f"Summary: {len(ranked)} ranked / {len(unranked)} not found / {len(errors)} errors out of {len(all_results)} keywords")

        if ranked:
            ranks = [e['rank'] for e in ranked]
            best = min(ranked, key=lambda x: x['rank'])
            print(f"Best rank: #{best['rank']} for \"{best['keyword']}\"")
            avg_rank = sum(ranks) / len(ranks)
            print(f"Average rank: #{avg_rank:.1f} (across {len(ranked)} ranked keywords)")


if __name__ == '__main__':
    main()
