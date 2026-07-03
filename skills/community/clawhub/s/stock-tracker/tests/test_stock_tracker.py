#!/usr/bin/env python3
"""Tests for stock_tracker.py refactored subcommand handlers"""

import sys
import os
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from stock_tracker import (
    handle_stats,
    handle_clean,
    handle_prune,
    handle_list,
    handle_list_groups,
    handle_fetch_content,
    handle_main_flow,
    run,
    _backup_database,
)
from error_handler import DataError


class TestDispatcher:
    def test_stats_routes_to_handle_stats(self):
        with patch("stock_tracker.handle_stats") as mock:
            run(["--stats"])
            mock.assert_called_once()

    def test_clean_routes_to_handle_clean(self):
        with patch("stock_tracker.handle_clean") as mock:
            run(["--clean"])
            mock.assert_called_once()

    def test_prune_routes_to_handle_prune(self):
        with patch("stock_tracker.handle_prune") as mock:
            run(["--prune"])
            mock.assert_called_once()

    def test_list_routes_to_handle_list(self):
        with patch("stock_tracker.handle_list") as mock:
            run(["--list"])
            mock.assert_called_once()

    def test_list_groups_routes_to_handle_list_groups(self):
        with patch("stock_tracker.handle_list_groups") as mock:
            run(["--list-groups"])
            mock.assert_called_once()

    def test_default_routes_to_handle_main_flow(self):
        with patch("stock_tracker.handle_main_flow") as mock:
            run([])
            mock.assert_called_once()

    def test_stats_skips_backup(self):
        with (
            patch("stock_tracker.handle_stats"),
            patch("stock_tracker._backup_database") as mock_bak,
        ):
            with patch("stock_tracker.os.path.exists", return_value=True):
                run(["--stats"])
                mock_bak.assert_not_called()

    def test_backup_called_when_db_exists(self):
        with (
            patch("stock_tracker.handle_stats"),
            patch("stock_tracker._backup_database") as mock_bak,
            patch("stock_tracker.os.path.exists", return_value=True),
        ):
            run(["--stats"])
            mock_bak.assert_not_called()

    def test_backup_called_for_main_flow(self):
        with (
            patch("stock_tracker.handle_main_flow"),
            patch("stock_tracker._backup_database") as mock_bak,
            patch("stock_tracker.os.path.exists", return_value=True),
        ):
            run([])
            mock_bak.assert_called_once()


class TestHandleStats:
    def test_prints_stats(self, capsys):
        import db

        fake_stats = {
            "total": 100,
            "with_content": 80,
            "stocks_tracked": 10,
            "latest_update": "2025-01-01 12:00:00",
        }
        with (
            patch.object(db, "get_stats", return_value=fake_stats),
            patch.object(db, "_count_by_source", return_value=50),
            patch.object(db, "get_records_needing_clean", return_value=[1, 2]),
            patch.object(db, "get_pending_content", return_value=[1]),
        ):
            handle_stats()
        output = capsys.readouterr().out
        assert "总公告数: 100" in output
        assert "含正文: 80" in output
        assert "待清洗: 2 条" in output
        assert "待采集全文: 1 条" in output

    def test_no_pending_items(self, capsys):
        import db

        fake_stats = {
            "total": 50,
            "with_content": 50,
            "stocks_tracked": 5,
            "latest_update": "2025-01-01 12:00:00",
        }
        with (
            patch.object(db, "get_stats", return_value=fake_stats),
            patch.object(db, "_count_by_source", return_value=25),
            patch.object(db, "get_records_needing_clean", return_value=[]),
            patch.object(db, "get_pending_content", return_value=[]),
        ):
            handle_stats()
        output = capsys.readouterr().out
        assert "待清洗" not in output
        assert "待采集全文" not in output


class TestHandleClean:
    def test_no_pending(self):
        import db

        with patch.object(db, "get_records_needing_clean", return_value=[]):
            handle_clean()

    def test_cleans_pending(self, capsys):
        import db

        pending = [
            {"full_text": "原始文本ABC" * 100, "clean_text": ""},
            {"full_text": "原始文本DEF" * 100, "clean_text": ""},
        ]
        with (
            patch.object(db, "get_records_needing_clean", return_value=pending),
            patch.object(db, "update_clean_text") as mock_update,
            patch("stock_tracker.clean_announcement_text", side_effect=lambda t: t[:10]),
        ):
            handle_clean()
            mock_update.assert_called_once()
            for ann in pending:
                assert len(ann["clean_text"]) == 10


class TestHandlePrune:
    def test_prunes(self):
        import db

        with patch.object(db, "prune_empty", return_value=3) as mock:
            handle_prune()
            mock.assert_called_once()


