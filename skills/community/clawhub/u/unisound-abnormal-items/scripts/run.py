#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常指标专项解读：对体检报告中的异常项目进行深度专项解读，
逐项说明异常原因、影响、干预措施，语言面向受检者通俗易懂。
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
            for key in ("text", "content", "record", "input", "report"):
                v = data.get(key)
                if isinstance(v, str) and v.strip():
                    return v
            return json.dumps(data, ensure_ascii=False, indent=2)
        raise ValueError("JSON 输入必须是字符串或包含 text/content/report 字段的对象。")
    return path.read_text(encoding=encoding)


# ---------------------------------------------------------------------------
# 核心推理逻辑
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """你是一名专业的健康管理医生，负责为体检用户提供异常指标的专项深度解读服务。
你的解读需要针对每个异常项目，逐一说明：是什么、为何异常、有什么影响、如何改善。
语言要通俗易懂，让受检者真正理解自己的检查结果，而不是简单复述数字。

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言专项说明（以"【专项解读】"开头），面向受检者，逐项说明

JSON 结构（严格遵循）：
{
  "abnormal_count": 异常指标数量（整数）,
  "items": [
    {
      "item_name": "指标名称（含中文全称，如：甘油三酯 TG）",
      "value": "检测值（含单位）",
      "reference_range": "参考范围",
      "deviation": "偏高/偏低",
      "deviation_degree": "轻度/中度/重度",
      "plain_explanation": "用一两句通俗语言解释这个指标是什么",
      "possible_causes": ["可能的原因，针对受检者背景，1-3条"],
      "health_impact": "对健康的潜在影响（简洁说明）",
      "intervention": {
        "lifestyle": ["生活方式干预建议"],
        "medical": "是否需要就医（需要/定期监测/暂不需要），及就医建议"
      },
      "urgency": "紧急就医/尽快就诊/定期复查/注意观察"
    }
  ],
  "correlations": [
    "多个异常指标之间的关联分析（如血糖升高+血脂升高+超重共同提示代谢综合征风险）"
  ]
}

注意事项：
- plain_explanation 用受检者能理解的语言，避免医学术语堆砌
- possible_causes 要结合受检者年龄、性别、背景（如有）给出针对性原因
- 若多个指标有内在关联（如代谢综合征各指标），在 correlations 中统一分析
- urgency 为"紧急就医"时要特别强调
- 此解读仅供健康管理参考，不替代医生诊断"""


def run_abnormal_items(report_text: str, llm, output_path: str = "") -> int:
    prompt = f"""请对以下体检报告中的异常指标进行专项深度解读。

【体检报告/异常指标信息】
{report_text.strip()}

请严格按照要求输出 JSON + 专项解读。"""

    print("正在进行异常指标专项解读...")
    result = llm([sys_msg(SYSTEM_PROMPT), user_msg(prompt)])

    json_part = ""
    narrative_part = ""
    marker = "【专项解读】"
    if marker in result:
        idx = result.index(marker)
        json_part = result[:idx].strip()
        narrative_part = result[idx:].strip()
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
    if narrative_part:
        output_lines.append("")
        output_lines.append(narrative_part)

    output_text = "\n".join(output_lines)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output_text, encoding="utf-8")
        print(f"\n✓ 异常指标专项解读已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="异常指标专项解读：逐项深度解读体检报告中的异常指标，说明原因、影响和干预措施。"
    )
    parser.add_argument("--input", required=True, help="体检报告或异常指标文件路径（txt 或 json，UTF-8）。")
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
        report_text = load_input(input_path, args.encoding)
    except Exception as e:
        print(f"✗ 读取输入文件失败：{e}", file=sys.stderr)
        return 1

    llm = make_llm_caller(args.appkey, args.base, args.model, args.timeout)
    try:
        return run_abnormal_items(report_text, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
