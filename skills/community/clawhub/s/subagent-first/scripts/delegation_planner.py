#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""delegation_planner.py —— 委派决策器（子代理优先 · 零依赖）

用途
    读一份任务清单 JSON，按《子代理优先》方法论逐条给出委派判定与执行建议：
    哪些任务应该派子代理后台并行、哪些必须主代理自己做、哪些该转 cron/后台存活。

依赖
    仅 Python 标准库；Python 3.8+ 可直接运行，无需安装任何第三方包。

用法
    python3 delegation_planner.py --demo
    python3 delegation_planner.py --task-file tasks.json
    python3 delegation_planner.py --task-file tasks.json --json

输入格式
    顶层可以是任务数组，或形如 {"tasks": [...]} 的对象。每个任务字段：

        name              字符串，任务名（必填，非空）
        est_tool_calls    整数 >= 0，预计工具调用轮数（必填）
        files_touched     整数 >= 0（涉及文件数），或字符串数组（具体文件路径）（必填）
        is_research       布尔，是否长研究/多源检索（必填）
        is_batch          布尔，是否批量重复处理（必填）
        needs_user_input  布尔，是否需要用户交互/拍板（必填）
        irreversible      布尔，是否有不可逆副作用（必填）
        cross_session     布尔，是否需要跨会话长期存活（必填）

判定规则（优先级从高到低）
    1. needs_user_input 为真            -> SELF       需用户交互，一律不可委派
    2. cross_session 为真               -> CRON       跨会话长任务，转 cron 或后台进程
    3. irreversible 为真                -> SELF       不可逆副作用需即时把关
    4. 命中任一"重活"条件               -> SUBAGENT   派子代理后台并行
           est_tool_calls > 3 / files_touched 多文件 / is_research / is_batch
    5. 其余（一轮内轻活）               -> SELF       主代理自己做更快

输出
    ① 逐任务判定表  ② 委派建议（并行/串行分组）  ③ 主代理必做清单  ④ 一行汇总统计

退出码
    0  全部任务判定明确
    1  输入缺字段 / 类型错 / JSON 解析失败等（错误信息打到 stderr）
