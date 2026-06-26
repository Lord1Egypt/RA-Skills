#!/usr/bin/env python3
"""
端到端测试 - 验证完整安装和运行流程
"""

import sys
import os
from pathlib import Path

# 添加父目录到 path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import unittest


class TestE2EInstallation(unittest.TestCase):
    """端到端安装测试"""
    
    def test_01_core_files_exist(self):
        """测试核心文件存在"""
        skill_dir = Path(__file__).parent.parent
        
        required = [
            "MODULES.json",
            "install_modules.py",
            "migrate.py",
            "WELCOME.py",
            "BOOTSTRAP.md",
            "SKILL.md",
            "publish.sh",
        ]
        
        for f in required:
            path = skill_dir / f
            self.assertTrue(path.exists(), f"{f} 应该存在")
    
    def test_02_modules_json_valid(self):
        """测试模块配置有效"""
        import json
        
        skill_dir = Path(__file__).parent.parent
        modules_file = skill_dir / "MODULES.json"
        
        data = json.loads(modules_file.read_text())
        self.assertIn("modules", data)
        
        # 检查必装模块
        required = ["core", "security", "health_check"]
        for mod_id in required:
            self.assertIn(mod_id, data["modules"])
            self.assertTrue(data["modules"][mod_id].get("required"))
    
    def test_03_install_functions_exist(self):
        """测试安装函数存在"""
        from install_modules import (
            is_safe_module_id,
            verify_installation,
            install_module,
            full_install
        )
        
        self.assertTrue(callable(is_safe_module_id))
        self.assertTrue(callable(verify_installation))
        self.assertTrue(callable(install_module))
        self.assertTrue(callable(full_install))
    
    def test_04_safe_module_id_validation(self):
        """测试模块ID安全验证"""
        from install_modules import is_safe_module_id
        
        # 有效ID
        self.assertTrue(is_safe_module_id("core"))
        self.assertTrue(is_safe_module_id("cloud_backup"))
        self.assertTrue(is_safe_module_id("stats"))
        
        # 无效ID
        self.assertFalse(is_safe_module_id("../etc"))
        self.assertFalse(is_safe_module_id(".."))
        self.assertFalse(is_safe_module_id(""))
    
    def test_05_memory_accessible(self):
        """测试记忆目录可访问"""
        memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
        
        if memory_dir.exists():
            self.assertTrue(memory_dir.is_dir())
    
    def test_06_database_accessible(self):
        """测试数据库可访问"""
        db_path = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
        
        if db_path.exists():
            self.assertTrue(db_path.is_file())


class TestE2EModuleIntegrity(unittest.TestCase):
    """端到端模块完整性测试"""
    
    def test_all_modules_have_scripts(self):
        """测试所有模块都有脚本"""
        import json
        
        skill_dir = Path(__file__).parent.parent
        modules_file = skill_dir / "MODULES.json"
        
        data = json.loads(modules_file.read_text())
        scripts_dir = skill_dir / "scripts"
        
        for mod_id, mod in data["modules"].items():
            scripts = mod.get("scripts", [])
            self.assertGreater(len(scripts), 0, f"{mod_id} 应该有脚本")
            
            for script in scripts:
                script_path = scripts_dir / f"{script}.py"
                self.assertTrue(script_path.exists(), 
                    f"{mod_id}.{script} 应该存在于 scripts/ 目录")


class TestE2ESecurity(unittest.TestCase):
    """端到端安全测试"""
    
    def test_no_hardcoded_secrets(self):
        """测试没有硬编码的密钥"""
        import re
        
        skill_dir = Path(__file__).parent.parent
        scripts_dir = skill_dir / "scripts"
        
        secret_patterns = [
            r'api[_-]?key["\']?\s*[:=]\s*["\'][A-Za-z0-9]{32,}',
            r'secret["\']?\s*[:=]\s*["\'][A-Za-z0-9]{32,}',
            r'password["\']?\s*[:=]\s*["\'][A-Za-z0-9]{20,}',
        ]
        
        violations = []
        
        for script in scripts_dir.glob("*.py"):
            if script.name in ["test_e2e.py", "test_install_modules.py"]:
                continue
                
            content = script.read_text()
            for pattern in secret_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    violations.append(f"{script.name}: matched {pattern}")
        
        self.assertEqual(len(violations), 0, 
            f"不应该有硬编码密钥: {violations}")
    
    def test_script_safety_check_exists(self):
        """测试脚本安全检查函数存在"""
        from install_modules import verify_script_safety
        self.assertTrue(callable(verify_script_safety))


if __name__ == "__main__":
    loader = unittest.TestLoader()
    
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestE2EInstallation))
    suite.addTests(loader.loadTestsFromTestCase(TestE2EModuleIntegrity))
    suite.addTests(loader.loadTestsFromTestCase(TestE2ESecurity))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
