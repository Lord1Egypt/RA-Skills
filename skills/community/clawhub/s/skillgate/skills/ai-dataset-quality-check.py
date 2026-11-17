#!/usr/bin/env python3
"""
ai-dataset-quality-check — 医疗 AI 数据集质量检查。
检查 AI 训练数据集的质量有没有覆盖关键要素。
"""
import re
import sys
from pathlib import Path


# AI 数据集质量的关键要素
REQUIRED_ELEMENTS = {
    "数据集大小（Dataset Size）": ["dataset size", "样本量", "训练集大小", "n ="],
    "数据标注（Data Labeling）": ["annotation", "labeling", "标注", "标签"],
    "标注一致性（Label Consistency）": ["inter-annotator", "一致性", "kappa", "一致率"],
    "数据划分（Data Split）": ["train", "validation", "test", "训练集", "验证集", "测试集"],
    "数据增强（Data Augmentation）": ["augmentation", "数据增强", "增强"],
    "数据隐私（Data Privacy）": ["privacy", "隐私", "脱敏", "HIPAA", "GDPR"],
    "数据来源（Data Sources）": ["data sources", "数据来源", "多中心", "多站点"],
}


def check_dataset_report(filepath: str) -> list:
    """检查数据集质量报告。"""
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
        print("用法: python ai_dataset_quality_check.py <数据集报告>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_dataset_report(filepath)

    if not findings:
        print("✅ 数据集质量报告覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")

    print(f"\n  覆盖率: {len(REQUIRED_ELEMENTS) - len(findings)}/{len(REQUIRED_ELEMENTS)}")

    sys.exit(1 if len(findings) > 3 else 0)


if __name__ == "__main__":
    main()