"""

import argparse
import json
import os
import sys
import unicodedata
from datetime import datetime

# ---------------------------------------------------------------- 常量与阈值

# 与 SKILL.md 方法论第 2 条对齐：> 2~3 轮即视为重活，此处取 3 为硬阈值
HEAVY_TOOL_CALL_THRESHOLD = 3

VERDICT_SUBAGENT = "SUBAGENT"
VERDICT_SELF = "SELF"
VERDICT_CRON = "CRON/BACKGROUND"

VERDICT_LABEL = {
    VERDICT_SUBAGENT: "派子代理",
    VERDICT_SELF: "自己做",
    VERDICT_CRON: "转后台",
}

TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"

REQUIRED_FIELDS = (
    "name",
    "est_tool_calls",
    "files_touched",
    "is_research",
    "is_batch",
    "needs_user_input",
    "irreversible",
    "cross_session",
)

BOOL_FIELDS = ("is_research", "is_batch", "needs_user_input", "irreversible", "cross_session")


class InputError(Exception):
    """输入不合法。触发时打印明确错误并以 1 退出。"""


# ---------------------------------------------------------------- 工具函数


def now_stamp():
    """严格格式 YYYY-MM-DD HH:MM:SS。"""
    return datetime.now().strftime(TIMESTAMP_FMT)


def display_width(text):
    """按东亚字符宽度估算显示列宽，用于表格对齐（无需第三方包）。"""
    width = 0
    for ch in str(text):
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def pad(text, width):
    """右侧补空格到指定显示宽度（中英混排可用）。"""
    text = str(text)
    return text + " " * max(0, width - display_width(text))


def truncate(text, max_width):
    """按显示宽度截断，超出部分用省略号。"""
    text = str(text)
    if display_width(text) <= max_width:
        return text
    out = ""
    used = 0
    for ch in text:
        step = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if used + step > max_width - 1:
            break
        out += ch
        used += step
    return out + "…"


def file_list_of(task):
    """把 files_touched 归一化为文件路径列表；整数形式返回空列表。"""
    touched = task["files_touched"]
    if isinstance(touched, list):
        return [str(p) for p in touched]
    return []


def file_count_of(task):
    """涉及文件数。"""
    touched = task["files_touched"]
    if isinstance(touched, list):
        return len(touched)
    return int(touched)


def paths_overlap(task_a, task_b):
    """两份任务的显式文件路径是否有交集。整数计数形式无法判断，返回 False。"""
    return bool(set(file_list_of(task_a)) & set(file_list_of(task_b)))


# ---------------------------------------------------------------- 校验


def validate_task(raw, index):
    """逐字段校验，出错抛 InputError（错误信息带任务序号，便于定位）。"""
    where = "第 %d 个任务" % (index + 1)
    if not isinstance(raw, dict):
        raise InputError("%s 不是对象（期望 JSON object，实际是 %s）" % (where, type(raw).__name__))

    name = raw.get("name")
    if name is not None and isinstance(name, str) and name.strip():
        where = "任务 “%s”" % name.strip()

    missing = [f for f in REQUIRED_FIELDS if f not in raw]
    if missing:
        raise InputError(
            "%s 缺字段：%s（需全部 %d 个字段：%s）"
            % (where, "、".join(missing), len(REQUIRED_FIELDS), "、".join(REQUIRED_FIELDS))
        )

    if not isinstance(raw["name"], str) or not raw["name"].strip():
        raise InputError("%s 的 name 必须是非空字符串" % where)

    calls = raw["est_tool_calls"]
    if isinstance(calls, bool) or not isinstance(calls, int) or calls < 0:
        raise InputError("%s 的 est_tool_calls 必须是 >= 0 的整数（实际：%r）" % (where, calls))

    touched = raw["files_touched"]
    if isinstance(touched, bool):
        raise InputError("%s 的 files_touched 必须是 >= 0 的整数或字符串数组（实际：%r）" % (where, touched))
    if isinstance(touched, int):
        if touched < 0:
            raise InputError("%s 的 files_touched 必须是 >= 0 的整数（实际：%r）" % (where, touched))
    elif isinstance(touched, list):
        if not all(isinstance(p, str) and p.strip() for p in touched):
            raise InputError("%s 的 files_touched 数组元素必须都是非空字符串路径" % where)
    else:
        raise InputError("%s 的 files_touched 必须是 >= 0 的整数或字符串数组（实际：%r）" % (where, touched))

    for field in BOOL_FIELDS:
        if not isinstance(raw[field], bool):
            raise InputError("%s 的 %s 必须是布尔值 true/false（实际：%r）" % (where, field, raw[field]))

    return {f: raw[f] for f in REQUIRED_FIELDS}


def load_tasks(path):
    """读并解析任务文件；失败抛 InputError。"""
    if not os.path.isfile(path):
        raise InputError("找不到任务文件：%s" % os.path.basename(path))
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as exc:
        raise InputError("JSON 解析失败（第 %d 行第 %d 列）：%s" % (exc.lineno, exc.colno, exc.msg))
    except OSError as exc:
        raise InputError("读取任务文件失败：%s" % exc.strerror or str(exc))

    if isinstance(payload, dict):
        if "tasks" not in payload:
            raise InputError('顶层是对象但缺 "tasks" 键（期望数组，或 {"tasks": [...]}）')
        payload = payload["tasks"]
    if not isinstance(payload, list):
        raise InputError("顶层必须是任务数组，或形如 {\"tasks\": [...]} 的对象")
    if not payload:
        raise InputError("任务清单为空，至少需要 1 个任务")

    return [validate_task(raw, i) for i, raw in enumerate(payload)]


# ---------------------------------------------------------------- 判定


def decide(task):
    """返回 (verdict, reason_codes, 中文理由)。优先级见文件头说明。"""
    if task["needs_user_input"]:
        return VERDICT_SELF, ["USER_INPUT"], "需用户交互/拍板，一律不可委派"

    if task["cross_session"]:
        return VERDICT_CRON, ["CROSS_SESSION"], "跨会话需长期存活，用 cron 或后台进程而非子代理"

    if task["irreversible"]:
        return VERDICT_SELF, ["IRREVERSIBLE"], "有不可逆副作用，需主代理即时把关"

    triggers = []
    if task["est_tool_calls"] > HEAVY_TOOL_CALL_THRESHOLD:
        triggers.append(("MANY_TOOL_CALLS", "预计 %d 轮 > %d 轮" % (task["est_tool_calls"], HEAVY_TOOL_CALL_THRESHOLD)))
    if file_count_of(task) >= 2:
        triggers.append(("MULTI_FILE", "跨 %d 个文件" % file_count_of(task)))
    if task["is_research"]:
        triggers.append(("RESEARCH", "长研究/多源检索"))
    if task["is_batch"]:
        triggers.append(("BATCH", "批量重复处理"))

    if triggers:
        detail = "、".join(label for _, label in triggers)
        return VERDICT_SUBAGENT, [code for code, _ in triggers], "重活：%s，派子代理后台并行" % detail

    detail = "%d 轮工具调用且无多文件/研究/批量" % task["est_tool_calls"]
    return VERDICT_SELF, ["LIGHT"], "轻活：%s，主代理一轮内可完成" % detail


def analyze(tasks):
    """判定全部任务并生成执行建议。"""
    results = []
    for task in tasks:
        verdict, codes, reason = decide(task)
        results.append(
            {
                "name": task["name"],
                "verdict": verdict,
                "verdict_label": VERDICT_LABEL[verdict],
                "reason_codes": codes,
                "reason": reason,
                "est_tool_calls": task["est_tool_calls"],
                "file_count": file_count_of(task),
                "files_touched": file_list_of(task),
            }
        )

    delegable = [r for r in results if r["verdict"] == VERDICT_SUBAGENT]
    self_tasks = [r for r in results if r["verdict"] == VERDICT_SELF]
    cron_tasks = [r for r in results if r["verdict"] == VERDICT_CRON]

    # 分组：与其他可委派任务存在文件路径冲突的进串行组，其余可并行
    task_by_name = {t["name"]: t for t in tasks}
    parallel, serial = [], []
    for item in delegable:
        me = task_by_name[item["name"]]
        conflict = any(
            other["name"] != item["name"] and paths_overlap(me, task_by_name[other["name"]])
            for other in delegable
        )
        (serial if conflict else parallel).append(item)

    plan = {"parallel": parallel, "serial": serial, "cron": cron_tasks}

    summary = "%d 个任务：%d 派子代理 / %d 自己做 / %d 转后台" % (
        len(results),
        len(delegable),
        len(self_tasks),
        len(cron_tasks),
    )

    return {
        "tasks": results,
        "self_tasks": self_tasks,
        "plan": plan,
        "summary": summary,
        "counts": {
            "total": len(results),
            "subagent": len(delegable),
            "self": len(self_tasks),
            "cron": len(cron_tasks),
        },
    }


# ---------------------------------------------------------------- 渲染


def render_text(report, source_label, stamp):
    lines = []
    lines.append("委派决策报告")
    lines.append("生成时间：%s ｜ 任务来源：%s" % (stamp, source_label))
    lines.append("")

    # ① 逐任务判定表
    lines.append("① 逐任务判定表")
    header = ["#", "任务名", "判定", "理由"]
    rows = []
    for i, item in enumerate(report["tasks"], 1):
        rows.append([str(i), item["name"], item["verdict_label"], item["reason"]])
    widths = []
    for col in range(len(header)):
        widths.append(max([display_width(header[col])] + [display_width(r[col]) for r in rows]))
    widths[1] = min(widths[1], 28)
    widths[3] = min(widths[3], 46)

    def fmt_row(cells):
        return "| " + " | ".join(pad(truncate(c, widths[i]), widths[i]) for i, c in enumerate(cells)) + " |"

    lines.append(fmt_row(header))
    lines.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for row in rows:
        lines.append(fmt_row(row))
    lines.append("")

    # ② 委派建议
    lines.append("② 委派建议")
    parallel = report["plan"]["parallel"]
    serial = report["plan"]["serial"]
    if not parallel and not serial:
        lines.append("  无可委派任务，全部由主代理自己做。")
    else:
        if parallel:
            lines.append("  [并行组] 互不共享文件，可同时派多个子代理：")
            for item in parallel:
                lines.append("    - %s（%s）" % (item["name"], item["reason"]))
        if serial:
            lines.append("  [串行组] 存在文件路径冲突，需排队、不可并行写同一文件：")
            for item in serial:
                lines.append("    - %s（%s）" % (item["name"], item["reason"]))
        lines.append("  派活前逐条套用 templates/派活工单.md；回收后逐条核对 templates/子代理验收清单.md。")
        lines.append("  子代理产出必须回读验证（handle/路径/实测）后才算完成，自报≠事实。")
    lines.append("")

    # ③ 主代理必做清单
    lines.append("③ 主代理必做清单（不可委派）")
    if report["self_tasks"]:
        for item in report["self_tasks"]:
            lines.append("  - [ ] %s —— %s" % (item["name"], item["reason"]))
    else:
        lines.append("  （无）")
    lines.append("")

    # 转后台提示
    cron = report["plan"]["cron"]
    if cron:
        lines.append("④ 转后台清单（cron / 常驻进程）")
        for item in cron:
            lines.append("  - [ ] %s —— %s" % (item["name"], item["reason"]))
        lines.append("")

    # 汇总
    lines.append("汇总：" + report["summary"])
    return "\n".join(lines)


def render_json(report, source_label, stamp):
    payload = {
        "generated_at": stamp,
        "task_source": source_label,
        "summary": report["summary"],
        "counts": report["counts"],
        "tasks": report["tasks"],
        "delegation_plan": {
            "parallel": [i["name"] for i in report["plan"]["parallel"]],
            "serial": [i["name"] for i in report["plan"]["serial"]],
            "cron_background": [i["name"] for i in report["plan"]["cron"]],
        },
        "manual_checklist": [
            {"name": i["name"], "verdict": i["verdict"], "reason": i["reason"]}
            for i in report["self_tasks"]
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- 示例数据


def demo_tasks():
    """覆盖全部判定分支的示例任务（7 条：4 派子代理 / 2 自己做 / 1 转后台）。"""
    return [
        {
            "name": "竞品资料检索与摘要",
            "est_tool_calls": 12,
            "files_touched": ["research/competitor-a.md", "research/competitor-b.md"],
            "is_research": True,
            "is_batch": False,
            "needs_user_input": False,
            "irreversible": False,
            "cross_session": False,
        },
        {
            "name": "批量截图改名归档",
            "est_tool_calls": 9,
            "files_touched": 60,
            "is_research": False,
            "is_batch": True,
            "needs_user_input": False,
            "irreversible": False,
            "cross_session": False,
        },
        {
            "name": "双文件口径对齐",
            "est_tool_calls": 2,
            "files_touched": ["deliver/report-draft.md", "deliver/report-final.md"],
            "is_research": False,
            "is_batch": False,
            "needs_user_input": False,
            "irreversible": False,
            "cross_session": False,
        },
        {
            "name": "多份PDF批量抽取字段",
            "est_tool_calls": 11,
            "files_touched": 8,
            "is_research": False,
            "is_batch": True,
            "needs_user_input": False,
            "irreversible": False,
            "cross_session": False,
        },
        {
            "name": "确认本期报告口径",
            "est_tool_calls": 2,
            "files_touched": 0,
            "is_research": False,
            "is_batch": False,
            "needs_user_input": True,
            "irreversible": False,
            "cross_session": False,
        },
        {
            "name": "查询本机运行环境版本",
            "est_tool_calls": 1,
            "files_touched": 0,
            "is_research": False,
            "is_batch": False,
            "needs_user_input": False,
            "irreversible": False,
            "cross_session": False,
        },
        {
            "name": "每日定时抓取行情入库",
            "est_tool_calls": 6,
            "files_touched": 1,
            "is_research": False,
            "is_batch": False,
            "needs_user_input": False,
            "irreversible": False,
            "cross_session": True,
        },
    ]


# ---------------------------------------------------------------- 入口


def build_parser():
    parser = argparse.ArgumentParser(
        prog="delegation_planner.py",
        description="委派决策器：读任务清单 JSON，输出每个任务该派子代理 / 自己做 / 转后台。",
        epilog="示例：python3 delegation_planner.py --demo ｜ python3 delegation_planner.py --task-file tasks.json --json",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task-file", metavar="X.json", help="任务清单 JSON 路径")
    group.add_argument("--demo", action="store_true", help="使用内置示例任务（覆盖全部分支）")
    parser.add_argument("--json", action="store_true", help="以 JSON 机读格式输出")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    stamp = now_stamp()

    if args.demo:
        source_label = "内置示例"
        try:
            tasks = [validate_task(raw, i) for i, raw in enumerate(demo_tasks())]
        except InputError as exc:  # 示例数据自身出错属于程序 bug，同样以 1 退出
            sys.stderr.write("错误：内置示例数据不合法 —— %s\n" % exc)
            return 1
    else:
        source_label = os.path.basename(args.task_file)
        try:
            tasks = load_tasks(args.task_file)
        except InputError as exc:
            sys.stderr.write("错误：%s\n" % exc)
            sys.stderr.write("提示：字段格式见脚本头部说明或用 --demo 查看合法样例。\n")
            return 1

    report = analyze(tasks)
    output = render_json(report, source_label, stamp) if args.json else render_text(report, source_label, stamp)
    sys.stdout.write(output + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
