"""
reactor.py - 记忆驱动的主动 Agent 反应器
事件触发 → 条件匹配 → 执行动作

记忆不是被动仓库，而是 Agent 的感知器官。

v1.0 支持的事件:
  - on_write:         新记忆写入时（时间解析 → 自动设提醒）
  - on_contradiction: 矛盾检测到时（主动问用户确认）
  - on_decay_review:  衰减到期时（主动问是否还 relevant）
  - on_decision_complete: 决策链条完整时（自动生成决策文档）

架构:
  MemoryReactor
  ├── hooks: dict[event_type, list[Hook]]
  ├── scan(store) → list[Event]   扫描并触发所有事件
  ├── fire(event) → list[Action]  触发单个事件，返回执行的动作
  └── built-in conditions + actions
"""

from __future__ import annotations

import re
import time
import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Callable, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════

@dataclass
class Hook:
    """一个事件钩子：条件 + 动作"""
    name: str
    condition: Callable[[dict], bool]   # 返回 True 则触发
    action: Callable[[dict, object], dict]  # (event_ctx, store) → action_result
    enabled: bool = True
    priority: int = 0                   # 数字越大越先执行


@dataclass
class Event:
    """一个待处理的事件"""
    event_type: str
    memory: dict                        # 触发事件的记忆
    context: dict = field(default_factory=dict)  # 附加上下文


@dataclass
class ActionResult:
    """动作执行结果"""
    action_name: str
    success: bool
    message: str
    data: dict = field(default_factory=dict)


# ═══════════════════════════════════════════════════════
# 时间表达式解析器
# ═══════════════════════════════════════════════════════

