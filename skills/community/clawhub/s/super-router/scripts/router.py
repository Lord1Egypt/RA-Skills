from __future__ import annotations

import argparse
import json
import operator
import os
import re
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Annotated, Any, Callable, Dict, List, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

OLLAMA_URL = os.environ.get("ROUTER_OLLAMA_URL", "http://localhost:11434/api/generate")
ROUTER_TASK_ENV_VAR = "ROUTER_TASK"
GEMINI_CLI_PATH = os.environ.get("ROUTER_GEMINI_CLI", shutil.which("gemini") or "/opt/homebrew/bin/gemini")
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
DEFAULT_FLASH_MODEL = "google-gemini-cli/flash"
WARMUP_PROMPT = "Return exactly OK."
GEMINI_PREFLIGHT_RESULTS: Dict[str, str] = {}
GEMINI_NETWORK_PREFLIGHT_RESULT: str | None = None


class PlannedSubtask(TypedDict):
    desc: str


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
    desc: str
    model: Literal["PRO", "FLASH"]
    assessment: ComplexityAssessment


class JudgedSubtask(TypedDict):
    index: int
    subtask: Subtask
    error: str


class StepResult(TypedDict):
    step: int
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


def resolve_model(explicit_value: str | None, env_name: str, fallback: str) -> str:
    if explicit_value and explicit_value.strip():
        return explicit_value.strip()
    env_value = os.environ.get(env_name, "").strip()
    return env_value or fallback


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


def normalize_model_name(model: str) -> str:
    normalized = model.strip()
    if normalized.startswith("google-gemini-cli/"):
        normalized = normalized.split("/", 1)[1]
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
    if summary_like and scores["io_heaviness"] >= 1 and scores["code_change_scope"] <= 1 and scores["risk"] <= 1:
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
    normalized = normalize_model_name(model)
    return normalized in {"auto", "pro", "flash", "flash-lite"} or normalized.startswith("gemini-")


def has_proxy_config() -> bool:
    return any(
        os.environ.get(name, "").strip()
        for name in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy")
    )


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


def ollama_generate(
    model: str,
    prompt: str,
    *,
    timeout: int = 60,
    num_predict: int = 400,
    temperature: float = 0.0,
) -> str:
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
    return text


def invoke_gemini_cli(
    model: str,
    prompt: str,
    *,
    timeout: int = 120,
) -> str:
    normalized_model = normalize_model_name(model)
    if not GEMINI_CLI_PATH or not os.path.exists(GEMINI_CLI_PATH):
        raise RuntimeError("Gemini CLI executable was not found. Set ROUTER_GEMINI_CLI or install `gemini`.")

    env = dict(os.environ)
    env["NO_COLOR"] = "1"
    env["NO_BROWSER"] = "true"
    command = [
        GEMINI_CLI_PATH,
        "-m",
        normalized_model,
        "-p",
        prompt,
        "-o",
        "json"
#        "-e",
#        GEMINI_EXTENSION_NAME,
    ]
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
        raise RuntimeError(f"Gemini CLI timed out after {timeout}s") from exc

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
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
        raise RuntimeError(f"Gemini CLI failed for model {normalized_model}: {error_text}")

    if parsed_payload and isinstance(parsed_payload.get("error"), dict):
        error_block = parsed_payload["error"]
        error_text = compact_text(
            str(error_block.get("message") or error_block.get("type") or payload_text),
            280,
        )
        raise RuntimeError(f"Gemini CLI returned an error for model {normalized_model}: {error_text}")

    if parsed_payload and str(parsed_payload.get("response", "")).strip():
        return str(parsed_payload["response"]).strip()

    if not payload_text:
        raise RuntimeError(f"Gemini CLI returned an empty response for model {normalized_model}")
    return payload_text


def ensure_gemini_cli_ready(model: str) -> None:
    normalized_model = normalize_model_name(model)
    cached_error = GEMINI_PREFLIGHT_RESULTS.get(normalized_model)
    if cached_error is not None:
        if cached_error:
            raise RuntimeError(cached_error)
        return

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
) -> str:
    ensure_gemini_cli_ready(model)
    return invoke_gemini_cli(model, prompt, timeout=timeout)


def generate_text(
    model: str,
    prompt: str,
    *,
    timeout: int = 60,
    num_predict: int = 400,
    temperature: float = 0.0,
) -> str:
    if is_gemini_model(model):
        return gemini_generate(model, prompt, timeout=timeout)
    return ollama_generate(
        model,
        prompt,
        timeout=timeout,
        num_predict=num_predict,
        temperature=temperature,
    )


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


def normalize_planned_subtasks(raw_subtasks: List[Any]) -> List[PlannedSubtask]:
    normalized: List[PlannedSubtask] = []
    for item in raw_subtasks:
        if isinstance(item, dict):
            desc = str(item.get("desc") or item.get("description") or item.get("step") or "").strip()
        else:
            desc = str(item).strip()

        if not desc:
            continue

        normalized.append({"desc": desc})

    if not normalized:
        raise ValueError("Planner did not return any usable subtasks")
    return normalized


