#!/usr/bin/env python3
"""
Unit tests for skill-dependency-resolver
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from typing import List

# 添加源码到 path
import sys
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "source"))

from resolver import DependencyResolver, PackageRequirement

class TestDependencyResolver(unittest.TestCase):
    def setUp(self):
        """创建临时的技能目录"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.skills_dir = self.test_dir / "skills"
        self.skills_dir.mkdir()
    
    def tearDown(self):
        """清理"""
        shutil.rmtree(self.test_dir)
    
    def create_skill(self, name: str, requirements: List[str]) -> Path:
        """创建技能目录和 requirements.txt"""
        skill_dir = self.skills_dir / name
        skill_dir.mkdir()
        req_file = skill_dir / "requirements.txt"
        content = "\n".join(requirements) + "\n"
        req_file.write_text(content)
        return skill_dir
    
    def test_parse_simple_requirement(self):
        """测试解析单行 requirements"""
        line = "pandas>=1.3.0"
        pkg = PackageRequirement.parse(line)
        self.assertIsNotNone(pkg)
        self.assertEqual(pkg.name, "pandas")
        self.assertEqual(pkg.raw_spec, ">=1.3.0")
        self.assertIsNone(pkg.version)
    
    def test_parse_exact_version(self):
        """解析精确版本"""
        line = "numpy==1.21.0"
        pkg = PackageRequirement.parse(line)
        self.assertEqual(pkg.name, "numpy")
        self.assertEqual(pkg.version, "1.21.0")
    
    def test_scan_multiple_skills(self):
        """扫描多个技能"""
        self.create_skill("skill-a", ["pandas>=1.3.0", "numpy>=1.21.0"])
        self.create_skill("skill-b", ["pandas>=1.5.0", "requests>=2.25.0"])
        
        resolver = DependencyResolver(
            skills_dir=self.skills_dir,
            output_file=self.test_dir / "out.txt",
            strategy="auto",
            verbose=False
        )
        count = resolver.scan_skills()
        self.assertEqual(count, 2)
        self.assertEqual(len(resolver.requirements), 3)  # pandas, numpy, requests
        self.assertEqual(len(resolver.requirements['pandas']), 2)
    
    def test_detect_conflict(self):
        """检测冲突"""
        self.create_skill("skill-a", ["pandas==1.3.0"])
        self.create_skill("skill-b", ["pandas==1.5.0"])
        
        resolver = DependencyResolver(
            skills_dir=self.skills_dir,
            output_file=self.test_dir / "out.txt",
            verbose=False
        )
        resolver.scan_skills()
        conflicts = resolver.detect_conflicts()
        
        self.assertEqual(conflicts, 1)
        self.assertEqual(len(resolver.conflicts), 1)
        conflict = resolver.conflicts[0]
        self.assertEqual(conflict.package, "pandas")
        self.assertIn("1.3.0", conflict.versions)
        self.assertIn("1.5.0", conflict.versions)
    
    def test_auto_resolve_highest_version(self):
        """自动解决：选择最高版本"""
        self.create_skill("skill-a", ["pandas==1.3.0"])
        self.create_skill("skill-b", ["pandas==1.5.0"])
        self.create_skill("skill-c", ["pandas==1.8.0"])
        
        resolver = DependencyResolver(
            skills_dir=self.skills_dir,
            output_file=self.test_dir / "out.txt",
            strategy="auto",
            verbose=False
        )
        resolver.scan_skills()
        resolver.detect_conflicts()
        resolver.resolve_conflicts()
        
        conflict = resolver.conflicts[0]
        self.assertEqual(conflict.resolved, "1.8.0")
    
    def test_generate_merged_requirements(self):
        """生成合并的 requirements.txt"""
        self.create_skill("skill-a", ["pandas==1.3.0", "numpy==1.21.0"])
        self.create_skill("skill-b", ["pandas==1.5.0", "requests==2.25.0"])
        
        resolver = DependencyResolver(
            skills_dir=self.skills_dir,
            output_file=self.test_dir / "merged.txt",
            strategy="auto",
            verbose=False
        )
        report = resolver.resolve()
        
        # 检查文件存在
        output_file = Path(report['output_file'])
        self.assertTrue(output_file.exists())
        
        content = output_file.read_text()
        lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith('#')]
        
        # pandas 应解决到最高版本 1.5.0
        self.assertIn("pandas==1.5.0", lines)
        # numpy 和 requests 应保留
        self.assertIn("numpy==1.21.0", lines)
        self.assertIn("requests==2.25.0", lines)
        
        self.assertEqual(report['conflicts_found'], 1)
        self.assertEqual(report['solutions_applied'], 1)

    def test_no_conflicts(self):
        """无冲突情况"""
        self.create_skill("skill-a", ["pandas==1.5.0"])
        self.create_skill("skill-b", ["numpy==1.21.0"])
        
        resolver = DependencyResolver(
            skills_dir=self.skills_dir,
            output_file=self.test_dir / "out.txt",
            verbose=False
        )
        report = resolver.resolve()
        
        self.assertEqual(report['conflicts_found'], 0)
        self.assertEqual(report['solutions_applied'], 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)