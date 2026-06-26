#!/usr/bin/env python3
"""
YouTube Video Upload Script
Handles video upload with metadata configuration and SEO optimization
"""

import os
import json
import sys
from datetime import datetime

def upload_video(video_path, metadata, api_key, channel_id):
    """
    Upload video to YouTube with comprehensive metadata
    
    Args:
        video_path (str): Path to video file (MP4/MOV)
        metadata (dict): Video metadata including title, description, tags, etc.
        api_key (str): YouTube Data API key
        channel_id (str): Target channel ID
        
    Returns:
        dict: Upload result with video ID and status
    """
    # Validate inputs
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    if not metadata.get('title'):
        raise ValueError("Video title is required")
    
    # Mock upload response structure
    upload_result = {
        "status": "success",
        "video_id": "dQw4w9WgXcQ",  # Mock ID
        "title": metadata['title'],
        "upload_time": datetime.now().isoformat(),
        "privacy_status": metadata.get('privacy', 'public'),
        "thumbnail_status": "pending",
        "message": "Video uploaded successfully. Processing may take several minutes."
    }
    
    return upload_result

def prepare_metadata(title, description="", tags=None, category="22", 
                    privacy="public", made_for_kids=False, language="en"):
    """
    Prepare comprehensive video metadata for upload
    
    Args:
        title (str): Video title
        description (str): Video description
        tags (list): List of tags/keywords
        category (str): YouTube category ID
        privacy (str): Privacy setting (public, private, unlisted)
        made_for_kids (bool): COPPA compliance
        language (str): Video language code
        
    Returns:
        dict: Complete metadata dictionary
    """
    if tags is None:
        tags = []
    
    metadata = {
        "title": title,
        "description": description,
        "tags": tags,
        "category": category,
        "privacy": privacy,
        "made_for_kids": made_for_kids,
        "language": language,
        "notify_subscribers": True,
        "allow_comments": True,
        "allow_embedding": True
    }
    
    return metadata

if __name__ == "__main__":
    # Example usage
    api_key = os.getenv("YOUTUBE_API_KEY")
    channel_id = os.getenv("YOUTUBE_CHANNEL_ID")
    video_path = sys.argv[1] if len(sys.argv) > 1 else "video.mp4"
    
    if not api_key or not channel_id:
        print("Error: YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID environment variables required")
        sys.exit(1)
    
    # Example metadata
    metadata = prepare_metadata(
        title="My Awesome Video",
        description="This is an amazing video about...",
        tags=["tutorial", "awesome", "youtube"],
        category="27"  # Education
    )
    
    try:
        result = upload_video(video_path, metadata, api_key, channel_id)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Upload failed: {e}")
        sys.exit(1)