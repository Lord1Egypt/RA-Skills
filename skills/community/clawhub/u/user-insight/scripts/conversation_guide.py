#!/usr/bin/env python3
"""
Conversation guidance for natural insight collection.
Provides strategies to elicit user information through natural chat flow.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

def load_profile(profile_path: str = None) -> Dict:
    """Load user profile."""
    if profile_path is None:
        profile_path = Path.home() / ".openclaw/workspace/memory/user-profile.json"
    else:
        profile_path = Path(profile_path)
    
    if not profile_path.exists():
        return {"interests": [], "basic_info": {}, "exploration_state": {}}
    
    with open(profile_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_missing_info(profile: Dict) -> List[str]:
    """Identify what information is still missing or low confidence."""
    missing = []
    
    # Check basic info
    basic = profile.get("basic_info", {})
    if not basic.get("name"):
        missing.append("name")
    if not basic.get("occupation"):
        missing.append("occupation")
    if not basic.get("location"):
        missing.append("location")
    
    # Check interests depth
    interests = profile.get("interests", [])
    if len(interests) < 3:
        missing.append("more_interests")
    
    # Check preferences
    style = profile.get("communication_style", {})
    if not style.get("preferred_opening"):
        missing.append("opening_preference")
    
    return missing

def generate_guidance_question(missing_info: str, context: str = "") -> str:
    """Generate a natural question to elicit specific information."""
    
    questions = {
        "name": [
            "对了，平时怎么称呼你比较方便？",
            "聊了这么久，还不知道该怎么称呼你呢~",
            "我应该叫你什么比较好？"
        ],
        "occupation": [
            "好奇问下，你平时是做什么工作的？",
            "感觉你对这些挺专业的，是从事相关行业的吗？",
            "聊到这个，突然好奇你的日常是做什么的？"
        ],
        "location": [
            "你在哪个城市？时区对得上吗？",
            "说起来，你现在在哪个地方？",
            "对了，你是在国内还是国外？"
        ],
        "more_interests": [
            "除了我们聊的这些，你平时还关注什么？",
            "工作之外，你一般怎么放松？",
            "如果有个下午完全空闲，你最可能做什么？"
        ],
        "opening_preference": [
            "我有时候想主动找你聊天，你喜欢我直接说事，还是先寒暄一下？",
            "你觉得什么样的开场比较舒服？",
            "如果我突然发个消息给你，希望是什么风格？"
        ],
        "weekend_routine": [
            "周末一般怎么安排？",
            "工作日和周末的状态差别大吗？",
            "最近有去哪里玩或者计划做什么吗？"
        ],
        "stress_relief": [
            "压力大的时候你一般怎么调节？",
            "有什么事情是你觉得特别解压的？",
            "心情不好的时候会做什么？"
        ],
        "learning_style": [
            "你学新东西喜欢先看理论还是直接上手试？",
            "如果我要教你一个新技能，你希望我怎么讲？",
            "你觉得自己是视觉型、听觉型还是动手型的学习者？"
        ]
    }
    
    if missing_info in questions:
        return random.choice(questions[missing_info])
    
    return "能跟我多聊聊你自己吗？"

def suggest_follow_up_strategy(user_response: str, topic: str) -> str:
    """Suggest how to continue the conversation based on user response."""
    
    response_length = len(user_response)
    has_detail = any(marker in user_response for marker in ["因为", "所以", "比如", "像", "会"])
    has_emotion = any(marker in user_response for marker in ["喜欢", "讨厌", "开心", "烦", "累", "兴奋"])
    
    strategies = []
    
    if response_length < 10:
        strategies.append("用户回复简短，可能需要换个角度或先分享自己再引导")
    elif has_detail:
        strategies.append("用户愿意展开，可以深入追问具体例子")
    else:
        strategies.append("用户参与但较克制，可以先认同再引导更多细节")
    
    if has_emotion:
        strategies.append("检测到情绪词，这是重要信号，记录并适时共情")
    
    return " | ".join(strategies)

def generate_casual_opener(profile: Dict, time_context: str = "") -> str:
    """Generate a casual greeting/check-in message."""
    
    # Get known interests for personalization
    interests = profile.get("interests", [])
    top_interest = interests[0]["topic"] if interests else ""
    
    openers = {
        "morning": [
            "早！今天有什么计划吗？",
            "早上好~ 刚想到你可能也起床了",
            "早啊，昨晚休息得怎么样？"
        ],
        "work_hours": [
            "忙完了吗？偷闲一下~",
            "在忙不？有个小事想问你",
            "工作间隙，来摸个鱼😄"
        ],
        "evening": [
            "晚上好！今天过得怎么样？",
            "下班了吗？",
            "晚上一般怎么安排？"
        ],
        "late_night": [
            "还没睡？夜猫子啊",
            "这么晚还在线，是在忙还是睡不着？",
            "深夜党你好👋"
        ],
        "weekend": [
            "周末愉快！有什么安排吗？",
            "休息日一般怎么过？",
            "周末有没有出门走走？"
        ],
        "interest_based": [
            f"刚看到个关于{top_interest}的新闻，想听听你的看法",
            f"突然好奇，你平时是怎么关注到{top_interest}这类信息的？",
            f"最近在研究{top_interest}，发现你可能比我懂..."
        ] if top_interest else []
    }
    
    # Select based on context
    if time_context and time_context in openers:
        candidates = openers[time_context]
        if time_context != "interest_based" and openers["interest_based"]:
            # 30% chance to use interest-based opener
            if random.random() < 0.3:
                candidates = openers["interest_based"]
        return random.choice(candidates)
    
    # Default: general casual
    general = ["在干嘛？", "忙不忙？", "有空聊两句吗？"]
    return random.choice(general)

def should_initiate_check_in(profile: Dict) -> bool:
    """Determine if it's appropriate to initiate a casual check-in."""
    
    last_interaction = profile.get("interaction_stats", {}).get("last_interaction")
    if last_interaction:
        last_time = datetime.fromisoformat(last_interaction)
        hours_passed = (datetime.now() - last_time).total_seconds() / 3600
        
        # Don't be too frequent
        if hours_passed < 6:
            return False
        
        # Good windows: morning (8-10), lunch (12-14), evening (18-22)
        current_hour = datetime.now().hour
        good_windows = [8, 9, 12, 13, 18, 19, 20, 21]
        
        if current_hour in good_windows and hours_passed > 12:
            return True
    
    return False

