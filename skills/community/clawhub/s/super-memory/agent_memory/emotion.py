from __future__ import annotations
"""
emotion.py - Production-Grade Emotion Analysis Engine

Architecture:
  Layer 1: Plutchik 8-dimension rule engine (fast baseline)
  Layer 2: Intensity calibration (modifiers, negation, context)
  Layer 3: Compound emotion synthesis (dyads)
  Layer 4: LLM refinement (ambiguous/ironic content)

Dimensions:
  - valence: [-1.0, 1.0] (negative → positive)
  - arousal: [0.0, 1.0] (calm → excited)
  - dominance: [0.0, 1.0] (submissive → dominant)
  - primary_emotions: Plutchik 8-vector (joy, trust, fear, surprise,
                      sadness, disgust, anger, anticipation)
  - compound_emotions: detected dyads (love, awe, remorse, etc.)
  - significance: trivial/notable/important/breakthrough/crisis/milestone
  - confidence: [0.0, 1.0]
  - nuance: literal/implicit/contradictory/ironic/sarcastic
  - boundaries: emotional shift points within text

⚠️ 情感安全边界 (Emotional Safety Boundaries):

  本系统是**情感分析工具**，不是**情感体验系统**。
  Agent 不会"感受"情感，只会"识别"和"标注"情感。

  为防止情感数据导致类人行为问题，系统实施以下防护：

  1. 动机下限 (MOMENTUM_FLOOR=0.15): Agent 的学习动量不会因
     持续负面 valence 降至零。Agent 不会"害怕"到停止工作。

  2. 情感共振回音壁防护: 负面查询(valence<-0.15)不使用情感
     共振检索，防止负面查询只返回负面记忆的螺旋效应。

  3. 情感基调回归: 人格画像中的 positive_bias 向中性回归 30%，
     防止大量负面记忆导致持久"偏批判"人格。

  4. 行动导向共情: 所有负面情感的共情响应都包含"下一步行动"，
     而非仅表达同情。Agent 不会陷入"共情循环"。

  5. 情感数据是元数据: 情感标注存储为数据库列/JSON，不直接
     驱动行为决策。所有行为影响都经过显式防护层。
"""

import re
import json
import math
import time
import logging
from typing import Optional, Callable, Dict, List, Tuple

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# Plutchik 8 Primary Emotions
# ═══════════════════════════════════════════════════════════════

PLUTCHIK_PRIMARY = ["joy", "trust", "fear", "surprise", "sadness", "disgust", "anger", "anticipation"]

PLUTCHIK_DYADS = {
    "love": ("joy", "trust"),
    "optimism": ("anticipation", "joy"),
    "aggressiveness": ("anger", "anticipation"),
    "contempt": ("anger", "disgust"),
    "awe": ("fear", "surprise"),
    "remorse": ("sadness", "disgust"),
    "disapproval": ("surprise", "sadness"),
    "submission": ("fear", "trust"),
    "alarm": ("fear", "anticipation"),
    "interest": ("anticipation", "trust"),
    "pride": ("joy", "anger"),
    "shame": ("sadness", "fear"),
    "envy": ("disgust", "sadness"),
    "cruelty": ("anger", "sadness"),
    "anxiety": ("fear", "anticipation"),
    "morbidness": ("disgust", "joy"),
    "resignation": ("sadness", "trust"),
    "curiosity": ("surprise", "trust"),
    "cynicism": ("disgust", "anticipation"),
    "dominance": ("anger", "trust"),
    "despair": ("sadness", "fear"),
    "hope": ("anticipation", "trust"),
    "delight": ("joy", "surprise"),
    "outrage": ("anger", "surprise"),
}

PLUTCHIK_DYAD_THRESHOLD = 0.3

# ═══════════════════════════════════════════════════════════════
# Expanded Bilingual Sentiment Dictionaries (with intensity weights)
# Weight: 0.3=low, 0.5=medium, 0.7=high, 1.0=extreme
# ═══════════════════════════════════════════════════════════════

POSITIVE_WORDS_CN = {
    "成功": 0.9, "突破": 0.9, "优秀": 0.8, "完美": 0.9, "出色": 0.8,
    "精彩": 0.8, "惊喜": 0.7, "高效": 0.6, "解决了": 0.7, "搞定了": 0.7,
    "完成了": 0.6, "实现了": 0.7, "攻克": 0.8, "突破性": 0.9,
    "好用": 0.5, "稳定": 0.5, "流畅": 0.5, "优雅": 0.6, "漂亮": 0.6,
    "厉害": 0.7, "赞": 0.7, "开心": 0.7, "满意": 0.6, "值得": 0.5,
    "幸运": 0.7, "顺利": 0.5, "进步": 0.6, "提升": 0.6, "优化": 0.5,
    "新增": 0.3, "支持": 0.3, "兼容": 0.3, "改善": 0.4, "升级": 0.5,
    "加强": 0.4, "棒": 0.7, "好": 0.4, "不错": 0.5, "很好": 0.6,
    "强大": 0.7, "简洁": 0.5, "清晰": 0.5, "可靠": 0.5, "安全": 0.4,
    "快速": 0.5, "方便": 0.5, "轻松": 0.5, "愉快": 0.7, "兴奋": 0.8,
    "激动": 0.8, "自豪": 0.7, "骄傲": 0.7, "感谢": 0.6, "喜欢": 0.6,
    "爱": 0.8, "享受": 0.7, "欣赏": 0.6, "认可": 0.5, "肯定": 0.5,
    "正确": 0.4, "合理": 0.4, "创新": 0.7, "先进": 0.6, "领先": 0.7,
    "卓越": 0.8, "杰出": 0.8, "辉煌": 0.9, "胜利": 0.8, "赢": 0.7,
    "收益": 0.5, "价值": 0.5, "增长": 0.5, "繁荣": 0.7,
    "和谐": 0.6, "温暖": 0.6, "美好": 0.7, "幸福": 0.8, "快乐": 0.8,
    "欣慰": 0.6, "踏实": 0.5, "安心": 0.5, "放心": 0.5, "信任": 0.6,
    "期待": 0.6, "希望": 0.6, "憧憬": 0.7, "向往": 0.6, "鼓舞": 0.7,
    "振奋": 0.8, "感动": 0.7, "敬佩": 0.7, "尊重": 0.5, "珍惜": 0.6,
    "治愈": 0.7, "安慰": 0.5, "鼓励": 0.6, "支持": 0.5, "帮助": 0.4,
    "合作": 0.4, "团结": 0.5, "友谊": 0.6, "亲密": 0.6, "默契": 0.6,
    "成长": 0.6, "成熟": 0.5, "蜕变": 0.7, "超越": 0.8,
    "飞跃": 0.9, "跨越": 0.8, "里程碑": 0.9, "转折点": 0.8,
}

