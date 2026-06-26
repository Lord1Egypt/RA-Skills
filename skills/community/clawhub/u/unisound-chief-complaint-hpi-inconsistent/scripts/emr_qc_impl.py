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

RULE_KEY = "chief-complaint-hpi-inconsistent"
RULE_CN = "主诉和现病史描述不一致"

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


def qc_chief_complaint_hpi_inconsistent(fields: Dict[str, str], llm) -> str:
    """主诉和现病史描述不一致"""
    cc = fields["cc"]
    hpi = fields["hpi"]
    if not cc or not hpi:
        return "无缺陷"

    # LLM1：判断主诉类型（症状/疾病名/操作名/其他）
    cc_type = llm([user_msg(
        f"""你是一名医疗助理，负责分析患者的主诉（即患者到医院时描述的主要不适）。你的任务是判断这些主诉属于哪种类型：症状、疾病名、操作名、或其他。

症状：患者能直接感受到的身体或精神上的不适，例如"头痛"或"恶心"。
疾病名：已确诊的医学病症名称，例如"糖尿病"。
操作名：描述某些医疗操作或过程，例如"拔牙"或"换药"。
其他：不符合以上三类的主诉。
请基于输入的主诉，返回所属类别。

以下是一些示例，用<example></example>标记，请参考

<example>
主诉：头晕乏力
症状
</example>

<example>
主诉：糖尿病
疾病名
</example>

<example>
主诉：咳嗽
症状
</example>

<example>
主诉：拔牙
操作名
</example>

<example>
主诉：健康检查
操作名
</example>

<example>
主诉：高血压
疾病名
</example>

<example>
主诉：胸闷气短
症状
</example>

<example>
主诉：复查
其他
</example>

现在请判断下面的主诉，请直接回答类型，避免任何分析
主诉：{cc}"""
    )])

    # 如果不是症状类型 → 无缺陷
    if "症状" not in cc_type:
        return "无缺陷"

    # 完整质控
    return llm([user_msg(
        f"""你是一位病历质控专家，给定门诊病历中的主诉和现病史，请判断主诉和现病史是否有描述不一致的情况。如果一致请直接回答"无缺陷"，不要分析原因；如果不一致请先回答"有缺陷"，然后另起一行分析原因。

以下6种情况都是不一致的情况，都算是缺陷病历，请必须注意，只有当主诉为症状描述时，才进行质控，如果主诉是疾病名、操作名或者其他任何非症状描述，请直接回答"无缺陷"
1.同一症状的部位不一致，如主诉中记录"右下肢水肿1周"，但是现病史中记录"1周前发现左下肢水肿"
2.同一症状描述不一致，如主诉中记录"间断气短2月，加重3天"，但是现病史中记录"2月前出现间断性气短，自行口服药物治疗，症状较前有所减轻"
3.同一症状持续时间不一致，如主诉中记录"咳痰20余天"，但是现病史中记录"1周前出现咳痰"
4.主诉中症状在现病史中未描述，如主诉中记录"咳嗽5天"，但是现病史中没有提及任何与咳嗽相关的内容；
5.现病史否认主诉中症状，如主诉中记录"口干1年"，但是现病史中记录"无口干、多饮、多尿等症状"
6.现病史未记录主诉中症状特点及其发展变化情况，如主诉中提及以下常见症状（发热、水肿、咳嗽与咳痰、咯血、胸痛、呼吸困难、呕吐、吞咽困难、呕血、便血、腹痛、腹泻、便秘、黄疸、关节痛、血尿、尿频、尿痛、少尿、多尿、消瘦、头痛、眩晕、晕厥、抽搐、意识障碍），现病史中需对该症状进行描述（包括但不限于症状部位、性质、程度、加重及缓解因素等），如有现病史中没有描述，判定为缺陷病历

以下是一些示例，用<example></example>标记，请参考

<example>
主诉：口干1年
现病史：患者1年前无明显诱因出现口干症状，饮水后不能缓解，伴体重增加10kg，无口干、多饮、多尿等症状，未行相关检查。

有缺陷
主诉中记录"口干1年"，但是现病史中记录"无口干、多饮、多尿等症状"
</example>

<example>
主诉：右下肢水肿1周
现病史：1周前发现左侧下肢水肿，按压水肿部位回弹性差，伴尿量减少，未行相关诊治，今日为求进一步诊治，遂就诊于我院。

有缺陷
主诉中记录"右下肢"，但是现病史中记录"1周前发现左侧下肢水肿"
</example>

<example>
主诉：咳嗽、咳痰3天
现病史：痰不易咳出，自觉畏寒，未发热。口服强力枇杷

无缺陷
</example>

现在请对下面的主诉和现病史进行判断
主诉：{cc}
现病史：{hpi}"""
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
    qc_result = qc_chief_complaint_hpi_inconsistent(fields, llm)

    default_dir = Path("..") / "runs" / "med-emr-qc"
    out = Path(output_path) if output_path else (default_dir / f"{RULE_KEY}.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(qc_result, encoding="utf-8")

    print(f"✓ 质控结果已保存至：{out}")
    print("\n--- 质控结果 ---")
    print(qc_result)
    return qc_result
