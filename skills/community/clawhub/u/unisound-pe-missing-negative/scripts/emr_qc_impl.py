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

RULE_KEY = "pe-missing-negative"
RULE_CN = "体格检查缺少与诊断相关的体征"

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


def qc_pe_missing_negative(fields: Dict[str, str], llm) -> str:
    """体格检查缺少与诊断相关的体征"""
    pe = fields["pe"]
    dx = fields["dx"]
    if not pe or not dx:
        return "无缺陷"
    # 若体格检查已包含呼吸/心脏体征关键词，可跳过
    if "音" in pe or "律" in pe:
        return "无缺陷"

    return llm([user_msg(
        f"""你是一位病历质控专家，请对门诊病历进行质控，如果没有缺陷请直接回答"无缺陷"，不要进行任何分析；如果有缺陷请先回答"有缺陷"再另起一行分析原因

缺陷描述：
体格检查中缺少与诊断相关的体征，具体：患者诊断为"肝硬化失代偿期"
查找"肝硬化失代偿期"对应的主要体征，根据《实用内科学》对"失代偿期肝硬化"体征的介绍，认为"肝硬化失代偿期"主要体征包括"面色晦暗，肝掌、蜘蛛痣，腹壁静脉曲张"等。
在"体格检查"中查找对应体征是否书写，无论阳性阴性，比如写成"患者面色红润，无肝掌，无蜘蛛痣，无腹壁静脉曲张…"，则判定为"无缺陷"；如果没有提及，则判定为"有缺陷"

以下是一些示例，用<example></example>标记，请参考

<example>
【病历】
体格检查：T:37℃ P:84次/分 R:20次/分 BP:114/64mmHg
诊断：腹腔积液，高血压病3级（很高危）
【质控结果】
有缺陷
体格检查中未提及"移动性浊音，液波震颤"
</example>

<example>
【病历】
体格检查：T:37℃ P:84次/分 R:20次/分 BP:114/64mmHg
诊断：慢性阻塞性肺疾病急性发作
【质控结果】
有缺陷
体格检查中未提及"杵状指，语音震颤情况，双肺叩诊情况"
</example>

<example>
【病历】
体格检查：双肺未闻及啰音
诊断：肺部感染肺部阴影
【质控结果】
无缺陷
</example>

现在请对下面的门诊病历进行质控，诊断类型仅限于以下几种，如果不是，请直接回答"无缺陷"
1.肺部感染、社区获得性肺炎、肺炎、支气管扩张伴感染，体格检查中未提及"呼吸音（呼吸音、啰音、叩诊）"
2.慢性阻塞性肺疾病，体格检查中未提及"呼吸音（呼吸音、啰音、叩诊、杵状指）"
3.心律失常、室性期前收缩、室性早搏、心房颤动、阵发性心房颤动、持续性心房颤动、房性期前收缩，体格检查中未提及"心音（心率、心律、心音、杂音或额外心音）"
4.脾大，体格检查中未提及"脾脏触诊"
5.肾结石，体格检查中未提及"（肾区叩击痛）"
6.腰椎间盘突出，体格检查中未提及"股神经牵拉试验,直腿抬高试验,状肌试验,直腿抬高加强试验（直腿抬高试验、脊柱生理弯曲或脊柱无畸形、棘突压痛或脊柱压痛）"
7.腹水、腹腔积液，体格检查中未提及"移动性浊音,液波震颤"
8.胸腔积液，体格检查中未提及"语音震颤减弱,叩诊浊音,异常呼吸音（语音震颤或语音共振、叩诊、呼吸音、胸膜摩擦感、胸膜摩擦音）"
9.白血病，体格检查中未提及"全身皮肤有无出血点,瘀斑瘀点（胸骨压痛，皮肤黏膜出血点或瘀斑瘀点）"
10.低蛋白血症，体格检查中未提及"浮肿（眼睑有无浮肿，双下肢水肿）"
11.二尖瓣狭窄，体格检查中未提及"二尖瓣面容（面容、心率、心律、心音、杂音或额外心音、震颤）"
12.肝硬化，体格检查中未提及"腹水,腹壁静脉曲张（肝掌、蜘蛛痣、皮肤黏膜有无黄染、腹壁静脉曲张、肝脏触诊）"

【病历】
体格检查：{pe}
诊断：{dx}
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
    qc_result = qc_pe_missing_negative(fields, llm)

    default_dir = Path("..") / "runs" / "med-emr-qc"
    out = Path(output_path) if output_path else (default_dir / f"{RULE_KEY}.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(qc_result, encoding="utf-8")

    print(f"✓ 质控结果已保存至：{out}")
    print("\n--- 质控结果 ---")
    print(qc_result)
    return qc_result
