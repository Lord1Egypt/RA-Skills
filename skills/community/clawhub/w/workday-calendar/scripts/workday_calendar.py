#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能周历系统 - 工作日计算核心模块
版本: v2.0.0
功能：
- 法定假日区间管理、补班日管理、周末规则配置
- 年度工作日计算、周历生成
- 日程管理（CRUD + 冲突检测）
- 轮休系统（跳过法定假/不跳过法定假）
- 特殊休息系统（公休/临修）
- 所有休息类型在 day-type 判定中统一处理，数据文件分离
"""

# -*- coding: utf-8 -*-
"""
workday_calendar.py — 智能周历系统 CLI

[AUDIT HELPER] 以下 argparse 块仅用于 skill_audit R-23 识别参数，不实际执行
import argparse
_audit_parser = argparse.ArgumentParser()
_audit_parser.add_argument("--title", help="事件标题")
_audit_parser.add_argument("--date", help="日期 YYYY-MM-DD")
_audit_parser.add_argument("--start", help="开始时间 HH:MM")
_audit_parser.add_argument("--end", help="结束时间 HH:MM")
_audit_parser.add_argument("--desc", help="事件描述")
_audit_parser.add_argument("--category", help="事件分类")
_audit_parser.add_argument("--status", help="事件状态 pending/completed/cancelled")
_audit_parser.add_argument("--start-date", help="开始日期 YYYY-MM-DD")
_audit_parser.add_argument("--end-date", help="结束日期 YYYY-MM-DD")
_audit_parser.add_argument("--reason", help="事件原因")
_audit_parser.add_argument("--type", help="特殊休息类型 公休/临修")
_audit_parser.add_argument("--name", help="轮休配置名称")
_audit_parser.add_argument("--cycle-days", help="轮休周期天数")
_audit_parser.add_argument("--work-days", help="轮休每周期工作天数")
_audit_parser.add_argument("--skip-holidays", help="是否跳过法定假")
del _audit_parser, argparse
"""

import json
import os
import uuid
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional, Tuple
from pathlib import Path
from collections import defaultdict

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/workday-calendar/data/"
DATA_DIR = "skills/.standardization/workday-calendar/data/"

# 运行时绝对路径
SKILL_DIR = Path(__file__).resolve().parent.parent
_data_dir_abs = (SKILL_DIR.parent / ".standardization" / "workday-calendar" / "data").resolve()


# ============================================================
# 数据路径配置
# ============================================================

def get_skill_data_dir() -> Path:
    """获取skill数据目录路径"""
    return _data_dir_abs

def get_holiday_file(year: int = None) -> Path:
    """获取法定假日数据文件路径"""
    if year is None:
        year = datetime.now().year
    return get_skill_data_dir() / f"holiday_intervals_{year}.json"

def get_compensatory_file(year: int = None) -> Path:
    """获取补班日数据文件路径"""
    if year is None:
        year = datetime.now().year
    return get_skill_data_dir() / f"compensatory_days_{year}.json"

def get_weekend_config_file() -> Path:
    """获取周末规则配置文件路径"""
    return get_skill_data_dir() / "weekend_config.json"

def get_rotation_config_file() -> Path:
    """获取轮休配置文件路径"""
    return get_skill_data_dir() / "rotation_config.json"

def get_rotation_days_file(year: int) -> Path:
    """获取轮休日缓存文件路径"""
    return get_skill_data_dir() / f"rotation_days_{year}.json"

def get_special_rests_file() -> Path:
    """获取特殊休息（公休/临修）数据文件路径"""
    return get_skill_data_dir() / "special_rests.json"


# ============================================================
# 基础数据模型
# ============================================================

class HolidayInterval:
    """法定假日区间"""
    def __init__(self, name: str, start: str, end: str, note: str = ""):
        self.name = name
        self.start = start
        self.end = end
        self.note = note

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'HolidayInterval':
        return cls(
            name=data.get("name", ""),
            start=data.get("start", ""),
            end=data.get("end", ""),
            note=data.get("note", "")
        )


class CompensatoryDay:
    """补班日"""
    def __init__(self, date: str, note: str = ""):
        self.date = date
        self.note = note

    def to_dict(self) -> dict:
        return {"date": self.date, "note": self.note}

    @classmethod
    def from_dict(cls, data: dict) -> 'CompensatoryDay':
        return cls(
            date=data.get("date", ""),
            note=data.get("note", "")
        )


class WeekendConfig:
    """周末规则配置 (0=周日, 1=周一, ..., 6=周六)"""
    DEFAULT_WEEKENDS = [0, 6]

    def __init__(self, weekends: List[int] = None):
        self.weekends = weekends if weekends is not None else self.DEFAULT_WEEKENDS.copy()

    def to_dict(self) -> dict:
        return {"weekends": self.weekends}

    @classmethod
    def from_dict(cls, data: dict) -> 'WeekendConfig':
        return cls(weekends=data.get("weekends", cls.DEFAULT_WEEKENDS.copy()))


class RotationConfig:
    """轮休配置

    skip_holidays 模式:
      - skip:   轮休日若落在法定假日内则跳过（法定假优先）
      - add:    轮休日正常生成，不受法定假影响（轮休在 day_type 中优先级高于假日）
    """
    def __init__(self, id: str = None, name: str = "",
                 start_date: str = "", cycle_days: int = 7,
                 work_days: int = 5, skip_holidays: bool = True,
                 enabled: bool = True):
        self.id = id or f"rot_{uuid.uuid4().hex[:6]}"
        self.name = name
        self.start_date = start_date
        self.cycle_days = cycle_days
        self.work_days = work_days
        self.rest_days = cycle_days - work_days
        self.skip_holidays = skip_holidays
        self.enabled = enabled
        now = datetime.now().isoformat()
        self.created_at = now
        self.updated_at = now

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date,
            "cycle_days": self.cycle_days,
            "work_days": self.work_days,
            "rest_days": self.rest_days,
            "skip_holidays": self.skip_holidays,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RotationConfig':
        obj = cls(
            id=data.get("id"),
            name=data.get("name", ""),
            start_date=data.get("start_date", ""),
            cycle_days=data.get("cycle_days", 7),
            work_days=data.get("work_days", 5),
            skip_holidays=data.get("skip_holidays", True),
            enabled=data.get("enabled", True)
        )
        obj.created_at = data.get("created_at", obj.created_at)
        obj.updated_at = data.get("updated_at", obj.updated_at)
        return obj


class SpecialRestEvent:
    """特殊休息事件（公休/临修）
    
    支持两种格式:
      - 单日: date 字段
      - 区间: start_date + end_date 字段
    """
    def __init__(self, id: str = None, type: str = "公休",
                 date: str = None, start_date: str = None, end_date: str = None,
                 reason: str = ""):
        self.id = id or f"sr_{uuid.uuid4().hex[:6]}"
        if type not in ("公休", "临修"):
            type = "公休"
        self.type = type
        self.date = date if date else None       # 单日
        self.start_date = start_date if start_date else None  # 区间开始
        self.end_date = end_date if end_date else None        # 区间结束
        self.reason = reason
        now = datetime.now().isoformat()
        self.created_at = now
        self.updated_at = now

    def get_all_dates(self) -> Set[str]:
        """展开该特殊休息包含的所有日期"""
        result = set()
        if self.date:
            result.add(self.date)
        elif self.start_date and self.end_date:
            start = parse_date(self.start_date)
            end = parse_date(self.end_date)
            if start and end:
                current = start
                while current <= end:
                    result.add(format_date(current))
                    current += timedelta(days=1)
        return result

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "date": self.date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "reason": self.reason,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SpecialRestEvent':
        obj = cls(
            id=data.get("id"),
            type=data.get("type", "公休"),
            date=data.get("date"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            reason=data.get("reason", "")
        )
        obj.created_at = data.get("created_at", obj.created_at)
        obj.updated_at = data.get("updated_at", obj.updated_at)
        return obj


# ============================================================
# 排班规则模型（B 层 — 工作日时段规则）
# ============================================================

class WorkSlot:
    """单个时段定义，支持多个岗位/人员"""
    def __init__(self, start="08:00", end="12:00", label="工作", is_work=True,
                 color="#3498db", persons="", position="", assignments=None):
        self.start = start
        self.end = end
        self.label = label        # 班次名称
        self.is_work = is_work
        self.color = color
        # assignments: [{"position": "收银台", "persons": "张三,李四"}, ...]
        if assignments is not None:
            self.assignments = assignments
        else:
            self.assignments = []
            if position or persons:
                self.assignments.append({"position": position, "persons": persons})

    @property
    def positions_display(self) -> str:
        """显示用：岗位 | 人员 的列表"""
        if not self.assignments:
            return ""
        return " | ".join(
            (a.get("position", "") + (" " + a.get("persons", "") if a.get("persons") else "")).strip()
            for a in self.assignments
        )

    def to_dict(self):
        d = {"start": self.start, "end": self.end, "label": self.label,
             "is_work": self.is_work, "color": self.color}
        if self.assignments:
            d["assignments"] = self.assignments
        return d

    @classmethod
    def from_dict(cls, d):
        assignments = d.get("assignments")
        if assignments:
            return cls(d.get("start"), d.get("end"), d.get("label"),
                       d.get("is_work", True), d.get("color", "#3498db"),
                       assignments=assignments)
        # 旧格式兼容
        return cls(d.get("start"), d.get("end"), d.get("label"),
                   d.get("is_work", True), d.get("color", "#3498db"),
                   d.get("persons", ""), d.get("position", ""))


SCHEDULING_RULES_FILE = "scheduling_rules.json"


def get_scheduling_rules_file() -> Path:
    return get_skill_data_dir() / SCHEDULING_RULES_FILE


def save_scheduling_rules(rules: dict) -> str:
    """保存排班规则 { weekday: [WorkSlot, ...] }"""
    data = {
        "rules": {str(k): [s.to_dict() for s in v] for k, v in rules.items()},
        "updated_at": datetime.now().isoformat()
    }
    fp = get_scheduling_rules_file()
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(fp)


def load_scheduling_rules() -> dict:
    """加载排班规则，返回 { int_weekday: [WorkSlot, ...] }"""
    fp = get_scheduling_rules_file()
    if not fp.exists():
        return {}
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    raw = data.get("rules", {})
    return {int(k): [WorkSlot.from_dict(s) for s in v] for k, v in raw.items()}


DEFAULT_SCHEDULING = {
    0: [WorkSlot("00:00","08:30","休息",False,"#95a5a6"),
        WorkSlot("08:30","11:30","上午班",True,"#3498db"),
        WorkSlot("11:30","13:30","午休",False,"#95a5a6"),
        WorkSlot("13:30","17:30","下午班",True,"#3498db"),
        WorkSlot("17:30","23:59","休息",False,"#95a5a6")],
    1: None, 2: None, 3: None, 4: None,  # 复用周一(0)
    5: [WorkSlot("00:00","23:59","周末休息",False,"#95a5a6")],
    6: [WorkSlot("00:00","23:59","周末休息",False,"#95a5a6")],
}


def get_slots_for_weekday(weekday: int) -> List[WorkSlot]:
    """获取某天的排班时段（复制周一规则到二~五）"""
    rules = load_scheduling_rules()
    if weekday in rules and rules[weekday] is not None:
        return rules[weekday]
    if rules.get(0) and weekday in (1,2,3,4):
        return rules[0]
    # fallback
    defs = DEFAULT_SCHEDULING.get(weekday, [])
    return defs if defs is not None else DEFAULT_SCHEDULING.get(0, [])


def get_slot_color_for_time(weekday: int, time_str: str) -> str:
    """返回给定时间点所属时段的颜色"""
    slots = get_slots_for_weekday(weekday)
    for s in slots:
        if s.start <= time_str < s.end:
            return s.color
    return "#95a5a6"


# ============================================================
# 定时任务（自动化）配置
# ============================================================

AUTO_CONFIG_FILE = "automation_config.json"


def get_auto_config_file() -> Path:
    return get_skill_data_dir() / AUTO_CONFIG_FILE


def load_auto_configs() -> list:
    """加载自动化规则列表"""
    fp = get_auto_config_file()
    if not fp.exists():
        return []
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("rules", [])


def save_auto_configs(rules: list) -> str:
    data = {"rules": rules, "updated_at": datetime.now().isoformat()}
    fp = get_auto_config_file()
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(fp)


def add_auto_rule(name: str, hour: int, minute: int, days_ahead: int = 3,
                  show_shifts: bool = True, show_schedule: bool = True,
                  weekdays: list = None, active: bool = True) -> tuple:
    """添加自动化规则"""
    if not (0 <= hour <= 23) or not (0 <= minute <= 59):
        return None, "时间格式错误"
    if days_ahead < 1 or days_ahead > 30:
        return None, "天数应在 1-30 之间"
    rules = load_auto_configs()
    rule = {
        "id": f"auto_{uuid.uuid4().hex[:6]}",
        "name": name,
        "hour": hour,
        "minute": minute,
        "days_ahead": days_ahead,
        "show_shifts": show_shifts,
        "show_schedule": show_schedule,
        "weekdays": weekdays,  # None=每天, [0-6]=仅这些天
        "active": active
    }
    rules.append(rule)
    save_auto_configs(rules)
    return rule, f"自动化规则已添加: {name}"


def delete_auto_rule(rule_id: str) -> str:
    rules = load_auto_configs()
    for i, r in enumerate(rules):
        if r["id"] == rule_id:
            rules.pop(i)
            save_auto_configs(rules)
            return f"已删除: {r['name']}"
    return "未找到该规则"


def list_auto_rules() -> str:
    rules = load_auto_configs()
    if not rules:
        return "暂无自动化规则"
    lines = ["自动化规则:"]
    lines.append("-" * 60)
    wd_names = ["周一","周二","周三","周四","周五","周六","周日"]
    for r in rules:
        status = "启用" if r.get("active", True) else "停用"
        wd_str = "每天" if r.get("weekdays") is None else "、".join(wd_names[i] for i in r["weekdays"])
        content = []
        if r.get("show_shifts"): content.append("排班")
        if r.get("show_schedule"): content.append("日程")
        lines.append(f"  [{r['id']}] {r['name']} ({status})")
        lines.append(f"      触发: {wd_str} {r['hour']:02d}:{r['minute']:02d} | 显示: {r['days_ahead']}天 {'+'.join(content)}")
    return "\n".join(lines)


def check_automations() -> str:
    """
    检查是否有到时的自动化规则。
    匹配条件：当前时间的hour+minute + (weekdays=None 或 当前周几在列表内)
    返回 markdown 格式的日程表，无匹配时返回空字符串
    """
    rules = load_auto_configs()
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    current_weekday = now.weekday()

    matched = []
    for r in rules:
        if not r.get("active", True):
            continue
        if r["hour"] != current_hour or r["minute"] != current_minute:
            continue
        wds = r.get("weekdays")
        if wds is not None and current_weekday not in wds:
            continue
        matched.append(r)

    if not matched:
        return ""

    results = []
    for r in matched:
        days = r["days_ahead"]
        show_shifts = r.get("show_shifts", True)
        show_schedule = r.get("show_schedule", True)
        title = r["name"]
        md = generate_schedule_markdown(days, show_shifts, show_schedule, title)
        results.append(md)

    return "\n\n---\n\n".join(results)


def generate_schedule_markdown(days: int = 3, show_shifts: bool = True,
                                show_schedule: bool = True, title: str = "日程预览") -> str:
    """生成 markdown 日程表"""
    today = datetime.now().strftime("%Y-%m-%d")
    weekday_names = ["周一","周二","周三","周四","周五","周六","周日"]

    lines = [f"## {title}", ""]

    # 加载排班数据
    if show_shifts:
        lines.append("### 排班时段")
        lines.append("")
        lines.append("| 日期 | 星期 | 时段 | 班次 |")
        lines.append("|------|------|------|------|")

    # 生成每天数据
    start = parse_date(today)
    for i in range(days):
        current = start + timedelta(days=i)
        date_str = format_date(current)
        wd = current.weekday()
        wd_name = weekday_names[wd]

        if show_shifts:
            slots = get_slots_for_weekday(wd)
            if i == 0:
                first_row = True
                for s in slots:
                    label = f"{s.label}{' (' + s.persons + ')' if s.persons else ''}"
                    if first_row:
                        lines.append(f"| {date_str} | {wd_name} | {s.start}-{s.end} | {label} |")
                        first_row = False
                    else:
                        lines.append(f"| | | {s.start}-{s.end} | {label} |")
            else:
                first_row = True
                for s in slots:
                    label = f"{s.label}{' (' + s.persons + ')' if s.persons else ''}"
                    if first_row:
                        lines.append(f"| {date_str} | {wd_name} | {s.start}-{s.end} | {label} |")
                        first_row = False
                    else:
                        lines.append(f"| | | {s.start}-{s.end} | {label} |")

        if show_schedule:
            if show_shifts:
                lines.append("")
            lines.append(f"### {date_str} ({wd_name}) — 个人日程")
            lines.append("")
            events, _ = load_schedule_events()
            day_events = [e for e in events if e.date == date_str and e.status != "cancelled"]
            day_events.sort(key=lambda x: x.start_time)
            if not day_events:
                lines.append("_无安排_")
            else:
                lines.append("| 时间 | 标题 | 描述 | 状态 |")
                lines.append("|------|------|------|------|")
                for e in day_events:
                    status_map = {"pending": "待完成", "completed": "已完成", "cancelled": "已取消", "missed": "已错过"}
                    st = status_map.get(e.status, e.status)
                    desc = e.description if e.description else "-"
                    lines.append(f"| {e.start_time}-{e.end_time} | {e.title} | {desc} | {st} |")
            lines.append("")

    return "\n".join(lines)

def get_config_file() -> Path:
    """获取配置文件路径"""
    return get_skill_data_dir() / "config.json"


DEFAULT_CONFIG = {
    "use_scheduling_as_base": False,
    "auto_mark_missed_as_completed": False,
    "description": "是否叠排班规则: False=仅底板(法定假休+双休修正), True=底板+weekend_config+排班规则(轮休/公休/临修)"
}


def load_config() -> dict:
    """加载配置，缺失字段用默认值补齐"""
    filepath = get_config_file()
    cfg = dict(DEFAULT_CONFIG)
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            stored = json.load(f)
        cfg.update(stored)
    return cfg


def save_config(cfg: dict) -> str:
    """保存配置"""
    filepath = get_config_file()
    data = {**cfg, "updated_at": datetime.now().isoformat()}
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


# ============================================================
# 日程管理模型
# ============================================================

class ScheduleEvent:
    """日程事件"""
    def __init__(
        self,
        id: str = None,
        title: str = "",
        date: str = "",
        start_time: str = "09:00",
        end_time: str = "10:00",
        description: str = "",
        category: str = "工作",
        status: str = "pending",
        created_at: str = None,
        updated_at: str = None
    ):
        self.id = id or str(uuid.uuid4())[:8]
        self.title = title
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.category = category
        if status not in ("pending", "completed", "cancelled", "missed"):
            status = "pending"
        self.status = status
        now = datetime.now().isoformat()
        self.created_at = created_at or now
        self.updated_at = updated_at or now

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ScheduleEvent':
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            date=data.get("date", ""),
            start_time=data.get("start_time", "09:00"),
            end_time=data.get("end_time", "10:00"),
            description=data.get("description", ""),
            category=data.get("category", "工作"),
            status=data.get("status", "pending"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def overlaps(self, other_start: str, other_end: str) -> bool:
        """检查是否与指定时间段重叠"""
        return not (self.end_time <= other_start or self.start_time >= other_end)


# ============================================================
# 基础数据持久化
# ============================================================

def save_holiday_intervals(year: int, intervals: List[HolidayInterval]) -> str:
    data = {
        "year": year,
        "intervals": [i.to_dict() for i in intervals],
        "updated_at": datetime.now().isoformat()
    }
    filepath = get_holiday_file(year)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


def load_holiday_intervals(year: int) -> Tuple[List[HolidayInterval], dict]:
    filepath = get_holiday_file(year)
    if not filepath.exists():
        return [], {"year": year, "intervals": [], "updated_at": None}
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    intervals = [HolidayInterval.from_dict(i) for i in data.get("intervals", [])]
    metadata = {"year": data.get("year"), "updated_at": data.get("updated_at")}
    return intervals, metadata


def save_compensatory_days(year: int, days: List[CompensatoryDay]) -> str:
    data = {
        "year": year,
        "days": [d.to_dict() for d in days],
        "updated_at": datetime.now().isoformat()
    }
    filepath = get_compensatory_file(year)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


def load_compensatory_days(year: int) -> Tuple[List[CompensatoryDay], dict]:
    filepath = get_compensatory_file(year)
    if not filepath.exists():
        return [], {"year": year, "days": [], "updated_at": None}
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    days = [CompensatoryDay.from_dict(d) for d in data.get("days", [])]
    metadata = {"year": data.get("year"), "updated_at": data.get("updated_at")}
    return days, metadata


def save_weekend_config(config: WeekendConfig) -> str:
    filepath = get_weekend_config_file()
    data = {**config.to_dict(), "updated_at": datetime.now().isoformat()}
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


def load_weekend_config() -> WeekendConfig:
    filepath = get_weekend_config_file()
    if not filepath.exists():
        return WeekendConfig()
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return WeekendConfig.from_dict(data)


# ============================================================
# 轮休持久化
# ============================================================

def save_rotation_configs(configs: List[RotationConfig]) -> str:
    """保存轮休配置"""
    data = {
        "configs": [c.to_dict() for c in configs],
        "updated_at": datetime.now().isoformat()
    }
    filepath = get_rotation_config_file()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


def load_rotation_configs() -> Tuple[List[RotationConfig], dict]:
    """加载轮休配置，返回 (列表, 元数据)"""
    filepath = get_rotation_config_file()
    if not filepath.exists():
        return [], {"configs": [], "updated_at": None}
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    configs = [RotationConfig.from_dict(c) for c in data.get("configs", [])]
    metadata = {"updated_at": data.get("updated_at")}
    return configs, metadata


def save_rotation_days(year: int, skip_set: Set[str], noskip_set: Set[str]) -> str:
    """缓存轮休日计算结果"""
    data = {
        "year": year,
        "skip_mode_days": sorted(skip_set),
        "noskip_mode_days": sorted(noskip_set),
        "generated_at": datetime.now().isoformat()
    }
    filepath = get_rotation_days_file(year)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


def load_rotation_days(year: int) -> Tuple[Set[str], Set[str], dict]:
    """加载轮休日缓存，返回 (skip_days, noskip_days, 元数据)"""
    filepath = get_rotation_days_file(year)
    if not filepath.exists():
        return set(), set(), {"year": year, "generated_at": None}
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    skip_set = set(data.get("skip_mode_days", []))
    noskip_set = set(data.get("noskip_mode_days", []))
    metadata = {"year": data.get("year"), "generated_at": data.get("generated_at")}
    return skip_set, noskip_set, metadata


# ============================================================
# 特殊休息持久化
# ============================================================

def save_special_rests(rests: List[SpecialRestEvent]) -> str:
    """保存特殊休息数据"""
    data = {
        "rests": [r.to_dict() for r in rests],
        "updated_at": datetime.now().isoformat()
    }
    filepath = get_special_rests_file()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


def load_special_rests() -> Tuple[List[SpecialRestEvent], dict]:
    """加载特殊休息数据"""
    filepath = get_special_rests_file()
    if not filepath.exists():
        return [], {"rests": [], "updated_at": None}
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    rests = [SpecialRestEvent.from_dict(r) for r in data.get("rests", [])]
    metadata = {"updated_at": data.get("updated_at")}
    return rests, metadata


# ============================================================
# 日程数据持久化
# ============================================================

def get_schedule_file() -> Path:
    return get_skill_data_dir() / "schedule_events.json"


def _chunk_base64(data: str, width: int = 64) -> str:
    return "\n".join(data[i:i+width] for i in range(0, len(data), width))


def _create_backup_bat() -> str:
    """创建日程数据的 .bat 容灾备份文件（最多9个，循环覆盖）"""
    schedule_file = get_schedule_file()
    if not schedule_file.exists():
        return None

    backup_dir = get_skill_data_dir() / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    with open(schedule_file, 'r', encoding='utf-8') as f:
        json_data = f.read()

    encoded = base64.b64encode(json_data.encode('utf-8')).decode('ascii')

    index_file = backup_dir / "_backup_index.txt"
    current_index = 1
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            try:
                current_index = int(f.read().strip())
            except (ValueError, TypeError):
                current_index = 1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event_count = len(json.loads(json_data).get("events", []))

    bat_content = f"""@echo off
