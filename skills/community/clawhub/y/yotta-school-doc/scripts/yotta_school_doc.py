#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""元公 yotta-school-doc —— 本地、确定性的学校公文可信起草与校验引擎（零依赖，Python 3.8+）。

边界：只读本地文种规则包、事实 JSON 与文稿；核心路径不联网、不调用模型；
不编造姓名、日期、数字、文号或事实；结论只作文书辅助与风险提示。

退出码：0 正常 / 1 触发闸门 / 2 输入错误 / 3 文种或规则包错误 / 4 运行时错误。
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.5"
SCHEMA_VERSION = "1.0"
TOOL_NAME = "yotta-school-doc"
PLACEHOLDER = "〔待补〕"

DISCLAIMER = (
    "本文件由元公（yotta-school-doc）基于本地文种规则包、事实 JSON 与文稿的确定性计算生成，"
    "仅作文书辅助与风险提示；不构成法律、合规、督导或意识形态审查结论，最终签发责任在学校。"
)

VALID_FIELDS = {
    "title", "issuer", "published_date", "audience", "action_deadline", "contact",
    "response_deadline", "decision_request", "reason", "summary", "next_steps",
    "meeting_date", "attendees", "decisions", "action_items", "goal", "steps",
    "owner", "timeline", "highlights", "body_points", "attachments",
}