def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Conversation guidance")
    parser.add_argument("--missing", action="store_true", help="Get missing info questions")
    parser.add_argument("--opener", type=str, help="Generate casual opener (morning/work/evening/late_night/weekend)")
    parser.add_argument("--check-in", action="store_true", help="Check if should initiate check-in")
    parser.add_argument("--strategy", nargs=2, metavar=("RESPONSE", "TOPIC"), help="Get follow-up strategy")
    
    args = parser.parse_args()
    
    profile = load_profile()
    
    if args.missing:
        missing = get_missing_info(profile)
        result = {
            "missing_fields": missing,
            "suggested_questions": [generate_guidance_question(m) for m in missing[:3]]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.opener:
        opener = generate_casual_opener(profile, args.opener)
        print(json.dumps({"opener": opener}, ensure_ascii=False))
    
    elif args.check_in:
        should_check = should_initiate_check_in(profile)
        result = {"should_check_in": should_check}
        if should_check:
            result["suggested_opener"] = generate_casual_opener(profile)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.strategy:
        strategy = suggest_follow_up_strategy(args.strategy[0], args.strategy[1])
        print(json.dumps({"strategy": strategy}, ensure_ascii=False))
    
    else:
        # Default: show what's missing
        missing = get_missing_info(profile)
        print(json.dumps({
            "missing_fields": missing,
            "next_question": generate_guidance_question(missing[0]) if missing else None
        }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
