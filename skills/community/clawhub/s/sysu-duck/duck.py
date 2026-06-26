#!/usr/bin/env python3
"""
仓库根目录入口：在技能包根目录执行 `python3 duck.py <命令>`，无需设置 PYTHONPATH。
实现见 `src/duck.py`。
"""
from __future__ import annotations

import importlib.util
import os
import sys

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _REPO_ROOT)

_SRC_DUCK = os.path.join(_REPO_ROOT, 'src', 'duck.py')
_spec = importlib.util.spec_from_file_location('__main__', _SRC_DUCK)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f'无法加载 {_SRC_DUCK}')
_mod = importlib.util.module_from_spec(_spec)
sys.modules['__main__'] = _mod
_spec.loader.exec_module(_mod)
