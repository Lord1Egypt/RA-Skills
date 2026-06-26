#!/usr/bin/env python3
"""测试 compress_session 模块"""
import unittest
import sys
import os
import tempfile
import json

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# 模拟环境变量，避免实际调用 API
os.environ['TOKEN_OPTIMIZER_API_KEY'] = 'test-key'
os.environ['TOKEN_OPTIMIZER_MODEL'] = 'gpt-4'

from compress_session import load_openclaw_config, check_dependencies


class TestCompressSession(unittest.TestCase):
    """compress_session 测试类"""

    def test_load_config_defaults(self):
        """测试默认配置加载"""
        config = load_openclaw_config()
        self.assertIn('memory_dir', config)
        self.assertIn('max_tokens', config)
        self.assertEqual(config['max_tokens'], 1500)
    
    def test_load_config_env_override(self):
        """测试环境变量覆盖"""
        os.environ['TOKEN_OPTIMIZER_API_KEY'] = 'test-key-override'
        config = load_openclaw_config()
        self.assertEqual(config['api_key'], 'test-key-override')
        # 清理
        del os.environ['TOKEN_OPTIMIZER_API_KEY']
    
    def test_check_dependencies(self):
        """测试依赖检查"""
        # openai 可能未安装，检查是否能正确处理
        try:
            import openai
            check_dependencies()  # 如果已安装，应该通过
        except ImportError:
            pass  # 如果未安装，跳过测试


class TestConfigFile(unittest.TestCase):
    """配置文件测试"""

    def test_config_structure(self):
        """测试配置结构"""
        config = load_openclaw_config()
        # 验证必需字段
        self.assertIn('memory_dir', config)
        self.assertIn('max_tokens', config)
        self.assertIn('max_chars', config)


class TestPathExpansion(unittest.TestCase):
    """路径展开测试"""

    def test_memory_dir_expansion(self):
        """测试 memory_dir 路径展开"""
        config = load_openclaw_config()
        # 应该展开为绝对路径
        self.assertTrue(config['memory_dir'].startswith('/'))


if __name__ == '__main__':
    unittest.main()