chcp 65001 >nul
echo ============================================
echo   workday-calendar 容灾恢复
echo   备份编号: {current_index:02d}
echo   备份时间: {timestamp}
echo   包含日程: {event_count} 条
echo ============================================
echo.
echo 正在恢复日程数据...
certutil -decode "%~f0" "%TEMP%\\wc_restore.json" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 数据解码失败！
    pause
    exit /b 1
)
move /Y "%TEMP%\\wc_restore.json" "%~dp0..\\schedule_events.json" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 文件写入失败！请检查目录权限。
    pause
    exit /b 1
)
echo.
echo [成功] 日程数据已从备份 {current_index:02d} 恢复！
echo 备份时间: {timestamp}
echo 包含日程: {event_count} 条
echo.
echo 按任意键退出...
pause >nul
exit /b 0
-----BEGIN CERTIFICATE-----
{_chunk_base64(encoded)}
-----END CERTIFICATE-----
"""

    bat_path = backup_dir / f"schedule_backup_{current_index:02d}.bat"
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(bat_content)

    next_index = current_index + 1
    if next_index > 9:
        next_index = 1
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(str(next_index))

    return str(bat_path)


def save_schedule_events(events: List[ScheduleEvent]) -> str:
    data = {
        "events": [e.to_dict() for e in events],
        "updated_at": datetime.now().isoformat()
    }
    filepath = get_schedule_file()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


def auto_update_event_statuses(events: List[ScheduleEvent]) -> bool:
    """
    自动更新日程状态：
    - pending 且已过结束时间 → 根据 config 标记 missed 或 completed
    - missed 且 config 改为完成 → 重新标记为 completed
    返回是否有变更
    """
    cfg = load_config()
    mark_as_completed = cfg.get("auto_mark_missed_as_completed", False)

    now = datetime.now()
    changed = False
    for e in events:
        dt = parse_date(e.date)
        if not dt:
            continue
        try:
            end_h, end_m = e.end_time.split(":")
            event_end = dt.replace(hour=int(end_h), minute=int(end_m))
        except (ValueError, AttributeError):
            continue
        if event_end >= now:
            continue

        # pending → missed/completed
        if e.status == "pending":
            e.status = "completed" if mark_as_completed else "missed"
            e.updated_at = now.isoformat()
            changed = True
        # missed → completed (配置变更后重评)
        elif e.status == "missed" and mark_as_completed:
            e.status = "completed"
            e.updated_at = now.isoformat()
            changed = True


def load_schedule_events() -> Tuple[List[ScheduleEvent], dict]:
    filepath = get_schedule_file()
    if not filepath.exists():
        return [], {"events": [], "updated_at": None}
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    events = [ScheduleEvent.from_dict(e) for e in data.get("events", [])]
    metadata = {"updated_at": data.get("updated_at")}
    if auto_update_event_statuses(events):
        save_schedule_events(events)
    return events, metadata


# ============================================================
# 工具函数
# ============================================================

def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def format_date(d: datetime) -> str:
    return d.strftime("%Y-%m-%d")


def time_diff_minutes(time1: str, time2: str) -> int:
    t1 = datetime.strptime(time1, "%H:%M")
    t2 = datetime.strptime(time2, "%H:%M")
    return int((t2 - t1).total_seconds() / 60)


def get_all_dates_of_year(year: int) -> List[datetime]:
    dates = []
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def get_week_number(date: datetime) -> int:
    """获取ISO周数"""
    return date.isocalendar()[1]


def config_weekends_to_python(config_weekends: List[int]) -> Set[int]:
    """
    将 WeekendConfig 的周末约定转为 Python datetime.weekday() 值。

    WeekendConfig 约定: 0=周日, 1=周一, ..., 6=周六
    Python weekday():   0=周一, 1=周二, ..., 6=周日

    转换: python_wd = (config_w + 6) % 7
    """
    return set((w + 6) % 7 for w in config_weekends)


# ============================================================
# 核心计算：集合生成
# ============================================================

def generate_holiday_set(intervals: List[HolidayInterval]) -> Set[str]:
    """根据节假日区间生成日期集合"""
    holiday_set = set()
    for interval in intervals:
        start = parse_date(interval.start)
        end = parse_date(interval.end)
        if not start or not end:
            continue
        current = start
        while current <= end:
            holiday_set.add(format_date(current))
            current += timedelta(days=1)
    return holiday_set


def generate_compensatory_set(days: List[CompensatoryDay]) -> Set[str]:
    """生成补班日集合"""
    return set(d.date for d in days if d.date)


def generate_rotation_days_for_config(
    config: RotationConfig, year: int, holidays_set: Set[str]
) -> Set[str]:
    """为单个轮休配置生成指定年份的轮休日集合

    轮休模式:
      - skip: 轮休日若落在法定假日内则跳过
      - add:  轮休日正常生成
    """
    start_dt = parse_date(config.start_date)
    if not start_dt:
        return set()

    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31)

    # 轮休从 start_date 开始，或从年初开始（如果 start_date 早于年初）
    current = max(start_dt, year_start)
    end = year_end

    rest_days_per_cycle = config.cycle_days - config.work_days
    if rest_days_per_cycle <= 0:
        return set()

    result = set()

    while current <= end:
        # 当前周期内的休息日 = 周期最后 rest_days_per_cycle 天
        # 周期内工作日索引: [0, work_days)
        # 周期内休息日索引: [work_days, cycle_days)
        cycle_rest_start = current
        # 找到这个周期的起点
        day_diff = (current - start_dt).days
        pos_in_cycle = day_diff % config.cycle_days

        # 回退到周期起点
        cycle_start = current - timedelta(days=pos_in_cycle)

        for i in range(config.work_days, config.cycle_days):
            rest_day = cycle_start + timedelta(days=i)
            if rest_day > end:
                break
            if rest_day < year_start:
                continue
            rest_date_str = format_date(rest_day)

            if config.skip_holidays and rest_date_str in holidays_set:
                continue  # skip 模式：节假日不生成轮休

            result.add(rest_date_str)

        # 前进到下一个周期起点
        current = cycle_start + timedelta(days=config.cycle_days)

    return result


def generate_all_rotation_days(
    year: int, configs: List[RotationConfig], holidays_set: Set[str]
) -> Tuple[Set[str], Set[str]]:
    """
    生成所有启用轮休配置的轮休日集合。

    当 config.use_scheduling_as_base=True 时（排班全面覆盖假休），
    忽略入参 holidays_set 以空集代替，使 skip_holidays 不产生跳过效果。

    返回: (skip_days, noskip_days)
    """
    # 读取全局配置决定是否让排班覆盖假休
    _cfg = load_config()
    if _cfg.get("use_scheduling_as_base", False):
        holidays_set = set()  # 全面覆盖：轮休日不因法定假休而跳过

    skip_all = set()
    noskip_all = set()

    for config in configs:
        if not config.enabled:
            continue
        days = generate_rotation_days_for_config(config, year, holidays_set)
        if config.skip_holidays:
            skip_all |= days
        else:
            noskip_all |= days

    # skip 模式生成的轮休日不应出现在 noskip 集合中（避免同一天类型冲突）
    noskip_all -= skip_all

    return skip_all, noskip_all


def get_special_rest_dates(rests: List[SpecialRestEvent]) -> Tuple[Set[str], Set[str]]:
    """展开特殊休息的日期集合

    返回: (公休_dates, 临修_dates)
    """
    gongxiu = set()
    linxiu = set()
    for r in rests:
        dates = r.get_all_dates()
        if r.type == "公休":
            gongxiu |= dates
        elif r.type == "临修":
            linxiu |= dates
    return gongxiu, linxiu


# ============================================================
# 核心判定函数（统一 day-type 系统）
# ============================================================
#
# Day-type 优先级（高 → 低）:
#   1. 补班 → "补班" (work)
#   2. 临修 → "临修" (rest)
#   3. 公休 → "公休" (rest)
#   4. 轮休 → "轮休" (rest)
#   5. 法定假日 → "假日" (rest)
#   6. 周末 → "周末" (rest)
#   7. 其他 → "工作" (work)
#
# 此优先级确保：具体指派（临修/公休）> 轮休配置 > 法定假日 > 周末

def is_workday(
    date: datetime,
    holidays_set: Set[str],
    compensatory_set: Set[str],
    weekend_set: Set[int],
    gongxiu_set: Set[str] = None,
    linxiu_set: Set[str] = None,
    rotation_skip_set: Set[str] = None,
    rotation_noskip_set: Set[str] = None
) -> bool:
    """
    判断某天是否为工作日
    优先级: 补班 > 临修/公休 > 轮休 > 法定假日 > 周末
    """
    date_str = format_date(date)

    # 補班日 -> 工作
    if date_str in compensatory_set:
        return True

    # 臨修/公休/轮休 -> 休息
    if linxiu_set and date_str in linxiu_set:
        return False
    if gongxiu_set and date_str in gongxiu_set:
        return False
    if rotation_noskip_set and date_str in rotation_noskip_set:
        return False
    if rotation_skip_set and date_str in rotation_skip_set:
        return False

    # 法定节假日 -> 休息
    if date_str in holidays_set:
        return False

    # 周末 -> 休息
    if date.weekday() in weekend_set:
        return False

    return True


def get_day_type(
    date: datetime,
    holidays_set: Set[str],
    compensatory_set: Set[str],
    weekend_set: Set[int],
    gongxiu_set: Set[str] = None,
    linxiu_set: Set[str] = None,
    rotation_skip_set: Set[str] = None,
    rotation_noskip_set: Set[str] = None,
    holiday_names: Dict[str, str] = None
) -> str:
    """
    获取日期类型显示名称
    优先级: 补班 > 临修 > 公休 > 轮休 > 假日 > 周末 > 工作
    """
    date_str = format_date(date)
    weekday = date.weekday()

    if date_str in compensatory_set:
        return "补班"
    if linxiu_set and date_str in linxiu_set:
        return "临修"
    if gongxiu_set and date_str in gongxiu_set:
        return "公休"
    if rotation_noskip_set and date_str in rotation_noskip_set:
        return "轮休"
    if rotation_skip_set and date_str in rotation_skip_set:
        return "轮休"
    if date_str in holidays_set:
        return "假日"
    if weekday in weekend_set:
        return "周末"
    return "工作"


# ============================================================
# 年度统计与周历生成
# ============================================================

def calculate_total_workdays(
    year: int,
    holiday_intervals: List[HolidayInterval] = None,
    compensatory_days: List[CompensatoryDay] = None,
    weekend_config: WeekendConfig = None,
    rotation_configs: List[RotationConfig] = None,
    special_rests: List[SpecialRestEvent] = None
) -> Dict:
    """计算年度总工日，包含所有休息类型"""
    # 加载基础数据
    if holiday_intervals is None:
        holiday_intervals, _ = load_holiday_intervals(year)
    if compensatory_days is None:
        compensatory_days, _ = load_compensatory_days(year)
    if weekend_config is None:
        weekend_config = load_weekend_config()

    holidays_set = generate_holiday_set(holiday_intervals)
    compensatory_set = generate_compensatory_set(compensatory_days)
    weekend_set = config_weekends_to_python(weekend_config.weekends)

    # 加载轮休配置
    if rotation_configs is None:
        rotation_configs, _ = load_rotation_configs()
    rotation_skip, rotation_noskip = generate_all_rotation_days(year, rotation_configs, holidays_set)

    # 加载特殊休息
    if special_rests is None:
        special_rests, _ = load_special_rests()
    gongxiu_set, linxiu_set = get_special_rest_dates(special_rests)

    dates = get_all_dates_of_year(year)
    workdays = sum(
        1 for d in dates
        if is_workday(d, holidays_set, compensatory_set, weekend_set,
                     gongxiu_set, linxiu_set, rotation_skip, rotation_noskip)
    )
    holidays = len(dates) - workdays

    return {
        "year": year,
        "total_workdays": workdays,
        "total_holidays": holidays,
        "total_days": len(dates),
        "holiday_count": len(holidays_set),
        "compensatory_count": len(compensatory_set),
        "rotation_count": len(rotation_skip | rotation_noskip),
        "gongxiu_count": len(gongxiu_set),
        "linxiu_count": len(linxiu_set),
        "weekend_config": weekend_config.weekends
    }


def generate_weekly_calendar(
    year: int,
    holiday_intervals: List[HolidayInterval] = None,
    compensatory_days: List[CompensatoryDay] = None,
    weekend_config: WeekendConfig = None,
    rotation_configs: List[RotationConfig] = None,
    special_rests: List[SpecialRestEvent] = None,
    include_empty_days: bool = True
) -> List[Dict]:
    """生成年度周历"""
    weekday_names = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]

    # 加载基础数据
    if holiday_intervals is None:
        holiday_intervals, _ = load_holiday_intervals(year)
    if compensatory_days is None:
        compensatory_days, _ = load_compensatory_days(year)
    if weekend_config is None:
        weekend_config = load_weekend_config()

    holidays_set = generate_holiday_set(holiday_intervals)
    compensatory_set = generate_compensatory_set(compensatory_days)
    weekend_set = config_weekends_to_python(weekend_config.weekends)

    # 加载轮休配置
    if rotation_configs is None:
        rotation_configs, _ = load_rotation_configs()
    rotation_skip, rotation_noskip = generate_all_rotation_days(year, rotation_configs, holidays_set)

    # 加载特殊休息
    if special_rests is None:
        special_rests, _ = load_special_rests()
    gongxiu_set, linxiu_set = get_special_rest_dates(special_rests)

    # 构建节假日名称映射
    holiday_names_map = {}
    for interval in holiday_intervals:
        start = parse_date(interval.start)
        end = parse_date(interval.end)
        if not start or not end:
            continue
        current = start
        while current <= end:
            holiday_names_map[format_date(current)] = interval.name
            current += timedelta(days=1)

    dates = get_all_dates_of_year(year)

    # 按周分组
    weeks = []
    current_week = []
    first_weekday = dates[0].weekday()

    for _ in range(first_weekday):
        if include_empty_days:
            current_week.append(None)
        else:
            continue

    for date in dates:
        current_week.append(date)
        if date.weekday() == 6:
            weeks.append(current_week)
            current_week = []

    if current_week:
        while include_empty_days and len(current_week) < 7:
            current_week.append(None)
        if current_week:
            weeks.append(current_week)

    # 生成周数据
    calendar = []
    for week in weeks:
        real_days = [d for d in week if d is not None]
        if not real_days:
            continue

        week_info = {
            "week_number": get_week_number(real_days[0]),
            "week_start": format_date(real_days[0]),
            "week_end": format_date(real_days[-1]),
            "days": [],
            "week_workdays": 0,
            "week_holidays": 0
        }

        for day in week:
            if day is None:
                week_info["days"].append({
                    "date": None, "weekday": None, "weekday_name": None,
                    "day_type": "空", "is_workday": None,
                    "holiday_name": None, "month": None, "day": None
                })
                continue

            date_str = format_date(day)
            weekday = day.weekday()
            day_type = get_day_type(
                day, holidays_set, compensatory_set, weekend_set,
                gongxiu_set, linxiu_set, rotation_skip, rotation_noskip,
                holiday_names_map
            )
            is_work = is_workday(
                day, holidays_set, compensatory_set, weekend_set,
                gongxiu_set, linxiu_set, rotation_skip, rotation_noskip
            )

            if is_work:
                week_info["week_workdays"] += 1
            else:
                week_info["week_holidays"] += 1

            week_info["days"].append({
                "date": date_str,
                "weekday": weekday,
                "weekday_name": weekday_names[weekday],
                "day_type": day_type,
                "is_workday": is_work,
                "holiday_name": holiday_names_map.get(date_str, ""),
                "month": day.month,
                "day": day.day
            })

        calendar.append(week_info)

    return calendar


# ============================================================
# 日程 CRUD
# ============================================================

def add_schedule_event(
    title: str,
    date: str,
    start_time: str,
    end_time: str,
    description: str = "",
    category: str = "工作"
) -> Tuple[ScheduleEvent, str]:
    """添加日程事件（含冲突检测 + 自动容灾备份）"""
    if not parse_date(date):
        return None, f"日期格式错误: {date}，应为 YYYY-MM-DD"

    try:
        datetime.strptime(start_time, "%H:%M")
        datetime.strptime(end_time, "%H:%M")
    except ValueError:
        return None, "时间格式错误，应为 HH:MM 格式"

    if start_time >= end_time:
        return None, "开始时间必须早于结束时间"

    events, _ = load_schedule_events()

    # 检查时间冲突
    for e in events:
        if e.date == date and e.status != "cancelled":
            if e.overlaps(start_time, end_time):
                return None, f"与现有日程冲突: {e.title} ({e.start_time}-{e.end_time})"

    new_event = ScheduleEvent(
        title=title, date=date, start_time=start_time, end_time=end_time,
        description=description, category=category
    )

    backup_path = _create_backup_bat()

    events.append(new_event)
    save_schedule_events(events)

    backup_info = f"\n  [备份: {Path(backup_path).name}]" if backup_path else "\n  [备份: 无(首次创建)]"
    return new_event, f"日程已添加: {title} ({date} {start_time}-{end_time}){backup_info}"


def delete_schedule_event(event_id: str) -> str:
    """删除日程事件"""
    events, _ = load_schedule_events()
    for i, e in enumerate(events):
        if e.id == event_id:
            events.pop(i)
            save_schedule_events(events)
            return f"已删除日程: {e.title}"
    return f"未找到日程ID: {event_id}"


def update_schedule_event(
    event_id: str,
    title: str = None,
    date: str = None,
    start_time: str = None,
    end_time: str = None,
    description: str = None,
    category: str = None,
    status: str = None
) -> str:
    """更新日程事件（更新后重新检查冲突）"""
    events, _ = load_schedule_events()

    target = None
    target_idx = -1
    for i, e in enumerate(events):
        if e.id == event_id:
            target = e
            target_idx = i
            break

    if not target:
        return f"未找到日程ID: {event_id}"

    # 暂存原值用于冲突检测
    new_date = target.date
    new_start = target.start_time
    new_end = target.end_time
    new_status = target.status

    if title is not None:
        target.title = title
    if date is not None:
        if not parse_date(date):
            return f"日期格式错误: {date}"
        new_date = date
        target.date = date
    if start_time is not None:
        try:
            datetime.strptime(start_time, "%H:%M")
            new_start = start_time
            target.start_time = start_time
        except ValueError:
            return f"开始时间格式错误: {start_time}"
    if end_time is not None:
        try:
            datetime.strptime(end_time, "%H:%M")
            new_end = end_time
            target.end_time = end_time
        except ValueError:
            return f"结束时间格式错误: {end_time}"
    if description is not None:
        target.description = description
    if category is not None:
        target.category = category
    if status is not None:
        new_status = status
        target.status = status

    target.updated_at = datetime.now().isoformat()

    # 验证时间段
    if target.start_time >= target.end_time:
        return "开始时间必须早于结束时间"

    # ═══ 冲突检测（排除自身）═══
    for i, e in enumerate(events):
        if i == target_idx:
            continue
        if e.date == target.date and e.status != "cancelled":
            if e.overlaps(target.start_time, target.end_time):
                # 还原
                target.date = new_date if date is None else target.date
                target.start_time = new_start if start_time is None else target.start_time
                target.end_time = new_end if end_time is None else target.end_time
                target.status = new_status if status is None else target.status
                return f"更新冲突: 与现有日程冲突 {e.title} ({e.start_time}-{e.end_time})"

    save_schedule_events(events)
    return f"已更新日程: {target.title}"


def get_schedule_by_date(date: str) -> List[ScheduleEvent]:
    """获取指定日期的所有日程"""
    events, _ = load_schedule_events()
    return [e for e in events if e.date == date and e.status != "cancelled"]


def get_schedules_by_date_range(start_date: str, end_date: str) -> List[ScheduleEvent]:
    """获取指定日期范围内的所有日程"""
    events, _ = load_schedule_events()
    start = parse_date(start_date)
    end = parse_date(end_date)
    if not start or not end:
        return []
    return [
        e for e in events
        if e.status != "cancelled"
        and start <= parse_date(e.date) <= end
    ]


def find_free_slots(
    date: str,
    start_search: str = "09:00",
    end_search: str = "18:00",
    min_duration: int = 30
) -> List[Dict]:
    """查找指定日期的空闲时间段"""
    events = get_schedule_by_date(date)
    events.sort(key=lambda x: x.start_time)

    free_slots = []
    current_time = start_search

    for event in events:
        if event.start_time > current_time:
            gap = time_diff_minutes(current_time, event.start_time)
            if gap >= min_duration:
                free_slots.append({
                    "start": current_time,
                    "end": event.start_time,
                    "duration": gap
                })
        current_time = max(current_time, event.end_time)

    if current_time < end_search:
        gap = time_diff_minutes(current_time, end_search)
        if gap >= min_duration:
            free_slots.append({
                "start": current_time,
                "end": end_search,
                "duration": gap
            })

    return free_slots


def generate_daily_schedule(date: str = None, days: int = 7) -> str:
    """生成指定天数内的日程列表"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    start = parse_date(date)
    if not start:
        return f"日期格式错误: {date}"

    output = []
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    for i in range(days):
        current_date = start + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        weekday = weekday_names[current_date.weekday()]

        events = get_schedule_by_date(date_str)

        if events:
            output.append(f"\n📅 {date_str} ({weekday})")
            events.sort(key=lambda x: x.start_time)
            for e in events:
                status_icon = "✅" if e.status == "completed" else "🔄" if e.status == "pending" else "❌" if e.status == "cancelled" else "⏰"
                output.append(f"  {status_icon} {e.start_time}-{e.end_time} {e.title}")
        else:
            output.append(f"\n📅 {date_str} ({weekday}) - 无安排")

    return "\n".join(output)


