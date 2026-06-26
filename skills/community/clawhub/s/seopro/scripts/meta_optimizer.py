#!/usr/bin/env python3
"""
Meta Tags Optimizer
Analyzes and optimizes meta title, description, and other SEO tags.
"""

import sys
import json
import argparse
import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse


# Recommended lengths
TITLE_MAX_LENGTH = 60
TITLE_OPTIMAL = 50
DESCRIPTION_MAX_LENGTH = 160
DESCRIPTION_OPTIMAL = 155


def analyze_title(title: str) -> Dict[str, Any]:
    """Analyze meta title for SEO optimization."""
    length = len(title)
    
    issues = []
    score = 100
    
    if length == 0:
        issues.append("Missing title tag")
        score = 0
    elif length > TITLE_MAX_LENGTH:
        issues.append(f"Title too long ({length} chars, max {TITLE_MAX_LENGTH})")
        score -= 30
    elif length < 30:
        issues.append(f"Title too short ({length} chars, min 30)")
        score -= 20
    
    # Check for keywords
    if not any(word in title.lower() for word in ['seo', 'optimization', 'guide', 'tips']):
        issues.append("Consider adding relevant keywords")
        score -= 10
    
    return {
        "title": title,
        "length": length,
        "status": "✅ Good" if not issues else "⚠️ Needs work",
        "issues": issues,
        "score": max(0, score),
        "recommendation": generate_title_recommendation(title)
    }


def generate_title_recommendation(title: str) -> str:
    """Generate optimized title recommendations."""
    if not title:
        return "Add a descriptive title (50-60 characters)"
    
    if len(title) > TITLE_MAX_LENGTH:
        return f"Shorten to {TITLE_MAX_LENGTH} chars: {title[:TITLE_MAX_LENGTH]}..."
    
    if len(title) < 30:
        return "Add more descriptive words (30-60 characters)"
    
    return "Title looks good! Consider adding brand name at end with | or -"


def analyze_description(description: str) -> Dict[str, Any]:
    """Analyze meta description for SEO optimization."""
    length = len(description)
    
    issues = []
    score = 100
    
    if length == 0:
        issues.append("Missing meta description")
        score = 0
    elif length > DESCRIPTION_MAX_LENGTH:
        issues.append(f"Description too long ({length} chars, max {DESCRIPTION_MAX_LENGTH})")
        score -= 25
    elif length < 120:
        issues.append(f"Description too short ({length} chars, min 120)")
        score -= 15
    
    # Check for call-to-action
    cta_keywords = ['learn', 'discover', 'find', 'get', 'download', 'read', 'try']
    if not any(word in description.lower() for word in cta_keywords):
        issues.append("Consider adding a call-to-action")
        score -= 10
    
    return {
        "description": description,
        "length": length,
        "status": "✅ Good" if not issues else "⚠️ Needs work",
        "issues": issues,
        "score": max(0, score),
        "recommendation": generate_description_recommendation(description)
    }


def generate_description_recommendation(description: str) -> str:
    """Generate optimized description recommendations."""
    if not description:
        return "Add a compelling description (120-160 characters)"
    
    if len(description) > DESCRIPTION_MAX_LENGTH:
        return f"Shorten to {DESCRIPTION_MAX_LENGTH} chars"
    
    if len(description) < 120:
        return "Expand description with more details (120-160 characters)"
    
    return "Description looks good! Add a clear CTA."


def generate_meta_description(content: str, max_length: int = 160) -> str:
    """Generate an optimized meta description from content."""
    # Clean content
    content = re.sub(r'<[^>]+>', '', content)  # Remove HTML
    content = re.sub(r'\s+', ' ', content).strip()
    
    if len(content) <= max_length:
        return content
    
    # Find a good break point
    truncated = content[:max_length]
    last_period = truncated.rfind('.')
    last_space = truncated.rfind(' ')
    
    # Prefer sentence breaks
    if last_period > max_length * 0.7:
        return truncated[:last_period + 1]
    elif last_space > max_length * 0.8:
        return truncated[:last_space] + "..."
    
    return truncated + "..."


def analyze_url(url: str) -> Dict[str, Any]:
    """Analyze URL structure for SEO."""
    parsed = urlparse(url)
    path = parsed.path
    
    issues = []
    score = 100
    
    if not path or path == '/':
        issues.append("Root URL - consider using specific page paths")
        score -= 10
    
    # Check for keywords in URL
    url_words = [w for w in path.split('/') if w and w not in ['index', 'html', 'php']]
    if len(url_words) < 2 and path != '/':
        issues.append("URL could be more descriptive")
        score -= 15
    
    # Check for hyphens vs underscores
    if '_' in path:
        issues.append("Use hyphens (-) instead of underscores (_) in URLs")
        score -= 10
    
    # Check for uppercase
    if any(c.isupper() for c in path):
        issues.append("Use lowercase in URLs")
        score -= 10
    
    return {
        "url": url,
        "path": path,
        "structure": "/".join(url_words) if url_words else "root",
        "issues": issues,
        "score": max(0, score)
    }


def generate_meta_tags(page_title: str, content: str = "") -> Dict[str, str]:
    """Generate optimized meta tags."""
    title = page_title.strip()
    
    # Generate description from content or title
    if content:
        description = generate_meta_description(content)
    else:
        description = f"Learn more about {title} with our comprehensive guide."
    
    return {
        "title": f"{title} | Your Brand",
        "description": description,
        "og:title": title,
        "og:description": description[:200],  # OG limit
    }


def main():
    parser = argparse.ArgumentParser(description="Meta Tags Optimizer")
    parser.add_argument("--title", help="Meta title to analyze")
    parser.add_argument("--description", help="Meta description to analyze")
    parser.add_argument("--url", help="URL to analyze")
    parser.add_argument("--generate", help="Generate meta from title and content")
    parser.add_argument("--content", help="Content for description generation")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    
    args = parser.parse_args()
    
    results = {}
    
    if args.title:
        results["title_analysis"] = analyze_title(args.title)
    
    if args.description:
        results["description_analysis"] = analyze_description(args.description)
    
    if args.url:
        results["url_analysis"] = analyze_url(args.url)
    
    if args.generate:
        results["generated"] = generate_meta_tags(args.generate, args.content or "")
    
    if not results:
        # Show default example
        print("Meta Optimizer - Usage Examples:")
        print("-" * 40)
        print('  python meta_optimizer.py --title "My Page Title"')
        print('  python meta_optimizer.py --description "My meta description..."')
        print('  python meta_optimizer.py --url "https://example.com/my-page"')
        print('  python meta_optimizer.py --generate "Page Title" --content "Content here..."')
        sys.exit(1)
    
    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        for key, value in results.items():
            print(f"\n{'=' * 50}")
            print(f"📋 {key.replace('_', ' ').title()}")
            print('=' * 50)
            
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, list):
                        if v:
                            print(f"\n  ⚠️ Issues:")
                            for item in v:
                                print(f"     - {item}")
                    elif k != "recommendation":
                        print(f"   {k}: {v}")
                    else:
                        print(f"\n   💡 {v}")


if __name__ == "__main__":
    main()
