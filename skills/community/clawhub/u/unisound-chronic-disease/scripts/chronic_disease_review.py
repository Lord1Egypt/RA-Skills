#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import urllib.error
import urllib.request

from format_review_nl import build_natural_language


DEFAULT_LLM_BASE = "https://maas-api.hivoice.cn/v1"
DEFAULT_LLM_MODEL = "u1-insuremed"

DISEASE_CODE_ALIASES: Dict[str, str] = {
    "diabetes": "糖尿病",
    "dm": "糖尿病",
    "糖尿病": "糖尿病",
    "hypertension": "高血压",
    "htn": "高血压",
    "高血压": "高血压",
}


def _http_post(url: str, payload: Dict[str, Any], headers: Dict[str, str], *, timeout: int = 0) -> Any:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", **headers},
    )
    try:
        ctx = urllib.request.urlopen(req) if not timeout else urllib.request.urlopen(req, timeout=timeout)
        with ctx as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body) if body.strip() else None
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def make_llm_caller(
    appkey: str,
    *,
    base: str = DEFAULT_LLM_BASE,
    model: str = DEFAULT_LLM_MODEL,
    timeout: int = 0,
):
    url = f"{base.rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {appkey}"}

    def llm(messages: List[Dict[str, str]]) -> str:
        payload = {"model": model, "messages": messages, "temperature": 0}
        resp = _http_post(url, payload, headers, timeout=timeout)
        try:
            return str(resp["choices"][0]["message"]["content"]).strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected LLM response: {resp}") from exc

    return llm


def validate_ocr_data(ocr_data: Any) -> List[Dict[str, Any]]:
    if not isinstance(ocr_data, list) or len(ocr_data) == 0:
        raise ValueError("OCR input must be a non-empty JSON array (list).")
    out: List[Dict[str, Any]] = []
    for i, item in enumerate(ocr_data):
        if not isinstance(item, dict):
            raise ValueError(f"OCR item #{i} must be an object.")
        if not item.get("ocrText"):
            raise ValueError(f"OCR item #{i} missing required field: ocrText")
        if "page" in item and not isinstance(item["page"], int):
            raise ValueError(f"OCR item #{i} field page must be int when provided.")
        out.append(item)
    return out


def _resolve_disease_code(args_disease_code: str) -> Optional[str]:
    s = (args_disease_code or "").strip()
    if not s:
        return None
    if s in DISEASE_CODE_ALIASES:
        return DISEASE_CODE_ALIASES[s]
    return s


def _infer_label(disease_code: Optional[str]) -> str:
    if disease_code == "糖尿病":
        return "diabetes"
    if disease_code == "高血压":
        return "hypertension"
    return "by_ocr"


def format_ocr_for_prompt(ocr_data: List[Dict[str, Any]]) -> str:
    blocks: List[str] = []
    for item in ocr_data:
        file_name = item.get("fileName") or "未知文件"
        page = item.get("page", "")
        doc_type = item.get("docType") or "未分类文书"
        text = item.get("ocrText") or ""
        blocks.append(f"【{doc_type}】{file_name} 第{page}页\n{text}")
    return "\n\n".join(blocks)


SYSTEM_PROMPT = """你是医疗保险门诊慢特病（慢病）理赔审核助手。
根据用户提供的 OCR 病历/检验等文书文本，判断是否符合该慢病的门诊慢特病认定或理赔审核要求。
仅依据给定文本作答，不要编造未出现的检查结果或诊断。
输出必须是合法 JSON，且只包含一个 JSON 对象，不要 markdown 代码块或额外说明。"""


def build_review_user_prompt(*, disease_code: str, review_type: str, ocr_data: List[Dict[str, Any]]) -> str:
    ocr_text = format_ocr_for_prompt(ocr_data)
    return f"""请对以下材料进行「{review_type}」，病种：{disease_code}。

材料正文：
{ocr_text}

请输出 JSON，字段如下（均为字符串）：
- final_decision：审核结论，取值为「通过」「不通过」「待补充」之一
- reasoning：审核原因说明，需与结论一致

示例：
{{"final_decision": "通过", "reasoning": "..."}}"""


def extract_json_object(text: str) -> Dict[str, Any]:
    text = (text or "").strip()
    if not text:
        raise ValueError("LLM returned empty content.")
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        parsed = json.loads(match.group(0))
        if isinstance(parsed, dict):
            return parsed
    raise ValueError(f"Could not parse JSON from LLM output: {text[:500]}")


