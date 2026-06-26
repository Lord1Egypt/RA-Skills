#!/usr/bin/env python3
"""
tc-migrate 入口脚本

用法:
    python3 {baseDir}/main.py config auto --skip-empty-vpc
    python3 {baseDir}/main.py scan --save
    python3 {baseDir}/main.py generate
    python3 {baseDir}/main.py run

等同于 tc-migrate CLI 命令。
"""

import sys
from pathlib import Path

# 将 src 目录加入 Python 路径
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

# 导入并运行 CLI
from tc_migrate.cli import cli

if __name__ == "__main__":
    cli()
