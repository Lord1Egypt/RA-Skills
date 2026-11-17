#!/usr/bin/env python3
"""Session Fork CLI — 会话分叉（打分支）入口（兼容壳）。

委托 fork_core.cli.main()。WorkBuddy 技能目录内的固定入口；
pip 安装后可用 `fork` / `fork-branch` 命令（跨平台、任意产品）。

Usage:
  create_branch.py --session current [--name "分支名"]
  create_branch.py --session <id> --match "<文本>" [--name "分支名"]
  create_branch.py --session <id> --line <N> [--name "分支名"]
  create_branch.py --session <id> --request-id <id> [--name "分支名"]
  create_branch.py --list [--adapter workbuddy|claude-code|pi|openclaw|codex|hermes]
  create_branch.py --fix <分支会话ID>

Built by the OfferKuai (Offer快) Team — https://www.offerkuai.com/
MIT License.
"""

import os
import sys

# 使脚本可直接运行（python3 scripts/create_branch.py）：
# 把技能根目录（本文件的上一级）加入模块搜索路径，以便 import 根目录下的 fork_core 包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fork_core.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