class TimeParser:
    """
    解析中文自然语言时间表达式，返回 UNIX 时间戳。

    支持:
      - "明天下午3点" / "明天15:00"
      - "后天上午10点半"
      - "3天后" / "一周后"
      - "下周一"
      - "2026-04-20 14:00"
      - "今晚8点" / "明早9点"
    """

    # 中文数字映射
    CN_DIGITS = {
        '零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
        '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
        '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24,
        '二十五': 25, '二十六': 26, '二十七': 27, '二十八': 28,
        '二十九': 29, '三十': 30, '三十一': 31,
        '半': 30,  # "半" 表示 30 分钟
    }

    WEEKDAY_MAP = {
        '一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6, '天': 6,
    }

    def __init__(self, now_fn=None):
        self._now_fn = now_fn or time.time

    def parse(self, text: str) -> Optional[int]:
        """
        尝试从文本中提取时间表达式并转换为 UNIX 时间戳。
        找不到返回 None。
        """
        now_ts = self._now_fn()
        now = datetime.fromtimestamp(now_ts)

        # 1. ISO 格式: 2026-04-20 14:00 / 2026-04-20T14:00
        m = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})\s*[T ](\d{1,2}):(\d{2})', text)
        if m:
            try:
                dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                              int(m.group(4)), int(m.group(5)))
                ts = dt.timestamp()
                if ts > now_ts:
                    return int(ts)
            except ValueError:
                pass

        # 2. "X天后" / "X周后" / "X个月后" (支持中文数字)
        m = re.search(r'(\d+|' + '|'.join(re.escape(k) for k in self.CN_DIGITS.keys()) + r')\s*(天|周|个月|小时|分钟)后', text)
        if m:
            n = self._parse_number(m.group(1))
            unit = m.group(2)
            if n is not None:
                delta = {
                    '天': timedelta(days=n),
                    '周': timedelta(weeks=n),
                    '个月': timedelta(days=n * 30),
                    '小时': timedelta(hours=n),
                    '分钟': timedelta(minutes=n),
                }.get(unit)
                if delta:
                    return int((now + delta).timestamp())

        # 3. "明天/后天/大后天" + [时段] + [时间]
        day_offset = 0
        if '大后天' in text:
            day_offset = 3
        elif '后天' in text:
            day_offset = 2
        elif '明天' in text:
            day_offset = 1
        elif '今晚' in text or '今晚' in text:
            day_offset = 0
        elif '明早' in text:
            day_offset = 1

        if day_offset > 0 or '今晚' in text or '明早' in text:
            target_date = now.date() + timedelta(days=day_offset)
            hour, minute = self._extract_time(text)
            if hour is not None:
                dt = datetime(target_date.year, target_date.month, target_date.day, hour, minute or 0)
                ts = dt.timestamp()
                if ts > now_ts:
                    return int(ts)
            elif '明早' in text:
                dt = datetime(target_date.year, target_date.month, target_date.day, 9, 0)
                return int(dt.timestamp())
            elif '今晚' in text:
                dt = datetime(target_date.year, target_date.month, target_date.day, 20, 0)
                ts = dt.timestamp()
                if ts > now_ts:
                    return int(ts)

        # 4. "下周一" / "下周三"
        m = re.search(r'下\s?周\s?([一二三四五六日天])', text)
        if m:
            target_weekday = self.WEEKDAY_MAP.get(m.group(1))
            if target_weekday is not None:
                days_ahead = (target_weekday - now.weekday()) % 7
                if days_ahead <= 0:
                    days_ahead += 7
                target_date = now.date() + timedelta(days=days_ahead)
                hour, minute = self._extract_time(text)
                if hour is None:
                    hour, minute = 9, 0  # 默认早上9点
                dt = datetime(target_date.year, target_date.month, target_date.day, hour, minute)
                return int(dt.timestamp())

        # 5. "X点" / "X点半" (今天)
        m = re.search(r'(\d{1,2}|' + '|'.join(self.CN_DIGITS.keys()) + r')\s*点\s*(半|(\d{1,2})\s*分?)?', text)
        if m:
            hour = self._parse_number(m.group(1))
            minute = 0
            if m.group(2) == '半':
                minute = 30
            elif m.group(3):
                minute = int(m.group(3))
            if hour is not None and 0 <= hour <= 23:
                candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if candidate.timestamp() <= now_ts:
                    candidate += timedelta(days=1)
                return int(candidate.timestamp())

        return None

    def _extract_time(self, text: str) -> tuple:
        """从文本中提取 [时段] + 时间"""
        hour, minute = None, None

        # 上午/下午 判断
        is_pm = False
        is_am = False
        if '下午' in text or '傍晚' in text or '晚上' in text:
            is_pm = True
        elif '上午' in text or '早上' in text or '早晨' in text:
            is_am = True

        # "X点[半/Y分]"
        m = re.search(r'(\d{1,2}|' + '|'.join(self.CN_DIGITS.keys()) + r')\s*点\s*(半|(\d{1,2})\s*分?)?', text)
        if m:
            hour = self._parse_number(m.group(1))
            if m.group(2) == '半':
                minute = 30
            elif m.group(3):
                minute = int(m.group(3))
            else:
                minute = 0

            if hour is not None:
                if is_pm and hour < 12:
                    hour += 12
                elif is_am and hour == 12:
                    hour = 0

        # "HH:MM" 格式
        if hour is None:
            m = re.search(r'(\d{1,2}):(\d{2})', text)
            if m:
                hour = int(m.group(1))
                minute = int(m.group(2))

        return hour, minute

    def _parse_number(self, s: str) -> Optional[int]:
        """解析阿拉伯数字或中文数字"""
        if not s:
            return None
        s = s.strip()
        if s.isdigit():
            return int(s)
        return self.CN_DIGITS.get(s)


# ═══════════════════════════════════════════════════════
# 内置条件函数
# ═══════════════════════════════════════════════════════

def has_time_expression(event: dict) -> bool:
    """记忆中包含时间表达式（可能需要设提醒）"""
    content = event.get("memory", {}).get("content", "") or ""
    # 匹配时间关键词
    time_patterns = [
        r'明天|后天|大后天',
        r'\d+\s*(天|周|个月|小时|分钟)后',
        r'下周\s?[一二三四五六日天]',
        r'\d{1,2}\s*点',
        r'(上午|下午|晚上|今晚|明早|早晨|傍晚)\s*\d{1,2}',
        r'\d{4}-\d{1,2}-\d{1,2}\s*\d{1,2}:\d{2}',
        r'会议|开会|deadline|截止|到期|提醒',
    ]
    return any(re.search(p, content) for p in time_patterns)


def is_high_importance(event: dict) -> bool:
    """高重要度记忆"""
    return event.get("memory", {}).get("importance") == "high"


