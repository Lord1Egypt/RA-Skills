#!/usr/bin/env python3
"""
RSS to Social Media Auto-Poster
Monitor RSS feeds, generate social posts with AI, and publish.
"""

import os
import sys
import json
import hashlib
import feedparser
from datetime import datetime, timedelta
from pathlib import Path

# Configuration from environment
RSS_FEED_URLS = os.getenv('RSS_FEED_URLS', '').split(',')
SOCIAL_PLATFORMS = os.getenv('SOCIAL_PLATFORMS', 'twitter').split(',')
POST_INTERVAL_HOURS = int(os.getenv('POST_INTERVAL_HOURS', '4'))
INCLUDE_HASHTAGS = os.getenv('INCLUDE_HASHTAGS', 'true').lower() == 'true'
DATA_DIR = Path(os.getenv('RSS_TO_SOCIAL_DATA_DIR', '.rss-to-social'))

def ensure_data_dir():
    """Ensure data directory exists"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_posted_history():
    """Load history of posted items"""
    history_file = DATA_DIR / 'posted.json'
    if history_file.exists():
        with open(history_file, 'r') as f:
            return json.load(f)
    return {'posted_urls': [], 'last_check': None}

def save_posted_history(history):
    """Save history of posted items"""
    ensure_data_dir()
    history_file = DATA_DIR / 'posted.json'
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def get_url_hash(url):
    """Generate hash for URL deduplication"""
    return hashlib.md5(url.encode()).hexdigest()

def is_already_posted(url, history, days=30):
    """Check if URL was already posted within deduplication window"""
    url_hash = get_url_hash(url)
    cutoff = datetime.now() - timedelta(days=days)
    
    for item in history['posted_urls']:
        if item['hash'] == url_hash:
            posted_date = datetime.fromisoformat(item['posted_at'])
            if posted_date > cutoff:
                return True
    return False

def mark_as_posted(url, history):
    """Mark URL as posted"""
    url_hash = get_url_hash(url)
    history['posted_urls'].append({
        'url': url,
        'hash': url_hash,
        'posted_at': datetime.now().isoformat()
    })
    # Keep only last 1000 items
    history['posted_urls'] = history['posted_urls'][-1000:]
    return history

def fetch_feeds():
    """Fetch all RSS feeds and return new items"""
    history = load_posted_history()
    new_items = []
    
    for feed_url in RSS_FEED_URLS:
        feed_url = feed_url.strip()
        if not feed_url:
            continue
            
        try:
            feed = feedparser.parse(feed_url)
            print(f"✓ Fetched: {feed.feed.get('title', feed_url)[:50]}")
            
            for entry in feed.entries[:10]:  # Limit to 10 latest per feed
                link = entry.get('link', '')
                if link and not is_already_posted(link, history):
                    new_items.append({
                        'title': entry.get('title', 'No title'),
                        'link': link,
                        'summary': entry.get('summary', '')[:500],
                        'published': entry.get('published', ''),
                        'source': feed.feed.get('title', feed_url)
                    })
        except Exception as e:
            print(f"✗ Error fetching {feed_url}: {e}")
    
    history['last_check'] = datetime.now().isoformat()
    save_posted_history(history)
    
    return new_items, history

def generate_twitter_post(item):
    """Generate Twitter-style post (280 chars)"""
    title = item['title'][:100]
    link = item['link']
    
    # Shorten link if needed
    if len(link) > 30:
        link = link[:27] + '...'
    
    hashtags = " #AI #Tech #Automation" if INCLUDE_HASHTAGS else ""
    
    post = f"""🚀 New: {title}

Source: {item['source']}
Read more: {link}{hashtags}"""
    
    # Ensure under 280 chars
    if len(post) > 280:
        post = post[:277] + '...'
    
    return post

def generate_linkedin_post(item):
    """Generate LinkedIn-style post (professional, longer)"""
    title = item['title']
    link = item['link']
    summary = item['summary'][:300]
    
    post = f"""Exciting update from {item['source']}!

📰 {title}

{summary}

Read the full article: {link}

#Technology #Innovation #Business"""
    
    return post

def generate_posts(items):
    """Generate social media posts for items"""
    posts = []
    
    for item in items:
        post = {
            'item': item,
            'twitter': generate_twitter_post(item),
            'linkedin': generate_linkedin_post(item),
            'created_at': datetime.now().isoformat()
        }
        posts.append(post)
        print(f"\n📝 Generated post for: {item['title'][:50]}...")
    
    return posts

def send_to_openclaw(posts, platforms):
    """Send posts to OpenClaw for publishing"""
    # This integrates with OpenClaw's messaging system
    # For now, output the posts for review
    
    print("\n" + "="*60)
    print("📱 READY TO POST")
    print("="*60)
    
    for i, post in enumerate(posts, 1):
        print(f"\n--- Post {i} ---")
        
        if 'twitter' in platforms:
            print(f"\n🐦 TWITTER:")
            print(post['twitter'])
            print(f"Characters: {len(post['twitter'])}/280")
        
        if 'linkedin' in platforms:
            print(f"\n💼 LINKEDIN:")
            print(post['linkedin'])
    
    print("\n" + "="*60)
    print(f"Total posts ready: {len(posts)}")
    print(f"Platforms: {', '.join(platforms)}")
    print("="*60)
    
    return posts

def mark_posts_posted(posts, history):
    """Mark all posts as posted in history"""
    for post in posts:
        history = mark_as_posted(post['item']['link'], history)
    save_posted_history(history)
    print(f"✓ Marked {len(posts)} items as posted")

def show_status():
    """Show current monitoring status"""
    history = load_posted_history()
    
    print("\n📊 RSS to Social Status")
    print("="*40)
    print(f"Feeds monitored: {len([f for f in RSS_FEED_URLS if f.strip()])}")
    print(f"Platforms: {', '.join(SOCIAL_PLATFORMS)}")
    print(f"Post interval: Every {POST_INTERVAL_HOURS} hours")
    print(f"Last check: {history['last_check'] or 'Never'}")
    print(f"Total posted: {len(history['posted_urls'])}")
    print("="*40)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'status':
            show_status()
            return
        
        elif command == 'test':
            # Test mode - fetch and show without posting
            print("🧪 TEST MODE - No posts will be saved")
            items, _ = fetch_feeds()
            if items:
                posts = generate_posts(items)
                send_to_openclaw(posts, SOCIAL_PLATFORMS)
            else:
                print("\n✅ No new content to post")
            return
    
    # Normal mode - fetch, generate, and prepare for posting
    print("📰 RSS to Social Auto-Poster")
    print(f"Started at: {datetime.now().isoformat()}")
    print(f"Monitoring {len([f for f in RSS_FEED_URLS if f.strip()])} feeds")
    print(f"Posting to: {', '.join(SOCIAL_PLATFORMS)}")
    print("-"*40)
    
    items, history = fetch_feeds()
    
    if not items:
        print("\n✅ No new content to post")
        print(f"Next check in {POST_INTERVAL_HOURS} hours")
        return
    
    print(f"\n🎯 Found {len(items)} new items")
    
    posts = generate_posts(items)
    send_to_openclaw(posts, SOCIAL_PLATFORMS)
    
    # Mark as posted (in real implementation, this happens after successful posting)
    mark_posts_posted(posts, history)
    
    print(f"\n✅ Done! Next check in {POST_INTERVAL_HOURS} hours")

if __name__ == '__main__':
    main()
