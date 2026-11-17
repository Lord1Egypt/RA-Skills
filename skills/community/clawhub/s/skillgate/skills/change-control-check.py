#!/usr/bin/env python3
"""
change-control-check — 变更控制检查。
检查变更控制程序（Change Control）有没有覆盖关键要素。
"""
import re
import sys
from pathlib import Path


# 变更控制关键要素
REQUIRED_ELEMENTS = {
    "变更申请（Change Request）": ["change request", "变更申请", "变更请求", "ECR"],
    "变更评估（Change Evaluation）": ["evaluation", "评估", "变更评估", "风险评估"],
    "变更审批（Change Approval）": ["approval", "审批", "变更审批", "批准"],
    "变更实施（Change Implementation）": ["implementation", "实施", "变更实施", "执行"],
    "变更验证（Change Verification）": ["verification", "验证", "变更验证"],
    "变更记录（Change Record）": ["record", "记录", "变更记录", "台账"],
    "受影响产品（Affected Products）": ["affected", "受影响", "受影响产品", "涉及产品"],
    "法规影响（Regulatory Impact）": ["regulatory", "法规", "法规影响", "注册变更"],
}


def check_change_control(filepath: str) -> list:
    """检查变更控制程序。"""
    content = Path(filepath).read_text(encoding="utf-8").lower()

    findings = []

    for element, keywords in REQUIRED_ELEMENTS.items():
        found = any(kw.lower() in content for kw in keywords)
        if not found:
            findings.append({
                "element": element,
                "severity": "MEDIUM",
                "message": f"缺少 {element}——变更控制程序里没找到相关内容"
            })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python change_control_check.py <变更控制文件>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_change_control(filepath)

    if not findings:
        print("✅ 变更控制程序覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")

    print(f"\n  覆盖率: {len(REQUIRED_ELEMENTS) - len(findings)}/{len(REQUIRED_ELEMENTS)}")

    sys.exit(1 if len(findings) > 3 else 0)


if __name__ == "__main__":
    main()
