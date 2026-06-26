#!/usr/bin/env python3
"""Benchmark: SCRY vs last30days head-to-head comparison."""

import json
import os
import subprocess
import sys
import time
from typing import Any, Dict, List

SCRY_SCRIPT = os.path.join(os.path.dirname(__file__), "scry.py")
LAST30_SCRIPT = os.path.expanduser("~/.claude/skills/last30days/scripts/last30days.py")


def run_tool(script: str, topic: str, extra_args: List[str] = None) -> Dict[str, Any]:
    """Run a research tool and capture results."""
    cmd = [sys.executable, script, topic, "--emit=json"]
    if extra_args:
        cmd.extend(extra_args)

    start = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=360
        )
        wall_time = time.time() - start
        if result.returncode != 0:
            return {"error": result.stderr[:500], "wall_time": wall_time, "items": []}
        data = json.loads(result.stdout)
        return {"data": data, "wall_time": wall_time, "items": data.get("items", [])}
    except subprocess.TimeoutExpired:
        return {"error": "Timeout (6 min)", "wall_time": 360, "items": []}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON output", "wall_time": time.time() - start, "items": []}
    except FileNotFoundError:
        return {"error": f"Script not found: {script}", "wall_time": 0, "items": []}


def extract_urls(items: List[Dict]) -> set:
    """Extract unique URLs from items."""
    urls = set()
    for item in items:
        url = item.get("url", "")
        if url:
            urls.add(url.rstrip("/").lower())
    return urls


def extract_sources(items: List[Dict]) -> List[str]:
    """Extract unique source IDs."""
    return list(set(item.get("source_id", item.get("source", "unknown")) for item in items))


def benchmark(topic: str, depth: str = "default") -> Dict[str, Any]:
    """Run both tools on same topic and compare."""
    print(f"\n{'='*60}")
    print(f"BENCHMARK: {topic}")
    print(f"{'='*60}\n")

    # Run SCRY
    print("[1/2] Running SCRY...")
    scry_args = []
    if depth == "quick":
        scry_args.append("--quick")
    elif depth == "deep":
        scry_args.append("--deep")
    scry = run_tool(SCRY_SCRIPT, topic, scry_args)

    # Run last30days
    print("[2/2] Running last30days...")
    l30_args = ["--no-native-web"]
    if depth == "quick":
        l30_args.append("--quick")
    elif depth == "deep":
        l30_args.append("--deep")
    last30 = run_tool(LAST30_SCRIPT, topic, l30_args)

    # Compare
    scry_urls = extract_urls(scry["items"])
    l30_urls = extract_urls(last30["items"])
    overlap = scry_urls & l30_urls
    scry_only = scry_urls - l30_urls
    l30_only = l30_urls - scry_urls

    scry_sources = extract_sources(scry["items"])
    l30_sources = extract_sources(last30["items"])

    # Score averages
    scry_scores = [i.get("score", 0) for i in scry["items"]]
    l30_scores = [i.get("score", 0) for i in last30["items"]]

    result = {
        "topic": topic,
        "depth": depth,
        "scry": {
            "wall_time_s": round(scry["wall_time"], 1),
            "total_items": len(scry["items"]),
            "unique_urls": len(scry_urls),
            "sources_used": scry_sources,
            "num_sources": len(scry_sources),
            "avg_score": round(sum(scry_scores) / max(len(scry_scores), 1), 1),
            "error": scry.get("error"),
        },
        "last30days": {
            "wall_time_s": round(last30["wall_time"], 1),
            "total_items": len(last30["items"]),
            "unique_urls": len(l30_urls),
            "sources_used": l30_sources,
            "num_sources": len(l30_sources),
            "avg_score": round(sum(l30_scores) / max(len(l30_scores), 1), 1),
            "error": last30.get("error"),
        },
        "comparison": {
            "url_overlap": len(overlap),
            "scry_only_urls": len(scry_only),
            "last30_only_urls": len(l30_only),
            "scry_extra_sources": sorted(set(scry_sources) - set(l30_sources)),
        },
    }

    # Display
    print(f"\n{'─'*60}")
    print(f"RESULTS: {topic}")
    print(f"{'─'*60}")
    print(f"{'Metric':<25} {'SCRY':>15} {'last30days':>15}")
    print(f"{'─'*55}")
    print(f"{'Wall time (s)':<25} {result['scry']['wall_time_s']:>15} {result['last30days']['wall_time_s']:>15}")
    print(f"{'Total items':<25} {result['scry']['total_items']:>15} {result['last30days']['total_items']:>15}")
    print(f"{'Unique URLs':<25} {result['scry']['unique_urls']:>15} {result['last30days']['unique_urls']:>15}")
    print(f"{'Sources used':<25} {result['scry']['num_sources']:>15} {result['last30days']['num_sources']:>15}")
    print(f"{'Avg score':<25} {result['scry']['avg_score']:>15} {result['last30days']['avg_score']:>15}")
    print(f"{'─'*55}")
    print(f"{'URL overlap':<25} {len(overlap):>15}")
    print(f"{'SCRY-only URLs':<25} {len(scry_only):>15}")
    print(f"{'last30-only URLs':<25} {len(l30_only):>15}")

    if result["comparison"]["scry_extra_sources"]:
        print(f"\nSCRY extra sources: {', '.join(result['comparison']['scry_extra_sources'])}")

    if scry.get("error"):
        print(f"\nSCRY error: {scry['error']}")
    if last30.get("error"):
        print(f"\nlast30days error: {last30['error']}")

    # Winner
    scry_score = 0
    l30_score = 0
    if result["scry"]["total_items"] > result["last30days"]["total_items"]:
        scry_score += 1
    else:
        l30_score += 1
    if result["scry"]["num_sources"] > result["last30days"]["num_sources"]:
        scry_score += 1
    else:
        l30_score += 1
    if result["scry"]["unique_urls"] > result["last30days"]["unique_urls"]:
        scry_score += 1
    else:
        l30_score += 1

    print(f"\n{'='*60}")
    if scry_score > l30_score:
        print(f"WINNER: SCRY ({scry_score}-{l30_score})")
    elif l30_score > scry_score:
        print(f"WINNER: last30days ({l30_score}-{scry_score})")
    else:
        print(f"TIE ({scry_score}-{l30_score})")
    print(f"{'='*60}\n")

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 benchmark.py <topic> [--quick|--deep] [--emit=json]")
        print("       python3 benchmark.py --batch=queries.txt")
        sys.exit(1)

    emit_json = "--emit=json" in sys.argv
    depth = "default"
    if "--quick" in sys.argv:
        depth = "quick"
    elif "--deep" in sys.argv:
        depth = "deep"

    # Batch mode
    batch_arg = next((a for a in sys.argv if a.startswith("--batch=")), None)
    if batch_arg:
        batch_file = batch_arg.split("=", 1)[1]
        with open(batch_file) as f:
            topics = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        results = [benchmark(topic, depth) for topic in topics]
        if emit_json:
            print(json.dumps(results, indent=2))
        return

    # Single topic
    topic_parts = [a for a in sys.argv[1:] if not a.startswith("--")]
    topic = " ".join(topic_parts)
    result = benchmark(topic, depth)
    if emit_json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
