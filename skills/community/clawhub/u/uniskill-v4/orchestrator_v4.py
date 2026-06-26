#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 核心编排器 - 8C8G优化版
整合苏格拉底探明 + 高速辩论 + 任务拆解

设计原则：
1. V2方法论 + V3工程效率
2. 内存安全（<100MB）
3. 异步优先
"""

import asyncio
import gc
from typing import Dict, List, Optional
from dataclasses import dataclass

try:
    from .socratic_engine_v4 import SocraticEngineV4, AnchorResult
    from .idea_debater_v4 import HighSpeedDebater, DebateResult
except ImportError:
    # 直接导入（用于独立测试）
    from socratic_engine_v4 import SocraticEngineV4, AnchorResult
    from idea_debater_v4 import HighSpeedDebater, DebateResult


@dataclass
class ExecutionResult:
    """执行结果"""
    success: bool
    anchor: Optional[AnchorResult]
    debate: Optional[DebateResult]
    output: str
    stats: Dict


class UniSkillOrchestratorV4:
    """
    V4 编排器 - 整合V2方法论与V3效率
    
    执行流程：
    1. 苏格拉底探明（需求锚定）
    2. 高速辩论验证（可选）
    3. 任务执行
    4. 结果交付
    """
    
    def __init__(self, enable_debate: bool = True, memory_limit_mb: int = 100):
        self.socratic = SocraticEngineV4()
        self.debater = HighSpeedDebater() if enable_debate else None
        self.enable_debate = enable_debate
        self.memory_limit = memory_limit_mb
        
        # 统计
        self.stats = {
            "total_runs": 0,
            "clear_runs": 0,
            "debate_runs": 0,
            "memory_peaks": []
        }
    
    def _check_memory(self) -> bool:
        """内存安全检查"""
        import psutil
        mem = psutil.virtual_memory()
        used_mb = mem.used / 1024 / 1024
        self.stats["memory_peaks"].append(used_mb)
        return used_mb < self.memory_limit * 1024  # 转换为MB
    
    def _gc_if_needed(self):
        """必要时强制GC"""
        if not self._check_memory():
            gc.collect()
    
    async def run_async(
        self,
        user_input: str,
        solutions: List[str] = None
    ) -> ExecutionResult:
        """
        异步执行
        
        Args:
            user_input: 用户输入
            solutions: 候选方案（可选）
            
        Returns:
            执行结果
        """
        self.stats["total_runs"] += 1
        self._gc_if_needed()
        
        # ===== 阶段1: 苏格拉底探明 =====
        score, prompt, anchor = self.socratic.analyze_clarity(user_input)
        
        # 如果需求不清晰，返回追问
        if prompt != "CLEAR":
            return ExecutionResult(
                success=False,
                anchor=anchor,
                debate=None,
                output=prompt,
                stats={"clarity_score": score}
            )
        
        self.stats["clear_runs"] += 1
        
        # ===== 阶段2: 高速辩论验证（可选）=====
        debate_result = None
        if self.enable_debate and solutions:
            debate_result = await self.debater.debate_async(user_input, solutions)
            self.stats["debate_runs"] += 1
        
        # ===== 阶段3: 任务执行 =====
        # TODO: 对接V3的TaskDecomposer或ClawHub
        
        output = f"需求已锚定，准备执行。得分: {score:.2f}"
        
        return ExecutionResult(
            success=True,
            anchor=anchor,
            debate=debate_result,
            output=output,
            stats={"clarity_score": score}
        )
    
    def run(self, user_input: str, solutions: List[str] = None) -> ExecutionResult:
        """同步接口"""
        return asyncio.run(self.run_async(user_input, solutions))
    
    def quick_check(self, user_input: str) -> tuple:
        """快速检查（仅苏格拉底探明）"""
        score, prompt, _ = self.socratic.analyze_clarity(user_input)
        return score >= 0.7, prompt


# 便捷函数
def execute(user_input: str, solutions: List[str] = None) -> ExecutionResult:
    """快速执行入口"""
    orchestrator = UniSkillOrchestratorV4()
    return orchestrator.run(user_input, solutions)


# 测试
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ("帮我加工10个TC4零件", ["五轴加工", "普通加工"]),
        ("需要车削50件7075铝，精度要求±0.02", None),
        ("做个零件", None)
    ]
    
    for user_input, solutions in test_cases:
        print(f"\n{'='*50}")
        print(f"输入: {user_input}")
        
        result = execute(user_input, solutions)
        
        print(f"成功: {result.success}")
        print(f"输出: {result.output}")
        if result.debate:
            print(f"辩论推荐: {result.debate.recommended}")
        print(f"统计: {result.stats}")