#!/usr/bin/env python3
"""
Web Change Monitor — core monitoring engine.
Fetches pages with Playwright, compares content, triggers notifications.
"""

import hashlib
import json
import os
import random
import re
import signal
import sqlite3
import sys
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List

# ─── Paths ────────────────────────────────────────────────────────────────────
DB_PATH = os.path.expanduser("~/.web-change-monitor/history.db")
SCRIPT_DIR = Path(__file__).parent.resolve()

# ─── User Agent Pool ──────────────────────────────────────────────────────────
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# ─── Frequency map ─────────────────────────────────────────────────────────────
FREQUENCY_SECONDS = {
    "15m": 15 * 60,
    "30m": 30 * 60,
    "1h": 60 * 60,
    "6h": 6 * 60 * 60,
    "12h": 12 * 60 * 60,
    "24h": 24 * 60 * 60,
}

# ─── Detection Modes ──────────────────────────────────────────────────────────
MODE_HASH = "hash"
MODE_KEYWORD = "keyword"
MODE_SELECTOR = "selector"
MODE_REGEX = "regex"
VALID_MODES = [MODE_HASH, MODE_KEYWORD, MODE_SELECTOR, MODE_REGEX]

# ─── Tier limits ──────────────────────────────────────────────────────────────
TIER_LIMITS = {
    "free": {"max_urls": 3, "max_frequency": "24h", "history_days": 0},
    "basic": {"max_urls": 10, "max_frequency": "12h", "history_days": 0},
    "standard": {"max_urls": 30, "max_frequency": "6h", "history_days": 7},
    "pro": {"max_urls": float("inf"), "max_frequency": "1h", "history_days": 30},
}

# ─── Dataclasses ──────────────────────────────────────────────────────────────
@dataclass
class MonitorTask:
    url: str
    name: str
    mode: str = MODE_HASH
    frequency: str = "24h"
    keyword: Optional[str] = None
    selector: Optional[str] = None
    regex: Optional[str] = None
    last_hash: Optional[str] = None
    last_content: Optional[str] = None
    last_check: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    change_count: int = 0

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "MonitorTask":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ChangeRecord:
    url: str
    name: str
    detected_at: str
    change_type: str
    detail: str
    mode: str

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Database ─────────────────────────────────────────────────────────────────
def _get_db() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS monitor_tasks (
            url TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            mode TEXT DEFAULT 'hash',
            frequency TEXT DEFAULT '24h',
            keyword TEXT,
            selector TEXT,
            regex TEXT,
            last_hash TEXT,
            last_content TEXT,
            last_check TEXT,
            created_at TEXT NOT NULL,
            change_count INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS change_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            name TEXT NOT NULL,
            detected_at TEXT NOT NULL,
            change_type TEXT NOT NULL,
            detail TEXT,
            mode TEXT
        )
    """)
    conn.commit()
    return conn


# ─── Playwright Fetcher ────────────────────────────────────────────────────────
def fetch_page(url: str, timeout_ms: int = 15000) -> Optional[str]:
    """
    Fetch page content using Playwright (Node.js subprocess).
    Returns HTML string or None on failure.
    """
    import subprocess

    script = f"""
    const {{ chromium }} = require('playwright');
    (async () => {{
        const browser = await chromium.launch({{ headless: true }});
        const page = await browser.newPage();
        await page.setExtraHTTPHeaders({{}});
        await page.setExtraHTTPHeaders({{ 'Accept-Language': 'zh-CN,zh;q=0.9' }});
        await page.goto({json.dumps(url)}, {{ waitUntil: 'networkidle', timeout: {timeout_ms} }});
        const content = await page.content();
        await browser.close();
        console.log(JSON.stringify({{ ok: true, content }}));
    }})().catch(e => {{ console.log(JSON.stringify({{ ok: false, error: e.message }})); process.exit(1); }});
    """

    try:
        result = subprocess.run(
            ["node", "-e", script],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout.strip())
        if data.get("ok"):
            return data["content"]
    except Exception:
        pass
    return None


# ─── Content extraction ────────────────────────────────────────────────────────
def extract_by_selector(html: str, selector: str) -> str:
    """Extract text from HTML using CSS selector via BeautifulSoup."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(selector)
    return "|".join(e.get_text(strip=True) for e in elements)


def extract_by_regex(html: str, pattern: str) -> str:
    """Extract content matching regex pattern."""
    try:
        matches = re.findall(pattern, html)
        return "|".join(matches)
    except re.error:
        return ""


