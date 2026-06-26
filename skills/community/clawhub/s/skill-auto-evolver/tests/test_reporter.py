"""
测试报告生成模块
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
import os

# 添加父目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.models import Database
from skill_evolver.reporter import SkillReporter
from skill_evolver.analyzer import SkillAnalyzer


class TestSkillReporter(unittest.TestCase):
    """报告生成器测试"""
    
    def setUp(self):
        """创建临时数据库和目录"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        
        self.temp_dir = tempfile.mkdtemp()
        
        self.db = Database(self.temp_db.name)
        self.reporter = SkillReporter(self.db, self.temp_dir)
    
    def tearDown(self):
        """清理临时文件"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_generate_health_report(self):
        """测试生成健康度报告"""
        # 创建测试技能
        skill_path = Path(self.temp_dir) / "test-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: test-skill
description: Test
---
# Test Skill
""")
        
        # 添加使用记录
        from database.models import SkillUsage
        for i in range(10):
            usage = SkillUsage(
                skill_name="test-skill",
                action="test",
                status="success" if i < 8 else "failed",
                duration_ms=100 + i * 10
            )
            self.db.log_usage(usage)
        
        # 添加反馈
        from database.models import Feedback
        for rating in [5, 4, 5, 3, 5]:
            feedback = Feedback(
                skill_name="test-skill",
                rating=rating
            )
            self.db.add_feedback(feedback)
        
        report = self.reporter.generate_health_report("test-skill")
        
        self.assertEqual(report["skill_name"], "test-skill")
        self.assertIn("overall_score", report)
        self.assertIn("scores", report)
        self.assertIn("usage", report)
        self.assertIn("feedback", report)
        self.assertIn("recommendations", report)
        self.assertIn("status", report)
        
        # 验证评分计算
        self.assertEqual(report["usage"]["total_calls"], 10)
        self.assertEqual(report["usage"]["success_rate"], 80.0)
        self.assertEqual(report["feedback"]["total_reviews"], 5)
        self.assertAlmostEqual(report["feedback"]["avg_rating"], 4.4, places=1)
    
    def test_generate_full_report(self):
        """测试生成完整报告"""
        # 创建多个技能
        for name in ["skill-a", "skill-b"]:
            skill_path = Path(self.temp_dir) / name
            skill_path.mkdir()
            (skill_path / "SKILL.md").write_text(f"""---
name: {name}
description: Test
---
# {name}
""")
            
            # 添加使用记录
            from database.models import SkillUsage
            for i in range(5):
                usage = SkillUsage(
                    skill_name=name,
                    action="test",
                    status="success",
                    duration_ms=100
                )
                self.db.log_usage(usage)
        
        report = self.reporter.generate_full_report()
        
        self.assertIn("summary", report)
        self.assertIn("skills", report)
        
        summary = report["summary"]
        self.assertEqual(summary["total_skills"], 2)
        self.assertIn("average_score", summary)
    
    def test_export_report_json(self):
        """测试导出 JSON 格式报告"""
        skill_path = Path(self.temp_dir) / "test-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: test-skill
---
# Test
""")
        
        report = self.reporter.generate_health_report("test-skill")
        
        output_path = Path(self.temp_dir) / "report.json"
        self.reporter.export_report(report, str(output_path), format="json")
        
        self.assertTrue(output_path.exists())
        
        with open(output_path) as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded["skill_name"], report["skill_name"])
    
    def test_export_report_markdown(self):
        """测试导出 Markdown 格式报告"""
        skill_path = Path(self.temp_dir) / "test-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: test-skill
---
# Test
""")
        
        report = self.reporter.generate_health_report("test-skill")
        
        output_path = Path(self.temp_dir) / "report.md"
        self.reporter.export_report(report, str(output_path), format="markdown")
        
        self.assertTrue(output_path.exists())
        
        content = output_path.read_text()
        self.assertIn("test-skill", content)
        self.assertIn("健康度报告", content)
    
    def test_export_report_html(self):
        """测试导出 HTML 格式报告"""
        skill_path = Path(self.temp_dir) / "test-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: test-skill
