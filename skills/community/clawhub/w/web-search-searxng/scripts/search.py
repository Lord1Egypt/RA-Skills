#!/usr/bin/env python3
"""
SearXNG Search - Web search using SearXNG meta-search engine.
"""

import requests
import json
import time
import argparse
from typing import Optional, List, Dict
from urllib.parse import urlencode, quote
from pathlib import Path


class SearXNGClient:
    """
    Client for SearXNG meta-search engine.
    
    Features:
    - Search across multiple engines
    - Category filtering (news, images, etc.)
    - Time range filtering
    - Rate limiting support
    """
    
    def __init__(self, base_url: str = "https://searx.be", rate_limit: float = 0.5):
        """
        Initialize SearXNG client.
        
        Args:
            base_url: SearXNG instance URL
            rate_limit: Minimum seconds between requests
        """
        self.base_url = base_url.rstrip("/")
        self.rate_limit = rate_limit
        self._last_request_time: Optional[float] = None
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/html",
            "Accept-Language": "en-US,en;q=0.9",
        })
    
    def _rate_limit_wait(self):
        """Wait to respect rate limit."""
        if self._last_request_time is not None:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.rate_limit:
                time.sleep(self.rate_limit - elapsed)
        self._last_request_time = time.time()
    
    def search(
        self,
        query: str,
        category: str = "general",
        language: str = "en-US",
        safesearch: int = 0,
        time_range: str = "",
        engines: Optional[List[str]] = None,
        limit: int = 10,
        timeout: int = 30
    ) -> Dict:
        """
        Perform search query.
        
        Args:
            query: Search query
            category: Search category (general, news, images, videos, files)
            language: Language code (e.g., en-US, de-DE)
            safesearch: 0=off, 1=moderate, 2=strict
            time_range: day, week, month, year, or empty
            engines: List of engines to use (e.g., ["google", "duckduckgo"])
            limit: Maximum number of results
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary with search results
        """
        self._rate_limit_wait()
        
        # Build request parameters
        params = {
            "q": query,
            "language": language,
            "safesearch": safesearch,
            "format": "json"
        }
        
        if category and category != "general":
            params["categories"] = category
        
        if time_range:
            params["time_range"] = time_range
        
        if engines:
            params["engines"] = ",".join(engines)
        
        try:
            url = f"{self.base_url}/search"
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Limit results if needed
            if "results" in data and limit > 0:
                data["results"] = data["results"][:limit]
            
            return data
            
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(f"Cannot connect to SearXNG at {self.base_url}: {e}")
        except requests.exceptions.Timeout:
            raise RuntimeError(f"SearXNG request timed out after {timeout}s")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"SearXNG request failed: {e}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid JSON response from SearXNG")
    
    def search_simple(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Simple search returning just results list.
        
        Args:
            query: Search query
            limit: Max results
            
        Returns:
            List of result dictionaries
        """
        response = self.search(query, limit=limit)
        return response.get("results", [])
    
    def get_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions for query.
        
        Args:
            query: Partial query
            
        Returns:
            List of suggestions
        """
        self._rate_limit_wait()
        
        try:
            url = f"{self.base_url}/autocompleter"
            response = self.session.get(url, params={"q": query}, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            return []


def load_config(config_path: Optional[str] = None) -> Dict:
    """Load SearXNG configuration."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "searxng.yaml"
    else:
        config_path = Path(config_path)
    
    default_config = {
        "base_url": "https://searx.be",
        "defaults": {
            "language": "en-US",
            "safesearch": 0,
            "time_range": "",
            "results_per_page": 10
        },
        "engines": [],
        "categories": {
            "general": "general",
            "news": "news",
            "images": "images",
            "videos": "videos",
            "files": "files"
        }
    }
    
    if config_path.exists():
        try:
            import yaml
            with open(config_path) as f:
                user_config = yaml.safe_load(f) or {}
                # Merge
                config = default_config.copy()
                config.update(user_config)
                return config
        except Exception as e:
            print(f"Warning: Could not load config: {e}", file=sys.stderr)
    
    return default_config


def format_results(results: List[Dict], format_type: str = "text") -> str:
    """Format search results for display."""
    if format_type == "json":
        return json.dumps(results, indent=2)
    
    # Text format
    lines = []
    lines.append(f"Found {len(results)} results")
    lines.append("=" * 70)
    
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        content = result.get("content", "")[:200]  # Truncate
        engine = result.get("engine", "unknown")
        
        lines.append(f"\n{i}. {title}")
        lines.append(f"   URL: {url}")
        if content:
            lines.append(f"   {content}...")
        lines.append(f"   [via {engine}]")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SearXNG Web Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--category", default="general", 
                       choices=["general", "news", "images", "videos", "files", "science"],
                       help="Search category")
    parser.add_argument("--engines", help="Comma-separated list of engines")
    parser.add_argument("--time", choices=["day", "week", "month", "year"],
                       help="Time range filter")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--base-url", help="SearXNG instance URL")
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    # Create client
    base_url = args.base_url or config.get("base_url", "https://searx.be")
    client = SearXNGClient(base_url=base_url)
    
    # Parse engines
    engines = None
    if args.engines:
        engines = [e.strip() for e in args.engines.split(",")]
    
    # Search
    try:
        results = client.search(
            query=args.query,
            category=args.category,
            time_range=args.time or config["defaults"].get("time_range", ""),
            engines=engines,
            limit=args.limit
        )
        
        # Output
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(format_results(results.get("results", []), "text"))
            
            # Show suggestions if any
            suggestions = results.get("suggestions", [])
            if suggestions:
                print("\n\nSuggestions:")
                for s in suggestions[:5]:
                    print(f"  - {s}")
    
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    import sys
    main()
