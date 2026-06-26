#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TechRecruiter Pro 单元测试
"""

import unittest
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from recruiter import TechRecruiterPro, CandidateProfile
from search import PlatformSearch


class TestCandidateProfile(unittest.TestCase):
    """测试候选人画像"""
    
    def test_create_profile(self):
        """测试创建画像"""
        profile = CandidateProfile("测试用户")
        self.assertEqual(profile.name, "测试用户")
        self.assertEqual(profile.match_score, 0)
        self.assertEqual(profile.status, "发现")
    
    def test_to_dict(self):
        """测试转换为字典"""
        profile = CandidateProfile("测试用户")
        profile.current_company = "测试公司"
        profile.paper_count = 10
        
        data = profile.to_dict()
        self.assertEqual(data["姓名"], "测试用户")
        self.assertEqual(data["当前公司"], "测试公司")
        self.assertEqual(data["论文数"], 10)


class TestTechRecruiterPro(unittest.TestCase):
    """测试招聘主程序"""
    
    def setUp(self):
        """测试前准备"""
        self.recruiter = TechRecruiterPro()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.recruiter.templates)
        self.assertIn("initial_outreach", self.recruiter.templates)
    
    def test_generate_email(self):
        """测试邮件生成"""
        profile = CandidateProfile("测试用户")
        profile.research_areas = ["RLHF", "LLM"]
        profile.top_papers = [{
            "title": "测试论文",
            "year": 2025
        }]
        
        job_desc = {
            "company": "测试公司",
            "position": "算法工程师"
        }
        
        email = self.recruiter.generate_email(profile, job_desc)
        self.assertIn("测试用户", email)
        self.assertIn("测试论文", email)
        self.assertIn("测试公司", email)


class TestPlatformSearch(unittest.TestCase):
    """测试平台搜索"""
    
    def setUp(self):
        """测试前准备"""
        self.searcher = PlatformSearch()
    
    def test_search_aminer(self):
        """测试 AMiner 搜索"""
        results = self.searcher.search_aminer(
            keywords=["RLHF", "LLM"],
            affiliation="Moonshot"
        )
        self.assertIsInstance(results, list)
    
    def test_search_google_scholar(self):
        """测试 Google Scholar 搜索"""
        results = self.searcher.search_google_scholar(
            author_name="Yifan Bai",
            keywords=["LLM"]
        )
        self.assertIsInstance(results, list)
    
    def test_search_github(self):
        """测试 GitHub 搜索"""
        results = self.searcher.search_github(
            keywords=["RLHF", "PPO"],
            language="Python",
            min_stars=100
        )
        self.assertIsInstance(results, list)
    
    def test_search_arxiv(self):
        """测试 arXiv 搜索"""
        results = self.searcher.search_arxiv(
            keywords=["Kimi", "K2"],
            date_range="20250101-20251231"
        )
        self.assertIsInstance(results, list)


if __name__ == "__main__":
    unittest.main()
