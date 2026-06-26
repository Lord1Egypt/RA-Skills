#!/usr/bin/env python3
"""
Secretary Skill v2.0 - 察言观色版
情感识别 + 意图理解 + 语境管理 + 自适应响应
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

class Emotion(Enum):
    """7 种基本情感"""
    HAPPY = "happy"
    ANGRY = "angry"
    SAD = "sad"
    SURPRISE = "surprise"
    FEAR = "fear"
    DISGUST = "disgust"
    NEUTRAL = "neutral"

class Intent(Enum):
    """6 类意图"""
    COMMAND = "command"
    QUESTION = "question"
    SUGGESTION = "suggestion"
    STATEMENT = "statement"
    EMOTIONAL = "emotional"
    AMBIGUOUS = "ambiguous"

class Priority(Enum):
    """4 级优先级"""
    P0 = "urgent_important"
    P1 = "important_not_urgent"
    P2 = "normal"
    P3 = "low"

@dataclass
class EmotionResult:
    """情感分析结果"""
    emotion: Emotion
    confidence: float
    keywords: List[str] = field(default_factory=list)
    tone: str = "neutral"

@dataclass
class IntentResult:
    """意图识别结果"""
    intent: Intent
    priority: Priority
    confidence: float
    action_items: List[str] = field(default_factory=list)

@dataclass
class Context:
    """语境信息"""
    scene: str = "work"  # work/life/social
    relationship: str = "unknown"
    recent_turns: deque = field(default_factory=lambda: deque(maxlen=10))
    user_preferences: Dict = field(default_factory=dict)

class SecretarySkill:
    """秘书技能 v2.0（察言观色版）"""
    
    # 情感关键词
    EMOTION_KEYWORDS = {
        Emotion.HAPPY: ["开心", "高兴", "太好了", "哈哈", "棒", "爽"],
        Emotion.ANGRY: ["生气", "气死", "烦", "讨厌", "可恶", "怒"],
        Emotion.SAD: ["难过", "伤心", "悲伤", "唉", "郁闷", "泪"],
        Emotion.SURPRISE: ["哇", "天啊", "没想到", "惊讶", "居然"],
        Emotion.FEAR: ["害怕", "担心", "恐惧", "糟了", "慌"],
        Emotion.DISGUST: ["恶心", "厌恶", "嫌弃", "呕"],
    }
    
    # 意图关键词
    INTENT_KEYWORDS = {
        Intent.COMMAND: ["帮我", "立即", "现在", "去", "做"],
        Intent.QUESTION: ["什么", "怎么", "哪里", "何时", "谁", "吗"],
        Intent.SUGGESTION: ["要不要", "可以吗", "觉得", "建议"],
        Intent.EMOTIONAL: ["好累", "开心", "烦", "唉", "哈哈"],
    }
    
    # 关系识别
    RELATIONSHIP_CUES = {
        "superior": ["安排", "任务", "去", "立即", "必须"],
        "colleague": ["一起", "帮忙", "协作", "我们", "咱们"],
        "client": ["咨询", "需求", "服务", "贵司", "合作"],
        "friend": ["哈", "啦", "～", "嘿嘿", "哈哈"],
        "family": ["记得", "别忘", "关心", "爱", "想"],
    }
    
    def __init__(self, verbose: bool = False):
        self.context = Context()
        self.verbose = verbose
        
    def analyze_emotion(self, text: str) -> EmotionResult:
        """情感分析"""
        scores = {e: 0.0 for e in Emotion}
        found_keywords = {e: [] for e in Emotion}
        
        # 关键词匹配
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    scores[emotion] += 0.3
                    found_keywords[emotion].append(kw)
        
        # 表情符号
        emojis = {"😄": Emotion.HAPPY, "😢": Emotion.SAD, "😠": Emotion.ANGRY}
        for emoji, emotion in emojis.items():
            if emoji in text:
                scores[emotion] += 0.2
        
        # 语气分析
        if "！" in text or "!" in text:
            scores[Emotion.HAPPY] += 0.1
        if "..." in text or "唉" in text:
            scores[Emotion.SAD] += 0.1
        
        # 找出最高分
        max_emotion = max(scores, key=scores.get)
        confidence = min(1.0, scores[max_emotion] + 0.5)
        
        return EmotionResult(
            emotion=max_emotion,
            confidence=confidence,
            keywords=found_keywords[max_emotion]
        )
    
    def recognize_intent(self, text: str) -> IntentResult:
        """意图识别"""
        scores = {i: 0.0 for i in Intent}
        action_items = []
        
        # 关键词匹配
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    scores[intent] += 0.4
        
        # 句式分析
        if text.endswith("?") or "吗" in text:
            scores[Intent.QUESTION] += 0.3
        if text.startswith(("请", "帮我", "立即")):
            scores[Intent.COMMAND] += 0.3
            action_items.append(text)
        
        # 优先级判断
        priority = Priority.P2
        if any(kw in text for kw in ["立即", "马上", "紧急", "急"]):
            priority = Priority.P0
        elif any(kw in text for kw in ["今天", "本周", "计划"]):
            priority = Priority.P1
        elif any(kw in text for kw in ["有空", "顺便", "可以"]):
            priority = Priority.P3
        
        max_intent = max(scores, key=scores.get)
        confidence = min(1.0, scores[max_intent] + 0.5)
        
        return IntentResult(
            intent=max_intent,
            priority=priority,
            confidence=confidence,
            action_items=action_items
        )
    
    def recognize_relationship(self, text: str) -> str:
        """关系识别"""
        for relation, cues in self.RELATIONSHIP_CUES.items():
            if any(cue in text for cue in cues):
                return relation
        return "unknown"
    
    def respond(self, text: str) -> str:
        """生成响应（察言观色版）"""
        # 多维度分析
        emotion = self.analyze_emotion(text)
        intent = self.recognize_intent(text)
        relationship = self.recognize_relationship(text)
        
        # 更新语境
        self.context.recent_turns.append({
            "text": text,
            "emotion": emotion.emotion.value,
            "intent": intent.intent.value,
            "timestamp": datetime.now().isoformat()
        })
        
        if self.verbose:
            print(f"情感：{emotion.emotion.value} ({emotion.confidence:.2f})")
            print(f"意图：{intent.intent.value} ({intent.priority.value})")
            print(f"关系：{relationship}")
        
        # 生成响应
        response = self._generate_response(text, emotion, intent, relationship)
        
        return response
    
    def _generate_response(self, text: str, emotion: EmotionResult, 
                          intent: IntentResult, relationship: str) -> str:
        """生成响应"""
        # 情感共鸣
        if emotion.emotion == Emotion.HAPPY:
            prefix = ["太棒了！", "恭喜！", "真好！"]
        elif emotion.emotion == Emotion.SAD:
            prefix = ["别难过...", "理解您...", "抱抱..."]
        elif emotion.emotion == Emotion.ANGRY:
            prefix = ["别生气...", "理解...", "冷静..."]
        else:
            prefix = ["好的", "收到", "明白"]
        
        # 意图响应
        if intent.intent == Intent.COMMAND:
            action = f"马上执行：{intent.action_items[0] if intent.action_items else '任务'}"
        elif intent.intent == Intent.QUESTION:
            action = "我来帮您查一下..."
        elif intent.intent == Intent.SUGGESTION:
            action = "我的建议是..."
        else:
            action = "已记录"
        
        # 关系调整
        if relationship == "superior":
            suffix = "请问还有其他安排吗？"
        elif relationship == "friend":
            suffix = "～"
        else:
            suffix = ""
        
        return f"{prefix[0]} {action}{suffix}"
    
    def reset(self):
        """重置语境"""
        self.context = Context()

# 测试
def main():
    secretary = SecretarySkill(verbose=True)
    
    test_cases = [
        "今天项目上线成功了！😄",
        "气死我了，客户又改需求！",
        "帮我预定明天下午 2 点的会议室",
        "明天的会议在哪里开？",
        "要不要今天下午去拜访客户？",
    ]
    
    for text in test_cases:
        print(f"\n用户：{text}")
        response = secretary.respond(text)
        print(f"秘书：{response}")
        print("-" * 50)

if __name__ == "__main__":
    main()
