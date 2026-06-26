#!/usr/bin/env python3
"""
YouTube Analytics Report Generator
Generates comprehensive reports combining upload data and analytics
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def generate_comprehensive_report(
    channel_data: Dict,
    video_analytics: List[Dict],
    upload_info: Optional[Dict] = None,
    report_type: str = "weekly"
) -> Dict:
    """
    Generate a comprehensive YouTube report
    
    Args:
        channel_data: Channel statistics from channel_analytics.py
        video_analytics: List of video analytics data
        upload_info: Information about recent uploads (optional)
        report_type: "daily", "weekly", "monthly", or "custom"
        
    Returns:
        Dict containing formatted report data
    """
    
    # Calculate key metrics
    total_views = sum(video.get('views', 0) for video in video_analytics)
    total_likes = sum(video.get('likes', 0) for video in video_analytics)
    total_comments = sum(video.get('comments', 0) for video in video_analytics)
    
    # Find best performing video
    best_video = max(video_analytics, key=lambda x: x.get('views', 0)) if video_analytics else {}
    
    # Calculate engagement rate
    subscriber_count = channel_data.get('subscriber_count', 1)
    avg_engagement_rate = (total_likes + total_comments) / (total_views or 1) * 100 if total_views else 0
    
    report = {
        "report_type": report_type,
        "generated_at": datetime.now().isoformat(),
        "channel_summary": {
            "channel_id": channel_data.get("channel_id"),
            "subscriber_count": channel_data.get("subscriber_count", 0),
            "total_views": channel_data.get("view_count", 0),
            "total_videos": channel_data.get("video_count", 0)
        },
        "period_metrics": {
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "average_engagement_rate": round(avg_engagement_rate, 2),
            "video_count": len(video_analytics)
        },
        "top_performers": {
            "best_video": {
                "video_id": best_video.get("video_id"),
                "views": best_video.get("views", 0),
                "likes": best_video.get("likes", 0),
                "engagement_rate": round(
                    (best_video.get("likes", 0) + best_video.get("comments", 0)) / 
                    (best_video.get("views", 1) or 1) * 100, 2
                ) if best_video else 0
            }
        },
        "recent_uploads": upload_info or {},
        "recommendations": generate_recommendations(channel_data, video_analytics)
    }
    
    return report

def generate_recommendations(channel_data: Dict, video_analytics: List[Dict]) -> List[str]:
    """Generate actionable recommendations based on the data"""
    recommendations = []
    
    # Basic recommendations
    if not video_analytics:
        recommendations.append("Upload your first video to start building your audience!")
        return recommendations
    
    # Engagement analysis
    avg_views = sum(v.get('views', 0) for v in video_analytics) / len(video_analytics)
    if avg_views < 100:
        recommendations.append("Consider optimizing your thumbnails and titles for better click-through rates")
    
    # Subscriber growth
    subscriber_count = channel_data.get('subscriber_count', 0)
    if subscriber_count > 0 and len(video_analytics) > 0:
        conversion_rate = subscriber_count / sum(v.get('views', 0) for v in video_analytics)
        if conversion_rate < 0.01:  # Less than 1% conversion
            recommendations.append("Focus on creating content that encourages subscriptions")
    
    # Content consistency
    if len(video_analytics) >= 3:
        recommendations.append("Maintain consistent upload schedule to build audience retention")
    
    return recommendations

def export_report_to_docx(report_data: Dict, output_path: str):
    """Export report to Word document format"""
    # This would use python-docx library in actual implementation
    # For now, we'll save as JSON
    with open(output_path.replace('.docx', '.json'), 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"Report exported to {output_path.replace('.docx', '.json')}")

if __name__ == "__main__":
    # Example usage
    sample_channel_data = {
        "channel_id": "UC_sample",
        "subscriber_count": 1500,
        "view_count": 45000,
        "video_count": 25
    }
    
    sample_video_analytics = [
        {"video_id": "vid1", "views": 2000, "likes": 150, "comments": 25},
        {"video_id": "vid2", "views": 1500, "likes": 120, "comments": 18},
        {"video_id": "vid3", "views": 3000, "likes": 200, "comments": 45}
    ]
    
    report = generate_comprehensive_report(
        sample_channel_data, 
        sample_video_analytics, 
        report_type="weekly"
    )
    
    print("Generated Report:")
    print(json.dumps(report, indent=2))