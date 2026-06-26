#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xiaohongshu Trend Analysis Tool

Usage:
    python analyze_trends.py --category Fashion --output report.md
    python analyze_trends.py --category Beauty --days 30
"""

import argparse
import json
from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, List


def analyze_trends(category: str, days: int = 7) -> Dict:
    """
    Analyze category trends
    
    Args:
        category: Category classification
        days: Number of days to analyze
    
    Returns:
        Trend analysis report
    """
    # Mock data (should be retrieved from database in actual use)
    mock_keywords = {
        "Fashion": ["OOTD", "Korean style", "Minimalist", "Office wear", "Petite", "Slimming", "Fall/Winter", "Layering"],
        "Beauty": ["No-makeup look", "Morning routine", "Affordable", "Student budget", "Warm skin tone", "Depuffing", "Beginner", "Tutorial"],
        "Food": ["Solo dining", "Lazy meals", "Weight loss", "Breakfast", "Meal prep", "Restaurant review", "Homemade", "Quick recipe"],
        "Travel": ["Hidden gems", "Guide", "Per person cost", "Avoid pitfalls", "Photo spots", "Photography", "Budget travel", "Weekend trip"],
    }
    
    keywords = mock_keywords.get(category, ["Trending", "Recommended", "Share", "Tutorial"])
    
    # Generate trend data
    report = {
        "category": category,
        "analysis_period": f"{days} days",
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_notes": 1500 + days * 100,
            "viral_notes": 200 + days * 20,
            "avg_engagement": 2500,
            "growth_rate": "+15.3%"
        },
        "hot_keywords": [
            {"keyword": kw, "count": 150 - i * 10, "trend": "up" if i < 4 else "stable"}
            for i, kw in enumerate(keywords[:8])
        ],
        "cover_styles": [
            {"style": "Solid color background", "percentage": 35},
            {"style": "Collage comparison", "percentage": 25},
            {"style": "Scene photography", "percentage": 20},
            {"style": "Portrait feature", "percentage": 15},
            {"style": "Text overlay cover", "percentage": 5}
        ],
        "best_posting_time": [
            {"time": "12:00-13:00", "engagement": "High"},
            {"time": "18:00-19:00", "engagement": "High"},
            {"time": "21:00-22:00", "engagement": "Medium-High"},
            {"time": "08:00-09:00", "engagement": "Medium"}
        ],
        "title_patterns": [
            "Number method: X tips/methods/items",
            "Audience method: Must-read for XX / Suitable for XX",
            "Scenario method: XX occasion / When XX",
            "Comparison method: Before & After",
            "Suspense method: Never / Regret not knowing sooner"
        ],
        "content_insights": [
            f"Recent viral posts in the {category} category are predominantly practical tips",
            "Users prefer authentic experience sharing and dislike overt advertisements",
            "Image posts account for 70%, short video posts show significant growth",
            "Posts with high comment section engagement are more likely to see secondary distribution"
        ]
    }
    
    return report


def generate_markdown_report(report: Dict) -> str:
    """Generate Markdown format report"""
    lines = []
    
    lines.append(f"# {report['category']} Category Trend Analysis Report")
    lines.append(f"\n> Analysis Period: {report['analysis_period']} | Generated on: {report['generated_at'][:10]}")
    
    # Data overview
    lines.append("\n## Data Overview")
    lines.append(f"- Total Posts Indexed: **{report['summary']['total_notes']}**")
    lines.append(f"- Viral Posts: **{report['summary']['viral_notes']}**")
    lines.append(f"- Average Engagement: **{report['summary']['avg_engagement']}**")
    lines.append(f"- Period-over-Period Growth: **{report['summary']['growth_rate']}**")
    
    # Hot keywords
    lines.append("\n## Top 8 Trending Keywords")
    lines.append("| Rank | Keyword | Occurrences | Trend |")
    lines.append("|------|---------|-------------|-------|")
    for i, kw in enumerate(report['hot_keywords'], 1):
        trend_emoji = "📈" if kw['trend'] == 'up' else "➡️"
        lines.append(f"| {i} | {kw['keyword']} | {kw['count']} | {trend_emoji} |")
    
    # Cover style distribution
    lines.append("\n## Viral Post Cover Style Distribution")
    lines.append("| Style | Percentage | Visualization |")
    lines.append("|-------|------------|---------------|")
    for style in report['cover_styles']:
        bar = "█" * (style['percentage'] // 5)
        lines.append(f"| {style['style']} | {style['percentage']}% | {bar} |")
    
    # Best posting times
    lines.append("\n## Optimal Posting Time Windows")
    lines.append("| Time Window | Engagement Level | Recommendation |")
    lines.append("|-------------|------------------|----------------|")
    for time_slot in report['best_posting_time']:
        suggestion = "⭐ Highly Recommended" if time_slot['engagement'] == 'High' else "✓ Recommended"
        lines.append(f"| {time_slot['time']} | {time_slot['engagement']} | {suggestion} |")
    
    # Viral title formulas
    lines.append("\n## Viral Title Formulas")
    for i, pattern in enumerate(report['title_patterns'], 1):
        lines.append(f"{i}. **{pattern}**")
    
    # Content insights
    lines.append("\n## Content Insights")
    for insight in report['content_insights']:
        lines.append(f"- {insight}")
    
    lines.append("\n---")
    lines.append("\n*Report generated by Xiaohongshu Data Insight Tool*")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Xiaohongshu Trend Analysis Tool")
    parser.add_argument("--category", "-c", required=True, help="Category classification")
    parser.add_argument("--days", "-d", type=int, default=7, help="Number of days to analyze")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", "-f", default="markdown",
                       choices=["markdown", "json"],
                       help="Output format")
    
    args = parser.parse_args()
    
    # Execute analysis
    report = analyze_trends(args.category, args.days)
    
    # Generate output
    if args.format == "json":
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        output = generate_markdown_report(report)
    
    # Output results
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()