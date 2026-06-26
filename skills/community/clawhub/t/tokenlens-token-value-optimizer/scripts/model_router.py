#!/usr/bin/env python3
"""
TokenLens Model Router
Simple model recommendation based on prompt complexity.
"""

import re
import sys
from typing import Dict, List, Tuple

def analyze_prompt_complexity(prompt: str) -> Tuple[str, float, Dict]:
    """
    Analyze prompt complexity and recommend appropriate model tier.
    Returns (tier, confidence, details)
    """
    prompt_lower = prompt.lower()
    word_count = len(prompt_lower.split())
    
    # Simple detection patterns
    simple_patterns = [
        r"^hi\b", r"^hello\b", r"^hey\b", r"^thanks", r"^thank you",
        r"^ok\b", r"^yes\b", r"^no\b", r"^bye\b", r"^\?+$",
        r"^good morning", r"^good afternoon", r"^good evening",
        r"^how are you", r"^what's up",
    ]
    
    complex_patterns = [
        r"design", r"architecture", r"system", r"framework",
        r"analyze", r"analysis", r"evaluate", r"assessment",
        r"algorithm", r"complex", r"complicated", r"detailed",
        r"research", r"study", r"investigate", r"explain in depth",
        r"compare and contrast", r"pros and cons", r"advantages disadvantages",
    ]
    
    coding_patterns = [
        r"code\b", r"program\b", r"function\b", r"class\b", r"method\b",
        r"script\b", r"write.*code", r"implement", r"debug", r"fix.*bug",
        r"api\b", r"endpoint", r"database", r"query", r"sql\b",
        r"react", r"vue", r"angular", r"node", r"python", r"javascript",
        r"html", r"css", r"typescript", r"java\b", r"c\+\+", r"go\b",
        r"rust\b",
    ]
    
    # Check for simple patterns
    is_simple = False
    for pattern in simple_patterns:
        if re.search(pattern, prompt_lower):
            is_simple = True
            break
    
    # Check for complex patterns
    is_complex = False
    for pattern in complex_patterns:
        if re.search(pattern, prompt_lower):
            is_complex = True
            break
    
    # Check for coding patterns
    is_coding = False
    for pattern in coding_patterns:
        if re.search(pattern, prompt_lower):
            is_coding = True
            break
    
    # Determine tier
    if is_simple or word_count < 5:
        tier = "cheap"
        confidence = 0.9
        reasoning = "Simple greeting or short query"
    elif is_complex and not is_coding:
        tier = "powerful"
        confidence = 0.7
        reasoning = "Complex analysis or design task"
    elif is_coding:
        tier = "balanced"
        confidence = 0.8
        reasoning = "Coding task requiring good reasoning"
    elif word_count > 100:
        tier = "balanced"
        confidence = 0.6
        reasoning = "Long query requiring detailed response"
    else:
        tier = "balanced"
        confidence = 0.5
        reasoning = "Standard task"
    
    # Model mappings by provider
    model_mappings = {
        "cheap": {
            "anthropic": "claude-haiku-4",
            "openai": "gpt-4.1-nano",
            "google": "gemini-2.0-flash",
            "openrouter": "google/gemini-2.0-flash",
            "minimax": "MiniMax-M2.1-lightning",
        },
        "balanced": {
            "anthropic": "claude-sonnet-4-5",
            "openai": "gpt-4.5-preview",
            "google": "gemini-2.0-pro",
            "openrouter": "anthropic/claude-sonnet-4-5",
            "minimax": "MiniMax-M2.5",
        },
        "powerful": {
            "anthropic": "claude-opus-3-5",
            "openai": "gpt-4.5-preview",
            "google": "gemini-2.0-pro-exp",
            "openrouter": "anthropic/claude-opus-3-5",
            "minimax": "MiniMax-M2.7",
        }
    }
    
    # Cost savings estimate (rough percentages)
    cost_savings = {
        "cheap": 70,  # 70% cheaper than powerful
        "balanced": 30,  # 30% cheaper than powerful
        "powerful": 0,
    }
    
    details = {
        "word_count": word_count,
        "is_simple": is_simple,
        "is_complex": is_complex,
        "is_coding": is_coding,
        "tier_display": {
            "cheap": "Cheap (Haiku/Nano/Flash)",
            "balanced": "Balanced (Sonnet/Pro)",
            "powerful": "Powerful (Opus/Pro-Exp)"
        }[tier],
        "recommended_models": model_mappings[tier],
        "cost_savings_percent": cost_savings[tier],
        "reasoning": reasoning,
        "should_switch": tier != "powerful",  # Assume default is powerful
    }
    
    return tier, confidence, details

def get_current_model() -> str:
    """Try to detect current model (simplistic)."""
    # This would need to read OpenClaw config
    # For now, return a placeholder
    return "unknown"

def main():
    """CLI entry point."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="TokenLens Model Router")
    parser.add_argument("prompt", help="Prompt to analyze for model routing")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    tier, confidence, details = analyze_prompt_complexity(args.prompt)
    current_model = get_current_model()
    
    if args.json:
        output = {
            "tier": tier,
            "confidence": confidence,
            "current_model": current_model,
            "details": details
        }
        print(json.dumps(output, indent=2))
    else:
        print("TokenLens Model Router")
        print("=" * 50)
        print(f"Prompt: {args.prompt}")
        print(f"Analysis: {details['reasoning']}")
        print(f"Word count: {details['word_count']}")
        print()
        
        print(f"Recommended tier: {details['tier_display']}")
        print(f"Confidence: {confidence:.1%}")
        print(f"Cost savings vs powerful: {details['cost_savings_percent']}%")
        print()
        
        print("Recommended models by provider:")
        for provider, model in details["recommended_models"].items():
            print(f"  {provider:15} → {model}")
        
        print()
        
        if details["should_switch"]:
            print(f"Recommendation: Switch to {tier} tier for this task.")
            print(f"Potential savings: {details['cost_savings_percent']}% vs powerful model.")
        else:
            print("Recommendation: Current tier is appropriate.")
        
        print("\nTo apply:")
        print("1. Check your OpenClaw config for model settings")
        print("2. Consider using model routing in your AGENTS.md")
        print("3. For simple tasks, manually switch to cheaper model")

if __name__ == "__main__":
    main()