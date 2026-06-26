#!/usr/bin/env python3
"""
memory_embed_test.py - memory_embed.py 单元测试
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

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from memory_embed import (
    make_content_hash,
    make_chunk_id,
    parse_sections,
    get_db_path,
    init_db,
    store_embedding,
    delete_embeddings,
    get_existing_records,
    safe_relpath,
)


class TestHashFunctions:
    """测试哈希函数"""

    def test_make_content_hash_deterministic(self):
        """相同内容应产生相同哈希"""
        content = "Test content"
        h1 = make_content_hash(content)
        h2 = make_content_hash(content)
        assert h1 == h2, "相同内容应产生相同哈希"

    def test_make_content_hash_different(self):
        """不同内容应产生不同哈希"""
        h1 = make_content_hash("Content A")
        h2 = make_content_hash("Content B")
        assert h1 != h2, "不同内容应产生不同哈希"

    def test_make_chunk_id_unique(self):
        """相同内容 + 不同 mtime 应产生不同 chunk_id"""
        content_hash = make_content_hash("content")
        cid1 = make_chunk_id(content_hash, 1234567890.0, 0)
        cid2 = make_chunk_id(content_hash, 9876543210.0, 0)
        assert cid1 != cid2, "不同 mtime 应产生不同 chunk_id"

    def test_make_chunk_id_format(self):
        """chunk_id 应为 24 字符"""
        cid = make_chunk_id("hash123", 1234567890.0, 0)
        assert len(cid) == 24, f"chunk_id 应为 24 字符，实际 {len(cid)}"


class TestParseSections:
    """测试 Markdown 解析"""

    def test_parse_sections_basic(self):
        """基本解析测试"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("""# Title

## [14:32] First Entry

Some content here.

## [15:00] Second Entry

More content.

""")
            f.flush()
            filepath = f.name

        try:
            sections = parse_sections(filepath)
            assert len(sections) == 2, f"应解析出 2 个条目，实际 {len(sections)}"
            assert "First Entry" in sections[0]["title"]
            assert "Second Entry" in sections[1]["title"]
            assert sections[0]["semantic_key"] == "First Entry"
            assert sections[1]["semantic_key"] == "Second Entry"
        finally:
            os.unlink(filepath)

    def test_parse_sections_time_prefix_removal(self):
        """时间前缀应被移除"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("""## [14:32] memory-manager v3.0 升级

Content here.
""")
            f.flush()
            filepath = f.name

        try:
            sections = parse_sections(filepath)
            assert sections[0]["title"] == "[14:32] memory-manager v3.0 升级"
            assert sections[0]["semantic_key"] == "memory-manager v3.0 升级"
        finally:
            os.unlink(filepath)

    def test_parse_sections_skip_short(self):
        """过短内容应被跳过"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("""# Title

## Short

A

""")
            f.flush()
            filepath = f.name

        try:
            sections = parse_sections(filepath)
            assert len(sections) == 0, "过短内容应被跳过"
        finally:
            os.unlink(filepath)


class TestDatabaseOperations:
    """测试数据库操作"""

    def setup_method(self):
        """每个测试前创建临时目录和数据库"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = get_db_path(self.temp_dir)
        self.conn = init_db(self.db_path)

    def teardown_method(self):
        """每个测试后清理"""
        if self.conn:
            self.conn.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_db_creates_table(self):
        """init_db 应创建正确的表结构"""
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='memory_embeddings'")
        result = c.fetchone()
        assert result is not None, "memory_embeddings 表应被创建"

    def test_init_db_creates_indexes(self):
        """init_db 应创建索引"""
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in c.fetchall()]
        assert any("uid" in idx.lower() for idx in indexes), "应有 uid 索引"
        assert any("scope" in idx.lower() for idx in indexes), "应有 scope 索引"

    def test_store_and_retrieve_embedding(self):
        """应能存储和检索向量"""
        import numpy as np

        now = "2026-04-03T12:00:00"
        row = (
            "chunk_123", "test_user", "private", "L1",
            "test.md", 0, "Test Title", "Test Key",
            "Test content", "raw content",
            np.random.rand(1024).astype(np.float32).tobytes(),
            "hash123", 1234567890.0, now,
            50.0, "[]",
        )
        store_embedding(self.conn, row)

        c = self.conn.cursor()
        c.execute("SELECT chunk_id, uid, title FROM memory_embeddings WHERE chunk_id = ?", ("chunk_123",))
        result = c.fetchone()
        assert result is not None, "应能检索到存储的向量"
        assert result[0] == "chunk_123"
        assert result[1] == "test_user"

    def test_delete_embeddings_by_uid(self):
        """delete_embeddings 应按 uid 删除"""
        import numpy as np

        now = "2026-04-03T12:00:00"
        row = (
            "chunk_del", "delete_user", "private", "L1",
            "test.md", 0, "Test", "Key",
            "content", "raw", np.zeros(1024, dtype=np.float32).tobytes(),
            "hash", 1234567890.0, now, 50.0, "[]",
        )
        store_embedding(self.conn, row)

        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM memory_embeddings WHERE uid = ?", ("delete_user",))
        assert c.fetchone()[0] == 1

        delete_embeddings(self.conn, uid="delete_user")

        c.execute("SELECT COUNT(*) FROM memory_embeddings WHERE uid = ?", ("delete_user",))
        assert c.fetchone()[0] == 0


class TestSafeRelpath:
    """测试路径安全"""

    def test_normal_path(self):
        """正常路径应返回相对路径"""
        base = "/home/user/memory"
        path = "/home/user/memory/users/test.md"
        result = safe_relpath(path, base)
        assert result == os.path.join("users", "test.md") or result == "users/test.md"

    def test_path_traversal_blocked(self):
        """路径穿越攻击应被阻止"""
        base = "/home/user/memory"
        path = "/home/user/memory/../../../etc/passwd"
        result = safe_relpath(path, base)
        assert result is None, "路径穿越攻击应被阻止"

    def test_sibling_path(self):
        """兄弟目录路径应被阻止"""
        base = "/home/user/memory"
        path = "/home/user/other_dir/file.md"
        result = safe_relpath(path, base)
        assert result is None, "兄弟目录路径应被阻止"


def run_tests():
    """运行所有测试"""
    print("🧪 Running memory_embed.py unit tests...\n")

    test_classes = [
        TestHashFunctions,
        TestParseSections,
        TestDatabaseOperations,
        TestSafeRelpath,
    ]

    passed = 0
    failed = 0

    for test_class in test_classes:
        print(f"📁 {test_class.__name__}")
        instance = test_class()

        for name in dir(instance):
            if name.startswith("test_"):
                # setup/teardown
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
