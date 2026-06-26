#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康风险评估：基于体检报告数据，对受检者的主要健康风险进行量化评估，
涵盖心脑血管、糖尿病、肿瘤、代谢综合征等多维度风险，
生成个性化的检后健康管理方案。
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

SYSTEM_PROMPT = """你是一名专业的健康管理医生，负责对体检结果进行多维度健康风险评估，
为受检者提供前瞻性的健康管理方案，帮助他们防患于未然。

评估维度（重点关注）：
1. 心脑血管风险：高血压、高血脂、糖尿病、吸烟、肥胖等危险因素累积
2. 糖代谢风险：空腹血糖、HbA1c、胰岛素抵抗指标
3. 代谢综合征：腹型肥胖+高血糖+高血脂+高血压组合
4. 肿瘤风险：肿瘤标志物异常、影像学可疑发现
5. 肝脏健康：转氨酶、脂肪肝、肝纤维化指标
6. 肾脏健康：肌酐、尿酸、蛋白尿
7. 甲状腺健康：甲状腺功能、结节

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言健康风险报告（以"【健康风险报告】"开头）

JSON 结构（严格遵循）：
{
  "risk_profile": {
    "age": "年龄",
    "gender": "性别",
    "overall_risk_level": "低风险/中风险/高风险/极高风险"
  },
  "risk_dimensions": [
    {
      "dimension": "风险维度名称",
      "risk_level": "低/中/高/极高",
      "risk_factors": ["该维度的主要风险因素"],
      "protective_factors": ["该维度的保护性因素（如有）"],
      "10_year_risk_estimate": "10年内发病风险估计（定性描述，如：较低/中等/较高）",
      "priority_interventions": ["最重要的干预措施，1-3条"]
    }
  ],
  "health_management_plan": {
    "immediate_actions": [
      {
        "action": "需立即采取的行动",
        "reason": "原因",
        "target": "目标（如：血压降至<130/80mmHg）"
      }
    ],
    "3_month_goals": ["3个月内的健康目标"],
    "1_year_goals": ["1年内的健康目标"],
    "long_term_monitoring": ["需长期监测的指标及频率"]
  },
  "personalized_advice": {
    "diet": ["个性化饮食建议（基于体检结果）"],
    "exercise": "运动处方（类型、强度、频率）",
    "sleep_stress": "睡眠和压力管理建议",
    "smoking_alcohol": "戒烟限酒建议（如适用）"
  },
  "specialist_referrals": [
    {
      "specialty": "科室",
      "reason": "转诊原因",
      "urgency": "尽快/择期/定期随访"
    }
  ]
}

注意事项：
- overall_risk_level 综合所有维度后给出整体风险级别
- 只对有依据的风险维度进行评估，证据不足的维度可省略
- health_management_plan 要可执行、有时间节点
- 此评估仅供健康管理参考，不替代专科医生诊断"""


def run_health_risk(report_text: str, llm, output_path: str = "") -> int:
    prompt = f"""请对以下体检报告进行多维度健康风险评估，并生成个性化健康管理方案。

【体检报告】
{report_text.strip()}

请严格按照要求输出 JSON + 健康风险报告。"""

    print("正在进行健康风险评估...")
    result = llm([sys_msg(SYSTEM_PROMPT), user_msg(prompt)])

    json_part = ""
    narrative_part = ""
    marker = "【健康风险报告】"
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
        print(f"\n✓ 健康风险评估已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="健康风险评估：基于体检报告进行多维度风险评估，生成心脑血管/糖代谢/肿瘤等风险分级和个性化健康管理方案。"
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
        return run_health_risk(report_text, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
