#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
grade.py — 自我评估 / rubric 评分器（元认知闭环核心）。

让 agent 对自己的输出做结构化、可复现的评分，而非凭感觉"我觉得不错"。
纯启发式 + 可选参考答案重叠，无需外部 API 即可离线运行。

用法:
  python grade.py --task "写一封英文道歉邮件" --output answer.md --out report.json
  python grade.py --task "..." --output "直接文本..." --auto-rubric
  python grade.py --task "..." --output mine.md --reference gold.md --rubric rubric.json --out report.json

rubric.json 结构:
  {"criteria":[{"name":..., "weight":0.2, "keywords":[...], "min_len":80}]}
  未提供 --rubric 时，使用内置默认 5 维 rubric（权重均分）。
"""
import os, sys, json, argparse, re


DEFAULT_RUBRIC = {
    "criteria": [
        {"name": "相关性", "weight": 0.2, "keywords": [], "min_len": 40},
        {"name": "完整性", "weight": 0.2, "keywords": [], "min_len": 60},
        {"name": "结构清晰度", "weight": 0.2, "keywords": ["1.", "2.", "-", "##", "###", "\n"], "min_len": 60},
        {"name": "准确性", "weight": 0.2, "keywords": [], "min_len": 40},
        {"name": "可执行性", "weight": 0.2, "keywords": ["步骤", "运行", "命令", "```"], "min_len": 40},
    ]
}


def read_text(path):
    if os.path.isfile(path):
        return open(path, encoding="utf-8").read()
    return path  # 当直接传入文本


def tokenize(text):
    """中文按字、英文/数字按词，做重叠比对用。"""
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    words = re.findall(r"[a-zA-Z0-9_]+", text.lower())
    return set(cjk) | set(words)


def keyword_coverage(text, keywords):
    if not keywords:
        return None  # 无关键词约束 -> 不参与此信号
    hit = sum(1 for k in keywords if k in text)
    return hit / len(keywords)


def length_factor(text, min_len):
    n = len(text.strip())
    if min_len <= 0:
        return 1.0
    return min(1.0, n / min_len)


def overlap(a, b):
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb:
        return None
    inter = ta & tb
    union = ta | tb
    return len(inter) / len(union) if union else 0.0


def score_criterion(c, text, reference=None):
    name = c.get("name", "?")
    weight = float(c.get("weight", 0.2))
    min_len = int(c.get("min_len", 0))

    kcov = keyword_coverage(text, c.get("keywords", []))
    lf = length_factor(text, min_len)
    ov = overlap(text, reference) if reference else None

    # 综合：关键词覆盖(0.5) + 长度(0.2) + 参考答案重叠(0.3, 若有)
    parts = []
    if kcov is not None:
        parts.append(("关键词", kcov, 0.5))
    parts.append(("长度", lf, 0.2))
    if ov is not None:
        parts.append(("重叠", ov, 0.3))

    wsum = sum(w for _, _, w in parts) or 1.0
    score = sum(s * w for _, s, w in parts) / wsum

    evidence = []
    if kcov is not None:
        evidence.append(f"关键词命中 {round(kcov*100)}%")
    evidence.append(f"长度系数 {round(lf,2)}")
    if ov is not None:
        evidence.append(f"与参考答案重叠 {round(ov,3)}")

    if score >= 0.75:
        verdict = "pass"
    elif score >= 0.5:
        verdict = "partial"
    else:
        verdict = "fail"
    return {
        "criterion": name,
        "score": round(score, 3),
        "weight": weight,
        "evidence": "; ".join(evidence),
        "verdict": verdict,
    }


def main():
    ap = argparse.ArgumentParser(description="自我评估 / rubric 评分器")
    ap.add_argument("--task", required=True)
    ap.add_argument("--output", required=True, help="输出文本或文件路径")
    ap.add_argument("--reference", help="参考答案文本或文件路径（可选，提升准确性评分）")
    ap.add_argument("--rubric", help="rubric JSON 文件")
    ap.add_argument("--out", help="报告输出 JSON 路径")
    ap.add_argument("--auto-rubric", action="store_true", help="忽略 rubric 文件，用默认 5 维")
    args = ap.parse_args()

    text = read_text(args.output)
    ref = read_text(args.reference) if args.reference else None

    if args.auto_rubric or not args.rubric:
        rubric = DEFAULT_RUBRIC
    else:
        rubric = json.loads(open(args.rubric, encoding="utf-8").read())

    per = [score_criterion(c, text, ref) for c in rubric["criteria"]]
    wsum = sum(p["weight"] for p in per) or 1.0
    overall = sum(p["score"] * p["weight"] for p in per) / wsum

    strengths = [p["criterion"] for p in per if p["verdict"] == "pass"]
    weaknesses = [p["criterion"] for p in per if p["verdict"] in ("partial", "fail")]
    suggestions = []
    for p in per:
        if p["verdict"] == "fail":
            suggestions.append(f"「{p['criterion']}」严重不达标（{p['score']}）：{p['evidence']} —— 需重点补强")
        elif p["verdict"] == "partial":
            suggestions.append(f"「{p['criterion']}」部分达标（{p['score']}）：可优化 {p['evidence']}")

    report = {
        "task": args.task,
        "overall": round(overall, 3),
        "verdict": "pass" if overall >= 0.75 else ("partial" if overall >= 0.5 else "fail"),
        "per_criterion": per,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }
    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
        print(f"✅ 评分完成 overall={report['overall']} verdict={report['verdict']} -> {args.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
