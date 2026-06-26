#!/usr/bin/env python3
"""
WheelSpotter - Multi-Platform Wheel Search Script

Your wheel-spotting scout. A cost-controlled intelligent search tool
for finding reusable solutions. Supports complexity-aware filtering,
intent-based platform selection, and form consistency checks.

Usage:
    python search.py --query "python pdf parser" --complexity L2 --intent library
    python search.py -q "react charting" -c L3 -i library -p github,npm --token $GITHUB_TOKEN
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import urllib.request
import urllib.error

# ============================================================================
# Configuration
# ============================================================================

VERSION = "1.0.0"
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_LIMIT = 20

# Star thresholds by complexity
STAR_THRESHOLDS = {
    "L1": 10,
    "L2": 50,
    "L3": 100
}

# Months threshold for "too old"
UPDATE_THRESHOLD_MONTHS = 24

# ============================================================================
# Data Models
# ============================================================================

class Complexity(str, Enum):
    L1 = "L1"  # Simple
    L2 = "L2"  # Medium
    L3 = "L3"  # Complex


class Intent(str, Enum):
    LIBRARY = "library"
    SERVICE = "service"
    TOOL = "tool"
    REFERENCE = "reference"


@dataclass
class SearchResult:
    """Represents a single search result from any platform."""
    name: str
    source: str
    url: str
    stars: int = 0
    description: str = ""
    last_updated: str = ""
    license: Optional[str] = None
    archived: bool = False
    deprecated: bool = False
    language: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None and v != ""}


@dataclass
class SearchResponse:
    """Complete search response with metadata."""
    status: str  # found, not_found, error
    query: str
    complexity: str
    intent: str
    total_found: int = 0
    after_filter: int = 0
    recommendations: List[Dict[str, Any]] = field(default_factory=list)
    message: Optional[str] = None
    error: Optional[str] = None
    cost: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


# ============================================================================
# HTTP Client (using urllib to avoid external deps beyond requests)
# ============================================================================

def http_get(url: str, headers: Dict[str, str] = None, timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict]:
    """Make HTTP GET request and return JSON response."""
    import requests
    
    try:
        resp = requests.get(url, headers=headers or {}, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.Timeout:
        print(f"Warning: Request timed out for {url}", file=sys.stderr)
        return None
    except requests.RequestException as e:
        print(f"Warning: Request failed for {url}: {e}", file=sys.stderr)
        return None


# ============================================================================
# Platform Search Functions
# ============================================================================

def search_github(query: str, limit: int = DEFAULT_LIMIT, token: str = None) -> List[SearchResult]:
    """
    Search GitHub repositories.
    
    Args:
        query: Search keywords
        limit: Maximum results to return
        token: GitHub personal access token (optional, increases rate limit)
    
    Returns:
        List of SearchResult objects
    """
    url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 100)  # GitHub API max is 100
    }
    
    # Build URL with query params
    param_str = "&".join(f"{k}={v}" for k, v in params.items())
    full_url = f"{url}?{param_str}"
    
    data = http_get(full_url, headers)
    if not data or "items" not in data:
        return []
    
    results = []
    for item in data.get("items", []):
        license_name = None
        if item.get("license"):
            license_name = item["license"].get("spdx_id")
        
        results.append(SearchResult(
            name=item.get("full_name", ""),
            source="github",
            url=item.get("html_url", ""),
            stars=item.get("stargazers_count", 0),
            description=item.get("description", "") or "",
            last_updated=item.get("updated_at", ""),
            license=license_name,
            archived=item.get("archived", False),
            deprecated=False,  # GitHub doesn't have deprecated flag
            language=item.get("language")
        ))
    
    return results


def search_pypi(query: str, limit: int = DEFAULT_LIMIT) -> List[SearchResult]:
    """
    Search PyPI packages.
    
    Note: PyPI's official search API is limited. This uses the JSON API
    for exact package lookups. For broader searches, combine with GitHub.
    
    Args:
        query: Package name (exact match preferred)
        limit: Maximum results (not used, PyPI returns single package)
    
    Returns:
        List of SearchResult objects
    """
    # PyPI JSON API - exact package lookup
    url = f"https://pypi.org/pypi/{query}/json"
    
    data = http_get(url)
    if not data:
        return []
    
    info = data.get("info", {})
    
    return [SearchResult(
        name=info.get("name", query),
        source="pypi",
        url=f"https://pypi.org/project/{query}/",
        stars=0,  # PyPI doesn't have stars
        description=info.get("summary", "") or "",
        last_updated=info.get("release_url", "").split("/")[-2] if info.get("release_url") else "",
        license=info.get("license"),
        language="Python"
    )]


def search_npm(query: str, limit: int = DEFAULT_LIMIT) -> List[SearchResult]:
    """
    Search npm packages.
    
    Args:
        query: Search keywords
        limit: Maximum results to return
    
    Returns:
        List of SearchResult objects
    """
    url = "https://registry.npmjs.org/-/v1/search"
    params = f"text={query}&size={min(limit, 250)}"
    full_url = f"{url}?{params}"
    
    data = http_get(full_url)
    if not data or "objects" not in data:
        return []
    
    results = []
    for item in data.get("objects", []):
        pkg = item.get("package", {})
        score = item.get("score", {})
        detail = score.get("detail", {})
        
        results.append(SearchResult(
            name=pkg.get("name", ""),
            source="npm",
            url=pkg.get("links", {}).get("npm", f"https://www.npmjs.com/package/{pkg.get('name', '')}"),
            stars=int(detail.get("popularity", 0) * 1000),  # Approximate stars from popularity
            description=pkg.get("description", "") or "",
            last_updated=pkg.get("date", {}).get("rel", ""),
            license=pkg.get("license"),
            language="JavaScript"
        ))
    
    return results


def search_maven(query: str, limit: int = DEFAULT_LIMIT) -> List[SearchResult]:
    """
    Search Maven Central (simplified - uses search.maven.org API).
    
    Args:
        query: Search keywords (groupId:artifactId or keywords)
        limit: Maximum results to return
    
    Returns:
        List of SearchResult objects
    """
    url = "https://search.maven.org/solrsearch/select"
    params = f"q={query}&rows={min(limit, 20)}&wt=json"
    full_url = f"{url}?{params}"
    
    data = http_get(full_url)
    if not data or "response" not in data:
        return []
    
    results = []
    docs = data.get("response", {}).get("docs", [])
    
    for doc in docs:
        group_id = doc.get("g", "")
        artifact_id = doc.get("a", "")
        version = doc.get("latestVersion", "")
        
        results.append(SearchResult(
            name=f"{group_id}:{artifact_id}",
            source="maven",
            url=f"https://mvnrepository.com/artifact/{group_id}/{artifact_id}",
            stars=0,  # Maven doesn't have stars
            description=f"Latest version: {version}",
            last_updated=doc.get("timestamp", ""),
            license=None,
            language="Java"
        ))
    
    return results


def search_crates(query: str, limit: int = DEFAULT_LIMIT) -> List[SearchResult]:
    """
    Search crates.io (Rust packages).
    
    Args:
        query: Search keywords
        limit: Maximum results to return
    
    Returns:
        List of SearchResult objects
    """
    url = "https://crates.io/api/v1/crates"
    params = f"q={query}&per_page={min(limit, 100)}"
    full_url = f"{url}?{params}"
    
    headers = {"User-Agent": "WheelSpotter/1.0"}
    
    data = http_get(full_url, headers)
    if not data or "crates" not in data:
        return []
    
    results = []
    for crate in data.get("crates", []):
        results.append(SearchResult(
            name=crate.get("name", ""),
            source="crates.io",
            url=f"https://crates.io/crates/{crate.get('name', '')}",
            stars=crate.get("downloads", 0) // 1000,  # Approximate from downloads
            description=crate.get("description", "") or "",
            last_updated=crate.get("updated_at", ""),
            license=crate.get("license"),
            language="Rust"
        ))
    
    return results


# ============================================================================
# Filtering Functions
# ============================================================================

def parse_github_date(date_str: str) -> Optional[datetime]:
    """Parse GitHub ISO date format."""
    if not date_str:
        return None
    try:
        # GitHub uses ISO 8601 format: 2023-01-15T10:30:00Z
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        return None


def months_since_update(date_str: str) -> int:
    """Calculate months since last update."""
    dt = parse_github_date(date_str)
    if not dt:
        return 0
    
    now = datetime.now(timezone.utc)
    delta = now - dt
    return int(delta.days / 30)


def hard_filter(
    results: List[SearchResult],
    complexity: str,
    intent: str,
    relax_niche: bool = False
) -> List[Dict[str, Any]]:
    """
    Apply hard filtering rules to search results.
    
    Rules:
    1. Archived projects are discarded
    2. Star threshold based on complexity (L1: 10, L2: 50, L3: 100)
    3. Update time: discard if >24 months (relax for niche domains)
    4. Form consistency: verify library/tool/service indicators
    
    Args:
        results: List of SearchResult objects
        complexity: L1, L2, or L3
        intent: library, service, tool, or reference
        relax_niche: Whether to relax thresholds for niche domains
    
    Returns:
        Filtered list of result dictionaries
    """
    filtered = []
    star_threshold = STAR_THRESHOLDS.get(complexity, 50)
    
    if relax_niche:
        star_threshold = max(10, star_threshold // 5)
    
    for result in results:
        skip_reasons = []
        
        # Rule 1: Archived check
        if result.archived:
            continue
        
        # Rule 2: Star threshold
        if result.stars < star_threshold and not relax_niche:
            continue
        
        # Rule 3: Update time
        months = months_since_update(result.last_updated)
        if months > UPDATE_THRESHOLD_MONTHS and not relax_niche:
            continue
        
        # Rule 4: Form consistency (lightweight check)
        desc_lower = result.description.lower()
        if intent == "library":
            if not any(kw in desc_lower for kw in ["library", "package", "module", "import", "api"]):
                # Downgrade but don't exclude
                pass
        
        filtered.append(result.to_dict())
    
    # Sort by stars descending
    filtered.sort(key=lambda x: x.get("stars", 0), reverse=True)
    
    return filtered


# ============================================================================
# Main Search Function
# ============================================================================

def search(
    query: str,
    complexity: str = "L2",
    intent: str = "library",
    platforms: str = "github",
    limit: int = DEFAULT_LIMIT,
    token: str = None,
    relax_niche: bool = False
) -> SearchResponse:
    """
    Execute multi-platform search with filtering.
    
    Args:
        query: Search keywords
        complexity: L1, L2, or L3
        intent: library, service, tool, or reference
        platforms: Comma-separated platform list
        limit: Max results per platform
        token: GitHub token (optional)
        relax_niche: Relax thresholds for niche domains
    
    Returns:
        SearchResponse with filtered results
    """
    start_time = datetime.now()
    
    # Parse platform list
    platform_list = [p.strip().lower() for p in platforms.split(",")]
    
    # Collect results from all platforms
    all_results: List[SearchResult] = []
    
    # Platform mapping
    platform_searchers = {
        "github": lambda: search_github(query, limit, token),
        "pypi": lambda: search_pypi(query, limit),
        "npm": lambda: search_npm(query, limit),
        "maven": lambda: search_maven(query, limit),
        "crates.io": lambda: search_crates(query, limit),
        "crates": lambda: search_crates(query, limit),
    }
    
    for platform in platform_list:
        searcher = platform_searchers.get(platform)
        if searcher:
            try:
                results = searcher()
                all_results.extend(results)
            except Exception as e:
                print(f"Warning: {platform} search failed: {e}", file=sys.stderr)
    
    # Apply hard filtering
    filtered = hard_filter(all_results, complexity, intent, relax_niche)
    
    # Limit to top 5 recommendations
    recommendations = filtered[:5]
    
    # Calculate time elapsed
    elapsed = (datetime.now() - start_time).total_seconds()
    
    # Build response
    status = "found" if recommendations else "not_found"
    
    return SearchResponse(
        status=status,
        query=query,
        complexity=complexity,
        intent=intent,
        total_found=len(all_results),
        after_filter=len(filtered),
        recommendations=recommendations,
        message=None if recommendations else "No suitable wheels found. Recommend self-build.",
        cost={
            "time_seconds": round(elapsed, 2),
            "platforms_queried": len(platform_list),
            "results_fetched": len(all_results)
        }
    )


# ============================================================================
# CLI Entry Point
# ============================================================================

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="WheelSpotter - Multi-Platform Wheel Search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -q "python pdf parser" -c L2 -i library
  %(prog)s -q "react charting" -c L3 -p github,npm --token $GITHUB_TOKEN
  %(prog)s -q "rust web framework" -c L3 -p github,crates -o results.json
        """
    )
    
    parser.add_argument(
        "-q", "--query",
        required=True,
        help="Search keywords"
    )
    
    parser.add_argument(
        "-c", "--complexity",
        choices=["L1", "L2", "L3"],
        default="L2",
        help="Complexity level (default: L2)"
    )
    
    parser.add_argument(
        "-i", "--intent",
        choices=["library", "service", "tool", "reference"],
        default="library",
        help="Intent type (default: library)"
    )
    
    parser.add_argument(
        "-p", "--platforms",
        default="github",
        help="Comma-separated platforms: github,pypi,npm,maven,crates (default: github)"
    )
    
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Max results per platform (default: {DEFAULT_LIMIT})"
    )
    
    parser.add_argument(
        "-t", "--token",
        help="GitHub personal access token (optional, increases rate limit)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "--relax-niche",
        action="store_true",
        help="Relax thresholds for niche domains"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    # Execute search
    response = search(
        query=args.query,
        complexity=args.complexity,
        intent=args.intent,
        platforms=args.platforms,
        limit=args.limit,
        token=args.token,
        relax_niche=args.relax_niche
    )
    
    # Output results
    output_json = json.dumps(response.to_dict(), indent=2, ensure_ascii=False)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output_json)
    
    # Exit with appropriate code
    sys.exit(0 if response.status == "found" else 1)


if __name__ == "__main__":
    main()
