#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转诊指导：根据患者病情摘要，判断是否需要转诊、转诊紧急程度、
目标科室/医院级别、转诊前准备和随附材料要求。
LLM 调用使用公司内部医疗大模型。
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import urllib.error
import urllib.request


DEFAULT_LLM_BASE = "https://maas-api.hivoice.cn/v1"
DEFAULT_LLM_MODEL = "u1-insuremed"


# ---------------------------------------------------------------------------
# HTTP / LLM 调用
# ---------------------------------------------------------------------------

def _http_post(url: str, payload: Dict[str, Any], headers: Dict[str, str], *, timeout: int = 0) -> Any:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url=url, data=data, method="POST",
        headers={"Content-Type": "application/json", **headers},
    )
    try:
        ctx = urllib.request.urlopen(req) if not timeout else urllib.request.urlopen(req, timeout=timeout)
        with ctx as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def make_llm_caller(appkey: str, base: str = DEFAULT_LLM_BASE, model: str = DEFAULT_LLM_MODEL, timeout: int = 0):
    url = f"{base.rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {appkey}"}

    def llm(messages: List[Dict[str, str]]) -> str:
        payload = {"model": model, "messages": messages, "temperature": 0}
        resp = _http_post(url, payload, headers, timeout=timeout)
        try:
            return resp["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected LLM response: {resp}") from e

    return llm


def user_msg(content: str) -> Dict[str, str]:
    return {"role": "user", "content": content}


def sys_msg(content: str) -> Dict[str, str]:
    return {"role": "system", "content": content}


# ---------------------------------------------------------------------------
# 输入解析
# ---------------------------------------------------------------------------

def load_input(path: Path, encoding: str) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        with path.open(encoding=encoding) as f:
            data = json.load(f)
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            for key in ("text", "content", "record", "input", "case_summary"):
                v = data.get(key)
                if isinstance(v, str) and v.strip():
                    return v
            return json.dumps(data, ensure_ascii=False, indent=2)
        raise ValueError("JSON 输入必须是字符串或包含 text/content/record 字段的对象。")
    return path.read_text(encoding=encoding)


# ---------------------------------------------------------------------------
# 核心推理逻辑
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """你是一名经验丰富的基层医疗机构全科医生，负责为患者提供转诊决策支持。
你的职责是根据患者病情摘要，判断是否需要向上级医院或专科转诊，并给出具体指导。

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言摘要（以"【摘要】"开头）

JSON 结构（严格遵循）：
{
  "referral_decision": "建议立即转诊/建议择期转诊/可在基层处理/暂不需要转诊",
  "urgency": "紧急（立即）/较急（24小时内）/择期（1周内）/不需转诊",
  "target_department": "目标科室（如：心内科、神经科、急诊科等）",
  "target_hospital_level": "三级医院/二级及以上医院/社区上级转诊",
  "referral_reason": "转诊原因的详细说明",
  "referral_criteria_met": [
    "满足的转诊指征，逐条列出"
  ],
  "pre_transfer_measures": [
    "转诊前需完成的处置措施"
  ],
  "transfer_documents_required": [
    "随患者携带的材料（如转诊单、检查报告、用药清单等）"
  ],
  "can_manage_locally_if_no_referral": "如果患者无法转诊时的基层处置建议（无此情况填 null）"
}

转诊决策依据（参考国家分级诊疗政策）：
- 紧急转诊（立即）：急性心梗、脑卒中、严重创伤、休克、急性呼吸衰竭等生命威胁情况
- 较急转诊（24h）：病情不稳定但非即刻生命威胁、基层诊断能力不足的复杂病例
- 择期转诊：慢性病需专科评估、手术治疗、特殊检查等
- 不需转诊：常见病可在基层规范处理

此建议仅供执业医生参考，不替代临床判断"""


def run_referral(case_summary: str, llm, output_path: str = "") -> int:
    prompt = f"""请根据以下患者病情摘要，给出转诊指导建议。

【患者病情】
{case_summary.strip()}

请严格按照要求输出 JSON + 摘要。"""

    print("正在评估患者转诊需求...")
    result = llm([sys_msg(SYSTEM_PROMPT), user_msg(prompt)])

    json_part = ""
    summary_part = ""
    if "【摘要】" in result:
        idx = result.index("【摘要】")
        json_part = result[:idx].strip()
        summary_part = result[idx:].strip()
    else:
        json_part = result

    parsed_json = None
    try:
        if "```" in json_part:
            start = json_part.find("{")
            end = json_part.rfind("}") + 1
            json_part = json_part[start:end]
        parsed_json = json.loads(json_part)
    except json.JSONDecodeError:
        print("⚠ 警告：模型输出的 JSON 无法解析，将原始输出保存。", file=sys.stderr)

    output_lines = []
    if parsed_json:
        output_lines.append(json.dumps(parsed_json, ensure_ascii=False, indent=2))
    else:
        output_lines.append(json_part)
    if summary_part:
        output_lines.append("")
        output_lines.append(summary_part)

    output_text = "\n".join(output_lines)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output_text, encoding="utf-8")
        print(f"\n✓ 转诊指导已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="转诊指导：根据患者病情摘要，判断转诊必要性、紧急程度、目标科室及转诊前准备。"
    )
    parser.add_argument("--input", required=True, help="患者病情摘要文件路径（txt 或 json，UTF-8）。")
    parser.add_argument("--appkey", required=True, help="内部医疗大模型鉴权 key，由平台分配。")
    parser.add_argument("--base", default=DEFAULT_LLM_BASE, help=f"内部大模型 base URL（默认：{DEFAULT_LLM_BASE}）。")
    parser.add_argument("--model", default=DEFAULT_LLM_MODEL, help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。")
    parser.add_argument("--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。")
    parser.add_argument("--output", default="", help="输出文件路径（默认：打印到 stdout）。")
    parser.add_argument("--encoding", default="utf-8", help="输入文件编码（默认：utf-8）。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"✗ Error: 输入文件不存在：{input_path}", file=sys.stderr)
        return 1
    try:
        case_summary = load_input(input_path, args.encoding)
    except Exception as e:
        print(f"✗ 读取输入文件失败：{e}", file=sys.stderr)
        return 1

    llm = make_llm_caller(args.appkey, args.base, args.model, args.timeout)
    try:
        return run_referral(case_summary, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
