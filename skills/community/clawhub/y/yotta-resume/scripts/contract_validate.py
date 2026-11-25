#!/usr/bin/env python3
"""Validate yotta-resume data contracts without network access or writes."""

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path


CONTRACT_VERSION = "1.0"
CONTRACT_FILES = (
    "security-role-map.json",
    "security-role-map.schema.json",
    "source-registry.json",
    "source-registry.schema.json",
    "source-watch-state.json",
    "source-watch-state.schema.json",
    "question-bank.json",
    "question-bank.schema.json",
    "evidence-ledger.json",
    "evidence-ledger.schema.json",
    "dual-role-contract.json",
    "dual-role-contract.schema.json",
    "industry-registry.json",
    "industry-registry.schema.json",
    "interview-session.schema.json",
)

REQUIRED_ROLE_IDS = {
    "soc",
    "incident_response",
    "offensive_security",
    "appsec",
    "security_engineering",
    "grc_data_security",
    "software_engineering",
    "data_ai",
    "business_operations",
    "generic",
}
REQUIRED_LEVELS = {"junior", "mid", "senior", "lead"}
REQUIRED_DATA_CLASSES = {
    "private_evidence_ledger",
    "raw_resume",
    "public_resume",
    "analysis_report",
    "interview_plan",
    "scorecard",
    "audit_log",
}
SOURCE_LAYERS = {"A", "B", "C", "D"}
SOURCE_POLICIES = {"facts_only", "link_only", "permission_required"}
LICENSE_STATUSES = {"unknown", "review_required", "cleared", "restricted"}
SOURCE_STATUSES = {"active", "draft", "retired"}
QUESTION_KINDS = {"knowledge", "scenario", "resume_followup"}
QUESTION_STATUSES = {"draft", "active", "retired"}
RESPONSIBILITY_VALUES = {"lead", "co_owner", "assist", "participate", "unknown"}
SENSITIVITY_VALUES = {"public", "internal", "confidential", "restricted"}

EVIDENCE_REQUIRED_FIELDS = (
    "evidence_id",
    "section",
    "claim",
    "scenario",
    "goal",
    "responsibility",
    "actions",
    "methods",
    "scale",
    "result",
    "supporting_artifacts",
    "boundaries",
    "user_confirmed",
    "source_refs",
    "sensitivity",
    "export_allowed",
)


def _error(code, path, message):
    return {
        "code": code,
        "path": path,
        "message": message,
    }


def _read_json(path, errors):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(_error("FILE_MISSING", path.name, "契约文件不存在"))
        return None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(_error("JSON_INVALID", path.name, str(exc)))
        return None
    if not isinstance(payload, dict):
        errors.append(_error("ROOT_NOT_OBJECT", path.name, "JSON 根节点必须是对象"))
        return None
    return payload


def _parse_date(value, path, field, errors, allow_none=False):
    if value is None and allow_none:
        return None
    if not isinstance(value, str):
        errors.append(_error("DATE_INVALID", path, "{} 必须是 ISO 日期".format(field)))
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        errors.append(_error("DATE_INVALID", path, "{} 不是有效 ISO 日期".format(field)))
        return None


