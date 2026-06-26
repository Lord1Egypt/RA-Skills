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

RULE_KEY = "chief-complaint-diagnosis-inconsistent"
RULE_CN = "主诉和诊断部位不一致"

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


def qc_chief_complaint_diagnosis_inconsistent(fields: Dict[str, str], llm) -> str:
    """主诉和诊断部位不一致"""
    cc = fields["cc"]
    dx = fields["dx"]

    # LLM1：主诉中是否包含身体部位
    cc_has_loc = llm([sys_msg(
        f"""给定门诊病历中主诉字段，请判断其中是否包含身体部位的描述，请直接回答"包含"或者"不包含"

请注意，这里指的是"上"、"下"、"左"、"右"、"单侧"、"双侧"等具体部位的描述，以下是一些示例，用<example></example>标记，请参考

<example>
咳嗽一月胸痛半月要求查明原因
不包含
</example>

<example>
发现背部肿物20天
不包含
</example>

<example>
腹痛2天
不包含
</example>

<example>
右上前牙牙龈起包1月余
包含
</example>

<example>
右手外伤1天
包含
</example>

请对下面的主诉进行判断
{cc}"""
    )])
    if "不包含" in cc_has_loc:
        return "无缺陷"

    # LLM2：诊断中是否包含身体部位
    dx_has_loc = llm([sys_msg(
        f"""给定门诊病历中初步诊断字段，请判断其中是否包含身体部位的描述，请直接回答"包含"或者"不包含"

请注意，这里指的是"上"、"下"、"左"、"右"、"单侧"、"双侧"等具体部位的描述，以下是一些示例，用<example></example>标记，请参考

<example>
幽门螺旋杆菌感染
不包含
</example>

<example>
皮肤感染。寻常疣。皮赘
不包含
</example>

<example>
高钾血症肝损伤
不包含
</example>

<example>
1.27牙体缺损2.27继发龋
不包含
</example>

<example>
外阴炎
不包含
</example>

<example>
面部裂伤
不包含
</example>

<example>
疼痛待查腰椎间盘突出症
不包含
</example>

<example>
双眼结膜炎
包含
</example>

<example>
右髋疼痛待查
包含
</example>

请对下面的初步诊断进行判断
{dx}"""
    )])
    if "不包含" in dx_has_loc:
        return "无缺陷"

    # 完整质控
    return llm([user_msg(
        f"""你是一位病历质控专家，给定门诊病历中的主诉和初步诊断，请判断主诉和初步诊断中症状部位是否一致。如果一致请直接回答"无缺陷"，不要分析原因；如果不一致请先回答"有缺陷"，然后另起一行分析原因。

请注意：
1.如果主诉中指明了身体部位的某一方位，但是初步诊断中没有指明具体的位置，比如主诉中描述"左下腹痛"，而初步诊断中描述"下腹痛"，请回答"无缺陷"
2.如果主诉和初步诊断是描述的不同的症状，比如主诉描述的"左下腹痛"，而初步诊断记录的"卵巢囊肿"，请回答"无缺陷"

以下是一些示例，用<example></example>标记，请参考

<example>
主诉：双眼突出3年
诊断：双眼屈光不正
无缺陷
</example>

<example>
主诉：右侧阴囊肿大
诊断：右侧腹股沟斜疝
无缺陷
</example>

<example>
主诉：右眼红3天
诊断：双眼结膜炎
无缺陷
</example>

<example>
主诉：右膝关节疼痛伴肿胀1月
诊断：左膝关节滑膜炎
有缺陷
因为主诉中是"右膝关节疼痛"，而初步诊断中是"左膝关节滑膜炎"，部位不一致，有缺陷
</example>

<example>
主诉：右肩部疼痛并活动不灵活半年
诊断：左肩肩周炎，神经病变待查
有缺陷
因为主诉中是"右肩部疼痛"，而初步诊断中是"左肩肩周炎"，部位不一致，有缺陷
</example>

现在请对下面的主诉和初步诊断进行判断
主诉：{cc}
诊断：{dx}"""
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
    qc_result = qc_chief_complaint_diagnosis_inconsistent(fields, llm)

    default_dir = Path("..") / "runs" / "med-emr-qc"
    out = Path(output_path) if output_path else (default_dir / f"{RULE_KEY}.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(qc_result, encoding="utf-8")

    print(f"✓ 质控结果已保存至：{out}")
    print("\n--- 质控结果 ---")
    print(qc_result)
    return qc_result
