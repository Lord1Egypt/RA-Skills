#!/usr/bin/env python3
"""
Tavily Web Search - Auto Update Script
Checks for API changes from official documentation and updates local skill.

Usage:
    python3 scripts/update.py [--check-only] [--force]

Schedule (recommended):
    Weekly cron job to check for updates
"""
import hashlib
import json
import os
import pathlib
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime

# Configuration
DOCS_BASE = "https://docs.tavily.com"
CHANGELOG_URL = f"{DOCS_BASE}/changelog.md"
SEARCH_API_URL = f"{DOCS_BASE}/documentation/api-reference/endpoint/search.md"
LLMS_TXT_URL = f"{DOCS_BASE}/llms.txt"
SKILL_DIR = pathlib.Path(__file__).parent.parent
VERSION_FILE = SKILL_DIR / "_meta.json"
UPDATE_LOG = SKILL_DIR / "update.log"
LAST_CHECK_FILE = SKILL_DIR / ".last_check"

# Parameters to track (from official API)
OFFICIAL_PARAMS = {
    # Search API
    "search": {
        "query": {"type": "string", "required": True},
        "search_depth": {"type": "string", "enum": ["basic", "advanced", "fast", "ultra-fast"], "default": "basic"},
        "max_results": {"type": "integer", "min": 0, "max": 20, "default": 5},
        "topic": {"type": "string", "enum": ["general", "news", "finance"], "default": "general"},
        "time_range": {"type": "string", "enum": ["day", "week", "month", "year", "d", "w", "m", "y"]},
        "start_date": {"type": "string", "format": "YYYY-MM-DD"},
        "end_date": {"type": "string", "format": "YYYY-MM-DD"},
        "include_answer": {"type": "boolean|string", "enum": [True, False, "basic", "advanced"], "default": False},
        "include_raw_content": {"type": "boolean|string", "enum": [True, False, "markdown", "text"], "default": False},
        "include_images": {"type": "boolean", "default": False},
        "include_image_descriptions": {"type": "boolean", "default": False},
        "include_favicon": {"type": "boolean", "default": False},
        "include_domains": {"type": "array", "max_items": 300},
        "exclude_domains": {"type": "array", "max_items": 150},
        "country": {"type": "string", "enum_count": 100},
        "auto_parameters": {"type": "boolean", "default": False},
        "exact_match": {"type": "boolean", "default": False},
        "chunks_per_source": {"type": "integer", "min": 1, "max": 3, "default": 3},
        "include_usage": {"type": "boolean", "default": False},
    },
    # Extract API
    "extract": {
        "urls": {"type": "string|array", "required": True},
        "query": {"type": "string"},
        "chunks_per_source": {"type": "integer", "min": 1, "max": 5, "default": 3},
        "extract_depth": {"type": "string", "enum": ["basic", "advanced"], "default": "basic"},
        "include_images": {"type": "boolean", "default": False},
        "include_favicon": {"type": "boolean", "default": False},
        "format": {"type": "string", "enum": ["markdown", "text"], "default": "markdown"},
        "timeout": {"type": "number", "min": 1, "max": 60},
        "include_usage": {"type": "boolean", "default": False},
    },
    # Crawl API
    "crawl": {
        "url": {"type": "string", "required": True},
        "instructions": {"type": "string"},
        "chunks_per_source": {"type": "integer", "min": 1, "max": 5, "default": 3},
        "max_depth": {"type": "integer", "default": 1},
        "max_breadth": {"type": "integer", "default": 20},
        "limit": {"type": "integer", "default": 50},
        "extract_depth": {"type": "string", "enum": ["basic", "advanced"], "default": "basic"},
        "format": {"type": "string", "enum": ["markdown", "text"], "default": "markdown"},
        "timeout": {"type": "number", "min": 10, "max": 150, "default": 150},
        "select_paths": {"type": "array"},
        "select_domains": {"type": "array"},
        "exclude_paths": {"type": "array"},
        "exclude_domains": {"type": "array"},
        "include_images": {"type": "boolean", "default": False},
        "include_favicon": {"type": "boolean", "default": False},
        "include_usage": {"type": "boolean", "default": False},
    },
    # Map API
    "map": {
        "url": {"type": "string", "required": True},
        "instructions": {"type": "string"},
        "max_depth": {"type": "integer", "default": 1},
        "max_breadth": {"type": "integer", "default": 20},
        "limit": {"type": "integer", "default": 50},
        "timeout": {"type": "number", "min": 10, "max": 150, "default": 60},
        "select_paths": {"type": "array"},
        "select_domains": {"type": "array"},
        "exclude_paths": {"type": "array"},
        "exclude_domains": {"type": "array"},
        "allow_external": {"type": "boolean", "default": True},
        "include_images": {"type": "boolean", "default": False},
        "include_favicon": {"type": "boolean", "default": False},
        "include_usage": {"type": "boolean", "default": False},
    },
    # Research API
    "research": {
        "query": {"type": "string", "required": True},
        "model": {"type": "string", "enum": ["mini", "pro"], "default": "mini"},
        "max_sources": {"type": "integer", "default": 10},
        "max_tokens": {"type": "integer", "default": 1000},
        "timeout": {"type": "number", "default": 300},
        "include_usage": {"type": "boolean", "default": False},
    },
}


