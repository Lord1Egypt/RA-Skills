#!/usr/bin/env python3
"""
ai-medical-algorithm-check — 医疗 AI 算法验证检查。
检查 AI 医疗器械的算法验证报告有没有覆盖关键要素。
"""
import re
import sys
from pathlib import Path


# AI 医疗器械算法验证的关键要素
REQUIRED_ELEMENTS = {
    "算法性能指标（Performance Metrics）": ["accuracy", "sensitivity", "specificity", "AUC", "准确率", "敏感性", "特异性", "AUC"],
    "测试数据集（Test Dataset）": ["test dataset", "test set", "测试集", "测试数据"],
    "外部验证（External Validation）": ["external validation", "外部验证", "多中心", "独立验证"],
    "亚组分析（Subgroup Analysis）": ["subgroup", "亚组", "亚组分析", "不同人群"],
    "偏倚评估（Bias Assessment）": ["bias", "偏倚", "公平性", "fairness"],
    "鲁棒性测试（Robustness）": ["robustness", "鲁棒性", "稳定性", "泛化"],
    "可解释性（Explainability）": ["explainability", "interpretability", "可解释", "可解释性", "SHAP", "Grad-CAM"],
    "错误分析（Error Analysis）": ["error analysis", "错误分析", "失败案例"],
}


def check_ai_validation_report(filepath: str) -> list:
    """检查 AI 算法验证报告。"""
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
        print("用法: python ai_medical_algorithm_check.py <AI验证报告>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_ai_validation_report(filepath)

    if not findings:
        print("✅ AI 算法验证报告覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")

    print(f"\n  覆盖率: {len(REQUIRED_ELEMENTS) - len(findings)}/{len(REQUIRED_ELEMENTS)}")

    sys.exit(1 if len(findings) > 3 else 0)


if __name__ == "__main__":
    main()
