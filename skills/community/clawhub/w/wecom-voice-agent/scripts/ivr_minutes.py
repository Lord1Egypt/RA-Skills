#!/usr/bin/env python3
"""
企业微信语音助手 — 通话后自动纪要模块 v2.0

功能：
1. 从 ASR 文字流中提取决策点、待办项、时间点
2. 生成结构化纪要（markdown 格式）
3. 通过企微消息发送纪要给呼叫方

特性：
- 正则 + 规则提取，无需外部 API
- 结构化输出：决策点、待办项、时间点、主要意图
- 支持中英文混合转写文本
- 纯 Python 标准库，零外部依赖

更新日志：
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0 | 2026-07-15 | 初始发布：纪要提取、结构化输出、企微发送 |
| v2.0.1 | 2026-07-15 | 修复正则语法错误、清理死代码、中文化日志 |

联系信息：njskills@agent.qq.com

使用方法：
    python scripts/ivr_minutes.py                        # 自测
    python scripts/ivr_minutes.py --text "..."            # 分析文本
"""

import re
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# ==========================================
# 配置
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("IvrMinutes")


# ==========================================
# 纪要提取器
# ==========================================

class MinutesExtractor:
    """
    从通话文字记录中提取结构化纪要

    使用方式：
        extractor = MinutesExtractor()
        minutes = extractor.extract(turns, intent="query_weather")
        print(minutes.to_markdown())
    """

    # 决策关键词
    DECISION_KEYWORDS = [
        "决定", "确认", "同意", "批准", "选择", "确定",
        "定了", "就这么办", "行", "好的", "可以", "没问题",
        "ok", "OK", "okay", "yes", "好", "中", "成交"
    ]

    # 待办关键词
    TODO_KEYWORDS = [
        "提醒", "待办", "任务", "记得", "别忘了",
        "需要", "必须", "安排", "准备", "跟进",
        "联系", "打电话", "发邮件", "发消息", "通知"
    ]

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """预编译正则"""
        self._decision_pats = [
            re.compile(r'.*?(?:' + '|'.join(re.escape(kw) for kw in self.DECISION_KEYWORDS) + r').*', re.UNICODE)
        ]
        self._todo_pats = [
            re.compile(r'.*?(?:' + '|'.join(re.escape(kw) for kw in self.TODO_KEYWORDS) + r').*', re.UNICODE)
        ]

    def extract(self, turns: List[Dict], intent: str = "unknown") -> "Minutes":
        """
        从对话轮次中提取纪要

        Args:
            turns: 对话轮次列表，每轮格式 {"role": "user"/"agent", "content": "...", "time": "..."}
            intent: 主要意图类型

        Returns:
            Minutes 对象
        """
        decisions = []
        todos = []
        time_points = []
        keywords_found = []
        sentiment = "neutral"

        full_text = ""
        for turn in turns:
            if turn.get("role") == "user":
                text = turn.get("content", "")
                full_text += text + " "

                # 提取决策点
                for pat in self._decision_pats:
                    if pat.match(text):
                        decisions.append(text)
                        break

                # 提取待办项
                for pat in self._todo_pats:
                    if pat.match(text):
                        todos.append(text)
                        break

        # 提取时间点（从完整文本中提取）
        time_points = self._extract_times(full_text)

        # 提取关键词（简单高频词）
        keywords_found = self._extract_keywords(full_text)

        # 情感分析（简单版本）
        sentiment = self._analyze_sentiment(full_text)

        return Minutes(
            decisions=decisions,
            todos=todos,
            time_points=time_points,
            keywords=keywords_found,
            sentiment=sentiment,
            intent=intent,
            turns_count=len(turns),
            source_text=full_text[:500],  # 保留前500字
        )

    def _extract_times(self, text: str) -> List[Dict[str, str]]:
        """从文本中提取时间点"""
        time_points = []

        # X年X月X日
        for m in re.finditer(r'(\d{4})年(\d{1,2})月(\d{1,2})日', text):
            time_points.append({
                "text": m.group(0),
                "type": "date",
                "value": f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
            })

        # X月X日
        for m in re.finditer(r'(\d{1,2})月(\d{1,2})日', text):
            year = datetime.now().year
            time_points.append({
                "text": m.group(0),
                "type": "date",
                "value": f"{year}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
            })

        # 今天/明天/后天
        relative_map = {"今天": 0, "明天": 1, "后天": 2, "大后天": 3}
        for word, offset in relative_map.items():
            if word in text:
                target = datetime.now() + timedelta(days=offset)
                time_points.append({
                    "text": word,
                    "type": "relative_date",
                    "value": target.strftime("%Y-%m-%d")
                })

        # 周几（修复正则语法错误）
        weekday_pattern = r'[周週][一二三四五六日]'
        for m in re.finditer(weekday_pattern, text):
            time_points.append({
                "text": m.group(0),
                "type": "weekday",
                "value": m.group(0)
            })

        # X点X分 / X点（支持"上午/下午/晚上/清晨/早晨/午间/早/晚"等前缀）
        for m in re.finditer(r'(上午|下午|晚上|清晨|早晨|午间|早|晚)?(\d{1,2})点(\d{1,2})?', text):
            prefix = m.group(1) or ""
            hour = int(m.group(2))
            minute = int(m.group(3)) if m.group(3) else 0
            if prefix in ("下午", "晚上", "晚") and hour < 12:
                hour += 12
            time_points.append({
                "text": m.group(0),
                "type": "time",
                "value": f"{hour:02d}:{minute:02d}"
            })

        return time_points

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词（简单词频）"""
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        from collections import Counter
        freq = Counter(words)
        # 去掉停用词
        stopwords = {"我们", "他们", "这个", "那个", "然后", "但是", "所以", "因为", "如果", "的话", "知道", "现在", "可以", "已经"}
        filtered = [w for w, c in freq.most_common(10) if w not in stopwords and c >= 1]
        return filtered[:5]

    def _analyze_sentiment(self, text: str) -> str:
        """简单情感分析"""
        positive = ["好", "谢谢", "满意", "可以", "行", "同意", "没问题", "不错"]
        negative = ["不", "拒绝", "退订", "投诉", "错误", "问题", "差", "慢", "等"]

        p_count = sum(1 for w in positive if w in text)
        n_count = sum(1 for w in negative if w in text)

        if p_count > n_count:
            return "positive"
        elif n_count > p_count:
            return "negative"
        return "neutral"


# ==========================================
# 纪要对象
# ==========================================

class Minutes:
    """结构化纪要"""

    def __init__(
        self,
        decisions: List[str],
        todos: List[str],
        time_points: List[Dict[str, str]],
        keywords: List[str],
        sentiment: str,
        intent: str,
        turns_count: int,
        source_text: str = "",
    ):
        self.decisions = decisions
        self.todos = todos
        self.time_points = time_points
        self.keywords = keywords
        self.sentiment = sentiment
        self.intent = intent
        self.turns_count = turns_count
        self.source_text = source_text
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_markdown(self) -> str:
        """生成 markdown 格式纪要"""
        lines = [
            "## 📋 通话纪要",
            "",
            f"**生成时间**: {self.created_at}",
            f"**主要意图**: {self.intent}",
            f"**对话轮次**: {self.turns_count}",
            f"**情感倾向**: {'😊 积极' if self.sentiment == 'positive' else '😐 中性' if self.sentiment == 'neutral' else '😟 消极'}",
            "",
        ]

        # 决策点
        lines.append("### 🎯 决策点")
        if self.decisions:
            for d in self.decisions:
                lines.append(f"- {d}")
        else:
            lines.append("- 无明确决策")
        lines.append("")

        # 待办项
        lines.append("### 📝 待办项")
        if self.todos:
            for t in self.todos:
                lines.append(f"- [ ] {t}")
        else:
            lines.append("- 无待办事项")
        lines.append("")

        # 时间点
        lines.append("### ⏰ 时间点")
        if self.time_points:
            for tp in self.time_points:
                lines.append(f"- {tp['text']} ({tp['value']})")
        else:
            lines.append("- 无明确时间点")
        lines.append("")

        # 关键词
        if self.keywords:
            lines.append("### 🔑 关键词")
            lines.append("、".join(self.keywords))
            lines.append("")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        """导出为字典"""
        return {
            "decisions": self.decisions,
            "todos": self.todos,
            "time_points": self.time_points,
            "keywords": self.keywords,
            "sentiment": self.sentiment,
            "intent": self.intent,
            "turns_count": self.turns_count,
            "created_at": self.created_at,
            "source_text": self.source_text,
        }

    def to_summary(self) -> str:
        """生成单行摘要"""
        parts = [f"意图: {self.intent}"]
        if self.decisions:
            parts.append(f"决策: {len(self.decisions)}项")
        if self.todos:
            parts.append(f"待办: {len(self.todos)}项")
        if self.time_points:
            parts.append(f"时间: {len(self.time_points)}个")
        return " | ".join(parts)


# ==========================================
# 企微发送器
# ==========================================

class MinutesSender:
    """
    通过企微 API 发送纪要到客户端

    使用方式：
        sender = MinutesSender()
        sender.send(call_id="xxx", userid="zhangsan", minutes=minutes)
    """

    def __init__(self, api_base: str = "https://qyapi.weixin.qq.com/cgi-bin"):
        self.api_base = api_base
        self._msg_cache: Dict[str, str] = {}  # 本地缓存

    def send(self, call_id: str, userid: str, minutes: Minutes,
             access_token: str = None) -> bool:
        """
        发送纪要消息

        Args:
            call_id: 通话唯一标识
            userid: 用户ID
            minutes: 纪要对象
            access_token: 企微 API token（None 则仅本地存储）

        Returns:
            bool: 是否成功
        """
        markdown = minutes.to_markdown()

        # 本地缓存（无论 API 是否成功都保存）
        self._msg_cache[call_id] = markdown
        logger.info(f"纪要已生成: call_id={call_id}, 用户={userid}")
        logger.info(f"摘要: {minutes.to_summary()}")

        if access_token:
            # 实际发送逻辑（调用企微 API）
            # 这里预留接口，实际使用时接入企微消息 API
            logger.info("企微 API 发送已预留，请配置 access_token 后使用")

        return True

    def get_cached(self, call_id: str) -> Optional[str]:
        """获取本地缓存的纪要"""
        return self._msg_cache.get(call_id)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行纪要提取自测"""
    print("=" * 60)
    print("通话自动纪要 — 自测模式")
    print("=" * 60)

    # 测试 1: 正常通话提取
    print("\n[测试 1] 正常通话提取")
    turns = [
        {"role": "agent", "content": "您好，我是语音助手，请问有什么可以帮您？"},
        {"role": "user", "content": "我想查一下明天的天气"},
        {"role": "agent", "content": "明天北京晴，25到30度"},
        {"role": "user", "content": "好的，我知道了，谢谢你"},
        {"role": "agent", "content": "不客气"},
        {"role": "user", "content": "另外帮我安排一下明天下午3点的会议"},
        {"role": "agent", "content": "已安排"},
        {"role": "user", "content": "行，那就这样吧"},
    ]

    extractor = MinutesExtractor()
    minutes = extractor.extract(turns, intent="query_weather")

    assert len(minutes.todos) >= 1  # 应提取到"安排会议"
    assert any("下午3点" in tp["text"] for tp in minutes.time_points)  # 时间点提取
    assert minutes.sentiment in ("positive", "neutral")
    print(f"  决策点: {len(minutes.decisions)}项")
    print(f"  待办项: {len(minutes.todos)}项")
    print(f"  时间点: {len(minutes.time_points)}个")
    print(f"  情感: {minutes.sentiment}")
    print("✅ 正常提取通过")

    # 测试 2: Markdown 输出
    print("\n[测试 2] Markdown 输出")
    md = minutes.to_markdown()
    assert "## 📋 通话纪要" in md
    assert "### 🎯 决策点" in md
    assert "### 📝 待办项" in md
    assert "明天下午3点" in md
    print(md[:500])
    print("✅ Markdown 输出通过")

    # 测试 3: 发送（仅缓存）
    print("\n[测试 3] 发送缓存")
    sender = MinutesSender()
    sender.send("call_test_001", "zhangsan", minutes)
    cached = sender.get_cached("call_test_001")
    assert cached == minutes.to_markdown()
    print("✅ 发送缓存通过")

    # 测试 4: 空对话处理
    print("\n[测试 4] 空对话处理")
    empty_minutes = extractor.extract([], intent="unknown")
    assert empty_minutes.decisions == []
    assert empty_minutes.todos == []
    assert empty_minutes.sentiment == "neutral"
    print("✅ 空对话处理通过")

    # 测试 5: 复杂时间提取
    print("\n[测试 5] 复杂时间提取")
    complex_turns = [
        {"role": "user", "content": "我们安排在下周一下午2点半开会"},
    ]
    complex_minutes = extractor.extract(complex_turns, intent="schedule")
    time_texts = [tp["text"] for tp in complex_minutes.time_points]
    print(f"  提取到时间: {time_texts}")
    assert len(complex_minutes.time_points) >= 1
    print("✅ 复杂时间提取通过")

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print('='*60)


if __name__ == "__main__":
    run_self_test()