def normalize_llm_decision(raw: Dict[str, Any]) -> Dict[str, str]:
    decision = str(raw.get("final_decision") or raw.get("decision") or "").strip()
    reasoning = str(raw.get("reasoning") or raw.get("reason") or raw.get("原因") or "").strip()
    if not decision:
        decision = "待补充"
    if not reasoning:
        reasoning = "模型未给出详细原因。"
    return {"final_decision": decision, "reasoning": reasoning}


def review_chronic_disease(
    ocr_data: List[Dict[str, Any]],
    *,
    disease_code: str,
    review_type: str = "慢病审核",
    appkey: str,
    base: str = DEFAULT_LLM_BASE,
    model: str = DEFAULT_LLM_MODEL,
    timeout: int = 120,
) -> Dict[str, Any]:
    llm = make_llm_caller(appkey, base=base, model=model, timeout=timeout)
    user_prompt = build_review_user_prompt(
        disease_code=disease_code,
        review_type=review_type or "慢病审核",
        ocr_data=ocr_data,
    )
    content = llm(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )
    parsed = normalize_llm_decision(extract_json_object(content))
    return {
        "success": True,
        "source": "llm",
        "model": model,
        "results": [
            {
                "disease_code": disease_code,
                "review_type": review_type or "慢病审核",
                "scenario_code": "chronic-disease-llm",
                "final_decision": parsed["final_decision"],
                "reasoning": parsed["reasoning"],
                "raw_llm_content": content,
            }
        ],
    }


def dry_run_response(*, disease_code: str, review_type: str) -> Dict[str, Any]:
    return {
        "success": True,
        "source": "dry-run",
        "results": [
            {
                "disease_code": disease_code,
                "review_type": review_type or "慢病审核",
                "scenario_code": "chronic-disease-dry-run",
                "final_decision": "待补充",
                "reasoning": "dry-run 模式，未调用医疗大模型。",
            }
        ],
    }


def _read_ocr_array(path: str) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists() and not p.is_absolute():
        fallback = Path(__file__).resolve().parents[4] / "data" / "med-chronic-disease-review" / p.name
        if fallback.exists():
            p = fallback
    raw = json.loads(p.read_text(encoding="utf-8"))
    return validate_ocr_data(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description="Chronic disease review via internal medical LLM.")
    parser.add_argument(
        "--disease-code",
        default="",
        help="Required disease_code: 糖尿病/高血压. Also supports aliases: diabetes/hypertension/dm/htn.",
    )
    parser.add_argument("--review-type", default="慢病审核", help="review_type (default: 慢病审核)")
    parser.add_argument("--input", required=True, help="Path to OCR array JSON (list).")
    parser.add_argument(
        "--appkey",
        default="",
        help="内部医疗大模型鉴权 key（--dry-run 时可选）。",
    )
    parser.add_argument("--base", default=DEFAULT_LLM_BASE, help=f"LLM base URL (default: {DEFAULT_LLM_BASE})")
    parser.add_argument("--model", default=DEFAULT_LLM_MODEL, help=f"LLM model (default: {DEFAULT_LLM_MODEL})")
    parser.add_argument("--timeout", type=int, default=120, help="HTTP timeout seconds (default: 120).")
    parser.add_argument("--dry-run", action="store_true", help="Skip LLM call; emit placeholder response.")
    parser.add_argument("--output-json", default="", help="Path to save raw response JSON.")
    parser.add_argument("--output-text", default="", help="Path to save natural language summary.")
    args = parser.parse_args()

    try:
        disease_code = _resolve_disease_code(args.disease_code)
        if disease_code is None:
            raise ValueError("--disease-code is required (糖尿病/高血压 or diabetes/hypertension/dm/htn).")
        ocr_data = _read_ocr_array(args.input)
        if args.dry_run:
            resp = dry_run_response(disease_code=disease_code, review_type=args.review_type)
        else:
            if not (args.appkey or "").strip():
                raise ValueError("--appkey is required unless --dry-run is set.")
            resp = review_chronic_disease(
                ocr_data,
                disease_code=disease_code,
                review_type=args.review_type,
                appkey=args.appkey.strip(),
                base=args.base,
                model=args.model,
                timeout=args.timeout,
            )
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

    label = _infer_label(disease_code)
    default_base = Path("../runs/med-chronic-disease-review")
    out_json = Path(args.output_json) if args.output_json else (default_base / f"{label}_resp.json")
    out_text = Path(args.output_text) if args.output_text else (default_base / f"{label}_resp.txt")

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")

    text = build_natural_language(resp)
    out_text.parent.mkdir(parents=True, exist_ok=True)
    out_text.write_text(text, encoding="utf-8")

    print(f"✓ Saved raw JSON to: {out_json}")
    print(f"✓ Saved natural language to: {out_text}")
    print("\n--- Natural language preview ---")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