def log(message: str, level: str = "INFO"):
    """Log to file and stdout"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}\n"
    print(log_line.strip())
    try:
        with open(UPDATE_LOG, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass


def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch URL content"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TavilySkill/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        log(f"Failed to fetch {url}: {e}", "ERROR")
        return ""


def get_current_version() -> str:
    """Get current skill version"""
    if VERSION_FILE.exists():
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("version", "0.0.0")
    return "0.0.0"


def save_version(version: str):
    """Save new version"""
    data = {
        "ownerId": "system",
        "slug": "tavily-web-search",
        "version": version,
        "publishedAt": int(datetime.now().timestamp() * 1000)
    }
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def parse_changelog(content: str) -> list:
    """Parse changelog and extract recent updates"""
    updates = []
    
    # Extract accordion titles and dates
    pattern = r'Accordion.*?title="([^"]+)".*?description="([^"]+)"'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for title, date in matches:
        updates.append({
            "title": title.strip(),
            "date": date.strip(),
            "month": date.split()[0] if date else ""
        })
    
    return updates[:10]  # Last 10 updates


def check_api_params(content: str) -> dict:
    """Check for new/changed API parameters"""
    changes = {
        "new_params": [],
        "updated_params": [],
        "deprecated_params": []
    }
    
    # Look for parameter definitions in documentation
    param_pattern = r'`(\w+)`.*?(?:type|Type):\s*`?(\w+)`?'
    matches = re.findall(param_pattern, content)
    
    found_params = set()
    for param_name, param_type in matches:
        found_params.add(param_name)
        
        if param_name not in OFFICIAL_PARAMS:
            changes["new_params"].append({
                "name": param_name,
                "type": param_type
            })
            log(f"New parameter detected: {param_name} ({param_type})", "WARN")
    
    return changes


def get_latest_changes() -> dict:
    """Fetch and parse latest changes from Tavily"""
    log("Fetching changelog from Tavily...")
    changelog = fetch_url(CHANGELOG_URL)
    
    if not changelog:
        log("Failed to fetch changelog", "ERROR")
        return {"error": "Failed to fetch changelog"}
    
    updates = parse_changelog(changelog)
    
    log(f"Found {len(updates)} recent updates")
    
    return {
        "updates": updates,
        "fetched_at": datetime.now().isoformat()
    }


def check_for_updates() -> dict:
    """Check if updates are available"""
    log("Checking for Tavily API updates...")
    
    # Get last check time
    last_check = None
    if LAST_CHECK_FILE.exists():
        with open(LAST_CHECK_FILE, "r", encoding="utf-8") as f:
            last_check = json.load(f)
    
    # Fetch latest changes
    changes = get_latest_changes()
    
    if "error" in changes:
        return changes
    
    # Check if any updates since last check
    new_updates = []
    if last_check and "updates" in last_check:
        last_dates = {u["title"] for u in last_check.get("updates", [])}
        new_updates = [u for u in changes["updates"] if u["title"] not in last_dates]
    else:
        new_updates = changes["updates"]
    
    result = {
        "has_updates": len(new_updates) > 0,
        "new_updates": new_updates,
        "total_updates": len(changes["updates"]),
        "checked_at": datetime.now().isoformat()
    }
    
    # Save check result
    with open(LAST_CHECK_FILE, "w", encoding="utf-8") as f:
        json.dump(changes, f, indent=2)
    
    return result


def update_skill(force: bool = False) -> bool:
    """Update skill if needed"""
    log("Checking if skill update is needed...")
    
    check_result = check_for_updates()
    
    if not check_result.get("has_updates") and not force:
        log("No updates needed")
        return False
    
    log(f"Found {len(check_result.get('new_updates', []))} new updates")
    
    # Fetch search API documentation
    search_doc = fetch_url(SEARCH_API_URL)
    
    if search_doc:
        param_changes = check_api_params(search_doc)
        
        if param_changes["new_params"]:
            log(f"⚠️  New API parameters detected: {[p['name'] for p in param_changes['new_params']]}")
            log("📝 Manual update recommended - review scripts/search.py")
        else:
            log("✅ No API parameter changes detected")
    
    # Update version
    current_version = get_current_version()
    parts = current_version.split(".")
    try:
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0
    except (ValueError, IndexError):
        major, minor, patch = 1, 0, 0
    
    # Bump patch version
    new_version = f"{major}.{minor}.{patch + 1}"
    save_version(new_version)
    
    log(f"✅ Version updated: {current_version} → {new_version}")
    
    # Print update summary
    print("\n" + "="*60)
    print("📋 UPDATE SUMMARY")
    print("="*60)
    for update in check_result.get("new_updates", [])[:5]:
        print(f"  • {update['title']} ({update['date']})")
    print("="*60)
    
    return True


def show_status():
    """Show current status"""
    print("\n" + "="*60)
    print("📊 TAVILY WEB SEARCH - UPDATE STATUS")
    print("="*60)
    print(f"  Version: {get_current_version()}")
    print(f"  Skill Dir: {SKILL_DIR}")
    
    if LAST_CHECK_FILE.exists():
        with open(LAST_CHECK_FILE, "r", encoding="utf-8") as f:
            last_check = json.load(f)
            print(f"  Last Check: {last_check.get('fetched_at', 'Never')}")
            print(f"  Known Updates: {len(last_check.get('updates', []))}")
    
    if UPDATE_LOG.exists():
        print(f"  Update Log: {UPDATE_LOG}")
    
    print("="*60)


def main():
    import argparse
    
    ap = argparse.ArgumentParser(description="Tavily Web Search - Auto Update")
    ap.add_argument("--check-only", action="store_true", help="Only check for updates, don't apply")
    ap.add_argument("--force", action="store_true", help="Force update even if no changes")
    ap.add_argument("--status", action="store_true", help="Show current status")
    args = ap.parse_args()
    
    if args.status:
        show_status()
        return
    
    if args.check_only:
        result = check_for_updates()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    # Perform update
    success = update_skill(force=args.force)
    
    if success:
        log("✅ Update completed")
        sys.exit(0)
    else:
        log("ℹ️  No updates applied")
        sys.exit(0)


if __name__ == "__main__":
    main()
