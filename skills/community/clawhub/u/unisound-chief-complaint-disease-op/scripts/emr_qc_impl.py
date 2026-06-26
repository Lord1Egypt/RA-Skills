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

RULE_KEY = "chief-complaint-disease-op"
RULE_CN = "主诉不应使用疾病和操作"

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


def qc_chief_complaint_disease_op(fields: Dict[str, str], llm) -> str:
    """主诉不应使用疾病和操作"""
    cc = fields["cc"]
    hpi = fields["hpi"]
    if not cc:
        return "无缺陷"

    # LLM1：判断主诉是否由"疾病名+持续时间"构成
    llm1_result = llm([user_msg(
        f"""任务：判断主诉是否由"疾病名"+"持续时间"构成，并且没有其他内容，请直接回答"是"或者"否"，请注意区分疾病名和症状名，比如"糖尿病"、"高血压"是疾病名；而"心悸"、"口干"、"咳嗽"等是症状名

以下是一些示例，用<example></example>标记，请参考

<example>
糖尿病5年
是
</example>

<example>
高血压10年
是
</example>

<example>
糖尿病
否
</example>

<example>
高血压
否
</example>

<example>
血糖升高
否
</example>

<example>
糖尿病5年，血糖控制不佳
否
</example>

<example>
持续头晕伴耳鸣
否
</example>

<example>
慢性胃炎复查，症状加重
否
</example>

<example>
口干
否
</example>

<example>
咳嗽3天，呼吸困难
否
</example>

现在请判断下面的主诉
{cc}"""
    )])

    # LLM2：判断主诉是否由"操作名+持续时间"构成
    llm2_result = llm([user_msg(
        f"""任务：判断主诉是否由"操作名"+"持续时间"构成，并且没有其他内容，请直接回答"是"或者"否"

以下是一些示例，用<example></example>标记，请参考

<example>
左乳癌术后2月余
是
</example>

<example>
右输尿管支架置入术后1月
是
</example>

<example>
糖尿病20年
否
</example>

<example>
高血压
否
</example>

<example>
肺癌术后
否
</example>

<example>
慢性胃炎复查，症状加重
否
</example>

现在请判断下面的主诉
{cc}"""
    )])

    # 两者均为"否" → 无缺陷
    if "是" not in llm1_result and "是" not in llm2_result:
        return "无缺陷"

    # 否则执行完整质控
    return llm([user_msg(
        f"""你是一位病历质控专家，请对门诊病历进行质控，如果没有缺陷请直接回答"无缺陷"，不要进行任何分析；如果有缺陷请先回答"有缺陷"再另起一行分析原因

缺陷描述：
1.如果主诉是疾病名+持续时间，并且现病史中有与该疾病同时出现且持续时间相同的症状，这种情况下应当使用症状作为主诉而不是疾病名，回答"有缺陷"
2.如果主诉是操作名+持续时间，并且现病史中有与该操作同时出现且持续时间相同的症状，这种情况下应当适用症状作为主诉而不是操作名，回答"有缺陷"

以下是一些示例，用<example></example>标记，请参考

<example>
【病历】
主诉：发现乙肝4年。
现病史：患者诉4年前无明显诱因出现乏力，纳差，当地医院就医，诊断为"乙型病毒性肝炎"，给予护肝（药名不详）等治疗，症状时轻时重，近半年来间有鼻出血、牙龈出血。3天前无明显诱因出现黑便、呕血。
【质控结果】
有缺陷
主诉中有疾病名，现病史有与该疾病同时出现且持续时间相同的症状（乏力、纳差）
</example>

<example>
【病历】
主诉：发现乙肝4年。
现病史：患者诉4年前诊断为"乙型病毒性肝炎"，给予护肝（药名不详）等治疗，症状时轻时重，近半年来间有鼻出血、牙龈出血。3天前无明显诱因出现黑便、呕血。
【质控结果】
无缺陷
主诉是疾病名，现病史中没有与该疾病同时出现且持续时间相同的症状
</example>

<example>
【病历】
主诉：胰腺癌术后2年余。
现病史: 患者2年余前因上腹部疼痛检查发现胰腺占位，在上海交通大学附属仁济医院行手术治疗，具体手术方式不详，病理报告未见。术后予以替吉奥单药口服化疗8周期。病程中，腹痛时轻时重，今日自觉腹痛难忍，为进一步诊治来我院，急诊以"胰腺恶性肿瘤"收住我科。
【质控结果】
有缺陷
主诉是操作名，现病史有与该操作同时出现且持续时间相同的症状（腹痛）
</example>

<example>
【病历】
主诉：右输尿管支架置入术后1月。
现病史:患者一月前因右输尿管结石于我院行右输尿管支架置入术，手术顺利；病程中无恶心、呕吐，无发热、畏寒，无排尿困难，无肉眼血尿，无尿流中断。今患者为进一步诊治，遂至我院就诊，拟"右输尿管支架置入术后"收入院。病程中，患者神清，精神可，大便正常，食纳睡眠正常，近期体重无明显变化
【质控结果】
无缺陷
主诉是操作名，现病史中没有与该操作同时出现且持续时间相同的症状
</example>

现在请对下面的病历进行质控
【病历】
主诉：{cc}
现病史：{hpi}
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
    qc_result = qc_chief_complaint_disease_op(fields, llm)

    default_dir = Path("..") / "runs" / "med-emr-qc"
    out = Path(output_path) if output_path else (default_dir / f"{RULE_KEY}.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(qc_result, encoding="utf-8")

    print(f"✓ 质控结果已保存至：{out}")
    print("\n--- 质控结果 ---")
    print(qc_result)
    return qc_result
