#!/usr/bin/env python3
"""
SkillGuard CLI — Agent Skill Security Scanner
Usage: python cli.py scan <skill.zip> [--format json|md] [--severity min] [--detector name]
"""

import sys, os, argparse
# Add parent directory for 'skillguard' package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skillguard.orchestrator import Orchestrator
from skillguard.pipeline import DetectorRegistry
from skillguard.detectors import *  # Auto-register all detectors


def main():
    parser = argparse.ArgumentParser(
        prog="skillguard",
        description="🔒 SkillGuard — Agent技能安全扫描器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  skillguard scan my-skill.zip                    # 默认JSON+Markdown
  skillguard scan my-skill.zip --format md        # 仅Markdown报告
  skillguard scan my-skill.zip --detector secret_exposure  # 仅检查凭据泄露
  skillguard list                                 # 列出所有检测器
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # scan command
    scan_parser = subparsers.add_parser("scan", help="扫描Skill包")
    scan_parser.add_argument("path", help="Skill ZIP文件路径")
    scan_parser.add_argument("--format", choices=["json", "md", "both"], default="both", 
                             help="报告输出格式 (默认: both)")
    scan_parser.add_argument("--severity", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                             help="最低严重级别过滤")
    scan_parser.add_argument("--detector", action="append", dest="detectors",
                             help="指定检测器（可多次使用）")
    scan_parser.add_argument("--output", "-o", help="输出文件路径（不含扩展名）")

    # list command
    list_parser = subparsers.add_parser("list", help="列出所有可用检测器")

    args = parser.parse_args()

    if args.command == "list":
        print("可用检测器:")
        for d in DetectorRegistry.all():
            print(f"  {d.name:25s} — {d.description}")
        return

    if args.command == "scan":
        if not os.path.exists(args.path):
            print(f"❌ 文件不存在: {args.path}", file=sys.stderr)
            sys.exit(1)

        print(f"🔒 SkillGuard v1.0.0 — 扫描中...")
        print(f"   目标: {args.path}")
        if args.detectors:
            print(f"   检测器: {', '.join(args.detectors)}")

        orchestrator = Orchestrator()
        result = orchestrator.scan(args.path, args.detectors, args.format)

        # Severity filter
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "": 9}
        output = ""

        if "json" in result:
            import json
            data = json.loads(result["json"])
            if args.severity:
                min_sev = severity_order[args.severity]
                data["findings"] = [f for f in data["findings"] 
                                    if severity_order.get(f["severity"], 9) <= min_sev]
                data["summary"] = {
                    "total_findings": len(data["findings"]),
                    "filtered": True,
                    "min_severity": args.severity,
                }
            result["json"] = json.dumps(data, ensure_ascii=False, indent=2)
            if args.format != "md":
                output += result["json"]

        if "md" in result:
            if args.format == "json":
                pass
            else:
                output += result["md"]

        # Output
        if args.output:
            ext = {"json": ".json", "md": ".md", "both": ""}
            if args.format == "both":
                with open(args.output + ".json", "w") as f:
                    f.write(result.get("json", ""))
                with open(args.output + ".md", "w") as f:
                    f.write(result.get("md", ""))
                print(f"✅ 报告已保存: {args.output}.json, {args.output}.md")
            else:
                path = args.output + ext.get(args.format, ".txt")
                with open(path, "w") as f:
                    f.write(output)
                print(f"✅ 报告已保存: {path}")
        else:
            print(output)

        # Summary line
        import json
        data = json.loads(result.get("json", "{}"))
        trace = data.get("trace_score", {})
        print(f"\n📊 TRACE评分: {trace.get('overall', '?')}/5 ({trace.get('level', '?')})")
        stats = trace.get("stats", {})
        print(f"   发现: 🔴{stats.get('critical',0)} 🟠{stats.get('high',0)} 🟡{stats.get('medium',0)} 🔵{stats.get('low',0)}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
