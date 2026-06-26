#!/usr/bin/env python3
"""初始化 .dev/ 目录结构

Usage:
  python3 init_dev.py [project_path]
  python3 init_dev.py /path/to/project
"""

import argparse
import os
from pathlib import Path
from datetime import datetime


def init_dev(project_path: str = "."):
    dev_dir = Path(project_path) / ".dev"
    dev_dir.mkdir(exist_ok=True)

    # 创建 .gitignore（可选：排除 .dev/ 或保留）
    gitignore = dev_dir / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("# 取消注释以下行来排除 .dev/ 中的产物\n# *\n# !.gitignore\n")

    # 创建空的 research.md 和 plan.md 模板
    research = dev_dir / "research.md"
    if not research.exists():
        research.write_text(f"""# Research
> 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 任务: [待填写]

## 架构理解

## 相关文件清单

## 现有约定

## 潜在风险
""")
        print(f"  ✅ 创建 {research}")

    plan = dev_dir / "plan.md"
    if not plan.exists():
        plan.write_text(f"""# Plan
> 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 任务: [待填写]
> 状态: 草稿

## 实现思路

## 文件改动清单

## 关键代码

## 取舍说明

## 排除项

## 实施清单
""")
        print(f"  ✅ 创建 {plan}")

    print(f"\n📁 .dev/ 目录就绪: {dev_dir.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="初始化 .dev/ 开发目录")
    parser.add_argument("project_path", nargs="?", default=".", help="项目根目录路径")
    args = parser.parse_args()
    init_dev(args.project_path)
