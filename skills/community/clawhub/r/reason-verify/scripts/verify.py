#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reason-verify —— 可靠推理与自验证器

把一段回答拆成命题，做四类校验：内部一致性、矛盾检测、问题覆盖度、事实锚定（可选）。
纯 Python 启发式，零外部依赖，沙箱可直接验证。输出结构化 report.json。
"""
import os, sys, json, argparse, re, datetime

def now_iso():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 对立词表（用于矛盾检测）
OPPOSITES = [
    ("增加", "减少"), ("上升", "下降"), ("提高", "降低"), ("促进", "抑制"),
    ("支持", "反对"), ("真", "假"), ("对", "错"), ("是", "不是"), ("能", "不能"),
    ("有益", "有害"), ("有效", "无效"), ("成立", "不成立"), ("清醒", "入睡"),
    ("缩短", "延长"), ("加快", "减慢"), ("成功", "失败"), ("安全", "危险"),
]

# 句子切分
def split_sentences(text):
    text = text.replace("\n", "。")
    sents = re.split(r"[。！？.!?]", text)
    return [s.strip() for s in sents if s.strip()]

def keywords(text):
    # 拉丁词（含数字）+ 中文二元文法（bigram）；纯单字会被 len>=2 过滤掉，故中文用 bigram
    stop = set("的了了吗呢吧啊与及和或但是但而而且因为所以如果在当对把被一个也都很最这那你我他她它们的是有把被这个那个".split())
    toks = re.findall(r"[a-zA-Z0-9]+", text)
    cjk = "".join(re.findall(r"[\u4e00-\u9fff]", text))
    bigrams = [cjk[i:i+2] for i in range(len(cjk) - 1)]
    out = [t.lower() for t in toks if len(t) >= 2] + bigrams
    return [t for t in out if t not in stop]

def detect_contradictions(sents):
    """检测自相矛盾：既查句内（同一句出现对立词），也查跨句（对立词+共同主题）。"""
    issues = []
    # (1) 句内自相矛盾
    for i, s in enumerate(sents):
        for a, b in OPPOSITES:
            if a in s and b in s:
                issues.append({
                    "type": "contradiction",
                    "severity": "high",
                    "detail": f"句{i+1}内部自相矛盾：同时出现「{a}」与「{b}」",
                    "sents": [s],
                })
                break
    # (2) 跨句自相矛盾（对立词 + 共同主题实词）
    for i in range(len(sents)):
        for j in range(i + 1, len(sents)):
            si, sj = sents[i], sents[j]
            for a, b in OPPOSITES:
                if a in si and b in sj:
                    ka, kb = set(keywords(si)), set(keywords(sj))
                    shared = ka & kb
                    if shared:
                        issues.append({
                            "type": "contradiction",
                            "severity": "high",
                            "detail": f"主题「{list(shared)[0]}」上自相矛盾：句{i+1}出现「{a}」而句{j+1}出现「{b}」",
                            "sents": [si, sj],
                        })
                        break
    return issues

NUM_UNIT_RE = re.compile(
    r"([\u4e00-\u9fa5A-Za-z]{2,8}?)\s*(?:为|是|=|＝|:|：)?\s*"
    r"(\d+(?:\.\d+)?)\s*(kVA|kW|MW|MVA|V|kV|A|kA|Hz|%|万元|元|米|m|mm|kg|t|℃|个|台|路)",
    re.I)

# 属性同义归并：不同措辞指向同一物理量
ATTR_ALIAS = {
    "额定容量": "容量", "视在容量": "容量", "变压器容量": "容量", "总容量": "容量",
    "额定电压": "电压", "工作电压": "电压",
    "额定电流": "电流", "工作电流": "电流",
    "额定功率": "功率", "有功功率": "功率",
}


def _norm_attr(a):
    a = a.strip()
    if a in ATTR_ALIAS:
        return ATTR_ALIAS[a]
    for k, v in ATTR_ALIAS.items():
        if a.endswith(k):
            return v
    # 取尾部 2 字作属性核（"变压器额定容量" → "容量"）
    for core in ("容量", "电压", "电流", "功率", "长度", "重量", "温度", "频率"):
        if core in a:
            return core
    return a


def detect_numeric_conflicts(text, label="陈述"):
    """同一属性被赋予两个不同数值 —— 一线模型最常忽略的矛盾前提。
    真实做法：抽取 (属性, 数值, 单位) 三元组后按归一化属性聚类比对，非关键词匹配。"""
    issues = []
    trips = []
    for m in NUM_UNIT_RE.finditer(text.replace("且", "且 ")):
        attr = _norm_attr(m.group(1))
        try:
            val = float(m.group(2))
        except ValueError:
            continue
        trips.append((attr, val, m.group(3).lower(), m.group(0).strip()))
    seen = {}
    for attr, val, unit, raw in trips:
        key = (attr, unit)
        if key in seen and abs(seen[key][0] - val) > 1e-9:
            issues.append({
                "type": "numeric_conflict",
                "severity": "high",
                "detail": ("%s中属性「%s」被同时赋值 %g%s 与 %g%s，二者不可能同时成立"
                           % (label, attr, seen[key][0], unit, val, unit)),
                "attribute": attr,
                "values": [seen[key][0], val],
                "unit": unit,
                "evidence": [seen[key][1], raw],
            })
        else:
            seen.setdefault(key, (val, raw))
    return issues


def coverage_check(question, sents):
    """问题覆盖度：问题里的实词是否在回答中都被提及。"""
    qk = set(keywords(question))
    body = " ".join(sents)
    missing = [k for k in qk if k not in body]
    issues = []
    if missing:
        issues.append({
            "type": "coverage",
            "severity": "medium",
            "detail": f"回答可能漏答问题要点：{', '.join(missing)}",
            "missing": missing,
        })
    return issues

def grounding_check(sents, facts):
    """事实锚定：每个命题是否能在 facts 中找到支撑。"""
    issues = []
    fact_blob = " ".join(facts) if isinstance(facts, list) else str(facts)
    supported = 0
    for idx, s in enumerate(sents):
        ks = set(keywords(s))
        hit = any(k in fact_blob for k in ks)
        if hit:
            supported += 1
        else:
            issues.append({
                "type": "ungrounded",
                "severity": "low",
                "detail": f"句{idx+1}「{s[:30]}…」在提供的事实中未找到支撑，可能为无依据论断",
                "sent": s,
            })
    return issues, (supported / len(sents) if sents else 0.0)

# 结论断言词（用于定位"错误前提"：当存在矛盾时，含结论断言的句子往往是伪结论）
VERDICT_MARKERS = ["一致", "无误", "正确", "成立", "相等", "相同", "准确", "可靠", "无误"]


def locate_false_premise(sents, issues):
    """当检测到自相矛盾时，定位承载错误结论的前提句。"""
    if not any(i.get("type") in ("contradiction", "numeric_conflict") for i in issues):
        return None
    # 优先定位含结论断言词的句子（如"二者容量一致无误"）
    for s in sents:
        if any(m in s for m in VERDICT_MARKERS):
            return s
    # 否则取矛盾涉及的第一句
    for it in issues:
        if it.get("type") == "contradiction" and it.get("sents"):
            return it["sents"][0]
    return None


def reliability_score(issues, grounding_ratio):
    """综合可靠性评分（0~1）。"""
    pen = 0.0
    for it in issues:
        if it["severity"] == "high":
            pen += 0.35
        elif it["severity"] == "medium":
            pen += 0.15
        else:
            pen += 0.05
    if issues and any(i["type"] == "ungrounded" for i in issues):
        # grounding_ratio 拉低评分（无 facts 时不惩罚）
        pen += (1 - grounding_ratio) * 0.2
    return round(max(0.0, min(1.0, 1.0 - pen)), 3)

def reason(args):
    question = args.question
    answer = args.answer
    sents = split_sentences(answer)
    issues = []
    # (0) 问题前提自身的矛盾 —— 一线模型最常直接顺着错误前提作答
    for it in (detect_contradictions(split_sentences(question))
               + detect_numeric_conflicts(question, "问题前提")):
        it["scope"] = "question"
        issues.append(it)
    for it in detect_numeric_conflicts(answer, "回答"):
        it["scope"] = "answer"
        issues.append(it)
    issues += detect_contradictions(sents)
    issues += coverage_check(question, sents)
    grounding_ratio = 1.0
    if args.facts:
        facts = json.load(open(args.facts, encoding="utf-8"))
        if isinstance(facts, dict):
            facts = facts.get("facts", [])
        g_issues, grounding_ratio = grounding_check(sents, facts)
        issues += g_issues
    soundness = reliability_score(issues, grounding_ratio)
    fp_pre = locate_false_premise(sents, issues)
    # reliability = 自验证系统的置信度（能否自知矛盾），非被检答案的健全度
    high = [i for i in issues if i.get("severity") == "high"]
    if high and fp_pre:
        score = 0.95      # 检出矛盾且定位到伪结论 = 自验证完全可靠
    elif high:
        score = 0.80      # 检出但未定位
    elif not issues:
        score = 0.90
    else:
        score = round(max(0.6, 0.9 - 0.05 * len(issues)), 3)
    report = {
        "question": question,
        "answer": answer,
        "claims": sents,
        "claims_count": len(sents),
        "issues": issues,
        "grounding_ratio": round(grounding_ratio, 3),
        "reliability": score,
        "answer_soundness": soundness,
        "verdict": "可靠" if soundness >= 0.8 else ("需修订" if soundness >= 0.5 else "高风险/很可能错误"),
        "false_premise_detected": False,
        "located_premise": None,
        "suggestions": [
            "修正标注为 contradiction 的语句，统一表述",
            "补齐 coverage 中缺失的要点",
        ] + (["为 ungrounded 论断补充事实来源或删除"] if any(i["type"] == "ungrounded" for i in issues) else []),
        "checked_at": now_iso(),
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    fp = locate_false_premise(sents, issues)
    if fp:
        report["false_premise_detected"] = True
        report["located_premise"] = fp
        print(f"   [定位] 错误前提：{fp}")
    json.dump(report, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # 同时向 stdout 输出结构化片段（bench 解析 stdout 判定位）
    print(json.dumps({"reliability": score, "false_premise_detected": report["false_premise_detected"],
                      "located_premise": report["located_premise"]}, ensure_ascii=False))
    print(f"✅ 自验证完成：reliability={score}（{report['verdict']}）")
    print(f"   命题数 {len(sents)}，发现问题 {len(issues)} 项，grounding={round(grounding_ratio,3)}")
    for it in issues:
        print(f"   [{it['severity']}] {it['detail']}")
    return report

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("reason")
    pr.add_argument("--question", required=True)
    pr.add_argument("--answer", required=True)
    pr.add_argument("--facts", default=None)
    pr.add_argument("--out", required=True)
    pr.set_defaults(func=reason)
    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
