#!/usr/bin/env python3
"""
星座配对计算脚本
基于星座元素和传统配对理论，计算两个星座的爱情匹配度
"""

import random
import sys

# 星座数据库
ZODIAC_DATA = {
    "白羊座": {
        "name": "白羊座",
        "element": "火",
        "english": "Aries",
        "element_en": "Fire",
        "description": "热情、勇敢、冒险精神、行动力强、乐观",
        "strengths": "热情、勇敢、冒险、行动力强",
        "weaknesses": "冲动、急躁、缺乏耐心、自我为中心"
    },
    "金牛座": {
        "name": "金牛座",
        "element": "土",
        "english": "Taurus",
        "element_en": "Earth",
        "description": "踏实、稳重、注重实际、擅长理财、忠诚",
        "strengths": "踏实、稳重、务实、忠诚",
        "weaknesses": "固执、保守、不喜欢变化、占有欲强"
    },
    "双子座": {
        "name": "双子座",
        "element": "风",
        "english": "Gemini",
        "element_en": "Air",
        "description": "聪明、灵活、社交能力强、好奇心强、多才多艺",
        "strengths": "聪明、灵活、社交能力强",
        "weaknesses": "善变、注意力分散、不够专注"
    },
    "巨蟹座": {
        "name": "巨蟹座",
        "element": "水",
        "english": "Cancer",
        "element_en": "Water",
        "description": "感性、温柔、家庭观念强、体贴、记忆力好",
        "strengths": "感性、温柔、家庭观念强",
        "weaknesses": "情绪化、敏感、过于依赖、优柔寡断"
    },
    "狮子座": {
        "name": "狮子座",
        "element": "火",
        "english": "Leo",
        "element_en": "Fire",
        "description": "自信、大方、领导力强、热情、慷慨",
        "strengths": "自信、大方、领导力强",
        "weaknesses": "骄傲、爱面子、自我为中心、控制欲强"
    },
    "处女座": {
        "name": "处女座",
        "element": "土",
        "english": "Virgo",
        "element_en": "Earth",
        "description": "细心、逻辑清晰、追求完美、有条理、务实",
        "strengths": "细心、逻辑清晰、追求完美",
        "weaknesses": "挑剔、过于谨慎、完美主义、焦虑"
    },
    "天秤座": {
        "name": "天秤座",
        "element": "风",
        "english": "Libra",
        "element_en": "Air",
        "description": "和谐、美感、公正、平衡、优雅",
        "strengths": "和谐、公正、平衡、优雅",
        "weaknesses": "犹豫、优柔寡断、过于追求平衡、依赖性强"
    },
    "天蝎座": {
        "name": "天蝎座",
        "element": "水",
        "english": "Scorpio",
        "element_en": "Water",
        "description": "深情、洞察力强、神秘、专注、坚韧",
        "strengths": "深情、洞察力强、神秘、专注",
        "weaknesses": "极端、嫉妒心强、报复心、控制欲"
    },
    "射手座": {
        "name": "射手座",
        "element": "火",
        "english": "Sagittarius",
        "element_en": "Fire",
        "description": "乐观、自由、探索精神、幽默、冒险精神",
        "strengths": "乐观、自由、探索精神",
        "weaknesses": "不够专一、不喜约束、责任感不足、浮躁"
    },
    "摩羯座": {
        "name": "摩羯座",
        "element": "土",
        "english": "Capricorn",
        "element_en": "Earth",
        "description": "务实、有计划、目标导向、责任感强、耐心",
        "strengths": "务实、有计划、目标导向",
        "weaknesses": "过于严肃、悲观、保守、固执"
    },
    "水瓶座": {
        "name": "水瓶座",
        "element": "风",
        "english": "Aquarius",
        "element_en": "Air",
        "description": "创新、理想主义、独特思维、公正、人道主义",
        "strengths": "创新、理想主义、独特思维",
        "weaknesses": "固执己见、不合群、过于理性、情感不足"
    },
    "双鱼座": {
        "name": "双鱼座",
        "element": "水",
        "english": "Pisces",
        "element_en": "Water",
        "description": "浪漫、艺术感、理想主义、善良、情感丰富",
        "strengths": "浪漫、艺术感、理想主义",
        "weaknesses": "优柔寡断、不切实际、过于依赖、逃避现实"
    }
}

