"""
memory_filter.py - 智能记忆过滤器
自动判断一条消息是否值得写入记忆，以及评估其重要度
"""

from __future__ import annotations

import hashlib
import re
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)


class MemoryFilter:
    """
    三层过滤：
    1. 值得记吗？（should_remember）→ 剔除寒暄/确认/重复
    2. 重要度多少？（assess_importance）→ high/medium/low
    3. 值得压缩吗？（is_compressible）→ 可压缩的低价值内容

    基于规则 + 启发式，可选接入 LLM 增强。
    """

    # ── LLM 结果缓存上限 ────────────────────────────────
    _CACHE_MAX_SIZE = 1000

    # ── 不值得记忆的模式 ────────────────────────────────

    SKIP_PATTERNS = [
        # 纯寒暄
        r"^(hi|hello|hey|哈喽|你好|嗨|嗯|哦|好的|ok|okay|谢谢|thanks|thank you|再见|bye|拜拜)[!~！。.]*$",
        # 确认语（含变体）
        r"^(收到|了解|明白|知道了|got it|sure|yep|yeah|好的好的|行|好滴|好嘞|okk|okay|行叭|好的呀|嗯嗯|哦哦|噢)[!~！。.~]*$",
        # 极短无意义
        r"^.{0,3}$",
        # 纯表情
        r"^[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\s\u2764\u2705\u274C\u2B50\u267B\uFE0F]+$",
        # 测试
        r"^(test|测试|hello world|ping|123)$",
        # 单字符重复（如 "。。。。" 或 "......"）
        r"^(.)\1{3,}$",
    ]

    # ── 高价值信号词 ────────────────────────────────────

    HIGH_SIGNAL_KEYWORDS = {
        # 决策
        "决定", "选择", "采用", "用", "选", "定下来", "确定",
        "decided", "chose", "going with", "picked",
        # 踩坑 / 教训
        "踩坑", "教训", "注意", "坑", "问题", "错误", "bug", "不行",
        "坑点", "gotcha", "issue", "problem", "fail",
        # 偏好
        "喜欢", "不喜欢", "偏好", "推荐", "最好", "prefer", "like", "dislike",
        # 结论
        "结论", "总结", "最终", "总之", "所以", "因此",
        "conclusion", "summary", "finally",
        # 事实
        "是", "等于", "意味着", "发现", "证明",
    }

    # ── 任务信号词 ──────────────────────────────────────

    TASK_KEYWORDS = [
        "计划", "打算", "准备", "明天", "下周", "接下来",
        "要", "需要", "应该", "TODO", "todo",
        "plan", "going to", "need to", "should",
    ]

    # ── 低价值信号（但仍值得记） ────────────────────────

    LOW_SIGNAL_KEYWORDS = [
        "随便看看", "了解一下", "随便", "无所谓",
        "maybe", "perhaps", "just curious",
    ]

    def __init__(self, llm_fn=None):
        """
        llm_fn: 可选的 LLM 函数，用于复杂场景判断
                签名 fn(prompt: str) -> str，返回 JSON
        """
        self.llm_fn = llm_fn
        self._filter_cache: OrderedDict = OrderedDict()  # content_hash -> should_remember result

        # 编译正则
        self._skip_res = [re.compile(p, re.IGNORECASE) for p in self.SKIP_PATTERNS]

    def should_remember(self, text: str) -> dict:
        """
        判断一条消息是否值得写入记忆（带缓存）。

        返回:
        {
            "remember": bool,          # 是否值得记
            "reason": str,             # 原因
            "confidence": float,       # 置信度 0~1
            "suggested_importance": str,  # 建议重要度
            "suggested_nature": str,   # 建议性质
        }
        """
        # 检查缓存
        content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        if content_hash in self._filter_cache:
            return self._filter_cache[content_hash]

        # 执行实际过滤
        result = self._do_filter(text)

        # 缓存结果
        self._filter_cache[content_hash] = result
        if len(self._filter_cache) > self._CACHE_MAX_SIZE:
            self._filter_cache.popitem(last=False)  # FIFO 淘汰

        return result

    def _do_filter(self, text: str) -> dict:
        """实际过滤逻辑（原 should_remember 实现）。"""
        text_stripped = text.strip()

        # 空文本
        if not text_stripped:
            return self._result(False, "空文本", 1.0, "low", "chat")

        # 模式匹配跳过
        for pat in self._skip_res:
            if pat.match(text_stripped):
                return self._result(False, f"匹配跳过模式: {pat.pattern[:30]}", 0.9, "low", "chat")

        # 模糊变体匹配（规范化后再匹配一次）
        normalized = self._normalize_variant(text_stripped)
        for pat in self._skip_res:
            if pat.match(normalized):
                return self._result(False, f"变体匹配跳过", 0.85, "low", "chat")

        # 长度过短（但不是纯寒暄）
        if len(text_stripped) < 5:
            return self._result(False, "内容过短", 0.7, "low", "chat")

        # 检测高价值信号
        high_hits = self._count_keyword_hits(text_stripped, self.HIGH_SIGNAL_KEYWORDS)
        task_hits = self._count_keyword_hits(text_stripped, self.TASK_KEYWORDS)
        low_hits = self._count_keyword_hits(text_stripped, self.LOW_SIGNAL_KEYWORDS)

        # 高价值信号
        if high_hits >= 2:
            return self._result(True, f"高价值信号 ({high_hits} hits)", 0.95, "high", self._guess_nature(text_stripped))
        if high_hits >= 1:
            return self._result(True, f"有价值内容 ({high_hits} hits)", 0.85, "medium", self._guess_nature(text_stripped))

        # 任务信号
        if task_hits >= 1:
            return self._result(True, "任务/计划内容", 0.8, "medium", "todo")

        # 低价值但仍值得记
        if low_hits >= 1:
            return self._result(True, "低价值但有信息量", 0.5, "low", "chat")

        # 长文本大概率有价值
        if len(text_stripped) > 100:
            return self._result(True, "长文本", 0.7, "medium", self._guess_nature(text_stripped))

        # 中等长度，有一定信息量
        if len(text_stripped) > 20:
            return self._result(True, "中等长度文本", 0.5, "low", "chat")

        # 默认：短文本不记
        return self._result(False, "无明显信号", 0.6, "low", "chat")

    def assess_importance(self, text: str, context: dict = None) -> str:
        """
        评估消息重要度。

        参数:
            text: 消息内容
            context: 可选上下文 {"is_continuation": bool, "topic_changed": bool, ...}

        返回: "high" / "medium" / "low"
        """
        high_hits = self._count_keyword_hits(text, self.HIGH_SIGNAL_KEYWORDS)
        task_hits = self._count_keyword_hits(text, self.TASK_KEYWORDS)

        # 明确的决策/教训/偏好 → high
        decision_words = ["决定", "选择", "采用", "踩坑", "教训", "结论", "总结", "decided", "chose"]
        if any(w in text.lower() for w in decision_words):
            return "high"

        # 多个高价值信号
        if high_hits >= 2:
            return "high"

        # 任务相关
        if task_hits >= 1:
            return "medium"

        # 有信息量
        if high_hits >= 1 or len(text) > 50:
            return "medium"

        return "low"

    def is_compressible(self, memory: dict) -> bool:
        """
        判断一条记忆是否适合压缩（丢失细节也无所谓）。
        """
        importance = memory.get("importance", "medium")
        content = memory.get("content", "")

        # 高优先不压缩
        if importance == "high":
            return False

        # 短文本容易压缩
        if len(content) < 100:
            return True

        # 没有特殊标记的普通笔记
        nature = memory.get("nature_id", "")
        if nature in ("D05", "D11", "D01"):  # note, chat, draft
            return True

        return False

    def batch_filter(self, messages: list[str]) -> list[dict]:
        """
        批量过滤消息列表。

        返回: [{"text": str, "remember": bool, ...}, ...]
        """
        results = []
        for msg in messages:
            result = self.should_remember(msg)
            result["text"] = msg
            results.append(result)
        return results

    def _count_keyword_hits(self, text: str, keywords: set | list) -> int:
        text_lower = text.lower()
        return sum(1 for kw in keywords if kw.lower() in text_lower)

    @staticmethod
    def _normalize_variant(text: str) -> str:
        """
        规范化变体，用于模糊匹配。

        "好滴～" → "好的"
        "okk" → "ok"
        "行叭！" → "行"
        "嗯嗯嗯" → "嗯"
        """
        import unicodedata
        text = unicodedata.normalize("NFKC", text).strip().lower()

        # 常见变体映射
        variants = {
            "好滴": "好的", "好嘞": "好的", "好的呀": "好的",
            "okk": "ok", "okay": "ok", "oke": "ok",
            "行叭": "行", "行吧": "行",
            "嗯嗯": "嗯", "哦哦": "哦", "噢噢": "噢",
            "哈哈哈": "哈哈", "hhhh": "haha",
        }
        for v, canonical in variants.items():
            if text.startswith(v):
                text = canonical + text[len(v):]

        # 去尾部语气词/标点
        text = re.sub(r'[~～！!。.…]+$', '', text)

        return text.strip()

    def _guess_nature(self, text: str) -> str:
        """猜测消息性质"""
        text_lower = text.lower()

        if any(w in text_lower for w in ["计划", "打算", "准备", "明天", "接下来", "plan"]):
            return "todo"
        if any(w in text_lower for w in ["总结", "回顾", "复盘", "反思"]):
            return "retro"
        if any(w in text_lower for w in ["笔记", "记录", "学到"]):
            return "note"
        if any(w in text_lower for w in ["完成了", "交付", "成果"]):
            return "output"
        if "?" in text or "？" in text or any(w in text_lower for w in ["怎么", "什么是", "为什么"]):
            return "ask"
        if any(w in text_lower for w in ["研究", "调研", "探索", "对比"]):
            return "explore"
        if any(w in text_lower for w in ["项目", "任务", "开发", "实现"]):
            return "task"

        return "chat"

    def _result(self, remember: bool, reason: str, confidence: float, importance: str, nature: str) -> dict:
        return {
            "remember": remember,
            "reason": reason,
            "confidence": confidence,
            "suggested_importance": importance,
            "suggested_nature": nature,
        }
