#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


FILLERS = ["那个", "就是", "然后", "呃", "嗯", "啊"]
HEDGES = ["可能", "也许", "大概", "我觉得", "其实", "有点", "是不是", "应该"]
APOLOGIES = ["不好意思", "抱歉", "对不起"]
WEAK_ENDINGS = ["再说", "看情况", "差不多", "先这样"]
ASK_MARKERS = ["我建议", "我希望", "我需要", "我的请求", "请你支持", "我想推进"]
EVIDENCE_MARKERS = ["数据", "指标", "结果", "同比", "环比", "提升", "下降"]


def count_matches(text: str, keywords: list[str]) -> int:
    return sum(text.count(keyword) for keyword in keywords)


def classify_tone(text: str) -> list[str]:
    labels = []
    if count_matches(text, APOLOGIES) >= 1 or count_matches(text, HEDGES) >= 3:
        labels.append("偏示弱")
    if "不是我的问题" in text or "别人没给" in text:
        labels.append("偏防御")
    if any(marker in text for marker in ASK_MARKERS):
        labels.append("有明确推进")
    if re.search(r"\d", text) or any(marker in text for marker in EVIDENCE_MARKERS):
        labels.append("有证据感")
    if not labels:
        labels.append("中性")
    return labels


def analyze_text(text: str) -> dict:
    findings = []
    filler_count = count_matches(text, FILLERS)
    hedge_count = count_matches(text, HEDGES)
    apology_count = count_matches(text, APOLOGIES)
    ask_present = any(marker in text for marker in ASK_MARKERS)
    evidence_present = bool(re.search(r"\d", text)) or any(marker in text for marker in EVIDENCE_MARKERS)
    weak_ending = any(text.endswith(marker) for marker in WEAK_ENDINGS)

    if filler_count >= 4:
        findings.append("口头填充词偏多，正式场景里会削弱稳感。")
    if hedge_count >= 3:
        findings.append("模糊表达偏多，容易让对方觉得你不够确定。")
    if apology_count >= 1:
        findings.append("道歉表达出现，除非确实需要，否则会削弱立场。")
    if not ask_present:
        findings.append("没有明确请求或推进动作，谈完后容易停在空中。")
    if not evidence_present:
        findings.append("几乎没有证据或数据支撑，可信度不够。")
    if weak_ending:
        findings.append("结尾偏虚，缺少有力收口。")

    score = 100
    score -= filler_count * 3
    score -= hedge_count * 4
    score -= apology_count * 8
    if not ask_present:
        score -= 12
    if not evidence_present:
        score -= 10
    if weak_ending:
        score -= 8
    score = max(score, 0)

    return {
        "score": score,
        "tone_labels": classify_tone(text),
        "counts": {
            "fillers": filler_count,
            "hedges": hedge_count,
            "apologies": apology_count,
        },
        "findings": findings,
        "recommended_fix": [
            "先讲结论，再讲证据，最后明确请求。",
            "减少『可能 / 我觉得 / 其实』这类缓冲词。",
            "结尾用一句明确下一步收口。",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a rehearsal transcript for tone and communication risks.")
    parser.add_argument("--transcript-file", required=True)
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    text = Path(args.transcript_file).read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("Transcript is empty.")
    result = analyze_text(text)

    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