def compute_hash(content: str) -> str:
    return hashlib.md5(content.encode("utf-8", errors="ignore")).hexdigest()


# ─── Detect change ────────────────────────────────────────────────────────────
def detect_change(task: MonitorTask, current_content: str) -> tuple[bool, str, str]:
    """
    Returns (changed: bool, change_type: str, detail: str)
    """
    current_hash = compute_hash(current_content)

    if task.mode == MODE_HASH:
        if task.last_hash and task.last_hash != current_hash:
            return True, "content_changed", "页面内容已变更"
        return False, "", ""

    elif task.mode == MODE_KEYWORD:
        if not task.keyword:
            return False, "", ""
        keyword_lower = task.keyword.lower()
        content_lower = current_content.lower()
        prev_lower = (task.last_content or "").lower()
        # Trigger if keyword now present (and wasn't before) OR now absent (and was before)
        keyword_now = keyword_lower in content_lower
        keyword_was = keyword_lower in prev_lower
        if keyword_now != keyword_was:
            triggered = "出现" if keyword_now else "消失"
            return True, f"keyword_{triggered}", f"关键词「{task.keyword}」{triggered}"
        return False, "", ""

    elif task.mode == MODE_SELECTOR:
        if not task.selector:
            return False, "", ""
        curr_items = extract_by_selector(current_content, task.selector)
        prev_items = task.last_content or ""
        if curr_items != prev_items:
            return True, "selector_changed", f"选择器内容变化: {curr_items[:100]}"
        return False, "", ""

    elif task.mode == MODE_REGEX:
        if not task.regex:
            return False, "", ""
        curr_match = extract_by_regex(current_content, task.regex)
        prev_match = task.last_content or ""
        if curr_match != prev_match:
            return True, "regex_matched", f"正则匹配变化: {curr_match[:100]}"
        return False, "", ""

    return False, "", ""


