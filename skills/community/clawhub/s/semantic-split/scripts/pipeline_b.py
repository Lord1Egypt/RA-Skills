#!/usr/bin/env python3
"""
semantic-split Pipeline B — 结构分析管线 v0.1.2

正则层（5W2H/主语/约束/分块），零外部依赖。

覆盖步骤：
  Step 2:   语义拆分(主语映射→分块→话题转移)
  Step 2.5b: 隐式约束升级(领域分类)
  Step 2.5c: 注意力锚定(CORE/ENTITY/RESISTANCE)
  Step 3:   5W2H 七维度提取
  Step 5:   WP分解(依赖分析+耗时估算)

用法:
  from pipeline_b import analyze_structure
  result = analyze_structure("请帮我用公司模板制作PPT")
"""

import os
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "semantic-split" / "data"
MODELS_DIR = DATA_DIR / "models"


# ============================================================
# 常量定义
# ============================================================

# 主语映射表
SUBJECT_MAP = {
    "我": "用户", "咱们": "用户", "俺": "用户",
    "你": "执行者", "您": "执行者",
    "他": "第三方", "她": "第三方", "它": "第三方",
}

# 约束关键词
CRITICAL_KW = re.compile(r'(必须|只能|截止|指定|强制|不允许|不得|禁止|一定)')
SOFT_KW = re.compile(r'(最好|尽量|如果|建议|通常|希望|可以|不妨)')
EXAMPLE_KW = re.compile(r'(比如|例如|像|假如|譬如)')
RESISTANCE_KW = re.compile(r'(但是|不过|担心|怕|难|卡|然而|但)')
CORE_VERB_KW = re.compile(r'(制作|安排|写|规划|分析|设计|开发|创建|修改|删除|导出|导入|查询|搜索)')
PURPOSE_KW = re.compile(r'(为了|目的是|目标是|旨在|想要|想)')
HOW_KW = re.compile(r'(用|通过|按照|根据|借助|利用|采用)')

# 时间词正则
DATE_KW = re.compile(
    r'(今天|明天|昨天|后天|前天|'
    r'下周|这周|上周|下个月|这个月|上个月|'
    r'周[一二三四五六日]|星期[一二三四五六日]|'
    r'\d{4}[-年]\d{1,2}[-月]\d{1,2}[日号]?|'
    r'\d{1,2}月\d{1,2}[日号]|'
    r'\d+[天小时分秒])'
)

# 数量词正则
AMOUNT_KW = re.compile(r'\d+\.?\d*(个|份|人|元|小时|天|次|张|页|条|项)')

# 隐式约束领域升级表
IMPLICIT_UPGRADE_DOMAINS = {
    "组织规范": re.compile(r'(公司模板|品牌|审批|规范|章程|制度|标准|模板|格式|命名)'),
    "法律合规": re.compile(r'(合同|数据保护|审计|合规|法律|条款|协议|版权|隐私)'),
    "安全底线": re.compile(r'(权限|加密|安全|密码|认证|防火墙|隔离)'),
    "协作依赖": re.compile(r'(接口|API|交付|依赖|对接|上下游|联调)'),
    "个人偏好": re.compile(r'(颜色|字体|风格|布局|喜欢|偏好)'),
}

# WP 耗时估算表（按动词类型）
ESTIMATE_MAP = {
    "搜索": 0.5, "查询": 0.5, "收集": 1.0, "整理": 1.0,
    "设计": 2.0, "制作": 2.0, "创建": 0.5, "编辑": 1.0,
    "写": 1.5, "撰写": 1.5, "修改": 0.5, "删除": 0.25,
    "审核": 0.5, "检查": 0.5, "验证": 0.5, "测试": 1.0,
    "导出": 0.25, "导入": 0.25, "提交": 0.25, "发布": 0.5,
    "分析": 2.0, "规划": 1.5, "讨论": 1.0, "确认": 0.5,
}

# ============================================================
# 正则层
# ============================================================

_EMPTY = {"subjects": [], "blocks": [], "constraints": [],
          "attention": {}, "five_w2h": {}, "coverage": 0.0}


