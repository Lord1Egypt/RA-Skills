"""
测试 CLI 模块
"""

import unittest
import tempfile
import shutil
import sys
import os
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from skill_evolver.cli import main


class TestCLI(unittest.TestCase):
    """CLI 命令测试"""
    
    def setUp(self):
        """创建临时目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
    
    def tearDown(self):
        """清理临时目录"""
        os.chdir(self.original_cwd)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_help(self):
        """测试帮助命令"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = ["skill-evolver", "--help"]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("Skill Evolver", output)
        self.assertIn("analyze", output)
        self.assertIn("report", output)
        self.assertIn("health", output)
    
    def test_version(self):
        """测试版本命令"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = ["skill-evolver", "--version"]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("0.1.0", output)
    
    def test_init_command(self):
        """测试 init 命令"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = ["skill-evolver", "init"]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("数据库已初始化", output)
    
    def test_log_command(self):
        """测试 log 命令"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = [
                "skill-evolver", "log",
                "test-skill", "test-action",
                "--status", "success",
                "--duration", "100"
            ]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("已记录技能使用", output)
    
    def test_log_list_command(self):
        """测试 log --list 命令"""
        # 先记录一条
        sys.argv = [
            "skill-evolver", "log",
            "test-skill", "test-action"
        ]
        try:
            main()
        except SystemExit:
            pass
        
        # 列出所有
        with redirect_stdout(StringIO()) as f:
            sys.argv = ["skill-evolver", "log", "--list"]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("已记录的技能", output)
    
    def test_feedback_command(self):
        """测试 feedback 命令"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = [
                "skill-evolver", "feedback",
                "test-skill", "5",
                "--comment", "很好用"
            ]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("已添加反馈", output)
    
    def test_health_command_empty(self):
        """测试 health 命令（无数据）"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = ["skill-evolver", "health", "--all"]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        # 应该显示暂无记录或类似信息
        self.assertIn("暂无", output)
    
    def test_analyze_nonexistent(self):
        """测试 analyze 不存在的技能"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = ["skill-evolver", "analyze", "nonexistent-skill"]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("不存在", output)
    
    def test_analyze_with_temp_skill(self):
        """测试 analyze 临时技能"""
        # 创建临时技能
        skill_path = Path(self.temp_dir) / "test-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: test-skill
description: Test
---
# Test Skill
""")
        
        with redirect_stdout(StringIO()) as f:
            sys.argv = [
                "skill-evolver", "analyze",
                "test-skill",
                "--skills-dir", self.temp_dir
            ]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("test-skill", output)
        self.assertIn("评分", output)
    
    def test_report_command(self):
        """测试 report 命令"""
        # 创建临时技能
        skill_path = Path(self.temp_dir) / "test-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: test-skill
description: Test
---
# Test Skill
""")
        
        # 先记录一些使用数据
        sys.argv = [
            "skill-evolver", "log",
            "test-skill", "test",
            "--status", "success"
        ]
        try:
            main()
        except SystemExit:
            pass
        
        output_path = Path(self.temp_dir) / "report.json"
        
        with redirect_stdout(StringIO()) as f:
            sys.argv = [
                "skill-evolver", "report",
                "test-skill",
                "--skills-dir", self.temp_dir,
                "-o", str(output_path),
                "-f", "json"
            ]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("健康度报告", output)
        self.assertIn("已导出", output)
        
        # 验证文件已创建
        self.assertTrue(output_path.exists())
    
    def test_clear_command(self):
        """测试 clear 命令"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = ["skill-evolver", "clear", "--days", "30"]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("已清理", output)
    
    def test_no_command_shows_help(self):
        """测试无命令时显示帮助"""
        with redirect_stdout(StringIO()) as f:
            sys.argv = ["skill-evolver"]
            try:
                main()
            except SystemExit:
                pass
        
        output = f.getvalue()
        self.assertIn("usage", output.lower())
    
    def test_invalid_command(self):
        """测试无效命令"""
        with redirect_stderr(StringIO()) as f:
            sys.argv = ["skill-evolver", "invalid-command"]
            try:
                main()
            except SystemExit as e:
                self.assertNotEqual(e.code, 0)
        
        output = f.getvalue()
        self.assertIn("invalid-command", output)


if __name__ == "__main__":
    unittest.main()
