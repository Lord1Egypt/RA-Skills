from __future__ import annotations

import re
import math
import json
import time
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)


def _get(obj, attr, default=None, dict_keys=None):
    if isinstance(obj, dict):
        keys = dict_keys or [attr]
        for k in keys:
            if k in obj:
                return obj[k]
        return default
    return getattr(obj, attr, default)


# ═══════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class TraitScore:
    name: str
    score: float
    confidence: float
    evidence_count: int = 0
    source_ids: List[str] = field(default_factory=list)


@dataclass
class PersonalityProfile:
    openness: TraitScore = field(default_factory=lambda: TraitScore("openness", 0.5, 0.0))
    conscientiousness: TraitScore = field(default_factory=lambda: TraitScore("conscientiousness", 0.5, 0.0))
    extraversion: TraitScore = field(default_factory=lambda: TraitScore("extraversion", 0.5, 0.0))
    agreeableness: TraitScore = field(default_factory=lambda: TraitScore("agreeableness", 0.5, 0.0))
    neuroticism: TraitScore = field(default_factory=lambda: TraitScore("neuroticism", 0.5, 0.0))

    cognitive_style: str = ""
    reasoning_style: str = ""
    attachment_style: str = ""

    social_dominance: TraitScore = field(default_factory=lambda: TraitScore("social_dominance", 0.5, 0.0))
    intimacy_capacity: TraitScore = field(default_factory=lambda: TraitScore("intimacy_capacity", 0.5, 0.0))
    social_energy_pattern: str = ""

    circadian_preference: str = ""
    decision_style: str = ""
    humor_style: str = ""

    narcissism_index: TraitScore = field(default_factory=lambda: TraitScore("narcissism", 0.3, 0.0))
    control_tendency: TraitScore = field(default_factory=lambda: TraitScore("control", 0.3, 0.0))
    anxiety_level: TraitScore = field(default_factory=lambda: TraitScore("anxiety", 0.3, 0.0))
    empathy_capacity: TraitScore = field(default_factory=lambda: TraitScore("empathy", 0.5, 0.0))

    total_messages_analyzed: int = 0
    analysis_confidence: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    version: int = 1
    created_at: int = 0
    updated_at: int = 0


# ═══════════════════════════════════════════════════════════════
# 心理语言学分析层
# ═══════════════════════════════════════════════════════════════

