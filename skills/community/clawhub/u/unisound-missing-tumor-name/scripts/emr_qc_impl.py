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

RULE_KEY = "missing-tumor-name"
RULE_CN = "未记录肿瘤名称"

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


def qc_missing_tumor_name(fields: Dict[str, str], llm) -> str:
    """未记录肿瘤名称"""
    hpi = fields["hpi"]
    pmh = fields["pmh"]

    # LLM1：是否有肿瘤/癌症病史
    has_tumor = llm([user_msg(
        f"""给定门诊病历中现病史和既往史字段，判断该患者是否有肿瘤或者癌症病史，请直接回答"有"或者"无"，不需要任何分析。

以下是一些示例，用<example></example>标记，请参考

<example>
现病史：未用药，否认口干、多饮、多尿、体重下降
既往史：乳腺恶性肿瘤术后，现靶向治疗。否认胰腺炎。
有
</example>

<example>
现病史：甲状腺乳头状癌术后2年。术后病理：甲状腺乳头状癌，经典型及滤泡亚型。现优甲乐100ug，否认心慌、手抖、多汗、体重下降。
既往史：2014诊断甲亢，赛治治疗，现已停药。
有
</example>

<example>
现病史：少痰，不烧复查CT，伴关节疼痛
既往史：肺部结节病史，过敏史：无。传染病史：无。
无
</example>

现在请判断下面的门诊病历
现病史：{hpi}
既往史：{pmh}"""
    )])
    if "无" in has_tumor and "有" not in has_tumor:
        return "无缺陷"

    # 完整质控
    return llm([user_msg(
        f"""你是一位病历质控专家，请对门诊病历进行质控，如果没有缺陷请直接回答"无缺陷"，不要进行任何分析；如果有缺陷请先回答"有缺陷"再另起一行分析原因

缺陷描述：
1.既往史或现病史中记录患者有肿瘤或者癌症病史，没有记录具体的肿瘤或者癌症名称
2.任何带有部位的肿瘤或者癌症，都认为是有肿瘤名称，请直接回答"无缺陷"，比如"甲状腺Ca"、"肺癌"、"肺部肿瘤"、"结肠癌"、"淋巴瘤"、"脑膜瘤"、"脑淋巴瘤"、"乳腺癌"、"直肠癌"、"直肠肿瘤"等等

以下是一些示例，用<example></example>标记，请参考

<example>
【病历】
现病史：体重下降
既往史：结肠癌术后，磺胺药敏史
【质控结果】
无缺陷
</example>

<example>
【病历】
现病史：未用药，否认口干、多饮、多尿、体重下降
既往史：乳腺恶性肿瘤术后，现靶向治疗。否认胰腺炎。
【质控结果】
无缺陷
</example>

<example>
【病历】
现病史：不烧，自觉胸背部不适，偶有咳痰。
既往史：肾功能不全，肿瘤病史，过敏史：无。传染病史：无。
【质控结果】
有缺陷
既往史中记录"肿瘤病史"，但是没有记录具体的肿瘤名称
</example>

现在请对下面的门诊病历进行质控
【病历】
现病史：{hpi}
既往史：{pmh}
【质控结果】"""
    )])


# ---------------------------------------------------------------------------


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
    qc_result = qc_missing_tumor_name(fields, llm)

    default_dir = Path("..") / "runs" / "med-emr-qc"
    out = Path(output_path) if output_path else (default_dir / f"{RULE_KEY}.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(qc_result, encoding="utf-8")

    print(f"✓ 质控结果已保存至：{out}")
    print("\n--- 质控结果 ---")
    print(qc_result)
    return qc_result
