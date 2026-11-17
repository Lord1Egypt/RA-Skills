#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""元案 yotta-lesson —— 本地、确定性的教案 / 学案骨架与覆盖校验引擎（零依赖，Python 3.8+）。

设计依据：项目设计稿（2026-09-24 定稿）。

边界：只读本地映射包与教案文本；核心路径不联网、不调用模型；不输出教材 / 题目原文；
结论只作备课辅助，最终教学设计由教师负责。

退出码：0 正常 / 1 触发闸门 / 2 输入错误 / 3 映射或配置错误 / 4 运行时错误。
"""

import argparse
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.4"
SCHEMA_VERSION = "1.0"
TOOL_NAME = "yotta-lesson"

DISCLAIMER = (
    "本文件由元案（yotta-lesson）基于本地映射包与结构配置的确定性计算生成，仅作备课辅助；"
    "教学设计与时间安排的最终决定由教师负责，课标引用请以官方文本为准。"
)

DEFAULT_STRUCTURE = {
    "minutes_per_period": 45,
    "stages": [
        {"id": "lead_in", "name": "导入", "ratio": 0.10},
        {"id": "explore", "name": "新知探究", "ratio": 0.30},
        {"id": "explain", "name": "例题精讲", "ratio": 0.25},
        {"id": "practice", "name": "练习巩固", "ratio": 0.25},
        {"id": "summary", "name": "小结与作业", "ratio": 0.10},
    ],
    "required_stages": ["lead_in", "explore", "practice", "summary"],
    "check_keywords": {
        "lead_in": ["导入", "情境", "复习"],
        "explore": ["探究", "新知", "概念"],
        "explain": ["例题", "精讲", "示范"],
        "practice": ["练习", "巩固", "变式"],
        "summary": ["小结", "作业", "总结"],
    },
}

STAGE_FOCUS = {
    "lead_in": "激活旧知、呈现真实情境，明确本课目标",
    "explore": "围绕关键问题展开探究，形成概念与结论",
    "explain": "以典型例题示范思路与方法，讲清易错点",
    "practice": "分层练习与变式训练，当堂反馈",
    "summary": "梳理知识结构，布置分层作业与预习任务",
}


class LessonError(Exception):
    exit_code = 4

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InputError(LessonError):
    exit_code = 2


class ConfigError(LessonError):
    exit_code = 3


def normalize_text(text):
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    return text.replace("\ufeff", "").replace("\r\n", "\n").replace("\r", "\n")


def _read_json(payload, where):
    if isinstance(payload, (str, Path)):
        path = Path(payload)
        if not path.is_file():
            raise ConfigError("%s：文件不存在：%s" % (where, path))
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise ConfigError("%s：JSON 解析失败：%s" % (where, exc))
    return payload


def _string_list(value, where, field, required=True):
    if value is None:
        if required:
            raise ConfigError("%s：%s 不能为空" % (where, field))
        return []
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        raise ConfigError("%s：%s 必须是字符串数组" % (where, field))
    if required and not value:
        raise ConfigError("%s：%s 不能为空数组" % (where, field))
    return [v.strip() for v in value]


def load_map(payload, where="map"):
    """加载并校验课标映射包。"""
    data = _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigError("%s：schema_version 必须是 %s（当前 %r）"
                          % (where, SCHEMA_VERSION, data.get("schema_version")))
    raw_lessons = data.get("lessons")
    if not isinstance(raw_lessons, list) or not raw_lessons:
        raise ConfigError("%s：lessons 必须是非空数组" % where)
    lessons = []
    by_id = {}
    for raw in raw_lessons:
        if not isinstance(raw, dict):
            raise ConfigError("%s：lessons 元素必须是对象" % where)
        lesson_id = raw.get("id")
        if not isinstance(lesson_id, str) or not lesson_id.strip():
            raise ConfigError("%s：课题 id 不能为空" % where)
        lesson_id = lesson_id.strip()
        if lesson_id in by_id:
            raise ConfigError("%s：课题 id 重复：%s" % (where, lesson_id))
        title = raw.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ConfigError("%s：课题 %s 缺少 title" % (where, lesson_id))
        periods = raw.get("periods", 1)
        if isinstance(periods, bool) or not isinstance(periods, int) or periods < 1:
            raise ConfigError("%s：课题 %s 的 periods 必须是不小于 1 的整数" % (where, lesson_id))
        standard = raw.get("standard")
        if not isinstance(standard, str) or not standard.strip():
            raise ConfigError("%s：课题 %s 缺少 standard（课标来源，可追溯性必需）" % (where, lesson_id))
        lesson = {
            "id": lesson_id,
            "title": title.strip(),
            "unit": (raw.get("unit") or "").strip(),
            "periods": periods,
            "knowledge": _string_list(raw.get("knowledge"), where, "课题 %s 的 knowledge" % lesson_id),
            "key_points": _string_list(raw.get("key_points"), where,
                                       "课题 %s 的 key_points" % lesson_id, required=False),
            "difficulties": _string_list(raw.get("difficulties"), where,
                                         "课题 %s 的 difficulties" % lesson_id, required=False),
            "misconceptions": _string_list(raw.get("misconceptions"), where,
                                           "课题 %s 的 misconceptions" % lesson_id, required=False),
            "standard": standard.strip(),
        }
        lessons.append(lesson)
        by_id[lesson_id] = lesson
    return {
        "schema_version": SCHEMA_VERSION,
        "subject": (data.get("subject") or "").strip(),
        "grade": (data.get("grade") or "").strip(),
        "lessons": lessons,
        "by_id": by_id,
    }


def load_structure(payload, where="structure"):
    """加载教学结构配置；缺省用内置默认值，支持部分覆盖。"""
    base = {
        "minutes_per_period": DEFAULT_STRUCTURE["minutes_per_period"],
        "stages": [dict(stage) for stage in DEFAULT_STRUCTURE["stages"]],
        "required_stages": list(DEFAULT_STRUCTURE["required_stages"]),
        "check_keywords": {k: list(v) for k, v in DEFAULT_STRUCTURE["check_keywords"].items()},
    }
    if payload is None:
        return base
    data = _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    if "schema_version" in data and data["schema_version"] != SCHEMA_VERSION:
        raise ConfigError("%s：schema_version 必须是 %s" % (where, SCHEMA_VERSION))
    if "minutes_per_period" in data:
        value = data["minutes_per_period"]
        if isinstance(value, bool) or not isinstance(value, int) or value < 5:
            raise ConfigError("%s：minutes_per_period 必须是不小于 5 的整数" % where)
        base["minutes_per_period"] = value
    if "stages" in data:
        raw_stages = data["stages"]
        if not isinstance(raw_stages, list) or not raw_stages:
            raise ConfigError("%s：stages 必须是非空数组" % where)
        stages = []
        seen = set()
        for raw in raw_stages:
            if not isinstance(raw, dict):
                raise ConfigError("%s：stages 元素必须是对象" % where)
            stage_id = raw.get("id")
            name = raw.get("name")
            ratio = raw.get("ratio")
            if not isinstance(stage_id, str) or not stage_id.strip():
                raise ConfigError("%s：环节 id 不能为空" % where)
            if stage_id in seen:
                raise ConfigError("%s：环节 id 重复：%s" % (where, stage_id))
            seen.add(stage_id)
            if not isinstance(name, str) or not name.strip():
                raise ConfigError("%s：环节 %s 缺少 name" % (where, stage_id))
            if isinstance(ratio, bool) or not isinstance(ratio, (int, float)) or ratio <= 0:
                raise ConfigError("%s：环节 %s 的 ratio 必须是正数" % (where, stage_id))
            stages.append({"id": stage_id.strip(), "name": name.strip(), "ratio": float(ratio)})
        base["stages"] = stages
    stage_ids = [stage["id"] for stage in base["stages"]]
    if "required_stages" in data:
        required = _string_list(data["required_stages"], where, "required_stages")
        unknown = [item for item in required if item not in stage_ids]
        if unknown:
            raise ConfigError("%s：required_stages 引用了未声明的环节：%s"
                              % (where, "、".join(unknown)))
        base["required_stages"] = required
    else:
        base["required_stages"] = [item for item in base["required_stages"] if item in stage_ids]
    if "check_keywords" in data:
        raw_keywords = data["check_keywords"]
        if not isinstance(raw_keywords, dict):
            raise ConfigError("%s：check_keywords 必须是对象" % where)
        keywords = {}
        for key, value in raw_keywords.items():
            keywords[key] = _string_list(value, where, "check_keywords.%s" % key)
        base["check_keywords"] = keywords
    return base


def allocate_minutes(total_minutes, stages):
    """按比例分配整分钟，合计精确等于 total（最大余数法，确定性）。"""
    if total_minutes < len(stages):
        raise ConfigError("总时长 %d 分钟少于环节数量 %d，无法分配" % (total_minutes, len(stages)))
    weight_sum = sum(stage["ratio"] for stage in stages)
    if weight_sum <= 0:
        raise ConfigError("环节比例之和必须为正数")
    raw = [(stage["ratio"] / weight_sum) * total_minutes for stage in stages]
    minutes = [int(value) for value in raw]
    remainder = total_minutes - sum(minutes)
    order = sorted(range(len(stages)), key=lambda i: (-(raw[i] - minutes[i]), i))
    for index in order[:remainder]:
        minutes[index] += 1
    return minutes


def build_plan(lesson, structure, periods=None, subject=None, grade=None, now=None):
    """生成教案骨架（确定性）。"""
    use_periods = lesson["periods"] if periods is None else periods
    if use_periods < 1:
        raise InputError("课时数必须不小于 1")
    total_minutes = use_periods * structure["minutes_per_period"]
    minutes = allocate_minutes(total_minutes, structure["stages"])
    stages = []
    for stage, stage_minutes in zip(structure["stages"], minutes):
        stages.append({
            "id": stage["id"],
            "name": stage["name"],
            "minutes": stage_minutes,
            "focus": STAGE_FOCUS.get(stage["id"], "按教学需要组织本环节"),
        })
    objectives = [{"knowledge": item, "source": lesson["standard"]} for item in lesson["knowledge"]]
    checklist = [
        "学习目标是否覆盖全部知识点并标注课标来源",
        "关键问题与活动是否指向重难点",
        "例题与练习是否覆盖易错点",
        "时间分配是否与教案实际环节一致",
        "是否安排当堂反馈与分层作业",
    ]
    findings = []
    if periods is not None and periods != lesson["periods"]:
        findings.append({
            "kind": "periods_override",
            "detail": "课时数被覆盖：映射包 %d 课时 → 本次 %d 课时" % (lesson["periods"], periods),
        })
    if not lesson["misconceptions"]:
        findings.append({
            "kind": "no_misconceptions",
            "detail": "映射包未登记易错点，例题与练习需教师自行补充易错点设计",
        })
    generated_at = now or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "tool_version": VERSION,
        "generated_at": generated_at,
        "lesson": {
            "id": lesson["id"],
            "title": lesson["title"],
            "unit": lesson["unit"],
            "subject": (subject or "").strip(),
            "grade": (grade or "").strip(),
            "periods": use_periods,
            "minutes_per_period": structure["minutes_per_period"],
            "total_minutes": total_minutes,
        },
        "objectives": objectives,
        "key_points": list(lesson["key_points"]),
        "difficulties": list(lesson["difficulties"]),
        "misconceptions": list(lesson["misconceptions"]),
        "stages": stages,
        "checklist": checklist,
        "findings": findings,
        "sources": [{"standard": lesson["standard"]}],
        "disclaimer": DISCLAIMER,
    }


def _contains(text, needle):
    return needle in text


def check_plan(text, lesson, structure):
    """对已有教案文本做确定性缺口检查。"""
    text = normalize_text(text)
    findings = []
    for item in lesson["knowledge"]:
        if not _contains(text, item):
            findings.append({
                "kind": "knowledge_missing",
                "detail": "教案未出现知识点：%s" % item,
            })
    for stage_id in structure["required_stages"]:
        stage = [s for s in structure["stages"] if s["id"] == stage_id]
        name = stage[0]["name"] if stage else stage_id
        keywords = structure["check_keywords"].get(stage_id) or [name]
        if not any(_contains(text, keyword) for keyword in keywords):
            findings.append({
                "kind": "stage_missing",
                "detail": "教案未识别到必填环节：%s（关键词：%s）" % (name, "、".join(keywords)),
            })
    standard = lesson["standard"]
    probe = standard.split("·")[0].strip() if "·" in standard else standard
    if not _contains(text, probe):
        findings.append({
            "kind": "source_missing",
            "detail": "教案未标注课标来源：%s" % standard,
        })
    if not re.search(r"\d+\s*分钟", text):
        findings.append({
            "kind": "time_missing",
            "detail": "教案未标注环节时间（如「10 分钟」）",
        })
    total_match = re.search(r"合计\s*(\d+)\s*分钟", text)
    if total_match:
        expected = lesson["periods"] * structure["minutes_per_period"]
        if int(total_match.group(1)) != expected:
            findings.append({
                "kind": "minutes_mismatch",
                "detail": "教案标注合计 %s 分钟，与 %d 课时 × %d 分钟 = %d 分钟不一致"
                          % (total_match.group(1), lesson["periods"],
                             structure["minutes_per_period"], expected),
            })
    findings.sort(key=lambda item: (item["kind"], item["detail"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "tool_version": VERSION,
        "lesson": {"id": lesson["id"], "title": lesson["title"], "periods": lesson["periods"]},
        "checked": {
            "knowledge": list(lesson["knowledge"]),
            "required_stages": list(structure["required_stages"]),
            "standard": lesson["standard"],
        },
        "findings": findings,
        "summary": {"findings": len(findings)},
        "disclaimer": DISCLAIMER,
    }


def render_plan_markdown(plan):
    lines = []
    lesson = plan["lesson"]
    lines.append("# 教案骨架：%s（元案 yotta-lesson %s）" % (lesson["title"], plan["tool_version"]))
    lines.append("")
    lines.append("- 学科 / 年级：%s %s" % (lesson["subject"] or "—", lesson["grade"] or "—"))
    lines.append("- 课题：%s（%s）" % (lesson["title"], lesson["id"]))
    lines.append("- 课时：%d 课时 × %d 分钟 = **合计 %d 分钟**"
                 % (lesson["periods"], lesson["minutes_per_period"], lesson["total_minutes"]))
    lines.append("")
    lines.append("## 1. 学习目标（带课标来源）")
    lines.append("")
    for objective in plan["objectives"]:
        lines.append("- %s（来源：%s）" % (objective["knowledge"], objective["source"]))
    lines.append("")
    lines.append("## 2. 教学重难点与易错点")
    lines.append("")
    lines.append("- 重点：%s" % ("；".join(plan["key_points"]) or "待教师补充"))
    lines.append("- 难点：%s" % ("；".join(plan["difficulties"]) or "待教师补充"))
    lines.append("- 易错点：%s" % ("；".join(plan["misconceptions"]) or "待教师补充"))
    lines.append("")
    lines.append("## 3. 教学环节与时间分配")
    lines.append("")
    lines.append("| 环节 | 时间 | 要点 |")
    lines.append("| --- | --- | --- |")
    for stage in plan["stages"]:
        lines.append("| %s | %d 分钟 | %s |" % (stage["name"], stage["minutes"], stage["focus"]))
    lines.append("")
    lines.append("## 4. 板书与评价清单")
    lines.append("")
    for item in plan["checklist"]:
        lines.append("- [ ] %s" % item)
    lines.append("")
    lines.append("## 5. 备课提示")
    lines.append("")
    if plan["findings"]:
        for finding in plan["findings"]:
            lines.append("- %s" % finding["detail"])
    else:
        lines.append("- 无。")
    lines.append("")
    lines.append("## 6. 来源与免责")
    lines.append("")
    for source in plan["sources"]:
        lines.append("- 课标来源：%s" % source["standard"])
    lines.append("- %s" % plan["disclaimer"])
    lines.append("")
    return "\n".join(lines)


def render_check_markdown(result):
    lines = []
    lines.append("# 教案覆盖检查：%s（元案 yotta-lesson %s）"
                 % (result["lesson"]["title"], result["tool_version"]))
    lines.append("")
    lines.append("- 知识点：%s" % "、".join(result["checked"]["knowledge"]))
    lines.append("- 必填环节：%s" % "、".join(result["checked"]["required_stages"]))
    lines.append("- 课标来源：%s" % result["checked"]["standard"])
    lines.append("")
    lines.append("## 1. 缺口清单")
    lines.append("")
    if not result["findings"]:
        lines.append("未发现结构性缺口。")
    else:
        for finding in result["findings"]:
            lines.append("- [%s] %s" % (finding["kind"], finding["detail"]))
    lines.append("")
    lines.append("## 2. 免责声明")
    lines.append("")
    lines.append(result["disclaimer"])
    lines.append("")
    return "\n".join(lines)


def render_json(payload):
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def resolve_output_path(path):
    parts = Path(str(path)).parts
    if ".." in parts:
        raise InputError("输出路径不允许包含 ..（防越界写入）：%s" % path)
    target = Path(str(path))
    if target.exists() and target.is_dir():
        raise InputError("输出路径是目录，不能写入：%s" % path)
    if not target.parent.exists():
        raise InputError("输出目录不存在：%s" % target.parent)
    return target


def _write_text(path, text):
    with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


TEMPLATE_MAP = {
    "schema_version": SCHEMA_VERSION,
    "subject": "示例学科",
    "grade": "示例年级",
    "lessons": [
        {
            "id": "L1",
            "title": "示例课题",
            "unit": "示例单元",
            "periods": 1,
            "knowledge": ["示例知识点A", "示例知识点B"],
            "key_points": ["示例知识点A"],
            "difficulties": ["示例难点"],
            "misconceptions": ["示例易错点"],
            "standard": "示例课程标准（2022 年版）· 示例条目",
        }
    ],
}


def cmd_template(args):
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_text(out_dir / "lesson-map.json",
                json.dumps(TEMPLATE_MAP, ensure_ascii=False, indent=2) + "\n")
    _write_text(out_dir / "structure.json",
                json.dumps(DEFAULT_STRUCTURE, ensure_ascii=False, indent=2) + "\n")
    print("已生成模板：%s（lesson-map.json / structure.json）" % out_dir)
    return 0


def _load_lesson(args, where="map"):
    lesson_map = load_map(args.map, where)
    lesson = lesson_map["by_id"].get(args.lesson)
    if lesson is None:
        raise ConfigError("映射包中不存在课题：%s（可用：%s）"
                          % (args.lesson, "、".join(lesson_map["by_id"])))
    return lesson_map, lesson


def _parse_gate(expr):
    if not expr:
        return None
    if not expr.startswith("findings="):
        raise InputError("--gate 只支持 findings=<数量> 形式（当前 %r）" % expr)
    try:
        value = int(expr.split("=", 1)[1])
    except ValueError:
        raise InputError("--gate 的 findings 阈值必须是整数：%r" % expr)
    if value < 1:
        raise InputError("--gate 的 findings 阈值必须不小于 1：%r" % expr)
    return value


def _emit(payload, markdown, args):
    output = render_json(payload) if args.format == "json" else markdown
    if getattr(args, "out", None):
        target = resolve_output_path(args.out)
        _write_text(target, output + ("" if output.endswith("\n") else "\n"))
        print("已写入：%s" % target)
    else:
        print(output)


def cmd_plan(args):
    lesson_map, lesson = _load_lesson(args)
    structure = load_structure(args.config)
    plan = build_plan(lesson, structure, periods=args.periods,
                      subject=lesson_map["subject"], grade=lesson_map["grade"])
    _emit(plan, render_plan_markdown(plan), args)
    gate = _parse_gate(args.gate)
    if gate is not None and len(plan["findings"]) >= gate:
        return 1
    return 0


def cmd_check(args, stdin_text=None):
    lesson_map, lesson = _load_lesson(args)
    structure = load_structure(args.config)
    if args.stdin:
        text = stdin_text if stdin_text is not None else sys.stdin.read()
    else:
        if not args.plan:
            raise InputError("check 需要 --plan <文件> 或 --stdin")
        path = Path(args.plan)
        if not path.is_file():
            raise InputError("教案文件不存在：%s" % path)
        text = path.read_text(encoding="utf-8")
    result = check_plan(text, lesson, structure)
    _emit(result, render_check_markdown(result), args)
    gate = _parse_gate(args.gate)
    if gate is not None and len(result["findings"]) >= gate:
        return 1
    return 0


def cmd_map(args):
    if args.map_command == "list":
        lesson_map = load_map(args.map, "map")
        print("课题清单（%s %s，共 %d 条）：" % (lesson_map["subject"], lesson_map["grade"],
                                                len(lesson_map["lessons"])))
        for lesson in lesson_map["lessons"]:
            print("- %s  %s  %d 课时  知识点 %d 条" % (
                lesson["id"], lesson["title"], lesson["periods"], len(lesson["knowledge"])))
        return 0
    if args.map_command == "show":
        lesson_map = load_map(args.map, "map")
        lesson = lesson_map["by_id"].get(args.lesson)
        if lesson is None:
            raise ConfigError("映射包中不存在课题：%s" % args.lesson)
        print(json.dumps(lesson, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.map_command == "validate":
        lesson_map = load_map(args.map, "map")
        print("映射包校验通过：%s %s，%d 个课题"
              % (lesson_map["subject"], lesson_map["grade"], len(lesson_map["lessons"])))
        return 0
    raise InputError("未知 map 子命令")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="yotta-lesson",
        description="元案 —— 本地、确定性的教案骨架与覆盖校验引擎（零依赖，不联网）",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command")

    plan = sub.add_parser("plan", help="按映射包生成教案骨架")
    plan.add_argument("--map", required=True)
    plan.add_argument("--lesson", required=True)
    plan.add_argument("--config")
    plan.add_argument("--periods", type=int)
    plan.add_argument("--format", choices=("md", "json"), default="md")
    plan.add_argument("--out")
    plan.add_argument("--gate")

    check = sub.add_parser("check", help="对已有教案文本做缺口检查")
    check.add_argument("--plan")
    check.add_argument("--stdin", action="store_true")
    check.add_argument("--map", required=True)
    check.add_argument("--lesson", required=True)
    check.add_argument("--config")
    check.add_argument("--format", choices=("md", "json"), default="md")
    check.add_argument("--out")
    check.add_argument("--gate")

    map_cmd = sub.add_parser("map", help="映射包操作")
    map_sub = map_cmd.add_subparsers(dest="map_command")
    for name in ("list", "validate"):
        item = map_sub.add_parser(name)
        item.add_argument("--map", required=True)
    show = map_sub.add_parser("show")
    show.add_argument("--map", required=True)
    show.add_argument("--lesson", required=True)

    template = sub.add_parser("template", help="生成映射包与结构配置模板")
    template.add_argument("--output-dir", required=True)
    return parser


def main(argv=None, stdin_text=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--version":
        print(VERSION)
        return 0
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    try:
        if args.command == "plan":
            return cmd_plan(args)
        if args.command == "check":
            return cmd_check(args, stdin_text=stdin_text)
        if args.command == "map":
            if getattr(args, "map_command", None):
                return cmd_map(args)
            sys.stderr.write("错误：map 需要子命令（list / show / validate）\n")
            return 2
        if args.command == "template":
            return cmd_template(args)
        sys.stderr.write("错误：未知命令。可用：plan / check / map / template\n")
        return 2
    except LessonError as exc:
        sys.stderr.write("错误：%s\n" % exc.message)
        return exc.exit_code
    except OSError as exc:
        sys.stderr.write("错误：文件操作失败：%s\n" % exc)
        return 4


if __name__ == "__main__":
    sys.exit(main())
