#!/usr/bin/env python3
"""
SQL 拆分工具 - GUI 界面 — 社区版桩
专业版功能，社区版使用时提示升级
"""

import sys


class SQLSplitterGUI:
    """社区版桩 — 提示升级专业版"""

    def __init__(self, root=None):
        print("┌──────────────────────────────────────┐")
        print("│  GUI界面需要专业版或企业版授权         │")
        print("│                                      │")
        print("│  升级专业版: ¥299/月                   │")
        print("│  访问 https://sqlsplitter.com        │")
        print("│  或运行: sql-splitter license activate│")
        print("└──────────────────────────────────────┘")


def run_gui():
    """启动GUI — 社区版提示升级"""
    SQLSplitterGUI()
    sys.exit(1)


if __name__ == '__main__':
    run_gui()
