#!/usr/bin/env python3
"""
iec62366-usability-check — IEC 62366 可用性工程文件检查。
检查可用性工程文件有没有覆盖 IEC 62366:2015 的关键元素。
"""
import re
import sys
from pathlib import Path


# IEC 62366:2015 关键元素（EN + ZH 关键词）+ 建议
REQUIRED_ELEMENTS = {
    "使用规范（Intended Use）": {
        "keywords": ["intended use", "intended purpose", "预期用途", "预期目的"],
        "suggestion": "应该写：这个器械是给谁用的、用来干什么的、在什么场景下用"
    },
    "用户特征（User Characteristics）": {
        "keywords": ["user characteristics", "user profile", "用户特征", "用户画像"],
        "suggestion": "应该写：目标用户的年龄、性别、教育程度、医疗背景、是否有特殊需求（如视力障碍）"
    },
    "使用环境（Use Environment）": {
        "keywords": ["use environment", "usage environment", "使用环境", "使用场景"],
        "suggestion": "应该写：在什么地方用（医院/家庭/救护车）、光线怎么样、噪音怎么样、有没有其他设备干扰"
    },
    "危险使用情况（Hazardous Use）": {
        "keywords": ["hazardous", "use error", "危险使用", "使用错误"],
        "suggestion": "应该写：用户可能会犯什么错误、这些错误会导致什么后果"
    },
    "使用规范文件（USE Specification）": {
        "keywords": ["use specification", "使用规范", "使用要求"],
        "suggestion": "应该写：用户要完成的任务、每一步要做什么、成功的标准是什么"
    },
    "形成性评价（Formative Evaluation）": {
        "keywords": ["formative evaluation", "形成性评价", "中期评价"],
        "suggestion": "应该写：设计过程中做的可用性测试——发现了什么问题、怎么改进的"
    },
    "总结性评价（Summative Evaluation）": {
        "keywords": ["summative evaluation", "总结性评价", "最终评价"],
        "suggestion": "应该写：最终的可用性测试——测试了多少用户、成功率多少、有没有残留问题"
    },
    "用户接口（User Interface）": {
        "keywords": ["user interface", "UI", "用户界面", "用户接口"],
        "suggestion": "应该写：屏幕显示、按钮布局、声音提示、报警方式等"
    },
    "可用性工程文件（UE File）": {
        "keywords": ["usability engineering file", "UE file", "可用性工程文件"],
        "suggestion": "应该写：整个可用性工程过程的文档——计划、设计、测试、结果"
    },
}


def check_usability_file(filepath: str) -> list:
    """检查可用性工程文件。"""
    content = Path(filepath).read_text(encoding="utf-8").lower()

    findings = []

    for element, info in REQUIRED_ELEMENTS.items():
        found = any(kw.lower() in content for kw in info["keywords"])
        if not found:
            findings.append({
                "element": element,
                "severity": "MEDIUM",
                "message": f"缺少 {element}",
                "suggestion": info["suggestion"]
            })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python iec62366_usability_check.py <可用性工程文件>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_usability_file(filepath)

    if not findings:
        print("✅ 可用性工程文件覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")
        print(f"    💡 建议: {f['suggestion']}")

    print(f"\n  覆盖率: {len(REQUIRED_ELEMENTS) - len(findings)}/{len(REQUIRED_ELEMENTS)}")

    sys.exit(1 if len(findings) > 3 else 0)


if __name__ == "__main__":
    main()
