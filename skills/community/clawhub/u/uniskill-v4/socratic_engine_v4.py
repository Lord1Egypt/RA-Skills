#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 极简苏格拉底引擎
脱水重组自V2 socratic_engine.py (360行 → 60行)

核心保留：
- 5W2H锚点逻辑
- 收敛阈值判断

剔除：
- 冗余的收敛检查器独立文件
- 复杂的提问生成模板
- 伪造的日志记录
"""

import json
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class AnchorResult:
    """锚点结果"""
    material: str = ""
    dimensions: str = ""
    quantity: str = ""
    process: str = ""
    precision: str = ""
    score: float = 0.0
    missing: List[str] = None
    
    def __post_init__(self):
        if self.missing is None:
            self.missing = []


class SocraticEngineV4:
    """
    V4 极简需求探明引擎
    
    设计原则：
    1. 只在关键参数缺失时"咬人"
    2. 阈值判断内置（不依赖外部收敛检查器）
    3. 适配CNC报价等工业场景
    """
    
    # 核心锚点（CNC报价必填）
    MUST_HAVE = ["material", "dimensions", "quantity", "process", "precision"]
    
    # 需求清晰度阈值
    THRESHOLD = 0.7
    
    # 追问映射（V2灵魂移植）
    QUESTION_MAP = {
        "material": "材料（如 TC4, 7075 铝）",
        "dimensions": "基本尺寸或外径",
        "quantity": "加工数量",
        "process": "工艺要求（如粗加工、精加工、五轴）",
        "precision": "公差/精度要求"
    }
    
    def __init__(self):
        self.call_count = 0
    
    def analyze_clarity(
        self, 
        user_input: str, 
        extracted: Dict = None
    ) -> Tuple[float, str, AnchorResult]:
        """
        分析需求清晰度
        
        Args:
            user_input: 用户输入
            extracted: 已提取的参数（可选）
            
        Returns:
            (得分, 追问建议, 锚点结果)
        """
        self.call_count += 1
        
        # 如果没有提取结果，尝试快速提取
        if extracted is None:
            extracted = self._fast_extract(user_input)
        
        # 计算覆盖率
        found_keys = [k for k in self.MUST_HAVE if extracted.get(k)]
        score = len(found_keys) / len(self.MUST_HAVE)
        
        # 构建锚点结果
        result = AnchorResult(
            material=extracted.get("material", ""),
            dimensions=extracted.get("dimensions", ""),
            quantity=extracted.get("quantity", ""),
            process=extracted.get("process", ""),
            precision=extracted.get("precision", ""),
            score=score,
            missing=[k for k in self.MUST_HAVE if k not in found_keys]
        )
        
        # 如果分值达标，直接放行
        if score >= self.THRESHOLD:
            return score, "CLEAR", result
        
        # 如果不达标，精准定位缺失项
        missing_desc = [self.QUESTION_MAP[m] for m in result.missing]
        prompt = f"大帅，当前需求缺少关键参数：{', '.join(missing_desc)}。请补全以获得精准报价。"
        
        return score, prompt, result
    
    def _fast_extract(self, user_input: str) -> Dict:
        """
        快速参数提取（本地/云端模型）
        
        TODO: 对接本地 0.6B 或云端模型
        """
        # 简单的正则提取（临时方案）
        result = {}
        
        # 材料关键词
        materials = ["TC4", "7075", "6061", "铝", "钛", "钢", "不锈钢"]
        for m in materials:
            if m in user_input:
                result["material"] = m
                break
        
        # 数量关键词
        import re
        qty_match = re.search(r'(\d+)\s*(个|件|件|pcs)', user_input)
        if qty_match:
            result["quantity"] = qty_match.group(1)
        
        # 工艺关键词
        processes = ["粗加工", "精加工", "五轴", "车削", "铣削", "磨削"]
        for p in processes:
            if p in user_input:
                result["process"] = p
                break
        
        return result
    
    def is_clear(self, user_input: str) -> bool:
        """
        快速判断需求是否清晰
        
        Args:
            user_input: 用户输入
            
        Returns:
            是否清晰
        """
        score, _, _ = self.analyze_clarity(user_input)
        return score >= self.THRESHOLD


# 便捷函数
def check_clarity(user_input: str) -> Tuple[bool, str]:
    """快速检查需求清晰度"""
    engine = SocraticEngineV4()
    score, prompt, _ = engine.analyze_clarity(user_input)
    return score >= 0.7, prompt if prompt != "CLEAR" else "需求清晰"


# 测试
if __name__ == "__main__":
    engine = SocraticEngineV4()
    
    # 测试用例
    test_cases = [
        "帮我加工10个TC4零件",
        "需要车削50件7075铝，精度要求±0.02",
        "做个零件"
    ]
    
    for case in test_cases:
        score, prompt, result = engine.analyze_clarity(case)
        print(f"\n输入: {case}")
        print(f"得分: {score:.2f}")
        print(f"结果: {prompt}")
        print(f"缺失: {result.missing}")