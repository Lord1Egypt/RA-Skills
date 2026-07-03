#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""todo-list skill 自然语言解析器。

本模块提供 :class:`NLParser` 类，将中/英文自然语言输入转换为结构化的
TODO 数据。

架构（4 步）：
    1. 动作识别：done > delete > update > add > list（优先级）
    2. 时间提取：相对时间（今天/明天/下周一）+ 绝对时间（14:00）
    3. 优先级提取：high / medium / low
    4. 标签提取：#tag 或 tag:tag 语法

可选依赖：
    - dateutil：高级日期解析（缺失时自动回退到正则）
    - jieba：中文分词（自动加载 data/user_dict.txt）

使用示例：
    >>> from src.nl_parser import parse
    >>> parse("提醒我明天下午3点检查止损")
    {
        "action": "add",
        "content": "检查止损",
        "due_at": "2026-06-12 15:00:00",
        "priority": "medium",
        "tags": [],
    }

参见：
    - DESIGN.md §4.3（NLP 解析器设计）
    - references/triggers.md（完整触发词表）
    - data/user_dict.txt（jieba 自定义词典）
    - data/test_cases.json（20 个回归测试 case）
    - SOUL.md 规则 16（数据源调研）

License:
    MIT

Version:
    1.4.0

Author:
    月海巫师 (Chen Qing)
