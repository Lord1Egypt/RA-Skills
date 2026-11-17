#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yotta-compliance（元规）—— 零依赖确定性合规条款审查内核
============================================================

设计依据：项目设计稿（2026-09-24 定稿）。
S2 范围：规范化与偏移映射 / 结构解析 / 规则包加载与校验 / 匹配原语 /
断言求值 / 证据链 / Markdown + JSON 报告 / CLI。

可信契约（红线）
----------------
- 结论优先于语言生成：没有原文证据，不输出风险结论；
- 核心路径不调用模型、不联网；规则包是只读 JSON 数据，绝不当作代码执行；
- 每条 finding 的 quote 必须由原文切片产生，start/end 基于原始文本；
- absence 断言必须给出搜索范围，不伪造原文引用；
- mapping_only 框架只做主题映射，不产生该框架的独立合规结论。

用法
----
  python3 scripts/yotta_compliance.py review --input contract.md --frameworks pipl,data-export
  python3 scripts/yotta_compliance.py review --input contract.md --format json --out report.json
  python3 scripts/yotta_compliance.py review --stdin --frameworks pipl --gate high
  python3 scripts/yotta_compliance.py rules list --framework pipl
  python3 scripts/yotta_compliance.py rules show PIPL-DATA-001
  python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
  python3 scripts/yotta_compliance.py --version

退出码：0 = 审查完成未超过 gate；1 = 存在达到 gate 的 finding；
2 = 输入缺失 / 编码错误 / 路径不可用；3 = 规则包缺失或 schema 无效；4 = CLI 用法错误。
Windows 下用 python 代替 python3。
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

try:
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VERSION = "0.1.3"
TOOL = "yotta-compliance"
TOOL_CN = "元规"
SCHEMA_VERSION = "1.0"

# 输入上限与证据上限（设计 §12 / §9）
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_EVIDENCE_PER_FINDING = 5

DEFAULT_FRAMEWORKS = ("pipl", "data-export")
SUPPORTED_SUFFIXES = (".txt", ".md", ".markdown")
UNSUPPORTED_SUFFIXES = (".pdf", ".docx", ".doc")

SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
SEVERITIES = tuple(SEVERITY_ORDER)
CONFIDENCE_LEVELS = ("low", "medium", "high")
COVERAGE_LEVELS = ("baseline_review", "mapping_only")
CONDITION_KINDS = ("keyword", "regex", "clause_type", "section_anchor")
ASSERT_OPERATORS = ("absent", "present", "numeric_compare", "date_compare", "duration_compare")
COMPARE_OPERATORS = ("gte", "lte", "gt", "lt", "eq", "ne")
EVIDENCE_KINDS = ("matched_span", "document_scope", "section_scope")
SCOPE_KINDS = ("document", "section")
DURATION_UNITS = {"day": ("天", "日"), "month": ("个月", "月"), "year": ("年",)}

DISCLAIMER = "本工具提供基于确定性规则的条款审查建议与证据链，不构成法律意见。"
MAPPING_ONLY_NOTE = "仅主题映射，不等同于对该框架的合规审查。"

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULES_DIR = os.path.normpath(os.path.join(HERE, os.pardir, "rules"))


# ---------------------------------------------------------------------------
# 异常与退出码
# ---------------------------------------------------------------------------
class ComplianceError(Exception):
    """内核异常基类：exit_code 决定 CLI 退出码。"""

    exit_code = 4


class InputError(ComplianceError):
    exit_code = 2


class RulePackError(ComplianceError):
    exit_code = 3


class UsageError(ComplianceError):
    exit_code = 4


# ---------------------------------------------------------------------------
# 规范化与偏移映射（设计 §7）
# ---------------------------------------------------------------------------
class NormalizedText(object):
    """规范化文本 + 每个字符回到原始文本的偏移区间。

    start/end 一律基于原始文本；quote 由原始切片产生。
    """

    __slots__ = ("original", "text", "_spans")

    def __init__(self, original, text, spans):
        self.original = original
        self.text = text
        self._spans = spans

    def span(self, start, end):
        if start >= end:
            raise ValueError("空区间没有原文映射")
        return self._spans[start][0], self._spans[end - 1][1]

    def quote(self, start, end):
        original_start, original_end = self.span(start, end)
        return self.original[original_start:original_end]


def normalize_text(original):
    """把原文规范化为可匹配文本，同时保留回原文的偏移映射。

    规范化仅做确定性、可逆定位的转换：
    换行统一为 \\n、NBSP / 全角空格转普通空格、全角 ASCII 转半角。
    不改动中文标点语义，不删除字符，不做同义词替换。
    """
    if not isinstance(original, str):
        raise InputError("输入必须是文本")
    chars = []
    spans = []
    index = 0
    length = len(original)
    while index < length:
        char = original[index]
        if char == "\r":
            if index + 1 < length and original[index + 1] == "\n":
                chars.append("\n")
                spans.append((index, index + 2))
                index += 2
                continue
            chars.append("\n")
            spans.append((index, index + 1))
        elif char in ("\u00a0", "\u3000"):
            chars.append(" ")
            spans.append((index, index + 1))
        elif "\uff01" <= char <= "\uff5e":
            chars.append(chr(ord(char) - 0xfee0))
            spans.append((index, index + 1))
        else:
            chars.append(char)
            spans.append((index, index + 1))
        index += 1
    return NormalizedText(original, "".join(chars), spans)


def locate_span(normalized, start, end):
    """把规范化区间转成原文位置（行 / 列 从 1 开始，按字符计数）。"""
    original = normalized.original
    original_start, original_end = normalized.span(start, end)
    line = original.count("\n", 0, original_start) + 1
    line_start = original.rfind("\n", 0, original_start) + 1
    return {
        "start": original_start,
        "end": original_end,
        "line": line,
        "column": original_start - line_start + 1,
        "quote": original[original_start:original_end],
    }


def _ascii_lower(text):
    """长度不变的小写化：只处理 ASCII 字母，保证偏移可用。"""
    return "".join(chr(ord(ch) + 32) if "A" <= ch <= "Z" else ch for ch in text)


def _line_table(text):
    """返回每行的 (内容起始, 内容结束, 下一行起始)。"""
    rows = []
    index = 0
    length = len(text)
    while index <= length:
        if index == length and (not rows or rows[-1][2] == index):
            break
        newline = text.find("\n", index)
        if newline < 0:
            rows.append((index, length, length))
            break
        rows.append((index, newline, newline + 1))
        index = newline + 1
    return rows