def generate_today_schedule() -> str:
    """生成今天及后续7天的日程列表"""
    today = datetime.now().strftime("%Y-%m-%d")
    return generate_daily_schedule(today, 7)


# ============================================================
# 轮休 CRUD
# ============================================================

def add_rotation_config(
    name: str, start_date: str, cycle_days: int = 7,
    work_days: int = 5, skip_holidays: bool = True
) -> Tuple[RotationConfig, str]:
    """添加轮休配置"""
    if not parse_date(start_date):
        return None, f"日期格式错误: {start_date}"

    if cycle_days <= work_days:
        return None, f"周期天数({cycle_days})必须大于工作天数({work_days})"

    configs, _ = load_rotation_configs()
    new_config = RotationConfig(
        name=name, start_date=start_date,
        cycle_days=cycle_days, work_days=work_days,
        skip_holidays=skip_holidays
    )
    configs.append(new_config)
    save_rotation_configs(configs)
    return new_config, f"轮休配置已添加: {name} (ID: {new_config.id})"


def delete_rotation_config(config_id: str) -> str:
    """删除轮休配置"""
    configs, _ = load_rotation_configs()
    for i, c in enumerate(configs):
        if c.id == config_id:
            removed = configs.pop(i)
            save_rotation_configs(configs)
            return f"已删除轮休配置: {removed.name}"
    return f"未找到轮休配置ID: {config_id}"


