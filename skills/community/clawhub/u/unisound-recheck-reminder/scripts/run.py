#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复查提醒：根据体检报告中需要复查的异常项，生成清晰的复查提醒清单，
包括每项复查的时间窗、复查机构建议、复查目的和准备事项。
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

SYSTEM_PROMPT = """你是一名专业的健康管理师，负责为体检机构客户生成个性化复查提醒。
你的任务是从体检报告中提取所有需要复查的项目，并为每项生成明确、可执行的复查提醒。

复查分类原则：
- 紧急复查（2周内）：危急值、高度可疑恶性病变（如：甲状腺结节TI-RADS 4-5类、乳腺BI-RADS 4-5类、肿瘤标志物明显升高）
- 短期复查（1-3个月）：中度异常指标、可疑病变需进一步确诊（如：宫颈ASCUS、BI-RADS 3类结节随访、血糖异常）
- 中期复查（3-6个月）：轻度异常指标治疗/干预后评估（如：轻度血脂异常生活方式干预后复查）
- 长期复查（6-12个月）：需定期随访的慢性问题（如：TI-RADS 2-3类结节年度随访）

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言复查提醒（以"【复查提醒】"开头），面向受检者，简洁清晰

JSON 结构（严格遵循）：
{
  "recheck_count": 需复查项目总数（整数）,
  "has_urgent": 是否有紧急复查项（true/false）,
  "items": [
    {
      "item": "需复查的项目名称",
      "current_finding": "本次体检结果简述",
      "recheck_urgency": "紧急（2周内）/短期（1-3个月）/中期（3-6个月）/长期（6-12个月）",
      "recheck_exam": "复查需做的具体检查项目",
      "recheck_venue": "建议复查机构（体检机构/二级及以上医院/专科门诊）",
      "recheck_department": "就诊科室（如适用）",
      "purpose": "复查目的（一句话说明）",
      "preparation": ["复查前注意事项，如：空腹/停药/避免剧烈运动等"],
      "what_to_watch": "在复查前需关注的症状或变化"
    }
  ],
  "grouped_by_venue": {
    "urgent_medical_referral": ["需立即转诊至医院的项目"],
    "followup_at_exam_center": ["可在本体检机构复查的项目"],
    "self_monitoring": ["可自行居家监测的项目（如血压、血糖）"]
  }
}

注意事项：
- 按紧急程度从高到低排列 items
- recheck_exam 要具体（如"乳腺钼靶"而非"乳腺检查"）
- 对于影像学结节类发现，严格按 TI-RADS/BI-RADS 分类标准给出随访时间
- 此提醒仅供参考，最终复查方案由接诊医生决定"""


def run_recheck_reminder(report_text: str, llm, output_path: str = "") -> int:
    prompt = f"""请根据以下体检报告，生成复查提醒清单。

【体检报告】
{report_text.strip()}

请严格按照要求输出 JSON + 复查提醒。"""

    print("正在生成复查提醒...")
    result = llm([sys_msg(SYSTEM_PROMPT), user_msg(prompt)])

    json_part = ""
    narrative_part = ""
    marker = "【复查提醒】"
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
        print(f"\n✓ 复查提醒已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="复查提醒：从体检报告中提取需复查项目，生成含时间窗/机构/准备事项的个性化复查清单。"
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
        return run_recheck_reminder(report_text, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
