#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xiaohongshu Viral Post Query Tool

Usage:
    python query_notes.py --category Beauty --days 7 --limit 20
    python query_notes.py --author_id xxxxxx --limit 50
    python query_notes.py --viral_type low_fan --limit 30
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Mock data storage (should connect to database or API in actual project)
MOCK_DATA = []


def generate_mock_data():
    """Generate mock data for demonstration"""
    categories = ["Beauty", "Fashion", "Food", "Travel", "Home", "Parenting", "Career", "Relationships"]
    data = []
    
    for i in range(100):
        category = categories[i % len(categories)]
        followers = [800, 2000, 3500, 600, 1500, 4000, 900, 2500][i % 8]
        engagement = [2000, 3500, 1500, 2800, 4200, 1800, 3100, 2600][i % 8]
        
        data.append({
            "note_id": f"note_{i+1:04d}",
            "title": f"Viral Post Example {i+1} - {category} Category",
            "author_name": f"Blogger_{i+1:03d}",
            "followers": followers,
            "category": category,
            "likes": engagement,
            "collections": int(engagement * 0.3),
            "comments": int(engagement * 0.1),
            "shares": int(engagement * 0.05),
            "publish_time": (datetime.now() - timedelta(days=i % 7)).isoformat(),
            "viral_tags": {
                "is_low_fan_viral": followers < 5000 and engagement > 2000,
                "viral_score": min(100, int(engagement / 50))
            }
        })
    
    return data


def query_notes(
    category: Optional[str] = None,
    days: int = 7,
    limit: int = 20,
    sort: str = "engagement",
    min_engagement: int = 0,
    author_id: Optional[str] = None,
    viral_type: Optional[str] = None
) -> List[Dict]:
    """
    Query viral posts
    
    Args:
        category: Category classification
        days: Number of days to query
        limit: Number of results to return
        sort: Sort field
        min_engagement: Minimum engagement threshold
        author_id: Author ID
        viral_type: Viral type (low_fan/period_spike/daily_spike/continuous)
    
    Returns:
        List of posts
    """
    global MOCK_DATA
    if not MOCK_DATA:
        MOCK_DATA = generate_mock_data()
    
    results = MOCK_DATA.copy()
    
    # Filter conditions
    if category:
        results = [n for n in results if n["category"] == category]
    
    if min_engagement > 0:
        results = [n for n in results if n["likes"] >= min_engagement]
    
    if viral_type == "low_fan":
        results = [n for n in results if n["viral_tags"]["is_low_fan_viral"]]
    
    # Sorting
    if sort == "engagement":
        results.sort(key=lambda x: x["likes"], reverse=True)
    elif sort == "growth":
        results.sort(key=lambda x: x["viral_tags"]["viral_score"], reverse=True)
    elif sort == "fans":
        results.sort(key=lambda x: x["followers"])
    
    return results[:limit]


def format_output(notes: List[Dict], format_type: str = "table") -> str:
    """Format output results"""
    if format_type == "json":
        return json.dumps(notes, ensure_ascii=False, indent=2)
    
    # Table format
    lines = []
    lines.append("=" * 100)
    lines.append(f"{'Rank':<4} {'Title':<30} {'Author':<12} {'Followers':<8} {'Likes':<8} {'Saves':<8} {'Category':<8}")
    lines.append("-" * 100)
    
    for i, note in enumerate(notes, 1):
        title = note["title"][:28] + ".." if len(note["title"]) > 30 else note["title"]
        lines.append(
            f"{i:<4} {title:<30} {note['author_name']:<12} "
            f"{note['followers']:<8} {note['likes']:<8} "
            f"{note['collections']:<8} {note['category']:<8}"
        )
    
    lines.append("=" * 100)
    lines.append(f"Total {len(notes)} viral posts found")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Xiaohongshu Viral Post Query Tool")
    parser.add_argument("--category", "-c", help="Category classification")
    parser.add_argument("--days", "-d", type=int, default=7, help="Number of days to query")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Number of results to return")
    parser.add_argument("--sort", "-s", default="engagement", 
                       choices=["engagement", "growth", "fans"],
                       help="Sort field")
    parser.add_argument("--min-engagement", "-m", type=int, default=0,
                       help="Minimum engagement threshold")
    parser.add_argument("--author-id", "-a", help="Author ID")
    parser.add_argument("--viral-type", "-v", 
                       choices=["low_fan", "period_spike", "daily_spike", "continuous"],
                       help="Viral type")
    parser.add_argument("--format", "-f", default="table",
                       choices=["table", "json"],
                       help="Output format")
    
    args = parser.parse_args()
    
    # Execute query
    results = query_notes(
        category=args.category,
        days=args.days,
        limit=args.limit,
        sort=args.sort,
        min_engagement=args.min_engagement,
        author_id=args.author_id,
        viral_type=args.viral_type
    )
    
    # Output results
    print(format_output(results, args.format))


if __name__ == "__main__":
    main()