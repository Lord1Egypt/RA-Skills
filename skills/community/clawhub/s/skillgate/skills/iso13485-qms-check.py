#!/usr/bin/env python3
"""
iso13485-qms-check — ISO 13485 质量管理体系检查。
检查质量管理体系文件有没有覆盖 ISO 13485:2016 的关键章节。
"""
import re
import sys
from pathlib import Path


# ISO 13485:2016 关键章节 + 建议
REQUIRED_CLAUSES = {
    "4 质量管理体系（QMS）": {
        "keywords": ["4 质量管理体系", "quality management system", "QMS"],
        "suggestion": "应该写：QMS 文件结构、程序文件清单、质量手册"
    },
    "5 管理职责（Management Responsibility）": {
        "keywords": ["5 管理职责", "management responsibility"],
        "suggestion": "应该写：管理承诺、质量方针、质量目标、管理评审"
    },
    "6 资源管理（Resource Management）": {
        "keywords": ["6 资源管理", "resource management"],
        "suggestion": "应该写：人员配置、培训、基础设施、工作环境"
    },
    "7 产品实现（Product Realization）": {
        "keywords": ["7 产品实现", "product realization"],
        "suggestion": "应该写：产品实现的策划、设计开发、采购、生产"
    },
    "8 测量分析和改进（Measurement Analysis Improvement）": {
        "keywords": ["8 测量分析", "measurement analysis", "持续改进"],
        "suggestion": "应该写：监视测量、不合格品控制、纠正预防、持续改进"
    },
    "文件控制（Document Control）": {
        "keywords": ["document control", "文件控制", "文件管理"],
        "suggestion": "应该写：文件怎么审批、怎么发布、怎么更改、怎么作废"
    },
    "记录控制（Record Control）": {
        "keywords": ["record control", "记录控制", "记录管理"],
        "suggestion": "应该写：记录怎么保存、保存多久、怎么检索、怎么保护"
    },
    "设计开发（Design Development）": {
        "keywords": ["design and development", "设计开发", "设计控制"],
        "suggestion": "应该写：设计输入、设计输出、设计评审、设计验证、设计确认、设计转换"
    },
    "采购（Purchasing）": {
        "keywords": ["purchasing", "采购", "供应商"],
        "suggestion": "应该写：供应商评价、采购信息、采购产品验证"
    },
    "生产服务（Production Service）": {
        "keywords": ["production", "生产", "服务提供"],
        "suggestion": "应该写：生产过程控制、设备确认、灭菌、无菌屏障"
    },
    "监视测量（Monitoring Measurement）": {
        "keywords": ["monitoring", "监视", "测量"],
        "suggestion": "应该写：监视测量装置的控制、内部审核"
    },
    "不合格品控制（Nonconforming Product）": {
        "keywords": ["nonconforming", "不合格", "不合格品"],
        "suggestion": "应该写：不合格品怎么识别、怎么隔离、怎么处置"
    },
    "纠正预防（Corrective Preventive）": {
        "keywords": ["corrective", "preventive", "纠正", "预防", "CAPA"],
        "suggestion": "应该写：纠正措施、预防措施、CAPA 流程"
    },
}


def check_qms_file(filepath: str) -> list:
    """检查质量管理体系文件。"""
    content = Path(filepath).read_text(encoding="utf-8").lower()

    findings = []

    for clause, info in REQUIRED_CLAUSES.items():
        found = any(kw.lower() in content for kw in info["keywords"])
        if not found:
            findings.append({
                "clause": clause,
                "severity": "MEDIUM",
                "message": f"缺少 {clause}",
                "suggestion": info["suggestion"]
            })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python iso13485_qms_check.py <质量管理体系文件>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_qms_file(filepath)

    if not findings:
        print("✅ 质量管理体系文件覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")
        print(f"    💡 建议: {f['suggestion']}")

    print(f"\n  覆盖率: {len(REQUIRED_CLAUSES) - len(findings)}/{len(REQUIRED_CLAUSES)}")

    sys.exit(1 if len(findings) > 6 else 0)


if __name__ == "__main__":
    main()
