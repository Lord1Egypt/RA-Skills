#!/usr/bin/env python3
"""
Social Media Scheduler
Post queue management for cross-platform scheduling
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class PostQueue:
    def __init__(self, queue_file: str = "queue.json"):
        self.queue_file = queue_file
        self.queue = self.load_queue()
    
    def load_queue(self) -> List[Dict]:
        try:
            with open(self.queue_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_queue(self):
        with open(self.queue_file, 'w') as f:
            json.dump(self.queue, f, indent=2)
    
    def add_post(self, content: str, platforms: List[str], scheduled_time: Optional[datetime] = None):
        post = {
            "id": len(self.queue) + 1,
            "content": content,
            "platforms": platforms,
            "scheduled_time": scheduled_time.isoformat() if scheduled_time else datetime.now().isoformat(),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self.queue.append(post)
        self.save_queue()
        return post
    
    def get_pending(self) -> List[Dict]:
        return [p for p in self.queue if p["status"] == "pending"]
    
    def mark_posted(self, post_id: int):
        for post in self.queue:
            if post["id"] == post_id:
                post["status"] = "posted"
                post["posted_at"] = datetime.now().isoformat()
        self.save_queue()

# Best posting times by platform
BEST_TIMES = {
    "twitter": [9, 12, 18],
    "instagram": [11, 14, 19],
    "tiktok": [6, 7, 8, 19, 20, 21],
    "linkedin": [9, 10, 11, 12],
    "facebook": [13, 14, 15, 16]
}

def suggest_best_time(platform: str) -> datetime:
    """Suggest the next best posting time"""
    now = datetime.now()
    best_hours = BEST_TIMES.get(platform.lower(), [9, 12, 18])
    
    for hour in best_hours:
        candidate = now.replace(hour=hour, minute=0, second=0)
        if candidate > now:
            return candidate
    
    return now + timedelta(days=1)

if __name__ == "__main__":
    queue = PostQueue()
    print(f"Queue has {len(queue.queue)} posts")
    print(f"Pending: {len(queue.get_pending())}")
