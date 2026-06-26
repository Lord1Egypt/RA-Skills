#!/usr/bin/env python3
"""
Tavily Search - Optimized Version
Fast web search with caching and timeout handling
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from functools import lru_cache

# Cache configuration
CACHE_DIR = Path.home() / ".cache" / "tavily_search"
CACHE_DURATION = 300  # 5 minutes cache

def get_cache_key(query: str, **kwargs) -> str:
    """Generate cache key from query and parameters."""
    cache_data = f"{query}:{json.dumps(kwargs, sort_keys=True)}"
    return hashlib.md5(cache_data.encode()).hexdigest()

def get_cached_result(cache_key: str) -> Optional[Dict]:
    """Get cached result if valid."""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    if not cache_file.exists():
        return None
    
    try:
        with open(cache_file, 'r') as f:
            cached = json.load(f)
        
        # Check if cache is still valid
        if time.time() - cached.get('timestamp', 0) < CACHE_DURATION:
            return cached['data']
    except Exception:
        pass
    
    return None

def cache_result(cache_key: str, data: Dict) -> None:
    """Cache search result."""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / f"{cache_key}.json"
        
        with open(cache_file, 'w') as f:
            json.dump({
                'timestamp': time.time(),
                'data': data
            }, f)
    except Exception:
        pass  # Cache failures shouldn't break search

def search_with_timeout(client, query: str, max_results: int = 5, **kwargs) -> Dict:
    """Perform search with timeout handling."""
    import signal
    
    class TimeoutError(Exception):
        pass
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Search timed out")
    
    # Set 15 second timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(15)
    
    try:
        result = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic",
            **kwargs
        )
        signal.alarm(0)  # Cancel timeout
        return result
    except TimeoutError:
        return {"error": "Search timed out after 15 seconds", "results": []}
    except Exception as e:
        signal.alarm(0)
        raise

def format_output(results: Dict, format_type: str = "json") -> str:
    """Format output for different use cases."""
    if format_type == "text":
        lines = []
        lines.append(f"Query: {results.get('query', 'N/A')}")
        lines.append(f"Results: {len(results.get('results', []))}")
        lines.append("-" * 50)
        
        for i, result in enumerate(results.get('results', []), 1):
            lines.append(f"\n{i}. {result.get('title', 'N/A')}")
            lines.append(f"   URL: {result.get('url', 'N/A')}")
            content = result.get('content', '')[:200]
            lines.append(f"   {content}...")
        
        return "\n".join(lines)
    
    else:  # json
        return json.dumps(results, indent=2, ensure_ascii=False)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fast Tavily Web Search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s "latest AI news" --max-results 10
    %(prog)s "weather today" --format text
    %(prog)s "stock market" --no-cache
        """
    )
    
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=5, help="Number of results (1-20)")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")
    parser.add_argument("--no-cache", action="store_true", help="Bypass cache")
    
    args = parser.parse_args()
    
    # Check API key
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("Error: TAVILY_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    
    # Check cache
    cache_key = get_cache_key(args.query, max_results=args.max_results)
    
    if not args.no_cache:
        cached = get_cached_result(cache_key)
        if cached:
            print(format_output(cached, args.format))
            return
    
    # Perform search
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=api_key)
        result = search_with_timeout(client, args.query, args.max_results)
        
        # Cache result
        if not args.no_cache and "error" not in result:
            cache_result(cache_key, result)
        
        print(format_output(result, args.format))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
