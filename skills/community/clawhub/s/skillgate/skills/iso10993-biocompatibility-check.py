#!/usr/bin/env python3
"""
iso10993-biocompatibility-check — ISO 10993 生物相容性检查。
检查生物相容性评价报告有没有覆盖 ISO 10993 系列标准的关键测试项目。
"""
import re
import sys
from pathlib import Path


# ISO 10993 关键测试项目 + 建议
REQUIRED_TESTS = {
    "细胞毒性（Cytotoxicity）": {
        "keywords": ["cytotoxicity", "细胞毒性", "ISO 10993-5"],
        "suggestion": "应该写：测试方法、测试结果、合格标准"
    },
    "致敏（Sensitization）": {
        "keywords": ["sensitization", "致敏", "ISO 10993-10"],
        "suggestion": "应该写：测试方法（如 maximization test）、结果、结论"
    },
    "刺激（Irritation）": {
        "keywords": ["irritation", "刺激", "ISO 10993-23"],
        "suggestion": "应该写：皮肤刺激 / 眼刺激 / 粘膜刺激的测试结果"
    },
    "全身毒性（Systemic Toxicity）": {
        "keywords": ["systemic toxicity", "全身毒性", "急性全身毒性"],
        "suggestion": "应该写：急性全身毒性测试、亚慢性毒性测试"
    },
    "遗传毒性（Genotoxicity）": {
        "keywords": ["genotoxicity", "遗传毒性", "致突变"],
        "suggestion": "应该写：三个标准试验（ Ames、染色体畸变、小鼠淋巴瘤）"
    },
    "植入（Implantation）": {
        "keywords": ["implantation", "植入", "ISO 10993-6"],
        "suggestion": "应该写：植入部位、植入时间、组织病理学结果"
    },
    "血液相互作用（Hemocompatibility）": {
        "keywords": ["hemocompatibility", "血液", "ISO 10993-4"],
        "suggestion": "应该写：凝血、溶血、血小板、补体激活的测试结果"
    },
    "材料表征（Chemical Characterization）": {
        "keywords": ["chemical characterization", "材料表征", "ISO 10993-18"],
        "suggestion": "应该写：材料化学成分、可浸提物、挥发性物质"
    },
    "毒理动力学（Toxicokinetics）": {
        "keywords": ["toxicokinetics", "毒理动力学", "ISO 10993-17"],
        "suggestion": "应该写：化学物质的暴露量、每日允许摄入量（ADI）"
    },
}


def check_biocompatibility_report(filepath: str) -> list:
    """检查生物相容性评价报告。"""
    content = Path(filepath).read_text(encoding="utf-8").lower()

    findings = []

    for test, info in REQUIRED_TESTS.items():
        found = any(kw.lower() in content for kw in info["keywords"])
        if not found:
            findings.append({
                "test": test,
                "severity": "MEDIUM",
                "message": f"缺少 {test}",
                "suggestion": info["suggestion"]
            })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python iso10993_biocompatibility_check.py <生物相容性报告>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_biocompatibility_report(filepath)

    if not findings:
        print("✅ 生物相容性报告覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")
        print(f"    💡 建议: {f['suggestion']}")

    print(f"\n  覆盖率: {len(REQUIRED_TESTS) - len(findings)}/{len(REQUIRED_TESTS)}")

    sys.exit(1 if len(findings) > 4 else 0)


if __name__ == "__main__":
    main()
