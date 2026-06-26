#!/usr/bin/env python3
"""
Skill Auditor - 主入口
支持中英文切换

Usage:
    python3 main.py <skills_dir> [options]

Examples:
    python3 main.py ~/.openclaw/workspace/skills/ --lang zh
    python3 main.py ~/.openclaw/workspace/skills/ --threshold 0.8
    python3 main.py ~/.openclaw/workspace/skills/ -o report.md
"""

import argparse
import sys
import json
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from skill_scanner import SkillScanner
from similarity_checker import SimilarityChecker
from report_generator import ReportGenerator
from locale_loader import LocaleLoader

def main():
    parser = argparse.ArgumentParser(
        description='Skill Auditor - Detect duplicate and similar skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s ~/.openclaw/workspace/skills/ --lang zh
  %(prog)s ~/.openclaw/workspace/skills/ --threshold 0.8
  %(prog)s ~/.openclaw/workspace/skills/ -o audit_report.md
        '''
    )
    parser.add_argument('skills_dir', nargs='?', 
                       default='~/.openclaw/workspace/skills/',
                       help='Skills directory to scan (default: ~/.openclaw/workspace/skills/)')
    parser.add_argument('--lang', '-l', choices=['en', 'zh', 'auto'], default='auto',
                       help='Language: en, zh, or auto-detect (default: auto)')
    parser.add_argument('--threshold', '-t', type=float, default=0.7,
                       help='Similarity threshold 0-1 (default: 0.7)')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output in JSON format')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # 展开路径
    skills_dir = Path(args.skills_dir).expanduser()
    
    # 加载语言包
    locales_dir = Path(__file__).parent.parent / 'locales'
    i18n = LocaleLoader(locales_dir)
    
    # 设置语言
    if args.lang == 'auto':
        lang = i18n.detect_system_language()
    else:
        lang = args.lang
    
    i18n.set_language(lang)
    
    if args.verbose:
        print(f"🌐 Language: {lang}")
        print(f"📂 Scanning: {skills_dir}")
    
    # 扫描技能
    print(f"🔍 {i18n.get('scan_directory')}: {skills_dir}")
    scanner = SkillScanner(str(skills_dir))
    skills = scanner.scan()
    print(f"📦 {i18n.get('total_skills')}: {len(skills)}")
    
    if not skills:
        print("⚠️ No skills found!")
        sys.exit(0)
    
    if args.verbose:
        print("\nSkills found:")
        for skill in skills:
            print(f"  - {skill['name']}")
    
    # 检查相似度
    checker = SimilarityChecker(threshold=args.threshold)
    conflicts = checker.check_all_pairs(skills)
    
    # 生成报告
    generator = ReportGenerator(i18n)
    
    if args.json:
        report = json.dumps(generator.generate_json(skills, conflicts), indent=2, ensure_ascii=False)
    else:
        report = generator.generate(skills, conflicts, str(skills_dir))
    
    # 输出
    if args.output:
        output_path = Path(args.output).expanduser()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ Report saved to {output_path}")
    else:
        print("\n" + report)
    
    # 返回状态码
    if conflicts:
        sys.exit(1)  # 有冲突
    else:
        sys.exit(0)  # 无冲突

if __name__ == '__main__':
    main()
