#!/usr/bin/env python3
"""db.py 单元测试"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import db


class TestMakeAnnId:
    """测试公告ID生成"""

    def test_basic_id(self):
        """测试基本ID生成"""
        ann = {
            "stock_code": "600519",
            "art_code": "AN202606111823465368",
            "notice_id": "2026-06-12 00:00:00",
            "title": "贵州茅台关于聘任董事会秘书的公告",
        }
        ann_id = db.make_ann_id(ann)
        assert isinstance(ann_id, str)
        assert len(ann_id) == 64  # SHA256 hex length

    def test_different_announcements_different_ids(self):
        """测试不同公告生成不同ID"""
        ann1 = {
            "stock_code": "600519",
            "art_code": "AN001",
            "notice_id": "2026-06-12",
            "title": "公告1",
        }
        ann2 = {
            "stock_code": "600519",
            "art_code": "AN002",
            "notice_id": "2026-06-12",
            "title": "公告2",
        }
        assert db.make_ann_id(ann1) != db.make_ann_id(ann2)

    def test_same_announcements_same_ids(self):
        """测试相同公告生成相同ID"""
        ann1 = {
            "stock_code": "600519",
            "art_code": "AN001",
            "notice_id": "2026-06-12",
            "title": "相同公告",
        }
        ann2 = {
            "stock_code": "600519",
            "art_code": "AN001",
            "notice_id": "2026-06-12",
            "title": "相同公告",
        }
        assert db.make_ann_id(ann1) == db.make_ann_id(ann2)


class TestDatabaseOperations:
    """测试数据库操作"""

    def setup_method(self):
        """每个测试前备份数据库"""
        self.original_db_path = db.DB_PATH
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test.db")
        db.DB_PATH = self.test_db_path
        db.init_db()

    def teardown_method(self):
        """每个测试后恢复数据库"""
        db.DB_PATH = self.original_db_path
        shutil.rmtree(self.temp_dir)

    def test_record_announcement(self):
        """测试记录公告"""
        ann = {
            "stock_code": "600519",
            "stock_name": "贵州茅台",
            "title": "测试公告",
            "ann_date": "2026-06-14 00:00:00",
            "url": "https://example.com",
            "art_code": "TEST001",
            "notice_id": "2026-06-14 00:00:00",
            "status": "valuable",
        }
        db.record_announcements([ann])
        
        # 验证记录已保存
        conn = db._get_conn()
        cursor = conn.execute("SELECT COUNT(*) FROM announcements")
        count = cursor.fetchone()[0]
        conn.close()
        assert count == 1

    def test_get_seen_ids(self):
        """测试获取已见ID"""
        ann = {
            "stock_code": "600519",
            "stock_name": "贵州茅台",
            "title": "测试公告",
            "ann_date": "2026-06-14 00:00:00",
            "url": "https://example.com",
            "art_code": "TEST001",
            "notice_id": "2026-06-14 00:00:00",
        }
        db.record_announcements([ann])
        
        seen_ids = db.get_seen_ids()
        assert len(seen_ids) == 1
        assert db.make_ann_id(ann) in seen_ids

    def test_get_stats(self):
        """测试获取统计信息"""
        stats = db.get_stats()
        assert "total" in stats
        assert "with_content" in stats
        assert "stocks_tracked" in stats
        assert "latest_update" in stats

    def test_prune_empty(self):
        """测试清理空记录"""
        # 插入一条被过滤的记录
        conn = db._get_conn()
        conn.execute("""
            INSERT INTO announcements (ann_id, stock_code, title, status, full_text)
            VALUES ('test_id', '600519', '测试', 'filtered', '')
        """)
        conn.commit()
        conn.close()
        
        deleted = db.prune_empty()
        assert deleted == 1

    def test_list_announcements(self):
        """测试列出公告"""
        ann = {
            "stock_code": "600519",
            "stock_name": "贵州茅台",
            "title": "测试公告",
            "ann_date": "2026-06-14 00:00:00",
            "url": "https://example.com",
            "art_code": "TEST001",
            "notice_id": "2026-06-14 00:00:00",
        }
        db.record_announcements([ann])
        
        anns = db.list_announcements()
        assert len(anns) == 1
        assert anns[0]["stock_code"] == "600519"
