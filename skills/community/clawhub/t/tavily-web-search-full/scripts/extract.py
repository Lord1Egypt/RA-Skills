#!/usr/bin/env python3
"""
Tavily Extract API - Extract content from URLs
Based on: https://docs.tavily.com/documentation/api-reference/endpoint/extract

Usage:
    python3 extract.py --urls "https://example.com"
    python3 extract.py --urls "https://a.com,https://b.com" --query "find pricing info"
    python3 extract.py --urls "https://example.com" --extract-depth advanced --format markdown
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
from typing import Optional, List, Dict, Any, Union

# Import rate limit handler
SCRIPT_DIR = pathlib.Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from rate_limit import rate_limit_handler

# Constants
TAVILY_URL = "https://api.tavily.com/extract"
CACHE_DIR = pathlib.Path.home() / ".openclaw" / "cache" / "tavily" / "extract"
LOG_FILE = pathlib.Path.home() / ".openclaw" / "logs" / "tavily_extract.log"
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
            "_urls": result.get("results", [{}])[0].get("url") if result.get("results") else None,
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
# Tavily Extract API
# ============================================================================

@rate_limit_handler(max_retries=MAX_RETRIES, base_delay=RETRY_DELAY, log_func=log)
def tavily_extract(params: Dict[str, Any]) -> Dict:
    """Extract content from URLs using Tavily Extract API"""
    key = load_key()
    if not key:
        log("Missing API key", "ERROR")
        raise SystemExit(
            "Missing TAVILY_API_KEY. Set env var TAVILY_API_KEY or add it to ~/.openclaw/.env"
        )

    payload = {"api_key": key, **params}

    urls_str = str(params.get("urls", ""))[:50]
    log(f"Request: {urls_str}...", "DEBUG")
    
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
        "results": [],
    }
    
    # Process results
    for r in (obj.get("results") or []):
        result_item = {
            "url": r.get("url"),
            "raw_content": r.get("raw_content"),
        }
        
        # Include images if requested
        if params.get("include_images"):
            result_item["images"] = r.get("images", [])
        
        # Include favicon if requested
        if params.get("include_favicon"):
            result_item["favicon"] = r.get("favicon")
        
        result["results"].append(result_item)

    # Include usage if requested
    if params.get("include_usage") and "usage" in obj:
        result["usage"] = obj["usage"]
    
    # Include images list if requested (top-level)
    if params.get("include_images") and "images" in obj:
        result["images"] = obj["images"]

    log(f"Success: {len(result['results'])} URLs extracted", "INFO")
    return result


# ============================================================================
# Output Formatters
# ============================================================================

def to_markdown(obj: Dict) -> str:
    """Convert to human-readable Markdown"""
    lines = []
    
    for i, r in enumerate(obj.get("results", []), 1):
        url = r.get("url", "")
        content = r.get("raw_content", "")
        
        lines.append(f"## {i}. {url}")
        lines.append("")
        
        if content:
            lines.append(content)
        else:
            lines.append("*No content extracted*")
        
        # Include images if available
        if r.get("images"):
            lines.append("")
            lines.append("### Images")
            for img in r["images"]:
                img_url = img.get("url", "")
                img_desc = img.get("description", "")
                lines.append(f"- ![]({img_url}) {img_desc}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines).strip() + "\n"


def to_compact_md(obj: Dict) -> str:
    """Convert to compact Markdown"""
    lines = []
    
    for i, r in enumerate(obj.get("results", []), 1):
        url = r.get("url", "")
        content = r.get("raw_content", "")
        
        # First 500 chars preview
        preview = content[:500] + ("..." if len(content) > 500 else "")
        
        lines.append(f"{i}. **{url}**")
        lines.append("")
        lines.append(preview)
        lines.append("")
    
    return "\n".join(lines).strip() + "\n"


def parse_urls_arg(arg: str) -> List[str]:
    """Parse comma-separated URLs"""
    return [u.strip() for u in arg.split(",") if u.strip()]


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(
        description="Tavily Extract - Extract content from URLs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract single URL
  %(prog)s --urls "https://example.com/article"

  # Extract multiple URLs
  %(prog)s --urls "https://a.com,https://b.com,https://c.com"

  # Extract with query (reranks content by relevance)
  %(prog)s --urls "https://example.com" --query "find pricing information"

  # Advanced extraction (more data, higher cost)
  %(prog)s --urls "https://example.com" --extract-depth advanced

  # Include images from page
  %(prog)s --urls "https://example.com" --include-images

  # Output as plain text
  %(prog)s --urls "https://example.com" --format text
        """
    )
    
    # Required
    ap.add_argument(
        "--urls",
        required=True,
        help="URL(s) to extract (comma-separated for multiple)"
    )
    
    # Query for reranking
    ap.add_argument(
        "--query",
        help="User intent for reranking extracted content chunks"
    )
    
    # Chunks per source
    ap.add_argument(
        "--chunks-per-source",
        type=int,
        default=3,
        choices=[1, 2, 3, 4, 5],
        help="Max chunks per source (1-5, default: 3). Only used with --query"
    )
    
    # Extract depth
    ap.add_argument(
        "--extract-depth",
        default="basic",
        choices=["basic", "advanced"],
        help="Extraction depth: basic (1 credit/5 URLs) or advanced (2 credits/5 URLs)"
    )
    
    # Format
    ap.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "text"],
        help="Output format: markdown (default) or text"
    )
    
    # Timeout
    ap.add_argument(
        "--timeout",
        type=float,
        help="Timeout in seconds (1-60). Default: 10s (basic) or 30s (advanced)"
    )
    
    # Media
    ap.add_argument(
        "--include-images",
        action="store_true",
        help="Include images extracted from pages"
    )
    ap.add_argument(
        "--include-favicon",
        action="store_true",
        help="Include favicon URLs"
    )
    
    # Usage
    ap.add_argument(
        "--include-usage",
        action="store_true",
        help="Include credit usage information in response"
    )
    
    # Output
    ap.add_argument(
        "--output",
        default="compact",
        choices=["raw", "md", "compact"],
        help="Output format: raw (JSON) | md (detailed Markdown) | compact (simple Markdown)"
    )
    ap.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching"
    )
    
    args = ap.parse_args()
    
    # Parse URLs
    urls = parse_urls_arg(args.urls)
    if not urls:
        raise SystemExit("Error: No valid URLs provided")
    
    # Build API parameters
    params = {
        "urls": urls if len(urls) > 1 else urls[0],
        "extract_depth": args.extract_depth,
        "format": args.format,
    }
    
    # Query for reranking
    if args.query:
        params["query"] = args.query
        params["chunks_per_source"] = args.chunks_per_source
    
    # Timeout
    if args.timeout:
        params["timeout"] = max(1.0, min(60.0, args.timeout))
    
    # Media
    if args.include_images:
        params["include_images"] = True
    if args.include_favicon:
        params["include_favicon"] = True
    
    # Usage
    if args.include_usage:
        params["include_usage"] = True
    
    # Check cache
    cache_key = None
    if not args.no_cache:
        cache_key = get_cache_key(params)
        cached = load_from_cache(cache_key)
        if cached:
            if args.output == "md":
                sys.stdout.write(to_markdown(cached))
            elif args.output == "compact":
                sys.stdout.write(to_compact_md(cached))
            else:
                json.dump(cached, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
            return
    
    # Perform extraction
    result = tavily_extract(params)
    
    # Cache result
    if cache_key:
        save_to_cache(cache_key, result)
    
    # Output
    if args.output == "md":
        sys.stdout.write(to_markdown(result))
    elif args.output == "compact":
        sys.stdout.write(to_compact_md(result))
    else:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
