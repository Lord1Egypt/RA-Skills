#!/usr/bin/env python3
"""
spatiotemporal_auditor.py · 时空智能分析法一致性审计器

功能：检查报告中每个事实是否可溯源、推测是否标注、时间戳是否最新。

用法:
  python spatiotemporal_auditor.py --report path/to/report.md
  python spatiotemporal_auditor.py --report report.md --json output.json
"""

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path


# ---------- 审计规则 ----------

def audit_source_traceability(report: str) -> dict:
    """每个事实是否标注了 source_url？"""
    # 检测"事实陈述 + 来源"模式
    fact_pattern = re.compile(r'([^\n。]{10,100}(?:是|为|达|达到|有|发布|推出|获得|完成)[^\n。]+)')
    sources = re.findall(r'https?://[^\s\)]+', report)

    facts = fact_pattern.findall(report)
    return {
        "facts_found": len(facts),
        "sources_found": len(sources),
        "ratio": round(len(sources) / max(len(facts), 1), 2),
        "verdict": "pass" if len(sources) / max(len(facts), 1) > 0.3 else "warn",
    }


def audit_temporal_anchors(report: str) -> dict:
    """时间戳/年份锚点是否充分？"""
    year_pattern = re.compile(r'(19|20)\d{2}')
    years = year_pattern.findall(report)
    unique_years = set([f"19{y}" if y == "19" else f"20{y}" for y in years])

    date_pattern = re.compile(r'(19|20)\d{2}[-年./](\d{1,2})[-月./]?(\d{1,2})?')
    full_dates = date_pattern.findall(report)

    return {
        "years_mentioned": len(unique_years),
        "full_dates_mentioned": len(full_dates),
        "verdict": "pass" if len(unique_years) >= 3 else "warn",
    }


def audit_speculation_labels(report: str) -> dict:
    """推测是否明确标注？"""
    speculation_markers = [
        "我推测", "可能", "也许", "大概", "推测", "猜想",
        "speculated", "probably", "likely", "may be", "perhaps",
    ]
    speculation_count = sum(report.count(m) for m in speculation_markers)

    # 反向：报告应该标注 confidence
    confidence_markers = ["confidence", "置信度", "高置信", "中置信", "低置信", "high", "medium", "low"]
    confidence_count = sum(report.count(m) for m in confidence_markers)

    return {
        "speculation_markers": speculation_count,
        "confidence_markers": confidence_count,
        "verdict": "pass" if confidence_count >= 3 or speculation_count <= 5 else "warn",
    }


def audit_narrative_arc(report: str) -> dict:
    """是否有故事弧线（不是流水账）？"""
    arc_keywords = {
        "起源": ["起源", "诞生", "成立于", "诞生于", "创立"],
        "转折": ["转折", "但是", "然而", "突然", "改变", "决策", "选择"],
        "沉淀": ["今天", "当前", "现在", "未来", "展望", "趋势"],
    }
    has_arc = {phase: any(kw in report for kw in keywords) for phase, keywords in arc_keywords.items()}
    return {
        "origin": has_arc["起源"],
        "turning_point": has_arc["转折"],
        "current_state": has_arc["沉淀"],
        "verdict": "pass" if all(has_arc.values()) else "warn",
    }


def audit_no_filler(report: str) -> dict:
    """检查是否含咨询公司套话"""
    filler = [
        "赋能", "抓手", "打造闭环", "价值重构",
        "底层逻辑", "顶层设计", "深度赋能",
    ]
    found = [f for f in filler if f in report]
    return {
        "filler_found": found,
        "verdict": "fail" if len(found) >= 3 else ("warn" if found else "pass"),
    }


# ---------- 主流程 ----------

def audit_report(report_path: str) -> dict:
    p = Path(report_path)
    if not p.exists():
        return {"error": f"文件不存在: {report_path}"}

    report = p.read_text(encoding="utf-8")

    result = {
        "report": str(p.absolute()),
        "audited_at": datetime.now().isoformat(),
        "report_length": len(report),
        "audits": {
            "source_traceability": audit_source_traceability(report),
            "temporal_anchors": audit_temporal_anchors(report),
            "speculation_labels": audit_speculation_labels(report),
            "narrative_arc": audit_narrative_arc(report),
            "no_filler": audit_no_filler(report),
        },
    }

    # 综合评分
    verdicts = [v["verdict"] for v in result["audits"].values()]
    if "fail" in verdicts:
        result["overall"] = "fail"
    elif verdicts.count("warn") > 2:
        result["overall"] = "warn"
    else:
        result["overall"] = "pass"

    return result


# ---------- CLI ----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="时空智能分析法报告审计器")
    parser.add_argument("--report", required=True, help="报告 Markdown 文件路径")
    parser.add_argument("--json", help="输出 JSON 结果路径")
    args = parser.parse_args()

    result = audit_report(args.report)

    if args.json:
        Path(args.json).write_text(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"✅ 审计结果已写入: {args.json}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


# ---------- 评分说明 ----------

"""
评分标准：
- overall: pass / warn / fail
- 单项: pass / warn / fail

修复建议：
- pass: 无需修改
- warn: 建议补充（如多 1-2 个证据来源）
- fail: 必须修改（如删除咨询公司套话）

通过标准：overall 至少要 warn，且 source_traceability 和
narrative_arc 不能 fail。
"""
