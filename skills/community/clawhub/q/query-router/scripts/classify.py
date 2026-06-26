#!/usr/bin/env python3
"""
Query Router Classifier - Merged approach
Combines:
  1. Content-type detection (vision, voice, tool, code, reasoning, qa)
  2. Complexity scoring (simple, moderate, complex)
  3. Prefix routing (@codex, @mini, @c, @m, @q, @cl)
"""

import sys
import json
import re
from pathlib import Path

# ─── Query Types (content-type detection) ───────────────────────────────────
QUERY_TYPES = {
    "vision": {
        "keywords": ["describe", "what's in", "what is in", "see", "image", "photo", "picture", "screenshot", "identify", "recognize", "vision"],
        "file_exts": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".heic"],
        "indicators": ["attached", "this image", "this photo", "this picture", "show me", "look at"],
    },
    "voice": {
        "keywords": ["transcribe", "speech to text", "voice to text", "voice message", "audio", "recording"],
        "file_exts": [".ogg", ".mp3", ".wav", ".m4a", ".flac", ".aac", ".opus"],
        "indicators": ["voice message", "audio file", "this recording", "speech-to-text"],
    },
    "tool": {
        "keywords": ["run", "execute", "check", "fetch", "send", "create", "delete", "update", "list", "show", "status", "monitor", "sync", "backup", "cron", "schedule", "install", "start", "stop", "restart"],
        "patterns": [r"^!/", r"^/[\w]+", r"openclaw", r"run.*script", r"execute.*command"],
        "indicators": ["run this", "execute", "trigger", "automate"],
    },
    "code": {
        "keywords": ["write code", "script", "debug", "function", "class", "import", "api", "endpoint", "database", "sql", "python", "javascript", "bash", "typescript", "java", "c++", "rust", "golang", "php", "ruby", "debug", "refactor", "optimize", "code review"],
        "patterns": [r"def\s+\w+", r"class\s+\w+", r"import\s+\w+", r"function\s*\(", r"=>\s*{", r"\$\w+\s*=", r"func\s+\w+", r"fn\s+\w+", r"pub\s+fn", r"async\s+fn"],
        "indicators": ["write a script", "create a function", "debug this", "fix the code", "code review"],
    },
    "reasoning": {
        "keywords": ["analyze", "compare", "evaluate", "plan", "think through", "strategy", "research", "investigate", "break down", "assess", "review", "examine", "deep dive"],
        "indicators": ["step by step", "pros and cons", "advantages and disadvantages", "how would you", "what if", "think about"],
    },
    "qa": {
        "keywords": ["what is", "what are", "how do", "how does", "when did", "where is", "who is", "define", "explain", "meaning of", "tell me about", "what does"],
        "indicators": ["factual", "definition", "information"],
    },
}

# ─── Complexity Tiers ───────────────────────────────────────────────────────
COMPLEXITY_TIERS = {
    "simple": {
        "patterns": [
            r"^(hi|hello|hey|thanks|thank you|ok|okay|yes|no|cancel|stop|help)$",
            r"^what time is it",
            r"^how are you",
            r"^(good)?morning|^(good)?evening|^(good)?afternoon",
            r"^bye$",
        ],
        "indicators": ["greeting", "confirmation", "one-liner"],
    },
    "moderate": {
        "patterns": [
            r"write.*(email|letter|message|report|summary|note)",
            r"analyze|compare|evaluate",
            r"search|find.*info|look up",
            r"calculate|compute",
            r"translate",
            r"recommend|suggest",
            r"plan.*(trip|event|day|week)",
        ],
        "indicators": ["multi-step", "requires retrieval", "moderate reasoning"],
    },
    "complex": {
        "patterns": [
            r"debug.*(complex|entire|whole).*codebase",
            r"write.*(chapter|novel|book|thesis|dissertation)",
            r"architect|design.*system",
            r"research.*(deep|thorough|comprehensive)",
            r"analyze.*(data|dataset|metrics).*from.*to",
            r"build.*(from scratch|entire|full)",
        ],
        "indicators": ["multi-file", "hours of work", "deep reasoning", "large context"],
    },
}

