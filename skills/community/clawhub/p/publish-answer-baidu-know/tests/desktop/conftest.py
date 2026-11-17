# -*- coding: utf-8 -*-
"""
可选桌面 E2E：pytest 收集时自动加载，负责把 jiangchang_desktop_sdk 加入 sys.path。

查找顺序：
1. 已 pip install 则直接 import；
2. 环境变量 JIANGCHANG_KIT_ROOT → sdk/jiangchang-desktop-sdk/src（旧版布局）；
3. 环境变量 JIANGCHANG_KIT_ROOT → src（新版 platform-kit 布局）；
4. 自本文件上溯：skill 根 → workspace 根 → OpenClaw 根，拼路径；
5. 兜底 D:\\AI\\jiangchang-platform-kit\\src（若存在）；
6. 都找不到则 pytest.exit 给出可操作的排障说明。
"""
from __future__ import annotations

import importlib.util
import os
import sys

import pytest


def _bootstrap_jiangchang_desktop_sdk() -> None:
    if importlib.util.find_spec("jiangchang_desktop_sdk") is not None:
        return

    env_kit_root = (os.environ.get("JIANGCHANG_KIT_ROOT") or "").strip()

    here = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.abspath(os.path.join(here, "..", ".."))
    workspace_root = os.path.abspath(os.path.join(skill_root, ".."))
    open_claw_root = os.path.abspath(os.path.join(workspace_root, ".."))

    candidates = []
    if env_kit_root:
        candidates.append(os.path.join(env_kit_root, "sdk", "jiangchang-desktop-sdk", "src"))
        candidates.append(os.path.join(env_kit_root, "src"))
    candidates.append(
        os.path.join(workspace_root, "jiangchang-platform-kit", "sdk", "jiangchang-desktop-sdk", "src")
    )
    candidates.append(
        os.path.join(open_claw_root, "jiangchang-platform-kit", "sdk", "jiangchang-desktop-sdk", "src")
    )
    candidates.append(
        os.path.join(workspace_root, "jiangchang-platform-kit", "src")
    )
    candidates.append(
        os.path.join(open_claw_root, "jiangchang-platform-kit", "src")
    )
    default_kit_src = r"D:\AI\jiangchang-platform-kit\src"
    if os.path.isdir(default_kit_src):
        candidates.append(default_kit_src)

    tried = []
    for cand in candidates:
        cand_abs = os.path.abspath(cand)
        tried.append(cand_abs)
        if os.path.isdir(cand_abs) and os.path.isdir(os.path.join(cand_abs, "jiangchang_desktop_sdk")):
            if cand_abs not in sys.path:
                sys.path.insert(0, cand_abs)
            return

    pytest.exit(
        "无法定位 jiangchang_desktop_sdk。请任选一种方式解决：\n"
        "  1) pip install -e <path-to>/jiangchang-platform-kit\n"
        "  2) 设置环境变量 JIANGCHANG_KIT_ROOT=<path-to>/jiangchang-platform-kit\n"
        "     （SDK 新版位置：<root>\\src；旧版：<root>\\sdk\\jiangchang-desktop-sdk\\src）\n"
        "  3) 将 jiangchang-platform-kit 与本仓库放在同一 workspace 父级可推断的位置\n"
        "已尝试的候选路径：\n  - " + "\n  - ".join(tried),
        returncode=4,
    )


_bootstrap_jiangchang_desktop_sdk()

_ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def failure_snapshot_dir() -> str:
    os.makedirs(_ARTIFACT_DIR, exist_ok=True)
    return _ARTIFACT_DIR
