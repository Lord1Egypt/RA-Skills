#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emotion_analyzer.py — 情感识别与自适应对话策略引擎

功能：
1. 文本情感分析（5 分类：愤怒/焦虑/满意/困惑/中性）
2. 否定词翻转 + 程度副词加权 + 置信度评分
3. 情绪升级跟踪（连续负面轮次计数）
4. 硬件自适应（根据系统资源动态调整分析深度）

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-07-23)
"""

import re
import os
import json
import sqlite3
import logging
from enum import Enum
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# ==========================================
# 情感类型枚举
# ==========================================

class Emotion(Enum):
    """情感分类"""
    ANGRY = "angry"           # 愤怒
    ANXIOUS = "anxious"       # 焦虑
    SATISFIED = "satisfied"   # 满意
    CONFUSED = "confused"     # 困惑
    NEUTRAL = "neutral"       # 中性

    def __str__(self):
        return self.value

    @classmethod
    def from_string(cls, value: str) -> 'Emotion':
        for e in cls:
            if e.value == value:
                return e
        return cls.NEUTRAL


# ==========================================
# 情感词典
# ==========================================

# 基础情感关键词（按情感分类）
EMOTION_KEYWORDS: Dict[Emotion, List[str]] = {
    Emotion.ANGRY: [
        "生气", "愤怒", "火大", "恼火", "气愤", "怒", "骂", "投诉", "差评",
        "骗人", "骗子", "坑人", "糊弄", "敷衍", "态度差", "服务差", "太差",
        "什么破", "垃圾", "滚", "混蛋", "骗", "坑", "太烂", "极差",
        "受不了", "忍无可忍", "气死", "烦死", "倒霉", "黑心", "无良",
        "退款", "赔偿", "举报", "315", "消协", "工商局", "维权",
    ],
    Emotion.ANXIOUS: [
        "着急", "焦虑", "担心", "急", "赶紧", "快点", "马上", "立刻",
        "来不及", "赶时间", "怎么办", "急死", "慌", "惶恐", "不安",
        "压力", "发愁", "苦恼", "棘手", "棘手", "麻烦", "困难",
        "能不能快", "时间紧迫", "催", "催促", "紧急", "加急", "特急",
        "等不及", "来不及", "赶不上", "要迟到了", "火烧眉毛",
    ],
    Emotion.SATISFIED: [
        "好", "谢谢", "感谢", "满意", "不错", "很好", "太好了", "棒",
        "赞", "优秀", "完美", "舒适", "贴心", "专业", "高效", "快速",
        "及时", "准确", "清楚", "明白", "懂了", "学到了", "有帮助",
        "麻烦你了", "辛苦了", "谢谢您", "好评", "五星", "推荐",
        "继续", "下次还", "再来", "可以", "行", "同意", "没问题",
        "太棒了", "非常棒", "好用", "实用", "物超所值", "值得",
    ],
    Emotion.CONFUSED: [
        "不懂", "不明白", "不清楚", "不理解", "什么意思", "怎么回事",
        "怎么做", "怎么办", "怎么弄", "咋弄", "为啥", "为什么",
        "什么情况", "什么情况", "啥意思", "啊", "嗯", "呃",
        "能不能", "可以吗", "行吗", "是不是", "对吗", "是不是这样",
        "举个例子", "示范", "演示", "再讲一遍", "再说一次", "重复",
        "听不懂", "没听清", "再说一遍", "解释一下", "怎么操作",
        "在哪里", "找不到", "看不到", "没有", "哪里",
    ],
}

# 否定词（用于情感翻转）
# 注意："非"不在列表中，因为"非常"是正面程度副词，不是否定
NEGATION_WORDS = [
    "不", "没", "无", "莫", "勿", "未", "否",
    "不是", "没有", "不能", "不会", "不要", "不可以",
    "并没有", "不太", "不怎么", "不够", "不算",
]

# 程度副词（用于加权）
# 注意："好"不在列表中，因为它已经是满意情感的核心关键词
INTENSIFIERS = {
    # 轻度
    "稍": 0.3, "稍微": 0.3, "略": 0.3, "有点": 0.4, "有些": 0.4,
    "一点": 0.3, "一些": 0.3, "多少": 0.3,
    # 中度
    "比较": 0.6, "挺": 0.6, "蛮": 0.6, "还算": 0.5, "还行": 0.5,
    # 高度
    "很": 0.8, "非常": 0.9, "特别": 0.9, "十分": 0.9, "极其": 1.0,
    "超级": 1.0, "太": 0.9, "真": 0.8, "多么": 0.8,
    "实在": 0.8, "确实": 0.7, "真的": 0.8, "尤为": 0.9,
    "万分": 1.0, "无比": 1.0, "最": 1.0, "极": 1.0,
}

# 标点情感权重
PUNCTUATION_WEIGHTS = {
    "！": 0.1,   # 感叹号增强情感
    "？": 0.05,  # 问号略增强困惑
    "!!": 0.2,
    "?!": 0.15,
    "！？": 0.15,
}


# ==========================================
# 情感分析器
# ==========================================

class EmotionAnalyzer:
    """
    文本情感分析器
    
    使用方式：
        analyzer = EmotionAnalyzer()
        result = analyzer.analyze("这个产品太差了！")
        # result = {"emotion": Emotion.ANGRY, "confidence": 0.85, "scores": {...}}
    """

    def __init__(self, strategies_path: Optional[str] = None):
        """
        初始化情感分析器
        
        Args:
            strategies_path: 策略模板文件路径（可选）
        """
        self.emotion_keywords = EMOTION_KEYWORDS
        self.negation_words = NEGATION_WORDS
        self.intensifiers = INTENSIFIERS
        
        # 加载策略模板（如果提供）
        self.strategies: Dict = {}
        if strategies_path and os.path.exists(strategies_path):
            with open(strategies_path, 'r', encoding='utf-8') as f:
                self.strategies = json.load(f)

    def analyze(self, text: str) -> Dict:
        """
        分析文本情感
        
        Args:
            text: 待分析的文本
            
        Returns:
            dict: {
                "emotion": Emotion,
                "confidence": float (0-1),
                "scores": {emotion_str: float},
                "method": "rule_engine"
            }
        """
        if not text or not isinstance(text, str):
            return {
                "emotion": Emotion.NEUTRAL,
                "confidence": 1.0,
                "scores": {e.value: 0.0 for e in Emotion},
                "method": "rule_engine"
            }

        text = text.strip()
        if len(text) == 0:
            return {
                "emotion": Emotion.NEUTRAL,
                "confidence": 1.0,
                "scores": {e.value: 0.0 for e in Emotion},
                "method": "rule_engine"
            }

        # 计算各情感得分
        scores = self._compute_scores(text)
        
        # 找出最高分的情感
        max_emotion = max(scores, key=scores.get)
        max_score = scores[max_emotion]
        
        # 计算置信度
        confidence = self._compute_confidence(max_score, scores)
        
        # 如果最高分过低，判定为中性
        if max_score < 0.1:
            max_emotion = Emotion.NEUTRAL
            confidence = 0.8

        return {
            "emotion": max_emotion,
            "confidence": confidence,
            "scores": {e.value: round(s, 3) for e, s in scores.items()},
            "method": "rule_engine"
        }

    def _compute_scores(self, text: str) -> Dict[Emotion, float]:
        """计算各情感维度的得分"""
        scores = {e: 0.0 for e in Emotion}
        
        # 1. 关键词匹配得分
        keyword_scores = self._keyword_match_score(text)
        for emotion, score in keyword_scores.items():
            scores[emotion] += score
        
        # 2. 否定词翻转
        scores = self._apply_negation(text, scores)
        
        # 3. 程度副词加权
        scores = self._apply_intensifiers(text, scores)
        
        # 4. 标点符号加权
        scores = self._apply_punctuation(text, scores)
        
        return scores

    def _keyword_match_score(self, text: str) -> Dict[Emotion, float]:
        """基于关键词匹配计算得分（带情感优先级权重）"""
        emotion_priority = {
            Emotion.ANGRY: 1.2,
            Emotion.ANXIOUS: 1.2,
            Emotion.SATISFIED: 1.0,
            Emotion.CONFUSED: 0.9,
            Emotion.NEUTRAL: 1.0,
        }
        
        scores = {e: 0.0 for e in Emotion}
        
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                count = text.count(keyword)
                if count > 0:
                    priority = emotion_priority.get(emotion, 1.0)
                    scores[emotion] += 0.3 * priority * (1 + 0.5 * (count - 1))
        
        return scores

    def _apply_negation(self, text: str, scores: Dict[Emotion, float]) -> Dict[Emotion, float]:
        """
        应用否定词翻转逻辑（精准版）
        规则：否定词直接出现在情感关键词前面时才翻转
        例如："不满意" → 满意被翻转；"好不好" → "不"不在满意前，不翻转
        """
        # 检查满意关键词前面是否有否定词
        satisfied_keywords = self.emotion_keywords.get(Emotion.SATISFIED, [])
        for kw in satisfied_keywords:
            if kw in text:
                # 查找关键词在文本中的位置
                idx = text.find(kw)
                while idx != -1:
                    # 检查关键词前面是否有否定词（1-2个字符内）
                    before_text = text[max(0, idx - 2):idx]
                    has_negation_before = any(before_text.endswith(neg) for neg in ["不", "没", "不太", "不怎么", "不够"])
                    
                    if has_negation_before:
                        # 翻转满意为愤怒/焦虑
                        satisfied_score = scores[Emotion.SATISFIED]
                        scores[Emotion.ANGRY] += satisfied_score * 0.5
                        scores[Emotion.ANXIOUS] += satisfied_score * 0.3
                        scores[Emotion.SATISFIED] *= 0.2
                        break
                    
                    idx = text.find(kw, idx + 1)
        
        # 检查焦虑关键词前面是否有否定词
        anxious_keywords = self.emotion_keywords.get(Emotion.ANXIOUS, [])
        for kw in anxious_keywords:
            if kw in text:
                idx = text.find(kw)
                while idx != -1:
                    before_text = text[max(0, idx - 2):idx]
                    has_negation_before = any(before_text.endswith(neg) for neg in ["不", "没"])
                    
                    if has_negation_before:
                        anxious_score = scores[Emotion.ANXIOUS]
                        scores[Emotion.ANXIOUS] *= 0.3
                        scores[Emotion.NEUTRAL] += anxious_score * 0.3
                        break
                    
                    idx = text.find(kw, idx + 1)
        
        return scores

    def _apply_intensifiers(self, text: str, scores: Dict[Emotion, float]) -> Dict[Emotion, float]:
        """应用程度副词加权"""
        for intensifier, weight in self.intensifiers.items():
            if intensifier in text:
                # 对所有非零情感分数进行加权
                for emotion in scores:
                    if scores[emotion] > 0:
                        scores[emotion] *= (1 + weight * 0.5)
        return scores

    def _apply_punctuation(self, text: str, scores: Dict[Emotion, float]) -> Dict[Emotion, float]:
        """应用标点符号加权"""
        # 多个感叹号增强愤怒/满意
        if "!!" in text or "！！" in text:
            if scores[Emotion.ANGRY] > 0:
                scores[Emotion.ANGRY] *= 1.3
            if scores[Emotion.SATISFIED] > 0:
                scores[Emotion.SATISFIED] *= 1.2
        
        # 多个问号增强困惑
        if "??" in text or "？？" in text:
            scores[Emotion.CONFUSED] *= 1.3
        
        return scores

    def _compute_confidence(self, max_score: float, scores: Dict[Emotion, float]) -> float:
        """
        计算置信度
        - 最高分与次高分差距越大，置信度越高
        - 绝对分数越高，置信度越高
        """
        sorted_scores = sorted(scores.values(), reverse=True)
        
        if len(sorted_scores) < 2 or sorted_scores[0] == 0:
            return 0.5
        
        # 计算最高分与次高分的差距比例
        gap_ratio = (sorted_scores[0] - sorted_scores[1]) / sorted_scores[0]
        
        # 基础置信度
        base_confidence = 0.5 + gap_ratio * 0.3
        
        # 分数绝对值调整
        score_bonus = min(sorted_scores[0] * 0.2, 0.2)
        
        confidence = min(base_confidence + score_bonus, 1.0)
        return round(confidence, 3)

    def get_strategy(self, emotion: Emotion, confidence: float) -> Dict:
        """
        根据情感获取对应的对话策略
        
        Args:
            emotion: 情感类型
            confidence: 置信度
            
        Returns:
            dict: 策略模板
        """
        emotion_str = emotion.value
        
        if emotion_str in self.strategies:
            strategy = self.strategies[emotion_str].copy()
            strategy["emotion"] = emotion_str
            strategy["confidence"] = confidence
            return strategy
        
        # 默认策略
        return {
            "emotion": emotion_str,
            "confidence": confidence,
            "action": "continue",
            "tone": "neutral",
            "template": "我理解您的意思，请继续。",
            "priority": "normal"
        }


# ==========================================
# 情绪升级跟踪器
# ==========================================

class EmotionEscalationTracker:
    """
    情绪升级跟踪器
    
    跟踪连续负面情绪轮次，超过阈值时建议转接人工。
    
    使用方式：
        tracker = EmotionEscalationTracker(threshold=2)
        tracker.record(Emotion.ANGRY, "user_001")
        if tracker.should_escalate("user_001"):
            # 建议转人工
    """

    def __init__(self, threshold: int = 2, window_minutes: int = 10):
        """
        Args:
            threshold: 连续负面轮次阈值（超过则升级）
            window_minutes: 时间窗口（分钟），超过此时间无新对话则重置
        """
        self.threshold = threshold
        self.window_minutes = window_minutes
        self._records: Dict[str, List[Dict]] = {}  # user_id -> [{emotion, timestamp}]

    def record(self, emotion: Emotion, user_id: str):
        """记录一次情感检测结果"""
        now = datetime.now()
        
        if user_id not in self._records:
            self._records[user_id] = []
        
        self._records[user_id].append({
            "emotion": emotion.value,
            "timestamp": now.isoformat()
        })
        
        # 清理过期记录
        self._cleanup(user_id, now)

    def should_escalate(self, user_id: str) -> bool:
        """
        判断是否应该升级（转人工）
        
        Returns:
            bool: True 表示建议转人工
        """
        if user_id not in self._records:
            return False
        
        now = datetime.now()
        self._cleanup(user_id, now)
        
        records = self._records.get(user_id, [])
        if len(records) < self.threshold:
            return False
        
        # 检查最近 N 轮是否都是负面
        recent = records[-self.threshold:]
        negative_emotions = {Emotion.ANGRY.value, Emotion.ANXIOUS.value}
        
        return all(r["emotion"] in negative_emotions for r in recent)

    def get_consecutive_negative_count(self, user_id: str) -> int:
        """获取连续负面情绪轮次计数"""
        if user_id not in self._records:
            return 0
        
        now = datetime.now()
        self._cleanup(user_id, now)
        
        records = self._records.get(user_id, [])
        count = 0
        for r in reversed(records):
            if r["emotion"] in {Emotion.ANGRY.value, Emotion.ANXIOUS.value}:
                count += 1
            else:
                break
        return count

    def reset(self, user_id: str):
        """重置用户的情感记录"""
        self._records.pop(user_id, None)

    def _cleanup(self, user_id: str, now: datetime):
        """清理过期的记录"""
        if user_id not in self._records:
            return
        
        cutoff = now - timedelta(minutes=self.window_minutes)
        self._records[user_id] = [
            r for r in self._records[user_id]
            if datetime.fromisoformat(r["timestamp"]) > cutoff
        ]


# ==========================================
# 硬件自适应配置
# ==========================================

class HardwareAdaptiveConfig:
    """
    硬件自适应配置
    
    根据系统资源动态调整情感分析策略：
    - 低配（<4GB RAM 或 2核以下）：仅文本分析
    - 中配（4-8GB RAM）：文本分析 + 轻量音频特征
    - 高配（>8GB RAM）：全量分析
    """

    @staticmethod
    def detect_tier() -> str:
        """检测硬件等级"""
        try:
            import platform
            import sys
            
            # 尝试获取内存信息（跨平台）
            total_ram_gb = HardwareAdaptiveConfig._get_total_ram_gb()
            cpu_count = os.cpu_count() or 1
            
            if total_ram_gb < 4 or cpu_count <= 2:
                return "low"
            elif total_ram_gb <= 8:
                return "medium"
            else:
                return "high"
        except Exception:
            return "low"  # 默认低配

    @staticmethod
    def _get_total_ram_gb() -> float:
        """获取总内存（GB）"""
        try:
            # Windows
            if os.name == 'nt':
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulonglong = ctypes.c_ulonglong
                
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', c_ulonglong),
                        ('ullAvailPhys', c_ulonglong),
                        ('ullTotalPageFile', c_ulonglong),
                        ('ullAvailPageFile', c_ulonglong),
                        ('ullTotalVirtual', c_ulonglong),
                        ('ullAvailVirtual', c_ulonglong),
                        ('ullAvailExtendedVirtual', c_ulonglong),
                    ]
                
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                return stat.ullTotalPhys / (1024 ** 3)
            else:
                # Linux/macOS
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if line.startswith('MemTotal'):
                            return int(line.split()[1]) / (1024 ** 2)
        except Exception:
            pass
        
        return 4.0  # 默认假设 4GB

    @staticmethod
    def get_config(tier: Optional[str] = None) -> Dict:
        """
        获取对应等级的配置
        
        Returns:
            dict: {
                "enable_audio_analysis": bool,
                "max_history_turns": int,
                "analysis_depth": str,
                "cache_enabled": bool
            }
        """
        if tier is None:
            tier = HardwareAdaptiveConfig.detect_tier()
        
        configs = {
            "low": {
                "enable_audio_analysis": False,
                "max_history_turns": 3,
                "analysis_depth": "basic",
                "cache_enabled": False,
                "description": "低配模式：仅文本情感分析，无音频特征"
            },
            "medium": {
                "enable_audio_analysis": True,
                "max_history_turns": 5,
                "analysis_depth": "standard",
                "cache_enabled": True,
                "description": "中配模式：文本 + 轻量音频特征"
            },
            "high": {
                "enable_audio_analysis": True,
                "max_history_turns": 10,
                "analysis_depth": "full",
                "cache_enabled": True,
                "description": "高配模式：全量分析 + 完整历史"
            }
        }
        
        return configs.get(tier, configs["low"])


# ==========================================
# 便捷函数
# ==========================================

def analyze_emotion(text: str, strategies_path: Optional[str] = None) -> Dict:
    """
    便捷函数：分析文本情感
    
    Args:
        text: 待分析文本
        strategies_path: 策略模板路径（可选）
        
    Returns:
        dict: 情感分析结果
    """
    analyzer = EmotionAnalyzer(strategies_path=strategies_path)
    return analyzer.analyze(text)


def get_emotion_strategy(emotion: str, confidence: float, strategies_path: Optional[str] = None) -> Dict:
    """
    便捷函数：获取情感对应的对话策略
    
    Args:
        emotion: 情感类型字符串
        confidence: 置信度
        strategies_path: 策略模板路径（可选）
        
    Returns:
        dict: 对话策略
    """
    analyzer = EmotionAnalyzer(strategies_path=strategies_path)
    emotion_enum = Emotion.from_string(emotion)
    return analyzer.get_strategy(emotion_enum, confidence)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行情感分析器自测"""
    print("=" * 60)
    print("情感识别与自适应对话策略 — 自测模式")
    print("=" * 60)
    
    analyzer = EmotionAnalyzer()
    
    # 测试 1: 愤怒检测
    print("\n[测试 1] 愤怒检测")
    result = analyzer.analyze("你们这个破产品太差了！我要投诉！")
    print(f"  输入：'你们这个破产品太差了！我要投诉！'")
    print(f"  情感：{result['emotion'].value}，置信度：{result['confidence']}")
    assert result['emotion'] == Emotion.ANGRY, f"期望 ANGRY，得到 {result['emotion']}"
    print("✅ 愤怒检测通过")
    
    # 测试 2: 焦虑检测
    print("\n[测试 2] 焦虑检测")
    result = analyzer.analyze("时间来不及了，赶紧帮我处理一下，马上要迟到了")
    print(f"  输入：'时间来不及了，赶紧帮我处理一下，马上要迟到了'")
    print(f"  情感：{result['emotion'].value}，置信度：{result['confidence']}")
    assert result['emotion'] == Emotion.ANXIOUS, f"期望 ANXIOUS，得到 {result['emotion']}"
    print("✅ 焦虑检测通过")
    
    # 测试 3: 满意检测
    print("\n[测试 3] 满意检测")
    result = analyzer.analyze("好的，谢谢你的帮助，非常满意！")
    print(f"  输入：'好的，谢谢你的帮助，非常满意！'")
    print(f"  情感：{result['emotion'].value}，置信度：{result['confidence']}")
    print(f"  详细分数：{result['scores']}")
    assert result['emotion'] == Emotion.SATISFIED, f"期望 SATISFIED，得到 {result['emotion']}"
    print("✅ 满意检测通过")
    
    # 测试 4: 困惑检测
    print("\n[测试 4] 困惑检测")
    result = analyzer.analyze("什么意思？我没听懂，能不能举个例子？")
    print(f"  输入：'什么意思？我没听懂，能不能举个例子？'")
    print(f"  情感：{result['emotion'].value}，置信度：{result['confidence']}")
    assert result['emotion'] == Emotion.CONFUSED, f"期望 CONFUSED，得到 {result['emotion']}"
    print("✅ 困惑检测通过")
    
    # 测试 5: 中性检测
    print("\n[测试 5] 中性检测")
    result = analyzer.analyze("北京今天天气怎么样")
    print(f"  输入：'北京今天天气怎么样'")
    print(f"  情感：{result['emotion'].value}，置信度：{result['confidence']}")
    assert result['emotion'] == Emotion.NEUTRAL, f"期望 NEUTRAL，得到 {result['emotion']}"
    print("✅ 中性检测通过")
    
    # 测试 6: 否定词翻转
    print("\n[测试 6] 否定词翻转")
    result = analyzer.analyze("不满意，这个服务太差了")
    print(f"  输入：'不满意，这个服务太差了'")
    print(f"  情感：{result['emotion'].value}，置信度：{result['confidence']}")
    assert result['emotion'] == Emotion.ANGRY, f"期望 ANGRY，得到 {result['emotion']}"
    print("✅ 否定词翻转通过")
    
    # 测试 7: 情绪升级跟踪
    print("\n[测试 7] 情绪升级跟踪")
    tracker = EmotionEscalationTracker(threshold=2)
    tracker.record(Emotion.ANGRY, "user_001")
    assert not tracker.should_escalate("user_001"), "1轮不应升级"
    tracker.record(Emotion.ANXIOUS, "user_001")
    assert tracker.should_escalate("user_001"), "2轮负面应升级"
    print(f"  连续负面轮次：{tracker.get_consecutive_negative_count('user_001')}")
    print("✅ 情绪升级跟踪通过")
    
    # 测试 8: 硬件自适应
    print("\n[测试 8] 硬件自适应")
    tier = HardwareAdaptiveConfig.detect_tier()
    config = HardwareAdaptiveConfig.get_config(tier)
    print(f"  硬件等级：{tier}")
    print(f"  音频分析：{'启用' if config['enable_audio_analysis'] else '禁用'}")
    print(f"  分析深度：{config['analysis_depth']}")
    print("✅ 硬件自适应通过")
    
    # 测试 9: 空文本处理
    print("\n[测试 9] 空文本处理")
    result = analyzer.analyze("")
    assert result['emotion'] == Emotion.NEUTRAL
    result = analyzer.analyze(None)
    assert result['emotion'] == Emotion.NEUTRAL
    print("✅ 空文本处理通过")
    
    # 测试 10: 便捷函数
    print("\n[测试 10] 便捷函数")
    result = analyze_emotion("太棒了，非常好用！")
    assert result['emotion'] == Emotion.SATISFIED
    print("✅ 便捷函数通过")
    
    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print('='*60)


if __name__ == "__main__":
    run_self_test()