BAD_DATE_RE = re.compile(r"(?<!\d)\d{4}[./]\d{1,2}[./]\d{2}(?!\d)")
ISO_DATE_RE = re.compile(r"(?<!\d)(\d{4})-(\d{1,2})-(\d{1,2})(?!\d)")
CN_DATE_RE = re.compile(r"(?<!\d)(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日")
PRIVACY_PATTERNS = (
    ("身份证号", re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")),
    ("手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("邮箱", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("个人地址或身份字段", re.compile(r"(家庭住址|家庭地址|现住址|身份证号|手机号)\s*[:：]\s*\S+")),
)
PLACEHOLDERS = ("〔待补〕", "【待补】", "TO" + "DO", "T" + "BD", "待定", "XXX")
OVERCLAIM_TERMS = ("确保", "全部", "彻底", "100%", "绝不")
DEFAULT_SENSITIVE_TERMS = ("处分", "开除", "劝退", "罚款", "追责", "承诺", "保证")


def _sections(*items):
    return list(items)


DEFAULT_TYPES = {
    "schema_version": SCHEMA_VERSION,
    "pack_version": "2026.09.1",
    "types": [
        {
            "id": "notice",
            "name": "通知",
            "title_keywords": ["通知"],
            "required_fields": ["title", "issuer", "published_date", "audience",
                                "action_deadline", "contact"],
            "required_sections": _sections(
                {"id": "title", "name": "标题", "keywords": ["通知"]},
                {"id": "audience", "name": "受文对象", "keywords": ["各", "全体", "各位", "全校"]},
                {"id": "body", "name": "正文", "min_lines": 4},
                {"id": "issuer", "name": "发文单位",
                 "keywords": ["学校", "中学", "小学", "教育局", "教务处"]},
                {"id": "date", "name": "成文日期", "date_required": True},
            ),
            "sensitive_terms": list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": "public",
        },
        {
            "id": "parents_letter",
            "name": "告家长书",
            "title_keywords": ["告家长书", "家长信"],
            "required_fields": ["title", "issuer", "published_date", "audience",
                                "response_deadline", "contact", "attachments"],
            "required_sections": _sections(
                {"id": "title", "name": "标题", "keywords": ["告家长书", "家长"]},
                {"id": "audience", "name": "受文对象", "keywords": ["家长", "各位", "全体"]},
                {"id": "body", "name": "正文", "min_lines": 4},
                {"id": "issuer", "name": "发文单位",
                 "keywords": ["学校", "中学", "小学", "教育局"]},
                {"id": "date", "name": "成文日期", "date_required": True},
            ),
            "sensitive_terms": list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": "public",
        },
        {
            "id": "request",
            "name": "请示",
            "title_keywords": ["请示"],
            "required_fields": ["title", "issuer", "published_date", "audience",
                                "decision_request", "reason", "contact"],
            "required_sections": _sections(
                {"id": "title", "name": "标题", "keywords": ["请示"]},
                {"id": "audience", "name": "主送对象", "keywords": ["教育局", "学校", "委员会"]},
                {"id": "body", "name": "请示事项", "keywords": ["请示", "请予", "批准", "恳请"]},
                {"id": "issuer", "name": "发文单位",
                 "keywords": ["学校", "中学", "小学", "教务处"]},
                {"id": "date", "name": "成文日期", "date_required": True},
            ),
            "sensitive_terms": list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": "internal",
        },
        {
            "id": "report",
            "name": "报告",
            "title_keywords": ["报告"],
            "required_fields": ["title", "issuer", "published_date", "audience",
                                "summary", "next_steps", "contact"],
            "required_sections": _sections(
                {"id": "title", "name": "标题", "keywords": ["报告"]},
                {"id": "audience", "name": "主送对象", "keywords": ["教育局", "学校", "委员会"]},
                {"id": "body", "name": "正文", "keywords": ["工作情况", "主要工作", "现将"]},
                {"id": "issuer", "name": "发文单位",
                 "keywords": ["学校", "中学", "小学", "教务处"]},
                {"id": "date", "name": "成文日期", "date_required": True},
            ),
            "sensitive_terms": list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": "internal",
        },
        {
            "id": "summary",
            "name": "工作总结",
            "title_keywords": ["工作总结", "总结"],
            "required_fields": ["title", "issuer", "published_date", "summary",
                                "next_steps", "contact"],
            "required_sections": _sections(
                {"id": "title", "name": "标题", "keywords": ["总结"]},
                {"id": "body", "name": "正文", "keywords": ["主要工作", "工作情况", "下一步"]},
                {"id": "issuer", "name": "发文单位",
                 "keywords": ["学校", "中学", "小学", "教务处"]},
                {"id": "date", "name": "成文日期", "date_required": True},
            ),
            "sensitive_terms": list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": "internal",
        },
        {
            "id": "minutes",
            "name": "会议纪要",
            "title_keywords": ["会议纪要", "纪要"],
            "required_fields": ["title", "issuer", "meeting_date", "attendees",
                                "decisions", "action_items"],
            "required_sections": _sections(
                {"id": "title", "name": "标题", "keywords": ["会议纪要", "纪要"]},
                {"id": "attendees", "name": "参会人员",
                 "keywords": ["参会", "出席", "参加人员", "列席", "与会"]},
                {"id": "decisions", "name": "议定事项", "keywords": ["议定", "决定", "研究", "通过"]},
                {"id": "action_items", "name": "待办事项",
                 "keywords": ["责任人", "负责人", "完成时间", "分工"]},
                {"id": "date", "name": "会议日期", "date_required": True},
            ),
            "sensitive_terms": list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": "internal",
        },
        {
            "id": "plan",
            "name": "工作方案",
            "title_keywords": ["工作方案", "实施方案", "方案"],
            "required_fields": ["title", "issuer", "published_date", "goal", "steps",
                                "owner", "timeline", "contact"],
            "required_sections": _sections(
                {"id": "title", "name": "标题", "keywords": ["方案"]},
                {"id": "body", "name": "目标与步骤", "keywords": ["目标", "措施", "步骤", "安排"]},
                {"id": "issuer", "name": "发文单位",
                 "keywords": ["学校", "中学", "小学", "教务处"]},
                {"id": "date", "name": "成文日期", "date_required": True},
            ),
            "sensitive_terms": list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": "internal",
        },
        {
            "id": "briefing",
            "name": "简报",
            "title_keywords": ["简报"],
            "required_fields": ["title", "issuer", "published_date", "summary",
                                "highlights", "contact"],
            "required_sections": _sections(
                {"id": "title", "name": "标题", "keywords": ["简报"]},
                {"id": "body", "name": "正文", "keywords": ["情况", "工作", "亮点", "重点"]},
                {"id": "issuer", "name": "发文单位",
                 "keywords": ["学校", "中学", "小学", "教务处"]},
                {"id": "date", "name": "成文日期", "date_required": True},
            ),
            "sensitive_terms": list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": "public",
        },
    ],
}

FIELD_PROBES = {
    "audience": ("各", "全体", "各位", "全校", "家长"),
    "contact": ("联系", "咨询", "电话", "邮箱"),
    "action_deadline": ("截止", "前完成", "前将", "办理", "报名", "报送", "反馈"),
    "response_deadline": ("反馈", "回复", "截止", "前将", "前交"),
    "decision_request": ("请示", "请予", "批准", "恳请", "报请"),
    "reason": ("原因", "理由", "由于", "鉴于", "为做好"),
    "summary": ("总结", "主要工作", "基本情况", "现将", "工作情况"),
    "next_steps": ("下一步", "下阶段", "后续", "计划", "安排"),
    "attendees": ("参会", "出席", "参加人员", "列席", "与会"),
    "decisions": ("议定", "决定", "研究", "通过"),
    "action_items": ("待办", "责任人", "负责人", "完成时间", "分工"),
    "goal": ("目标", "目的", "要求", "旨在"),
    "steps": ("步骤", "措施", "安排", "一、", "二、"),
    "owner": ("责任人", "负责人", "牵头"),
    "timeline": ("时间", "进度", "期限", "节点"),
    "highlights": ("亮点", "重点", "主要"),
}


class SchoolDocError(Exception):
    exit_code = 4

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InputError(SchoolDocError):
    exit_code = 2


class ConfigError(SchoolDocError):
    exit_code = 3


def normalize_text(text):
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    return text.replace("\ufeff", "").replace("\r\n", "\n").replace("\r", "\n")


def normalize_date(value):
    if not isinstance(value, str):
        return None
    text = value.strip()
    match = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if not match:
        match = re.fullmatch(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", text)
    if not match:
        return None
    try:
        parsed = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None
    return parsed.strftime("%Y-%m-%d")


def extract_dates(text):
    text = normalize_text(text)
    values = []
    for match in ISO_DATE_RE.finditer(text):
        value = normalize_date(match.group(0))
        if value and value not in values:
            values.append(value)
    for match in CN_DATE_RE.finditer(text):
        value = normalize_date(match.group(0))
        if value and value not in values:
            values.append(value)
    return values


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


def _string_value(value, where, field, required=False):
    if value is None:
        if required:
            raise ConfigError("%s：%s 不能为空" % (where, field))
        return ""
    if not isinstance(value, str):
        raise ConfigError("%s：%s 必须是字符串" % (where, field))
    value = value.strip()
    if required and not value:
        raise ConfigError("%s：%s 不能为空" % (where, field))
    return value


def _string_list(value, where, field, required=False):
    if value is None:
        if required:
            raise ConfigError("%s：%s 不能为空" % (where, field))
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ConfigError("%s：%s 必须是字符串数组" % (where, field))
    if required and not value:
        raise ConfigError("%s：%s 不能为空数组" % (where, field))
    return [item.strip() for item in value]


def load_types(payload, where="types"):
    data = json.loads(json.dumps(DEFAULT_TYPES, ensure_ascii=False)) if payload is None else _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigError("%s：schema_version 必须是 %s（当前 %r）"
                          % (where, SCHEMA_VERSION, data.get("schema_version")))
    raw_types = data.get("types")
    if not isinstance(raw_types, list) or not raw_types:
        raise ConfigError("%s：types 必须是非空数组" % where)
    types = []
    by_id = {}
    for raw in raw_types:
        if not isinstance(raw, dict):
            raise ConfigError("%s：types 元素必须是对象" % where)
        type_id = _string_value(raw.get("id"), where, "type.id", required=True)
        if type_id in by_id:
            raise ConfigError("%s：文种 id 重复：%s" % (where, type_id))
        name = _string_value(raw.get("name"), where, "type.name", required=True)
        title_keywords = _string_list(raw.get("title_keywords"), where,
                                      "%s.title_keywords" % type_id, required=True)
        required_fields = _string_list(raw.get("required_fields"), where,
                                       "%s.required_fields" % type_id, required=True)
        unknown_fields = [item for item in required_fields if item not in VALID_FIELDS]
        if unknown_fields:
            raise ConfigError("%s：文种 %s 引用未知字段：%s"
                              % (where, type_id, "、".join(unknown_fields)))
        raw_sections = raw.get("required_sections")
        if not isinstance(raw_sections, list) or not raw_sections:
            raise ConfigError("%s：文种 %s 的 required_sections 必须是非空数组" % (where, type_id))
        sections = []
        section_ids = set()
        for section in raw_sections:
            if not isinstance(section, dict):
                raise ConfigError("%s：文种 %s 的 section 必须是对象" % (where, type_id))
            section_id = _string_value(section.get("id"), where,
                                       "%s.required_sections.id" % type_id, required=True)
            if section_id in section_ids:
                raise ConfigError("%s：文种 %s 的 section id 重复：%s"
                                  % (where, type_id, section_id))
            section_ids.add(section_id)
            section_name = _string_value(section.get("name"), where,
                                         "%s.%s.name" % (type_id, section_id), required=True)
            keywords = _string_list(section.get("keywords"), where,
                                    "%s.%s.keywords" % (type_id, section_id), required=False)
            min_lines = section.get("min_lines")
            if min_lines is not None:
                if isinstance(min_lines, bool) or not isinstance(min_lines, int) or min_lines < 1:
                    raise ConfigError("%s：文种 %s 的 %s.min_lines 必须是正整数"
                                      % (where, type_id, section_id))
            date_required = section.get("date_required", False)
            if not isinstance(date_required, bool):
                raise ConfigError("%s：文种 %s 的 %s.date_required 必须是布尔值"
                                  % (where, type_id, section_id))
            if not keywords and min_lines is None and not date_required:
                raise ConfigError("%s：文种 %s 的 section %s 至少要声明 keywords / min_lines / date_required"
                                  % (where, type_id, section_id))
            parsed = {"id": section_id, "name": section_name, "keywords": keywords,
                      "min_lines": min_lines, "date_required": date_required}
            sections.append(parsed)
        sensitive_terms = _string_list(raw.get("sensitive_terms"), where,
                                       "%s.sensitive_terms" % type_id, required=False)
        visibility = raw.get("visibility_default", "public")
        if visibility not in ("public", "internal"):
            raise ConfigError("%s：文种 %s 的 visibility_default 必须是 public / internal"
                              % (where, type_id))
        parsed_type = {
            "id": type_id,
            "name": name,
            "title_keywords": title_keywords,
            "required_fields": required_fields,
            "required_sections": sections,
            "sensitive_terms": sensitive_terms or list(DEFAULT_SENSITIVE_TERMS),
            "visibility_default": visibility,
        }
        types.append(parsed_type)
        by_id[type_id] = parsed_type
    return {
        "schema_version": SCHEMA_VERSION,
        "pack_version": data.get("pack_version") or "",
        "types": types,
        "by_id": by_id,
    }


def load_facts(payload, where="facts"):
    data = _read_json(payload, where)
    if not isinstance(data, dict):
        raise ConfigError("%s：顶层应为 JSON 对象" % where)
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigError("%s：schema_version 必须是 %s（当前 %r）"
                          % (where, SCHEMA_VERSION, data.get("schema_version")))
    doc_type = data.get("doc_type")
    if not isinstance(doc_type, str) or not doc_type.strip():
        raise ConfigError("%s：doc_type 不能为空" % where)
    visibility = data.get("visibility", "public")
    if visibility not in ("public", "internal"):
        raise ConfigError("%s：visibility 必须是 public / internal" % where)
    facts = json.loads(json.dumps(data, ensure_ascii=False))
    facts["doc_type"] = doc_type.strip()
    facts["visibility"] = visibility
    for field in ("body_points", "attachments"):
        if field in facts:
            facts[field] = _string_list(facts[field], where, field, required=False)
    if "approval" in facts and not isinstance(facts["approval"], dict):
        raise ConfigError("%s：approval 必须是对象" % where)
    return facts


def get_type(types, type_id):
    doc_type = types["by_id"].get(type_id)
    if doc_type is None:
        raise ConfigError("文种不存在：%s（可用：%s）"
                          % (type_id, "、".join(sorted(types["by_id"]))))
    return doc_type


def _finding(kind, severity, detail, suggestion, field="", line=0, quote=""):
    return {
        "kind": kind,
        "severity": severity,
        "field": field,
        "detail": detail,
        "suggestion": suggestion,
        "evidence": {"line": line, "quote": quote},
    }


def _line_for(text, needle):
    for index, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return index, line.strip()
    return 0, ""


def _content_line_count(text):
    return sum(1 for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#"))


def _section_present(text, section):
    if section["keywords"] and any(keyword in text for keyword in section["keywords"]):
        return True
    if section["min_lines"] is not None and _content_line_count(text) >= section["min_lines"]:
        return True
    if section["date_required"] and extract_dates(text):
        return True
    return False


def _fact_value_text(facts, field):
    if not facts or field not in facts:
        return None
    value = facts.get(field)
    if value is None:
        return None
    if isinstance(value, list):
        return " ".join(value)
    return str(value)


def _field_present(text, doc_type, field, facts):
    if field == "title":
        first = next((line.strip() for line in text.splitlines() if line.strip()), "")
        if facts and _fact_value_text(facts, "title"):
            return _fact_value_text(facts, "title") in text
        return any(keyword in first for keyword in doc_type["title_keywords"])
    if field == "issuer":
        fact = _fact_value_text(facts, "issuer")
        if fact:
            return fact in text
        return any(keyword in text for keyword in ("学校", "中学", "小学", "教育局", "教务处"))
    if field == "audience":
        fact = _fact_value_text(facts, "audience")
        if fact:
            return fact in text
        return bool(re.search(r"(?m)^\s*(各|全体|各位|全校)[^\n]{0,40}[:：]\s*$", text))
    if field == "contact":
        fact = _fact_value_text(facts, "contact")
        if fact:
            return fact in text
        return bool(re.search(r"(?m)^[^\n]*(联系|咨询|电话|邮箱)[^\n]*[:：][^\n]*\S", text)
                    or re.search(r"(?<!\d)1[3-9]\d{9}(?!\d)|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", text))
    if field in ("published_date", "action_deadline", "response_deadline", "meeting_date"):
        fact = _fact_value_text(facts, field)
        dates = extract_dates(text)
        if fact:
            normalized = normalize_date(fact)
            return bool(normalized and normalized in dates)
        return bool(dates)
    probes = FIELD_PROBES.get(field)
    if probes:
        if facts and _fact_value_text(facts, field):
            return _fact_value_text(facts, field) in text or any(probe in text for probe in probes)
        return any(probe in text for probe in probes)
    if facts and _fact_value_text(facts, field):
        return _fact_value_text(facts, field) in text
    return False


def build_skeleton(facts, types, now=None):
    doc_type = get_type(types, facts["doc_type"])
    fields = {}
    findings = []
    for field in doc_type["required_fields"]:
        value = facts.get(field)
        if isinstance(value, list):
            value = [item for item in value if item]
        if value in (None, "", []):
            fields[field] = PLACEHOLDER
            findings.append(_finding(
                "field_missing", "high", "缺少必填字段：%s（%s）" % (field, doc_type["name"]),
                "补充真实事实后再生成或签发；不要用推断内容代替。", field=field))
        else:
            fields[field] = value
    body_points = facts.get("body_points") or []
    if not body_points:
        body_points = [PLACEHOLDER]
        findings.append(_finding(
            "field_missing", "high", "缺少正文要点：body_points",
            "补充要写进正文的事实要点；本工具不生成事实。", field="body_points"))
    attachments = facts.get("attachments") or []
    findings.sort(key=lambda item: (item["kind"], item["field"], item["detail"]))
    generated_at = now or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "tool_version": VERSION,
        "generated_at": generated_at,
        "document": {
            "type": doc_type["id"],
            "type_name": doc_type["name"],
            "title": fields.get("title", PLACEHOLDER),
            "visibility": facts.get("visibility", doc_type["visibility_default"]),
        },
        "facts": {
            "doc_type": facts["doc_type"],
            "visibility": facts.get("visibility", doc_type["visibility_default"]),
        },
        "fields": fields,
        "body_points": list(body_points),
        "attachments": list(attachments),
        "findings": findings,
        "sources": [{"rule_pack": "builtin", "pack_version": types.get("pack_version", "")}],
        "disclaimer": DISCLAIMER,
    }


def _append_term_findings(findings, text, terms, kind, severity, detail_tpl, suggestion):
    seen = set()
    for term in terms:
        if term not in text or term in seen:
            continue
        seen.add(term)
        line, quote = _line_for(text, term)
        findings.append(_finding(kind, severity, detail_tpl % term, suggestion,
                                 line=line, quote=quote))


def check_document(text, doc_type, facts=None, now=None):
    del now  # 检查结果不依赖运行时间，保留参数便于调用方统一。
    text = normalize_text(text)
    facts = facts or {}
    visibility = facts.get("visibility", doc_type["visibility_default"])
    findings = []

    for field in doc_type["required_fields"]:
        if not _field_present(text, doc_type, field, facts):
            findings.append(_finding(
                "field_missing", "high", "文稿未找到必填字段：%s（%s）" % (field, doc_type["name"]),
                "补上真实字段；若暂时没有，请保留占位并在签发前确认。", field=field))

    for section in doc_type["required_sections"]:
        if not _section_present(text, section):
            findings.append(_finding(
                "section_missing", "high", "缺少必填结构段：%s" % section["name"],
                "按文种结构补齐该段，或由学校规则包调整要求。", field=section["id"]))

    for match in BAD_DATE_RE.finditer(text):
        line, quote = _line_for(text, match.group(0))
        findings.append(_finding(
            "date_format_invalid", "medium", "日期格式不符合约定：%s" % match.group(0),
            "统一使用 YYYY-MM-DD 或 YYYY年M月D日；内部会归一化后再比较。",
            field="date", line=line, quote=quote))

    if facts:
        published = normalize_date(facts.get("published_date"))
        deadline = normalize_date(facts.get("action_deadline") or facts.get("response_deadline"))
        if published and deadline and published > deadline:
            findings.append(_finding(
                "date_order_invalid", "high", "成文日期晚于办理截止日期：%s > %s"
                % (published, deadline),
                "核对成文日期与办理截止日期，避免出现倒置。",
                field="action_deadline"))
        dates = extract_dates(text)
        for field in ("published_date", "action_deadline", "response_deadline", "meeting_date"):
            expected = normalize_date(facts.get(field))
            if expected and expected not in dates:
                findings.append(_finding(
                    "fact_date_mismatch", "medium", "文稿未出现事实清单中的 %s：%s"
                    % (field, expected),
                    "核对事实清单与文稿；日期不一致时不要直接签发。",
                    field=field))

    attachment_names = facts.get("attachments") or []
    if attachment_names:
        for name in attachment_names:
            if name not in text:
                findings.append(_finding(
                    "attachment_missing", "high", "事实附件未在文稿中出现：%s" % name,
                    "在正文引用或附件清单中补上该附件；没有附件则从事实清单移除。",
                    field="attachments"))
    elif facts and "附件" in text:
        line, quote = _line_for(text, "附件")
        findings.append(_finding(
            "attachment_unknown", "medium", "文稿写了附件，但事实清单没有附件",
            "补全附件清单，或删除无依据的附件引用。",
            field="attachments", line=line, quote=quote))

    for placeholder in PLACEHOLDERS:
        if placeholder in text:
            line, quote = _line_for(text, placeholder)
            findings.append(_finding(
                "placeholder_present", "medium", "文稿仍含未定值：%s" % placeholder,
                "签发前补齐或删除占位值；不要带着占位值对外发布。",
                field="content", line=line, quote=quote))

    for label, pattern in PRIVACY_PATTERNS:
        match = pattern.search(text)
        if match:
            line, quote = _line_for(text, match.group(0))
            severity = "high" if visibility == "public" else "medium"
            findings.append(_finding(
                "privacy_risk", severity, "发现可能的学生个人信息：%s" % label,
                "删除、脱敏或改为内部流转；不要将学生个人信息放入公开文书。",
                field="privacy", line=line, quote=quote))

    _append_term_findings(
        findings, text, doc_type.get("sensitive_terms") or DEFAULT_SENSITIVE_TERMS,
        "sensitive_term_review", "low", "需人工复核的表述：%s",
        "确认措辞、依据和审批链；本工具不判断其合法性。")
    _append_term_findings(
        findings, text, OVERCLAIM_TERMS, "overclaim_review", "low", "可能存在过度承诺：%s",
        "改为可核查、可执行的表述，避免无法兑现的承诺。")

    if doc_type["id"] == "minutes" and "待办" in text:
        has_owner = any(term in text for term in ("责任人", "负责人", "牵头"))
        has_time = any(term in text for term in ("完成时间", "截止", "前完成", "前提交"))
        if not has_owner or not has_time:
            findings.append(_finding(
                "action_item_incomplete", "medium", "会议纪要待办缺少责任人或不完整完成时间",
                "每条待办补上责任人和完成时间，便于会后跟踪。",
                field="action_items"))

    findings.sort(key=lambda item: (item["kind"], item["field"], item["detail"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "tool_version": VERSION,
        "document": {
            "type": doc_type["id"],
            "type_name": doc_type["name"],
            "visibility": visibility,
        },
        "facts": {
            "used": bool(facts),
            "doc_type": facts.get("doc_type", ""),
        },
        "checked": {
            "fields": list(doc_type["required_fields"]),
            "sections": [section["id"] for section in doc_type["required_sections"]],
            "dates": extract_dates(text),
        },
        "findings": findings,
        "summary": {"findings": len(findings)},
        "sources": [{"rule_pack": "builtin"}],
        "disclaimer": DISCLAIMER,
    }


def render_skeleton_markdown(skeleton):
    fields = skeleton["fields"]
    lines = []
    lines.append("# 学校公文骨架：%s（元公 yotta-school-doc %s）"
                 % (skeleton["document"]["title"], skeleton["tool_version"]))
    lines.append("")
    lines.append("## 1. 基本信息")
    lines.append("")
    lines.append("- 文种：%s" % skeleton["document"]["type_name"])
    lines.append("- 受文对象：%s" % fields.get("audience", PLACEHOLDER))
    lines.append("- 成文单位：%s" % fields.get("issuer", PLACEHOLDER))
    lines.append("- 成文日期：%s" % fields.get("published_date", PLACEHOLDER))
    lines.append("")
    lines.append("## 2. 正文要点")
    lines.append("")
    for index, point in enumerate(skeleton["body_points"], 1):
        lines.append("%d. %s" % (index, point))
    lines.append("")
    lines.append("## 3. 办理要求")
    lines.append("")
    for key in ("action_deadline", "response_deadline", "decision_request", "reason",
                "summary", "next_steps", "goal", "steps", "owner", "timeline",
                "highlights"):
        if key in fields:
            lines.append("- %s：%s" % (key, fields[key]))
    lines.append("- 联系方式：%s" % fields.get("contact", PLACEHOLDER))
    lines.append("")
    lines.append("## 4. 附件")
    lines.append("")
    if skeleton["attachments"]:
        for index, name in enumerate(skeleton["attachments"], 1):
            lines.append("%d. %s" % (index, name))
    else:
        lines.append("- 无附件或尚未登记。")
    lines.append("")
    lines.append("## 5. 来源与免责")
    lines.append("")
    for source in skeleton["sources"]:
        lines.append("- 规则包：%s（%s）" % (source.get("rule_pack", ""),
                                              source.get("pack_version", "")))
    lines.append("- %s" % skeleton["disclaimer"])
    lines.append("")
    return "\n".join(lines)


def render_check_markdown(result):
    lines = []
    lines.append("# 学校公文检查：%s（元公 yotta-school-doc %s）"
                 % (result["document"]["type_name"], result["tool_version"]))
    lines.append("")
    lines.append("- 文种：%s" % result["document"]["type_name"])
    lines.append("- 流水依据：%s" % ("事实清单 + 文稿" if result["facts"]["used"] else "仅文稿"))
    lines.append("")
    lines.append("## 1. 缺口清单")
    lines.append("")
    if not result["findings"]:
        lines.append("未发现结构性缺口。")
    else:
        for finding in result["findings"]:
            lines.append("- [%s/%s] %s" % (finding["kind"], finding["severity"],
                                            finding["detail"]))
            if finding["evidence"].get("quote"):
                lines.append("  - 证据：第 %d 行「%s」"
                             % (finding["evidence"]["line"], finding["evidence"]["quote"]))
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


TEMPLATE_FACTS = {
    "schema_version": SCHEMA_VERSION,
    "doc_type": "notice",
    "visibility": "public",
    "title": "关于开展示例活动的通知",
    "issuer": "示例中学",
    "published_date": "2026-09-24",
    "audience": "各年级组、各班级",
    "action_deadline": "2026-09-30",
    "contact": "教务处（010-00000000）",
    "body_points": ["示例活动时间与地点", "报名办法", "安全工作要求"],
    "attachments": ["报名表.xlsx"],
}


def _drop_private_facts(facts):
    keep = {
        "schema_version": facts.get("schema_version"),
        "doc_type": facts.get("doc_type"),
        "visibility": facts.get("visibility", "public"),
        "title": facts.get("title", PLACEHOLDER),
        "issuer": facts.get("issuer", PLACEHOLDER),
        "published_date": facts.get("published_date", PLACEHOLDER),
        "audience": facts.get("audience", PLACEHOLDER),
        "action_deadline": facts.get("action_deadline", PLACEHOLDER),
        "contact": facts.get("contact", PLACEHOLDER),
        "body_points": list(facts.get("body_points") or []),
        "attachments": list(facts.get("attachments") or []),
    }
    return keep


def cmd_template(args):
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    types = load_types(None)
    facts = load_facts(TEMPLATE_FACTS)
    skeleton = build_skeleton(facts, types)
    _write_text(out_dir / "types.json",
                json.dumps(DEFAULT_TYPES, ensure_ascii=False, indent=2) + "\n")
    _write_text(out_dir / "facts.json",
                json.dumps(_drop_private_facts(TEMPLATE_FACTS), ensure_ascii=False, indent=2) + "\n")
    _write_text(out_dir / "document.md", render_skeleton_markdown(skeleton))
    print("已生成模板：%s（types.json / facts.json / document.md）" % out_dir)
    return 0


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


def _load_doc_type(args):
    types = load_types(getattr(args, "types_path", None), "types")
    return types, get_type(types, args.type)


def cmd_draft(args):
    types, doc_type = _load_doc_type(args)
    facts = load_facts(args.facts)
    if facts["doc_type"] != doc_type["id"]:
        raise ConfigError("事实清单 doc_type=%s 与 --type=%s 不一致"
                          % (facts["doc_type"], doc_type["id"]))
    skeleton = build_skeleton(facts, types)
    _emit(skeleton, render_skeleton_markdown(skeleton), args)
    gate = _parse_gate(args.gate)
    if gate is not None and len(skeleton["findings"]) >= gate:
        return 1
    return 0


def cmd_check(args, stdin_text=None):
    types, doc_type = _load_doc_type(args)
    facts = load_facts(args.facts) if args.facts else None
    if facts and facts["doc_type"] != doc_type["id"]:
        raise ConfigError("事实清单 doc_type=%s 与 --type=%s 不一致"
                          % (facts["doc_type"], doc_type["id"]))
    if args.stdin:
        text = stdin_text if stdin_text is not None else sys.stdin.read()
    else:
        if not args.doc:
            raise InputError("check 需要 --doc <文件> 或 --stdin")
        path = Path(args.doc)
        if not path.is_file():
            raise InputError("文稿文件不存在：%s" % path)
        text = path.read_text(encoding="utf-8")
    result = check_document(text, doc_type, facts=facts)
    _emit(result, render_check_markdown(result), args)
    gate = _parse_gate(args.gate)
    if gate is not None and len(result["findings"]) >= gate:
        return 1
    return 0


def cmd_types(args):
    types = load_types(getattr(args, "types_path", None), "types")
    if args.types_command == "list":
        print("文种清单（规则包 %s，共 %d 类）："
              % (types.get("pack_version") or "-", len(types["types"])))
        for doc_type in types["types"]:
            print("- %s  %s  必填字段 %d 项"
                  % (doc_type["id"], doc_type["name"], len(doc_type["required_fields"])))
        return 0
    if args.types_command == "show":
        if not getattr(args, "type", None):
            raise InputError("types show 需要 --type <文种 id>")
        print(json.dumps(get_type(types, args.type), ensure_ascii=False,
                         indent=2, sort_keys=True))
        return 0
    if args.types_command == "validate":
        print("规则包校验通过：%s，共 %d 类" % (types.get("pack_version") or "-",
                                                len(types["types"])))
        return 0
    raise InputError("未知 types 子命令")


def build_parser():
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="元公 —— 本地、确定性的学校公文可信起草与校验引擎（零依赖，不联网）",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command")

    draft = sub.add_parser("draft", help="按事实 JSON 生成学校公文骨架")
    draft.add_argument("--type", required=True)
    draft.add_argument("--facts", required=True)
    draft.add_argument("--types", dest="types_path")
    draft.add_argument("--format", choices=("md", "json"), default="md")
    draft.add_argument("--out")
    draft.add_argument("--gate")

    check = sub.add_parser("check", help="对已有文稿做确定性校验")
    check.add_argument("--doc")
    check.add_argument("--stdin", action="store_true")
    check.add_argument("--type", required=True)
    check.add_argument("--facts")
    check.add_argument("--types", dest="types_path")
    check.add_argument("--format", choices=("md", "json"), default="md")
    check.add_argument("--out")
    check.add_argument("--gate")

    types_cmd = sub.add_parser("types", help="文种规则包操作")
    types_sub = types_cmd.add_subparsers(dest="types_command")
    for name in ("list", "validate"):
        item = types_sub.add_parser(name)
        item.add_argument("--types", dest="types_path")
    show = types_sub.add_parser("show")
    show.add_argument("--type", required=True)
    show.add_argument("--types", dest="types_path")

    template = sub.add_parser("template", help="生成规则包 / 事实 / 文稿模板")
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
        if args.command == "draft":
            return cmd_draft(args)
        if args.command == "check":
            return cmd_check(args, stdin_text=stdin_text)
        if args.command == "types":
            if getattr(args, "types_command", None):
                return cmd_types(args)
            sys.stderr.write("错误：types 需要子命令（list / show / validate）\n")
            return 2
        if args.command == "template":
            return cmd_template(args)
        sys.stderr.write("错误：未知命令。可用：draft / check / types / template\n")
        return 2
    except SchoolDocError as exc:
        sys.stderr.write("错误：%s\n" % exc.message)
        return exc.exit_code
    except OSError as exc:
        sys.stderr.write("错误：文件操作失败：%s\n" % exc)
        return 4


if __name__ == "__main__":
    sys.exit(main())
