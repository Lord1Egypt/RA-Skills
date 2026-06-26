#!/usr/bin/env python3
"""
Test script for Web Change Monitor.
Simulates URL change detection without making real HTTP calls.
"""
import hashlib
import json
import sys

SCRIPT_DIR = __import__('pathlib').Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR.parent))


def test_hash_detection():
    """Test hash-based change detection."""
    from monitor import compute_hash, detect_change, MonitorTask, MODE_HASH

    content = "original content"
    content_hash = compute_hash(content)

    task = MonitorTask(
        url="https://example.com/page1",
        name="Test Page",
        mode=MODE_HASH,
        last_hash=content_hash,   # use actual hash so identical content == no change
        last_content=content,
    )

    # No change - same hash, same content
    changed, change_type, detail = detect_change(task, "original content")
    assert not changed, f"Should not detect change for identical content"

    # Change detected
    changed, change_type, detail = detect_change(task, "modified content")
    assert changed, f"Should detect change for modified content"
    assert change_type == "content_changed", f"Expected content_changed, got {change_type}"
    print("✅ Hash detection test passed")


def test_keyword_detection():
    """Test keyword-based change detection."""
    from monitor import detect_change, MonitorTask, MODE_KEYWORD

    task = MonitorTask(
        url="https://example.com/page2",
        name="Price Monitor",
        mode=MODE_KEYWORD,
        keyword="缺货",
        last_content="商品A 有货",
    )

    # Keyword appears (was absent)
    changed, change_type, detail = detect_change(task, "商品A 缺货")
    assert changed, "Should detect when keyword appears"
    assert "出现" in change_type, f"Expected keyword_出现, got {change_type}"
    print("✅ Keyword appearance detection test passed")

    # Keyword disappears (was present)
    task2 = MonitorTask(
        url="https://example.com/page3",
        name="Stock Monitor",
        mode=MODE_KEYWORD,
        keyword="有货",
        last_content="商品A 有货",
    )
    changed, change_type, detail = detect_change(task2, "商品A 缺货")
    assert changed, "Should detect when keyword disappears"
    assert "消失" in change_type
    print("✅ Keyword disappearance detection test passed")


def test_selector_detection():
    """Test CSS selector-based change detection."""
    from monitor import detect_change, MonitorTask, MODE_SELECTOR

    html_old = """
    <html><body>
        <div class="product-list">
            <div class="item">商品A</div>
            <div class="item">商品B</div>
        </div>
    </body></html>
    """
    html_new = """
    <html><body>
        <div class="product-list">
            <div class="item">商品A</div>
            <div class="item">商品B</div>
            <div class="item">商品C</div>
        </div>
    </body></html>
    """

    task = MonitorTask(
        url="https://example.com/list",
        name="Product List",
        mode=MODE_SELECTOR,
        selector=".product-list .item",
        last_content="商品A|商品B",
    )

    changed, change_type, detail = detect_change(task, html_new)
    assert changed, "Should detect change when new item added"
    print("✅ Selector detection test passed")


def test_regex_detection():
    """Test regex-based change detection."""
    from monitor import detect_change, MonitorTask, MODE_REGEX

    task = MonitorTask(
        url="https://example.com/price",
        name="Price Regex",
        mode=MODE_REGEX,
        regex=r"¥(\d+(?:\.\d{2})?)",
        last_content="¥99.00",
    )

    changed, change_type, detail = detect_change(task, "商品价格：¥88.50")
    assert changed, "Should detect price change via regex"
    print("✅ Regex detection test passed")


def test_compute_hash():
    """Test hash computation consistency."""
    from monitor import compute_hash
    content = "Hello World"
    h1 = compute_hash(content)
    h2 = compute_hash(content)
    assert h1 == h2, "Hash should be deterministic"
    assert len(h1) == 32, "MD5 hash should be 32 chars"
    print("✅ Hash computation test passed")


def test_tier_limits():
    """Test tier limit enforcement."""
    from monitor import TIER_LIMITS

    assert TIER_LIMITS["free"]["max_urls"] == 3
    assert TIER_LIMITS["pro"]["max_urls"] == float("inf")
    assert TIER_LIMITS["standard"]["history_days"] == 7
    print("✅ Tier limits test passed")


def test_db_operations():
    """Test SQLite operations (in memory)."""
    import tempfile
    import sqlite3
    import os

    # Override DB path temporarily
    tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp_db.close()
    os.environ["WEB_MONITOR_DB"] = tmp_db.name

    # Re-import with env
    import importlib
    import monitor as m
    m.DB_PATH = tmp_db.name

    # Test in-memory init
    conn = sqlite3.connect(tmp_db.name)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS monitor_tasks (
            url TEXT PRIMARY KEY, name TEXT NOT NULL, mode TEXT DEFAULT 'hash',
            frequency TEXT DEFAULT '24h', keyword TEXT, selector TEXT, regex TEXT,
            last_hash TEXT, last_content TEXT, last_check TEXT,
            created_at TEXT NOT NULL, change_count INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS change_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL, name TEXT NOT NULL,
            detected_at TEXT NOT NULL, change_type TEXT NOT NULL, detail TEXT, mode TEXT
        )
    """)
    conn.commit()

    # Insert test task
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""
        INSERT OR REPLACE INTO monitor_tasks (url, name, mode, frequency, created_at)
        VALUES (?, ?, ?, ?, ?)""",
        ("https://test.com", "Test Task", "hash", "24h", now)
    )
    conn.commit()

    # Verify
    row = conn.execute("SELECT url, name FROM monitor_tasks WHERE url=?", ("https://test.com",)).fetchone()
    assert row is not None, "Task should be inserted"
    assert row[0] == "https://test.com"
    print("✅ DB operations test passed")

    os.unlink(tmp_db.name)


def test_change_message_builder():
    """Test Feishu message building."""
    from monitor import build_change_message

    msg = build_change_message("商品A监控", "https://example.com/p/123", "content_changed", "页面内容已变更")
    assert "商品A监控" in msg
    assert "https://example.com/p/123" in msg
    assert "content_changed" in msg
    assert "🔄" in msg
    print("✅ Change message builder test passed")


def main():
    tests = [
        test_compute_hash,
        test_hash_detection,
        test_keyword_detection,
        test_selector_detection,
        test_regex_detection,
        test_tier_limits,
        test_db_operations,
        test_change_message_builder,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())