# ─── WebMonitor class ──────────────────────────────────────────────────────────
class WebMonitor:
    def __init__(self, tier: str = "free"):
        self.tier = tier
        self.conn = _get_db()

    def add_task(
        self,
        url: str,
        name: str,
        mode: str = MODE_HASH,
        frequency: str = "24h",
        keyword: Optional[str] = None,
        selector: Optional[str] = None,
        regex: Optional[str] = None,
    ) -> dict:
        """Add or update a monitoring task."""
        now = datetime.now(timezone.utc).isoformat()

        # Check tier limit
        limit = TIER_LIMITS.get(self.tier, TIER_LIMITS["free"])
        existing = self.list_tasks()
        if len(existing) >= limit["max_urls"]:
            return {"ok": False, "error": f"{self.tier} 套餐最多监控 {limit['max_urls']} 个 URL"}

        if mode not in VALID_MODES:
            return {"ok": False, "error": f"Invalid mode. Choose: {VALID_MODES}"}

        cursor = self.conn.execute(
            """INSERT OR REPLACE INTO monitor_tasks
               (url, name, mode, frequency, keyword, selector, regex, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (url, name, mode, frequency, keyword, selector, regex, now)
        )
        self.conn.commit()
        return {"ok": True, "url": url, "name": name}

    def remove_task(self, url: str) -> dict:
        self.conn.execute("DELETE FROM monitor_tasks WHERE url = ?", (url,))
        self.conn.commit()
        return {"ok": True, "url": url}

    def list_tasks(self) -> List[dict]:
        rows = self.conn.execute(
            "SELECT url, name, mode, frequency, keyword, selector, regex, last_hash, last_content, last_check, created_at, change_count FROM monitor_tasks"
        ).fetchall()
        tasks = []
        for r in rows:
            tasks.append({
                "url": r[0], "name": r[1], "mode": r[2], "frequency": r[3],
                "keyword": r[4], "selector": r[5], "regex": r[6],
                "last_hash": r[7], "last_content": r[8], "last_check": r[9],
                "created_at": r[10], "change_count": r[11],
            })
        return tasks

    def get_task(self, url: str) -> Optional[dict]:
        rows = self.list_tasks()
        for t in rows:
            if t["url"] == url:
                return t
        return None

    def check_task(self, url: str, dry_run: bool = False) -> dict:
        """Check a single task, return change result."""
        task_data = self.get_task(url)
        if not task_data:
            return {"ok": False, "error": "Task not found"}

        task = MonitorTask.from_dict(task_data)
        interval = FREQUENCY_SECONDS.get(task.frequency, 86400)

        # Check frequency
        if task.last_check and not dry_run:
            last_ts = datetime.fromisoformat(task.last_check.replace("Z", "+00:00"))
            elapsed = (datetime.now(timezone.utc) - last_ts).total_seconds()
            if elapsed < interval:
                remaining = int(interval - elapsed)
                return {"ok": True, "skipped": True, "reason": f"检查间隔未到，还剩 {remaining}s"}

        # Fetch page
        html = fetch_page(task.url)
        if not html:
            return {"ok": False, "error": "Failed to fetch page"}

        # Detect change
        changed, change_type, detail = detect_change(task, html)

        if dry_run:
            return {
                "ok": True, "changed": changed, "type": change_type, "detail": detail,
                "html_length": len(html)
            }

        now = datetime.now(timezone.utc).isoformat()
        new_hash = compute_hash(html)

        if changed:
            # Log change
            self.conn.execute(
                """INSERT INTO change_logs (url, name, detected_at, change_type, detail, mode)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (task.url, task.name, now, change_type, detail, task.mode)
            )
            # Update task
            self.conn.execute(
                """UPDATE monitor_tasks SET last_hash=?, last_content=?, last_check=?, change_count=change_count+1 WHERE url=?""",
                (new_hash, html, now, task.url)
            )
            self.conn.commit()
            return {
                "ok": True, "changed": True, "type": change_type, "detail": detail,
                "task": {"url": task.url, "name": task.name}
            }
        else:
            # Just update last_check and hash
            self.conn.execute(
                "UPDATE monitor_tasks SET last_hash=?, last_check=? WHERE url=?",
                (new_hash, now, task.url)
            )
            self.conn.commit()
            return {"ok": True, "changed": False}

    def check_all(self, on_change_callback=None) -> dict:
        """Check all tasks. Returns summary of changes."""
        tasks = self.list_tasks()
        changed_tasks = []
        for task_data in tasks:
            result = self.check_task(task_data["url"])
            if result.get("changed"):
                changed_tasks.append(result)
                if on_change_callback:
                    on_change_callback(result)

        return {
            "ok": True,
            "total": len(tasks),
            "changed": len(changed_tasks),
            "changes": changed_tasks
        }

    def get_change_logs(self, url: Optional[str] = None, limit: int = 50) -> List[dict]:
        if url:
            rows = self.conn.execute(
                "SELECT url, name, detected_at, change_type, detail, mode FROM change_logs WHERE url=? ORDER BY detected_at DESC LIMIT ?",
                (url, limit)
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT url, name, detected_at, change_type, detail, mode FROM change_logs ORDER BY detected_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [
            {"url": r[0], "name": r[1], "detected_at": r[2], "change_type": r[3], "detail": r[4], "mode": r[5]}
            for r in rows
        ]


# ─── Feishu notification ──────────────────────────────────────────────────────
def build_change_message(task_name: str, url: str, change_type: str, detail: str) -> str:
    """Build Feishu notification text."""
    emoji_map = {
        "content_changed": "🔄",
        "keyword_出现": "🔍",
        "keyword_消失": "🔍",
        "selector_changed": "🎯",
        "regex_matched": "⚙️",
    }
    emoji = emoji_map.get(change_type, "🔔")
    lines = [
        f"{emoji} **{task_name}** 有变化",
        f"URL: {url}",
        f"类型: {change_type}",
        f"详情: {detail}",
    ]
    return "\n".join(lines)


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 monitor.py <command> [args...]"}))
        sys.exit(1)

    cmd = sys.argv[1]
    monitor = WebMonitor()

    if cmd == "add":
        # python3 monitor.py add <url> <name> [mode] [frequency]
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        name = sys.argv[3] if len(sys.argv) > 3 else url
        mode = sys.argv[4] if len(sys.argv) > 4 else MODE_HASH
        freq = sys.argv[5] if len(sys.argv) > 5 else "24h"
        result = monitor.add_task(url=url, name=name, mode=mode, frequency=freq)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "remove":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = monitor.remove_task(url=url)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "list":
        tasks = monitor.list_tasks()
        print(json.dumps({"ok": True, "tasks": tasks}, ensure_ascii=False))

    elif cmd == "check":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = monitor.check_task(url)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "check-all":
        result = monitor.check_all()
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "logs":
        url = sys.argv[2] if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        logs = monitor.get_change_logs(url=url, limit=limit)
        print(json.dumps({"ok": True, "logs": logs}, ensure_ascii=False))

    elif cmd == "dry-run":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = monitor.check_task(url, dry_run=True)
        print(json.dumps(result, ensure_ascii=False))

    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()