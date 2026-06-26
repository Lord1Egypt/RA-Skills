#!/usr/bin/env python3
"""Web search via DuckDuckGo HTML (no API key needed)."""

import sys
import urllib.parse
import subprocess
import re
import json
import argparse


def search(query, num=10):
    """Search DuckDuckGo and return results."""
    encoded_q = urllib.parse.quote(query)
    url = f"https://duckduckgo.com/html/?q={encoded_q}"
    
    result = subprocess.run(['curl', '-s', '--max-time', '15', url], 
                          capture_output=True, text=True, timeout=20)
    html = result.stdout
    
    if not html:
        print(f"Error: No response from DuckDuckGo (network may be blocked)")
        return []
    
    pattern = re.compile(r'<a class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>')
    matches = pattern.findall(html)
    
    results = []
    for url, title in matches[:num]:
        title = re.sub(r'<[^>]+>', '', title)
        title = title.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        results.append({'title': title, 'url': url})
    return results


def search_json(query, num=10):
    """Search DuckDuckGo JSON API."""
    encoded_q = urllib.parse.quote(query)
    url = f"https://api.duckduckgo.com/?q={encoded_q}&format=json&no_redirect=1"
    
    result = subprocess.run(['curl', '-s', '--max-time', '15', url],
                          capture_output=True, text=True, timeout=20)
    
    if not result.stdout:
        print(f"Error: No response from DuckDuckGo API")
        return {}
    
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON response")
        return {}


def main():
    parser = argparse.ArgumentParser(description='Web search via DuckDuckGo')
    parser.add_argument('query', nargs='+', help='Search query')
    parser.add_argument('-n', '--num', type=int, default=10, help='Number of results')
    parser.add_argument('--json', action='store_true', help='Use JSON API')
    args = parser.parse_args()
    
    query = ' '.join(args.query)
    
    if args.json:
        data = search_json(query, args.num)
        if 'RelatedTopics' in data:
            for item in data['RelatedTopics'][:args.num]:
                if 'Text' in item:
                    print(item['Text'])
                    if 'FirstURL' in item:
                        print(f"  {item['FirstURL']}")
                    print()
    else:
        results = search(query, args.num)
        print(f"Search: {query}")
        print("-" * 60)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}")
        if not results:
            print("(No results - network may be blocked)")


if __name__ == "__main__":
    main()
