#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 主流程集成入口
连接 OpenClaw Agent 与 UniSkill V4 核心

使用方式：
1. 自动触发：复杂决策问题
2. 手动触发："点子王验证"、"帮我评估"等关键词
"""

import os
import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json

# 添加路径
V4_PATH = os.path.dirname(os.path.abspath(__file__))
if V4_PATH not in sys.path:
    sys.path.insert(0, V4_PATH)

try:
    from .orchestrator_v4 import UniSkillOrchestratorV4, ExecutionResult
    from .socratic_engine_v4 import SocraticEngineV4, check_clarity
    from .idea_debater_v4 import HighSpeedDebater, quick_debate
except ImportError:
    # 直接导入（用于独立测试）
    from orchestrator_v4 import UniSkillOrchestratorV4, ExecutionResult
    from socratic_engine_v4 import SocraticEngineV4, check_clarity
    from idea_debater_v4 import HighSpeedDebater, quick_debate


@dataclass
class IntegratedResult:
    """集成结果"""
    triggered: bool           # 是否触发V4
    clarity_score: float      # 清晰度评分
    needs_more_info: bool     # 是否需要更多信息
    question: str             # 追问内容（如果有）
    debate_result: Optional[Dict]  # 辩论结果
    recommendation: str       # 最终推荐
    confidence: float         # 置信度


class UniSkillV4Gateway:
    """
    V4 网关 - 连接主流程与 UniSkill V4
    """
    
    # 触发关键词
    TRIGGER_KEYWORDS = [
        "帮我评估", "验证这个", "哪个更好", "点子王验证",
        "分析一下", "比较", "选择", "决策",
        "开源", "闭源", "策略", "方案"
    ]
    
    # CNC相关关键词（优先触发）
    CNC_KEYWORDS = [
        "报价", "加工", "材料", "零件", "车削", "铣削",
        "TC4", "7075", "6061", "铝", "钛", "钢"
    ]
    
    def __init__(self):
        self.orchestrator = UniSkillOrchestratorV4(enable_debate=True)
        self.socratic = SocraticEngineV4()
        self.debater = HighSpeedDebater()
    
    def should_trigger(self, user_input: str) -> bool:
        """
        判断是否应该触发 UniSkill V4
        
        Args:
            user_input: 用户输入
            
        Returns:
            是否触发
        """
        # CNC相关优先触发
        for kw in self.CNC_KEYWORDS:
            if kw in user_input:
                return True
        
        # 决策相关触发
        for kw in self.TRIGGER_KEYWORDS:
            if kw in user_input:
                return True
        
        return False
    
    def process(self, user_input: str) -> IntegratedResult:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入
            
        Returns:
            集成结果
        """
        # 1. 检查是否应该触发
        triggered = self.should_trigger(user_input)
        
        if not triggered:
            return IntegratedResult(
                triggered=False,
                clarity_score=0.0,
                needs_more_info=False,
                question="",
                debate_result=None,
                recommendation="",
                confidence=0.0
            )
        
        # 2. 判断场景类型
        is_cnc_scene = any(kw in user_input for kw in self.CNC_KEYWORDS)
        is_decision_scene = any(kw in user_input for kw in ["评估", "验证", "选择", "比较", "决策", "开源", "闭源"])
        
        # 3. 决策场景：直接辩论（不做苏格拉底追问）
        if is_decision_scene and not is_cnc_scene:
            solutions = self._generate_solutions(user_input)
            
            if solutions:
                debate = self.debater.debate(user_input, solutions)
                return IntegratedResult(
                    triggered=True,
                    clarity_score=1.0,  # 决策问题默认清晰
                    needs_more_info=False,
                    question="",
                    debate_result={
                        "recommended": debate.recommended,
                        "score": debate.score,
                        "confidence": debate.confidence,
                        "details": debate.details
                    },
                    recommendation=f"推荐方案: {debate.recommended}（评分: {debate.score:.2f}）",
                    confidence=debate.confidence
                )
            else:
                return IntegratedResult(
                    triggered=True,
                    clarity_score=0.5,
                    needs_more_info=False,
                    question="",
                    debate_result=None,
                    recommendation="决策问题需要提供候选方案",
                    confidence=0.5
                )
        
        # 4. CNC场景：苏格拉底探明
        score, prompt, anchor = self.socratic.analyze_clarity(user_input)
        
        # 如果需求不清晰，返回追问
        if prompt != "CLEAR":
            return IntegratedResult(
                triggered=True,
                clarity_score=score,
                needs_more_info=True,
                question=prompt,
                debate_result=None,
                recommendation="",
                confidence=score
            )
        
        # 需求清晰，准备执行
        return IntegratedResult(
            triggered=True,
            clarity_score=score,
            needs_more_info=False,
            question="",
            debate_result=None,
            recommendation="需求已锚定，准备执行报价",
            confidence=score
        )
    
    def _generate_solutions(self, user_input: str) -> List[str]:
        """
        自动生成候选方案
        
        Args:
            user_input: 用户输入
            
        Returns:
            候选方案列表
        """
        solutions = []
        
        # 开源/闭源策略问题
        if "开源" in user_input or "闭源" in user_input:
            solutions = [
                "开源框架，闭源应用",
                "开源应用，闭源框架",
                "全部开源",
                "全部闭源"
            ]
        
        # 收费策略问题
        elif "收费" in user_input or "定价" in user_input:
            solutions = [
                "订阅制收费",
                "一次性买断",
                "免费+增值服务",
                "API按量计费"
            ]
        
        # CNC相关问题（不生成方案，直接执行）
        elif any(kw in user_input for kw in self.CNC_KEYWORDS):
            solutions = []  # 不辩论，直接走报价流程
        
        return solutions
    
    def quick_analyze(self, user_input: str) -> Tuple[bool, str]:
        """
        快速分析（轻量接口）
        
        Args:
            user_input: 用户输入
            
        Returns:
            (是否清晰, 提示信息)
        """
        return check_clarity(user_input)
    
    def multi_model_debate(
        self,
        problem: str,
        solutions: List[str],
        rounds: int = 3
    ) -> Dict:
        """
        多模型辩论（完整版）
        
        Args:
            problem: 问题描述
            solutions: 候选方案
            rounds: 辩论轮次
            
        Returns:
            辩论结果
        """
        results = []
        
        for r in range(rounds):
            debate = self.debater.debate(problem, solutions)
            results.append({
                "round": r + 1,
                "recommended": debate.recommended,
                "score": debate.score,
                "confidence": debate.confidence
            })
        
        # 汇总结果
        best = max(results, key=lambda x: x["score"])
        
        return {
            "total_rounds": rounds,
            "final_recommendation": best["recommended"],
            "final_score": best["score"],
            "final_confidence": best["confidence"],
            "round_details": results
        }


