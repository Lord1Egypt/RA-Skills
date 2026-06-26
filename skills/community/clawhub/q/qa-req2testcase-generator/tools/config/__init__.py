# -*- coding: utf-8 -*-
"""
config - 统一配置模块
V4.6.14: 集中管理全链路配置
"""
from .forbidden_words import (
    L1_ABSOLUTE,
    L1_PATTERNS,
    L2_CONTEXTUAL,
    G2_PATTERNS,
    P7_CHECK_WORDS,
    has_context_signal,
    check_forbidden_words,
    CONTEXT_SIGNALS,
)

__all__ = [
    "L1_ABSOLUTE",
    "L1_PATTERNS",
    "L2_CONTEXTUAL",
    "G2_PATTERNS",
    "P7_CHECK_WORDS",
    "has_context_signal",
    "check_forbidden_words",
    "CONTEXT_SIGNALS",
]
