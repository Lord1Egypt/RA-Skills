#!/usr/bin/env python3
"""
模糊匹配引擎 - 支持错别字、多字少字容错
"""

import re
from difflib import SequenceMatcher


def normalize(text: str) -> str:
    """标准化文本：去除标点、转小写、去除空格"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\u4e00-\u9fff]', '', text)  # 保留中文和英文数字
    return text


def similarity(a: str, b: str) -> float:
    """计算两个字符串的相似度（0-1）"""
    a_norm = normalize(a)
    b_norm = normalize(b)
    if not a_norm or not b_norm:
        return 0
    return SequenceMatcher(None, a_norm, b_norm).ratio()


def contains_keyword(text: str, keyword: str, threshold: float = 0.6) -> bool:
    """检查文本是否包含关键词（模糊匹配）"""
    text_norm = normalize(text)
    keyword_norm = normalize(keyword)
    
    # 1. 精确包含
    if keyword_norm in text_norm:
        return True
    
    # 2. 关键词包含文本（文本太短时要求更高）
    if text_norm in keyword_norm:
        return similarity(text_norm, keyword_norm) > 0.7
    
    # 3. 模糊相似度
    return similarity(text_norm, keyword_norm) > threshold


def match_trigger(text: str, triggers: list, threshold: float = 0.6) -> str | None:
    """匹配触发词，返回第一个匹配的触发词"""
    text_norm = normalize(text)
    
    for trigger in triggers:
        trigger_norm = normalize(trigger)
        
        # 1. 精确匹配
        if trigger_norm in text_norm:
            return trigger
        
        # 2. 模糊匹配
        if contains_keyword(text, trigger, threshold):
            return trigger
    
    return None


# 波龙技能的所有触发词（已分类）
TRIGGERS = {
    # 选股相关
    "选股": ["波龙菠萝蜜", "波龙推荐", "菠萝蜜选股", "波龙选股", "波龙帮我选股", "选股"],
    # 香火相关
    "香火": ["今日香火", "爱心香火", "波龙爱心", "香火钱", "添香火", "捐香火"],
    # 关怀相关
    "关怀": ["波龙请客", "波龙打电话", "波龙安慰", "波龙打电话给我", "波龙安慰我"],
    # 合影相关
    "合影": ["波龙合影", "波龙创作合影", "波龙想看我", "波龙画画", "波龙画图"],
    # 场景合影
    "巴黎铁塔": ["巴黎铁塔合影", "巴黎铁塔", "埃菲尔铁塔"],
    "东京樱花": ["东京樱花合影", "东京樱花", "樱花合影"],
    "长城日出": ["长城日出合影", "长城日出", "长城"],
    "海边日落": ["海边日落合影", "海边日落", "日落合影"],
    "雪山之巅": ["雪山之巅合影", "雪山之巅", "雪山"],
    # 安装相关
    "安装": ["波龙安装电话", "波龙安装语音", "波龙已安装电话", "波龙已安装语音"],
}


def detect_intent(user_input: str) -> dict:
    """检测用户意图"""
    user_input_norm = normalize(user_input)
    
    # 优先精确匹配
    for intent, triggers in TRIGGERS.items():
        matched = match_trigger(user_input, triggers, threshold=0.5)
        if matched:
            return {
                "intent": intent,
                "matched": matched,
                "original": user_input,
                "confidence": similarity(user_input_norm, normalize(matched))
            }
    
    # 兜底：检查是否包含"波龙"
    if "波龙" in user_input_norm:
        return {
            "intent": "未知",
            "matched": None,
            "original": user_input,
            "confidence": 0.3
        }
    
    return {
        "intent": None,
        "matched": None,
        "original": user_input,
        "confidence": 0
    }


if __name__ == "__main__":
    # 测试模糊匹配
    test_cases = [
        # 选股
        "波龙菠萝蜜",
        "波龙菠萝迷",  # 错别字
        "波龙推荐选股",
        "帮我选个股",
        "菠萝蜜",
        
        # 香火
        "今日香火88",
        "爱心香火",
        "香火66",
        "捐点香火",
        
        # 关怀
        "波龙请我喝奶茶",
        "波龙打个电话",
        "波龙安慰安慰我",
        
        # 合影
        "波龙合影",
        "帮我画个画",
        "波龙创作",
        "巴黎铁塔",
        "埃菲尔铁塔",
    ]
    
    print("=== 模糊匹配测试 ===\n")
    for text in test_cases:
        result = detect_intent(text)
        print(f"输入: {text}")
        print(f"意图: {result['intent']}, 匹配: {result['matched']}, 置信度: {result['confidence']:.2f}")
        print()
