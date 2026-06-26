# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能领航员

自动选择最优技能，失败自动降级，支持技能自动发现和自适应优化

名称含义：Pilot = 领航员，引导选择最优技能路径
"""

from .scripts.engine import ExecutionEngine
from .scripts.models import SkillRequest, SkillResult, SkillMetadata
from .scripts.registry import SkillRegistry

__version__ = "0.1.0"
__author__ = "JARVIS"

# 快捷入口
def create_pilot(skills_dir: str = None) -> ExecutionEngine:
    """创建 SkillPilot 实例"""
    return ExecutionEngine(skills_dir)

# 默认实例
_default_pilot = None

def get_pilot() -> ExecutionEngine:
    """获取默认 SkillPilot 实例"""
    global _default_pilot
    if _default_pilot is None:
        _default_pilot = ExecutionEngine()
    return _default_pilot

# 快捷方法
def search(query: str, **kwargs) -> SkillResult:
    """搜索"""
    return get_pilot().search(query, **kwargs)

def fetch(url: str, **kwargs) -> SkillResult:
    """抓取"""
    return get_pilot().fetch(url, **kwargs)

def summarize(content: str, **kwargs) -> SkillResult:
    """总结"""
    return get_pilot().summarize(content, **kwargs)
