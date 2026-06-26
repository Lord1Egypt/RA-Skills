#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检后随访管理：根据体检报告和异常发现，生成结构化的检后随访计划，
包括随访时间节点、随访内容、健康指导要点，支撑体检闭环服务。
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

SYSTEM_PROMPT = """你是一名专业的健康管理师，负责为体检机构制定客户的检后随访计划，
确保受检者在体检后得到持续的健康管理服务，实现体检闭环。

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言随访通知（以"【随访通知】"开头），面向受检者，语言友好清晰

JSON 结构（严格遵循）：
{
  "followup_summary": {
    "total_followup_items": 需随访的事项总数（整数）,
    "highest_priority": "最高优先级事项一句话描述",
    "exam_date": "本次体检日期（如输入中有提及）"
  },
  "followup_schedule": [
    {
      "timepoint": "随访时间节点（如：1个月内/3个月后/6个月后/1年后）",
      "items": [
        {
          "issue": "需随访的问题/异常项",
          "followup_action": "具体随访行动（如：复查血脂四项/就诊心内科/复查超声）",
          "target_value": "期望达到的目标值或结果（如有）",
          "channel": "随访渠道（医院就诊/本机构复查/线上咨询/居家自测）"
        }
      ]
    }
  ],
  "health_coaching_points": [
    {
      "topic": "健康指导主题（如：饮食管理/运动指导/戒烟/用药依从性）",
      "key_messages": ["核心指导内容，2-3条"],
      "materials_to_provide": ["建议提供给受检者的健康教育资料（如有）"]
    }
  ],
  "alert_conditions": [
    "出现以下情况时需立即就医的预警条件（如：出现胸痛、头晕等症状）"
  ],
  "next_annual_exam_focus": ["下次年度体检建议重点关注的项目"]
}

注意事项：
- followup_schedule 按时间节点从近到远排列
- 对同一个问题，复查和就医就诊要区分清楚
- health_coaching_points 要有针对性，基于本次体检具体问题
- alert_conditions 要实用，让受检者知道什么情况需要立即就医
- 此随访计划仅供健康管理参考"""


def run_followup(report_text: str, llm, output_path: str = "") -> int:
    prompt = f"""请根据以下体检报告，制定检后随访管理计划。

【体检报告】
{report_text.strip()}

请严格按照要求输出 JSON + 随访通知。"""

    print("正在生成检后随访管理计划...")
    result = llm([sys_msg(SYSTEM_PROMPT), user_msg(prompt)])

    json_part = ""
    narrative_part = ""
    marker = "【随访通知】"
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
        print(f"\n✓ 检后随访计划已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="检后随访管理：根据体检报告生成结构化随访计划，含时间节点、随访内容和健康指导要点。"
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
        return run_followup(report_text, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
