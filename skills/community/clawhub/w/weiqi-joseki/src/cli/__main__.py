#!/usr/bin/env python3
"""
CLI入口 - 支持 python -m src.cli.commands
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from cli.commands import main

if __name__ == "__main__":
    sys.exit(main())
