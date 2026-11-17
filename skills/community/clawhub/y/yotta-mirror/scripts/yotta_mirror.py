#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""元镜 yotta-mirror —— 本地、确定性的学情分析引擎（零依赖，Python 3.8+ 标准库）。

设计依据：项目设计稿（2026-09-24 定稿）。

边界：只读本地结构化表格（CSV / TSV / stdin），核心路径不联网、不调用模型；
结论只作为教学改进线索，并强制附带数据证据；低样本一律降级为人工复核项。

退出码：0 正常 / 1 触发闸门 / 2 输入错误 / 3 配置或映射错误 / 4 运行时错误。
"""

import argparse
import csv
import hashlib
import io
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.3"
SCHEMA_VERSION = "1.0"
TOOL_NAME = "yotta-mirror"

DISCLAIMER = (
    "本报告由元镜（yotta-mirror）基于本地数据的确定性统计生成，仅用于教学改进与备课决策，"
    "不用于学生评价、排名或升学判断；低样本与分界附近的结论需人工复核后再使用。"
)

DEFAULT_CONFIG = {
    "mastery": {"weak_below": 0.6, "solid_at_or_above": 0.8},
    "layers": {"a_at_or_above": 0.85, "b_at_or_above": 0.7},
    "min_respondents": 3,
    "critical_margin": 0.05,
}

DIFFICULTIES = ("easy", "medium", "hard")


class MirrorError(Exception):
    """元镜错误基类。"""

    exit_code = 4

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InputError(MirrorError):
    exit_code = 2


class ConfigError(MirrorError):
    exit_code = 3


# ---------------------------------------------------------------- 规范化与解析

def normalize_text(text):
    """统一换行与 BOM；不改动内容语义。"""
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    return text.replace("\ufeff", "").replace("\r\n", "\n").replace("\r", "\n")


def _split_lines(text):
    lines = []
    for raw in normalize_text(text).split("\n"):
        if not raw.strip():
            continue
        lines.append(raw)
    return lines


def parse_table(text):
    """解析 CSV / TSV（首行表头，第一列 = 学生标识）。"""
    lines = _split_lines(text)
    if not lines:
        raise InputError("输入为空：至少需要一行表头与一行学生数据")
    header = lines[0]
    delimiter = "\t" if "\t" in header else ","
    reader = csv.reader(io.StringIO("\n".join(lines)), delimiter=delimiter)
    rows = []
    columns = None
    for index, row in enumerate(reader):
        cells = [cell.strip() for cell in row]
        if columns is None:
            columns = cells
            if not columns or not any(columns):
                raise InputError("表头为空：第一行应为列名（第一列 = 学生标识）")
            continue
        if not any(cells):
            continue
        if len(cells) != len(columns):
            raise InputError(
                "第 %d 行有 %d 列，与表头 %d 列不一致" % (index + 1, len(cells), len(columns))
            )
        rows.append(cells)
    if not rows:
        raise InputError("没有学生数据行（表头之后为空）")
    return {"columns": columns, "rows": rows}


# ---------------------------------------------------------------- 映射与配置

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


def load_items(payload, where="items"):
    """加载并校验题目-知识点映射。"""
    data = _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    version = data.get("schema_version")
    if version != SCHEMA_VERSION:
        raise ConfigError(
            "%s：schema_version 必须是 %s（当前 %r）" % (where, SCHEMA_VERSION, version)
        )
    raw_items = data.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise ConfigError("%s：items 必须是非空数组" % where)
    items = []
    by_id = {}
    for raw in raw_items:
        if not isinstance(raw, dict):
            raise ConfigError("%s：items 元素必须是对象" % where)
        item_id = raw.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            raise ConfigError("%s：题目 id 不能为空" % where)
        item_id = item_id.strip()
        if item_id in by_id:
            raise ConfigError("%s：题目 id 重复：%s" % (where, item_id))
        max_score = raw.get("max_score")
        if isinstance(max_score, bool) or not isinstance(max_score, (int, float)) or max_score <= 0:
            raise ConfigError("%s：题目 %s 的 max_score 必须是正数" % (where, item_id))
        knowledge = raw.get("knowledge")
        if not isinstance(knowledge, list) or not knowledge or not all(
                isinstance(k, str) and k.strip() for k in knowledge):
            raise ConfigError("%s：题目 %s 的 knowledge 必须是非空字符串数组" % (where, item_id))
        difficulty = raw.get("difficulty")
        if difficulty is not None and difficulty not in DIFFICULTIES:
            raise ConfigError(
                "%s：题目 %s 的 difficulty 只能是 %s" % (where, item_id, "/".join(DIFFICULTIES))
            )
        item = {
            "id": item_id,
            "max_score": float(max_score),
            "knowledge": [k.strip() for k in knowledge],
        }
        if difficulty:
            item["difficulty"] = difficulty
        items.append(item)
        by_id[item_id] = item
    return {
        "schema_version": SCHEMA_VERSION,
        "items": items,
        "by_id": by_id,
        "order": [item["id"] for item in items],
    }


def _rate(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError("配置项 %s 必须是 0-1 之间的数字" % label)
    value = float(value)
    if value < 0 or value > 1:
        raise ConfigError("配置项 %s 必须在 0-1 之间（当前 %s）" % (label, value))
    return value


def load_config(payload, where="config"):
    """加载阈值配置；缺省用内置默认值，支持部分覆盖。"""
    config = {
        "mastery": dict(DEFAULT_CONFIG["mastery"]),
        "layers": dict(DEFAULT_CONFIG["layers"]),
        "min_respondents": DEFAULT_CONFIG["min_respondents"],
        "critical_margin": DEFAULT_CONFIG["critical_margin"],
    }
    if payload is None:
        return config
    data = _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    allowed = {"schema_version", "mastery", "layers", "min_respondents", "critical_margin"}
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ConfigError("%s：未知配置项：%s" % (where, "、".join(unknown)))
    if "schema_version" in data and data["schema_version"] != SCHEMA_VERSION:
        raise ConfigError("%s：schema_version 必须是 %s" % (where, SCHEMA_VERSION))
    mastery = data.get("mastery")
    if mastery is not None:
        if not isinstance(mastery, dict):
            raise ConfigError("%s：mastery 必须是对象" % where)
        for key in ("weak_below", "solid_at_or_above"):
            if key in mastery:
                config["mastery"][key] = _rate(mastery[key], "mastery.%s" % key)
    layers = data.get("layers")
    if layers is not None:
        if not isinstance(layers, dict):
            raise ConfigError("%s：layers 必须是对象" % where)
        for key in ("a_at_or_above", "b_at_or_above"):
            if key in layers:
                config["layers"][key] = _rate(layers[key], "layers.%s" % key)
    if "min_respondents" in data:
        value = data["min_respondents"]
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ConfigError("%s：min_respondents 必须是不小于 1 的整数" % where)
        config["min_respondents"] = value
    if "critical_margin" in data:
        margin = data["critical_margin"]
        if isinstance(margin, bool) or not isinstance(margin, (int, float)) or margin < 0:
            raise ConfigError("%s：critical_margin 必须是不小于 0 的数字" % where)
        config["critical_margin"] = float(margin)
    if config["mastery"]["weak_below"] >= config["mastery"]["solid_at_or_above"]:
        raise ConfigError(
            "%s：weak_below 必须小于 solid_at_or_above（当前 %.2f / %.2f）"
            % (where, config["mastery"]["weak_below"], config["mastery"]["solid_at_or_above"])
        )
    if config["layers"]["b_at_or_above"] >= config["layers"]["a_at_or_above"]:
        raise ConfigError(
            "%s：b_at_or_above 必须小于 a_at_or_above（当前 %.2f / %.2f）"
            % (where, config["layers"]["b_at_or_above"], config["layers"]["a_at_or_above"])
        )
    return config


# ---------------------------------------------------------------- 主分析

def anonymize_id(student):
    """可复算的匿名代号：同一输入得到同一代号。"""
    digest = hashlib.sha256(str(student).encode("utf-8")).hexdigest()
    return "S-" + digest[:8]


def _to_number(cell, item_id, student):
    try:
        return float(cell)
    except (TypeError, ValueError):
        raise InputError(
            "学生 %s 的题目 %s 不是数字：%r（可留空表示缺失）" % (student, item_id, cell)
        )


def analyze(table, item_map, config, now=None, anonymize=False):
    """确定性学情分析：返回稳定结构的结果对象。"""
    columns = table["columns"]
    rows = table["rows"]
    student_column = columns[0]
    item_columns = columns[1:]
    unknown = [name for name in item_columns if name not in item_map["by_id"]]
    if unknown:
        raise InputError("表格列不在题目映射中：%s" % "、".join(unknown))
    missing_items = [item_id for item_id in item_map["order"] if item_id not in item_columns]
    if missing_items:
        raise InputError("题目映射声明但表格缺失的题目：%s" % "、".join(missing_items))

    students = []
    seen = set()
    scores = {}
    missing_cells = 0
    for row_index, row in enumerate(rows, start=2):
        raw_student = row[0]
        if not raw_student:
            raise InputError("第 %d 行缺少学生标识" % row_index)
        if raw_student in seen:
            raise InputError("学生标识重复：%s（请先合并重复行）" % raw_student)
        seen.add(raw_student)
        display = anonymize_id(raw_student) if anonymize else raw_student
        students.append({"raw": raw_student, "id": display})
        scores[raw_student] = {}
        for cell, item_id in zip(row[1:], item_columns):
            item = item_map["by_id"][item_id]
            if cell == "":
                missing_cells += 1
                scores[raw_student][item_id] = None
                continue
            value = _to_number(cell, item_id, raw_student)
            if value < 0 or value > item["max_score"]:
                raise InputError(
                    "学生 %s 的题目 %s 得分 %s 超出范围（0 - %s）"
                    % (raw_student, item_id, value, item["max_score"])
                )
            scores[raw_student][item_id] = value

    warnings = []
    if missing_cells:
        warnings.append("存在 %d 个缺失单元格（缺失不计入该题分母，已单独计数）" % missing_cells)

    items_stats = []
    for item_id in item_map["order"]:
        item = item_map["by_id"][item_id]
        values = [scores[student["raw"]][item_id] for student in students]
        answered = [v for v in values if v is not None]
        respondents = len(answered)
        total = sum(answered)
        rate = (total / (respondents * item["max_score"])) if respondents else None
        items_stats.append({
            "id": item_id,
            "max_score": item["max_score"],
            "knowledge": list(item["knowledge"]),
            "respondents": respondents,
            "missing": len(values) - respondents,
            "mean": (total / respondents) if respondents else None,
            "rate": rate,
            "full_marks": len([v for v in answered if v == item["max_score"]]),
            "zero": len([v for v in answered if v == 0]),
        })

    knowledge_names = []
    for item_id in item_map["order"]:
        for name in item_map["by_id"][item_id]["knowledge"]:
            if name not in knowledge_names:
                knowledge_names.append(name)
    knowledge_rows = []
    for name in knowledge_names:
        member_items = [item_id for item_id in item_map["order"]
                        if name in item_map["by_id"][item_id]["knowledge"]]
        numerator = 0.0
        denominator = 0.0
        respondents_min = None
        for item_id in member_items:
            item = item_map["by_id"][item_id]
            for student in students:
                value = scores[student["raw"]][item_id]
                if value is None:
                    continue
                numerator += value
                denominator += item["max_score"]
            answered = len([s for s in students if scores[s["raw"]][item_id] is not None])
            respondents_min = answered if respondents_min is None else min(respondents_min, answered)
        rate = (numerator / denominator) if denominator else None
        if rate is None:
            level = None
        elif rate < config["mastery"]["weak_below"]:
            level = "weak"
        elif rate >= config["mastery"]["solid_at_or_above"]:
            level = "solid"
        else:
            level = "developing"
        knowledge_rows.append({
            "name": name,
            "items": member_items,
            "respondents": respondents_min or 0,
            "rate": rate,
            "level": level,
        })
    knowledge_rows.sort(key=lambda row: (row["rate"] is None, row["rate"] or 0.0, row["name"]))

    layers = {"a": [], "b": [], "c": [], "critical": []}
    student_rates = {}
    for student in students:
        total = 0.0
        maximum = 0.0
        for item_id in item_map["order"]:
            value = scores[student["raw"]][item_id]
            if value is None:
                continue
            total += value
            maximum += item_map["by_id"][item_id]["max_score"]
        rate = (total / maximum) if maximum else None
        student_rates[student["raw"]] = rate
        if rate is None:
            layers["c"].append(student["id"])
            continue
        if rate >= config["layers"]["a_at_or_above"]:
            layers["a"].append(student["id"])
        elif rate >= config["layers"]["b_at_or_above"]:
            layers["b"].append(student["id"])
        else:
            layers["c"].append(student["id"])
        margin = config["critical_margin"]
        for boundary in (config["layers"]["a_at_or_above"], config["layers"]["b_at_or_above"]):
            if abs(rate - boundary) <= margin:
                layers["critical"].append(student["id"])
                break

    review_items = []
    for row in items_stats:
        if row["respondents"] == 0:
            review_items.append({
                "reason": "item_no_data",
                "item": row["id"],
                "detail": "题目 %s 无有效作答数据" % row["id"],
            })
        elif row["respondents"] < config["min_respondents"]:
            review_items.append({
                "reason": "item_low_sample",
                "item": row["id"],
                "respondents": row["respondents"],
                "detail": "题目 %s 样本量 %d 低于阈值 %d"
                          % (row["id"], row["respondents"], config["min_respondents"]),
            })

    diagnoses = []
    for row in knowledge_rows:
        if row["level"] != "weak":
            continue
        if row["respondents"] < config["min_respondents"]:
            review_items.append({
                "reason": "knowledge_low_sample",
                "knowledge": row["name"],
                "respondents": row["respondents"],
                "detail": "知识点「%s」样本量 %d 低于阈值 %d，降级为人工复核"
                          % (row["name"], row["respondents"], config["min_respondents"]),
            })
            continue
        weak_below = config["mastery"]["weak_below"]
        severity = "high" if row["rate"] < weak_below * 0.75 else "medium"
        diagnoses.append({
            "knowledge": row["name"],
            "severity": severity,
            "rate": row["rate"],
            "threshold": weak_below,
            "evidence": {
                "items": list(row["items"]),
                "respondents": row["respondents"],
                "rate": row["rate"],
                "threshold": weak_below,
            },
        })
    diagnoses.sort(key=lambda row: (row["rate"], row["knowledge"]))

    for student in students:
        missing = len([item_id for item_id in item_map["order"]
                       if scores[student["raw"]][item_id] is None])
        if missing:
            review_items.append({
                "reason": "student_missing_answers",
                "student": student["id"],
                "missing": missing,
                "detail": "学生 %s 有 %d 道题未作答" % (student["id"], missing),
            })
    for student in students:
        rate = student_rates[student["raw"]]
        if rate is None or student["id"] not in layers["critical"]:
            continue
        boundary = None
        for candidate in (config["layers"]["a_at_or_above"], config["layers"]["b_at_or_above"]):
            if abs(rate - candidate) <= config["critical_margin"]:
                boundary = candidate
                break
        review_items.append({
            "reason": "critical_student",
            "student": student["id"],
            "rate": rate,
            "boundary": boundary,
            "detail": "学生 %s 得分率 %.1f%% 距分界线 %.0f%% 在 %.0f 个百分点内，属临界生，需人工复核"
                      % (student["id"], rate * 100, (boundary or 0) * 100,
                         config["critical_margin"] * 100),
        })

    generated_at = now or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "tool_version": VERSION,
        "generated_at": generated_at,
        "input": {
            "students": len(students),
            "items": len(item_map["order"]),
            "missing_cells": missing_cells,
            "student_column": student_column,
            "anonymized": bool(anonymize),
        },
        "quality": {"missing_cells": missing_cells, "warnings": warnings},
        "items_stats": items_stats,
        "knowledge": knowledge_rows,
        "layers": layers,
        "diagnoses": diagnoses,
        "review_items": review_items,
        "summary": {
            "students": len(students),
            "items": len(item_map["order"]),
            "knowledge_points": len(knowledge_rows),
            "weak_points": len(diagnoses),
            "layer_counts": {"a": len(layers["a"]), "b": len(layers["b"]), "c": len(layers["c"])},
            "critical_students": len(layers["critical"]),
            "review_items": len(review_items),
        },
        "thresholds": {
            "mastery": dict(config["mastery"]),
            "layers": dict(config["layers"]),
            "min_respondents": config["min_respondents"],
            "critical_margin": config["critical_margin"],
        },
        "disclaimer": DISCLAIMER,
    }


# ---------------------------------------------------------------- 渲染

def _percent(value):
    return "—" if value is None else "%.1f%%" % (value * 100)


def render_markdown(result):
    lines = []
    lines.append("# 学情分析报告（元镜 yotta-mirror %s）" % result["tool_version"])
    lines.append("")
    lines.append("生成时间：%s" % result["generated_at"])
    lines.append("")
    lines.append("## 1. 输入摘要")
    lines.append("")
    lines.append("- 学生数：%d ｜ 题目数：%d ｜ 缺失单元格：%d"
                 % (result["input"]["students"], result["input"]["items"],
                    result["input"]["missing_cells"]))
    lines.append("- 学生标识：%s" % ("已匿名化（可复算代号）" if result["input"]["anonymized"]
                                     else "原始标识（对外分享请加 --anonymize）"))
    for warning in result["quality"]["warnings"]:
        lines.append("- 数据提示：%s" % warning)
    lines.append("")
    lines.append("## 2. 逐题统计")
    lines.append("")
    lines.append("| 题目 | 满分 | 作答 | 缺失 | 平均分 | 得分率 | 满分人数 | 零分人数 | 知识点 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in result["items_stats"]:
        lines.append("| %s | %s | %d | %d | %s | %s | %d | %d | %s |" % (
            row["id"], ("%g" % row["max_score"]), row["respondents"], row["missing"],
            ("—" if row["mean"] is None else "%.2f" % row["mean"]),
            _percent(row["rate"]), row["full_marks"], row["zero"],
            "、".join(row["knowledge"]),
        ))
    lines.append("")
    lines.append("## 3. 知识点掌握")
    lines.append("")
    lines.append("| 知识点 | 题目 | 样本量 | 掌握率 | 判定 |")
    lines.append("| --- | --- | --- | --- | --- |")
    level_label = {"weak": "薄弱", "developing": "待巩固", "solid": "掌握", None: "数据不足"}
    for row in result["knowledge"]:
        lines.append("| %s | %s | %d | %s | %s |" % (
            row["name"], "、".join(row["items"]), row["respondents"],
            _percent(row["rate"]), level_label.get(row["level"], "—"),
        ))
    lines.append("")
    lines.append("## 4. 学生分层")
    lines.append("")
    layers = result["layers"]
    lines.append("- A 层（%.0f%% 及以上）：%d 人%s" % (
        result["thresholds"]["layers"]["a_at_or_above"] * 100, len(layers["a"]),
        ("：" + "、".join(layers["a"])) if layers["a"] else ""))
    lines.append("- B 层：%d 人%s" % (
        len(layers["b"]), ("：" + "、".join(layers["b"])) if layers["b"] else ""))
    lines.append("- C 层：%d 人%s" % (
        len(layers["c"]), ("：" + "、".join(layers["c"])) if layers["c"] else ""))
    lines.append("- 临界生（待人工复核）：%d 人%s" % (
        len(layers["critical"]), ("：" + "、".join(layers["critical"])) if layers["critical"] else ""))
    lines.append("")
    lines.append("## 5. 薄弱点诊断")
    lines.append("")
    if not result["diagnoses"]:
        lines.append("本次数据未出现低于薄弱阈值（%s）的知识点。" % _percent(result["thresholds"]["mastery"]["weak_below"]))
    else:
        for item in result["diagnoses"]:
            evidence = item["evidence"]
            lines.append("- **[%s] %s**：掌握率 %s（薄弱阈值 %s，样本量 %d）"
                         % ("高" if item["severity"] == "high" else "中", item["knowledge"],
                            _percent(evidence["rate"]), _percent(evidence["threshold"]),
                            evidence["respondents"]))
            lines.append("  - 证据：涉及题目 %s；按分值加权统计，可复算（同数据同结论）"
                         % "、".join(evidence["items"]))
    lines.append("")
    lines.append("## 6. 人工复核")
    lines.append("")
    if not result["review_items"]:
        lines.append("无。")
    else:
        for item in result["review_items"]:
            lines.append("- %s" % item["detail"])
    lines.append("")
    lines.append("## 7. 免责声明")
    lines.append("")
    lines.append(result["disclaimer"])
    lines.append("")
    return "\n".join(lines)


def render_json(result):
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)


# ---------------------------------------------------------------- 安全边界

def resolve_output_path(path):
    """输出路径防护：拒绝目录、拒绝包含 .. 的越界路径。"""
    parts = Path(str(path)).parts
    if ".." in parts:
        raise InputError("输出路径不允许包含 ..（防越界写入）：%s" % path)
    target = Path(str(path))
    if target.exists() and target.is_dir():
        raise InputError("输出路径是目录，不能写入：%s" % path)
    if not target.parent.exists():
        raise InputError("输出目录不存在：%s" % target.parent)
    return target


# ---------------------------------------------------------------- CLI

TEMPLATE_CSV = "student,T1,T2,T3\n学生A,5,2,1\n"
TEMPLATE_ITEMS = {
    "schema_version": SCHEMA_VERSION,
    "items": [
        {"id": "T1", "max_score": 5, "knowledge": ["示例知识点A"], "difficulty": "easy"},
        {"id": "T2", "max_score": 2, "knowledge": ["示例知识点A"]},
        {"id": "T3", "max_score": 1, "knowledge": ["示例知识点B"]},
    ],
}


def _write_text(path, text):
    # Python 3.8 兼容：Path.write_text 的 newline 参数自 3.10 才支持
    with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def cmd_template(args):
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_text(out_dir / "scores.csv", TEMPLATE_CSV)
    _write_text(out_dir / "item-map.json",
                json.dumps(TEMPLATE_ITEMS, ensure_ascii=False, indent=2) + "\n")
    _write_text(out_dir / "thresholds.json",
                json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2) + "\n")
    print("已生成录入模板：%s（scores.csv / item-map.json / thresholds.json）" % out_dir)
    return 0


def cmd_config_validate(args):
    config = load_config(args.pack, "config")
    print("配置校验通过：weak_below=%s / solid_at_or_above=%s / min_respondents=%d"
          % (config["mastery"]["weak_below"], config["mastery"]["solid_at_or_above"],
             config["min_respondents"]))
    return 0


def _parse_gate(expr):
    if not expr:
        return None
    if not expr.startswith("weak="):
        raise InputError("--gate 只支持 weak=<数量> 形式（当前 %r）" % expr)
    try:
        value = int(expr.split("=", 1)[1])
    except ValueError:
        raise InputError("--gate 的 weak 阈值必须是整数：%r" % expr)
    if value < 1:
        raise InputError("--gate 的 weak 阈值必须不小于 1：%r" % expr)
    return value


def cmd_analyze(args, stdin_text=None):
    if args.stdin:
        text = stdin_text if stdin_text is not None else sys.stdin.read()
    else:
        if not args.input:
            raise InputError("analyze 需要 --input <文件> 或 --stdin")
        path = Path(args.input)
        if not path.is_file():
            raise InputError("输入文件不存在：%s" % path)
        text = path.read_text(encoding="utf-8")
    table = parse_table(text)
    item_map = load_items(args.items, "items")
    config = load_config(args.config, "config")
    result = analyze(table, item_map, config, anonymize=args.anonymize)
    gate = _parse_gate(args.gate)
    output = render_json(result) if args.format == "json" else render_markdown(result)
    if args.out:
        target = resolve_output_path(args.out)
        _write_text(target, output + ("" if output.endswith("\n") else "\n"))
        print("已写入：%s" % target)
    else:
        print(output)
    if gate is not None and len(result["diagnoses"]) >= gate:
        return 1
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="yotta-mirror",
        description="元镜 —— 本地、确定性的学情分析引擎（零依赖，不联网）",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command")

    analyze = sub.add_parser("analyze", help="分析成绩 / 答题表并生成诊断报告")
    analyze.add_argument("--input")
    analyze.add_argument("--stdin", action="store_true")
    analyze.add_argument("--items", required=True, help="题目-知识点映射 JSON")
    analyze.add_argument("--config", help="阈值配置 JSON（可选）")
    analyze.add_argument("--format", choices=("md", "json"), default="md")
    analyze.add_argument("--out")
    analyze.add_argument("--anonymize", action="store_true", help="学生标识匿名化（可复算代号）")
    analyze.add_argument("--gate", help="weak=<数量>：薄弱知识点数量达到该值时退出码 1")

    template = sub.add_parser("template", help="生成录入模板（成绩表 / 映射 / 阈值）")
    template.add_argument("--output-dir", required=True)

    config = sub.add_parser("config", help="配置操作")
    config_sub = config.add_subparsers(dest="config_command")
    validate = config_sub.add_parser("validate", help="校验阈值配置")
    validate.add_argument("--pack", required=True)
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
        if args.command == "analyze":
            return cmd_analyze(args, stdin_text=stdin_text)
        if args.command == "template":
            return cmd_template(args)
        if args.command == "config":
            if getattr(args, "config_command", None) == "validate":
                return cmd_config_validate(args)
            parser.parse_args(["config", "--help"])
            return 2
        sys.stderr.write("错误：未知命令。可用：analyze / template / config validate\n")
        return 2
    except MirrorError as exc:
        sys.stderr.write("错误：%s\n" % exc.message)
        return exc.exit_code
    except OSError as exc:
        sys.stderr.write("错误：文件操作失败：%s\n" % exc)
        return 4


if __name__ == "__main__":
    sys.exit(main())
