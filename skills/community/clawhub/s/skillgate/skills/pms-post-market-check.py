#!/usr/bin/env python3
"""
pms-post-market-check — 上市后监督（PMS）检查。
检查上市后监督计划（Post-Market Surveillance）有没有覆盖关键要素。
"""
import re
import sys
from pathlib import Path


# PMS 关键要素
REQUIRED_ELEMENTS = {
    "PMS 计划（PMS Plan）": ["PMS plan", "post-market surveillance", "上市后监督", "PMS计划"],
    "投诉监测（Complaint Monitoring）": ["complaint", "投诉", "投诉监测"],
    "不良事件（Adverse Events）": ["adverse event", "不良事件", "不良事件报告"],
    "趋势报告（Trend Reporting）": ["trend", "趋势", "趋势报告"],
    "现场安全纠正措施（FSCA）": ["FSCA", "field safety", "现场安全", "纠正措施"],
    "定期安全更新报告（PSUR）": ["PSUR", "periodic safety", "定期安全", "定期风险评价"],
    "客户反馈（Customer Feedback）": ["customer feedback", "客户反馈", "用户反馈"],
    "文献监测（Literature Monitoring）": ["literature", "文献", "文献监测", "文献检索"],
}


def check_pms_plan(filepath: str) -> list:
    """检查上市后监督计划。"""
    content = Path(filepath).read_text(encoding="utf-8").lower()

    findings = []

    for element, keywords in REQUIRED_ELEMENTS.items():
        found = any(kw.lower() in content for kw in keywords)
        if not found:
            findings.append({
                "element": element,
                "severity": "MEDIUM",
                "message": f"缺少 {element}——PMS计划里没找到相关内容"
            })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python pms_post_market_check.py <PMS计划文件>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_pms_plan(filepath)

    if not findings:
        print("✅ PMS 计划覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")

    print(f"\n  覆盖率: {len(REQUIRED_ELEMENTS) - len(findings)}/{len(REQUIRED_ELEMENTS)}")

    sys.exit(1 if len(findings) > 3 else 0)


if __name__ == "__main__":
    main()
