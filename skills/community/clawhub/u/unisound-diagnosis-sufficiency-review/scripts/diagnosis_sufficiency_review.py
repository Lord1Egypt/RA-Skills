#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
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


@dataclass(frozen=True)
class CaseDiagnosis:
    role: str
    code: str
    name: str


@dataclass(frozen=True)
class SufficiencyGuideline:
    category: str
    code: str
    scope: str
    standard_name: str
    guideline_text: str
    required_doc_types: list[str]
    source_file: str
    raw_payload: dict[str, Any]
    best_pass_rate: float | None = None


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


def row_to_sufficiency_guideline(row: dict[str, Any]) -> SufficiencyGuideline:
    required_doc_types = _json_value(row.get("required_doc_types"), [])
    if not isinstance(required_doc_types, list):
        required_doc_types = []
    raw_payload = _json_value(row.get("raw_payload"), {})
    if not isinstance(raw_payload, dict):
        raw_payload = {}
    best_pass_rate = row.get("best_pass_rate")
    return SufficiencyGuideline(
        category="diagnosis",
        code=str(row["code"]),
        scope=str(row["scope"]),
        standard_name=str(row["standard_name"]),
        guideline_text=str(row["guideline_text"]),
        required_doc_types=[str(item) for item in required_doc_types],
        source_file=str(row.get("source_file", "")),
        best_pass_rate=float(best_pass_rate) if best_pass_rate is not None else None,
        raw_payload=raw_payload,
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


class GuidelineApiSufficiencyGuidelineRepository:
    def __init__(self, settings: GuidelineApiSettings) -> None:
        self._settings = settings

    def _get(self, path: str, query: dict[str, str]) -> dict[str, Any] | None:
        url = f"{self._settings.base_url.rstrip('/')}{path}?{parse.urlencode(query)}"
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

    def find_diagnosis_sufficiency_guideline_by_code_scope(
        self,
        diagnosis_code: str,
        scope: str,
    ) -> SufficiencyGuideline | None:
        encoded_code = parse.quote(str(diagnosis_code), safe="")
        payload = _extract_api_payload(
            self._get(
                f"/api/v1/icd-drg/diagnosis-sufficiency-guidelines/{encoded_code}",
                {"scope": scope},
            )
        )
        if payload is None:
            return None
        row = dict(payload)
        row.setdefault("code", row.get("diagnosis_code"))
        row.setdefault("standard_name", row.get("standard_diagnosis_name"))
        return row_to_sufficiency_guideline(row)


def normalize_diagnosis_code(value: str) -> str:
    normalized = "".join(str(value or "").strip().upper().split())
    if re.fullmatch(r"1\d{2}(?:\.[A-Z0-9X.]+)?", normalized):
        return f"I{normalized[1:]}"
    return normalized


def diagnosis_code_lookup_candidates(code: str) -> list[str]:
    normalized = normalize_diagnosis_code(code)
    if not normalized:
        return []
    candidates = [normalized]
    if "." in normalized:
        head, tail = normalized.split(".", 1)
        if tail and tail[0] != "X":
            candidates.append(f"{head}.{tail[0]}")
        candidates.append(head)
    elif len(normalized) > 3:
        match = re.match(r"^([A-Z])(\d{2})(.*)$", normalized)
        if match:
            letter, first_two_digits, rest = match.groups()
            head = f"{letter}{first_two_digits}"
            if rest:
                candidates.append(f"{head}.{rest}")
            candidates.append(head)
    return list(dict.fromkeys(candidate for candidate in candidates if candidate))


def _scope(value: str) -> str:
    return "primary" if str(value or "").strip().lower() == "primary" else "other"


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
        if code or name:
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


def truncate_text_by_utf8_bytes(text: str, max_bytes: int = 24000) -> str:
    encoded = str(text or "").encode("utf-8")
    if len(encoded) <= max_bytes:
        return str(text or "")
    return encoded[:max_bytes].decode("utf-8", errors="ignore") + "\n...[已截断]"


def _doc_matches_type(doc: dict[str, Any], doc_type: str) -> bool:
    haystack = " ".join(str(doc.get(key, "")) for key in ["docClassName", "fileName", "docName"])
    return doc_type in haystack


def _select_evidence_docs(record_payload: dict[str, Any], guideline: SufficiencyGuideline) -> list[dict[str, Any]]:
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
        if content:
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


def _evidence_text(evidence_docs: list[dict[str, Any]]) -> str:
    return "\n\n".join(
        f"【文书#{doc['doc_index']} / {doc['doc_type']} / {doc['file_name']}】\n{doc['content']}"
        for doc in evidence_docs
    )


def _record_id(payload: dict[str, Any]) -> str:
    hospital_id = str(payload.get("hospitalId", "")).strip()
    serial_num = str(payload.get("serialNum", "")).strip()
    return "_".join(part for part in [hospital_id, serial_num] if part)


def _find_guideline(
    repository: GuidelineApiSufficiencyGuidelineRepository,
    diagnosis: CaseDiagnosis,
) -> SufficiencyGuideline | None:
    scope = _scope(diagnosis.role)
    for candidate in diagnosis_code_lookup_candidates(diagnosis.code):
        guideline = repository.find_diagnosis_sufficiency_guideline_by_code_scope(candidate, scope)
        if guideline is not None:
            return guideline
    return None


def _sufficiency_guideline_payload(guideline: SufficiencyGuideline) -> dict[str, Any]:
    return {
        "diagnosis_code": guideline.code,
        "diagnosis_name": guideline.standard_name,
        "scope": guideline.scope,
        "guideline_text": guideline.guideline_text,
        "required_doc_types": guideline.required_doc_types,
        "source_file": guideline.source_file,
        "best_pass_rate": guideline.best_pass_rate,
        "raw_payload": guideline.raw_payload,
    }


def _missing_guideline_item(item: CaseDiagnosis) -> dict[str, Any]:
    return {
        "role": item.role,
        "code": item.code,
        "name": item.name,
        "matched_guideline_code": "",
        "matched_guideline_name": "",
        "guideline": None,
        "compliance": {
            "role": item.role,
            "code": item.code,
            "name": item.name,
            "canonical_code": "",
            "canonical_name": "",
            "code_exists": False,
            "name_exists": bool(item.name),
            "name_matches_code": False,
            "compliance": "待人工复核",
            "issues": ["未找到对应诊断依据充分性审核指南"],
            "suggestions": [],
        },
        "review": {
            "result": "待人工复核",
            "reason": "未检索到匹配的诊断依据充分性审核指南。",
            "thinking": "已检索诊断依据充分性规则库，但未命中该编码与角色对应的审核指南。",
            "audit_log": ["确认审核对象。", "检索审核指南：未命中。", "形成审核结论：待人工复核。"],
            "key_evidence": [],
            "missing_evidence": ["缺少可用的诊断依据充分性审核指南"],
            "suggestions": [],
        },
    }


def _build_prompt(
    *,
    case_id: str,
    diagnosis: CaseDiagnosis,
    guideline: SufficiencyGuideline,
    evidence_docs: list[dict[str, Any]],
) -> str:
    role_label = "主诊断" if _scope(diagnosis.role) == "primary" else "其他诊断"
    prompt=f"""
你是住院病历"诊断依据充分性审核助手"。

请严格根据【审核指南】、【待审核病例信息】和【病例文书】完成审核。不得脑补。

你的任务是判断给出诊断的"依据是否充分"
- 主诊断：必须同时满足"诊断成立"+"是本次住院主轴"。
- 其他诊断：只要求"诊断成立"，且在住院管理中有记录或影响。
- 只能依据输入内容判断，不得脑补。
- 注意病历文书截断情况：若因篇幅限制导致部分文书内容未完整展示，截断本身不能作为“诊断依据不充分”的理由。
- 审核时只能基于当前可见内容判断：可见内容中如存在支持目标诊断成立的证据，应予采纳，并可作为“依据充分”的依据；
- 不得将“证据可能出现在被截断部分”作为判定不通过的直接原因。

请严格按以下 JSON 格式输出：

{{
    "final_decision": "依据充分" 或 "依据不充分",
    "confidence": 0.0,
    "reasoning": "综合说明判定理由",
    "evidence": "列出每个审核条目的审核结果",
    "source": "列出对应的病例文书原始内容",
}}

【审核指南】
{guideline.guideline_text}

【待审核病例信息】
待审核诊断名称：{diagnosis.name}
是否主诊断：{role_label}

【病例文书】
{_evidence_text(evidence_docs) or '未检索到优先文书'}
    """
    return prompt


def _extract_audit_thinking(text: str) -> str:
    match = re.search(r"<thinking>(.*?)</thinking>", text or "", flags=re.S)
    return match.group(1).strip() if match else ""


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


def _normalize_review_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result = str(payload.get("final_decision") or payload.get("result") or "").strip()
    if result == "通过":
        result = "依据充分"
    elif result == "不通过":
        result = "依据不充分"
    elif result not in {"依据充分", "依据不充分", "待人工复核"}:
        result = "待人工复核"
    key_evidence = payload.get("key_evidence")
    audit_log = payload.get("audit_log")
    missing_evidence = payload.get("missing_evidence")
    suggestions = payload.get("suggestions")
    return {
        "result": result,
        "reason": str(payload.get("reasoning") or payload.get("reason") or ""),
        "thinking": str(payload.get("thinking") or ""),
        "audit_log": audit_log if isinstance(audit_log, list) else [],
        "key_evidence": key_evidence if isinstance(key_evidence, list) else [],
        "missing_evidence": missing_evidence if isinstance(missing_evidence, list) else [],
        "suggestions": suggestions if isinstance(suggestions, list) else [],
    }


def _fallback_review(
    diagnosis: CaseDiagnosis,
    guideline: SufficiencyGuideline,
    evidence_docs: list[dict[str, Any]],
) -> dict[str, Any]:
    evidence_text = "\n".join(str(doc.get("content", "")) for doc in evidence_docs)
    normalized_evidence = re.sub(r"\s+", "", evidence_text).lower()
    normalized_name = re.sub(r"\s+", "", diagnosis.name).lower()
    has_direct_name = bool(normalized_name and normalized_name in normalized_evidence)
    has_code = bool(diagnosis.code and diagnosis.code.lower() in normalized_evidence)
    result = "待人工复核"
    reason = (
        "病历证据中可见候选诊断名称或编码，但本地回退逻辑不能确认诊断依据充分性，需结合指南人工复核。"
        if has_direct_name or has_code
        else "未通过本地规则直接确认诊断依据，需结合指南人工复核。"
    )
    return {
        "result": result,
        "reason": reason,
        "thinking": "未启用或未成功调用模型，已使用 skill 内置本地回退逻辑完成判断。",
        "audit_log": ["读取诊断依据充分性指南。", "抽取优先文书证据。", f"形成审核结论：{result}。"],
        "key_evidence": [
            {
                "doc_index": doc["doc_index"],
                "doc_type": doc["doc_type"],
                "file_name": doc["file_name"],
                "quote": truncate_text_by_utf8_bytes(doc["content"], 500),
                "explanation": "该文书被选为诊断依据审核证据。",
            }
            for doc in evidence_docs[:2]
        ],
        "missing_evidence": ["缺少可由本地规则直接确认的诊断依据"],
        "suggestions": ["建议人工核对入院记录、首次病程记录、出院记录、检查/检验记录中的诊断依据。"],
    }


def review_diagnosis_sufficiency_record(
    record_payload: dict[str, Any],
    diagnoses: list[CaseDiagnosis],
    guideline_repository: GuidelineApiSufficiencyGuidelineRepository,
    llm_client: HardcodedLlmClient | None,
    model_name: str | None = None,
) -> dict[str, Any]:
    case_id = _record_id(record_payload) or "record"
    items: list[dict[str, Any]] = []
    for diagnosis in diagnoses:
        guideline = _find_guideline(guideline_repository, diagnosis)
        if guideline is None:
            items.append(_missing_guideline_item(diagnosis))
            continue
        evidence_docs = _select_evidence_docs(record_payload, guideline)
        compliance_item = {
            "role": diagnosis.role,
            "code": diagnosis.code,
            "name": diagnosis.name,
            "canonical_code": guideline.code,
            "canonical_name": guideline.standard_name,
            "code_exists": True,
            "name_exists": bool(diagnosis.name),
            "name_matches_code": False,
            "compliance": "合规",
            "issues": [],
            "suggestions": [],
        }
        if llm_client is None:
            review_payload = _fallback_review(diagnosis, guideline, evidence_docs)
        else:
            try:
                raw_response = llm_client.complete(
                    _build_prompt(case_id=case_id, diagnosis=diagnosis, guideline=guideline, evidence_docs=evidence_docs),
                    model_name=model_name,
                )
                parsed = parse_json_object(raw_response)
                thinking = _extract_audit_thinking(raw_response)
                if thinking:
                    parsed["thinking"] = thinking
                review_payload = _normalize_review_payload(parsed)
                if not review_payload["reason"]:
                    review_payload["reason"] = "模型已完成诊断依据充分性审核。"
            except Exception as exc:
                review_payload = _fallback_review(diagnosis, guideline, evidence_docs)
                review_payload["reason"] = f"{review_payload['reason']} 模型审核未完成：{exc}"
        items.append(
            {
                "role": diagnosis.role,
                "code": diagnosis.code,
                "name": diagnosis.name,
                "matched_guideline_code": guideline.code,
                "matched_guideline_name": guideline.standard_name,
                "guideline": _sufficiency_guideline_payload(guideline),
                "compliance": compliance_item,
                "review": review_payload,
            }
        )
    return _build_final_response(items, pass_result="依据充分", fail_result="依据不充分", pending_result="待人工复核")


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


def review_diagnosis_sufficiency_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Function entrypoint for the diagnosis sufficiency skill.

    Expected payload:
    {
      "record": {...},
      "diagnoses": [{"role": "primary", "code": "E11.901", "name": "2型糖尿病"}],
      "model": "optional-model-name",
      "use_llm": true,
      "appkey": "required-when-use-llm"
    }
    """
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
    use_llm = _coerce_bool(payload.get("use_llm"), True)
    llm_client = _load_llm_client(
        use_llm,
        str(payload.get("appkey") or "").strip(),
        str(payload.get("base") or DEFAULT_LLM_BASE).strip(),
        model_name,
        int(payload.get("timeout") or 0),
    )

    repository = GuidelineApiSufficiencyGuidelineRepository(load_guideline_api_settings_from_env())
    return review_diagnosis_sufficiency_record(
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
            {
                "role": args.role,
                "code": normalize_diagnosis_code(args.diagnosis_code),
                "name": args.diagnosis_name.strip(),
            }
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
    parser = argparse.ArgumentParser(description="Run diagnosis sufficiency review.")
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
        response = review_diagnosis_sufficiency_payload(_build_cli_payload(args))
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