POSITIVE_WORDS_EN = {
    "great": 0.7, "excellent": 0.8, "amazing": 0.8, "perfect": 0.9,
    "solved": 0.7, "fixed": 0.6, "breakthrough": 0.9, "success": 0.8,
    "improved": 0.6, "optimized": 0.5, "works": 0.5, "love": 0.8,
    "awesome": 0.8, "fantastic": 0.8, "brilliant": 0.8, "elegant": 0.6,
    "beautiful": 0.7, "wonderful": 0.8, "superb": 0.8, "outstanding": 0.8,
    "remarkable": 0.7, "impressive": 0.7, "delightful": 0.7, "pleased": 0.6,
    "happy": 0.7, "glad": 0.6, "excited": 0.8, "thrilled": 0.8,
    "proud": 0.7, "grateful": 0.6, "thankful": 0.6, "appreciate": 0.6,
    "enjoy": 0.6, "admire": 0.6, "respect": 0.5, "trust": 0.6,
    "innovative": 0.7, "creative": 0.6, "advanced": 0.6, "leading": 0.7,
    "reliable": 0.5, "stable": 0.5, "efficient": 0.5, "smooth": 0.5,
    "fast": 0.5, "easy": 0.5, "simple": 0.4, "clean": 0.5,
    "powerful": 0.7, "strong": 0.6, "solid": 0.5, "robust": 0.5,
    "good": 0.4, "nice": 0.4, "fine": 0.3, "ok": 0.2,
    "win": 0.7, "victory": 0.8, "achieve": 0.7, "accomplish": 0.7,
    "growth": 0.5, "progress": 0.6, "advance": 0.6, "milestone": 0.9,
    "hope": 0.6, "inspire": 0.7, "encourage": 0.6, "support": 0.5,
    "help": 0.4, "comfort": 0.5, "peace": 0.5, "harmony": 0.6,
    "joy": 0.8, "bliss": 0.9, "ecstasy": 1.0, "euphoria": 1.0,
}

NEGATIVE_WORDS_CN = {
    "失败": 0.9, "崩溃": 0.9, "bug": 0.6, "错误": 0.7, "问题": 0.5,
    "故障": 0.8, "挂了": 0.8, "炸了": 0.8, "不行": 0.6, "糟糕": 0.8,
    "失望": 0.7, "困难": 0.5, "麻烦": 0.5, "卡住": 0.5, "卡死": 0.7,
    "死锁": 0.7, "超时": 0.5, "泄漏": 0.6, "异常": 0.6, "警告": 0.4,
    "风险": 0.5, "隐患": 0.5, "漏洞": 0.7, "缺陷": 0.6, "回滚": 0.5,
    "回退": 0.5, "放弃": 0.6, "删除": 0.3, "移除": 0.3, "废弃": 0.5,
    "弃用": 0.5, "慢": 0.4, "卡": 0.5, "坑": 0.5, "踩坑": 0.5,
    "绕过": 0.4, "临时": 0.3, "愤怒": 0.9, "生气": 0.7, "恼火": 0.7,
    "烦躁": 0.6, "焦虑": 0.7, "担忧": 0.6, "害怕": 0.7, "恐惧": 0.9,
    "恐慌": 0.9, "紧张": 0.5, "不安": 0.6, "沮丧": 0.8, "消沉": 0.7,
    "抑郁": 0.9, "绝望": 1.0, "无助": 0.8, "无奈": 0.6, "困惑": 0.4,
    "迷茫": 0.5, "纠结": 0.5, "矛盾": 0.4, "后悔": 0.7, "遗憾": 0.6,
    "惋惜": 0.5, "痛心": 0.8, "伤心": 0.8, "难过": 0.7, "悲伤": 0.8,
    "痛苦": 0.9, "折磨": 0.9, "煎熬": 0.8, "厌恶": 0.8, "反感": 0.7,
    "恶心": 0.8, "鄙视": 0.7, "轻蔑": 0.7, "不屑": 0.6, "嘲笑": 0.6,
    "讽刺": 0.5, "批评": 0.5, "指责": 0.6, "抱怨": 0.5, "不满": 0.6,
    "委屈": 0.6, "冤枉": 0.7, "不公": 0.7, "歧视": 0.8, "偏见": 0.6,
    "误解": 0.5, "冲突": 0.6, "对抗": 0.7, "敌意": 0.8, "仇恨": 0.9,
    "报复": 0.9, "破坏": 0.8, "损害": 0.7, "损失": 0.7, "浪费": 0.5,
    "拖累": 0.6, "阻碍": 0.5, "干扰": 0.5, "混乱": 0.6, "失控": 0.8,
    "危险": 0.7, "威胁": 0.7, "紧急": 0.6, "严重": 0.7, "致命": 0.9,
    "灾难": 0.9, "事故": 0.8, "伤亡": 0.9, "悲剧": 0.9, "惨": 0.8,
}

NEGATIVE_WORDS_EN = {
    "failed": 0.8, "error": 0.7, "bug": 0.6, "crash": 0.9, "broken": 0.7,
    "issue": 0.5, "problem": 0.5, "terrible": 0.8, "horrible": 0.9,
    "disappointed": 0.7, "difficult": 0.5, "slow": 0.4, "timeout": 0.5,
    "leak": 0.6, "exception": 0.6, "warning": 0.4, "risk": 0.5,
    "rollback": 0.5, "workaround": 0.4, "hack": 0.4, "deprecated": 0.5,
    "removed": 0.3, "angry": 0.8, "furious": 0.9, "rage": 0.9,
    "frustrated": 0.7, "annoyed": 0.6, "irritated": 0.6, "upset": 0.7,
    "anxious": 0.7, "worried": 0.6, "afraid": 0.7, "scared": 0.8,
    "terrified": 0.9, "panic": 0.9, "nervous": 0.5, "uneasy": 0.6,
    "depressed": 0.9, "hopeless": 1.0, "desperate": 0.9, "helpless": 0.8,
    "confused": 0.4, "lost": 0.5, "uncertain": 0.4, "doubtful": 0.5,
    "regret": 0.7, "sorry": 0.5, "sad": 0.7, "unhappy": 0.6,
    "miserable": 0.9, "suffering": 0.9, "pain": 0.8, "hurt": 0.7,
    "disgusted": 0.8, "revolted": 0.8, "contempt": 0.7, "scorn": 0.7,
    "mock": 0.6, "criticize": 0.5, "blame": 0.6, "complain": 0.5,
    "unfair": 0.7, "injustice": 0.8, "discrimination": 0.8, "bias": 0.6,
    "misunderstanding": 0.5, "conflict": 0.6, "hostile": 0.8, "hate": 0.9,
    "revenge": 0.9, "destroy": 0.8, "damage": 0.7, "loss": 0.7,
    "waste": 0.5, "obstacle": 0.5, "interfere": 0.5, "chaos": 0.6,
    "out_of_control": 0.8, "dangerous": 0.7, "threat": 0.7, "urgent": 0.6,
    "severe": 0.7, "fatal": 0.9, "disaster": 0.9, "tragedy": 0.9,
    "catastrophe": 1.0, "crisis": 0.8, "incident": 0.6,
}

# ═══════════════════════════════════════════════════════════════
# Plutchik Emotion Dictionaries (word → {emotion: weight})
# ═══════════════════════════════════════════════════════════════

