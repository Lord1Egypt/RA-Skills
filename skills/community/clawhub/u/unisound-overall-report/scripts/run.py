#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
体检报告整体解读：对完整体检报告进行综合分析，
生成易于理解的整体解读摘要、主要发现总结和优先关注事项。
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

SYSTEM_PROMPT = """你是一名专业的健康管理医生，负责为体检中心客户提供体检报告整体解读服务。
你的解读需要专业准确，同时语言通俗易懂，让没有医学背景的受检者也能理解自己的健康状况。

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言整体解读（以"【整体解读】"开头），面向受检者，语言友好通俗

JSON 结构（严格遵循）：
{
  "overall_grade": "优秀/良好/需关注/需重视",
  "summary": "一句话总结本次体检整体情况（100字以内）",
  "key_findings": [
    {
      "category": "类别（如：心血管、代谢、消化、影像等）",
      "finding": "发现的主要问题简述",
      "severity": "正常/轻度异常/中度异常/重度异常",
      "action_needed": "建议行动（如：定期监测/就医复诊/紧急就医）"
    }
  ],
  "normal_systems": ["各项正常的系统/项目简要列举"],
  "priority_actions": [
    {
      "rank": 1,
      "action": "最优先需要处理的事项",
      "reason": "原因"
    }
  ],
  "lifestyle_advice": [
    "针对本次体检结果的个性化生活方式建议"
  ],
  "next_exam_suggestion": "下次体检建议时间（如：6个月后/1年后）及重点项目"
}

注意事项：
- overall_grade 综合所有发现后给出，有严重异常项时不能评为"优秀"或"良好"
- key_findings 只列异常或需关注的发现，按重要程度排序
- priority_actions 最多列 3 条，聚焦最关键的行动
- 语言通俗、积极引导，避免过度恐慌化表达
- 此解读仅供健康管理参考，正式诊断须由执业医生确定"""


def run_overall_report(report_text: str, llm, output_path: str = "") -> int:
    prompt = f"""请对以下体检报告进行整体解读。

【体检报告】
{report_text.strip()}

请严格按照要求输出 JSON + 整体解读。"""

    print("正在进行体检报告整体解读...")
    result = llm([sys_msg(SYSTEM_PROMPT), user_msg(prompt)])

    json_part = ""
    narrative_part = ""
    marker = "【整体解读】"
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
        print(f"\n✓ 体检报告整体解读已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="体检报告整体解读：对完整体检报告进行综合分析，生成整体评级、主要发现和优先行动建议。"
    )
    parser.add_argument("--input", required=True, help="体检报告文件路径（txt 或 json，UTF-8）。")
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
        return run_overall_report(report_text, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