def _regex_subjects(text: str) -> dict:
    """正则层：主语识别"""
    subjects = []
    for kw, mapping in SUBJECT_MAP.items():
        if kw in text:
            subjects.append({"keyword": kw, "role": mapping, "method": "regex"})
    # 去重保序
    seen = set()
    unique = []
    for s in subjects:
        key = s["role"]
        if key not in seen:
            seen.add(key)
            unique.append(s)
    return {"subjects": unique, "coverage": min(len(unique) / 3, 1.0) if unique else 0.0}


def _regex_blocks(text: str) -> dict:
    """正则层：分句 + 块划分"""
    sents = re.split(r'[。！？\n]+', text)
    sents = [s.strip() for s in sents if s.strip()]
    blocks = []
    for sid, sent in enumerate(sents):
        subj = None
        for kw, role in SUBJECT_MAP.items():
            if kw in sent:
                subj = role
                break
        if not subj and CORE_VERB_KW.search(sent):
            subj = "用户"
        blocks.append({
            "id": f"b{sid}",
            "text": sent,
            "subject": subj or "用户",
            "method": "regex",
        })
    return {"blocks": blocks, "coverage": len(blocks) / max(len(sents), 1)}


def _regex_constraints(text: str, blocks: list) -> dict:
    """正则层：约束关键词初判 + 注意力锚定"""
    constraints = []
    attention = {"critical": [], "core": [], "entity": [], "example": [], "resistance": []}

    for blk in blocks:
        t = blk["text"]

        # 硬约束
        if CRITICAL_KW.search(t):
            constraints.append({
                "block_id": blk["id"],
                "level": "critical", "keyword": CRITICAL_KW.search(t).group(0),
                "domain": "", "method": "regex",
            })
            attention["critical"].append(t[:60])

        # 软约束
        elif SOFT_KW.search(t):
            constraints.append({
                "block_id": blk["id"],
                "level": "soft", "keyword": SOFT_KW.search(t).group(0),
                "domain": "", "method": "regex",
            })

        # 注意力锚定
        for m in CORE_VERB_KW.finditer(t):
            attention["core"].append({"block": blk["id"], "verb": m.group(0), "context": t[:50]})
        for m in re.finditer(r'\d+[天小时分元个份%]', t):
            attention["entity"].append({"block": blk["id"], "value": m.group(0)})
        for m in EXAMPLE_KW.finditer(t):
            attention["example"].append({"block": blk["id"], "context": t[m.start():m.start()+30]})
        for m in RESISTANCE_KW.finditer(t):
            attention["resistance"].append({"block": blk["id"], "context": t[m.start():m.start()+30]})

    coverage = min(len(constraints) / max(len(blocks), 1), 1.0) if blocks else 0.0
    return {"constraints": constraints, "attention": attention, "coverage": coverage}


def _regex_5w2h(text: str) -> dict:
    """正则层：5W2H 初步提取"""
    result = {}
    matched = 0

    # Why
    m = PURPOSE_KW.search(text)
    result["why"] = {"value": m.group(0) if m else "", "source": "regex"} if m else {}
    if m: matched += 1

    # What（CORE_VERB_KW）
    verbs = CORE_VERB_KW.findall(text)
    result["what"] = {"value": verbs[0] if verbs else "", "all_verbs": verbs, "source": "regex"}

    # Who
    for kw, role in SUBJECT_MAP.items():
        if kw in text:
            result["who"] = {"value": role, "source": "regex"}
            matched += 1
            break

    # When
    dates = DATE_KW.findall(text)
    if dates:
        result["when"] = {"value": dates[0], "all": dates, "source": "regex"}
        matched += 1

    # Where（简单地点匹配）
    where_m = re.search(r'在\s*(.{2,10}?)(?:里|上|中|处|方)', text)
    if where_m:
        result["where"] = {"value": where_m.group(1).strip(), "source": "regex"}
        matched += 1

    # How
    how_m = HOW_KW.search(text)
    if how_m:
        # 提取工具/方式
        tool_m = re.search(r'(用|通过|按照|根据|借助|利用)\s*(.{1,15}?)(?:制作|写|做|分析|创建|开发|设计)', text)
        if tool_m:
            result["how"] = {"value": tool_m.group(2).strip(), "source": "regex"}
        else:
            result["how"] = {"value": how_m.group(0), "source": "regex"}
        matched += 1

    # How much
    amt = AMOUNT_KW.findall(text)
    if amt:
        result["how_much"] = {"value": amt[0], "all": amt, "source": "regex"}
        matched += 1

    result["_matched"] = matched
    result["_coverage"] = matched / 7.0
    return result


