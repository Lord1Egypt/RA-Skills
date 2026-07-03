"""
Audit installed skills by usage, overlap, impact, confidence, and risk.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

from .risk_signatures import RISK_RULES


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "help",
    "how",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "uses",
    "using",
    "when",
    "with",
    "your",
}

API_STRONG_KEYWORDS = {
    "connector",
    "connectors",
    "gateway",
    "github",
    "gmail",
    "mcp",
    "sdk",
    "slack",
    "stripe",
    "supabase",
    "vercel",
    "webhook",
}

API_SUPPORT_KEYWORDS = {
    "api",
    "apis",
    "http",
    "https",
    "provider",
    "providers",
}

TOOL_KEYWORDS = {
    "browser",
    "csv",
    "deploy",
    "deployment",
    "docx",
    "excel",
    "git",
    "image",
    "ocr",
    "pdf",
    "playwright",
    "pptx",
    "shell",
    "spreadsheet",
    "xlsx",
    "xml",
}

NAME_KEYS = (
    "skill",
    "name",
    "skill_name",
    "技能",
    "技能名",
    "技能名称",
)

IDENTIFIER_KEYS = (
    "id",
    "identifier",
    "skill_id",
    "skillid",
    "技能id",
    "技能标识",
)

SLUG_KEYS = (
    "slug",
    "skill_slug",
    "技能slug",
    "技能短名",
)

PATH_KEYS = (
    "path",
    "skill_path",
    "skill_root",
    "root",
    "directory",
    "dir",
    "location",
    "路径",
    "目录",
    "技能路径",
)

SOURCE_KEYS = (
    "source",
    "origin",
    "来源",
)

NAMESPACE_KEYS = (
    "namespace",
    "plugin",
    "plugin_name",
    "package",
    "namespace_name",
    "命名空间",
    "插件",
    "插件名",
)

COUNT_KEYS = (
    "calls",
    "count",
    "uses",
    "usage",
    "invocations",
    "call_count",
    "usage_count",
    "invoke_count",
    "调用次数",
    "调用数",
    "使用次数",
    "次数",
)

RECENT_30D_KEYS = (
    "recent_30d_calls",
    "recent30_calls",
    "recent_calls_30d",
    "calls_30d",
    "last_30d_calls",
    "30d_calls",
    "近30天调用",
    "最近30天调用",
    "近30天调用次数",
)

RECENT_90D_KEYS = (
    "recent_90d_calls",
    "recent90_calls",
    "recent_calls_90d",
    "calls_90d",
    "last_90d_calls",
    "90d_calls",
    "近90天调用",
    "最近90天调用",
    "近90天调用次数",
)

LAST_USED_KEYS = (
    "last_used_at",
    "last_used",
    "last_invoked_at",
    "last_invocation_at",
    "recent_use_at",
    "上次使用时间",
    "最后使用时间",
    "最近使用时间",
    "最近调用时间",
)

FIRST_SEEN_KEYS = (
    "first_seen_at",
    "installed_at",
    "first_used_at",
    "created_at",
    "首次出现时间",
    "安装时间",
    "首次使用时间",
)

ACTIVE_DAYS_KEYS = (
    "active_days",
    "days_active",
    "used_days",
    "usage_days",
    "活跃天数",
    "使用天数",
)

EXECUTION_COUNT_KEYS = (
    "executions",
    "actual_runs",
    "script_runs",
    "tool_executions",
    "执行次数",
    "实际执行次数",
    "脚本执行次数",
)

SCRIPT_FAILURE_KEYS = (
    "script_failures",
    "execution_failures",
    "failure_count",
    "error_count",
    "脚本失败次数",
    "执行失败次数",
    "错误次数",
)

REPAIR_TURN_KEYS = (
    "repair_turns",
    "fix_turns",
    "debug_turns",
    "manual_fixes",
    "修复轮数",
    "调试轮数",
    "擦屁股轮数",
)

REFERENCE_LOAD_KEYS = (
    "reference_loads",
    "references_loaded",
    "reference_reads",
    "context_loads",
    "reference_files_read",
    "引用加载次数",
    "参考加载次数",
    "上下文加载次数",
)

FALSE_TRIGGER_KEYS = (
    "false_triggers",
    "misfires",
    "accidental_triggers",
    "wrong_triggers",
    "误触发次数",
    "错误触发次数",
)

COLLECTION_KEYS = {
    "skills",
    "items",
    "results",
    "records",
    "entries",
    "data",
    "usage",
    "counts",
    "metrics",
    "cases",
    "rows",
    "messages",
    "conversations",
    "threads",
    "history",
    "community",
    "registry",
}

SCALAR_MAP_KEYS = {
    "usage",
    "counts",
    "metrics",
    "skill_usage",
    "skill_usages",
    "skill_counts",
    "skill_calls",
    "调用统计",
    "按技能调用",
}

WITH_SKILL_KEYS = ("with_skill", "with", "enabled", "treatment", "experiment", "skill_run", "启用技能")
WITHOUT_SKILL_KEYS = ("without_skill", "without", "disabled", "baseline", "control", "no_skill", "基线", "未启用技能")

FLAT_WITH_SCORE_KEYS = ("with_skill_score", "score_with_skill", "skill_score", "enabled_score", "实验分数", "启用技能分数")
FLAT_WITHOUT_SCORE_KEYS = (
    "without_skill_score",
    "score_without_skill",
    "baseline_score",
    "control_score",
    "基线分数",
    "未启用技能分数",
)
FLAT_WITH_PASS_KEYS = ("with_skill_pass", "pass_with_skill", "skill_pass", "enabled_pass", "实验通过", "启用技能通过")
FLAT_WITHOUT_PASS_KEYS = (
    "without_skill_pass",
    "pass_without_skill",
    "baseline_pass",
    "control_pass",
    "基线通过",
    "未启用技能通过",
)

COMMUNITY_RATING_KEYS = ("rating", "score", "community_rating", "registry_rating", "评分", "社区评分")
COMMUNITY_STARS_KEYS = ("stars", "star_count", "likes", "点赞", "收藏数")
COMMUNITY_DOWNLOADS_KEYS = ("downloads", "download_count", "下载量", "下载次数")
COMMUNITY_INSTALLS_CURRENT_KEYS = (
    "installs",
    "installs_current",
    "active_installs",
    "当前安装",
    "当前安装数",
    "安装数",
)
COMMUNITY_INSTALLS_ALL_TIME_KEYS = (
    "installs_all_time",
    "total_installs",
    "all_time_installs",
    "累计安装",
    "累计安装数",
)
COMMUNITY_TRENDING_KEYS = ("trending_7d", "trending", "trend_score", "7日趋势", "趋势分")
COMMUNITY_COMMENTS_KEYS = ("comments", "comments_count", "评论数", "评论数量")
COMMUNITY_UPDATED_KEYS = (
    "last_updated",
    "updated_at",
    "published_at",
    "更新时间",
    "最后更新时间",
    "发布时间",
)

VERDICT_ALIASES = {
    "same": "same",
    "equal": "same",
    "equivalent": "same",
    "一致": "same",
    "相同": "same",
    "无差异": "same",
    "持平": "same",
    "better": "better",
    "improved": "better",
    "improve": "better",
    "更好": "better",
    "更优": "better",
    "提升": "better",
    "worse": "worse",
    "degraded": "worse",
    "regressed": "worse",
    "更差": "worse",
    "退化": "worse",
    "变差": "worse",
}

TEXT_FILE_SUFFIXES = {
    "",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".ps1",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".txt",
}

RISK_SCAN_SUFFIXES = {
    "",
    ".cfg",
    ".ini",
    ".json",
    ".js",
    ".jsx",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
}

RISK_SCAN_DIRS = {"scripts", "resources", "bin", "hooks", ".github", "workflows"}

MAX_SCAN_BYTES = 512 * 1024
HISTORY_EVIDENCE_WEIGHT = 0.45
TEXT_BYTES_PER_CONTEXT_UNIT = 4
CJK_CONTEXT_UNITS_PER_CHAR = 2.0
NON_ASCII_CONTEXT_UNITS_PER_CHAR = 1.0
ABLATION_BASELINE_CASES = 10
ABLATION_INITIAL_CASES = 3
ABLATION_EXPAND_CASES = 5
ABLATION_MAX_CASES = 10
ABLATION_MIN_CANDIDATES = 3
ABLATION_DEFAULT_MAX_CANDIDATES = 8
ABLATION_COST_PROFILES = {
    "light": 6200,
    "realistic": 24000,
    "coding": 50000,
}
ABLATION_COST_UNIT = "estimated_context_units_per_case"
ALLOWED_HISTORY_ROLES = {"user", "assistant"}
HISTORY_SKIP_FIELDS = {
    "developer-instructions",
    "developer-prompt",
    "environment-context",
    "sandbox-policy",
    "skills",
    "tool-definitions",
    "tools",
    "turn-context",
    "user-instructions",
}
HOST_PROMPT_MARKERS = (
    "# " + "agents" + ".md instructions",
    "### available skills",
    "### how to use skills",
    "<app-context>",
    "<environment_context>",
    "<instructions>",
    "\"type\":\"turn_context\"",
    "developer_instructions",
    "user_instructions",
)

COMPILED_RISK_RULES = tuple(
    {
        "label": str(rule["label"]),
        "severity": float(rule["severity"]),
        "patterns": tuple(re.compile(pattern, re.MULTILINE) for pattern in rule["patterns"]),
    }
    for rule in RISK_RULES
)

BROAD_TRIGGER_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\balways\b",
        r"\bany(?:thing| task| request)?\b",
        r"\bevery(?:thing| task| request| time)?\b",
        r"\bwhenever\b",
        r"\ball tasks?\b",
        r"\bgeneral purpose\b",
        r"任何",
        r"所有",
        r"每次",
        r"总是",
        r"通用",
        r"万能",
    )
)

SCRIPT_BURDEN_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    for pattern in (
        r"\btodo\b",
        r"\bfixme\b",
        r"\bplaceholder\b",
        r"\bnotimplementederror\b",
        r"\bpass\s*(?:#|$)",
        r"c:\\users\\",
        r"/users/[^/\s]+/",
        r"/home/[^/\s]+/",
    )
)

VAGUE_RESOURCE_NAME_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^(?:file|doc|document|data|tmp|temp|new|copy|backup|final|misc|stuff)[-_ ]?\d*$",
        r"^(?:untitled|example|sample)[-_ ]?\d*$",
        r"^(?:文件|文档|临时|备份|最终)[-_ ]?\d*$",
    )
)

REFERENCE_TOC_MARKERS = ("table of contents", "[toc]", "## contents", "# contents", "目录")

PRIVATE_BUNDLE_NAME_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"(^|[\\/])\.env(?:\.|$)",
        r"(^|[\\/])id_rsa(?:\.|$)",
        r"(^|[\\/])\.aws(?:[\\/]|$)",
        r"(^|[\\/])\.ssh(?:[\\/]|$)",
        r"(?:^|[\\/])secret(?:s)?(?:\.|[\\/]|$)",
        r"\.(?:pem|pfx|p12|key)$",
    )
)

EXECUTABLE_ASSET_SUFFIXES = {".bat", ".cmd", ".com", ".dll", ".dylib", ".exe", ".msi", ".scr", ".so"}

INSTALL_LIFECYCLE_SCRIPT_KEYS = {
    "preinstall",
    "install",
    "postinstall",
    "prepublish",
    "prepare",
}

PRIVATE_CONTENT_PATTERNS = tuple(
    (label, re.compile(pattern, re.IGNORECASE))
    for label, pattern in (
        ("private-key-block", r"-----BEGIN [A-Z ]{0,30}PRIVATE KEY-----"),
        (
            "credential-assignment",
            r"\b(?:api|access|auth|refresh|session)[_-]?(?:token|key|secret)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{24,}",
        ),
        ("cloud-access-id", r"\bA[SK]IA[0-9A-Z]{16}\b"),
    )
)
