#!/usr/bin/env python3
"""
塔罗牌占卜脚本
包含78张塔罗牌（22张大阿卡纳 + 56张小阿卡纳）的占卜功能
"""

import random
import json
import os
import sys
import datetime

# 塔罗牌数据库
# 这里暂时用简化版本，完整版本需要更丰富的数据库
TAROT_DATABASE = {
    "major": [
        {
            "name": "愚人",
            "english": "The Fool",
            "ascii_art": """
   ☆
 ╭────╮
 │    │
 │ ᠰ  │
 │    │
 ╰────╯
 旅行者
""",
            "keywords": ["冒险", "新开始", "天真", "自由"],
            "meaning": "新的开始、冒险、天真、勇气、信任",
            "reverse_meaning": "鲁莽、不切实际、缺乏计划、过度冒险",
            "advice": "敢于尝试新事物，但要保持谨慎"
        },
        {
            "name": "魔术师",
            "english": "The Magician",
            "ascii_art": """
   ✨
 ╭────╮
 │ ᠰ  │
 │◎◎◎│
 │ ᠰ  │
 ╰────╯
 创造者
""",
            "keywords": ["创造力", "意志", "技能", "专注"],
            "meaning": "创造力、意志、技能、专注、机会",
            "reverse_meaning": "欺骗、缺乏自信、浪费机会、不专注",
            "advice": "相信自己的能力，专注目标，积极行动"
        },
        {
            "name": "女祭司",
            "english": "The High Priestess",
            "ascii_art": """
   🌙
 ╭────╮
 │ᠰ 🌙│
 │    │
 │ ᠰ  │
 ╰────╯
 直觉
""",
            "keywords": ["直觉", "智慧", "神秘", "潜意识"],
            "meaning": "直觉、智慧、神秘、潜意识、沉默",
            "reverse_meaning": "秘密、隐藏、压抑、隐瞒、不信任",
            "advice": "相信直觉，倾听内在的声音"
        }
    ],
    "minor": {
        "cups": [
            {
                "name": "圣杯王牌",
                "english": "Ace of Cups",
                "ascii_art": """
   💧
 ╭────╮
 │ ᠰ  │
 │ 🍶 │
 │ ᠰ  │
 ╰────╯
 新爱
""",
                "keywords": ["新爱", "情感", "幸福", "机会"],
                "meaning": "新的爱情、情感、幸福、机会、灵感",
                "reverse_meaning": "情感受阻、失去灵感、爱的困难",
                "advice": "迎接新的情感机会，保持开放心态"
            }
        ]
    }
}

# 占卜主题
DIVINATION_TYPES = {
    "love": ["爱情", "情感", "恋爱", "婚姻", "人际关系", "亲密关系"],
    "career": ["事业", "工作", "职业", "职场", "发展", "工作机会"],
    "health": ["健康", "身体", "心理", "养生", "疾病", "康复"],
    "finance": ["财运", "金钱", "投资", "理财", "财富", "经济"],
    "spiritual": ["灵性", "成长", "自我", "精神", "心灵", "修行"],
    "decision": ["选择", "决定", "判断", "抉择", "决定", "选项"]
}

def draw_tarot_card(divination_type=None):
    """随机抽取一张塔罗牌"""
    
    # 随机选择牌组和牌
    card_group = random.choice(["major", "minor"])
    
    if card_group == "major":
        card = random.choice(TAROT_DATABASE["major"])
    else:
        # 选择小阿卡纳牌组
        deck_type = random.choice(["cups", "wands", "swords", "pentacles"])
        card = random.choice(TAROT_DATABASE["minor"][deck_type])
    
    # 随机决定正逆位（30%概率逆位）
    is_reversed = random.random() < 0.3
    
    # 获取占卜主题
    if divination_type and divination_type in DIVINATION_TYPES:
        topic = random.choice(DIVINATION_TYPES[divination_type])
    else:
        topic = "未知"
    
    # 根据占卜主题调整解读
    if is_reversed:
        meaning = f"{card['reverse_meaning']}。在{topic}方面，可能需要更加谨慎"
        advice = f"{card['advice']}。面对{topic}问题时，注意潜在的挑战"
    else:
        meaning = f"{card['meaning']}。在{topic}方面，这是一个积极的机会"
        advice = f"{card['advice']}。对于{topic}问题，这是一个好的开始"
    
    return {
        "card": card,
        "reversed": is_reversed,
        "topic": topic,
        "meaning": meaning,
        "advice": advice
    }

def draw_three_card_spread(divination_type=None):
    """抽取三张牌牌阵"""
    cards = []
    
    for position in ["过去", "现在", "未来"]:
        card_info = draw_tarot_card(divination_type)
        card_info["position"] = position
        cards.append(card_info)
    
    return cards

def draw_cross_spread(divination_type=None):
    """抽取十字牌阵"""
    positions = ["核心问题", "影响因素", "可能结果", "建议指引", "基础情况"]
    cards = []
    
    for position in positions:
        card_info = draw_tarot_card(divination_type)
        card_info["position"] = position
        cards.append(card_info)
    
    return cards

def display_single_card(card_info):
    """显示单张牌占卜结果"""
    
    reversed_symbol = "🔁" if card_info["reversed"] else "✓"
    
    output = f"""
🎴 塔罗牌占卜 🎴
═══════════════════════════════════════════
🔮 问题：{card_info['topic']}
═══════════════════════════════════════════

🃏 抽到的牌：{card_info['card']['name']} ({card_info['card']['english']})
📍 牌位：{reversed_symbol} {'逆位' if card_info['reversed'] else '正位'}

💫 关键词：{', '.join(card_info['card']['keywords'])}

{card_info['card']['ascii_art']}

💡 牌义解读：
    {card_info['meaning']}

✅ 建议指引：
    {card_info['advice']}

📅 占卜时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    return output

def display_three_card_spread(cards):
    """显示三张牌牌阵结果"""
    
    output = f"""
🎴 塔罗牌占卜 🎴
═══════════════════════════════════════════
🔮 牌阵：三张牌牌阵（过去、现在、未来）
═══════════════════════════════════════════
"""
    
    for card_info in cards:
        reversed_symbol = "🔁" if card_info["reversed"] else "✓"
        
        output += f"""

【{card_info['position']}】
═══════════════════════════════════════════
🃏 牌：{card_info['card']['name']}
📍 牌位：{reversed_symbol} {'逆位' if card_info['reversed'] else '正位'}

💫 关键词：{', '.join(card_info['card']['keywords'])}

💡 牌义解读：
    {card_info['meaning']}

✅ 建议指引：
    {card_info['advice']}
"""
    
    output += f"""
📅 占卜时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    return output

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python tarot.py single <占卜主题>")
        print("  python tarot.py three <占卜主题>")
        print("  python tarot.py cross <占卜主题>")
        print("")
        print("占卜主题可选：love, career, health, finance, spiritual, decision")
        return
    
    spread_type = sys.argv[1]
    divination_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    if spread_type == "single":
        card_info = draw_tarot_card(divination_type)
        print(display_single_card(card_info))
    elif spread_type == "three":
        cards = draw_three_card_spread(divination_type)
        print(display_three_card_spread(cards))
    elif spread_type == "cross":
        cards = draw_cross_spread(divination_type)
        # 暂时简化显示十字牌阵
        print(f"十字牌阵占卜 - {divination_type}")
        for card_info in cards:
            print(f"\n{card_info['position']}: {card_info['card']['name']} ({'逆位' if card_info['reversed'] else '正位'})")
    else:
        print("未知牌阵类型！请使用 single, three 或 cross")

if __name__ == "__main__":
    main()