# -*- coding: utf-8 -*-
"""
测试公共支撑。

1. 将 scripts/ 加入 sys.path，便于 `from cli…` / `from db…` / `from util…` 等导入。
2. `IsolatedDataRoot`：设置 `JIANGCHANG_DATA_ROOT` 与 `JIANGCHANG_USER_ID`，
   退出时恢复原值并删除临时目录，避免污染真实用户数据目录。
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
from typing import Optional

_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.abspath(os.path.join(_TESTS_DIR, ".."))
_SCRIPTS_DIR = os.path.join(_SKILL_ROOT, "scripts")

if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

_ISOLATION_KEYS = (
    "JIANGCHANG_DATA_ROOT",
    "JIANGCHANG_USER_ID",
)


def get_scripts_dir() -> str:
    return _SCRIPTS_DIR


def get_skill_root() -> str:
    return _SKILL_ROOT


def platform_kit_version_patch(version: str = "1.0.17"):
    """Mock installed jiangchang-platform-kit version for health/diagnostics tests."""
    from unittest.mock import patch

    return patch(
        "jiangchang_skill_core.runtime_diagnostics._platform_kit_version",
        return_value=version,
    )


class IsolatedDataRoot:
    """
    在独立临时目录下模拟数据根，避免污染本机默认数据目录。

    进入上下文时：
      - JIANGCHANG_DATA_ROOT -> tempfile.mkdtemp(prefix='skill-test-')
      - JIANGCHANG_USER_ID     -> _test（与业务默认用户区分）

    退出时：两个变量均恢复为进入前状态（若原先未设置则 pop），并删除临时目录。
    """

    def __init__(self, user_id: str = "_test") -> None:
        self._tmp: Optional[str] = None
        self._old: dict[str, Optional[str]] = {}
        self._user_id = user_id

    def __enter__(self) -> str:
        self._tmp = tempfile.mkdtemp(prefix="skill-test-")
        for k in _ISOLATION_KEYS:
            self._old[k] = os.environ.get(k)
        os.environ["JIANGCHANG_DATA_ROOT"] = self._tmp
        os.environ["JIANGCHANG_USER_ID"] = self._user_id
        return self._tmp

    def __exit__(self, *exc_info: object) -> None:
        for k in _ISOLATION_KEYS:
            v = self._old.get(k)
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        if self._tmp and os.path.isdir(self._tmp):
            shutil.rmtree(self._tmp, ignore_errors=True)
        self._tmp = None
