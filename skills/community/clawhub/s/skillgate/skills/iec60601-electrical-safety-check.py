#!/usr/bin/env python3
"""
iec60601-electrical-safety-check — 电气安全文件检查。
基于 GB 9706.1 / IEC 60601-1。
"""
from pathlib import Path


CHECKS = {
    "CRITICAL": [
        ("电气安全设计", "electrical safety design", "Electrical Safety", "缺少 电气安全设计", "应该写：绝缘设计、漏电流限制、接地保护"),
        ("漏电流测试", "leakage current test", "Leakage Current", "缺少 漏电流测试", "应该写：漏电流测试方法、限值、结果"),
        ("接地阻抗", "grounding impedance", "Grounding", "缺少 接地阻抗", "应该写：接地阻抗测试方法、限值、结果"),
        ("介电强度", "dielectric strength", "Dielectric Strength", "缺少 介电强度", "应该写：耐压测试方法、电压、结果"),
    ],
    "MEDIUM": [
        ("医用电气设备分类", "medical electrical equipment classification", "Classification", "缺少 医用电气设备分类", "应该写：按 IEC 60601-1 的分类（I类/II类、BF型/CF型）"),
        ("温升测试", "temperature rise test", "Temperature Rise", "缺少 温升测试", "应该写：温升测试方法、限值、结果"),
        ("机械强度", "mechanical strength", "Mechanical Strength", "缺少 机械强度", "应该写：机械强度测试方法、结果"),
        ("外壳防护", "enclosure protection", "Enclosure", "缺少 外壳防护", "应该写：外壳防护等级（IP 代码）"),
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
        print("用法: python iec60601-electrical-safety-check.py <文件路径>")
        sys.exit(1)

    print("=" * 60)
    print("  ⚡ 电气安全文件检查（GB 9706.1 / IEC 60601-1）")
    print("=" * 60)
    print(f"\n  目标: {sys.argv[1]}\n")

    check_medical_device_doc(sys.argv[1])

    print("\n" + "=" * 60)