"""
from __future__ import annotations  # PEP 563：延后求值类型注解

import re
from datetime import datetime, timedelta
from typing import Any

try:
    from dateutil import parser as dateutil_parser
    HAS_DATEUTIL = True
except ImportError:
    HAS_DATEUTIL = False

try:
    import jieba
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False


# ── 触发词表（业界参考：anthropics/skills todo） ─────────────────

# 动作识别（按优先级：done > delete > update > add > list）
ACTION_DONE = {
    "完成", "完成了", "做完", "做完了", "done", "finished", "完成下", "完成它",
    "搞定了", "搞定", "✓", "已办", "办完", "完成：", "完了：",
}

ACTION_DELETE = {
    "删除", "删掉", "删", "remove", "delete", "取消", "撤销",
    "不要了", "扔了",
}

ACTION_UPDATE = {
    "修改", "改", "更新", "改一下", "改成", "update", "改时间",
    "延后", "提前",
}

ACTION_ADD = {
    "提醒我", "提醒", "记一下", "加个待办", "加个", "加",
    "新建", "新待办", "紧急", "重要",
    "写", "做", "准备", "安排", "记得", "需要", "看",
    "提交", "开会", "起床", "上班", "下班", "吃饭", "睡觉", "锻炼", "学习",
    "交", "去", "买", "拿", "寄", "取", "问",
    "复盘", "建仓", "加仓", "减仓", "清仓", "调仓", "定投", "止损", "止盈",
    "上线", "发版", "交付", "复习", "预习",
}

ACTION_LIST = {
    "查询", "列出", "显示", "list", "show",
    "查看", "有什么", "什么待办", "哪些", "我的待办", "我的任务",
    "查", "查所有", "查一下", "看下", "看看",
}

# 优先级关键词
PRIORITY_HIGH = {"高", "紧急", "急", "重要", "high", "urgent", "!!"}
PRIORITY_LOW = {"低", "不急", "low", "慢慢", "无所谓", "·"}

# 时间关键词
TIME_NOW = {"刚才", "现在", "此刻", "now", "just now"}


class NLParser:
    """
    自然语言解析器

    业界参考：
    - DESIGN.md §4.3（NLP 解析模块）
    - anthropics/skills/todo（简化版触发词）
    """

    # 预编译正则（性能优化）
    RE_TIME = re.compile(
        r"(?:"
        r"(今天|明天|后天|大后天|下周|下个月|下周一|下周二|下周三|下周四|下周五|下周六|下周日"
        r"|今早|今晚|明早|明晚|今晚上|明晚上)"
        r"(?:"
        r"\s*(?:上午|下午|早上|晚上|am|pm|AM|PM)?"
        r"\s*"
        r"\d{1,2}\s*[点时:：]\s*\d{0,2}\s*[分]?"
        r")"
        r")"
        r"|"
        r"(?:"
        r"(今天|明天|后天|大后天|下周|下个月|下周一|下周二|下周三|下周四|下周五|下周六|下周日"
        r"|今早|今晚|明早|明晚|今晚上|明晚上)"
        r"(?=\s*\d)"  # 必须后跟数字才匹配
        r")"
        r"|"
        r"\d{1,2}\s*[点时:：]\s*\d{0,2}\s*[分]?"
        r"|"
        r"\d{4}-\d{1,2}-\d{1,2}\s*\d{0,2}[点时:：]?\d{0,2}[分]?",
        re.UNICODE,
    )

    RE_TAG_EXPLICIT = re.compile(r"(?:tag[:：]|#)([一-鿿\w,\s]+?)(?=\s|$|，|。|；)")
    RE_PRIORITY = re.compile(r"!!+|!!|high|urgent|紧急|急")

    def __init__(self):
        if HAS_JIEBA:
            # 加载自定义词典（行业术语，可选）
            dict_path = self._custom_dict_path()
            import os
            if os.path.exists(dict_path):
                jieba.load_userdict(dict_path)

    def _custom_dict_path(self) -> str:
        """返回自定义词典路径"""
        import os
        return os.path.join(os.path.dirname(__file__), "..", "data", "user_dict.txt")

    def parse(self, text: str) -> dict[str, Any]:
        """
        解析用户输入的自然语言

        Returns:
            {
                "action": "add" | "list" | "done" | "delete" | "update" | "unknown",
                "content": str,
                "due_at": str | None,  # ISO8601 格式
                "priority": "high" | "medium" | "low" | None,
                "tags": list[str],
                "raw": str,  # 原始输入
                "matched_keywords": list[str],  # 命中的关键词
            }
        """
        # 1. 边界处理
        if not text or not text.strip():
            return self._make_result("unknown", "", raw=text)

        text = text.strip()
        if len(text) > 2000:
            text = text[:2000]

        # 2. 识别 action（按优先级）
        action, action_keyword = self._extract_action(text)
        if action == "unknown":
            return self._make_result("unknown", text, raw=text, matched_keywords=[action_keyword] if action_keyword else [])

        # 3. 提取 content（去除动作词 + 时间词 + 标签 + 优先级）
        content = self._extract_content(text, action_keyword)
        content = content.strip().rstrip("，,。.!?！？").strip()

        # 4. 提取时间
        due_at = self._extract_time(text)

        # 5. 提取优先级
        priority = self._extract_priority(text)

        # 6. 提取标签
        tags = self._extract_tags(text)

        # 7. content 必填（除 list 外）
        if not content and action != "list":
            return self._make_result("unknown", text, raw=text, matched_keywords=[action_keyword])

        return self._make_result(
            action, content, due_at, priority, tags,
            raw=text, matched_keywords=[action_keyword] if action_keyword else [],
        )

    def _make_result(
        self,
        action: str,
        content: str,
        due_at: str | None = None,
        priority: str | None = None,
        tags: list[str] | None = None,
        raw: str = "",
        matched_keywords: list[str] | None = None,
    ) -> dict[str, Any]:
        return {
            "action": action,
            "content": content,
            "due_at": due_at,
            "priority": priority or "medium",
            "tags": tags or [],
            "raw": raw,
            "matched_keywords": matched_keywords or [],
        }

    # ── 动作识别 ──────────────────────────────────────────────

    def _extract_action(self, text: str) -> tuple[str, str]:
        """
        识别 action

        Returns: (action, matched_keyword)
        """
        # 优先级：done > delete > update > add > list
        # 每个集合内做最长匹配
        text_lower = text.lower()
        text_stripped = text.strip()

        for kw_set, action in [
            (ACTION_DONE, "done"),
            (ACTION_DELETE, "delete"),
            (ACTION_UPDATE, "update"),
            (ACTION_ADD, "add"),
            (ACTION_LIST, "list"),
        ]:
            for kw in sorted(kw_set, key=len, reverse=True):  # 长词优先匹配
                # 关键词在句首 OR 是独立词才触发
                if kw.lower() in text_lower or kw in text:
                    # 避免误命中："已完成 5 个" 中"完成"不是命令
                    if kw in ("完成", "搞定") and not (
                        text_stripped.startswith(kw) or
                        text_stripped.startswith(kw + "：") or
                        text_stripped.startswith(kw + ":")
                    ):
                        continue
                    return action, kw

        return "unknown", ""

    # ── 内容提取 ──────────────────────────────────────────────

    def _extract_content(self, text: str, action_keyword: str) -> str:
        """提取核心内容（去除时间、标签、优先级）"""
        content = text

        # 1. 去除时间词
        content = self.RE_TIME.sub("", content)

        # 2. 去除优先级关键词
        for kw in PRIORITY_HIGH | PRIORITY_LOW:
            content = content.replace(kw, "")
        content = self.RE_PRIORITY.sub("", content)

        # 3. 去除标签
        content = self.RE_TAG_EXPLICIT.sub("", content)

        # 4. 去除"明天3点"等组合（用简单的"X点"模式）
        content = re.sub(r"\d{1,2}[点时:：]\d{0,2}[分]?", "", content)

        # 5. 清理标点
        content = re.sub(r"^[：:，,。.!?！？\s]+", "", content)
        content = re.sub(r"[：:，,。.!?！？\s]+$", "", content)
        content = re.sub(r"\s+", " ", content).strip()

        # 注意：不再删除 action 关键词（中文里 action 词常也是 content 词）
        return content

    # ── 时间解析 ──────────────────────────────────────────────

    def _extract_time(self, text: str) -> str | None:
        """
        提取并解析时间

        Returns: ISO8601 字符串 或 None
        """
        # 1. 匹配时间关键词
        match = self.RE_TIME.search(text)
        if not match:
            return None

        time_str = match.group(0)

        # 2. 解析"明天 15:00"格式
        return self._parse_time_string(time_str, text)

    def _parse_time_string(self, time_str: str, full_text: str) -> str | None:
        """解析时间字符串为 ISO8601"""
        now = datetime.now()

        # 1. 相对日期
        if "今天" in time_str:
            base = now
        elif "明天" in time_str:
            base = now + timedelta(days=1)
        elif "后天" in time_str:
            base = now + timedelta(days=2)
        elif "大后天" in time_str:
            base = now + timedelta(days=3)
        elif "下周" in time_str:
            base = now + timedelta(days=7)
        elif "下个月" in time_str:
            base = now + timedelta(days=30)
        elif "下周一" in time_str:
            base = now + timedelta(days=(7 - now.weekday() + 0) % 7 or 7)
        elif "下周二" in time_str:
            base = now + timedelta(days=(7 - now.weekday() + 1) % 7 or 7)
        elif "下周三" in time_str:
            base = now + timedelta(days=(7 - now.weekday() + 2) % 7 or 7)
        elif "下周四" in time_str:
            base = now + timedelta(days=(7 - now.weekday() + 3) % 7 or 7)
        elif "下周五" in time_str:
            base = now + timedelta(days=(7 - now.weekday() + 4) % 7 or 7)
        elif "下周六" in time_str:
            base = now + timedelta(days=(7 - now.weekday() + 5) % 7 or 7)
        elif "下周日" in time_str:
            base = now + timedelta(days=(7 - now.weekday() + 6) % 7 or 7)
        elif "今早" in time_str or "明早" in time_str:
            base = now + (timedelta(days=1) if "明" in time_str else timedelta(days=0))
        elif "今晚" in time_str or "明晚" in time_str:
            base = now + (timedelta(days=1) if "明" in time_str else timedelta(days=0))
        else:
            # 2. 尝试 dateutil
            if HAS_DATEUTIL:
                try:
                    dt = dateutil_parser.parse(time_str, fuzzy=True)
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, OverflowError):
                    pass
            return None

        # 3. 提取时间部分（如 "15:00" 或 "15点30分"）
        time_part = re.search(r"(\d{1,2})\s*[点时:：]\s*(\d{0,2})\s*[分]?", time_str)
        if time_part:
            hour = int(time_part.group(1))
            minute = int(time_part.group(2) or 0)
            # 上下午处理（包括"今晚/明晚"）
            if "下午" in time_str or "晚上" in time_str or "今晚" in time_str or "明晚" in time_str:
                if hour < 12:
                    hour += 12
            # 边界校验
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                return None
            result = base.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return result.strftime("%Y-%m-%d %H:%M:%S")

        # 没指定时间，默认为当天 9:00
        return base.replace(hour=9, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")

    # ── 优先级解析 ──────────────────────────────────────────────

    def _extract_priority(self, text: str) -> str | None:
        text_lower = text.lower()
        # 长词优先（"不急" 优先于 "急"，"重要" 优先于 "急"）
        all_kws_high = sorted(PRIORITY_HIGH, key=len, reverse=True)
        all_kws_low = sorted(PRIORITY_LOW, key=len, reverse=True)
        for kw in all_kws_low:
            if kw in text or kw.lower() in text_lower:
                return "low"
        for kw in all_kws_high:
            if kw in text or kw.lower() in text_lower:
                return "high"
        return None  # 默认 medium（但 _make_result 会用 medium）

    # ── 标签解析 ──────────────────────────────────────────────

    def _extract_tags(self, text: str) -> list[str]:
        """提取标签（tag:xxx 或 #xxx 格式）"""
        tags = []
        matches = self.RE_TAG_EXPLICIT.findall(text)
        for match in matches:
            # 多个 tag 用逗号或空格分隔
            for tag in re.split(r"[,，\s]+", match):
                tag = tag.strip()
                if tag and tag not in tags:
                    tags.append(tag)
        return tags


# ── 模块级单例 ────────────────────────────────────────────────

_parser: NLParser | None = None


def parse(text: str) -> dict[str, Any]:
    """便捷函数：解析自然语言"""
    global _parser
    if _parser is None:
        _parser = NLParser()
    return _parser.parse(text)


__all__ = ["NLParser", "parse"]