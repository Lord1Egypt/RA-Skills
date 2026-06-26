#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日报报表生成器 - 使用示例

演示如何使用 daily-report-generator skill 生成日报报表
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    """主函数"""
    print("=" * 80)
    print("日报报表生成器 - 使用示例")
    print("=" * 80)
    print()

    # 设置路径
    workspace_dir = "/Users/ahs/.openclaw/workspace"
    skill_dir = os.path.join(workspace_dir, "skills/daily-report-generator")
    script_path = os.path.join(skill_dir, "scripts/generate_assessment_period_report.py")

    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return 1

    print(f"✅ 找到脚本: {script_path}")
    print()

    # 显示使用说明
    print("使用方法:")
    print("-" * 80)
    print("1. 确保输入数据文件存在:")
    print("   /Users/ahs/.openclaw/workspace/传输单边故障/output/结果D_最终数据.xlsx")
    print()
    print("2. 运行脚本:")
    print(f"   python3 {script_path}")
    print()
    print("3. 查看输出:")
    print("   /Users/ahs/.openclaw/workspace/传输单边故障/output/日报报表_按考核周期_*.xlsx")
    print("-" * 80)
    print()

    # 询问是否运行
    response = input("是否现在运行脚本？(y/n): ").strip().lower()

    if response == 'y' or response == 'yes':
        print()
        print("正在运行脚本...")
        print("-" * 80)

        # 运行脚本
        try:
            result = subprocess.run(
                ["python3", script_path],
                cwd="/Users/ahs/.openclaw/workspace/传输单边故障",
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )

            # 输出结果
            print(result.stdout)
            if result.stderr:
                print("错误输出:")
                print(result.stderr)

            print("-" * 80)
            print()

            if result.returncode == 0:
                print("✅ 脚本运行成功！")
                return 0
            else:
                print(f"❌ 脚本运行失败，返回码: {result.returncode}")
                return 1

        except subprocess.TimeoutExpired:
            print("❌ 脚本运行超时")
            return 1
        except Exception as e:
            print(f"❌ 运行脚本时出错: {e}")
            return 1
    else:
        print("已取消运行")
        return 0

if __name__ == '__main__':
    sys.exit(main())