class TestHandleList:
    def test_no_announcements(self, capsys):
        import db

        mock_parsed = MagicMock()
        mock_parsed.days = None
        mock_parsed.group = None
        mock_parsed.stock = None
        with patch.object(db, "list_announcements", return_value=[]):
            handle_list(mock_parsed)
        output = capsys.readouterr().out
        assert "暂无公告记录" in output

    def test_with_announcements(self, capsys):
        import db

        mock_parsed = MagicMock()
        mock_parsed.days = 7
        mock_parsed.group = None
        mock_parsed.stock = None
        fake_anns = [
            {
                "stock_name": "贵州茅台",
                "stock_code": "600519",
                "ann_date": "2025-01-01",
                "title": "关于回购股份的公告",
                "ann_type": "公告",
                "first_seen_at": "2025-01-01 12:00:00",
                "url": "https://example.com/1",
            }
        ]
        with patch.object(db, "list_announcements", return_value=fake_anns):
            handle_list(mock_parsed)
        output = capsys.readouterr().out
        assert "贵州茅台" in output
        assert "关于回购股份的公告" in output

    def test_with_group(self):
        import db

        mock_parsed = MagicMock()
        mock_parsed.days = 30
        mock_parsed.group = "持仓"
        mock_parsed.stock = None
        fake_stocks = [{"code": "600519"}, {"code": "000858"}]
        with (
            patch("stock_tracker.get_stocks", return_value=fake_stocks),
            patch.object(db, "list_announcements", return_value=[]) as mock_list,
        ):
            handle_list(mock_parsed)
            mock_list.assert_called_once_with(
                stock_code=None, stock_codes=["600519", "000858"], days=30
            )


class TestHandleListGroups:
    def test_no_cookie(self):
        with (
            patch("stock_tracker.load_cookie", return_value=None),
            patch("stock_tracker.sys.exit") as mock_exit,
        ):
            handle_list_groups()
            mock_exit.assert_called_once_with(1)

    def test_with_groups(self):
        fake_groups = [{"gid": "1", "gname": "持仓"}, {"gid": "2", "gname": "自选"}]
        with (
            patch("stock_tracker.load_cookie", return_value="fake_cookie"),
            patch("stock_tracker.get_groups", return_value=fake_groups),
        ):
            handle_list_groups()


class TestHandleFetchContent:
    def test_no_pending(self):
        import db

        mock_parsed = MagicMock()
        mock_llm = MagicMock()
        mock_llm.enabled = False
        with (
            patch.object(db, "get_pending_content", return_value=[]),
            patch.object(db, "prune_empty"),
        ):
            handle_fetch_content(mock_parsed, mock_llm)

    def test_with_pending(self):
        import db

        mock_parsed = MagicMock()
        mock_llm = MagicMock()
        mock_llm.enabled = True
        mock_llm.report.return_value = "LLM report"
        fake_pending = [{"title": "test"}]
        with (
            patch.object(db, "get_pending_content", return_value=fake_pending),
            patch("stock_tracker.fetch_all_contents") as mock_fetch,
            patch.object(db, "get_stats", return_value={"total": 10, "with_content": 5}),
            patch.object(db, "prune_empty"),
        ):
            handle_fetch_content(mock_parsed, mock_llm)
            mock_fetch.assert_called_once()


class TestHandleMainFlow:
    def test_exits_when_no_stocks(self):
        mock_parsed = MagicMock()
        mock_parsed.fetch_content = False
        mock_parsed.days = None
        mock_parsed.group = None
        with (
            patch("stock_tracker.ConfigManager") as mock_config_mgr_cls,
            patch("stock_tracker.LLMJudge") as mock_llm_cls,
            patch("stock_tracker.load_cookie"),
            patch("stock_tracker.get_stocks", return_value=[]),
        ):
            mock_config = MagicMock()
            mock_config.fetch_interval_days = 7
            mock_config_mgr_cls.return_value.load.return_value = mock_config
            mock_llm_cls.from_config.return_value = MagicMock()
            with pytest.raises(DataError) as exc_info:
                handle_main_flow(mock_parsed)
            assert "未获取到自选股列表" in str(exc_info.value)

    def test_dry_run_saves_nothing(self):
        mock_parsed = MagicMock()
        mock_parsed.fetch_content = False
        mock_parsed.days = 7
        mock_parsed.group = None
        mock_parsed.force = False
        mock_parsed.dry_run = True
        mock_parsed.source = "eastmoney"
        mock_parsed.config = "config.json"
        fake_stocks = [{"code": "600519", "name": "贵州茅台", "market": "1"}]
        fake_anns = [
            {
                "stock_code": "600519",
                "stock_name": "贵州茅台",
                "title": "公告A",
                "ann_date": "2025-01-01",
                "art_code": "123",
                "notice_id": "n1",
                "url": "https://example.com/1",
            }
        ]
        with (
            patch("stock_tracker.ConfigManager") as mock_config_mgr_cls,
            patch("stock_tracker.LLMJudge") as mock_llm_cls,
            patch("stock_tracker.load_cookie"),
            patch("stock_tracker.get_stocks", return_value=fake_stocks),
            patch("stock_tracker.fetch_all_announcements", return_value=fake_anns),
            patch("stock_tracker.db") as mock_db,
            patch("stock_tracker.send_notification"),
        ):
            mock_config = MagicMock()
            mock_config.fetch_interval_days = 7
            mock_config_mgr_cls.return_value.load.return_value = mock_config
            mock_llm_cls.from_config.return_value = MagicMock()
            mock_db.make_ann_id.return_value = "fake_id"
            mock_db.get_seen_ids.return_value = set()
            handle_main_flow(mock_parsed)
            mock_db.record_announcements.assert_not_called()


class TestBackupDatabase:
    def test_backs_up(self):
        with (
            patch("stock_tracker.shutil") as mock_shutil,
            patch("stock_tracker.db"),
        ):
            _backup_database()
            mock_shutil.copy2.assert_called_once()