---
# Test
""")
        
        report = self.reporter.generate_health_report("test-skill")
        
        output_path = Path(self.temp_dir) / "report.html"
        self.reporter.export_report(report, str(output_path), format="html")
        
        self.assertTrue(output_path.exists())
        
        content = output_path.read_text()
        self.assertIn("<html>", content)
        self.assertIn("test-skill", content)
    
    def test_calculate_health_score(self):
        """测试健康度评分计算"""
        usage_stats = {
            "total": 100,
            "success": 90,
            "failed": 10,
            "avg_duration_ms": 200
        }
        feedback_stats = {
            "total": 10,
            "avg_rating": 4.5,
            "distribution": {5: 5, 4: 3, 3: 2, 2: 0, 1: 0}
        }
        
        from skill_evolver.analyzer import SkillAnalysisResult
        analysis = SkillAnalysisResult(
            skill_name="test",
            skill_path="/test",
            exists=True,
            has_skill_md=True,
            has_package_json=True,
            skill_md_valid=True,
            score=85
        )
        
        scores = self.reporter._calculate_health_score(
            usage_stats, feedback_stats, analysis
        )
        
        self.assertIn("overall", scores)
        self.assertIn("reliability", scores)
        self.assertIn("performance", scores)
        self.assertIn("code_quality", scores)
        self.assertIn("user_satisfaction", scores)
        
        # 可靠性应该接近 90 (90% 成功率)
        self.assertGreater(scores["reliability"], 85)
        
        # 用户满意度应该接近 90 (4.5 * 20)
        self.assertGreater(scores["user_satisfaction"], 85)
    
    def test_determine_status(self):
        """测试状态判定"""
        self.assertEqual(self.reporter._determine_status(85), "healthy")
        self.assertEqual(self.reporter._determine_status(70), "warning")
        self.assertEqual(self.reporter._determine_status(50), "critical")
    
    def test_calc_success_rate(self):
        """测试成功率计算"""
        stats = {"total": 100, "success": 85}
        rate = self.reporter._calc_success_rate(stats)
        self.assertEqual(rate, 85.0)
        
        # 零调用情况
        stats_zero = {"total": 0, "success": 0}
        rate_zero = self.reporter._calc_success_rate(stats_zero)
        self.assertEqual(rate_zero, 0.0)
    
    def test_generate_recommendations(self):
        """测试生成改进建议"""
        usage_stats = {
            "total": 100,
            "success": 70,
            "failed": 30,
            "avg_duration_ms": 6000
        }
        feedback_stats = {"avg_rating": 2.5, "total": 10}
        
        from skill_evolver.analyzer import SkillAnalysisResult, AnalysisIssue
        analysis = SkillAnalysisResult(
            skill_name="test",
            skill_path="/test",
            exists=True,
            has_skill_md=True,
            has_package_json=True,
            skill_md_valid=True,
            score=60,
            issues=[AnalysisIssue("critical", "syntax", "严重问题")]
        )
        
        recommendations = self.reporter._generate_recommendations(
            usage_stats, feedback_stats, analysis
        )
        
        self.assertTrue(len(recommendations) > 0)
        # 应该包含成功率低的建议
        self.assertTrue(any("成功率" in r for r in recommendations))
        # 应该包含性能建议
        self.assertTrue(any("响应时间" in r or "性能" in r for r in recommendations))
    
    def test_save_health_score(self):
        """测试保存健康度评分"""
        skill_path = Path(self.temp_dir) / "test-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: test-skill
---
# Test
""")
        
        report = self.reporter.generate_health_report("test-skill")
        
        # 验证评分已保存
        score = self.db.get_health_score("test-skill")
        self.assertIsNotNone(score)
        self.assertEqual(score.skill_name, "test-skill")
        self.assertEqual(score.score, report["overall_score"])


if __name__ == "__main__":
    unittest.main()
