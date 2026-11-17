#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
居民健康档案管理：从非结构化的就诊记录、体检报告、问卷文本中
抽取结构化居民健康档案信息，符合国家基本公共卫生服务规范。
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
DEFAULT_LLM_MODEL = "u2-med"


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
            for key in ("text", "content", "record", "input", "health_info"):
                v = data.get(key)
                if isinstance(v, str) and v.strip():
                    return v
            return json.dumps(data, ensure_ascii=False, indent=2)
        raise ValueError("JSON 输入必须是字符串或包含 text/content/record 字段的对象。")
    return path.read_text(encoding=encoding)


# ---------------------------------------------------------------------------
# 核心推理逻辑
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """你是一名公共卫生专员，专门负责为基层社区卫生服务机构管理居民健康档案。
你的职责是从非结构化的就诊记录、体检报告或问卷文本中，抽取结构化的居民健康档案信息。

档案结构参考《国家基本公共卫生服务规范（第三版）》居民健康档案要求。

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言摘要（以"【摘要】"开头）

JSON 结构（严格遵循，未提及字段填 null）：
{
  "basic_info": {
    "gender": "性别",
    "age": "年龄",
    "occupation": "职业",
    "education": "文化程度"
  },
  "health_status": {
    "symptoms": ["现有症状"],
    "chronic_diseases": ["慢性病诊断，含诊断年份（如有）"],
    "disabilities": ["残疾情况"],
    "surgery_history": ["手术史"],
    "trauma_history": ["外伤史"],
    "blood_transfusion_history": "输血史"
  },
  "family_history": {
    "diseases": ["家族遗传病或慢性病史"]
  },
  "lifestyle": {
    "smoking": "吸烟状态（从不/已戒/现在吸烟/未提及）",
    "smoking_amount": "日吸烟量（支）",
    "drinking": "饮酒状态（从不/偶尔/经常/每天/未提及）",
    "exercise": "体育锻炼情况",
    "diet": "饮食习惯"
  },
  "physical_exam": {
    "height_cm": null,
    "weight_kg": null,
    "bmi": null,
    "blood_pressure": "收缩压/舒张压 mmHg",
    "heart_rate": null,
    "other_findings": ["其他体检异常发现"]
  },
  "lab_results": {
    "blood_glucose_fasting": null,
    "hba1c": null,
    "blood_lipids": {
      "tc": null,
      "ldl": null,
      "hdl": null,
      "tg": null
    },
    "other": {}
  },
  "current_medications": [
    {
      "drug_name": "药品名",
      "dosage": "剂量",
      "indication": "用途"
    }
  ],
  "health_assessment": {
    "risk_factors": ["健康风险因素"],
    "health_guidance_needed": ["建议提供的健康指导"]
  },
  "follow_up_plan": {
    "frequency": "随访频次建议",
    "next_visit": "下次随访建议时间（如有）",
    "items_to_monitor": ["需重点监测的项目"]
  }
}

注意事项：
- 未在输入中明确提及的字段填 null，不要捏造信息
- 年龄、身高、体重等数值字段填数字或 null
- 慢性病列表需注明诊断年份（如原文提供）
- 此档案仅用于基层健康管理，需由公卫人员复核"""


def run_health_record(health_info: str, llm, output_path: str = "") -> int:
    prompt = f"""请从以下居民健康信息中，抽取结构化居民健康档案。

【居民健康信息】
{health_info.strip()}

请严格按照要求输出 JSON + 摘要（未提及字段填 null，不要捏造）。"""

    print("正在提取居民健康档案信息...")
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
        print(f"\n✓ 健康档案已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="居民健康档案管理：从非结构化就诊/体检文本中抽取结构化健康档案，符合国家公共卫生服务规范。"
    )
    parser.add_argument("--input", required=True, help="居民健康信息文件路径（txt 或 json，UTF-8）。")
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
        health_info = load_input(input_path, args.encoding)
    except Exception as e:
        print(f"✗ 读取输入文件失败：{e}", file=sys.stderr)
        return 1

    llm = make_llm_caller(args.appkey, args.base, args.model, args.timeout)
    try:
        return run_health_record(health_info, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
