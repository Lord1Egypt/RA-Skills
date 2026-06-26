#!/usr/bin/env python3
"""
中文特有表达识别模块
Chinese Expressions Detection Module
"""

from typing import List, Dict, Any

# 成语库
IDIOMS_DB = {
    "画蛇添足": {"type": "idiom", "sentiment": "negative", "usage": "提醒勿多此一举", "meaning": "做了多余的事"},
    "亡羊补牢": {"type": "idiom", "sentiment": "positive", "usage": "鼓励及时改正", "meaning": "出了问题后及时补救"},
    "守株待兔": {"type": "idiom", "sentiment": "negative", "usage": "批评不劳而获", "meaning": "妄想不劳而获"},
    "掩耳盗铃": {"type": "idiom", "sentiment": "negative", "usage": "讽刺自欺欺人", "meaning": "自欺欺人"},
    "井底之蛙": {"type": "idiom", "sentiment": "negative", "usage": "批评见识短浅", "meaning": "见识短浅的人"},
    "班门弄斧": {"type": "idiom", "sentiment": "neutral", "usage": "自谦或提醒", "meaning": "在行家面前卖弄"},
    "对牛弹琴": {"type": "idiom", "sentiment": "negative", "usage": "批评沟通无效", "meaning": "对不懂的人讲道理"},
    "狐假虎威": {"type": "idiom", "sentiment": "negative", "usage": "批评仗势欺人", "meaning": "借别人的势力欺压人"}
}

# 网络用语库
SLANG_DB = {
    "yyds": {"type": "internet_slang", "meaning": "永远的神", "sentiment": "positive", "category": "赞美"},
    "内卷": {"type": "slang", "meaning": "非理性竞争", "sentiment": "negative", "category": "社会现象"},
    "躺平": {"type": "slang", "meaning": "放弃竞争", "sentiment": "neutral", "category": "生活态度"},
    "emo": {"type": "internet_slang", "meaning": "情绪低落", "sentiment": "negative", "category": "情绪"},
    "破防": {"type": "internet_slang", "meaning": "心理防线被突破", "sentiment": "neutral", "category": "情绪"},
    "绝绝子": {"type": "internet_slang", "meaning": "太绝了", "sentiment": "positive", "category": "赞美"},
    "yygq": {"type": "internet_slang", "meaning": "阴阳怪气", "sentiment": "negative", "category": "讽刺"},
    "xswl": {"type": "internet_slang", "meaning": "笑死我了", "sentiment": "positive", "category": "情绪"},
    "awsl": {"type": "internet_slang", "meaning": "啊我死了", "sentiment": "positive", "category": "赞美"},
    "u1s1": {"type": "internet_slang", "meaning": "有一说一", "sentiment": "neutral", "category": "语气词"},
    "nsdd": {"type": "internet_slang", "meaning": "你说得对", "sentiment": "positive", "category": "认同"},
    "zqsg": {"type": "internet_slang", "meaning": "真情实感", "sentiment": "neutral", "category": "态度"}
}

# 俗语库
PROVERBS_DB = {
    "吃一堑长一智": {"type": "proverb", "meaning": "从失败中吸取教训", "sentiment": "positive"},
    "不听老人言吃亏在眼前": {"type": "proverb", "meaning": "应该听取长辈建议", "sentiment": "neutral"},
    "心急吃不了热豆腐": {"type": "proverb", "meaning": "做事不能急躁", "sentiment": "neutral"},
    "羊毛出在羊身上": {"type": "proverb", "meaning": "利益来源本质", "sentiment": "neutral"},
    "打铁还需自身硬": {"type": "proverb", "meaning": "自身能力最重要", "sentiment": "positive"}
}


def detect_expression(text: str) -> List[Dict[str, Any]]:
    """
    识别中文特有表达并标注语义
    """
    results = []
    
    # 合并所有数据库
    all_expressions = {}
    all_expressions.update(IDIOMS_DB)
    all_expressions.update(SLANG_DB)
    all_expressions.update(PROVERBS_DB)
    
    # 检测匹配
    for expr, meta in all_expressions.items():
        if expr in text:
            result = {
                "expression": expr,
                "position": text.find(expr),
                **meta
            }
            results.append(result)
    
    # 按位置排序
    results.sort(key=lambda x: x["position"])
    
    return results


def get_expression_detail(expression: str) -> Dict[str, Any]:
    """
    获取特定表达的详细信息
    """
    all_db = {**IDIOMS_DB, **SLANG_DB, **PROVERBS_DB}
    
    if expression in all_db:
        return {
            "expression": expression,
            **all_db[expression]
        }
    
    return {"expression": expression, "found": False}


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    基于特殊表达分析情感倾向
    """
    expressions = detect_expression(text)
    
    if not expressions:
        return {"sentiment": "neutral", "score": 0.5, "expressions": []}
    
    # 计算情感分数
    sentiment_scores = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }
    
    for expr in expressions:
        sentiment = expr.get("sentiment", "neutral")
        sentiment_scores[sentiment] += 1
    
    # 判断整体情感
    total = sum(sentiment_scores.values())
    if total == 0:
        overall = "neutral"
        score = 0.5
    else:
        pos_ratio = sentiment_scores["positive"] / total
        neg_ratio = sentiment_scores["negative"] / total
        
        if pos_ratio > neg_ratio and pos_ratio > 0.3:
            overall = "positive"
            score = 0.5 + pos_ratio * 0.5
        elif neg_ratio > pos_ratio and neg_ratio > 0.3:
            overall = "negative"
            score = 0.5 - neg_ratio * 0.5
        else:
            overall = "neutral"
            score = 0.5
    
    return {
        "sentiment": overall,
        "score": round(score, 2),
        "expressions": expressions,
        "breakdown": sentiment_scores
    }


if __name__ == "__main__":
    # 测试
    test_texts = [
        "yyds永远的神",
        "现在太内卷了，我想躺平",
        "你这是画蛇添足，多此一举",
        "u1s1，这个设计真的绝绝子",
        "不要掩耳盗铃，自欺欺人"
    ]
    
    for text in test_texts:
        print(f"\n输入: {text}")
        expressions = detect_expression(text)
        print(f"识别到 {len(expressions)} 个特殊表达:")
        for expr in expressions:
            print(f"  - {expr['expression']} ({expr['type']}): {expr['meaning']}")
        
        sentiment = analyze_sentiment(text)
        print(f"情感分析: {sentiment['sentiment']} (分数: {sentiment['score']})")
