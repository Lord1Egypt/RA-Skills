#!/usr/bin/env python3
"""
Keyword Research Tool
Provides keyword suggestions and basic search insights.
"""

import sys
import json
import argparse
from typing import List, Dict, Any


def get_keyword_suggestions(keyword: str) -> List[Dict[str, Any]]:
    """Generate keyword suggestions based on input."""
    
    # Common keyword modifiers for expansion
    modifiers = [
        "guide", "tutorial", "best", "top", "how to", "tips",
        "tools", "software", "free", "online", "for beginners",
        "examples", "review", "comparison", "vs", "alternatives"
    ]
    
    suggestions = []
    keyword_lower = keyword.lower()
    
    # Generate combinations
    for mod in modifiers:
        if mod not in keyword_lower:
            suggestions.append({
                "keyword": f"{keyword} {mod}",
                "type": "long-tail",
                "priority": "high" if len(mod.split()) > 1 else "medium"
            })
    
    # Add question-based keywords
    question_keywords = [
        f"what is {keyword}",
        f"how to {keyword}",
        f"why {keyword}",
        f"where to {keyword}"
    ]
    
    for q in question_keywords:
        suggestions.append({
            "keyword": q,
            "type": "question",
            "priority": "high"
        })
    
    return suggestions[:10]


def calculate_keyword_difficulty(keyword: str) -> Dict[str, Any]:
    """Estimate keyword difficulty based on length and competition indicators."""
    
    word_count = len(keyword.split())
    
    if word_count >= 4:
        difficulty = "low"
        difficulty_score = 25
    elif word_count >= 3:
        difficulty = "medium-low"
        difficulty_score = 45
    elif word_count >= 2:
        difficulty = "medium"
        difficulty_score = 60
    else:
        difficulty = "high"
        difficulty_score = 80
    
    return {
        "keyword": keyword,
        "difficulty": difficulty,
        "score": difficulty_score,
        "word_count": word_count,
        "recommendation": "Long-tail keywords rank easier" if word_count >= 3 else "Consider long-tail variations"
    }


def main():
    parser = argparse.ArgumentParser(description="Keyword Research Tool")
    parser.add_argument("keyword", help="Primary keyword to research")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    keyword = args.keyword.strip()
    
    if not keyword:
        print("Error: Please provide a keyword", file=sys.stderr)
        sys.exit(1)
    
    # Get suggestions
    suggestions = get_keyword_suggestions(keyword)
    
    # Get difficulty
    difficulty = calculate_keyword_difficulty(keyword)
    
    if args.format == "json":
        result = {
            "primary_keyword": keyword,
            "difficulty": difficulty,
            "suggestions": suggestions
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"🔍 Keyword Research: {keyword}")
        print("=" * 50)
        print(f"\n📊 Difficulty Analysis:")
        print(f"   Level: {difficulty['difficulty'].upper()}")
        print(f"   Score: {difficulty['score']}/100")
        print(f"   Words: {difficulty['word_count']}")
        print(f"   Tip: {difficulty['recommendation']}")
        
        print(f"\n📝 Suggested Keywords:")
        for i, s in enumerate(suggestions, 1):
            priority_emoji = "⭐" if s["priority"] == "high" else "  "
            print(f"   {priority_emoji} {i}. {s['keyword']} ({s['type']})")
        
        print(f"\n💡 Tip: Focus on high-priority long-tail keywords for better rankings!")


if __name__ == "__main__":
    main()
