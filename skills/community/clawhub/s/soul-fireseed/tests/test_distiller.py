#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tests/test_distiller.py
火种·灵魂 v2.0 - 蒸馏器单元测试
"""

import unittest
import sys
from pathlib import Path

# 添加 lib 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from extractor import Fossil
from distiller import FossilDistiller, PersonaModel


class TestFossilDistiller(unittest.TestCase):
    """测试蒸馏器"""
    
    def setUp(self):
        """初始化测试环境"""
        self.distiller = FossilDistiller()
        
        # 创建测试化石
        self.test_fossils = [
            Fossil(
                id=f"TEST-{i}",
                dimension=3,
                subdimension="决策风格",
                content="我倾向于分析型决策",
                timestamp="2026-05-09T00:00:00Z",
                confidence=0.8
            )
            for i in range(5)
        ]
    
    def test_distill_basic(self):
        """测试基础蒸馏功能"""
        persona = self.distiller.distill(self.test_fossils)
        
        self.assertIsInstance(persona, PersonaModel)
        self.assertEqual(persona.version, "2.0")
        self.assertGreater(persona.fossil_count, 0)
    
    def test_distill_dimensions(self):
        """测试六维度蒸馏"""
        fossils = []
        for dim in range(1, 7):
            fossils.append(Fossil(
                id=f"DIM-{dim}",
                dimension=dim,
                subdimension="test",
                content=f"维度{dim}的测试内容",
                timestamp="2026-05-09T00:00:00Z",
                confidence=0.7
            ))
        
        persona = self.distiller.distill(fossils)
        
        # 检查所有维度都有数据
        self.assertEqual(len(persona.dimensions), 6)
    
    def test_evolution_tracking(self):
        """测试演化追踪"""
        # 第一次蒸馏
        persona1 = self.distiller.distill(self.test_fossils[:3])
        
        # 第二次蒸馏（添加新化石）
        persona2 = self.distiller.update_persona(self.test_fossils[3:])
        
        # 检查是否有演化记录
        self.assertGreater(len(persona2.evolution_timeline), 0)
    
    def test_generate_report(self):
        """测试报告生成"""
        self.distiller.distill(self.test_fossils)
        report = self.distiller.generate_evolution_report(days=30)
        
        self.assertIsInstance(report, str)
        self.assertIn("人格演化报告", report)


if __name__ == "__main__":
    unittest.main()
