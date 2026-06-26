#!/usr/bin/env python3
"""
Content Calendar Planner - Plan and schedule social media content
Usage:
    python calendar_planner.py --month 2026-03
    python calendar_planner.py --week 12
    python calendar_planner.py --add "Monday" "tech tip"
    python calendar_planner.py --platforms twitter instagram linkedin
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# Content themes by day of week
WEEKLY_THEMES = {
    "monday": {"theme": "Motivation", "focus": "Goals, fresh starts", "type": "quote, inspiration"},
    "tuesday": {"theme": "Educational", "focus": "Tips, how-to content", "type": "tutorial, tips"},
    "wednesday": {"theme": "Product/Feature", "focus": "Showcase offerings", "type": "feature, product"},
    "thursday": {"theme": "Community", "focus": "User stories, UGC", "type": "testimonial, UGC"},
    "friday": {"theme": "Engagement", "focus": "Questions, polls", "type": "poll, question, fun"},
    "saturday": {"theme": "Behind-the-Scenes", "focus": "Team, culture", "type": "BTS, team"},
    "sunday": {"theme": "Curated/Planning", "focus": "Repurpose, reflect", "type": "repurpose, recap"}
}

# Monthly content themes
MONTHLY_THEMES = {
    1: "New Year, Goals, Fresh Starts",
    2: "Love, Relationships, Community",
    3: "Spring, Growth, New Beginnings",
    4: "Spring, Nature, Renewal",
    5: "Mother's Day, Appreciation",
    6: "Summer, Vacations, Travel",
    7: "Independence, Freedom",
    8: "Back to School, Preparation",
    9: "New Season, Transitions",
    10: "Halloween, Fall, Spooky",
    11: "Gratitude, Thanksgiving",
    12: "Holiday Season, Celebration"
}

# Platform best posting times (UTC - adjust for local)
BEST_TIMES = {
    "twitter": ["09:00", "12:00", "17:00"],
    "instagram": ["11:00", "14:00", "19:00"],
    "linkedin": ["08:00", "10:00", "12:00"],
    "facebook": ["09:00", "13:00", "16:00"]
}

# Content pillars
CONTENT_PILLARS = [
    "Educational", "Entertainment", "Promotional", 
    "Community", "Behind-the-Scenes", "User Generated"
]


def generate_weekly_calendar(week: int = None, year: int = None, platforms: list = None) -> dict:
    """Generate a weekly content calendar."""
    if not year:
        year = datetime.now().year
    if not week:
        week = datetime.now().isocalendar()[1]
    
    # Get Monday of the week
    jan1 = datetime(year, 1, 1)
    monday = jan1 + timedelta(weeks=week - 1)
    monday = monday - timedelta(days=monday.weekday())
    
    calendar = {
        "week": week,
        "year": year,
        "start_date": monday.strftime("%Y-%m-%d"),
        "platforms": platforms or ["twitter", "instagram", "linkedin"],
        "posts": []
    }
    
    for day_idx, (day_name, theme_info) in enumerate(WEEKLY_THEMES.items()):
        date = monday + timedelta(days=day_idx)
        day_posts = []
        
        for platform in calendar["platforms"]:
            post = {
                "day": day_name.capitalize(),
                "date": date.strftime("%Y-%m-%d"),
                "platform": platform,
                "theme": theme_info["theme"],
                "focus": theme_info["focus"],
                "content_type": theme_info["type"],
                "best_time": BEST_TIMES.get(platform, ["12:00"])[day_idx % 3],
                "content_pillars": CONTENT_PILLARS[day_idx % len(CONTENT_PILLARS)]
            }
            day_posts.append(post)
        
        calendar["posts"].extend(day_posts)
    
    return calendar


def generate_monthly_calendar(month: int = None, year: int = None, platforms: list = None) -> dict:
    """Generate a monthly content calendar."""
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    # Get first day of month
    first_day = datetime(year, month, 1)
    # Get last day of month
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    days_in_month = last_day.day
    
    calendar = {
        "month": month,
        "year": year,
        "month_name": first_day.strftime("%B"),
        "theme": MONTHLY_THEMES.get(month, "General Content"),
        "platforms": platforms or ["twitter", "instagram", "linkedin", "facebook"],
        "posts": [],
        "stats": {"total_posts": 0, "by_platform": {}, "by_type": defaultdict(int)}
    }
    
    for day in range(1, days_in_month + 1):
        date = datetime(year, month, day)
        day_name = date.strftime("%A").lower()
        week_num = date.isocalendar()[1]
        
        # Skip weekends for daily posting (optional)
        # if day_name in ["saturday", "sunday"]:
        #     continue
        
        theme_info = WEEKLY_THEMES.get(day_name, WEEKLY_THEMES["monday"])
        
        for platform in calendar["platforms"]:
            # Adjust frequency based on platform
            freq = {"twitter": 2, "instagram": 1, "linkedin": 1, "facebook": 1}
            posts_today = freq.get(platform, 1)
            
            for p in range(posts_today):
                post = {
                    "day": day,
                    "date": date.strftime("%Y-%m-%d"),
                    "weekday": day_name.capitalize(),
                    "platform": platform,
                    "theme": theme_info["theme"],
                    "content_type": theme_info["type"],
                    "best_time": BEST_TIMES.get(platform, ["12:00"])[p % 3],
                    "content_pillar": CONTENT_PILLARS[(day + p) % len(CONTENT_PILLARS)]
                }
                calendar["posts"].append(post)
                calendar["stats"]["total_posts"] += 1
                calendar["stats"]["by_platform"][platform] = calendar["stats"]["by_platform"].get(platform, 0) + 1
                calendar["stats"]["by_type"][theme_info["type"]] += 1
    
    return calendar


def generate_content_ideas(topic: str, num_ideas: int = 10) -> dict:
    """Generate content ideas for a topic."""
    idea_templates = [
        f"5 Tips for {topic}",
        f"How {topic} Changed My Business",
        f"The Ultimate Guide to {topic}",
        f"Common Mistakes in {topic} (And How to Fix Them)",
        f"Why {topic} Matters in 2026",
        f"{topic}: What You Need to Know",
        f"Behind the Scenes: Our {topic} Process",
        f"Customer Success: How They Used {topic}",
        f"The Future of {topic}",
        f"Q&A: Your Questions About {topic}",
        f"{topic} vs Competition: Which is Better?",
        f"7 Facts About {topic} You Didn't Know"
    ]
    
    ideas = []
    for i, template in enumerate(idea_templates[:num_ideas]):
        ideas.append({
            "id": i + 1,
            "title": template,
            "format": ["blog", "social post", "video", "infographic"][i % 4],
            "platform": ["LinkedIn", "Twitter", "Instagram", "Facebook"][i % 4],
            "estimated_engagement": ["high", "medium", "high", "medium"][i % 4]
        })
    
    return {"topic": topic, "ideas": ideas, "count": len(ideas)}


def add_custom_post(calendar: dict, day: str, content: str, platform: str = None) -> dict:
    """Add a custom post to calendar."""
    post = {
        "day": day,
        "content": content,
        "platform": platform,
        "custom": True
    }
    if "custom_posts" not in calendar:
        calendar["custom_posts"] = []
    calendar["custom_posts"].append(post)
    return calendar


def main():
    parser = argparse.ArgumentParser(description="Content Calendar Planner")
    parser.add_argument("--week", type=int, help="Week number (1-52)")
    parser.add_argument("--month", help="Month in YYYY-MM format")
    parser.add_argument("--year", type=int, help="Year")
    parser.add_argument("--platforms", nargs="+", choices=["twitter", "instagram", "linkedin", "facebook"],
                        default=["twitter", "instagram", "linkedin"])
    parser.add_argument("--ideas", help="Generate content ideas for a topic")
    parser.add_argument("--output", "-o", help="Output JSON file")
    args = parser.parse_args()

    if args.month:
        try:
            year, month = map(int, args.month.split("-"))
            result = generate_monthly_calendar(month, year, args.platforms)
        except:
            print("Error: Use YYYY-MM format for month")
            sys.exit(1)
    elif args.ideas:
        result = generate_content_ideas(args.ideas)
    else:
        result = generate_weekly_calendar(args.week, args.year, args.platforms)

    result["generated_at"] = datetime.now().isoformat()
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"✓ Calendar saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
