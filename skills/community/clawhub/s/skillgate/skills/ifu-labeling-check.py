#!/usr/bin/env python3
"""
ifu-labeling-check — 标签和说明书（IFU）检查。
检查使用说明书（Instructions for Use）有没有覆盖关键要素。
"""
import re
import sys
from pathlib import Path


# IFU 关键要素 + 建议怎么写
REQUIRED_ELEMENTS = {
    "产品名称（Product Name）": {
        "keywords": ["product name", "产品名称", "商品名"],
        "suggestion": "应该写：产品的正式名称 + 商品名（如：一次性使用注射器 / 安尔康）"
    },
    "型号规格（Model / Catalog）": {
        "keywords": ["model", "catalog", "型号", "规格", "REF"],
        "suggestion": "应该写：型号编号 + 规格（如：REF 12345，规格：5ml）"
    },
    "预期用途（Intended Use）": {
        "keywords": ["intended use", "intended purpose", "预期用途", "预期目的"],
        "suggestion": "应该写：这个器械是用来干什么的，给谁用，在什么场景下用"
    },
    "适应症（Indications）": {
        "keywords": ["indication", "适应症", "适用范围"],
        "suggestion": "应该写：这个器械适用于哪些疾病、哪些症状、哪些人群"
    },
    "禁忌症（Contraindications）": {
        "keywords": ["contraindication", "禁忌症", "禁忌"],
        "suggestion": "应该写：哪些人不能用，什么情况下不能用"
    },
    "警告（Warnings）": {
        "keywords": ["warning", "警告", "WARNING"],
        "suggestion": "应该写：可能导致严重伤害或死亡的情况（DANGER/WARNING 级别）"
    },
    "注意事项（Precautions）": {
        "keywords": ["precaution", "注意", "注意事项", "CAUTION"],
        "suggestion": "应该写：可能导致轻微伤害或设备损坏的情况（CAUTION 级别）"
    },
    "使用方法（Directions for Use）": {
        "keywords": ["directions for use", "使用方法", "操作说明", "如何使用"],
        "suggestion": "应该写：一步一步的操作步骤，从准备到使用到结束"
    },
    "储存条件（Storage）": {
        "keywords": ["storage", "储存", "保存", "存储条件"],
        "context_keywords": ["温度", "湿度", "避光", "防潮", "temperature", "humidity"],
        "suggestion": "应该写：温度范围、湿度要求、避光、防潮等"
    },
    "生产日期 / 有效期（Expiry Date）": {
        "keywords": ["expiry", "expiration", "有效期", "生产日期", "use by"],
        "suggestion": "应该写：生产日期 + 有效期至（如：2026-10，有效期至 2029-10）"
    },
    "生产企业（Manufacturer）": {
        "keywords": ["manufacturer", "生产企业", "生产商", "制造商"],
        "suggestion": "应该写：生产企业名称 + 地址 + 联系方式"
    },
    "CE 标志 / FDA 标志（Certification）": {
        "keywords": ["CE mark", "FDA", "认证", "注册证号"],
        "suggestion": "应该写：CE 标志 + 公告体编号，或 FDA 510(k) 编号，或 NMPA 注册证号"
    },
}


def check_ifu(filepath: str) -> list:
    """检查使用说明书。"""
    content = Path(filepath).read_text(encoding="utf-8").lower()

    findings = []

    for element, info in REQUIRED_ELEMENTS.items():
        # 先检查有没有主关键词
        has_keyword = any(kw.lower() in content for kw in info["keywords"])

        if not has_keyword:
            findings.append({
                "element": element,
                "severity": "MEDIUM",
                "message": f"缺少 {element}",
                "suggestion": info["suggestion"]
            })
            continue

        # 如果有上下文关键词要求，再检查上下文
        if "context_keywords" in info:
            has_context = any(kw.lower() in content for kw in info["context_keywords"])
            if not has_context:
                findings.append({
                    "element": element,
                    "severity": "MEDIUM",
                    "message": f"{element} 只有关键词，没有上下文（可能是误报）",
                    "suggestion": info["suggestion"]
                })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python ifu_labeling_check.py <说明书文件>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_ifu(filepath)

    if not findings:
        print("✅ 说明书覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")
        print(f"    💡 建议: {f['suggestion']}")

    print(f"\n  覆盖率: {len(REQUIRED_ELEMENTS) - len(findings)}/{len(REQUIRED_ELEMENTS)}")

    sys.exit(1 if len(findings) > 4 else 0)


if __name__ == "__main__":
    main()
