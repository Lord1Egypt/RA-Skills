#!/usr/bin/env python3
"""
Tavily Crawl API - Crawl websites with intelligent extraction
Based on: https://docs.tavily.com/documentation/api-reference/endpoint/crawl

Cost: 3-5 credits per 10 pages (mapping + extraction)
Default: DISABLED (expensive) - requires --enable flag

Usage:
    python3 crawl.py --urls "https://example.com" --enable
    python3 crawl.py --urls "https://example.com" --enable --instructions "find all pricing pages"
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

# Constants
TAVILY_URL = "https://api.tavily.com/crawl"
CACHE_DIR = pathlib.Path.home() / ".openclaw" / "cache" / "tavily" / "crawl"
LOG_FILE = pathlib.Path.home() / ".openclaw" / "logs" / "tavily_crawl.log"
MAX_RETRIES = 3
RETRY_DELAY = 2.0
CACHE_TTL = 7200  # 2 hours (crawl is expensive)

# Warning about cost
COST_WARNING = """
⚠️  WARNING: Crawl API is EXPENSIVE!
   Cost: 3-5 credits per 10 pages
   Free tier (1000 credits/month) = ~200-300 pages
   
   This API is disabled by default. Use --enable to proceed.
"""


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
            "_url": result.get("results", [{}])[0].get("url") if result.get("results") else None,
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
# Tavily Crawl API
# ============================================================================

def tavily_crawl(params: Dict[str, Any]) -> Dict:
    """Crawl website using Tavily Crawl API"""
    key = load_key()
    if not key:
        log("Missing API key", "ERROR")
        raise SystemExit(
            "Missing TAVILY_API_KEY. Set env var TAVILY_API_KEY or add it to ~/.openclaw/.env"
        )

    payload = {"api_key": key, **params}

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            url = str(params.get("url", ""))[:50]
            log(f"Request attempt {attempt}/{MAX_RETRIES}: {url}...", "DEBUG")
            
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                TAVILY_URL,
                data=data,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method="POST",
            )

            # Crawl can take longer
            timeout = params.get("timeout", 150)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
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
                    "title": r.get("title"),
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

            log(f"Success: {len(result['results'])} pages crawled", "INFO")
            return result

        except urllib.error.HTTPError as e:
            last_error = f"HTTP {e.code}: {e.reason}"
            log(f"HTTP error (attempt {attempt}): {last_error}", "ERROR")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)
                continue
            break
            
        except urllib.error.URLError as e:
            last_error = f"URL error: {e.reason}"
            log(f"Network error (attempt {attempt}): {last_error}", "ERROR")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)
                continue
            break
            
        except Exception as e:
            last_error = str(e)
            log(f"Unexpected error (attempt {attempt}): {last_error}", "ERROR")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)
                continue
            break

    log(f"All retries failed: {last_error}", "ERROR")
    raise SystemExit(f"Tavily crawl failed after {MAX_RETRIES} attempts: {last_error}")


# ============================================================================
# Output Formatters
# ============================================================================

def to_markdown(obj: Dict) -> str:
    """Convert to human-readable Markdown"""
    lines = []
    
    lines.append(f"## Crawled {len(obj.get('results', []))} pages")
    lines.append("")
    
    for i, r in enumerate(obj.get("results", []), 1):
        url = r.get("url", "")
        title = r.get("title", "")
        content = r.get("raw_content", "")
        
        lines.append(f"### {i}. {title or url}")
        lines.append(f"**URL**: {url}")
        lines.append("")
        
        if content:
            # First 1000 chars
            preview = content[:1000] + ("..." if len(content) > 1000 else "")
            lines.append(preview)
        else:
            lines.append("*No content*")
        
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines).strip() + "\n"


def to_compact_md(obj: Dict) -> str:
    """Convert to compact Markdown"""
    lines = []
    
    lines.append(f"🕷️  Crawled {len(obj.get('results', []))} pages")
    lines.append("")
    
    for i, r in enumerate(obj.get("results", []), 1):
        url = r.get("url", "")
        title = r.get("title", "")
        
        lines.append(f"{i}. **{title or 'No title'}**")
        lines.append(f"   {url}")
        lines.append("")
    
    return "\n".join(lines).strip() + "\n"


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(
        description="Tavily Crawl - Crawl websites (EXPENSIVE - disabled by default)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{COST_WARNING}
Examples:
  # Crawl website (must use --enable)
  %(prog)s --url "https://example.com" --enable

  # Crawl with instructions
  %(prog)s --url "https://example.com" --enable --instructions "find all pricing pages"

  # Advanced crawl (higher cost)
  %(prog)s --url "https://example.com" --enable --extract-depth advanced

  # Limit pages
  %(prog)s --url "https://example.com" --enable --limit 20
        """
    )
    
    # Required
    ap.add_argument(
        "--url",
        required=True,
        help="Website URL to crawl"
    )
    
    # Safety flag (required for this expensive API)
    ap.add_argument(
        "--enable",
        action="store_true",
        help="REQUIRED: Enable crawl (acknowledges cost warning)"
    )
    
    # Instructions for targeted crawl
    ap.add_argument(
        "--instructions",
        help="Natural language instructions for what to crawl"
    )
    
    # Chunks per source
    ap.add_argument(
        "--chunks-per-source",
        type=int,
        default=3,
        choices=[1, 2, 3, 4, 5],
        help="Max chunks per source (1-5, default: 3)"
    )
    
    # Crawl depth
    ap.add_argument(
        "--max-depth",
        type=int,
        default=1,
        help="Maximum crawl depth (default: 1)"
    )
    ap.add_argument(
        "--max-breadth",
        type=int,
        default=20,
        help="Maximum pages per depth level (default: 20)"
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum total pages to crawl (default: 50)"
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
        default=150,
        help="Timeout in seconds (10-150, default: 150)"
    )
    
    # Path selection
    ap.add_argument(
        "--select-paths",
        help="Comma-separated path patterns to include"
    )
    ap.add_argument(
        "--select-domains",
        help="Comma-separated domains to include"
    )
    ap.add_argument(
        "--exclude-paths",
        help="Comma-separated path patterns to exclude"
    )
    ap.add_argument(
        "--exclude-domains",
        help="Comma-separated domains to exclude"
    )
    
    # Media
    ap.add_argument(
        "--include-images",
        action="store_true",
        help="Include images from pages"
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
        help="Include credit usage information"
    )
    
    # Output
    ap.add_argument(
        "--output",
        default="compact",
        choices=["raw", "md", "compact"],
        help="Output format: raw (JSON) | md (detailed Markdown) | compact (simple)"
    )
    ap.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching"
    )
    
    args = ap.parse_args()
    
    # Safety check
    if not args.enable:
        print(COST_WARNING, file=sys.stderr)
        print("❌ Error: Crawl API is disabled by default due to high cost.", file=sys.stderr)
        print("   Use --enable to proceed (you acknowledge the cost).", file=sys.stderr)
        sys.exit(1)
    
    # Build API parameters
    params = {
        "url": args.url,
        "instructions": args.instructions,
        "chunks_per_source": args.chunks_per_source,
        "max_depth": args.max_depth,
        "max_breadth": args.max_breadth,
        "limit": args.limit,
        "extract_depth": args.extract_depth,
        "format": args.format,
        "timeout": args.timeout,
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Path/domain filtering
    if args.select_paths:
        params["select_paths"] = [p.strip() for p in args.select_paths.split(",")]
    if args.select_domains:
        params["select_domains"] = [d.strip() for d in args.select_domains.split(",")]
    if args.exclude_paths:
        params["exclude_paths"] = [p.strip() for p in args.exclude_paths.split(",")]
    if args.exclude_domains:
        params["exclude_domains"] = [d.strip() for d in args.exclude_domains.split(",")]
    
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
    
    # Perform crawl
    result = tavily_crawl(params)
    
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