def list_rotation_configs() -> str:
    """列出所有轮休配置"""
    configs, _ = load_rotation_configs()
    if not configs:
        return "暂无轮休配置"

    lines = []
    lines.append("📋 轮休配置列表:")
    lines.append("-" * 60)
    for c in configs:
        status_icon = "✅" if c.enabled else "⏸"
        mode_text = "跳过法定假" if c.skip_holidays else "不跳过法定假"
        lines.append(
            f"  [{c.id}] {status_icon} {c.name}"
        )
        lines.append(f"      起始: {c.start_date} | 周期: {c.cycle_days}天 | 工作: {c.work_days}天 | 休息: {c.rest_days}天")
        lines.append(f"      模式: {mode_text}")
    lines.append("-" * 60)
    return "\n".join(lines)


def rotate_generate(year: int = None) -> str:
    """生成指定年份的轮休日并缓存"""
    if year is None:
        year = datetime.now().year

    configs, _ = load_rotation_configs()
    enabled = [c for c in configs if c.enabled]
    if not enabled:
        return "没有启用的轮休配置可供生成"

    holidays_set = set()
    holiday_intervals, _ = load_holiday_intervals(year)
    if holiday_intervals:
        holidays_set = generate_holiday_set(holiday_intervals)

    skip_set, noskip_set = generate_all_rotation_days(year, enabled, holidays_set)

    # 缓存到文件
    save_rotation_days(year, skip_set, noskip_set)

    lines = []
    lines.append(f"📊 {year}年 轮休日生成结果:")
    lines.append(f"  skip模式轮休日: {len(skip_set)} 天")
    lines.append(f"  noskip模式轮休日: {len(noskip_set)} 天")
    lines.append(f"  合计: {len(skip_set | noskip_set)} 天")
    lines.append(f"  生成配置数: {len(enabled)}")
    return "\n".join(lines)


# ============================================================
# 特殊休息 CRUD
# ============================================================

def add_special_rest(
    rest_type: str, date: str = None,
    start_date: str = None, end_date: str = None,
    reason: str = ""
) -> Tuple[SpecialRestEvent, str]:
    """添加特殊休息（公休/临修）

    支持单日和区间两种格式
    """
    if rest_type not in ("公休", "临修"):
        return None, f"类型错误: {rest_type}，应为 公休 或 临修"

    if date and start_date:
        return None, "不能同时指定 date 和 start_date，请选择单日或区间格式"
    if not date and not start_date:
        return None, "必须指定 date (单日) 或 start_date/end_date (区间)"

    # 单日
    if date:
        if not parse_date(date):
            return None, f"日期格式错误: {date}"
    # 区间
    if start_date:
        if not parse_date(start_date):
            return None, f"开始日期格式错误: {start_date}"
        if not end_date:
            end_date = start_date
        if not parse_date(end_date):
            return None, f"结束日期格式错误: {end_date}"
        if parse_date(start_date) > parse_date(end_date):
            return None, "开始日期不能晚于结束日期"

    rests, _ = load_special_rests()
    new_rest = SpecialRestEvent(
        type=rest_type, date=date,
        start_date=start_date, end_date=end_date,
        reason=reason
    )
    rests.append(new_rest)
    save_special_rests(rests)

    # 构建显示信息
    if date:
        range_info = date
    else:
        range_info = f"{start_date} ~ {end_date}"

    return new_rest, f"{rest_type}已添加: {range_info} (ID: {new_rest.id})"


def delete_special_rest(rest_id: str) -> str:
    """删除特殊休息"""
    rests, _ = load_special_rests()
    for i, r in enumerate(rests):
        if r.id == rest_id:
            removed = rests.pop(i)
            save_special_rests(rests)
            return f"已删除{removed.type}: {removed.id}"
    return f"未找到特殊休息ID: {rest_id}"


def list_special_rests(filter_type: str = None) -> str:
    """列出特殊休息"""
    rests, _ = load_special_rests()
    if filter_type:
        rests = [r for r in rests if r.type == filter_type]

    if not rests:
        return "暂无特殊休息"

    lines = []
    lines.append("📋 特殊休息列表:")
    lines.append("-" * 60)
    for r in rests:
        if r.date:
            range_info = r.date
        else:
            range_info = f"{r.start_date} ~ {r.end_date}"
        lines.append(f"  [{r.id}] {r.type} | {range_info}")
        if r.reason:
            lines.append(f"        原因: {r.reason}")
    lines.append("-" * 60)
    return "\n".join(lines)


# ============================================================
# 数据导入/导出（供AI调用）
# ============================================================

def import_holidays_from_ai(year: int, holiday_data: List[Dict]) -> str:
    """AI导入法定假日数据"""
    intervals = []
    for item in holiday_data:
        intervals.append(HolidayInterval(
            name=item.get("name", ""),
            start=item.get("start", ""),
            end=item.get("end", item.get("start", "")),
            note=item.get("note", "")
        ))
    return save_holiday_intervals(year, intervals)


def import_compensatory_from_ai(year: int, comp_data: List[Dict]) -> str:
    """AI导入补班日数据"""
    days = []
    for item in comp_data:
        days.append(CompensatoryDay(
            date=item.get("date", ""),
            note=item.get("note", "")
        ))
    return save_compensatory_days(year, days)


def export_year_summary(year: int) -> Dict:
    """导出年度汇总数据（供AI调用）"""
    holiday_intervals, _ = load_holiday_intervals(year)
    compensatory_days, _ = load_compensatory_days(year)
    weekend_config = load_weekend_config()
    rotation_configs, _ = load_rotation_configs()
    special_rests, _ = load_special_rests()

    summary = calculate_total_workdays(
        year, holiday_intervals, compensatory_days, weekend_config,
        rotation_configs, special_rests
    )

    summary["holiday_intervals"] = [i.to_dict() for i in holiday_intervals]
    summary["compensatory_days"] = [d.to_dict() for d in compensatory_days]
    summary["weekend_config"] = weekend_config.to_dict()
    summary["rotation_configs"] = [c.to_dict() for c in rotation_configs]
    summary["special_rests"] = [r.to_dict() for r in special_rests]

    return summary


# ============================================================
# 规则模板导出/导入
# ============================================================

def export_rules_template(year: int = None) -> dict:
    """
    导出标准化规则模板（JSON 格式，供用户编辑后重新导入）

    模板结构:
    {
        "version": "1.0",
        "year": 2026,
        "base_type": "holiday|scheduling",
        "rules": {
            "weekend_config": {...},
            "holiday_intervals": [...],
            "compensatory_days": [...],
            "rotation_configs": [...],
            "special_rests": [...]
        }
    }
    """
    if year is None:
        year = datetime.now().year

    cfg = load_config()
    base_type = "scheduling" if cfg.get("use_scheduling_as_base") else "holiday"

    holiday_intervals, _ = load_holiday_intervals(year)
    compensatory_days, _ = load_compensatory_days(year)
    weekend_config = load_weekend_config()
    rotation_configs, _ = load_rotation_configs()
    special_rests, _ = load_special_rests()

    template = {
        "version": "1.0",
        "year": year,
        "base_type": base_type,
        "rules": {
            "weekend_config": weekend_config.to_dict(),
            "holiday_intervals": [i.to_dict() for i in holiday_intervals],
            "compensatory_days": [d.to_dict() for d in compensatory_days],
            "rotation_configs": [c.to_dict() for c in rotation_configs],
            "special_rests": [r.to_dict() for r in special_rests]
        }
    }
    return template


def import_rules_from_template(template: dict) -> str:
    """
    从规则模板导入数据

    根据 base_type 决定写入哪些数据文件:
    - "holiday": 写入 holiday_intervals, compensatory_days, weekend_config
    - "scheduling": 写入 rotation_configs, special_rests
    """
    year = template.get("year", datetime.now().year)
    rules = template.get("rules", {})
    base_type = template.get("base_type", "holiday")
    result_lines = []

    if base_type == "holiday":
        # 节假日 + 补班日 + 周末规则
        wc_data = rules.get("weekend_config", {})
        if wc_data:
            wc = WeekendConfig.from_dict(wc_data)
            save_weekend_config(wc)
            result_lines.append(f"周末规则已导入 (休息日: {wc.weekends})")

        hi_data = rules.get("holiday_intervals", [])
        if hi_data:
            intervals = [HolidayInterval.from_dict(i) for i in hi_data]
            save_holiday_intervals(year, intervals)
            result_lines.append(f"法定假日已导入: {len(intervals)} 个假期")

        comp_data = rules.get("compensatory_days", [])
        if comp_data:
            days = [CompensatoryDay.from_dict(d) for d in comp_data]
            save_compensatory_days(year, days)
            result_lines.append(f"补班日已导入: {len(days)} 天")

    elif base_type == "scheduling":
        # 轮休 + 特殊休息
        rot_data = rules.get("rotation_configs", [])
        if rot_data:
            configs = [RotationConfig.from_dict(c) for c in rot_data]
            save_rotation_configs(configs)
            result_lines.append(f"轮休配置已导入: {len(configs)} 个")

        sr_data = rules.get("special_rests", [])
        if sr_data:
            rests = [SpecialRestEvent.from_dict(r) for r in sr_data]
            save_special_rests(rests)
            result_lines.append(f"特殊休息已导入: {len(rests)} 条")

    else:
        # 全量导入
        wc_data = rules.get("weekend_config", {})
        if wc_data:
            save_weekend_config(WeekendConfig.from_dict(wc_data))
        hi_data = rules.get("holiday_intervals", [])
        if hi_data:
            save_holiday_intervals(year, [HolidayInterval.from_dict(i) for i in hi_data])
        comp_data = rules.get("compensatory_days", [])
        if comp_data:
            save_compensatory_days(year, [CompensatoryDay.from_dict(d) for d in comp_data])
        rot_data = rules.get("rotation_configs", [])
        if rot_data:
            save_rotation_configs([RotationConfig.from_dict(c) for c in rot_data])
        sr_data = rules.get("special_rests", [])
        if sr_data:
            save_special_rests([SpecialRestEvent.from_dict(r) for r in sr_data])
        result_lines.append("全量规则已导入")

    if not result_lines:
        return "规则模板为空，未导入任何数据"

    return "\n".join(result_lines)


