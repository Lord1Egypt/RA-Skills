"""
session_context.py - 跨会话上下文连续性
让 Agent 记住上一轮检索了什么，解决"那个方案"指代消解

v2: 滑动窗口摘要 — 超出 max_history 的旧轮次不再丢弃，压缩为摘要保留
v3: 精确 token 计数 + 多源上下文优先级
"""

from __future__ import annotations

import time
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TokenEstimator:
    """Token 估算器 — 支持中英文混合、多模型适配"""

    # 各模型 token 比例（字符→token）
    MODEL_RATIOS = {
        "gpt-4o": {"cn": 1.5, "en": 0.25},       # 英文约 4 char/token
        "gpt-4": {"cn": 1.5, "en": 0.25},
        "gpt-3.5": {"cn": 1.5, "en": 0.25},
        "claude": {"cn": 1.5, "en": 0.3},
        "qwen": {"cn": 1.2, "en": 0.25},          # 通义千问中文 token 更密
        "deepseek": {"cn": 1.3, "en": 0.25},
        "gemini": {"cn": 1.5, "en": 0.25},
        "llama": {"cn": 1.5, "en": 0.25},
        "default": {"cn": 1.5, "en": 0.3},
    }

    def __init__(self, model_name: str = None):
        self.ratios = self._match_ratios(model_name)

    def _match_ratios(self, model_name: str = None) -> dict:
        if not model_name:
            return self.MODEL_RATIOS["default"]
        ml = model_name.lower()
        for key, ratios in self.MODEL_RATIOS.items():
            if key in ml:
                return ratios
        return self.MODEL_RATIOS["default"]

    def estimate(self, text: str) -> int:
        """精确估算 token 数"""
        cn_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        en_chars = len(text) - cn_chars
        return int(cn_chars * self.ratios["cn"] + en_chars * self.ratios["en"])

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """按 token 预算截断文本（保留开头+省略提示）"""
        if self.estimate(text) <= max_tokens:
            return text
        # 逐步缩减
        for ratio in [0.9, 0.8, 0.7, 0.6, 0.5]:
            cut = int(len(text) * ratio)
            candidate = text[:cut] + "\n…(已截断)"
            if self.estimate(candidate) <= max_tokens:
                return candidate
        return text[:max_tokens]  # 最坏情况硬截


