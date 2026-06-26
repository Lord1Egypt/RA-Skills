#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本 skill 独立质控实现：与同目录 `emr_qc.py`、`run.py` 一并打包发布，无其它 emr-qc 子目录依赖。
LLM：HiVoice MaaS OpenAI 兼容接口（默认 https://maas-api.hivoice.cn/v1）。
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import urllib.error
import urllib.request


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

DEFAULT_LLM_BASE = "https://maas-api.hivoice.cn/v1"
DEFAULT_LLM_MODEL = "u1-insuremed"


# ---------------------------------------------------------------------------
# 本 skill 固定规则
# ---------------------------------------------------------------------------

RULE_KEY = "pmh-missing-bp-glucose"
RULE_CN = "既往史缺血压血糖控制情况"

# ---------------------------------------------------------------------------
# 本条质控规则
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# LLM 调用（OpenAI 兼容接口，使用标准库，无额外依赖）
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
    """返回一个 llm(messages) → str 的调用函数。"""
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
# 病历字段解析（与 Dify 代码节点逻辑相同）
# ---------------------------------------------------------------------------

def parse_record(record: str) -> Dict[str, str]:
    """解析门诊病历文本，提取各字段。"""
    fields = {k: "" for k in ("cc", "hpi", "pmh", "pe", "lab", "dx", "plan")}
    record = record.replace("：", ":")
    for line in record.split("\n"):
        line = line.strip()
        if line.startswith("主诉:"):
            fields["cc"] = line.replace("主诉:", "", 1).strip()
        elif line.startswith("现病史:"):
            fields["hpi"] = line.replace("现病史:", "", 1).strip()
        elif line.startswith("既往史:"):
            fields["pmh"] = line.replace("既往史:", "", 1).strip()
        elif line.startswith("体格检查:"):
            fields["pe"] = line.replace("体格检查:", "", 1).strip()
        elif line.startswith("辅助检查:"):
            fields["lab"] = line.replace("辅助检查:", "", 1).strip()
        elif line.startswith("初步诊断:") or line.startswith("诊断:"):
            fields["dx"] = line.replace("初步诊断:", "", 1).replace("诊断:", "", 1).strip()
        elif line.startswith("处理意见:") or line.startswith("处理:"):
            fields["plan"] = line.replace("处理意见:", "", 1).replace("处理:", "", 1).strip()
    return fields


def qc_pmh_missing_bp_glucose(fields: Dict[str, str], llm) -> str:
    """既往史缺血压血糖控制情况"""
    pmh = fields["pmh"]
    if not pmh:
        return "无缺陷"

    # LLM1：既往史中是否已包含用药/控制相关关键词（快速判断）
    has_keywords = llm([user_msg(
        f"""给定门诊病历中既往史字段，请判断其中是否包含"降糖药"，"降压药"，"控制血糖"，"控制血压"或者相关的描述，请直接回答"是"或者"否"

既往史：{pmh}"""
    )])
    # 若已包含控制信息关键词，则跳过完整质控
    if "是" in has_keywords and "否" not in has_keywords:
        return "无缺陷"

    # 完整质控
    return llm([user_msg(
        f"""你是一位病历质控专家，请对门诊病历进行质控，如果没有缺陷请直接回答"无缺陷"，不要进行任何分析；如果有缺陷请先回答"有缺陷"再另起一行分析原因

缺陷描述：
1.既往史中记录高血压，但是没有记录血压控制情况
2.既往史中描述糖尿病，但是没有记录血糖控制情况

请注意，控制情况包含但不限于以下几种
- 血糖有具体数值mmol/L，血压有具体数值和mmgh
- 控制尚可
- 控制可
- 未监测
- 控制良好
- 控制不佳
- 轻度异常
- 波动明显
- 稳定
- 有记录
- 有症状
- 治疗效果不佳
- 随访中

以下是一些示例，用<example></example>标记，请参考

<example>
【病历】
既往史：高血压病史10年，长期口服缬沙坦。
【质控结果】
有缺陷
有高血压病史，但是没有记录血压情况
</example>

<example>
【病历】
既往史：高血压病史10年，长期口服吲达帕胺，近期血压140/90mmgh
【质控结果】
无缺陷
</example>

<example>
【病历】
既往史：高血压病史年，口服药物治疗，控制良好；糖尿病病史年，口服药物/注射胰岛素治疗，控制良好
【质控结果】
无缺陷
</example>

<example>
【病历】
既往史：糖尿病史：10年，药物控制，控制不佳
【质控结果】
无缺陷
</example>

现在请对下面的门诊病历进行质控
【病历】
既往史：{pmh}
【质控结果】"""
    )])


def read_record(path: str) -> str:
    p = Path(path)
    if not p.exists():
        fallback = Path(__file__).resolve().parents[4] / "data" / "med-emr-qc" / p.name
        if fallback.exists():
            p = fallback
        else:
            raise FileNotFoundError(f"Input file not found: {path}")
    return p.read_text(encoding="utf-8")


def run_qc(
    record: str,
    appkey: str,
    *,
    base: str = DEFAULT_LLM_BASE,
    model: str = DEFAULT_LLM_MODEL,
    timeout: int = 0,
    output_path: Optional[str] = None,
) -> str:
    print(f"质控规则：{RULE_CN}（{RULE_KEY}）")

    fields = parse_record(record)
    llm = make_llm_caller(appkey, base=base, model=model, timeout=timeout)
    qc_result = qc_pmh_missing_bp_glucose(fields, llm)

    default_dir = Path("..") / "runs" / "med-emr-qc"
    out = Path(output_path) if output_path else (default_dir / f"{RULE_KEY}.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(qc_result, encoding="utf-8")

    print(f"✓ 质控结果已保存至：{out}")
    print("\n--- 质控结果 ---")
    print(qc_result)
    return qc_result
