#!/usr/bin/env python3
"""
Social Media Trends Research Tool
==================================
Programmatic trend research using pytrends (Google Trends) and yars (Reddit).
No API keys required.

Usage:
    python trend_research.py --keywords "heart health" "cardiology" 
    python trend_research.py --keywords "AI" --subreddits "artificial" "MachineLearning"
    python trend_research.py --keywords "fitness" --output results.json
    python trend_research.py --trending-only  # Just show trending searches
"""

import argparse
import json
import time
import sys
from datetime import datetime

def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    try:
        from pytrends.request import TrendReq
    except ImportError:
        missing.append("pytrends")
    
    try:
        import requests
    except ImportError:
        missing.append("requests")
    
    if missing:
        print("❌ Missing dependencies. Install with:")
        for pkg in missing:
            print(f"   pip install {pkg} --break-system-packages")
        sys.exit(1)

def get_trending_searches(country='india'):
    """Get real-time trending searches from Google."""
    from pytrends.request import TrendReq
    
    pytrends = TrendReq(hl='en-US', tz=330)
    trending = pytrends.trending_searches(pn=country)
    return trending[0].tolist()[:20]

def get_keyword_data(keywords, timeframe='now 7-d', geo='IN'):
    """Get interest and related queries for keywords."""
    from pytrends.request import TrendReq
    
    pytrends = TrendReq(hl='en-US', tz=330)
    
    results = {
        'keywords': keywords,
        'timeframe': timeframe,
        'geo': geo,
        'interest_over_time': None,
        'rising_queries': {},
        'related_topics': {}
    }
    
    # Interest over time
    print(f"📊 Analyzing: {', '.join(keywords)}")
    pytrends.build_payload(keywords[:5], timeframe=timeframe, geo=geo)
    
    try:
        interest = pytrends.interest_over_time()
        if not interest.empty:
            # Get average interest for each keyword
            results['interest_over_time'] = {}
            for kw in keywords[:5]:
                if kw in interest.columns:
                    results['interest_over_time'][kw] = round(interest[kw].mean(), 2)
    except Exception as e:
        print(f"   ⚠️ Interest data error: {e}")
    
    time.sleep(3)
    
    # Related queries (rising = potential viral topics)
    try:
        related = pytrends.related_queries()
        for kw in keywords[:5]:
            rising = related[kw]['rising']
            if rising is not None and not rising.empty:
                results['rising_queries'][kw] = rising.head(10).to_dict('records')
    except Exception as e:
        print(f"   ⚠️ Related queries error: {e}")
    
    time.sleep(3)
    
    # Related topics
    try:
        topics = pytrends.related_topics()
        for kw in keywords[:5]:
            rising = topics[kw]['rising']
            if rising is not None and not rising.empty:
                results['related_topics'][kw] = rising.head(5).to_dict('records')
    except Exception as e:
        print(f"   ⚠️ Related topics error: {e}")
    
    return results

def search_reddit(keywords, limit=10):
    """Search Reddit for keyword discussions."""
    import requests
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    results = {}
    
    for kw in keywords[:3]:  # Limit to avoid rate limiting
        print(f"👽 Searching Reddit: {kw}")
        try:
            url = f"https://www.reddit.com/search.json?q={kw}&limit={limit}&sort=relevance&t=week"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results[kw] = []
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                results[kw].append({
                    'title': post.get('title', ''),
                    'subreddit': post.get('subreddit', ''),
                    'score': post.get('score', 0),
                    'comments': post.get('num_comments', 0),
                    'url': f"https://reddit.com{post.get('permalink', '')}"
                })
            time.sleep(3)
        except Exception as e:
            print(f"   ⚠️ Error searching '{kw}': {e}")
            results[kw] = []
    
    return results

def get_subreddit_hot(subreddits, limit=5):
    """Get hot posts from specific subreddits."""
    import requests
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    results = {}
    
    for sub in subreddits[:5]:  # Limit to avoid rate limiting
        print(f"🔥 Checking r/{sub}")
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results[sub] = []
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                results[sub].append({
                    'title': post.get('title', ''),
                    'score': post.get('score', 0),
                    'comments': post.get('num_comments', 0),
                    'url': f"https://reddit.com{post.get('permalink', '')}"
                })
            time.sleep(3)
        except Exception as e:
            print(f"   ⚠️ Error with r/{sub}: {e}")
            results[sub] = []
    
    return results

def generate_recommendations(google_data, reddit_data):
    """Generate content recommendations from research."""
    recommendations = []
    
    # From Google rising queries
    for kw, queries in google_data.get('rising_queries', {}).items():
        for q in queries[:3]:
            if isinstance(q, dict):
                recommendations.append({
                    'source': 'Google Trends',
                    'topic': q.get('query', ''),
                    'signal': f"Rising search (+{q.get('value', 0)}%)",
                    'priority': 'HIGH' if q.get('value', 0) >= 500 else 'MEDIUM'
                })
    
    # From Reddit high-engagement posts
    for kw, posts in reddit_data.items():
        for post in posts[:2]:
            if post.get('score', 0) >= 100:
                recommendations.append({
                    'source': f"Reddit (r/{post.get('subreddit', kw)})",
                    'topic': post.get('title', '')[:80],
                    'signal': f"High engagement ({post.get('score')} upvotes)",
                    'priority': 'HIGH' if post.get('score', 0) >= 500 else 'MEDIUM'
                })
    
    # Sort by priority
    priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'LOW'), 2))
    
    return recommendations

