#!/usr/bin/env python3
"""
skill-security-scanner CLI entry point
"""

import sys
import argparse
from pathlib import Path

# Add skill source to path
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "source"))

from scanner import SecurityScanner
from reporter import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description="🔒 Skill Security Scanner - 自动扫描技能代码安全风险",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s skill_path="./skills/batch-renamer"
  %(prog)s skill_path="./skills/social-publisher" output_format=html
  %(prog)s skill_path="./skills/your-skill" virustotal_api_key="${VT_API_KEY}" output_format=both
        """
    )

    parser.add_argument("skill_path", help="技能目录路径")
    parser.add_argument("--output-format", "-o", choices=["json", "html", "both"], default="json",
                       help="输出格式 (默认: json)")
    parser.add_argument("--virustotal-api-key", help="VirusTotal API key (可选)")
    parser.add_argument("--severity-threshold", choices=["low", "medium", "high", "critical"],
                       default="low", help="最低严重程度报告 (默认: low)")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    args = parser.parse_args()

    # Run scan
    scanner = SecurityScanner(
        skill_path=args.skill_path,
        virustotal_api_key=args.virustotal_api_key,
        severity_threshold=args.severity_threshold,
        verbose=args.verbose
    )

    results = scanner.scan()

    # Generate report
    reporter = ReportGenerator(results, output_format=args.output_format)
    output = reporter.generate()

    if args.output_format == "json":
        print(output)
    else:
        # Write HTML to file
        output_file = Path(args.skill_path) / "security_report.html"
        output_file.write_text(output)
        print(f"✅ HTML report generated: {output_file}")

    # Exit with non-zero if high/critical issues found
    if results["risk_level"] in ["high", "critical"]:
        sys.exit(1)

if __name__ == "__main__":
    main()