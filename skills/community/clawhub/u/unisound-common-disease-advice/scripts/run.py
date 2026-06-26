#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基层常见病诊疗建议：根据患者主诉、症状、体征及基本信息，
给出鉴别诊断建议、推荐检查和处理意见。
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
        url=url,
        data=data,
        method="POST",
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
            for key in ("text", "content", "record", "input", "patient_info"):
                v = data.get(key)
                if isinstance(v, str) and v.strip():
                    return v
            return json.dumps(data, ensure_ascii=False, indent=2)
        raise ValueError("JSON 输入必须是字符串或包含 text/content/record 字段的对象。")
    return path.read_text(encoding=encoding)


# ---------------------------------------------------------------------------
# 核心推理逻辑
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """你是一名经验丰富的全科医生，专门为基层社区诊所提供临床决策支持。
你的职责是根据患者信息，给出合理的鉴别诊断、推荐检查和初步处理建议。

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言摘要（以"【摘要】"开头）

JSON 结构（严格遵循）：
{
  "possible_diagnoses": [
    {
      "diagnosis": "疾病名称",
      "probability": "高/中/低",
      "basis": "诊断依据简述"
    }
  ],
  "recommended_exams": ["检查项目1", "检查项目2"],
  "treatment_advice": {
    "medication": "药物建议（含药名、剂量、用法）",
    "general": "一般处理建议"
  },
  "warnings": ["注意事项或红旗症状警示"],
  "referral_needed": true/false,
  "referral_reason": "如需转诊，说明原因；不需转诊填 null"
}

注意事项：
- 鉴别诊断按可能性从高到低排列，最多列 3 种
- 药物建议必须符合基层诊所用药目录（优先国家基本药物）
- 有红旗症状时必须在 warnings 中注明，referral_needed 置为 true
- 不能捏造检查结果，仅基于已提供信息推理
- 此建议仅供执业医生参考，不替代临床判断"""


def run_advice(patient_info: str, llm, output_path: str = "") -> int:
    prompt = f"""请根据以下患者信息，给出常见病诊疗建议。

【患者信息】
{patient_info.strip()}

请严格按照要求输出 JSON + 摘要。"""

    print("正在分析患者信息并生成诊疗建议...")
    result = llm([sys_msg(SYSTEM_PROMPT), user_msg(prompt)])

    # 分离 JSON 和摘要
    json_part = ""
    summary_part = ""
    if "【摘要】" in result:
        idx = result.index("【摘要】")
        json_part = result[:idx].strip()
        summary_part = result[idx:].strip()
    else:
        json_part = result

    # 验证 JSON 可解析
    parsed_json = None
    try:
        # 提取 JSON 块（可能包含 markdown 代码块）
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
        print(f"\n✓ 诊疗建议已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="基层常见病诊疗建议：根据患者主诉/症状/体征生成鉴别诊断、推荐检查和处理意见。"
    )
    parser.add_argument("--input", required=True, help="患者信息文件路径（txt 或 json，UTF-8）。")
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
        patient_info = load_input(input_path, args.encoding)
    except Exception as e:
        print(f"✗ 读取输入文件失败：{e}", file=sys.stderr)
        return 1

    llm = make_llm_caller(args.appkey, args.base, args.model, args.timeout)
    try:
        return run_advice(patient_info, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
