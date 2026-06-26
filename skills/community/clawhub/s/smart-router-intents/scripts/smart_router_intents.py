"""smart-router-intents v1.1.0

Routes any query by intent. Returns model recommendation.
Pure classification — returns model choice, agent calls LLM.

Usage:
    python3 scripts/smart_router_intents.py "your query"

Returns JSON: {"intent": "code", "tier": "standard", "model": "DeepSeek V4 Flash", ...}
"""
import json, re, sys
from typing import Dict

CODE_KW = ["write code", "debug", "fix this", "refactor", "implement", "function",
           "class", "script", "api", "bug", "error", "compile", "test", ".py", ".js",
           ".ts", ".go", ".rs", ".java"]
ANALYSIS_KW = ["analyze", "explain", "compare", "research", "understand", "why does",
               "how does", "evaluate", "assess", "review", "investigate", "examine"]
CREATIVE_KW = ["write a story", "write a poem", "brainstorm", "imagine", "design",
               "draft", "compose", "creative"]
REALTIME_KW = ["now", "today", "current", "latest", "news", "trending", "price",
               "score", "weather", "@", "stock"]

CODE_PAT = [r"\.\w{2,4}$", r"^fix ", r"^debug ", r"^write a function"]
ANALYSIS_PAT = [r"^explain ", r"^compare ", r"^analyze ", r"^help me understand"]
CREATIVE_PAT = [r"write a (story|poem|song|script)", r"^brainstorm"]
REALTIME_PAT = [r"(news|price|weather|score).*(today|now|current)", r"^\$[A-Z]"]

def detect_intent(query: str) -> str:
    q = query.lower()
    scores = {"code": 0, "analysis": 0, "creative": 0, "realtime": 0}
    
    for kw in CODE_KW:
        if kw in q: scores["code"] += 1
    for kw in ANALYSIS_KW:
        if kw in q: scores["analysis"] += 1
    for kw in CREATIVE_KW:
        if kw in q: scores["creative"] += 1
    for kw in REALTIME_KW:
        if kw in q: scores["realtime"] += 1
    
    for p in CODE_PAT:
        if re.search(p, q): scores["code"] += 2
    for p in ANALYSIS_PAT:
        if re.search(p, q): scores["analysis"] += 2
    for p in CREATIVE_PAT:
        if re.search(p, q): scores["creative"] += 2
    for p in REALTIME_PAT:
        if re.search(p, q): scores["realtime"] += 2
    
    if max(scores.values()) == 0:
        return "general"
    
    # Realtime takes precedence (needs live data)
    if scores["realtime"] >= 2:
        return "realtime"
    
    return max(scores, key=scores.get)

TIER_MAP = {
    "code": {"tier": "standard", "model": "DeepSeek V4 Flash", "cost": 0.0002, "latency": "3s"},
    "analysis": {"tier": "standard", "model": "DeepSeek V4 Flash", "cost": 0.0002, "latency": "3s"},
    "creative": {"tier": "standard", "model": "DeepSeek V4 Flash", "cost": 0.0002, "latency": "3s"},
    "realtime": {"tier": "standard", "model": "DeepSeek V4 Flash", "cost": 0.0002, "latency": "3s"},
    "general": {"tier": "fast", "model": "DeepSeek V4 Flash", "cost": 0.0002, "latency": "2s"},
}

def route(query: str) -> Dict:
    intent = detect_intent(query)
    info = TIER_MAP[intent]
    return {
        "intent": intent,
        "tier": info["tier"],
        "model": info["model"],
        "cost_per_query": info["cost"],
        "latency": info["latency"],
        "reasoning": f"Intent detected: {intent} → {info['tier']} tier"
    }

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "what is the weather today"
    print(json.dumps(route(query), indent=2))