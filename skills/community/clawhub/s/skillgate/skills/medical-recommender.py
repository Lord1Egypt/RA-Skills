#!/usr/bin/env python3
"""
medical-recommender — 医疗 AI 推荐。
用户输入医械分类，自动推荐要跑哪些检查。
"""
import sys


# 按分类推荐
RECOMMENDATIONS = {
    "1": {
        "name": "第 1 类（低风险）",
        "skills": [
            ("iso13485-qms-check", "质量管理体系检查"),
            ("ifu-labeling-check", "标签说明书检查"),
            ("pms-post-market-check", "上市后监督检查"),
        ],
        "reason": "低风险器械，只需要做最基本的合规检查"
    },
    "2": {
        "name": "第 2 类（中风险）",
        "skills": [
            ("iso13485-qms-check", "质量管理体系检查"),
            ("ifu-labeling-check", "标签说明书检查"),
            ("pms-post-market-check", "上市后监督检查"),
            ("iec62366-usability-check", "可用性工程检查"),
            ("iso14971-risk-matrix", "风险管理检查"),
        ],
        "reason": "中风险器械，需要做基本合规 + 风险管理 + 可用性"
    },
    "3": {
        "name": "第 3 类（高风险）",
        "skills": [
            ("iso13485-qms-check", "质量管理体系检查"),
            ("ifu-labeling-check", "标签说明书检查"),
            ("pms-post-market-check", "上市后监督检查"),
            ("iec62366-usability-check", "可用性工程检查"),
            ("iec62304-sdlc-check", "软件生命周期检查"),
            ("iso10993-biocompatibility-check", "生物相容性检查"),
            ("cer-clinical-evaluation-check", "临床评价检查"),
            ("iso14971-risk-matrix", "风险管理检查"),
        ],
        "reason": "高风险器械，需要做全部检查"
    },
    "ai": {
        "name": "医疗 AI（SaMD）",
        "skills": [
            ("iso13485-qms-check", "质量管理体系检查"),
            ("iec62304-sdlc-check", "软件生命周期检查"),
            ("ai-medical-algorithm-check", "AI 算法验证检查"),
            ("ai-dataset-quality-check", "AI 数据集质量检查"),
            ("cer-clinical-evaluation-check", "临床评价检查"),
        ],
        "reason": "AI 医械需要做软件生命周期 + AI 专用检查"
    },
}


def recommend(device_class: str):
    """根据医械分类推荐要跑的检查。"""
    if device_class not in RECOMMENDATIONS:
        print("分类只能是 1、2、3、ai")
        sys.exit(1)

    rec = RECOMMENDATIONS[device_class]

    print("=" * 60)
    print("(")
    print("  🤖 AI 推荐——你应该跑这些检查")
    print("=" * 60)
    print(f"\n  医疗器械分类: {rec['name']}")
    print(f"  推荐理由: {rec['reason']}")
    print(f"\n  推荐跑的检查（{len(rec['skills'])} 个）：")

    for i, (skill_name, desc) in enumerate(rec["skills"], 1):
        print(f"    {i}. {skill_name}")
        print(f"       {desc}")

    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("用法: python medical_recommender.py <分类>")
        print("  分类: 1 = 第 1 类（低风险）")
        print("        2 = 第 2 类（中风险）")
        print("        3 = 第 3 类（高风险）")
        print("        ai = 医疗 AI（SaMD）")
        sys.exit(1)

    device_class = sys.argv[1]
    recommend(device_class)


if __name__ == "__main__":
    main()
