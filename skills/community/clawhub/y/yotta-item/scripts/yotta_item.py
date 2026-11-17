#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""元题 yotta-item —— 本地、确定性的组卷与试卷校验引擎（零依赖，Python 3.8+）。

设计依据：项目设计稿（2026-09-24 定稿）。

边界：只读本地题库 / 双向细目表 / 试卷；核心路径不联网、不调用模型；
不生成题面内容；结论只作命题辅助，试卷定稿由命题组与教研组负责。

退出码：0 正常 / 1 触发闸门或组卷无法满足约束 / 2 输入错误 /
3 题库或蓝图校验错误 / 4 运行时错误。
"""

import argparse
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.3"
SCHEMA_VERSION = "1.0"
TOOL_NAME = "yotta-item"

DEFAULT_DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

DISCLAIMER = (
    "本文件由元题（yotta-item）基于本地题库与双向细目表的确定性计算生成，仅作命题辅助；"
    "题目内容来自学校自备题库，未生成或改写题面；难度标注为题库相对口径，"
    "不等于考后实测难度与区分度；试卷最终定稿由命题组与教研组负责。"
)


class ItemError(Exception):
    exit_code = 4

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InputError(ItemError):
    exit_code = 2


class ConfigError(ItemError):
    exit_code = 3


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def _as_number(value, where, field, minimum=None, allow_zero=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError("%s：%s 必须是数字" % (where, field))
    if allow_zero and value == 0:
        return value
    if minimum is not None and value < minimum:
        raise ConfigError("%s：%s 必须不小于 %s（当前 %r）" % (where, field, minimum, value))
    return value


def _as_positive_int(value, where, field):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ConfigError("%s：%s 必须是正整数（当前 %r）" % (where, field, value))
    return value


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


def load_bank(payload, where="bank"):
    """加载并校验题库。"""
    data = _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigError("%s：schema_version 必须是 %s（当前 %r）"
                          % (where, SCHEMA_VERSION, data.get("schema_version")))

    levels = data.get("difficulty_levels", DEFAULT_DIFFICULTY_LEVELS)
    if not isinstance(levels, list) or not all(isinstance(v, str) and v.strip() for v in levels):
        raise ConfigError("%s：difficulty_levels 必须是字符串数组" % where)
    levels = [v.strip() for v in levels]
    if len(levels) < 2 or len(levels) > 5:
        raise ConfigError("%s：difficulty_levels 需要 2-5 档（当前 %d 档）" % (where, len(levels)))
    if len(set(levels)) != len(levels):
        raise ConfigError("%s：difficulty_levels 不允许重复" % where)

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
            raise ConfigError("%s：id 不能为空" % where)
        item_id = item_id.strip()
        if item_id in by_id:
            raise ConfigError("%s：题目 id 重复：%s" % (where, item_id))
        if "type" not in raw:
            raise ConfigError("%s：题目 %s 缺少字段 type" % (where, item_id))
        item_type = raw.get("type")
        if not isinstance(item_type, str) or not item_type.strip():
            raise ConfigError("%s：题目 %s 的 type 不能为空" % (where, item_id))
        points = _as_number(raw.get("points"), "%s[%s]" % (where, item_id),
                            "points", minimum=0, allow_zero=False)
        if points <= 0:
            raise ConfigError("%s：题目 %s 的 points 必须大于 0（当前 %r）"
                              % (where, item_id, points))
        difficulty = raw.get("difficulty")
        if not isinstance(difficulty, str) or difficulty.strip() not in levels:
            raise ConfigError("%s：题目 %s 的 difficulty 不在题库档位内（当前 %r；可用：%s）"
                              % (where, item_id, difficulty, "、".join(levels)))
        knowledge = _string_list(raw.get("knowledge"), "%s[%s]" % (where, item_id),
                                 "knowledge", required=True)
        minutes = raw.get("minutes")
        if minutes is not None:
            minutes = _as_number(minutes, "%s[%s]" % (where, item_id), "minutes", minimum=0)
        source = raw.get("source")
        if source is not None and (not isinstance(source, str) or not source.strip()):
            raise ConfigError("%s：题目 %s 的 source 必须是非空字符串" % (where, item_id))

        item = {
            "id": item_id,
            "type": item_type.strip(),
            "points": points,
            "difficulty": difficulty.strip(),
            "knowledge": knowledge,
            "minutes": minutes,
            "source": source.strip() if isinstance(source, str) else None,
        }
        items.append(item)
        by_id[item_id] = item

    return {
        "schema_version": SCHEMA_VERSION,
        "subject": data.get("subject"),
        "grade": data.get("grade"),
        "difficulty_levels": levels,
        "items": items,
        "by_id": by_id,
    }


def load_blueprint(payload, where="blueprint", difficulty_levels=None):
    """加载并校验双向细目表（蓝图）。"""
    data = _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigError("%s：schema_version 必须是 %s（当前 %r）"
                          % (where, SCHEMA_VERSION, data.get("schema_version")))

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ConfigError("%s：title 不能为空" % where)
    title = title.strip()

    total_points = _as_number(data.get("total_points"), where, "total_points", minimum=0.000001)
    time_limit = _as_number(data.get("time_limit_minutes"), where,
                            "time_limit_minutes", minimum=0.000001)

    coverage = _string_list(data.get("coverage"), where, "coverage", required=False)
    if len(set(coverage)) != len(coverage):
        raise ConfigError("%s：coverage 不允许重复考点" % where)

    raw_sections = data.get("sections")
    if not isinstance(raw_sections, list) or not raw_sections:
        raise ConfigError("%s：sections 必须是非空数组" % where)

    levels = list(difficulty_levels) if difficulty_levels else list(DEFAULT_DIFFICULTY_LEVELS)
    sections = []
    by_id = {}
    computed_points = 0
    for raw in raw_sections:
        if not isinstance(raw, dict):
            raise ConfigError("%s：sections 元素必须是对象" % where)
        section_id = raw.get("id")
        if not isinstance(section_id, str) or not section_id.strip():
            raise ConfigError("%s：分节 id 不能为空" % where)
        section_id = section_id.strip()
        if section_id in by_id:
            raise ConfigError("%s：分节 id 重复：%s" % (where, section_id))
        section_type = raw.get("type")
        if not isinstance(section_type, str) or not section_type.strip():
            raise ConfigError("%s：分节 %s 的 type 不能为空" % (where, section_id))
        count = _as_positive_int(raw.get("count"), "%s[%s]" % (where, section_id), "count")
        points_each = _as_number(raw.get("points_each"), "%s[%s]" % (where, section_id),
                                 "points_each", minimum=0.000001)
        raw_difficulty = raw.get("difficulty")
        if not isinstance(raw_difficulty, dict) or not raw_difficulty:
            raise ConfigError("%s：分节 %s 的 difficulty 必须是非空对象" % (where, section_id))
        difficulty = {}
        for level, quota in raw_difficulty.items():
            if level not in levels:
                raise ConfigError("%s：分节 %s 的难度档 %r 不在可用档位内（%s）"
                                  % (where, section_id, level, "、".join(levels)))
            difficulty[level] = _as_positive_int(
                quota, "%s[%s].difficulty" % (where, section_id), level)
        if sum(difficulty.values()) != count:
            raise ConfigError("%s：分节 %s 的难度配额之和（%d）必须等于题量 count（%d）"
                              % (where, section_id, sum(difficulty.values()), count))
        knowledge = _string_list(raw.get("knowledge"), "%s[%s]" % (where, section_id),
                                 "knowledge", required=False)
        section = {
            "id": section_id,
            "title": raw.get("title") if isinstance(raw.get("title"), str) else section_id,
            "type": section_type.strip(),
            "count": count,
            "points_each": points_each,
            "difficulty": difficulty,
            "knowledge": knowledge,
        }
        sections.append(section)
        by_id[section_id] = section
        computed_points += count * points_each

    if abs(computed_points - total_points) > 1e-9:
        raise ConfigError("%s：蓝图总分不一致——sections 合计 %.2f 分，total_points 为 %.2f 分"
                          % (where, computed_points, total_points))

    return {
        "schema_version": SCHEMA_VERSION,
        "title": title,
        "total_points": total_points,
        "time_limit_minutes": time_limit,
        "coverage": coverage,
        "sections": sections,
        "by_id": by_id,
    }


def load_paper(payload, where="paper"):
    """加载试卷（只记题目 id 引用）。

    兼容两种形态：试卷对象（顶层 items）；以及 `assemble` 的 JSON 输出
    （题目在 paper.items 下），便于把组卷结果直接交给 check 复核。
    """
    data = _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    if "items" not in data and isinstance(data.get("paper"), dict):
        nested = data["paper"]
        data = {
            "schema_version": data.get("schema_version", nested.get("schema_version")),
            "title": nested.get("title", data.get("title")),
            "items": nested.get("items"),
        }
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigError("%s：schema_version 必须是 %s（当前 %r）"
                          % (where, SCHEMA_VERSION, data.get("schema_version")))
    raw_items = data.get("items")
    if not isinstance(raw_items, list):
        raise ConfigError("%s：items 必须是数组" % where)
    entries = []
    ids = []
    for raw in raw_items:
        if not isinstance(raw, dict):
            raise ConfigError("%s：items 元素必须是对象" % where)
        item_id = raw.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            raise ConfigError("%s：items 元素缺少 id" % where)
        section = raw.get("section")
        if section is not None and (not isinstance(section, str) or not section.strip()):
            raise ConfigError("%s：items 元素的 section 必须是非空字符串" % where)
        entries.append({"id": item_id.strip(),
                        "section": section.strip() if isinstance(section, str) else None})
        ids.append(item_id.strip())
    title = data.get("title")
    return {
        "schema_version": SCHEMA_VERSION,
        "title": title.strip() if isinstance(title, str) and title.strip() else where,
        "entries": entries,
        "ids": ids,
    }


def _finding(code, severity, message, evidence):
    return {"code": code, "severity": severity, "message": message, "evidence": evidence}


def select_items(bank, blueprint, seed=0):
    """按蓝图从题库确定性选题；同一输入 + 同一 seed 得到同一试卷。"""
    rng = random.Random(seed)
    used = set()
    covered_global = set()
    sections_out = []
    findings = []
    selected_all = []

    for section in blueprint["sections"]:
        candidates = [item for item in bank["items"] if item["type"] == section["type"]]
        quotas = dict(section["difficulty"])
        selected = []

        def take(pool):
            pool = sorted(pool, key=lambda entry: entry["id"])
            if not pool:
                return None
            chosen = pool[rng.randrange(len(pool))]
            used.add(chosen["id"])
            selected.append(chosen["id"])
            selected_all.append(chosen)
            quotas[chosen["difficulty"]] = quotas.get(chosen["difficulty"], 0) - 1
            for knowledge in chosen["knowledge"]:
                covered_global.add(knowledge)
            return chosen

        required = list(section["knowledge"])
        for knowledge in blueprint["coverage"]:
            if knowledge in covered_global or knowledge in required:
                continue
            if any(knowledge in item["knowledge"] for item in candidates):
                required.append(knowledge)

        for knowledge in required:
            pool = [item for item in candidates
                    if item["id"] not in used
                    and knowledge in item["knowledge"]
                    and quotas.get(item["difficulty"], 0) > 0]
            take(pool)

        while len(selected) < section["count"]:
            pool = [item for item in candidates
                    if item["id"] not in used and quotas.get(item["difficulty"], 0) > 0]
            if not pool:
                break
            take(pool)

        shortfall = section["count"] - len(selected)
        difficulty_selected = {}
        for item_id in selected:
            item = bank["by_id"][item_id]
            level = item["difficulty"]
            difficulty_selected[level] = difficulty_selected.get(level, 0) + 1
        difficulty_shortfall = {level: remain for level, remain in quotas.items() if remain > 0}
        knowledge_missing = []
        for knowledge in section["knowledge"]:
            if not any(knowledge in bank["by_id"][item_id]["knowledge"] for item_id in selected):
                knowledge_missing.append(knowledge)

        sections_out.append({
            "id": section["id"],
            "title": section["title"],
            "type": section["type"],
            "count": section["count"],
            "points_each": section["points_each"],
            "selected": selected,
            "shortfall": shortfall,
            "knowledge": list(section["knowledge"]),
            "knowledge_missing": knowledge_missing,
            "difficulty_selected": difficulty_selected,
            "difficulty_shortfall": difficulty_shortfall,
        })

        if shortfall > 0:
            findings.append(_finding(
                "insufficient_items", "high",
                "分节 %s（%s）需要 %d 题，题库仅能选出 %d 题（缺 %d 题）"
                % (section["id"], section["title"], section["count"], len(selected), shortfall),
                {"section": section["id"], "type": section["type"], "needed": section["count"],
                 "selected": len(selected), "shortfall": shortfall,
                 "difficulty_shortfall": difficulty_shortfall}))
        if knowledge_missing:
            findings.append(_finding(
                "coverage_gap", "medium",
                "分节 %s 未覆盖必考考点：%s" % (section["id"], "、".join(knowledge_missing)),
                {"section": section["id"], "missing": knowledge_missing}))

    required_coverage = list(blueprint["coverage"])
    covered = [knowledge for knowledge in required_coverage if knowledge in covered_global]
    missing = [knowledge for knowledge in required_coverage if knowledge not in covered_global]
    if missing:
        findings.append(_finding(
            "coverage_gap", "medium",
            "全卷未覆盖蓝图必考考点：%s" % "、".join(missing),
            {"missing": missing}))

    estimated = sum(item["minutes"] or 0 for item in selected_all)
    limit = blueprint["time_limit_minutes"]
    over = estimated > limit
    if over:
        findings.append(_finding(
            "time_over_budget", "medium",
            "预计作答 %.1f 分钟，超出限时 %.1f 分钟" % (estimated, limit),
            {"estimated": estimated, "limit": limit}))

    paper_items = []
    for section in sections_out:
        for item_id in section["selected"]:
            paper_items.append({"id": item_id, "section": section["id"]})

    totals = {
        "count": len(paper_items),
        "points": sum(bank["by_id"][entry["id"]]["points"] for entry in paper_items),
        "minutes": estimated,
    }
    difficulty_summary = {}
    for item in selected_all:
        level = item["difficulty"]
        difficulty_summary[level] = difficulty_summary.get(level, 0) + 1

    sources = sorted(set(item["source"] for item in selected_all if item["source"]))

    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "generated_at": _now(),
        "title": blueprint["title"],
        "seed": seed,
        "sections": sections_out,
        "paper": {"schema_version": SCHEMA_VERSION,
                  "title": blueprint["title"],
                  "items": paper_items},
        "totals": totals,
        "coverage": {"required": required_coverage, "covered": covered, "missing": missing},
        "difficulty_summary": difficulty_summary,
        "time_budget": {"limit": limit, "estimated": estimated, "over": over},
        "sources": {"subject": bank["subject"], "grade": bank["grade"], "item_sources": sources},
        "findings": findings,
        "disclaimer": DISCLAIMER,
    }


def check_paper(bank, paper, blueprint=None, time_limit_minutes=None):
    """对已有试卷做确定性校验（可对比蓝图）。"""
    findings = []
    ids = paper["ids"]
    known = [bank["by_id"][item_id] for item_id in ids if item_id in bank["by_id"]]
    unknown = sorted(set(item_id for item_id in ids if item_id not in bank["by_id"]))
    duplicates = sorted(set(item_id for item_id in ids if ids.count(item_id) > 1))

    if unknown:
        findings.append(_finding(
            "unknown_item", "high",
            "试卷包含题库中不存在的题目 id：%s" % "、".join(unknown),
            {"ids": unknown}))
    if duplicates:
        findings.append(_finding(
            "duplicate_item", "high",
            "试卷中题目重复出现：%s" % "、".join(duplicates),
            {"ids": duplicates}))

    totals = {
        "count": len(ids),
        "points": sum(item["points"] for item in known),
        "minutes": sum(item["minutes"] or 0 for item in known),
    }
    covered = set()
    for item in known:
        for knowledge in item["knowledge"]:
            covered.add(knowledge)

    sections_out = []
    if blueprint is not None:
        if abs(totals["points"] - blueprint["total_points"]) > 1e-9:
            findings.append(_finding(
                "total_points_mismatch", "high",
                "试卷总分 %.2f 分，蓝图要求 %.2f 分"
                % (totals["points"], blueprint["total_points"]),
                {"expected": blueprint["total_points"], "actual": totals["points"]}))

        unlabeled = [entry["id"] for entry in paper["entries"] if not entry["section"]]
        if unlabeled:
            findings.append(_finding(
                "section_label_missing", "low",
                "有 %d 道题未标注分节，无法逐节核对" % len(unlabeled),
                {"count": len(unlabeled), "ids": unlabeled[:10]}))

        for section in blueprint["sections"]:
            section_ids = [entry["id"] for entry in paper["entries"]
                           if entry["section"] == section["id"] and entry["id"] in bank["by_id"]]
            section_items = [bank["by_id"][item_id] for item_id in section_ids]
            if not section_items:
                findings.append(_finding(
                    "section_missing", "medium",
                    "蓝图分节 %s（%s）在试卷中没有任何题目" % (section["id"], section["title"]),
                    {"section": section["id"], "expected_count": section["count"]}))
                continue
            if len(section_items) != section["count"]:
                findings.append(_finding(
                    "section_count_mismatch", "medium",
                    "分节 %s 题量 %d，蓝图要求 %d"
                    % (section["id"], len(section_items), section["count"]),
                    {"section": section["id"], "expected": section["count"],
                     "actual": len(section_items)}))
            type_bad = [item["id"] for item in section_items if item["type"] != section["type"]]
            if type_bad:
                findings.append(_finding(
                    "section_type_mismatch", "medium",
                    "分节 %s 中题型不符的题目：%s" % (section["id"], "、".join(type_bad)),
                    {"section": section["id"], "expected_type": section["type"],
                     "ids": type_bad}))
            points_bad = [item["id"] for item in section_items
                          if abs(item["points"] - section["points_each"]) > 1e-9]
            if points_bad:
                findings.append(_finding(
                    "section_points_mismatch", "medium",
                    "分节 %s 中分值不符的题目：%s" % (section["id"], "、".join(points_bad)),
                    {"section": section["id"], "expected_points_each": section["points_each"],
                     "ids": points_bad}))
            actual_levels = {}
            for item in section_items:
                level = item["difficulty"]
                actual_levels[level] = actual_levels.get(level, 0) + 1
            if actual_levels != section["difficulty"]:
                findings.append(_finding(
                    "difficulty_mismatch", "medium",
                    "分节 %s 难度分布 %s，蓝图要求 %s"
                    % (section["id"], json.dumps(actual_levels, ensure_ascii=False),
                       json.dumps(section["difficulty"], ensure_ascii=False)),
                    {"section": section["id"], "expected": section["difficulty"],
                     "actual": actual_levels}))
            section_covered = set()
            for item in section_items:
                for knowledge in item["knowledge"]:
                    section_covered.add(knowledge)
            section_missing = [knowledge for knowledge in section["knowledge"]
                               if knowledge not in section_covered]
            if section_missing:
                findings.append(_finding(
                    "coverage_gap", "medium",
                    "分节 %s 未覆盖必考考点：%s"
                    % (section["id"], "、".join(section_missing)),
                    {"section": section["id"], "missing": section_missing}))

        global_missing = [knowledge for knowledge in blueprint["coverage"]
                          if knowledge not in covered]
        if global_missing:
            findings.append(_finding(
                "coverage_gap", "medium",
                "全卷未覆盖蓝图必考考点：%s" % "、".join(global_missing),
                {"missing": global_missing}))

    limit = time_limit_minutes
    if limit is None and blueprint is not None:
        limit = blueprint["time_limit_minutes"]
    if limit is not None and totals["minutes"] > limit:
        findings.append(_finding(
            "time_over_budget", "medium",
            "预计作答 %.1f 分钟，超出限时 %.1f 分钟" % (totals["minutes"], limit),
            {"estimated": totals["minutes"], "limit": limit}))

    difficulty_summary = {}
    for item in known:
        level = item["difficulty"]
        difficulty_summary[level] = difficulty_summary.get(level, 0) + 1

    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "generated_at": _now(),
        "title": paper["title"],
        "sections": sections_out,
        "totals": totals,
        "coverage": {"required": list(blueprint["coverage"]) if blueprint else [],
                     "covered": sorted(knowledge for knowledge in covered
                                       if not blueprint or knowledge in blueprint["coverage"]),
                     "missing": [knowledge for knowledge in (blueprint["coverage"] if blueprint else [])
                                 if knowledge not in covered]},
        "difficulty_summary": difficulty_summary,
        "time_budget": {"limit": limit, "estimated": totals["minutes"],
                        "over": bool(limit is not None and totals["minutes"] > limit)},
        "findings": findings,
        "disclaimer": DISCLAIMER,
    }


def render_assemble_markdown(result):
    lines = []
    lines.append("# 元题组卷报告：%s" % result["title"])
    lines.append("")
    subject = result["sources"].get("subject") or "未标注学科"
    grade = result["sources"].get("grade") or "未标注年级"
    lines.append("- 题库：%s / %s" % (subject, grade))
    lines.append("- 随机种子：%s" % result["seed"])
    lines.append("- 选卷题量：%d 题 / %s 分"
                 % (result["totals"]["count"], _format_number(result["totals"]["points"])))
    budget = result["time_budget"]
    lines.append("- 预计作答：%s 分钟（限时 %s 分钟）"
                 % (_format_number(budget["estimated"]), _format_number(budget["limit"])))
    lines.append("")
    lines.append("## 组卷结果")
    lines.append("")
    for section in result["sections"]:
        lines.append("### 分节明细：%s %s（%s · 每题 %s 分 · %d 题）"
                     % (section["id"], section["title"], section["type"],
                        _format_number(section["points_each"]), section["count"]))
        if not section["selected"]:
            lines.append("- （该分节未能选到题目）")
        for index, item_id in enumerate(section["selected"], start=1):
            lines.append("%d. %s" % (index, item_id))
        lines.append("")

    lines.append("## 覆盖矩阵")
    lines.append("")
    lines.append("| 考点 | 状态 | 覆盖题目 |")
    lines.append("| --- | --- | --- |")
    for knowledge in result["coverage"]["required"]:
        status = "缺失" if knowledge in result["coverage"]["missing"] else "已覆盖"
        lines.append("| %s | %s | - |" % (knowledge, status))
    if not result["coverage"]["required"]:
        lines.append("| （蓝图未声明必考考点） | - | - |")
    lines.append("")

    lines.append("## 难度分布")
    lines.append("")
    lines.append("| 难度 | 题量 |")
    lines.append("| --- | --- |")
    for level in sorted(result["difficulty_summary"]):
        lines.append("| %s | %d |" % (level, result["difficulty_summary"][level]))
    lines.append("")

    lines.append("## 时间预算")
    lines.append("")
    lines.append("- 预计作答：%s 分钟" % _format_number(budget["estimated"]))
    lines.append("- 限时：%s 分钟" % _format_number(budget["limit"]))
    lines.append("- 判定：%s" % ("超出限时" if budget["over"] else "在限时内"))
    lines.append("")

    if result["findings"]:
        lines.append("## 缺口清单")
        lines.append("")
        for finding in result["findings"]:
            lines.append("- [%s] %s" % (finding["severity"], finding["message"]))
        lines.append("")

    lines.append("## 声明")
    lines.append("")
    lines.append(result["disclaimer"])
    lines.append("")
    return "\n".join(lines)


def render_check_markdown(result):
    lines = []
    lines.append("# 元题试卷校验：%s" % result["title"])
    lines.append("")
    lines.append("- 题量：%d 题" % result["totals"]["count"])
    lines.append("- 总分：%s 分" % _format_number(result["totals"]["points"]))
    lines.append("- 预计作答：%s 分钟" % _format_number(result["totals"]["minutes"]))
    lines.append("")
    lines.append("## 试卷校验")
    lines.append("")
    if result["coverage"]["required"]:
        lines.append("- 必考考点：%s" % "、".join(result["coverage"]["required"]))
        lines.append("- 已覆盖考点：%s"
                     % ("、".join(result["coverage"]["covered"]) or "（无）"))
        lines.append("- 缺失考点：%s"
                     % ("、".join(result["coverage"]["missing"]) or "（无）"))
    if result["difficulty_summary"]:
        lines.append("- 难度分布：%s"
                     % "、".join("%s %d" % (level, result["difficulty_summary"][level])
                                 for level in sorted(result["difficulty_summary"])))
    lines.append("")
    lines.append("## 缺口清单")
    lines.append("")
    if result["findings"]:
        for finding in result["findings"]:
            lines.append("- [%s] %s" % (finding["severity"], finding["message"]))
    else:
        lines.append("- 未发现缺口。")
    lines.append("")
    lines.append("## 声明")
    lines.append("")
    lines.append(result["disclaimer"])
    lines.append("")
    return "\n".join(lines)


def _format_number(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


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


TEMPLATE_BANK = {
    "schema_version": SCHEMA_VERSION,
    "subject": "示例学科",
    "grade": "示例年级",
    "difficulty_levels": ["easy", "medium", "hard"],
    "items": [
        {"id": "SC-001", "type": "single_choice", "points": 3, "difficulty": "easy",
         "knowledge": ["示例考点A"], "minutes": 2, "source": "示例题库"},
        {"id": "SC-002", "type": "single_choice", "points": 3, "difficulty": "medium",
         "knowledge": ["示例考点B"], "minutes": 3, "source": "示例题库"},
        {"id": "FB-001", "type": "fill_blank", "points": 4, "difficulty": "easy",
         "knowledge": ["示例考点A"], "minutes": 3, "source": "示例题库"},
        {"id": "FB-002", "type": "fill_blank", "points": 4, "difficulty": "hard",
         "knowledge": ["示例考点C"], "minutes": 4, "source": "示例题库"},
    ],
}

TEMPLATE_BLUEPRINT = {
    "schema_version": SCHEMA_VERSION,
    "title": "示例单元测试",
    "total_points": 18,
    "time_limit_minutes": 20,
    "coverage": ["示例考点C"],
    "sections": [
        {"id": "S1", "title": "选择题", "type": "single_choice", "count": 2,
         "points_each": 3, "difficulty": {"easy": 1, "medium": 1},
         "knowledge": ["示例考点A"]},
        {"id": "S2", "title": "填空题", "type": "fill_blank", "count": 3,
         "points_each": 4, "difficulty": {"easy": 1, "hard": 2},
         "knowledge": ["示例考点C"]},
    ],
}

TEMPLATE_PAPER = {
    "schema_version": SCHEMA_VERSION,
    "title": "示例单元测试",
    "items": [{"id": "SC-001", "section": "S1"}, {"id": "SC-002", "section": "S1"}],
}


def cmd_template(args):
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_text(out_dir / "bank.json",
                json.dumps(TEMPLATE_BANK, ensure_ascii=False, indent=2) + "\n")
    _write_text(out_dir / "blueprint.json",
                json.dumps(TEMPLATE_BLUEPRINT, ensure_ascii=False, indent=2) + "\n")
    _write_text(out_dir / "paper.json",
                json.dumps(TEMPLATE_PAPER, ensure_ascii=False, indent=2) + "\n")
    print("已生成模板：%s（bank.json / blueprint.json / paper.json）" % out_dir)
    return 0


def _emit(payload, markdown, args):
    output = render_json(payload) if args.format == "json" else markdown
    if getattr(args, "out", None):
        target = resolve_output_path(args.out)
        _write_text(target, output + ("" if output.endswith("\n") else "\n"))
        print("已写入：%s" % target)
    else:
        print(output)


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


def _load_bank_and_blueprint(args):
    bank = load_bank(args.bank, "bank")
    blueprint = load_blueprint(args.blueprint, "blueprint",
                               difficulty_levels=bank["difficulty_levels"])
    return bank, blueprint


def cmd_assemble(args):
    bank, blueprint = _load_bank_and_blueprint(args)
    seed = args.seed if args.seed is not None else 0
    result = select_items(bank, blueprint, seed=seed)
    _emit(result, render_assemble_markdown(result), args)
    gate = _parse_gate(args.gate)
    if result["findings"]:
        return 1
    if gate is not None and len(result["findings"]) >= gate:
        return 1
    return 0


def cmd_check(args):
    bank = load_bank(args.bank, "bank")
    blueprint = None
    if args.blueprint:
        blueprint = load_blueprint(args.blueprint, "blueprint",
                                   difficulty_levels=bank["difficulty_levels"])
    paper = load_paper(args.paper, "paper")
    result = check_paper(bank, paper, blueprint)
    _emit(result, render_check_markdown(result), args)
    gate = _parse_gate(args.gate)
    if gate is not None and len(result["findings"]) >= gate:
        return 1
    return 0


def cmd_bank(args):
    bank = load_bank(args.bank, "bank")
    if args.bank_command == "validate":
        print("题库校验通过：%d 题（%s / %s；难度档：%s）"
              % (len(bank["items"]), bank["subject"] or "未标注学科",
                 bank["grade"] or "未标注年级", "、".join(bank["difficulty_levels"])))
        return 0
    print("题库：%d 题（%s / %s）"
          % (len(bank["items"]), bank["subject"] or "未标注学科",
             bank["grade"] or "未标注年级"))
    return 0


def cmd_blueprint(args):
    levels = None
    if args.bank:
        levels = load_bank(args.bank, "bank")["difficulty_levels"]
    blueprint = load_blueprint(args.blueprint, "blueprint", difficulty_levels=levels)
    print("蓝图校验通过：%s（%d 节 / %d 题 / %s 分 / 限时 %s 分钟）"
          % (blueprint["title"], len(blueprint["sections"]),
             sum(section["count"] for section in blueprint["sections"]),
             _format_number(blueprint["total_points"]),
             _format_number(blueprint["time_limit_minutes"])))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME, description="元题 —— 本地、确定性的组卷与试卷校验")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    assemble = sub.add_parser("assemble", help="按蓝图从题库组卷")
    assemble.add_argument("--bank", required=True)
    assemble.add_argument("--blueprint", required=True)
    assemble.add_argument("--seed", type=int, default=0)
    assemble.add_argument("--format", choices=("md", "json"), default="md")
    assemble.add_argument("--out")
    assemble.add_argument("--gate")
    assemble.set_defaults(func=cmd_assemble)

    check = sub.add_parser("check", help="对已有试卷做缺口检查")
    check.add_argument("--bank", required=True)
    check.add_argument("--paper", required=True)
    check.add_argument("--blueprint")
    check.add_argument("--format", choices=("md", "json"), default="md")
    check.add_argument("--out")
    check.add_argument("--gate")
    check.set_defaults(func=cmd_check)

    bank_cmd = sub.add_parser("bank", help="题库操作")
    bank_sub = bank_cmd.add_subparsers(dest="bank_command", required=True)
    for name in ("validate", "show"):
        entry = bank_sub.add_parser(name)
        entry.add_argument("--bank", required=True)
    bank_cmd.set_defaults(func=cmd_bank)

    blueprint_cmd = sub.add_parser("blueprint", help="蓝图操作")
    blueprint_sub = blueprint_cmd.add_subparsers(dest="blueprint_command", required=True)
    for name in ("validate", "show"):
        entry = blueprint_sub.add_parser(name)
        entry.add_argument("--blueprint", required=True)
        entry.add_argument("--bank")
    blueprint_cmd.set_defaults(func=cmd_blueprint)

    template = sub.add_parser("template", help="生成题库 / 蓝图 / 试卷模板")
    template.add_argument("--output-dir", required=True)
    template.set_defaults(func=cmd_template)
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
        return args.func(args)
    except ItemError as exc:
        sys.stderr.write("错误：%s\n" % exc.message)
        return exc.exit_code
    except OSError as exc:
        sys.stderr.write("错误：文件操作失败：%s\n" % exc)
        return 4


if __name__ == "__main__":
    sys.exit(main())
