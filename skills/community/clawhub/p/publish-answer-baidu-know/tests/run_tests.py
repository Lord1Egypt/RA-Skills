# -*- coding: utf-8 -*-
"""后端 / CLI / DB 单元测试入口（unittest，不强制 pytest）。

用法：
    python tests/run_tests.py              # 发现 tests/ 根目录下全部 test_*.py
    python tests/run_tests.py -v           # 详细输出
    python tests/run_tests.py cli_smoke    # 仅匹配 test_cli_smoke.py
    python tests/run_tests.py test_cli_smoke

说明：
    只发现本目录（tests/）下一层的 test_*.py；不递归 ``samples/``、``integration/``、
    ``desktop/``（后三者提供 ``*.sample`` 或 pytest 专用用例，见 ``tests/README.md``）。
"""
from __future__ import annotations

import os
import sys
import unittest

_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.abspath(os.path.join(_TESTS_DIR, ".."))
_SCRIPTS_DIR = os.path.abspath(os.path.join(_SKILL_ROOT, "scripts"))

for _p in (_SCRIPTS_DIR, _TESTS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Windows 下统一 stdout/stderr 为 UTF-8，避免 GBK 控制台中文/emoji 报错
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def _pattern_from_argv(argv: list[str]) -> str:
    for a in argv[1:]:
        if a.startswith("-"):
            continue
        s = a if a.startswith("test_") else f"test_{a}"
        if not s.endswith(".py"):
            s = f"{s}.py"
        return s
    return "test_*.py"


def _verbosity_from_argv(argv: list[str]) -> int:
    return 2 if ("-v" in argv or "--verbose" in argv) else 1


def main() -> int:
    pattern = _pattern_from_argv(sys.argv)
    verbosity = _verbosity_from_argv(sys.argv)
    loader = unittest.TestLoader()
    suite = loader.discover(_TESTS_DIR, pattern=pattern)
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
