#!/usr/bin/env python3
"""Tests for dependencies.py module"""

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


class TestDependencies:
    def test_get_db_returns_db_module(self):
        from dependencies import get_db
        db = get_db()
        assert hasattr(db, 'DB_PATH')
        assert hasattr(db, 'get_stats')

    def test_get_llm_judge_returns_class(self):
        from dependencies import get_llm_judge
        LLMJudge = get_llm_judge()
        assert hasattr(LLMJudge, 'from_config')

    def test_get_text_cleaner_returns_function(self):
        from dependencies import get_text_cleaner
        clean_announcement_text = get_text_cleaner()
        assert callable(clean_announcement_text)

    def test_get_ann_detail_returns_module(self):
        from dependencies import get_ann_detail
        ann_detail = get_ann_detail()
        assert hasattr(ann_detail, 'fetch_all_contents')

    def test_get_eastmoney_api_returns_module(self):
        from dependencies import get_eastmoney_api
        eastmoney_api = get_eastmoney_api()
        assert hasattr(eastmoney_api, 'get_stocks')

    def test_get_cninfo_api_returns_module(self):
        from dependencies import get_cninfo_api
        cninfo_api = get_cninfo_api()
        assert hasattr(cninfo_api, 'fetch_all_cninfo')

    def test_get_daily_summary_returns_module(self):
        from dependencies import get_daily_summary
        daily_summary = get_daily_summary()
        assert hasattr(daily_summary, 'main')

    def test_scripts_dir_in_sys_path(self):
        from dependencies import SCRIPTS_DIR
        assert SCRIPTS_DIR in sys.path


class TestStockTrackerImports:
    def test_stock_tracker_uses_dependencies(self):
        import stock_tracker
        assert hasattr(stock_tracker, 'db')
        assert hasattr(stock_tracker, 'LLMJudge')
        assert hasattr(stock_tracker, 'clean_announcement_text')
        assert hasattr(stock_tracker, 'ann_detail')
        assert hasattr(stock_tracker, 'eastmoney_api')
        assert hasattr(stock_tracker, 'cninfo_api')
        assert hasattr(stock_tracker, 'fetch_all_contents')
        assert hasattr(stock_tracker, 'fetch_all_cninfo')
        assert hasattr(stock_tracker, 'get_stocks')
        assert hasattr(stock_tracker, 'get_groups')
        assert hasattr(stock_tracker, 'fetch_all_announcements')
        assert hasattr(stock_tracker, 'load_cookie')


class TestAnnDetailImports:
    def test_ann_detail_uses_dependencies(self):
        import ann_detail
        assert hasattr(ann_detail, 'clean_announcement_text')
        assert hasattr(ann_detail, 'LLMJudge')
