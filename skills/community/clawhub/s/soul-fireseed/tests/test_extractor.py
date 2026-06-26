#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tests/test_extractor.py
火种·灵魂 v2.0 - 提取引擎单元测试
"""

import unittest
import sys
from pathlib import Path

# 添加 lib 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from extractor import FossilExtractor, ExtractorConfig, Fossil


class TestExtractorConfig(unittest.TestCase):
    """测试配置类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = ExtractorConfig()
        self.assertEqual(config.max_fossils_per_dimension, 2)
        self.assertEqual(config.pending_confidence_threshold, 0.6)
        self.assertEqual(config.high_confidence_threshold, 0.8)
    
    def test_dimension_weights(self):
        """测试维度权重"""
        config = ExtractorConfig()
        self.assertEqual(len(config.dimension_weights), 6)
        for dim in range(1, 7):
            self.assertIn(dim, config.dimension_weights)


class TestFossilExtractor(unittest.TestCase):
    """测试提取引擎"""
    
    def setUp(self):
        """初始化测试环境"""
        self.extractor = FossilExtractor()
    
    def test_extract_basic(self):
        """测试基础提取功能"""
        text = "我最近很累，经常熬夜"
        fossils = self.extractor.extract(text)
        
        self.assertIsInstance(fossils, list)
        self.assertGreater(len(fossils), 0)
        
        # 检查化石结构
        for fossil in fossils:
            self.assertIsInstance(fossil, Fossil)
            self.assertIsNotNone(fossil.id)
            self.assertIn(fossil.dimension, range(1, 7))
            self.assertTrue(0.0 <= fossil.confidence <= 1.0)
    
    def test_extract_empty_text(self):
        """测试空文本"""
        fossils = self.extractor.extract("")
        self.assertEqual(len(fossils), 0)
    
    def test_extract_multiple_dimensions(self):
        """测试多维度提取"""
        text = "我以前很内向，但现在学会了主动与人交流，这让我很开心"
        fossils = self.extractor.extract(text)
        
        dimensions = set(f.dimension for f in fossils)
        self.assertGreater(len(dimensions), 1)
    
    def test_batch_extract(self):
        """测试批量提取"""
        texts = [
            "今天工作很累",
            "我和朋友去爬山了",
            "我正在学习新技能"
        ]
        
        fossils = self.extractor.batch_extract(texts)
        self.assertGreater(len(fossils), 0)
    
    def test_extraction_stats(self):
        """测试统计信息"""
        self.extractor.extract("测试文本")
        stats = self.extractor.get_extraction_stats()
        
        self.assertIn("extraction_count", stats)
        self.assertIn("total_fossils_extracted", stats)
        self.assertGreater(stats["extraction_count"], 0)


class TestDimensionExtractors(unittest.TestCase):
    """测试各维度提取器"""
    
    def setUp(self):
        """初始化测试环境"""
        self.config = ExtractorConfig()
    
    def test_bio_physical_extractor(self):
        """测试生物物理维度提取"""
        from extractor import BioPhysicalExtractor
        
        extractor = BioPhysicalExtractor(self.config)
        fossils = extractor.extract({}, "我最近很累，经常熬夜")
        
        self.assertGreater(len(fossils), 0)
        self.assertEqual(fossils[0].dimension, 1)
    
    def test_cognitive_extractor(self):
        """测试认知架构维度提取"""
        from extractor import CognitiveExtractor
        
        extractor = CognitiveExtractor(self.config)
        fossils = extractor.extract({}, "我做决定时会先分析所有选项")
        
        self.assertGreater(len(fossils), 0)
        self.assertEqual(fossils[0].dimension, 3)
    
    def test_affective_extractor(self):
        """测试情感动力学维度提取"""
        from extractor import AffectiveExtractor
        
        extractor = AffectiveExtractor(self.config)
        fossils = extractor.extract({}, "今天很开心，完成了重要项目")
        
        self.assertGreater(len(fossils), 0)
        self.assertEqual(fossils[0].dimension, 4)


if __name__ == "__main__":
    unittest.main()
