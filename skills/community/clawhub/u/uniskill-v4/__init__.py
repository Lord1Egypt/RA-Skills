#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 - 极简高效版
脱水重组自 V2 (8,771行) + V3 (1,807行)

核心模块：
- socratic_engine_v4.py (60行) - 需求探明
- idea_debater_v4.py (80行) - 高速辩论
- orchestrator_v4.py (120行) - 核心编排
- uniskill_v4_gateway.py (新增) - 主流程集成入口

总计：~260行（V2的3%）
"""

from .socratic_engine_v4 import SocraticEngineV4, check_clarity
from .idea_debater_v4 import HighSpeedDebater, quick_debate, validate_need
from .orchestrator_v4 import UniSkillOrchestratorV4, execute
from .uniskill_v4_gateway import (
    UniSkillV4Gateway,
    process_with_uniskill_v4,
    should_use_uniskill_v4,
    get_gateway
)


__all__ = [
    # 核心
    "SocraticEngineV4",
    "check_clarity",
    "HighSpeedDebater", 
    "quick_debate",
    "validate_need",
    "UniSkillOrchestratorV4",
    "execute",
    # 集成入口
    "UniSkillV4Gateway",
    "process_with_uniskill_v4",
    "should_use_uniskill_v4",
    "get_gateway",
]

__version__ = "4.0.0"