#!/usr/bin/env python3
"""
ClawGuard Scanner
Scan ClawHub skills for security risks before installing.

Usage:
    python scan.py --skill <skill-name>        # Download and scan from ClawHub
    python scan.py --path <local-path>         # Scan local skill directory
    python scan.py --skill <skill-name> --json # Output JSON
"""

import sys
import argparse
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from analyzer import CodeAnalyzer
from reporter import Reporter
from downloader import SkillDownloader

def main():
    parser = argparse.ArgumentParser(
        description="ClawGuard: Scan ClawHub skills for security risks"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--skill",
        help="Skill name to download and scan from ClawHub"
    )
    group.add_argument(
        "--path",
        help="Local path to skill directory"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    args = parser.parse_args()
    
    # Determine skill path
    skill_path = None
    skill_name = ""
    cleanup_after = False
    
    if args.skill:
        skill_name = args.skill
        print(f"📥 Downloading skill: {skill_name}")
        skill_path = SkillDownloader.download_skill(skill_name)
        cleanup_after = True
        
        if not skill_path:
            print("❌ Failed to download skill")
            sys.exit(1)
    
    elif args.path:
        skill_path = Path(args.path)
        skill_name = skill_path.name
        
        if not skill_path.exists():
            print(f"❌ Path not found: {skill_path}")
            sys.exit(1)
        
        if not skill_path.is_dir():
            print(f"❌ Path is not a directory: {skill_path}")
            sys.exit(1)
    
    # Analyze skill
    print(f"🔍 Analyzing: {skill_name}")
    print()
    
    analyzer = CodeAnalyzer(skill_path)
    result = analyzer.analyze()
    
    # Generate report
    if args.json:
        report = Reporter.generate_json_report(result, skill_name)
    else:
        report = Reporter.generate_text_report(result, skill_name)
    
    print(report)
    
    # Cleanup if downloaded
    if cleanup_after and skill_path:
        SkillDownloader.cleanup(skill_path)
    
    # Exit code based on risk level
    if result.risk_level == "DANGEROUS":
        sys.exit(2)
    elif result.risk_level == "CAUTION":
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
