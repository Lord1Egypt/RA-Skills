#!/usr/bin/env python3
"""
core/__init__.py — 核心模块导出
"""

from .constants import *
from .utils import (
    _ensure_dir, _write_json, _read_json, _file_exists, _sha256,
    _detect_domain, _write_text, _read_file_safe, _get_nested,
    _get_case_field, _is_smoke,
)
from .security import (
    _get_hmac_key, _get_legacy_hmac_key, _sign_gate,
    _write_signed_gate, _verify_gate_hmac, _CURRENT_ACTION,
)
from .state import TaskState, check_gate, run_truncation_guard