def _regex_detect_implicit_upgrade(constraints: list) -> list:
    """正则层：隐式约束领域检测"""
    for c in constraints:
        if c.get("level") != "soft":
            continue
        for domain, pattern in IMPLICIT_UPGRADE_DOMAINS.items():
            if pattern.search(c.get("keyword", "")):
                c["domain"] = domain
                c["upgraded"] = domain in ("组织规范", "法律合规", "安全底线")
                break
    return constraints


# ============================================================
# 各环节主函数（纯正则）
# ============================================================

def extract_subjects(text: str) -> dict:
    """正则层：主语识别"""
    result = _regex_subjects(text)
    return result


def extract_blocks(text: str) -> dict:
    """正则层：分块"""
    result = _regex_blocks(text)
    return result


def extract_constraints_and_attention(text: str) -> dict:
    """正则层：约束标注 + 注意力锚定"""
    blocks_result = _regex_blocks(text)
    result = _regex_constraints(text, blocks_result["blocks"])
    result["constraints"] = _regex_detect_implicit_upgrade(result["constraints"])
    return result


def extract_5w2h(text: str) -> dict:
    """正则层：5W2H 七维度提取"""
    result = _regex_5w2h(text)
    return result
    for dim in ["why", "what", "who", "when", "where", "how", "how_much"]:
        if dim in result and result[dim].get("value"):
            matched = max(matched, sum(1 for d in ["why", "what", "who", "when", "where", "how", "how_much"]
                          if d in result and result[d].get("value")))
    result["_coverage"] = matched / 7.0

    return result


def extract_attention_anchoring(text: str) -> dict:
    """Step 2.5c: 注意力锚定"""
    blocks_result = _regex_blocks(text)
    const_result = _regex_constraints(text, blocks_result["blocks"])
    return const_result["attention"]


def wps_decompose(steps: list) -> list:
    """Step 5: 工作包分解"""
    wps = []
    for step in steps:
        action = step.get("action", "")
        # 按顿号/逗号拆分子任务
        parts = re.split(r'[，、,]', action)
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            # 估算耗时
            hours = 1.0
            for verb, est in ESTIMATE_MAP.items():
                if verb in part:
                    hours = est
                    break
            wps.append({
                "id": f"WP{len(wps)+1}",
                "name": part,
                "action": part,
                "estimated_hours": hours,
                "depends_on": step.get("depends_on", []) if i == 0 else [f"WP{len(wps)}"],
                "milestone": step.get("milestone", False) and i == 0,
            })
    return wps


# ============================================================
# 统一入口
# ============================================================

def analyze_structure(text: str) -> dict:
    """
    Pipeline B 统一入口。
    返回结构化分析结果，包含 subjects/blocks/constraints/attention/5w2h/wp。
    """
    if not text or not text.strip():
        return {"error": "empty input", "text": ""}

    result = {
        "text": text,
        "subjects": extract_subjects(text),
        "blocks": extract_blocks(text),
        "constraints_attention": extract_constraints_and_attention(text),
        "five_w2h": extract_5w2h(text),
        "attention": extract_attention_anchoring(text),
    }

    # 管线使用统计
    layers_used = ["regex"]
    result["pipeline_layers"] = layers_used

    return result


if __name__ == "__main__":
    import json
    test = "请帮我用公司模板制作一份关于钛合金马扎的演示 PPT，下周之前要交给客户"
    result = analyze_structure(test)
    print(json.dumps(result, ensure_ascii=False, indent=2))