# ─── Prefix Routing ─────────────────────────────────────────────────────────
PREFIX_MAP = {
    "@codex": {"model": "openai-codex/gpt-5.3-codex", "aliases": ["@c"]},
    "@mini":  {"model": "minimax/MiniMax-M2.5",        "aliases": ["@m"]},
    "@cl":      {"model": "qwen3-coder-next:cloud",   "aliases": []},
    "@q":      {"model": "minimax-m2.7:cloud",         "aliases": []},
    "@llava":  {"model": "qwen3.5:cloud",              "aliases": ["@qwen", "@qv"]},
    "@whisper": {"model": "whisper",                  "aliases": []},
}

# Reverse alias lookup
ALIAS_TO_PREFIX = {}
for prefix, config in PREFIX_MAP.items():
    for alias in config.get("aliases", []):
        ALIAS_TO_PREFIX[alias] = prefix
    ALIAS_TO_PREFIX[prefix] = prefix  # include canonical form

# ─── Model Routing (cloud primary, local fallback) ──────────────────────────────
MODEL_ROUTING = {
    "vision":    "qwen3.5:cloud",                   # cloud vision multimodal
    "voice":     "whisper",                     # local transcription
    "tool":      "minimax-m2.7:cloud",          # cloud — tool use
    "code":      "qwen3-coder-next:cloud",           # cloud code model
    "reasoning": "minimax-m2.7:cloud",          # cloud — reasoning
    "qa":        "minimax-m2.7:cloud",            # cloud fast Q&A
    "default":   "minimax-m2.7:cloud",          # cloud default
}

COMPLEXITY_MODEL = {
    "simple":   "minimax-m2.7:cloud",            # cloud fast
    "moderate": "minimax-m2.7:cloud",   # cloud
    "complex":  "minimax-m2.7:cloud",   # cloud
}

# ─── Available models cache ─────────────────────────────────────────────────
_AVAILABLE_MODELS = None


def check_available_models():
    global _AVAILABLE_MODELS
    if _AVAILABLE_MODELS is not None:
        return _AVAILABLE_MODELS
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            _AVAILABLE_MODELS = [m["name"] for m in data.get("models", [])]
    except Exception:
        _AVAILABLE_MODELS = []
    return _AVAILABLE_MODELS


# ─── Classification Logic ────────────────────────────────────────────────────
def detect_prefix(query: str) -> tuple:
    """Check for prefix routing. Returns (prefix_used, model, stripped_query)."""
    query_stripped = query.strip()
    for alias, prefix in ALIAS_TO_PREFIX.items():
        if query_stripped.startswith(alias):
            model = PREFIX_MAP[prefix]["model"]
            clean_query = query_stripped[len(alias):].strip()
            return prefix, model, clean_query
    return None, None, query


def score_content_type(query: str, has_attachment: bool = False, attachment_ext: str = "") -> dict:
    """Score each content type. Returns dict of type -> score."""
    query_lower = query.lower().strip()
    scores = {qtype: 0.0 for qtype in QUERY_TYPES}
    
    # Attachment is strong signal
    if has_attachment and attachment_ext:
        ext = attachment_ext.lower()
        for qtype, config in QUERY_TYPES.items():
            if ext in config.get("file_exts", []):
                scores[qtype] += 0.9
                break
    
    # Keyword, pattern, indicator matching
    for qtype, config in QUERY_TYPES.items():
        for kw in config.get("keywords", []):
            if kw.lower() in query_lower:
                scores[qtype] += 0.3
        
        for pattern in config.get("patterns", []):
            if re.search(pattern, query, re.IGNORECASE):
                scores[qtype] += 0.4
        
        for indicator in config.get("indicators", []):
            if indicator.lower() in query_lower:
                scores[qtype] += 0.5
    
    # Normalize
    max_score = max(scores.values()) if any(scores.values()) else 1.0
    return {k: v / max_score for k, v in scores.items()}


def score_complexity(query: str) -> dict:
    """Score complexity tiers. Returns dict of tier -> score."""
    query_lower = query.lower().strip()
    scores = {tier: 0.0 for tier in COMPLEXITY_TIERS}
    
    for tier, config in COMPLEXITY_TIERS.items():
        for pattern in config.get("patterns", []):
            if re.search(pattern, query_lower, re.IGNORECASE):
                scores[tier] += 0.5
        
        for indicator in config.get("indicators", []):
            if indicator in query_lower:
                scores[tier] += 0.3
    
    # Length heuristic
    word_count = len(query.split())
    if word_count <= 5:
        scores["simple"] += 0.3
    elif word_count <= 30:
        scores["moderate"] += 0.3
    else:
        scores["complex"] += 0.3
    
    max_score = max(scores.values()) if any(scores.values()) else 1.0
    return {k: v / max_score for k, v in scores.items()}


