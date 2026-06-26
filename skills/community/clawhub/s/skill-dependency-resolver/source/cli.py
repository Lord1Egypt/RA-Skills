#!/usr/bin/env python3
"""
skill-dependency-resolver CLI
扫描技能依赖，解决 requirements.txt 冲突
"""

import sys
import argparse
from pathlib import Path

# 添加技能源码到 path
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "source"))

from resolver import DependencyResolver

def main():
    parser = argparse.ArgumentParser(
        description="自动检测并解决技能间的 requirements.txt 依赖冲突",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s skills_dir="./skills" output_file="requirements-merged.txt"
  %(prog)s strategy="manual"  # 交互式解决冲突
        """
    )
    
    parser.add_argument("--skills-dir", default="~/.openclaw/workspace/skills",
                       help="技能目录路径（默认: ~/.openclaw/workspace/skills）")
    parser.add_argument("--output-file", default="requirements-merged.txt",
                       help="输出文件路径（默认: requirements-merged.txt）")
    parser.add_argument("--strategy", choices=["auto", "manual"], default="auto",
                       help="冲突解决策略：auto（自动选最高版本）或 manual（交互式选择）")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # 运行解析器
    resolver = DependencyResolver(
        skills_dir=Path(args.skills_dir).expanduser(),
        output_file=Path(args.output_file),
        strategy=args.strategy,
        verbose=args.verbose
    )
    
    report = resolver.resolve()
    
    # 打印报告
    print("✅ 依赖分析完成！")
    print(f"   扫描技能数: {report['skills_scanned']}")
    print(f"   发现冲突: {report['conflicts_found']} 个包")
    print(f"   解决方案: {report['solutions_applied']} 个")
    print(f"   输出文件: {report['output_file']}")
    
    if report['conflicts']:
        print("\n⚠️  冲突详情:")
        for conflict in report['conflicts']:
            print(f"   - {conflict['package']}: {conflict['versions']} → {conflict['resolved']}")
    
    return report

if __name__ == "__main__":
    main()