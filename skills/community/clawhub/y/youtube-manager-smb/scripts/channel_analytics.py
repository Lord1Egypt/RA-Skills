#!/usr/bin/env python3
"""
YouTube Channel Analytics Script
Comprehensive channel data analysis and monitoring
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class YouTubeChannelAnalytics:
    def __init__(self, api_key: str, channel_id: str):
        self.api_key = api_key
        self.channel_id = channel_id
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def get_basic_stats(self) -> Dict:
        """Get basic channel statistics"""
        url = f"{self.base_url}/channels"
        params = {
            'part': 'statistics,snippet',
            'id': self.channel_id,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                channel = data['items'][0]
                stats = channel['statistics']
                snippet = channel['snippet']
                
                return {
                    'channel_id': self.channel_id,
                    'channel_title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'published_at': snippet.get('publishedAt', ''),
                    'subscriber_count': int(stats.get('subscriberCount', 0)),
                    'view_count': int(stats.get('viewCount', 0)),
                    'video_count': int(stats.get('videoCount', 0)),
                    'hidden_subscriber_count': stats.get('hiddenSubscriberCount', False),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {'error': 'Channel not found'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def get_recent_videos(self, max_results: int = 10) -> List[Dict]:
        """Get recent videos from the channel"""
        url = f"{self.base_url}/search"
        params = {
            'part': 'snippet',
            'channelId': self.channel_id,
            'order': 'date',
            'maxResults': max_results,
            'type': 'video',
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url']
                }
                videos.append(video)
                
            return videos
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_video_analytics(self, video_id: str) -> Dict:
        """Get detailed analytics for a specific video"""
        # This would require YouTube Analytics API (different from Data API v3)
        # For now, we'll use the Data API to get basic stats
        
        url = f"{self.base_url}/videos"
        params = {
            'part': 'statistics,snippet',
            'id': video_id,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                video = data['items'][0]
                stats = video['statistics']
                snippet = video['snippet']
                
                return {
                    'video_id': video_id,
                    'title': snippet.get('title', ''),
                    'published_at': snippet.get('publishedAt', ''),
                    'view_count': int(stats.get('viewCount', 0)),
                    'like_count': int(stats.get('likeCount', 0)),
                    'comment_count': int(stats.get('commentCount', 0)),
                    'favorite_count': int(stats.get('favoriteCount', 0)),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {'error': 'Video not found'}
                
        except Exception as e:
            return {'error': str(e)}

def main():
    """Main function for command line usage"""
    api_key = os.getenv('YOUTUBE_API_KEY')
    channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
    
    if not api_key or not channel_id:
        print("Error: Please set YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID environment variables")
        return
    
    analytics = YouTubeChannelAnalytics(api_key, channel_id)
    
    # Get basic stats
    stats = analytics.get_basic_stats()
    print("=== Channel Statistics ===")
    print(json.dumps(stats, indent=2))
    
    # Get recent videos
    print("\n=== Recent Videos ===")
    videos = analytics.get_recent_videos(5)
    print(json.dumps(videos, indent=2))
    
    # Get analytics for latest video (if available)
    if videos and 'error' not in videos[0]:
        latest_video_id = videos[0]['video_id']
        print(f"\n=== Latest Video Analytics ({latest_video_id}) ===")
        video_stats = analytics.get_video_analytics(latest_video_id)
        print(json.dumps(video_stats, indent=2))

if __name__ == "__main__":
    main()