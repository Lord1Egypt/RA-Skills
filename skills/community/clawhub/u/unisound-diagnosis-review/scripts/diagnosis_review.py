#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
from urllib import error, parse, request


DEFAULT_DIAGNOSIS_DOC_TYPES = [
    "出院记录",
    "入院记录",
    "首次病程记录",
    "术后首次病程记录",
    "检查记录",
    "检验记录",
    "other",
]

DIAGNOSIS_AUDIT_MAX_WORKERS = 8


@dataclass(frozen=True)
class CaseDiagnosis:
    role: str
    code: str
    name: str


@dataclass(frozen=True)
class DiagnosisGuideline:
    diagnosis_code: str
    diagnosis_name: str
    guideline_text: str
    required_doc_types: list[str]
    source_file: str
    best_pass_rate: float | None = None


@dataclass(frozen=True)
class GuidelineApiSettings:
    base_url: str
    api_key: str = ""
    timeout: int = 30


@dataclass(frozen=True)
class LlmModelSettings:
    name: str
    type: str
    base_url: str
    temperature: float
    api_key: str = ""
    model_id: str = ""


@dataclass(frozen=True)
class LlmSettings:
    default_model: str
    timeout: int
    models: dict[str, LlmModelSettings]


class DiagnosisGuidelineRepository(Protocol):
    def find_diagnosis_guideline_by_code(self, diagnosis_code: str) -> DiagnosisGuideline | None:
        ...


class LlmClient(Protocol):
    def complete(self, prompt: str, model_name: str | None = None) -> str:
        ...


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got: {value}") from exc


def load_guideline_api_settings_from_env() -> GuidelineApiSettings:
    return GuidelineApiSettings(
        base_url=_required_env("GUIDELINE_API_BASE"),
        api_key=os.getenv("GUIDELINE_API_KEY", ""),
        timeout=_env_int("GUIDELINE_API_TIMEOUT", 30),
    )

DEFAULT_LLM_BASE = "https://maas-api.hivoice.cn/v1"
DEFAULT_LLM_MODEL = "u1-insuremed"


def build_internal_llm_settings(
    appkey: str,
    base: str = DEFAULT_LLM_BASE,
    model: str = DEFAULT_LLM_MODEL,
    timeout: int = 0,
) -> LlmSettings:
    return LlmSettings(
        default_model=model,
        timeout=timeout,
        models={
            model: LlmModelSettings(
                name=model,
                type="openai_compatible",
                base_url=base,
                temperature=0.0,
                api_key=appkey,
                model_id=model,
            ),
        },
    )

def _json_value(value: Any, default: Any) -> Any:
    if value is None:
        return default
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return default
    return value


def row_to_diagnosis_guideline(row: dict[str, Any]) -> DiagnosisGuideline:
    required_doc_types = _json_value(row.get("required_doc_types"), [])
    if not isinstance(required_doc_types, list):
        required_doc_types = []
    best_pass_rate = row.get("best_pass_rate")
    return DiagnosisGuideline(
        diagnosis_code=str(row["diagnosis_code"]),
        diagnosis_name=str(row["diagnosis_name"]),
        guideline_text=str(row["guideline_text"]),
        required_doc_types=[str(item) for item in required_doc_types],
        source_file=str(row.get("source_file", "")),
        best_pass_rate=float(best_pass_rate) if best_pass_rate is not None else None,
    )


def _extract_api_payload(response_payload: Any) -> dict[str, Any] | None:
    if not isinstance(response_payload, dict):
        return None
    if response_payload.get("found") is False:
        return None
    for key in ("guideline", "data", "result"):
        value = response_payload.get(key)
        if isinstance(value, dict):
            return value
    return response_payload


