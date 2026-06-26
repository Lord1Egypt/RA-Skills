#!/usr/bin/env python3
"""
memory_access_log_test.py - memory_access_log.py 单元测试
"""

import os
import sys
import tempfile
import shutil
import io

# Windows GBK 环境支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from memory_access_log import (
    get_db_path,
    init_access_db,
    log_access,
    get_access_stats,
    set_manual_importance,
    calculate_importance_score,
)


class TestAccessLogDatabase:
    """测试访问日志数据库"""

    def setup_method(self):
        """每个测试前创建临时目录和数据库"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = get_db_path(self.temp_dir)
        self.conn = init_access_db(self.db_path)

    def teardown_method(self):
        """每个测试后清理"""
        if self.conn:
            self.conn.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_access_db(self):
        """init_access_db 应创建正确的表"""
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in c.fetchall()]
        assert "memory_access_log" in tables
        assert "manual_importance" in tables

    def test_log_access(self):
        """log_access 应记录访问"""
        log_access(self.db_path, "chunk_123", "test_user", "read")

        stats = get_access_stats(self.db_path, "test_user", ["chunk_123"])
        assert "chunk_123" in stats
        assert stats["chunk_123"]["access_count"] == 1

    def test_get_access_stats_multiple(self):
        """应正确统计多次访问"""
        for _ in range(5):
            log_access(self.db_path, "chunk_multi", "test_user", "read")

        stats = get_access_stats(self.db_path, "test_user", ["chunk_multi"])
        assert stats["chunk_multi"]["access_count"] == 5

    def test_set_manual_importance(self):
        """应能设置手动重要性"""
        set_manual_importance(self.db_path, "chunk_imp", "test_user", 95, "重要项目")

        score = calculate_importance_score(
            self.db_path, "test_user", "chunk_imp", "L1"
        )
        assert score > 50, "手动设置的重要性应超过基础分 50"

    def test_importance_score_formula(self):
        """重要性评分公式应在 [0, 100] 范围内"""
        # 无访问记录时，基础分 + L1 默认重要性
        score = calculate_importance_score(self.db_path, "new_user", "new_chunk", "L1")
        assert 0 <= score <= 100, f"分数 {score} 应在 [0, 100] 范围内"

        # L3 默认最高
        score_l3 = calculate_importance_score(self.db_path, "new_user", "new_chunk", "L3")
        assert score_l3 >= score, "L3 默认重要性应 >= L1"


def run_tests():
    """运行所有测试"""
    print("🧪 Running memory_access_log.py unit tests...\n")

    test_classes = [TestAccessLogDatabase]

    passed = 0
    failed = 0

    for test_class in test_classes:
        print(f"📁 {test_class.__name__}")
        instance = test_class()

        for name in dir(instance):
            if name.startswith("test_"):
                if name.startswith("test_") and name != "test_class":
                    if hasattr(instance, "setup_method"):
                        try:
                            instance.setup_method()
                        except Exception as e:
                            print(f"  ❌ {name}: Setup failed: {e}")
                            failed += 1
                            continue

                    try:
                        getattr(instance, name)()
                        print(f"  ✅ {name}")
                        passed += 1
                    except AssertionError as e:
                        print(f"  ❌ {name}: {e}")
                        failed += 1
                    except Exception as e:
                        print(f"  ❌ {name}: Unexpected error: {e}")
                        failed += 1
                    finally:
                        if hasattr(instance, "teardown_method"):
                            try:
                                instance.teardown_method()
                            except Exception:
                                pass

        print()

    print(f"📊 Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