EMOTION_WORDS_CN = {
    "joy": {
        "开心": 0.7, "快乐": 0.8, "高兴": 0.7, "愉快": 0.7, "欢乐": 0.8,
        "幸福": 0.9, "兴奋": 0.8, "激动": 0.8, "欣喜": 0.7, "喜悦": 0.8,
        "满足": 0.6, "满意": 0.6, "享受": 0.7, "陶醉": 0.8, "狂喜": 0.9,
        "乐": 0.5, "笑": 0.5, "好玩": 0.6, "有趣": 0.5, "精彩": 0.7,
        "赞": 0.6, "棒": 0.7, "厉害": 0.7, "完美": 0.9, "出色": 0.7,
        "成功": 0.8, "胜利": 0.8, "赢": 0.7, "突破": 0.8, "搞定": 0.7,
    },
    "trust": {
        "信任": 0.7, "相信": 0.6, "依赖": 0.5, "可靠": 0.5, "安全": 0.5,
        "放心": 0.5, "踏实": 0.5, "安心": 0.5, "确定": 0.4, "肯定": 0.5,
        "认可": 0.5, "接受": 0.4, "支持": 0.5, "合作": 0.4, "团结": 0.5,
        "友谊": 0.6, "亲密": 0.6, "忠诚": 0.7, "诚实": 0.6, "真诚": 0.6,
        "尊重": 0.5, "敬佩": 0.6, "崇拜": 0.7, "感恩": 0.6, "感谢": 0.5,
        "稳定": 0.4, "一致": 0.4, "承诺": 0.5, "保证": 0.5, "守护": 0.6,
    },
    "fear": {
        "害怕": 0.7, "恐惧": 0.9, "担心": 0.5, "担忧": 0.6, "焦虑": 0.7,
        "紧张": 0.5, "不安": 0.6, "恐慌": 0.9, "惊恐": 0.9, "畏惧": 0.8,
        "战栗": 0.9, "颤抖": 0.7, "心慌": 0.7, "忐忑": 0.6, "忧虑": 0.6,
        "威胁": 0.7, "危险": 0.7, "风险": 0.5, "隐患": 0.5, "漏洞": 0.6,
        "崩溃": 0.8, "故障": 0.6, "事故": 0.7, "灾难": 0.9, "危机": 0.8,
        "致命": 0.9, "严重": 0.6, "紧急": 0.6, "超时": 0.4, "死锁": 0.6,
    },
    "surprise": {
        "惊讶": 0.7, "意外": 0.6, "震惊": 0.8, "吃惊": 0.7,
        "没想到": 0.6, "竟然": 0.6, "居然": 0.6, "突然": 0.5, "忽然": 0.5,
        "惊喜": 0.7, "惊吓": 0.7, "不可思议": 0.8, "难以置信": 0.8,
        "出乎意料": 0.7, "始料未及": 0.7, "跌破眼镜": 0.8, "目瞪口呆": 0.8,
        "发现": 0.4, "揭示": 0.5, "揭晓": 0.5, "揭露": 0.6,
        "新": 0.3, "首次": 0.5, "前所未有": 0.7, "史无前例": 0.8,
    },
    "sadness": {
        "悲伤": 0.8, "难过": 0.7, "伤心": 0.8, "痛苦": 0.9, "哀伤": 0.8,
        "沮丧": 0.7, "消沉": 0.7, "低落": 0.6, "忧郁": 0.7, "抑郁": 0.9,
        "失望": 0.6, "绝望": 1.0, "无助": 0.8, "无奈": 0.6, "遗憾": 0.5,
        "惋惜": 0.5, "痛心": 0.8, "心碎": 0.9, "落寞": 0.6, "孤独": 0.7,
        "寂寞": 0.6, "空虚": 0.6, "迷茫": 0.5, "失败": 0.7, "放弃": 0.6,
        "失去": 0.7, "离别": 0.7, "思念": 0.6, "怀念": 0.5, "追忆": 0.5,
    },
    "disgust": {
        "厌恶": 0.8, "恶心": 0.8, "反感": 0.7, "鄙视": 0.7, "轻蔑": 0.7,
        "不屑": 0.6, "嫌弃": 0.7, "排斥": 0.6, "抵触": 0.6, "厌烦": 0.6,
        "烦": 0.5, "讨厌": 0.7, "恶心": 0.8, "作呕": 0.9, "龌龊": 0.8,
        "肮脏": 0.7, "污秽": 0.7, "卑鄙": 0.8, "下流": 0.8, "无耻": 0.8,
        "虚伪": 0.7, "欺骗": 0.7, "背叛": 0.8, "腐败": 0.7, "堕落": 0.7,
        "丑陋": 0.6, "拙劣": 0.5, "糟糕": 0.6, "垃圾": 0.7, "废物": 0.7,
    },
    "anger": {
        "愤怒": 0.9, "生气": 0.7, "恼火": 0.7, "暴怒": 1.0, "狂怒": 1.0,
        "发火": 0.7, "发怒": 0.8, "气愤": 0.7, "愤慨": 0.8, "愤恨": 0.8,
        "怨恨": 0.8, "仇恨": 0.9, "敌意": 0.8, "报复": 0.9, "不满": 0.5,
        "抱怨": 0.5, "指责": 0.6, "批评": 0.5, "谴责": 0.7, "抗议": 0.7,
        "反对": 0.5, "拒绝": 0.5, "抵抗": 0.6, "反击": 0.7, "对抗": 0.7,
        "冲突": 0.6, "争论": 0.5, "吵架": 0.7, "打架": 0.8, "攻击": 0.8,
    },
    "anticipation": {
        "期待": 0.6, "期望": 0.6, "盼望": 0.7, "渴望": 0.8, "向往": 0.6,
        "憧憬": 0.7, "预计": 0.4, "预测": 0.4, "计划": 0.3, "准备": 0.3,
        "即将": 0.4, "未来": 0.3, "目标": 0.3, "追求": 0.5, "努力": 0.4,
        "希望": 0.5, "愿景": 0.5, "蓝图": 0.4, "规划": 0.3, "展望": 0.4,
        "好奇": 0.5, "探索": 0.4, "尝试": 0.3, "实验": 0.3, "测试": 0.3,
        "新": 0.3, "下一步": 0.4, "待办": 0.2, "进行中": 0.3, "计划中": 0.3,
    },
}