class PsycholinguisticAnalyzer:

    OCEAN_PATTERNS = {
        "openness": {
            "high": [r"创新|尝试|探索|新|不同|可能|想象|创意|有趣|好奇",
                     r"也许|或许|说不定|万一|理论上"],
            "low": [r"传统|规矩|一直|从来|应该|必须|按部就班|稳妥|保守"]
        },
        "conscientiousness": {
            "high": [r"计划|安排|目标|完成|准时|认真|仔细|负责|检查|确认",
                     r"deadline|截止|进度|待办|todo"],
            "low": [r"随便|都行|无所谓|再说|以后|拖延|懒|摸鱼"]
        },
        "extraversion": {
            "high": [r"哈哈|嘻嘻|太棒了|好开心|一起|聚会|热闹|分享|聊聊",
                     r"！{2,}|～|~|呀|呢|吧|嘛|哇|耶"],
            "low": [r"嗯|哦|好|行|可以|没事|算了|不想|安静|独处"]
        },
        "agreeableness": {
            "high": [r"谢谢|感谢|理解|支持|帮忙|关心|体谅|包容|合作|一起",
                     r"不好意思|抱歉|对不起|没关系"],
            "low": [r"但是|然而|不对|错了|不同意|反驳|批评|指责|抱怨"]
        },
        "neuroticism": {
            "high": [r"焦虑|担心|害怕|紧张|压力|崩溃|烦|累|难受|抑郁",
                     r"怎么办|会不会|万一|可怕|吓人"],
            "low": [r"淡定|冷静|放松|没事|无所谓|顺其自然|随缘"]
        }
    }

    POSITIVE_WORDS = [
        "开心", "喜欢", "爱", "棒", "好", "高兴", "快乐", "幸福", "满足",
        "满意", "享受", "赞", "优秀", "成功", "完美", "精彩", "厉害",
        "不错", "很好", "太好了", "期待", "希望", "感谢", "感动",
        "兴奋", "激动", "自豪", "骄傲", "欣慰", "安心", "放心",
        "温暖", "美好", "舒适", "愉快", "欢乐", "甜蜜", "治愈",
    ]

    NEGATIVE_WORDS = [
        "烦", "讨厌", "恨", "差", "累", "难过", "伤心", "失望", "沮丧",
        "愤怒", "生气", "焦虑", "担心", "害怕", "恐惧", "崩溃", "绝望",
        "无聊", "郁闷", "纠结", "痛苦", "折磨", "无奈", "委屈", "后悔",
        "尴尬", "紧张", "不安", "烦躁", "恼火", "厌恶", "恶心", "孤独",
        "寂寞", "空虚", "迷茫", "困惑", "疲惫", "无力", "挫败",
    ]

    CONCRETE_PATTERNS = [
        r"\d+[%％]", r"\d+个", r"\d+次", r"\d+天", r"\d+小时",
        r"具体|实际|数据|数字|结果|事实|证据|案例|例子|细节",
        r"第一步|第二步|首先|然后|接着|最后",
    ]

    ABSTRACT_PATTERNS = [
        r"概念|理论|可能|本质|意义|价值|哲学|思想|观点|理念",
        r"宏观|微观|系统|整体|趋势|规律|模式|框架|逻辑",
        r"也许|或许|大概|似乎|某种程度上",
    ]

    LOGICAL_PATTERNS = [
        r"因为|所以|因此|由于|导致|造成|结果|原因|逻辑|推理",
        r"如果.*那么|假设|前提|结论|证明|验证|对比|分析",
        r"首先|其次|再次|最后|一方面|另一方面|综上|总之",
    ]

    INTUITIVE_PATTERNS = [
        r"感觉|直觉|好像|似乎|大概|也许|可能|觉得|认为|以为",
        r"猜|估|应该|差不多|八九不离十|凭感觉|凭经验",
        r"本能|第六感|下意识|不自觉|自然而然",
    ]

    SECURE_PATTERNS = [r"谢谢|理解|好的|没问题|放心|相信|信任|坦诚|直接"]
    ANXIOUS_PATTERNS = [r"在吗|？{2,}|怎么不回|是不是|到底|确认下|收到了吗|对吧|是吧"]
    AVOIDANT_PATTERNS = [r"嗯|哦|好|行|算了|无所谓|随便|不想说|以后再说|别问了"]

    def analyze_big_five(self, messages: list) -> dict[str, TraitScore]:
        all_text = "\n".join(_get(m, "content", "") for m in messages if _get(m, "content", ""))
        source_ids = [_get(m, "msg_id", "", ["msg_id", "id"]) for m in messages if _get(m, "msg_id", "", ["msg_id", "id"])]

        results = {}
        for trait, patterns in self.OCEAN_PATTERNS.items():
            high_hits = PersonalityAnalyzer._count_pattern_hits(all_text, patterns["high"])
            low_hits = PersonalityAnalyzer._count_pattern_hits(all_text, patterns["low"])
            evidence_count = high_hits + low_hits
            score = high_hits / (high_hits + low_hits + 1)
            confidence = min(1.0, evidence_count / 50)

            matched_sources = []
            for msg in messages:
                text = _get(msg, "content", "")
                if not text:
                    continue
                msg_hits = PersonalityAnalyzer._count_pattern_hits(text, patterns["high"]) + \
                           PersonalityAnalyzer._count_pattern_hits(text, patterns["low"])
                msg_id = _get(msg, "msg_id", "", ["msg_id", "id"])
                if msg_hits > 0 and msg_id:
                    matched_sources.append(msg_id)

            results[trait] = TraitScore(
                name=trait,
                score=round(score, 4),
                confidence=round(confidence, 4),
                evidence_count=evidence_count,
                source_ids=matched_sources[:100],
            )

        return results

    def analyze_sentiment(self, messages: list) -> dict:
        pos_count = 0
        neg_count = 0
        sentiment_scores = []
        trigger_words = []

        for msg in messages:
            text = _get(msg, "content", "")
            if not text:
                continue

            msg_pos = sum(1 for w in self.POSITIVE_WORDS if w in text)
            msg_neg = sum(1 for w in self.NEGATIVE_WORDS if w in text)
            pos_count += msg_pos
            neg_count += msg_neg

            total = msg_pos + msg_neg
            if total > 0:
                sentiment_scores.append((msg_pos - msg_neg) / total)
            else:
                sentiment_scores.append(0.0)

            if msg_pos > 0:
                trigger_words.extend(w for w in self.POSITIVE_WORDS if w in text)
            if msg_neg > 0:
                trigger_words.extend(w for w in self.NEGATIVE_WORDS if w in text)

        ratio = pos_count / (pos_count + neg_count + 1)

        volatility = 0.0
        if len(sentiment_scores) >= 2:
            diffs = [abs(sentiment_scores[i] - sentiment_scores[i - 1])
                     for i in range(1, len(sentiment_scores))]
            volatility = sum(diffs) / len(diffs)

        trigger_counter = Counter(trigger_words).most_common(10)

        return {
            "positive_count": pos_count,
            "negative_count": neg_count,
            "positive_ratio": round(ratio, 4),
            "volatility": round(volatility, 4),
            "trigger_words": trigger_counter,
        }

    def classify_cognitive_style(self, messages: list) -> Tuple[str, str]:
        all_text = "\n".join(_get(m, "content", "") for m in messages if _get(m, "content", ""))

        concrete_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.CONCRETE_PATTERNS)
        abstract_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.ABSTRACT_PATTERNS)
        cognitive_style = "concrete" if concrete_hits >= abstract_hits else "abstract"

        logical_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.LOGICAL_PATTERNS)
        intuitive_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.INTUITIVE_PATTERNS)
        reasoning_style = "logical" if logical_hits >= intuitive_hits else "intuitive"

        return cognitive_style, reasoning_style

    def identify_attachment_style(self, messages: list) -> str:
        all_text = "\n".join(_get(m, "content", "") for m in messages if _get(m, "content", ""))

        secure_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.SECURE_PATTERNS)
        anxious_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.ANXIOUS_PATTERNS)
        avoidant_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.AVOIDANT_PATTERNS)

        scores = {"secure": secure_hits, "anxious": anxious_hits, "avoidant": avoidant_hits}
        total = sum(scores.values())
        if total == 0:
            return "secure"

        return max(scores, key=scores.get)