def build_fallback_subtasks(task: str) -> List[PlannedSubtask]:
    lowered = task.lower()
    subtasks: List[PlannedSubtask] = []

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

    return subtasks


def build_planner_prompt(task: str) -> str:
    return (
        "Role: Expert Technical Architect and Task Decomposer.\\n"
        f"Task: {task}\\n"
        "Instruction: Break the task into atomic, actionable, and outcome-oriented subtasks. Each subtask must be a discrete unit of work.\\n"
        "CRITICAL FOR PARALLELISM: If the task involves multiple entities, technologies, or components (e.g., 3 different model families, 5 providers, 10 files), you MUST create a separate subtask for EACH individual entity. Do not group them into a single 'Research' or 'Analysis' phase. One entity = One subtask.\\n"
        "TECHNICAL GOLD REQUIREMENT: For each research or analysis subtask, explicitly aim to identify quantitative metrics, specific version numbers, architectural constants, and hard limits. This 'Technical Gold' is required for the final synthesis.\\n"
        "Structure: When a task mixes investigation and reporting, keep the reporting/update step separate from the investigation step.\\n"
        "Artifacts: If the task asks for a summary, update, impact note, or table, you MUST emit that as its own final subtask.\\n"
        "Do not assign model labels, complexity labels, or scores.\\n"
        "Output rules: Return a raw JSON array only. Each item must be an object with key 'desc'.\\n"
        "Example 1 (Parallel): Research the KV cache of Llama-3 and Mistral-v0.3.\\n"
        "Example 1 Output: [{\"desc\":\"Analyze Llama-3 KV cache implementation and bandwidth metrics\"},{\"desc\":\"Analyze Mistral-v0.3 KV cache implementation and bandwidth metrics\"},{\"desc\":\"Synthesize a technical comparison table of KV cache metrics\"}]\\n"
        "Example 2: Debug an API failure and send a la-concise team update.\\n"
        "Example 2 Output: [{\"desc\":\"Inspect the failing API path and isolate the root cause\"},{\"desc\":\"Prepare a concise team status update with the findings\"}]\\n"
        "JSON Output:"
    )