def classify(query: str, has_attachment: bool = False, attachment_ext: str = "") -> dict:
    """
    Full classification merging content-type + complexity + prefix.
    Returns complete routing decision.
    """
    # 1. Check prefix first (explicit user intent)
    prefix_used, prefix_model, clean_query = detect_prefix(query)
    
    # 2. Content type scoring (on clean query)
    content_scores = score_content_type(clean_query, has_attachment, attachment_ext)
    primary_type = max(content_scores, key=content_scores.get)
    type_confidence = content_scores[primary_type] if content_scores[primary_type] > 0 else 0.1
    
    # 3. Complexity scoring
    complexity_scores = score_complexity(clean_query)
    primary_complexity = max(complexity_scores, key=complexity_scores.get)
    complexity_conf = complexity_scores[primary_complexity]
    
    # 4. Determine final model
    if prefix_model:
        final_model = prefix_model
        routing_reason = f"prefix: {prefix_used}"
    elif type_confidence >= 0.6:
        final_model = MODEL_ROUTING.get(primary_type, MODEL_ROUTING["default"])
        routing_reason = f"content-type: {primary_type} ({type_confidence:.0%})"
    else:
        final_model = COMPLEXITY_MODEL.get(primary_complexity, MODEL_ROUTING["default"])
        routing_reason = f"complexity: {primary_complexity} ({complexity_conf:.0%})"
    
    return {
        "prefix_used": prefix_used,
        "prefix_model": prefix_model,
        "content_type": primary_type,
        "content_scores": {k: round(v, 2) for k, v in content_scores.items()},
        "type_confidence": round(type_confidence, 2),
        "complexity": primary_complexity,
        "complexity_scores": {k: round(v, 2) for k, v in complexity_scores.items()},
        "complexity_confidence": round(complexity_conf, 2),
        "recommended_model": final_model,
        "routing_reason": routing_reason,
        "clean_query": clean_query,
    }


def format_output(result: dict, as_json: bool = False) -> str:
    if as_json:
        return json.dumps(result, indent=2)
    
    prefix_info = f" (prefix: {result['prefix_used']} → {result['prefix_model']})" if result["prefix_used"] else ""
    
    lines = [
        f"🎯 Content Type : {result['content_type'].upper()}  (confidence: {result['type_confidence']:.0%})",
        f"⚡ Complexity    : {result['complexity'].upper()}   (confidence: {result['complexity_confidence']:.0%}){prefix_info}",
        f"🤖 Model        : {result['recommended_model']}",
        f"📝 Reason       : {result['routing_reason']}",
        "",
        "   Content scores:",
    ]
    
    for qtype, score in sorted(result["content_scores"].items(), key=lambda x: -x[1]):
        bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        marker = "→" if qtype == result["content_type"] else " "
        lines.append(f"     {marker} {qtype:12} {bar} {score:.0%}")
    
    lines.append("")
    lines.append("   Complexity scores:")
    for tier, score in sorted(result["complexity_scores"].items(), key=lambda x: -x[1]):
        bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        marker = "→" if tier == result["complexity"] else " "
        lines.append(f"     {marker} {tier:12} {bar} {score:.0%}")
    
    return "\n".join(lines)


def main():
    has_attachment = False
    attachment_ext = ""
    query = ""
    as_json = False
    
    args = sys.argv[1:]
    if "--json" in args:
        as_json = True
        args.remove("--json")
    
    if "--attachment" in args:
        idx = args.index("--attachment")
        if idx + 1 < len(args):
            attachment_ext = args[idx + 1]
            has_attachment = True
            args.pop(idx)
            args.pop(idx)
    
    if args:
        query = " ".join(args)
    
    if not query:
        print("Usage: classify.py [--json] [--attachment .ext] <query>...")
        print("Example: classify.py --attachment .png describe this image")
        print("         classify.py @codex write a python script")
        print("         classify.py @mini analyze this data")
        sys.exit(1)
    
    result = classify(query, has_attachment, attachment_ext)
    print(format_output(result, as_json))


if __name__ == "__main__":
    main()
