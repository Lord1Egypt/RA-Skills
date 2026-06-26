#!/usr/bin/env python3
"""
toolrouter-gateway — proxy to ToolRouter API with caching and usage tracking
"""

import json
import sys
import os
import time
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path.cwd()
MEMORY_DIR = WORKSPACE / "memory"
CONFIG_FILE = WORKSPACE / "toolrouter-gateway-config.json"
CACHE_FILE = MEMORY_DIR / "toolrouter-cache.jsonl"
USAGE_FILE = MEMORY_DIR / "toolrouter-usage.jsonl"

def load_config():
    default = {
        "api_url": "https://api.toolrouter.com/mcp",
        "cache_ttl_minutes": 1440,
        "enable_caching": True,
        "timeout_seconds": 60,
        "usage_log_file": str(USAGE_FILE)
    }
    if CONFIG_FILE.exists():
        try:
            user = json.loads(CONFIG_FILE.read_text())
            default.update(user)
        except:
            pass
    return default

def ensure_dirs():
    MEMORY_DIR.mkdir(exist_ok=True)

def get_api_key():
    api_key = os.environ.get("TOOLROUTER_API_KEY")
    if not api_key:
        return None
    return api_key

def fetch_catalog():
    """Fetch ToolRouter tool catalog via MCP or HTTP"""
    api_key = get_api_key()
    if not api_key:
        return {"error": "TOOLROUTER_API_KEY not set"}
    
    # In production, this would call ToolRouter's API or MCP server.
    # For demo, return mock catalog
    return {
        "tools": [
            {"slug": "competitor_research", "name": "Competitor Research", "description": "Generate competitor analysis report", "category": "research", "input_schema": {"type": "object", "properties": {"url": {"type": "string"}, "depth": {"type": "string"}}}},
            {"slug": "security_scan", "name": "Security Scan", "description": "Scan for vulnerabilities", "category": "security", "input_schema": {"type": "object", "properties": {"target": {"type": "string"}}}},
            {"slug": "video_from_brief", "name": "Video from Brief", "description": "Generate video from creative brief", "category": "video", "input_schema": {"type": "object", "properties": {"brief": {"type": "string"}, "style": {"type": "string"}}}}
        ]
    }

def toolrouter_discovery(query=None, category=None, limit=20):
    """Search the ToolRouter catalog"""
    catalog = fetch_catalog()
    if "error" in catalog:
        return catalog
    
    tools = catalog.get("tools", [])
    # Filter
    if query:
        q = query.lower()
        tools = [t for t in tools if q in t.get("name", "").lower() or q in t.get("description", "").lower()]
    if category:
        tools = [t for t in tools if t.get("category") == category]
    
    # Limit
    tools = tools[:limit]
    return {"tools": tools, "count": len(tools)}

def toolrouter_status():
    """Get gateway status"""
    ensure_dirs()
    api_key = get_api_key()
    if not api_key:
        return {"error": "TOOLROUTER_API_KEY not set"}
    
    # Count usage file lines
    total_calls = 0
    today_calls = 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    if USAGE_FILE.exists():
        with open(USAGE_FILE) as f:
            for line in f:
                total_calls += 1
                try:
                    entry = json.loads(line)
                    ts = entry.get("timestamp", "")
                    if ts.startswith(today_str):
                        today_calls += 1
                except:
                    continue
    
    # Cache age
    cache_age = None
    if CACHE_FILE.exists():
        cache_age_sec = time.time() - CACHE_FILE.stat().st_mtime
        cache_age = int(cache_age_sec / 60)
    
    # Test API connectivity (quick call)
    api_connected = True  # would do a ping
    
    return {
        "api_connected": api_connected,
        "api_key_set": True,
        "cache_age_minutes": cache_age,
        "total_calls": total_calls,
        "calls_today": today_calls,
        "enabled_tools": 0,  # from catalog
        "errors_last_24h": 0
    }

def toolrouter_proxy(tool, input_data):
    """Proxy a call to ToolRouter"""
    api_key = get_api_key()
    if not api_key:
        return {"error": "TOOLROUTER_API_KEY not set"}
    
    config = load_config()
    
    # Check cache
    if config["enable_caching"]:
        cache_key = hashlib.sha256(f"{tool}:{json.dumps(input_data, sort_keys=True)}".encode()).hexdigest()
        if CACHE_FILE.exists():
            with open(CACHE_FILE) as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if entry.get("cache_key") == cache_key:
                            # Check TTL
                            age_sec = time.time() - entry.get("timestamp_epoch", 0)
                            if age_sec < config["cache_ttl_minutes"] * 60:
                                return entry.get("result")
                    except:
                        continue
    
    # Make API call (simulate — in real impl would use MCP or HTTP)
    # For demo, return placeholder
    result = {"status": "ok", "tool": tool, "message": "ToolRouter call would happen here", "input": input_data}
    
    # Cache result
    if config["enable_caching"]:
        ensure_dirs()
        cache_entry = {
            "cache_key": cache_key,
            "tool": tool,
            "input": input_data,
            "result": result,
            "timestamp_epoch": time.time(),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        with open(CACHE_FILE, "a") as f:
            f.write(json.dumps(cache_entry) + "\n")
    
    # Log usage
    ensure_dirs()
    usage_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tool": tool,
        "input_hash": hashlib.sha256(json.dumps(input_data, sort_keys=True).encode()).hexdigest()[:16],
        "cached": False  # could be true if from cache
    }
    with open(USAGE_FILE, "a") as f:
        f.write(json.dumps(usage_entry) + "\n")
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: run.py [tool-call|discover|status] ...")
        sys.exit(1)
    
    action = sys.argv[1]
    args = sys.argv[2:]
    
    if action == "tool-call":
        if len(args) < 2:
            print(json.dumps({"error": "tool-call requires tool_name and json_input"}))
            sys.exit(1)
        tool = args[0]
        try:
            input_data = json.loads(args[1])
        except json.JSONDecodeError:
            print(json.dumps({"error": "invalid JSON input"}))
            sys.exit(1)
        
        if tool == "toolrouter_discovery":
            result = toolrouter_discovery(**input_data)
        elif tool == "toolrouter_status":
            result = toolrouter_status()
        elif tool == "toolrouter_proxy":
            # requires 'target_tool' inside input_data
            target_tool = input_data.pop("target_tool", None)
            if not target_tool:
                result = {"error": "target_tool required in input"}
            else:
                result = toolrouter_proxy(target_tool, input_data)
        else:
            result = {"error": f"unknown tool: {tool}"}
        
        print(json.dumps(result, indent=2))
        sys.exit(0 if "error" not in result else 1)
    
    elif action == "discover":
        # CLI convenience
        query = args[0] if args else None
        result = toolrouter_discovery(query=query)
        print(json.dumps(result, indent=2))
    
    elif action == "status":
        result = toolrouter_status()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