def build_judge_prompt(task: str, subtask_desc: str) -> str:
    return (
        "Role: Complexity judge for model routing.\n"
        f"Original task: {task}\n"
        f"Subtask: {subtask_desc}\n"
        "Judge the subtask itself, but use the original task to understand domain risk. Only avoid inheriting the overall-task complexity when the subtask is purely a summary, report, or status update.\n"
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


def build_subtask(desc: str, assessment: ComplexityAssessment) -> Subtask:
    return {
        "desc": desc,
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
        print(
            f"步骤 {index}: {icon}| score={assessment['complexity_score']} "
            f"| conf={assessment['confidence']:.2f} | {step['desc']}"
        )
        print(
            f"         判定依据: {assessment['reason']} "
            f"({assessment['judge_source']}, suggested={assessment['suggested_route']})"
        )
    print("=" * 58)


def planner_warmup_node(state: RouterState) -> Dict[str, Any]:
    attempt = state["planner_warmup_attempt"] + 1
    if attempt == 1:
        print("\n[Node: Planner Warmup] 🔥 Warming up planner model with a LangGraph loop...")
    try:
        generate_text(state["planner_model"], WARMUP_PROMPT, timeout=180, num_predict=4)
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
        raw_text = generate_text(
            state["planner_model"],
            build_planner_prompt(state["task"]),
            timeout=300,  # 5 minutes for large models like gemma4:26b
            num_predict=409600,  # Increased for full JSON array output from large models
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
    return "planner_ready"


def planner_fallback_node(state: RouterState) -> Dict[str, Any]:
    planned_subtasks = build_fallback_subtasks(state["task"])
    planned_subtasks = ensure_communication_subtask(state["task"], planned_subtasks)
    error_text = state["planner_error"] or "Unknown planner failure"
    print(f"⚠️ 规划器异常：{error_text}。已切换到启发式回退规划。")
    return {
        "planned_subtasks": planned_subtasks,
        "errors": [f"Planner fallback: {error_text}"],
        "status": "planner_fallback",
    }


def planner_ready_node(state: RouterState) -> Dict[str, Any]:
    return {
        "subtasks": [],
        "current_step": 0,
        "history": [f"Planner produced {len(state['planned_subtasks'])} planned subtasks."],
        "status": "planned",
    }


def judge_warmup_node(state: RouterState) -> Dict[str, Any]:
    print("\n[Node: Judge Warmup] 🔥 Warming up judge model before LangGraph fanout...")
    try:
        generate_text(state["judge_model"], WARMUP_PROMPT, timeout=180, num_predict=4)
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
    desc = state["judge_desc"]
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
                "subtask": build_subtask(desc, assessment),
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

    prompt = (
        f"Task: {state['task']}\n"
        f"Subtask: {result['desc']}\n"
        f"Output: {active_output}\n\n"
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
    prompt_state = dict(state)
    prompt_state.update(
        {
            "results": list(state["execution_context_results"] or state["results"]),
            "current_step": index - 1,
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
    completed_results = state["results"]
    completed_context = "\n".join(
        [
            f"- Step {result['step']} [{result['route']}]: {result['desc']} => {compact_text(result['output'], 160)}"
            for result in completed_results
        ]
    ) or "None"

    assessment = state["active_subtask"].get("assessment") or {}
    route_reason = str(assessment.get("reason", "N/A"))
    route_score = assessment.get("complexity_score", "N/A")
    route_confidence = assessment.get("confidence", "N/A")
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
        f"Original task: {state['task']}\n"
        f"Current subtask: {state['active_subtask'].get('desc', 'N/A')}\n"
        f"Routing rationale: route={route}, score={route_score}, confidence={route_confidence}, reason={route_reason}\n"
        f"{escalation_context}"
        f"Completed context:\n{completed_context}\n"
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
    results_json = json.dumps(state["results"], ensure_ascii=False, indent=2)
    
    # Collect all technical metadata markers from history
    metadata_blocks = [line for line in state["history"] if "TECHNICAL METADATA STEP" in line]
    metadata_context = "\n".join(metadata_blocks) if metadata_blocks else "No technical metadata extracted."

    role = "FLASH summarizer" if route == FLASH else "PRO summarizer"
    route_instruction = (
        "Write a concise final report with three sections: Routing Summary, Step Outcomes, Next Action. Use the Technical Metadata blocks for precise facts."
        if route == FLASH
        else "Write a concise but higher-signal final report with three sections: Routing Summary, Step Outcomes, Next Action. Use the Technical Metadata blocks for precision, but refer back to the Execution Log for full context if needed."
    )
    return (
        f"Role: {role}.\n"
        f"Original task: {state['task']}\n"
        f"Planner model: {state['planner_model']}\n"
        f"Judge model: {state['judge_model']}\n"
        f"Technical Data Gold:\n{metadata_context}\n\n"
        f"Execution log JSON:\n{results_json}\n"
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
    print("\n" + "=" * 58)
    print(state["final_report"])
    print("=" * 58)

    return {
        "history": ["Finalizer completed."],
        "status": "finished",
    }


def build_router_graph():
    workflow = StateGraph(RouterState)
    workflow.add_node("planner_warmup", planner_warmup_node)
    workflow.add_node("planner_invoke", planner_invoke_node)
    workflow.add_node("planner_parse", planner_parse_node)
    workflow.add_node("planner_fallback", planner_fallback_node)
    workflow.add_node("planner_ready", planner_ready_node)
    workflow.add_node("judge_warmup", judge_warmup_node)
    workflow.add_node("judge_subtask", judge_subtask_node)
    workflow.add_node("assemble_plan", assemble_plan_node)
    workflow.add_node("parallel_executor", parallel_executor_node)
    workflow.add_node("parallel_execution_join", parallel_execution_join_node)
    workflow.add_node("deferred_executor", parallel_executor_node)
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
            "planner_ready": "planner_ready",
            "planner_fallback": "planner_fallback",
        },
    )
    workflow.add_edge("planner_fallback", "planner_ready")
    workflow.add_edge("planner_ready", "judge_warmup")
    workflow.add_conditional_edges("judge_warmup", route_to_judge_subtasks)
    workflow.add_edge("judge_subtask", "assemble_plan")
    workflow.add_conditional_edges("assemble_plan", route_to_parallel_executor_subtasks)
    workflow.add_edge("parallel_executor", "parallel_execution_join")
    workflow.add_conditional_edges("parallel_execution_join", route_to_deferred_executor_subtasks)
    workflow.add_edge("deferred_executor", "execution_finalize_join")
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


def build_graph_config(recursion_limit: int, max_concurrency: int | None = None) -> Dict[str, int]:
    config = {"recursion_limit": recursion_limit}
    if max_concurrency is not None:
        config["max_concurrency"] = max_concurrency
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
    resolved_planner = resolve_model(planner_model, "ROUTER_PLANNER_MODEL", "gemma4:26b")
    resolved_judge = resolve_model(judge_model, "ROUTER_JUDGE_MODEL", "llama3.1:8b")
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
    graph_config = build_graph_config(resolved_recursion_limit, resolved_max_concurrency)
    if resolved_max_concurrency == 1 and is_large_model(initial_state["judge_model"]):
        print("[LangGraph Config] Large Judge model detected; max_concurrency=1 to avoid local model contention.")
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