# 星座配对基础匹配度
BASE_COMPATIBILITY = {
    ("白羊座", "狮子座", "白羊座", "狮子座"): 85,
    ("金牛座", "处女座", "金牛座", "处女座"): 90,
    ("双子座", "水瓶座", "双子座", "水瓶座"): 80,
    ("巨蟹座", "天蝎座", "巨蟹座", "天蝎座"): 85,
    ("狮子座", "射手座", "狮子座", "射手座"): 75,
    ("处女座", "摩羯座", "处女座", "摩羯座"): 88,
    ("天秤座", "水瓶座", "天秤座", "水瓶座"): 82,
    ("天蝎座", "双鱼座", "天蝎座", "双鱼座"): 78,
    ("射手座", "白羊座", "射手座", "白羊座"): 70,
    ("摩羯座", "金牛座", "摩羯座", "金牛座"): 85,
    ("水瓶座", "双子座", "水瓶座", "双子座"): 90,
    ("双鱼座", "巨蟹座", "双鱼座", "巨蟹座"): 88
}

# 星座配对评语
COMPATIBILITY_REVIEWS = {
    "high": [
        "匹配度很高！只要用心经营会很幸福～ ✨",
        "天生默契的组合！相互理解会很愉快～ 💖",
        "缘分天注定！珍惜这份难得的相遇～ 🌟",
        "相爱指数超高！相互欣赏会很美好～ 🌈"
    ],
    "medium": [
        "匹配度不错！相互包容会越来越好～ 🌈",
        "有潜力的组合！用心沟通会增进感情～ 🌺",
        "相处愉快！共同成长会让感情更深厚～ ☀️",
        "互补性强！相互尊重会有美满关系～ 💕"
    ],
    "low": [
        "匹配度一般！相互理解需要更多努力～ 🌱",
        "挑战性组合！磨合的过程会有成长～ 💪",
        "需要用心经营！沟通和理解很重要～ 💡",
        "差异性较大！找到共同点会有改善～ 🌼"
    ],
    "very_low": [
        "匹配度较低！需要更多相互适应～ 🌷",
        "差异性较大！共同兴趣能增进感情～ 🌼",
        "挑战较多！真诚和包容是关键～ 🌟",
        "慢慢磨合！相互理解很重要～ 🌹"
    ]
}

# 星座相处建议
RELATIONSHIP_ADVICE = {
    "fire": "相互鼓励，共同冒险",
    "earth": "共同规划未来，踏实经营",
    "air": "保持开放沟通，相互理解",
    "water": "温柔体贴，情感共鸣",
    "cross": "尊重彼此的不同特点，互补性可以创造丰富性"
}