class GuidelineApiDiagnosisRepository:
    def __init__(self, settings: GuidelineApiSettings) -> None:
        self._settings = settings

    def _get(self, path: str) -> dict[str, Any] | None:
        url = f"{self._settings.base_url.rstrip('/')}{path}"
        headers = {"Content-Type": "application/json"}
        if self._settings.api_key:
            headers["Authorization"] = f"Bearer {self._settings.api_key}"
        req = request.Request(url=url, headers=headers, method="GET")
        try:
            with request.urlopen(req, timeout=self._settings.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            if exc.code == 404:
                return None
            raise

    def find_diagnosis_guideline_by_code(self, diagnosis_code: str) -> DiagnosisGuideline | None:
        encoded_code = parse.quote(str(diagnosis_code), safe="")
        payload = _extract_api_payload(self._get(f"/api/v1/icd-drg/diagnosis-guidelines/{encoded_code}"))
        if payload is None:
            return None
        return row_to_diagnosis_guideline(payload)


def truncate_text_by_utf8_bytes(text: str, max_bytes: int = 24000) -> str:
    encoded = str(text or "").encode("utf-8")
    if len(encoded) <= max_bytes:
        return str(text or "")
    return encoded[:max_bytes].decode("utf-8", errors="ignore") + "\n...[已截断]"


def parse_json_object(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"<think[^>]*>.*?</think>", "", text or "", flags=re.S | re.I)
    cleaned = re.sub(r"<thinking[^>]*>.*?</thinking>", "", cleaned, flags=re.S | re.I).strip()
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    start = cleaned.find("{")
    if start < 0:
        raise ValueError("模型输出中未找到 JSON 对象")
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(cleaned[start:], start=start):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                parsed = json.loads(cleaned[start : index + 1])
                if not isinstance(parsed, dict):
                    raise ValueError("模型 JSON 输出必须是对象")
                return parsed
    raise ValueError("模型输出中的 JSON 对象不完整")


class HardcodedLlmClient:
    def __init__(self, llm_settings: LlmSettings) -> None:
        self._settings = llm_settings

    def complete(self, prompt: str, model_name: str | None = None) -> str:
        selected_model = model_name or self._settings.default_model
        model_config = self._settings.models.get(selected_model)
        if model_config is None:
            raise ValueError(f"未找到模型配置: {selected_model}")
        payload = {
            "model": model_config.model_id or selected_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": model_config.temperature,
        }
        if model_config.type == "openai_compatible":
            return self._post_chat(
                url=f"{model_config.base_url.rstrip('/')}/chat/completions",
                payload=payload,
                headers={"Authorization": f"Bearer {model_config.api_key}"},
            )
        raise ValueError(f"不支持的模型类型: {model_config.type}")

    def _post_chat(self, url: str, payload: dict[str, Any], headers: dict[str, str]) -> str:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = request.Request(
            url=url,
            data=body,
            headers={"Content-Type": "application/json", **{key: value for key, value in headers.items() if value}},
            method="POST",
        )
        opener = request.urlopen(req) if not self._settings.timeout else request.urlopen(req, timeout=self._settings.timeout)
        with opener as response:
            response_payload = json.loads(response.read().decode("utf-8"))
        choices = response_payload.get("choices") or []
        if not choices:
            return json.dumps(response_payload, ensure_ascii=False)
        message = choices[0].get("message") or {}
        return str(message.get("content", ""))


def normalize_diagnosis_code(value: str) -> str:
    # 移除所有空格，转大写
    normalized = "".join(str(value or "").strip().upper().split())
    # 修正 1 开头误识别为 I 开头（如 110 → I10）
    if re.fullmatch(r"1\d{2}(?:\.[A-Z0-9X.]+)?", normalized):
        return f"I{normalized[1:]}"
    return normalized


def diagnosis_code_lookup_candidates(code: str) -> list[str]:
    """
    生成诊断编码的匹配候选列表，支持从细到粗的层级匹配。

    示例：
    - "I10.x00" → ["I10.x00", "I10.x", "I10"]
    - "G6102" → ["G6102", "G61.02", "G61"]  # 支持无小数点格式
    - "G61 02" → ["G6102", "G61.02", "G61"]
    """
    normalized = normalize_diagnosis_code(code)
    if not normalized:
        return []

    candidates: list[str] = [normalized]

    # 情况1：已有小数点（如 I10.x00）
    if "." in normalized:
        head, tail = normalized.split(".", 1)
        if tail and tail[0] != "X":
            candidates.append(f"{head}.{tail[0]}")
        candidates.append(head)

    # 情况2：无小数点但长度 > 3（如 G6102、I10x00）
    # 尝试在第3位后插入小数点，生成标准格式
    elif len(normalized) > 3:
        # 提取字母前缀和数字部分
        match = re.match(r"^([A-Z])(\d{2})(.*)$", normalized)
        if match:
            letter, first_two_digits, rest = match.groups()
            head = f"{letter}{first_two_digits}"

            # 生成带小数点的候选（如 G6102 → G61.02）
            if rest:
                candidates.append(f"{head}.{rest}")

            # 添加类目级别（如 G61）
            candidates.append(head)

    return list(dict.fromkeys(candidate for candidate in candidates if candidate))


def find_diagnosis_guideline(
    guideline_repository: DiagnosisGuidelineRepository,
    diagnosis_code: str,
) -> DiagnosisGuideline | None:
    for candidate in diagnosis_code_lookup_candidates(diagnosis_code):
        guideline = guideline_repository.find_diagnosis_guideline_by_code(candidate)
        if guideline is not None:
            return guideline
    return None


def _record_id(payload: dict[str, Any]) -> str:
    hospital_id = str(payload.get("hospitalId", "")).strip()
    serial_num = str(payload.get("serialNum", "")).strip()
    return "_".join(part for part in [hospital_id, serial_num] if part)


def extract_case_diagnoses(record_payload: dict[str, Any]) -> list[CaseDiagnosis]:
    diagnosis_payload = record_payload.get("diagnosis") or {}
    diagnoses: list[CaseDiagnosis] = []

    primary = diagnosis_payload.get("primaryDiagnosis") or {}
    if primary.get("code") or primary.get("name"):
        diagnoses.append(
            CaseDiagnosis(
                role="primary",
                code=normalize_diagnosis_code(str(primary.get("code", "")).strip()),
                name=str(primary.get("name", "")).strip(),
            )
        )

    for diagnosis in diagnosis_payload.get("otherDiagnoses") or []:
        if not isinstance(diagnosis, dict):
            continue
        code = normalize_diagnosis_code(str(diagnosis.get("code", "")).strip())
        name = str(diagnosis.get("name", "")).strip()
        if not code and not name:
            continue
        diagnoses.append(CaseDiagnosis(role="other", code=code, name=name))
    return diagnoses


def normalize_case_diagnoses(raw_items: list[dict[str, Any]] | None, record_payload: dict[str, Any]) -> list[CaseDiagnosis]:
    if not raw_items:
        return extract_case_diagnoses(record_payload)

    diagnoses: list[CaseDiagnosis] = []
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            continue
        code = normalize_diagnosis_code(str(raw_item.get("code", "")).strip())
        name = str(raw_item.get("name", "")).strip()
        if not code and not name:
            continue
        role = str(raw_item.get("role", "other")).strip() or "other"
        diagnoses.append(CaseDiagnosis(role=role, code=code, name=name))
    return diagnoses


def _normalize_text(value: str) -> str:
    return re.sub(r"[\s，。、；：:（）()【】\[\]\"'“”‘’\-_/]+", "", value or "").lower()


def validate_diagnosis_candidates(
    diagnoses: list[CaseDiagnosis],
    guideline_repository: DiagnosisGuidelineRepository,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for diagnosis in diagnoses:
        by_code = None
        for candidate in diagnosis_code_lookup_candidates(diagnosis.code):
            by_code = guideline_repository.find_diagnosis_guideline_by_code(candidate)
            if by_code is not None:
                break

        canonical = by_code
        issues: list[str] = []
        suggestions: list[str] = []
        code_exists = by_code is not None if diagnosis.code else False
        has_name = bool(diagnosis.name)

        if not diagnosis.code:
            issues.append("缺少诊断编码")
        elif by_code is None:
            issues.append("未找到对应诊断审核规则")

        compliance = "合规" if diagnosis.code and by_code is not None else "待人工复核"
        if not diagnosis.code and not diagnosis.name:
            compliance = "不通过"

        results.append(
            {
                "role": diagnosis.role,
                "code": diagnosis.code,
                "name": diagnosis.name,
                "canonical_code": canonical.diagnosis_code if canonical else "",
                "canonical_name": canonical.diagnosis_name if canonical else "",
                "code_exists": code_exists,
                "name_exists": has_name,
                "name_matches_code": False,
                "compliance": compliance,
                "issues": issues,
                "suggestions": suggestions,
            }
        )
    return results


def _doc_matches_type(doc: dict[str, Any], doc_type: str) -> bool:
    haystack = " ".join(str(doc.get(key, "")) for key in ["docClassName", "fileName", "docName"])
    return doc_type in haystack


def _select_evidence_docs(record_payload: dict[str, Any], guideline: DiagnosisGuideline) -> list[dict[str, Any]]:
    preferred_doc_types = guideline.required_doc_types or DEFAULT_DIAGNOSIS_DOC_TYPES
    selected: list[dict[str, Any]] = []
    docs = record_payload.get("docs", [])

    for doc_type in preferred_doc_types:
        for index, doc in enumerate(docs):
            if not isinstance(doc, dict) or not _doc_matches_type(doc, doc_type):
                continue
            selected.append(
                {
                    "doc_index": index,
                    "doc_type": str(doc.get("docClassName", "")),
                    "file_name": str(doc.get("fileName", "")),
                    "content": truncate_text_by_utf8_bytes(str(doc.get("content", ""))),
                }
            )
            if len(selected) >= 8:
                return selected

    if selected:
        return selected

    fallback_chunks: list[str] = []
    for index, doc in enumerate(docs):
        if not isinstance(doc, dict):
            continue
        title = str(doc.get("fileName") or doc.get("docName") or f"文书#{index}")
        doc_type = str(doc.get("docClassName") or "未标注文书")
        content = str(doc.get("content", "")).strip()
        if not content:
            continue
        fallback_chunks.append(f"【文书#{index} / {doc_type} / {title}】\n{content}")

    if not fallback_chunks:
        return []

    return [
        {
            "doc_index": -1,
            "doc_type": "fallback_concat",
            "file_name": "全部文书拼接",
            "content": truncate_text_by_utf8_bytes("\n\n".join(fallback_chunks)),
        }
    ]


def build_diagnosis_review_prompt(
    case_id: str,
    diagnosis: CaseDiagnosis,
    guideline: DiagnosisGuideline,
    evidence_docs: list[dict[str, Any]],
) -> str:
    evidence_text = "\n\n".join(
        (
            f"【文书#{doc['doc_index']} / {doc['doc_type']} / {doc['file_name']}】\n"
            f"{doc['content']}"
        )
        for doc in evidence_docs
    )
    prompt = f"""
你是一个医疗审核专家。你的任务是根据{guideline.diagnosis_code} {guideline.diagnosis_name}的审核规则审核病例文书内容，判断是否满足审核点要求，返回该审核的审核结果。

## 审核规则
{guideline.diagnosis_name}

## 病例文书内容（已按依赖文书过滤）
{evidence_text or '未检索到优先文书'}

注意：
-先看审核规则，然后按照审核规则对病例文书内容进行审核；

输出格式要求：
{{
    "final_decision":"通过" 或 "不通过",
    "confidence": 0.0-1.0之间的浮点数（表示对最终结论的置信度）,
    "reasoning": "详细的审核理由和推理过程...",
    "evidence": "列出审核规则中每个审核条目的审核结果（特别是对不通过的审核条件）",
    "source": "列出每个审核条目审核结果对应的病例文书原始内容",
}}
请直接返回JSON，不要添加其他说明。
    """
    return prompt

def _snippet_from_doc(content: str, term: str, radius: int = 36) -> tuple[str, int, int] | None:
    if not term:
        return None
    index = content.find(term)
    if index < 0:
        return None
    start = max(0, index - radius)
    end = min(len(content), index + len(term) + radius)
    return content[start:end].strip(), index, index + len(term)


def _candidate_terms(diagnosis: CaseDiagnosis, guideline: DiagnosisGuideline) -> list[str]:
    raw_terms = [diagnosis.name, guideline.diagnosis_name]
    terms: list[str] = []
    for term in raw_terms:
        if not term:
            continue
        terms.append(term)
        for piece in re.split(r"[，、/（）() ]+", term):
            piece = piece.strip()
            if len(piece) >= 4:
                terms.append(piece)

    deduped: list[str] = []
    seen: set[str] = set()
    for term in terms:
        normalized = _normalize_text(term)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(term)
    return deduped


def _fallback_review(
    diagnosis: CaseDiagnosis,
    guideline: DiagnosisGuideline,
    evidence_docs: list[dict[str, Any]],
    compliance_item: dict[str, Any],
) -> dict[str, Any]:
    evidence_items: list[dict[str, Any]] = []
    for doc in evidence_docs:
        content = str(doc.get("content", ""))
        for term in _candidate_terms(diagnosis, guideline):
            snippet = _snippet_from_doc(content, term)
            if snippet is None:
                continue
            quote, start, end = snippet
            evidence_items.append(
                {
                    "doc_index": doc["doc_index"],
                    "doc_type": doc["doc_type"],
                    "file_name": doc["file_name"],
                    "quote": quote,
                    "explanation": f"文书中出现与诊断相关的关键词“{term}”",
                    "highlight_start": start,
                    "highlight_end": end,
                }
            )
            break
        if len(evidence_items) >= 3:
            break

    if evidence_items and compliance_item["compliance"] == "合规":
        result = "通过"
        reason = "诊断编码已命中审核规则，且病例文书存在直接诊断证据。"
    elif evidence_items:
        result = "待人工复核"
        reason = "找到部分病例证据，但编码规范性仍需人工确认。"
    else:
        result = "不通过"
        reason = "未在优先文书中找到可直接支撑该诊断的证据。"

    missing = [] if evidence_items else ["缺少可追溯的诊断原文证据"]
    suggestions = list(compliance_item.get("suggestions", []))
    if not evidence_items:
        suggestions.append("请补充出院记录、病程记录或检查/检验记录中的直接诊断依据")
    return {
        "result": result,
        "reason": reason,
        "audit_log": _build_audit_log(
            target_label=f"{diagnosis.name or diagnosis.code}",
            guideline_label=f"{guideline.diagnosis_code} {guideline.diagnosis_name}".strip(),
            evidence_items=evidence_items,
            missing_evidence=missing,
            suggestions=suggestions,
            result=result,
        ),
        "key_evidence": evidence_items,
        "missing_evidence": missing,
        "suggestions": suggestions,
    }


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _extract_audit_thinking(raw_output: str) -> str:
    matches = re.findall(r"<thinking[^>]*>([\s\S]*?)</thinking>", raw_output or "", flags=re.IGNORECASE)
    return "\n\n".join(match.strip() for match in matches if match.strip())


def _build_audit_log(
    target_label: str,
    guideline_label: str,
    evidence_items: list[dict[str, Any]],
    missing_evidence: list[str],
    suggestions: list[str],
    result: str,
) -> list[str]:
    logs = [
        f"确认审核对象：{target_label or '未命名诊断'}。",
        f"匹配审核指南：{guideline_label or '未命中明确指南'}。",
    ]
    if evidence_items:
        evidence_text = "；".join(
            f"{item.get('doc_type') or item.get('file_name') or '病历文书'}：{str(item.get('quote') or '')[:80]}"
            for item in evidence_items[:3]
        )
        logs.append(f"核对病历证据：{evidence_text}。")
    else:
        logs.append("核对病历证据：未找到可直接支撑该编码的关键原文。")
    if missing_evidence:
        logs.append(f"缺失项：{'；'.join(missing_evidence[:3])}。")
    if suggestions:
        logs.append(f"处理建议：{'；'.join(suggestions[:3])}。")
    logs.append(f"形成审核结论：{result or '待人工复核'}。")
    return logs


def _coerce_llm_review_payload(payload: dict[str, Any], docs: list[dict[str, Any]]) -> dict[str, Any]:
    evidence_items: list[dict[str, Any]] = []
    for item in payload.get("key_evidence") or []:
        if not isinstance(item, dict):
            continue
        doc_index = int(item.get("doc_index", -1))
        if doc_index < 0 or doc_index >= len(docs):
            continue
        doc = docs[doc_index]
        quote = str(item.get("quote", "")).strip()
        span = locate_quote_span(str(doc.get("content", "")), quote)
        evidence_items.append(
            {
                "doc_index": doc_index,
                "doc_type": str(item.get("doc_type") or doc.get("docClassName", "")),
                "file_name": str(item.get("file_name") or doc.get("fileName", "")),
                "quote": quote,
                "explanation": str(item.get("explanation", "")).strip(),
                "highlight_start": span["start"] if span else None,
                "highlight_end": span["end"] if span else None,
            }
        )
    result = str(payload.get("final_decision") or payload.get("result") or "待人工复核").strip() or "待人工复核"
    if result not in {"通过", "不通过", "待人工复核"}:
        result = "待人工复核"
    reason = str(payload.get("reasoning") or payload.get("reason") or "").strip()
    return {
        "result": result,
        "reason": reason,
        "thinking": str(payload.get("thinking") or payload.get("audit_thinking") or "").strip(),
        "audit_log": _string_list(payload.get("audit_log") or payload.get("model_audit_log") or payload.get("thinking")),
        "key_evidence": evidence_items,
        "missing_evidence": [str(item) for item in payload.get("missing_evidence") or [] if str(item).strip()],
        "suggestions": [str(item) for item in payload.get("suggestions") or [] if str(item).strip()],
    }


def locate_quote_span(content: str, quote: str) -> dict[str, int] | None:
    if not content or not quote:
        return None

    index = content.find(quote)
    if index >= 0:
        return {"start": index, "end": index + len(quote)}

    fragments = sorted(
        {
            fragment.strip()
            for fragment in re.split(r"[\n，。；：:、]", quote)
            if len(fragment.strip()) >= 6
        },
        key=len,
        reverse=True,
    )
    for fragment in fragments:
        index = content.find(fragment)
        if index >= 0:
            return {"start": index, "end": index + len(fragment)}
    return None


def review_diagnosis_record(
    record_payload: dict[str, Any],
    diagnoses: list[CaseDiagnosis],
    guideline_repository: DiagnosisGuidelineRepository,
    llm_client: LlmClient | None = None,
    model_name: str | None = None,
) -> dict[str, Any]:
    case_id = _record_id(record_payload) or "record"
    compliance_items = validate_diagnosis_candidates(diagnoses, guideline_repository)
    compliance_by_key = {(item["role"], item["code"], item["name"]): item for item in compliance_items}
    guideline_by_key = {
        (diagnosis.role, diagnosis.code, diagnosis.name): find_diagnosis_guideline(
            guideline_repository=guideline_repository,
            diagnosis_code=diagnosis.code,
        )
        for diagnosis in diagnoses
    }

    docs = record_payload.get("docs", [])

    def review_one(diagnosis: CaseDiagnosis) -> dict[str, Any]:
        compliance_item = compliance_by_key[(diagnosis.role, diagnosis.code, diagnosis.name)]
        guideline = guideline_by_key[(diagnosis.role, diagnosis.code, diagnosis.name)]

        if guideline is None:
            return {
                "role": diagnosis.role,
                "code": diagnosis.code,
                "name": diagnosis.name,
                "compliance": compliance_item,
                "guideline": None,
                    "review": {
                        "result": "待人工复核",
                        "reason": "未检索到匹配的诊断审核规则。",
                        "thinking": "已检索诊断审核规则库，但未命中该诊断编码对应的审核规则，暂不能自动完成规则核对。",
                        "audit_log": [
                            f"确认审核对象：{diagnosis.name or diagnosis.code or '未命名诊断'}。",
                            "检索审核指南：未命中匹配的诊断审核规则。",
                            "形成审核结论：待人工复核。",
                        ],
                        "key_evidence": [],
                        "missing_evidence": ["缺少可用的诊断审核规则"],
                        "suggestions": compliance_item.get("suggestions", []),
                    },
            }

        evidence_docs = _select_evidence_docs(record_payload, guideline)
        review_payload: dict[str, Any]
        if llm_client is None:
            review_payload = _fallback_review(diagnosis, guideline, evidence_docs, compliance_item)
        else:
            prompt = build_diagnosis_review_prompt(case_id, diagnosis, guideline, evidence_docs)
            try:
                raw_response = llm_client.complete(prompt, model_name=model_name)
                audit_thinking = _extract_audit_thinking(raw_response)
                parsed = parse_json_object(raw_response)
                review_payload = _coerce_llm_review_payload(parsed, docs)
                if audit_thinking:
                    review_payload["thinking"] = audit_thinking
                if not review_payload["reason"]:
                    review_payload["reason"] = "模型已完成诊断审核。"
                if not review_payload["audit_log"]:
                    review_payload["audit_log"] = _build_audit_log(
                        target_label=diagnosis.name or diagnosis.code,
                        guideline_label=f"{guideline.diagnosis_code} {guideline.diagnosis_name}".strip(),
                        evidence_items=review_payload["key_evidence"],
                        missing_evidence=review_payload["missing_evidence"],
                        suggestions=review_payload["suggestions"],
                        result=review_payload["result"],
                    )
            except Exception:
                review_payload = _fallback_review(diagnosis, guideline, evidence_docs, compliance_item)

        return {
            "role": diagnosis.role,
            "code": diagnosis.code,
            "name": diagnosis.name,
            "matched_guideline_code": guideline.diagnosis_code,
            "matched_guideline_name": guideline.diagnosis_name,
            "guideline": {
                "diagnosis_code": guideline.diagnosis_code,
                "diagnosis_name": guideline.diagnosis_name,
                "guideline_text": guideline.guideline_text,
                "required_doc_types": guideline.required_doc_types,
                "source_file": guideline.source_file,
            },
            "compliance": compliance_item,
            "review": review_payload,
        }

    max_workers = min(DIAGNOSIS_AUDIT_MAX_WORKERS, max(len(diagnoses), 1))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        items = list(executor.map(review_one, diagnoses))

    return _build_final_response(items, pass_result="通过", fail_result="不通过", pending_result="待人工复核")


def _build_final_response(
    items: list[dict[str, Any]],
    *,
    pass_result: str,
    fail_result: str,
    pending_result: str,
) -> dict[str, str]:
    results = [str((item.get("review") or {}).get("result") or "").strip() for item in items]
    if any(result == fail_result for result in results):
        final_decision = fail_result
    elif any(result == pending_result for result in results) or not results:
        final_decision = pending_result
    else:
        final_decision = pass_result

    reasoning_parts: list[str] = []
    for item in items:
        review = item.get("review") or {}
        label = " ".join(part for part in [str(item.get("code") or "").strip(), str(item.get("name") or "").strip()] if part)
        result = str(review.get("result") or pending_result).strip()
        reason = str(review.get("reason") or "").strip()
        if len(items) == 1:
            reasoning_parts.append(reason or f"{label or '未命名诊断'}：{result}")
        else:
            reasoning_parts.append(f"{label or '未命名诊断'}：{result}。{reason}".strip())
    return {"final_decision": final_decision, "reasoning": "\n".join(reasoning_parts)}


def _load_llm_client(use_llm: bool, appkey: str, base: str = DEFAULT_LLM_BASE, model: str = DEFAULT_LLM_MODEL, timeout: int = 0) -> HardcodedLlmClient | None:
    if not use_llm:
        return None
    return HardcodedLlmClient(build_internal_llm_settings(appkey, base=base, model=model, timeout=timeout))


def _coerce_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "no", "off", "否"}
    return bool(value)


def review_diagnosis_payload(payload: dict[str, Any]) -> dict[str, Any]:
    record = payload.get("record")
    if not isinstance(record, dict):
        raise ValueError("请求体缺少 record")
    raw_diagnoses = payload.get("diagnoses")
    if raw_diagnoses is not None and not isinstance(raw_diagnoses, list):
        raise ValueError("diagnoses 必须是数组")
    diagnoses = normalize_case_diagnoses(raw_diagnoses, record)
    if not diagnoses:
        raise ValueError("未提供可审核的诊断编码/名称")

    model_name = str(payload.get("model") or "").strip() or DEFAULT_LLM_MODEL
    llm_client = _load_llm_client(
        _coerce_bool(payload.get("use_llm"), True),
        str(payload.get("appkey") or "").strip(),
        str(payload.get("base") or DEFAULT_LLM_BASE).strip(),
        model_name,
        int(payload.get("timeout") or 0),
    )
    repository = GuidelineApiDiagnosisRepository(load_guideline_api_settings_from_env())
    return review_diagnosis_record(
        record_payload=record,
        diagnoses=diagnoses,
        guideline_repository=repository,
        llm_client=llm_client,
        model_name=model_name,
    )


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("input JSON 必须是对象")
    return payload


def _build_cli_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = _read_json(Path(args.input))
    if "record" not in payload:
        payload = {"record": payload}
    if args.diagnosis_code or args.diagnosis_name:
        payload["diagnoses"] = [
            {"role": args.role, "code": normalize_diagnosis_code(args.diagnosis_code), "name": args.diagnosis_name.strip()}
        ]
    if args.model:
        payload["model"] = args.model
    if args.base:
        payload["base"] = args.base
    payload["timeout"] = args.timeout
    payload["appkey"] = args.appkey
    payload["use_llm"] = not args.no_llm
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run diagnosis coding review.")
    parser.add_argument("--input", required=True, help="Path to record JSON, or payload JSON containing record.")
    parser.add_argument("--diagnosis-code", default="", help="Optional diagnosis code override.")
    parser.add_argument("--diagnosis-name", default="", help="Optional diagnosis name override.")
    parser.add_argument("--role", default="primary", choices=["primary", "other"], help="Diagnosis role.")
    parser.add_argument("--base", default=DEFAULT_LLM_BASE, help=f"内部大模型 base URL（默认：{DEFAULT_LLM_BASE}）。")
    parser.add_argument("--model", default=DEFAULT_LLM_MODEL, help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。")
    parser.add_argument("--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。")
    parser.add_argument("--appkey", required=True, help="内部医疗大模型鉴权 key，由平台分配；调用时必填，使用 Bearer 鉴权。")
    parser.add_argument("--no-llm", action="store_true", help="Disable LLM and use fallback review only.")
    parser.add_argument("--output-json", default="", help="Optional path to save response JSON.")
    args = parser.parse_args()

    try:
        response = review_diagnosis_payload(_build_cli_payload(args))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(response, ensure_ascii=False, indent=2)
    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"Saved response JSON to: {out_path}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
