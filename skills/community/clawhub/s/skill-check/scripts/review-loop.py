#!/usr/bin/env python3
"""
技能审查自我迭代脚本 - 循环执行审查-修复-再审查直到无问题

用法:
    review-loop.py <skill-directory> [--max-iterations N]

示例:
    review-loop.py .qoder/skills/my-skill
    review-loop.py . --max-iterations 5
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_analyze(skill_path: Path) -> tuple[bool, str]:
    """
    运行 analyze.py 脚本
    
    Returns:
        (是否有问题, 输出内容)
    """
    script_path = Path(__file__).parent / "analyze.py"
    result = subprocess.run(
        [sys.executable, str(script_path), str(skill_path)],
        capture_output=True,
        text=True
    )
    output = result.stdout + result.stderr
    
    # 检查是否有问题（P0/P1/P2 问题）
    has_issues = "P0" in output or "P1" in output or "P2" in output
    has_issues = has_issues and "未发现结构性问题" not in output
    
    return has_issues, output


def run_fix(skill_path: Path) -> tuple[bool, str]:
    """
    运行 fix.py 脚本
    
    Returns:
        (是否修复了问题, 输出内容)
    """
    script_path = Path(__file__).parent / "fix.py"
    result = subprocess.run(
        [sys.executable, str(script_path), str(skill_path)],
        capture_output=True,
        text=True
    )
    output = result.stdout + result.stderr
    
    # 检查是否修复了问题
    fixed = "已修复" in output or "已创建" in output
    
    return fixed, output


def review_loop(skill_path: Path, max_iterations: int = 10) -> None:
    """
    执行审查-修复循环
    
    Args:
        skill_path: 技能目录路径
        max_iterations: 最大迭代次数，防止无限循环
    """
    print(f"🔍 开始审查自我迭代: {skill_path.name}")
    print(f"   最大迭代次数: {max_iterations}")
    print()
    
    for iteration in range(1, max_iterations + 1):
        print(f"--- 第 {iteration} 轮迭代 ---")
        print()
        
        # 步骤1: 运行分析
        print("📋 步骤1: 结构分析")
        has_issues, analyze_output = run_analyze(skill_path)
        print(analyze_output)
        
        if not has_issues:
            print(f"✅ 第 {iteration} 轮审查通过，未发现结构性问题")
            print()
            break
        
        # 步骤2: 运行修复
        print("🔧 步骤2: 自动修复")
        fixed, fix_output = run_fix(skill_path)
        print(fix_output)
        
        if not fixed:
            print("⚠️ 自动修复未能解决问题，需要手动处理")
            print()
            break
        
        print(f"🔄 完成第 {iteration} 轮，继续下一轮...")
        print()
    else:
        print(f"⚠️ 达到最大迭代次数 ({max_iterations})，停止迭代")
        print("   可能存在问题需要手动修复")
        return
    
    # 最终报告
    print("=" * 50)
    print("✅ 自我迭代完成")
    print(f"   总迭代次数: {iteration}")
    print(f"   技能目录: {skill_path}")
    print()
    print("💡 提示: 如仍有逻辑性问题，需 LLM 进行深度内容分析")


def main():
    parser = argparse.ArgumentParser(
        description="技能审查自我迭代脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  review-loop.py .qoder/skills/my-skill
  review-loop.py . --max-iterations 5
        """
    )
    parser.add_argument(
        "skill_dir",
        help="技能目录路径"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="最大迭代次数 (默认: 10)"
    )
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_dir).resolve()
    
    if not skill_path.exists():
        print(f"❌ 错误: 目录不存在: {skill_path}")
        sys.exit(1)
    
    if not (skill_path / "SKILL.md").exists():
        print(f"❌ 错误: SKILL.md 不存在: {skill_path}")
        sys.exit(1)
    
    review_loop(skill_path, args.max_iterations)


if __name__ == "__main__":
    main()
