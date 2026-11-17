#!/usr/bin/env python3
"""
medical-device-chain — 医械法规技能链。
一键跑完所有医械法规检查，形成完整的审查工作流。
"""
import subprocess
import sys
from pathlib import Path


# 技能链的顺序（按医械法规文档审查的真实工作流）
CHAIN_STEPS = [
    {
        "name": "1. 可用性工程检查",
        "script": "iec62366-usability-check.py",
        "description": "检查可用性工程文件覆盖度",
    },
    {
        "name": "2. 软件生命周期检查",
        "script": "iec62304-sdlc-check.py",
        "description": "检查软件生命周期文件覆盖度",
    },
    {
        "name": "3. 生物相容性检查",
        "script": "iso10993-biocompatibility-check.py",
        "description": "检查生物相容性报告覆盖度",
    },
    {
        "name": "4. 临床评价检查",
        "script": "cer-clinical-evaluation-check.py",
        "description": "检查 CER 报告覆盖度",
    },
    {
        "name": "5. 质量管理体系检查",
        "script": "iso13485-qms-check.py",
        "description": "检查 QMS 文件覆盖度",
    },
    {
        "name": "6. 电气安全检查",
        "script": "iec60601-electrical-safety-check.py",
        "description": "检查电气安全文件覆盖度（GB 9706.1）",
    },
    {
        "name": "7. 网络安全检查",
        "script": "iec81001-cybersecurity-check.py",
        "description": "检查网络安全文件覆盖度（IEC 81001）",
    },
]


# 按医疗器械分类调整检查严格程度
# 第 1 类（低风险）：只做最基本的
# 第 2 类（中风险）：做中等程度
# 第 3 类（高风险）：做全部
CLASS_RULES = {
    "1": {
        "name": "第 1 类（低风险）",
        "steps": ["质量管理体系检查"],  # 只做最基本的
    },
    "2": {
        "name": "第 2 类（中风险）",
        "steps": ["可用性工程检查", "质量管理体系检查"],  # 中等程度
    },
    "3": {
        "name": "第 3 类（高风险）",
        "steps": ["可用性工程检查", "软件生命周期检查", "生物相容性检查", "临床评价检查", "质量管理体系检查", "电气安全检查", "网络安全检查"],  # 全部
    },
}


def run_chain(filepath: str, device_class: str = "3") -> dict:
    """跑完整的医械法规技能链。"""
    print("=" * 70)
    print("(")
    print("  🔗 医械法规技能链——一键跑完所有检查")
    print("=" * 70)
    print(f"\n  目标文件: {filepath}")
    print(f"  医疗器械分类: {CLASS_RULES[device_class]['name']}")
    print(f"  要跑的步骤: {len(CLASS_RULES[device_class]['steps'])} 步")
    print()

    # 按分类筛选要跑的步骤
    steps_to_run = [s for s in CHAIN_STEPS if s["name"].split(". ")[1] in CLASS_RULES[device_class]["steps"]]

    results = []
    passed = 0
    failed = 0

    for step in steps_to_run:
        print(f"  {step['name']}...", end=" ")

        # 检查脚本在不在
        script_path = Path(__file__).parent / step["script"]
        if not script_path.exists():
            print(f"⚠️ 脚本不存在——跳过")
            results.append({
                "step": step["name"],
                "status": "SKIPPED",
                "reason": "脚本不存在"
            })
            continue

        # 跑这个脚本
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), filepath],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                print(f"✅ 通过")
                results.append({
                    "step": step["name"],
                    "status": "PASSED",
                    "output": result.stdout
                })
                passed += 1
            else:
                print(f"⚠️ 有问题（{result.returncode}）")
                results.append({
                    "step": step["name"],
                    "status": "FAILED",
                    "output": result.stdout  # 保存完整输出
                })
                failed += 1

        except Exception as e:
            print(f"❌ 出错: {e}")
            results.append({
                "step": step["name"],
                "status": "ERROR",
                "error": str(e)
            })
            failed += 1

    # 总结
    print("\n" + "=" * 70)
    print("  📊 技能链总结")
    print("=" * 70)
    print(f"\n  医疗器械分类: {CLASS_RULES[device_class]['name']}")
    print(f"  总共 {len(steps_to_run)} 步：")
    print(f"    ✅ 通过: {passed} 步")
    print(f"    ⚠️ 有问题: {failed} 步")

    if failed == 0:
        print(f"\n  🎉 全部通过！文档审查完成")
    else:
        print(f"\n  ⚠️ 有 {failed} 步有问题——下面是汇总建议：")
        print("\n" + "-" * 70)
        print("  📋 汇总改进建议（按优先级）：")
        print("-" * 70)

        # 汇总所有建议
        for r in results:
            if r["status"] == "FAILED":
                print(f"\n  📌 {r['step']}:")
                # 提取建议行（💡 开头的）
                for line in r["output"].split("\n"):
                    if "💡" in line:
                        print(f"     {line.strip()}")

    print("\n" + "=" * 70)

    # 生成 HTML 报告（仅写输入文档所在目录——用户明确提供文件的目录，绝不写引擎/外部目录）
    report_path = Path(filepath).resolve().parent / "scan-report.html"
    if report_path.is_symlink() or report_path.is_junction():
        print("错误: 报告输出路径不能是符号链接/junction", file=sys.stderr)
        sys.exit(2)
    _generate_html_report(filepath, device_class, results, passed, failed, report_path)
    print(f"\n  📄 HTML 报告已生成: {report_path.name}")

    return {
        "device_class": device_class,
        "total": len(steps_to_run),
        "passed": passed,
        "failed": failed,
        "results": results,
        "report_path": str(report_path)
    }


def _generate_html_report(filepath: str, device_class: str, results: list, passed: int, failed: int, report_path: Path):
    """生成 HTML 检查报告。"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>医械法规检查报告</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #58a6ff; }}
        .summary {{ background: #161b22; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .passed {{ color: #3fb950; }}
        .failed {{ color: #f85149; }}
        .step {{ background: #161b22; border-radius: 8px; padding: 16px; margin: 12px 0; }}
        .suggestion {{ color: #8b949e; font-size: 14px; margin-top: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 医械法规检查报告</h1>
        <div class="summary">
            <p>📄 目标文件: {filepath}</p>
            <p>🏷️ 分类: {CLASS_RULES[device_class]['name']}</p>
            <p>✅ 通过: {passed} 步</p>
            <p>⚠️ 有问题: {failed} 步</p>
        </div>
"""

    for r in results:
        icon = "✅" if r["status"] == "PASSED" else "⚠️"
        html += f"""
        <div class="step">
            <h3>{icon} {r['step']}</h3>
"""
        if r["status"] == "FAILED" and "output" in r:
            for line in r["output"].split("\n"):
                if "💡" in line:
                    html += f'            <p class="suggestion">{line.strip()}</p>\n'

        html += "        </div>\n"

    html += """
    </div>
</body>
</html>
"""

    report_path.write_text(html, encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("用法: python medical_device_chain.py <医械文档> [分类]")
        print("  分类: 1 = 第 1 类（低风险）")
        print("        2 = 第 2 类（中风险）")
        print("        3 = 第 3 类（高风险，默认）")
        sys.exit(1)

    filepath = sys.argv[1]
    device_class = sys.argv[2] if len(sys.argv) > 2 else "3"

    if device_class not in CLASS_RULES:
        print("分类只能是 1、2、3")
        sys.exit(1)

    run_chain(filepath, device_class)


if __name__ == "__main__":
    main()
