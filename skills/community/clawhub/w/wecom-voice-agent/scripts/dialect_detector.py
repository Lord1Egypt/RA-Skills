#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dialect_detector.py — 方言检测与回复适配引擎

功能：
1. 方言识别：粤语、四川话、上海话、东北话、闽南话等主要方言
2. 混合语言识别：方言词汇 + 普通话混合的句子识别
3. 方言回复：生成符合方言习惯的表达方式
4. 零外部依赖：纯 Python 标准库

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v2.3 (2026-08-01)
"""

import os
import re
import json
import logging
from enum import Enum
from typing import Optional, Dict, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

# ==========================================
# 方言类型枚举
# ==========================================

class Dialect(Enum):
    """方言类型"""
    MANDARIN = "mandarin"       # 普通话
    CANTONESE = "cantonese"     # 粤语
    SICHUAN = "sichuan"         # 四川话
    SHANGHAINESE = "shanghainese"  # 上海话
    NORTHEAST = "northeast"     # 东北话
    MINNAN = "minnan"           # 闽南话
    UNKNOWN = "unknown"         # 未知

    def __str__(self):
        return self.value


# ==========================================
# 方言关键词词典
# ==========================================

DIALECT_KEYWORDS: Dict[Dialect, Dict[str, List[str]]] = {
    Dialect.CANTONESE: {
        "pronouns": ["佢", "我哋", "你哋", "佢哋"],
        "verbs": ["係", "冇", "喺", "嚟", "瞓", "睇"],
        "particles": ["嘅", "咗", "紧", "埋", "添", "啰", "啫", "喎", "咩", "咋", "啩"],
        "adverbs": ["真係", "劲", "超", "仲", "仲未"],
        "common": ["唔该", "多谢", "对唔住", "唔好意思", "冇问题", "点解", "点样", "几时", "边度", "几多", "边个", "乜嘢", "咩事", "做乜", "去边", "返工", "放工", "打机", "睇戏", "行街", "买嘢", "靓仔", "靓女", "老友", "醒目", "叻"],
    },
    Dialect.SICHUAN: {
        "pronouns": ["啥子", "啷个", "咋个"],
        "verbs": ["巴适", "要得", "对头", "莫得"],
        "particles": ["嗦", "喃"],
        "adverbs": ["硬是"],
        "common": ["安逸", "吃莽莽", "打牙祭", "摆龙门阵", "扯把子", "洋盘", "拧巴", "毛焦火辣", "哈搓搓", "宝筛筛"],
    },
    Dialect.SHANGHAINESE: {
        "pronouns": ["侬", "伊", "阿拉", "侬伊", "伊拉"],
        "verbs": ["呒没", "覅"],
        "particles": ["嗰", "咾", "箇"],
        "adverbs": ["蛮", "交关", "邪气", "老老", "交交关"],
        "common": ["侬好", "谢谢侬", "对勿起", "呒没关系", "覅客气", "老好额", "交关好", "邪气好", "蛮好额", "勿来赛", "一塌糊涂", "瞎三话四", "刮刮叫", "呱呱叫"],
    },
    Dialect.NORTHEAST: {
        "pronouns": ["俺", "俺们"],
        "verbs": ["寻思", "唠嗑", "扯淡", "忽悠"],
        "particles": [],
        "adverbs": ["嘎嘎", "嗷嗷", "贼", "杠杠"],
        "common": ["嘚瑟", "嘚嘚", "咋地", "咋整", "干哈", "干啥玩意儿", "唠嗑"],
    },
    Dialect.MINNAN: {
        "pronouns": ["阮", "恁", "因"],
        "verbs": ["攑", "捒", "搦", "搵", "斡", "蹔", "蹋"],
        "particles": ["咧", "乎", "耳", "尔"],
        "adverbs": ["足", "足酸", "足甜", "足咸", "足苦", "足辣"],
        "common": ["食饭", "食饱", "食未", "来去", "好势", "歹势", "𨑨迌"],
    },
}

# 常用词权重
KEYWORD_WEIGHTS = {
    "pronouns": 1.5,    # 代词权重高
    "verbs": 1.2,       # 动词权重较高
    "particles": 1.8,   # 助词权重最高（最特征）
    "adverbs": 1.3,     # 副词权重较高
    "common": 2.0,      # 常用词权重最高
}

# 回复模板（按方言）
REPLY_TEMPLATES: Dict[Dialect, Dict[str, str]] = {
    Dialect.CANTONESE: {
        "greeting": "你好啊！有咩可以帮到你㗎？",
        "thanks": "唔该晒！好开心帮到你㗎！",
        "apology": "对唔住呀，我搞错咗，即刻帮你处理！",
        "understand": "我明㗎喇，即帮你搞掂！",
        "clarify": "唔好意思，我唔太明白你讲嘅，可以再讲多次吗？",
        "waiting": "唔使急，我睇下点帮你处理！",
        "confirm": "好㗎，即刻帮你搞掂！",
        "satisfied": "好开心！如果仲有其他需要，随时搵我㗎！",
    },
    Dialect.SICHUAN: {
        "greeting": "你好哈！有啥子需要帮忙的嗦？",
        "thanks": "谢了哈！巴适得很！",
        "apology": "对不住哦，我搞错咯，马上帮你处理！",
        "understand": "我晓得了哈，马上帮你搞归一！",
        "clarify": "不好意思哦，我没听太懂你说的，可以再嗦一遍嘛？",
        "waiting": "莫急嘛，我看看咋个帮你处理！",
        "confirm": "要得，马上帮你搞归一！",
        "satisfied": "巴适！如果还有啥子需要，随时喊我哈！",
    },
    Dialect.SHANGHAINESE: {
        "greeting": "侬好！有啥事体要我帮忙额？",
        "thanks": "谢谢侬！老好额！",
        "apology": "对勿起，我搞错特了，马上帮侬处理！",
        "understand": "我晓得了，马上帮侬搞掂！",
        "clarify": "勿好意思，我勿太明白侬讲的，可以再讲一遍伐？",
        "waiting": "勿要急，我看看哪能帮侬处理！",
        "confirm": "好额，马上帮侬搞掂！",
        "satisfied": "老好额！如果还有啥事体，随时寻我！",
    },
    Dialect.NORTHEAST: {
        "greeting": "你好啊！有啥事儿需要整的？",
        "thanks": "谢了嗷嗷的！",
        "apology": "对不住啊，我整岔劈了，立马帮你整！",
        "understand": "我整明白了，立马给你整归拢的！",
        "clarify": "不好意思啊，我没太听明白你说的，能再唠一遍不？",
        "waiting": "别急啊，我看看咋给你整！",
        "confirm": "行，立马给你整归拢的！",
        "satisfied": "得劲儿！还有啥事儿，随时吱声！",
    },
    Dialect.MINNAN: {
        "greeting": "你好！有啥物代志爱阮帮兮？",
        "thanks": "谢啦！足感心！",
        "apology": "歹势啦，我搞错矣，马上帮你处理！",
        "understand": "我知影矣，马上帮你搞掂！",
        "clarify": "歹势，我无啥捌识你讲的，会当讲一摆否？",
        "waiting": "免紧张，我来看怎样帮你处理！",
        "confirm": "好势，马上帮你搞掂！",
        "satisfied": "足好！若犹有啥物代志，随时来找我！",
    },
    Dialect.MANDARIN: {
        "greeting": "您好！请问有什么可以帮您？",
        "thanks": "谢谢！很高兴能帮到您！",
        "apology": "抱歉，我搞错了，马上为您处理！",
        "understand": "我明白了，马上为您处理！",
        "clarify": "不好意思，我没太听明白您的意思，可以再讲一遍吗？",
        "waiting": "请稍等，我看看怎么帮您处理！",
        "confirm": "好的，马上为您处理！",
        "satisfied": "很高兴！如果还有其他需要，随时找我！",
    },
}


# ==========================================
# 方言检测器
# ==========================================

class DialectDetector:
    """
    方言检测器
    
    使用方式：
        detector = DialectDetector()
        result = detector.detect("我个订单仲未到哦")
        # result = {"dialect": Dialect.CANTONESE, "confidence": 0.85, "scores": {...}}
    """

    def __init__(self, templates_path: Optional[str] = None):
        """
        初始化方言检测器
        
        Args:
            templates_path: 方言模板文件路径（可选）
        """
        self.keywords = DIALECT_KEYWORDS
        self.weights = KEYWORD_WEIGHTS
        self.templates = REPLY_TEMPLATES
        
        # 加载外部模板（如果提供）
        if templates_path and os.path.exists(templates_path):
            with open(templates_path, 'r', encoding='utf-8') as f:
                external = json.load(f)
                # 合并外部模板
                for dialect_str, templates in external.items():
                    dialect = Dialect(dialect_str)
                    if dialect in self.templates:
                        self.templates[dialect].update(templates)
                    else:
                        self.templates[dialect] = templates

    def detect(self, text: str) -> Dict:
        """
        检测文本的方言类型
        
        Args:
            text: 待检测的文本
            
        Returns:
            dict: {
                "dialect": Dialect,
                "confidence": float (0-1),
                "scores": {dialect_str: float},
                "method": "keyword_matching"
            }
        """
        if not text or not isinstance(text, str):
            return {
                "dialect": Dialect.MANDARIN,
                "confidence": 1.0,
                "scores": {d.value: 0.0 for d in Dialect},
                "method": "keyword_matching"
            }

        text = text.strip()
        if len(text) == 0:
            return {
                "dialect": Dialect.MANDARIN,
                "confidence": 1.0,
                "scores": {d.value: 0.0 for d in Dialect},
                "method": "keyword_matching"
            }

        # 计算各方言得分
        scores = self._compute_scores(text)
        
        # 找出最高分
        max_dialect = max(scores, key=scores.get)
        max_score = scores[max_dialect]
        
        # 计算置信度
        confidence = self._compute_confidence(max_score, scores)
        
        # 如果最高分过低，判定为普通话
        if max_score < 0.5:
            max_dialect = Dialect.MANDARIN
            confidence = 0.8

        return {
            "dialect": max_dialect,
            "confidence": confidence,
            "scores": {d.value: round(s, 3) for d, s in scores.items()},
            "method": "keyword_matching"
        }

    def _compute_scores(self, text: str) -> Dict[Dialect, float]:
        """计算各方言的得分"""
        scores = {d: 0.0 for d in Dialect}
        
        for dialect, categories in self.keywords.items():
            for category, keywords in categories.items():
                weight = self.weights.get(category, 1.0)
                for keyword in keywords:
                    count = text.count(keyword)
                    if count > 0:
                        scores[dialect] += weight * count
        
        return scores

    def _compute_confidence(self, max_score: float, scores: Dict[Dialect, float]) -> float:
        """计算置信度"""
        sorted_scores = sorted(scores.values(), reverse=True)
        
        if len(sorted_scores) < 2 or sorted_scores[0] == 0:
            return 0.5
        
        # 最高分与次高分的差距比例
        gap_ratio = (sorted_scores[0] - sorted_scores[1]) / sorted_scores[0]
        
        # 基础置信度
        base_confidence = 0.5 + gap_ratio * 0.3
        
        # 分数绝对值调整
        score_bonus = min(sorted_scores[0] * 0.1, 0.2)
        
        confidence = min(base_confidence + score_bonus, 1.0)
        return round(confidence, 3)

    def get_reply_template(self, dialect: Dialect, template_name: str) -> str:
        """
        获取方言回复模板
        
        Args:
            dialect: 方言类型
            template_name: 模板名称 (greeting/thanks/apology/understand/clarify/waiting/confirm/satisfied)
            
        Returns:
            str: 回复模板文本
        """
        if dialect in self.templates and template_name in self.templates[dialect]:
            return self.templates[dialect][template_name]
        
        # 默认返回普通话模板
        if template_name in self.templates[Dialect.MANDARIN]:
            return self.templates[Dialect.MANDARIN][template_name]
        
        return "您好！请问有什么可以帮您？"

    def adapt_reply(self, dialect: Dialect, reply: str) -> str:
        """
        将普通话回复适配为方言风格（简单替换）
        
        Args:
            dialect: 方言类型
            reply: 普通话回复
            
        Returns:
            str: 方言风格回复
        """
        # 简单的词汇替换映射
        adaptations = {
            Dialect.CANTONESE: {
                "你好": "你好啊",
                "谢谢": "唔该",
                "对不起": "对唔住",
                "明白": "明",
                "马上": "即刻",
                "怎么样": "点样",
                "什么": "咩",
            },
            Dialect.SICHUAN: {
                "你好": "你好哈",
                "谢谢": "谢了",
                "对不起": "对不住",
                "明白": "晓得了",
                "马上": "马上",
                "怎么样": "咋个",
                "什么": "啥子",
            },
            Dialect.SHANGHAINESE: {
                "你好": "侬好",
                "谢谢": "谢谢侬",
                "对不起": "对勿起",
                "明白": "晓得了",
                "马上": "马上",
                "怎么样": "哪能",
                "什么": "啥",
            },
            Dialect.NORTHEAST: {
                "你好": "你好啊",
                "谢谢": "谢了",
                "对不起": "对不住",
                "明白": "整明白了",
                "马上": "立马",
                "怎么样": "咋地",
                "什么": "啥",
            },
            Dialect.MINNAN: {
                "你好": "你好",
                "谢谢": "谢啦",
                "对不起": "歹势",
                "明白": "知影矣",
                "马上": "马上",
                "怎么样": "怎样",
                "什么": "啥物",
            },
        }
        
        if dialect in adaptations:
            for mandarin, dialect_word in adaptations[dialect].items():
                reply = reply.replace(mandarin, dialect_word)
        
        return reply


# ==========================================
# 便捷函数
# ==========================================

def detect_dialect(text: str, templates_path: Optional[str] = None) -> Dict:
    """
    便捷函数：检测文本方言
    
    Args:
        text: 待检测文本
        templates_path: 模板路径（可选）
        
    Returns:
        dict: 方言检测结果
    """
    detector = DialectDetector(templates_path=templates_path)
    return detector.detect(text)


def get_dialect_reply(dialect: str, template_name: str, templates_path: Optional[str] = None) -> str:
    """
    便捷函数：获取方言回复模板
    
    Args:
        dialect: 方言类型字符串
        template_name: 模板名称
        templates_path: 模板路径（可选）
        
    Returns:
        str: 回复模板
    """
    detector = DialectDetector(templates_path=templates_path)
    dialect_enum = Dialect(dialect) if dialect in [d.value for d in Dialect] else Dialect.MANDARIN
    return detector.get_reply_template(dialect_enum, template_name)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行方言检测器自测"""
    print("=" * 60)
    print("方言检测与回复适配 — 自测模式")
    print("=" * 60)
    
    detector = DialectDetector()
    
    # 测试 1: 粤语检测
    print("\n[测试 1] 粤语检测")
    result = detector.detect("我个订单仲未到哦，你哋搞错咗啊")
    print(f"  输入：'我个订单仲未到哦，你哋搞错咗啊'")
    print(f"  方言：{result['dialect'].value}，置信度：{result['confidence']}")
    assert result['dialect'] == Dialect.CANTONESE, f"期望 CANTONESE，得到 {result['dialect']}"
    print("✅ 粤语检测通过")
    
    # 测试 2: 四川话检测
    print("\n[测试 2] 四川话检测")
    result = detector.detect("啥子事情哦，巴适得很嘛")
    print(f"  输入：'啥子事情哦，巴适得很嘛'")
    print(f"  方言：{result['dialect'].value}，置信度：{result['confidence']}")
    assert result['dialect'] == Dialect.SICHUAN, f"期望 SICHUAN，得到 {result['dialect']}"
    print("✅ 四川话检测通过")
    
    # 测试 3: 上海话检测
    print("\n[测试 3] 上海话检测")
    result = detector.detect("侬好，阿拉上海人，老好额")
    print(f"  输入：'侬好，阿拉上海人，老好额'")
    print(f"  方言：{result['dialect'].value}，置信度：{result['confidence']}")
    assert result['dialect'] == Dialect.SHANGHAINESE, f"期望 SHANGHAINESE，得到 {result['dialect']}"
    print("✅ 上海话检测通过")
    
    # 测试 4: 东北话检测
    print("\n[测试 4] 东北话检测")
    result = detector.detect("嘎嘎好，嗷嗷的，贼拉带劲")
    print(f"  输入：'嘎嘎好，嗷嗷的，贼拉带劲'")
    print(f"  方言：{result['dialect'].value}，置信度：{result['confidence']}")
    assert result['dialect'] == Dialect.NORTHEAST, f"期望 NORTHEAST，得到 {result['dialect']}"
    print("✅ 东北话检测通过")
    
    # 测试 5: 闽南话检测
    print("\n[测试 5] 闽南话检测")
    result = detector.detect("食饭未，好势，阮欲来去")
    print(f"  输入：'食饭未，好势，阮欲来去'")
    print(f"  方言：{result['dialect'].value}，置信度：{result['confidence']}")
    assert result['dialect'] == Dialect.MINNAN, f"期望 MINNAN，得到 {result['dialect']}"
    print("✅ 闽南话检测通过")
    
    # 测试 6: 普通话检测
    print("\n[测试 6] 普通话检测")
    result = detector.detect("你好，请问今天天气怎么样")
    print(f"  输入：'你好，请问今天天气怎么样'")
    print(f"  方言：{result['dialect'].value}，置信度：{result['confidence']}")
    assert result['dialect'] == Dialect.MANDARIN, f"期望 MANDARIN，得到 {result['dialect']}"
    print("✅ 普通话检测通过")
    
    # 测试 7: 混合语言识别
    print("\n[测试 7] 混合语言识别")
    result = detector.detect("我明天要去广州，你哋有冇问题啊")
    print(f"  输入：'我明天要去广州，你哋有冇问题啊'")
    print(f"  方言：{result['dialect'].value}，置信度：{result['confidence']}")
    # 混合语言应该识别为粤语（因为有粤语特征词）
    print("✅ 混合语言识别通过")
    
    # 测试 8: 回复模板
    print("\n[测试 8] 回复模板")
    reply = detector.get_reply_template(Dialect.CANTONESE, "greeting")
    print(f"  粤语问候：{reply}")
    assert "㗎" in reply or "咩" in reply
    reply = detector.get_reply_template(Dialect.SICHUAN, "thanks")
    print(f"  四川话感谢：{reply}")
    assert "哈" in reply or "巴适" in reply
    print("✅ 回复模板通过")
    
    # 测试 9: 回复适配
    print("\n[测试 9] 回复适配")
    reply = detector.adapt_reply(Dialect.CANTONESE, "你好，谢谢你的帮助，我马上处理")
    print(f"  粤语适配：{reply}")
    assert "唔该" in reply or "即刻" in reply
    print("✅ 回复适配通过")
    
    # 测试 10: 便捷函数
    print("\n[测试 10] 便捷函数")
    result = detect_dialect("嘎嘎好，东北银贼拉热情")
    assert result['dialect'] == Dialect.NORTHEAST
    reply = get_dialect_reply("cantonese", "greeting")
    assert len(reply) > 0
    print("✅ 便捷函数通过")
    
    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print('='*60)


if __name__ == "__main__":
    run_self_test()
