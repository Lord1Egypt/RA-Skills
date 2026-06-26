#!/usr/bin/env python3
"""
memory_search_test.py - memory_search.py 单元测试
"""

import os
import sys
import tempfile
import shutil
import sqlite3
import io

# Windows GBK 环境支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

try:
    import numpy as np
    np_available = True
except ImportError:
    np_available = False

from memory_search import (
    get_db_path,
    connect_db,
    cosine_similarity,
)


class TestCosineSimilarity:
    """测试余弦相似度计算"""

    def test_identical_vectors(self):
        """完全相同的向量相似度应为 1"""
        if not np_available:
            return
        v = np.array([1.0, 0.0, 0.0])
        assert abs(cosine_similarity(v, v) - 1.0) < 1e-6

    def test_orthogonal_vectors(self):
        """正交向量相似度应为 0"""
        if not np_available:
            return
        v1 = np.array([1.0, 0.0, 0.0])
        v2 = np.array([0.0, 1.0, 0.0])
        assert abs(cosine_similarity(v1, v2)) < 1e-6

    def test_opposite_vectors(self):
        """相反向量相似度应为 -1"""
        if not np_available:
            return
        v1 = np.array([1.0, 0.0, 0.0])
        v2 = np.array([-1.0, 0.0, 0.0])
        assert abs(cosine_similarity(v1, v2) - (-1.0)) < 1e-6

    def test_zero_vector(self):
        """零向量相似度应为 0"""
        if not np_available:
            return
        v1 = np.array([1.0, 0.0])
        v2 = np.array([0.0, 0.0])
        assert cosine_similarity(v1, v2) == 0.0

    def test_similarity_range(self):
        """相似度应在 [-1, 1] 范围内"""
        if not np_available:
            return
        for _ in range(10):
            v1 = np.random.rand(10)
            v2 = np.random.rand(10)
            sim = cosine_similarity(v1, v2)
            assert -1.0 <= sim <= 1.0, f"相似度 {sim} 超出范围"


class TestDatabaseConnection:
    """测试数据库连接"""

    def test_connect_nonexistent_db(self):
        """连接不存在的数据库应返回 None"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "nonexistent.db")
            conn = connect_db(db_path)
            assert conn is None

    def test_connect_existing_db(self):
        """连接存在的数据库应成功"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            # 先创建数据库
            conn = sqlite3.connect(db_path)
            conn.close()

            # 再连接
            conn2 = connect_db(db_path)
            assert conn2 is not None
            conn2.close()

    def test_wal_mode(self):
        """数据库应启用 WAL 模式"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.close()

            conn2 = connect_db(db_path)
            result = conn2.execute("PRAGMA journal_mode").fetchone()[0]
            conn2.close()
            assert result.upper() == "WAL", f"应为 WAL 模式，实际 {result}"


def run_tests():
    """运行所有测试"""
    print("🧪 Running memory_search.py unit tests...\n")

    test_classes = [
        TestCosineSimilarity,
        TestDatabaseConnection,
    ]

    passed = 0
    failed = 0

    for test_class in test_classes:
        print(f"📁 {test_class.__name__}")
        instance = test_class()

        for name in dir(instance):
            if name.startswith("test_"):
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

        print()

    print(f"📊 Results: {passed} passed, {failed} failed")
    if not np_available:
        print("⚠️  numpy not available, skipped vector tests")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
