#!/usr/bin/env python3
"""
Tavily Web Search - Full Featured
Based on: https://docs.tavily.com/documentation/api-reference/endpoint/search

Features:
- All search_depth options (basic, advanced, fast, ultra-fast)
- Topic filtering (general, news, finance)
- Time range filtering (day, week, month, year)
- Date range filtering (start_date, end_date)
- Domain filtering (include_domains, exclude_domains)
- Country targeting
- Raw content extraction (markdown, text)
- Image search
- Auto parameters
- Exact match
- Query caching
- Auto-retry with exponential backoff
- Comprehensive logging
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional, List, Dict, Any

# Import rate limit handler
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from rate_limit import rate_limit_handler, RateLimitError

# Constants
TAVILY_URL = "https://api.tavily.com/search"
CACHE_DIR = pathlib.Path.home() / ".openclaw" / "cache" / "tavily"
LOG_FILE = pathlib.Path.home() / ".openclaw" / "logs" / "tavily.log"
MAX_RETRIES = 3
RETRY_DELAY = 1.0
CACHE_TTL = 3600  # 1 hour


# ============================================================================
# Logging
# ============================================================================

def log(message: str, level: str = "INFO"):
    """Simple logging to file and stderr"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}\n"
    print(log_line.strip(), file=sys.stderr)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass


# ============================================================================
# Caching
# ============================================================================

def get_cache_key(params: Dict[str, Any]) -> str:
    """Generate cache key from all parameters"""
    key_str = json.dumps(params, sort_keys=True, default=str)
    return hashlib.md5(key_str.encode("utf-8")).hexdigest()


def load_from_cache(cache_key: str) -> Optional[Dict]:
    """Load result from cache if valid"""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    if not cache_file.exists():
        return None
    
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        cached_at = data.get("_cached_at", 0)
        if time.time() - cached_at > CACHE_TTL:
            log(f"Cache expired", "DEBUG")
            return None
        
        log(f"Cache hit", "DEBUG")
        return {k: v for k, v in data.items() if not k.startswith("_")}
    except Exception as e:
        log(f"Cache read error: {e}", "WARN")
        return None


def save_to_cache(cache_key: str, result: Dict):
    """Save result to cache"""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / f"{cache_key}.json"
        
        data = {
            "_cached_at": time.time(),
            "_query": result.get("query"),
            **result
        }
        
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        log(f"Cache saved", "DEBUG")
    except Exception as e:
        log(f"Cache write error: {e}", "WARN")


# ============================================================================
# API Key Management
# ============================================================================

def load_key() -> str:
    """Load API key from environment or .env file"""
    key = os.environ.get("TAVILY_API_KEY")
    if key:
        return key.strip()

    env_path = pathlib.Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\s*TAVILY_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except Exception as e:
            log(f"Error reading .env: {e}", "ERROR")

    return None


# ============================================================================
# Tavily API
# ============================================================================

@rate_limit_handler(max_retries=MAX_RETRIES, base_delay=RETRY_DELAY, log_func=log)
def tavily_search(params: Dict[str, Any]) -> Dict:
    """Search Tavily API with rate limit handling"""
    key = load_key()
    if not key:
        log("Missing API key", "ERROR")
        raise SystemExit(
            "Missing TAVILY_API_KEY. Set env var TAVILY_API_KEY or add it to ~/.openclaw/.env"
        )

    payload = {"api_key": key, **params}

    log(f"Request: {params.get('query', '')[:50]}...", "DEBUG")
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        TAVILY_URL,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8", errors="replace")

    try:
        obj = json.loads(body)
    except json.JSONDecodeError as e:
        log(f"JSON decode error: {e}", "ERROR")
        raise SystemExit(f"Tavily returned non-JSON: {body[:300]}")

    if "error" in obj:
        error_msg = obj.get("error", {}).get("message", "Unknown error")
        log(f"API error: {error_msg}", "ERROR")
        raise SystemExit(f"Tavily API error: {error_msg}")

    # Build response
    result = {
        "query": params.get("query"),
        "results": [],
    }
    
    # Include answer if requested
    if params.get("include_answer"):
        result["answer"] = obj.get("answer")
    
    # Include images if requested
    if params.get("include_images"):
        result["images"] = obj.get("images", [])
    
    # Process results
    for r in (obj.get("results") or []):
        result_item = {
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content"),
            "score": r.get("score"),
        }
        
        # Include raw_content if requested
        if params.get("include_raw_content"):
            result_item["raw_content"] = r.get("raw_content")
        
        # Include favicon if requested
        if params.get("include_favicon"):
            result_item["favicon"] = r.get("favicon")
        
        # Include published_date for news topic
        if params.get("topic") == "news":
            result_item["published_date"] = r.get("published_date")
        
        result["results"].append(result_item)

    log(f"Success: {len(result['results'])} results", "INFO")
    return result