def is_contradiction_event(event: dict) -> bool:
    """矛盾事件"""
    return event.get("event_type") == "on_contradiction"


def is_decay_review_event(event: dict) -> bool:
    """衰减审查事件"""
    return event.get("event_type") == "on_decay_review"


def is_decision_complete_event(event: dict) -> bool:
    """决策链条完整事件"""
    return event.get("event_type") == "on_decision_complete"


def always_true(event: dict) -> bool:
    """始终触发"""
    return True


# ═══════════════════════════════════════════════════════
# 内置动作函数
# ═══════════════════════════════════════════════════════

def action_set_reminder(event: dict, store) -> ActionResult:
    """
    从记忆内容中解析时间，自动创建提醒任务。
    """
    memory = event.get("memory", {})
    content = memory.get("content", "")
    memory_id = memory.get("memory_id", "")

    parser = TimeParser()
    deadline_ts = parser.parse(content)

    if deadline_ts is None:
        return ActionResult(
            action_name="set_reminder",
            success=False,
            message="未找到明确的时间表达式",
        )

    # 提取提醒标题：取前 50 字符
    title = f"⏰ 提醒: {content[:50].strip()}"
    if len(content) > 50:
        title += "..."

    # 检查是否已有相同提醒（防重复）
    existing = store.get_tasks(status="pending", limit=100)
    for task in existing:
        if task.get("memory_id") == memory_id and task.get("deadline") == deadline_ts:
            return ActionResult(
                action_name="set_reminder",
                success=False,
                message="相同提醒已存在",
                data={"task_id": task["task_id"]},
            )

    task_id = store.add_task(
        memory_id=memory_id,
        title=title,
        assignee="ai",
        deadline=deadline_ts,
        topic_code=None,
    )

    dt_str = datetime.fromtimestamp(deadline_ts).strftime("%m-%d %H:%M")
    logger.info(f"⏰ 自动提醒已创建: {task_id} @ {dt_str} — {title}")

    return ActionResult(
        action_name="set_reminder",
        success=True,
        message=f"已设提醒 {dt_str}",
        data={"task_id": task_id, "deadline": deadline_ts, "title": title},
    )


def action_notify_contradiction(event: dict, store) -> ActionResult:
    """
    生成矛盾确认通知。
    将通知写入 tasks 表（status=pending），Agent 可在下次对话时检查。
    """
    ctx = event.get("context", {})
    mem_a = ctx.get("memory_a", {})
    mem_b = ctx.get("memory_b", {})
    score = ctx.get("contradiction_score", 0)

    content_a = (mem_a.get("content") or "")[:80]
    content_b = (mem_b.get("content") or "")[:80]

    title = (
        f"⚡ 记忆矛盾 (score={score:.0%})\n"
        f"  A: {content_a}\n"
        f"  B: {content_b}\n"
        f"  → 需要你确认哪个是对的"
    )

    memory_id = mem_a.get("memory_id", "")

    # 检查是否已有相同矛盾通知
    existing = store.get_tasks(status="pending", limit=100)
    for task in existing:
        if "矛盾" in task.get("title", "") and memory_id in task.get("title", ""):
            return ActionResult(
                action_name="notify_contradiction",
                success=False,
                message="矛盾通知已存在",
            )

    task_id = store.add_task(
        memory_id=memory_id,
        title=title[:200],
        assignee="user",  # 需要用户确认
    )

    logger.info(f"⚡ 矛盾通知已创建: {task_id}")

    return ActionResult(
        action_name="notify_contradiction",
        success=True,
        message="矛盾确认任务已创建",
        data={"task_id": task_id},
    )


def action_notify_decay_review(event: dict, store) -> ActionResult:
    """
    衰减到期通知：问用户"这件事还 relevant 吗？"
    """
    memory = event.get("memory", {})
    ctx = event.get("context", {})
    content = (memory.get("content") or "")[:80]
    age_days = ctx.get("age_days", 0)
    decay_status = ctx.get("decay_status", "review")

    title = f"📅 记忆审查 ({age_days:.0f}天): {content}... → 还 relevant 吗？"

    memory_id = memory.get("memory_id", "")

    # 防重复
    existing = store.get_tasks(status="pending", limit=100)
    for task in existing:
        if "记忆审查" in task.get("title", "") and memory_id in task.get("memory_content", ""):
            return ActionResult(
                action_name="notify_decay_review",
                success=False,
                message="审查通知已存在",
            )

    task_id = store.add_task(
        memory_id=memory_id,
        title=title[:200],
        assignee="user",
    )

    logger.info(f"📅 衰减审查通知: {task_id}")

    return ActionResult(
        action_name="notify_decay_review",
        success=True,
        message="衰减审查任务已创建",
        data={"task_id": task_id, "age_days": age_days},
    )


