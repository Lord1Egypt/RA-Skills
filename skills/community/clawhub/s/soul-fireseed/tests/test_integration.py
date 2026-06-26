#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tests/test_integration.py
火种·灵魂 v2.0 - 集成测试
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from extractor import FossilExtractor
from distiller import FossilDistiller
from validator import ConfidenceValidator


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流：提取 → 验证 → 蒸馏"""
        # 1. 提取化石
        extractor = FossilExtractor()
        text = "我最近工作压力很大，经常熬夜到凌晨。但我发现完成项目后很有成就感。"
        fossils = extractor.extract(text)
        
        self.assertGreater(len(fossils), 0)
        
        # 2. 验证化石
        validator = ConfidenceValidator()
        for fossil in fossils:
            result = validator.validate(fossil)
            self.assertIn("calibrated_confidence", result)
        
        # 3. 蒸馏人格模型
        distiller = FossilDistiller()
        persona = distiller.distill(fossils)
        
        self.assertIsNotNone(persona)
        self.assertEqual(len(persona.dimensions), 6)
    
    def test_batch_workflow(self):
        """测试批量工作流"""
        extractor = FossilExtractor()
        
        texts = [
            "今天工作很累，但很有收获",
            "我和朋友一起去爬山了",
            "我正在学习新的编程技能",
            "我对未来充满期待"
        ]
        
        fossils = extractor.batch_extract(texts)
        self.assertGreater(len(fossils), 0)
        
        # 蒸馏
        distiller = FossilDistiller()
        persona = distiller.distill(fossils)
        
        self.assertIsNotNone(persona)


if __name__ == "__main__":
    unittest.main()
