from __future__ import annotations

import argparse
import contextlib
import contextvars
import copy
import datetime
import json
import operator
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import uuid
from typing import Annotated, Any, Callable, Dict, Iterator, List, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

try:
    import langsmith as _langsmith
except Exception:
    _langsmith = None

try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass


def load_openclaw_env_file(env_file: str | None = None) -> None:
    """Load KEY=VALUE pairs from OpenClaw's .env without overriding explicit env."""
    configured_path = (env_file or os.environ.get("OPENCLAW_ENV_FILE", "")).strip()
    if configured_path:
        env_path = os.path.expanduser(configured_path)
    else:
        openclaw_home = os.path.expanduser(os.environ.get("OPENCLAW_HOME", "~/.openclaw"))
        env_path = os.path.join(openclaw_home, ".env")
    if not env_path or not os.path.exists(env_path):
        return

    try:
        with open(env_path, "r", encoding="utf-8") as env_handle:
            lines = env_handle.readlines()
    except OSError:
        return

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ[key] = value


load_openclaw_env_file()

OLLAMA_URL = os.environ.get("ROUTER_OLLAMA_URL", "http://localhost:11434/api/generate")
ROUTER_MODEL_ENV_VAR = "ROUTER_MODEL"
ROUTER_TASK_ENV_VAR = "ROUTER_TASK"
CODEX_CLI_PATH = os.environ.get("ROUTER_CODEX_CLI", shutil.which("codex") or "codex")
ROUTER_CODEX_CWD_ENV_VAR = "ROUTER_CODEX_CWD"
ROUTER_CODEX_SANDBOX_ENV_VAR = "ROUTER_CODEX_SANDBOX"
GEMINI_CLI_PATH = os.environ.get("ROUTER_GEMINI_CLI", shutil.which("gemini") or "/opt/homebrew/bin/gemini")
CLAUDE_CLI_PATH = os.environ.get("ROUTER_CLAUDE_CLI", shutil.which("claude") or "claude")
GEMINI_SYSTEM_SETTINGS_ENV_VAR = "GEMINI_CLI_SYSTEM_SETTINGS_PATH"
ROUTER_SKIP_WARMUP = os.environ.get("ROUTER_SKIP_WARMUP", "0").lower() in ("1", "true", "yes")
ROUTER_LANGSMITH_ENABLED_ENV_VAR = "ROUTER_LANGSMITH_ENABLED"
ROUTER_LANGSMITH_PROJECT_ENV_VAR = "ROUTER_LANGSMITH_PROJECT"
ROUTER_LANGSMITH_TAGS_ENV_VAR = "ROUTER_LANGSMITH_TAGS"
ROUTER_TOKEN_USAGE_LEDGER_ENV_VAR = "ROUTER_TOKEN_USAGE_LEDGER"
#GEMINI_EXTENSION_NAME = os.environ.get("ROUTER_GEMINI_EXTENSION", "superpowers")
PRO = "PRO"
FLASH = "FLASH"
PRO_COMPLEXITY_THRESHOLD = 5
FLASH_COMPLEXITY_THRESHOLD = 2
LOW_CONFIDENCE_THRESHOLD = 0.35
SUMMARY_ROUTE_KEYWORDS = (
    "summary",
    "summarize",
    "report",
    "impact note",
    "risk note",
    "action summary",
    "status update",
    "team update",
    "brief",
    "briefing",
    "recap",
    "write-up",
    "conclusion",
    "document",
    "format",
    "整理",
    "总结",
    "摘要",
    "概述",
    "汇报",
    "状态更新",
    "团队状态更新",
    "影响说明",
    "风险说明",
    "行动摘要",
    "简报",
    "结论",
    "要点",
)
DEFERRED_EXECUTION_KEYWORDS = (
    "synthesize",
    "synthesis",
    "consolidate",
    "combine findings",
    "final comparison",
    "comparison table",
    "final table",
    "final output",
    "final answer",
    "综合",
    "汇总",
    "整合",
    "最终",
    "对比表",
    "比较表",
)
COMMUNICATION_AUDIENCE_KEYWORDS = (
    "产品经理",
    "项目负责人",
    "负责人",
    "值班同事",
    "值班",
    "团队",
    "运营同事",
    "运营",
    "客户",
    "manager",
    "product manager",
    "pm",
    "team",
    "on-call",
    "operations",
    "operator",
    "customer",
    "stakeholder",
)
DEEP_WORK_HINT_KEYWORDS = (
    "inspect",
    "check",
    "audit",
    "examine",
    "identify",
    "compare",
    "determine",
    "isolate",
    "review",
    "verify",
    "analy",
    "debug",
    "diagnos",
    "fix",
    "implement",
    "investig",
    "trace",
    "optimiz",
    "refactor",
    "rewrite",
    "migrate",
    "design",
    "logic",
    "排查",
    "检查",
    "分析",
    "确定",
    "定位",
    "比对",
    "核实",
    "确认",
    "审查",
    "调试",
    "诊断",
    "修复",
    "实现",
    "追踪",
    "优化",
    "重构",
    "重写",
    "迁移",
    "设计",
    "逻辑",
)
HIGH_RISK_CONTEXT_KEYWORDS = (
    "incident",
    "outage",
    "prod",
    "production",
    "billing",
    "payment",
    "payments",
    "finance",
    "financial",
    "settlement",
    "refund",
    "refunds",
    "charge",
    "charges",
    "duplicate charge",
    "double charge",
    "overcharge",
    "auth",
    "authentication",
    "authorization",
    "privilege",
    "security",
    "breach",
    "rollback",
    "roll back",
    "containment",
    "stop-loss",
    "stop loss",
    "kill switch",
    "fraud",
    "事故",
    "故障",
    "线上",
    "生产",
    "计费",
    "账单",
    "支付",
    "财务",
    "金融",
    "结算",
    "退款",
    "扣费",
    "重复扣费",
    "多扣费",
    "鉴权",
    "认证",
    "授权",
    "权限",
    "越权",
    "安全",
    "漏洞",
    "回滚",
    "止损",
    "止血",
    "遏制",
    "熔断",
    "冻结",
    "欺诈",
    "对账",
    "批处理",
)
HIGH_RISK_EVIDENCE_KEYWORDS = (
    "inspect",
    "check",
    "review",
    "collect",
    "gather",
    "compare",
    "trace",
    "query",
    "audit",
    "reconcile",
    "read",
    "log",
    "logs",
    "evidence",
    "data",
    "record",
    "records",
    "transaction",
    "ledger",
    "sample",
    "检查",
    "排查",
    "核对",
    "核实",
    "审查",
    "收集",
    "读取",
    "查看",
    "比对",
    "追踪",
    "查询",
    "审计",
    "对账",
    "日志",
    "证据",
    "数据",
    "记录",
    "流水",
    "交易",
    "账本",
    "样本",
)
HIGH_RISK_DECISION_KEYWORDS = (
    "evaluate",
    "assess",
    "determine",
    "decide",
    "plan",
    "mitigation",
    "containment",
    "rollback",
    "repair plan",
    "recovery",
    "是否需要",
    "必要性",
    "可行性",
    "评估",
    "判断",
    "决定",
    "方案",
    "止损",
    "止血",
    "回滚",
    "缓解",
    "修复方案",
    "补救",
    "恢复",
    "冻结",
)
INFRA_FAILURE_KEYWORDS = (
    "timed out",
    "timeout",
    "cannot reach required google endpoints",
    "unable to reach",
    "service unavailable",
    "temporarily unavailable",
    "rate limit",
    "too many requests",
    "connection reset",
    "connection refused",
    "network",
    "transport",
    "broken pipe",
    "deadline exceeded",
    "preflight failed",
    "认证",
    "鉴权",
    "超时",
    "限流",
    "网络",
    "连接",
    "不可达",
    "服务不可用",
)
CAPABILITY_FAILURE_KEYWORDS = (
    "unable to complete",
    "cannot complete",
    "can't complete",
    "unable to determine",
    "cannot determine",
    "can't determine",
    "need more context",
    "need more information",
    "not enough context",
    "not enough information",
    "insufficient information",
    "无法完成",
    "无法判断",
    "需要更多信息",
    "信息不足",
)
LOW_QUALITY_OUTPUT_MARKERS = (
    "unable to complete",
    "cannot complete",
    "can't complete",
    "unable to determine",
    "cannot determine",
    "can't determine",
    "need more context",
    "need more information",
    "not enough context",
    "not enough information",
    "insufficient information",
    "无法完成",
    "无法判断",
    "需要更多信息",
    "信息不足",
)
DEFAULT_FLASH_RETRY_BUDGET = 1
MIN_NON_SUMMARY_OUTPUT_CHARS = 48
DEFAULT_ROUTER_RECURSION_LIMIT = 128
DEFAULT_LARGE_MODEL_TIMEOUT = 6000
#DEFAULT_PRO_EXECUTION_TIMEOUT = 45
DEFAULT_PRO_EXECUTION_TIMEOUT = 6000
#DEFAULT_FLASH_EXECUTION_TIMEOUT = 30
DEFAULT_FLASH_EXECUTION_TIMEOUT = 6000
DEFAULT_PRO_FINALIZER_TIMEOUT = 6000
DEFAULT_FLASH_FINALIZER_TIMEOUT = 6000
DEFAULT_PRO_MODEL = "google-gemini-cli/gemini-3-pro-preview"
DEFAULT_FLASH_MODEL = "google-gemini-cli/gemini-3-flash-preview"
DEFAULT_PLANNER_MODEL = DEFAULT_PRO_MODEL
DEFAULT_JUDGE_MODEL = DEFAULT_FLASH_MODEL
ROUTER_PLANNER_TASK_CHAR_LIMIT_ENV_VAR = "ROUTER_PLANNER_TASK_CHAR_LIMIT"
ROUTER_PLANNER_MAX_OUTPUT_TOKENS_ENV_VAR = "ROUTER_PLANNER_MAX_OUTPUT_TOKENS"
ROUTER_JUDGE_CONTEXT_CHAR_LIMIT_ENV_VAR = "ROUTER_JUDGE_CONTEXT_CHAR_LIMIT"
ROUTER_EXECUTOR_CONTEXT_CHAR_LIMIT_ENV_VAR = "ROUTER_EXECUTOR_CONTEXT_CHAR_LIMIT"
ROUTER_METADATA_OUTPUT_CHAR_LIMIT_ENV_VAR = "ROUTER_METADATA_OUTPUT_CHAR_LIMIT"
ROUTER_FINALIZER_CONTEXT_CHAR_LIMIT_ENV_VAR = "ROUTER_FINALIZER_CONTEXT_CHAR_LIMIT"
DEFAULT_PLANNER_TASK_CHAR_LIMIT = 6000
DEFAULT_PLANNER_MAX_OUTPUT_TOKENS = 4096
DEFAULT_JUDGE_CONTEXT_CHAR_LIMIT = 3000
DEFAULT_EXECUTOR_CONTEXT_CHAR_LIMIT = 8000
DEFAULT_METADATA_OUTPUT_CHAR_LIMIT = 6000
DEFAULT_FINALIZER_CONTEXT_CHAR_LIMIT = 12000
GEMINI_PREFLIGHT_RESULTS: Dict[str, str] = {}
GEMINI_NETWORK_PREFLIGHT_RESULT: str | None = None
TOKEN_USAGE_RUN_ID: contextvars.ContextVar[str] = contextvars.ContextVar("TOKEN_USAGE_RUN_ID", default="")
TOKEN_USAGE_LOCK = threading.RLock()
TOKEN_USAGE_RECORDS_BY_RUN: Dict[str, List["TokenUsageRecord"]] = {}
TOKEN_USAGE_ACTIVE_RUN_IDS: set[str] = set()


class PlannedSubtask(TypedDict):
    id: str
    desc: str
    depends_on: List[str]
    dependency_reason: str


class ComplexityScores(TypedDict):
    reasoning_depth: int
    code_change_scope: int
    ambiguity: int
    risk: int
    io_heaviness: int


class ComplexityAssessment(TypedDict):
    scores: ComplexityScores
    complexity_score: int
    suggested_route: Literal["PRO", "FLASH"]
    final_route: Literal["PRO", "FLASH"]
    confidence: float
    reason: str
    judge_source: str

class FlashReviewResult(TypedDict):
    decision: Literal["record", "retry", "escalate"]
    failure_type: Literal["none", "infra_transient", "capability_quality", "unknown"]
    reason: str
class ModelInvocationResult(TypedDict):
    success: bool
    output: str
    model_name: str
    used_provider_fallback: bool
    failure_type: Literal["none", "infra_transient", "capability_quality", "unknown"]
    error_text: str
    attempt_log: List[str]


class TextGenerationResult(TypedDict):
    text: str
    usage_metadata: Dict[str, int]
    provider: str
    model_name: str
    usage_source: str


class TokenUsageRecord(TypedDict):
    run_id: str
    call_index: int
    label: str
    provider: str
    model_name: str
    usage_source: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cached_tokens: int
    candidate_tokens: int
    thought_tokens: int
    tool_tokens: int
    prompt_chars: int
    output_chars: int


class TokenUsageSummary(TypedDict):
    calls: int
    calls_with_usage: int
    calls_without_usage: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cached_tokens: int
    candidate_tokens: int
    thought_tokens: int
    tool_tokens: int
    by_model: Dict[str, Dict[str, int]]
    by_provider: Dict[str, Dict[str, int]]


class ModelInvocationState(TypedDict):
    primary_model: str
    candidates: List[str]
    candidate_index: int
    current_model: str
    prompt: str
    timeout: int
    num_predict: int
    temperature: float
    label: str
    log: List[str]
    errors: List[str]
    result: ModelInvocationResult
    status: str


class FinalizerOutcome(TypedDict):
    route: Literal["FLASH", "PRO", "DETERMINISTIC"]
    model_name: str
    status: str
    used_provider_fallback: bool
    reason: str
    attempt_log: List[str]


class Subtask(TypedDict):
    id: str
    desc: str
    depends_on: List[str]
    dependency_reason: str
    model: Literal["PRO", "FLASH"]
    assessment: ComplexityAssessment


class JudgedSubtask(TypedDict):
    index: int
    subtask: Subtask
    error: str


class StepResult(TypedDict):
    step: int
    subtask_id: str
    depends_on: List[str]
    planned_route: Literal["PRO", "FLASH"]
    route: Literal["PRO", "FLASH"]
    model_name: str
    desc: str
    output: str
    status: str
    attempt_count: int
    retry_count: int
    escalated_from_flash: bool
    used_provider_fallback: bool
    flash_review: FlashReviewResult
    attempt_log: List[str]


class RouterState(TypedDict):
    run_id: str
    task: str
    planner_model: str
    judge_model: str
    pro_model: str
    flash_model: str
    pro_fallback_models: List[str]
    flash_fallback_models: List[str]
    flash_retry_budget: int
    planned_subtasks: List[PlannedSubtask]
    planner_raw_text: str
    planner_error: str
    dependency_raw_text: str
    dependency_error: str
    dependency_issues: List[str]
    dependency_confidence: float
    planner_warmup_attempt: int
    judge_warmup_done: bool
    subtasks: List[Subtask]
    judge_index: int
    judge_desc: str
    judge_results: Annotated[Dict[int, JudgedSubtask], operator.or_]
    execution_index: int
    execution_subtask: Dict[str, Any]
    execution_results: Annotated[Dict[int, StepResult], operator.or_]
    execution_context_results: List[StepResult]
    current_step: int
    active_subtask: Dict[str, Any]
    active_route: str
    active_model_name: str
    active_output: str
    active_last_error: str
    active_attempt_count: int
    active_retry_count: int
    active_escalated_from_flash: bool
    active_used_provider_fallback: bool
    active_flash_review: FlashReviewResult
    active_attempt_log: List[str]
    active_invocation_result: ModelInvocationResult
    results: Annotated[List[StepResult], operator.add]
    history: Annotated[List[str], operator.add]
    errors: Annotated[List[str], operator.add]
    status: str
    final_report: str
    finalizer_outcome: FinalizerOutcome
    finalizer_attempt_log: List[str]
    finalizer_error: str
    finalizer_flash_reason: str
    finalizer_invocation_result: ModelInvocationResult
    token_usage: List[TokenUsageRecord]
    token_usage_summary: TokenUsageSummary


def resolve_model(explicit_value: str | None, env_name: str, fallback: str) -> str:
    if explicit_value and explicit_value.strip():
        return explicit_value.strip()
    env_value = os.environ.get(env_name, "").strip()
    if env_value:
        return env_value
    global_model = os.environ.get(ROUTER_MODEL_ENV_VAR, "").strip()
    return global_model or fallback


def resolve_execution_model(explicit_value: str | None, env_name: str, fallback: str) -> str:
    selected = resolve_model(explicit_value, env_name, fallback)
    uses_default = (
        not (explicit_value and explicit_value.strip())
        and not os.environ.get(env_name, "").strip()
    )
    if uses_default and any(hint in selected.lower() for hint in (":26b", ":31b", ":70b")):
        print(
            f"[Execution Model] ⚠️ Using {selected} - large model may be slow, "
            f"consider setting {env_name} explicitly"
        )
    return selected


def resolve_non_negative_int(explicit_value: int | None, env_name: str, fallback: int) -> int:
    if explicit_value is not None:
        return max(0, explicit_value)
    env_value = os.environ.get(env_name, "").strip()
    if not env_value:
        return fallback
    try:
        parsed = int(env_value)
    except ValueError:
        return fallback
    return max(0, parsed)


def resolve_positive_int(explicit_value: int | None, env_name: str, fallback: int) -> int:
    if explicit_value is not None:
        return max(1, explicit_value)
    env_value = os.environ.get(env_name, "").strip()
    if not env_value:
        return fallback
    try:
        parsed = int(env_value)
    except ValueError:
        return fallback
    return max(1, parsed)


def resolve_optional_positive_int(explicit_value: int | None, env_name: str) -> int | None:
    if explicit_value is not None:
        return max(1, explicit_value)
    env_value = os.environ.get(env_name, "").strip()
    if not env_value:
        return None
    try:
        parsed = int(env_value)
    except ValueError:
        return None
    return max(1, parsed)


def resolve_bool(env_name: str, fallback: bool = False) -> bool:
    env_value = os.environ.get(env_name, "").strip().lower()
    if not env_value:
        return fallback
    return env_value in {"1", "true", "yes", "on", "debug"}


def router_debug_enabled() -> bool:
    return resolve_bool("ROUTER_DEBUG")


def resolve_model_list(explicit_values: List[str] | None, env_name: str) -> List[str]:
    raw_values = explicit_values
    if raw_values is None:
        env_value = os.environ.get(env_name, "").strip()
        raw_values = env_value.split(",") if env_value else []
    resolved: List[str] = []
    for value in raw_values:
        candidate = str(value).strip()
        if candidate and candidate not in resolved:
            resolved.append(candidate)
    return resolved


def compact_text(text: str, limit: int = 160) -> str:
    one_line = " ".join(text.strip().split())
    if len(one_line) <= limit:
        return one_line
    return one_line[: limit - 3] + "..."


