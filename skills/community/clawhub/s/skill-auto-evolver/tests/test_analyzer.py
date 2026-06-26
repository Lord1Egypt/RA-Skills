"""
测试代码分析模块
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import os

# 添加父目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from skill_evolver.analyzer import SkillAnalyzer, AnalysisIssue, SkillAnalysisResult


class TestSkillAnalyzer(unittest.TestCase):
    """技能分析器测试"""
    
    def setUp(self):
        """创建临时技能目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.analyzer = SkillAnalyzer(self.temp_dir)
    
    def tearDown(self):
        """清理临时目录"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_analyze_nonexistent_skill(self):
        """测试分析不存在的技能"""
        result = self.analyzer.analyze_skill("nonexistent")
        
        self.assertFalse(result.exists)
        self.assertEqual(result.score, 0)
        self.assertTrue(any(i.severity == "critical" for i in result.issues))
    
    def test_analyze_empty_directory(self):
        """测试分析空目录"""
        skill_path = Path(self.temp_dir) / "empty-skill"
        skill_path.mkdir()
        
        result = self.analyzer.analyze_skill("empty-skill")
        
        self.assertTrue(result.exists)
        self.assertFalse(result.has_skill_md)
        self.assertFalse(result.has_package_json)
        self.assertLess(result.score, 50)
    
    def test_analyze_complete_skill(self):
        """测试分析完整的技能"""
        skill_path = Path(self.temp_dir) / "complete-skill"
        skill_path.mkdir()
        
        # 创建 SKILL.md
        skill_md = skill_path / "SKILL.md"
        skill_md.write_text("""---
name: complete-skill
description: 一个完整的技能
---

# Complete Skill

这是一个完整的技能示例。

## 使用方法

```python
from skill import do_something
do_something()
```
""")
        
        # 创建 package.json
        package_json = skill_path / "package.json"
        package_json.write_text("""{
    "name": "complete-skill",
    "version": "1.0.0",
    "description": "A complete skill"
}
""")
        
        result = self.analyzer.analyze_skill("complete-skill")
        
        self.assertTrue(result.exists)
        self.assertTrue(result.has_skill_md)
        self.assertTrue(result.has_package_json)
        self.assertTrue(result.skill_md_valid)
        self.assertGreater(result.score, 70)
    
    def test_analyze_invalid_yaml(self):
        """测试分析 YAML 格式错误的 SKILL.md"""
        skill_path = Path(self.temp_dir) / "invalid-yaml"
        skill_path.mkdir()
        
        skill_md = skill_path / "SKILL.md"
        skill_md.write_text("""---
name: invalid
description: [unclosed bracket
---

Content
""")
        
        result = self.analyzer.analyze_skill("invalid-yaml")
        
        self.assertTrue(result.has_skill_md)
        self.assertFalse(result.skill_md_valid)
        self.assertTrue(any(
            "YAML" in i.message or "解析" in i.message
            for i in result.issues
        ))
    
    def test_analyze_invalid_json(self):
        """测试分析 JSON 格式错误的 package.json"""
        skill_path = Path(self.temp_dir) / "invalid-json"
        skill_path.mkdir()
        
        skill_md = skill_path / "SKILL.md"
        skill_md.write_text("""---
name: test
description: test
---
""")
        
        package_json = skill_path / "package.json"
        package_json.write_text("""{
    "name": "invalid",
    "version": invalid
}
""")
        
        result = self.analyzer.analyze_skill("invalid-json")
        
        self.assertTrue(result.has_package_json)
        self.assertTrue(any(
            "JSON" in i.message or "解析" in i.message
            for i in result.issues
        ))
    
    def test_analyze_python_syntax_error(self):
        """测试分析 Python 语法错误"""
        skill_path = Path(self.temp_dir) / "syntax-error"
        skill_path.mkdir()
        
        # 创建有语法错误的 Python 文件
        py_file = skill_path / "main.py"
        py_file.write_text("""
def broken_function(
    # Missing closing parenthesis and colon
    print("hello"
""")
        
        result = self.analyzer.analyze_skill("syntax-error")
        
        self.assertTrue(any(
            i.severity == "critical" and "语法" in i.message
            for i in result.issues
        ))
    
    def test_analyze_code_quality_issues(self):
        """测试分析代码质量问题"""
        skill_path = Path(self.temp_dir) / "quality-issues"
        skill_path.mkdir()
        
        # 创建有质量问题的 Python 文件
        py_file = skill_path / "code.py"
        py_file.write_text("""
# TODO: fix this later
def test():
    x = 1
    try:
        risky_operation()
    except:  # bare except
        pass
    print("done")  # print statement
""")
        
        result = self.analyzer.analyze_skill("quality-issues")
        
        # 应该检测到 TODO、bare except、print
        categories = [i.category for i in result.issues]
        self.assertIn("style", categories)
        self.assertIn("content", categories)
    
    def test_calculate_score(self):
        """测试评分计算"""
        # 创建一个问题较多的技能
        skill_path = Path(self.temp_dir) / "low-score"
        skill_path.mkdir()
        
        # 只有 SKILL.md，内容很少
        skill_md = skill_path / "SKILL.md"
        skill_md.write_text("""---
name: low-score
---
Short content.
""")
        
        result = self.analyzer.analyze_skill("low-score")
        
        # 评分应该较低
        self.assertLess(result.score, 60)
    
    def test_generate_suggestions(self):
        """测试生成改进建议"""
        skill_path = Path(self.temp_dir) / "needs-improvement"
        skill_path.mkdir()
        
        result = SkillAnalysisResult(
            skill_name="needs-improvement",
            skill_path=str(skill_path),
            exists=True,
            has_skill_md=False,
            has_package_json=False,
            score=40,
            issues=[
                AnalysisIssue("critical", "structure", "缺少 SKILL.md"),
                AnalysisIssue("warning", "content", "内容不完整"),
            ]
        )
        
        suggestions = self.analyzer._generate_suggestions(result)
        
        self.assertTrue(len(suggestions) > 0)
        self.assertTrue(any("SKILL.md" in s for s in suggestions))
    
    def test_compare_skills(self):
        """测试技能对比"""
        # 创建两个技能
        for name in ["skill-a", "skill-b"]:
            skill_path = Path(self.temp_dir) / name
            skill_path.mkdir()
            
            skill_md = skill_path / "SKILL.md"
            skill_md.write_text(f"""---
name: {name}
description: Test skill
---

# {name}
""")
        
        comparison = self.analyzer.compare_skills(["skill-a", "skill-b"])
        
        self.assertIn("ranking", comparison)
        self.assertEqual(len(comparison["ranking"]), 2)
        self.assertIn("average_score", comparison)


class TestAnalysisIssue(unittest.TestCase):
    """AnalysisIssue 数据类测试"""
    
    def test_create_issue(self):
        """测试创建问题实例"""
        issue = AnalysisIssue(
            severity="warning",
            category="syntax",
            message="测试问题",
            line=10,
            suggestion="修复方法"
        )
        
        self.assertEqual(issue.severity, "warning")
        self.assertEqual(issue.line, 10)
        self.assertEqual(issue.suggestion, "修复方法")


if __name__ == "__main__":
    unittest.main()
