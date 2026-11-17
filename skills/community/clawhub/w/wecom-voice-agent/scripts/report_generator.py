#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_generator.py — 运营报表（v2.8）

功能：
1. 核心指标聚合：总通话、外呼接通率、平均时长、录音覆盖率
2. 通话时长分布：0-30秒 / 30-60秒 / 1-3分钟 / 3分钟以上
3. 意图分布：Top 10 意图 + 其他聚合（未识别意图单列）
4. 外呼四级漏斗：调度发起 → 振铃接通 → 有效通话（≥30秒）→ 待办跟进
5. 待办跟进统计：新增、已完成、逾期（pending/reminded 且已过截止日）
6. 周一 HTML 周报：上周一至上周日完整周期，自包含单文件，可直接转发

数据来源（全部本地，零外部依赖）：
- ~/.wecom_voice/call_records.db  通话记录（call_records 表）
- ~/.wecom_voice/todos.db         跟进待办（todos 表）
- <skill>/temp_scheduler/tasks.json  外呼调度任务（漏斗第一级）

指标口径：
- 振铃接通：direction='outbound' 且 duration_seconds > 0
- 有效通话：已接通且 duration_seconds >= 30 秒
- 待办跟进：统计周期内新建的待办条数（漏斗末级，衡量通话转化）

降级策略（规则 9）：
- 任一数据源缺失或不可读 → 对应指标置零并记入 warnings，不阻断其他指标
- 不主动创建数据库文件，仅只读查询
- HTML 报表在数据源缺失时展示警告横幅，内容仍可正常打开

依赖：纯 Python 标准库（sqlite3 + json + html + datetime）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-09-20)
"""

import os
import json
import html
import sqlite3
import logging
from datetime import datetime, timedelta, time as dtime
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

# ==========================================
# 配置
# ==========================================

CALLS_DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "call_records.db")
TODOS_DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "todos.db")
TASKS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "temp_scheduler", "tasks.json"
)
REPORT_DIR = os.path.join(os.path.expanduser("~"), ".wecom_voice", "reports")

# 有效通话时长下限（秒）
EFFECTIVE_MIN_SECONDS = 30

# 意图分布展示上限（超出聚合为「其他」）
TOP_INTENTS = 10

# 时长分布桶（秒）：[下限, 上限, 标签]
DURATION_BUCKETS = [
    (0, 30, "0-30秒"),
    (30, 60, "30-60秒"),
    (60, 180, "1-3分钟"),
    (180, float("inf"), "3分钟以上"),
]

# 外呼漏斗层级定义
FUNNEL_STAGES = [
    ("scheduled", "调度发起"),
    ("connected", "振铃接通"),
    ("effective", "有效通话"),
    ("todos", "待办跟进"),
]


# ==========================================
# 周期工具
# ==========================================

def _fmt(dt: datetime) -> str:
    """格式化为 SQL 比较用的 'YYYY-MM-DD HH:MM:SS'"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _parse_ts(value: str) -> Optional[datetime]:
    """宽容解析 ISO / 'YYYY-MM-DD HH:MM:SS' 时间串"""
    if not value or not isinstance(value, str):
        return None
    text = value.strip().replace("T", " ")[:19]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


# ==========================================
# 运营报表生成器
# ==========================================

