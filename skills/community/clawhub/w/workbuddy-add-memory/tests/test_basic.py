#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy智能记忆管理系统基础测试
作者: zcg007
日期: 2026-03-15
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# 添加技能目录到Python路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))


class TestConfigLoader(unittest.TestCase):
    """配置加载器测试"""
    
    def setUp(self):
        from config_loader import ConfigLoader
        self.loader = ConfigLoader()
    
    def test_load_default_config(self):
        """测试加载默认配置"""
        config = self.loader.load_config()
        
        self.assertIn("memory_sources", config)
        self.assertIn("retrieval_config", config)
        self.assertIn("detection_config", config)
        
        self.assertIsInstance(config["memory_sources"], list)
        self.assertIsInstance(config["retrieval_config"], dict)
    
    def test_get_memory_sources(self):
        """测试获取记忆源"""
        sources = self.loader.get_memory_sources()
        self.assertIsInstance(sources, list)
    
    def test_get_retrieval_config(self):
        """测试获取检索配置"""
        config = self.loader.get_retrieval_config()
        self.assertIsInstance(config, dict)
        self.assertIn("max_results", config)
        self.assertIn("min_relevance", config)


class TestTaskDetector(unittest.TestCase):
    """任务检测器测试"""
    
    def setUp(self):
        from task_detector import TaskDetector
        self.detector = TaskDetector()
    
    def test_detect_excel_task(self):
        """测试检测Excel任务"""
        result = self.detector.detect_task("制作Excel预算表")
        
        self.assertIn("primary_task", result)
        self.assertIn("confidence", result)
        self.assertIn("keywords_found", result)
        
        # 应该检测到Excel任务
        self.assertEqual(result["primary_task"], "excel")
        self.assertGreater(result["confidence"], 0.3)
    
    def test_detect_skill_task(self):
        """测试检测技能任务"""
        result = self.detector.detect_task("安装新技能")
        
        self.assertEqual(result["primary_task"], "skill")
        self.assertGreater(result["confidence"], 0.3)
    
    def test_detect_question_intent(self):
        """测试检测问题意图"""
        result = self.detector.detect_task("如何安装技能？")
        
        self.assertEqual(result["intent"], "question")
        self.assertGreater(result["confidence"], 0.3)


class TestMemoryRetriever(unittest.TestCase):
    """记忆检索器测试"""
    
    def setUp(self):
        from memory_retriever import MemoryRetriever
        self.retriever = MemoryRetriever()
        
        # 添加测试记忆
        self.test_memories = [
            {
                "id": "test1",
                "title": "Excel处理关键经验",
                "content": "处理Excel文件时，必须保留公式，使用openpyxl的data_only=False参数。",
                "clean_content": "处理Excel文件时，必须保留公式，使用openpyxl的data_only=False参数。",
                "importance": "important",
                "category": "excel",
                "keywords": ["excel", "公式", "openpyxl", "处理"],
            },
            {
                "id": "test2",
                "title": "技能安装原则",
                "content": "所有skill都必须通过SkillHub下载，这是不可违反的核心技能管理原则。",
                "clean_content": "所有skill都必须通过SkillHub下载，这是不可违反的核心技能管理原则。",
                "importance": "critical",
                "category": "skill",
                "keywords": ["skill", "SkillHub", "安装", "原则"],
            },
        ]
        
        for memory in self.test_memories:
            self.retriever._add_memory(memory)
    
    def test_add_memory(self):
        """测试添加记忆"""
        initial_count = len(self.retriever.memory_data)
        
        new_memory = {
            "id": "test3",
            "title": "测试记忆",
            "content": "测试内容",
            "clean_content": "测试内容",
            "importance": "normal",
            "category": "test",
            "keywords": ["测试"],
        }
        
        self.retriever._add_memory(new_memory)
        
        self.assertEqual(len(self.retriever.memory_data), initial_count + 1)
    
    def test_build_index(self):
        """测试构建索引"""
        success = self.retriever.build_index()
        
        self.assertTrue(success)
        self.assertTrue(self.retriever.is_indexed)
        self.assertIsNotNone(self.retriever.memory_vectors)