# ═══════════════════════════════════════════════════════════════
# 社交行为分析层
# ═══════════════════════════════════════════════════════════════

class SocialBehaviorAnalyzer:

    IMPERATIVE_PATTERNS = [
        r"必须|应该|一定|赶紧|马上|立刻|快|去|来|给我",
        r"你[要得须应]|不要|不许|不能|别",
    ]

    INTIMACY_PATTERNS = [
        r"想你了|想念|亲爱|宝贝|心|爱|抱抱|么么|晚安|早安",
        r"秘密|心里话|跟你说|只有你|信任你|依赖你",
    ]

    def analyze_social_network(self, sessions: list) -> dict:
        contact_counter = Counter()
        contact_messages = defaultdict(int)

        for session in sessions:
            contact = _get(session, "chat_name", "", ["chat_name", "contact_name", "peer_name"]) or "unknown"
            msgs = _get(session, "messages", [])
            msg_count = len(msgs)
            contact_counter[contact] += msg_count
            contact_messages[contact] += msg_count

        total_contacts = len(contact_counter)
        total_messages = sum(contact_counter.values())
        avg_depth = total_messages / total_contacts if total_contacts > 0 else 0

        core_contacts = contact_counter.most_common(5)

        return {
            "total_contacts": total_contacts,
            "social_breadth": total_contacts,
            "social_depth": round(avg_depth, 2),
            "core_contacts": core_contacts,
            "total_messages": total_messages,
        }

    def analyze_power_dynamics(self, messages: list) -> TraitScore:
        all_text = "\n".join(_get(m, "content", "") for m in messages if _get(m, "content", ""))
        source_ids = [_get(m, "msg_id", "", ["msg_id", "id"]) for m in messages if _get(m, "msg_id", "", ["msg_id", "id"])]

        imperative_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.IMPERATIVE_PATTERNS)
        total_chars = max(len(all_text), 1)

        score = min(1.0, imperative_hits / (total_chars / 100 + 1))
        evidence_count = imperative_hits
        confidence = min(1.0, evidence_count / 50)

        return TraitScore(
            name="social_dominance",
            score=round(score, 4),
            confidence=round(confidence, 4),
            evidence_count=evidence_count,
            source_ids=source_ids[:100],
        )

    def analyze_intimacy(self, messages: list) -> TraitScore:
        source_ids = []
        intimacy_hits = 0
        late_night_count = 0
        total_with_time = 0

        for msg in messages:
            text = _get(msg, "content", "")
            if not text:
                continue
            msg_id = _get(msg, "msg_id", "", ["msg_id", "id"])
            if msg_id:
                source_ids.append(msg_id)

            intimacy_hits += PersonalityAnalyzer._count_pattern_hits(text, self.INTIMACY_PATTERNS)

            ts = _get(msg, "timestamp", 0)
            if ts > 0:
                total_with_time += 1
                hour = time.localtime(ts).tm_hour
                if hour >= 22 or hour < 5:
                    late_night_count += 1

        late_ratio = late_night_count / total_with_time if total_with_time > 0 else 0.0
        intimacy_text_score = min(1.0, intimacy_hits / (len(messages) + 1))

        score = 0.6 * intimacy_text_score + 0.4 * late_ratio
        evidence_count = intimacy_hits + late_night_count
        confidence = min(1.0, evidence_count / 50)

        return TraitScore(
            name="intimacy_capacity",
            score=round(score, 4),
            confidence=round(confidence, 4),
            evidence_count=evidence_count,
            source_ids=source_ids[:100],
        )

    def analyze_social_energy(self, messages: list) -> dict:
        hourly = defaultdict(int)
        weekday = defaultdict(int)
        weekend = defaultdict(int)

        for msg in messages:
            ts = _get(msg, "timestamp", 0)
            if ts <= 0:
                continue
            t = time.localtime(ts)
            hourly[t.tm_hour] += 1
            if t.tm_wday < 5:
                weekday[t.tm_hour] += 1
            else:
                weekend[t.tm_hour] += 1

        if not hourly:
            return {"peak_hours": [], "low_hours": [], "weekday_total": 0, "weekend_total": 0}

        avg_per_hour = sum(hourly.values()) / 24
        peak_hours = sorted(hourly.keys(), key=lambda h: hourly[h], reverse=True)[:5]
        low_hours = [h for h in range(24) if hourly.get(h, 0) < avg_per_hour * 0.3]

        weekday_total = sum(weekday.values())
        weekend_total = sum(weekend.values())

        return {
            "peak_hours": peak_hours,
            "low_hours": low_hours,
            "hourly_distribution": dict(hourly),
            "weekday_total": weekday_total,
            "weekend_total": weekend_total,
        }


