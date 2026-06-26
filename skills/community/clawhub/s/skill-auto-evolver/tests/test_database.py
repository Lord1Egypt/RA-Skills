"""
测试数据库模型
"""

import unittest
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path

# 添加父目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.models import Database, SkillUsage, HealthScore, Feedback


class TestDatabase(unittest.TestCase):
    """数据库模型测试"""
    
    def setUp(self):
        """创建临时数据库"""
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.db = Database(self.temp_file.name)
    
    def tearDown(self):
        """清理临时文件"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_init_creates_tables(self):
        """测试数据库初始化创建表"""
        # 应该能正常执行查询
        skills = self.db.get_all_skills()
        self.assertIsInstance(skills, list)
    
    def test_log_usage(self):
        """测试记录技能使用"""
        usage = SkillUsage(
            skill_name="test-skill",
            action="test_action",
            status="success",
            duration_ms=100
        )
        usage_id = self.db.log_usage(usage)
        
        self.assertIsNotNone(usage_id)
        self.assertGreater(usage_id, 0)
    
    def test_get_usage_stats(self):
        """测试获取使用统计"""
        # 插入测试数据
        for i in range(5):
            usage = SkillUsage(
                skill_name="test-skill",
                action="test",
                status="success" if i < 4 else "failed",
                duration_ms=100 + i * 10
            )
            self.db.log_usage(usage)
        
        stats = self.db.get_usage_stats("test-skill")
        
        self.assertEqual(stats["total"], 5)
        self.assertEqual(stats["success"], 4)
        self.assertEqual(stats["failed"], 1)
        self.assertEqual(stats["avg_duration_ms"], 120.0)
    

    def test_get_usage_stats_rejects_non_integer_days(self):
        """Reject non-integer day windows before SQL execution."""
        with self.assertRaises(ValueError):
            self.db.get_usage_stats("test-skill", "1); DROP TABLE skill_usage; --")

        # The table should still be usable after the rejected input.
        self.assertEqual(self.db.get_usage_stats("test-skill")["total"], 0)

    def test_update_health_score(self):
        """测试更新健康度评分"""
        score = HealthScore(
            skill_name="test-skill",
            success_rate=95.0,
            avg_duration_ms=150.0,
            usage_count=100,
            score=85,
            issues=["建议优化性能"]
        )
        score_id = self.db.update_health_score(score)
        
        self.assertIsNotNone(score_id)
        
        # 验证可以读取
        retrieved = self.db.get_health_score("test-skill")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.skill_name, "test-skill")
        self.assertEqual(retrieved.score, 85)
    
    def test_add_feedback(self):
        """测试添加反馈"""
        feedback = Feedback(
            skill_name="test-skill",
            rating=5,
            comment="很好用！",
            user_id="user123"
        )
        feedback_id = self.db.add_feedback(feedback)
        
        self.assertIsNotNone(feedback_id)
        
        # 验证反馈统计
        stats = self.db.get_feedback_stats("test-skill")
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["avg_rating"], 5.0)
    
    def test_get_all_skills(self):
        """测试获取所有技能"""
        # 插入不同技能的数据
        skills_data = [
            SkillUsage(skill_name="skill-a", action="test", status="success"),
            SkillUsage(skill_name="skill-b", action="test", status="success"),
            SkillUsage(skill_name="skill-c", action="test", status="success"),
        ]
        
        for usage in skills_data:
            self.db.log_usage(usage)
        
        all_skills = self.db.get_all_skills()
        
        self.assertEqual(len(all_skills), 3)
        self.assertIn("skill-a", all_skills)
        self.assertIn("skill-b", all_skills)
        self.assertIn("skill-c", all_skills)
    
    def test_clear_old_data(self):
        """测试清理旧数据"""
        # 插入一条旧数据
        old_usage = SkillUsage(
            skill_name="old-skill",
            action="test",
            status="success",
            timestamp=datetime.now() - timedelta(days=100)
        )
        self.db.log_usage(old_usage)
        
        # 插入一条新数据
        new_usage = SkillUsage(
            skill_name="new-skill",
            action="test",
            status="success"
        )
        self.db.log_usage(new_usage)
        
        # 清理 90 天前的数据
        self.db.clear_old_data(90)
        
        # 验证旧数据被清理
        all_skills = self.db.get_all_skills()
        self.assertIn("new-skill", all_skills)
        # 旧技能应该被清理了
        old_stats = self.db.get_usage_stats("old-skill")
        self.assertEqual(old_stats["total"], 0)


    def test_clear_old_data_rejects_non_integer_days(self):
        """Reject unsafe cleanup windows before SQL execution."""
        with self.assertRaises(ValueError):
            self.db.clear_old_data("90); DROP TABLE feedback; --")

        self.assertIsInstance(self.db.get_all_skills(), list)


class TestSkillUsage(unittest.TestCase):
    """SkillUsage 数据类测试"""
    
    def test_create_with_defaults(self):
        """测试创建带默认值的实例"""
        usage = SkillUsage(skill_name="test", action="run")
        
        self.assertEqual(usage.skill_name, "test")
        self.assertEqual(usage.action, "run")
        self.assertEqual(usage.status, "")
        self.assertEqual(usage.duration_ms, 0)
        self.assertIsNone(usage.context)
    
    def test_create_with_all_fields(self):
        """测试创建完整实例"""
        usage = SkillUsage(
            id=1,
            skill_name="test",
            action="run",
            status="success",
            duration_ms=100,
            context={"key": "value"},
            error_message=None
        )
        
        self.assertEqual(usage.id, 1)
        self.assertEqual(usage.context, {"key": "value"})


class TestHealthScore(unittest.TestCase):
    """HealthScore 数据类测试"""
    
    def test_create_with_defaults(self):
        """测试创建带默认值的实例"""
        score = HealthScore(skill_name="test")
        
        self.assertEqual(score.skill_name, "test")
        self.assertEqual(score.success_rate, 0.0)
        self.assertEqual(score.score, 0)
    
    def test_create_with_issues_list(self):
        """测试创建带问题列表的实例"""
        score = HealthScore(
            skill_name="test",
            score=80,
            issues=["问题 1", "问题 2"]
        )
        
        self.assertEqual(score.issues, ["问题 1", "问题 2"])


if __name__ == "__main__":
    unittest.main()
