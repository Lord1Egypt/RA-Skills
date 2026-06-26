#!/usr/bin/env python3
"""
Tavily Research API - Deep research with comprehensive reports
Based on: https://docs.tavily.com/documentation/api-reference/endpoint/research

Cost: 4-250 credits per research task (VERY EXPENSIVE!)
Default: DISABLED - requires --enable flag AND explicit confirmation

Usage:
    python3 research.py --query "AI impact on healthcare" --enable
    python3 research.py --query "market analysis" --model pro --enable
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
TAVILY_URL = "https://api.tavily.com/research"
TAVILY_STATUS_URL = "https://api.tavily.com/research/{request_id}"
CACHE_DIR = pathlib.Path.home() / ".openclaw" / "cache" / "tavily" / "research"
LOG_FILE = pathlib.Path.home() / ".openclaw" / "logs" / "tavily_research.log"
MAX_RETRIES = 3
RETRY_DELAY = 5.0
CACHE_TTL = 86400  # 24 hours (research is very expensive)

# Strong warning about cost
COST_WARNING = """
⚠️  ⚠️  ⚠️  EXTREME COST WARNING  ⚠️  ⚠️  ⚠️

   Tavily Research API is VERY EXPENSIVE!
   
   Cost per research task:
   - model=mini:  4-110 credits
   - model=pro:   15-250 credits
   
   Free tier (1000 credits/month) = 
   - mini:  9-250 research tasks
   - pro:   4-66 research tasks
   
   This API is DISABLED by default.
   You MUST use --enable AND --confirm to proceed.
   
   Consider using Search API instead for most use cases.
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
# Tavily Research API
# ============================================================================

def tavily_research(params: Dict[str, Any]) -> Dict:
    """Start research task using Tavily Research API"""
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
            query = str(params.get("query", ""))[:50]
            log(f"Request attempt {attempt}/{MAX_RETRIES}: {query}...", "DEBUG")
            
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                TAVILY_URL,
                data=data,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method="POST",
            )

            # Research can take a long time
            timeout = params.get("timeout", 300)
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

            log(f"Success: Research task completed", "INFO")
            return obj

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
    raise SystemExit(f"Tavily research failed after {MAX_RETRIES} attempts: {last_error}")


def get_research_status(request_id: str) -> Dict:
    """Get research task status"""
    key = load_key()
    if not key:
        log("Missing API key", "ERROR")
        raise SystemExit("Missing TAVILY_API_KEY")

    url = TAVILY_STATUS_URL.format(request_id=request_id)
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {key}",
                "Accept": "application/json",
            },
            method="GET",
        )

        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8", errors="replace")

        return json.loads(body)
    except Exception as e:
        log(f"Status check failed: {e}", "ERROR")
        raise


# ============================================================================
# Output Formatters
# ============================================================================

def to_markdown(obj: Dict) -> str:
    """Convert to human-readable Markdown"""
    lines = []
    
    # Title
    query = obj.get("query", "Research")
    lines.append(f"# Research Report")
    lines.append("")
    lines.append(f"**Query**: {query}")
    lines.append("")
    
    # Answer/Summary
    if "answer" in obj:
        lines.append("## Summary")
        lines.append("")
        lines.append(obj["answer"])
        lines.append("")
    
    # Full report
    if "report" in obj:
        lines.append("## Full Report")
        lines.append("")
        lines.append(obj["report"])
        lines.append("")
    
    # Sources
    if "sources" in obj:
        lines.append("## Sources")
        lines.append("")
        for i, source in enumerate(obj["sources"], 1):
            title = source.get("title", "Unknown")
            url = source.get("url", "")
            lines.append(f"{i}. [{title}]({url})")
        lines.append("")
    
    # Usage
    if "usage" in obj:
        lines.append("## Cost")
        lines.append("")
        usage = obj["usage"]
        credits = usage.get("credits", 0)
        lines.append(f"**Credits Used**: {credits}")
        lines.append("")
    
    return "\n".join(lines).strip() + "\n"


def to_compact_md(obj: Dict) -> str:
    """Convert to compact Markdown"""
    lines = []
    
    query = obj.get("query", "Research")
    lines.append(f"📚 Research: {query}")
    lines.append("")
    
    if "answer" in obj:
        lines.append(obj["answer"][:500] + ("..." if len(obj["answer"]) > 500 else ""))
        lines.append("")
    
    if "usage" in obj:
        credits = obj["usage"].get("credits", 0)
        lines.append(f"💰 Cost: {credits} credits")
    
    return "\n".join(lines).strip() + "\n"


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(
        description="Tavily Research - Deep research (VERY EXPENSIVE - disabled by default)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{COST_WARNING}
Examples:
  # Basic research (requires --enable AND --confirm)
  %(prog)s --query "AI impact on healthcare" --enable --confirm

  # Pro model (more expensive, better quality)
  %(prog)s --query "market analysis" --model pro --enable --confirm

  # Custom parameters
  %(prog)s --query "climate change" --max-sources 20 --enable --confirm
        """
    )
    
    # Required
    ap.add_argument(
        "--query",
        required=True,
        help="Research query/topic"
    )
    
    # Safety flags (BOTH required for this very expensive API)
    ap.add_argument(
        "--enable",
        action="store_true",
        help="REQUIRED: Enable research (acknowledges cost)"
    )
    ap.add_argument(
        "--confirm",
        action="store_true",
        help="REQUIRED: Confirm you understand the cost (type: yes)"
    )
    
    # Model selection
    ap.add_argument(
        "--model",
        default="mini",
        choices=["mini", "pro"],
        help="Research model: mini (4-110 credits) or pro (15-250 credits)"
    )
    
    # Research parameters
    ap.add_argument(
        "--max-sources",
        type=int,
        default=10,
        help="Maximum sources to analyze (default: 10)"
    )
    ap.add_argument(
        "--max-tokens",
        type=int,
        default=1000,
        help="Maximum tokens in report (default: 1000)"
    )
    
    # Timeout
    ap.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout in seconds (default: 300 = 5 min)"
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
        help="Output format: raw (JSON) | md (detailed) | compact (simple)"
    )
    ap.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching"
    )
    
    args = ap.parse_args()
    
    # Safety check - BOTH flags required
    if not args.enable or not args.confirm:
        print(COST_WARNING, file=sys.stderr)
        print("❌ Error: Research API is disabled by default due to EXTREME cost.", file=sys.stderr)
        print("   You MUST use BOTH --enable AND --confirm to proceed.", file=sys.stderr)
        print("", file=sys.stderr)
        print("   Example:", file=sys.stderr)
        print("   python3 research.py --query 'your topic' --enable --confirm", file=sys.stderr)
        sys.exit(1)
    
    # Build API parameters
    params = {
        "query": args.query,
        "model": args.model,
        "max_sources": args.max_sources,
        "max_tokens": args.max_tokens,
        "timeout": args.timeout,
    }
    
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
    
    # Perform research
    result = tavily_research(params)
    result["query"] = args.query
    
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
