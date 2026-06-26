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

RULE_KEY = "hypertension-missing-bp"
RULE_CN = "高血压未记录血压最高值"

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


def qc_hypertension_missing_bp(fields: Dict[str, str], llm) -> str:
    """高血压未记录血压最高值"""
    hpi = fields["hpi"]
    pmh = fields["pmh"]
    pe = fields["pe"]

    # LLM1：患者是否有高血压病史
    has_htn = llm([user_msg(
        f"""给定门诊病历中现病史和既往史字段，判断该患者是否有高血压病史，请直接回答"有"或者"无"，不需要任何分析。

以下是一些示例，用<example></example>标记，请参考

<example>
现病史：现二甲双胍格列吡嗪（250mg/2.5mg）1#Bid，FBG6.4mmol/L，2hPBG7.3mmol/L
既往史：高血压，慢性肾功能不全，流行病学史：-
有
</example>

<example>
现病史：自觉口干，否认体重下降，FBG11.87mmol/L
既往史：动脉硬化，支架置入术后，流行病学史：-
无
</example>

<example>
现病史：现格华止0.5gTid，拜唐苹100mgTid，达格列净10mgQd，FBG17mmol/L，2hPBG22mmol/L
既往史：流行病学史：-
无
</example>

现在请判断下面的门诊病历
现病史：{hpi}
既往史：{pmh}"""
    )])
    if "无" in has_htn and "有" not in has_htn:
        return "无缺陷"

    # 完整质控
    return llm([user_msg(
        f"""你是一位病历质控专家，请对门诊病历进行质控，如果没有缺陷请直接回答"无缺陷"，不要进行任何分析；如果有缺陷请先回答"有缺陷"再另起一行分析原因

缺陷描述：
1.既往史或现病史中记录患者有高血压，但是在现病史、既往史、体格检查中，没有写明最高血压值
2.只需关注高血压，其他症状（如高血脂、高血糖、高尿酸等）请忽略，直接回答"无缺陷"

以下是一些示例，用<example></example>标记，请参考

<example>
【病历】
现病史：患者1年前无明显诱因出现口干症状，饮水后不能缓解，伴体重增加10kg，无多饮、多尿等症状，未行相关检查。
既往史：有高血压病史5年，平素口服药物治疗，血压控制差。
体格检查：心率82次/分
【质控结果】
有缺陷
有高血压病史，但是没有记录血压最高值
</example>

<example>
【病历】
现病史：患者1年前无明显诱因出现口干症状，饮水后不能缓解，伴体重增加10kg，无多饮、多尿等症状，未行相关检查。
既往史：有高血压病史5年，平素口服药物治疗，血压控制差。
体格检查：心率82次/分，血压150/90mmgh
【质控结果】
无缺陷
体格检查中有记录血压值
</example>

<example>
【病历】
现病史：血压最高192/?mmHg，现比索洛尔5mgQd，监测BP140/60mmHg，间断补钾治疗，自觉心悸、乏力。
既往史：糖尿病10年，现艾托格列净1#Qd，FBG6-7mmol/L，流行病学史：-
【质控结果】
无缺陷
</example>

现在请对下面的门诊病历进行质控
【病历】
现病史：{hpi}
既往史：{pmh}
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
    qc_result = qc_hypertension_missing_bp(fields, llm)

    default_dir = Path("..") / "runs" / "med-emr-qc"
    out = Path(output_path) if output_path else (default_dir / f"{RULE_KEY}.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(qc_result, encoding="utf-8")

    print(f"✓ 质控结果已保存至：{out}")
    print("\n--- 质控结果 ---")
    print(qc_result)
    return qc_result