def compact_text_middle(text: str, limit: int) -> str:
    one_line = " ".join(text.strip().split())
    if len(one_line) <= limit:
        return one_line
    if limit <= 3:
        return one_line[:limit]
    marker = " ... "
    available = limit - len(marker)
    if available <= 0:
        return one_line[:limit]
    head_size = max(1, available // 2)
    tail_size = max(1, available - head_size)
    return f"{one_line[:head_size].rstrip()}{marker}{one_line[-tail_size:].lstrip()}"


PLANNER_RELEVANT_TASK_KEYWORDS = (
    "must",
    "should",
    "need",
    "needs",
    "required",
    "requirement",
    "constraint",
    "deliverable",
    "output",
    "format",
    "table",
    "summary",
    "report",
    "brief",
    "compare",
    "analy",
    "debug",
    "diagnos",
    "fix",
    "implement",
    "investig",
    "trace",
    "optimiz",
    "refactor",
    "rewrite",
    "migrate",
    "design",
    "component",
    "provider",
    "model",
    "file",
    "service",
    "region",
    "backend",
    "risk",
    "incident",
    "rollback",
    "validation",
    "test",
    "evidence",
    "citation",
    "version",
    "metric",
    "limit",
    "budget",
)
PLANNER_CONSTRAINT_KEYWORDS = (
    "must",
    "should",
    "required",
    "requirement",
    "constraint",
    "preserve",
    "do not",
    "avoid",
    "without",
    "risk",
    "rollback",
    "security",
    "pci",
    "budget",
    "deadline",
    "slo",
    "sla",
    "必须",
    "需要",
    "要求",
    "约束",
    "保留",
    "不要",
    "避免",
    "风险",
    "回滚",
    "安全",
    "预算",
)
PLANNER_DELIVERABLE_KEYWORDS = (
    "deliverable",
    "output",
    "return",
    "write",
    "summary",
    "report",
    "brief",
    "table",
    "format",
    "final",
    "include",
    "artifact",
    "产出",
    "输出",
    "返回",
    "总结",
    "报告",
    "简报",
    "表格",
    "格式",
    "最终",
    "包含",
)
PLANNER_EVIDENCE_KEYWORDS = (
    "evidence",
    "metric",
    "metrics",
    "version",
    "versions",
    "hard limit",
    "limit",
    "citation",
    "citations",
    "file",
    "files",
    "command",
    "commands",
    "test",
    "tests",
    "validation",
    "verify",
    "logs",
    "traces",
    "数据",
    "证据",
    "指标",
    "版本",
    "限制",
    "引用",
    "文件",
    "命令",
    "测试",
    "验证",
    "日志",
)
PLANNER_DECOMPOSITION_HINT_KEYWORDS = (
    "each",
    "per",
    "independent",
    "component",
    "components",
    "provider",
    "providers",
    "model",
    "models",
    "region",
    "regions",
    "backend",
    "backends",
    "service",
    "services",
    "technical area",
    "technical areas",
    "entity",
    "entities",
    "每个",
    "分别",
    "独立",
    "组件",
    "提供商",
    "模型",
    "区域",
    "后端",
    "服务",
    "技术领域",
)
PLANNER_ENTITY_LIST_PATTERNS = (
    r"\b(?:across|between|among|covering|including)\s+([^.;\n]+)",
    r"\b(?:components?|services?|providers?|models?|regions?|backends?|technical areas?|entities)\s*[:=]\s*([^.;\n]+)",
    r"\bone\s+per\s+([^.;\n]+)",
)
PLANNER_ENTITY_STOPWORDS = {
    "a",
    "an",
    "analyze",
    "and",
    "avoid",
    "brief",
    "do",
    "each",
    "final",
    "goal",
    "if",
    "include",
    "including",
    "investigate",
    "must",
    "one",
    "output",
    "preserve",
    "required",
    "return",
    "role",
    "rules",
    "should",
    "summary",
    "task",
    "technical",
    "the",
    "this",
    "with",
}


def split_planner_task_segments(task: str) -> List[str]:
    segments: List[str] = []
    for line in task.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        parts = re.split(r"(?<=[.!?])\s+", stripped)
        for part in parts:
            normalized = " ".join(part.strip().split())
            if normalized:
                segments.append(normalized)
    return segments


def is_planner_relevant_task_segment(segment: str) -> bool:
    stripped = segment.strip()
    if not stripped:
        return False
    lowered = stripped.lower()
    if contains_any(lowered, PLANNER_RELEVANT_TASK_KEYWORDS):
        return True
    if re.search(r"^([-*+]|\d+[.)]|[A-Za-z][.)])\s+", stripped):
        return True
    if "`" in stripped:
        return True
    return bool(re.search(r"\b[A-Z][A-Za-z0-9_.:/-]{2,}\b", stripped))


def compact_planner_relevant_segment(segment: str, limit: int) -> str:
    return compact_text_middle(segment, limit)


def compact_planner_task(task: str, limit: int) -> str:
    one_line = " ".join(task.strip().split())
    if len(one_line) <= limit:
        return one_line
    if limit < 240:
        return compact_text_middle(one_line, limit)

    marker = f"[planner input compacted from {len(one_line)} chars]"
    remaining = limit - len(marker) - 2
    if remaining < 160:
        return compact_text_middle(one_line, limit)

    head_budget = min(max(240, remaining // 4), remaining // 2)
    tail_budget = min(max(200, remaining // 5), remaining - head_budget)
    head = one_line[:head_budget].rstrip()
    tail = one_line[-tail_budget:].lstrip()
    middle_budget = remaining - len(head) - len(tail)

    selected: List[str] = []
    used = 0
    if middle_budget > 80:
        for segment in split_planner_task_segments(task):
            if not is_planner_relevant_task_segment(segment):
                continue
            if segment in head or segment in tail:
                continue
            spacing = 1 if selected else 0
            available = middle_budget - used - spacing
            if available < 60:
                break
            compacted_segment = compact_planner_relevant_segment(segment, min(220, available))
            selected.append(compacted_segment)
            used += len(compacted_segment) + spacing

    middle = " ".join(selected)
    compacted = " ".join(part for part in (head, marker, middle, tail) if part)
    if len(compacted) <= limit:
        return compacted
    return compact_text_middle(compacted, limit)


def append_unique_planner_item(items: List[str], value: str, max_items: int, item_limit: int) -> None:
    normalized = " ".join(value.strip().strip("`'\"-:;,.()[]{}").split())
    if not normalized:
        return
    if len(normalized) < 2 or normalized.isdigit():
        return
    if normalized.lower() in PLANNER_ENTITY_STOPWORDS:
        return
    compacted = compact_text_middle(normalized, item_limit)
    existing = {item.lower() for item in items}
    if compacted.lower() in existing:
        return
    items.append(compacted)
    if len(items) > max_items:
        del items[max_items:]


def split_planner_entity_list(text: str) -> List[str]:
    normalized = re.sub(r"\b(?:and|or)\b", ",", text, flags=re.IGNORECASE)
    normalized = normalized.replace("/", ",")
    entities: List[str] = []
    for raw_part in re.split(r"[,;|]", normalized):
        part = " ".join(raw_part.strip().strip("`'\"-:;,.()[]{}").split())
        part = re.sub(r"^(?:the|a|an)\s+", "", part, flags=re.IGNORECASE)
        if not part:
            continue
        if len(part.split()) > 6:
            continue
        entities.append(part)
    return entities


def extract_planner_entities(segments: List[str], max_items: int = 24) -> List[str]:
    entities: List[str] = []
    for segment in segments:
        for pattern in PLANNER_ENTITY_LIST_PATTERNS:
            for match in re.finditer(pattern, segment, flags=re.IGNORECASE):
                for entity in split_planner_entity_list(match.group(1)):
                    append_unique_planner_item(entities, entity, max_items, 80)

        for code_match in re.finditer(r"`([^`]{2,120})`", segment):
            append_unique_planner_item(entities, code_match.group(1), max_items, 80)

        for path_match in re.finditer(
            r"\b(?:[\w.-]+/)+[\w./-]+|\b[\w.-]+\.(?:py|js|ts|tsx|json|ya?ml|md|sql|go|rs|java|sh|tf)\b",
            segment,
        ):
            append_unique_planner_item(entities, path_match.group(0), max_items, 80)

        for token_match in re.finditer(r"\b[A-Z][A-Za-z0-9]*(?:[-_./:][A-Za-z0-9]+)*\b|\b[a-z]+(?:-[a-z0-9]+)+\b", segment):
            append_unique_planner_item(entities, token_match.group(0), max_items, 80)

        if len(entities) >= max_items:
            break
    return entities


def collect_planner_segments(
    segments: List[str],
    keywords: tuple[str, ...],
    *,
    max_items: int,
    item_limit: int = 180,
) -> List[str]:
    collected: List[str] = []
    for segment in segments:
        lowered = segment.lower()
        if contains_any(lowered, keywords):
            append_unique_planner_item(collected, segment, max_items, item_limit)
        if len(collected) >= max_items:
            break
    return collected


def serialize_planner_manifest(manifest: Dict[str, Any]) -> str:
    return json.dumps(manifest, ensure_ascii=False, indent=2)


def build_planner_manifest_payload(
    task: str,
    source_brief_budget: int,
    *,
    max_entities: int = 24,
    max_constraints: int = 10,
    max_deliverables: int = 8,
    max_evidence: int = 8,
    max_decomposition_hints: int = 8,
) -> Dict[str, Any]:
    one_line = " ".join(task.strip().split())
    segments = split_planner_task_segments(task)
    objective = segments[0] if segments else one_line
    return {
        "original_chars": len(one_line),
        "objective": compact_text_middle(objective, 420),
        "entities": extract_planner_entities(segments, max_items=max_entities),
        "constraints": collect_planner_segments(
            segments,
            PLANNER_CONSTRAINT_KEYWORDS,
            max_items=max_constraints,
        ),
        "deliverables": collect_planner_segments(
            segments,
            PLANNER_DELIVERABLE_KEYWORDS,
            max_items=max_deliverables,
        ),
        "evidence_requirements": collect_planner_segments(
            segments,
            PLANNER_EVIDENCE_KEYWORDS,
            max_items=max_evidence,
        ),
        "decomposition_hints": collect_planner_segments(
            segments,
            PLANNER_DECOMPOSITION_HINT_KEYWORDS,
            max_items=max_decomposition_hints,
        ),
        "source_brief": compact_planner_task(task, source_brief_budget),
    }


def build_planner_context_manifest(task: str, limit: int) -> str:
    one_line = " ".join(task.strip().split())
    effective_limit = max(240, limit)
    source_brief_budget = max(80, min(2000, effective_limit // 3))
    manifest = build_planner_manifest_payload(task, source_brief_budget)
    serialized = serialize_planner_manifest(manifest)
    if len(serialized) <= effective_limit:
        return serialized

    for item_count in (8, 4, 2, 1, 0):
        source_budget = max(40, min(source_brief_budget, effective_limit // 5))
        manifest = build_planner_manifest_payload(
            task,
            source_budget,
            max_entities=max(4, item_count * 2),
            max_constraints=item_count,
            max_deliverables=item_count,
            max_evidence=item_count,
            max_decomposition_hints=item_count,
        )
        serialized = serialize_planner_manifest(manifest)
        if len(serialized) <= effective_limit:
            return serialized

    minimal_manifest = {
        "original_chars": len(one_line),
        "objective": compact_text_middle(one_line, max(40, effective_limit // 4)),
        "entities": [],
        "constraints": [],
        "deliverables": [],
        "evidence_requirements": [],
        "decomposition_hints": [],
        "source_brief": compact_text_middle(one_line, max(40, effective_limit // 4)),
    }
    serialized = serialize_planner_manifest(minimal_manifest)
    if len(serialized) <= effective_limit:
        return serialized
    return json.dumps(
        {"source_brief": compact_text_middle(one_line, max(1, effective_limit - 24))},
        ensure_ascii=False,
        separators=(",", ":"),
    )


def resolve_context_char_limit(env_name: str, fallback: int, task: str = "", subtask_desc: str = "") -> int:
    if os.environ.get(env_name, "").strip():
        return resolve_positive_int(None, env_name, fallback)
    if task and is_high_risk_context(task, subtask_desc):
        return fallback * 2
    return fallback


def tokenize_context_text(text: str) -> set[str]:
    return {
        token.lower()
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{2,}", text)
    }


def prioritize_items_for_context(items: List[str], text: str, max_items: int) -> List[str]:
    if max_items <= 0:
        return []
    text_lower = text.lower()
    text_tokens = tokenize_context_text(text)
    relevant: List[str] = []
    remainder: List[str] = []
    for item in items:
        item_lower = item.lower()
        item_tokens = tokenize_context_text(item)
        if item_lower in text_lower or (item_tokens and item_tokens & text_tokens):
            relevant.append(item)
        else:
            remainder.append(item)
    return (relevant + remainder)[:max_items]


def matched_context_keywords(text: str, keywords: tuple[str, ...], max_items: int = 12) -> List[str]:
    lowered = text.lower()
    matched: List[str] = []
    for keyword in keywords:
        if keyword in lowered and keyword not in matched:
            matched.append(keyword)
        if len(matched) >= max_items:
            break
    return matched


def serialize_context_payload(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def build_task_context_payload(
    task: str,
    subtask_desc: str = "",
    *,
    source_brief_budget: int,
    max_entities: int = 24,
    max_constraints: int = 10,
    max_deliverables: int = 8,
    max_evidence: int = 8,
    max_decomposition_hints: int = 8,
) -> Dict[str, Any]:
    manifest = build_planner_manifest_payload(
        task,
        source_brief_budget,
        max_entities=max(max_entities, 24),
        max_constraints=max_constraints,
        max_deliverables=max_deliverables,
        max_evidence=max_evidence,
        max_decomposition_hints=max_decomposition_hints,
    )
    context_text = f"{task}\n{subtask_desc}"
    payload: Dict[str, Any] = {
        "original_chars": manifest["original_chars"],
        "objective": manifest["objective"],
    }
    if subtask_desc:
        payload["subtask"] = compact_text_middle(subtask_desc, 420)
    payload.update(
        {
            "entities": prioritize_items_for_context(
                manifest["entities"],
                subtask_desc or task,
                max_entities,
            ),
            "constraints": manifest["constraints"][:max_constraints],
            "deliverables": manifest["deliverables"][:max_deliverables],
            "evidence_requirements": manifest["evidence_requirements"][:max_evidence],
            "decomposition_hints": manifest["decomposition_hints"][:max_decomposition_hints],
            "risk_context": {
                "high_risk": is_high_risk_context(task, subtask_desc),
                "matched_keywords": matched_context_keywords(context_text, HIGH_RISK_CONTEXT_KEYWORDS),
            },
            "source_brief": manifest["source_brief"],
        }
    )
    return payload


def build_task_context_pack_json(task: str, subtask_desc: str, limit: int) -> str:
    effective_limit = max(240, limit)
    source_brief_budget = max(80, min(2000, effective_limit // 3))
    for item_count in (12, 8, 4, 2, 1):
        payload = build_task_context_payload(
            task,
            subtask_desc,
            source_brief_budget=source_brief_budget,
            max_entities=max(4, item_count * 2),
            max_constraints=item_count,
            max_deliverables=item_count,
            max_evidence=item_count,
            max_decomposition_hints=item_count,
        )
        serialized = serialize_context_payload(payload)
        if len(serialized) <= effective_limit:
            return serialized
        source_brief_budget = max(40, source_brief_budget // 2)
    return serialize_context_payload(
        build_task_context_payload(
            task,
            subtask_desc,
            source_brief_budget=max(40, effective_limit // 8),
            max_entities=2,
            max_constraints=1,
            max_deliverables=1,
            max_evidence=1,
            max_decomposition_hints=1,
        )
    )


def build_judge_context_pack_json(task: str, subtask_desc: str) -> str:
    limit = resolve_context_char_limit(
        ROUTER_JUDGE_CONTEXT_CHAR_LIMIT_ENV_VAR,
        DEFAULT_JUDGE_CONTEXT_CHAR_LIMIT,
        task,
        subtask_desc,
    )
    return build_task_context_pack_json(task, subtask_desc, limit)


def compact_step_result_for_context(result: StepResult, output_limit: int) -> Dict[str, Any]:
    return {
        "step": result["step"],
        "subtask_id": result.get("subtask_id", ""),
        "depends_on": list(result.get("depends_on", [])),
        "planned_route": result["planned_route"],
        "actual_route": result["route"],
        "model_name": result["model_name"],
        "status": result["status"],
        "desc": compact_text_middle(result["desc"], 220),
        "output_excerpt": compact_text_middle(result["output"], output_limit) if output_limit > 0 else "",
        "attempt_count": result["attempt_count"],
        "retry_count": result["retry_count"],
        "escalated_from_flash": result["escalated_from_flash"],
        "used_provider_fallback": result["used_provider_fallback"],
    }


def build_executor_context_payload(
    state: RouterState,
    route: Literal["PRO", "FLASH"],
    *,
    source_brief_budget: int,
    prior_output_limit: int,
    max_prior_results: int,
    item_count: int,
) -> Dict[str, Any]:
    subtask_desc = str(state["active_subtask"].get("desc", "N/A"))
    assessment = state["active_subtask"].get("assessment") or {}
    prior_results = state["results"][-max_prior_results:] if max_prior_results > 0 else []
    payload: Dict[str, Any] = {
        "task_context": build_task_context_payload(
            state["task"],
            subtask_desc,
            source_brief_budget=source_brief_budget,
            max_entities=max(4, item_count * 2),
            max_constraints=item_count,
            max_deliverables=item_count,
            max_evidence=item_count,
            max_decomposition_hints=item_count,
        ),
        "routing": {
            "route": route,
            "score": assessment.get("complexity_score", "N/A"),
            "confidence": assessment.get("confidence", "N/A"),
            "reason": str(assessment.get("reason", "N/A")),
        },
        "dependency_context": {
            "subtask_id": state["active_subtask"].get("id", ""),
            "depends_on": list(state["active_subtask"].get("depends_on", [])),
            "dependency_reason": str(state["active_subtask"].get("dependency_reason", "")),
            "prior_results_are_direct_dependencies": True,
        },
        "prior_results": [
            compact_step_result_for_context(result, prior_output_limit)
            for result in prior_results
        ],
        "response_contract": "Return only the result for the current subtask. No markdown fences.",
    }
    if route == PRO and state["active_escalated_from_flash"]:
        flash_review = state["active_flash_review"]
        payload["escalation"] = {
            "from": FLASH,
            "to": PRO,
            "failure_type": flash_review["failure_type"],
            "retries": state["active_retry_count"],
            "reason": flash_review["reason"],
        }
    return payload


def build_executor_context_pack_json(state: RouterState, route: Literal["PRO", "FLASH"]) -> str:
    subtask_desc = str(state["active_subtask"].get("desc", ""))
    limit = resolve_context_char_limit(
        ROUTER_EXECUTOR_CONTEXT_CHAR_LIMIT_ENV_VAR,
        DEFAULT_EXECUTOR_CONTEXT_CHAR_LIMIT,
        state["task"],
        subtask_desc,
    )
    effective_limit = max(480, limit)
    source_brief_budget = max(120, min(3000, effective_limit // 3))
    max_prior = len(state["results"])
    for item_count, prior_limit, prior_count in (
        (12, 320, max_prior),
        (8, 220, min(max_prior, 8)),
        (4, 140, min(max_prior, 4)),
        (2, 80, min(max_prior, 2)),
        (1, 0, 0),
    ):
        payload = build_executor_context_payload(
            state,
            route,
            source_brief_budget=source_brief_budget,
            prior_output_limit=prior_limit,
            max_prior_results=prior_count,
            item_count=item_count,
        )
        serialized = serialize_context_payload(payload)
        if len(serialized) <= effective_limit:
            return serialized
        source_brief_budget = max(60, source_brief_budget // 2)
    return serialize_context_payload(
        build_executor_context_payload(
            state,
            route,
            source_brief_budget=60,
            prior_output_limit=0,
            max_prior_results=0,
            item_count=1,
        )
    )


def build_metadata_context_pack_json(state: RouterState, result: StepResult, output: str) -> str:
    limit = resolve_context_char_limit(
        ROUTER_METADATA_OUTPUT_CHAR_LIMIT_ENV_VAR,
        DEFAULT_METADATA_OUTPUT_CHAR_LIMIT,
        state["task"],
        result["desc"],
    )
    effective_limit = max(480, limit)
    output_budget = max(120, min(effective_limit // 2, DEFAULT_METADATA_OUTPUT_CHAR_LIMIT))
    for item_count in (8, 4, 2, 1):
        payload = {
            "task_context": build_task_context_payload(
                state["task"],
                result["desc"],
                source_brief_budget=max(80, effective_limit // 5),
                max_entities=max(4, item_count * 2),
                max_constraints=item_count,
                max_deliverables=item_count,
                max_evidence=item_count,
                max_decomposition_hints=item_count,
            ),
            "result": compact_step_result_for_context(result, 0),
            "output_excerpt": compact_text_middle(output, output_budget),
            "extraction_schema": [
                "architectural_decisions",
                "library_or_tool_choices",
                "critical_logic_or_algorithm_details",
                "tradeoffs",
                "verified_results",
            ],
        }
        serialized = serialize_context_payload(payload)
        if len(serialized) <= effective_limit:
            return serialized
        output_budget = max(80, output_budget // 2)
    return serialize_context_payload(
        {
            "task_context": build_task_context_payload(
                state["task"],
                result["desc"],
                source_brief_budget=40,
                max_entities=4,
                max_constraints=1,
                max_deliverables=1,
                max_evidence=1,
                max_decomposition_hints=1,
            ),
            "result": compact_step_result_for_context(result, 0),
            "output_excerpt": compact_text_middle(output, max(80, effective_limit // 4)),
        }
    )


def build_finalizer_context_payload(
    state: RouterState,
    route: Literal["PRO", "FLASH"],
    *,
    source_brief_budget: int,
    result_output_limit: int,
    max_results: int,
    metadata_limit: int,
    item_count: int,
) -> Dict[str, Any]:
    metadata_blocks = [line for line in state["history"] if "TECHNICAL METADATA STEP" in line]
    results = state["results"][-max_results:] if max_results > 0 else []
    return {
        "task_context": build_task_context_payload(
            state["task"],
            "",
            source_brief_budget=source_brief_budget,
            max_entities=max(4, item_count * 2),
            max_constraints=item_count,
            max_deliverables=item_count,
            max_evidence=item_count,
            max_decomposition_hints=item_count,
        ),
        "models": {
            "planner": state["planner_model"],
            "judge": state["judge_model"],
            "finalizer_route": route,
        },
        "technical_metadata": [
            compact_text_middle(block, metadata_limit) for block in metadata_blocks
        ] or ["No technical metadata extracted."],
        "execution_results": [
            compact_step_result_for_context(result, result_output_limit)
            for result in results
        ],
        "required_sections": ["Routing Summary", "Step Outcomes", "Next Action"],
    }


def build_finalizer_context_pack_json(state: RouterState, route: Literal["PRO", "FLASH"]) -> str:
    limit = resolve_context_char_limit(
        ROUTER_FINALIZER_CONTEXT_CHAR_LIMIT_ENV_VAR,
        DEFAULT_FINALIZER_CONTEXT_CHAR_LIMIT,
        state["task"],
        "",
    )
    effective_limit = max(800, limit)
    max_results = len(state["results"])
    source_brief_budget = max(160, min(3000, effective_limit // 4))
    for item_count, result_limit, result_count, metadata_limit in (
        (12, 360, max_results, 900),
        (8, 240, min(max_results, 12), 600),
        (4, 160, min(max_results, 8), 420),
        (2, 80, min(max_results, 4), 240),
        (1, 0, min(max_results, 2), 160),
    ):
        payload = build_finalizer_context_payload(
            state,
            route,
            source_brief_budget=source_brief_budget,
            result_output_limit=result_limit,
            max_results=result_count,
            metadata_limit=metadata_limit,
            item_count=item_count,
        )
        serialized = serialize_context_payload(payload)
        if len(serialized) <= effective_limit:
            return serialized
        source_brief_budget = max(80, source_brief_budget // 2)
    return serialize_context_payload(
        build_finalizer_context_payload(
            state,
            route,
            source_brief_budget=80,
            result_output_limit=0,
            max_results=min(max_results, 1),
            metadata_limit=120,
            item_count=1,
        )
    )


def normalize_model_name(model: str) -> str:
    normalized = model.strip()
    for prefix in ("google-gemini-cli/", "codex/", "ollama/", "claude/"):
        if normalized.startswith(prefix):
            normalized = normalized.split("/", 1)[1]
            break
    return normalized


def is_large_model(model: str) -> bool:
    lowered = normalize_model_name(model).lower()
    return any(hint in lowered for hint in (":20b", ":26b", ":31b", ":32b", ":70b", ":72b"))


def normalize_route(value: Any, default: Literal["PRO", "FLASH"] = PRO) -> Literal["PRO", "FLASH"]:
    candidate = str(value or "").strip().upper()
    if candidate == FLASH:
        return FLASH
    if candidate == PRO:
        return PRO
    return default


def clamp_int(value: Any, minimum: int, maximum: int, default: int = 0) -> int:
    try:
        parsed = int(float(str(value).strip()))
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))


def clamp_float(value: Any, minimum: float, maximum: float, default: float = 0.5) -> float:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)

def is_summary_like_subtask(description: str) -> bool:
    return contains_any(description.lower(), SUMMARY_ROUTE_KEYWORDS)


def is_deferred_execution_subtask(subtask: Subtask) -> bool:
    description = subtask["desc"]
    lowered = description.lower()
    if is_summary_like_subtask(description) and not has_deep_work_hint(description):
        return True
    return contains_any(lowered, DEFERRED_EXECUTION_KEYWORDS)


def has_deep_work_hint(description: str) -> bool:
    return contains_any(description.lower(), DEEP_WORK_HINT_KEYWORDS)


def is_high_risk_context(task: str, description: str) -> bool:
    return contains_any(f"{task.lower()} {description.lower()}", HIGH_RISK_CONTEXT_KEYWORDS)


def is_high_risk_evidence_step(description: str) -> bool:
    return contains_any(description.lower(), HIGH_RISK_EVIDENCE_KEYWORDS)


def is_high_risk_decision_step(description: str) -> bool:
    return contains_any(description.lower(), HIGH_RISK_DECISION_KEYWORDS)


def is_high_risk_core_step(task: str, description: str) -> bool:
    summary_like = is_summary_like_subtask(description)
    deep_work_hint = has_deep_work_hint(description)
    if not is_high_risk_context(task, description):
        return False
    if summary_like and not deep_work_hint:
        return False
    return (
        deep_work_hint
        or is_high_risk_evidence_step(description)
        or is_high_risk_decision_step(description)
    )


def apply_contextual_score_biases(
    task: str,
    description: str,
    scores: ComplexityScores,
) -> ComplexityScores:
    adjusted: ComplexityScores = {
        "reasoning_depth": scores["reasoning_depth"],
        "code_change_scope": scores["code_change_scope"],
        "ambiguity": scores["ambiguity"],
        "risk": scores["risk"],
        "io_heaviness": scores["io_heaviness"],
    }
    if is_high_risk_core_step(task, description):
        adjusted["reasoning_depth"] = max(adjusted["reasoning_depth"], 2)
        adjusted["ambiguity"] = max(adjusted["ambiguity"], 1)
        adjusted["risk"] = max(adjusted["risk"], 2)
        if is_high_risk_evidence_step(description):
            adjusted["io_heaviness"] = min(adjusted["io_heaviness"], 1)
    return adjusted


def build_high_risk_reason(description: str) -> str:
    if is_high_risk_evidence_step(description):
        return (
            "High-risk incident evidence gathering stays on PRO because it is part of triage and diagnosis, not mere IO."
        )
    if is_high_risk_decision_step(description):
        return (
            "High-risk incident stop-loss, rollback, or containment evaluation stays on PRO because it is a consequential decision step."
        )
    return (
        "High-risk incident diagnosis or repair strategy stays on PRO because it requires stronger reasoning and safer judgment."
    )


def empty_flash_review() -> FlashReviewResult:
    return {
        "decision": "record",
        "failure_type": "none",
        "reason": "",
    }


def empty_finalizer_outcome() -> FinalizerOutcome:
    return {
        "route": "DETERMINISTIC",
        "model_name": "",
        "status": "not_started",
        "used_provider_fallback": False,
        "reason": "",
        "attempt_log": [],
    }


def empty_model_invocation_result(primary_model: str = "") -> ModelInvocationResult:
    return {
        "success": False,
        "output": "",
        "model_name": primary_model,
        "used_provider_fallback": False,
        "failure_type": "unknown",
        "error_text": "",
        "attempt_log": [],
    }


def classify_failure_type(error_text: str) -> Literal["infra_transient", "capability_quality", "unknown"]:
    lowered = error_text.lower()
    if contains_any(lowered, INFRA_FAILURE_KEYWORDS):
        return "infra_transient"
    if contains_any(lowered, CAPABILITY_FAILURE_KEYWORDS):
        return "capability_quality"
    return "unknown"


def classify_flash_execution_failure(error_text: str) -> FlashReviewResult:
    detail = compact_text(error_text, 220)
    failure_type = classify_failure_type(error_text)
    if failure_type == "infra_transient":
        return {
            "decision": "retry",
            "failure_type": "infra_transient",
            "reason": f"Transient infrastructure/provider failure during FLASH execution: {detail}",
        }
    if failure_type == "capability_quality":
        return {
            "decision": "escalate",
            "failure_type": "capability_quality",
            "reason": f"FLASH execution indicated the step likely needs a stronger model: {detail}",
        }
    return {
        "decision": "retry",
        "failure_type": "unknown",
        "reason": f"Unknown FLASH execution failure; retry within budget before recording it: {detail}",
    }


def verify_flash_output(
    description: str,
    output: str,
    prior_review: FlashReviewResult,
    retry_count: int,
) -> FlashReviewResult:
    stripped = output.strip()
    if not stripped:
        return {
            "decision": "escalate",
            "failure_type": "capability_quality",
            "reason": "FLASH returned empty output after a nominally successful call.",
        }

    normalized_output = " ".join(stripped.split())
    lowered = normalized_output.lower()
    normalized_desc = " ".join(description.strip().split()).lower()

    if contains_any(lowered, LOW_QUALITY_OUTPUT_MARKERS):
        return {
            "decision": "escalate",
            "failure_type": "capability_quality",
            "reason": "FLASH output explicitly signaled insufficient context or inability to finish the step.",
        }

    if not is_summary_like_subtask(description):
        if lowered == normalized_desc:
            return {
                "decision": "escalate",
                "failure_type": "capability_quality",
                "reason": "FLASH mostly repeated the subtask description instead of executing it.",
            }
        if len(normalized_output) < MIN_NON_SUMMARY_OUTPUT_CHARS:
            return {
                "decision": "escalate",
                "failure_type": "capability_quality",
                "reason": "FLASH output was too short for a non-summary step and likely lacks enough substance.",
            }

    prior_failure_type = prior_review["failure_type"]
    if prior_failure_type != "none" and retry_count > 0:
        return {
            "decision": "record",
            "failure_type": prior_failure_type,
            "reason": (
                f"FLASH succeeded after {retry_count} retr"
                f"{'y' if retry_count == 1 else 'ies'} following {prior_failure_type} issues."
            ),
        }

    return {
        "decision": "record",
        "failure_type": "none",
        "reason": "FLASH output passed heuristic verification.",
    }


def dedupe_model_sequence(primary_model: str, fallback_models: List[str]) -> List[str]:
    sequence: List[str] = []
    for model in [primary_model, *fallback_models]:
        candidate = str(model).strip()
        if candidate and candidate not in sequence:
            sequence.append(candidate)
    return sequence


def route_fallback_models(state: RouterState, route: Literal["PRO", "FLASH"]) -> List[str]:
    return state["pro_fallback_models"] if route == PRO else state["flash_fallback_models"]


MODEL_INVOCATION_GRAPH: Any | None = None


def model_attempt_prepare_node(state: ModelInvocationState) -> Dict[str, Any]:
    candidates = state["candidates"]
    index = state["candidate_index"]
    log = list(state["log"])
    if not candidates or index >= len(candidates):
        result = empty_model_invocation_result(state["primary_model"])
        result["error_text"] = "No provider model candidates were available."
        result["attempt_log"] = log
        return {"result": result, "status": "provider_finished"}

    model_name = candidates[index]
    if index == 0:
        log.append(f"{state['label']} primary model attempt: {model_name}")
    else:
        log.append(f"{state['label']} provider fallback attempt {index}: {model_name}")
    return {
        "current_model": model_name,
        "log": log,
        "status": "provider_attempt_ready",
    }


def model_invoke_node(state: ModelInvocationState) -> Dict[str, Any]:
    if state["status"] == "provider_finished":
        return {}

    log = list(state["log"])
    errors = list(state["errors"])
    model_name = state["current_model"]
    index = state["candidate_index"]
    try:
        output = generate_text(
            model_name,
            state["prompt"],
            timeout=state["timeout"],
            num_predict=state["num_predict"],
            temperature=state["temperature"],
            usage_label=state["label"],
        )
        log.append(f"{state['label']} succeeded with model {model_name}.")
        return {
            "result": {
                "success": True,
                "output": output.strip(),
                "model_name": model_name,
                "used_provider_fallback": index > 0,
                "failure_type": "none",
                "error_text": "",
                "attempt_log": log,
            },
            "log": log,
            "status": "provider_finished",
        }
    except Exception as exc:
        error_text = compact_text(str(exc), 220)
        failure_type = classify_failure_type(error_text)
        errors.append(f"{model_name}: {error_text}")
        log.append(
            f"{state['label']} failed with model {model_name}: {error_text} ({failure_type})"
        )
        is_last_candidate = index == len(state["candidates"]) - 1
        if is_last_candidate or failure_type == "capability_quality":
            if failure_type == "capability_quality" and not is_last_candidate:
                log.append(
                    f"{state['label']} stopped before provider fallback because the failure looked like capability/quality, not infrastructure."
                )
            return {
                "result": {
                    "success": False,
                    "output": "",
                    "model_name": state["primary_model"],
                    "used_provider_fallback": False,
                    "failure_type": failure_type,
                    "error_text": "; ".join(errors),
                    "attempt_log": log,
                },
                "log": log,
                "errors": errors,
                "status": "provider_finished",
            }
        return {
            "candidate_index": index + 1,
            "log": log,
            "errors": errors,
            "status": "provider_retry",
        }


def route_after_model_invoke(state: ModelInvocationState) -> str:
    if state["status"] == "provider_finished":
        return END
    return "model_attempt_prepare"


def build_model_invocation_graph():
    workflow = StateGraph(ModelInvocationState)
    workflow.add_node("model_attempt_prepare", model_attempt_prepare_node)
    workflow.add_node("model_invoke", model_invoke_node)
    workflow.add_edge(START, "model_attempt_prepare")
    workflow.add_edge("model_attempt_prepare", "model_invoke")
    workflow.add_conditional_edges("model_invoke", route_after_model_invoke)
    return workflow.compile()


def get_model_invocation_graph():
    global MODEL_INVOCATION_GRAPH
    if MODEL_INVOCATION_GRAPH is None:
        MODEL_INVOCATION_GRAPH = build_model_invocation_graph()
    return MODEL_INVOCATION_GRAPH


def invoke_with_provider_fallback(
    primary_model: str,
    fallback_models: List[str],
    prompt: str,
    *,
    timeout: int,
    num_predict: int,
    temperature: float,
    label: str,
    attempt_log: List[str] | None = None,
) -> ModelInvocationResult:
    candidates = dedupe_model_sequence(primary_model, fallback_models)
    initial_state: ModelInvocationState = {
        "primary_model": primary_model,
        "candidates": candidates,
        "candidate_index": 0,
        "current_model": "",
        "prompt": prompt,
        "timeout": timeout,
        "num_predict": num_predict,
        "temperature": temperature,
        "label": label,
        "log": list(attempt_log or []),
        "errors": [],
        "result": empty_model_invocation_result(primary_model),
        "status": "provider_created",
    }
    final_state = get_model_invocation_graph().invoke(
        initial_state,
        config={"recursion_limit": max(8, len(candidates) * 3 + 4)},
    )
    return final_state["result"]


def find_communication_clause(text: str) -> tuple[int, str] | None:
    patterns = (
        r"(?:并|并且|再|然后|最后)\s*((?:把[^。；;]{0,120}?)?(?:整理|准备|撰写|输出|生成|写|发送|同步|汇总|总结|概述|汇报)[^。；;]*)",
        r"(?:and|then|finally)\s+((?:prepare|write|draft|generate|send|summarize|report|share)[^.;;]*)",
        r"((?:整理|准备|撰写|输出|生成|写|发送|同步|汇总|总结|概述|汇报)[^。；;]*?(?:状态更新|影响说明|风险说明|行动摘要|摘要|总结|报告|简报|说明))",
        r"((?:prepare|write|draft|generate|send|summarize|report|share)[^.;;]*?(?:status update|impact note|risk note|action summary|summary|report))",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        clause = match.group(1).strip(" ，,；;。:：")
        if clause and is_summary_like_subtask(clause):
            return match.start(1), clause
    return None


def extract_communication_audience_markers(text: str) -> List[str]:
    lowered = text.lower()
    markers: List[str] = []
    for keyword in COMMUNICATION_AUDIENCE_KEYWORDS:
        if keyword.lower() in lowered:
            markers.append(keyword)
    return markers


def default_communication_subtask(task: str) -> PlannedSubtask:
    lowered = task.lower()
    if "值班" in task:
        return {"desc": "整理一份发给值班同事的简短中文行动摘要。"}
    if "产品经理" in task:
        return {"desc": "整理一段给产品经理的简短中文影响说明。"}
    if "运营" in task:
        return {"desc": "整理一份发给运营同事的简短中文影响说明。"}
    if "项目负责人" in task or "负责人" in task:
        return {"desc": "整理一段给项目负责人的简短中文风险说明。"}
    if "团队" in task:
        return {"desc": "整理一段给团队的简短中文状态更新。"}
    if "on-call" in lowered:
        return {"desc": "Prepare a concise action summary for the on-call engineer."}
    if "manager" in lowered or "pm" in lowered:
        return {"desc": "Prepare a concise impact note for the manager."}
    return {"desc": "整理面向相关方的简短中文总结或状态更新。"}


def split_mixed_planned_subtask(description: str) -> List[PlannedSubtask]:
    match = find_communication_clause(description)
    if not match or not has_deep_work_hint(description):
        return [{"desc": description}]

    clause_start, communication_clause = match
    base_desc = description[:clause_start].strip(" ，,；;。")
    if not base_desc or base_desc == communication_clause:
        return [{"desc": description}]
    return [{"desc": base_desc}, {"desc": communication_clause}]


def ensure_communication_subtask(task: str, planned_subtasks: List[PlannedSubtask]) -> List[PlannedSubtask]:
    expanded: List[PlannedSubtask] = []
    for subtask in planned_subtasks:
        expanded.extend(split_mixed_planned_subtask(subtask["desc"]))

    match = find_communication_clause(task)
    summary_indices = [
        index for index, subtask in enumerate(expanded) if is_summary_like_subtask(subtask["desc"])
    ]
    if summary_indices:
        if match:
            task_clause = match[1]
            audience_markers = extract_communication_audience_markers(task_clause)
            if audience_markers and not any(
                any(marker.lower() in expanded[index]["desc"].lower() for marker in audience_markers)
                for index in summary_indices
            ):
                expanded[summary_indices[-1]] = {"desc": task_clause}
        return expanded
    if match:
        expanded.append({"desc": match[1]})
        return expanded

    if is_summary_like_subtask(task):
        expanded.append(default_communication_subtask(task))
    return expanded


def score_complexity(scores: ComplexityScores) -> int:
    return (
        scores["reasoning_depth"]
        + scores["code_change_scope"]
        + scores["ambiguity"]
        + scores["risk"]
    )


def decide_route(
    task: str,
    description: str,
    scores: ComplexityScores,
    suggested_route: Literal["PRO", "FLASH"],
    confidence: float,
) -> Literal["PRO", "FLASH"]:
    complexity_score = score_complexity(scores)
    summary_like = is_summary_like_subtask(description)
    deep_work_hint = has_deep_work_hint(description)
    high_risk_core_step = is_high_risk_core_step(task, description)

    if summary_like and not deep_work_hint:
        return FLASH
    if summary_like and not deep_work_hint and scores["io_heaviness"] >= 1 and scores["code_change_scope"] <= 1 and scores["risk"] <= 1:
        return FLASH
    if high_risk_core_step:
        return PRO
    if deep_work_hint and not summary_like:
        return PRO

    if confidence < LOW_CONFIDENCE_THRESHOLD:
        return PRO
    if complexity_score >= PRO_COMPLEXITY_THRESHOLD:
        return PRO
    if (
        scores["reasoning_depth"] >= 2
        or scores["code_change_scope"] >= 2
        or scores["risk"] >= 2
    ):
        return PRO
    if complexity_score <= FLASH_COMPLEXITY_THRESHOLD and scores["io_heaviness"] >= 1:
        return FLASH
    if complexity_score <= 3 and scores["io_heaviness"] == 2 and confidence >= 0.7:
        return FLASH
    if suggested_route == FLASH and complexity_score <= 3 and confidence >= 0.8:
        return FLASH
    if suggested_route == PRO and confidence >= 0.6:
        return PRO
    return PRO


def is_gemini_model(model: str) -> bool:
    raw = model.strip().lower()
    if raw.startswith(("codex/", "ollama/", "claude/")):
        return False
    if raw.startswith("google-gemini-cli/"):
        return True
    normalized = normalize_model_name(model)
    return normalized in {"auto", "pro", "flash", "flash-lite"} or normalized.startswith("gemini-")


def is_codex_model(model: str) -> bool:
    raw = model.strip().lower()
    if raw.startswith(("google-gemini-cli/", "ollama/", "claude/")):
        return False
    normalized = normalize_model_name(model).lower()
    if raw.startswith("codex/"):
        return True
    if ":" in normalized:
        return False
    return (
        normalized.startswith("gpt-")
        or normalized.startswith("chatgpt-")
        or re.match(r"^o\d(?:[-.].*)?$", normalized) is not None
    )


def is_claude_model(model: str) -> bool:
    raw = model.strip().lower()
    if raw.startswith(("google-gemini-cli/", "codex/", "ollama/")):
        return False
    if raw.startswith("claude/"):
        return True
    normalized = normalize_model_name(model).lower()
    return normalized.startswith("claude-")


def model_transport_name(model: str) -> str:
    if is_claude_model(model):
        return "claude_cli"
    if is_gemini_model(model):
        return "gemini_cli"
    if is_codex_model(model):
        return "codex_cli"
    return "ollama_http"


def langsmith_provider_name(model: str) -> str:
    if is_claude_model(model):
        return "anthropic"
    if is_gemini_model(model):
        return "google_genai"
    if is_codex_model(model):
        return "codex"
    return "ollama"


def build_text_generation_result(
    text: str,
    usage_metadata: Dict[str, int] | None,
    provider: str,
    model_name: str,
    usage_source: str = "unavailable",
) -> TextGenerationResult:
    return {
        "text": text,
        "usage_metadata": usage_metadata or {},
        "provider": provider,
        "model_name": model_name,
        "usage_source": usage_source if usage_metadata else "unavailable",
    }


def coerce_non_negative_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        parsed = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None
    if parsed < 0:
        return None
    return parsed


def normalize_usage_metadata(
    *,
    input_tokens: Any = None,
    output_tokens: Any = None,
    total_tokens: Any = None,
    cached_tokens: Any = None,
    thought_tokens: Any = None,
    tool_tokens: Any = None,
    candidates_tokens: Any = None,
) -> Dict[str, int]:
    input_count = coerce_non_negative_int(input_tokens)
    output_count = coerce_non_negative_int(output_tokens)
    candidates_count = coerce_non_negative_int(candidates_tokens)
    thought_count = coerce_non_negative_int(thought_tokens)
    total_count = coerce_non_negative_int(total_tokens)
    cached_count = coerce_non_negative_int(cached_tokens)
    tool_count = coerce_non_negative_int(tool_tokens)
    if output_count is None and (candidates_count is not None or thought_count is not None):
        output_count = (candidates_count or 0) + (thought_count or 0)
    if total_count is None and input_count is not None and output_count is not None:
        total_count = input_count + output_count + (tool_count or 0)
    if output_count is None and total_count is not None and input_count is not None:
        output_count = max(0, total_count - input_count)
    if input_count is None and total_count is not None and output_count is not None:
        input_count = max(0, total_count - output_count)

    usage: Dict[str, int] = {}
    if input_count is not None:
        usage["input_tokens"] = input_count
    if output_count is not None:
        usage["output_tokens"] = output_count
    if total_count is not None:
        usage["total_tokens"] = total_count
    if cached_count is not None:
        usage["cached_tokens"] = cached_count
    if thought_count is not None:
        usage["thought_tokens"] = thought_count
    if tool_count is not None:
        usage["tool_tokens"] = tool_count
    if candidates_count is not None:
        usage["candidate_tokens"] = candidates_count
    return usage


def extract_ollama_usage_metadata(data: Dict[str, Any]) -> Dict[str, int]:
    return normalize_usage_metadata(
        input_tokens=data.get("prompt_eval_count"),
        output_tokens=data.get("eval_count"),
    )


def extract_gemini_cli_stats_usage_metadata(payload: Any) -> Dict[str, int]:
    if not isinstance(payload, dict):
        return {}
    stats = payload.get("stats")
    if not isinstance(stats, dict):
        return {}
    models = stats.get("models")
    if not isinstance(models, dict):
        return {}

    totals = {
        "prompt": 0,
        "candidates": 0,
        "total": 0,
        "cached": 0,
        "thoughts": 0,
        "tool": 0,
    }
    saw_tokens = False
    for model_stats in models.values():
        if not isinstance(model_stats, dict):
            continue
        tokens = model_stats.get("tokens")
        if not isinstance(tokens, dict):
            continue
        token_values: Dict[str, int] = {}
        for key in totals:
            value = coerce_non_negative_int(tokens.get(key))
            if value is not None:
                token_values[key] = value
        if not token_values:
            continue
        saw_tokens = True
        for key, value in token_values.items():
            totals[key] += value

    if not saw_tokens:
        return {}
    return normalize_usage_metadata(
        input_tokens=totals["prompt"],
        candidates_tokens=totals["candidates"],
        total_tokens=totals["total"],
        cached_tokens=totals["cached"],
        thought_tokens=totals["thoughts"],
        tool_tokens=totals["tool"],
    )


def first_present_value(data: Dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in data:
            return data[key]
    return None


def extract_usage_metadata_from_mapping(data: Dict[str, Any]) -> Dict[str, int]:
    return normalize_usage_metadata(
        input_tokens=first_present_value(
            data,
            (
                "input_tokens",
                "prompt_tokens",
                "prompt_token_count",
                "promptTokenCount",
            ),
        ),
        output_tokens=first_present_value(
            data,
            (
                "output_tokens",
                "completion_tokens",
                "completion_token_count",
                "completionTokenCount",
            ),
        ),
        candidates_tokens=first_present_value(
            data,
            (
                "candidate_tokens",
                "candidates_tokens",
                "candidates_token_count",
                "candidatesTokenCount",
            ),
        ),
        total_tokens=first_present_value(
            data,
            (
                "total_tokens",
                "total_token_count",
                "totalTokenCount",
            ),
        ),
        cached_tokens=first_present_value(
            data,
            (
                "cached_tokens",
                "cached_token_count",
                "cachedContentTokenCount",
                "cached_content_token_count",
            ),
        ),
        thought_tokens=first_present_value(
            data,
            (
                "thought_tokens",
                "thoughts_token_count",
                "thoughtsTokenCount",
                "thinking_tokens",
            ),
        ),
        tool_tokens=first_present_value(
            data,
            (
                "tool_tokens",
                "tool_token_count",
                "toolUsePromptTokenCount",
                "tool_use_prompt_token_count",
            ),
        ),
    )


def extract_nested_gemini_usage_metadata(payload: Any) -> Dict[str, int]:
    candidates: List[Dict[str, Any]] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for usage_key in ("usage_metadata", "usageMetadata", "usage"):
                usage_value = value.get(usage_key)
                if isinstance(usage_value, dict):
                    candidates.append(usage_value)
            if extract_usage_metadata_from_mapping(value):
                candidates.append(value)
            for nested_value in value.values():
                visit(nested_value)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(payload)
    for candidate in candidates:
        usage = extract_usage_metadata_from_mapping(candidate)
        if usage:
            return usage
    return {}


def extract_gemini_usage_metadata_with_source(payload: Any) -> tuple[Dict[str, int], str]:
    cli_stats_usage = extract_gemini_cli_stats_usage_metadata(payload)
    if cli_stats_usage:
        return cli_stats_usage, "gemini_cli_stats"
    nested_usage = extract_nested_gemini_usage_metadata(payload)
    if nested_usage:
        return nested_usage, "usage_metadata"
    return {}, "unavailable"


def extract_gemini_usage_metadata(payload: Any) -> Dict[str, int]:
    usage, _ = extract_gemini_usage_metadata_with_source(payload)
    return usage


def annotate_langsmith_model_run(
    *,
    model: str,
    provider: str,
    num_predict: int,
    temperature: float,
) -> None:
    if _langsmith is None or not langsmith_tracing_configured():
        return
    get_current_run_tree = getattr(_langsmith, "get_current_run_tree", None)
    if get_current_run_tree is None:
        return
    try:
        run_tree = get_current_run_tree()
    except Exception:
        return
    if run_tree is None:
        return
    try:
        run_tree.add_metadata(
            {
                "ls_provider": provider,
                "ls_model_name": normalize_model_name(model),
                "ls_temperature": temperature,
                "ls_max_tokens": num_predict,
                "ls_invocation_params": {
                    "model": normalize_model_name(model),
                    "raw_model": model,
                    "provider": provider,
                },
            }
        )
    except Exception:
        return


def resolve_bool_value(value: str | None, fallback: bool = False) -> bool:
    if value is None or not str(value).strip():
        return fallback
    return str(value).strip().lower() in {"1", "true", "yes", "on", "debug"}


def langsmith_tracing_requested() -> bool:
    router_value = os.environ.get(ROUTER_LANGSMITH_ENABLED_ENV_VAR)
    if router_value is not None and router_value.strip():
        return resolve_bool_value(router_value)
    for env_name in ("LANGSMITH_TRACING", "LANGCHAIN_TRACING_V2"):
        env_value = os.environ.get(env_name)
        if env_value is not None and env_value.strip():
            return resolve_bool_value(env_value)
    return False


def langsmith_tracing_forced_disabled() -> bool:
    router_value = os.environ.get(ROUTER_LANGSMITH_ENABLED_ENV_VAR)
    return router_value is not None and router_value.strip() and not resolve_bool_value(router_value)


def langsmith_api_key_configured() -> bool:
    return bool(
        os.environ.get("LANGSMITH_API_KEY", "").strip()
        or os.environ.get("LANGCHAIN_API_KEY", "").strip()
    )


def langsmith_tracing_configured() -> bool:
    return _langsmith is not None and langsmith_tracing_requested() and langsmith_api_key_configured()


def langsmith_project_name() -> str:
    return (
        os.environ.get(ROUTER_LANGSMITH_PROJECT_ENV_VAR, "").strip()
        or os.environ.get("LANGSMITH_PROJECT", "").strip()
        or "super-router"
    )


def parse_langsmith_tags() -> List[str]:
    tags = ["super-router", "langgraph"]
    raw_tags = os.environ.get(ROUTER_LANGSMITH_TAGS_ENV_VAR, "")
    for raw_tag in raw_tags.split(","):
        tag = raw_tag.strip()
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def build_langsmith_metadata(state: RouterState) -> Dict[str, Any]:
    return {
        "component": "super-router",
        "run_id": state["run_id"],
        "planner_model": state["planner_model"],
        "judge_model": state["judge_model"],
        "pro_model": state["pro_model"],
        "flash_model": state["flash_model"],
        "pro_fallback_count": len(state["pro_fallback_models"]),
        "flash_fallback_count": len(state["flash_fallback_models"]),
        "flash_retry_budget": state["flash_retry_budget"],
        "task_chars": len(state["task"]),
    }


def process_langsmith_model_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    if resolve_bool("ROUTER_LANGSMITH_HIDE_INPUTS"):
        return {}
    args = inputs.get("args")
    if not isinstance(args, (list, tuple)):
        args = []
    model = str(inputs.get("model") or (args[0] if len(args) > 0 else ""))
    prompt = str(inputs.get("prompt") or (args[1] if len(args) > 1 else ""))
    processed: Dict[str, Any] = {
        "model": model,
        "provider": langsmith_provider_name(model),
        "transport": model_transport_name(model),
        "timeout": inputs.get("timeout"),
        "num_predict": inputs.get("num_predict"),
        "temperature": inputs.get("temperature"),
        "usage_label": inputs.get("usage_label", ""),
        "prompt_chars": len(prompt),
    }
    if resolve_bool("ROUTER_LANGSMITH_TRACE_PROMPTS"):
        processed["prompt_preview"] = compact_text(prompt, 1000)
    return processed


def process_langsmith_model_outputs(output: Any) -> Dict[str, Any]:
    output_text = str(output.get("text", "")) if isinstance(output, dict) else str(output or "")
    usage_metadata = (
        output.get("usage_metadata", {})
        if isinstance(output, dict) and isinstance(output.get("usage_metadata"), dict)
        else {}
    )
    usage_source = str(output.get("usage_source", "")) if isinstance(output, dict) else ""
    if resolve_bool("ROUTER_LANGSMITH_HIDE_OUTPUTS"):
        processed_hidden: Dict[str, Any] = {}
        if usage_metadata:
            processed_hidden["usage_metadata"] = usage_metadata
        if usage_source:
            processed_hidden["usage_source"] = usage_source
        return processed_hidden
    processed: Dict[str, Any] = {"output_chars": len(output_text)}
    if usage_metadata:
        processed["usage_metadata"] = usage_metadata
    if usage_source:
        processed["usage_source"] = usage_source
    if resolve_bool("ROUTER_LANGSMITH_TRACE_OUTPUTS"):
        processed["output_preview"] = compact_text(output_text, 1000)
    return processed


def create_langsmith_client() -> Any | None:
    if _langsmith is None:
        return None
    client_cls = getattr(_langsmith, "Client", None)
    if client_cls is None:
        return None
    kwargs: Dict[str, Any] = {}
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip() or os.environ.get("LANGCHAIN_API_KEY", "").strip()
    endpoint = os.environ.get("LANGSMITH_ENDPOINT", "").strip() or os.environ.get("LANGCHAIN_ENDPOINT", "").strip()
    workspace_id = os.environ.get("LANGSMITH_WORKSPACE_ID", "").strip()
    if api_key:
        kwargs["api_key"] = api_key
    if endpoint:
        kwargs["api_url"] = endpoint
    if workspace_id:
        kwargs["workspace_id"] = workspace_id
    if resolve_bool("ROUTER_LANGSMITH_HIDE_INPUTS"):
        kwargs["hide_inputs"] = True
    if resolve_bool("ROUTER_LANGSMITH_HIDE_OUTPUTS"):
        kwargs["hide_outputs"] = True
    try:
        return client_cls(**kwargs)
    except Exception as exc:
        print(f"[LangSmith] Failed to initialize client; continuing without telemetry: {compact_text(str(exc), 220)}")
        return None


@contextlib.contextmanager
def langsmith_tracing_context(state: RouterState) -> Iterator[None]:
    if langsmith_tracing_forced_disabled():
        tracing_context = getattr(_langsmith, "tracing_context", None) if _langsmith is not None else None
        if tracing_context is None:
            yield
        else:
            with tracing_context(enabled=False):
                yield
        return
    if not langsmith_tracing_requested():
        yield
        return
    if _langsmith is None:
        print("[LangSmith] Telemetry requested but the langsmith package is unavailable; continuing without tracing.")
        yield
        return
    tracing_context = getattr(_langsmith, "tracing_context", None)
    if tracing_context is None:
        print("[LangSmith] Telemetry requested but tracing_context is unavailable; continuing without tracing.")
        yield
        return
    if not langsmith_api_key_configured():
        print("[LangSmith] Telemetry requested but LANGSMITH_API_KEY is not set; continuing without tracing.")
        with tracing_context(enabled=False):
            yield
        return

    client = create_langsmith_client()
    context_kwargs: Dict[str, Any] = {
        "enabled": True,
        "project_name": langsmith_project_name(),
        "tags": parse_langsmith_tags(),
        "metadata": build_langsmith_metadata(state),
    }
    if client is not None:
        context_kwargs["client"] = client
    try:
        with tracing_context(**context_kwargs):
            yield
    finally:
        if client is not None and resolve_bool("ROUTER_LANGSMITH_FLUSH", True):
            try:
                client.flush()
            except Exception as exc:
                print(f"[LangSmith] Failed to flush traces: {compact_text(str(exc), 220)}")


def empty_token_usage_summary() -> TokenUsageSummary:
    return {
        "calls": 0,
        "calls_with_usage": 0,
        "calls_without_usage": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cached_tokens": 0,
        "candidate_tokens": 0,
        "thought_tokens": 0,
        "tool_tokens": 0,
        "by_model": {},
        "by_provider": {},
    }


def current_token_usage_run_id() -> str:
    run_id = TOKEN_USAGE_RUN_ID.get("")
    if run_id:
        return run_id
    with TOKEN_USAGE_LOCK:
        if len(TOKEN_USAGE_ACTIVE_RUN_IDS) == 1:
            return next(iter(TOKEN_USAGE_ACTIVE_RUN_IDS))
    return ""


@contextlib.contextmanager
def token_usage_tracking_context(run_id: str) -> Iterator[None]:
    token = TOKEN_USAGE_RUN_ID.set(run_id)
    with TOKEN_USAGE_LOCK:
        TOKEN_USAGE_RECORDS_BY_RUN[run_id] = []
        TOKEN_USAGE_ACTIVE_RUN_IDS.add(run_id)
    try:
        yield
    finally:
        TOKEN_USAGE_RUN_ID.reset(token)
        with TOKEN_USAGE_LOCK:
            TOKEN_USAGE_ACTIVE_RUN_IDS.discard(run_id)


def get_token_usage_records(run_id: str) -> List[TokenUsageRecord]:
    with TOKEN_USAGE_LOCK:
        return list(TOKEN_USAGE_RECORDS_BY_RUN.get(run_id, []))


def resolve_token_usage_ledger_path() -> str:
    return os.path.expanduser(os.environ.get(ROUTER_TOKEN_USAGE_LEDGER_ENV_VAR, "").strip())


def persist_token_usage_ledger(
    records: List[TokenUsageRecord],
    summary: TokenUsageSummary,
    *,
    state: RouterState,
) -> str:
    ledger_path = resolve_token_usage_ledger_path()
    if not ledger_path or not records:
        return ""

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ledger_dir = os.path.dirname(ledger_path)
    if ledger_dir:
        os.makedirs(ledger_dir, exist_ok=True)

    base_event = {
        "event": "token_usage",
        "schema_version": 1,
        "timestamp": timestamp,
        "run_id": state["run_id"],
        "task_chars": len(state["task"]),
        "status": state["status"],
        "planner_model": state["planner_model"],
        "judge_model": state["judge_model"],
        "pro_model": state["pro_model"],
        "flash_model": state["flash_model"],
        "summary": summary,
    }
    with open(ledger_path, "a", encoding="utf-8") as ledger_file:
        for record in records:
            event = dict(base_event)
            event["record"] = record
            ledger_file.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return ledger_path


def metric_value(record: TokenUsageRecord, key: str) -> int:
    return int(record.get(key, 0) or 0)


def add_usage_to_bucket(bucket: Dict[str, int], record: TokenUsageRecord) -> None:
    bucket["calls"] = bucket.get("calls", 0) + 1
    if metric_value(record, "total_tokens") > 0:
        bucket["calls_with_usage"] = bucket.get("calls_with_usage", 0) + 1
    else:
        bucket["calls_without_usage"] = bucket.get("calls_without_usage", 0) + 1
    for key in (
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "cached_tokens",
        "candidate_tokens",
        "thought_tokens",
        "tool_tokens",
    ):
        bucket[key] = bucket.get(key, 0) + metric_value(record, key)


def summarize_token_usage_records(records: List[TokenUsageRecord]) -> TokenUsageSummary:
    summary = empty_token_usage_summary()
    for record in records:
        add_usage_to_bucket(summary, record)
        model_name = record["model_name"] or "unknown"
        provider = record["provider"] or "unknown"
        model_bucket = summary["by_model"].setdefault(model_name, {})
        provider_bucket = summary["by_provider"].setdefault(provider, {})
        add_usage_to_bucket(model_bucket, record)
        add_usage_to_bucket(provider_bucket, record)
    return summary


def format_int(value: int) -> str:
    return f"{value:,}"


def format_token_usage_summary(summary: TokenUsageSummary) -> str:
    if summary["calls"] == 0:
        return "Token Usage Summary\n- Calls: 0 (no provider token usage captured)."
    lines = [
        "Token Usage Summary",
        (
            f"- Calls: {summary['calls']} "
            f"({summary['calls_with_usage']} with token counts, "
            f"{summary['calls_without_usage']} unavailable)"
        ),
        (
            "- Tokens: "
            f"input={format_int(summary['input_tokens'])}, "
            f"output={format_int(summary['output_tokens'])}, "
            f"total={format_int(summary['total_tokens'])}"
        ),
    ]
    extras: List[str] = []
    if summary["cached_tokens"]:
        extras.append(f"cached={format_int(summary['cached_tokens'])}")
    if summary["candidate_tokens"]:
        extras.append(f"candidates={format_int(summary['candidate_tokens'])}")
    if summary["thought_tokens"]:
        extras.append(f"thoughts={format_int(summary['thought_tokens'])}")
    if summary["tool_tokens"]:
        extras.append(f"tool={format_int(summary['tool_tokens'])}")
    if extras:
        lines.append("- Extra tokens: " + ", ".join(extras))
    if summary["by_model"]:
        lines.append("- By model:")
        for model_name, bucket in sorted(summary["by_model"].items()):
            lines.append(
                f"  - {model_name}: calls={bucket.get('calls', 0)}, "
                f"total={format_int(bucket.get('total_tokens', 0))}, "
                f"input={format_int(bucket.get('input_tokens', 0))}, "
                f"output={format_int(bucket.get('output_tokens', 0))}"
            )
    return "\n".join(lines)


def record_token_usage(
    result: TextGenerationResult,
    *,
    label: str,
    prompt: str,
) -> None:
    run_id = current_token_usage_run_id()
    if not run_id:
        return
    usage = result.get("usage_metadata", {})
    if not isinstance(usage, dict):
        usage = {}
    output_text = str(result.get("text", ""))
    record: TokenUsageRecord = {
        "run_id": run_id,
        "call_index": 0,
        "label": label,
        "provider": str(result.get("provider", "")),
        "model_name": str(result.get("model_name", "")),
        "usage_source": str(result.get("usage_source", "unavailable")),
        "input_tokens": int(usage.get("input_tokens", 0) or 0),
        "output_tokens": int(usage.get("output_tokens", 0) or 0),
        "total_tokens": int(usage.get("total_tokens", 0) or 0),
        "cached_tokens": int(usage.get("cached_tokens", 0) or 0),
        "candidate_tokens": int(usage.get("candidate_tokens", 0) or 0),
        "thought_tokens": int(usage.get("thought_tokens", 0) or 0),
        "tool_tokens": int(usage.get("tool_tokens", 0) or 0),
        "prompt_chars": len(prompt),
        "output_chars": len(output_text),
    }
    with TOKEN_USAGE_LOCK:
        records = TOKEN_USAGE_RECORDS_BY_RUN.setdefault(run_id, [])
        record["call_index"] = len(records) + 1
        records.append(record)


def has_proxy_config() -> bool:
    return any(
        os.environ.get(name, "").strip()
        for name in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy")
    )


def env_flag_enabled(name: str, default: bool = False) -> bool:
    raw_value = os.environ.get(name, "").strip().lower()
    if not raw_value:
        return default
    return raw_value in {"1", "true", "yes", "on"}


def openclaw_auth_profiles_path() -> str:
    agent_dir = os.environ.get("OPENCLAW_AGENT_DIR", "").strip()
    if agent_dir:
        return os.path.join(os.path.expanduser(agent_dir), "auth-profiles.json")
    openclaw_home = os.path.expanduser(os.environ.get("OPENCLAW_HOME", "~/.openclaw"))
    return os.path.join(openclaw_home, "agents", "main", "agent", "auth-profiles.json")


def detect_openclaw_gemini_auth_issue(now_ms: int | None = None) -> str:
    if env_flag_enabled("ROUTER_IGNORE_OPENCLAW_GEMINI_AUTH", False):
        return ""
    auth_path = openclaw_auth_profiles_path()
    if not os.path.exists(auth_path):
        return ""
    try:
        with open(auth_path, "r", encoding="utf-8") as auth_file:
            auth_data = json.load(auth_file)
    except (OSError, json.JSONDecodeError):
        return ""
    profiles = auth_data.get("profiles")
    if not isinstance(profiles, dict):
        return ""
    gemini_profiles = [
        profile
        for profile in profiles.values()
        if isinstance(profile, dict) and profile.get("provider") == "google-gemini-cli"
    ]
    if not gemini_profiles:
        return ""

    now = now_ms if now_ms is not None else int(time.time() * 1000)
    for profile in gemini_profiles:
        expires = profile.get("expires") or profile.get("expiresAt")
        try:
            expires_ms = int(expires)
        except (TypeError, ValueError):
            continue
        if expires_ms <= now + 60_000:
            email = str(profile.get("email") or "configured account")
            return (
                "OpenClaw Gemini OAuth profile for "
                f"{email} is expired. Run `openclaw models auth login --provider google-gemini-cli`."
            )
    return ""


def ensure_gemini_network_ready(timeout: float = 3.0) -> None:
    global GEMINI_NETWORK_PREFLIGHT_RESULT

    if GEMINI_NETWORK_PREFLIGHT_RESULT is not None:
        if GEMINI_NETWORK_PREFLIGHT_RESULT:
            raise RuntimeError(GEMINI_NETWORK_PREFLIGHT_RESULT)
        return

    if has_proxy_config():
        GEMINI_NETWORK_PREFLIGHT_RESULT = ""
        return

    failures: List[str] = []
    for host in ("oauth2.googleapis.com", "generativelanguage.googleapis.com"):
        try:
            with socket.create_connection((host, 443), timeout=timeout):
                pass
        except OSError as exc:
            reason = "timed out" if isinstance(exc, TimeoutError) else compact_text(str(exc), 120)
            failures.append(f"{host}:443 ({reason})")

    if failures:
        GEMINI_NETWORK_PREFLIGHT_RESULT = (
            "Cannot reach required Google endpoints for Gemini CLI: "
            + ", ".join(failures)
            + ". Gemini cannot authenticate or execute until Google network access works or a proxy is configured."
        )
        raise RuntimeError(GEMINI_NETWORK_PREFLIGHT_RESULT)

    GEMINI_NETWORK_PREFLIGHT_RESULT = ""


def ollama_generate_with_usage(
    model: str,
    prompt: str,
    *,
    timeout: int = 60,
    num_predict: int = 400,
    temperature: float = 0.0,
) -> TextGenerationResult:
    # Increase num_predict for large models (e.g. gemma4:26b) to allow full JSON responses
    # Large models need more tokens for structured output like JSON
    if "gemma4" in model.lower() and num_predict < 204800:
        num_predict = 204800
        print(f"[ollama_generate] Auto-increased num_predict to {num_predict} for large model {model}")
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
        },
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Unable to reach Ollama at {OLLAMA_URL}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError(f"Ollama timed out after {timeout}s") from exc

    if router_debug_enabled():
        print(f"\n[DEBUG ollama_generate] Model: {model}, Timeout: {timeout}s, num_predict: {num_predict}")
        print(f"  Raw data keys: {list(data.keys())}")
        print(f"  'response' field length: {len(str(data.get('response', '')))} chars")
        print(f"  'response' first 500 chars: {str(data.get('response', ''))[:500]}")
        if len(str(data.get('response', ''))) > 500:
            print(f"  'response' last 200 chars: {str(data.get('response', ''))[-200:]}")
        print(f"  Metadata: eval_count={data.get('eval_count')}, prompt_eval_count={data.get('prompt_eval_count')}")
        print(f"  done={data.get('done')}, done_reason={data.get('done_reason')}")
        print(f"  Text after strip: {len(str(data.get('response', '')).strip())} chars")
        print(f"  ---\n")
    
    text = str(data.get("response", "")).strip()
    if not text:
        raise RuntimeError(f"Ollama returned an empty response for model {model}")
    return build_text_generation_result(
        text,
        extract_ollama_usage_metadata(data),
        "ollama",
        model,
        "ollama_generate",
    )


def ollama_generate(
    model: str,
    prompt: str,
    *,
    timeout: int = 60,
    num_predict: int = 400,
    temperature: float = 0.0,
) -> str:
    return ollama_generate_with_usage(
        model,
        prompt,
        timeout=timeout,
        num_predict=num_predict,
        temperature=temperature,
    )["text"]


def default_gemini_system_settings_path() -> str:
    if sys.platform == "darwin":
        return "/Library/Application Support/GeminiCli/settings.json"
    if os.name == "nt":
        return r"C:\ProgramData\gemini-cli\settings.json"
    return "/etc/gemini-cli/settings.json"


def load_gemini_system_settings() -> Dict[str, Any]:
    settings_path = os.environ.get(GEMINI_SYSTEM_SETTINGS_ENV_VAR, "").strip()
    if not settings_path:
        settings_path = default_gemini_system_settings_path()
    if not settings_path or not os.path.exists(settings_path):
        return {}
    try:
        with open(settings_path, "r", encoding="utf-8") as settings_file:
            settings = json.load(settings_file)
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(settings, dict):
        return {}
    return settings


def build_gemini_temperature_settings(normalized_model: str, temperature: float) -> Dict[str, Any]:
    settings = copy.deepcopy(load_gemini_system_settings())
    model_configs = settings.get("modelConfigs")
    if not isinstance(model_configs, dict):
        model_configs = {}
        settings["modelConfigs"] = model_configs

    custom_overrides = model_configs.get("customOverrides")
    if not isinstance(custom_overrides, list):
        custom_overrides = []
    else:
        custom_overrides = list(custom_overrides)

    custom_overrides.append(
        {
            "match": {"model": normalized_model},
            "modelConfig": {
                "generateContentConfig": {
                    "temperature": temperature,
                },
            },
        }
    )
    model_configs["customOverrides"] = custom_overrides
    return settings


def invoke_gemini_cli_with_usage(
    model: str,
    prompt: str,
    *,
    timeout: int = 120,
    temperature: float = 0.0,
) -> TextGenerationResult:
    normalized_model = normalize_model_name(model)
    if not GEMINI_CLI_PATH or not os.path.exists(GEMINI_CLI_PATH):
        raise RuntimeError("Gemini CLI executable was not found. Set ROUTER_GEMINI_CLI or install `gemini`.")

    env = dict(os.environ)
    env["NO_COLOR"] = "1"
    env["NO_BROWSER"] = "true"
    # Force inject ripgrep + common tool paths (fixes "Ripgrep is not available" warning)
    extra_paths = ["/opt/homebrew/bin", "/usr/local/bin"]
    current_path = env.get("PATH", "")
    path_parts = [p for p in extra_paths if p not in current_path.split(":")]
    if path_parts:
        env["PATH"] = ":".join(path_parts + [current_path]) if current_path else ":".join(path_parts)
    command = [
        GEMINI_CLI_PATH,
        "-m",
        normalized_model,
        "-p",
        prompt,
        "-o",
        "json",
        "-y",
#        "-e",
#        GEMINI_EXTENSION_NAME,
    ]
    try:
        with tempfile.TemporaryDirectory(prefix="router-gemini-") as settings_dir:
            settings_path = os.path.join(settings_dir, "settings.json")
            with open(settings_path, "w", encoding="utf-8") as settings_file:
                json.dump(build_gemini_temperature_settings(normalized_model, temperature), settings_file)
            env[GEMINI_SYSTEM_SETTINGS_ENV_VAR] = settings_path

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                check=False,
                stdin=subprocess.DEVNULL,
            )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Gemini CLI timed out after {timeout}s") from exc

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    # Filter known benign Gemini CLI tool warnings (YOLO mode, ripgrep fallback, etc.)
    # These are non-fatal and should not cause the call to fail
    BENIGN_WARNINGS = [
        "YOLO mode is enabled",
        "All tool calls will be automatically approved",
        "Ripgrep is not available",
        "Falling back to GrepTool",
        "ripgrep",
    ]

    def _strip_benign_warnings(text: str) -> str:
        if not text:
            return ""
        lines = text.splitlines()
        filtered = [line for line in lines if not any(w.lower() in line.lower() for w in BENIGN_WARNINGS)]
        return "\n".join(filtered).strip()

    stdout = _strip_benign_warnings(stdout)
    stderr = _strip_benign_warnings(stderr)
    payload_text = stdout or stderr

    parsed_payload: Dict[str, Any] | None = None
    if payload_text:
        try:
            candidate = json.loads(payload_text)
        except json.JSONDecodeError:
            candidate = None
        if isinstance(candidate, dict):
            parsed_payload = candidate

    if result.returncode != 0:
        if parsed_payload and isinstance(parsed_payload.get("error"), dict):
            error_block = parsed_payload["error"]
            error_text = compact_text(
                str(error_block.get("message") or error_block.get("type") or payload_text),
                280,
            )
        else:
            error_text = compact_text(stderr or stdout or f"exit code {result.returncode}", 280)
        # Only raise if we still have a real error after filtering warnings
        if error_text and not any(w.lower() in error_text.lower() for w in BENIGN_WARNINGS):
            raise RuntimeError(f"Gemini CLI failed for model {normalized_model}: {error_text}")

    if parsed_payload and isinstance(parsed_payload.get("error"), dict):
        error_block = parsed_payload["error"]
        error_text = compact_text(
            str(error_block.get("message") or error_block.get("type") or payload_text),
            280,
        )
        if error_text and not any(w.lower() in error_text.lower() for w in BENIGN_WARNINGS):
            raise RuntimeError(f"Gemini CLI returned an error for model {normalized_model}: {error_text}")

    usage_metadata, usage_source = extract_gemini_usage_metadata_with_source(parsed_payload or {})
    if parsed_payload and str(parsed_payload.get("response", "")).strip():
        return build_text_generation_result(
            str(parsed_payload["response"]).strip(),
            usage_metadata,
            "google_genai",
            normalized_model,
            usage_source,
        )

    if not payload_text:
        raise RuntimeError(f"Gemini CLI returned an empty response for model {normalized_model}")
    return build_text_generation_result(
        payload_text,
        usage_metadata,
        "google_genai",
        normalized_model,
        usage_source,
    )


def invoke_gemini_cli(
    model: str,
    prompt: str,
    *,
    timeout: int = 120,
    temperature: float = 0.0,
) -> str:
    return invoke_gemini_cli_with_usage(
        model,
        prompt,
        timeout=timeout,
        temperature=temperature,
    )["text"]


def ensure_gemini_cli_ready(model: str) -> None:
    normalized_model = normalize_model_name(model)
    cached_error = GEMINI_PREFLIGHT_RESULTS.get(normalized_model)
    if cached_error is not None:
        if cached_error:
            raise RuntimeError(cached_error)
        return

    auth_issue = detect_openclaw_gemini_auth_issue()
    if auth_issue:
        error_text = f"Gemini CLI auth preflight failed: {auth_issue}"
        GEMINI_PREFLIGHT_RESULTS[normalized_model] = error_text
        raise RuntimeError(error_text)

    try:
        ensure_gemini_network_ready()
    except Exception as exc:
        error_text = f"Gemini network preflight failed: {exc}"
        GEMINI_PREFLIGHT_RESULTS[normalized_model] = error_text
        raise RuntimeError(error_text) from exc

    GEMINI_PREFLIGHT_RESULTS[normalized_model] = ""


def gemini_generate(
    model: str,
    prompt: str,
    *,
    timeout: int = 120,
    temperature: float = 0.0,
) -> str:
    return gemini_generate_with_usage(
        model,
        prompt,
        timeout=timeout,
        temperature=temperature,
    )["text"]


def gemini_generate_with_usage(
    model: str,
    prompt: str,
    *,
    timeout: int = 120,
    temperature: float = 0.0,
) -> TextGenerationResult:
    ensure_gemini_cli_ready(model)
    return invoke_gemini_cli_with_usage(model, prompt, timeout=timeout, temperature=temperature)


def codex_generate_with_usage(
    model: str,
    prompt: str,
    *,
    timeout: int = 60,
    num_predict: int = 400,
    temperature: float = 0.0,
) -> TextGenerationResult:
    del num_predict, temperature

    normalized_model = normalize_model_name(model)
    if os.path.sep in CODEX_CLI_PATH and not os.path.exists(CODEX_CLI_PATH):
        raise RuntimeError("Codex CLI executable was not found. Set ROUTER_CODEX_CLI or install `codex`.")

    env = dict(os.environ)
    env["NO_COLOR"] = "1"
    sandbox = os.environ.get(ROUTER_CODEX_SANDBOX_ENV_VAR, "read-only").strip() or "read-only"
    command = [
        CODEX_CLI_PATH,
        "exec",
        "-m",
        normalized_model,
        "--sandbox",
        sandbox,
        "--skip-git-repo-check",
        "--color",
        "never",
        "--ephemeral",
    ]
    codex_cwd = os.environ.get(ROUTER_CODEX_CWD_ENV_VAR, "").strip()
    if codex_cwd:
        command.extend(["--cd", codex_cwd])

    try:
        with tempfile.TemporaryDirectory(prefix="router-codex-") as output_dir:
            output_path = os.path.join(output_dir, "last-message.txt")
            command.extend(["--output-last-message", output_path, "-"])
            result = subprocess.run(
                command,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                check=False,
            )
            output_text = ""
            if os.path.exists(output_path):
                with open(output_path, "r", encoding="utf-8") as output_file:
                    output_text = output_file.read().strip()
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Codex CLI timed out after {timeout}s") from exc

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    if result.returncode != 0:
        error_text = compact_text(stderr or stdout or f"exit code {result.returncode}", 280)
        raise RuntimeError(f"Codex CLI failed for model {normalized_model}: {error_text}")

    text = output_text or stdout
    if not text.strip():
        raise RuntimeError(f"Codex CLI returned an empty response for model {normalized_model}")
    return build_text_generation_result(
        text.strip(),
        {},
        "codex",
        normalized_model,
        "unavailable",
    )


def codex_generate(
    model: str,
    prompt: str,
    *,
    timeout: int = 60,
    num_predict: int = 400,
    temperature: float = 0.0,
) -> str:
    return codex_generate_with_usage(
        model,
        prompt,
        timeout=timeout,
        num_predict=num_predict,
        temperature=temperature,
    )["text"]


def sum_optional_ints(values: List[Any]) -> int | None:
    total = 0
    found = False
    for value in values:
        count = coerce_non_negative_int(value)
        if count is None:
            continue
        total += count
        found = True
    return total if found else None


def extract_claude_usage_metadata(parsed: Dict[str, Any], normalized_model: str) -> Dict[str, int]:
    usage = parsed.get("usage")
    if isinstance(usage, dict):
        cache_creation_tokens = first_present_value(
            usage,
            ("cache_creation_input_tokens", "cacheCreationInputTokens"),
        )
        cache_read_tokens = first_present_value(
            usage,
            ("cache_read_input_tokens", "cacheReadInputTokens"),
        )
        return normalize_usage_metadata(
            input_tokens=first_present_value(usage, ("input_tokens", "inputTokens")),
            output_tokens=first_present_value(usage, ("output_tokens", "outputTokens")),
            total_tokens=first_present_value(usage, ("total_tokens", "totalTokens")),
            cached_tokens=sum_optional_ints([cache_creation_tokens, cache_read_tokens]),
        )

    model_usage = parsed.get("model_usage") or parsed.get("modelUsage")
    if isinstance(model_usage, dict):
        model_entry = model_usage.get(normalized_model)
        entries = (
            [model_entry]
            if isinstance(model_entry, dict)
            else [entry for entry in model_usage.values() if isinstance(entry, dict)]
        )
        if entries:
            input_tokens = sum_optional_ints(
                [first_present_value(entry, ("inputTokens", "input_tokens")) for entry in entries]
            )
            output_tokens = sum_optional_ints(
                [first_present_value(entry, ("outputTokens", "output_tokens")) for entry in entries]
            )
            cache_creation_tokens = sum_optional_ints(
                [
                    first_present_value(
                        entry,
                        ("cacheCreationInputTokens", "cache_creation_input_tokens"),
                    )
                    for entry in entries
                ]
            )
            cache_read_tokens = sum_optional_ints(
                [
                    first_present_value(
                        entry,
                        ("cacheReadInputTokens", "cache_read_input_tokens"),
                    )
                    for entry in entries
                ]
            )
            total_tokens = sum_optional_ints(
                [first_present_value(entry, ("totalTokens", "total_tokens")) for entry in entries]
            )
            return normalize_usage_metadata(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cached_tokens=sum_optional_ints([cache_creation_tokens, cache_read_tokens]),
            )

    cache_creation_tokens = first_present_value(
        parsed,
        ("cache_creation_input_tokens", "cacheCreationInputTokens"),
    )
    cache_read_tokens = first_present_value(
        parsed,
        ("cache_read_input_tokens", "cacheReadInputTokens"),
    )
    return normalize_usage_metadata(
        input_tokens=first_present_value(parsed, ("total_input_tokens", "input_tokens", "inputTokens")),
        output_tokens=first_present_value(parsed, ("total_output_tokens", "output_tokens", "outputTokens")),
        total_tokens=first_present_value(parsed, ("total_tokens", "totalTokens")),
        cached_tokens=sum_optional_ints([cache_creation_tokens, cache_read_tokens]),
    )


def claude_generate_with_usage(
    model: str,
    prompt: str,
    *,
    timeout: int = 120,
    temperature: float = 0.0,
) -> TextGenerationResult:
    del temperature

    normalized_model = normalize_model_name(model)
    if os.path.sep in CLAUDE_CLI_PATH and not os.path.exists(CLAUDE_CLI_PATH):
        raise RuntimeError("Claude CLI executable was not found. Set ROUTER_CLAUDE_CLI or install `claude`.")

    env = dict(os.environ)
    env["NO_COLOR"] = "1"
    command = [CLAUDE_CLI_PATH, "--model", normalized_model, "--output-format", "json", "-p", prompt]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Claude CLI timed out after {timeout}s") from exc

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    if result.returncode != 0:
        error_text = compact_text(stderr or stdout or f"exit code {result.returncode}", 280)
        raise RuntimeError(f"Claude CLI failed for model {normalized_model}: {error_text}")

    try:
        parsed = json.loads(stdout)
    except json.JSONDecodeError as exc:
        error_text = compact_text(stderr or stdout or "no output", 280)
        raise RuntimeError(f"Claude CLI returned non-JSON output for model {normalized_model}: {error_text}") from exc

    if parsed.get("is_error"):
        error_text = compact_text(parsed.get("result") or stderr or "unknown error", 280)
        raise RuntimeError(f"Claude CLI reported error for model {normalized_model}: {error_text}")

    text = parsed.get("result", "")
    if not text.strip():
        raise RuntimeError(f"Claude CLI returned an empty response for model {normalized_model}")

    usage = extract_claude_usage_metadata(parsed, normalized_model)
    return build_text_generation_result(
        text.strip(),
        usage or {},
        "anthropic",
        normalized_model,
        "claude_cli_json" if usage else "unavailable",
    )


def _execute_generate_text_with_usage(
    model: str,
    prompt: str,
    *,
    timeout: int = 60,
    num_predict: int = 400,
    temperature: float = 0.0,
    usage_label: str = "",
) -> TextGenerationResult:
    provider = langsmith_provider_name(model)
    annotate_langsmith_model_run(
        model=model,
        provider=provider,
        num_predict=num_predict,
        temperature=temperature,
    )
    if is_claude_model(model):
        return claude_generate_with_usage(model, prompt, timeout=timeout, temperature=temperature)
    if is_gemini_model(model):
        return gemini_generate_with_usage(model, prompt, timeout=timeout, temperature=temperature)
    if is_codex_model(model):
        return codex_generate_with_usage(
            model,
            prompt,
            timeout=timeout,
            num_predict=num_predict,
            temperature=temperature,
        )
    return ollama_generate_with_usage(
        model,
        prompt,
        timeout=timeout,
        num_predict=num_predict,
        temperature=temperature,
    )


if _langsmith is not None and getattr(_langsmith, "traceable", None) is not None:
    _traced_generate_text = _langsmith.traceable(
        name="Super Router Model Call",
        run_type="llm",
        process_inputs=process_langsmith_model_inputs,
        process_outputs=process_langsmith_model_outputs,
    )(_execute_generate_text_with_usage)
else:
    _traced_generate_text = _execute_generate_text_with_usage


def unwrap_text_generation_result(result: Any) -> str:
    if isinstance(result, dict) and "text" in result:
        return str(result["text"])
    return str(result)


def generate_text(
    model: str,
    prompt: str,
    *,
    timeout: int = 60,
    num_predict: int = 400,
    temperature: float = 0.0,
    usage_label: str = "",
) -> str:
    if langsmith_tracing_configured():
        result = _traced_generate_text(
            model,
            prompt,
            timeout=timeout,
            num_predict=num_predict,
            temperature=temperature,
            usage_label=usage_label,
        )
        if isinstance(result, dict):
            record_token_usage(
                result,
                label=usage_label or normalize_model_name(model),
                prompt=prompt,
            )
        return unwrap_text_generation_result(result)
    result = _execute_generate_text_with_usage(
        model,
        prompt,
        timeout=timeout,
        num_predict=num_predict,
        temperature=temperature,
        usage_label=usage_label,
    )
    record_token_usage(
        result,
        label=usage_label or normalize_model_name(model),
        prompt=prompt,
    )
    return unwrap_text_generation_result(result)


def extract_first_json_array(text: str) -> List[Any]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "[":
            continue
        try:
            parsed, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            return parsed
    raise ValueError("No valid JSON array found in planner output")


def extract_first_json_object(text: str) -> Dict[str, Any]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    raise ValueError("No valid JSON object found in judge output")


def normalize_dependency_id(value: Any, fallback: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        raw = fallback
    normalized = re.sub(r"[^A-Za-z0-9_.:-]+", "_", raw).strip("_")
    return normalized or fallback


def normalize_dependency_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw_items = value
    elif isinstance(value, str):
        stripped = value.strip()
        raw_items = re.split(r"[\s,]+", stripped) if stripped else []
    else:
        raw_items = [value]

    dependencies: List[str] = []
    for item in raw_items:
        dependency_id = normalize_dependency_id(item, "")
        if dependency_id and dependency_id not in dependencies:
            dependencies.append(dependency_id)
    return dependencies


def dependency_reason_from_raw(raw: Any, default: str) -> str:
    if isinstance(raw, dict):
        reason = (
            raw.get("dependency_reason")
            or raw.get("depends_reason")
            or raw.get("reason")
            or raw.get("dependency")
        )
        if reason:
            return compact_text(str(reason), 220)
    return default


def normalize_planned_subtasks(raw_subtasks: List[Any]) -> List[PlannedSubtask]:
    pending: List[Dict[str, Any]] = []
    used_ids: set[str] = set()
    id_aliases: Dict[str, str] = {}

    for item in raw_subtasks:
        if isinstance(item, dict):
            desc = str(item.get("desc") or item.get("description") or item.get("step") or "").strip()
            raw_id = item.get("id") or item.get("step_id") or item.get("name")
            raw_depends_on = item.get("depends_on") or item.get("dependencies") or item.get("requires")
        else:
            desc = str(item).strip()
            raw_id = None
            raw_depends_on = []

        if not desc:
            continue

        fallback_id = f"S{len(pending) + 1}"
        subtask_id = normalize_dependency_id(raw_id, fallback_id)
        if subtask_id in used_ids:
            subtask_id = fallback_id
            suffix = 2
            while subtask_id in used_ids:
                subtask_id = f"{fallback_id}_{suffix}"
                suffix += 1
        used_ids.add(subtask_id)
        if raw_id:
            id_aliases[str(raw_id).strip()] = subtask_id
            id_aliases[normalize_dependency_id(raw_id, subtask_id)] = subtask_id

        pending.append(
            {
                "id": subtask_id,
                "desc": desc,
                "raw_depends_on": raw_depends_on,
                "dependency_reason": dependency_reason_from_raw(
                    item,
                    "Dependency not specified by planner.",
                ),
            }
        )

    normalized: List[PlannedSubtask] = []
    for item in pending:
        dependencies: List[str] = []
        for dependency_id in normalize_dependency_list(item["raw_depends_on"]):
            resolved_dependency_id = id_aliases.get(dependency_id, dependency_id)
            if resolved_dependency_id != item["id"] and resolved_dependency_id not in dependencies:
                dependencies.append(resolved_dependency_id)
        normalized.append(
            {
                "id": item["id"],
                "desc": item["desc"],
                "depends_on": dependencies,
                "dependency_reason": item["dependency_reason"],
            }
        )

    if not normalized:
        raise ValueError("Planner did not return any usable subtasks")
    return normalized


def validate_dependency_graph(subtasks: List[PlannedSubtask]) -> List[PlannedSubtask]:
    ids = [subtask["id"] for subtask in subtasks]
    duplicate_ids = sorted({subtask_id for subtask_id in ids if ids.count(subtask_id) > 1})
    if duplicate_ids:
        raise ValueError(f"Duplicate dependency ids: {', '.join(duplicate_ids)}")

    known_ids = set(ids)
    for subtask in subtasks:
        if not subtask["id"]:
            raise ValueError("Dependency graph contains an empty subtask id")
        missing = [dependency_id for dependency_id in subtask["depends_on"] if dependency_id not in known_ids]
        if missing:
            raise ValueError(
                f"Subtask {subtask['id']} references unknown dependencies: {', '.join(missing)}"
            )
        if subtask["id"] in subtask["depends_on"]:
            raise ValueError(f"Subtask {subtask['id']} depends on itself")

    visiting: set[str] = set()
    visited: set[str] = set()
    by_id = {subtask["id"]: subtask for subtask in subtasks}

    def visit(subtask_id: str, path: List[str]) -> None:
        if subtask_id in visited:
            return
        if subtask_id in visiting:
            cycle = " -> ".join(path + [subtask_id])
            raise ValueError(f"Dependency cycle detected: {cycle}")
        visiting.add(subtask_id)
        for dependency_id in by_id[subtask_id]["depends_on"]:
            visit(dependency_id, path + [subtask_id])
        visiting.remove(subtask_id)
        visited.add(subtask_id)

    for subtask_id in ids:
        visit(subtask_id, [])

    return subtasks


def make_serial_dependency_plan(
    subtasks: List[PlannedSubtask],
    *,
    reason: str = "Conservative serial fallback after invalid dependency judgment.",
) -> List[PlannedSubtask]:
    serial_subtasks: List[PlannedSubtask] = []
    previous_id = ""
    for subtask in subtasks:
        serial_subtasks.append(
            {
                **subtask,
                "depends_on": [previous_id] if previous_id else [],
                "dependency_reason": reason if previous_id else "First serial fallback step has no dependency.",
            }
        )
        previous_id = subtask["id"]
    return serial_subtasks


def normalize_dependency_judgment(
    raw: Dict[str, Any],
    planned_subtasks: List[PlannedSubtask],
) -> tuple[List[PlannedSubtask], float, List[str]]:
    raw_subtasks = raw.get("subtasks") or raw.get("planned_subtasks") or raw.get("plan")
    raw_dependencies = raw.get("dependencies")
    updates: Dict[str, Dict[str, Any]] = {}

    if isinstance(raw_subtasks, list):
        for item in raw_subtasks:
            if not isinstance(item, dict):
                continue
            subtask_id = normalize_dependency_id(
                item.get("id") or item.get("step_id") or item.get("name"),
                "",
            )
            if subtask_id:
                updates[subtask_id] = item

    if isinstance(raw_dependencies, dict):
        for raw_id, raw_depends_on in raw_dependencies.items():
            subtask_id = normalize_dependency_id(raw_id, "")
            if not subtask_id:
                continue
            updates.setdefault(subtask_id, {})["depends_on"] = raw_depends_on

    judged: List[PlannedSubtask] = []
    for planned in planned_subtasks:
        update = updates.get(planned["id"], {})
        dependency_value = planned["depends_on"]
        for key in ("depends_on", "dependencies", "requires"):
            if key in update:
                dependency_value = update[key]
                break
        dependencies = normalize_dependency_list(dependency_value)
        dependencies = [
            dependency_id
            for dependency_id in dependencies
            if dependency_id != planned["id"]
        ]
        judged.append(
            {
                **planned,
                "depends_on": dependencies,
                "dependency_reason": dependency_reason_from_raw(
                    update,
                    planned["dependency_reason"],
                ),
            }
        )

    confidence = clamp_float(raw.get("confidence"), 0.0, 1.0, default=0.5)
    raw_issues = raw.get("issues")
    issues = [
        compact_text(str(issue), 220)
        for issue in raw_issues
        if str(issue).strip()
    ] if isinstance(raw_issues, list) else []
    return judged, confidence, issues


def build_fallback_subtasks(task: str) -> List[PlannedSubtask]:
    lowered = task.lower()
    subtasks: List[Any] = []

    if any(
        keyword in lowered
        for keyword in (
            "analy",
            "debug",
            "fix",
            "refactor",
            "rewrite",
            "implement",
            "design",
            "logic",
            "分析",
            "调试",
            "修复",
            "重构",
            "实现",
            "设计",
            "逻辑",
        )
    ):
        subtasks.append({"desc": f"分析任务中的核心逻辑与高风险部分: {task}"})
        subtasks.append({"desc": f"执行核心实现或修复步骤: {task}"})
    else:
        subtasks.append({"desc": task})

    if any(
        keyword in lowered
        for keyword in (
            "summary",
            "summarize",
            "report",
            "pdf",
            "status",
            "save",
            "document",
            "总结",
            "报告",
            "保存",
            "整理",
        )
    ):
        subtasks.append({"desc": "整理执行结果并生成最终总结或输出。"})

    return normalize_planned_subtasks(subtasks)


def build_planner_prompt(task: str) -> str:
    task_limit = resolve_positive_int(
        None,
        ROUTER_PLANNER_TASK_CHAR_LIMIT_ENV_VAR,
        DEFAULT_PLANNER_TASK_CHAR_LIMIT,
    )
    planner_context = build_planner_context_manifest(task, task_limit)
    original_chars = len(" ".join(task.strip().split()))
    compaction_note = ""
    if len(planner_context) < original_chars:
        compaction_note = (
            f"Planner context manifest compacted from {original_chars} to {len(planner_context)} chars. "
            "Plan from the manifest JSON's objective, entities, constraints, deliverables, evidence requirements, "
            "and decomposition hints; do not copy omitted context into every subtask.\n"
        )
    return (
        "Role: Task decomposition planner.\n"
        "Goal: produce the execution plan only; do not solve the task.\n"
        f"{compaction_note}"
        "Planner context manifest JSON:\n"
        f"{planner_context}\n"
        "Rules:\n"
        "- Split by independent entity/component/file/provider/region/backend/technical area.\n"
        "- Separate investigation/implementation/validation/reporting when mixed.\n"
        "- Preserve deliverables, constraints, and needed evidence.\n"
        "- Use stable ids S1, S2, S3.\n"
        "- depends_on only when earlier outputs/evidence/decisions are required; otherwise [].\n"
        "- No model labels, complexity labels, or scores.\n"
        "Return raw JSON only: [{\"id\":\"S1\",\"desc\":\"atomic subtask\",\"depends_on\":[],"
        "\"dependency_reason\":\"why\"}]\n"
        "JSON Output:"
    )


def build_dependency_judge_prompt(task: str, planned_subtasks: List[PlannedSubtask]) -> str:
    planned_json = json.dumps(planned_subtasks, ensure_ascii=False, indent=2)
    return (
        "Role: Dependency judge for a LangGraph task router.\n"
        "Goal: verify and correct only execution dependencies; do not solve the task and do not score complexity.\n"
        f"Original task:\n{task}\n"
        f"Planner subtasks JSON:\n{planned_json}\n"
        "Rules:\n"
        "- Keep every existing id exactly as provided.\n"
        "- Do not add, remove, merge, split, or rewrite subtasks.\n"
        "- Use depends_on only when the current subtask needs prior outputs, evidence, decisions, or generated artifacts.\n"
        "- Independent investigations, file/provider/region checks, and unrelated evidence collection should have empty depends_on.\n"
        "- Synthesis, comparison, validation-after-implementation, reporting, and final answer steps should depend on the producing subtasks.\n"
        "- If uncertain whether a dependency is required for correctness, include the dependency.\n"
        "- Dependencies may reference only ids from the provided list.\n"
        "Return raw JSON only with keys: subtasks, confidence, issues.\n"
        "Each subtask item must contain: id, depends_on, dependency_reason.\n"
        "JSON Output:"
    )


def judge_dependencies_with_model(
    task: str,
    planned_subtasks: List[PlannedSubtask],
    judge_model: str,
) -> tuple[List[PlannedSubtask], float, List[str], str]:
    default_timeout = DEFAULT_LARGE_MODEL_TIMEOUT if is_large_model(judge_model) else 300
    judge_timeout = int(os.environ.get("ROUTER_JUDGE_TIMEOUT", str(default_timeout)))
    raw_text = generate_text(
        judge_model,
        build_dependency_judge_prompt(task, planned_subtasks),
        timeout=judge_timeout,
        num_predict=4096,
        temperature=0.0,
        usage_label="Dependency judge",
    )
    if router_debug_enabled():
        print("\n[DEBUG Dependency Judge Output]")
        print(f"  Model: {judge_model}")
        print(f"  Raw text length: {len(raw_text)} chars")
        print(f"  First 400 chars: {raw_text[:400]}")
        if len(raw_text) > 400:
            print(f"  Last 200 chars: {raw_text[-200:]}")
        print(f"  Contains '{{': { '{' in raw_text }, Contains '}}': {'}' in raw_text }")
        print("  ---\n")
    judged_subtasks, confidence, issues = normalize_dependency_judgment(
        extract_first_json_object(raw_text),
        planned_subtasks,
    )
    return judged_subtasks, confidence, issues, raw_text


def build_judge_prompt(task: str, subtask_desc: str) -> str:
    context_pack = build_judge_context_pack_json(task, subtask_desc)
    return (
        "Role: Complexity judge for model routing.\n"
        f"Task context JSON:\n{context_pack}\n"
        f"Subtask: {subtask_desc}\n"
        "Judge the subtask itself, but use the task context JSON to understand domain risk. Only avoid inheriting the overall-task complexity when the subtask is purely a summary, report, or status update.\n"
        "Score the subtask with these ranges:\n"
        "- reasoning_depth: 0-3 (0 = lookup/formatting only, 1 = straightforward transformation, 2 = debugging or multi-step reasoning, 3 = architecture or open-ended investigation)\n"
        "- code_change_scope: 0-3 (0 = no code changes, 1 = small local edit, 2 = non-trivial or multi-file change, 3 = broad refactor/migration)\n"
        "- ambiguity: 0-2 (0 = clear, 1 = some interpretation needed, 2 = unclear/open-ended)\n"
        "- risk: 0-2 (0 = low risk, 1 = moderate impact, 2 = high-risk or hard-to-reverse)\n"
        "- io_heaviness: 0-2 (0 = little IO/reporting, 1 = some read/write/reporting, 2 = mostly IO/reporting/formatting)\n"
        "If the subtask is primarily summarizing findings, preparing a team update, writing a concise report, or formatting final output, prefer reasoning_depth <= 1, code_change_scope = 0, and suggested_route = FLASH unless the subtask explicitly says to debug, fix, implement, or investigate.\n"
        "Diagnostic evidence gathering such as inspecting logs, checking failing paths, comparing config changes, or isolating a root cause should still lean PRO even if it mostly reads files.\n"
        "If the original task is a billing/payment/finance/security/production incident, then evidence gathering, stop-loss or rollback evaluation, and containment decisions should usually score reasoning_depth >= 2, risk = 2, and suggested_route = PRO even when the step mostly reads logs or data.\n"
        "Also provide:\n"
        "- suggested_route: PRO or FLASH\n"
        "- confidence: 0.0-1.0\n"
        "- reason: one short sentence\n"
        "Guidance example A: {\"scores\":{\"reasoning_depth\":0,\"code_change_scope\":0,\"ambiguity\":0,\"risk\":0,\"io_heaviness\":2},\"suggested_route\":\"FLASH\",\"confidence\":0.92,\"reason\":\"Mostly reporting and formatting work.\"}\n"
        "Guidance example B: {\"scores\":{\"reasoning_depth\":2,\"code_change_scope\":2,\"ambiguity\":1,\"risk\":1,\"io_heaviness\":0},\"suggested_route\":\"PRO\",\"confidence\":0.87,\"reason\":\"Requires debugging and non-trivial code changes.\"}\n"
        "Guidance example C: {\"scores\":{\"reasoning_depth\":1,\"code_change_scope\":0,\"ambiguity\":0,\"risk\":0,\"io_heaviness\":2},\"suggested_route\":\"FLASH\",\"confidence\":0.9,\"reason\":\"This step only packages the findings into a concise update.\"}\n"
        "Guidance example D: {\"scores\":{\"reasoning_depth\":2,\"code_change_scope\":0,\"ambiguity\":1,\"risk\":1,\"io_heaviness\":1},\"suggested_route\":\"PRO\",\"confidence\":0.84,\"reason\":\"Inspecting logs here is part of root-cause diagnosis, not just copying data.\"}\n"
        "Guidance example E: {\"scores\":{\"reasoning_depth\":2,\"code_change_scope\":0,\"ambiguity\":1,\"risk\":2,\"io_heaviness\":1},\"suggested_route\":\"PRO\",\"confidence\":0.86,\"reason\":\"Collecting evidence for a billing incident is part of triage and should stay on the stronger model.\"}\n"
        "Guidance example F: {\"scores\":{\"reasoning_depth\":2,\"code_change_scope\":0,\"ambiguity\":1,\"risk\":2,\"io_heaviness\":0},\"suggested_route\":\"PRO\",\"confidence\":0.88,\"reason\":\"Assessing stop-loss or rollback in a high-risk incident is a consequential decision step.\"}\n"
        "Return raw JSON only with keys: scores, suggested_route, confidence, reason.\n"
        "JSON Output:"
    )


def normalize_complexity_assessment(raw: Dict[str, Any], task: str, desc: str) -> ComplexityAssessment:
    raw_scores = raw.get("scores")
    score_source = raw_scores if isinstance(raw_scores, dict) else {}
    base_scores: ComplexityScores = {
        "reasoning_depth": clamp_int(
            score_source.get("reasoning_depth", raw.get("reasoning_depth")),
            0,
            3,
        ),
        "code_change_scope": clamp_int(
            score_source.get("code_change_scope", raw.get("code_change_scope")),
            0,
            3,
        ),
        "ambiguity": clamp_int(score_source.get("ambiguity", raw.get("ambiguity")), 0, 2),
        "risk": clamp_int(score_source.get("risk", raw.get("risk")), 0, 2),
        "io_heaviness": clamp_int(
            score_source.get("io_heaviness", raw.get("io_heaviness")),
            0,
            2,
        ),
    }
    scores = apply_contextual_score_biases(task, desc, base_scores)
    confidence = clamp_float(raw.get("confidence"), 0.0, 1.0, default=0.5)
    suggested_route = normalize_route(
        raw.get("suggested_route") or raw.get("route") or raw.get("model"),
        default=PRO,
    )
    summary_like = is_summary_like_subtask(desc)
    deep_work_hint = has_deep_work_hint(desc)
    high_risk_core_step = is_high_risk_core_step(task, desc)
    reason = compact_text(
        str(raw.get("reason") or raw.get("summary") or f"Structured complexity judgment for: {desc}"),
        220,
    )
    complexity_score = score_complexity(scores)
    final_route = decide_route(task, desc, scores, suggested_route, confidence)
    judge_source = "structured_llm"
    if (
        summary_like
        and not deep_work_hint
        and final_route == FLASH
        and (suggested_route != FLASH or complexity_score > 3)
    ):
        reason = compact_text(
            "Summary/status-update subtask judged in isolation; prefer FLASH despite the broader debugging context.",
            220,
        )
        judge_source = "structured_llm+summary_bias"
    elif (
        high_risk_core_step
        and final_route == PRO
    ):
        reason = compact_text(build_high_risk_reason(desc), 220)
        judge_source = "structured_llm+high_risk_bias"
    elif deep_work_hint and not summary_like and final_route == PRO and suggested_route != PRO:
        reason = compact_text(
            "Diagnostic investigation step kept on PRO because log inspection/config comparison here supports root-cause analysis.",
            220,
        )
        judge_source = "structured_llm+diagnostic_bias"
    return {
        "scores": scores,
        "complexity_score": complexity_score,
        "suggested_route": suggested_route,
        "final_route": final_route,
        "confidence": confidence,
        "reason": reason,
        "judge_source": judge_source,
    }


def build_fallback_assessment(task: str, desc: str) -> ComplexityAssessment:
    text = desc.lower()
    summary_like = is_summary_like_subtask(desc)
    deep_work_hint = has_deep_work_hint(desc)
    reasoning_depth = 0
    code_change_scope = 0
    ambiguity = 0
    risk = 0
    io_heaviness = 0

    if contains_any(
        text,
        (
            "architecture",
            "architect",
            "migrate",
            "migration",
            "refactor",
            "redesign",
            "架构",
            "迁移",
            "重构",
            "重新设计",
        ),
    ):
        reasoning_depth = 3
        code_change_scope = 3
    elif contains_any(
        text,
        (
            "analy",
            "debug",
            "diagnos",
            "fix",
            "implement",
            "investig",
            "trace",
            "optimiz",
            "logic",
            "分析",
            "调试",
            "诊断",
            "修复",
            "实现",
            "排查",
            "追踪",
            "优化",
            "逻辑",
        ),
    ):
        reasoning_depth = 2
        code_change_scope = max(code_change_scope, 1)
    elif len(desc.strip()) > 40:
        reasoning_depth = 1

    if contains_any(
        text,
        (
            "multi-file",
            "across",
            "rewrite",
            "refactor",
            "migration",
            "重写",
            "重构",
            "迁移",
            "跨文件",
        ),
    ):
        code_change_scope = max(code_change_scope, 2)
    elif contains_any(
        text,
        (
            "edit",
            "update",
            "patch",
            "fix",
            "implement",
            "修改",
            "更新",
            "补丁",
            "修复",
            "实现",
        ),
    ):
        code_change_scope = max(code_change_scope, 1)

    if contains_any(
        text,
        (
            "investig",
            "determine",
            "why",
            "compare",
            "evaluate",
            "explore",
            "排查",
            "确定原因",
            "比较",
            "评估",
            "探索",
        ),
    ):
        ambiguity = 1
    if contains_any(
        text,
        (
            "open-ended",
            "strategy",
            "design direction",
            "方案",
            "策略",
            "方向",
        ),
    ):
        ambiguity = 2

    if contains_any(
        text,
        (
            "prod",
            "production",
            "database",
            "schema",
            "auth",
            "security",
            "payment",
            "delete",
            "生产",
            "数据库",
            "鉴权",
            "安全",
            "支付",
            "删除",
            "模式变更",
        ),
    ):
        risk = 2
    elif contains_any(
        text,
        (
            "config",
            "deploy",
            "k8s",
            "yaml",
            "配置",
            "部署",
            "集群",
            "清单",
        ),
    ):
        risk = 1

    if contains_any(
        text,
        (
            "summary",
            "summarize",
            "report",
            "status",
            "format",
            "document",
            "整理",
            "总结",
            "报告",
            "状态",
            "格式化",
            "文档",
        ),
    ):
        io_heaviness = 2
    elif contains_any(
        text,
        (
            "save",
            "write",
            "read",
            "collect",
            "list",
            "scan",
            "保存",
            "写入",
            "读取",
            "收集",
            "列出",
            "扫描",
        ),
    ):
        io_heaviness = 1

    base_scores: ComplexityScores = {
        "reasoning_depth": reasoning_depth,
        "code_change_scope": code_change_scope,
        "ambiguity": ambiguity,
        "risk": risk,
        "io_heaviness": io_heaviness,
    }
    scores = apply_contextual_score_biases(task, desc, base_scores)
    complexity_score = score_complexity(scores)
    suggested_route = (
        FLASH
        if complexity_score <= FLASH_COMPLEXITY_THRESHOLD and io_heaviness >= 1
        else PRO
    )
    confidence = 0.55 if (complexity_score > 0 or io_heaviness > 0) else 0.45
    final_route = decide_route(task, desc, scores, suggested_route, confidence)
    judge_source = "heuristic_fallback"
    if summary_like and not deep_work_hint and final_route == FLASH:
        reason = "启发式规则将该子任务视为独立的总结/状态更新步骤，优先走 FLASH。"
        judge_source = "heuristic_fallback+summary_bias"
    elif is_high_risk_core_step(task, desc) and final_route == PRO:
        if is_high_risk_evidence_step(desc):
            reason = "启发式规则将该子任务视为高风险事故里的取证步骤，因此优先走 PRO。"
        elif is_high_risk_decision_step(desc):
            reason = "启发式规则将该子任务视为高风险事故里的止损/回滚等关键决策步骤，因此优先走 PRO。"
        else:
            reason = "启发式规则将该子任务视为高风险事故里的诊断或修复策略步骤，因此优先走 PRO。"
        judge_source = "heuristic_fallback+high_risk_bias"
    elif deep_work_hint and not summary_like and final_route == PRO:
        reason = "启发式规则将该子任务视为诊断/排查步骤，即使主要是读日志或检查配置，也优先走 PRO。"
        judge_source = "heuristic_fallback+diagnostic_bias"
    else:
        reason = (
            "启发式评分判定该步骤以汇总/IO为主。"
            if final_route == FLASH
            else "启发式评分判定该步骤需要更强的推理或实现能力。"
        )
    return {
        "scores": scores,
        "complexity_score": complexity_score,
        "suggested_route": suggested_route,
        "final_route": final_route,
        "confidence": confidence,
        "reason": reason,
        "judge_source": judge_source,
    }


def score_subtask_with_model(task: str, subtask_desc: str, judge_model: str) -> ComplexityAssessment:
    default_timeout = DEFAULT_LARGE_MODEL_TIMEOUT if is_large_model(judge_model) else 300
    judge_timeout = int(os.environ.get("ROUTER_JUDGE_TIMEOUT", str(default_timeout)))
    raw_text = generate_text(
        judge_model,
        build_judge_prompt(task, subtask_desc),
        timeout=judge_timeout,
        num_predict=204800,  # Increased for full JSON object output from large models
        usage_label=f"Judge subtask: {compact_text(subtask_desc, 80)}",
    )
    if router_debug_enabled():
        print(f"\n[DEBUG Judge Output for: {subtask_desc[:60]}...]")
        print(f"  Model: {judge_model}")
        print(f"  Raw text length: {len(raw_text)} chars")
        print(f"  First 400 chars: {raw_text[:400]}")
        if len(raw_text) > 400:
            print(f"  Last 200 chars: {raw_text[-200:]}")
        print(f"  Contains '{{': { '{' in raw_text }, Contains '}}': {'}' in raw_text }")
        print(f"  ---\n")
    return normalize_complexity_assessment(extract_first_json_object(raw_text), task, subtask_desc)


def build_subtask(planned: PlannedSubtask, assessment: ComplexityAssessment) -> Subtask:
    return {
        "id": planned["id"],
        "desc": planned["desc"],
        "depends_on": list(planned["depends_on"]),
        "dependency_reason": planned["dependency_reason"],
        "model": assessment["final_route"],
        "assessment": assessment,
    }


def display_plan(subtasks: List[Subtask], planner_model: str, judge_model: str) -> None:
    print("\n" + "=" * 58)
    print("🤖 LANGGRAPH 路由计划已生成")
    print("=" * 58)
    print(f"规划模型: {planner_model}")
    print(f"判定模型: {judge_model}")
    for index, step in enumerate(subtasks, start=1):
        icon = "🧠 [PRO]  " if step["model"] == PRO else "⚡ [FLASH] "
        assessment = step["assessment"]
        dependencies = ", ".join(step["depends_on"]) if step["depends_on"] else "-"
        print(
            f"步骤 {index} [{step['id']}]: {icon}| score={assessment['complexity_score']} "
            f"| conf={assessment['confidence']:.2f} | deps={dependencies} | {step['desc']}"
        )
        print(
            f"         判定依据: {assessment['reason']} "
            f"({assessment['judge_source']}, suggested={assessment['suggested_route']})"
        )
        print(f"         依赖依据: {step['dependency_reason']}")
    print("=" * 58)


def planner_warmup_node(state: RouterState) -> Dict[str, Any]:
    if ROUTER_SKIP_WARMUP:
        print("[Node: Planner Warmup] ⏭️  Skipping warmup (ROUTER_SKIP_WARMUP=1)")
        return {"planner_warmup_attempt": 3, "status": "planner_warmup_skipped"}
    attempt = state["planner_warmup_attempt"] + 1
    if attempt == 1:
        print("\n[Node: Planner Warmup] 🔥 Warming up planner model with a LangGraph loop...")
    try:
        generate_text(
            state["planner_model"],
            "OK",
            timeout=300,
            num_predict=4,
            usage_label=f"Planner warmup {attempt}",
        )
        print(f"[Planner Warmup] ✅ Ping {attempt}/3 successful")
    except Exception as exc:
        print(f"[Planner Warmup] ⚠️ Ping {attempt}/3 failed: {exc}")
    return {
        "planner_warmup_attempt": attempt,
        "status": f"planner_warmup_{attempt}_done",
    }


def route_after_planner_warmup(state: RouterState) -> str:
    if state["planner_warmup_attempt"] < 3:
        return "planner_warmup"
    return "planner_invoke"


def planner_invoke_node(state: RouterState) -> Dict[str, Any]:
    print("\n[Node: Planner Invoke] 🧠 调用规划模型拆解任务...")
    try:
        planner_output_tokens = resolve_positive_int(
            None,
            ROUTER_PLANNER_MAX_OUTPUT_TOKENS_ENV_VAR,
            DEFAULT_PLANNER_MAX_OUTPUT_TOKENS,
        )
        raw_text = generate_text(
            state["planner_model"],
            build_planner_prompt(state["task"]),
            timeout=300,  # 5 minutes for large models like gemma4:26b
            num_predict=planner_output_tokens,
            usage_label="Planner invoke",
        )
        return {
            "planner_raw_text": raw_text,
            "planner_error": "",
            "status": "planner_invoked",
        }
    except Exception as exc:
        error_text = compact_text(str(exc), 260)
        print(f"⚠️ 规划模型调用异常：{error_text}")
        return {
            "planner_raw_text": "",
            "planner_error": error_text,
            "status": "planner_invoke_failed",
        }


def route_after_planner_invoke(state: RouterState) -> str:
    if state["status"] == "planner_invoke_failed":
        return "planner_fallback"
    return "planner_parse"


def planner_parse_node(state: RouterState) -> Dict[str, Any]:
    raw_text = state["planner_raw_text"]
    if router_debug_enabled():
        print(f"\n[DEBUG Planner Output]")
        print(f"  Model: {state['planner_model']}")
        print(f"  Raw text length: {len(raw_text)} chars")
        print(f"  First 400 chars: {raw_text[:400]}")
        if len(raw_text) > 400:
            print(f"  Last 200 chars: {raw_text[-200:]}")
        print(f"  Contains '[': { '[' in raw_text }, Contains ']': {']' in raw_text }")
        print(f"  ---\n")
    try:
        planned_subtasks = normalize_planned_subtasks(extract_first_json_array(raw_text))
        planned_subtasks = ensure_communication_subtask(state["task"], planned_subtasks)
        planned_subtasks = normalize_planned_subtasks(planned_subtasks)
        print(f"✅ 规划成功，拆解出 {len(planned_subtasks)} 个步骤。")
        return {
            "planned_subtasks": planned_subtasks,
            "planner_error": "",
            "status": "planner_parsed",
        }
    except Exception as exc:
        error_text = compact_text(str(exc), 260)
        print(f"⚠️ 规划输出解析异常：{error_text}")
        return {
            "planner_error": error_text,
            "status": "planner_parse_failed",
        }


def route_after_planner_parse(state: RouterState) -> str:
    if state["status"] == "planner_parse_failed":
        return "planner_fallback"
    return "dependency_judge"


def planner_fallback_node(state: RouterState) -> Dict[str, Any]:
    planned_subtasks = build_fallback_subtasks(state["task"])
    planned_subtasks = ensure_communication_subtask(state["task"], planned_subtasks)
    planned_subtasks = normalize_planned_subtasks(planned_subtasks)
    error_text = state["planner_error"] or "Unknown planner failure"
    print(f"⚠️ 规划器异常：{error_text}。已切换到启发式回退规划。")
    return {
        "planned_subtasks": planned_subtasks,
        "errors": [f"Planner fallback: {error_text}"],
        "status": "planner_fallback",
    }


def dependency_judge_node(state: RouterState) -> Dict[str, Any]:
    print("\n[Node: Dependency Judge] 🧭 验证子任务依赖关系...")
    try:
        judged_subtasks, confidence, issues, raw_text = judge_dependencies_with_model(
            state["task"],
            state["planned_subtasks"],
            state["judge_model"],
        )
        print(
            f"  依赖判定完成: subtasks={len(judged_subtasks)} "
            f"| confidence={confidence:.2f} | issues={len(issues)}"
        )
        return {
            "planned_subtasks": judged_subtasks,
            "dependency_raw_text": raw_text,
            "dependency_error": "",
            "dependency_issues": issues,
            "dependency_confidence": confidence,
            "history": [f"Dependency judge reviewed {len(judged_subtasks)} planned subtasks."],
            "status": "dependencies_judged",
        }
    except Exception as exc:
        error_text = compact_text(str(exc), 260)
        print(f"  依赖判定异常: {error_text}。保留规划器依赖并进入结构校验。")
        return {
            "dependency_error": error_text,
            "errors": [f"Dependency judge fallback: {error_text}"],
            "status": "dependency_judge_failed",
        }


def dependency_validate_node(state: RouterState) -> Dict[str, Any]:
    try:
        validated_subtasks = validate_dependency_graph(state["planned_subtasks"])
        dependency_edges = sum(len(subtask["depends_on"]) for subtask in validated_subtasks)
        print(
            f"\n[Node: Dependency Validate] ✅ DAG 校验通过: "
            f"subtasks={len(validated_subtasks)}, edges={dependency_edges}"
        )
        return {
            "planned_subtasks": validated_subtasks,
            "history": [
                f"Dependency graph validated with {len(validated_subtasks)} subtasks and {dependency_edges} edges."
            ],
            "status": "dependencies_validated",
        }
    except Exception as exc:
        error_text = compact_text(str(exc), 260)
        fallback_subtasks = make_serial_dependency_plan(state["planned_subtasks"])
        print(
            f"\n[Node: Dependency Validate] ⚠️ DAG 校验失败: {error_text}。"
            "已切换到保守串行依赖。"
        )
        return {
            "planned_subtasks": fallback_subtasks,
            "dependency_error": error_text,
            "dependency_issues": state["dependency_issues"] + [error_text],
            "errors": [f"Dependency validation fallback: {error_text}"],
            "history": ["Dependency graph invalid; switched to conservative serial execution order."],
            "status": "dependencies_validated_with_fallback",
        }


def planner_ready_node(state: RouterState) -> Dict[str, Any]:
    return {
        "subtasks": [],
        "current_step": 0,
        "history": [f"Planner produced {len(state['planned_subtasks'])} planned subtasks."],
        "status": "planned",
    }


def judge_warmup_node(state: RouterState) -> Dict[str, Any]:
    if ROUTER_SKIP_WARMUP:
        print("[Node: Judge Warmup] ⏭️  Skipping warmup (ROUTER_SKIP_WARMUP=1)")
        return {"judge_warmup_done": True, "status": "judge_warmup_skipped"}
    print("\n[Node: Judge Warmup] 🔥 Warming up judge model before LangGraph fanout...")
    try:
        generate_text(
            state["judge_model"],
            "OK",
            timeout=300,
            num_predict=4,
            usage_label="Judge warmup",
        )
        print("[Judge Warmup] ✅ Warmup successful")
        return {
            "judge_warmup_done": True,
            "history": ["Judge warmup completed before fanout."],
            "status": "judge_warmed",
        }
    except Exception as exc:
        error_text = compact_text(str(exc), 220)
        print(f"[Judge Warmup] ⚠️ Warmup failed: {error_text}")
        return {
            "judge_warmup_done": False,
            "history": [f"Judge warmup failed before fanout: {error_text}"],
            "status": "judge_warmup_failed",
        }


def route_to_judge_subtasks(state: RouterState) -> List[Send] | str:
    if not state["planned_subtasks"]:
        return "assemble_plan"
    print("\n[Edge: Planner -> Judge Fanout] 🎯 为每个子任务分发独立 LangGraph 判定节点...")
    return [
        Send(
            "judge_subtask",
            {
                **state,
                "judge_index": index,
                "judge_desc": planned["desc"],
            },
        )
        for index, planned in enumerate(state["planned_subtasks"], start=1)
    ]


def judge_subtask_node(state: RouterState) -> Dict[str, Dict[int, JudgedSubtask]]:
    index = state["judge_index"]
    planned = state["planned_subtasks"][index - 1]
    desc = state["judge_desc"] or planned["desc"]
    print(f"\n[Node: Judge Subtask] 🎯 Step {index} 结构化复杂度评分...")
    error = ""
    try:
        assessment = score_subtask_with_model(state["task"], desc, state["judge_model"])
        print(
            f"  步骤 {index}: ✅ {assessment['final_route']} "
            f"(score={assessment['complexity_score']}, conf={assessment['confidence']:.2f})"
        )
    except Exception as exc:
        assessment = build_fallback_assessment(state["task"], desc)
        error = f"Judge fallback on step {index}: {exc}"
        print(f"  步骤 {index}: ⚠️ 判定异常 ({exc})，已切换到启发式评分。")

    return {
        "judge_results": {
            index: {
                "index": index,
                "subtask": build_subtask(planned, assessment),
                "error": error,
            }
        }
    }


def assemble_plan_node(state: RouterState) -> RouterState:
    print("\n[Node: Assemble Plan] 🧩 汇总 LangGraph 判定结果...")
    ordered_results = sorted(state["judge_results"].values(), key=lambda item: item["index"])
    subtasks = [result["subtask"] for result in ordered_results]
    errors = [result["error"] for result in ordered_results if result["error"]]
    display_plan(subtasks, state["planner_model"], state["judge_model"])
    return {
        "subtasks": subtasks,
        "judge_index": 0,
        "judge_desc": "",
        "history": [f"Judge assigned routes for {len(subtasks)} subtasks via LangGraph fanout."],
        "errors": errors,
        "status": "judged",
    }


def extract_technical_metadata_for_result(state: RouterState, result: StepResult) -> List[str]:
    step_number = result["step"]
    step_status = result["status"]
    active_output = result["output"].strip()

    print(f"\n[Node: Metadata Extractor] 🔍 Extracting technical gold from Step {step_number}")

    if (
        not active_output
        or "failed" in step_status
        or step_status == "executor_fallback"
        or "exhausted" in step_status
    ):
        return [f"Step {step_number} metadata extraction skipped (no output or failure)."]

    metadata_context = build_metadata_context_pack_json(state, result, active_output)
    prompt = (
        f"Metadata context JSON:\n{metadata_context}\n\n"
        "Instruction: Extract the 'technical gold' from this output. "
        "Identify: 1. Key architectural decisions, 2. Specific library/tool choices, 3. Critical logic/algorithm details, "
        "4. CAP theorem trade-offs identified, 5. Final outcomes or verified results. "
        "Do not summarize generally; list these as atomic, high-precision facts. "
        "Return as a concise bulleted list."
    )

    invocation = invoke_with_provider_fallback(
        state["pro_model"],
        state["pro_fallback_models"],
        prompt,
        timeout=120,
        num_predict=800,
        temperature=0.0,
        label="Metadata Extractor",
        attempt_log=list(state["history"]),
    )

    metadata = invocation["output"] if invocation["success"] else "Metadata extraction failed."
    return [f"--- TECHNICAL METADATA STEP {step_number} ---\n{metadata}\n---"]


def route_to_parallel_executor_subtasks(state: RouterState) -> List[Send] | str:
    sends = [
        Send(
            "parallel_executor",
            {
                **state,
                "execution_index": index,
                "execution_subtask": subtask,
            },
        )
        for index, subtask in enumerate(state["subtasks"], start=1)
        if not is_deferred_execution_subtask(subtask)
    ]
    if not sends:
        return "parallel_execution_join"

    print(
        "\n[Edge: Plan -> Executor Fanout] 🚀 Dispatching "
        f"{len(sends)} independent subtasks with LangGraph concurrency..."
    )
    return sends


def completed_subtask_ids(state: RouterState) -> set[str]:
    return {
        str(result.get("subtask_id") or "")
        for result in state["execution_results"].values()
        if str(result.get("subtask_id") or "")
    }


def dependency_context_results_for_subtask(
    state: RouterState,
    subtask: Subtask,
) -> List[StepResult]:
    dependency_ids = set(subtask["depends_on"])
    if not dependency_ids:
        return []
    return [
        result
        for result in sorted(state["execution_results"].values(), key=lambda item: item["step"])
        if result.get("subtask_id") in dependency_ids
    ]


def dependency_scheduler_node(state: RouterState) -> Dict[str, Any]:
    completed_ids = completed_subtask_ids(state)
    remaining_count = sum(1 for subtask in state["subtasks"] if subtask["id"] not in completed_ids)
    return {
        "current_step": len(completed_ids),
        "history": [
            f"Dependency scheduler sees {len(completed_ids)} completed and {remaining_count} remaining subtasks."
        ],
        "status": "dependency_scheduling",
    }


def route_to_ready_executor_subtasks(state: RouterState) -> List[Send] | str:
    completed_ids = completed_subtask_ids(state)
    ready: List[tuple[int, Subtask]] = []
    remaining: List[Subtask] = []

    for index, subtask in enumerate(state["subtasks"], start=1):
        if subtask["id"] in completed_ids:
            continue
        remaining.append(subtask)
        if all(dependency_id in completed_ids for dependency_id in subtask["depends_on"]):
            ready.append((index, subtask))

    if not remaining:
        return "execution_finalize_join"
    if not ready:
        return "dependency_deadlock"

    print(
        "\n[Edge: Dependency Scheduler -> Executor Fanout] 🚀 Dispatching "
        f"{len(ready)} ready subtasks; completed={len(completed_ids)}, remaining={len(remaining)}."
    )
    return [
        Send(
            "parallel_executor",
            {
                **state,
                "execution_index": index,
                "execution_subtask": subtask,
            },
        )
        for index, subtask in ready
    ]


def route_to_deferred_executor_subtasks(state: RouterState) -> List[Send] | str:
    sends = [
        Send(
            "deferred_executor",
            {
                **state,
                "execution_index": index,
                "execution_subtask": subtask,
            },
        )
        for index, subtask in enumerate(state["subtasks"], start=1)
        if is_deferred_execution_subtask(subtask)
    ]
    if not sends:
        return "execution_finalize_join"

    print(
        "\n[Edge: Context Join -> Deferred Executor Fanout] 🧾 Dispatching "
        f"{len(sends)} synthesis/reporting subtasks after parallel context is ready..."
    )
    return sends


def invoke_parallel_executor_attempt(
    state: RouterState,
    index: int,
    subtask: Subtask,
    route: Literal["PRO", "FLASH"],
    attempt_count: int,
    retry_count: int,
    escalated_from_flash: bool,
    flash_review: FlashReviewResult,
    attempt_log: List[str],
) -> tuple[ModelInvocationResult, int]:
    model_name = state["pro_model"] if route == PRO else state["flash_model"]
    dependency_results = dependency_context_results_for_subtask(state, subtask)
    prompt_state = dict(state)
    prompt_state.update(
        {
            "results": dependency_results,
            "current_step": len(state["execution_results"]),
            "active_subtask": subtask,
            "active_route": route,
            "active_model_name": model_name,
            "active_output": "",
            "active_last_error": "",
            "active_attempt_count": attempt_count,
            "active_retry_count": retry_count,
            "active_escalated_from_flash": escalated_from_flash,
            "active_used_provider_fallback": False,
            "active_flash_review": flash_review,
            "active_attempt_log": list(attempt_log),
            "active_invocation_result": empty_model_invocation_result(),
        }
    )

    next_attempt_count = attempt_count + 1
    next_attempt_log = list(attempt_log)
    next_attempt_log.append(f"Attempt {next_attempt_count}: route={route} model={model_name}")
    invocation = invoke_with_provider_fallback(
        model_name,
        route_fallback_models(state, route),
        build_execution_prompt(prompt_state, route),
        timeout=DEFAULT_PRO_EXECUTION_TIMEOUT if route == PRO else DEFAULT_FLASH_EXECUTION_TIMEOUT,
        num_predict=450 if route == PRO else 240,
        temperature=0.0,
        label=f"{route} executor step {index}",
        attempt_log=next_attempt_log,
    )
    return invocation, next_attempt_count


def build_parallel_step_result(
    *,
    index: int,
    subtask: Subtask,
    planned_route: Literal["PRO", "FLASH"],
    final_route: Literal["PRO", "FLASH"],
    model_name: str,
    output: str,
    status: str,
    attempt_count: int,
    retry_count: int,
    escalated_from_flash: bool,
    used_provider_fallback: bool,
    flash_review: FlashReviewResult,
    attempt_log: List[str],
) -> StepResult:
    return {
        "step": index,
        "subtask_id": subtask["id"],
        "depends_on": list(subtask["depends_on"]),
        "planned_route": planned_route,
        "route": final_route,
        "model_name": model_name,
        "desc": subtask["desc"],
        "output": output,
        "status": status,
        "attempt_count": attempt_count,
        "retry_count": retry_count,
        "escalated_from_flash": escalated_from_flash,
        "used_provider_fallback": used_provider_fallback,
        "flash_review": flash_review,
        "attempt_log": attempt_log,
    }


def execute_subtask_in_parallel_branch(
    state: RouterState,
    index: int,
    subtask: Subtask,
) -> tuple[StepResult, List[str]]:
    planned_route = normalize_route(subtask.get("model"), default=PRO)
    route = planned_route
    retry_count = 0
    attempt_count = 0
    escalated_from_flash = False
    flash_review = empty_flash_review()
    attempt_log: List[str] = []
    errors: List[str] = []
    output = ""
    status = "executor_failed"
    model_name = state["pro_model"] if route == PRO else state["flash_model"]
    used_provider_fallback = False
    total_steps = len(state["subtasks"])

    icon = "🧠 [PRO]" if route == PRO else "⚡ [FLASH]"
    print(
        f"\n[Node: Parallel Executor] {icon} Step {index}/{total_steps} -> {model_name}"
    )
    print(
        f"  描述: {subtask['desc']} | score={subtask['assessment']['complexity_score']} "
        f"| conf={subtask['assessment']['confidence']:.2f}"
    )

    while True:
        invocation, attempt_count = invoke_parallel_executor_attempt(
            state,
            index,
            subtask,
            route,
            attempt_count,
            retry_count,
            escalated_from_flash,
            flash_review,
            attempt_log,
        )
        attempt_log = list(invocation["attempt_log"])
        model_name = invocation["model_name"] or model_name
        used_provider_fallback = invocation["used_provider_fallback"] if invocation["success"] else False

        if invocation["success"]:
            output = invocation["output"].strip()
            status = "executed_via_provider_fallback" if used_provider_fallback else "executed"
            last_error = ""
        else:
            output = ""
            status = "executor_failed"
            last_error = invocation["error_text"] or "Unknown execution failure"

        if route == FLASH:
            review = (
                verify_flash_output(subtask["desc"], output, flash_review, retry_count)
                if invocation["success"]
                else classify_flash_execution_failure(last_error)
            )
            attempt_log.append(
                f"FLASH review => decision={review['decision']} failure_type={review['failure_type']} reason={review['reason']}"
            )
            flash_review = review

            if review["decision"] == "record":
                break

            if review["decision"] == "retry":
                if retry_count < state["flash_retry_budget"]:
                    retry_count += 1
                    message = (
                        f"Retrying FLASH for step {index} "
                        f"({retry_count}/{state['flash_retry_budget']}) after {review['failure_type']} failure."
                    )
                    print(f"\n[Node: Parallel Retry Guard] 🔁 {message}")
                    attempt_log.append(message)
                    continue

                exhausted_reason = (
                    f"{review['reason']} Retry budget exhausted after {retry_count} retr"
                    f"{'y' if retry_count == 1 else 'ies'}."
                )
                flash_review = {
                    "decision": "record",
                    "failure_type": review["failure_type"],
                    "reason": exhausted_reason,
                }
                if not output or output.startswith("FLASH executor fallback output:"):
                    output = (
                        f"FLASH execution failed after {retry_count} retr"
                        f"{'y' if retry_count == 1 else 'ies'} "
                        f"({review['failure_type']}): {exhausted_reason}"
                    )
                status = "flash_retry_exhausted"
                break

            escalated_from_flash = True
            route = PRO
            model_name = state["pro_model"]
            message = (
                f"Escalated step {index} from FLASH to PRO "
                f"because {review['failure_type']}: {review['reason']}"
            )
            print(f"\n[Node: Parallel Escalation] 🧠 {message}")
            attempt_log.append(message)
            continue

        if invocation["success"]:
            break

        error = f"PRO executor fallback on step {index}: {last_error}"
        errors.append(error)
        output = f"PRO executor fallback output: {subtask['desc']}"
        status = "executor_fallback"
        print(f"\n[Node: Parallel Executor Fallback] 🧯 {error}")
        break

    result = build_parallel_step_result(
        index=index,
        subtask=subtask,
        planned_route=planned_route,
        final_route=route,
        model_name=model_name,
        output=output,
        status=status,
        attempt_count=attempt_count,
        retry_count=retry_count,
        escalated_from_flash=escalated_from_flash,
        used_provider_fallback=used_provider_fallback,
        flash_review=flash_review,
        attempt_log=attempt_log,
    )
    print(f"[Node: Parallel Recorder] 已记录步骤 {index} -> {result['route']} ({result['model_name']})")
    return result, errors


def parallel_executor_node(state: RouterState) -> Dict[str, Any]:
    index = state["execution_index"]
    subtask = state["execution_subtask"]
    try:
        result, errors = execute_subtask_in_parallel_branch(state, index, subtask)
    except Exception as exc:
        error_text = compact_text(str(exc), 260)
        subtask = state["execution_subtask"]
        planned_route = normalize_route(subtask.get("model"), default=PRO)
        result = build_parallel_step_result(
            index=index,
            subtask=subtask,
            planned_route=planned_route,
            final_route=planned_route,
            model_name=state["pro_model"] if planned_route == PRO else state["flash_model"],
            output=f"{planned_route} executor fallback output: {subtask.get('desc', 'N/A')}",
            status="executor_fallback",
            attempt_count=0,
            retry_count=0,
            escalated_from_flash=False,
            used_provider_fallback=False,
            flash_review=empty_flash_review(),
            attempt_log=[f"Unhandled parallel executor exception: {error_text}"],
        )
        errors = [f"Parallel executor fallback on step {index}: {error_text}"]

    history = [f"Recorded parallel step {index}: {result['desc']}"]
    history.extend(extract_technical_metadata_for_result(state, result))
    return {
        "execution_results": {index: result},
        "history": history,
        "errors": errors,
    }


def parallel_execution_join_node(state: RouterState) -> RouterState:
    context_results = sorted(
        [
            result
            for index, result in state["execution_results"].items()
            if not is_deferred_execution_subtask(state["subtasks"][index - 1])
        ],
        key=lambda result: result["step"],
    )
    print(
        "\n[Node: Parallel Execution Join] 🧩 "
        f"Collected {len(context_results)} independent subtask results."
    )
    return {
        "execution_context_results": context_results,
        "current_step": len(context_results),
        "history": [f"Parallel executor completed {len(context_results)} independent subtasks."],
        "status": "parallel_executed",
    }


def dependency_execution_join_node(state: RouterState) -> RouterState:
    ordered_results = sorted(state["execution_results"].values(), key=lambda result: result["step"])
    completed_ids = completed_subtask_ids(state)
    print(
        "\n[Node: Dependency Execution Join] 🧩 "
        f"Collected {len(ordered_results)} completed dependency-aware subtask results."
    )
    return {
        "execution_context_results": ordered_results,
        "current_step": len(completed_ids),
        "history": [f"Dependency executor has completed {len(completed_ids)} subtasks."],
        "status": "dependency_wave_executed",
    }


def dependency_deadlock_node(state: RouterState) -> RouterState:
    completed_ids = completed_subtask_ids(state)
    fallback_results: Dict[int, StepResult] = {}
    errors: List[str] = []
    for index, subtask in enumerate(state["subtasks"], start=1):
        if subtask["id"] in completed_ids:
            continue
        missing = [
            dependency_id
            for dependency_id in subtask["depends_on"]
            if dependency_id not in completed_ids
        ]
        planned_route = normalize_route(subtask.get("model"), default=PRO)
        error = (
            f"Dependency deadlock on step {index} ({subtask['id']}): "
            f"missing dependencies {', '.join(missing) or 'unknown'}"
        )
        errors.append(error)
        fallback_results[index] = build_parallel_step_result(
            index=index,
            subtask=subtask,
            planned_route=planned_route,
            final_route=planned_route,
            model_name=state["pro_model"] if planned_route == PRO else state["flash_model"],
            output=f"Dependency scheduler fallback output: {error}",
            status="dependency_deadlock",
            attempt_count=0,
            retry_count=0,
            escalated_from_flash=False,
            used_provider_fallback=False,
            flash_review=empty_flash_review(),
            attempt_log=[error],
        )
    print(
        "\n[Node: Dependency Deadlock] ⚠️ "
        f"Recorded {len(fallback_results)} fallback results for blocked subtasks."
    )
    return {
        "execution_results": fallback_results,
        "errors": errors,
        "history": ["Dependency scheduler deadlock fallback recorded blocked subtasks."],
        "status": "dependency_deadlock",
    }


def execution_finalize_join_node(state: RouterState) -> RouterState:
    ordered_results = sorted(state["execution_results"].values(), key=lambda result: result["step"])
    print(
        "\n[Node: Execution Final Join] ✅ "
        f"Collected {len(ordered_results)} total subtask results; entering finalizer."
    )
    return {
        "results": ordered_results,
        "current_step": len(ordered_results),
        "execution_index": 0,
        "execution_subtask": {},
        "history": [f"Executor fanout joined {len(ordered_results)} total subtask results."],
        "status": "ready_to_finalize",
    }


def dispatch_node(state: RouterState) -> RouterState:
    total_steps = len(state["subtasks"])
    if state["current_step"] >= total_steps:
        print("\n[Node: Dispatcher] ✅ 所有步骤已完成，进入最终汇总节点。")
        return {
            "active_subtask": {},
            "active_route": "",
            "active_model_name": "",
            "active_output": "",
            "active_last_error": "",
            "active_attempt_count": 0,
            "active_retry_count": 0,
            "active_escalated_from_flash": False,
            "active_used_provider_fallback": False,
            "active_flash_review": empty_flash_review(),
            "active_attempt_log": [],
            "active_invocation_result": empty_model_invocation_result(),
            "status": "ready_to_finalize",
        }

    subtask = state["subtasks"][state["current_step"]]
    route = subtask["model"]
    model_name = state["pro_model"] if route == PRO else state["flash_model"]
    icon = "🧠 [PRO]" if route == PRO else "⚡ [FLASH]"
    assessment = subtask["assessment"]

    print(
        f"\n[Node: Dispatcher] {icon} Step {state['current_step'] + 1}/{total_steps} "
        f"-> {model_name}"
    )
    print(
        f"  描述: {subtask['desc']} | score={assessment['complexity_score']} "
        f"| conf={assessment['confidence']:.2f}"
    )

    return {
        "active_subtask": subtask,
        "active_route": route,
        "active_model_name": model_name,
        "active_output": "",
        "active_last_error": "",
        "active_attempt_count": 0,
        "active_retry_count": 0,
        "active_escalated_from_flash": False,
        "active_used_provider_fallback": False,
        "active_flash_review": empty_flash_review(),
        "active_attempt_log": [],
        "active_invocation_result": empty_model_invocation_result(),
        "history": [f"Dispatched step {state['current_step'] + 1} to {route} using {model_name}."],
        "status": "dispatched",
    }


def route_after_dispatch(state: RouterState) -> str:
    if state["status"] == "ready_to_finalize":
        return "flash_finalizer"
    return "pro_executor" if state["active_route"] == PRO else "flash_executor"


def build_execution_prompt(state: RouterState, route: Literal["PRO", "FLASH"]) -> str:
    context_pack = build_executor_context_pack_json(state, route)
    escalation_context = ""
    if route == PRO and state["active_escalated_from_flash"]:
        flash_review = state["active_flash_review"]
        escalation_context = (
            "Escalation context: this step was first attempted on FLASH and then escalated to PRO. "
            f"failure_type={flash_review['failure_type']}, retries={state['active_retry_count']}, "
            f"reason={flash_review['reason']}\n"
        )

    mode_instruction = (
        "Think carefully and provide a high-signal technical result."
        if route == PRO
        else "Respond quickly and concisely with the operational or summary result."
    )
    return (
        f"Role: {route} task executor.\n"
        f"Execution mode: {mode_instruction}\n"
        f"Execution context JSON:\n{context_pack}\n"
        f"{escalation_context}"
        "Return only the result for the current subtask. No markdown fences."
    )


def invoke_executor_with_route(state: RouterState, route: Literal["PRO", "FLASH"]) -> Dict[str, Any]:
    node_label = "PRO Executor" if route == PRO else "FLASH Executor"
    model_name = state["active_model_name"] or (
        state["pro_model"] if route == PRO else state["flash_model"]
    )
    print(f"\n[Node: {node_label} Invoke] 开始执行子任务...")

    attempt_log = list(state["active_attempt_log"])
    attempt_count = state["active_attempt_count"] + 1
    attempt_log.append(f"Attempt {attempt_count}: route={route} model={model_name}")
    invocation = invoke_with_provider_fallback(
        model_name,
        route_fallback_models(state, route),
        build_execution_prompt(state, route),
        timeout=DEFAULT_PRO_EXECUTION_TIMEOUT if route == PRO else DEFAULT_FLASH_EXECUTION_TIMEOUT,
        num_predict=450 if route == PRO else 240,
        temperature=0.0,
        label=f"{route} executor step {state['current_step'] + 1}",
        attempt_log=attempt_log,
    )
    return {
        "active_invocation_result": invocation,
        "active_attempt_count": attempt_count,
        "active_attempt_log": invocation["attempt_log"],
        "status": "executor_invoked",
    }


def executor_result_node(state: RouterState) -> Dict[str, Any]:
    print("\n[Node: Executor Result] Classifying executor invocation result...")
    invocation = state["active_invocation_result"]
    model_name = state["active_model_name"] or (
        state["pro_model"] if state["active_route"] == PRO else state["flash_model"]
    )
    if invocation["success"]:
        output = invocation["output"]
        status = "executed_via_provider_fallback" if invocation["used_provider_fallback"] else "executed"
        print(
            f"  状态: 模型执行成功。"
            f"{' (provider fallback)' if invocation['used_provider_fallback'] else ''}"
        )
    else:
        output = ""
        status = "executor_failed"
        print(f"  状态: 执行异常 ({invocation['error_text']})，交由 LangGraph 回退路径处理。")

    return {
        "active_output": output.strip(),
        "active_last_error": invocation["error_text"],
        "active_model_name": invocation["model_name"] if invocation["success"] else model_name,
        "active_used_provider_fallback": invocation["used_provider_fallback"] if invocation["success"] else False,
        "active_attempt_log": invocation["attempt_log"],
        "history": [
            f"Executed step {state['current_step'] + 1} with route {state['active_route']} using {invocation['model_name'] if invocation['success'] else model_name}."
        ],
        "status": status,
    }


def pro_executor_node(state: RouterState) -> RouterState:
    return invoke_executor_with_route(state, PRO)


def flash_executor_node(state: RouterState) -> RouterState:
    return invoke_executor_with_route(state, FLASH)


def route_after_executor_result(state: RouterState) -> str:
    if state["status"] == "executor_failed":
        # RESILIENCE FIX: If PRO fails, try to la-concisely rescue with FLASH before giving up
        if state["active_route"] == PRO:
            return "flash_review" 
        return "flash_review"
    if state["active_route"] == FLASH:
        return "flash_review"
    return "recorder"


def executor_fallback_node(state: RouterState) -> Dict[str, Any]:
    route = state["active_route"] or PRO
    output = f"{route} executor fallback output: {state['active_subtask'].get('desc', 'N/A')}"
    error = (
        f"{route} executor fallback on step {state['current_step'] + 1}: "
        f"{state['active_last_error'] or 'Unknown execution failure'}"
    )
    print(f"\n[Node: Executor Fallback] 🧯 {error}")
    return {
        "active_output": output,
        "errors": [error],
        "history": [f"Executor fallback produced deterministic output for step {state['current_step'] + 1}."],
        "status": "executor_fallback",
    }


def flash_review_node(state: RouterState) -> RouterState:
    print("\n[Node: Flash Review] 🧪 正在验证 FLASH 结果并分类失败原因...")
    attempt_log = list(state["active_attempt_log"])
    prior_review = state["active_flash_review"]

    if state["status"] in {"executed", "executed_via_provider_fallback"}:
        review = verify_flash_output(
            state["active_subtask"].get("desc", ""),
            state["active_output"],
            prior_review,
            state["active_retry_count"],
        )
        if review["decision"] == "record":
            status = "flash_verified"
            print("  状态: FLASH 输出通过验证。")
        else:
            status = "flash_needs_escalation"
            print(f"  状态: FLASH 输出需要升级到 PRO。原因: {review['reason']}")
    else:
        review = classify_flash_execution_failure(
            state["active_last_error"] or state["active_output"] or "Unknown FLASH failure"
        )
        status = "flash_retry_candidate" if review["decision"] == "retry" else "flash_needs_escalation"
        if review["decision"] == "retry":
            print(f"  状态: FLASH 失败被判定为可重试。原因: {review['reason']}")
        else:
            print(f"  状态: FLASH 失败被判定应升级到 PRO。原因: {review['reason']}")

    attempt_log.append(
        f"FLASH review => decision={review['decision']} failure_type={review['failure_type']} reason={review['reason']}"
    )
    return {
        "active_flash_review": review,
        "active_attempt_log": attempt_log,
        "history": [
            f"Flash review for step {state['current_step'] + 1}: decision={review['decision']} failure_type={review['failure_type']}."
        ],
        "status": status,
    }


def route_after_flash_review(state: RouterState) -> str:
    decision = state["active_flash_review"]["decision"]
    if decision == "retry":
        return "retry_guard"
    if decision == "escalate":
        return "escalation"
    return "recorder"


def retry_guard_node(state: RouterState) -> RouterState:
    review = state["active_flash_review"]
    retries_used = state["active_retry_count"]
    retry_budget = state["flash_retry_budget"]
    attempt_log = list(state["active_attempt_log"])

    if retries_used < retry_budget:
        next_retry_count = retries_used + 1
        message = (
            f"Retrying FLASH for step {state['current_step'] + 1} "
            f"({next_retry_count}/{retry_budget}) after {review['failure_type']} failure."
        )
        print(f"\n[Node: Retry Guard] 🔁 {message}")
        attempt_log.append(message)
        return {
            "active_retry_count": next_retry_count,
            "active_attempt_log": attempt_log,
            "history": [message],
            "status": "flash_retrying",
        }

    exhausted_reason = (
        f"{review['reason']} Retry budget exhausted after {retries_used} retr"
        f"{'y' if retries_used == 1 else 'ies'}."
    )
    print(
        "\n[Node: Retry Guard] ⛔ FLASH retry budget exhausted，记录当前步骤失败并继续后续流程。"
    )
    attempt_log.append(exhausted_reason)
    review = {
        "decision": "record",
        "failure_type": review["failure_type"],
        "reason": exhausted_reason,
    }
    output = state["active_output"].strip()
    if not output or output.startswith("FLASH executor fallback output:"):
        output = (
            f"FLASH execution failed after {retries_used} retr"
            f"{'y' if retries_used == 1 else 'ies'} "
            f"({review['failure_type']}): {review['reason']}"
        )
    return {
        "active_output": output,
        "active_flash_review": review,
        "active_attempt_log": attempt_log,
        "history": [f"FLASH retry budget exhausted on step {state['current_step'] + 1}; recording failure."],
        "status": "flash_retry_exhausted",
    }


def route_after_retry_guard(state: RouterState) -> str:
    if state["status"] == "flash_retrying":
        return "retry_flash"
    return "recorder"


def retry_flash_node(state: RouterState) -> RouterState:
    print("\n[Node: Retry FLASH] ⚡ 准备重新执行 FLASH 子任务...")
    return {
        "active_output": "",
        "active_last_error": "",
        "history": [f"Retrying FLASH executor on step {state['current_step'] + 1} after review classification."],
        "status": "retrying_flash",
    }


def escalation_node(state: RouterState) -> RouterState:
    review = state["active_flash_review"]
    print(
        "\n[Node: Escalation] 🧠 FLASH 结果不足或不适配，升级到 PRO 执行..."
    )
    attempt_log = list(state["active_attempt_log"])
    message = (
        f"Escalated step {state['current_step'] + 1} from FLASH to PRO "
        f"because {review['failure_type']}: {review['reason']}"
    )
    attempt_log.append(message)
    return {
        "active_route": PRO,
        "active_model_name": state["pro_model"],
        "active_escalated_from_flash": True,
        "active_used_provider_fallback": False,
        "active_attempt_log": attempt_log,
        "history": [message],
        "status": "escalated_to_pro",
    }


def record_step_node(state: RouterState) -> RouterState:
    step_number = state["current_step"] + 1
    route = state["active_route"] or PRO
    planned_route = normalize_route(state["active_subtask"].get("model"), default=route)
    model_name = state["active_model_name"] or (
        state["pro_model"] if route == PRO else state["flash_model"]
    )
    desc = state["active_subtask"].get("desc", "N/A")
    result: StepResult = {
        "step": step_number,
        "subtask_id": str(state["active_subtask"].get("id") or f"S{step_number}"),
        "depends_on": list(state["active_subtask"].get("depends_on", [])),
        "planned_route": planned_route,
        "route": PRO if route == PRO else FLASH,
        "model_name": model_name,
        "desc": desc,
        "output": state["active_output"],
        "status": state["status"],
        "attempt_count": state["active_attempt_count"],
        "retry_count": state["active_retry_count"],
        "escalated_from_flash": state["active_escalated_from_flash"],
        "used_provider_fallback": state["active_used_provider_fallback"],
        "flash_review": state["active_flash_review"],
        "attempt_log": list(state["active_attempt_log"]),
    }

    print(
        f"[Node: Recorder] 已记录步骤 {step_number} -> {result['route']} ({result['model_name']})"
    )

    return {
        "results": [result],
        "history": [f"Recorded step {step_number}: {desc}"],
        "current_step": step_number,
        "active_subtask": {},
        "active_route": "",
        "active_model_name": "",
        "active_output": "",
        "active_last_error": "",
        "active_attempt_count": 0,
        "active_retry_count": 0,
        "active_escalated_from_flash": False,
        "active_used_provider_fallback": False,
        "active_flash_review": empty_flash_review(),
        "active_attempt_log": [],
        "active_invocation_result": empty_model_invocation_result(),
        "status": "recorded",
    }


def build_fallback_report(state: RouterState, finalizer_error: str = "") -> str:
    lines = [
        "路由执行摘要",
        f"- 原始任务: {state['task']}",
        f"- 规划模型: {state['planner_model']}",
        f"- 判定模型: {state['judge_model']}",
        f"- PRO 模型: {state['pro_model']}",
        f"- FLASH 模型: {state['flash_model']}",
        f"- 已完成步骤数: {len(state['results'])}",
    ]
    for result in state["results"]:
        detail_bits: List[str] = []
        if result["planned_route"] != result["route"]:
            detail_bits.append(f"planned={result['planned_route']}")
        if result["retry_count"] > 0:
            detail_bits.append(f"retries={result['retry_count']}")
        if result["escalated_from_flash"]:
            detail_bits.append("escalated")
        if result["used_provider_fallback"]:
            detail_bits.append("provider_fallback")
        flash_review = result["flash_review"]
        if flash_review["failure_type"] != "none":
            detail_bits.append(f"failure={flash_review['failure_type']}")
        detail_suffix = f" ({', '.join(detail_bits)})" if detail_bits else ""
        lines.append(
            f"  {result['step']}. [{result['route']}] {result['desc']}{detail_suffix} -> "
            f"{compact_text(result['output'], 140)}"
        )
        if flash_review["reason"]:
            lines.append(f"     cascade: {compact_text(flash_review['reason'], 140)}")
    if state["errors"] or finalizer_error:
        lines.append("- 回退/异常:")
        for error in state["errors"]:
            lines.append(f"  - {error}")
        if finalizer_error:
            lines.append(f"  - Finalizer fallback: {finalizer_error}")
    finalizer_outcome = state["finalizer_outcome"]
    if finalizer_outcome["status"] not in {"", "not_started"}:
        lines.append("- Finalizer path:")
        lines.append(
            f"  - route={finalizer_outcome['route']} model={finalizer_outcome['model_name'] or 'deterministic'} "
            f"status={finalizer_outcome['status']}"
        )
        if finalizer_outcome["reason"]:
            lines.append(f"  - reason: {finalizer_outcome['reason']}")
    return "\n".join(lines)


def has_distinct_finalizer_model_path(state: RouterState) -> bool:
    flash_candidates = [
        normalize_model_name(model)
        for model in dedupe_model_sequence(
            state["flash_model"], state["flash_fallback_models"]
        )
    ]
    pro_candidates = [
        normalize_model_name(model)
        for model in dedupe_model_sequence(
            state["pro_model"], state["pro_fallback_models"]
        )
    ]
    return any(candidate and candidate not in flash_candidates for candidate in pro_candidates)



def build_finalizer_prompt(state: RouterState, route: Literal["PRO", "FLASH"]) -> str:
    finalizer_context = build_finalizer_context_pack_json(state, route)
    role = "FLASH summarizer" if route == FLASH else "PRO summarizer"
    route_instruction = (
        "Write a concise final report with three sections: Routing Summary, Step Outcomes, Next Action. Use the Technical Metadata blocks for precise facts."
        if route == FLASH
        else "Write a concise but higher-signal final report with three sections: Routing Summary, Step Outcomes, Next Action. Use the compact execution results and Technical Metadata blocks for precision."
    )
    return (
        f"Role: {role}.\n"
        f"Finalizer context JSON:\n{finalizer_context}\n"
        f"{route_instruction}"
    )



def verify_finalizer_output(report: str) -> tuple[bool, str]:
    stripped = report.strip()
    if not stripped:
        return False, "Finalizer returned empty output."
    lowered = " ".join(stripped.split()).lower()
    if contains_any(lowered, LOW_QUALITY_OUTPUT_MARKERS):
        return False, "Finalizer output explicitly signaled inability to finish."
    if len(stripped) < 80:
        return False, "Finalizer output was too short for a useful final report."
    return True, "Finalizer output passed heuristic verification."


def flash_finalizer_node(state: RouterState) -> Dict[str, Any]:
    print("\n[Node: FLASH Finalizer Invoke] 🧾 正在生成最终路由报告...")
    attempt_log: List[str] = []
    flash_invocation = invoke_with_provider_fallback(
        state["flash_model"],
        state["flash_fallback_models"],
        build_finalizer_prompt(state, FLASH),
        timeout=resolve_positive_int(
            None,
            "ROUTER_FINALIZER_TIMEOUT",
            DEFAULT_FLASH_FINALIZER_TIMEOUT,
        ),
        num_predict=320,
        temperature=0.0,
        label="Finalizer FLASH",
        attempt_log=attempt_log,
    )
    return {
        "finalizer_invocation_result": flash_invocation,
        "finalizer_attempt_log": flash_invocation["attempt_log"],
        "status": "flash_finalizer_invoked",
    }


def flash_finalizer_verify_node(state: RouterState) -> Dict[str, Any]:
    print("\n[Node: FLASH Finalizer Verify] 验证 FLASH 最终报告...")
    flash_invocation = state["finalizer_invocation_result"]
    attempt_log = list(state["finalizer_attempt_log"])
    if flash_invocation["success"]:
        passed, reason = verify_finalizer_output(flash_invocation["output"])
        if passed:
            finalizer_outcome = {
                "route": FLASH,
                "model_name": flash_invocation["model_name"],
                "status": "finished",
                "used_provider_fallback": flash_invocation["used_provider_fallback"],
                "reason": reason,
                "attempt_log": attempt_log,
            }
            print(
                "✅ 最终报告生成成功。"
                f"{' (provider fallback)' if flash_invocation['used_provider_fallback'] else ''}"
            )
            return {
                "final_report": flash_invocation["output"],
                "finalizer_outcome": finalizer_outcome,
                "finalizer_attempt_log": attempt_log,
                "finalizer_error": "",
                "finalizer_flash_reason": reason,
                "status": "finalizer_finished",
            }

        attempt_log.append(f"Finalizer FLASH output rejected: {reason}")
        print(f"⚠️ FLASH finalizer 输出不足，准备升级到 PRO。原因: {reason}")
        return {
            "finalizer_attempt_log": attempt_log,
            "finalizer_error": f"FLASH finalizer rejected: {reason}",
            "finalizer_flash_reason": reason,
            "status": "finalizer_flash_rejected",
        }

    if (
        flash_invocation["failure_type"] != "capability_quality"
        and not has_distinct_finalizer_model_path(state)
    ):
        attempt_log.append(
            "Skipped PRO finalizer escalation because no distinct finalizer model path was available after FLASH failed."
        )
        finalizer_error = (
            f"FLASH finalizer failed: {flash_invocation['error_text']}; "
            "skipped redundant PRO cascade because PRO would reuse the same effective model path"
        )
        print("⚠️ FLASH finalizer 失败且 PRO 无新增模型路径，准备进入确定性回退报告节点。")
        return {
            "finalizer_attempt_log": attempt_log,
            "finalizer_error": finalizer_error,
            "finalizer_flash_reason": flash_invocation["error_text"],
            "status": "finalizer_deterministic_needed",
        }

    attempt_log.append(
        f"Finalizer FLASH failed with {flash_invocation['failure_type']}; escalating to PRO finalizer."
    )
    print(
        f"⚠️ FLASH finalizer 调用失败，准备升级到 PRO。原因: {flash_invocation['error_text']}"
    )
    return {
        "finalizer_attempt_log": attempt_log,
        "finalizer_error": f"FLASH finalizer failed: {flash_invocation['error_text']}",
        "finalizer_flash_reason": flash_invocation["error_text"],
        "status": "finalizer_flash_failed",
    }


def route_after_flash_finalizer_verify(state: RouterState) -> str:
    if state["status"] == "finalizer_finished":
        return "finalizer_complete"
    if state["status"] == "finalizer_deterministic_needed":
        return "deterministic_finalizer"
    return "pro_finalizer"



def extract_technical_metadata_node(state: RouterState) -> Dict[str, Any]:
    results = state.get("results", [])
    if not results:
        print("\n[Node: Metadata Extractor] 🔍 No recorded step available for metadata extraction.")
        return {"history": ["Metadata extraction skipped because no step result was recorded."]}

    latest_result = results[-1]
    return {"history": extract_technical_metadata_for_result(state, latest_result)}


def pro_finalizer_node(state: RouterState) -> Dict[str, Any]:
    print("\n[Node: PRO Finalizer Invoke] 🧠 正在级联生成最终路由报告...")
    attempt_log = list(state["finalizer_attempt_log"])
    pro_invocation = invoke_with_provider_fallback(
        state["pro_model"],
        state["pro_fallback_models"],
        build_finalizer_prompt(state, PRO),
        timeout=resolve_positive_int(
            None,
            "ROUTER_FINALIZER_TIMEOUT",
            DEFAULT_PRO_FINALIZER_TIMEOUT,
        ),
        num_predict=420,
        temperature=0.0,
        label="Finalizer PRO",
        attempt_log=attempt_log,
    )
    return {
        "finalizer_invocation_result": pro_invocation,
        "finalizer_attempt_log": pro_invocation["attempt_log"],
        "status": "pro_finalizer_invoked",
    }


def pro_finalizer_verify_node(state: RouterState) -> Dict[str, Any]:
    print("\n[Node: PRO Finalizer Verify] 验证 PRO 最终报告...")
    pro_invocation = state["finalizer_invocation_result"]
    attempt_log = list(state["finalizer_attempt_log"])
    flash_reason = state["finalizer_flash_reason"]

    if pro_invocation["success"]:
        pro_passed, pro_reason = verify_finalizer_output(pro_invocation["output"])
        if pro_passed:
            reason_prefix = (
                "Escalated after FLASH finalizer rejection"
                if "rejected" in state["finalizer_error"]
                else "Escalated after FLASH finalizer failure"
            )
            finalizer_outcome = {
                "route": PRO,
                "model_name": pro_invocation["model_name"],
                "status": "finished",
                "used_provider_fallback": pro_invocation["used_provider_fallback"],
                "reason": f"{reason_prefix}: {flash_reason}",
                "attempt_log": attempt_log,
            }
            print(
                "✅ 最终报告通过 PRO 级联生成成功。"
                f"{' (provider fallback)' if pro_invocation['used_provider_fallback'] else ''}"
            )
            return {
                "final_report": pro_invocation["output"],
                "finalizer_outcome": finalizer_outcome,
                "finalizer_attempt_log": attempt_log,
                "status": "finalizer_finished",
            }

        finalizer_error = f"{state['finalizer_error']}; PRO finalizer rejected: {pro_reason}"
        print("⚠️ PRO finalizer 输出不足，准备进入确定性回退报告节点。")
        return {
            "finalizer_attempt_log": attempt_log,
            "finalizer_error": finalizer_error,
            "status": "finalizer_deterministic_needed",
        }

    finalizer_error = f"{state['finalizer_error']}; PRO finalizer failed: {pro_invocation['error_text']}"
    print("⚠️ PRO finalizer 级联失败，准备进入确定性回退报告节点。")
    return {
        "finalizer_attempt_log": attempt_log,
        "finalizer_error": finalizer_error,
        "status": "finalizer_deterministic_needed",
    }


def route_after_pro_finalizer_verify(state: RouterState) -> str:
    if state["status"] == "finalizer_finished":
        return "finalizer_complete"
    return "deterministic_finalizer"


def deterministic_finalizer_node(state: RouterState) -> RouterState:
    print("\n[Node: Deterministic Finalizer] 🧾 使用确定性模板生成最终路由报告...")
    finalizer_error = state["finalizer_error"]
    final_report = build_fallback_report(state, finalizer_error)
    finalizer_outcome = {
        "route": "DETERMINISTIC",
        "model_name": "",
        "status": "deterministic_fallback",
        "used_provider_fallback": False,
        "reason": finalizer_error,
        "attempt_log": list(state["finalizer_attempt_log"]),
    }
    return {
        "final_report": final_report,
        "finalizer_outcome": finalizer_outcome,
        "status": "finalizer_finished",
    }


def finalizer_complete_node(state: RouterState) -> RouterState:
    token_usage = get_token_usage_records(state["run_id"])
    token_usage_summary = summarize_token_usage_records(token_usage)
    token_usage_history: List[str] = ["Finalizer completed."]
    print("\n" + "=" * 58)
    print(state["final_report"])
    print("-" * 58)
    print(format_token_usage_summary(token_usage_summary))
    try:
        ledger_path = persist_token_usage_ledger(
            token_usage,
            token_usage_summary,
            state=state,
        )
        if ledger_path:
            print(f"- Ledger: {ledger_path}")
            token_usage_history.append(f"Token usage ledger appended: {ledger_path}")
    except Exception as exc:
        error_text = compact_text(str(exc), 220)
        print(f"- Ledger write failed: {error_text}")
        token_usage_history.append(f"Token usage ledger write failed: {error_text}")
    print("=" * 58)

    return {
        "history": token_usage_history,
        "token_usage": token_usage,
        "token_usage_summary": token_usage_summary,
        "status": "finished",
    }


def build_router_graph():
    workflow = StateGraph(RouterState)
    workflow.add_node("planner_warmup", planner_warmup_node)
    workflow.add_node("planner_invoke", planner_invoke_node)
    workflow.add_node("planner_parse", planner_parse_node)
    workflow.add_node("planner_fallback", planner_fallback_node)
    workflow.add_node("dependency_judge", dependency_judge_node)
    workflow.add_node("dependency_validate", dependency_validate_node)
    workflow.add_node("planner_ready", planner_ready_node)
    workflow.add_node("judge_warmup", judge_warmup_node)
    workflow.add_node("judge_subtask", judge_subtask_node)
    workflow.add_node("assemble_plan", assemble_plan_node)
    workflow.add_node("dependency_scheduler", dependency_scheduler_node)
    workflow.add_node("parallel_executor", parallel_executor_node)
    workflow.add_node("dependency_execution_join", dependency_execution_join_node)
    workflow.add_node("dependency_deadlock", dependency_deadlock_node)
    workflow.add_node("execution_finalize_join", execution_finalize_join_node)
    workflow.add_node("flash_finalizer", flash_finalizer_node)
    workflow.add_node("flash_finalizer_verify", flash_finalizer_verify_node)
    workflow.add_node("pro_finalizer", pro_finalizer_node)
    workflow.add_node("pro_finalizer_verify", pro_finalizer_verify_node)
    workflow.add_node("deterministic_finalizer", deterministic_finalizer_node)
    workflow.add_node("finalizer_complete", finalizer_complete_node)

    workflow.add_edge(START, "planner_warmup")
    workflow.add_conditional_edges(
        "planner_warmup",
        route_after_planner_warmup,
        {
            "planner_warmup": "planner_warmup",
            "planner_invoke": "planner_invoke",
        },
    )
    workflow.add_conditional_edges(
        "planner_invoke",
        route_after_planner_invoke,
        {
            "planner_parse": "planner_parse",
            "planner_fallback": "planner_fallback",
        },
    )
    workflow.add_conditional_edges(
        "planner_parse",
        route_after_planner_parse,
        {
            "dependency_judge": "dependency_judge",
            "planner_fallback": "planner_fallback",
        },
    )
    workflow.add_edge("planner_fallback", "dependency_judge")
    workflow.add_edge("dependency_judge", "dependency_validate")
    workflow.add_edge("dependency_validate", "planner_ready")
    workflow.add_edge("planner_ready", "judge_warmup")
    workflow.add_conditional_edges("judge_warmup", route_to_judge_subtasks)
    workflow.add_edge("judge_subtask", "assemble_plan")
    workflow.add_edge("assemble_plan", "dependency_scheduler")
    workflow.add_conditional_edges("dependency_scheduler", route_to_ready_executor_subtasks)
    workflow.add_edge("parallel_executor", "dependency_execution_join")
    workflow.add_edge("dependency_execution_join", "dependency_scheduler")
    workflow.add_edge("dependency_deadlock", "execution_finalize_join")
    workflow.add_edge("execution_finalize_join", "flash_finalizer")
    workflow.add_edge("flash_finalizer", "flash_finalizer_verify")
    workflow.add_conditional_edges(
        "flash_finalizer_verify",
        route_after_flash_finalizer_verify,
        {
            "pro_finalizer": "pro_finalizer",
            "deterministic_finalizer": "deterministic_finalizer",
            "finalizer_complete": "finalizer_complete",
        },
    )
    workflow.add_edge("pro_finalizer", "pro_finalizer_verify")
    workflow.add_conditional_edges(
        "pro_finalizer_verify",
        route_after_pro_finalizer_verify,
        {
            "deterministic_finalizer": "deterministic_finalizer",
            "finalizer_complete": "finalizer_complete",
        },
    )
    workflow.add_edge("deterministic_finalizer", "finalizer_complete")
    workflow.add_edge("finalizer_complete", END)
    return workflow.compile()


def resolve_graph_max_concurrency(explicit_value: int | None, state: RouterState) -> int | None:
    resolved = resolve_optional_positive_int(explicit_value, "ROUTER_MAX_CONCURRENCY")
    if resolved is not None:
        return resolved
    if is_large_model(state["judge_model"]):
        return 1
    return None


def build_graph_config(
    recursion_limit: int,
    max_concurrency: int | None = None,
    state: RouterState | None = None,
) -> Dict[str, Any]:
    config: Dict[str, Any] = {"recursion_limit": recursion_limit}
    if max_concurrency is not None:
        config["max_concurrency"] = max_concurrency
    if state is not None:
        config["run_name"] = "super-router"
        config["tags"] = parse_langsmith_tags()
        config["metadata"] = build_langsmith_metadata(state)
    return config


def prepare_router_run(
    user_task: str,
    *,
    planner_model: str | None = None,
    judge_model: str | None = None,
    pro_model: str | None = None,
    flash_model: str | None = None,
    pro_fallback_models: List[str] | None = None,
    flash_fallback_models: List[str] | None = None,
    flash_retry_budget: int | None = None,
    recursion_limit: int | None = None,
    max_concurrency: int | None = None,
):
    graph = build_router_graph()
    initial_state = create_initial_state(
        user_task,
        planner_model=planner_model,
        judge_model=judge_model,
        pro_model=pro_model,
        flash_model=flash_model,
        pro_fallback_models=pro_fallback_models,
        flash_fallback_models=flash_fallback_models,
        flash_retry_budget=flash_retry_budget,
    )
    resolved_recursion_limit = resolve_positive_int(
        recursion_limit,
        "ROUTER_RECURSION_LIMIT",
        DEFAULT_ROUTER_RECURSION_LIMIT,
    )
    resolved_max_concurrency = resolve_graph_max_concurrency(max_concurrency, initial_state)
    return graph, initial_state, resolved_recursion_limit, resolved_max_concurrency


def create_initial_state(
    task: str,
    *,
    planner_model: str | None = None,
    judge_model: str | None = None,
    pro_model: str | None = None,
    flash_model: str | None = None,
    pro_fallback_models: List[str] | None = None,
    flash_fallback_models: List[str] | None = None,
    flash_retry_budget: int | None = None,
) -> RouterState:
    resolved_planner = resolve_model(planner_model, "ROUTER_PLANNER_MODEL", DEFAULT_PLANNER_MODEL)
    resolved_judge = resolve_model(judge_model, "ROUTER_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)
    resolved_pro = resolve_execution_model(pro_model, "ROUTER_PRO_MODEL", DEFAULT_PRO_MODEL)
    resolved_flash = resolve_execution_model(flash_model, "ROUTER_FLASH_MODEL", DEFAULT_FLASH_MODEL)
    resolved_pro_fallback_models = resolve_model_list(
        pro_fallback_models,
        "ROUTER_PRO_FALLBACK_MODELS",
    )
    resolved_flash_fallback_models = resolve_model_list(
        flash_fallback_models,
        "ROUTER_FLASH_FALLBACK_MODELS",
    )
    resolved_flash_retry_budget = resolve_non_negative_int(
        flash_retry_budget,
        "ROUTER_FLASH_RETRY_BUDGET",
        DEFAULT_FLASH_RETRY_BUDGET,
    )
    return {
        "run_id": str(uuid.uuid4()),
        "task": task,
        "planner_model": resolved_planner,
        "judge_model": resolved_judge,
        "pro_model": resolved_pro,
        "flash_model": resolved_flash,
        "pro_fallback_models": resolved_pro_fallback_models,
        "flash_fallback_models": resolved_flash_fallback_models,
        "flash_retry_budget": resolved_flash_retry_budget,
        "planned_subtasks": [],
        "planner_raw_text": "",
        "planner_error": "",
        "dependency_raw_text": "",
        "dependency_error": "",
        "dependency_issues": [],
        "dependency_confidence": 0.0,
        "planner_warmup_attempt": 0,
        "judge_warmup_done": False,
        "subtasks": [],
        "judge_index": 0,
        "judge_desc": "",
        "judge_results": {},
        "execution_index": 0,
        "execution_subtask": {},
        "execution_results": {},
        "execution_context_results": [],
        "current_step": 0,
        "active_subtask": {},
        "active_route": "",
        "active_model_name": "",
        "active_output": "",
        "active_last_error": "",
        "active_attempt_count": 0,
        "active_retry_count": 0,
        "active_escalated_from_flash": False,
        "active_used_provider_fallback": False,
        "active_flash_review": empty_flash_review(),
        "active_attempt_log": [],
        "active_invocation_result": empty_model_invocation_result(),
        "results": [],
        "history": [],
        "errors": [],
        "status": "created",
        "final_report": "",
        "finalizer_outcome": empty_finalizer_outcome(),
        "finalizer_attempt_log": [],
        "finalizer_error": "",
        "finalizer_flash_reason": "",
        "finalizer_invocation_result": empty_model_invocation_result(),
        "token_usage": [],
        "token_usage_summary": empty_token_usage_summary(),
    }


def unpack_stream_event(event: Any) -> tuple[str | None, Any]:
    if isinstance(event, tuple):
        if len(event) == 3:
            _, mode, payload = event
            return str(mode), payload
        if len(event) == 2:
            mode, payload = event
            return str(mode), payload
    return None, event


def summarize_stream_update(node_name: str, update: Any) -> str:
    if not isinstance(update, dict):
        return f"[LangGraph Stream] {node_name} completed | payload={compact_text(str(update), 120)}"

    details: List[str] = []
    if "status" in update:
        details.append(f"status={update['status']}")
    if "planned_subtasks" in update:
        details.append(f"planned_subtasks={len(update['planned_subtasks'])}")
    if "subtasks" in update:
        details.append(f"subtasks={len(update['subtasks'])}")
    if "execution_results" in update:
        details.append(f"execution_results={len(update['execution_results'])}")
    if "execution_context_results" in update:
        details.append(f"context_results={len(update['execution_context_results'])}")
    if "current_step" in update:
        details.append(f"current_step={update['current_step']}")
    if "active_route" in update and update["active_route"]:
        details.append(f"route={update['active_route']}")
    if "active_model_name" in update and update["active_model_name"]:
        details.append(f"model={update['active_model_name']}")
    active_subtask = update.get("active_subtask")
    if isinstance(active_subtask, dict) and active_subtask.get("desc"):
        details.append(f"subtask={compact_text(str(active_subtask['desc']), 80)}")
    flash_review = update.get("active_flash_review")
    if isinstance(flash_review, dict) and flash_review.get("decision"):
        details.append(
            "flash_review="
            f"{flash_review['decision']}/{flash_review.get('failure_type', 'none')}"
        )
    if "results" in update:
        details.append(f"results={len(update['results'])}")
    if "errors" in update and isinstance(update["errors"], list) and update["errors"]:
        details.append(f"errors={len(update['errors'])}")
    if "final_report" in update and str(update["final_report"]).strip():
        details.append("final_report=ready")
    if not details:
        details.append(f"updated={', '.join(update.keys()) or 'no_fields'}")
    return f"[LangGraph Stream] {node_name} completed | " + " | ".join(details)


def emit_stream_updates(event: Any) -> None:
    if not isinstance(event, dict):
        print(f"[LangGraph Stream] update={compact_text(str(event), 120)}")
        return
    for node_name, update in event.items():
        print(summarize_stream_update(node_name, update))


def observe_stream_event(
    event: Any,
    *,
    final_state: RouterState,
    on_update: Callable[[Any], None] = emit_stream_updates,
) -> RouterState:
    mode, payload = unpack_stream_event(event)
    if mode == "updates":
        on_update(payload)
        return final_state
    if mode == "values" and isinstance(payload, dict):
        return payload
    return final_state


def run_router_app(
    user_task: str,
    *,
    planner_model: str | None = None,
    judge_model: str | None = None,
    pro_model: str | None = None,
    flash_model: str | None = None,
    pro_fallback_models: List[str] | None = None,
    flash_fallback_models: List[str] | None = None,
    flash_retry_budget: int | None = None,
    recursion_limit: int | None = None,
    max_concurrency: int | None = None,
    stream: bool = False,
) -> RouterState:
    graph, initial_state, resolved_recursion_limit, resolved_max_concurrency = prepare_router_run(
        user_task,
        planner_model=planner_model,
        judge_model=judge_model,
        pro_model=pro_model,
        flash_model=flash_model,
        pro_fallback_models=pro_fallback_models,
        flash_fallback_models=flash_fallback_models,
        flash_retry_budget=flash_retry_budget,
        recursion_limit=recursion_limit,
        max_concurrency=max_concurrency,
    )
    graph_config = build_graph_config(
        resolved_recursion_limit,
        resolved_max_concurrency,
        initial_state,
    )
    if resolved_max_concurrency == 1 and is_large_model(initial_state["judge_model"]):
        print("[LangGraph Config] Large Judge model detected; max_concurrency=1 to avoid local model contention.")
    with token_usage_tracking_context(initial_state["run_id"]):
        with langsmith_tracing_context(initial_state):
            if not stream:
                return graph.invoke(
                    initial_state,
                    config=graph_config,
                )

            print("\n[LangGraph Stream] 🔄 节点级流式输出已启用。")
            final_state: RouterState = initial_state
            for event in graph.stream(
                initial_state,
                config=graph_config,
                stream_mode=["updates", "values"],
            ):
                final_state = observe_stream_event(event, final_state=final_state)
            return final_state


def parse_cli_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the LangGraph-based super-router."
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream node-level LangGraph updates during execution.",
    )
    parser.add_argument(
        "task",
        nargs="*",
        help=f"Task description to route. If omitted, {ROUTER_TASK_ENV_VAR} is used when present.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    raw_args = argv if argv is not None else sys.argv[1:]
    parsed_args = parse_cli_args(raw_args)
    task = (
        " ".join(parsed_args.task).strip()
        or os.environ.get(ROUTER_TASK_ENV_VAR, "").strip()
    )
    if not task:
        raise SystemExit(
            f"Task description required. Provide positional args or set {ROUTER_TASK_ENV_VAR}."
        )
    run_router_app(task, stream=parsed_args.stream)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
