#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-Improving Enhancement - Pattern Detection
Automatically identifies recurring patterns in user corrections
"""

import sys
from pathlib import Path
from collections import Counter
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_corrections(base_dir):
    """Load corrections.md"""
    corrections_md = base_dir / "corrections.md"
    if not corrections_md.exists():
        return []
    
    content = corrections_md.read_text(encoding='utf-8')
    lines = [line.strip() for line in content.split('\n') 
             if line.strip() and not line.strip().startswith('#')]
    return lines


def extract_keywords(text):
    """Extract keywords from text"""
    # Remove common words
    stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                  'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                  'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                  'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
                  'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
                  'through', 'during', 'before', 'after', 'above', 'below',
                  'between', 'under', 'again', 'further', 'then', 'once',
                  'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                  'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
                  'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
                  'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                  'what', 'which', 'who', 'whom', 'this', 'that', 'these',
                  'those', 'am', 'and', 'but', 'if', 'or', 'because', 'until',
                  'while', 'although', 'though', 'so', 'than', 'too', 'very'}
    
    words = re.findall(r'\b[a-z]+\b', text.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return keywords


def detect_patterns(base_dir):
    """Detect patterns in corrections"""
    print("=" * 60)
    print("🔍 Pattern Detection")
    print("=" * 60)
    print()
    
    lines = load_corrections(base_dir)
    
    if len(lines) < 3:
        print("✓ Not enough corrections to detect patterns (need ≥3)")
        print(f"  Current: {len(lines)} corrections")
        return
    
    print(f"Analyzing {len(lines)} corrections...")
    print()
    
    # Extract all keywords
    all_keywords = []
    for line in lines:
        keywords = extract_keywords(line)
        all_keywords.extend(keywords)
    
    # Count keyword frequency
    keyword_counts = Counter(all_keywords)
    
    # Find recurring themes
    recurring = {k: v for k, v in keyword_counts.items() if v >= 2}
    
    if not recurring:
        print("✓ No recurring patterns detected yet")
        return
    
    print("Detected patterns:")
    print()
    
    # Sort by frequency
    sorted_patterns = sorted(recurring.items(), key=lambda x: x[1], reverse=True)
    
    for keyword, count in sorted_patterns[:10]:
        bar = "█" * count
        print(f"  {keyword:15} {bar} ({count}x)")
    
    print()
    
    # Detect pattern categories
    categories = {
        "Format": ["format", "style", "markdown", "code", "text"],
        "Communication": ["reply", "response", "message", "say", "tell"],
        "Preference": ["prefer", "like", "want", "need", "always"],
        "Correction": ["wrong", "incorrect", "error", "mistake", "fix"],
        "Tool": ["tool", "command", "script", "skill", "function"]
    }
    
    print("Pattern categories:")
    print()
    
    for category, keywords in categories.items():
        matches = [k for k in recurring.keys() if k in keywords]
        if matches:
            count = sum(recurring[m] for m in matches)
            print(f"  {category:15} ({count} occurrences)")
    
    print()
    print("=" * 60)
    print()
    print("Recommendation:")
    if len(recurring) >= 5:
        print("  ✓ Strong patterns detected - consider promoting to HOT memory")
    else:
        print("  → Continue collecting corrections")


def main():
    base_dir = Path.home() / "self-improving"
    detect_patterns(base_dir)


if __name__ == "__main__":
    main()
