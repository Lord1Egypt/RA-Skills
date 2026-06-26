#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自媒体文案生成器 - 单元测试
"""

import sys
import unittest
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from generator import (
    CopywriterGenerator,
    GenerateRequest,
    Platform,
    generate_titles
)
from tag_recommender import TagRecommender


class TestGenerateTitles(unittest.TestCase):
    """测试标题生成"""
    
    def test_title_count(self):
        """测试生成指定数量的标题"""
        titles = generate_titles("测试主题", count=5)
        self.assertEqual(len(titles), 5)
    
    def test_title_contains_topic(self):
        """测试标题包含主题"""
        titles = generate_titles("AI 写作", count=5)
        for title in titles:
            self.assertIn("AI 写作", title)
    
    def test_title_has_emoji_or_number(self):
        """测试标题有 emoji 或数字"""
        titles = generate_titles("测试", count=10)
        # 至少部分标题应该有 emoji 或数字
        has_special = any(
            any(c.isdigit() for c in title) or 
            any(ord(c) > 127 for c in title)
            for title in titles
        )
        self.assertTrue(has_special)


class TestTagRecommender(unittest.TestCase):
    """测试标签推荐"""
    
    def setUp(self):
        self.recommender = TagRecommender()
    
    def test_recommend_count(self):
        """测试推荐指定数量的标签"""
        recs = self.recommender.recommend("AI", "xiaohongshu", count=10)
        self.assertEqual(len(recs), 10)
    
    def test_recommend_categories(self):
        """测试标签包含不同类别"""
        recs = self.recommender.recommend("AI", "xiaohongshu", count=10)
        categories = set(rec.category for rec in recs)
        # 应该至少包含 2 种类别
        self.assertGreaterEqual(len(categories), 2)
    
    def test_format_tags_xiaohongshu(self):
        """测试小红书标签格式"""
        recs = self.recommender.recommend("AI", "xiaohongshu", count=5)
        formatted = self.recommender.format_tags(recs, "xiaohongshu")
        # 小红书格式：#标签 1 #标签 2
        self.assertIn("#", formatted)
        self.assertIn(" ", formatted)
    
    def test_format_tags_douyin(self):
        """测试抖音标签格式"""
        recs = self.recommender.recommend("AI", "douyin", count=5)
        formatted = self.recommender.format_tags(recs, "douyin")
        # 抖音格式：#标签 1#标签 2（无空格）
        self.assertIn("#", formatted)


class TestCopywriterGenerator(unittest.TestCase):
    """测试文案生成器"""
    
    def setUp(self):
        self.generator = CopywriterGenerator()
    
    def test_generate_request(self):
        """测试生成请求"""
        request = GenerateRequest(
            topic="测试主题",
            platform=Platform.XIAOHONGSHU,
            tone="自然",
            length="medium"
        )
        self.assertEqual(request.topic, "测试主题")
        self.assertEqual(request.platform, Platform.XIAOHONGSHU)
    
    def test_generate_all_platforms(self):
        """测试所有平台生成"""
        for platform in Platform:
            request = GenerateRequest(
                topic="AI 写作",
                platform=platform,
                tone="自然"
            )
            result = self.generator.generate(request)
            self.assertIsNotNone(result.title)
            self.assertIsNotNone(result.content)
            self.assertEqual(result.platform, platform)
    
    def test_mock_generation(self):
        """测试 mock 生成（不依赖 API）"""
        request = GenerateRequest(
            topic="测试",
            platform=Platform.XIAOHONGSHU
        )
        result = self.generator.generate(request)
        self.assertGreater(len(result.content), 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