# ============================================================================
# Output Formatters
# ============================================================================

def to_brave_like(obj: Dict) -> Dict:
    """Convert to Brave-like schema (title/url/snippet)"""
    results = []
    for r in obj.get("results", []):
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "snippet": r.get("content"),
            "score": r.get("score"),
        })
    out = {"query": obj.get("query"), "results": results}
    if "answer" in obj:
        out["answer"] = obj.get("answer")
    if "images" in obj:
        out["images"] = obj.get("images")
    return out


def to_markdown(obj: Dict) -> str:
    """Convert to human-readable Markdown"""
    lines = []
    
    # Answer section
    if obj.get("answer"):
        lines.append("## Answer")
        lines.append(obj["answer"].strip())
        lines.append("")
    
    # Images section
    if obj.get("images"):
        lines.append("## Images")
        for img in obj["images"]:
            lines.append(f"- ![]({img.get('url', '')}) {img.get('description', '')}")
        lines.append("")
    
    # Results section
    lines.append("## Results")
    for i, r in enumerate(obj.get("results", []), 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        snippet = (r.get("content") or "").strip()
        score = r.get("score")
        
        lines.append(f"### {i}. {title}")
        if url:
            lines.append(f"**URL**: {url}")
        if score is not None:
            lines.append(f"**Score**: {score:.2f}")
        if snippet:
            lines.append(f"\n{snippet}")
        
        # Include raw_content if available
        if r.get("raw_content"):
            lines.append("\n**Full Content:**")
            lines.append("```markdown")
            lines.append(r["raw_content"][:2000] + ("..." if len(r["raw_content"]) > 2000 else ""))
            lines.append("```")
        
        lines.append("")
    
    return "\n".join(lines).strip() + "\n"


def to_compact_md(obj: Dict) -> str:
    """Convert to compact Markdown (default format)"""
    lines = []
    
    if obj.get("answer"):
        lines.append(obj["answer"].strip())
        lines.append("")
    
    for i, r in enumerate(obj.get("results", []), 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        snippet = (r.get("content") or "").strip()
        
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
        if snippet:
            lines.append(f"   - {snippet}")
    
    return "\n".join(lines).strip() + "\n"


# ============================================================================
# Main
# ============================================================================

def parse_list_arg(arg: Optional[str]) -> List[str]:
    """Parse comma-separated list argument"""
    if not arg:
        return []
    return [x.strip() for x in arg.split(",") if x.strip()]


def main():
    ap = argparse.ArgumentParser(
        description="Tavily Web Search - Full-featured AI-optimized search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  %(prog)s --query "Python tutorial"

  # News search with time filter
  %(prog)s --query "AI breakthrough" --topic news --time-range day

  # Deep research with full content
  %(prog)s --query "LLM architecture" --search-depth advanced --include-raw-content markdown

  # Domain-specific search
  %(prog)s --query "React best practices" --include-domains "github.com,dev.to"

  # Finance news
  %(prog)s --query "stock market" --topic finance --time-range week

  # Image search
  %(prog)s --query "sunset photography" --include-images

  # Country-specific
  %(prog)s --query "tech startups" --country "united states"
        """
    )
    
    # Required
    ap.add_argument("--query", required=True, help="Search query (recommended max 400 chars)")
    
    # Search depth
    ap.add_argument(
        "--search-depth",
        default="basic",
        choices=["basic", "advanced", "fast", "ultra-fast"],
        help="Search depth: basic (balanced), advanced (best), fast/ultra-fast (speed)"
    )
    
    # Result count
    ap.add_argument("--max-results", type=int, default=5, help="Max results (1-20, default: 5)")
    
    # Topic
    ap.add_argument(
        "--topic",
        default="general",
        choices=["general", "news", "finance"],
        help="Search topic category"
    )
    
    # Time filtering
    ap.add_argument(
        "--time-range",
        choices=["day", "week", "month", "year", "d", "w", "m", "y"],
        help="Filter by time range from now"
    )
    ap.add_argument(
        "--start-date",
        help="Start date (YYYY-MM-DD format)"
    )
    ap.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD format)"
    )
    
    # Domain filtering
    ap.add_argument(
        "--include-domains",
        help="Comma-separated domains to include (e.g., 'github.com,dev.to')"
    )
    ap.add_argument(
        "--exclude-domains",
        help="Comma-separated domains to exclude"
    )
    
    # Country
    ap.add_argument(
        "--country",
        help="Boost results from specific country (e.g., 'united states', 'china')"
    )
    
    # Content options
    ap.add_argument(
        "--include-answer",
        action="store_true",
        help="Include AI-generated answer (basic or use --answer-type)"
    )
    ap.add_argument(
        "--answer-type",
        choices=["basic", "advanced"],
        help="Answer type: basic (quick) or advanced (detailed)"
    )
    ap.add_argument(
        "--include-raw-content",
        nargs="?",
        const="markdown",
        choices=["markdown", "text"],
        help="Include full page content (markdown or text)"
    )
    
    # Media
    ap.add_argument(
        "--include-images",
        action="store_true",
        help="Include image search results"
    )
    ap.add_argument(
        "--include-image-descriptions",
        action="store_true",
        help="Include image descriptions (requires --include-images)"
    )
    ap.add_argument(
        "--include-favicon",
        action="store_true",
        help="Include favicon URLs for results"
    )
    
    # Advanced
    ap.add_argument(
        "--auto-parameters",
        action="store_true",
        help="Let Tavily auto-configure parameters based on query"
    )
    ap.add_argument(
        "--exact-match",
        action="store_true",
        help="Require exact match for query phrases"
    )
    ap.add_argument(
        "--chunks-per-source",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="Max chunks per source (advanced depth only, default: 3)"
    )
    ap.add_argument(
        "--min-score",
        type=float,
        help="Minimum relevance score (0-1). Filter out low-quality results."
    )
    
    # Output
    ap.add_argument(
        "--format",
        default="compact",
        choices=["raw", "brave", "md", "compact"],
        help="Output: raw (JSON) | brave (web_search-like) | md (detailed Markdown) | compact (simple Markdown)"
    )
    ap.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching"
    )
    
    args = ap.parse_args()
    
    # Validate query length
    if len(args.query) > 400:
        log(f"⚠️  Warning: Query ({len(args.query)} chars) exceeds recommended 400 chars. Consider breaking it into smaller queries.", "WARN")
    
    # Build API parameters
    params = {
        "query": args.query,
        "search_depth": args.search_depth,
        "max_results": max(1, min(args.max_results, 20)),
        "topic": args.topic,
    }
    
    # Time filtering
    if args.time_range:
        params["time_range"] = args.time_range
    if args.start_date:
        params["start_date"] = args.start_date
    if args.end_date:
        params["end_date"] = args.end_date
    
    # Domain filtering
    include_domains = parse_list_arg(args.include_domains)
    exclude_domains = parse_list_arg(args.exclude_domains)
    if include_domains:
        params["include_domains"] = include_domains
    if exclude_domains:
        params["exclude_domains"] = exclude_domains
    
    # Country
    if args.country:
        params["country"] = args.country
    
    # Answer
    if args.answer_type:
        params["include_answer"] = args.answer_type
    elif args.include_answer:
        params["include_answer"] = True
    
    # Raw content
    if args.include_raw_content:
        params["include_raw_content"] = args.include_raw_content
    
    # Images
    if args.include_images:
        params["include_images"] = True
        if args.include_image_descriptions:
            params["include_image_descriptions"] = True
    
    # Favicon
    if args.include_favicon:
        params["include_favicon"] = True
    
    # Advanced
    if args.auto_parameters:
        params["auto_parameters"] = True
    if args.exact_match:
        params["exact_match"] = True
    if args.search_depth == "advanced":
        params["chunks_per_source"] = args.chunks_per_source
    
    # Check cache
    cache_key = None
    if not args.no_cache:
        cache_key = get_cache_key(params)
        cached = load_from_cache(cache_key)
        if cached:
            if args.format == "md":
                sys.stdout.write(to_markdown(cached))
            elif args.format == "compact":
                sys.stdout.write(to_compact_md(cached))
            elif args.format == "brave":
                json.dump(to_brave_like(cached), sys.stdout, ensure_ascii=False, indent=2)
            else:
                json.dump(cached, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
            return
    
    # Perform search
    result = tavily_search(params)
    
    # Cache result
    if cache_key:
        save_to_cache(cache_key, result)
    
    # Apply score filtering if requested
    if args.min_score is not None:
        original_count = len(result["results"])
        result["results"] = [
            r for r in result["results"]
            if r.get("score", 0) >= args.min_score
        ]
        filtered_count = len(result["results"])
        if filtered_count < original_count:
            log(f"Filtered {original_count - filtered_count} results below score {args.min_score}", "INFO")
    
    # Output
    if args.format == "md":
        sys.stdout.write(to_markdown(result))
    elif args.format == "compact":
        sys.stdout.write(to_compact_md(result))
    elif args.format == "brave":
        json.dump(to_brave_like(result), sys.stdout, ensure_ascii=False, indent=2)
    else:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