# ═══════════════════════════════════════════════════════════════
# 习惯生活方式分析层
# ═══════════════════════════════════════════════════════════════

class HabitLifestyleAnalyzer:

    VALUE_TOPICS = {
        "achievement": [r"成功|成就|目标|进步|突破|赢|胜利|第一|最好|优秀"],
        "relationship": [r"朋友|家人|爱情|陪伴|信任|忠诚|关心|温暖|在一起"],
        "knowledge": [r"学习|知识|读书|研究|探索|发现|理解|思考|智慧"],
        "freedom": [r"自由|独立|选择|自主|不受束缚|自己决定|随性|随缘"],
        "security": [r"稳定|安全|保障|可靠|踏实|安心|确定|保险"],
        "creativity": [r"创意|创造|设计|艺术|想象|灵感|独特|原创"],
        "pleasure": [r"享受|快乐|开心|好玩|有趣|美食|旅行|娱乐"],
    }

    ANALYTICAL_PATTERNS = [
        r"数据|统计|分析|对比|利弊|优劣|性价比|指标|量化",
        r"根据|基于|参考|调研|研究|报告|文献|证据",
        r"首先.*其次|一方面.*另一方面|优点.*缺点",
    ]

    INTUITIVE_DECISION_PATTERNS = [
        r"感觉|直觉|觉得|认为|好像|大概|差不多|凭感觉",
        r"一眼|瞬间|立刻决定|毫不犹豫|跟着心|随心",
        r"缘分|命中注定|天意|运气|命运",
    ]

    AFFILIATIVE_HUMOR = [r"哈哈|嘻嘻|好玩|有趣|逗|搞笑|段子|笑话|开心"]
    SELF_ENHANCING_HUMOR = [r"我厉害|我牛|我优秀|我最强|我第一|我太强了|我天才"]
    AGGRESSIVE_HUMOR = [r"嘲笑|讽刺|挖苦|吐槽|鄙视|嫌弃|恶心|你真|你好意思"]
    SELF_DEFEATING_HUMOR = [r"我太菜|我废物|我垃圾|我笨|我蠢|我差劲|我不行|我无能"]

    def infer_circadian_rhythm(self, messages: list) -> str:
        hourly = defaultdict(int)
        for msg in messages:
            ts = _get(msg, "timestamp", 0)
            if ts <= 0:
                continue
            hour = time.localtime(ts).tm_hour
            hourly[hour] += 1

        if not hourly:
            return "bimodal"

        morning = sum(hourly.get(h, 0) for h in range(6, 11))
        evening = sum(hourly.get(h, 0) for h in range(20, 24))
        late_night = sum(hourly.get(h, 0) for h in range(0, 5))

        total = morning + evening + late_night
        if total == 0:
            return "bimodal"

        morning_ratio = morning / total
        evening_ratio = (evening + late_night) / total

        if morning_ratio > 0.5:
            return "morning"
        elif evening_ratio > 0.5:
            return "evening"
        else:
            return "bimodal"

    def assess_value_system(self, messages: list) -> dict:
        all_text = "\n".join(_get(m, "content", "") for m in messages if _get(m, "content", ""))

        values = {}
        for domain, patterns in self.VALUE_TOPICS.items():
            hits = PersonalityAnalyzer._count_pattern_hits(all_text, patterns)
            values[domain] = round(hits / (len(all_text) / 500 + 1), 4)

        return values

    def classify_decision_style(self, messages: list) -> str:
        all_text = "\n".join(_get(m, "content", "") for m in messages if _get(m, "content", ""))

        analytical_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.ANALYTICAL_PATTERNS)
        intuitive_hits = PersonalityAnalyzer._count_pattern_hits(all_text, self.INTUITIVE_DECISION_PATTERNS)

        if analytical_hits > intuitive_hits * 1.5:
            return "analytical"
        elif intuitive_hits > analytical_hits * 1.5:
            return "intuitive"
        else:
            return "mixed"

    def categorize_humor(self, messages: list) -> str:
        all_text = "\n".join(_get(m, "content", "") for m in messages if _get(m, "content", ""))

        scores = {
            "affiliative": PersonalityAnalyzer._count_pattern_hits(all_text, self.AFFILIATIVE_HUMOR),
            "self-enhancing": PersonalityAnalyzer._count_pattern_hits(all_text, self.SELF_ENHANCING_HUMOR),
            "aggressive": PersonalityAnalyzer._count_pattern_hits(all_text, self.AGGRESSIVE_HUMOR),
            "self-defeating": PersonalityAnalyzer._count_pattern_hits(all_text, self.SELF_DEFEATING_HUMOR),
        }

        total = sum(scores.values())
        if total == 0:
            return "affiliative"

        return max(scores, key=scores.get)


