#!/usr/bin/env python3
"""
Hashtag Tool - Research and generate relevant hashtags
Usage:
    python hashtag_tool.py --niche "technology"
    python hashtag_tool.py --topic "AI productivity"
    python hashtag_tool.py --generate-mix --topic "digital marketing"
"""

import argparse
import json
import random
import sys
from datetime import datetime

# Hashtag database with reach estimates
HASHTAG_DATABASE = {
    "tech": {
        "broad": [("#Tech", 150000000), ("#Technology", 100000000), ("#Innovation", 80000000)],
        "medium": [("#Startup", 30000000), ("#AI", 25000000), ("#MachineLearning", 20000000)],
        "niche": [("#TechStartup", 2000000), ("#CodingLife", 800000), ("#DeveloperLife", 600000)]
    },
    "business": {
        "broad": [("#Business", 90000000), ("#Entrepreneur", 70000000), ("#Success", 60000000)],
        "medium": [("#Leadership", 25000000), ("#Growth", 20000000), ("#Marketing", 15000000)],
        "niche": [("#StartupLife", 1200000), ("#SideHustle", 250000), ("#OnlineBusiness", 200000)]
    },
    "lifestyle": {
        "broad": [("#Lifestyle", 150000000), ("#Life", 140000000), ("#Love", 130000000)],
        "medium": [("#Inspiration", 60000000), ("#Goals", 40000000), ("#Mindset", 35000000)],
        "niche": [("#LifestyleBlog", 3000000), ("#SelfLoveJourney", 1500000), ("#DailyInspiration", 300000)]
    },
    "food": {
        "broad": [("#Food", 500000000), ("#Foodie", 200000000), ("#Yummy", 150000000)],
        "medium": [("#FoodPhotography", 50000000), ("#FoodBlog", 30000000), ("#InstaFood", 12000000)],
        "niche": [("#HomeCooking", 1200000), ("#FoodBlogger", 400000), ("#RecipeShare", 300000)]
    },
    "travel": {
        "broad": [("#Travel", 600000000), ("#Adventure", 150000000), ("#Explore", 100000000)],
        "medium": [("#TravelPhotography", 40000000), ("#TravelBlog", 25000000), ("#Vacation", 20000000)],
        "niche": [("#TravelTips", 3000000), ("#SoloTravel", 2500000), ("#HiddenGems", 400000)]
    },
    "education": {
        "broad": [("#Education", 100000000), ("#Learning", 80000000), ("#Knowledge", 60000000)],
        "medium": [("#Teacher", 25000000), ("#OnlineLearning", 12000000), ("#EdTech", 10000000)],
        "niche": [("#StudentLife", 1000000), ("#StudyGram", 600000), ("#LearnToCode", 250000)]
    },
    "marketing": {
        "broad": [("#Marketing", 50000000), ("#DigitalMarketing", 35000000), ("#SocialMedia", 30000000)],
        "medium": [("#ContentMarketing", 15000000), ("#MarketingTips", 12000000), ("#GrowthHacking", 3500000)],
        "niche": [("#DigitalMarketer", 1500000), ("#SEOTips", 300000), ("#ContentTips", 250000)]
    },
    "fitness": {
        "broad": [("#Fitness", 500000000), ("#Health", 400000000), ("#Workout", 150000000)],
        "medium": [("#FitFam", 60000000), ("#Wellness", 50000000), ("#FitnessMotivation", 40000000)],
        "niche": [("#HomeWorkout", 3000000), ("#FitnessTips", 2500000), ("#FitnessGoals", 1500000)]
    },
    "fashion": {
        "broad": [("#Fashion", 1000000000), ("#Style", 800000000), ("#Ootd", 400000000)],
        "medium": [("#FashionStyle", 60000000), ("#StreetStyle", 50000000), ("#Trends", 25000000)],
        "niche": [("#FashionTips", 3000000), ("#StyleTips", 2500000), ("#OutfitIdeas", 2000000)]
    }
}

PLATFORM_LIMITS = {
    "twitter": {"optimal": 2}, "instagram": {"optimal": 11}, 
    "linkedin": {"optimal": 3}, "facebook": {"optimal": 2}
}

KEYWORDS_MAP = {
    "tech": ["tech", "ai", "software", "code", "digital"],
    "business": ["business", "entrepreneur", "startup", "money", "marketing"],
    "lifestyle": ["life", "style", "living", "inspiration", "motivation"],
    "food": ["food", "eat", "cook", "recipe", "coffee"],
    "travel": ["travel", "trip", "vacation", "adventure", "explore"],
    "education": ["learn", "study", "education", "school", "course"],
    "marketing": ["marketing", "social media", "brand", "content", "seo"],
    "fitness": ["fitness", "workout", "gym", "health", "exercise"],
    "fashion": ["fashion", "style", "clothes", "outfit", "trend"]
}

def detect_category(topic: str) -> str:
    topic_lower = topic.lower()
    for cat, kws in KEYWORDS_MAP.items():
        for kw in kws:
            if kw in topic_lower:
                return cat
    return "tech"

def generate_mixed_bundle(niche: str, platform: str = "instagram") -> list:
    if niche not in HASHTAG_DATABASE:
        niche = "tech"
    data = HASHTAG_DATABASE[niche]
    opt = PLATFORM_LIMITS.get(platform, {"optimal": 11})["optimal"]
    broad = random.sample(data["broad"], min(2, len(data["broad"])))
    medium = random.sample(data["medium"], min(4, len(data["medium"])))
    niche_tags = random.sample(data["niche"], min(opt - 2, len(data["niche"])))
    return [h[0] for h in broad + medium + niche_tags][:opt]

def generate_trending_mix(topic: str, platform: str = "instagram") -> dict:
    category = detect_category(topic)
    bundle = generate_mixed_bundle(category, platform)
    return {"topic": topic, "category": category, "hashtags": bundle, "platform": platform}

def main():
    parser = argparse.ArgumentParser(description="Hashtag Tool")
    parser.add_argument("--niche", help="Niche category")
    parser.add_argument("--topic", help="Topic for hashtag generation")
    parser.add_argument("--platform", choices=["twitter", "instagram", "linkedin", "facebook"], default="instagram")
    parser.add_argument("--generate-mix", action="store_true", help="Generate mixed hashtag bundle")
    parser.add_argument("--output", "-o", help="Output JSON file")
    args = parser.parse_args()

    if args.niche:
        result = get_hashtags_by_niche(args.niche, args.platform)
    elif args.topic and args.generate_mix:
        result = generate_trending_mix(args.topic, args.platform)
    elif args.topic:
        result = generate_trending_mix(args.topic, args.platform)
    else:
        print("Error: Specify --niche or --topic")
        sys.exit(1)

    result["generated_at"] = datetime.now().isoformat()
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"✓ Saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))

def get_hashtags_by_niche(niche: str, platform: str = None) -> dict:
    niche_lower = niche.lower()
    category = None
    for key in HASHTAG_DATABASE:
        if key in niche_lower or niche_lower in key:
            category = key
            break
    if not category:
        return {"error": f"Niche '{niche}' not found"}
    data = HASHTAG_DATABASE[category]
    result = {"niche": category, "hashtags": {"broad": [h[0] for h in data["broad"]], "medium": [h[0] for h in data["medium"]], "niche": [h[0] for h in data["niche"]]}}
    if platform:
        result["recommended"] = generate_mixed_bundle(category, platform)
    return result

if __name__ == "__main__":
    main()
