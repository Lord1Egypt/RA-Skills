"""
Simple Reddit Scraper - No API Keys Required
=============================================
Uses Reddit's public .json API endpoints.
No authentication needed.
"""

import requests
import time

class SimpleRedditScraper:
    """Simple Reddit scraper using public .json endpoints."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = 'https://www.reddit.com'
    
    def _make_request(self, url):
        """Make a request with rate limiting."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def search(self, query, limit=25, sort='relevance', time_filter='week'):
        """
        Search Reddit for a query.
        
        Args:
            query: Search term
            limit: Max results (up to 100)
            sort: 'relevance', 'hot', 'top', 'new', 'comments'
            time_filter: 'hour', 'day', 'week', 'month', 'year', 'all'
        
        Returns:
            List of post dictionaries
        """
        url = f"{self.base_url}/search.json?q={query}&limit={limit}&sort={sort}&t={time_filter}"
        data = self._make_request(url)
        
        if 'error' in data:
            return {'posts': [], 'error': data['error']}
        
        posts = []
        for child in data.get('data', {}).get('children', []):
            post = child.get('data', {})
            posts.append({
                'title': post.get('title', ''),
                'subreddit': post.get('subreddit', ''),
                'score': post.get('score', 0),
                'num_comments': post.get('num_comments', 0),
                'url': f"https://reddit.com{post.get('permalink', '')}",
                'created_utc': post.get('created_utc', 0),
                'selftext': post.get('selftext', '')[:200]  # First 200 chars
            })
        
        return {'posts': posts}
    
    def get_subreddit(self, subreddit, sort='hot', limit=25, time_filter='week'):
        """
        Get posts from a subreddit.
        
        Args:
            subreddit: Subreddit name (without r/)
            sort: 'hot', 'new', 'top', 'rising'
            limit: Max results
            time_filter: For 'top' sort - 'hour', 'day', 'week', 'month', 'year', 'all'
        
        Returns:
            List of post dictionaries
        """
        if sort == 'top':
            url = f"{self.base_url}/r/{subreddit}/top.json?limit={limit}&t={time_filter}"
        else:
            url = f"{self.base_url}/r/{subreddit}/{sort}.json?limit={limit}"
        
        data = self._make_request(url)
        
        if 'error' in data:
            return {'posts': [], 'error': data['error']}
        
        posts = []
        for child in data.get('data', {}).get('children', []):
            post = child.get('data', {})
            posts.append({
                'title': post.get('title', ''),
                'subreddit': post.get('subreddit', ''),
                'score': post.get('score', 0),
                'num_comments': post.get('num_comments', 0),
                'url': f"https://reddit.com{post.get('permalink', '')}",
                'created_utc': post.get('created_utc', 0),
                'selftext': post.get('selftext', '')[:200]
            })
        
        return {'posts': posts}
    
    def get_trending_subreddits(self):
        """Get popular/trending subreddits."""
        url = f"{self.base_url}/subreddits/popular.json?limit=25"
        data = self._make_request(url)
        
        if 'error' in data:
            return {'subreddits': [], 'error': data['error']}
        
        subreddits = []
        for child in data.get('data', {}).get('children', []):
            sub = child.get('data', {})
            subreddits.append({
                'name': sub.get('display_name', ''),
                'title': sub.get('title', ''),
                'subscribers': sub.get('subscribers', 0),
                'description': sub.get('public_description', '')[:100]
            })
        
        return {'subreddits': subreddits}


# Quick test
if __name__ == "__main__":
    scraper = SimpleRedditScraper()
    
    print("🔍 Testing Reddit Search...")
    results = scraper.search("heart health", limit=5)
    for post in results.get('posts', []):
        print(f"  [{post['score']}] r/{post['subreddit']}: {post['title'][:60]}...")
    
    print("\n🔥 Testing Subreddit Hot Posts...")
    time.sleep(2)  # Rate limiting
    results = scraper.get_subreddit("health", sort="hot", limit=5)
    for post in results.get('posts', []):
        print(f"  [{post['score']}] {post['title'][:60]}...")