def action_generate_decision_doc(event: dict, store) -> ActionResult:
    """
    决策链条完整时，自动生成决策文档摘要。
    写入一条新的聚合记忆（nature=decision）。
    """
    memory = event.get("memory", {})
    ctx = event.get("context", {})
    chain = ctx.get("causal_chain", {})

    root_id = chain.get("root", "")
    caused_by = chain.get("caused_by", [])
    led_to = chain.get("led_to", [])

    # 构建决策文档
    parts = ["## 决策摘要\n"]

    # 前因
    if caused_by:
        parts.append("### 依据")
        for m in caused_by[:5]:
            content = (m.get("content") or "")[:100]
            icon = m.get("_causal_icon", "→")
            parts.append(f"  {icon} {content}")

    # 结论
    root_mem = store.get_memory(root_id)
    if root_mem:
        parts.append(f"\n### 结论\n  {(root_mem.get('content') or '')[:200]}")

    # 后果
    if led_to:
        parts.append("\n### 影响")
        for m in led_to[:5]:
            content = (m.get("content") or "")[:100]
            icon = m.get("_causal_icon", "→")
            parts.append(f"  {icon} {content}")

    doc_content = "\n".join(parts)

    logger.info(f"📄 决策文档已生成 ({len(led_to + caused_by)} 条关联)")

    return ActionResult(
        action_name="generate_decision_doc",
        success=True,
        message="决策文档已生成",
        data={"doc": doc_content, "root_id": root_id},
    )


# ═══════════════════════════════════════════════════════
# Layer 3: LLM 异步因果提取
# ═══════════════════════════════════════════════════════

_CAUSAL_LLM_PROMPT = """分析以下记忆内容，提取因果关系。

当前记忆: {content}
性质: {nature_id}
主题: {topics}

近期记忆上下文（按时间排序）:
{recent_context}

任务：判断当前记忆与近期记忆之间是否存在因果关系。

如果有，返回 JSON 数组（每条一个因果对）：
[{{"source_id": "原因记忆ID", "target_id": "结果记忆ID", "type": "decision_based_on|led_to|supports", "explanation": "简短解释"}}]

如果没有因果关系，返回空数组: []

只返回 JSON，不要解释。"""


def is_high_importance_causal(event: dict) -> bool:
    """高重要度记忆 → 触发 LLM 因果提取"""
    mem = event.get("memory", {})
    return mem.get("importance") == "high"