class ReportGenerator:
    """
    运营报表生成器

    使用方式：
        gen = ReportGenerator()
        start, end = ReportGenerator.last_week_range()
        report = gen.collect(start, end)
        html_path = gen.export_html(report)          # 周一 HTML 周报
        print(gen.render_text(report))               # 控制台摘要
    """

    def __init__(self, calls_db: str = CALLS_DB_PATH, todos_db: str = TODOS_DB_PATH,
                 tasks_file: str = TASKS_FILE, report_dir: str = REPORT_DIR):
        self.calls_db = calls_db
        self.todos_db = todos_db
        self.tasks_file = tasks_file
        self.report_dir = report_dir
        self.warnings: List[str] = []

    # ---------- 周期计算 ----------

    @staticmethod
    def last_week_range(now: Optional[datetime] = None) -> Tuple[datetime, datetime]:
        """
        上一个完整自然周（周一 00:00:00 ~ 周日 23:59:59）

        周一运行本函数即得到「上周」周期，用于周一 HTML 周报。
        """
        now = now or datetime.now()
        today = now.date()
        this_monday = today - timedelta(days=today.weekday())
        last_monday = this_monday - timedelta(days=7)
        last_sunday = this_monday - timedelta(days=1)
        return (datetime.combine(last_monday, dtime(0, 0, 0)),
                datetime.combine(last_sunday, dtime(23, 59, 59)))

    @staticmethod
    def last_n_days_range(n: int = 7, now: Optional[datetime] = None) -> Tuple[datetime, datetime]:
        """最近 n 天（含今天）"""
        now = now or datetime.now()
        start = datetime.combine((now - timedelta(days=n - 1)).date(), dtime(0, 0, 0))
        return start, now

    @staticmethod
    def month_range(now: Optional[datetime] = None) -> Tuple[datetime, datetime]:
        """本月 1 号至今"""
        now = now or datetime.now()
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start, now

    # ---------- 数据采集（只读，失败隔离） ----------

    def _query_calls(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """读取周期内通话记录；数据源缺失/异常时返回空列表并记警告"""
        if not os.path.exists(self.calls_db):
            self.warnings.append(f"通话记录数据库不存在：{self.calls_db}")
            return []
        try:
            # 已做存在性检查，普通连接只执行 SELECT，不会创建文件
            with sqlite3.connect(self.calls_db) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """SELECT call_id, direction, start_time, duration_seconds,
                              intent, hangup_reason, has_recording
                       FROM call_records
                       WHERE substr(start_time, 1, 19) BETWEEN ? AND ?
                       ORDER BY start_time""",
                    (_fmt(start), _fmt(end))
                ).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            self.warnings.append(f"读取通话记录失败：{e}")
            logger.warning(f"读取通话记录失败（不影响其他指标）: {e}")
            return []

    def _query_todos(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """读取周期内新建待办；数据源缺失/异常时返回空列表并记警告"""
        if not os.path.exists(self.todos_db):
            self.warnings.append(f"待办数据库不存在：{self.todos_db}")
            return []
        try:
            # 已做存在性检查，普通连接只执行 SELECT，不会创建文件
            with sqlite3.connect(self.todos_db) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """SELECT todo_id, call_id, userid, content, responsible_person,
                              due_date, status, created_at
                       FROM todos
                       WHERE substr(replace(created_at, 'T', ' '), 1, 19) BETWEEN ? AND ?
                       ORDER BY created_at""",
                    (_fmt(start), _fmt(end))
                ).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            self.warnings.append(f"读取待办数据失败：{e}")
            logger.warning(f"读取待办数据失败（不影响其他指标）: {e}")
            return []

    def _load_tasks(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """
        读取周期内外呼调度任务（漏斗第一级）

        时间口径：优先 executed_at（实际执行），缺失时取 scheduled_time，再退 created_at。
        文件缺失/解析失败时返回空列表并记警告（漏斗第一级降级为外呼记录数）。
        """
        if not os.path.exists(self.tasks_file):
            self.warnings.append(f"调度任务文件不存在：{self.tasks_file}")
            return []
        try:
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.warnings.append(f"读取调度任务失败：{e}")
            logger.warning(f"读取调度任务失败（不影响其他指标）: {e}")
            return []

        tasks = data if isinstance(data, list) else data.get("tasks", [])
        result = []
        for t in tasks:
            if not isinstance(t, dict):
                continue
            ts = (_parse_ts(t.get("executed_at") or "")
                  or _parse_ts(t.get("scheduled_time") or "")
                  or _parse_ts(t.get("created_at") or ""))
            if ts and start <= ts <= end:
                result.append(t)
        return result

    # ---------- 指标计算 ----------

    def _overview(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """核心指标：总量 / 方向 / 接通 / 时长 / 录音覆盖"""
        total = len(rows)
        outbound = [r for r in rows if r.get("direction") == "outbound"]
        inbound = [r for r in rows if r.get("direction") == "inbound"]
        durations = [float(r.get("duration_seconds") or 0) for r in rows]

        out_connected = sum(1 for r in outbound if float(r.get("duration_seconds") or 0) > 0)
        all_connected = sum(1 for d in durations if d > 0)
        recorded = sum(1 for r in rows if r.get("has_recording"))
        total_duration = sum(durations)

        return {
            "total_calls": total,
            "outbound_calls": len(outbound),
            "inbound_calls": len(inbound),
            "unanswered_calls": total - all_connected,
            "outbound_connected": out_connected,
            "outbound_connect_rate": round(out_connected / len(outbound), 4) if outbound else 0.0,
            "overall_answer_rate": round(all_connected / total, 4) if total else 0.0,
            "total_duration_seconds": int(total_duration),
            "avg_duration_seconds": round(total_duration / total, 1) if total else 0.0,
            "recording_rate": round(recorded / total, 4) if total else 0.0,
        }

    def _duration_buckets(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """时长分布（所有通话，含未接通 0 秒档）"""
        counts = [0] * len(DURATION_BUCKETS)
        for r in rows:
            d = float(r.get("duration_seconds") or 0)
            for i, (lo, hi, _label) in enumerate(DURATION_BUCKETS):
                if lo <= d < hi:
                    counts[i] += 1
                    break
        total = len(rows) or 1
        return [
            {"label": label, "count": cnt, "ratio": round(cnt / total, 4)}
            for cnt, (lo, hi, label) in zip(counts, DURATION_BUCKETS)
        ]

    def _intent_distribution(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """意图分布 Top N + 其他聚合；未识别意图单列"""
        counter: Dict[str, int] = {}
        for r in rows:
            intent = (r.get("intent") or "").strip() or "(未识别)"
            counter[intent] = counter.get(intent, 0) + 1
        ordered = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
        top = ordered[:TOP_INTENTS]
        rest = ordered[TOP_INTENTS:]
        result = [{"intent": k, "count": v} for k, v in top]
        if rest:
            result.append({"intent": "其他", "count": sum(v for _, v in rest)})
        return result

    def _funnel(self, tasks: List[Dict[str, Any]], rows: List[Dict[str, Any]],
                todo_count: int) -> List[Dict[str, Any]]:
        """
        外呼四级漏斗：调度发起 → 振铃接通 → 有效通话 → 待办跟进

        调度任务文件缺失时，第一级降级为周期内外呼记录数。
        """
        outbound = [r for r in rows if r.get("direction") == "outbound"]
        connected = [r for r in outbound if float(r.get("duration_seconds") or 0) > 0]
        effective = [r for r in connected
                     if float(r.get("duration_seconds") or 0) >= EFFECTIVE_MIN_SECONDS]

        counts = {
            "scheduled": len(tasks) if tasks else len(outbound),
            "connected": len(connected),
            "effective": len(effective),
            "todos": todo_count,
        }
        degraded_first_stage = not tasks and bool(outbound)

        stages = []
        prev = None
        for key, label in FUNNEL_STAGES:
            cnt = counts[key]
            conversion = round(cnt / prev, 4) if prev else None
            stages.append({
                "key": key, "label": label, "count": cnt,
                "conversion_from_prev": conversion,
            })
            prev = cnt
        return stages, degraded_first_stage

    def _todo_stats(self, todos: List[Dict[str, Any]], now: Optional[datetime] = None) -> Dict[str, Any]:
        """待办统计：新增 / 已完成 / 逾期 / 状态分布"""
        now = now or datetime.now()
        by_status: Dict[str, int] = {}
        overdue = 0
        for t in todos:
            status = (t.get("status") or "").strip() or "unknown"
            by_status[status] = by_status.get(status, 0) + 1
            due = _parse_ts(t.get("due_date") or "")
            if due and due < now and status in ("pending", "reminded"):
                overdue += 1
        return {
            "new_todos": len(todos),
            "closed_todos": by_status.get("closed", 0),
            "overdue_todos": overdue,
            "by_status": by_status,
        }

    def _daily_trend(self, rows: List[Dict[str, Any]], start: datetime,
                     end: datetime) -> List[Dict[str, Any]]:
        """每日趋势（按 start_time 日期分组，补零空白天）"""
        counter: Dict[str, int] = {}
        for r in rows:
            day = (r.get("start_time") or "")[:10]
            if day:
                counter[day] = counter.get(day, 0) + 1
        trend = []
        day = start.date()
        last = end.date()
        while day <= last:
            key = day.strftime("%Y-%m-%d")
            trend.append({"date": key, "calls": counter.get(key, 0)})
            day += timedelta(days=1)
        return trend

    # ---------- 主入口 ----------

    def collect(self, start: datetime, end: datetime) -> Dict[str, Any]:
        """
        采集周期内全量运营指标

        Returns:
            报表 dict（含 overview / duration_buckets / intents / funnel /
            todo_stats / daily_trend / warnings / period 等字段）
        """
        self.warnings = []
        rows = self._query_calls(start, end)
        todos = self._query_todos(start, end)
        tasks = self._load_tasks(start, end)

        funnel, degraded_stage = self._funnel(tasks, rows, len(todos))
        if degraded_stage:
            self.warnings.append("调度任务文件缺失，漏斗第一级已降级为外呼记录数。")

        report = {
            "period": {"start": _fmt(start), "end": _fmt(end),
                       "days": (end.date() - start.date()).days + 1},
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "overview": self._overview(rows),
            "duration_buckets": self._duration_buckets(rows),
            "intents": self._intent_distribution(rows),
            "funnel": funnel,
            "todo_stats": self._todo_stats(todos),
            "daily_trend": self._daily_trend(rows, start, end),
            "warnings": list(self.warnings),
            "data_available": bool(rows),
        }
        return report

    # ---------- 渲染：控制台文本 ----------

    def render_text(self, report: Dict[str, Any]) -> str:
        """渲染为控制台摘要文本"""
        ov = report["overview"]
        period = report["period"]
        lines = [
            "",
            "=" * 60,
            f"运营报表（{period['start']} ~ {period['end']}）",
            "=" * 60,
            f"总通话: {ov['total_calls']} 次（外呼 {ov['outbound_calls']} / 来电 {ov['inbound_calls']}）",
            f"外呼接通率: {ov['outbound_connect_rate'] * 100:.1f}%"
            f"（{ov['outbound_connected']}/{ov['outbound_calls']}）",
            f"平均时长: {ov['avg_duration_seconds']:.1f} 秒    录音覆盖率: {ov['recording_rate'] * 100:.1f}%",
            "",
            "外呼漏斗:",
        ]
        for st in report["funnel"]:
            conv = f"  转化率 {st['conversion_from_prev'] * 100:.1f}%" if st["conversion_from_prev"] is not None else ""
            lines.append(f"  {st['label']}: {st['count']}{conv}")

        lines.append("")
        lines.append("时长分布:")
        for b in report["duration_buckets"]:
            bar = "█" * int(b["ratio"] * 20)
            lines.append(f"  {b['label']:>6}: {b['count']:>4} 次 │{bar}")

        lines.append("")
        lines.append("意图分布 Top 5:")
        for it in report["intents"][:5]:
            lines.append(f"  {it['intent']}: {it['count']} 次")

        ts = report["todo_stats"]
        lines.append("")
        lines.append(f"待办跟进: 新增 {ts['new_todos']} 条 / 已完成 {ts['closed_todos']} 条 / 逾期 {ts['overdue_todos']} 条")

        if report["warnings"]:
            lines.append("")
            lines.append("⚠ 数据源提示:")
            for w in report["warnings"]:
                lines.append(f"  - {w}")
        lines.append("=" * 60)
        return "\n".join(lines)

    # ---------- 渲染：HTML 周报 ----------

    def _bar(self, ratio: float) -> str:
        """生成 CSS 横向条形（宽度百分比）"""
        pct = max(0.0, min(1.0, ratio)) * 100
        return f'<div class="bar"><span style="width:{pct:.1f}%"></span></div>'

    def render_html(self, report: Dict[str, Any]) -> str:
        """渲染为自包含 HTML 周报（单文件，无外部依赖，可直接转发）"""
        ov = report["overview"]
        period = report["period"]
        esc = html.escape

        # KPI 卡片
        kpis = [
            ("总通话", f"{ov['total_calls']}", "次"),
            ("外呼接通率", f"{ov['outbound_connect_rate'] * 100:.1f}", "%"),
            ("平均时长", f"{ov['avg_duration_seconds']:.0f}", "秒"),
            ("待办生成", f"{report['todo_stats']['new_todos']}", "条"),
        ]
        kpi_html = "".join(
            f'<div class="kpi"><div class="kpi-value">{v}<small> {u}</small></div>'
            f'<div class="kpi-label">{esc(k)}</div></div>'
            for k, v, u in kpis
        )

        # 漏斗表
        funnel_rows = []
        max_count = max((s["count"] for s in report["funnel"]), default=0) or 1
        for st in report["funnel"]:
            conv = (f"{st['conversion_from_prev'] * 100:.1f}%"
                    if st["conversion_from_prev"] is not None else "—")
            funnel_rows.append(
                f'<tr><td>{esc(st["label"])}</td><td class="num">{st["count"]}</td>'
                f'<td class="num">{conv}</td><td>{self._bar(st["count"] / max_count)}</td></tr>'
            )
        funnel_html = "".join(funnel_rows)

        # 时长分布
        dur_html = "".join(
            f'<tr><td>{esc(b["label"])}</td><td class="num">{b["count"]}</td>'
            f'<td class="num">{b["ratio"] * 100:.1f}%</td>'
            f'<td>{self._bar(b["ratio"])}</td></tr>'
            for b in report["duration_buckets"]
        )

        # 意图分布
        intent_total = ov["total_calls"] or 1
        intent_html = "".join(
            f'<tr><td>{esc(it["intent"])}</td><td class="num">{it["count"]}</td>'
            f'<td class="num">{it["count"] / intent_total * 100:.1f}%</td></tr>'
            for it in report["intents"]
        ) or '<tr><td colspan="3" class="empty">暂无数据</td></tr>'

        # 每日趋势
        trend_max = max((d["calls"] for d in report["daily_trend"]), default=0) or 1
        trend_html = "".join(
            f'<tr><td>{esc(d["date"])}</td><td class="num">{d["calls"]}</td>'
            f'<td>{self._bar(d["calls"] / trend_max)}</td></tr>'
            for d in report["daily_trend"]
        )

        # 待办统计
        ts = report["todo_stats"]
        status_text = "、".join(f"{esc(k)} {v}" for k, v in ts["by_status"].items()) or "无"
        todo_html = (
            f'<tr><td>新增待办</td><td class="num">{ts["new_todos"]}</td></tr>'
            f'<tr><td>已完成</td><td class="num">{ts["closed_todos"]}</td></tr>'
            f'<tr><td>逾期未闭环</td><td class="num">{ts["overdue_todos"]}</td></tr>'
            f'<tr><td>状态分布</td><td>{status_text}</td></tr>'
        )

        # 数据源警告横幅
        warning_html = ""
        if report["warnings"]:
            items = "".join(f"<li>{esc(w)}</li>" for w in report["warnings"])
            warning_html = f'<div class="banner"><strong>数据源提示</strong><ul>{items}</ul></div>'

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>语音外呼运营周报（{esc(period['start'][:10])} ~ {esc(period['end'][:10])}）</title>
<style>
  body {{ margin: 0; background: #f3f5f9; color: #1f2937;
         font-family: "Microsoft YaHei", "PingFang SC", sans-serif; }}
  .report {{ max-width: 880px; margin: 24px auto; padding: 0 16px 32px; }}
  header {{ background: #2563eb; color: #fff; border-radius: 12px; padding: 24px 28px; }}
  header h1 {{ margin: 0 0 6px; font-size: 22px; }}
  header p {{ margin: 2px 0; font-size: 13px; opacity: .92; }}
  .banner {{ background: #fffbeb; border: 1px solid #f59e0b; color: #92400e;
             border-radius: 10px; padding: 12px 16px; margin: 16px 0; font-size: 13px; }}
  .banner ul {{ margin: 6px 0 0; padding-left: 18px; }}
  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; }}
  .kpi {{ background: #fff; border-radius: 10px; padding: 16px; text-align: center;
          box-shadow: 0 1px 3px rgba(15,23,42,.08); }}
  .kpi-value {{ font-size: 26px; font-weight: 700; color: #2563eb; }}
  .kpi-value small {{ font-size: 12px; color: #6b7280; font-weight: 400; }}
  .kpi-label {{ font-size: 12px; color: #6b7280; margin-top: 4px; }}
  section {{ background: #fff; border-radius: 10px; padding: 20px 24px; margin: 16px 0;
             box-shadow: 0 1px 3px rgba(15,23,42,.08); }}
  section h2 {{ margin: 0 0 12px; font-size: 16px; color: #0f172a;
                border-left: 4px solid #0d9488; padding-left: 8px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th, td {{ padding: 7px 10px; border-bottom: 1px solid #eef2f7; text-align: left; }}
  th {{ color: #6b7280; font-weight: 600; background: #f8fafc; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  td.empty {{ text-align: center; color: #9ca3af; }}
  .bar {{ background: #eef2f7; border-radius: 4px; height: 10px; width: 100%; overflow: hidden; }}
  .bar span {{ display: block; height: 100%; background: #0d9488; border-radius: 4px; }}
  footer {{ text-align: center; color: #9ca3af; font-size: 12px; margin-top: 20px; line-height: 1.8; }}
</style>
</head>
<body>
<div class="report">
  <header>
    <h1>语音外呼运营周报</h1>
    <p>统计周期：{esc(period['start'])} ~ {esc(period['end'])}（{period['days']} 天）</p>
    <p>生成时间：{esc(report['generated_at'])}</p>
  </header>
  {warning_html}
  <div class="kpis">{kpi_html}</div>
  <section>
    <h2>外呼四级漏斗</h2>
    <table>
      <tr><th>层级</th><th>数量</th><th>上一级转化率</th><th>分布</th></tr>
      {funnel_html}
    </table>
  </section>
  <section>
    <h2>通话时长分布</h2>
    <table>
      <tr><th>时长区间</th><th>次数</th><th>占比</th><th>分布</th></tr>
      {dur_html}
    </table>
  </section>
  <section>
    <h2>意图分布</h2>
    <table>
      <tr><th>意图</th><th>次数</th><th>占比</th></tr>
      {intent_html}
    </table>
  </section>
  <section>
    <h2>每日趋势</h2>
    <table>
      <tr><th>日期</th><th>通话次数</th><th>分布</th></tr>
      {trend_html}
    </table>
  </section>
  <section>
    <h2>待办跟进</h2>
    <table>{todo_html}</table>
  </section>
  <footer>
    由 wecom-voice-agent report_generator 自动生成 ｜ 数据来源于本地通话记录，仅限内部运营使用<br>
    问题与建议：njskills@agent.qq.com
  </footer>
</div>
</body>
</html>"""

    def export_html(self, report: Dict[str, Any], filepath: Optional[str] = None) -> str:
        """
        导出 HTML 周报

        Args:
            report: collect() 的返回值
            filepath: 输出路径（默认 ~/.wecom_voice/reports/weekly_report_<周期结束日>.html）

        Returns:
            实际写入的文件路径
        """
        if not filepath:
            period_end = report["period"]["end"][:10].replace("-", "")
            filepath = os.path.join(self.report_dir, f"weekly_report_{period_end}.html")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.render_html(report))
        logger.info(f"周报已导出: {filepath}")
        return filepath


# ==========================================
# 便捷函数
# ==========================================

_generator_instance: Optional[ReportGenerator] = None


def get_generator() -> ReportGenerator:
    """获取报表生成器单例"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = ReportGenerator()
    return _generator_instance


def generate_weekly_report(filepath: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
    """
    生成上周完整周 HTML 周报（周一部署定时任务时调用）

    Returns:
        (HTML 文件路径, 报表 dict)
    """
    gen = get_generator()
    start, end = ReportGenerator.last_week_range()
    report = gen.collect(start, end)
    path = gen.export_html(report, filepath)
    return path, report


# ==========================================
# 命令行入口
# ==========================================

def _print_encoding_safe(text: str):
    """GBK 终端安全输出"""
    try:
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(text)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="运营报表生成器（v2.8）")
    sub = parser.add_subparsers(dest="command")

    p_weekly = sub.add_parser("weekly", help="生成上周 HTML 周报（默认命令）")
    p_weekly.add_argument("--out", default=None, help="HTML 输出路径")

    p_sum = sub.add_parser("summary", help="控制台摘要")
    p_sum.add_argument("--period", choices=["week", "month", "lastweek"],
                       default="week", help="统计周期（默认最近7天）")
    p_sum.add_argument("--out", default=None, help="同时导出 HTML 的路径")

    sub.add_parser("selftest", help="运行自测")

    args = parser.parse_args()
    command = args.command or "weekly"
    gen = get_generator()

    if command == "weekly":
        path, report = generate_weekly_report(getattr(args, "out", None))
        _print_encoding_safe(gen.render_text(report))
        _print_encoding_safe(f"\nHTML 周报已导出: {path}")
    elif command == "summary":
        if args.period == "month":
            start, end = ReportGenerator.month_range()
        elif args.period == "lastweek":
            start, end = ReportGenerator.last_week_range()
        else:
            start, end = ReportGenerator.last_n_days_range(7)
        report = gen.collect(start, end)
        _print_encoding_safe(gen.render_text(report))
        if args.out:
            path = gen.export_html(report, args.out)
            _print_encoding_safe(f"\nHTML 报表已导出: {path}")
    elif command == "selftest":
        run_self_test()
    else:
        parser.print_help()


# ==========================================
# 自测
# ==========================================

def _make_calls_db(path: str, start: datetime, end: datetime):
    """构造测试用通话记录库"""
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE call_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_id TEXT NOT NULL,
            caller TEXT, callee TEXT, direction TEXT,
            start_time TEXT, end_time TEXT, duration_seconds REAL,
            intent TEXT, hangup_reason TEXT, has_recording INTEGER DEFAULT 0,
            consent_given INTEGER DEFAULT 0
        )
    """)
    mid = start + (end - start) / 2
    stamp = mid.strftime("%Y-%m-%d %H:%M:%S")
    # (call_id, direction, duration, intent, hangup, recording)
    data = [
        ("call_ob_01", "outbound", 0, "query", "timeout", 0),
        ("call_ob_02", "outbound", 0, "complaint", "timeout", 0),
        ("call_ob_03", "outbound", 0, "appointment", "busy", 0),
        ("call_ob_04", "outbound", 20, "query", "normal", 1),
        ("call_ob_05", "outbound", 45, "query", "normal", 1),
        ("call_ob_06", "outbound", 200, "query", "normal", 1),
        ("call_ib_01", "inbound", 60, "query", "normal", 1),
        ("call_ib_02", "inbound", 75, "query", "normal", 1),
        ("call_ib_03", "inbound", 90, "complaint", "normal", 1),
        ("call_ib_04", "inbound", 110, "appointment", "normal", 0),
    ]
    for cid, direction, dur, intent, reason, rec in data:
        conn.execute(
            """INSERT INTO call_records
               (call_id, caller, callee, direction, start_time, end_time,
                duration_seconds, intent, hangup_reason, has_recording, consent_given)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
            (cid, "13800000000", "13900000000", direction, stamp,
             stamp, dur, intent, reason, rec)
        )
    conn.commit()
    conn.close()


def _make_todos_db(path: str, start: datetime, end: datetime):
    """构造测试用待办库"""
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            todo_id TEXT NOT NULL,
            call_id TEXT, userid TEXT, content TEXT,
            responsible_person TEXT, due_date TEXT,
            status TEXT DEFAULT 'pending', retry_count INTEGER DEFAULT 0,
            source TEXT, priority TEXT,
            created_at TEXT, updated_at TEXT, closed_at TEXT, close_reason TEXT
        )
    """)
    mid = start + (end - start) / 2
    stamp = mid.isoformat()
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    future = (datetime.now() + timedelta(days=3)).isoformat()
    # (todo_id, status, due_date)
    data = [
        ("todo_01", "pending", yesterday),    # 逾期
        ("todo_02", "pending", future),       # 未逾期
        ("todo_03", "reminded", yesterday),   # 逾期
        ("todo_04", "closed", future),        # 已完成
    ]
    for tid, status, due in data:
        conn.execute(
            """INSERT INTO todos
               (todo_id, call_id, userid, content, responsible_person, due_date,
                status, source, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'test', ?, ?)""",
            (tid, "call_ob_05", "zhangsan", "提交修订方案", "张三",
             due, status, stamp, stamp)
        )
    conn.commit()
    conn.close()


def _make_tasks_file(path: str, start: datetime, end: datetime):
    """构造测试用调度任务文件（周期内 6 个 + 周期外 2 个）"""
    mid = start + (end - start) / 2
    in_range = mid.isoformat()
    out_range = (start - timedelta(days=10)).isoformat()
    tasks = []
    for i in range(6):
        tasks.append({
            "task_id": f"task_{i:03d}", "target": f"1380000000{i}",
            "target_name": f"客户{i}", "task_type": "one_shot",
            "status": "completed", "created_at": out_range,
            "executed_at": in_range, "result": {"ok": True},
        })
    for i in range(2):
        tasks.append({
            "task_id": f"task_old_{i}", "target": f"1370000000{i}",
            "task_type": "one_shot", "status": "completed",
            "created_at": out_range, "executed_at": out_range,
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def run_self_test():
    """运行运营报表自测（使用临时数据库，不触碰真实数据）"""
    import tempfile
    import shutil

    _print_encoding_safe("=" * 60)
    _print_encoding_safe("report_generator.py — 自测模式")
    _print_encoding_safe("=" * 60)

    tmp_dir = tempfile.mkdtemp(prefix="report_gen_test_")
    try:
        calls_db = os.path.join(tmp_dir, "call_records.db")
        todos_db = os.path.join(tmp_dir, "todos.db")
        tasks_file = os.path.join(tmp_dir, "tasks.json")

        # 固定测试周期：上周一 ~ 上周日
        start, end = ReportGenerator.last_week_range()
        _make_calls_db(calls_db, start, end)
        _make_todos_db(todos_db, start, end)
        _make_tasks_file(tasks_file, start, end)

        gen = ReportGenerator(calls_db=calls_db, todos_db=todos_db,
                              tasks_file=tasks_file, report_dir=tmp_dir)
        report = gen.collect(start, end)

        # 测试 1: 总量与方向
        _print_encoding_safe("\n[测试 1] 总量与方向分布")
        ov = report["overview"]
        assert ov["total_calls"] == 10, f"总数应为10，实际 {ov['total_calls']}"
        assert ov["outbound_calls"] == 6
        assert ov["inbound_calls"] == 4
        assert ov["unanswered_calls"] == 3
        _print_encoding_safe(f"  总通话 {ov['total_calls']} / 外呼 {ov['outbound_calls']} / 来电 {ov['inbound_calls']} ✅")

        # 测试 2: 外呼接通率
        _print_encoding_safe("\n[测试 2] 外呼接通率")
        assert ov["outbound_connected"] == 3
        assert abs(ov["outbound_connect_rate"] - 0.5) < 1e-9
        _print_encoding_safe(f"  接通 {ov['outbound_connected']}/{ov['outbound_calls']} = {ov['outbound_connect_rate'] * 100:.0f}% ✅")

        # 测试 3: 时长分布
        _print_encoding_safe("\n[测试 3] 时长分布")
        buckets = report["duration_buckets"]
        assert sum(b["count"] for b in buckets) == 10, "时长分布合计应等于总通话数"
        assert buckets[0]["count"] == 4, f"0-30秒应为4次（3次未接通+20秒），实际 {buckets[0]['count']}"
        assert buckets[1]["count"] == 1
        assert buckets[2]["count"] == 4
        assert buckets[3]["count"] == 1
        _print_encoding_safe(f"  0-30秒 {buckets[0]['count']} / 30-60秒 {buckets[1]['count']} / "
                             f"1-3分钟 {buckets[2]['count']} / 3分钟以上 {buckets[3]['count']} ✅")

        # 测试 4: 四级漏斗
        _print_encoding_safe("\n[测试 4] 外呼四级漏斗")
        funnel = {s["key"]: s for s in report["funnel"]}
        assert funnel["scheduled"]["count"] == 6, "调度发起应为周期内任务数 6"
        assert funnel["connected"]["count"] == 3
        assert funnel["effective"]["count"] == 2, "有效通话应剔除 20 秒通话"
        assert funnel["todos"]["count"] == 4
        assert abs(funnel["connected"]["conversion_from_prev"] - 0.5) < 1e-9
        assert abs(funnel["effective"]["conversion_from_prev"] - 2 / 3) < 1e-3
        assert abs(funnel["todos"]["conversion_from_prev"] - 2.0) < 1e-9
        _print_encoding_safe("  调度发起 6 → 振铃接通 3 → 有效通话 2 → 待办跟进 4 ✅")

        # 测试 5: 待办统计
        _print_encoding_safe("\n[测试 5] 待办统计")
        ts = report["todo_stats"]
        assert ts["new_todos"] == 4
        assert ts["closed_todos"] == 1
        assert ts["overdue_todos"] == 2, f"逾期应为2（pending+reminded各1），实际 {ts['overdue_todos']}"
        _print_encoding_safe(f"  新增 {ts['new_todos']} / 已完成 {ts['closed_todos']} / 逾期 {ts['overdue_todos']} ✅")

        # 测试 6: 意图分布
        _print_encoding_safe("\n[测试 6] 意图分布")
        intents = report["intents"]
        assert intents[0]["intent"] == "query" and intents[0]["count"] == 6
        assert all(intents[i]["count"] >= intents[i + 1]["count"] for i in range(len(intents) - 1))
        _print_encoding_safe(f"  Top1: {intents[0]['intent']} x{intents[0]['count']}，降序排列 ✅")

        # 测试 7: 每日趋势（同一天数据 → 1 天，其余补零）
        _print_encoding_safe("\n[测试 7] 每日趋势")
        trend = report["daily_trend"]
        assert len(trend) == 7, "周周期应输出 7 天"
        assert sum(d["calls"] for d in trend) == 10
        _print_encoding_safe(f"  {len(trend)} 天，合计 {sum(d['calls'] for d in trend)} 次 ✅")

        # 测试 8: 数据源缺失降级（规则 9）
        _print_encoding_safe("\n[测试 8] 数据源缺失降级")
        gen_bad = ReportGenerator(calls_db=os.path.join(tmp_dir, "nonexistent.db"),
                                  todos_db=os.path.join(tmp_dir, "nonexistent2.db"),
                                  tasks_file=os.path.join(tmp_dir, "nonexistent.json"),
                                  report_dir=tmp_dir)
        bad_report = gen_bad.collect(start, end)
        assert bad_report["overview"]["total_calls"] == 0
        assert len(bad_report["warnings"]) >= 3, "三个数据源缺失应各记一条警告"
        assert all(s["count"] == 0 for s in bad_report["funnel"])
        assert bad_report["data_available"] is False
        # 降级报告的 HTML 应展示数据源警告横幅
        bad_html = gen_bad.render_html(bad_report)
        assert "数据源提示" in bad_html
        _print_encoding_safe(f"  零指标 + {len(bad_report['warnings'])} 条警告，未抛异常 ✅")

        # 测试 9: HTML 导出与 XSS 转义
        _print_encoding_safe("\n[测试 9] HTML 导出与转义")
        # 注入恶意意图名验证转义
        conn = sqlite3.connect(calls_db)
        conn.execute("UPDATE call_records SET intent = '<script>alert(1)</script>' WHERE call_id = 'call_ob_01'")
        conn.commit()
        conn.close()
        report2 = gen.collect(start, end)
        out_path = os.path.join(tmp_dir, "weekly_report_test.html")
        written = gen.export_html(report2, out_path)
        assert written == out_path and os.path.exists(out_path)
        content = open(out_path, encoding="utf-8").read()
        assert "<script>alert(1)</script>" not in content, "HTML 必须转义恶意输入"
        assert "&lt;script&gt;" in content
        for keyword in ("外呼四级漏斗", "通话时长分布", "意图分布", "待办跟进",
                        "外呼接通率", "njskills@agent.qq.com"):
            assert keyword in content, f"HTML 周报缺少关键区块: {keyword}"
        _print_encoding_safe("  单文件自包含、恶意输入已转义、关键区块齐全 ✅")

        # 测试 10: 上周周期口径
        _print_encoding_safe("\n[测试 10] 上周周期口径（周一生成上周报）")
        s2, e2 = ReportGenerator.last_week_range()
        assert s2.weekday() == 0 and e2.weekday() == 6
        assert (e2 - s2).days == 6
        assert e2 < datetime.now(), "上周结束时间应早于当前时间"
        _print_encoding_safe(f"  {s2:%Y-%m-%d %H:%M:%S} ~ {e2:%Y-%m-%d %H:%M:%S}（周一~周日）✅")

        _print_encoding_safe(f"\n{'=' * 60}")
        _print_encoding_safe("所有自测通过 ✓")
        _print_encoding_safe("=" * 60)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
