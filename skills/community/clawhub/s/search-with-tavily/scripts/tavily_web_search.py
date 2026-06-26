#!/usr/bin/env python3
"""
Tavily Web Search - Simple wrapper for OpenClaw integration
Usage: tavily_web_search.py <query> [max_results]
"""

import sys
import json
import os

try:
    from tavily import TavilyClient
except ImportError:
    print(json.dumps({"error": "tavily-python not installed"}), file=sys.stderr)
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: tavily_web_search.py <query> [max_results]", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print(json.dumps({"error": "TAVILY_API_KEY not set"}), file=sys.stderr)
        sys.exit(1)
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic"
        )
        
        # Simplified output for OpenClaw
        results = []
        for r in response.get('results', []):
            results.append({
                "title": r.get('title'),
                "url": r.get('url'),
                "content": r.get('content', '')[:500],  # Truncate for readability
                "score": r.get('score')
            })
        
        output = {
            "query": query,
            "results_count": len(results),
            "results": results
        }
        
        print(json.dumps(output, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
