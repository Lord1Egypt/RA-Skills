#!/usr/bin/env python3
"""
共享库加载器（自包含版）
优先从 skill 包目录加载 stock_utils / stock_indicators，
兼容向上查找 workspace 根目录的开发模式。
"""

import sys
import os
from pathlib import Path
from typing import Optional


def _find_skill_dir() -> Optional[str]:
    """获取 skill 包所在目录（utils 的父目录）。"""
    current = Path(__file__).resolve()
    skill_dir = current.parent.parent
    if (skill_dir / "stock_utils.py").exists() and \
       (skill_dir / "stock_indicators.py").exists():
        return str(skill_dir)
    return None


def _find_workspace_root() -> Optional[str]:
    """向上查找包含 stock_utils.py + stock_indicators.py 的目录。"""
    current = Path(__file__).resolve()
    for _ in range(8):
        current = current.parent
        if (current / "stock_utils.py").exists() and \
           (current / "stock_indicators.py").exists():
            return str(current)
    return None


def ensure_shared_libs() -> str:
    """
    确保 stock_utils / stock_indicators 可被 import。
    优先级：skill包目录 > workspace根目录
    """
    skill_dir = _find_skill_dir()
    if skill_dir and skill_dir not in sys.path:
        sys.path.insert(0, skill_dir)

    ws_root = _find_workspace_root()
    if ws_root and ws_root not in sys.path:
        sys.path.insert(0, ws_root)

    try:
        __import__("stock_utils")
        __import__("stock_indicators")
        return ws_root or skill_dir or ""
    except ImportError:
        raise ImportError(
            "无法找到 stock_utils.py / stock_indicators.py。"
            "请确认 stock-selecter 目录包含这两个共享库文件。"
        )


def import_shared_libs():
    """导入并返回 (stock_utils, stock_indicators)。"""
    ensure_shared_libs()
    try:
        import stock_utils
        import stock_indicators
        return stock_utils, stock_indicators
    except ImportError as e:
        raise ImportError(f"共享库导入失败: {e}") from e


try:
    _root = ensure_shared_libs()
except ImportError:
    _root = None
