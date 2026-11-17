#!/usr/bin/env python3
"""
iec81001-cybersecurity-check — 网络安全文件检查。
基于 IEC 81001-5-1（医械网络安全）。
"""
from pathlib import Path


CHECKS = {
    "CRITICAL": [
        ("威胁建模", "threat modeling", "Threat Model", "缺少 威胁建模", "应该写：识别资产、识别威胁、分析风险"),
        ("安全架构", "security architecture", "Security Architecture", "缺少 安全架构", "应该写：网络分段、访问控制、加密"),
        ("漏洞管理", "vulnerability management", "Vulnerability", "缺少 漏洞管理", "应该写：漏洞发现、评估、修复的流程"),
        ("补丁管理", "patch management", "Patch", "缺少 补丁管理", "应该写：补丁更新流程、验证、部署"),
    ],
    "MEDIUM": [
        ("身份认证", "authentication", "Authentication", "缺少 身份认证", "应该写：用户认证方法、密码策略、多因素认证"),
        ("访问控制", "access control", "Access Control", "缺少 访问控制", "应该写：权限模型、最小权限原则"),
        ("数据加密", "data encryption", "Encryption", "缺少 数据加密", "应该写：传输加密、存储加密"),
        ("日志审计", "logging audit", "Logging", "缺少 日志审计", "应该写：日志记录内容、保留时间、审计方法"),
    ],
}


def check_medical_device_doc(filepath: str):
    doc_path = Path(filepath)
    if not doc_path.exists():
        print(f"文件不存在: {filepath}")
        return

    content = doc_path.read_text(encoding="utf-8", errors="replace")
    content_lower = content.lower()

    findings = []

    for severity, checks in CHECKS.items():
        for (zh, en, alt, missing_msg, suggestion) in checks:
            if zh in content or en in content_lower or alt.lower() in content_lower:
                continue

            findings.append({
                "severity": severity,
                "message": missing_msg,
                "suggestion": suggestion
            })

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        icon = "🔴" if f["severity"] == "CRITICAL" else "🟡"
        print(f"  {icon} [{f['severity']}] {f['message']}")
        print(f"    💡 建议: {f['suggestion']}")

    critical_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
    medium_count = sum(1 for f in findings if f["severity"] == "MEDIUM")

    print(f"\n  覆盖率: {len(CHECKS['CRITICAL']) + len(CHECKS['MEDIUM']) - len(findings)}/{len(CHECKS['CRITICAL']) + len(CHECKS['MEDIUM'])}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python iec81001-cybersecurity-check.py <文件路径>")
        sys.exit(1)

    print("=" * 60)
    print("(")
    print("  🔒 网络安全文件检查（IEC 81001）")
    print("=" * 60)
    print(f"\n  目标: {sys.argv[1]}\n")

    check_medical_device_doc(sys.argv[1])

    print("\n" + "=" * 60)