def action_llm_causal_extract(event: dict, store) -> ActionResult:
    """
    Layer 3: 对高重要度记忆调用 LLM 提取因果关系。

    在 reactor 的 on_write 事件中异步执行，不阻塞写入管道。
    需要通过 MemoryReactor.set_llm_fn() 注入 LLM 函数。
    """
    memory = event.get("memory", {})
    content = memory.get("content", "")
    memory_id = memory.get("memory_id", "")
    nature_id = memory.get("nature_id", "")
    topics = memory.get("topics", [])

    # 获取 LLM 函数（从 event context 中传入）
    llm_fn = event.get("llm_fn")
    if not llm_fn:
        return ActionResult(
            action_name="llm_causal_extract",
            success=False,
            message="LLM 函数未配置，跳过因果提取",
        )

    # 获取近期记忆作为上下文（最近 20 条）
    recent = store.query(limit=20)
    recent = [m for m in recent if m.get("memory_id") != memory_id]

    # 构建上下文摘要
    ctx_lines = []
    for m in recent[:10]:
        mid = m.get("memory_id", "")[:16]
        c = (m.get("content") or "")[:60]
        ctx_lines.append(f"  [{mid}] {c}")
    recent_ctx = "\n".join(ctx_lines) if ctx_lines else "  (无近期记忆)"

    prompt = _CAUSAL_LLM_PROMPT.format(
        content=content[:200],
        nature_id=nature_id,
        topics=", ".join(topics) if isinstance(topics, list) else str(topics),
        recent_context=recent_ctx,
    )

    try:
        response = llm_fn(prompt)
        # 解析 JSON
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]
        causal_pairs = json.loads(cleaned.strip())

        if not isinstance(causal_pairs, list):
            causal_pairs = []

        created = 0
        for pair in causal_pairs:
            src = pair.get("source_id", "")
            tgt = pair.get("target_id", "")
            link_type = pair.get("type", "led_to")
            explanation = pair.get("explanation", "LLM 因果提取")

            # 验证记忆 ID 存在
            if src and tgt and store.get_memory(src) and store.get_memory(tgt):
                if link_type in ("decision_based_on", "led_to", "supports"):
                    store.insert_link(
                        source_id=src,
                        target_id=tgt,
                        link_type=f"causal.{link_type}",
                        weight=0.85,
                        reason=f"LLM 提取: {explanation}",
                    )
                    created += 1

        logger.info(f"🧠 LLM 因果提取: {created} 条 (from {len(causal_pairs)} candidates)")
        return ActionResult(
            action_name="llm_causal_extract",
            success=True,
            message=f"提取了 {created} 条因果关系",
            data={"created": created, "candidates": len(causal_pairs)},
        )

    except (json.JSONDecodeError, Exception) as e:
        logger.debug(f"LLM 因果提取失败: {e}")
        return ActionResult(
            action_name="llm_causal_extract",
            success=False,
            message=f"解析失败: {e}",
        )


# ═══════════════════════════════════════════════════════
# MemoryReactor 主类
# ═══════════════════════════════════════════════════════