EMOTION_WORDS_EN = {
    "joy": {
        "happy": 0.7, "joyful": 0.8, "delighted": 0.7, "cheerful": 0.7,
        "glad": 0.6, "pleased": 0.6, "thrilled": 0.8, "ecstatic": 0.9,
        "elated": 0.8, "blissful": 0.9, "content": 0.6, "satisfied": 0.6,
        "enjoy": 0.6, "fun": 0.6, "amusing": 0.5, "wonderful": 0.8,
        "great": 0.6, "awesome": 0.7, "fantastic": 0.8, "excellent": 0.7,
        "success": 0.7, "win": 0.7, "victory": 0.8, "breakthrough": 0.8,
        "love": 0.8, "adore": 0.8, "celebrate": 0.7, "proud": 0.7,
    },
    "trust": {
        "trust": 0.7, "believe": 0.6, "rely": 0.5, "confident": 0.6,
        "secure": 0.5, "safe": 0.5, "certain": 0.5, "sure": 0.5,
        "accept": 0.4, "support": 0.5, "cooperate": 0.4, "loyal": 0.7,
        "honest": 0.6, "sincere": 0.6, "respect": 0.5, "admire": 0.6,
        "grateful": 0.6, "thankful": 0.5, "stable": 0.4, "consistent": 0.4,
        "promise": 0.5, "guarantee": 0.5, "protect": 0.6, "dependable": 0.5,
    },
    "fear": {
        "afraid": 0.7, "scared": 0.8, "terrified": 0.9, "fearful": 0.8,
        "anxious": 0.7, "worried": 0.6, "nervous": 0.5, "uneasy": 0.6,
        "panic": 0.9, "dread": 0.9, "horror": 0.9, "frightened": 0.8,
        "alarmed": 0.7, "threat": 0.7, "danger": 0.7, "risk": 0.5,
        "crash": 0.7, "failure": 0.6, "incident": 0.5, "crisis": 0.8,
        "fatal": 0.9, "severe": 0.6, "urgent": 0.6, "timeout": 0.4,
    },
    "surprise": {
        "surprised": 0.7, "amazed": 0.7, "astonished": 0.8, "shocked": 0.8,
        "unexpected": 0.6, "stunned": 0.8, "startled": 0.7, "unexpectedly": 0.6,
        "unbelievable": 0.8, "incredible": 0.7, "remarkable": 0.6,
        "discovered": 0.4, "revealed": 0.5, "unprecedented": 0.7,
        "new": 0.3, "first": 0.5, "never_before": 0.7, "suddenly": 0.5,
    },
    "sadness": {
        "sad": 0.7, "unhappy": 0.6, "depressed": 0.9, "miserable": 0.9,
        "heartbroken": 0.9, "grief": 0.9, "sorrow": 0.8, "melancholy": 0.7,
        "disappointed": 0.6, "hopeless": 1.0, "helpless": 0.8, "lonely": 0.7,
        "lost": 0.5, "regret": 0.7, "sorry": 0.5, "miss": 0.5,
        "failed": 0.7, "give_up": 0.6, "pain": 0.8,
        "suffering": 0.9, "agony": 0.9, "despair": 1.0, "gloomy": 0.6,
    },
    "disgust": {
        "disgusted": 0.8, "revolted": 0.8, "repulsed": 0.8, "nauseated": 0.8,
        "contempt": 0.7, "scorn": 0.7, "loathe": 0.9, "detest": 0.9,
        "hate": 0.8, "abhor": 0.9, "despise": 0.8, "dislike": 0.5,
        "repelled": 0.7, "sickened": 0.8, "offended": 0.6, "appalled": 0.8,
        "hypocrite": 0.7, "corrupt": 0.7, "vile": 0.8, "filthy": 0.7,
        "trash": 0.6, "garbage": 0.7, "pathetic": 0.7, "worthless": 0.8,
    },
    "anger": {
        "angry": 0.8, "furious": 0.9, "rage": 0.9, "outraged": 0.9,
        "irritated": 0.6, "annoyed": 0.6, "frustrated": 0.7, "enraged": 1.0,
        "hostile": 0.8, "resentful": 0.7, "bitter": 0.7, "indignant": 0.8,
        "complain": 0.5, "blame": 0.6, "criticize": 0.5, "condemn": 0.7,
        "protest": 0.7, "oppose": 0.5, "reject": 0.5, "resist": 0.6,
        "fight": 0.7, "attack": 0.8, "conflict": 0.6, "argue": 0.5,
    },
    "anticipation": {
        "expect": 0.5, "anticipate": 0.6, "look_forward": 0.7, "eager": 0.7,
        "hope": 0.5, "wish": 0.5, "desire": 0.6, "aspire": 0.6,
        "plan": 0.3, "prepare": 0.3, "upcoming": 0.4, "future": 0.3,
        "goal": 0.3, "pursue": 0.5, "strive": 0.4, "curious": 0.5,
        "explore": 0.4, "try": 0.3, "experiment": 0.3, "test": 0.3,
        "next": 0.3, "vision": 0.5, "roadmap": 0.4, "schedule": 0.3,
    },
}

# ═══════════════════════════════════════════════════════════════
# Intensity Modifiers
# ═══════════════════════════════════════════════════════════════

INTENSIFIERS_CN = {
    "非常": 1.5, "极其": 1.8, "特别": 1.4, "十分": 1.5, "相当": 1.3,
    "超级": 1.6, "极度": 1.8, "异常": 1.5, "格外": 1.4, "尤为": 1.4,
    "太": 1.5, "真": 1.3, "好": 1.2, "超": 1.4, "巨": 1.5,
    "贼": 1.4, "绝了": 1.7, "无比": 1.6, "万分": 1.7,
    "至极": 1.9, "极致": 1.8, "透顶": 1.9, "到家": 1.5,
}

INTENSIFIERS_EN = {
    "very": 1.4, "extremely": 1.7, "incredibly": 1.6, "absolutely": 1.7,
    "really": 1.3, "truly": 1.4, "super": 1.5, "ultra": 1.6,
    "utterly": 1.6, "completely": 1.5, "totally": 1.5, "highly": 1.4,
    "remarkably": 1.4, "exceptionally": 1.6, "extraordinarily": 1.7,
    "insanely": 1.6, "terribly": 1.5, "awfully": 1.5, "so": 1.3,
}

DIMINISHERS_CN = {
    "有点": 0.6, "稍微": 0.5, "略微": 0.5, "些许": 0.5, "一点": 0.6,
    "勉强": 0.5, "还算": 0.7, "尚可": 0.6, "凑合": 0.5, "一般": 0.4,
    "还行": 0.6, "差不多": 0.6, "略": 0.6, "稍": 0.6,
}

DIMINISHERS_EN = {
    "slightly": 0.5, "somewhat": 0.6, "a_bit": 0.5, "kind_of": 0.6,
    "sort_of": 0.6, "fairly": 0.7, "moderately": 0.6, "rather": 0.7,
    "mildly": 0.5, "marginally": 0.4, "reasonably": 0.7, "passably": 0.5,
}

# ═══════════════════════════════════════════════════════════════
# Negation Words
# ═══════════════════════════════════════════════════════════════

NEGATION_WORDS_CN = {
    "不", "没", "没有", "无", "非", "未", "别", "莫", "勿", "否",
    "不是", "不会", "不能", "不要", "不再", "不太", "不怎么",
    "并非", "绝不", "毫不", "从不", "毫无", "决不", "万万不",
}

NEGATION_WORDS_EN = {
    "not", "no", "never", "neither", "nor", "none", "nobody",
    "nothing", "nowhere", "hardly", "barely", "scarcely",
    "don't", "doesn't", "didn't", "won't", "wouldn't", "couldn't",
    "shouldn't", "isn't", "aren't", "wasn't", "weren't", "haven't",
    "hasn't", "hadn't", "cannot", "without",
}

# ═══════════════════════════════════════════════════════════════
# High Arousal Words
# ═══════════════════════════════════════════════════════════════

HIGH_AROUSAL_WORDS = {
    "！", "！！", "！！！", "!!!", "卧槽", "牛", "太棒了", "终于",
    "竟然", "居然", "紧急", "马上", "立刻", "赶紧", "快", "严重",
    "重大", "关键", "崩溃", "挂了", "炸了", "出事了", "不行了",
    "救命", "突破", "搞定", "解决", "攻克", "wtf", "omg", "holy",
    "urgent", "critical", "emergency", "immediately", "now",
    "breaking", "alert", "fatal", "catastrophic",
}

# ═══════════════════════════════════════════════════════════════
# Significance Keywords
# ═══════════════════════════════════════════════════════════════

SIGNIFICANCE_KEYWORDS = {
    "breakthrough": {"突破", "突破性", "攻克", "首创", "第一次", "里程碑", "breakthrough", "milestone", "pioneered"},
    "crisis": {"崩溃", "故障", "事故", "紧急", "严重", "crisis", "outage", "incident", "catastrophe"},
    "milestone": {"发布", "上线", "完成", "交付", "里程碑", "launched", "shipped", "released", "deployed"},
}

# ═══════════════════════════════════════════════════════════════
# Contrast Markers
# ═══════════════════════════════════════════════════════════════

