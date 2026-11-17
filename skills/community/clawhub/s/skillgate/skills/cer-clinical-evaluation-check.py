#!/usr/bin/env python3
"""
cer-clinical-evaluation-check — CER 临床评价报告检查。
检查临床评价报告（Clinical Evaluation Report）有没有覆盖关键要素。
"""
import re
import sys
from pathlib import Path


# CER 关键要素
REQUIRED_ELEMENTS = {
    "临床评价计划（CEP）": ["clinical evaluation plan", "CEP", "临床评价计划"],
    "器械描述（Device Description）": ["device description", "器械描述", "产品描述"],
    "预期用途（Intended Purpose）": ["intended purpose", "intended use", "预期用途", "预期目的"],
    "等效性分析（Equivalence）": ["equivalence", "equivalent", "等效性", "同品种"],
    "文献检索（Literature Search）": ["literature search", "文献检索", "文献综述"],
    "临床数据（Clinical Data）": ["clinical data", "临床数据", "临床证据"],
    "利益风险分析（Benefit Risk）": ["benefit risk", "benefit-risk", "利益风险", "获益风险"],
    "结论（Conclusion）": ["conclusion", "结论", "总结论"],
}


def check_cer_report(filepath: str) -> list:
    """检查临床评价报告。"""
    content = Path(filepath).read_text(encoding="utf-8").lower()

    findings = []

    for element, keywords in REQUIRED_ELEMENTS.items():
        found = any(kw.lower() in content for kw in keywords)
        if not found:
            findings.append({
                "element": element,
                "severity": "MEDIUM",
                "message": f"缺少 {element}——报告里没找到相关内容"
            })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python cer_clinical_evaluation_check.py <CER报告>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_cer_report(filepath)

    if not findings:
        print("✅ CER 报告覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")

    print(f"\n  覆盖率: {len(REQUIRED_ELEMENTS) - len(findings)}/{len(REQUIRED_ELEMENTS)}")

    sys.exit(1 if len(findings) > 3 else 0)


if __name__ == "__main__":
    main()
