#!/usr/bin/env python3
"""
Sentiment Compass — Test Suite
Tests: unit tests + integration tests for all core features.
"""

import hashlib
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))


# ─── Test Utilities ───────────────────────────────────────────────────────────
class TestDB:
    """In-memory test database."""
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE NOT NULL,
                platforms TEXT NOT NULL,
                frequency TEXT DEFAULT 'daily',
                priority INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TEXT NOT NULL,
                last_crawl_at TEXT,
                alert_threshold INTEGER DEFAULT 5,
                alert_channels TEXT DEFAULT ''
            )
        """)
        self.conn.execute("""
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                platform TEXT NOT NULL,
                post_id TEXT NOT NULL,
                title TEXT,
                content TEXT,
                author TEXT,
                author_id TEXT,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                published_at TEXT,
                fetched_at TEXT NOT NULL,
                url TEXT UNIQUE,
                UNIQUE(keyword, platform, post_id)
            )
        """)
        self.conn.execute("""
            CREATE TABLE analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
                sentiment TEXT,
                score REAL,
                reason TEXT,
                analyzed_at TEXT NOT NULL
            )
        """)
        self.conn.execute("""
            CREATE TABLE alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                threshold INTEGER,
                negative_count INTEGER,
                negative_rate REAL,
                triggered_at TEXT NOT NULL,
                notification_sent INTEGER DEFAULT 0
            )
        """)
        self.conn.execute("""
            CREATE TABLE configs (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.conn.commit()


def seed_test_data(conn):
    """Insert realistic test data into the test DB."""
    now = datetime.now(timezone.utc).isoformat()
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Tasks
    conn.execute("""
        INSERT INTO tasks (keyword, platforms, frequency, priority, status, created_at, alert_threshold)
        VALUES
        ('某品牌', 'xhs,douyin', 'daily', 1, 'active', ?, 5),
        ('某竞品', 'xhs,douyin,weibo', 'daily', 0, 'active', ?, 3)
    """, (now, now))
    conn.commit()

    # Posts
    posts = [
        ("某品牌", "xhs", "post1", "这家咖啡真的太好喝了！强烈推荐", "这家咖啡真的太好喝了！强烈推荐", "咖啡达人", "uid1", 5200, 340, 120, today, now, "https://xhs.com/p/1"),
        ("某品牌", "xhs", "post2", "质量太差，完全不值这个价格", "质量太差，完全不值这个价格", "消费者甲", "uid2", 12, 5, 2, today, now, "https://xhs.com/p/2"),
        ("某品牌", "xhs", "post3", "还行吧，中规中矩，没有特别出彩的地方", "还行吧，中规中矩", "普通人", "uid3", 88, 22, 10, yesterday, now, "https://xhs.com/p/3"),
        ("某品牌", "douyin", "post4", "这个护肤品真的惊艳到我了", "用了之后皮肤明显变好了", "美妆博主", "uid4", 15000, 890, 430, today, now, "https://douyin.com/v/4"),
        ("某品牌", "weibo", "post5", "垃圾产品，售后服务也差，大家别买", "垃圾产品，售后服务也差", "愤怒用户", "uid5", 45, 120, 30, today, now, "https://weibo.com/w/5"),
    ]
    conn.executemany("""
        INSERT OR IGNORE INTO posts (keyword, platform, post_id, title, content, author, author_id, likes, comments, shares, published_at, fetched_at, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, posts)
    conn.commit()

    # Analyses
    analyses = [
        (1, "positive", 0.85, "检测到'太好喝''强烈推荐'等正面词汇"),
        (2, "negative", -0.82, "检测到'太差''不值'等负面词汇"),
        (3, "neutral", 0.02, "中性表达，无明显情感倾向"),
        (4, "positive", 0.78, "检测到'惊艳'等正面词汇"),
        (5, "negative", -0.91, "检测到'垃圾''别买'等负面词汇"),
    ]
    conn.executemany("""
        INSERT INTO analyses (post_id, sentiment, score, reason, analyzed_at)
        VALUES (?, ?, ?, ?, ?)
    """, [(a[0], a[1], a[2], a[3], now) for a in analyses])
    conn.commit()


# ─── Unit Tests ───────────────────────────────────────────────────────────────
class TestRuleBasedSentiment(unittest.TestCase):
    """Test rule-based sentiment analysis (no API needed)."""

    def setUp(self):
        import importlib
        import sentiment as s
        importlib.reload(s)
        self.module = s

    def test_positive_text(self):
        result = self.module.rule_based_sentiment("这个产品真的很好用，强烈推荐给大家！")
        self.assertEqual(result.sentiment, "positive")
        self.assertGreater(result.score, 0)

    def test_negative_text(self):
        result = self.module.rule_based_sentiment("质量太差了，完全不值这个价格，垃圾产品")
        self.assertEqual(result.sentiment, "negative")
        self.assertLess(result.score, 0)

    def test_neutral_text(self):
        result = self.module.rule_based_sentiment("今天天气不错")
        self.assertEqual(result.sentiment, "neutral")

    def test_mixed_text(self):
        result = self.module.rule_based_sentiment("包装还可以但是质量一般")
        self.assertIn(result.sentiment, ["positive", "neutral", "negative"])

    def test_empty_text(self):
        result = self.module.rule_based_sentiment("")
        self.assertEqual(result.sentiment, "neutral")

    def test_intensifier_boost(self):
        result1 = self.module.rule_based_sentiment("好")
        result2 = self.module.rule_based_sentiment("非常好")
        self.assertGreater(result2.score, result1.score)

    def test_negation_reversal(self):
        result = self.module.rule_based_sentiment("不好")
        self.assertEqual(result.sentiment, "negative")

    def test_wan_format_parsing(self):
        result = self.module._parse_number("1.2万")
        self.assertEqual(result, 12000)

        result2 = self.module._parse_number("3.5万")
        self.assertEqual(result2, 35000)

        result3 = self.module._parse_number("999")
        self.assertEqual(result3, 999)


class TestParsing(unittest.TestCase):
    """Test HTML parsing functions."""

    def setUp(self):
        import importlib
        import sentiment as s
        importlib.reload(s)
        self.module = s

    def test_parse_xhs_posts(self):
        html = """
        <html><body>
            <div class="feeds-page">
                <div class="note-item">
                    <h2 class="title">测试咖啡笔记</h2>
                    <div class="desc">这家咖啡真的太好喝了</div>
                    <div class="author">咖啡达人</div>
                    <div class="like">1200</div>
                    <a href="/discovery/item/abc123">链接</a>
                </div>
            </div>
        </body></html>
        """
        posts = self.module.parse_xhs_posts(html, "咖啡")
        self.assertGreaterEqual(len(posts), 1)
        self.assertEqual(posts[0].platform, "xhs")
        self.assertEqual(posts[0].keyword, "咖啡")
        self.assertIn("咖啡", posts[0].title)

    def test_parse_weibo_posts(self):
        html = """
        <html><body>
            <div class="card-feed">
                <div class="content">
                    <p>这条微博真的很赞，推荐给大家！</p>
                </div>
                <div class="name">微博用户A</div>
                <div class="like">888</div>
                <a href="/detail/Bbb456">查看</a>
            </div>
        </body></html>
        """
        posts = self.module.parse_weibo_posts(html, "推荐")
        self.assertGreaterEqual(len(posts), 1)

    def test_parse_wechat_posts(self):
        html = """
        <html><body>
            <div class="news-box">
                <ul class="news-list">
                    <li>
                        <h3 class="tit">公众号文章标题</h3>
                        <p class="txt">这是文章摘要</p>
                        <div class="account">公众号名称</div>
                        <div class="date">2024-01-01</div>
                        <a href="https://mp.weixin.qq.com/s/xyz">阅读</a>
                    </li>
                </ul>
            </div>
        </body></html>
        """
        posts = self.module.parse_wechat_posts(html, "文章")
        self.assertGreaterEqual(len(posts), 1)

    def test_parse_douyin_posts(self):
        html = """
        <html><body>
            <ul class="video-feed-list">
                <li class="video-item">
                    <h3 class="title">抖音视频标题</h3>
                    <div class="author">抖音博主</div>
                    <div class="like-count">5000</div>
                    <a href="/video/123456789">查看</a>
                </li>
            </ul>
        </body></html>
        """
        posts = self.module.parse_douyin_posts(html, "视频")
        self.assertGreaterEqual(len(posts), 1)


class TestTierLimits(unittest.TestCase):
    """Test tier limit enforcement."""

    def test_tier_limits_structure(self):
        import sentiment as s
        self.assertIn("FREE", s.TIER_LIMITS)
        self.assertIn("STD", s.TIER_LIMITS)
        self.assertIn("PRO", s.TIER_LIMITS)
        self.assertIn("MAX", s.TIER_LIMITS)

    def test_free_tier(self):
        import sentiment as s
        free = s.TIER_LIMITS["FREE"]
        self.assertEqual(free["max_keywords"], 1)
        self.assertEqual(free["platforms"], ["xhs"])
        self.assertEqual(free["daily_limit"], 50)
        self.assertFalse(free["report"])
        self.assertFalse(free["feishu_alert"])

    def test_std_tier(self):
        import sentiment as s
        std = s.TIER_LIMITS["STD"]
        self.assertEqual(std["max_keywords"], 3)
        self.assertEqual(std["platforms"], ["xhs", "douyin"])
        self.assertEqual(std["daily_limit"], 300)
        self.assertTrue(std["alert_email"])

    def test_pro_tier(self):
        import sentiment as s
        pro = s.TIER_LIMITS["PRO"]
        self.assertEqual(pro["max_keywords"], 10)
        self.assertEqual(pro["platforms"], ["xhs", "douyin", "weibo", "wechat"])
        self.assertEqual(pro["daily_limit"], 1000)
        self.assertTrue(pro["report"])
        self.assertTrue(pro["feishu_alert"])

    def test_max_tier(self):
        import sentiment as s
        mx = s.TIER_LIMITS["MAX"]
        self.assertEqual(mx["max_keywords"], -1)
        self.assertEqual(mx["daily_limit"], -1)
        self.assertTrue(mx["api"])


class TestAlertThresholds(unittest.TestCase):
    """Test alert threshold logic."""

    def setUp(self):
        self.db = TestDB()
        seed_test_data(self.db.conn)

    def test_threshold_triggered(self):
        """Negative count >= threshold should trigger alert."""
        # Insert 5 more negative posts to trigger threshold=5
        now = datetime.now(timezone.utc).isoformat()
        today = datetime.now().strftime("%Y-%m-%d")

        for i in range(5):
            self.db.conn.execute("""
                INSERT OR IGNORE INTO posts (keyword, platform, post_id, title, content, author, author_id, likes, comments, shares, published_at, fetched_at, url)
                VALUES ('某品牌', 'xhs', ?, '负面帖子', '真的很差', '用户', 'uid', 1, 0, 0, ?, ?, ?)
            """, (f"neg{i}", today, now, f"https://xhs.com/neg{i}"))
            post_id = self.db.conn.execute("SELECT id FROM posts WHERE post_id=?", (f"neg{i}",)).fetchone()[0]
            self.db.conn.execute("""
                INSERT INTO analyses (post_id, sentiment, score, reason, analyzed_at)
                VALUES (?, 'negative', -0.8, '负面', ?)
            """, (post_id, now))
        self.db.conn.commit()

        # Count negatives today
        cutoff = f"{today}T00:00:00+00:00"
        neg_count = self.db.conn.execute("""
            SELECT COUNT(*) FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword='某品牌' AND a.sentiment='negative' AND p.fetched_at>=?
        """, (cutoff,)).fetchone()[0]

        self.assertGreaterEqual(neg_count, 5)


class TestDataQuery(unittest.TestCase):
    """Test data querying functions."""

    def setUp(self):
        self.db = TestDB()
        seed_test_data(self.db.conn)

    def test_query_by_sentiment(self):
        neg_posts = self.db.conn.execute("""
            SELECT p.title, a.sentiment FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE a.sentiment='negative'
        """).fetchall()
        self.assertEqual(len(neg_posts), 2)

    def test_query_by_platform(self):
        xhs_posts = self.db.conn.execute("""
            SELECT COUNT(*) FROM posts WHERE platform='xhs'
        """).fetchone()[0]
        self.assertEqual(xhs_posts, 3)

    def test_query_with_time_filter(self):
        today = datetime.now().strftime("%Y-%m-%d")
        cutoff = f"{today}T00:00:00+00:00"
        today_posts = self.db.conn.execute("""
            SELECT COUNT(*) FROM posts WHERE fetched_at>=?
        """, (cutoff,)).fetchone()[0]
        self.assertGreaterEqual(today_posts, 1)


class TestSentimentScoring(unittest.TestCase):
    """Test sentiment scoring ranges."""

    def setUp(self):
        import importlib
        import sentiment as s
        importlib.reload(s)
        self.module = s

    def test_score_range_positive(self):
        result = self.module.rule_based_sentiment("真的太棒了，非常非常好，完美！")
        self.assertGreater(result.score, 0)
        self.assertLessEqual(result.score, 1.0)

    def test_score_range_negative(self):
        result = self.module.rule_based_sentiment("太差了，垃圾，废物，完全不行")
        self.assertLess(result.score, 0)
        self.assertGreaterEqual(result.score, -1.0)

    def test_score_range_neutral(self):
        result = self.module.rule_based_sentiment("今天吃了米饭")
        self.assertGreaterEqual(result.score, -1.0)
        self.assertLessEqual(result.score, 1.0)


class TestDBOperations(unittest.TestCase):
    """Test SQLite operations."""

    def test_insert_and_fetch_task(self):
        db = TestDB()
        now = datetime.now(timezone.utc).isoformat()
        db.conn.execute("""
            INSERT INTO tasks (keyword, platforms, frequency, created_at)
            VALUES (?, ?, ?, ?)
        """, ("测试关键词", "xhs,douyin", "daily", now))
        db.conn.commit()

        row = db.conn.execute("SELECT keyword, platforms FROM tasks WHERE keyword=?", ("测试关键词",)).fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "测试关键词")
        self.assertEqual(row[1], "xhs,douyin")

    def test_unique_post_constraint(self):
        db = TestDB()
        now = datetime.now(timezone.utc).isoformat()
        db.conn.execute("""
            INSERT INTO posts (keyword, platform, post_id, title, fetched_at, url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("品牌A", "xhs", "p1", "标题", now, "https://x.com/1"))
        db.conn.commit()

        # Try duplicate
        try:
            db.conn.execute("""
                INSERT INTO posts (keyword, platform, post_id, title, fetched_at, url)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("品牌A", "xhs", "p1", "标题2", now, "https://x.com/1"))
            db.conn.commit()
        except sqlite3.IntegrityError:
            pass  # Expected

        count = db.conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        self.assertEqual(count, 1)


class TestPlatformConfig(unittest.TestCase):
    """Test platform configuration."""

    def test_all_platforms_configured(self):
        import sentiment as s
        for key in ["xhs", "douyin", "weibo", "wechat"]:
            self.assertIn(key, s.PLATFORM_CONFIG)
            self.assertIn("name", s.PLATFORM_CONFIG[key])
            self.assertIn("search_url", s.PLATFORM_CONFIG[key])

    def test_keyword_url_format(self):
        import sentiment as s
        cfg = s.PLATFORM_CONFIG["xhs"]
        url = cfg["search_url"].format(keyword="咖啡")
        self.assertIn("咖啡", url)


class TestAlertRecord(unittest.TestCase):
    """Test AlertRecord dataclass."""

    def test_alert_record_creation(self):
        import sentiment as s
        alert = s.AlertRecord(
            keyword="某品牌",
            alert_type="threshold",
            threshold=5,
            negative_count=7,
            negative_rate=35.0,
        )
        self.assertEqual(alert.keyword, "某品牌")
        self.assertEqual(alert.alert_type, "threshold")
        self.assertEqual(alert.negative_count, 7)
        self.assertIsNotNone(alert.triggered_at)


class TestSentimentResult(unittest.TestCase):
    """Test SentimentResult dataclass."""

    def test_sentiment_result_creation(self):
        import sentiment as s
        result = s.SentimentResult(
            post_id=1,
            sentiment="positive",
            score=0.85,
            reason="检测到正面词汇",
        )
        self.assertEqual(result.sentiment, "positive")
        self.assertEqual(result.score, 0.85)
        self.assertIsNotNone(result.analyzed_at)


class TestEdgeCases(unittest.TestCase):
    """Edge case tests."""

    def setUp(self):
        import importlib
        import sentiment as s
        importlib.reload(s)
        self.module = s

    def test_very_long_text(self):
        long_text = "好 " * 1000
        result = self.module.rule_based_sentiment(long_text)
        self.assertIn(result.sentiment, ["positive", "neutral", "negative"])

    def test_emoji_only(self):
        result = self.module.rule_based_sentiment("😀😃😄😁")
        self.assertIn(result.sentiment, ["positive", "neutral", "negative"])

    def test_special_characters(self):
        result = self.module.rule_based_sentiment("！@#$%^&*()")
        self.assertIn(result.sentiment, ["positive", "neutral", "negative"])

    def test_chinese_and_english_mixed(self):
        result = self.module.rule_based_sentiment("这个product真的very good，强烈recommend！")
        self.assertIn(result.sentiment, ["positive", "neutral", "negative"])


# ─── Test Runner ──────────────────────────────────────────────────────────────
def main():
    # Build test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestRuleBasedSentiment,
        TestParsing,
        TestTierLimits,
        TestAlertThresholds,
        TestDataQuery,
        TestSentimentScoring,
        TestDBOperations,
        TestPlatformConfig,
        TestAlertRecord,
        TestSentimentResult,
        TestEdgeCases,
    ]

    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    # Run
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print(f"\n{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    if result.failures:
        print("\n--- Failures ---")
        for test, traceback in result.failures:
            print(f"{test}: {traceback}")
    if result.errors:
        print("\n--- Errors ---")
        for test, traceback in result.errors:
            print(f"{test}: {traceback}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
