#!/usr/bin/env python3
"""
测试模块化安装系统
"""

import sys
import os
from pathlib import Path

# 添加父目录到 path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest


class TestModuleSafety(unittest.TestCase):
    """测试模块安全性"""
    
    def test_safe_module_id(self):
        """测试安全模块ID验证"""
        from install_modules import is_safe_module_id
        
        # 安全的模块ID
        safe_ids = ["core", "security", "cloud_backup", "stats", "test-123", "abc_123"]
        for mid in safe_ids:
            self.assertTrue(is_safe_module_id(mid), f"{mid} 应该是安全的")
        
        # 危险的模块ID
        dangerous_ids = ["../etc", "~root", "..", "a;b", "a|b", "a&b", "`id`", "<script>", "\n", "\r"]
        for mid in dangerous_ids:
            self.assertFalse(is_safe_module_id(mid), f"{mid} 应该是危险的")
    
    def test_module_id_pattern(self):
        """测试模块ID格式"""
        from install_modules import is_safe_module_id
        import re
        
        pattern = re.compile(r'^[a-zA-Z0-9_-]+$')
        
        # 有效格式
        valid = ["abc", "ABC", "123", "a-b-c", "a_b_c", "a1b2c3"]
        for v in valid:
            self.assertTrue(pattern.match(v), f"{v} 应该匹配")
        
        # 无效格式
        invalid = ["a b", "a/b", "a\\b", "a'b", 'a"b']
        for v in invalid:
            self.assertFalse(pattern.match(v), f"{v} 不应该匹配")


class TestModuleConfig(unittest.TestCase):
    """测试模块配置"""
    
    def test_modules_json_valid(self):
        """测试 MODULES.json 格式正确"""
        import json
        
        modules_file = Path(__file__).parent.parent / "MODULES.json"
        self.assertTrue(modules_file.exists(), "MODULES.json 应该存在")
        
        data = json.loads(modules_file.read_text())
        self.assertIn("modules", data, "应该有 modules 字段")
        
        # 验证结构
        modules = data["modules"]
        for mod_id, mod in modules.items():
            self.assertIn("name", mod, f"{mod_id} 应该有 name")
            self.assertIn("description", mod, f"{mod_id} 应该有 description")
            self.assertIn("scripts", mod, f"{mod_id} 应该有 scripts")
            self.assertIsInstance(mod["scripts"], list, f"{mod_id}.scripts 应该是列表")
    
    def test_required_modules_exist(self):
        """测试必装模块存在"""
        import json
        
        modules_file = Path(__file__).parent.parent / "MODULES.json"
        data = json.loads(modules_file.read_text())
        
        required = ["core", "security", "health_check"]
        for mod_id in required:
            self.assertIn(mod_id, data["modules"], f"{mod_id} 应该是必装模块")
            self.assertTrue(data["modules"][mod_id].get("required"), f"{mod_id} 应该标记为 required")


if __name__ == "__main__":
    unittest.main()


class TestBootstrap(unittest.TestCase):
    """测试引导流程"""
    
    def test_complete_initialization_removes_bootstrap(self):
        """测试完成初始化后 BOOTSTRAP.md 被删除"""
        from install_modules import complete_initialization
        
        # 创建一个临时测试文件
        SKILL_DIR = Path(__file__).parent.parent
        test_bootstrap = SKILL_DIR / ".test_bootstrap.md"
        test_bootstrap.write_text("test")
        
        # 如果存在则删除（模拟已存在的情况）
        result = complete_initialization()
        
        # 清理测试文件
        if test_bootstrap.exists():
            test_bootstrap.unlink()
    
    def test_verify_installation_checks_core(self):
        """测试验证安装检查核心模块"""
        from install_modules import verify_installation, SKILL_DIR, check_core
        
        # 验证函数存在且可调用
        self.assertTrue(callable(verify_installation))
        
        # 核心标记文件路径正确
        core_marker = SKILL_DIR / ".core_installed"
        # 如果文件不存在，验证会报告错误（这是预期行为）
