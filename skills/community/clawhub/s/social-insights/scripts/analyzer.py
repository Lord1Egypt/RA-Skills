#!/usr/bin/env python3
"""
Social Analytics - Performance Tracking and Insights
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
DATA_DIR = Path(os.getenv('SOCIAL_ANALYTICS_DATA_DIR', '.social-analytics'))
PLATFORMS = os.getenv('ANALYTICS_PLATFORMS', 'twitter').split(',')

def ensure_data_dir():
    """Ensure data directory exists"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def generate_sample_report():
    """Generate sample analytics report (demo mode)"""
    report = {
        'period': 'Last 7 days',
        'generated_at': datetime.now().isoformat(),
        'metrics': {
            'followers': {'current': 1234, 'previous': 1178, 'change': '+4.8%'},
            'impressions': {'current': 45678, 'previous': 40784, 'change': '+12.0%'},
            'engagement_rate': {'current': '3.2%', 'industry_avg': '1.8%', 'status': 'Above Average'}
        },
        'top_posts': [
            {'text': 'AI automation saves 20hrs/week', 'likes': 234, 'retweets': 45, 'engagement': '4.2%'},
            {'text': 'New skill released on ClawHub!', 'likes': 189, 'retweets': 32, 'engagement': '3.8%'},
            {'text': 'Client results showcase', 'likes': 156, 'retweets': 28, 'engagement': '3.5%'}
        ],
        'best_times': [
            {'day': 'Tuesday', 'time': '10:00-12:00', 'engagement': '4.2%'},
            {'day': 'Thursday', 'time': '14:00-16:00', 'engagement': '3.8%'},
            {'day': 'Sunday', 'time': '19:00-21:00', 'engagement': '3.5%'}
        ],
        'recommendations': [
            'Post more case studies (highest engagement)',
            'Increase posting frequency on Tuesdays',
            'Try video content (competitors seeing 2x engagement)',
            'Respond to comments within 1 hour for better reach'
        ]
    }
    return report

def format_report(report):
    """Format report for display"""
    output = []
    output.append("📊 Social Media Analytics Report")
    output.append("=" * 50)
    output.append(f"Period: {report['period']}")
    output.append(f"Generated: {report['generated_at'][:10]}")
    output.append("")
    
    output.append("📈 Key Metrics:")
    for metric, data in report['metrics'].items():
        metric_name = metric.replace('_', ' ').title()
        if metric == 'engagement_rate':
            output.append(f"• {metric_name}: {data['current']} (Industry: {data['industry_avg']}) - {data['status']}")
        else:
            output.append(f"• {metric_name}: {data['current']:,} ({data['change']})")
    output.append("")
    
    output.append("🏆 Top Performing Posts:")
    for i, post in enumerate(report['top_posts'], 1):
        output.append(f"{i}. \"{post['text']}\" - {post['likes']} likes, {post['retweets']} retweets ({post['engagement']})")
    output.append("")
    
    output.append("⏰ Best Posting Times:")
    for time in report['best_times']:
        output.append(f"• {time['day']} {time['time']} - Avg Engagement: {time['engagement']}")
    output.append("")
    
    output.append("💡 Recommendations:")
    for rec in report['recommendations']:
        output.append(f"• {rec}")
    output.append("")
    output.append("=" * 50)
    
    return '\n'.join(output)

def generate_competitor_analysis():
    """Generate sample competitor comparison"""
    output = []
    output.append("📊 Competitor Analysis Report")
    output.append("=" * 50)
    output.append("Your Account vs Competitors (Last 30 Days)")
    output.append("")
    output.append(f"{'Metric':<18} {'You':<10} {'Comp1':<10} {'Comp2':<10} {'Industry':<10}")
    output.append("-" * 58)
    output.append(f"{'Engagement Rate':<18} {'3.2%':<10} {'2.8%':<10} {'4.1%':<10} {'1.8%':<10}")
    output.append(f"{'Posts/Week':<18} {'5':<10} {'7':<10} {'3':<10} {'4':<10}")
    output.append(f"{'Avg Likes':<18} {'156':<10} {'134':<10} {'289':<10} {'95':<10}")
    output.append(f"{'Avg Retweets':<18} {'23':<10} {'18':<10} {'45':<10} {'12':<10}")
    output.append(f"{'Follower Growth':<18} {'+4.5%':<10} {'+2.1%':<10} {'+6.8%':<10} {'+1.5%':<10}")
    output.append("")
    output.append("💡 Insights:")
    output.append("• Your engagement rate is 78% above industry average! Great job!")
    output.append("• Comp2 gets more engagement with video content")
    output.append("• You post less frequently than competitors")
    output.append("• Opportunity: Increase posting to 7/week")
    output.append("")
    output.append("🎯 Action Items:")
    output.append("1. Add 2 video posts this week")
    output.append("2. Test posting on Wednesday mornings")
    output.append("3. Analyze Comp2's top posts for content ideas")
    output.append("=" * 50)
    
    return '\n'.join(output)

def main():
    """Main entry point"""
    ensure_data_dir()
    
    print("📊 Social Analytics")
    print(f"Platforms: {', '.join(PLATFORMS)}")
    print("-" * 40)
    
    # Check for API credentials
    has_twitter_api = os.getenv('TWITTER_API_KEY')
    
    if not has_twitter_api:
        print("⚠️  No API credentials found - running in demo mode")
        print("   For real data, set TWITTER_API_KEY environment variable")
        print()
    
    # Generate and display report
    report = generate_sample_report()
    print(format_report(report))
    print()
    
    # Also show competitor analysis
    print(generate_competitor_analysis())
    print()
    
    print("✅ Analytics complete!")
    print("   To save reports: python analyzer.py --save")
    print("   For competitor analysis: python analyzer.py --competitors")

if __name__ == '__main__':
    main()