# ---------------------------------------------------------------------------
# 结构解析（设计 §7）
# ---------------------------------------------------------------------------
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
CLAUSE_RE = re.compile(r"^(第[0-9一二三四五六七八九十百零〇两]+[章节条])\s*(.*)$")
ITEM_RE = re.compile(
    r"^(\s*)(\(?\d+[).、]|[（(][0-9一二三四五六七八九十]+[)）]|[一二三四五六七八九十]+、)\s*(.*)$"
)


def _trim_span(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def _make_block(kind, index, level, start, end, label, normalized, id_kind=None, label_span=None):
    original_start, original_end = normalized.span(start, end)
    original = normalized.original
    line = original.count("\n", 0, original_start) + 1
    line_start = original.rfind("\n", 0, original_start) + 1
    if label_span is not None:
        label = normalized.quote(label_span[0], label_span[1])
    return {
        "block_id": "%s-%d" % (id_kind or kind, index),
        "kind": kind,
        "level": level,
        "label": label or "",
        "start": original_start,
        "end": original_end,
        "line": line,
        "column": original_start - line_start + 1,
        "text": original[original_start:original_end],
        "n_start": start,
        "n_end": end,
    }


def parse_structure(normalized):
    """解析标题 / 第X条 / 编号项 / 段落，返回带双坐标系的块列表。

    kind ∈ heading / clause / item / paragraph；block_id 前缀固定为
    heading- / clause- / item- / para-，标签文本取原文切片。
    """
    text = normalized.text
    blocks = []
    counters = {"heading": 0, "clause": 0, "item": 0, "para": 0}
    para_start = None
    para_end = None

    def flush_paragraph():
        state = [para_start, para_end]
        start, end = state[0], state[1]
        if start is None:
            return None
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        para = None
        if end > start:
            counters["para"] += 1
            para = _make_block(
                "paragraph", counters["para"], 1, start, end, None, normalized, id_kind="para"
            )
        return para

    for line_start, line_end, _next in _line_table(text):
        raw_line = text[line_start:line_end]
        stripped = raw_line.strip()
        if not stripped:
            paragraph = flush_paragraph()
            if paragraph:
                blocks.append(paragraph)
            para_start = None
            para_end = None
            continue
        heading = HEADING_RE.match(raw_line)
        if heading:
            paragraph = flush_paragraph()
            if paragraph:
                blocks.append(paragraph)
            para_start = None
            para_end = None
            counters["heading"] += 1
            label_span = _trim_span(
                text, line_start + heading.start(2), line_start + heading.end(2)
            )
            blocks.append(
                _make_block(
                    "heading", counters["heading"], len(heading.group(1)),
                    line_start, line_end, heading.group(2).strip(), normalized,
                    label_span=label_span,
                )
            )
            continue
        clause = CLAUSE_RE.match(raw_line)
        if clause:
            paragraph = flush_paragraph()
            if paragraph:
                blocks.append(paragraph)
            para_start = None
            para_end = None
            counters["clause"] += 1
            label_span = (line_start + clause.start(1), line_start + clause.end(1))
            blocks.append(
                _make_block(
                    "clause", counters["clause"], 1,
                    line_start, line_end, clause.group(1), normalized,
                    label_span=label_span,
                )
            )
            continue
        item = ITEM_RE.match(raw_line)
        if item:
            paragraph = flush_paragraph()
            if paragraph:
                blocks.append(paragraph)
            para_start = None
            para_end = None
            counters["item"] += 1
            level = 1 + (len(item.group(1)) // 4)
            label_span = (line_start + item.start(2), line_start + item.end(2))
            blocks.append(
                _make_block(
                    "item", counters["item"], min(level, 4),
                    line_start, line_end, item.group(2), normalized,
                    label_span=label_span,
                )
            )
            continue
        if para_start is None:
            para_start = line_start
        para_end = line_end
    paragraph = flush_paragraph()
    if paragraph:
        blocks.append(paragraph)
    blocks.sort(key=lambda block: block["n_start"])
    return blocks


# ---------------------------------------------------------------------------
# 规则包加载与校验（设计 §8）
# ---------------------------------------------------------------------------
def _require(condition, message):
    if not condition:
        raise RulePackError(message)


def _validate_condition(condition, where, lexicon):
    _require(isinstance(condition, dict), "%s：条件必须是 JSON 对象" % where)
    kind = condition.get("kind")
    _require(kind in CONDITION_KINDS, "%s：未知条件类型 %r（允许：%s）" % (where, kind, ", ".join(CONDITION_KINDS)))
    if kind == "regex":
        pattern = condition.get("pattern")
        _require(isinstance(pattern, str) and pattern, "%s：regex 条件缺少 pattern" % where)
        try:
            re.compile(pattern)
        except re.error as exc:
            raise RulePackError("%s：regex 无法编译（%s）" % (where, exc))
    elif kind in ("keyword", "clause_type", "section_anchor"):
        value = condition.get("value")
        _require(isinstance(value, str) and value, "%s：%s 条件缺少 value" % (where, kind))
        if kind == "clause_type":
            _require(
                value in lexicon,
                "%s：clause_type %r 未在 clause_type_lexicon 声明" % (where, value),
            )
    return condition


def _validate_assert(assert_spec, where, lexicon):
    _require(isinstance(assert_spec, dict), "%s：assert 必须是 JSON 对象" % where)
    operator = assert_spec.get("operator")
    _require(
        operator in ASSERT_OPERATORS,
        "%s：未知断言 operator %r（允许：%s）" % (where, operator, ", ".join(ASSERT_OPERATORS)),
    )
    target = assert_spec.get("target")
    _require(isinstance(target, str) and target, "%s：assert 缺少 target" % where)
    search = assert_spec.get("search")
    _require(isinstance(search, dict), "%s：assert 缺少 search（absence 必须给出搜索范围）" % where)
    _validate_condition(search, "%s.assert.search" % where, lexicon)
    if operator == "absent":
        scope = assert_spec.get("scope")
        _require(scope in SCOPE_KINDS, "%s：absence 断言必须声明 scope（%s）" % (where, ", ".join(SCOPE_KINDS)))
    elif operator in ("numeric_compare", "date_compare", "duration_compare"):
        group = search.get("group", 1)
        _require(isinstance(group, int) and group >= 1, "%s：compare 断言需要 search.group >= 1" % where)
        pattern = search.get("pattern")
        _require(isinstance(pattern, str) and re.compile(pattern).groups >= group,
                 "%s：search 正则缺少第 %s 个捕获组" % (where, group))
        compare = assert_spec.get("compare")
        _require(isinstance(compare, dict), "%s：compare 断言缺少 compare" % where)
        _require(compare.get("op") in COMPARE_OPERATORS,
                 "%s：compare.op 非法（允许：%s）" % (where, ", ".join(COMPARE_OPERATORS)))
        _require("value" in compare, "%s：compare 缺少 value" % where)
        if operator == "numeric_compare":
            _require(isinstance(compare["value"], (int, float)) and not isinstance(compare["value"], bool),
                     "%s：numeric_compare 的 value 必须是数字" % where)
        elif operator == "date_compare":
            _require(isinstance(compare["value"], str) and _parse_date(compare["value"]) is not None,
                     "%s：date_compare 的 value 必须是可解析日期（YYYY-MM-DD）" % where)
        else:
            _require(assert_spec.get("unit") in DURATION_UNITS,
                     "%s：duration_compare 必须声明 unit（%s）" % (where, ", ".join(sorted(DURATION_UNITS))))
    return assert_spec


def validate_pack(pack, source=None):
    """校验规则包；任何不合规直接抛 RulePackError，绝不降级继续审查。"""
    where = source or "规则包"
    _require(isinstance(pack, dict), "%s：根节点必须是 JSON 对象" % where)
    for field in ("schema_version", "pack_id", "framework", "pack_version", "coverage_level", "rules"):
        _require(field in pack and pack[field] not in (None, ""), "%s：缺少字段 %s" % (where, field))
    _require(pack["schema_version"] == SCHEMA_VERSION,
             "%s：schema_version 必须是 %s（当前 %r）" % (where, SCHEMA_VERSION, pack["schema_version"]))
    _require(pack["coverage_level"] in COVERAGE_LEVELS,
             "%s：coverage_level 非法（允许：%s）" % (where, ", ".join(COVERAGE_LEVELS)))
    lexicon = pack.get("clause_type_lexicon") or {}
    _require(isinstance(lexicon, dict), "%s：clause_type_lexicon 必须是对象" % where)
    rules = pack["rules"]
    _require(isinstance(rules, list) and rules, "%s：rules 必须是非空数组" % where)

    seen_rule_ids = set()
    for index, rule in enumerate(rules):
        rule_where = "%s#rules[%d]" % (where, index)
        _require(isinstance(rule, dict), "%s：规则必须是 JSON 对象" % rule_where)
        rule_id = rule.get("rule_id")
        _require(isinstance(rule_id, str) and rule_id, "%s：缺少 rule_id" % rule_where)
        rule_where = "%s(%s)" % (rule_where, rule_id)
        _require(rule_id not in seen_rule_ids, "%s：rule_id 重复" % rule_where)
        seen_rule_ids.add(rule_id)
        for field in ("title", "severity", "evidence", "rationale", "source", "remediation", "test_ids"):
            _require(field in rule and rule[field] not in (None, ""), "%s：缺少字段 %s" % (rule_where, field))
        _require(rule["severity"] in SEVERITY_ORDER,
                 "%s：severity 非法（允许：%s）" % (rule_where, ", ".join(SEVERITIES)))
        source_spec = rule["source"]
        _require(isinstance(source_spec, dict), "%s：source 必须是对象" % rule_where)
        _require(isinstance(source_spec.get("citation"), str) and source_spec["citation"],
                 "%s：source 缺少 citation" % rule_where)
        evidence = rule["evidence"]
        _require(isinstance(evidence, list) and evidence, "%s：evidence 不能为空" % rule_where)
        for kind in evidence:
            _require(kind in EVIDENCE_KINDS,
                     "%s：未知证据类型 %r（允许：%s）" % (rule_where, kind, ", ".join(EVIDENCE_KINDS)))
        test_ids = rule["test_ids"]
        _require(isinstance(test_ids, list) and test_ids, "%s：test_ids 不能为空（每条规则需正反例）" % rule_where)
        match = rule.get("match")
        _require(isinstance(match, dict), "%s：缺少 match" % rule_where)
        _require(match.get("operator") in ("any", "all"), "%s：match.operator 必须是 any / all" % rule_where)
        conditions = match.get("conditions")
        _require(isinstance(conditions, list) and conditions, "%s：match.conditions 不能为空" % rule_where)
        regex_seen = set()
        for position, condition in enumerate(conditions):
            _validate_condition(condition, "%s.match.conditions[%d]" % (rule_where, position), lexicon)
            if condition.get("kind") == "regex":
                pattern = condition["pattern"]
                _require(pattern not in regex_seen,
                         "%s：同一规则内重复 regex（%r）会导致同一证据重复计数" % (rule_where, pattern))
                regex_seen.add(pattern)
        _validate_assert(rule.get("assert"), "%s.assert" % rule_where, lexicon)
        confidence_policy = rule.get("confidence_policy") or {}
        _require(isinstance(confidence_policy, dict), "%s：confidence_policy 必须是对象" % rule_where)
        for key in ("exact_match", "absence"):
            if key in confidence_policy:
                _require(confidence_policy[key] in CONFIDENCE_LEVELS,
                         "%s：confidence_policy.%s 非法" % (rule_where, key))

    mapping_only = pack.get("mapping_only") or []
    _require(isinstance(mapping_only, list), "%s：mapping_only 必须是数组" % where)
    for index, entry in enumerate(mapping_only):
        entry_where = "%s#mapping_only[%d]" % (where, index)
        _require(isinstance(entry, dict), "%s：必须是 JSON 对象" % entry_where)
        _require(isinstance(entry.get("framework"), str) and entry["framework"],
                 "%s：缺少 framework" % entry_where)
        topics = entry.get("topics")
        _require(isinstance(topics, dict) and topics, "%s：mapping_only 必须声明 topics" % entry_where)
        for topic, rule_ids in topics.items():
            _require(isinstance(rule_ids, list) and rule_ids,
                     "%s：topic %s 必须给出引用的 rule_id" % (entry_where, topic))
            for rule_id in rule_ids:
                _require(rule_id in seen_rule_ids,
                         "%s：topic %s 引用了不存在的 rule_id %s" % (entry_where, topic, rule_id))
    return pack


def load_pack(path):
    """读取并校验单个规则包；返回带 _path / _sha256 元数据的包。"""
    if not os.path.isfile(path):
        raise RulePackError("规则包不存在：%s" % path)
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        raise RulePackError("规则包不可读（%s）：%s" % (exc, path))
    try:
        pack = json.loads(raw.decode("utf-8-sig"))
    except UnicodeDecodeError:
        raise RulePackError("规则包必须是 UTF-8 编码：%s" % path)
    except ValueError as exc:
        raise RulePackError("规则包不是合法 JSON（%s）：%s" % (exc, path))
    validate_pack(pack, source=os.path.basename(path))
    pack["_path"] = os.path.abspath(path)
    pack["_sha256"] = hashlib.sha256(raw).hexdigest()
    return pack


def available_frameworks(rules_dir):
    """列出规则目录内可用的框架 slug（文件名的 stem，例如 pipl.json -> pipl）。"""
    if not os.path.isdir(rules_dir):
        raise RulePackError("规则包目录不存在：%s" % rules_dir)
    names = []
    for name in sorted(os.listdir(rules_dir)):
        if name.endswith(".json"):
            names.append(name[:-5])
    return names


def load_rule_packs(rules_dir, frameworks=None):
    """加载规则包；frameworks 为空时加载目录内全部包。"""
    names = available_frameworks(rules_dir)
    if not names:
        raise RulePackError("规则包目录内没有 JSON 规则包：%s" % rules_dir)
    if frameworks:
        unknown = [item for item in frameworks if item not in names]
        if unknown:
            raise UsageError(
                "未知框架：%s；可用框架：%s" % (", ".join(unknown), ", ".join(names))
            )
        selected = list(frameworks)
    else:
        selected = names
    packs = []
    seen_rule_ids = {}
    for name in selected:
        pack = load_pack(os.path.join(rules_dir, name + ".json"))
        for rule in pack["rules"]:
            rule_id = rule["rule_id"]
            if rule_id in seen_rule_ids:
                raise RulePackError(
                    "rule_id 跨包重复：%s（%s 与 %s）" % (rule_id, seen_rule_ids[rule_id], name)
                )
            seen_rule_ids[rule_id] = name
        packs.append(pack)
    return packs


# ---------------------------------------------------------------------------
# 匹配原语（设计 §8.3）
# ---------------------------------------------------------------------------
class _MatchContext(object):
    __slots__ = ("normalized", "lowered", "blocks", "pack")

    def __init__(self, normalized, blocks, pack):
        self.normalized = normalized
        self.lowered = _ascii_lower(normalized.text)
        self.blocks = blocks
        self.pack = pack


def _section_for_span(blocks, n_start, n_end):
    for block in blocks:
        if block["n_start"] <= n_start and n_end <= block["n_end"]:
            return block["block_id"]
    return None


def _hit(ctx, n_start, n_end, condition_kind):
    locator = locate_span(ctx.normalized, n_start, n_end)
    hit = {
        "condition_kind": condition_kind,
        "n_start": n_start,
        "n_end": n_end,
        "section_id": _section_for_span(ctx.blocks, n_start, n_end),
    }
    hit.update(locator)
    return hit


def _literal_hits(ctx, keyword, condition_kind):
    needle = _ascii_lower(keyword)
    hits = []
    start = ctx.lowered.find(needle)
    while start >= 0:
        hits.append(_hit(ctx, start, start + len(needle), condition_kind))
        start = ctx.lowered.find(needle, start + len(needle))
    return hits


def _regex_hits(ctx, pattern, condition_kind):
    hits = []
    for match in re.finditer(pattern, ctx.normalized.text, re.IGNORECASE):
        if match.start() == match.end():
            continue
        hits.append(_hit(ctx, match.start(), match.end(), condition_kind))
    return hits


def _condition_hits(condition, ctx):
    kind = condition["kind"]
    if kind == "keyword":
        return _literal_hits(ctx, condition["value"], kind)
    if kind == "regex":
        return _regex_hits(ctx, condition["pattern"], kind)
    if kind == "clause_type":
        keywords = (ctx.pack.get("clause_type_lexicon") or {}).get(condition["value"], [])
        hits = []
        for block in ctx.blocks:
            block_text = ctx.normalized.text[block["n_start"]:block["n_end"]]
            lowered = _ascii_lower(block_text)
            for keyword in keywords:
                offset = lowered.find(_ascii_lower(keyword))
                if offset >= 0:
                    start = block["n_start"] + offset
                    hits.append(_hit(ctx, start, start + len(keyword), kind))
                    break
        return hits
    # section_anchor：锚点文本命中所在块
    hits = []
    anchor = _ascii_lower(condition["value"])
    for block in ctx.blocks:
        block_text = _ascii_lower(ctx.normalized.text[block["n_start"]:block["n_end"]])
        offset = block_text.find(anchor)
        if offset >= 0:
            start = block["n_start"] + offset
            hits.append(_hit(ctx, start, start + len(anchor), kind))
    return hits


def _dedupe_hits(hits):
    seen = set()
    unique = []
    for hit in sorted(hits, key=lambda item: (item["n_start"], item["n_end"])):
        key = (hit["n_start"], hit["n_end"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(hit)
    return unique


def match_rule(rule, normalized, blocks, pack):
    """按 match 条件求候选；返回命中区间（原文坐标）与是否命中。"""
    ctx = _MatchContext(normalized, blocks, pack)
    conditions = rule["match"]["conditions"]
    per_condition = [_condition_hits(condition, ctx) for condition in conditions]
    if rule["match"]["operator"] == "all":
        matched = all(per_condition)
    else:
        matched = any(per_condition)
    hits = _dedupe_hits([hit for hits in per_condition for hit in hits])
    return {"matched": bool(matched and hits), "hits": hits}


# ---------------------------------------------------------------------------
# 断言求值（设计 §8.2 / §9 / §10）
# ---------------------------------------------------------------------------
_CHINESE_DIGITS = {
    "零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
}
_DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y年%m月%d日")


def _parse_number(text):
    token = text.strip()
    if not token:
        return None
    try:
        return float(token)
    except ValueError:
        pass
    if all(char in _CHINESE_DIGITS for char in token):
        return float("".join(str(_CHINESE_DIGITS[char]) for char in token))
    if "十" in token:
        parts = token.split("十")
        if len(parts) == 2 and all(part == "" or all(c in _CHINESE_DIGITS for c in part) for part in parts):
            tens = 1 if parts[0] == "" else _CHINESE_DIGITS.get(parts[0], 0)
            ones = 0 if parts[1] == "" else _CHINESE_DIGITS.get(parts[1], 0)
            return float(tens * 10 + ones)
    return None


def _parse_date(text):
    token = text.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(token, fmt).date()
        except ValueError:
            continue
    return None


def _compare(left, right, operator):
    if operator == "gte":
        return left >= right
    if operator == "lte":
        return left <= right
    if operator == "gt":
        return left > right
    if operator == "lt":
        return left < right
    if operator == "eq":
        return left == right
    return left != right


def _extract_group_span(pattern, text, n_start, n_end, group):
    for match in re.finditer(pattern, text, re.IGNORECASE):
        if match.span() == (n_start, n_end):
            span = match.span(group)
            if span[0] < 0:
                return None
            return span
    return None


def _scope_evidence(ctx, scope, hits):
    def with_range(locator, n_start, n_end):
        locator.pop("quote", None)
        end = locate_span(ctx.normalized, n_end - 1, n_end) if n_end > n_start else locator
        locator["end_line"] = end["line"]
        locator["end_column"] = end["column"]
        return locator

    if scope == "section" and hits:
        section_id = hits[0]["section_id"]
        for block in ctx.blocks:
            if block["block_id"] == section_id:
                locator = locate_span(ctx.normalized, block["n_start"], block["n_end"])
                locator = with_range(locator, block["n_start"], block["n_end"])
                locator["kind"] = "section_scope"
                locator["section_id"] = block["block_id"]
                locator["scope_label"] = "所在段：%s" % block["block_id"]
                return locator
    length = len(ctx.normalized.text)
    locator = locate_span(ctx.normalized, 0, length)
    locator = with_range(locator, 0, length)
    locator["kind"] = "document_scope"
    locator["section_id"] = None
    locator["scope_label"] = "全文范围"
    return locator


def _matched_evidence(hits, limit=MAX_EVIDENCE_PER_FINDING):
    evidence = []
    for hit in hits[:limit]:
        entry = {
            "kind": "matched_span",
            "quote": hit["quote"],
            "start": hit["start"],
            "end": hit["end"],
            "line": hit["line"],
            "column": hit["column"],
            "section_id": hit["section_id"],
        }
        evidence.append(entry)
    return evidence


def _confidence(rule, key, default):
    policy = rule.get("confidence_policy") or {}
    return policy.get(key, default)


def _framework_mapping(rule, pack):
    mapping = [pack["framework"]]
    for entry in pack.get("mapping_only") or []:
        for rule_ids in (entry.get("topics") or {}).values():
            if rule["rule_id"] in rule_ids:
                label = "%s:mapping_only" % entry["framework"]
                if label not in mapping:
                    mapping.append(label)
                break
    return mapping


def _evaluate_assert(rule, ctx, hits):
    """返回 {"outcome": finding|none, "confidence":..., "evidence":[...], "review":{...}}。"""
    assert_spec = rule["assert"]
    operator = assert_spec["operator"]
    search = assert_spec["search"]
    search_hits = _dedupe_hits(_condition_hits(search, ctx))
    if search.get("kind") == "regex" and search.get("group"):
        search_hits = [
            hit for hit in search_hits
            if _extract_group_span(
                search["pattern"], ctx.normalized.text, hit["n_start"], hit["n_end"], search["group"]
            ) is not None
        ]

    if operator == "absent":
        if search_hits:
            return {"outcome": "none"}
        evidence = _matched_evidence(hits)
        evidence.append(_scope_evidence(ctx, assert_spec.get("scope", "document"), hits))
        return {
            "outcome": "finding",
            "confidence": _confidence(rule, "absence", "medium"),
            "evidence": evidence,
            "evidence_total": len(hits) + 1,
        }

    if operator == "present":
        if not search_hits:
            return {"outcome": "none"}
        return {
            "outcome": "finding",
            "confidence": _confidence(rule, "exact_match", "high"),
            "evidence": _matched_evidence(search_hits),
            "evidence_total": len(search_hits),
        }

    if not search_hits:
        return {
            "outcome": "review",
            "review": {
                "kind": "unverifiable",
                "rule_id": rule["rule_id"],
                "reason": "断言目标无法在原文中定位，未输出数值结论，请人工核验。",
            },
        }

    hit = search_hits[0]
    group_span = _extract_group_span(
        search["pattern"], ctx.normalized.text, hit["n_start"], hit["n_end"], search.get("group", 1)
    )
    if group_span is None:
        return {
            "outcome": "review",
            "review": {
                "kind": "unverifiable",
                "rule_id": rule["rule_id"],
                "reason": "断言目标无法从原文切片中解析，未输出结论，请人工核验。",
            },
        }
    value_text = ctx.normalized.text[group_span[0]:group_span[1]]
    compare = assert_spec["compare"]

    if operator == "numeric_compare":
        value = _parse_number(value_text)
        if value is None:
            return _unverifiable(rule, "原文数值无法解析（%s），未自动换算或补值。" % value_text.strip())
        left, right = value, float(compare["value"])
    elif operator == "date_compare":
        value = _parse_date(value_text)
        if value is None:
            return _unverifiable(rule, "原文日期无法解析（%s），未输出结论。" % value_text.strip())
        left, right = value, _parse_date(compare["value"])
    else:
        unit = assert_spec["unit"]
        found_units = [
            name for name, tokens in DURATION_UNITS.items()
            if any(token in hit["quote"] for token in tokens)
        ]
        if found_units != [unit]:
            return _unverifiable(
                rule,
                "时长单位与规则声明不一致（原文：%s；规则：%s），不做跨单位换算。"
                % (", ".join(found_units) or "未识别", unit),
            )
        value = _parse_number(value_text)
        if value is None:
            return _unverifiable(rule, "原文时长数值无法解析（%s）。" % value_text.strip())
        left, right = value, float(compare["value"])

    if not _compare(left, right, compare["op"]):
        return {"outcome": "none"}
    return {
        "outcome": "finding",
        "confidence": _confidence(rule, "exact_match", "high"),
        "evidence": _matched_evidence([hit]),
        "evidence_total": 1,
    }


def _unverifiable(rule, reason):
    return {
        "outcome": "review",
        "review": {"kind": "unverifiable", "rule_id": rule["rule_id"], "reason": reason},
    }


# ---------------------------------------------------------------------------
# 审查主流程（设计 §4 / §7 / §11.2）
# ---------------------------------------------------------------------------
def _severity_rank(severity):
    return SEVERITY_ORDER.get(severity, 0)


def _input_summary(text, input_meta):
    meta = dict(input_meta or {})
    payload = text.encode("utf-8")
    summary = {
        "kind": meta.get("kind", "memory"),
        "path": meta.get("path"),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "lines": (text.count("\n") + 1) if text else 0,
    }
    return summary


def _framework_coverage(packs):
    coverage = []
    seen = set()
    for pack in packs:
        coverage.append({
            "framework": pack["framework"],
            "coverage_level": pack["coverage_level"],
            "status": "reviewed" if pack["coverage_level"] == "baseline_review" else "mapping_only",
            "pack_id": pack["pack_id"],
            "pack_version": pack["pack_version"],
            "rule_count": len(pack["rules"]),
            "note": "" if pack["coverage_level"] == "baseline_review" else MAPPING_ONLY_NOTE,
        })
        seen.add(pack["framework"])
        for entry in pack.get("mapping_only") or []:
            framework = entry["framework"]
            topics = sorted((entry.get("topics") or {}).keys())
            coverage.append({
                "framework": framework,
                "coverage_level": "mapping_only",
                "status": "mapping_only",
                "pack_id": pack["pack_id"],
                "pack_version": pack["pack_version"],
                "rule_count": sum(len(ids) for ids in (entry.get("topics") or {}).values()),
                "topics": topics,
                "note": MAPPING_ONLY_NOTE,
            })
            seen.add(framework)
    return coverage


def _unique_in_order(items):
    """按首次出现顺序去重，用于覆盖摘要的框架清单。"""
    seen = set()
    unique = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return unique


def review_text(text, packs, min_severity="low", include_safe=False, input_meta=None, generated_at=None):
    """对文本执行确定性审查，返回稳定 JSON 契约结果。"""
    if min_severity not in SEVERITY_ORDER:
        raise UsageError("未知严重度阈值：%s" % min_severity)
    normalized = normalize_text(text)
    blocks = parse_structure(normalized)
    checked = []
    raw_findings = []
    review_items = []

    for pack in packs:
        ctx = _MatchContext(normalized, blocks, pack)
        for rule in pack["rules"]:
            matched = match_rule(rule, normalized, blocks, pack)
            if not matched["matched"]:
                checked.append({
                    "rule_id": rule["rule_id"],
                    "pack_id": pack["pack_id"],
                    "status": "no_match",
                })
                continue
            outcome = _evaluate_assert(rule, ctx, matched["hits"])
            if outcome["outcome"] == "finding":
                raw_findings.append({
                    "rule_id": rule["rule_id"],
                    "title": rule["title"],
                    "severity": rule["severity"],
                    "confidence": outcome["confidence"],
                    "framework_mapping": _framework_mapping(rule, pack),
                    "clause_types": list(rule.get("clause_types") or []),
                    "evidence": outcome["evidence"],
                    "evidence_total": outcome.get("evidence_total", len(outcome["evidence"])),
                    "rationale": rule["rationale"],
                    "remediation": rule["remediation"],
                    "source": rule["source"],
                })
                checked.append({
                    "rule_id": rule["rule_id"],
                    "pack_id": pack["pack_id"],
                    "status": "matched",
                })
            elif outcome["outcome"] == "review":
                item = dict(outcome["review"])
                item["pack_id"] = pack["pack_id"]
                review_items.append(item)
                checked.append({
                    "rule_id": rule["rule_id"],
                    "pack_id": pack["pack_id"],
                    "status": "matched_no_finding",
                })
            else:
                checked.append({
                    "rule_id": rule["rule_id"],
                    "pack_id": pack["pack_id"],
                    "status": "matched_no_finding",
                })

    raw_findings.sort(key=lambda item: (
        -_severity_rank(item["severity"]),
        item["rule_id"],
        item["evidence"][0]["start"] if item["evidence"] else 0,
    ))
    findings = []
    for index, item in enumerate(raw_findings, start=1):
        finding = {"finding_id": "F-%04d" % index}
        finding.update(item)
        total = finding["evidence_total"]
        finding["evidence_total"] = total
        if total > MAX_EVIDENCE_PER_FINDING:
            finding["evidence_note"] = "仅显示前 %d 条证据，共 %d 条。" % (MAX_EVIDENCE_PER_FINDING, total)
        findings.append(finding)

    for finding in findings:
        if finding["confidence"] == "low":
            review_items.insert(0, {
                "kind": "low_confidence",
                "rule_id": finding["rule_id"],
                "pack_id": None,
                "finding_id": finding["finding_id"],
                "reason": "低置信结论，必须人工核验后才能采信。",
            })

    by_severity = {severity: 0 for severity in SEVERITIES}
    by_confidence = {level: 0 for level in CONFIDENCE_LEVELS}
    for finding in findings:
        by_severity[finding["severity"]] += 1
        by_confidence[finding["confidence"]] += 1

    emitted = [finding for finding in findings if _severity_rank(finding["severity"]) >= _severity_rank(min_severity)]
    summary = {
        "findings_total": len(emitted),
        "findings_total_all": len(findings),
        "by_severity": by_severity,
        "by_confidence": by_confidence,
        "rules_checked": len(checked),
        "rules_matched": len([item for item in checked if item["status"] != "no_match"]),
        "review_items": len(review_items),
    }
    if include_safe:
        summary["checked_rules"] = checked

    packs_meta = []
    for pack in packs:
        packs_meta.append({
            "pack_id": pack["pack_id"],
            "framework": pack["framework"],
            "pack_version": pack["pack_version"],
            "coverage_level": pack["coverage_level"],
            "sha256": pack.get("_sha256", ""),
            "rule_count": len(pack["rules"]),
        })

    stamp = generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL,
        "tool_version": VERSION,
        "generated_at": stamp,
        "input": _input_summary(text, input_meta),
        "rule_packs": packs_meta,
        "framework_coverage": _framework_coverage(packs),
        "summary": summary,
        "findings": emitted,
        "review_items": review_items,
        "disclaimer": DISCLAIMER,
    }


# ---------------------------------------------------------------------------
# 报告渲染（设计 §11）
# ---------------------------------------------------------------------------
def _finding_lines(finding):
    lines = [
        "### %s %s %s" % (finding["finding_id"], finding["rule_id"], finding["title"]),
        "",
        "- 严重度：%s ｜ 置信度：%s" % (finding["severity"], finding["confidence"]),
        "- 框架映射：%s" % "、".join(finding["framework_mapping"]),
    ]
    if finding.get("clause_types"):
        lines.append("- 条款类型：%s" % "、".join(finding["clause_types"]))
    lines.append("- 证据：")
    for evidence in finding["evidence"]:
        if evidence["kind"] == "matched_span":
            lines.append(
                "  - [matched_span] 第 %s 行 第 %s 列 `%s`"
                % (evidence["line"], evidence["column"], evidence["quote"].replace("\n", "\\n"))
            )
        else:
            lines.append(
                "  - [%s] %s（第 %s 行 第 %s 列 至 第 %s 行 第 %s 列）"
                % (
                    evidence["kind"], evidence.get("scope_label", ""),
                    evidence["line"], evidence["column"],
                    evidence.get("end_line", evidence["line"]),
                    evidence.get("end_column", evidence["column"]),
                )
            )
    if finding.get("evidence_note"):
        lines.append("- 证据说明：%s" % finding["evidence_note"])
    lines.extend([
        "- 规则说明：%s" % finding["rationale"],
        "- 建议动作：%s" % finding["remediation"],
        "- 规则来源：%s" % finding["source"].get("citation", ""),
        "",
    ])
    return lines


def render_markdown(result):
    """渲染人类可读报告，节顺序固定（设计 §11.1）。"""
    lines = ["# 合规条款审查报告", "", "生成时间：%s" % result["generated_at"], ""]

    lines.append("## 1. 输入摘要")
    lines.append("")
    input_info = result["input"]
    lines.append("- 来源：%s" % (input_info.get("path") or input_info.get("kind")))
    lines.append("- 大小：%s 字节 ｜ 行数：%s" % (input_info["bytes"], input_info["lines"]))
    lines.append("- SHA-256：%s" % input_info["sha256"])
    for pack in result["rule_packs"]:
        lines.append(
            "- 规则包：%s %s（%s，%s 条规则）"
            % (pack["pack_id"], pack["pack_version"], pack["coverage_level"], pack["rule_count"])
        )
    lines.append("")

    lines.append("## 2. 框架覆盖摘要")
    lines.append("")
    lines.append("| 规则包 | 框架 | 覆盖级别 | 状态 | 规则数 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for entry in result["framework_coverage"]:
        lines.append(
            "| %s | %s | %s | %s | %s |"
            % (
                entry.get("pack_id", "-"),
                entry["framework"],
                entry["coverage_level"],
                entry["status"],
                entry["rule_count"],
            )
        )
    lines.append("")
    mapping_only = _unique_in_order(
        entry["framework"] for entry in result["framework_coverage"]
        if entry["coverage_level"] == "mapping_only"
    )
    if mapping_only:
        lines.append(
            "说明：%s 为 mapping_only（%s）。"
            % ("、".join(mapping_only), MAPPING_ONLY_NOTE.strip("。"))
        )
    lines.append("")

    lines.append("## 3. 风险汇总")
    lines.append("")
    summary = result["summary"]
    if result["findings"]:
        lines.append("- 本次输出 %s 条发现（全部 %s 条）" % (summary["findings_total"], summary["findings_total_all"]))
        for severity in reversed(SEVERITIES):
            if summary["by_severity"].get(severity):
                lines.append("- %s：%s 条" % (severity, summary["by_severity"][severity]))
    else:
        lines.append("- 本报告未发现达到输出阈值的风险项。")
    lines.append("- 已检查规则：%s 条 ｜ 命中规则：%s 条" % (summary["rules_checked"], summary["rules_matched"]))
    lines.append("")

    lines.append("## 4. 逐条发现")
    lines.append("")
    if result["findings"]:
        for finding in result["findings"]:
            lines.extend(_finding_lines(finding))
    else:
        lines.append("（无达到输出阈值的发现。）")
        lines.append("")

    lines.append("## 5. 未覆盖范围")
    lines.append("")
    if mapping_only:
        lines.append("- mapping_only 框架（仅主题映射）：%s" % "、".join(mapping_only))
    lines.append("- v0.1 不直接解析 PDF / docx，请先用文档适配器转成文本或 Markdown。")
    checked_rules = summary.get("checked_rules") or []
    unmatched = [item["rule_id"] for item in checked_rules if item["status"] == "no_match"]
    if checked_rules:
        lines.append("- 本次已检查未命中的规则：%s" % ("、".join(unmatched) if unmatched else "无"))
    lines.append("")

    lines.append("## 6. 人工复核清单")
    lines.append("")
    if result["review_items"]:
        for item in result["review_items"]:
            lines.append(
                "- [%s] %s：%s"
                % (item["kind"], item.get("rule_id") or item.get("finding_id") or "-", item["reason"])
            )
    else:
        lines.append("（无需人工复核项。）")
    lines.append("")

    lines.append("## 7. 免责声明")
    lines.append("")
    lines.append(result["disclaimer"])
    lines.append("")
    return "\n".join(lines)


def render_json(result):
    return json.dumps(result, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI（设计 §6）
# ---------------------------------------------------------------------------
class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def _read_input(args):
    if args.stdin:
        text = sys.stdin.read()
        meta = {"kind": "stdin", "path": None}
    else:
        path = args.input
        if not os.path.exists(path):
            raise InputError("输入文件不存在：%s" % path)
        if os.path.isdir(path):
            raise InputError("输入路径不是文件：%s" % path)
        suffix = os.path.splitext(path)[1].lower()
        if suffix in UNSUPPORTED_SUFFIXES:
            raise InputError(
                "v0.1 不支持直接读取 %s；请先用文档适配器转成文本或 Markdown 再审查。" % suffix
            )
        size = os.path.getsize(path)
        if size > MAX_INPUT_BYTES:
            raise InputError(
                "输入超过 2 MiB 上限（%s 字节）；请分批处理或先精简文本。" % size
            )
        try:
            with open(path, "rb") as handle:
                raw = handle.read()
        except OSError as exc:
            raise InputError("输入文件不可读：%s" % exc)
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise InputError("输入必须是 UTF-8 文本；请先转码（例如 GB18030 → UTF-8）。")
        meta = {"kind": "file", "path": os.path.abspath(path)}
    if not text.strip():
        raise InputError("输入内容为空，未执行审查。")
    return text, meta


def _resolve_output_path(out_path, rules_dir, input_path):
    out_abs = os.path.realpath(os.path.abspath(out_path))
    rules_abs = os.path.realpath(os.path.abspath(rules_dir))
    if out_abs == rules_abs or out_abs.startswith(rules_abs + os.sep):
        raise InputError("输出路径不得位于规则包目录内：%s" % out_path)
    if input_path:
        input_abs = os.path.realpath(os.path.abspath(input_path))
        if out_abs == input_abs:
            raise InputError("输出路径不得与输入文件相同，避免覆盖原文。")
    parent = os.path.dirname(out_abs)
    if parent and not os.path.isdir(parent):
        raise InputError("输出目录不存在：%s" % parent)
    return out_abs


def _write_output(path, content):
    temporary = path + ".tmp-yotta-compliance"
    try:
        with open(temporary, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(temporary, path)
    except OSError as exc:
        try:
            if os.path.exists(temporary):
                os.remove(temporary)
        except OSError:
            pass
        raise InputError("报告写入失败：%s" % exc)


def _gate_hit(summary, gate):
    if gate == "off":
        return False
    threshold = SEVERITY_ORDER[gate]
    for severity, count in summary["by_severity"].items():
        if count and SEVERITY_ORDER[severity] >= threshold:
            return True
    return False


def _cmd_review(args):
    if args.input and args.stdin:
        raise UsageError("--input 与 --stdin 互斥，只能选择一种输入方式。")
    if not args.input and not args.stdin:
        raise UsageError("必须提供 --input <文件> 或 --stdin。")
    if args.locale != "zh-CN":
        raise UsageError("v0.1 仅支持 --locale zh-CN。")
    if args.gate not in (("off",) + SEVERITIES):
        raise UsageError("--gate 非法（允许：off, %s）" % ", ".join(SEVERITIES))
    if args.min_severity not in SEVERITY_ORDER:
        raise UsageError("--min-severity 非法（允许：%s）" % ", ".join(SEVERITIES))
    frameworks = None
    if args.frameworks:
        frameworks = [item.strip() for item in args.frameworks.split(",") if item.strip()]
    packs = load_rule_packs(args.rules_dir, frameworks)
    text, meta = _read_input(args)
    result = review_text(
        text, packs,
        min_severity=args.min_severity,
        include_safe=args.include_safe,
        input_meta=meta,
    )
    if args.format == "json":
        rendered = render_json(result)
    else:
        rendered = render_markdown(result)
    if args.out:
        target = _resolve_output_path(args.out, args.rules_dir, meta.get("path"))
        _write_output(target, rendered if rendered.endswith("\n") else rendered + "\n")
        sys.stderr.write("已写入：%s\n" % target)
    else:
        sys.stdout.write(rendered if rendered.endswith("\n") else rendered + "\n")
    return 1 if _gate_hit(result["summary"], args.gate) else 0


def _cmd_rules_list(args):
    frameworks = None
    if args.framework:
        frameworks = [item.strip() for item in args.framework.split(",") if item.strip()]
    packs = load_rule_packs(args.rules_dir, frameworks)
    for pack in packs:
        sys.stdout.write("# %s（%s，%s）\n" % (pack["pack_id"], pack["framework"], pack["coverage_level"]))
        for rule in pack["rules"]:
            sys.stdout.write("- %s  %s  [%s]\n" % (rule["rule_id"], rule["title"], rule["severity"]))
    return 0


def _cmd_rules_show(args):
    packs = load_rule_packs(args.rules_dir)
    for pack in packs:
        for rule in pack["rules"]:
            if rule["rule_id"] != args.rule_id:
                continue
            sys.stdout.write("%s  %s\n" % (rule["rule_id"], rule["title"]))
            sys.stdout.write("严重度：%s\n" % rule["severity"])
            sys.stdout.write("规则说明：%s\n" % rule["rationale"])
            sys.stdout.write("建议动作：%s\n" % rule["remediation"])
            sys.stdout.write("规则来源：%s\n" % rule["source"].get("citation", ""))
            if rule["source"].get("url"):
                sys.stdout.write("来源链接：%s\n" % rule["source"]["url"])
            sys.stdout.write("测试用例：%s\n" % "、".join(rule["test_ids"]))
            return 0
    raise UsageError("未找到规则：%s" % args.rule_id)


def _cmd_rules_validate(args):
    pack = load_pack(args.pack)
    sys.stdout.write(
        "规则包校验通过：%s（%s，%s 条规则，sha256=%s）\n"
        % (pack["pack_id"], pack["framework"], len(pack["rules"]), pack["_sha256"][:12])
    )
    return 0


def build_parser():
    parser = _ArgumentParser(prog=TOOL, description="%s（%s）：确定性合规条款审查内核" % (TOOL_CN, TOOL))
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="command")

    review = subparsers.add_parser("review", help="审查文本 / Markdown")
    review.add_argument("--input", help="输入文件（UTF-8 .txt / .md）")
    review.add_argument("--stdin", action="store_true", help="从标准输入读取")
    review.add_argument("--frameworks", help="框架列表，逗号分隔（默认全部已装载规则包）")
    review.add_argument("--rules-dir", default=DEFAULT_RULES_DIR, help="规则包目录")
    review.add_argument("--format", choices=("md", "json"), default="md")
    review.add_argument("--out", help="报告输出路径（默认写 stdout）")
    review.add_argument("--gate", default="off", help="CI 闸门阈值：off/low/medium/high/critical")
    review.add_argument("--min-severity", default="low", help="输出最低严重度（默认 low）")
    review.add_argument("--include-safe", action="store_true", help="输出已检查未命中的规则清单")
    review.add_argument("--locale", default="zh-CN", help="报告语言（v0.1 仅 zh-CN）")
    review.set_defaults(handler=_cmd_review)

    rules = subparsers.add_parser("rules", help="规则包操作")
    rules_sub = rules.add_subparsers(dest="rules_command")

    rules_list = rules_sub.add_parser("list", help="列出规则")
    rules_list.add_argument("--rules-dir", default=DEFAULT_RULES_DIR)
    rules_list.add_argument("--framework", help="按框架过滤（逗号分隔）")
    rules_list.set_defaults(handler=_cmd_rules_list)

    rules_show = rules_sub.add_parser("show", help="查看单条规则")
    rules_show.add_argument("rule_id")
    rules_show.add_argument("--rules-dir", default=DEFAULT_RULES_DIR)
    rules_show.set_defaults(handler=_cmd_rules_show)

    rules_validate = rules_sub.add_parser("validate", help="校验规则包")
    rules_validate.add_argument("--pack", required=True, help="规则包 JSON 路径")
    rules_validate.set_defaults(handler=_cmd_rules_validate)

    return parser


def main(argv=None):
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        handler = getattr(args, "handler", None)
        if handler is None:
            raise UsageError("请指定子命令：review / rules")
        return handler(args)
    except ComplianceError as exc:
        sys.stderr.write("错误：%s\n" % exc)
        return exc.exit_code


if __name__ == "__main__":
    sys.exit(main())