def print_report(data):
    """Print a formatted research report."""
    print("\n" + "="*60)
    print("📈 TREND RESEARCH REPORT")
    print("="*60)
    print(f"Generated: {data['timestamp']}")
    print(f"Keywords: {', '.join(data['keywords'])}")
    
    # Google Trends
    if data.get('google_trends', {}).get('interest_over_time'):
        print("\n📊 GOOGLE TRENDS - INTEREST LEVELS")
        print("-"*40)
        for kw, score in data['google_trends']['interest_over_time'].items():
            bar = "█" * int(score / 10)
            print(f"  {kw}: {bar} ({score})")
    
    # Rising Queries
    if data.get('google_trends', {}).get('rising_queries'):
        print("\n🚀 RISING SEARCH QUERIES (Potential Viral Topics)")
        print("-"*40)
        for kw, queries in data['google_trends']['rising_queries'].items():
            print(f"\n  Related to '{kw}':")
            for q in queries[:5]:
                if isinstance(q, dict):
                    value = q.get('value', 0)
                    marker = "🔥" if value >= 500 else "📈"
                    print(f"    {marker} {q.get('query', '')} (+{value}%)")
    
    # Reddit
    if data.get('reddit'):
        print("\n👽 REDDIT DISCUSSIONS")
        print("-"*40)
        for source, posts in data['reddit'].items():
            if posts:
                print(f"\n  {source}:")
                for post in posts[:3]:
                    print(f"    ↑{post.get('score', 0):4d} | {post.get('title', '')[:50]}...")
    
    # Recommendations
    if data.get('recommendations'):
        print("\n🎯 CONTENT RECOMMENDATIONS")
        print("-"*40)
        for i, rec in enumerate(data['recommendations'][:10], 1):
            priority_icon = "🔴" if rec['priority'] == 'HIGH' else "🟡"
            print(f"  {i}. {priority_icon} [{rec['source']}]")
            print(f"     Topic: {rec['topic']}")
            print(f"     Signal: {rec['signal']}")
    
    print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description='Social Media Trends Research Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python trend_research.py --keywords "heart health" "cardiology"
  python trend_research.py --keywords "AI" --subreddits "artificial" "MachineLearning"
  python trend_research.py --trending-only
  python trend_research.py --keywords "fitness" --output results.json
        """
    )
    
    parser.add_argument('--keywords', '-k', nargs='+', 
                        help='Keywords to research (max 5)')
    parser.add_argument('--subreddits', '-s', nargs='+',
                        help='Subreddits to monitor (max 5)')
    parser.add_argument('--trending-only', '-t', action='store_true',
                        help='Only show trending searches')
    parser.add_argument('--timeframe', default='now 7-d',
                        help='Timeframe for Google Trends (default: now 7-d)')
    parser.add_argument('--geo', default='IN',
                        help='Geographic region (default: IN for India)')
    parser.add_argument('--output', '-o',
                        help='Save results to JSON file')
    parser.add_argument('--country', default='india',
                        help='Country for trending searches (default: india)')
    
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    
    # Trending only mode
    if args.trending_only:
        print("🔥 REAL-TIME TRENDING SEARCHES")
        print("-"*40)
        trending = get_trending_searches(args.country)
        for i, topic in enumerate(trending, 1):
            print(f"  {i:2d}. {topic}")
        return
    
    # Need keywords for full research
    if not args.keywords:
        parser.print_help()
        print("\n❌ Please provide keywords with --keywords")
        sys.exit(1)
    
    # Full research
    data = {
        'timestamp': datetime.now().isoformat(),
        'keywords': args.keywords,
        'google_trends': {},
        'reddit': {},
        'recommendations': []
    }
    
    # Google Trends
    google_data = get_keyword_data(args.keywords, args.timeframe, args.geo)
    data['google_trends'] = google_data
    
    # Reddit keyword search
    reddit_search = search_reddit(args.keywords)
    data['reddit'].update(reddit_search)
    
    # Reddit subreddits (if provided)
    if args.subreddits:
        subreddit_data = get_subreddit_hot(args.subreddits)
        for sub, posts in subreddit_data.items():
            data['reddit'][f'r/{sub}'] = posts
    
    # Generate recommendations
    data['recommendations'] = generate_recommendations(google_data, data['reddit'])
    
    # Print report
    print_report(data)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {args.output}")
    
    # Reminder about Perplexity
    print("\n💡 TIP: For Twitter/TikTok trends, ask Claude to use Perplexity MCP:")
    print("   'What's trending on Twitter about [your niche] this week?'")

if __name__ == "__main__":
    main()