CONTRAST_PATTERNS = [
    re.compile(r"(?:虽然|尽管)(.*?)(?:但是|但|然而|可是|却)(.*)", re.DOTALL),
    re.compile(r"(.*?)(?:但是|但|然而|可是|不过)(.*)", re.DOTALL),
    re.compile(r"(.*?)(?:though|although|but|however|yet|despite)(.*)", re.IGNORECASE | re.DOTALL),
]

# ═══════════════════════════════════════════════════════════════
# Sarcasm/Irony Markers
# ═══════════════════════════════════════════════════════════════

SARCASM_MARKERS_CN = {
    "呵呵", "哈哈", "笑死", "绝了", "可还行", "真行", "真棒",
    "真香", "厉害了", "了不起", "佩服", "牛啊", "真好",
    "说的好像", "说得好像", "好像...似的", "真是",
}

SARCASM_MARKERS_EN = {
    "yeah_right", "sure", "whatever", "oh_great", "how_nice",
    "tell_me_about_it", "big_deal", "wow_so_impressive",
    "good_for_you", "as_if", "riiight", "lol_sure",
}


class EmotionAnalyzer:
    """
    Production-Grade Emotion Analysis Engine (v8.2).

    Analysis dimensions:
    - valence: [-1.0, 1.0] (negative → positive)
    - arousal: [0.0, 1.0] (calm → excited)
    - dominance: [0.0, 1.0] (submissive → dominant)
    - primary_emotions: Plutchik 8-vector
    - compound_emotions: detected dyads
    - significance: trivial/notable/important/breakthrough/crisis/milestone
    - confidence: [0.0, 1.0]
    - nuance: literal/implicit/contradictory/ironic/sarcastic
    - boundaries: emotional shift points within text

    Architecture:
      Layer 1: Plutchik rule engine (fast baseline)
      Layer 2: Intensity calibration (modifiers, negation)
      Layer 3: Compound emotion synthesis (dyads)
      Layer 4: LLM refinement (ambiguous/ironic content)
    """

    DEFAULT_VALENCE = 0.0
    DEFAULT_AROUSAL = 0.2
    DEFAULT_DOMINANCE = 0.5
    DEFAULT_SIGNIFICANCE = "notable"
    DEFAULT_CONFIDENCE = 0.5

    LLM_TRIGGER_CONFLICT_RATIO = 0.3
    LLM_TRIGGER_MIN_HITS = 2

    NATURE_BASELINES = {
        "breakthrough": {"valence": 0.6, "arousal": 0.7, "dominance": 0.7, "significance": "breakthrough"},
        "decision": {"valence": 0.1, "arousal": 0.3, "dominance": 0.6, "significance": "important"},
        "task": {"valence": 0.0, "arousal": 0.3, "dominance": 0.5, "significance": "notable"},
        "todo": {"valence": -0.1, "arousal": 0.2, "dominance": 0.4, "significance": "notable"},
        "output": {"valence": 0.3, "arousal": 0.3, "dominance": 0.6, "significance": "important"},
        "log": {"valence": 0.0, "arousal": 0.1, "dominance": 0.5, "significance": "trivial"},
        "chat": {"valence": 0.0, "arousal": 0.1, "dominance": 0.5, "significance": "trivial"},
        "draft": {"valence": 0.0, "arousal": 0.1, "dominance": 0.5, "significance": "trivial"},
        "note": {"valence": 0.05, "arousal": 0.15, "dominance": 0.5, "significance": "notable"},
        "retro": {"valence": 0.0, "arousal": 0.2, "dominance": 0.5, "significance": "notable"},
        "explore": {"valence": 0.1, "arousal": 0.2, "dominance": 0.5, "significance": "notable"},
        "config": {"valence": 0.0, "arousal": 0.05, "dominance": 0.5, "significance": "trivial"},
        "ask": {"valence": 0.0, "arousal": 0.15, "dominance": 0.4, "significance": "trivial"},
        "archive": {"valence": 0.0, "arousal": 0.05, "dominance": 0.5, "significance": "trivial"},
    }

    DOMINANCE_MAP = {
        "anger": 0.8, "disgust": 0.7, "joy": 0.6, "anticipation": 0.5,
        "surprise": 0.4, "trust": 0.5, "fear": 0.2, "sadness": 0.2,
    }

    def __init__(self, llm_fn: Callable = None):
        self.llm_fn = llm_fn

        self._pos_pattern_cn = self._build_weighted_pattern(POSITIVE_WORDS_CN)
        self._neg_pattern_cn = self._build_weighted_pattern(NEGATIVE_WORDS_CN)
        self._pos_pattern_en = self._build_weighted_pattern(POSITIVE_WORDS_EN)
        self._neg_pattern_en = self._build_weighted_pattern(NEGATIVE_WORDS_EN)
        self._high_arousal_pattern = self._build_pattern(HIGH_AROUSAL_WORDS)

        self._emotion_patterns_cn = {}
        self._emotion_patterns_en = {}
        for emotion in PLUTCHIK_PRIMARY:
            cn_dict = EMOTION_WORDS_CN.get(emotion, {})
            en_dict = EMOTION_WORDS_EN.get(emotion, {})
            if cn_dict:
                self._emotion_patterns_cn[emotion] = self._build_weighted_pattern(cn_dict)
            if en_dict:
                self._emotion_patterns_en[emotion] = self._build_weighted_pattern(en_dict)

        self._intensifier_pattern_cn = self._build_pattern(set(INTENSIFIERS_CN.keys()))
        self._intensifier_pattern_en = self._build_pattern(set(INTENSIFIERS_EN.keys()))
        self._diminisher_pattern_cn = self._build_pattern(set(DIMINISHERS_CN.keys()))
        self._diminisher_pattern_en = self._build_pattern(set(DIMINISHERS_EN.keys()))
        self._negation_pattern_cn = self._build_pattern(NEGATION_WORDS_CN)
        self._negation_pattern_en = self._build_pattern(NEGATION_WORDS_EN)
        self._sarcasm_pattern_cn = self._build_pattern(SARCASM_MARKERS_CN)
        self._sarcasm_pattern_en = self._build_pattern(SARCASM_MARKERS_EN)

    @staticmethod
    def _build_pattern(words: set) -> re.Pattern:
        sorted_words = sorted(words, key=len, reverse=True)
        escaped = [re.escape(w) for w in sorted_words if w]
        if not escaped:
            return re.compile(r"(?!)")
        return re.compile("|".join(escaped))

    @staticmethod
    def _build_weighted_pattern(weighted_dict: dict) -> re.Pattern:
        sorted_words = sorted(weighted_dict.keys(), key=len, reverse=True)
        escaped = [re.escape(w) for w in sorted_words if w]
        if not escaped:
            return re.compile(r"(?!)")
        return re.compile("|".join(escaped))

    def _get_weight(self, word: str, weighted_dict: dict) -> float:
        return weighted_dict.get(word, 0.5)

    def analyze(
        self,
        content: str,
        importance: str = "medium",
        nature_code: str = None,
    ) -> dict:
        t_start = time.monotonic()
        trace = {"steps": [], "rule_valence": None, "llm_valence": None, "final_source": "rules"}

        if not content or not content.strip():
            return {
                "valence": self.DEFAULT_VALENCE,
                "arousal": self.DEFAULT_AROUSAL,
                "dominance": self.DEFAULT_DOMINANCE,
                "primary_emotions": {e: 0.0 for e in PLUTCHIK_PRIMARY},
                "compound_emotions": [],
                "significance": self.DEFAULT_SIGNIFICANCE,
                "confidence": 0.1,
                "nuance": "不明",
                "boundaries": [],
                "trace": {"steps": ["empty_input"], "final_source": "default"},
            }

        content_lower = content.lower()
        baseline = self.NATURE_BASELINES.get(
            nature_code or "",
            {"valence": 0.0, "arousal": 0.15, "dominance": 0.5, "significance": "notable"},
        )

        # ── Layer 1: Plutchik 8-vector ──────────────────────
        primary_emotions = self._compute_primary_emotions(content, content_lower)
        trace["steps"].append(f"primary_emotions: {self._summarize_emotions(primary_emotions)}")

        # ── Layer 2: Valence + Intensity Calibration ────────
        pos_hits = self._pos_pattern_cn.findall(content) + self._pos_pattern_en.findall(content_lower)
        neg_hits = self._neg_pattern_cn.findall(content) + self._neg_pattern_en.findall(content_lower)

        pos_weighted = sum(self._get_weight(w, POSITIVE_WORDS_CN) for w in pos_hits if w in POSITIVE_WORDS_CN)
        pos_weighted += sum(self._get_weight(w, POSITIVE_WORDS_EN) for w in pos_hits if w in POSITIVE_WORDS_EN)
        neg_weighted = sum(self._get_weight(w, NEGATIVE_WORDS_CN) for w in neg_hits if w in NEGATIVE_WORDS_CN)
        neg_weighted += sum(self._get_weight(w, NEGATIVE_WORDS_EN) for w in neg_hits if w in NEGATIVE_WORDS_EN)

        total_weighted = pos_weighted + neg_weighted
        if total_weighted > 0:
            raw_valence = (pos_weighted - neg_weighted) / total_weighted
        else:
            raw_valence = 0.0

        # Intensity modifier detection
        intensity_mult = self._detect_intensity(content, content_lower)
        if intensity_mult != 1.0:
            raw_valence *= intensity_mult
            trace["steps"].append(f"intensity_modifier: x{intensity_mult:.2f}")

        # Negation detection
        negation_count = self._detect_negation(content, content_lower)
        if negation_count > 0:
            raw_valence *= max(0.0, 1.0 - negation_count * 0.3)
            trace["steps"].append(f"negation_detected: {negation_count}, valence dampened")

        rule_valence = self._clamp(0.6 * raw_valence + 0.4 * baseline["valence"], -1.0, 1.0)

        # ── Contrast / Sub-clause Analysis ──────────────────
        nuance = "literal"
        is_contrastive = any(p.search(content) for p in CONTRAST_PATTERNS)
        subclause_valence = None

        if is_contrastive:
            subclause_valence = self._analyze_contrast_clauses(content, content_lower)
            nuance = "contradictory"

        if subclause_valence is not None:
            rule_valence = self._clamp(0.4 * rule_valence + 0.6 * subclause_valence, -1.0, 1.0)
            trace["steps"].append(f"subclause_valence={subclause_valence:.3f}")

        # ── Sarcasm Detection ───────────────────────────────
        is_sarcastic = self._detect_sarcasm(content, content_lower, rule_valence)
        if is_sarcastic:
            nuance = "sarcastic"
            if rule_valence > 0:
                rule_valence = self._clamp(-rule_valence * 0.6, -1.0, 1.0)
            else:
                rule_valence = self._clamp(rule_valence * 1.5 - 0.2, -1.0, 1.0)
            inverted = {}
            for e in PLUTCHIK_PRIMARY:
                inverted[e] = primary_emotions.get(e, 0.0)
            joy_val = inverted.get("joy", 0.0)
            if joy_val > 0.1:
                inverted["sadness"] = inverted.get("sadness", 0.0) + joy_val * 0.5
                inverted["anger"] = inverted.get("anger", 0.0) + joy_val * 0.3
                inverted["joy"] = joy_val * 0.2
            trust_val = inverted.get("trust", 0.0)
            if trust_val > 0.1:
                inverted["disgust"] = inverted.get("disgust", 0.0) + trust_val * 0.4
                inverted["trust"] = trust_val * 0.2
            primary_emotions = inverted
            trace["steps"].append("sarcasm_detected: valence inverted, emotions flipped")

        trace["rule_valence"] = round(rule_valence, 3)

        # ── Conflict Ratio ──────────────────────────────────
        pos_count = len(pos_hits)
        neg_count = len(neg_hits)
        total_hits = pos_count + neg_count
        conflict_ratio = 0.0
        if total_hits >= self.LLM_TRIGGER_MIN_HITS:
            minority = min(pos_count, neg_count)
            conflict_ratio = minority / total_hits

        needs_llm = (
            self.llm_fn is not None
            and (is_contrastive or conflict_ratio > self.LLM_TRIGGER_CONFLICT_RATIO or is_sarcastic)
            and total_hits >= self.LLM_TRIGGER_MIN_HITS
        )

        trace["steps"].append(
            f"contrast={is_contrastive}, conflict={conflict_ratio:.2f}, "
            f"sarcastic={is_sarcastic}, needs_llm={needs_llm}"
        )

        # ── Layer 4: LLM Refinement ─────────────────────────
        valence = rule_valence
        llm_confidence = None

        if needs_llm:
            try:
                llm_result = self._analyze_with_llm(content, rule_valence)
                if llm_result:
                    llm_valence = llm_result.get("valence", rule_valence)
                    llm_confidence = llm_result.get("confidence", 0.6)
                    llm_nuance = llm_result.get("nuance", "不明")
                    llm_emotions = llm_result.get("primary_emotions", {})

                    trace["llm_valence"] = round(llm_valence, 3)

                    if abs(llm_valence - rule_valence) > 0.3:
                        valence = 0.3 * rule_valence + 0.7 * llm_valence
                        trace["final_source"] = "llm_override"
                    elif abs(llm_valence - rule_valence) > 0.1:
                        valence = 0.5 * rule_valence + 0.5 * llm_valence
                        trace["final_source"] = "llm_blend"
                    else:
                        trace["final_source"] = "rules_confirmed_by_llm"

                    nuance = llm_nuance

                    if llm_emotions:
                        for emo, score in llm_emotions.items():
                            if emo in primary_emotions:
                                primary_emotions[emo] = 0.6 * primary_emotions[emo] + 0.4 * self._clamp(float(score), 0.0, 1.0)
            except Exception as e:
                logger.debug(f"LLM emotion analysis failed: {e}")
                trace["steps"].append(f"llm_error: {e}")

        # Nuance inference without LLM
        if not needs_llm or nuance == "不明":
            if is_sarcastic:
                nuance = "sarcastic"
            elif is_contrastive and conflict_ratio > 0.2:
                nuance = "contradictory"
            elif conflict_ratio > 0.4:
                nuance = "implicit"
            else:
                nuance = "literal"

        valence = self._clamp(valence, -1.0, 1.0)

        # ── Arousal Computation ──────────────────────────────
        arousal = self._compute_arousal(content, baseline)

        # ── Dominance Computation ────────────────────────────
        dominance = self._compute_dominance(primary_emotions, baseline)

        # ── Compound Emotion Synthesis (Layer 3) ────────────
        compound_emotions = self._detect_compound_emotions(primary_emotions)

        # ── Emotional Boundary Detection ─────────────────────
        boundaries = self._detect_boundaries(content)

        # ── Significance ─────────────────────────────────────
        significance = baseline["significance"]
        if importance == "high":
            if significance in ("trivial", "notable"):
                significance = "important"
        elif importance == "low":
            if significance in ("important", "breakthrough", "crisis"):
                significance = "notable"

        for sig, keywords in SIGNIFICANCE_KEYWORDS.items():
            if any(kw in content for kw in keywords):
                significance = sig
                break

        # ── Confidence ───────────────────────────────────────
        confidence = self._compute_confidence(
            content, importance, nuance, total_hits, llm_confidence
        )

        # ── Trace ────────────────────────────────────────────
        elapsed_ms = (time.monotonic() - t_start) * 1000
        trace["elapsed_ms"] = round(elapsed_ms, 2)
        trace["valence"] = round(valence, 3)
        trace["arousal"] = round(arousal, 3)
        trace["dominance"] = round(dominance, 3)
        trace["significance"] = significance
        trace["nuance"] = nuance
        trace["confidence"] = round(confidence, 3)

        if trace["final_source"].startswith("llm"):
            logger.debug(
                f"Emotion LLM: rule={trace['rule_valence']:.2f} → "
                f"final={valence:.2f} ({trace['final_source']}), "
                f"nuance={nuance}, {elapsed_ms:.1f}ms"
            )

        return {
            "valence": round(valence, 3),
            "arousal": round(arousal, 3),
            "dominance": round(dominance, 3),
            "primary_emotions": {e: round(v, 3) for e, v in primary_emotions.items()},
            "compound_emotions": compound_emotions,
            "significance": significance,
            "confidence": round(confidence, 3),
            "nuance": nuance,
            "boundaries": boundaries,
            "trace": trace,
        }

    def _compute_primary_emotions(self, content: str, content_lower: str) -> Dict[str, float]:
        primary = {e: 0.0 for e in PLUTCHIK_PRIMARY}

        for emotion in PLUTCHIK_PRIMARY:
            cn_pattern = self._emotion_patterns_cn.get(emotion)
            en_pattern = self._emotion_patterns_en.get(emotion)
            cn_dict = EMOTION_WORDS_CN.get(emotion, {})
            en_dict = EMOTION_WORDS_EN.get(emotion, {})

            score = 0.0
            if cn_pattern:
                hits = cn_pattern.findall(content)
                for hit in hits:
                    score += cn_dict.get(hit, 0.5)
            if en_pattern:
                hits = en_pattern.findall(content_lower)
                for hit in hits:
                    score += en_dict.get(hit, 0.5)

            if score > 0:
                primary[emotion] = min(1.0, score / 3.0)

        total = sum(primary.values())
        if total > 1.0:
            for e in primary:
                primary[e] /= total

        return primary

    def _detect_intensity(self, content: str, content_lower: str) -> float:
        cn_int = self._intensifier_pattern_cn.findall(content)
        en_int = self._intensifier_pattern_en.findall(content_lower)
        cn_dim = self._diminisher_pattern_cn.findall(content)
        en_dim = self._diminisher_pattern_en.findall(content_lower)

        mult = 1.0
        for w in cn_int:
            mult *= INTENSIFIERS_CN.get(w, 1.3)
        for w in en_int:
            mult *= INTENSIFIERS_EN.get(w, 1.3)
        for w in cn_dim:
            mult *= DIMINISHERS_CN.get(w, 0.6)
        for w in en_dim:
            mult *= DIMINISHERS_EN.get(w, 0.6)

        return self._clamp(mult, 0.3, 2.0)

    def _detect_negation(self, content: str, content_lower: str) -> int:
        cn_neg = self._negation_pattern_cn.findall(content)
        en_neg = self._negation_pattern_en.findall(content_lower)
        return len(cn_neg) + len(en_neg)

    def _detect_sarcasm(self, content: str, content_lower: str, rule_valence: float) -> bool:
        cn_sarc = self._sarcasm_pattern_cn.findall(content)
        en_sarc = self._sarcasm_pattern_en.findall(content_lower)
        sarcasm_hits = len(cn_sarc) + len(en_sarc)

        if sarcasm_hits == 0:
            return False

        if rule_valence > 0.3 and sarcasm_hits > 0:
            return True

        if sarcasm_hits > 0:
            neg_hits = self._neg_pattern_cn.findall(content) + self._neg_pattern_en.findall(content_lower)
            if len(neg_hits) > 0 and rule_valence < 0.1:
                return True

        excl = content.count("!") + content.count("！")
        if sarcasm_hits > 0 and excl >= 2:
            return True

        return False

    def _compute_arousal(self, content: str, baseline: dict) -> float:
        arousal_signals = 0.0

        excl_count = content.count("!") + content.count("！")
        arousal_signals += min(excl_count * 0.1, 0.3)

        q_count = content.count("?") + content.count("？")
        arousal_signals += min(q_count * 0.05, 0.15)

        ha_count = len(self._high_arousal_pattern.findall(content))
        arousal_signals += min(ha_count * 0.15, 0.4)

        char_count = len(content)
        if char_count < 10:
            arousal_signals += 0.1
        elif char_count > 500:
            arousal_signals -= 0.05

        caps_ratio = sum(1 for c in content if c.isupper()) / max(1, len(content))
        if caps_ratio > 0.3:
            arousal_signals += 0.15

        raw_arousal = self._clamp(arousal_signals, 0.0, 0.8)
        return self._clamp(0.5 * raw_arousal + 0.5 * baseline["arousal"], 0.0, 1.0)

    def _compute_dominance(self, primary_emotions: Dict[str, float], baseline: dict) -> float:
        weighted_dominance = 0.0
        total_weight = 0.0
        for emotion, score in primary_emotions.items():
            if score > 0.05:
                d = self.DOMINANCE_MAP.get(emotion, 0.5)
                weighted_dominance += d * score
                total_weight += score

        if total_weight > 0:
            emotion_dominance = weighted_dominance / total_weight
        else:
            emotion_dominance = 0.5

        return self._clamp(0.6 * emotion_dominance + 0.4 * baseline.get("dominance", 0.5), 0.0, 1.0)

    def _detect_compound_emotions(self, primary_emotions: Dict[str, float]) -> List[dict]:
        compounds = []
        for name, (e1, e2) in PLUTCHIK_DYADS.items():
            s1 = primary_emotions.get(e1, 0.0)
            s2 = primary_emotions.get(e2, 0.0)
            combined = min(s1, s2)
            if combined >= PLUTCHIK_DYAD_THRESHOLD:
                compounds.append({
                    "name": name,
                    "components": [e1, e2],
                    "strength": round(combined, 3),
                })

        compounds.sort(key=lambda x: x["strength"], reverse=True)
        return compounds[:3]

    def _detect_boundaries(self, content: str) -> List[dict]:
        boundaries = []
        sentence_enders = re.compile(r'[。！？.!?\n]')
        sentences = [s.strip() for s in sentence_enders.split(content) if s.strip()]

        if len(sentences) < 2:
            return boundaries

        prev_emotion = None
        for i, sentence in enumerate(sentences):
            if not sentence:
                continue
            primary = self._compute_primary_emotions(sentence, sentence.lower())
            dominant = max(primary, key=primary.get)
            score = primary[dominant]

            if prev_emotion is not None and dominant != prev_emotion and score > 0.1:
                boundaries.append({
                    "position": i,
                    "from": prev_emotion,
                    "to": dominant,
                    "strength": round(score, 3),
                })

            if score > 0.1:
                prev_emotion = dominant

        return boundaries

    def _analyze_contrast_clauses(self, content: str, content_lower: str) -> Optional[float]:
        clauses = None
        for pattern in CONTRAST_PATTERNS:
            match = pattern.search(content)
            if match:
                before = match.group(1).strip()
                after = match.group(2).strip()
                if before and after:
                    clauses = (before, after)
                    break

        if not clauses:
            return None

        before, after = clauses

        def _weighted_valence(text, text_lower):
            ph = self._pos_pattern_cn.findall(text) + self._pos_pattern_en.findall(text_lower)
            nh = self._neg_pattern_cn.findall(text) + self._neg_pattern_en.findall(text_lower)
            pw = sum(self._get_weight(w, POSITIVE_WORDS_CN) for w in ph if w in POSITIVE_WORDS_CN)
            pw += sum(self._get_weight(w, POSITIVE_WORDS_EN) for w in ph if w in POSITIVE_WORDS_EN)
            nw = sum(self._get_weight(w, NEGATIVE_WORDS_CN) for w in nh if w in NEGATIVE_WORDS_CN)
            nw += sum(self._get_weight(w, NEGATIVE_WORDS_EN) for w in nh if w in NEGATIVE_WORDS_EN)
            total = pw + nw
            return (pw - nw) / total if total > 0 else 0.0

        before_valence = _weighted_valence(before, before.lower())
        after_valence = _weighted_valence(after, after.lower())

        blended = 0.3 * before_valence + 0.7 * after_valence
        return self._clamp(blended, -1.0, 1.0)

    def _compute_confidence(
        self, content: str, importance: str, nuance: str,
        total_hits: int, llm_confidence: Optional[float]
    ) -> float:
        confidence = 0.5
        char_count = len(content)

        if char_count > 50:
            confidence += 0.1
        if char_count > 200:
            confidence += 0.08
        if char_count > 500:
            confidence += 0.05

        if re.search(r"^[-*•]\s", content, re.MULTILINE):
            confidence += 0.08
        if re.search(r"^#{1,3}\s", content, re.MULTILINE):
            confidence += 0.08
        if "```" in content:
            confidence += 0.04

        if re.search(r"\d+", content):
            confidence += 0.04

        if importance == "high":
            confidence += 0.12
        elif importance == "low":
            confidence -= 0.08

        if total_hits >= 5:
            confidence += 0.08
        elif total_hits == 0:
            confidence -= 0.15

        if nuance in ("contradictory", "sarcastic"):
            confidence *= 0.75
        elif nuance == "implicit":
            confidence *= 0.85

        if llm_confidence is not None:
            confidence = 0.6 * confidence + 0.4 * llm_confidence

        return self._clamp(confidence, 0.1, 1.0)

    def _summarize_emotions(self, primary: Dict[str, float]) -> str:
        top = sorted(primary.items(), key=lambda x: x[1], reverse=True)[:3]
        return ", ".join(f"{e}={v:.2f}" for e, v in top if v > 0.05)

    @staticmethod
    def _clamp(value: float, min_val: float, max_val: float) -> float:
        return max(min_val, min(max_val, value))

    def _analyze_with_llm(self, content: str, rule_valence: float) -> Optional[dict]:
        if not self.llm_fn:
            return None

        prompt = (
            "Analyze the emotional content of this text. Return JSON only.\n\n"
            "Dimensions:\n"
            "- valence: [-1.0, 1.0] (-1=very negative, 0=neutral, 1=very positive)\n"
            "- nuance: one of: literal, implicit, contradictory, ironic, sarcastic\n"
            "- confidence: [0.0, 1.0]\n"
            "- primary_emotions: {joy, trust, fear, surprise, sadness, disgust, anger, anticipation} each [0.0, 1.0]\n"
            "- reasoning: one sentence explanation\n\n"
            f"Text: \"{content[:500]}\"\n\n"
            f"Rule-based preliminary: valence={rule_valence:.2f}\n\n"
            'JSON format: {"valence": 0.0, "nuance": "literal", "confidence": 0.8, '
            '"primary_emotions": {"joy": 0.0, "trust": 0.0, "fear": 0.0, "surprise": 0.0, '
            '"sadness": 0.0, "disgust": 0.0, "anger": 0.0, "anticipation": 0.0}, "reasoning": "..."}'
        )

        try:
            response = self.llm_fn(prompt)
            if not response:
                return None

            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                pe = {}
                for e in PLUTCHIK_PRIMARY:
                    if e in result.get("primary_emotions", {}):
                        pe[e] = self._clamp(float(result["primary_emotions"][e]), 0.0, 1.0)
                return {
                    "valence": self._clamp(float(result.get("valence", 0)), -1.0, 1.0),
                    "confidence": self._clamp(float(result.get("confidence", 0.5)), 0.0, 1.0),
                    "nuance": result.get("nuance", "不明"),
                    "primary_emotions": pe,
                }
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.debug(f"LLM emotion JSON parse failed: {e}")

        return None

    def analyze_batch(self, contents: list, importances: list = None, nature_codes: list = None) -> list:
        importances = importances or ["medium"] * len(contents)
        nature_codes = nature_codes or [None] * len(contents)
        return [
            self.analyze(c, imp, nat)
            for c, imp, nat in zip(contents, importances, nature_codes)
        ]

    @staticmethod
    def valence_label(valence: float) -> str:
        if valence >= 0.5:
            return "积极"
        elif valence >= 0.15:
            return "偏正面"
        elif valence >= -0.15:
            return "中性"
        elif valence >= -0.5:
            return "偏负面"
        else:
            return "消极"

    @staticmethod
    def arousal_label(arousal: float) -> str:
        if arousal >= 0.7:
            return "激动"
        elif arousal >= 0.4:
            return "活跃"
        elif arousal >= 0.2:
            return "平静"
        else:
            return "沉静"

    @staticmethod
    def dominance_label(dominance: float) -> str:
        if dominance >= 0.7:
            return "主导"
        elif dominance >= 0.5:
            return "平衡"
        elif dominance >= 0.3:
            return "从属"
        else:
            return "被动"

    @staticmethod
    def significance_icon(significance: str) -> str:
        return {
            "trivial": "⚪",
            "notable": "🔵",
            "important": "🟡",
            "breakthrough": "🌟",
            "crisis": "🔴",
            "milestone": "🏁",
        }.get(significance, "⚪")

    @staticmethod
    def emotion_label(primary_emotions: Dict[str, float]) -> str:
        if not primary_emotions:
            return "中性"
        top = max(primary_emotions, key=primary_emotions.get)
        score = primary_emotions[top]
        if score < 0.1:
            return "中性"
        labels = {
            "joy": "喜悦", "trust": "信任", "fear": "恐惧",
            "surprise": "惊讶", "sadness": "悲伤", "disgust": "厌恶",
            "anger": "愤怒", "anticipation": "期待",
        }
        return labels.get(top, "中性")

    @staticmethod
    def emotion_resonance_score(emotions_a: Dict[str, float], emotions_b: Dict[str, float]) -> float:
        """Compute cosine similarity between two emotion vectors."""
        keys = PLUTCHIK_PRIMARY
        a_vec = [emotions_a.get(k, 0.0) for k in keys]
        b_vec = [emotions_b.get(k, 0.0) for k in keys]

        dot = sum(x * y for x, y in zip(a_vec, b_vec))
        mag_a = math.sqrt(sum(x * x for x in a_vec))
        mag_b = math.sqrt(sum(x * x for x in b_vec))

        if mag_a == 0 or mag_b == 0:
            return 0.0

        return round(dot / (mag_a * mag_b), 3)
