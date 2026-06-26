"""smart-router-coding v1.2.0

Routes coding queries to model tiers based on complexity.
Pure recommendation — returns model choice, agent calls LLM.

Usage:
    python3 scripts/smart_router_coding.py "your coding query"

Returns JSON: {"tier": "standard", "model": "DeepSeek V4 Flash", "cost": 0.0002, "reasoning": "..."}
"""
import json, re, sys
from typing import Dict

MODELS = {
    "fast": {"model": "DeepSeek V4 Flash", "cost": 0.0002, "latency": "2s"},
    "standard": {"model": "DeepSeek V4 Flash", "cost": 0.0002, "latency": "3s"},
    "deep": {"model": "Kimi K2.7 Code", "cost": 0.004, "latency": "8s"},
}

SIMPLE_KW = ["lint", "format", "boilerplate", "regex", "syntax", "indent", "comment",
             "rename", "one-liner", "find and replace", "print", "variable"]
MODERATE_KW = ["debug", "refactor", "implement", "write a function", "code review",
               "write tests", "unit test", "sql", "script", "fix", "class", "module"]
COMPLEX_KW = ["architecture", "system design", "security audit", "performance optimization",
              "complex algorithm", "concurrency", "multi-threaded", "distributed",
              "optimization", "critical"]

SIMPLE_PAT = [r"^what is", r"^how to print", r"^syntax for", r"^rename"]
MODERATE_PAT = [r"write a function", r"fix this code", r"debug this", r"implement",
                r"^review", r"write tests for"]
COMPLEX_PAT = [r"design a", r"architecture for", r"optimize", r"audit", r"secure"]

def route(query: str) -> Dict:
    q = query.lower()
    
    if any(kw in q for kw in COMPLEX_KW) or any(re.search(p, q) for p in COMPLEX_PAT):
        tier = "deep"
        reason = "Complex task — needs Kimi K2.7 Code"
    elif any(kw in q for kw in SIMPLE_KW) or any(re.search(p, q) for p in SIMPLE_PAT):
        tier = "fast"
        reason = "Simple task — use DeepSeek V4 Flash"
    else:
        tier = "standard"
        reason = "Standard coding task — use DeepSeek V4 Flash"
    
    m = MODELS[tier]
    return {"tier": tier, "model": m["model"], "cost_per_query": m["cost"],
            "latency": m["latency"], "reasoning": reason}

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "write a function"
    print(json.dumps(route(query), indent=2))