# ═══════════════════════════════════════════════════════════════
# 深层特质分析层
# ═══════════════════════════════════════════════════════════════

class DeepTraitAnalyzer:

    NARCISSISM_PATTERNS = [
        r"我[是最能做得会]|我的|我觉得|我认为|我决定|我选择",
        r"别人[都不没]|他们不懂|只有我",
        r"炫耀|厉害|优秀|完美|第一|最好",
    ]

    CONTROL_PATTERNS = [
        r"必须|应该|一定|不许|不能|不要|赶紧|马上",
        r"你[要得须应]|给我|过来|听话",
    ]

    ANXIETY_PATTERNS = [
        r"怎么办|会不会|万一|好怕|紧张|焦虑|担心",
        r"撤回|编辑|修改|算了|当我没说",
        r"？？？|！！！|\?\?+",
    ]

    EMPATHY_PATTERNS = [
        r"理解|感受|心疼|难过|开心为你|替你",
        r"你还好吗|没事吧|辛苦了|加油|抱抱",
        r"如果我是你|换作我|站在你的角度",
    ]

    def calculate_narcissism(self, messages: list) -> TraitScore:
        source_ids = []
        total_hits = 0

        for msg in messages:
            text = _get(msg, "content", "")
            if not text:
                continue
            msg_id = _get(msg, "msg_id", "", ["msg_id", "id"])
            if msg_id:
                source_ids.append(msg_id)
            total_hits += PersonalityAnalyzer._count_pattern_hits(text, self.NARCISSISM_PATTERNS)

        total_chars = sum(len(_get(m, "content", "")) for m in messages)
        score = min(1.0, total_hits / (total_chars / 200 + 1))
        confidence = min(1.0, total_hits / 50)

        return TraitScore(
            name="narcissism",
            score=round(score, 4),
            confidence=round(confidence, 4),
            evidence_count=total_hits,
            source_ids=source_ids[:100],
        )

    def assess_control_tendency(self, messages: list) -> TraitScore:
        source_ids = []
        total_hits = 0

        for msg in messages:
            text = _get(msg, "content", "")
            if not text:
                continue
            msg_id = _get(msg, "msg_id", "", ["msg_id", "id"])
            if msg_id:
                source_ids.append(msg_id)
            total_hits += PersonalityAnalyzer._count_pattern_hits(text, self.CONTROL_PATTERNS)

        total_chars = sum(len(_get(m, "content", "")) for m in messages)
        score = min(1.0, total_hits / (total_chars / 200 + 1))
        confidence = min(1.0, total_hits / 50)

        return TraitScore(
            name="control",
            score=round(score, 4),
            confidence=round(confidence, 4),
            evidence_count=total_hits,
            source_ids=source_ids[:100],
        )

    def detect_anxiety_indicators(self, messages: list) -> TraitScore:
        source_ids = []
        total_hits = 0

        for msg in messages:
            text = _get(msg, "content", "")
            if not text:
                continue
            msg_id = _get(msg, "msg_id", "", ["msg_id", "id"])
            if msg_id:
                source_ids.append(msg_id)
            total_hits += PersonalityAnalyzer._count_pattern_hits(text, self.ANXIETY_PATTERNS)

        total_chars = sum(len(_get(m, "content", "")) for m in messages)
        score = min(1.0, total_hits / (total_chars / 200 + 1))
        confidence = min(1.0, total_hits / 50)

        return TraitScore(
            name="anxiety",
            score=round(score, 4),
            confidence=round(confidence, 4),
            evidence_count=total_hits,
            source_ids=source_ids[:100],
        )

    def evaluate_empathy(self, messages: list) -> TraitScore:
        source_ids = []
        total_hits = 0

        for msg in messages:
            text = _get(msg, "content", "")
            if not text:
                continue
            msg_id = _get(msg, "msg_id", "", ["msg_id", "id"])
            if msg_id:
                source_ids.append(msg_id)
            total_hits += PersonalityAnalyzer._count_pattern_hits(text, self.EMPATHY_PATTERNS)

        total_chars = sum(len(_get(m, "content", "")) for m in messages)
        score = min(1.0, total_hits / (total_chars / 200 + 1))
        confidence = min(1.0, total_hits / 50)

        return TraitScore(
            name="empathy",
            score=round(score, 4),
            confidence=round(confidence, 4),
            evidence_count=total_hits,
            source_ids=source_ids[:100],
        )