def _canonical_hash(payload):
    filtered = {
        key: value
        for key, value in payload.items()
        if key != "content_hash"
    }
    canonical = json.dumps(
        filtered,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validate_header(data, filename, errors):
    if data.get("schema_version") != CONTRACT_VERSION:
        errors.append(_error(
            "SCHEMA_VERSION_INVALID",
            filename,
            "schema_version 必须为 {}".format(CONTRACT_VERSION),
        ))
    if data.get("contract_version") != CONTRACT_VERSION:
        errors.append(_error(
            "CONTRACT_VERSION_INVALID",
            filename,
            "contract_version 必须为 {}".format(CONTRACT_VERSION),
        ))
    if "generated_at" in data:
        _parse_date(data["generated_at"], filename, "generated_at", errors)


def _validate_schema_files(loaded, errors):
    for filename in CONTRACT_FILES:
        if not filename.endswith(".schema.json"):
            continue
        data = loaded.get(filename)
        if data is None:
            continue
        if not isinstance(data.get("$schema"), str):
            errors.append(_error("SCHEMA_METADATA_MISSING", filename, "缺少 $schema"))
        if not isinstance(data.get("title"), str) or not data["title"].strip():
            errors.append(_error("SCHEMA_METADATA_MISSING", filename, "缺少 title"))


def _validate_role_map(data, errors):
    filename = "security-role-map.json"
    if data is None:
        return set(), set()
    _validate_header(data, filename, errors)
    levels = data.get("levels")
    if not isinstance(levels, list):
        errors.append(_error("LEVELS_INVALID", filename, "levels 必须是数组"))
        levels = []
    level_set = {item for item in levels if isinstance(item, str)}
    if level_set != REQUIRED_LEVELS or len(levels) != len(REQUIRED_LEVELS):
        errors.append(_error(
            "LEVELS_INVALID",
            filename,
            "levels 必须精确包含 junior / mid / senior / lead",
        ))

    families = data.get("role_families")
    if not isinstance(families, list):
        errors.append(_error("ROLES_INVALID", filename, "role_families 必须是数组"))
        families = []

    seen = set()
    for index, family in enumerate(families):
        if not isinstance(family, dict):
            errors.append(_error("ROLE_INVALID", filename, "岗位族 #{} 必须是对象".format(index)))
            continue
        role_id = family.get("id")
        if not isinstance(role_id, str) or not role_id:
            errors.append(_error("ROLE_INVALID", filename, "岗位族缺少 id"))
            continue
        if role_id in seen:
            errors.append(_error("ROLE_DUPLICATE", filename, "岗位族 ID 重复：{}".format(role_id)))
        seen.add(role_id)
        for field in (
            "display_name",
            "aliases",
            "nice_work_roles",
            "evidence_dimensions",
            "interview_dimensions",
            "risk_rules",
            "resume_evidence_requirements",
        ):
            value = family.get(field)
            if field == "display_name":
                if not isinstance(value, str) or not value.strip():
                    errors.append(_error("ROLE_FIELD_MISSING", filename, "{} 缺少 {}".format(role_id, field)))
            elif not isinstance(value, list) or not value:
                errors.append(_error("ROLE_FIELD_MISSING", filename, "{} 缺少 {}".format(role_id, field)))

    if seen != REQUIRED_ROLE_IDS:
        missing = sorted(REQUIRED_ROLE_IDS - seen)
        extra = sorted(seen - REQUIRED_ROLE_IDS)
        if missing:
            errors.append(_error(
                "ROLE_UNKNOWN",
                filename,
                "缺少岗位族：{}".format(", ".join(missing)),
            ))
        if extra:
            errors.append(_error(
                "ROLE_UNKNOWN",
                filename,
                "未登记岗位族：{}".format(", ".join(extra)),
            ))
    return seen, level_set


def _validate_sources(data, today, errors):
    filename = "source-registry.json"
    if data is None:
        return {}
    _validate_header(data, filename, errors)
    sources = data.get("sources")
    if not isinstance(sources, list):
        errors.append(_error("SOURCES_INVALID", filename, "sources 必须是数组"))
        return {}

    by_id = {}
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(_error("SOURCE_INVALID", filename, "来源 #{} 必须是对象".format(index)))
            continue
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            errors.append(_error("SOURCE_INVALID", filename, "来源缺少 source_id"))
            continue
        if source_id in by_id:
            errors.append(_error("SOURCE_DUPLICATE", filename, "来源 ID 重复：{}".format(source_id)))
        by_id[source_id] = source

        if source.get("layer") not in SOURCE_LAYERS:
            errors.append(_error("SOURCE_LAYER_INVALID", filename, "{} layer 非法".format(source_id)))
        for field in ("title", "publisher"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                errors.append(_error("SOURCE_FIELD_MISSING", filename, "{} 缺少 {}".format(source_id, field)))
        url = source.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            errors.append(_error("SOURCE_URL_INVALID", filename, "{} URL 必须以 https:// 开头".format(source_id)))

        _parse_date(source.get("published_at"), filename, "published_at", errors, allow_none=True)
        _parse_date(source.get("retrieved_at"), filename, "retrieved_at", errors)
        verified = _parse_date(source.get("last_verified_at"), filename, "last_verified_at", errors)
        for field in ("refresh_interval_days", "stale_after_days"):
            value = source.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                errors.append(_error("SOURCE_INTERVAL_INVALID", filename, "{} {} 必须是正整数".format(source_id, field)))
        if source.get("usage_policy") not in SOURCE_POLICIES:
            errors.append(_error("SOURCE_POLICY_INVALID", filename, "{} usage_policy 非法".format(source_id)))
        if source.get("license_review_status") not in LICENSE_STATUSES:
            errors.append(_error("SOURCE_LICENSE_INVALID", filename, "{} license_review_status 非法".format(source_id)))
        if source.get("status") not in SOURCE_STATUSES:
            errors.append(_error("SOURCE_STATUS_INVALID", filename, "{} status 非法".format(source_id)))

        stale_after = source.get("stale_after_days")
        if verified is not None and isinstance(stale_after, int) and (today - verified).days > stale_after:
            errors.append(_error(
                "SOURCE_EXPIRED",
                filename,
                "{} 已超过 {} 天有效期".format(source_id, stale_after),
            ))
    return by_id


def _validate_source_watch_state(data, sources, errors):
    filename = "source-watch-state.json"
    if data is None:
        return 0
    _validate_header(data, filename, errors)
    entries = data.get("sources")
    if not isinstance(entries, list):
        errors.append(_error(
            "SOURCE_STATE_INVALID",
            filename,
            "sources 必须是数组",
        ))
        return 0

    seen = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(_error(
                "SOURCE_STATE_INVALID",
                filename,
                "来源指纹 #{} 必须是对象".format(index),
            ))
            continue
        source_id = entry.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            errors.append(_error(
                "SOURCE_STATE_INVALID",
                filename,
                "来源指纹 #{} 缺少 source_id".format(index),
            ))
            continue
        if source_id in seen:
            errors.append(_error(
                "SOURCE_STATE_DUPLICATE",
                filename,
                "来源指纹重复：{}".format(source_id),
            ))
        seen.add(source_id)
        if source_id not in sources:
            errors.append(_error(
                "SOURCE_STATE_UNKNOWN",
                filename,
                "来源指纹引用了未登记来源 {}".format(source_id),
            ))
        content_hash = entry.get("content_sha256")
        if (
            not isinstance(content_hash, str)
            or len(content_hash) != 64
            or any(char not in "0123456789abcdef" for char in content_hash)
        ):
            errors.append(_error(
                "SOURCE_STATE_HASH_INVALID",
                filename,
                "{} content_sha256 必须是 64 位小写十六进制".format(source_id),
            ))
        _parse_date(entry.get("checked_at"), filename, "checked_at", errors)
        for field in ("etag", "last_modified"):
            value = entry.get(field)
            if value is not None and not isinstance(value, str):
                errors.append(_error(
                    "SOURCE_STATE_FIELD_INVALID",
                    filename,
                    "{} {} 必须是字符串或 null".format(source_id, field),
                ))
    return len(seen)


def _validate_questions(data, role_ids, level_ids, sources, today, errors):
    filename = "question-bank.json"
    if data is None:
        return 0
    _validate_header(data, filename, errors)
    questions = data.get("questions")
    if not isinstance(questions, list):
        errors.append(_error("QUESTIONS_INVALID", filename, "questions 必须是数组"))
        return 0

    seen = set()
    prompts = {}
    for index, question in enumerate(questions):
        if not isinstance(question, dict):
            errors.append(_error("QUESTION_INVALID", filename, "题目 #{} 必须是对象".format(index)))
            continue
        question_id = question.get("question_id")
        if not isinstance(question_id, str) or not question_id:
            errors.append(_error("QUESTION_INVALID", filename, "题目缺少 question_id"))
            continue
        if question_id in seen:
            errors.append(_error("QUESTION_DUPLICATE", filename, "题目 ID 重复：{}".format(question_id)))
        seen.add(question_id)

        if question.get("role_family") not in role_ids:
            errors.append(_error("ROLE_UNKNOWN", filename, "{} role_family 未登记".format(question_id)))
        if question.get("level") not in level_ids:
            errors.append(_error("LEVEL_UNKNOWN", filename, "{} level 未登记".format(question_id)))
        if question.get("kind") not in QUESTION_KINDS:
            errors.append(_error("QUESTION_KIND_INVALID", filename, "{} kind 非法".format(question_id)))
        if question.get("status") not in QUESTION_STATUSES:
            errors.append(_error("QUESTION_STATUS_INVALID", filename, "{} status 非法".format(question_id)))
        for field in ("dimension", "prompt", "answer_boundary"):
            if not isinstance(question.get(field), str) or not question[field].strip():
                errors.append(_error("QUESTION_FIELD_MISSING", filename, "{} 缺少 {}".format(question_id, field)))
        prompt = question.get("prompt")
        if isinstance(prompt, str) and prompt.strip():
            if prompt in prompts:
                errors.append(_error(
                    "QUESTION_PROMPT_DUPLICATE",
                    filename,
                    "{} 与 {} 题干重复".format(question_id, prompts[prompt]),
                ))
            else:
                prompts[prompt] = question_id
        for field in ("expected_evidence", "followups", "source_refs"):
            if not isinstance(question.get(field), list):
                errors.append(_error("QUESTION_FIELD_MISSING", filename, "{} 缺少 {}".format(question_id, field)))

        source_refs = question.get("source_refs")
        refs = source_refs if isinstance(source_refs, list) else []
        if any(not isinstance(item, str) or not item for item in refs):
            errors.append(_error(
                "QUESTION_SOURCE_REF_INVALID",
                filename,
                "{} source_refs 只能包含非空字符串".format(question_id),
            ))
            refs = [item for item in refs if isinstance(item, str) and item]
        missing_refs = [item for item in refs if item not in sources]
        for source_id in missing_refs:
            errors.append(_error(
                "QUESTION_SOURCE_MISSING",
                filename,
                "{} 引用了不存在的来源 {}".format(question_id, source_id),
            ))
        existing = [sources[item] for item in refs if item in sources]
        if not any(item.get("layer") in {"A", "B"} for item in existing):
            errors.append(_error(
                "QUESTION_SOURCE_WEAK",
                filename,
                "{} 至少需要一个 A 或 B 层来源".format(question_id),
            ))
        if any(item.get("status") != "active" for item in existing):
            errors.append(_error(
                "QUESTION_SOURCE_INACTIVE",
                filename,
                "{} 引用了非 active 来源".format(question_id),
            ))

        verified = _parse_date(
            question.get("last_verified_at"),
            filename,
            "last_verified_at",
            errors,
        )
        stale_after = question.get("stale_after_days")
        if not isinstance(stale_after, int) or isinstance(stale_after, bool) or stale_after < 1:
            errors.append(_error(
                "QUESTION_STALE_POLICY_INVALID",
                filename,
                "{} stale_after_days 必须是正整数".format(question_id),
            ))
        elif verified is not None and (today - verified).days > stale_after:
            if question.get("freshness_label") == "latest":
                errors.append(_error(
                    "QUESTION_STALE",
                    filename,
                    "{} 已过期，不能标记为 latest".format(question_id),
                ))

        expected_hash = question.get("content_hash")
        actual_hash = _canonical_hash(question)
        if expected_hash != actual_hash:
            errors.append(_error(
                "QUESTION_HASH_MISMATCH",
                filename,
                "{} content_hash 不匹配".format(question_id),
            ))
    return len(questions)


def _validate_ledger(data, sources, errors):
    filename = "evidence-ledger.json"
    if data is None:
        return
    _validate_header(data, filename, errors)
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append(_error("LEDGER_INVALID", filename, "entries 必须是数组"))
        return
    seen = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(_error("LEDGER_INVALID", filename, "证据 #{} 必须是对象".format(index)))
            continue
        evidence_id = entry.get("evidence_id")
        if evidence_id in seen:
            errors.append(_error("EVIDENCE_DUPLICATE", filename, "证据 ID 重复：{}".format(evidence_id)))
        seen.add(evidence_id)
        for field in EVIDENCE_REQUIRED_FIELDS:
            if field not in entry:
                errors.append(_error(
                    "LEDGER_FIELD_MISSING",
                    filename,
                    "{} 缺少 {}".format(evidence_id or index, field),
                ))
        if entry.get("responsibility") not in RESPONSIBILITY_VALUES:
            errors.append(_error("LEDGER_RESPONSIBILITY_INVALID", filename, "{} responsibility 非法".format(evidence_id or index)))
        if entry.get("sensitivity") not in SENSITIVITY_VALUES:
            errors.append(_error("LEDGER_SENSITIVITY_INVALID", filename, "{} sensitivity 非法".format(evidence_id or index)))
        actions = entry.get("actions")
        if not isinstance(actions, list) or not actions:
            errors.append(_error("LEDGER_ACTIONS_MISSING", filename, "{} actions 不能为空".format(evidence_id or index)))
        if not isinstance(entry.get("user_confirmed"), bool):
            errors.append(_error(
                "LEDGER_FIELD_TYPE_INVALID",
                filename,
                "{} user_confirmed 必须是布尔值".format(evidence_id or index),
            ))
        if not isinstance(entry.get("export_allowed"), bool):
            errors.append(_error(
                "LEDGER_FIELD_TYPE_INVALID",
                filename,
                "{} export_allowed 必须是布尔值".format(evidence_id or index),
            ))
        if entry.get("user_confirmed") is False and entry.get("export_allowed") is True:
            errors.append(_error(
                "LEDGER_UNCONFIRMED_EXPORT",
                filename,
                "{} 未确认事实不得进入导出".format(evidence_id or index),
            ))
        for source_id in entry.get("source_refs", []) if isinstance(entry.get("source_refs"), list) else []:
            if source_id not in sources:
                errors.append(_error(
                    "LEDGER_SOURCE_MISSING",
                    filename,
                    "{} 引用了不存在的来源 {}".format(evidence_id or index, source_id),
                ))


def _validate_dual_role(data, errors):
    filename = "dual-role-contract.json"
    if data is None:
        return
    _validate_header(data, filename, errors)
    if data.get("default_policy") != "deny":
        errors.append(_error("DEFAULT_POLICY_INVALID", filename, "default_policy 必须为 deny"))
    if data.get("roles") != ["candidate", "hr"]:
        errors.append(_error("ROLES_INVALID", filename, "roles 必须为 candidate / hr"))
    data_classes = data.get("data_classes")
    if (
        not isinstance(data_classes, list)
        or any(not isinstance(item, str) for item in data_classes)
        or set(data_classes) != REQUIRED_DATA_CLASSES
    ):
        errors.append(_error("DATA_CLASSES_INVALID", filename, "data_classes 必须精确覆盖固定数据类"))
    permissions = data.get("permissions")
    if not isinstance(permissions, dict):
        errors.append(_error("PERMISSIONS_INVALID", filename, "permissions 必须是对象"))
        permissions = {}
    for role in ("candidate", "hr"):
        if not isinstance(permissions.get(role), dict):
            errors.append(_error("PERMISSIONS_INVALID", filename, "缺少 {} 权限".format(role)))

    hr = permissions.get("hr", {}) if isinstance(permissions.get("hr"), dict) else {}
    allowed_actions = {"read", "write"}
    for role_name in ("candidate", "hr"):
        role_permissions = permissions.get(role_name)
        if not isinstance(role_permissions, dict):
            continue
        if set(role_permissions) != REQUIRED_DATA_CLASSES:
            errors.append(_error(
                "PERMISSIONS_INVALID",
                filename,
                "{} 权限必须精确覆盖固定数据类".format(role_name),
            ))
        for data_class, actions in role_permissions.items():
            if not isinstance(actions, list) or any(
                action not in allowed_actions for action in actions
            ):
                errors.append(_error(
                    "ROLE_ACTION_INVALID",
                    filename,
                    "{} 的 {} 权限包含非法动作".format(role_name, data_class),
                ))
    for data_class in ("private_evidence_ledger", "raw_resume", "analysis_report"):
        if hr.get(data_class):
            errors.append(_error(
                "ROLE_ACCESS_DENIED",
                filename,
                "HR 不得读取 {}".format(data_class),
            ))
    candidate = permissions.get("candidate", {}) if isinstance(permissions.get("candidate"), dict) else {}
    if not {"read", "write"}.issubset(set(candidate.get("private_evidence_ledger", []))):
        errors.append(_error(
            "CANDIDATE_ACCESS_REQUIRED",
            filename,
            "候选人必须可读写私有证据账本",
        ))

    protected = data.get("protected_attributes")
    if not isinstance(protected, list) or not protected:
        errors.append(_error("PROTECTED_ATTRIBUTES_INVALID", filename, "受保护属性不能为空"))
        protected = []
    scoring = data.get("scoring_fields")
    if not isinstance(scoring, list):
        errors.append(_error("SCORING_FIELDS_INVALID", filename, "scoring_fields 必须是数组"))
        scoring = []
    overlap = set(protected) & set(scoring)
    if overlap:
        errors.append(_error(
            "PROTECTED_ATTRIBUTE_SCORED",
            filename,
            "受保护属性进入评分：{}".format(", ".join(sorted(overlap))),
        ))

    export = data.get("cross_role_export")
    if not isinstance(export, dict):
        errors.append(_error(
            "CROSS_ROLE_CONFIRMATION_REQUIRED",
            filename,
            "缺少 cross_role_export 契约",
        ))
        return
    required_true = (
        "requires_field_manifest",
        "requires_confirmation",
        "independent_workdirs",
        "independent_outputs",
    )
    if any(export.get(field) is not True for field in required_true):
        errors.append(_error(
            "CROSS_ROLE_CONFIRMATION_REQUIRED",
            filename,
            "跨角色导出必须保留字段清单、确认和独立目录输出",
        ))
    if export.get("default_export_class") != "public_resume":
        errors.append(_error(
            "CROSS_ROLE_DEFAULT_INVALID",
            filename,
            "跨角色默认导出只能是 public_resume",
        ))


def _validate_industry_registry(data, errors):
    filename = "industry-registry.json"
    if data is None:
        return 0
    _validate_header(data, filename, errors)
    extension = data.get("extensions")
    if not isinstance(extension, dict) or extension.get("allow_new_profiles") is not True:
        errors.append(_error(
            "INDUSTRY_EXTENSION_INVALID",
            filename,
            "extensions 必须允许新增行业且将 allow_new_profiles 设为 true",
        ))
    elif not isinstance(extension.get("required_fields"), list) or not extension["required_fields"]:
        errors.append(_error(
            "INDUSTRY_EXTENSION_INVALID",
            filename,
            "extensions.required_fields 必须是非空数组",
        ))

    detection = data.get("detection")
    if (
        not isinstance(detection, dict)
        or detection.get("strategy") != "keyword_score_v1"
        or not isinstance(detection.get("min_high_confidence_hits"), int)
        or detection.get("min_high_confidence_hits") < 1
        or not isinstance(detection.get("ambiguity_margin"), int)
        or detection.get("ambiguity_margin") < 0
    ):
        errors.append(_error(
            "INDUSTRY_DETECTION_INVALID",
            filename,
            "detection 必须是有效的 keyword_score_v1 配置",
        ))

    industries = data.get("industries")
    if not isinstance(industries, list) or len(industries) < 2:
        errors.append(_error(
            "INDUSTRY_INVALID",
            filename,
            "industries 至少需要两个行业配置",
        ))
        return 0

    seen = set()
    fallback_ids = []
    required_fields = (
        "id",
        "display_name",
        "keywords",
        "evidence_dimensions",
        "question_dimensions",
        "role_map_ref",
        "is_fallback",
    )
    for index, industry in enumerate(industries):
        if not isinstance(industry, dict):
            errors.append(_error(
                "INDUSTRY_INVALID",
                filename,
                "行业 #{} 必须是对象".format(index),
            ))
            continue
        industry_id = industry.get("id")
        if (
            not isinstance(industry_id, str)
            or not industry_id
            or not industry_id[0].islower()
            or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789_" for char in industry_id)
        ):
            errors.append(_error(
                "INDUSTRY_ID_INVALID",
                filename,
                "行业 #{} 的 id 非法".format(index),
            ))
            continue
        if industry_id in seen:
            errors.append(_error(
                "INDUSTRY_DUPLICATE",
                filename,
                "行业 ID 重复：{}".format(industry_id),
            ))
        seen.add(industry_id)
        for field in required_fields:
            if field not in industry:
                errors.append(_error(
                    "INDUSTRY_FIELD_MISSING",
                    filename,
                    "{} 缺少 {}".format(industry_id, field),
                ))
        if not isinstance(industry.get("display_name"), str) or not industry.get("display_name", "").strip():
            errors.append(_error(
                "INDUSTRY_FIELD_INVALID",
                filename,
                "{} display_name 必须是非空字符串".format(industry_id),
            ))
        keywords = industry.get("keywords")
        if not isinstance(keywords, list) or any(
            not isinstance(keyword, str) or not keyword.strip()
            for keyword in keywords
        ):
            errors.append(_error(
                "INDUSTRY_FIELD_INVALID",
                filename,
                "{} keywords 必须是字符串数组".format(industry_id),
            ))
        elif not industry.get("is_fallback") and not keywords:
            errors.append(_error(
                "INDUSTRY_FIELD_INVALID",
                filename,
                "{} 非兜底行业必须有识别关键词".format(industry_id),
            ))
        for field in ("evidence_dimensions", "question_dimensions"):
            values = industry.get(field)
            if not isinstance(values, list) or not values or any(
                not isinstance(value, str) or not value.strip()
                for value in values
            ):
                errors.append(_error(
                    "INDUSTRY_FIELD_INVALID",
                    filename,
                    "{} {} 必须是非空字符串数组".format(industry_id, field),
                ))
        if not isinstance(industry.get("is_fallback"), bool):
            errors.append(_error(
                "INDUSTRY_FIELD_INVALID",
                filename,
                "{} is_fallback 必须是布尔值".format(industry_id),
            ))
        elif industry["is_fallback"]:
            fallback_ids.append(industry_id)
        role_map_ref = industry.get("role_map_ref")
        if role_map_ref is not None and not isinstance(role_map_ref, str):
            errors.append(_error(
                "INDUSTRY_FIELD_INVALID",
                filename,
                "{} role_map_ref 必须是字符串或 null".format(industry_id),
            ))

    default_industry = data.get("default_industry")
    if (
        len(fallback_ids) != 1
        or default_industry != fallback_ids[0]
        or default_industry not in seen
    ):
        errors.append(_error(
            "INDUSTRY_FALLBACK_INVALID",
            filename,
            "default_industry 必须指向唯一的兜底行业",
        ))
    return len(seen)


def _validate_interview_schema(data, errors):
    filename = "interview-session.schema.json"
    if data is None:
        return
    properties = data.get("properties")
    if not isinstance(properties, dict):
        errors.append(_error(
            "INTERVIEW_SCHEMA_INVALID",
            filename,
            "缺少 properties",
        ))
        return
    schema_version = properties.get("schema_version")
    if not isinstance(schema_version, dict) or schema_version.get("const") != "1.0":
        errors.append(_error(
            "INTERVIEW_SCHEMA_INVALID",
            filename,
            "schema_version 必须固定为 1.0",
        ))
    required = data.get("required")
    required_fields = {
        "session_id",
        "status",
        "inputs",
        "selection",
        "questions",
        "answers",
        "current_question_id",
        "current_phase",
    }
    if not isinstance(required, list) or not required_fields.issubset(set(required)):
        errors.append(_error(
            "INTERVIEW_SCHEMA_INVALID",
            filename,
            "缺少面试会话必需字段",
        ))
    status = properties.get("status")
    if not isinstance(status, dict) or set(status.get("enum", [])) != {
        "in_progress",
        "completed",
    }:
        errors.append(_error(
            "INTERVIEW_SCHEMA_INVALID",
            filename,
            "status 枚举必须覆盖进行中和已完成",
        ))


def validate_contracts(root=None, today=None):
    """Return a deterministic, local-only contract validation report."""
    base = Path(root) if root else Path(__file__).resolve().parent.parent / "data"
    if (base / "data" / "security-role-map.json").is_file() and not (base / "security-role-map.json").is_file():
        base = base / "data"
    current = today or dt.date.today()
    if isinstance(current, str):
        try:
            current = dt.date.fromisoformat(current)
        except ValueError:
            return {
                "ok": False,
                "contract_version": CONTRACT_VERSION,
                "checked_files": 0,
                "role_family_count": 0,
                "level_count": 0,
                "question_count": 0,
                "source_count": 0,
                "watch_state_count": 0,
                "industry_count": 0,
                "errors": [_error(
                    "TODAY_INVALID",
                    "--today",
                    "today 必须是 YYYY-MM-DD 格式的有效日期",
                )],
                "warnings": [],
            }

    errors = []
    loaded = {}
    for filename in CONTRACT_FILES:
        data = _read_json(base / filename, errors)
        if data is not None:
            loaded[filename] = data

    _validate_schema_files(loaded, errors)
    role_ids, level_ids = _validate_role_map(
        loaded.get("security-role-map.json"),
        errors,
    )
    sources = _validate_sources(
        loaded.get("source-registry.json"),
        current,
        errors,
    )
    watch_state_count = _validate_source_watch_state(
        loaded.get("source-watch-state.json"),
        sources,
        errors,
    )
    question_count = _validate_questions(
        loaded.get("question-bank.json"),
        role_ids,
        level_ids,
        sources,
        current,
        errors,
    )
    _validate_ledger(
        loaded.get("evidence-ledger.json"),
        sources,
        errors,
    )
    _validate_dual_role(
        loaded.get("dual-role-contract.json"),
        errors,
    )
    industry_count = _validate_industry_registry(
        loaded.get("industry-registry.json"),
        errors,
    )
    _validate_interview_schema(
        loaded.get("interview-session.schema.json"),
        errors,
    )

    errors.sort(key=lambda item: (item["path"], item["code"], item["message"]))
    return {
        "ok": not errors,
        "contract_version": CONTRACT_VERSION,
        "checked_files": len(CONTRACT_FILES),
        "role_family_count": len(role_ids),
        "level_count": len(level_ids),
        "question_count": question_count,
        "source_count": len(sources),
        "watch_state_count": watch_state_count,
        "industry_count": industry_count,
        "errors": errors,
        "warnings": [],
    }


def _render_text(report):
    lines = [
        "元简数据契约校验",
        "状态：{}".format("PASS" if report["ok"] else "FAIL"),
        "契约版本：{}".format(report["contract_version"]),
        "文件：{}".format(report["checked_files"]),
        "岗位族：{}".format(report["role_family_count"]),
        "职级：{}".format(report["level_count"]),
        "题目：{}".format(report["question_count"]),
        "来源：{}".format(report["source_count"]),
        "来源指纹：{}".format(report["watch_state_count"]),
        "行业：{}".format(report["industry_count"]),
    ]
    if report["errors"]:
        lines.append("错误：")
        for item in report["errors"]:
            lines.append("- [{}] {}: {}".format(item["code"], item["path"], item["message"]))
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="contract-validate",
        description="离线校验元简岗位族、证据账本、题库、来源、双角色权限与行业扩展契约。",
    )
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent / "data"),
        help="data 目录或技能根目录",
    )
    parser.add_argument("--format", choices=("json", "text"), default="json")
    parser.add_argument("--today", help="覆盖校验日期（YYYY-MM-DD），用于测试与回放")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    report = validate_contracts(args.root, args.today)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(_render_text(report))
    if report["ok"]:
        return 0
    if any(item["code"] == "TODAY_INVALID" for item in report["errors"]):
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
