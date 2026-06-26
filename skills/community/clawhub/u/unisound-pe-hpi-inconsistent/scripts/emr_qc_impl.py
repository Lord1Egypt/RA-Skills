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

RULE_KEY = "pe-hpi-inconsistent"
RULE_CN = "体格检查结果与现病史不符"

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


def qc_pe_hpi_inconsistent(fields: Dict[str, str], llm) -> str:
    """体格检查结果与现病史不符"""
    pe = fields["pe"]
    hpi = fields["hpi"]
    if not pe or not hpi:
        return "无缺陷"

    return llm([user_msg(
        f"""你是一位病历质控专家，请对门诊病历进行质控，如果没有缺陷请直接回答"无缺陷"，不要进行任何分析；如果有缺陷请先回答"有缺陷"再另起一行分析原因

缺陷描述：
1.现病史提及"昏迷，意识不清，意识障碍，意识模糊"，体格检查中出现"神志清楚，精神可，查体合作，自主体位，步态正常，步入病房"，有缺陷
2.现病史提及"瘫痪"，体格检查中出现"查体合作，自主体位，步态正常，步入病房"，有缺陷
3.现病史提及"口角歪斜"，体格检查中出现"面容正常，面容及表情正常"，有缺陷
4.现病史提及"淤斑淤点"，体格检查中"无淤斑淤点，无皮下出血"，有缺陷
5.现病史提及血红蛋白低于60g/L，体格检查中"无贫血貌"，有缺陷
6.现病史提及触及淋巴结肿大，体格检查中"全身未触及淋巴结肿大"，有缺陷
7.如果体格检查未记录实质性内容，则不存在不符的情况，判定为"无缺陷"

以下是一些示例，用<example></example>标记，请参考

<example>
【病历】
现病史：患者9小时前无明显诱因下出现晕厥，被家属发现后送至急诊。患者呈浅昏迷状态，双侧瞳孔等大等圆，光反迟钝。
体格检查：体温36.0℃ 脉搏112次/分 呼吸22次/分 血压95/54mmHg，发育正常，营养良好，自主体位
【质控结果】
有缺陷
体格检查结果（自主体位）与现病史（浅昏迷）不符
</example>

<example>
【病历】
现病史：患者家属发现患者中昏迷状态，GSC评分E1V1M3。
体格检查：体温37.4℃ 脉搏88次/分 呼吸17次/分 血压143/83mmHg，被动体位
【质控结果】
无缺陷
</example>

<example>
【病历】
现病史：背痛就诊否认高血压
体格检查：血压146/92mmHg，神清状可，双肺（-），HR64次/分，律齐，未及杂音。
【质控结果】
无缺陷
</example>

现在请对下面的门诊病历进行质控，请注意，如果体格检查中提及某种情况而现病史中没有提及，或者现病史提及某种情况而体格检查中没有提及，不触发本条质控规则，直接回答"无缺陷"
【病历】
现病史：{hpi}
体格检查：{pe}
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
    qc_result = qc_pe_hpi_inconsistent(fields, llm)

    default_dir = Path("..") / "runs" / "med-emr-qc"
    out = Path(output_path) if output_path else (default_dir / f"{RULE_KEY}.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(qc_result, encoding="utf-8")

    print(f"✓ 质控结果已保存至：{out}")
    print("\n--- 质控结果 ---")
    print(qc_result)
    return qc_result
