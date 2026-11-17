"""
输入适配层 — 用户输入归一化与意图路由
──────────────────────────────────────
所有用户输入在此层完成：
1. 语言检测
2. 意图分类
3. 参数归一化
4. 合法性校验（通过 ACL）

下游模块只接收标准化请求对象，严禁二次解析用户输入。
"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class QueryIntent(str, Enum):
    QUICK = "quick"          # 快速简报
    DEEP = "deep"            # 深度分析
    COMPARE = "compare"      # 对比分析
    VERIFY = "verify"        # 可信度验证
    MONITOR = "monitor"      # 持续监控
    TREND = "trend"          # 趋势检测


class QueryLanguage(str, Enum):
    ZH = "zh"
    EN = "en"
    OTHER = "other"


@dataclass(frozen=True)
class NormalizedRequest:
    """
    标准化请求对象 — 输入适配层的唯一输出

    这是不可变值对象，确保下游模块不会意外修改输入参数。
    """
    query: str
    intent: QueryIntent
    language: QueryLanguage
    max_results: int = 100
    engine_group: str = "all"   # "cn" | "global" | "all"
    timeout: int = 600
    session_id: Optional[str] = None

    def __post_init__(self):
        """不可变对象创建后校验"""
        if not self.query or len(self.query.strip()) < 2:
            raise ValueError(f"Query too short: '{self.query}'")
        if self.max_results < 10 or self.max_results > 500:
            raise ValueError(f"max_results out of range: {self.max_results}")
        if self.timeout < 30 or self.timeout > 3600:
            raise ValueError(f"timeout out of range: {self.timeout}")


class InputAdapter:
    """
    输入适配器

    用法:
        adapter = InputAdapter()
        request = adapter.adapt(user_input={"query": "帮我查一下AI趋势"})
        # → NormalizedRequest(query="AI趋势", intent=DEEP, language=ZH, ...)
    """

    # 意图匹配规则 (关键词, 意图)
    _INTENT_PATTERNS: list[tuple[re.Pattern, QueryIntent]] = [
        (re.compile(r"快速|简要|简报|速览|quick|brief"), QueryIntent.QUICK),
        (re.compile(r"深入|详细|分析|深度|deep|analyze|分析报告"), QueryIntent.DEEP),
        (re.compile(r"对比|比较|区别|vs|compare|diff"), QueryIntent.COMPARE),
        (re.compile(r"可信|真伪|验证|fact.?check|verify|求证"), QueryIntent.VERIFY),
        (re.compile(r"监控|追踪|watch|track|monitor|持续"), QueryIntent.MONITOR),
        (re.compile(r"趋势|最新|进展|trend|latest|recent"), QueryIntent.TREND),
    ]

    # 中文特征检测
    _ZH_PATTERN = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')

    def adapt(self, user_input: dict | str) -> NormalizedRequest:
        """
        将原始用户输入转换为标准化请求

        Args:
            user_input: 用户输入，可以是 dict 或字符串

        Returns:
            NormalizedRequest: 标准化请求对象

        Raises:
            ValueError: 输入不合法
        """
        from middlewares.anti_corruption import InputSanitizer

        # 统一转换为 dict
        if isinstance(user_input, str):
            user_input = {"query": user_input}

        # 输入净化
        sanitizer = InputSanitizer()
        clean_input = sanitizer.clean(**user_input)

        query = clean_input.get("query", "")
        if not query or len(query.strip()) < 2:
            raise ValueError("查询内容过短，至少需要2个字符")

        # 语言检测
        language = self._detect_language(query)

        # 意图分类
        intent = self._classify_intent(query)

        # 构建标准化请求
        request = NormalizedRequest(
            query=query.strip(),
            intent=intent,
            language=language,
            max_results=clean_input.get("max_results", 100),
            engine_group=clean_input.get("engine_group", "all"),
            timeout=clean_input.get("timeout", 600),
            session_id=clean_input.get("session_id"),
        )

        logger.info(
            f"[InputAdapter] intent={intent.value} lang={language.value} "
            f"query=\"{query[:50]}...\""
        )
        return request

    def _detect_language(self, query: str) -> QueryLanguage:
        """检测查询语言"""
        zh_chars = len(self._ZH_PATTERN.findall(query))
        total_chars = len(query.replace(" ", ""))
        if total_chars > 0 and zh_chars / total_chars > 0.3:
            return QueryLanguage.ZH
        # 简单判断：如果主要是 ASCII 字符，视为英文
        ascii_chars = sum(1 for c in query if ord(c) < 128)
        if ascii_chars / max(len(query), 1) > 0.7:
            return QueryLanguage.EN
        return QueryLanguage.OTHER

    def _classify_intent(self, query: str) -> QueryIntent:
        """根据查询内容分类意图"""
        for pattern, intent in self._INTENT_PATTERNS:
            if pattern.search(query):
                return intent
        # 默认深度分析
        return QueryIntent.DEEP

    def get_engine_list(self, language: QueryLanguage, engine_group: str = "all") -> list[str]:
        """
        根据语言和引擎组返回引擎列表

        中文查询 → 国内引擎 + 国际引擎混合
        英文查询 → 国际引擎
        """
        cn_engines = ["baidu", "bing_cn", "bing_int", "360", "sogou", "wechat", "shenma"]
        global_engines = [
            "google", "google_hk", "duckduckgo", "yahoo",
            "startpage", "brave", "ecosia", "qwant", "wolframalpha",
        ]

        if engine_group == "cn":
            return cn_engines
        elif engine_group == "global":
            return global_engines
        else:
            if language == QueryLanguage.ZH:
                # 中文：国内为主 + 国际为辅
                return cn_engines + global_engines[:4]
            else:
                return global_engines
