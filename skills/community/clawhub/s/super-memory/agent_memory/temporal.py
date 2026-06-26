"""
temporal.py - 双时间线事实管理 (Phase 2.1)

参考 Zep 的双时间线 (t_event + t_valid) 和 Hindsight 的双时间戳 (occurrence + mention)，
为记忆系统增加时间维度的推理能力。

核心概念：
- valid_from / valid_until: 事实的有效期（类似 Zep 的 t_valid）
- occurrence_time: 事件实际发生的时间（类似 Hindsight 的 occurrence）
- mention_time: 用户首次提及此事实的时间（类似 Hindsight 的 mention）
- time_ts: 记忆写入系统的时间（系统时间戳，原有字段）

TemporalReasoner 负责：
1. 从内容中提取时间信号
2. 判断事实是否仍然有效
3. 检测修正信号并标记旧事实失效
"""

from __future__ import annotations

import contextlib
import json
import logging
import re
import time
from datetime import datetime, timedelta
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class TemporalReasoner:
    """双时间线推理器"""

    def __init__(self, llm_fn: Optional[Callable[[str], str]] = None):
        """
        初始化双时间线推理器。

        参数:
            llm_fn: 可选的 LLM 调用函数，签名 fn(prompt: str) -> str。
                    提供时将启用 LLM 驱动的事实失效检测。
        """
        self._llm_fn = llm_fn

    # ── 修正信号词 ──────────────────────────────────
    # 检测新内容是否使旧事实失效
    INVALIDATION_SIGNALS = [
        r"不再",
        r"已经不用",
        r"已经不?没有",
        r"改成了?",
        r"其实是",
        r"更正",
        r"纠正",
        r"修正",
        r"不对[，,]",
        r"不是.*而是",
        r"已经换了",
        r"已经换了",
        r"换成了?",
        r"现在用的是",
        r"现在改用",
        r"之前.*现在",
        r"以前.*现在",
        r"以前.*后来",
        r"过期了",
        r"已经取消了",
        r"取消了",
        r"作废了",
        r"失效了",
        r"不再使用",
        r"不再需要",
        r"已经不用了",
    ]

    # ── 相对时间表达 ────────────────────────────────
    # 匹配中文相对时间表达，提取 occurrence_time
    _RELATIVE_TIME_PATTERNS = [
        # "X天前", "X个星期前", "X周前", "X个月前", "X年前"
        (r"(\d+)\s*天前", "days"),
        (r"(\d+)\s*个?星期前", "weeks"),
        (r"(\d+)\s*周前", "weeks"),
        (r"(\d+)\s*个?月前", "months"),
        (r"(\d+)\s*年前", "years"),
        # "昨天", "前天", "大前天"
        (r"大前天", "days_3"),
        (r"前天", "days_2"),
        (r"昨天", "days_1"),
        # "上周", "上个月", "去年"
        (r"上周", "last_week"),
        (r"上个?月", "last_month"),
        (r"去年", "last_year"),
        # "刚刚", "刚才"
        (r"刚刚|刚才", "just_now"),
    ]

    # ── 有效期起始表达 ──────────────────────────────
    # 匹配"从X开始"类表达，提取 valid_from
    _VALID_FROM_PATTERNS = [
        (r"从(\d{4})年(\d{1,2})月(\d{1,2})日?开始", "absolute_date"),
        (r"从(\d{4})年(\d{1,2})月开始", "absolute_month"),
        (r"从(\d{4})年开始", "absolute_year"),
        (r"从去年开始", "from_last_year"),
        (r"从上个月开始", "from_last_month"),
    ]

    # ── 有效期结束表达 ──────────────────────────────
    # 匹配"到X为止"、"X之后不用了"类表达，提取 valid_until
    _VALID_UNTIL_PATTERNS = [
        (r"到(\d{4})年(\d{1,2})月(\d{1,2})日?为止", "absolute_date"),
        (r"到(\d{4})年(\d{1,2})月为止", "absolute_month"),
        (r"到(\d{4})年为止", "absolute_year"),
    ]

    # ── 已编译正则缓存 ──────────────────────────────
    _compiled_invalidation: list[re.Pattern] | None = None

    @classmethod
    def _get_invalidation_patterns(cls) -> list[re.Pattern]:
        if cls._compiled_invalidation is None:
            cls._compiled_invalidation = [
                re.compile(p) for p in cls.INVALIDATION_SIGNALS
            ]
        return cls._compiled_invalidation

    def extract_temporal_signals(self, content: str) -> dict:
        """
        从内容中提取时间信号。

        返回:
            {
                "occurrence_time": float | None,  # 事件实际发生的时间
                "valid_from": float | None,       # 事实开始有效的时间
                "valid_until": float | None,      # 事实失效的时间
                "is_correction": bool,            # 是否为修正信号
            }
        """
        result = {
            "occurrence_time": None,
            "valid_from": None,
            "valid_until": None,
            "is_correction": False,
        }

        if not content:
            return result

        # 1. 检测修正信号
        result["is_correction"] = self.detect_invalidation(content)

        # 2. 提取 occurrence_time（事件实际发生的时间）
        result["occurrence_time"] = self._extract_occurrence_time(content)

        # 3. 提取 valid_from（事实开始有效的时间）
        result["valid_from"] = self._extract_valid_from(content)

        # 4. 提取 valid_until（事实失效的时间）
        result["valid_until"] = self._extract_valid_until(content)

        return result

    def is_fact_valid(self, memory: dict) -> bool:
        """
        判断事实是否仍然有效。

        规则：
        - valid_until 不为 None 且已过期 → False
        - 否则 → True
        """
        valid_until = memory.get("valid_until")
        return not (valid_until is not None and valid_until < time.time())

    def detect_invalidation(self, new_content: str, existing: dict = None) -> bool:
        """
        检测新内容是否包含修正信号。

        如果提供了 existing，则额外检查语义层面的修正关系。
        如果只提供 new_content，则仅检测修正信号词。

        返回: True 表示检测到修正信号
        """
        if not new_content:
            return False

        return any(pattern.search(new_content) for pattern in self._get_invalidation_patterns())

    def detect_invalidation_llm(
        self,
        new_content: str,
        old_facts: list[dict],
    ) -> list[dict]:
        """
        LLM 驱动的事实失效检测。

        当 llm_fn 可用时，用 LLM 判断新内容是否使旧事实失效。
        LLM 调用失败时静默跳过，返回空列表。

        参数:
            new_content: 新写入的内容
            old_facts: 旧事实列表，每项需包含 memory_id 和 content 字段

        返回: 失效事实列表 [{"old_fact_id": "xxx", "reason": "xxx"}, ...]
        """
        if not self._llm_fn or not new_content or not old_facts:
            return []

        # 构建旧事实摘要，限制条数避免 prompt 过长
        max_facts = 20
        facts_to_check = old_facts[:max_facts]
        facts_text = "\n".join(
            f"- ID: {f.get('memory_id', '?')[:16]}, 内容: {f.get('content', '')[:200]}"
            for f in facts_to_check
        )

        prompt = (
            "你是一个事实一致性检测器。给定新写入的内容和旧事实列表，"
            "判断哪些旧事实被新内容推翻或修正。\n\n"
            "新内容:\n"
            f"{new_content[:500]}\n\n"
            "旧事实列表:\n"
            f"{facts_text}\n\n"
            "请返回 JSON 数组，每项包含 old_fact_id（旧事实的 ID）和 reason（失效原因）。"
            "只返回被新内容直接推翻或修正的旧事实，不要包含仍然有效的事实。"
            "如果没有旧事实被推翻或修正，返回空数组 []。\n"
            '返回格式: [{"old_fact_id": "xxx", "reason": "xxx"}, ...]\n'
            "只返回 JSON，不要包含其他文字。"
        )

        try:
            raw = self._llm_fn(prompt)
            if not raw:
                return []

            # 尝试从返回文本中提取 JSON
            text = raw.strip()
            # 处理 markdown 代码块包裹的情况
            if text.startswith("```"):
                lines = text.split("\n")
                # 去掉首尾的 ``` 行
                lines = [l for l in lines if not l.strip().startswith("```")]
                text = "\n".join(lines).strip()

            result = json.loads(text)
            if not isinstance(result, list):
                return []

            # 校验每项的字段
            validated = []
            for item in result:
                if isinstance(item, dict) and "old_fact_id" in item and "reason" in item:
                    validated.append({
                        "old_fact_id": str(item["old_fact_id"]),
                        "reason": str(item["reason"]),
                    })

            return validated

        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.debug("temporal: LLM 失效检测返回解析失败: %s", e)
            return []
        except Exception as e:
            logger.warning("temporal: LLM 失效检测调用异常: %s", e)
            return []

    def mark_invalid(
        self,
        memory_id: str,
        invalidated_by: str,
        store,
    ) -> bool:
        """
        标记事实失效。

        操作：
        1. 设置 valid_until = time.time()
        2. 更新 lifecycle_state = "superseded"
        3. 记录失效原因

        参数:
            memory_id: 要标记失效的记忆 ID
            invalidated_by: 导致失效的新记忆 ID
            store: MemoryStore 实例

        返回: 是否成功标记
        """
        now = time.time()
        try:
            with store.transaction() as txn_conn:
                # 更新 valid_until
                txn_conn.execute(
                    "UPDATE memories SET valid_until = ? WHERE memory_id = ? AND valid_until IS NULL",
                    (now, memory_id),
                )
                # 更新 lifecycle 相关字段（如果存在）
                with contextlib.suppress(Exception):
                    txn_conn.execute(
                        "UPDATE memories SET lifecycle_state = 'superseded' WHERE memory_id = ?",
                        (memory_id,),
                    )

                # 记录失效原因到 memory_links
                txn_conn.execute(
                    """INSERT OR IGNORE INTO memory_links (source_id, target_id, link_type, weight, reason)
                       VALUES (?, ?, 'temporal_superseded', 1.0, ?)""",
                    (invalidated_by, memory_id, f"被 {invalidated_by[:16]}... 时间线失效标记"),
                )

            logger.info(
                "temporal: 记忆 %s 已标记失效 (invalidated_by=%s, valid_until=%.1f)",
                memory_id[:16], invalidated_by[:16], now,
            )
            return True
        except Exception as e:
            logger.error("temporal: 标记失效失败: %s", e)
            return False

    # ── 内部方法 ──────────────────────────────────────

    def _extract_occurrence_time(self, content: str) -> float | None:
        """从内容中提取事件实际发生的时间"""

        for pattern, unit in self._RELATIVE_TIME_PATTERNS:
            match = re.search(pattern, content)
            if not match:
                continue

            try:
                if unit == "days":
                    delta = timedelta(days=int(match.group(1)))
                elif unit == "weeks":
                    delta = timedelta(weeks=int(match.group(1)))
                elif unit == "months":
                    delta = timedelta(days=int(match.group(1)) * 30)
                elif unit == "years":
                    delta = timedelta(days=int(match.group(1)) * 365)
                elif unit == "days_3":
                    delta = timedelta(days=3)
                elif unit == "days_2":
                    delta = timedelta(days=2)
                elif unit == "days_1":
                    delta = timedelta(days=1)
                elif unit == "last_week":
                    delta = timedelta(weeks=1)
                elif unit == "last_month":
                    delta = timedelta(days=30)
                elif unit == "last_year":
                    delta = timedelta(days=365)
                elif unit == "just_now":
                    delta = timedelta(seconds=0)
                else:
                    continue

                return (datetime.now() - delta).timestamp()
            except (ValueError, IndexError):
                continue

        # 检测绝对时间表达："2024年3月15日"
        abs_match = re.search(
            r"(\d{4})年(\d{1,2})月(\d{1,2})日?", content
        )
        if abs_match:
            try:
                dt = datetime(
                    int(abs_match.group(1)),
                    int(abs_match.group(2)),
                    int(abs_match.group(3)),
                )
                return dt.timestamp()
            except ValueError:
                pass

        return None

    def _extract_valid_from(self, content: str) -> float | None:
        """从内容中提取事实开始有效的时间"""

        for pattern, unit in self._VALID_FROM_PATTERNS:
            match = re.search(pattern, content)
            if not match:
                continue

            try:
                if unit == "absolute_date":
                    dt = datetime(
                        int(match.group(1)),
                        int(match.group(2)),
                        int(match.group(3)),
                    )
                    return dt.timestamp()
                elif unit == "absolute_month":
                    dt = datetime(int(match.group(1)), int(match.group(2)), 1)
                    return dt.timestamp()
                elif unit == "absolute_year":
                    dt = datetime(int(match.group(1)), 1, 1)
                    return dt.timestamp()
                elif unit == "from_last_year":
                    dt = datetime(datetime.now().year - 1, 1, 1)
                    return dt.timestamp()
                elif unit == "from_last_month":
                    d = datetime.now()
                    month = d.month - 1
                    year = d.year
                    if month < 1:
                        month = 12
                        year -= 1
                    dt = datetime(year, month, 1)
                    return dt.timestamp()
            except (ValueError, IndexError):
                continue

        return None

    def _extract_valid_until(self, content: str) -> float | None:
        """从内容中提取事实失效的时间"""
        for pattern, unit in self._VALID_UNTIL_PATTERNS:
            match = re.search(pattern, content)
            if not match:
                continue

            try:
                if unit == "absolute_date":
                    dt = datetime(
                        int(match.group(1)),
                        int(match.group(2)),
                        int(match.group(3)),
                        23, 59, 59,
                    )
                    return dt.timestamp()
                elif unit == "absolute_month":
                    d = datetime(int(match.group(1)), int(match.group(2)), 1)
                    # 月末
                    if d.month == 12:
                        dt = datetime(d.year + 1, 1, 1, 23, 59, 59)
                    else:
                        dt = datetime(d.year, d.month + 1, 1, 23, 59, 59)
                    return dt.timestamp() - 1  # 月末最后一秒
                elif unit == "absolute_year":
                    dt = datetime(int(match.group(1)), 12, 31, 23, 59, 59)
                    return dt.timestamp()
            except (ValueError, IndexError):
                continue

        return None
