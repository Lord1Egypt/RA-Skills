#!/usr/bin/env python3
"""
Social Media Content Generator
Generate platform-specific social media posts with customizable tone and content.
"""

import argparse
import json
import random
import re
from typing import Dict, List, Optional

PLATFORM_CONFIGS = {
    "twitter": {"max_length": 280, "optimal_hashtags": 3, "best_times": ["9AM", "12PM", "5PM"]},
    "instagram": {"max_length": 2200, "optimal_hashtags": 11, "best_times": ["11AM", "7PM"]},
    "linkedin": {"max_length": 3000, "optimal_hashtags": 5, "best_times": ["8AM", "12PM", "5PM"]},
    "facebook": {"max_length": 63206, "optimal_hashtags": 2, "best_times": ["1PM", "8PM"]}
}

CONTENT_TEMPLATES = {
    "announcement": {
        "twitter": ["Big news! {announcement}", "Announcement: {announcement}"],
        "instagram": ["{announcement}\n\nWe're thrilled to share this!", "BIG NEWS! {announcement}\nLink in bio!"],
        "linkedin": ["I'm excited to announce {announcement}\n\nThis is a milestone...", "Big News! {announcement}"],
        "facebook": ["Exciting news!\n\n{announcement}\n\nStay tuned!"]
    },
    "tip": {
        "twitter": ["Quick tip: {tip}", "Pro tip: {tip}"],
        "instagram": ["Daily Tip: {tip}\n\nSave for later! #Tips"],
        "linkedin": ["Tip of the day: {tip}\n\nHere's what I learned..."],
        "facebook": ["Today's Tip: {tip}\n\nShare with friends!"]
    },
    "question": {
        "twitter": ["What's your take on {topic}?", "I'd love to hear thoughts on {topic}"],
        "instagram": ["Question for you:\n{question}\nComment below!"],
        "linkedin": ["Question: {question}\nWhat's your experience?"],
        "facebook": ["Question of the day:\n{question}\nDrop answers below!"]
    },
    "testimonial": {
        "twitter": ["Client success: {testimonial} - {name}"],
        "instagram": ["Client Love\n\"{testimonial}\"\n— {name}\n#ClientSuccess"],
        "linkedin": ["Client Success Story\n\"{testimonial}\"\n— {name}, {title}"],
        "facebook": ["Client Love\n\"{testimonial}\"\n— {name}"]
    },
    "behind_scenes": {
        "twitter": ["Behind the scenes of {topic}..."],
        "instagram": ["Behind the Scenes\nA peek into our process...\n#BTS"],
        "linkedin": ["Behind the scenes\nHere's how we approach {topic}..."],
        "facebook": ["Behind the Scenes\nA peek behind the curtain..."]
    },
    "motivation": {
        "twitter": ["{quote} — {author}"],
        "instagram": ["Daily Motivation\n\"{quote}\"\n— {author}\n#Motivation"],
        "linkedin": ["Monday Motivation\n\"{quote}\"\n— {author}\nLet's make this week count!"],
        "facebook": ["Daily Reminder\n\"{quote}\"\n— {author}\nSave this!"]
    }
}

def generate_content(platform: str, category: str, topic: str, tone: str = "casual") -> str:
    platform, category, tone = platform.lower(), category.lower().replace(" ", "_"), tone.lower()
    templates = CONTENT_TEMPLATES.get(category, CONTENT_TEMPLATES["announcement"])
    platform_templates = templates.get(platform, templates.get("twitter", [""]))
    
    data = {"topic": topic, "announcement": topic, "tip": topic, "question": f"Thoughts on {topic}?",
            "testimonial": f"Great experience with {topic}!", "content": topic, "quote": f"Success with {topic}",
            "author": "Unknown", "product": topic, "description": f"Discover {topic}", "highlight1": "Easy",
            "highlight2": "Fast", "highlight3": "Quality", "link": "link.in.bio", "name": "Customer", "title": "Client"}
    
    template = random.choice(platform_templates)
    try:
        content = template.format(**data)
    except:
        content = template.replace("{topic}", topic)
    if tone == "professional":
        content = re.sub(r'[^\w\s,.\-!?;:\'"()]', '', content)
    return content

def generate_thread(topic: str, num_tweets: int = 5) -> List[str]:
    return [
        f"🧵 {topic}: Everything you need to know (1/{num_tweets})\nLet's dive in",
        f"Point #1: Understanding {topic} is crucial because... (2/{num_tweets})",
        f"Point #2: The biggest mistake with {topic} is... (3/{num_tweets})",
        f"Point #3: Here's what actually works: (4/{num_tweets})",
        f"Key takeaways:\n• {topic} matters\n• Start small\n• Stay consistent\n\nThanks for reading! (5/{num_tweets})"
    ][:num_tweets]

def generate_calendar(theme: str = "general", days: int = 7) -> List[Dict]:
    themes = {
        "general": [
            {"day": "Monday", "type": "Motivation", "suggestion": "Inspiring quote or goal-setting post"},
            {"day": "Tuesday", "type": "Educational", "suggestion": "Share a tip or industry insight"},
            {"day": "Wednesday", "type": "Product/Service", "suggestion": "Highlight a product feature"},
            {"day": "Thursday", "type": "Social Proof", "suggestion": "Share a testimonial or success story"},
            {"day": "Friday", "type": "Behind the Scenes", "suggestion": "Show team or company culture"},
            {"day": "Saturday", "type": "User-Generated", "suggestion": "Repost community content"},
            {"day": "Sunday", "type": "Engagement", "suggestion": "Ask questions, run polls"}
        ]
    }
    return themes.get(theme, themes["general"])[:days]

def main():
    parser = argparse.ArgumentParser(description="Social Media Content Generator")
    parser.add_argument("--platform", "-p", default="twitter", choices=["twitter", "instagram", "linkedin", "facebook"])
    parser.add_argument("--category", "-c", default="announcement", choices=["announcement", "tip", "question", "testimonial", "behind_scenes", "motivation"])
    parser.add_argument("--topic", "-t", required=True)
    parser.add_argument("--tone", default="casual", choices=["professional", "casual", "humorous", "inspirational"])
    parser.add_argument("--thread", action="store_true")
    parser.add_argument("--calendar", action="store_true")
    parser.add_argument("--theme", default="general")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    
    if args.thread:
        print(json.dumps(generate_thread(args.topic), indent=2))
    elif args.calendar:
        print(json.dumps(generate_calendar(args.theme, args.days), indent=2))
    else:
        print(generate_content(args.platform, args.category, args.topic, args.tone))

if __name__ == "__main__":
    main()
