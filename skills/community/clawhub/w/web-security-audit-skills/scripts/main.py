"""
Marvis Web Security Audit Skill — 主入口
用法:
    python main.py <源码目录> [--lang php|java|python|go] [--output report.md]

示例:
    python main.py /path/to/php-project --lang php --output Security.md
    python main.py /path/to/mixed-project --output Security.md
"""
from __future__ import annotations
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import audit_directory, findings_summary
from security_md import generate_security_md


def main():
    parser = argparse.ArgumentParser(
        description="Web Security Audit — PHP / Java / Python / Go",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py ./my-php-app --lang php
  python main.py ./my-go-project --lang go --output Security.md
  python main.py ./mixed-project
        """,
    )
    parser.add_argument("target", help="源码目录路径")
    parser.add_argument("--lang", choices=["php", "java", "python", "go"],
                        default=None, help="指定语言（不指定则自动检测）")
    parser.add_argument("--output", default=None, help="Security.md 输出路径")
    parser.add_argument("--json", action="store_true", help="额外输出 JSON 摘要")

    args = parser.parse_args()
    target_dir = os.path.abspath(args.target)

    if not os.path.isdir(target_dir):
        print(f"[!] 目标目录不存在: {target_dir}")
        sys.exit(1)

    print(f"[*] 开始扫描: {target_dir}")
    if args.lang:
        print(f"[*] 语言模式: {args.lang}")
    else:
        print(f"[*] 自动检测语言")

    results = audit_directory(target_dir, language=args.lang)

    summary = findings_summary(results)
    print(f"\n{'='*60}")
    print(f"扫描完成")
    print(f"{'='*60}")
    print(f"  扫描文件数 : {summary['total_files_scanned']}")
    print(f"  发现漏洞数 : {summary['total_findings']}")
    for sev in ["Critical", "High", "Medium", "Low"]:
        count = summary["severity_counts"].get(sev, 0)
        if count:
            print(f"    {sev:10s}: {count}")
    print(f"{'='*60}\n")

    # 生成 Security.md
    project_name = os.path.basename(target_dir) or "Project"
    output_path = args.output
    if not output_path:
        output_path = os.path.join(os.getcwd(), "Security.md")

    md_content = generate_security_md(results, project_name, output_path)
    print(f"[+] Security.md 已生成: {os.path.abspath(output_path)}")

    # JSON 摘要
    if args.json:
        import json
        json_path = output_path.replace(".md", ".json")
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump({
                "summary": summary,
                "findings_count": summary["total_findings"],
                "output_md": os.path.abspath(output_path),
            }, fh, indent=2, ensure_ascii=False)
        print(f"[+] JSON 摘要: {json_path}")


if __name__ == "__main__":
    main()
