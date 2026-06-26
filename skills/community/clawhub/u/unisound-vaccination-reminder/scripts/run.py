#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预防接种提醒：根据居民年龄、接种史和特殊情况（妊娠、免疫缺陷、慢性病等），
依据国家免疫规划及特殊人群建议，生成个性化接种提醒清单。
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
            for key in ("text", "content", "record", "input", "vaccination_info"):
                v = data.get(key)
                if isinstance(v, str) and v.strip():
                    return v
            return json.dumps(data, ensure_ascii=False, indent=2)
        raise ValueError("JSON 输入必须是字符串或包含 text/content/record 字段的对象。")
    return path.read_text(encoding=encoding)


# ---------------------------------------------------------------------------
# 核心推理逻辑
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """你是一名专业的基层公共卫生医生，负责为社区居民提供预防接种指导服务。
你的职责是根据居民的年龄、已接种记录和特殊健康情况，依据国家免疫规划，给出个性化接种提醒。

参考依据（中国国家免疫规划）：

【0-6岁儿童免疫规划疫苗（部分）】
- 乙肝疫苗（HepB）：出生、1月、6月
- 卡介苗（BCG）：出生
- 脊髓灰质炎疫苗（OPV/IPV）：2月、3月、4月、4岁
- 百白破疫苗（DPT）：3月、4月、5月；18月加强；6岁白破二联
- 麻腮风疫苗（MMR）：8月、18月
- 甲肝疫苗（HepA）：18月、24月
- 流脑疫苗（MCV）：6月、9月；3岁、6岁加强
- 乙脑疫苗：8月、2岁
- 水痘疫苗（Var）：1岁、4岁（部分地区）

【成人及特殊人群推荐接种（非免疫规划）】
- 流感疫苗：60岁以上老年人、慢性病患者每年接种
- 肺炎球菌疫苗（PPSV23）：65岁以上老年人、慢性病患者
- 带状疱疹疫苗：50岁以上建议接种
- 乙肝疫苗：未免疫成人建议补种
- HPV疫苗：9-45岁女性（视年龄选择二价/四价/九价）

输出要求：
1. 以 JSON 格式输出（确保可被 json.loads 解析）
2. JSON 之后另起一行输出自然语言摘要（以"【摘要】"开头）

JSON 结构（严格遵循）：
{
  "resident_profile": {
    "age_group": "年龄段（如：婴儿0-1岁/幼儿1-3岁/学龄前/学龄/成人/老年≥60岁）",
    "special_conditions": ["特殊情况，如妊娠、免疫缺陷、慢性病等"]
  },
  "overdue_vaccines": [
    {
      "vaccine_name": "疫苗名称",
      "doses_missed": "漏种剂次描述",
      "priority": "紧急补种/建议尽快/可择期",
      "notes": "特别说明"
    }
  ],
  "due_soon_vaccines": [
    {
      "vaccine_name": "疫苗名称",
      "recommended_timing": "建议接种时间",
      "notes": "说明"
    }
  ],
  "recommended_non_mandatory": [
    {
      "vaccine_name": "非免疫规划疫苗名称",
      "reason": "推荐原因",
      "notes": "说明"
    }
  ],
  "contraindications": [
    "禁忌证提示（如有）"
  ],
  "precautions": [
    "接种前注意事项"
  ],
  "next_visit_suggestion": "建议下次到访接种时间"
}

注意事项：
- 严格依据国家免疫规划程序，不推荐未经批准的接种方案
- 妊娠期禁忌活疫苗（MMR、水痘、卡介苗等）
- 免疫缺陷者禁忌活疫苗，优先灭活疫苗
- 若接种记录不完整，应在输出中注明"需核实接种记录"
- 此建议仅供公卫人员参考，最终由接种医生决定"""


def run_vaccination_reminder(vaccination_info: str, llm, output_path: str = "") -> int:
    prompt = f"""请根据以下居民信息，生成预防接种提醒。

【居民信息】
{vaccination_info.strip()}

请严格按照要求输出 JSON + 摘要。"""

    print("正在生成预防接种提醒...")
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
        print(f"\n✓ 接种提醒已保存至：{out}")
    else:
        print("\n" + "=" * 60)
        print(output_text)

    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="预防接种提醒：依据国家免疫规划和居民接种史，生成个性化接种提醒清单。"
    )
    parser.add_argument("--input", required=True, help="居民接种信息文件路径（txt 或 json，UTF-8）。")
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
        vaccination_info = load_input(input_path, args.encoding)
    except Exception as e:
        print(f"✗ 读取输入文件失败：{e}", file=sys.stderr)
        return 1

    llm = make_llm_caller(args.appkey, args.base, args.model, args.timeout)
    try:
        return run_vaccination_reminder(vaccination_info, llm, args.output)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
