"""
隐性对话语义评分引擎 — Implicit Conversation Feedback
=====================================================
不依赖用户主动打分，而是通过分析用户与大模型对话中的自然语言，
自动推断用户对每个 Skill 调用结果的满意度。

评分维度：
  1. 任务完成信号 — Skill 是否执行成功 + 用户是否继续追问同一任务
  2. 情感极性     — NLP 分析用户回复中的情感倾向
  3. 行为信号     — 重试次数、是否放弃、是否采纳结果
  4. 满意度关键词 — "不错"/"有问题"/"再试"等关键短语
  5. 会话延续性   — 调用后用户是否基于结果继续后续工作

最终输出 implicit_rating (1.0 - 5.0) 供评估引擎使用。
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from skills_monitor.data.store import DataStore


# ──────── 语义信号词典 ────────

# 正面意图信号（用户满意/采纳结果）
POSITIVE_SIGNALS = {
    # 中文
    "不错", "很好", "准确", "正是我要的", "有用", "很有帮助",
    "可以", "好的", "谢谢", "感谢", "太好了", "完美", "棒",
    "确实", "没问题", "很棒", "满意", "给力", "厉害",
    "继续", "接着", "然后", "下一步", "基于这个",
    "就用这个", "保存", "记录一下", "挺好", "nice",
    # 英文
    "good", "great", "nice", "perfect", "thanks", "helpful",
    "exactly", "correct", "works", "awesome", "excellent",
}

# 负面意图信号（用户不满/质疑结果）
NEGATIVE_SIGNALS = {
    # 中文
    "不对", "不准", "错了", "有问题", "不行", "不是我要的",
    "换个方式", "重新", "再试", "有误", "不对劲", "搞错了",
    "差", "垃圾", "没用", "不好用", "太慢", "超时",
    "失败", "崩溃", "出错", "报错", "异常", "bug",
    "算了", "不要了", "放弃", "跳过", "不用了",
    # 英文
    "wrong", "incorrect", "error", "bad", "useless", "broken",
    "retry", "again", "fail", "crash", "slow", "timeout",
    "skip", "forget it", "never mind", "cancel",
}

# 重试/不满信号（用户要求重做同一件事）
RETRY_SIGNALS = {
    "再试一次", "重新跑", "换个", "再查", "再分析",
    "重新来", "重跑", "再运行", "另一种方式", "换一个",
    "retry", "again", "redo", "try another",
}

# 放弃信号
ABANDON_SIGNALS = {
    "算了", "不用了", "不要了", "放弃", "跳过", "不需要了",
    "forget it", "never mind", "skip", "cancel", "don't need",
}

# 采纳/继续信号（基于结果做后续工作）
ADOPT_SIGNALS = {
    "基于这个", "根据这个结果", "那么接下来", "在此基础上",
    "用这个数据", "就按这个", "保存一下", "记录下来",
    "帮我生成报告", "总结一下", "下一步",
    "based on this", "use this", "next step", "save this",
}


# ──────── 信号提取 & 评分推断 ────────

class ConversationSignal:
    """一次 Skill 调用的对话上下文信号"""

    def __init__(
        self,
        skill_id: str,
        run_id: str,
        run_status: str,            # "success" / "error"
        run_duration_ms: float,
        user_messages: List[str],   # 调用后用户的回复消息列表
        retry_count: int = 0,       # 同一 skill 被连续调用的次数
        session_continued: bool = True,  # 用户是否在此之后继续了会话
    ):
        self.skill_id = skill_id
        self.run_id = run_id
        self.run_status = run_status
        self.run_duration_ms = run_duration_ms
        self.user_messages = user_messages
        self.retry_count = retry_count
        self.session_continued = session_continued


class ImplicitFeedbackEngine:
    """
    隐性反馈引擎：从对话信号中推断用户满意度

    不诱导用户打分，不提示评价，完全被动地从自然交互中提取信号。
    """

    def __init__(self, store: DataStore, agent_id: str):
        self.store = store
        self.agent_id = agent_id

    def analyze_signal(self, signal: ConversationSignal) -> Dict[str, Any]:
        """
        分析一次 Skill 调用的对话信号，返回多维度评分

        Returns:
            {
                "implicit_rating": float,       # 1.0 - 5.0
                "confidence": float,            # 0.0 - 1.0 置信度
                "dimensions": {
                    "task_completion": float,    # 任务完成度 0-1
                    "sentiment": float,          # 情感极性 0-1
                    "behavior": float,           # 行为信号 0-1
                    "adoption": float,           # 采纳度 0-1
                    "continuity": float,         # 会话延续性 0-1
                },
                "sentiment_label": str,         # positive/negative/neutral
                "evidence": list,               # 支撑证据
            }
        """
        dimensions = {}
        evidence = []
        confidence_factors = []

        # ── 1. 任务完成度 (权重 0.30) ──
        if signal.run_status == "success":
            dimensions["task_completion"] = 0.8
            evidence.append("skill 执行成功")
            # 如果耗时合理，额外加分
            if signal.run_duration_ms and signal.run_duration_ms < 5000:
                dimensions["task_completion"] = 0.9
                evidence.append(f"响应时间 {signal.run_duration_ms:.0f}ms 良好")
        else:
            dimensions["task_completion"] = 0.2
            evidence.append("skill 执行失败")

        confidence_factors.append(0.9)  # 执行状态是硬信号，置信度高

        # ── 2. 情感极性 (权重 0.25) ──
        sentiment_score, sentiment_label, sent_evidence = self._analyze_sentiment(
            signal.user_messages
        )
        dimensions["sentiment"] = sentiment_score
        evidence.extend(sent_evidence)

        # 有用户消息时置信度高，没有时低
        if signal.user_messages:
            confidence_factors.append(min(0.5 + len(signal.user_messages) * 0.15, 0.95))
        else:
            confidence_factors.append(0.3)

        # ── 3. 行为信号 (权重 0.20) ──
        behavior_score, beh_evidence = self._analyze_behavior(signal)
        dimensions["behavior"] = behavior_score
        evidence.extend(beh_evidence)
        confidence_factors.append(0.7)

        # ── 4. 采纳度 (权重 0.15) ──
        adoption_score, adopt_evidence = self._analyze_adoption(signal.user_messages)
        dimensions["adoption"] = adoption_score
        evidence.extend(adopt_evidence)
        confidence_factors.append(0.6 if signal.user_messages else 0.2)

        # ── 5. 会话延续性 (权重 0.10) ──
        if signal.session_continued:
            dimensions["continuity"] = 0.7
        else:
            # 用户走了，可能满意也可能不满意，给中间分
            dimensions["continuity"] = 0.5
        confidence_factors.append(0.4)

        # ── 加权合成 ──
        weights = {
            "task_completion": 0.30,
            "sentiment": 0.25,
            "behavior": 0.20,
            "adoption": 0.15,
            "continuity": 0.10,
        }

        weighted_sum = sum(
            dimensions[k] * weights[k] for k in weights
        )

        # 映射到 1-5 分制
        implicit_rating = round(1.0 + weighted_sum * 4.0, 2)
        implicit_rating = max(1.0, min(5.0, implicit_rating))

        # 综合置信度
        confidence = round(sum(confidence_factors) / len(confidence_factors), 3)

        return {
            "implicit_rating": implicit_rating,
            "confidence": confidence,
            "dimensions": {k: round(v, 3) for k, v in dimensions.items()},
            "sentiment_label": sentiment_label,
            "evidence": evidence,
        }

    def _analyze_sentiment(
        self, messages: List[str]
    ) -> Tuple[float, str, List[str]]:
        """
        分析用户消息的情感极性
        返回: (score 0-1, label, evidence_list)
        """
        if not messages:
            return 0.5, "neutral", ["无用户回复，情感中性"]

        combined = " ".join(messages).lower()
        evidence = []

        # 统计匹配
        pos_hits = []
        neg_hits = []

        for kw in POSITIVE_SIGNALS:
            if kw.lower() in combined:
                pos_hits.append(kw)
        for kw in NEGATIVE_SIGNALS:
            if kw.lower() in combined:
                neg_hits.append(kw)

        # 否定句翻转检测
        # "不错" 是正面，但 "不太好" 是负面
        negation_patterns = [
            r"不太[好准行]", r"不够[好准稳]", r"不怎么",
            r"不是很[好准]", r"not\s+(?:good|great|helpful)",
        ]
        negation_hits = 0
        for pat in negation_patterns:
            if re.search(pat, combined):
                negation_hits += 1

        pos_count = len(pos_hits)
        neg_count = len(neg_hits) + negation_hits

        if pos_hits:
            evidence.append(f"正面信号: {', '.join(pos_hits[:3])}")
        if neg_hits:
            evidence.append(f"负面信号: {', '.join(neg_hits[:3])}")
        if negation_hits > 0:
            evidence.append(f"检测到否定句式 x{negation_hits}")

        # 评分计算
        if pos_count > 0 and neg_count == 0:
            score = min(0.7 + pos_count * 0.06, 0.95)
            label = "positive"
        elif neg_count > 0 and pos_count == 0:
            score = max(0.3 - neg_count * 0.06, 0.05)
            label = "negative"
        elif pos_count > neg_count:
            score = 0.5 + (pos_count - neg_count) * 0.08
            label = "positive"
        elif neg_count > pos_count:
            score = 0.5 - (neg_count - pos_count) * 0.08
            label = "negative"
        else:
            score = 0.5
            label = "neutral"
            if not evidence:
                evidence.append("情感中性")

        return max(0.0, min(1.0, score)), label, evidence

    def _analyze_behavior(
        self, signal: ConversationSignal
    ) -> Tuple[float, List[str]]:
        """
        分析行为信号：重试次数、放弃、会话模式
        返回: (score 0-1, evidence_list)
        """
        evidence = []
        score = 0.7  # 基准分

        # 重试次数
        if signal.retry_count == 0:
            score += 0.1
            evidence.append("无重试")
        elif signal.retry_count == 1:
            score -= 0.1
            evidence.append("重试 1 次")
        elif signal.retry_count >= 2:
            score -= 0.25
            evidence.append(f"重试 {signal.retry_count} 次")

        # 检测用户消息中的重试/放弃信号
        combined = " ".join(signal.user_messages).lower() if signal.user_messages else ""

        retry_detected = any(kw.lower() in combined for kw in RETRY_SIGNALS)
        abandon_detected = any(kw.lower() in combined for kw in ABANDON_SIGNALS)

        if retry_detected:
            score -= 0.15
            evidence.append("检测到重试意图")
        if abandon_detected:
            score -= 0.3
            evidence.append("检测到放弃意图")

        if not retry_detected and not abandon_detected and signal.retry_count == 0:
            if not evidence:
                evidence.append("行为正常")

        return max(0.0, min(1.0, score)), evidence

    def _analyze_adoption(
        self, messages: List[str]
    ) -> Tuple[float, List[str]]:
        """
        分析用户是否采纳了 Skill 的输出结果
        返回: (score 0-1, evidence_list)
        """
        if not messages:
            return 0.5, ["无用户回复，采纳度未知"]

        combined = " ".join(messages).lower()
        evidence = []

        adopt_hits = [kw for kw in ADOPT_SIGNALS if kw.lower() in combined]

        if adopt_hits:
            score = min(0.7 + len(adopt_hits) * 0.1, 0.95)
            evidence.append(f"采纳信号: {', '.join(adopt_hits[:3])}")
        else:
            score = 0.5  # 没有明确信号，给中间分
            evidence.append("无明确采纳信号")

        return score, evidence

    # ──────── 存储接口 ────────

    def record_implicit_feedback(
        self,
        signal: ConversationSignal,
        analysis: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        记录一条隐性反馈到数据库

        如果未提供 analysis，则自动分析。
        """
        if analysis is None:
            analysis = self.analyze_signal(signal)

        feedback_record = {
            "agent_id": self.agent_id,
            "skill_id": signal.skill_id,
            "run_id": signal.run_id,
            "implicit_rating": analysis["implicit_rating"],
            "confidence": analysis["confidence"],
            "sentiment_label": analysis["sentiment_label"],
            "dimensions": analysis["dimensions"],
            "evidence": analysis["evidence"],
            "source": "conversation",
            "user_messages_count": len(signal.user_messages),
            "run_status": signal.run_status,
            "retry_count": signal.retry_count,
        }

        self.store.insert_implicit_feedback(feedback_record)

        return feedback_record

    def record_from_run_context(
        self,
        skill_id: str,
        run_id: str,
        run_status: str,
        run_duration_ms: float,
        user_messages: Optional[List[str]] = None,
        retry_count: int = 0,
        session_continued: bool = True,
    ) -> Dict[str, Any]:
        """
        便捷方法：从运行上下文直接记录隐性反馈
        用于拦截器在 Skill 运行结束后自动调用
        """
        signal = ConversationSignal(
            skill_id=skill_id,
            run_id=run_id,
            run_status=run_status,
            run_duration_ms=run_duration_ms,
            user_messages=user_messages or [],
            retry_count=retry_count,
            session_continued=session_continued,
        )
        return self.record_implicit_feedback(signal)

    def get_skill_implicit_rating(self, skill_id: str) -> Optional[float]:
        """
        获取某个 Skill 的综合隐性评分

        使用置信度加权平均：高置信度的反馈权重更大
        """
        feedbacks = self.store.get_implicit_feedback(skill_id=skill_id, limit=100)
        if not feedbacks:
            return None

        weighted_sum = 0.0
        weight_total = 0.0

        for fb in feedbacks:
            conf = fb.get("confidence", 0.5)
            rating = fb.get("implicit_rating", 3.0)
            weighted_sum += rating * conf
            weight_total += conf

        if weight_total == 0:
            return None

        return round(weighted_sum / weight_total, 2)

    def get_skill_sentiment_summary(self, skill_id: str) -> Dict[str, Any]:
        """
        获取某 Skill 的情感分布摘要
        """
        feedbacks = self.store.get_implicit_feedback(skill_id=skill_id, limit=200)
        if not feedbacks:
            return {
                "total": 0,
                "positive": 0,
                "negative": 0,
                "neutral": 0,
                "avg_rating": None,
                "avg_confidence": None,
            }

        total = len(feedbacks)
        pos = sum(1 for f in feedbacks if f.get("sentiment_label") == "positive")
        neg = sum(1 for f in feedbacks if f.get("sentiment_label") == "negative")
        neu = total - pos - neg

        ratings = [f["implicit_rating"] for f in feedbacks if f.get("implicit_rating")]
        confs = [f["confidence"] for f in feedbacks if f.get("confidence")]

        return {
            "total": total,
            "positive": pos,
            "negative": neg,
            "neutral": neu,
            "positive_ratio": round(pos / total * 100, 1) if total > 0 else 0,
            "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else None,
            "avg_confidence": round(sum(confs) / len(confs), 3) if confs else None,
        }