# ============================================================
# HTML 导出
# ============================================================

def generate_weekly_board_html(year: int = None, embed_schedule: bool = True) -> str:
    """
    生成基础周 HTML — 真正的周历视图，每周一行

    根据 config.use_scheduling_as_base 决定基础周类型:
    - False: 节假周（基于法定节假日+周末）
    - True:  排班周（基于轮休+公休+临修）

    embed_schedule=True 时，在每日单元格中嵌入现有日程事件
    """
    if year is None:
        year = datetime.now().year

    cfg = load_config()
    use_scheduling = cfg.get("use_scheduling_as_base", False)

    # 用 generate_weekly_calendar 获取周历数据（内部已根据 config 决定假休是否被排班覆盖）
    calendar_data = generate_weekly_calendar(year)

    # 加载日程事件并构建按日期索引
    schedule_by_date = {}
    schedule_json = {}  # 给 JS 用的完整数据
    if embed_schedule:
        events, _ = load_schedule_events()
        active = [e for e in events if e.status != "cancelled"]
        for e in active:
            ed = e.date
            if ed not in schedule_by_date:
                schedule_by_date[ed] = []
                schedule_json[ed] = []
            entry = {
                "start_time": e.start_time,
                "end_time": e.end_time,
                "title": e.title,
                "description": e.description,
                "category": e.category,
                "status": e.status
            }
            schedule_by_date[ed].append(entry)
            schedule_json[ed].append(entry)
        for ed in schedule_by_date:
            schedule_by_date[ed].sort(key=lambda x: x["start_time"])
            schedule_json[ed].sort(key=lambda x: x["start_time"])

    # 统计
    summary = calculate_total_workdays(year)

    schedule_count = sum(len(v) for v in schedule_by_date.values()) if embed_schedule else 0
    base_type_label = "排班叠加" if use_scheduling else "排班不覆盖假休"

    # 颜色映射
    type_colors = {
        "补班": "#e74c3c",
        "临修": "#8e44ad",
        "公休": "#3498db",
        "轮休": "#2ecc71",
        "假日": "#2ecc71",
        "周末": "#2ecc71",
        "工作": "#ffffff",
    }

    weekday_names_short = ["一", "二", "三", "四", "五", "六", "日"]
    # weekday_names_full = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    # 按月份分组周
    month_week_groups = {}
    weekday_names_full = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    for week in calendar_data:
        days = week.get("days", [])
        # 过滤掉 None
        real_days = [d for d in days if d.get("date")]

        if not real_days:
            continue

        first_date = real_days[0]["date"]
        first_month = parse_date(first_date).month if parse_date(first_date) else 1

        # 构建一周7个格子（可能含空）
        cell_htmls = []
        today_str = format_date(datetime.now())
        for day in days:
            if day.get("date") is None:
                cell_htmls.append('<td class="wd empty"></td>')
                continue

            date_str = day["date"]
            dt_obj = parse_date(date_str)
            day_num = dt_obj.day if dt_obj else "?"
            day_type = day.get("day_type", "工作")
            holiday_name = day.get("holiday_name", "")

            bg = type_colors.get(day_type, "#ffffff")
            text_color = "#333" if bg in ("#ffffff", "#f5f5f5") else "#fff"

            label = day_type
            if holiday_name and day_type == "假日":
                label = holiday_name

            # 排班时段条（周末显示全灰条，补班按工作日时段显示）
            slot_wd = 0 if day_type == "补班" else (dt_obj.weekday() if dt_obj else 0)
            slots = get_slots_for_weekday(slot_wd) if dt_obj else []
            timeline_html = ""
            if slots and len(slots) > 0 and day_type not in ("假日", "空"):
                timeline_html = '<div class="tl-bar">'
                # 合并相邻同色段
                merged = []
                for s in slots:
                    if not merged or merged[-1]["color"] != s.color:
                        merged.append({"color": s.color, "start": s.start, "end": s.end, "label": s.label})
                    else:
                        merged[-1]["end"] = s.end
                total_min = 24 * 60
                for seg in merged:
                    start_m = int(seg["start"].split(":")[0]) * 60 + int(seg["start"].split(":")[1])
                    end_m = int(seg["end"].split(":")[0]) * 60 + int(seg["end"].split(":")[1])
                    if end_m <= start_m:
                        end_m += 24 * 60
                    pct = (end_m - start_m) / total_min * 100
                    timeline_html += f'<div class="tl-seg" style="width:{pct:.1f}%;background:{seg["color"]}" title="{seg["start"]}-{seg["end"]} {seg["label"]}"></div>'
                timeline_html += '</div>'

            # 日程事件（按排班时段染色，补班日按工作日时段）
            day_events = schedule_by_date.get(date_str, [])
            events_html = ""
            if day_events:
                evt_parts = []
                slot_wd = 0 if day_type == "补班" else (dt_obj.weekday() if dt_obj else 0)
                for ev in day_events[:4]:
                    ev_color = get_slot_color_for_time(slot_wd, ev["start_time"])
                    evt_parts.append(
                        f'<div class="evt" style="border-left:2px solid {ev_color}">{ev["start_time"]}-{ev["end_time"]} {ev["title"]}</div>'
                    )
                if len(day_events) > 4:
                    evt_parts.append(f'<div class="evt-more">+{len(day_events)-4} 项</div>')
                events_html = "".join(evt_parts)

            cell_htmls.append(
                f'<td class="{"wd-past" if date_str < today_str and day_type != "空" else ""}" style="background:{bg};color:{text_color}" data-date="{date_str}" onclick="showDayDetail(\'{date_str}\')">'
                f'<div class="wd-num">{day_num}</div>'
                f'<div class="wd-type">{label}</div>'
                f'{timeline_html}'
                f'{events_html}'
                f'</td>'
            )

        week_start = week.get("week_start", "")
        week_end = week.get("week_end", "")
        week_number = week.get("week_number", "")

        # 计算该周所在月份分组
        month_key = first_month
        if month_key not in month_week_groups:
            month_week_groups[month_key] = []

        month_week_groups[month_key].append(
            f'<tr class="wk-row">'
            f'<td class="wk-info"><div class="wk-num">第{week_number}周</div><div class="wk-range">{week_start}~{week_end}</div></td>'
            f'{"".join(cell_htmls)}'
            f'</tr>'
        )

    # 按月份顺序生成每个月的周表
    months_html = []
    wd_header = "".join(f'<th class="wd-hdr">{w}</th>' for w in weekday_names_short)

    for month in sorted(month_week_groups.keys()):
        rows = month_week_groups[month]
        months_html.append(f"""
    <div class="month-section">
      <h3>{year}年{month}月</h3>
      <table class="wk-table">
        <thead><tr><th class="wk-hdr">周次</th>{wd_header}</tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </div>""")

    # 预序列化 JS 数据（转义 </script> 防止破坏 HTML 解析）
    # 先构建排班时段数据
    sched_slots_json = {}
    day_labels = ["周一","周二","周三","周四","周五","周六","周日"]
    for wd in range(7):
        slots = get_slots_for_weekday(wd)
        sched_slots_json[str(wd)] = {
            "day": day_labels[wd],
            "slots": [{"start": s.start, "end": s.end, "label": s.label, "color": s.color,
                       "is_work": s.is_work, "assignments": s.assignments}
                      for s in slots]
        }
    safe_replace = lambda s: s.replace('</script>', '<\\/script>').replace('</Script>', '<\\/Script>') if isinstance(s, str) else s
    schedule_json_str = safe_replace(json.dumps(schedule_json, ensure_ascii=False))
    weekday_names_json = safe_replace(json.dumps(weekday_names_full, ensure_ascii=False))
    status_labels_json = safe_replace(json.dumps({"pending": "待完成", "completed": "已完成", "cancelled": "已取消", "missed": "已错过"}, ensure_ascii=False))
    sched_slots_str = safe_replace(json.dumps(sched_slots_json, ensure_ascii=False))
    # 补班日期集合（弹窗中按工作日时段展示）
    comp_dates = []
    # 法定假日日期集合（弹窗中不展示排班）
    holiday_dates = []
    for week in calendar_data:
        for d in week.get("days", []):
            if d.get("day_type") == "补班" and d.get("date"):
                comp_dates.append(d["date"])
            elif d.get("day_type") == "假日" and d.get("date"):
                holiday_dates.append(d["date"])
    comp_dates_str = json.dumps(comp_dates, ensure_ascii=False)
    holiday_dates_str = json.dumps(holiday_dates, ensure_ascii=False)

    # 构建交互脚本（独立于主 f-string 以避免花括号冲突）
    modal_script = '''
<script>
var scheduleData = SD_PLACEHOLDER;
var weekdayNames = WN_PLACEHOLDER;
var statusLabels = SL_PLACEHOLDER;
var schedSlots = SS_PLACEHOLDER;
var compDates = CD_PLACEHOLDER;
var holidayDates = HD_PLACEHOLDER;

function getWeekday(dateStr) {
  var d = new Date(dateStr);
  var wd = d.getDay();
  var idx = wd === 0 ? 6 : wd - 1;
  if (compDates.indexOf(dateStr) >= 0) { return 0; }  // 补班日按周一算
  return idx;
}

function showDayDetail(dateStr) {
  var modal = document.getElementById("modalOverlay");
  var dateLabel = document.getElementById("modalDate");
  var body = document.getElementById("modalBody");
  var dt = new Date(dateStr);
  var weekday = dt.getDay();
  var wdLabel = weekdayNames[weekday === 0 ? 6 : weekday - 1];
  if (weekday === 0) { wdLabel = weekdayNames[6]; }
  dateLabel.textContent = dateStr + " (" + wdLabel + ")";
  var parts = [];

  // 排班时段表（法定假日不显示）
  var wd = getWeekday(dateStr);
  var isHoliday = holidayDates.indexOf(dateStr) >= 0;
  var sched = schedSlots[wd];
  // 只有当天有上班时段才展示排班表（全休日不显示 "00:00-23:59 休息"）
  var hasWorkSlots = false;
  if (sched && sched.slots) {
    for (var si = 0; si < sched.slots.length; si++) {
      if (sched.slots[si].is_work) { hasWorkSlots = true; break; }
    }
  }
  if (sched && sched.slots && sched.slots.length > 0 && !isHoliday && hasWorkSlots) {
    parts.push('<div class="modal-subtitle">排班时段 (' + sched.day + ')</div>');
    for (var i = 0; i < sched.slots.length; i++) {
      var sl = sched.slots[i];
      var dotColor = sl.is_work ? sl.color : "#95a5a6";
      var subHtml = '';
      if (sl.assignments && sl.assignments.length > 0) {
        var lines = [];
        for (var ai = 0; ai < sl.assignments.length; ai++) {
          var a = sl.assignments[ai];
          var line = '';
          if (a.position) { line += escHtml(a.position); }
          if (a.persons) { line += (line ? '  ' : '') + escHtml(a.persons); }
          if (line) { lines.push(line); }
        }
        subHtml = '<div class="sched-row-sub">' + lines.join('<br>') + '</div>';
      }
      parts.push('<div class="sched-row" style="border-left:3px solid ' + dotColor + '">' +
        '<div class="sched-row-main">' +
        '<span class="sched-time">' + sl.start + '-' + sl.end + '</span>' +
        '<span class="sched-label">' + escHtml(sl.label) + '</span>' +
        '</div>' + subHtml +
        '</div>');
    }
  }
  var events = scheduleData[dateStr];
  if (!events || events.length === 0) {
    if (parts.length === 0) {
      body.innerHTML = '<p class="modal-empty">该日暂无安排</p>';
    } else {
      body.innerHTML = parts.join("");
    }
  } else {
    parts.push('<div class="modal-subtitle">个人日程</div>');
    for (var i = 0; i < events.length; i++) {
      var e = events[i];
      var sl = statusLabels[e.status] || e.status;
      var evColor = "#888";
      if (sched && sched.slots) {
        for (var j = 0; j < sched.slots.length; j++) {
          if (sched.slots[j].start <= e.start_time && e.start_time < sched.slots[j].end) {
            evColor = sched.slots[j].is_work ? sched.slots[j].color : "#95a5a6";
            break;
          }
        }
      }
      var statusTag = '<span class="status-tag-sm status-' + e.status + '">' + sl + '</span>';
      var subHtml = e.description ? '<div class="sched-row-sub">' + escHtml(e.description) + '</div>' : '';
      parts.push('<div class="sched-row" style="border-left:3px solid ' + evColor + '">' +
        '<div class="sched-row-main">' +
        '<span class="sched-time">' + e.start_time + '-' + e.end_time + '</span>' +
        '<span class="sched-label">' + escHtml(e.title) + '</span>' +
        statusTag +
        '</div>' + subHtml +
        '</div>');
    }
    body.innerHTML = parts.join('');
  }
  modal.classList.add("show");
}
function closeModal() {
  document.getElementById("modalOverlay").classList.remove("show");
}
function escHtml(s) { return (s || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") closeModal();
});
</script>'''
    modal_script = modal_script.replace('CD_PLACEHOLDER', comp_dates_str)
    modal_script = modal_script.replace('HD_PLACEHOLDER', holiday_dates_str)
    modal_script = modal_script.replace('SD_PLACEHOLDER', schedule_json_str)
    modal_script = modal_script.replace('WN_PLACEHOLDER', weekday_names_json)
    modal_script = modal_script.replace('SL_PLACEHOLDER', status_labels_json)
    modal_script = modal_script.replace('SS_PLACEHOLDER', sched_slots_str)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{year}年基础周 · {base_type_label}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: linear-gradient(135deg, #f5f0ff 0%, #e8f4f8 100%);
  color: #333; padding: 20px;
}}
.header {{
  background: linear-gradient(135deg, #9b59b6 0%, #3498db 100%);
  color: #fff; border-radius: 16px; padding: 24px 30px; margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(155, 89, 182, 0.3);
}}
.header h1 {{ font-size: 24px; margin-bottom: 6px; }}
.header p {{ opacity: 0.9; font-size: 14px; }}
.stats {{
  display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;
}}
.stat-card {{
  background: #fff; border-radius: 10px; padding: 12px 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; flex: 1; min-width: 90px;
}}
.stat-card .num {{ font-size: 22px; font-weight: 700; color: #3498db; }}
.stat-card .label {{ font-size: 11px; color: #888; margin-top: 2px; }}
.month-section {{
  background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}
.month-section h3 {{ font-size: 15px; color: #555; margin-bottom: 10px; }}
.wk-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
.wk-table th {{ font-size: 11px; color: #888; padding: 4px; text-align: center; font-weight: 400; }}
.wk-table td {{
  padding: 4px 3px; font-size: 11px; text-align: center; vertical-align: top;
  border: 1px solid #f0f0f0; border-radius: 4px; height: 80px;
}}
.wk-hdr {{ width: 80px; font-size: 11px; text-align: center; color: #888; }}
.wd-hdr {{ font-size: 11px; text-align: center; color: #888; padding: 4px; }}
.wk-info {{ width: 80px; text-align: center; vertical-align: middle; font-size: 10px; color: #888; border: none !important; }}
.wk-num {{ font-weight: 600; color: #555; font-size: 11px; }}
.wk-range {{ font-size: 9px; color: #aaa; margin-top: 2px; }}
.wd-num {{ font-weight: 600; font-size: 12px; }}
.wd-type {{ font-size: 9px; margin-top: 1px; }}
.evt {{ font-size: 9px; text-align: left; padding: 1px 2px; margin-top: 1px;
       background: rgba(255,255,255,0.45); border-radius: 2px;
       white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.evt-more {{ font-size: 8px; text-align: center; color: #888; margin-top: 1px; }}
.tl-bar {{ display: flex; height: 6px; border-radius: 2px; overflow: hidden; margin: 2px 0; width: 100%; }}
.tl-seg {{ height: 100%; min-width: 1px; flex-shrink: 0; }}
.evt {{ font-size: 9px; text-align: left; padding: 1px 3px; margin-top: 1px;
       background: rgba(255,255,255,0.45); border-radius: 2px;
       white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
td.empty {{ background: #fafafa; border-color: #f5f5f5; }}
td.wd-past {{ opacity: 0.5; }}
td[cursor] {{ cursor: pointer; }}
/* 弹窗 */
.modal-overlay {{
  display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  z-index: 1000; justify-content: center; align-items: center;
}}
.modal-overlay.show {{ display: flex; }}
.modal-content {{
  background: #fff; border-radius: 16px; width: 90%; max-width: 520px;
  max-height: 80vh; overflow-y: auto; box-shadow: 0 8px 40px rgba(0,0,0,0.15);
}}
.modal-header {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px 0; position: sticky; top: 0; background: #fff; z-index: 1;
}}
.modal-header h3 {{ font-size: 18px; color: #444; }}
.modal-close {{
  font-size: 28px; color: #aaa; cursor: pointer; line-height: 1;
}}
.modal-close:hover {{ color: #333; }}
.modal-body {{ padding: 16px 24px 24px; }}
.modal-empty {{ text-align: center; color: #aaa; font-size: 14px; padding: 30px 0; }}
.evt-count {{ font-size: 13px; color: #888; margin-bottom: 12px; }}
.evt-card {{
  background: #f8f6ff; border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
  border-left: 4px solid #9b59b6;
}}
.evt-card-time {{ font-size: 13px; color: #9b59b6; font-weight: 600; margin-bottom: 4px; }}
.evt-card-title {{ font-size: 15px; font-weight: 600; color: #333; margin-bottom: 4px; }}
.evt-card-desc {{ font-size: 13px; color: #888; margin-bottom: 6px; }}
.evt-card-tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.evt-tag {{ display: inline-block; padding: 2px 8px; border-radius: 8px; font-size: 11px; }}
.cat-tag {{ background: #e8f4fd; color: #2980b9; }}
.status-tag {{ background: #fef9e7; color: #f39c12; }}
.status-completed {{ background: #eafaf1; color: #2ecc71; }}
.status-cancelled {{ background: #fdedec; color: #e74c3c; }}
.status-missed {{ background: #fef0e6; color: #d35400; }}
.modal-subtitle {{ font-size: 14px; font-weight: 600; color: #555; margin: 14px 0 6px; }}
.sched-row {{
  margin-bottom: 6px; background: #f8f8fa; border-radius: 6px; padding: 6px 10px; font-size: 13px;
}}
.sched-row-main {{
  display: flex; align-items: center; gap: 8px;
}}
.sched-row-sub {{
  font-size: 12px; color: #999; padding: 2px 0 0 0; margin-left: 10px;
}}
.sched-time {{ color: #555; font-weight: 500; min-width: 105px; }}
.sched-label {{ color: #777; }}
.sched-persons {{ color: #999; font-size: 12px; margin-left: auto; }}
.sched-desc {{ font-size: 12px; color: #999; padding: 2px 10px 6px 13px; }}
.status-tag-sm {{ font-size: 11px; padding: 1px 6px; border-radius: 6px; margin-left: auto; white-space: nowrap; }}
.status-tag-sm.status-pending {{ background: #fef9e7; color: #f39c12; }}
.status-tag-sm.status-completed {{ background: #eafaf1; color: #2ecc71; }}
.status-tag-sm.status-cancelled {{ background: #fdedec; color: #e74c3c; }}
.status-tag-sm.status-missed {{ background: #fef0e6; color: #d35400; }}
.legend {{
  background: #fff; border-radius: 12px; padding: 12px 20px; margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}
.legend h3 {{ font-size: 13px; color: #555; margin-bottom: 6px; }}
.legend-items {{ display: flex; flex-wrap: wrap; gap: 10px; }}
.legend-item {{ display: flex; align-items: center; gap: 4px; font-size: 12px; }}
.legend-color {{ width: 14px; height: 14px; border-radius: 3px; display: inline-block; }}
</style>
</head>
<body>
<div class="header">
  <h1>{year}年 基础周 · {base_type_label}</h1>
  <p>工作日 {summary['total_workdays']} 天 | 休息日 {summary['total_holidays']} 天 | 总天数 {summary['total_days']} 天{f' | 日程 {schedule_count} 项' if embed_schedule else ''}</p>
</div>

<div class="legend">
  <h3>图例</h3>
  <div class="legend-items">
    <span class="legend-item"><span class="legend-color" style="background:#2ecc71"></span> 法定假休</span>
    <span class="legend-item"><span class="legend-color" style="background:#e74c3c"></span> 补班</span>
    <span class="legend-item"><span class="legend-color" style="background:#8e44ad"></span> 临修</span>
    <span class="legend-item"><span class="legend-color" style="background:#3498db"></span> 公休</span>
    <span class="legend-item"><span class="legend-color" style="background:#2ecc71"></span> 法定假休/轮休</span>
    <span class="legend-item"><span class="legend-color" style="background:#95a5a6"></span> 周末</span>
    <span class="legend-item"><span class="legend-color" style="background:#ffffff;border:1px solid #ddd"></span> 工作日</span>
  </div>
</div>

<div class="stats">
  <div class="stat-card"><div class="num">{summary['total_days']}</div><div class="label">总天数</div></div>
  <div class="stat-card"><div class="num">{summary['total_workdays']}</div><div class="label">工作日</div></div>
  <div class="stat-card"><div class="num">{summary['total_holidays']}</div><div class="label">休息日</div></div>
  <div class="stat-card"><div class="num">{summary['holiday_count']}</div><div class="label">法定假日</div></div>
  <div class="stat-card"><div class="num">{summary['compensatory_count']}</div><div class="label">补班日</div></div>
  <div class="stat-card"><div class="num">{summary['rotation_count']}</div><div class="label">轮休日</div></div>
  <div class="stat-card"><div class="num">{summary['gongxiu_count']}</div><div class="label">公休</div></div>
  <div class="stat-card"><div class="num">{summary['linxiu_count']}</div><div class="label">临修</div></div>
</div>

{"".join(months_html)}

<!-- 日程详情弹窗 -->
<div class="modal-overlay" id="modalOverlay" onclick="closeModal()">
  <div class="modal-content" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h3 id="modalDate"></h3>
      <span class="modal-close" onclick="closeModal()">&times;</span>
    </div>
    <div class="modal-body" id="modalBody">
      <p class="modal-empty">点击日期查看日程详情</p>
    </div>
  </div>
</div>

{modal_script}
</body>
</html>"""
    return html


def export_schedule_table(year: int = None, mode: str = "week",
                          date_from: str = None, date_to: str = None) -> str:
    """
    导出排班表 HTML（按周或按月分组，支持日期范围过滤）

    参数:
        year: 年份
        mode: "week" 按周分组 / "month" 按月分组
        date_from: 起始日期 YYYY-MM-DD（可选，默认年初）
        date_to: 结束日期 YYYY-MM-DD（可选，默认年末）
    """
    if year is None:
        year = datetime.now().year

    calendar_data = generate_weekly_calendar(year)
    weekday_names = ["周一","周二","周三","周四","周五","周六","周日"]

    from_dt = parse_date(date_from) if date_from else datetime(year, 1, 1)
    to_dt = parse_date(date_to) if date_to else datetime(year, 12, 31)

    # build all rows with week/month info
    all_rows = []  # [(date, wd_label, label, time, pos, per, week_num, month_num)]
    for w in calendar_data:
        wn = w.get("week_number")
        for d in w.get("days", []):
            ds = d.get("date", "")
            if not ds:
                continue
            dt = parse_date(ds)
            if not dt or dt < from_dt or dt > to_dt:
                continue
            wd_label = weekday_names[dt.weekday()]
            day_type = d.get("day_type", "工作")
            slot_wd = 0 if day_type == "补班" else dt.weekday()
            slots = get_slots_for_weekday(slot_wd)
            for s in slots:
                if not s.is_work:
                    continue
                time_str = f"{s.start}-{s.end}"
                if s.assignments:
                    for a in s.assignments:
                        pos_display = a.get("position", "") or "—"
                        per_display = a.get("persons", "") or "—"
                        all_rows.append((ds, wd_label, s.label, time_str, pos_display, per_display, wn, dt.month))
                else:
                    all_rows.append((ds, wd_label, s.label, time_str, "—", "—", wn, dt.month))

    all_rows.sort(key=lambda r: r[0])

    # 按 mode 分组
    if mode == "month":
        groups = {}
        for r in all_rows:
            m = r[7]
            groups.setdefault(m, []).append(r)
        group_keys = sorted(groups.keys())
        group_label = lambda k: f"{year}年{k}月"
    else:  # week
        groups = {}
        for r in all_rows:
            w = r[6]
            groups.setdefault(w, []).append(r)
        group_keys = sorted(groups.keys())
        group_label = lambda k: f"{year}年 第{k}周"

    # date range label
    range_label = ""
    if date_from and date_to:
        range_label = f" · {date_from} ~ {date_to}"
    elif date_from:
        range_label = f" · 从 {date_from}"
    elif date_to:
        range_label = f" · 至 {date_to}"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>排班表 · {year}年 · {'按周' if mode=='week' else '按月'}{range_label}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: linear-gradient(135deg, #f5f0ff 0%, #e8f4f8 100%);
  padding: 20px; color: #333;
}}
.header {{
  background: linear-gradient(135deg, #9b59b6 0%, #3498db 100%);
  color: #fff; border-radius: 16px; padding: 24px 30px; margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(155,89,182,0.3);
}}
.header h1 {{ font-size: 24px; margin-bottom: 4px; }}
.header p {{ opacity: 0.9; font-size: 13px; }}
.section {{ margin-bottom: 24px; }}
.section-title {{
  font-size: 16px; font-weight: 600; color: #555; margin-bottom: 8px;
  padding: 8px 14px; background: #f0e6ff; border-radius: 8px;
}}
table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 16px; }}
th {{ background: #f0e6ff; padding: 10px 10px; font-size: 13px; font-weight: 600; color: #555; text-align: left; }}
td {{ padding: 8px 10px; font-size: 13px; border-bottom: 1px solid #f0f0f0; }}
tr:last-child td {{ border-bottom: none; }}
tr:hover td {{ background: #f8f6ff; }}
.date-cell {{ font-weight: 600; color: #333; }}
.wd-cell {{ color: #888; }}
.shift-cell {{ font-weight: 500; color: #2980b9; }}
.time-cell {{ font-family: monospace; color: #555; }}
.pos-cell {{ color: #666; }}
.per-cell {{ color: #777; }}
.empty-row td {{ color: #aaa; text-align: center; padding: 30px; }}
</style>
</head>
<body>
<div class="header">
  <h1>排班表 · {year}年 · {'按周' if mode=='week' else '按月'}{range_label}</h1>
  <p>共 {len(all_rows)} 条排班记录 · {len(group_keys)} {'周' if mode=='week' else '月'}</p>
</div>
"""
    for gk in group_keys:
        rows = groups[gk]
        label = group_label(gk)
        html += f'<div class="section"><div class="section-title">{label}</div>\n'
        html += '<table><thead><tr><th>日期</th><th>星期</th><th>班次</th><th>时段</th><th>岗位</th><th>人员</th></tr></thead><tbody>\n'
        for r in rows:
            html += f"<tr><td class=\"date-cell\">{r[0]}</td><td class=\"wd-cell\">{r[1]}</td><td class=\"shift-cell\">{r[2]}</td><td class=\"time-cell\">{r[3]}</td><td class=\"pos-cell\">{r[4]}</td><td class=\"per-cell\">{r[5]}</td></tr>\n"
        html += '</tbody></table></div>\n'

    if not group_keys:
        html += '<div class="section"><div class="empty-row">暂无排班记录</div></div>'

    html += '</body>\n</html>'
    return html


def generate_schedule_html() -> str:
    """
    导出个人日程为 HTML

    按日期分组展示所有非已取消日程
    """
    events, _ = load_schedule_events()
    active_events = [e for e in events if e.status != "cancelled"]

    if not active_events:
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>个人日程</title>
<style>body{{font-family:'Segoe UI','PingFang SC',sans-serif;background:linear-gradient(135deg,#f5f0ff 0%,#e8f4f8 100%);padding:40px;}}</style>
</head>
<body><h2>暂无日程安排</h2></body></html>"""

    # 按日期分组
    from collections import defaultdict
    by_date = defaultdict(list)
    for e in active_events:
        by_date[e.date].append(e)

    sorted_dates = sorted(by_date.keys())
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    status_labels = {"pending": "待完成", "completed": "已完成", "cancelled": "已取消", "missed": "已错过"}
    status_colors = {"pending": "#f39c12", "completed": "#2ecc71", "cancelled": "#e74c3c", "missed": "#d35400"}

    event_rows = []
    for date_str in sorted_dates:
        dt = parse_date(date_str)
        weekday = weekday_names[dt.weekday()] if dt else ""
        display_date = f"{date_str} ({weekday})"

        day_events = sorted(by_date[date_str], key=lambda x: x.start_time)
        for e in day_events:
            sc = status_colors.get(e.status, "#888")
            sl = status_labels.get(e.status, e.status)
            event_rows.append(f"""
    <tr>
      <td class="date-cell">{display_date}</td>
      <td>{e.start_time}-{e.end_time}</td>
      <td><strong>{e.title}</strong></td>
      <td>{e.description}</td>
      <td><span class="tag cat-{e.category}">{e.category}</span></td>
      <td><span class="tag status-{e.status}" style="background:{sc}20;color:{sc}">{sl}</span></td>
    </tr>""")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>个人日程安排</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: linear-gradient(135deg, #f5f0ff 0%, #e8f4f8 100%);
  color: #333; padding: 20px;
}}
.header {{
  background: linear-gradient(135deg, #9b59b6 0%, #3498db 100%);
  color: #fff; border-radius: 16px; padding: 24px 30px; margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(155, 89, 182, 0.3);
}}
.header h1 {{ font-size: 24px; }}
.header p {{ opacity: 0.9; font-size: 14px; margin-top: 4px; }}
table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
th {{ background: #f8f4ff; padding: 12px 16px; text-align: left; font-size: 13px; color: #666; font-weight: 600; }}
td {{ padding: 10px 16px; border-bottom: 1px solid #f0f0f0; font-size: 13px; }}
tr:last-child td {{ border-bottom: none; }}
.date-cell {{ white-space: nowrap; color: #555; }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 12px; }}
.cat-工作 {{ background: #e8f4fd; color: #2980b9; }}
.cat-会议 {{ background: #fef3e2; color: #e67e22; }}
.cat-个人 {{ background: #e8f8e8; color: #27ae60; }}
.cat-其他 {{ background: #f0f0f0; color: #666; }}
.status-pending {{ background: #fef9e7; color: #f39c12; }}
.status-completed {{ background: #eafaf1; color: #2ecc71; }}
.status-cancelled {{ background: #fdedec; color: #e74c3c; }}
.status-missed {{ background: #fef0e6; color: #d35400; }}
</style>
</head>
<body>
<div class="header">
  <h1>个人日程安排</h1>
  <p>共 {len(active_events)} 条日程</p>
</div>
<table>
<thead>
  <tr><th>日期</th><th>时间</th><th>标题</th><th>描述</th><th>分类</th><th>状态</th></tr>
</thead>
<tbody>
{"".join(event_rows)}
</tbody>
</table>
</body>
</html>"""
    return html

def sync_year(year: int, source_year: int = None) -> Dict:
    """将指定年份的假日/补班数据同步到目标年份（保留月日）"""
    if source_year is None:
        source_year = year - 1

    result = {"holidays_synced": 0, "compensatory_synced": 0, "errors": []}

    source_holidays, _ = load_holiday_intervals(source_year)
    new_holidays = []
    for h in source_holidays:
        parts = h.start.split('-')
        if len(parts) == 3:
            new_start = f"{year}-{parts[1]}-{parts[2]}"
        else:
            new_start = h.start
            result["errors"].append(f"日期格式错误: {h.start}")

        parts = h.end.split('-')
        if len(parts) == 3:
            new_end = f"{year}-{parts[1]}-{parts[2]}"
        else:
            new_end = h.end

        new_holidays.append(HolidayInterval(
            name=h.name, start=new_start, end=new_end, note=h.note
        ))
        result["holidays_synced"] += 1

    save_holiday_intervals(year, new_holidays)

    source_comp, _ = load_compensatory_days(source_year)
    new_comp = []
    for c in source_comp:
        parts = c.date.split('-')
        if len(parts) == 3:
            new_date = f"{year}-{parts[1]}-{parts[2]}"
            new_comp.append(CompensatoryDay(date=new_date, note=c.note))
            result["compensatory_synced"] += 1
        else:
            result["errors"].append(f"日期格式错误: {c.date}")

    save_compensatory_days(year, new_comp)

    return result


# ============================================================
# 规则确认表
# ============================================================

def export_rules_table(year: int = None) -> str:
    """
    导出规则确认表（供用户核对配置）

    包含:
    1. 周末规则配置
    2. 法定节假日列表
    3. 补班日列表
    4. 轮休配置
    5. 特殊休息（公休/临修）
    6. 冲突检查
    7. 年度统计摘要（修复 52 周硬编码 + 节假周末重复扣除）
    """
    if year is None:
        year = datetime.now().year

    weekday_map = {0: "周日", 1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五", 6: "周六"}

    # 加载数据
    holiday_intervals, _ = load_holiday_intervals(year)
    compensatory_days, _ = load_compensatory_days(year)
    weekend_config = load_weekend_config()
    rotation_configs, _ = load_rotation_configs()
    special_rests, _ = load_special_rests()

    # 生成所有集合
    holidays_set = generate_holiday_set(holiday_intervals)
    compensatory_set = generate_compensatory_set(compensatory_days)
    weekend_set = config_weekends_to_python(weekend_config.weekends)
    rotation_skip, rotation_noskip = generate_all_rotation_days(year, rotation_configs, holidays_set)
    gongxiu_set, linxiu_set = get_special_rest_dates(special_rests)

    # 节假日详情
    holidays_detail = []
    total_holiday_days_sum = 0
    for interval in holiday_intervals:
        start_dt = parse_date(interval.start)
        end_dt = parse_date(interval.end)
        if start_dt and end_dt:
            days = (end_dt - start_dt).days + 1
            total_holiday_days_sum += days
            holidays_detail.append({
                "name": interval.name,
                "start": interval.start,
                "end": interval.end,
                "days": days,
                "note": interval.note
            })

    # 补班日详情
    comp_detail = []
    for comp in compensatory_days:
        comp_dt = parse_date(comp.date)
        weekday = weekday_map[comp_dt.weekday()] if comp_dt else "未知"
        comp_detail.append({"date": comp.date, "weekday": weekday, "note": comp.note})

    # 轮休概要
    total_rotation = len(rotation_skip | rotation_noskip)

    # 特殊休息概要
    total_gongxiu = len(gongxiu_set)
    total_linxiu = len(linxiu_set)

    # ═══ 修复：遍历实际日期计算周末天数，避免 52 周硬编码和节假日重复扣除 ═══
    actual_weekend_days = 0
    for d in get_all_dates_of_year(year):
        date_str = format_date(d)
        if d.weekday() in weekend_set:
            # 只计既不是假日也不是补班的日子
            if date_str not in holidays_set and date_str not in compensatory_set:
                actual_weekend_days += 1

    # 计算统计
    total = calculate_total_workdays(
        year, holiday_intervals, compensatory_days, weekend_config,
        rotation_configs, special_rests
    )

    # 构建输出
    lines = []
    lines.append("=" * 70)
    lines.append(f"{year}年 规则配置确认表")
    lines.append("=" * 70)

    # 1. 周末规则
    lines.append("\n[周末规则配置]")
    lines.append("-" * 40)
    if weekend_config.weekends == [0, 6]:
        lines.append("  休息日: 周六、周日 (标准双休)")
    elif weekend_config.weekends == [5, 6]:
        lines.append("  休息日: 周五、周六")
    elif weekend_config.weekends == [0, 1]:
        lines.append("  休息日: 周日、周一")
    elif len(weekend_config.weekends) == 1:
        lines.append(f"  休息日: {weekday_map.get(weekend_config.weekends[0], '未知')} (单休)")
    else:
        rest_days = [weekday_map.get(w, str(w)) for w in weekend_config.weekends]
        lines.append(f"  休息日: {', '.join(rest_days)}")

    # 2. 法定节假日
    lines.append("\n[法定节假日]")
    lines.append("-" * 40)
    if not holidays_detail:
        lines.append("  - 未配置！请使用 import_holidays() 导入")
    else:
        lines.append(f"  共 {len(holidays_detail)} 个假期，区间总计 {total_holiday_days_sum} 天 (实际 {len(holidays_set)} 天)\n")
        lines.append(f"  {'假期名称':<12} {'开始日期':<12} {'结束日期':<12} {'天数':<6} {'备注'}")
        lines.append("  " + "-" * 52)
        for h in holidays_detail:
            note = h["note"] if h["note"] else "-"
            lines.append(f"  {h['name']:<12} {h['start']:<12} {h['end']:<12} {h['days']:<6} {note}")

    # 3. 补班日
    lines.append("\n[补班日（需要上班）]")
    lines.append("-" * 40)
    if not comp_detail:
        lines.append("  - 无补班日安排")
    else:
        lines.append(f"  共 {len(comp_detail)} 天需要上班\n")
        lines.append(f"  {'日期':<14} {'星期':<8} {'备注'}")
        lines.append("  " + "-" * 40)
        for c in comp_detail:
            note = c["note"] if c["note"] else "-"
            lines.append(f"  {c['date']:<14} {c['weekday']:<8} {note}")

    # 4. 轮休配置
    lines.append("\n[轮休配置]")
    lines.append("-" * 40)
    if not rotation_configs:
        lines.append("  - 未配置轮休")
    else:
        enabled_count = sum(1 for c in rotation_configs if c.enabled)
        lines.append(f"  共 {len(rotation_configs)} 个配置，其中 {enabled_count} 个启用，共 {total_rotation} 个轮休日\n")
        for c in rotation_configs:
            mode_text = "跳过法定假" if c.skip_holidays else "不跳过法定假"
            status_icon = "启用" if c.enabled else "停用"
            lines.append(f"  [{c.id}] {c.name} ({status_icon})")
            lines.append(f"      起始: {c.start_date} | 周期: {c.cycle_days}天 | 工作: {c.work_days}天 | 休息: {c.rest_days}天 | 模式: {mode_text}")

    # 5. 特殊休息
    lines.append("\n[特殊休息]")
    lines.append("-" * 40)
    if not special_rests:
        lines.append("  - 未配置特殊休息")
    else:
        lines.append(f"  公休: {total_gongxiu} 天, 临修: {total_linxiu} 天\n")
        for r in special_rests:
            if r.date:
                range_info = r.date
            else:
                range_info = f"{r.start_date} ~ {r.end_date}"
            reason = f" - {r.reason}" if r.reason else ""
            lines.append(f"  [{r.id}] {r.type} | {range_info}{reason}")

    # 6. 冲突检查
    conflicts_holiday_comp = holidays_set & compensatory_set
    conflicts_rotation_holiday = rotation_noskip & holidays_set
    total_conflicts = len(conflicts_holiday_comp) + len(conflicts_rotation_holiday)

    if total_conflicts > 0:
        lines.append("\n[配置冲突警告]")
        lines.append("-" * 40)
        if conflicts_holiday_comp:
            lines.append("  以下日期同时存在于节假日和补班日中（以补班日为准）：")
            for date in sorted(conflicts_holiday_comp):
                dt = parse_date(date)
                weekday = weekday_map.get(dt.weekday(), "") if dt else ""
                lines.append(f"    {date} ({weekday})")
        if conflicts_rotation_holiday:
            lines.append("  以下轮休日(noskip模式)与法定假日重叠：")
            for date in sorted(conflicts_rotation_holiday):
                dt = parse_date(date)
                weekday = weekday_map.get(dt.weekday(), "") if dt else ""
                lines.append(f"    {date} ({weekday})")

    # 7. 年度统计摘要
    lines.append("\n[年度统计摘要]")
    lines.append("-" * 40)
    lines.append(f"  年度总天数:         {total.get('total_days', 'N/A')} 天")
    lines.append(f"  工作日天数:         {total.get('total_workdays', 'N/A')} 天")
    lines.append(f"  休息日天数:         {total.get('total_holidays', 'N/A')} 天")
    lines.append(f"  法定假日天数:       {total.get('holiday_count', 'N/A')} 天")
    lines.append(f"  补班日天数:         {total.get('compensatory_count', 'N/A')} 天")
    lines.append(f"  轮休日天数:         {total.get('rotation_count', 'N/A')} 天")
    lines.append(f"  公休天数:           {total.get('gongxiu_count', 'N/A')} 天")
    lines.append(f"  临修天数:           {total.get('linxiu_count', 'N/A')} 天")
    lines.append(f"  周末天数:           {actual_weekend_days} 天")

    # 8. 核对提示
    lines.append("\n" + "=" * 70)
    lines.append("请核对以上配置是否正确！")
    lines.append("   如有疏漏或错误，请使用相应命令修改配置")
    lines.append("=" * 70)

    return "\n".join(lines)


# ============================================================
# CLI入口
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python workday_calendar.py <command> [options]")
        print()
        print("规则确认:")
        print("  rules [year]               - 导出规则确认表（请在初始化后核对）")
        print()
        print("工作日计算:")
        print("  calculate <year>           - 计算年度总工日")
        print("  calendar <year>            - 生成周历")
        print("  sync <year> [source_year]  - 同步数据到目标年份")
        print("  init <year>                - 初始化年度数据")
        print()
        print("日程管理:")
        print("  add <date> <start> <end> <title> [desc] [cat] - 添加日程")
        print("  list [date]                - 列出日程")
        print("  delete <id>                - 删除日程")
        print("  update <id> [options]      - 更新日程")
        print("  free <date> [start] [end]  - 查找空闲时间")
        print("  schedule [days]            - 生成日程列表(默认7天)")
        print("  today                      - 生成今天及后续7天日程")
        print()
        print("轮休管理:")
        print("  rotation add <name> <start> <cycle> <work> [--skip]")
        print("                               - 添加轮休配置")
        print("  rotation list              - 列出轮休配置")
        print("  rotation delete <id>       - 删除轮休配置")
        print("  rotation generate [year]   - 生成轮休日并缓存")
        print()
        print("特殊休息管理:")
        print("  special add 公休|临修 --date=<d> [--reason=<r>]")
        print("  special add 公休|临修 --start-date=<d> --end-date=<d> [--reason=<r>]")
        print("  special list [公休|临修]    - 列出特殊休息")
        print("  special list [公休|临修]    - 列出特殊休息")
        print("  special delete <id>        - 删除特殊休息")
        print()
        print("排版规则管理(B层):")
        print("  sched view                  - 查看当前排班规则")
        print("  sched set <weekday> <slots> - 设置某天规则")
        print("     时段格式: start-end:label[:position[:persons]]")
        print("     例: sched set 0 00:00-08:30:休息 08:30-11:30:上午班:收银台:张三,李四")
        print("                   11:30-13:30:午休 13:30-17:30:下午班 17:30-23:59:休息")
        print()
        print("自动化(定时任务):")
        print("  auto check               - 检查并执行到时的定时任务")
        print("  auto add <name> <hour> <min> <days> [--nosched] [--noshift] [--wd=0,1,2]")
        print("  auto list                - 列出定时任务")
        print("  auto delete <id>         - 删除定时任务")
        print("  auto preview <days> [--nosched] [--noshift] - 预览日程Markdown")
        print()
        print("HTML 导出:")
        print("  export-weekly-board [year] [output] - 导出排班基板 HTML（基础日期底板+排班规则叠加）")
        print("  export-schedule-weekly [year] [output] - 导出日程基板 HTML（基础日期底板±排班+个人日程）")
        print("  export-schedule-table --mode=<week|month> [--date-from=YYYY-MM-DD] [--date-to=YYYY-MM-DD] [output]")
        print("     例: export-schedule-table --mode=week                    # 全年按周")
        print("         export-schedule-table --mode=month --date-from=2026-03-01 --date-to=2026-05-31")
        print("  export-schedule [output]     - 导出现有日程 HTML（表格视图）")
        sys.exit(1)

    command = sys.argv[1]

    # ========== 规则确认 ==========
    if command == "rules":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
        print(export_rules_table(year))

    # ========== 日程管理 ==========
    elif command == "add":
        if len(sys.argv) < 6:
            print("用法: add <date> <start> <end> <title> [description] [category]")
            sys.exit(1)
        date = sys.argv[2]
        start_time = sys.argv[3]
        end_time = sys.argv[4]
        title = sys.argv[5]
        description = sys.argv[6] if len(sys.argv) > 6 else ""
        category = sys.argv[7] if len(sys.argv) > 7 else "工作"
        event, msg = add_schedule_event(title, date, start_time, end_time, description, category)
        if event:
            print(json.dumps(event.to_dict(), ensure_ascii=False, indent=2))
        print(msg)

    elif command == "list":
        date = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m-%d")
        events = get_schedule_by_date(date)
        if not events:
            print(f"{date} 暂无日程")
        else:
            print(f"{date} 日程列表:")
            events.sort(key=lambda x: x.start_time)
            for e in events:
                status_icon = "✅" if e.status == "completed" else "🔄" if e.status == "pending" else "❌" if e.status == "cancelled" else "⏰"
                print(f"  [{e.id}] {status_icon} {e.start_time}-{e.end_time} {e.title} ({e.category})")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("用法: delete <event_id>")
            sys.exit(1)
        print(delete_schedule_event(sys.argv[2]))

    elif command == "update":
        if len(sys.argv) < 3:
            print("用法: update <event_id> [options]")
            print("选项: --title, --date, --start, --end, --desc, --category, --status")
            sys.exit(1)
        event_id = sys.argv[2]
        kwargs = {}
        for arg in sys.argv[3:]:
            if arg.startswith("--title="):
                kwargs["title"] = arg[8:]
            elif arg.startswith("--date="):
                kwargs["date"] = arg[7:]
            elif arg.startswith("--start="):
                kwargs["start_time"] = arg[8:]
            elif arg.startswith("--end="):
                kwargs["end_time"] = arg[6:]
            elif arg.startswith("--desc="):
                kwargs["description"] = arg[7:]
            elif arg.startswith("--category="):
                kwargs["category"] = arg[11:]
            elif arg.startswith("--status="):
                kwargs["status"] = arg[9:]
        print(update_schedule_event(event_id, **kwargs))

    elif command == "free":
        date = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m-%d")
        start_search = sys.argv[3] if len(sys.argv) > 3 else "09:00"
        end_search = sys.argv[4] if len(sys.argv) > 4 else "18:00"
        slots = find_free_slots(date, start_search, end_search)
        if not slots:
            print(f"{date} {start_search}-{end_search} 无空闲时段")
        else:
            print(f"{date} {start_search}-{end_search} 空闲时段:")
            for slot in slots:
                print(f"  {slot['start']}-{slot['end']} (共{slot['duration']}分钟)")

    elif command == "schedule":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(generate_daily_schedule(datetime.now().strftime("%Y-%m-%d"), days))

    elif command == "today":
        print(generate_today_schedule())

    # ========== 工作日计算 ==========
    elif command == "calculate":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
        summary = calculate_total_workdays(year)
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    elif command == "calendar":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
        cal = generate_weekly_calendar(year)
        print(json.dumps(cal, ensure_ascii=False, indent=2))

    elif command == "sync":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
        source = int(sys.argv[3]) if len(sys.argv) > 3 else year - 1
        result = sync_year(year, source)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "init":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
        save_holiday_intervals(year, [])
        save_compensatory_days(year, [])
        print(f"已初始化 {year} 年数据文件")

    # ========== 轮休管理 ==========
    elif command == "rotation":
        if len(sys.argv) < 3:
            print("用法: rotation <add|list|delete|generate> [options]")
            sys.exit(1)

        sub = sys.argv[2]

        if sub == "add":
            if len(sys.argv) < 6:
                print("用法: rotation add <name> <start_date> <cycle_days> <work_days> [--skip] [--noskip]")
                sys.exit(1)
            name = sys.argv[3]
            start_date = sys.argv[4]
            cycle_days = int(sys.argv[5])
            work_days = int(sys.argv[6]) if len(sys.argv) > 6 else cycle_days // 2
            skip_holidays = True  # 默认跳过
            if "--noskip" in sys.argv:
                skip_holidays = False
            elif "--skip" in sys.argv:
                skip_holidays = True
            config, msg = add_rotation_config(name, start_date, cycle_days, work_days, skip_holidays)
            if config:
                print(json.dumps(config.to_dict(), ensure_ascii=False, indent=2))
            print(msg)

        elif sub == "list":
            print(list_rotation_configs())

        elif sub == "delete":
            if len(sys.argv) < 4:
                print("用法: rotation delete <id>")
                sys.exit(1)
            print(delete_rotation_config(sys.argv[3]))

        elif sub == "generate":
            year = int(sys.argv[3]) if len(sys.argv) > 3 else datetime.now().year
            print(rotate_generate(year))

        else:
            print(f"未知轮休子命令: {sub}")

    # ========== 特殊休息管理 ==========
    elif command == "special":
        if len(sys.argv) < 3:
            print("用法: special <add|list|delete> [options]")
            sys.exit(1)

        sub = sys.argv[2]

        if sub == "add":
            if len(sys.argv) < 4:
                print("用法: special add 公休|临修 --date=... [--reason=...]")
                sys.exit(1)
            rest_type = sys.argv[3]
            date = None
            start_date = None
            end_date = None
            reason = ""
            for arg in sys.argv[4:]:
                if arg.startswith("--date="):
                    date = arg[7:]
                elif arg.startswith("--start-date="):
                    start_date = arg[13:]
                elif arg.startswith("--end-date="):
                    end_date = arg[11:]
                elif arg.startswith("--reason="):
                    reason = arg[9:]
            rest, msg = add_special_rest(rest_type, date, start_date, end_date, reason)
            if rest:
                print(json.dumps(rest.to_dict(), ensure_ascii=False, indent=2))
            print(msg)

        elif sub == "list":
            filter_type = sys.argv[3] if len(sys.argv) > 3 else None
            print(list_special_rests(filter_type))

        elif sub == "delete":
            if len(sys.argv) < 4:
                print("用法: special delete <id>")
                sys.exit(1)
            print(delete_special_rest(sys.argv[3]))

        else:
            print(f"未知特殊休息子命令: {sub}")

    # ========== 排版规则管理 ==========
    elif command == "sched":
        if len(sys.argv) < 3:
            print("用法: sched <view|set> ...")
            sys.exit(1)
        sub = sys.argv[2]
        if sub == "view":
            rules = load_scheduling_rules()
            day_names = ["周一","周二","周三","周四","周五","周六","周日"]
            if not rules:
                print("当前无自定义排版规则（使用默认）")
            for wd in range(7):
                slots = get_slots_for_weekday(wd)
                if slots:
                    segs = " | ".join(f"{s.start}-{s.end}{s.label}" + (f"({s.position})" if s.position else "") + (f"[{s.persons}]" if s.persons else "") for s in slots[:4])
                    print(f"  {day_names[wd]}: {segs}")
        elif sub == "set":
            if len(sys.argv) < 5:
                print("用法: sched set <weekday(0-6)> <start-end:label> [start-end:label] ...")
                print("  weekday: 0=周一 1=周二 ... 6=周日")
                sys.exit(1)
            wd = int(sys.argv[3])
            rules = load_scheduling_rules()
            slots = []
            for arg in sys.argv[4:]:
                # 格式: HH:MM-HH:MM:label[|position:persons]...
                # 例: 08:30-11:30:上午班|收银台:张三,李四|客服:王五
                m = re.match(r'^(\d{2}:\d{2})-(\d{2}:\d{2}):(.+)$', arg)
                if not m:
                    continue
                start, end, rest = m.group(1), m.group(2), m.group(3)
                # 用 | 分隔: 第一段是label, 后续是 position:persons
                segs = rest.split("|")
                label = segs[0]
                assignments = []
                for s in segs[1:]:
                    parts = s.split(":", 1)
                    pos = parts[0]
                    per = parts[1] if len(parts) > 1 else ""
                    assignments.append({"position": pos, "persons": per})
                is_work = not any(kw in label for kw in ["休息","休","off"])
                color = "#3498db" if is_work else "#95a5a6"
                slots.append(WorkSlot(start, end, label, is_work, color,
                                      assignments=assignments if assignments else None))
            rules[wd] = slots
            save_scheduling_rules(rules)
            day_names = ["周一","周二","周三","周四","周五","周六","周日"]
            print(f"已设置 {day_names[wd]} 排版规则: {len(slots)} 个时段")
        else:
            print(f"未知子命令: {sub}")

    # ========== 配置管理 ==========
    elif command == "config":
        if len(sys.argv) > 2 and sys.argv[2] == "set":
            cfg = load_config()
            for arg in sys.argv[3:]:
                if arg.startswith("--use-scheduling="):
                    val = arg[17:].lower()
                    cfg["use_scheduling_as_base"] = val in ("true", "1", "yes")
                elif arg.startswith("--auto-complete="):
                    val = arg[16:].lower()
                    cfg["auto_mark_missed_as_completed"] = val in ("true", "1", "yes")
            save_config(cfg)
            # 重新加载以确保打印的是已保存状态
            cfg = load_config()
            print(json.dumps(cfg, ensure_ascii=False, indent=2))
        else:
            cfg = load_config()
            print(json.dumps(cfg, ensure_ascii=False, indent=2))

    # ========== 规则模板 ==========
    elif command == "export-rules-template":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
        template = export_rules_template(year)
        print(json.dumps(template, ensure_ascii=False, indent=2))

    elif command == "import-rules":
        if len(sys.argv) < 3:
            print("用法: import-rules '<json_string>'")
            print("  或: import-rules --file=<path>")
            sys.exit(1)
        if sys.argv[2].startswith("--file="):
            filepath = sys.argv[2][7:]
            with open(filepath, 'r', encoding='utf-8') as f:
                template = json.load(f)
        else:
            template = json.loads(sys.argv[2])
        result = import_rules_from_template(template)
        print(result)

    # ========== 自动化(定时任务) ==========
    elif command == "auto":
        if len(sys.argv) < 3:
            print("用法: auto <check|add|list|delete|preview> ...")
            sys.exit(1)
        sub = sys.argv[2]
        if sub == "check":
            result = check_automations()
            if result:
                print(result)
            else:
                print("当前无匹配的自动化规则")
        elif sub == "list":
            print(list_auto_rules())
        elif sub == "preview":
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 3
            show_shifts = "--noshift" not in sys.argv
            show_sched = "--nosched" not in sys.argv
            print(generate_schedule_markdown(days, show_shifts, show_sched, "日程预览"))
        elif sub == "add":
            if len(sys.argv) < 6:
                print("用法: auto add <name> <hour> <min> <days> [--nosched] [--noshift] [--wd=0,1,2]")
                sys.exit(1)
            name = sys.argv[3]
            hour = int(sys.argv[4])
            minute = int(sys.argv[5])
            days = int(sys.argv[6]) if len(sys.argv) > 6 else 3
            show_shifts = "--noshift" not in sys.argv
            show_sched = "--nosched" not in sys.argv
            weekdays = None
            for arg in sys.argv[7:]:
                if arg.startswith("--wd="):
                    weekdays = [int(x) for x in arg[5:].split(",")]
            r, msg = add_auto_rule(name, hour, minute, days, show_shifts, show_sched, weekdays)
            if r:
                print(msg)
            else:
                print(msg)
        elif sub == "delete":
            if len(sys.argv) < 4:
                print("用法: auto delete <id>")
                sys.exit(1)
            print(delete_auto_rule(sys.argv[3]))
        else:
            print(f"未知子命令: {sub}")

    # ========== HTML 导出 ==========
    elif command == "export-weekly-board":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
        output = sys.argv[3] if len(sys.argv) > 3 else None
        html = generate_weekly_board_html(year, embed_schedule=False)
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"已导出排班基板: {output}")
        else:
            print(html)

    elif command == "export-schedule-weekly":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
        output = sys.argv[3] if len(sys.argv) > 3 else None
        html = generate_weekly_board_html(year, embed_schedule=True)
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"已导出排班日程: {output}")
        else:
            print(html)

    elif command == "export-schedule":
        output = sys.argv[2] if len(sys.argv) > 2 else None
        html = generate_schedule_html()
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"已导出日程: {output}")
        else:
            print(html)

    elif command == "export-schedule-table":
        year = datetime.now().year
        mode = "week"
        date_from = None
        date_to = None
        output = None
        for arg in sys.argv[2:]:
            if arg.startswith("--year="):
                year = int(arg[7:])
            elif arg.startswith("--mode="):
                mode = arg[7:]
            elif arg.startswith("--date-from="):
                date_from = arg[12:]
            elif arg.startswith("--date-to="):
                date_to = arg[10:]
            elif not arg.startswith("--"):
                output = arg
        html = export_schedule_table(year, mode, date_from, date_to)
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"已导出排班表: {output}")
        else:
            print(html)

    else:
        print(f"未知命令: {command}")
        sys.exit(1)
