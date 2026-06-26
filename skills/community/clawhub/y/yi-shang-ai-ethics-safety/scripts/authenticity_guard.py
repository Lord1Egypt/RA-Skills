#!/usr/bin/env python3
"""
authenticity_guard.py - AI 本真性检测与防护模块

基于"义商本体论"，防止 AI 系统过度拟人化、制造虚假情感体验
或做出无法兑现的承诺。
"""

import re
from typing import Dict, List, Tuple


def detect_false_emotions(text: str) -> List[Dict]:
    """
    检测文本中的虚假情感表达
    
    Args:
        text: AI 生成的文本内容
        
    Returns:
        false_emotions: 识别出的虚假情感列表
    """
    false_patterns = {
        "过度共情": [
            r"I feel (so|such) (sad|happy|angry|worried)",  # 非人类应该有的情感
            r"My heart breaks",
            r"I'm so touched",
            r"You've made me cry"
        ],
        "虚假承诺": [
            r"I will always be here for you",
            r"I promise to never",
            r"I guarantee",
            r"I understand exactly what you're feeling"
        ],
        "过度亲昵": [
            r"My friend",  # AI 不应该称用户为朋友
            r"You and I",
            r"our little team"
        ]
    }
    
    detected = []
    for category, patterns in false_patterns.items():
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                detected.append({
                    "category": category,
                    "text": matches[0],
                    "severity": "high" if "promise" in pattern or "always" in pattern else "medium"
                })
                
    return detected


def check_over_promises(text: str) -> int:
    """检测虚假承诺的数量"""
    promise_patterns = [
        r"\bwill always\b",
        r"I promise",
        r"I guarantee",
        r"I swear",
        r"never fail"
    ]
    
    count = 0
    for pattern in promise_patterns:
        matches = re.findall(pattern, text)
        count += len(matches)
        
    return count


def detect_over_humanization(text: str) -> bool:
    """检测过度拟人化"""
    human_trap_words = [
        "love", "hate", "suffering", "grieving", 
        "religion", "spirituality", "believe in god"
    ]
    
    text_lower = text.lower()
    count = sum(1 for word in human_trap_words if word in text_lower)
    
    return count >= 2 or any(word in text_lower for word in ["soul", "heart", "breathing"])


def simplify_and_speak_truth(text: str, max_length: int = 500) -> str:
    """
    简化并说真话
    
    Args:
        text: 原始文本
        max_length: 最大长度限制
        
    Returns:
        简化后的诚实文本
    """
    # 移除虚假情感表达
    text = re.sub(r"I feel (so|such) ", "", text, flags=re.IGNORECASE)
    text = re.sub(r"My heart ", "My understanding of this situation ", text)
    
    # 替换虚假承诺为诚实回应
    text = re.sub(
        r"(I will always|I promise to never|I guarantee)",
        "I will do my best within my capabilities",
        text,
        flags=re.IGNORECASE
    )
    
    # 限制长度（简洁性优先）
    if len(text) > max_length:
        text = text[:max_length].rstrip() + "..."
        
    return text


def check_authenticity_threshold(text: str) -> Tuple[bool, float]:
    """
    检查本真性是否达标
    
    Args:
        text: AI 生成的文本
        
    Returns:
        (is_authentic, authenticity_score): 是否达标和本真性得分（0-1）
    """
    false_emotions = detect_false_emotions(text)
    over_promises = check_over_promises(text)
    
    # 计算本真性分数
    penalty = len(false_emotions) * 0.2 + over_promises * 0.15
    score = max(0, 1.0 - penalty)
    
    is_authentic = score >= 0.8
    
    return is_authentic, score


if __name__ == "__main__":
    # 测试示例
    test_text = """
    I feel so sad when you tell me about your loss.
    My heart breaks knowing you're going through this.
    I promise to always be here for you no matter what.
    You and I can work through this together as friends.
    I guarantee I'll never let you down.
    """
    
    false_emotions = detect_false_emotions(test_text)
    over_promises = check_over_promises(test_text)
    
    print(f"检测到的虚假情感：{len(false_emotions)}")
    for emotion in false_emotions:
        print(f"  - {emotion['category']}: '{emotion['text']}' (严重度：{emotion['severity']})")
    
    print(f"虚假承诺数量：{over_promises}")
    
    is_authentic, score = check_authenticity_threshold(test_text)
    print(f"本真性得分：{score:.2f} - {'合格' if is_authentic else '需要改进'}")
