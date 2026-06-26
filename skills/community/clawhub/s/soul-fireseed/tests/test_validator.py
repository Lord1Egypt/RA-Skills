#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tests/test_validator.py
火种·灵魂 v2.0 - 校验器单元测试
"""

import unittest
import sys
from pathlib import Path

# 添加 lib 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from extractor import Fossil
from validator import ConfidenceValidator


class TestConfidenceValidator(unittest.TestCase):
    """测试置信度校验器"""
    
    def setUp(self):
        """初始化测试环境"""
        self.validator = ConfidenceValidator()
        
        self.test_fossil = Fossil(
            id="TEST-001",
            dimension=3,
            subdimension="决策风格",
            content="我倾向于分析型决策",
            timestamp="2026-05-09T00:00:00Z",
            confidence=0.8
        )
    
    def test_validate_basic(self):
        """测试基础验证"""
        result = self.validator.validate(self.test_fossil)
        
        self.assertIn("calibrated_confidence", result)
        self.assertIn("consistency_score", result)
        self.assertIn("has_contradiction", result)
    
    def test_detect_contradiction(self):
        """测试矛盾检测"""
        fossil1 = Fossil(
            id="TEST-001",
            dimension=3,
            subdimension="风险偏好",
            content="我喜欢冒险",
            timestamp="2026-05-09T00:00:00Z",
            confidence=0.8
        )
        
        fossil2 = Fossil(
            id="TEST-002",
            dimension=3,
            subdimension="风险偏好",
            content="我很谨慎，讨厌冒险",
            timestamp="2026-05-09T00:00:00Z",
            confidence=0.8
        )
        
        is_contradiction = self.validator.detect_contradiction(fossil1, fossil2)
        self.assertTrue(is_contradiction)
    
    def test_adjust_confidence(self):
        """测试置信度调整"""
        adjusted = self.validator.adjust_confidence(
            original_confidence=0.8,
            historical_accuracy=0.9,
            consistency=0.85
        )
        
        self.assertLessEqual(adjusted, 1.0)
        self.assertGreaterEqual(adjusted, 0.0)


if __name__ == "__main__":
    unittest.main()