class MemoryReactor:
    """
    记忆驱动的主动 Agent 反应器。

    扫描记忆系统的状态变化，触发预定义的 hook，执行对应动作。

    用法:
        reactor = MemoryReactor()
        reactor.register_default_hooks()

        # 写入时触发
        reactor.fire_write(memory_dict, store)

        # 定期扫描（在 maintain() 中调用）
        results = reactor.scan(store, decay, self_healing, causal)
    """

    def __init__(self):
        self._hooks: dict[str, list[Hook]] = {}
        self._fired_hashes: set[str] = set()  # 防重复触发
        self._llm_fn = None  # LLM 函数（Layer 3 因果提取用）
        self._stats = {
            "events_scanned": 0,
            "hooks_fired": 0,
            "actions_succeeded": 0,
            "actions_failed": 0,
        }

    def set_llm_fn(self, llm_fn):
        """设置 LLM 函数，启用 Layer 3 异步因果提取"""
        self._llm_fn = llm_fn

    # ── Hook 注册 ────────────────────────────────────────

    def register_hook(
        self,
        event_type: str,
        condition: Callable[[dict], bool],
        action: Callable[[dict, object], ActionResult],
        name: str = None,
        priority: int = 0,
    ):
        """注册一个事件钩子"""
        if event_type not in self._hooks:
            self._hooks[event_type] = []

        hook = Hook(
            name=name or f"{event_type}:{action.__name__}",
            condition=condition,
            action=action,
            priority=priority,
        )
        self._hooks[event_type].append(hook)
        self._hooks[event_type].sort(key=lambda h: -h.priority)
        logger.debug(f"Hook registered: {hook.name} on {event_type}")

    def register_default_hooks(self):
        """注册默认钩子集合"""
        # on_write: 时间表达式 → 自动设提醒
        self.register_hook(
            "on_write",
            condition=has_time_expression,
            action=action_set_reminder,
            name="auto_reminder",
            priority=10,
        )

        # on_contradiction: 矛盾 → 通知用户
        self.register_hook(
            "on_contradiction",
            condition=is_contradiction_event,
            action=action_notify_contradiction,
            name="contradiction_notify",
            priority=10,
        )

        # on_decay_review: 衰减到期 → 问用户
        self.register_hook(
            "on_decay_review",
            condition=is_decay_review_event,
            action=action_notify_decay_review,
            name="decay_review_notify",
            priority=10,
        )

        # on_decision_complete: 决策链完整 → 生成文档
        self.register_hook(
            "on_decision_complete",
            condition=is_decision_complete_event,
            action=action_generate_decision_doc,
            name="decision_doc",
            priority=10,
        )

        # on_write (Layer 3): 高重要度记忆 → LLM 异步因果提取
        self.register_hook(
            "on_write",
            condition=is_high_importance_causal,
            action=action_llm_causal_extract,
            name="llm_causal_extract",
            priority=5,  # 低于 auto_reminder
        )

        logger.info("✅ 默认 hooks 已注册: auto_reminder, contradiction_notify, decay_review_notify, decision_doc, llm_causal_extract")

    # ── 事件触发 ─────────────────────────────────────────

    def _event_hash(self, event: Event) -> str:
        """生成事件指纹，防止重复触发"""
        raw = f"{event.event_type}:{event.memory.get('memory_id', '')}:{json.dumps(event.context, sort_keys=True, default=str)}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def fire(self, event: Event, store) -> list[ActionResult]:
        """
        触发一个事件，匹配所有 hooks 并执行动作。

        返回: 执行结果列表
        """
        # Security: require explicit opt-in for auto-execution of hook actions
        import os as _os
        auto_execute = _os.environ.get("REACTOR_AUTO_EXECUTE", "").lower() in ("1", "true", "yes")

        results = []
        hooks = self._hooks.get(event.event_type, [])

        if not hooks:
            return results

        # 防重复
        evt_hash = self._event_hash(event)
        if evt_hash in self._fired_hashes:
            logger.debug(f"事件已触发过，跳过: {event.event_type} {evt_hash}")
            return results
        self._fired_hashes.add(evt_hash)

        # 限制 fired_hashes 集合大小
        if len(self._fired_hashes) > 10000:
            # 保留最近的 5000 条
            self._fired_hashes = set(list(self._fired_hashes)[-5000:])

        event_ctx = {
            "event_type": event.event_type,
            "memory": event.memory,
            **event.context,
        }

        for hook in hooks:
            if not hook.enabled:
                continue

            self._stats["events_scanned"] += 1

            try:
                if hook.condition(event_ctx):
                    self._stats["hooks_fired"] += 1
                    if not auto_execute:
                        logger.info("Reactor: hook '%s' matched but auto-execute disabled (set REACTOR_AUTO_EXECUTE=true)", hook.name)
                        continue
                    result = hook.action(event_ctx, store)
                    results.append(result)

                    if result.success:
                        self._stats["actions_succeeded"] += 1
                    else:
                        self._stats["actions_failed"] += 1

                    logger.debug(f"Hook fired: {hook.name} → {result.message}")
            except Exception as e:
                logger.warning("reactor: %s", e)
                self._stats["actions_failed"] += 1
                results.append(ActionResult(
                    action_name=hook.name,
                    success=False,
                    message=str(e),
                ))

        return results

    def fire_write(self, memory: dict, store) -> list[ActionResult]:
        """快捷方法：触发 on_write 事件"""
        ctx = {}
        if self._llm_fn:
            ctx["llm_fn"] = self._llm_fn
        event = Event(event_type="on_write", memory=memory, context=ctx)
        return self.fire(event, store)

    # ── 扫描阶段 ─────────────────────────────────────────

    def scan_contradictions(self, self_healing, store) -> list[ActionResult]:
        """扫描矛盾记忆并触发 on_contradiction"""
        results = []
        try:
            contradictions = self_healing.detect_contradictions()
            for c in contradictions:
                mem_a = store.get_memory(c.get("memory_a", ""))
                mem_b = store.get_memory(c.get("memory_b", ""))
                if mem_a and mem_b:
                    event = Event(
                        event_type="on_contradiction",
                        memory=mem_a,
                        context={
                            "memory_a": dict(mem_a),
                            "memory_b": dict(mem_b),
                            "contradiction_score": c.get("contradiction_score", 0),
                            "shared_topics": c.get("shared_topics", []),
                        },
                    )
                    results.extend(self.fire(event, store))
        except Exception as e:
            logger.warning("reactor: %s", e)
        return results

    def scan_decay(self, decay_analyzer, store) -> list[ActionResult]:
        """扫描衰减到期记忆并触发 on_decay_review"""
        results = []
        try:
            analysis = decay_analyzer.analyze_all()
            needs_action = analysis.get("needs_action", [])
            for item in needs_action:
                if item.get("status") not in ("review", "decay"):
                    continue
                memory = store.get_memory(item["memory_id"])
                if memory:
                    event = Event(
                        event_type="on_decay_review",
                        memory=dict(memory),
                        context={
                            "age_days": item.get("age_days", 0),
                            "decay_score": item.get("decay_score", 0),
                            "decay_status": item.get("status", ""),
                        },
                    )
                    results.extend(self.fire(event, store))
        except Exception as e:
            logger.warning("reactor: %s", e)
        return results

    def scan_causal_chains(self, causal_chain, store) -> list[ActionResult]:
        """
        扫描完整的决策链条并触发 on_decision_complete。

        完整链条 = 有 explore/ask (D04/D12) → decision (D03) → output (D06) 的因果路径
        """
        results = []
        try:
            # 查找所有决策型记忆（nature=D03）
            memories = store.query(limit=200)
            decisions = [m for m in memories if m.get("nature_id") == "D03"]

            for decision in decisions:
                mid = decision["memory_id"]
                chain = causal_chain.get_causal_chain(mid, max_depth=3)

                caused_by = chain.get("caused_by", [])
                led_to = chain.get("led_to", [])

                # 判断链条完整性：有前因 + 有后果 = 完整决策链
                has_explore = any(
                    m.get("nature_id") in ("D04", "D12")
                    for m in caused_by
                )
                has_outcome = len(led_to) > 0

                if has_explore and has_outcome:
                    event = Event(
                        event_type="on_decision_complete",
                        memory=decision,
                        context={"causal_chain": chain},
                    )
                    results.extend(self.fire(event, store))
        except Exception as e:
            logger.warning("reactor: %s", e)
        return results

    # ── 统一扫描入口 ─────────────────────────────────────

    def scan(self, store, decay=None, self_healing=None, causal=None) -> dict:
        """
        一站式扫描：触发所有定期检测事件。

        在 maintain() 中调用此方法。

        返回: {
            "contradictions": [ActionResult, ...],
            "decay_reviews": [ActionResult, ...],
            "decisions": [ActionResult, ...],
            "total_actions": int,
            "stats": dict,
        }
        """
        all_results = {
            "contradictions": [],
            "decay_reviews": [],
            "decisions": [],
        }

        if self_healing:
            all_results["contradictions"] = self.scan_contradictions(self_healing, store)

        if decay:
            all_results["decay_reviews"] = self.scan_decay(decay, store)

        if causal:
            all_results["decisions"] = self.scan_causal_chains(causal, store)

        total = sum(len(v) for v in all_results.values())
        all_results["total_actions"] = total
        all_results["stats"] = self.get_stats()

        if total > 0:
            logger.info(f"🔔 Reactor 扫描完成: {total} 个动作触发")

        return all_results

    # ── 查询接口 ─────────────────────────────────────────

    def get_pending_notifications(self, store) -> list[dict]:
        """
        获取待处理的通知（由 reactor 创建的 tasks）。
        Agent 可在对话开始时调用此方法检查是否有待处理事项。
        包含：用户确认类通知 + Agent 提醒类任务。
        """
        # 用户确认类（矛盾/衰减审查）
        user_tasks = store.get_tasks(status="pending", assignee="user", limit=20)
        # Agent 提醒类（时间提醒）
        ai_tasks = store.get_tasks(status="pending", assignee="ai", limit=20)
        all_tasks = user_tasks + ai_tasks

        # 只返回 reactor 创建的任务（标题包含 ⚡/📅/⏰/📄 标记）
        reactor_tasks = []
        seen_ids = set()
        for t in all_tasks:
            tid = t.get("task_id", "")
            if tid in seen_ids:
                continue
            if any(marker in t.get("title", "") for marker in ("⚡", "📅", "⏰", "📄")):
                reactor_tasks.append(t)
                seen_ids.add(tid)

        # 按 deadline 排序（最近的排前面）
        reactor_tasks.sort(key=lambda t: t.get("deadline") or 0)
        return reactor_tasks

    def get_stats(self) -> dict:
        """返回统计信息"""
        return dict(self._stats)

    def reset_fired_cache(self):
        """重置触发缓存（测试用）"""
        self._fired_hashes.clear()
