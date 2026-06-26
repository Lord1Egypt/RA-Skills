#!/usr/bin/env python3
"""
Estimate token and time costs for a skill execution.
Usage: calculate_cost.py <skill_name> [--task "description"]
"""

import argparse
import json
import os
from typing import Dict, Any

# Historical data file
HISTORY_FILE = os.path.expanduser("~/.openclaw/workspace/skill-router-history.json")

# Base estimates for different skill types
BASE_ESTIMATES = {
    "doc": {"tokens": 2000, "time": 5, "description": "Document processing"},
    "api": {"tokens": 1500, "time": 3, "description": "API calls"},
    "search": {"tokens": 1000, "time": 2, "description": "Search operations"},
    "analysis": {"tokens": 3000, "time": 8, "description": "Data analysis"},
    "default": {"tokens": 2000, "time": 5, "description": "General task"}
}


def load_history() -> Dict[str, Any]:
    """Load historical usage data."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_history(history: Dict[str, Any]):
    """Save historical usage data."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def categorize_skill(skill_name: str) -> str:
    """Categorize skill by name patterns."""
    name_lower = skill_name.lower()
    
    if any(x in name_lower for x in ["doc", "pdf", "word", "document"]):
        return "doc"
    elif any(x in name_lower for x in ["api", "http", "request", "webhook"]):
        return "api"
    elif any(x in name_lower for x in ["search", "find", "query"]):
        return "search"
    elif any(x in name_lower for x in ["analyze", "analysis", "stats", "report"]):
        return "analysis"
    else:
        return "default"


def estimate_cost(skill_name: str, task_description: str = "") -> Dict[str, Any]:
    """Estimate token and time costs."""
    history = load_history()
    category = categorize_skill(skill_name)
    
    # Start with base estimate
    base = BASE_ESTIMATES.get(category, BASE_ESTIMATES["default"]).copy()
    
    # Adjust based on task complexity
    if task_description:
        complexity = analyze_complexity(task_description)
        base["tokens"] = int(base["tokens"] * complexity["token_multiplier"])
        base["time"] = int(base["time"] * complexity["time_multiplier"])
        base["complexity"] = complexity["level"]
    
    # Check historical data for this skill
    if skill_name in history:
        hist = history[skill_name]
        runs = hist.get("runs", 0)
        if runs > 0:
            # Blend historical average with base estimate
            avg_tokens = hist.get("total_tokens", 0) / runs
            avg_time = hist.get("total_time", 0) / runs
            
            # Weight: 70% historical, 30% base (if we have history)
            base["tokens"] = int(0.7 * avg_tokens + 0.3 * base["tokens"])
            base["time"] = int(0.7 * avg_time + 0.3 * base["time"])
            base["historical_runs"] = runs
    
    # Calculate cost (placeholder rates)
    input_rate = 0.0015  # per 1K tokens
    output_rate = 0.002  # per 1K tokens
    
    # Assume 60% input, 40% output
    input_tokens = base["tokens"] * 0.6
    output_tokens = base["tokens"] * 0.4
    
    estimated_cost = (input_tokens / 1000 * input_rate) + (output_tokens / 1000 * output_rate)
    base["estimated_cost_usd"] = round(estimated_cost, 4)
    
    return {
        "skill_name": skill_name,
        "category": category,
        "estimated_tokens": base["tokens"],
        "estimated_time_seconds": base["time"],
        "estimated_cost_usd": base["estimated_cost_usd"],
        "confidence": "high" if skill_name in history else "medium"
    }


def analyze_complexity(task_description: str) -> Dict[str, Any]:
    """Analyze task complexity based on description."""
    desc_lower = task_description.lower()
    
    # Complexity indicators
    simple_indicators = ["simple", "basic", "quick", "small"]
    complex_indicators = ["complex", "detailed", "comprehensive", "large", "many", "multiple"]
    
    simple_count = sum(1 for i in simple_indicators if i in desc_lower)
    complex_count = sum(1 for i in complex_indicators if i in desc_lower)
    
    if complex_count > simple_count:
        return {"level": "high", "token_multiplier": 2.0, "time_multiplier": 2.5}
    elif simple_count > complex_count:
        return {"level": "low", "token_multiplier": 0.6, "time_multiplier": 0.5}
    else:
        return {"level": "medium", "token_multiplier": 1.0, "time_multiplier": 1.0}


def record_actual(skill_name: str, actual_tokens: int, actual_time: float):
    """Record actual usage for future estimates."""
    history = load_history()
    
    if skill_name not in history:
        history[skill_name] = {"runs": 0, "total_tokens": 0, "total_time": 0}
    
    history[skill_name]["runs"] += 1
    history[skill_name]["total_tokens"] += actual_tokens
    history[skill_name]["total_time"] += actual_time
    
    save_history(history)


def main():
    parser = argparse.ArgumentParser(description="Estimate skill execution costs")
    parser.add_argument("skill_name", help="Name of the skill")
    parser.add_argument("--task", help="Task description for complexity analysis")
    parser.add_argument("--record", action="store_true", help="Record actual usage")
    parser.add_argument("--tokens", type=int, help="Actual tokens (with --record)")
    parser.add_argument("--time", type=float, help="Actual time in seconds (with --record)")
    
    args = parser.parse_args()
    
    if args.record:
        if args.tokens is None or args.time is None:
            print("Error: --record requires --tokens and --time")
            return
        record_actual(args.skill_name, args.tokens, args.time)
        print(json.dumps({"status": "recorded", "skill": args.skill_name}, indent=2))
    else:
        estimate = estimate_cost(args.skill_name, args.task or "")
        print(json.dumps(estimate, indent=2))


if __name__ == "__main__":
    main()