# 全局单例
_gateway = None

def get_gateway() -> UniSkillV4Gateway:
    """获取网关单例"""
    global _gateway
    if _gateway is None:
        _gateway = UniSkillV4Gateway()
    return _gateway


def process_with_uniskill_v4(user_input: str) -> IntegratedResult:
    """
    使用 UniSkill V4 处理用户输入
    
    这是主流程应该调用的入口函数
    
    Args:
        user_input: 用户输入
        
    Returns:
        集成结果
    """
    gateway = get_gateway()
    return gateway.process(user_input)


def should_use_uniskill_v4(user_input: str) -> bool:
    """
    判断是否应该使用 UniSkill V4
    
    Args:
        user_input: 用户输入
        
    Returns:
        是否应该使用
    """
    gateway = get_gateway()
    return gateway.should_trigger(user_input)


# 测试
if __name__ == "__main__":
    test_cases = [
        "帮我评估一下开源框架还是开源应用？",
        "加工10个TC4零件",
        "做个零件",
        "你好"
    ]
    
    print("=" * 60)
    print("🦫 UniSkill V4 集成测试")
    print("=" * 60)
    
    for case in test_cases:
        print(f"\n输入: {case}")
        result = process_with_uniskill_v4(case)
        
        print(f"触发V4: {result.triggered}")
        print(f"清晰度: {result.clarity_score:.2f}")
        
        if result.needs_more_info:
            print(f"追问: {result.question}")
        elif result.debate_result:
            print(f"辩论推荐: {result.debate_result['recommended']}")
            print(f"置信度: {result.confidence*100:.1f}%")
        
        print("-" * 40)