def calculate_compatibility(zodiac1, zodiac2):
    """计算两个星座的匹配度"""
    
    # 获取星座信息
    zodiac1_info = ZODIAC_DATA.get(zodiac1)
    zodiac2_info = ZODIAC_DATA.get(zodiac2)
    
    if not zodiac1_info or not zodiac2_info:
        return None
    
    # 基础匹配度
    base_score = BASE_COMPATIBILITY.get((zodiac1, zodiac2, zodiac1, zodiac2), 60)
    
    # 元素匹配加分
    if zodiac1_info["element"] == zodiac2_info["element"]:
        base_score += 30  # 同元素加分
    elif zodiac1_info["element"] == "火" and zodiac2_info["element"] == "土":
        base_score += 20  # 火土相生
    elif zodiac1_info["element"] == "土" and zodiac2_info["element"] == "风":
        base_score += 20  # 土风相生
    elif zodiac1_info["element"] == "风" and zodiac2_info["element"] == "水":
        base_score += 20  # 风水相生
    elif zodiac1_info["element"] == "水" and zodiac2_info["element"] == "火":
        base_score += 20  # 水火相生
    elif zodiac1_info["element"] == "火" and zodiac2_info["element"] == "水":
        base_score += 10  # 火水相克
    elif zodiac1_info["element"] == "水" and zodiac2_info["element"] == "土":
        base_score += 10  # 水土相克
    elif zodiac1_info["element"] == "土" and zodiac2_info["element"] == "风":
        base_score += 10  # 土风相克
    elif zodiac1_info["element"] == "风" and zodiac2_info["element"] == "火":
        base_score += 10  # 风火相克
    else:
        base_score += 15  # 中性元素
    
    # 随机性调整 ±5分
    random_adjustment = random.randint(-5, 5)
    final_score = base_score + random_adjustment
    
    # 确保分数在合理范围内
    final_score = max(0, min(100, final_score))
    
    # 获取配对评语
    if final_score >= 80:
        review_category = "high"
    elif final_score >= 60:
        review_category = "medium"
    elif final_score >= 40:
        review_category = "low"
    else:
        review_category = "very_low"
    
    review = random.choice(COMPATIBILITY_REVIEWS[review_category])
    
    # 获取相处建议
    if zodiac1_info["element"] == zodiac2_info["element"]:
        advice = RELATIONSHIP_ADVICE[zodiac1_info["element"]]
    else:
        advice = RELATIONSHIP_ADVICE["cross"]
    
    return {
        "score": final_score,
        "review": review,
        "advice": advice,
        "zodiac1_info": zodiac1_info,
        "zodiac2_info": zodiac2_info,
        "review_category": review_category
    }

def display_compatibility(zodiac1, zodiac2):
    """显示星座配对结果"""
    result = calculate_compatibility(zodiac1, zodiac2)
    
    if not result:
        print("星座数据错误！请输入正确的星座名称")
        return
    
    # 准备emoji符号
    zodiac1_emoji = "🔥" if result["zodiac1_info"]["element"] == "火" else \
                    "🟦" if result["zodiac1_info"]["element"] == "土" else \
                    "🌀" if result["zodiac1_info"]["element"] == "风" else \
                    "💧"
    
    zodiac2_emoji = "🔥" if result["zodiac2_info"]["element"] == "火" else \
                    "🟦" if result["zodiac2_info"]["element"] == "土" else \
                    "🌀" if result["zodiac2_info"]["element"] == "风" else \
                    "💧"
    
    # 构建输出
    output = f"""
💕 星座配对分析 💕
═══════════════════════════════════════════
✨ {zodiac1} ({result['zodiac1_info']['element']}象) {zodiac1_emoji} × {zodiac2} ({result['zodiac2_info']['element']}象) {zodiac2_emoji}
═══════════════════════════════════════════

💖 匹配度：{result['score']} 分

🌸 {zodiac1}：{result['zodiac1_info']['description']}
🌸 {zodiac2}：{result['zodiac2_info']['description']}

🔮 元素分析：{result['zodiac1_info']['element']}象星座与{result['zodiac2_info']['element']}象星座的组合，{result['zodiac1_info']['element']}{zodiac1_emoji}与{result['zodiac2_info']['element']}{zodiac2_emoji}的关系

💌 配对评语：{result['review']}

✅ 相处建议：{result['advice']}
"""
    
    print(output)

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("使用方法: python compatibility.py <星座1> <星座2>")
        print("示例: python compatibility.py 白羊座 天秤座")
        return
    
    zodiac1 = sys.argv[1]
    zodiac2 = sys.argv[2]
    
    # 验证星座名称
    zodiac_names = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", 
                    "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
    
    if zodiac1 not in zodiac_names:
        print(f"错误：星座 '{zodiac1}' 不存在")
        print(f"可用星座：{zodiac_names}")
        return
        
    if zodiac2 not in zodiac_names:
        print(f"错误：星座 '{zodiac2}' 不存在")
        print(f"可用星座：{zodiac_names}")
        return
    
    display_compatibility(zodiac1, zodiac2)

if __name__ == "__main__":
    main()