class SessionContext:
    """
    会话级上下文管理器。

    核心功能：
    1. 记录最近 N 轮查询 + 检索结果
    2. 当新查询含指代词（"那个"、"它"、"之前说的"）时，自动补充上文
    3. 暴露记忆引用元数据，让 Agent 能说"你 X 天前提到过..."
    4. 滑动窗口摘要 — 旧轮次压缩为摘要而非丢弃（v2）

    用法：
        ctx = SessionContext()
        ctx.push_query("RAG 怎么做", results)   # 存入
        resolved = ctx.resolve("就用那个方案")    # → "就用那个方案 [补全: RAG 检索增强生成方案]"
    """

    # 指代词模式
    PRONOUN_PATTERNS = [
        # 中文
        r"那个", r"这个", r"它", r"他", r"她",
        r"之前说的", r"刚才说的", r"上面的", r"那个方案",
        r"就用", r"还是用", r"按那个",
        # 英文
        r"that", r"it", r"the one", r"the one I mentioned",
        r"as I said", r"the above",
    ]

    # 摘要触发阈值：超过 max_history 时压缩
    COMPACTION_TRIGGER_MULTIPLIER = 1  # 严格保持 max_history 上限

    def __init__(self, max_history: int = 5, ttl_seconds: int = 3600, summarizer_fn=None, model_name: str = None):
        """
        参数:
            max_history: 活跃窗口大小（最近 N 轮保留完整记录）
            ttl_seconds: 历史记录有效期（秒）
            summarizer_fn: 摘要函数 fn(list[dict]) -> str（可选）
            model_name: 模型名称（用于精确 token 估算）
        """
        self._max_history = max_history
        self._ttl = ttl_seconds
        self._summarizer_fn = summarizer_fn
        self._token_estimator = TokenEstimator(model_name)

        # 分层存储
        self._active: list[dict] = []     # 活跃窗口（最近 N 轮，完整保留）
        self._summary: str = ""           # 压缩摘要（更早的轮次）
        self._summary_count: int = 0      # 被压缩的轮次数

        # 多源上下文（v3）
        self._external_contexts: list[dict] = []  # [{"content": str, "source": str, "priority": int, "ts": float}]

    def push_query(
        self,
        query: str,
        recall_result: dict = None,
        intent: str = "general",
    ):
        """
        存入一轮查询及其结果。

        参数:
            query: 用户查询
            recall_result: RecallEngine.recall() 的返回
            intent: 意图分类结果
        """
        # 提取 top 记忆作为引用候选
        references = []
        if recall_result and recall_result.get("primary"):
            for mem in recall_result["primary"][:3]:
                references.append({
                    "memory_id": mem.get("memory_id", ""),
                    "content_preview": mem.get("content", "")[:80],
                    "topics": [
                        t.get("code", "") if isinstance(t, dict) else t
                        for t in mem.get("topics", [])
                    ],
                    "importance": mem.get("importance", "medium"),
                    "time_ts": mem.get("time_ts", 0),
                })

        entry = {
            "query": query,
            "intent": intent,
            "timestamp": time.time(),
            "references": references,
            "result_count": recall_result.get("total", 0) if recall_result else 0,
        }

        self._active.append(entry)

        # 超出活跃窗口 → 触发压缩
        if len(self._active) >= self._max_history * self.COMPACTION_TRIGGER_MULTIPLIER:
            self._compact()

    def _compact(self):
        """将活跃窗口中较旧的轮次压缩为摘要"""
        keep_count = self._max_history
        to_compact = self._active[:-keep_count]
        self._active = self._active[-keep_count:]

        if not to_compact:
            return

        # 生成摘要
        if self._summarizer_fn:
            try:
                compact_summary = self._summarizer_fn(to_compact)
            except Exception:
                compact_summary = self._heuristic_summary(to_compact)
        else:
            compact_summary = self._heuristic_summary(to_compact)

        # 追加到已有摘要
        if self._summary:
            self._summary = f"{self._summary}\n{compact_summary}"
        else:
            self._summary = compact_summary

        self._summary_count += len(to_compact)
        logger.debug(f"Session compact: {len(to_compact)} 轮 → 摘要 (累计压缩 {self._summary_count} 轮)")

    @staticmethod
    def _heuristic_summary(entries: list[dict]) -> str:
        """启发式摘要：提取每轮的核心主题和关键引用"""
        lines = []
        topics_seen = set()

        for entry in entries:
            query = entry.get("query", "")
            intent = entry.get("intent", "")
            refs = entry.get("references", [])

            # 提取主题
            for ref in refs:
                for t in ref.get("topics", []):
                    if t:
                        topics_seen.add(t)

            # 核心内容摘要
            if refs:
                top_content = refs[0].get("content_preview", "")[:40]
                lines.append(f"- [{intent}] {query[:30]} → {top_content}")
            else:
                lines.append(f"- [{intent}] {query[:50]}")

        topic_str = ", ".join(sorted(topics_seen)[:5]) if topics_seen else "通用"
        return f"更早的对话（涉及: {topic_str}）:\n" + "\n".join(lines[:10])

    def resolve(self, query: str) -> dict:
        """
        解析含指代的查询，补全上下文。

        返回:
        {
            "original_query": str,
            "resolved_query": str,         # 补全后的查询
            "has_pronoun": bool,
            "prior_context": str | None,   # 上一轮的核心内容
            "suggested_topics": [str],     # 从历史推断的主题
            "session_summary": str | None, # 滑动窗口摘要（如有）
        }
        """
        if not query:
            return {"original_query": query, "resolved_query": query, "has_pronoun": False,
                    "prior_context": None, "suggested_topics": [], "session_summary": None}

        has_pronoun = self._contains_pronoun(query)

        if not has_pronoun:
            return {"original_query": query, "resolved_query": query, "has_pronoun": False,
                    "prior_context": None, "suggested_topics": [], "session_summary": None}

        # 清理过期历史
        self._clean_expired()

        if not self._active:
            return {"original_query": query, "resolved_query": query, "has_pronoun": True,
                    "prior_context": None, "suggested_topics": [], "session_summary": self._summary or None}

        # 取最近一轮
        last = self._active[-1]
        last_query = last["query"]
        last_refs = last.get("references", [])

        # 补全查询
        resolved = query
        prior_context = None
        suggested_topics = []

        if last_refs:
            top_ref = last_refs[0]
            prior_content = top_ref["content_preview"]
            prior_context = prior_content
            suggested_topics = top_ref.get("topics", [])

            if "那个" in query or "这个" in query or "that" in query.lower():
                resolved = f"{query} [指代: {prior_content}]"
            elif "之前说的" in query or "刚才说的" in query:
                resolved = f"{query} [上文: {last_query} → {prior_content}]"
            elif "就用" in query or "还是用" in query:
                resolved = f"{query} [方案: {prior_content}]"

        return {
            "original_query": query,
            "resolved_query": resolved,
            "has_pronoun": True,
            "prior_context": prior_context,
            "prior_query": last_query,
            "suggested_topics": suggested_topics,
            "session_summary": self._summary or None,
        }

    def get_full_context(self, max_tokens: int = 500) -> str:
        """
        获取完整的会话上下文（摘要 + 活跃窗口 + 外部源），用于拼入 Agent prompt。

        多源优先级竞争：
        1. 会话摘要（最高优先，保留对话连贯性）
        2. 最近活跃轮次（次高）
        3. 外部上下文按 priority 降序填充剩余预算

        参数:
            max_tokens: token 预算上限
        """
        parts = []
        token_count = 0

        # 1. 摘要部分（如果有）
        if self._summary:
            est = self._token_estimator.estimate(self._summary)
            if token_count + est <= max_tokens:
                parts.append(f"[更早的 {self._summary_count} 轮对话摘要]\n{self._summary}")
                token_count += est

        # 2. 活跃窗口
        if self._active:
            parts.append("[最近对话]")
            for entry in reversed(self._active[-self._max_history:]):
                query = entry.get("query", "")[:50]
                intent = entry.get("intent", "")
                line = f"- [{intent}] {query}"
                est = self._token_estimator.estimate(line)
                if token_count + est > max_tokens:
                    break
                parts.append(line)
                token_count += est

        # 3. 外部上下文（按 priority 降序填充剩余预算）
        remaining = max_tokens - token_count
        if remaining > 50 and self._external_contexts:
            sorted_ext = sorted(self._external_contexts, key=lambda x: -x.get("priority", 0))
            ext_parts = []
            ext_tokens = 0
            for ctx in sorted_ext:
                source = ctx.get("source", "外部")
                content = ctx.get("content", "")
                line = f"[{source}] {content}"
                est = self._token_estimator.estimate(line)
                if ext_tokens + est > remaining:
                    break
                ext_parts.append(line)
                ext_tokens += est
            if ext_parts:
                parts.append("[外部上下文]")
                parts.extend(ext_parts)

        return "\n".join(parts)

    def push_external_context(self, content: str, source: str = "知识库", priority: int = 0):
        """
        注入外部上下文（知识库、工具返回、文件内容等）。

        参数:
            content: 上下文内容
            source: 来源标识（如"知识库"、"文件"、"API返回"）
            priority: 优先级（数字越大越优先保留）
        """
        self._external_contexts.append({
            "content": content,
            "source": source,
            "priority": priority,
            "ts": time.time(),
        })
        # 只保留最近 10 条外部上下文
        if len(self._external_contexts) > 10:
            self._external_contexts = self._external_contexts[-10:]

    def clear_external_contexts(self):
        """清空外部上下文"""
        self._external_contexts.clear()

    def get_references_for_agent(self, max_age_hours: float = 24) -> list[dict]:
        """
        获取最近的记忆引用，供 Agent 主动追问。
        """
        cutoff = time.time() - max_age_hours * 3600
        references = []

        for entry in self._active:
            if entry["timestamp"] < cutoff:
                continue
            for ref in entry.get("references", []):
                age_hours = (time.time() - ref.get("time_ts", entry["timestamp"])) / 3600
                if age_hours < 1:
                    age_str = "刚才"
                elif age_hours < 24:
                    age_str = f"{int(age_hours)}小时前"
                else:
                    age_str = f"{int(age_hours/24)}天前"

                references.append({
                    "memory_id": ref["memory_id"],
                    "content": ref["content_preview"],
                    "age": age_str,
                    "query_context": entry["query"],
                    "topics": ref.get("topics", []),
                })

        return references

    def _contains_pronoun(self, query: str) -> bool:
        """检查查询是否含指代词"""
        q = query.lower()
        for pattern in self.PRONOUN_PATTERNS:
            if re.search(pattern, q):
                return True
        return False

    def _clean_expired(self):
        """清理过期历史"""
        cutoff = time.time() - self._ttl
        self._active = [h for h in self._active if h["timestamp"] >= cutoff]

    def clear(self):
        """清空会话历史"""
        self._active.clear()
        self._summary = ""
        self._summary_count = 0
        self._external_contexts.clear()

    def get_stats(self) -> dict:
        return {
            "active_count": len(self._active),
            "summary_count": self._summary_count,
            "summary_length": len(self._summary),
            "max_history": self._max_history,
            "ttl_seconds": self._ttl,
            "external_contexts": len(self._external_contexts),
            "token_estimator": type(self._token_estimator.ratios).__name__ if hasattr(self, '_token_estimator') else "legacy",
        }
