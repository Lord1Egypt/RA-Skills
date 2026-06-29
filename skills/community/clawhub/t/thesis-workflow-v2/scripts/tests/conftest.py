#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conftest.py - pytest 自动设置 PYTHONPATH

修复 P2-4：scripts/tests/ 下的测试模块互引用
（from test_context_builder import setup_mock_state），
必须在 scripts/ 和 scripts/tests/ 都在 sys.path 时才能跑。

加本文件后，pytest 会自动发现并运行，无需手动设 PYTHONPATH。
"""

import sys
import os

# 当前文件 = scripts/tests/conftest.py
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(TESTS_DIR)

# 把 scripts/ 和 scripts/tests/ 都加进 sys.path
for p in (SCRIPTS_DIR, TESTS_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)