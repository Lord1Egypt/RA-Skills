#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试 - Agent 自我学习技能
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime


class TestConfig(unittest.TestCase):
    """配置类测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        from scripts.memory_update import Config
        
        config = Config()
        self.assertEqual(config.get('backup.retain_days'), 7)
        self.assertEqual(config.get('logging.level'), 'INFO')
    
    def test_custom_config(self):
        """测试自定义配置"""
        from scripts.memory_update import Config
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
workspace:
  default: /tmp/test_ws
backup:
  retain_days: 14
""")
            f.flush()
            
            config = Config(Path(f.name))
            self.assertEqual(config.get('workspace.default'), '/tmp/test_ws')
            self.assertEqual(config.get('backup.retain_days'), 14)


class TestFileManager(unittest.TestCase):
    """文件管理类测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        
        # 创建测试文件
        (self.workspace / 'MEMORY.md').write_text('# Memory\n\nContent')
        (self.workspace / 'IDENTITY.md').write_text('# Identity\n\nContent')
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_read_core_files(self):
        """测试读取核心文件"""
        from scripts.memory_update import Config, FileManager
        
        config = Config()
        fm = FileManager(self.workspace, config)
        
        files = fm.read_core_files()
        self.assertIn('MEMORY.md', files)
        self.assertIn('IDENTITY.md', files)
    
    def test_backup_files(self):
        """测试备份文件"""
        from scripts.memory_update import Config, FileManager
        
        config = Config()
        fm = FileManager(self.workspace, config)
        
        files_content = {
            'MEMORY.md': '# Memory\n\nTest Content',
            'IDENTITY.md': '# Identity\n\nTest Content'
        }
        
        backup_dir = fm.backup_files(files_content)
        self.assertTrue(backup_dir.exists())
    
    def test_validate_file(self):
        """测试文件验证"""
        from scripts.memory_update import Config, FileManager
        
        config = Config()
        fm = FileManager(self.workspace, config)
        
        # 有效文件
        is_valid, msg = fm.validate_file(self.workspace / 'MEMORY.md')
        self.assertTrue(is_valid)
        
        # 无效文件 (空文件)
        empty_file = self.workspace / 'empty.md'
        empty_file.write_text('')
        is_valid, msg = fm.validate_file(empty_file)
        self.assertFalse(is_valid)


class TestWorkspaceDetector(unittest.TestCase):
    """工作目录检测测试"""
    
    def test_detect_with_arg(self):
        """测试命令行参数指定"""
        from scripts.memory_update import WorkspaceDetector
        
        workspace = WorkspaceDetector.detect('/tmp/test')
        self.assertEqual(str(workspace), '/tmp/test')
    
    def test_detect_with_env(self):
        """测试环境变量指定"""
        import os
        from scripts.memory_update import WorkspaceDetector
        
        os.environ['WORKSPACE'] = '/tmp/env_test'
        workspace = WorkspaceDetector.detect(None)
        self.assertEqual(str(workspace), '/tmp/env_test')
        del os.environ['WORKSPACE']


class TestAIAnalyzer(unittest.TestCase):
    """AI 分析器测试"""
    
    def test_build_prompt(self):
        """测试 prompt 构建"""
        from scripts.memory_update import AIAnalyzer, Config
        
        config = Config()
        analyzer = AIAnalyzer(config)
        
        conversation = [{'type': 'question', 'content': 'test'}]
        files_content = {'MEMORY.md': '# Memory'}
        
        prompt = analyzer._build_prompt(conversation, files_content, 'main')
        self.assertIn('Agent 信息', prompt)
        self.assertIn('对话内容', prompt)


if __name__ == '__main__':
    unittest.main()