# ═══════════════════════════════════════════════════════════════
# 人格分析引擎
# ═══════════════════════════════════════════════════════════════

class PersonalityAnalyzer:

    def __init__(self):
        self.psycho = PsycholinguisticAnalyzer()
        self.social = SocialBehaviorAnalyzer()
        self.habit = HabitLifestyleAnalyzer()
        self.deep = DeepTraitAnalyzer()

    def analyze(self, sessions: list, self_name: str = "") -> PersonalityProfile:
        # Security: require explicit consent for deep psychological analysis
        import os as _os
        if _os.environ.get("AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED", "").lower() not in ("1", "true", "yes"):
            logger.warning("Personality analysis disabled. Set AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED=true to enable.")
            profile = PersonalityProfile()
            profile.created_at = int(time.time())
            profile.updated_at = int(time.time())
            return profile

        self_messages = self._collect_self_messages(sessions, self_name)

        if not self_messages:
            profile = PersonalityProfile()
            profile.created_at = int(time.time())
            profile.updated_at = int(time.time())
            return profile

        profile = PersonalityProfile()

        big_five = self.psycho.analyze_big_five(self_messages)
        profile.openness = big_five.get("openness", profile.openness)
        profile.conscientiousness = big_five.get("conscientiousness", profile.conscientiousness)
        profile.extraversion = big_five.get("extraversion", profile.extraversion)
        profile.agreeableness = big_five.get("agreeableness", profile.agreeableness)
        profile.neuroticism = big_five.get("neuroticism", profile.neuroticism)

        cognitive_style, reasoning_style = self.psycho.classify_cognitive_style(self_messages)
        profile.cognitive_style = cognitive_style
        profile.reasoning_style = reasoning_style

        profile.attachment_style = self.psycho.identify_attachment_style(self_messages)

        profile.social_dominance = self.social.analyze_power_dynamics(self_messages)
        profile.intimacy_capacity = self.social.analyze_intimacy(self_messages)

        social_energy = self.social.analyze_social_energy(self_messages)
        if social_energy.get("weekday_total", 0) > social_energy.get("weekend_total", 0) * 2:
            profile.social_energy_pattern = "morning_person"
        elif social_energy.get("weekend_total", 0) > social_energy.get("weekday_total", 0):
            profile.social_energy_pattern = "night_owl"
        else:
            profile.social_energy_pattern = "irregular"

        profile.circadian_preference = self.habit.infer_circadian_rhythm(self_messages)
        profile.decision_style = self.habit.classify_decision_style(self_messages)
        profile.humor_style = self.habit.categorize_humor(self_messages)

        profile.narcissism_index = self.deep.calculate_narcissism(self_messages)
        profile.control_tendency = self.deep.assess_control_tendency(self_messages)
        profile.anxiety_level = self.deep.detect_anxiety_indicators(self_messages)
        profile.empathy_capacity = self.deep.evaluate_empathy(self_messages)

        profile.total_messages_analyzed = len(self_messages)

        trait_confidences = [
            profile.openness.confidence,
            profile.conscientiousness.confidence,
            profile.extraversion.confidence,
            profile.agreeableness.confidence,
            profile.neuroticism.confidence,
            profile.social_dominance.confidence,
            profile.intimacy_capacity.confidence,
            profile.narcissism_index.confidence,
            profile.control_tendency.confidence,
            profile.anxiety_level.confidence,
            profile.empathy_capacity.confidence,
        ]
        profile.analysis_confidence = round(sum(trait_confidences) / len(trait_confidences), 4)

        profile.data_sources = list(set(
            _get(s, "chat_id", "", ["chat_id", "id", "session_id"])
            for s in sessions
            if _get(s, "chat_id", "", ["chat_id", "id", "session_id"])
        ))

        now = int(time.time())
        profile.created_at = now
        profile.updated_at = now
        profile.version = 1

        return profile

    def analyze_incremental(self, profile: PersonalityProfile,
                            new_sessions: list) -> PersonalityProfile:
        new_messages = self._collect_self_messages(new_sessions)

        if not new_messages:
            return profile

        new_profile = PersonalityProfile()

        big_five = self.psycho.analyze_big_five(new_messages)
        new_profile.openness = big_five.get("openness", new_profile.openness)
        new_profile.conscientiousness = big_five.get("conscientiousness", new_profile.conscientiousness)
        new_profile.extraversion = big_five.get("extraversion", new_profile.extraversion)
        new_profile.agreeableness = big_five.get("agreeableness", new_profile.agreeableness)
        new_profile.neuroticism = big_five.get("neuroticism", new_profile.neuroticism)

        cognitive_style, reasoning_style = self.psycho.classify_cognitive_style(new_messages)
        new_profile.cognitive_style = cognitive_style
        new_profile.reasoning_style = reasoning_style
        new_profile.attachment_style = self.psycho.identify_attachment_style(new_messages)

        new_profile.social_dominance = self.social.analyze_power_dynamics(new_messages)
        new_profile.intimacy_capacity = self.social.analyze_intimacy(new_messages)

        social_energy = self.social.analyze_social_energy(new_messages)
        if social_energy.get("weekday_total", 0) > social_energy.get("weekend_total", 0) * 2:
            new_profile.social_energy_pattern = "morning_person"
        elif social_energy.get("weekend_total", 0) > social_energy.get("weekday_total", 0):
            new_profile.social_energy_pattern = "night_owl"
        else:
            new_profile.social_energy_pattern = "irregular"

        new_profile.circadian_preference = self.habit.infer_circadian_rhythm(new_messages)
        new_profile.decision_style = self.habit.classify_decision_style(new_messages)
        new_profile.humor_style = self.habit.categorize_humor(new_messages)

        new_profile.narcissism_index = self.deep.calculate_narcissism(new_messages)
        new_profile.control_tendency = self.deep.assess_control_tendency(new_messages)
        new_profile.anxiety_level = self.deep.detect_anxiety_indicators(new_messages)
        new_profile.empathy_capacity = self.deep.evaluate_empathy(new_messages)

        profile.openness = self._merge_trait(profile.openness, new_profile.openness)
        profile.conscientiousness = self._merge_trait(profile.conscientiousness, new_profile.conscientiousness)
        profile.extraversion = self._merge_trait(profile.extraversion, new_profile.extraversion)
        profile.agreeableness = self._merge_trait(profile.agreeableness, new_profile.agreeableness)
        profile.neuroticism = self._merge_trait(profile.neuroticism, new_profile.neuroticism)

        if new_profile.cognitive_style:
            profile.cognitive_style = new_profile.cognitive_style
        if new_profile.reasoning_style:
            profile.reasoning_style = new_profile.reasoning_style
        if new_profile.attachment_style:
            profile.attachment_style = new_profile.attachment_style

        profile.social_dominance = self._merge_trait(profile.social_dominance, new_profile.social_dominance)
        profile.intimacy_capacity = self._merge_trait(profile.intimacy_capacity, new_profile.intimacy_capacity)

        if new_profile.social_energy_pattern:
            profile.social_energy_pattern = new_profile.social_energy_pattern

        if new_profile.circadian_preference:
            profile.circadian_preference = new_profile.circadian_preference
        if new_profile.decision_style:
            profile.decision_style = new_profile.decision_style
        if new_profile.humor_style:
            profile.humor_style = new_profile.humor_style

        profile.narcissism_index = self._merge_trait(profile.narcissism_index, new_profile.narcissism_index)
        profile.control_tendency = self._merge_trait(profile.control_tendency, new_profile.control_tendency)
        profile.anxiety_level = self._merge_trait(profile.anxiety_level, new_profile.anxiety_level)
        profile.empathy_capacity = self._merge_trait(profile.empathy_capacity, new_profile.empathy_capacity)

        profile.total_messages_analyzed += len(new_messages)

        trait_confidences = [
            profile.openness.confidence,
            profile.conscientiousness.confidence,
            profile.extraversion.confidence,
            profile.agreeableness.confidence,
            profile.neuroticism.confidence,
            profile.social_dominance.confidence,
            profile.intimacy_capacity.confidence,
            profile.narcissism_index.confidence,
            profile.control_tendency.confidence,
            profile.anxiety_level.confidence,
            profile.empathy_capacity.confidence,
        ]
        profile.analysis_confidence = round(sum(trait_confidences) / len(trait_confidences), 4)

        new_sources = list(set(
            _get(s, "chat_id", "", ["chat_id", "id", "session_id"])
            for s in new_sessions
            if _get(s, "chat_id", "", ["chat_id", "id", "session_id"])
        ))
        profile.data_sources = list(set(profile.data_sources + new_sources))

        profile.updated_at = int(time.time())
        profile.version += 1

        return profile

    @staticmethod
    def _collect_self_messages(sessions: list, self_name: str = "") -> list:
        messages = []
        for session in sessions:
            session_messages = _get(session, "messages", [])
            for msg in session_messages:
                sender = _get(msg, "sender_name", "", ["sender_name", "sender", "from", "role"])
                is_self = False
                if self_name and self_name in sender:
                    is_self = True
                elif sender in ("self", "user", "me", "我"):
                    is_self = True
                elif _get(msg, "is_self", False):
                    is_self = True

                if is_self and _get(msg, "content", ""):
                    messages.append(msg)

        if not messages and sessions:
            for session in sessions:
                session_messages = _get(session, "messages", [])
                for msg in session_messages:
                    if _get(msg, "content", ""):
                        messages.append(msg)

        return messages

    @staticmethod
    def _merge_trait(old: TraitScore, new: TraitScore, weight: float = 0.3) -> TraitScore:
        merged_score = old.score * (1 - weight) + new.score * weight
        merged_confidence = min(1.0, old.confidence + new.confidence * weight)
        merged_evidence = old.evidence_count + new.evidence_count
        merged_sources = list(set(old.source_ids + new.source_ids))
        return TraitScore(
            name=old.name,
            score=merged_score,
            confidence=merged_confidence,
            evidence_count=merged_evidence,
            source_ids=merged_sources[:100],
        )

    @staticmethod
    def _count_pattern_hits(text: str, patterns: list) -> int:
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, text))
        return count