class TestWorkPreparation(unittest.TestCase):
    """工作准备测试"""
    
    def setUp(self):
        from work_preparation import WorkPreparation
        
        # 创建临时工作空间
        self.temp_dir = Path("/tmp/test_work_preparation")
        if self.temp_dir.exists():
            import shutil
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True)
        
        self.preparer = WorkPreparation(self.temp_dir)
    
    def tearDown(self):
        # 清理临时目录
        if self.temp_dir.exists():
            import shutil
            shutil.rmtree(self.temp_dir)
    
    def test_analyze_task(self):
        """测试任务分析"""
        task_description = "制作Excel预算表"
        analysis = self.preparer._analyze_task(task_description)
        
        self.assertIn("primary_task_type", analysis)
        self.assertIn("complexity", analysis)
        self.assertIn("estimated_time", analysis)
        
        self.assertEqual(analysis["primary_task_type"], "excel")
    
    def test_assess_complexity(self):
        """测试复杂度评估"""
        task_description = "制作复杂的Excel预算表"
        
        # 模拟任务检测结果
        mock_detection = {
            "primary_task": "excel",
            "keywords_found": [
                {"keyword": "Excel", "task_type": "excel"},
                {"keyword": "预算表", "task_type": "excel"},
                {"keyword": "复杂", "task_type": "excel"},
            ],
        }
        
        complexity = self.preparer._assess_complexity(task_description, mock_detection)
        
        self.assertIn(complexity, ["low", "medium", "high"])
    
    def test_check_workspace(self):
        """测试检查工作空间"""
        workspace_info = self.preparer._check_workspace()
        
        self.assertIn("path", workspace_info)
        self.assertIn("exists", workspace_info)
        self.assertIn("is_writable", workspace_info)
        
        self.assertTrue(workspace_info["exists"])
        self.assertTrue(workspace_info["is_writable"])


class TestConversationHook(unittest.TestCase):
    """对话钩子测试"""
    
    def setUp(self):
        from conversation_hook import ConversationHook
        
        # 模拟配置
        mock_config = {
            "memory_sources": ["/tmp/test_memories"],
            "retrieval_config": {"max_results": 5, "min_relevance": 0.3},
            "detection_config": {
                "task_keywords": {
                    "excel": ["excel", "表格", "报表"],
                    "skill": ["技能", "skill", "安装"],
                },
                "min_confidence": 0.3,
                "context_window": 5,
            },
        }
        
        self.hook = ConversationHook(mock_config)
    
    def test_detect_trigger_new_task(self):
        """测试检测新任务触发"""
        message = "请帮我制作Excel预算表"
        
        result = self.hook._detect_trigger(message)
        
        self.assertIn("triggered", result)
        self.assertIn("type", result)
        self.assertIn("confidence", result)
        
        if result["triggered"]:
            self.assertEqual(result["type"], "new_task")
            self.assertGreater(result["confidence"], 0.3)
    
    def test_detect_trigger_question(self):
        """测试检测问题触发"""
        message = "如何安装技能？"
        
        result = self.hook._detect_trigger(message)
        
        if result["triggered"]:
            self.assertEqual(result["type"], "question")
            self.assertGreater(result["confidence"], 0.3)
    
    def test_format_memories(self):
        """测试格式化记忆"""
        test_memories = [
            {
                "title": "测试记忆1",
                "relevance_score": 0.8,
                "category": "test",
                "importance": "normal",
                "content": "测试内容1",
            },
            {
                "title": "测试记忆2",
                "relevance_score": 0.6,
                "category": "test",
                "importance": "important",
                "content": "测试内容2",
            },
        ]
        
        formatted = self.hook._format_memories(test_memories)
        
        self.assertIsInstance(formatted, str)
        self.assertIn("测试记忆1", formatted)
        self.assertIn("测试记忆2", formatted)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTest(unittest.makeSuite(TestConfigLoader))
    suite.addTest(unittest.makeSuite(TestTaskDetector))
    suite.addTest(unittest.makeSuite(TestMemoryRetriever))
    suite.addTest(unittest.makeSuite(TestWorkPreparation))
    suite.addTest(unittest.makeSuite(TestConversationHook))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("WorkBuddy智能记忆管理系统 v3.0 - 单元测试")
    print("=" * 60)
    
    result = run_tests()
    
    print("\n" + "=" * 60)
    print("测试统计:")
    print(f"  运行测试: {result.testsRun}")
    print(f"  通过测试: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  失败测试: {len(result.failures)}")
    print(f"  错误测试: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)