#!/usr/bin/env python3
"""
Tavily Usage API - Check credit usage
Based on: https://docs.tavily.com/documentation/api-reference/endpoint/usage

Usage:
    python3 usage.py
    python3 usage.py --json
"""
import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request
from datetime import datetime
from typing import Optional, Dict, Any

# Constants
TAVILY_USAGE_URL = "https://api.tavily.com/usage"
LOG_FILE = pathlib.Path.home() / ".openclaw" / "logs" / "tavily_usage.log"


# ============================================================================
# Logging
# ============================================================================

def log(message: str, level: str = "INFO"):
    """Simple logging"""
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
# Tavily Usage API
# ============================================================================

def get_usage() -> Optional[Dict[str, Any]]:
    """
    Get Tavily API usage information
    
    Returns:
        Usage dict or None
    """
    key = load_key()
    if not key:
        log("Missing API key", "ERROR")
        return None
    
    try:
        req = urllib.request.Request(
            TAVILY_USAGE_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "Accept": "application/json",
            },
            method="GET",
        )
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        
        data = json.loads(body)
        log("Usage retrieved successfully", "INFO")
        return data
        
    except urllib.error.HTTPError as e:
        log(f"HTTP error: {e.code} - {e.reason}", "ERROR")
        return None
    except Exception as e:
        log(f"Error: {e}", "ERROR")
        return None


def format_usage(usage: Dict[str, Any], json_output: bool = False) -> str:
    """Format usage information"""
    if json_output:
        return json.dumps(usage, indent=2, ensure_ascii=False)
    
    lines = []
    lines.append("📊 Tavily API Usage")
    lines.append("=" * 50)
    
    # Account info
    if "account" in usage:
        account = usage["account"]
        lines.append(f"\nPlan: {account.get('current_plan', 'Unknown')}")
        
        if "plan_limit" in account:
            lines.append(f"Monthly Limit: {account['plan_limit']:,} credits")
        
        if "plan_usage" in account:
            lines.append(f"Used This Month: {account['plan_usage']:,} credits")
        
        if "plan_limit" in account and "plan_usage" in account:
            remaining = account["plan_limit"] - account["plan_usage"]
            lines.append(f"Remaining: {remaining:,} credits")
            
            # Percentage
            pct_used = (account["plan_usage"] / account["plan_limit"] * 100) if account["plan_limit"] > 0 else 0
            lines.append(f"Usage: {pct_used:.1f}%")
            
            # Warning
            if remaining < 100:
                lines.append(f"\n⚠️  WARNING: Low credits! ({remaining} remaining)")
            elif remaining < 300:
                lines.append(f"\n⚠️  Caution: Moderate credits ({remaining} remaining)")
            else:
                lines.append(f"\n✅ Good credit balance ({remaining} remaining)")
    
    # Breakdown by API
    lines.append("\nUsage by API:")
    if "account" in usage:
        account = usage["account"]
        if "search_usage" in account:
            lines.append(f"  - Search: {account['search_usage']:,} credits")
        if "extract_usage" in account:
            lines.append(f"  - Extract: {account['extract_usage']:,} credits")
        if "crawl_usage" in account:
            lines.append(f"  - Crawl: {account['crawl_usage']:,} credits")
        if "map_usage" in account:
            lines.append(f"  - Map: {account['map_usage']:,} credits")
        if "research_usage" in account:
            lines.append(f"  - Research: {account['research_usage']:,} credits")
    
    # Key-level usage (if available)
    if "key" in usage:
        key_usage = usage["key"]
        lines.append("\nKey-level Usage:")
        if "usage" in key_usage:
            lines.append(f"  Total: {key_usage['usage']:,} credits")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(description="Tavily Usage - Check API credit usage")
    ap.add_argument("--json", action="store_true", help="JSON output")
    
    args = ap.parse_args()
    
    # Get usage
    usage = get_usage()
    
    if not usage:
        print("❌ Failed to retrieve usage information", file=sys.stderr)
        sys.exit(1)
    
    # Output
    print(format_usage(usage, json_output=args.json))


if __name__ == "__main__":
    main()
