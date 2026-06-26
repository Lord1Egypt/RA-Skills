#!/usr/bin/env python3
"""
Search clawhub for skills matching keywords.
Usage: search_clawhub.py <keywords> [--limit N]
"""

import argparse
import json
import subprocess
import sys
from typing import List, Dict, Any


def run_cmd(cmd: list) -> tuple:
    """Run a command and return (stdout, stderr, returncode)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


def search_clawhub(keywords: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search clawhub for skills."""
    stdout, stderr, rc = run_cmd(["clawhub", "search", keywords, "--json"])
    
    if rc != 0:
        # Try without --json flag
        stdout, stderr, rc = run_cmd(["clawhub", "search", keywords])
        if rc != 0:
            return [{"error": f"Search failed: {stderr}"}]
        
        # Parse text output (placeholder)
        return parse_text_output(stdout, limit)
    
    try:
        results = json.loads(stdout)
        return results[:limit]
    except json.JSONDecodeError:
        return [{"error": "Failed to parse search results"}]


def parse_text_output(output: str, limit: int) -> List[Dict[str, Any]]:
    """Parse text output from clawhub search."""
    results = []
    lines = output.strip().split("\n")
    
    for line in lines[:limit]:
        # Simple parsing - adjust based on actual clawhub output format
        if line.strip() and not line.startswith("-"):
            parts = line.split()
            if len(parts) >= 2:
                results.append({
                    "name": parts[0],
                    "description": " ".join(parts[1:]) if len(parts) > 1 else "",
                    "source": "clawhub"
                })
    
    return results


def get_skill_details(skill_name: str) -> Dict[str, Any]:
    """Get detailed info about a skill from clawhub."""
    stdout, stderr, rc = run_cmd(["clawhub", "info", skill_name, "--json"])
    
    if rc != 0:
        return {"error": f"Failed to get info: {stderr}"}
    
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"error": "Failed to parse skill info"}


def main():
    parser = argparse.ArgumentParser(description="Search clawhub for skills")
    parser.add_argument("keywords", help="Search keywords")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument("--details", action="store_true", help="Fetch full details")
    
    args = parser.parse_args()
    
    results = search_clawhub(args.keywords, args.limit)
    
    if args.details and results and "error" not in results[0]:
        detailed = []
        for skill in results:
            if "name" in skill:
                details = get_skill_details(skill["name"])
                skill.update(details)
            detailed.append(skill)
        results = detailed
    
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
