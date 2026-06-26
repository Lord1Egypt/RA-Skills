#!/usr/bin/env python3
"""
单元测试 - AIAG-VDA 报告生成器
测试 Figure 12-1, 12-2, 12-3 报告生成
"""

import unittest
import numpy as np
import sys
import os
import tempfile

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from aiagvda_unified_report import (
    AIAGVDAReportGenerator,
    StudyInfo,
    Specification,
    calculate_stats,
    TEXTS
)


class TestAIAVDAReportGenerator(unittest.TestCase):
    """AIAG-VDA 报告生成器测试"""
    
    def setUp(self):
        """设置测试数据"""
        np.random.seed(42)
        self.data = np.random.normal(130.0392, 0.033, 875)
        self.spec = Specification(usl=130.15, lsl=129.95, target=130.05)
        self.study_info = StudyInfo(
            process_name="Test Process",
            machine_name="Test Machine",
            study_location="Test Lab",
            part_name="Part A",
            part_id="001",
            characteristic_name="Dimension"
        )
    
    def test_text_resources(self):
        """测试文本资源"""
        # 中文资源
        self.assertIn('zh', TEXTS)
        self.assertEqual(TEXTS['zh']['title'], 'SPC 过程能力研究报告')
        
        # 英文资源
        self.assertIn('en', TEXTS)
        self.assertEqual(TEXTS['en']['title'], 'SPC Process Capability Study Report')
    
    def test_specification(self):
        """测试规格限类"""
        # 计算 tolerance
        tolerance = self.spec.usl - self.spec.lsl
        self.assertAlmostEqual(tolerance, 0.2, places=4)
        self.assertAlmostEqual(self.spec.target, 130.05, places=4)
    
    def test_calculate_stats(self):
        """测试统计计算"""
        results = calculate_stats(self.data, self.spec)
        
        # 验证返回字典
        self.assertIsInstance(results, dict)
        
        # 验证基本统计
        self.assertEqual(results['n'], 875)
        self.assertGreater(results['mean'], 130.0)
        self.assertLess(results['mean'], 130.1)
        
        # 验证能力指数
        self.assertGreater(results['cp_g'], 0)
        self.assertGreater(results['cpk_g'], 0)
        
        # 验证 PPM
        self.assertGreater(results['ppm_upper'], 0)
        self.assertGreater(results['ppm_lower'], 0)
    
    def test_generate_figure12_1_english(self):
        """测试 Figure 12-1 英文报告生成"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            generator = AIAGVDAReportGenerator(lang='en')
            result = generator.generate_figure12_1(output_path, self.data, self.spec)
            
            # 验证文件生成
            self.assertTrue(os.path.exists(result))
            self.assertGreater(os.path.getsize(result), 1000)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_generate_figure12_3(self):
        """测试 Figure 12-3 报告生成"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        try:
            generator = AIAGVDAReportGenerator(lang='en')
            result = generator.generate_figure12_3(output_path, self.data, self.spec)
            
            # 验证文件生成
            self.assertTrue(os.path.exists(result))
            self.assertGreater(os.path.getsize(result), 1000)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


class TestCapabilityResults(unittest.TestCase):
    """能力分析结果测试"""
    
    def test_normal_distribution(self):
        """测试正态分布数据"""
        np.random.seed(42)
        data = np.random.normal(10.0, 0.1, 100)
        spec = Specification(usl=10.3, lsl=9.7, target=10.0)
        
        results = calculate_stats(data, spec)
        
        # 能力应该很好
        self.assertGreater(results['cpk_g'], 1.0)
    
    def test_shifted_process(self):
        """测试偏移过程"""
        np.random.seed(42)
        data = np.random.normal(10.2, 0.1, 100)  # 偏移
        spec = Specification(usl=10.3, lsl=9.7, target=10.0)
        
        results = calculate_stats(data, spec)
        
        # 偏移过程的 Cpk 应该低于 Cp
        self.assertLess(results['cpk_g'], results['cp_g'])
    
    def test_small_sample(self):
        """测试小样本"""
        data = np.array([10.1, 10.2, 10.15, 10.18, 10.12])
        spec = Specification(usl=10.5, lsl=9.5, target=10.0)
        
        results = calculate_stats(data, spec)
        
        self.assertEqual(results['n'], 5)
        self.assertGreater(results['cp_g'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
