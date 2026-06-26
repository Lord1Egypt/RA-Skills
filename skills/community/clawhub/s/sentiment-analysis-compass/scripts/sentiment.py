#!/usr/bin/env python3
"""
Sentiment Compass —舆情监测核心引擎
AI-driven social media sentiment monitoring for Chinese platforms.
"""

import hashlib
import json
import os
import random
import re
import signal
import sqlite3
import subprocess
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

# ─── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = Path.home() / ".sentiment-compass"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "data.db"
CONFIG_PATH = DATA_DIR / "config.json"
LOG_DIR = DATA_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ─── Tier Limits ───────────────────────────────────────────────────────────────
TIER_LIMITS = {
    "FREE": {
        "max_keywords": 1, "platforms": ["xhs"],
        "daily_limit": 50, "history_days": 7,
        "report": False, "priority": False, "api": False,
        "alert_email": False, "feishu_alert": False, "pro_report": False,
    },
    "STD": {
        "max_keywords": 3, "platforms": ["xhs", "douyin"],
        "daily_limit": 300, "history_days": 30,
        "report": False, "priority": False, "api": False,
        "alert_email": True, "feishu_alert": False, "pro_report": False,
    },
    "PRO": {
        "max_keywords": 10, "platforms": ["xhs", "douyin", "weibo", "wechat"],
        "daily_limit": 1000, "history_days": 90,
        "report": True, "priority": True, "api": False,
        "alert_email": False, "feishu_alert": True, "pro_report": True,
    },
    "MAX": {
        "max_keywords": -1, "platforms": ["xhs", "douyin", "weibo", "wechat"],
        "daily_limit": -1, "history_days": -1,
        "report": True, "priority": True, "api": True,
        "alert_email": False, "feishu_alert": True, "pro_report": True,
    },
}

# ─── Platform Config ──────────────────────────────────────────────────────────
PLATFORM_CONFIG = {
    "xhs": {
        "name": "小红书",
        "search_url": "https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_explore_search",
        "search_url_fallback": "https://www.xiaohongshu.com/search_result?keyword={keyword}",
    },
    "douyin": {
        "name": "抖音",
        "search_url": "https://www.douyin.com/search/{keyword}",
    },
    "weibo": {
        "name": "微博",
        "search_url": "https://s.weibo.com/weibo?q={keyword}&typeall=1",
    },
    "wechat": {
        "name": "微信公众号",
        "search_url": "https://weixin.sogou.com/weixin?type=2&query={keyword}",
    },
}

# ─── User Agent Pool ───────────────────────────────────────────────────────────
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
]

# ─── GLM-4 API Config ──────────────────────────────────────────────────────────
GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GLM_MODEL = "glm-4-flash"

# ─── Dataclasses ──────────────────────────────────────────────────────────────
@dataclass
class Post:
    keyword: str
    platform: str          # xhs/douyin/weibo/wechat
    post_id: str
    title: str
    content: str
    author: str
    author_id: str
    likes: int = 0
    comments: int = 0
    shares: int = 0
    published_at: str = ""
    fetched_at: str = ""
    url: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Post":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class SentimentResult:
    post_id: int
    sentiment: str          # positive/neutral/negative
    score: float            # -1.0 ~ 1.0
    reason: str
    analyzed_at: str = ""

    def __post_init__(self):
        if not self.analyzed_at:
            self.analyzed_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AlertRecord:
    keyword: str
    alert_type: str         # threshold/trend
    threshold: int
    negative_count: int
    negative_rate: float
    triggered_at: str = ""
    notification_sent: int = 0

    def __post_init__(self):
        if not self.triggered_at:
            self.triggered_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Database ─────────────────────────────────────────────────────────────────
def _get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
            sentiment TEXT,
            score REAL,
            reason TEXT,
            analyzed_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS configs (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    return conn


# ─── Config ────────────────────────────────────────────────────────────────────
def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"tier": "FREE", "glm_api_key": "", "feishu_webhook": "", "smtp_config": {}}


def save_config(cfg: dict):
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


# ─── 91Skillhub Token Verification ───────────────────────────────────────────
VERIFY_URL = "https://api.yk-global.com/v1/verify"  # Fixed

VALID_PREFIXES = {
    "GEO", "PROFIT", "INV", "DATA", "MON",
    "PDF", "BANK", "CONTRACT", "EMAIL", "CONV",
    "RPT", "SENTIMENT",
}


def _get_cached(key: str) -> dict:
    """读取本地缓存（5分钟TTL）"""
    import time as _time
    cache_dir = Path.home() / ".sentiment_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / (key[:8].replace("/", "_") + ".json")
    if not cache_file.exists():
        return None
    try:
        with open(cache_file) as f:
            data = json.load(f)
        if _time.time() - data.get("_ts", 0) > 300:
            return None
        return data
    except Exception:
        return None


def _set_cached(key: str, data: dict) -> None:
    """写入本地缓存"""
    import time as _time
    cache_dir = Path.home() / ".sentiment_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / (key[:8].replace("/", "_") + ".json")
    try:
        data["_ts"] = _time.time()
        with open(cache_file, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def _map_prefix_to_tier(api_key: str) -> str:
    """Map API key prefix to tier name."""
    upper = api_key.upper()
    if "-MAX" in upper:
        return "MAX"
    if "-ENT" in upper:
        return "MAX"
    if "-PRO" in upper:
        return "PRO"
    if "-STD" in upper:
        return "STD"
    if "-BSC" in upper:
        return "BASIC"
    if "-FREE" in upper:
        return "FREE"
    return "FREE"


def verify_token(api_key: str) -> dict:
    """
    Verify API key via 91Skillhub API.
    Returns dict with keys: valid (bool), tier (str), error (str, if failed).
    On network error, degrades to FREE tier gracefully.
    """
    if not api_key:
        return {"valid": False, "tier": "FREE", "error": "No API key provided"}

    # 快速判断：不在已知前缀列表 = 外部 key，跳过验证
    prefix = api_key.split("-")[0].upper() if "-" in api_key else api_key[:4].upper()
    if prefix not in VALID_PREFIXES:
        return {"valid": False, "tier": "FREE", "error": "Not a 91Skillhub key"}

    cached = _get_cached(api_key)
    if cached:
        return cached

    try:
        req = urllib.request.Request(
            VERIFY_URL,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=b"{}",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("valid", False):
                tier = _map_prefix_to_tier(api_key)
                result = {"valid": True, "tier": tier, "prefix": data.get("prefix", ""), "plan_id": data.get("plan_id"), "quota_remaining": data.get("quota_remaining")}
                _set_cached(api_key, result)
                return result
            else:
                result = {"valid": False, "tier": "FREE",
                           "error": data.get("error", "Invalid or expired key")}
                _set_cached(api_key, result)
                return result
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8"))
            return {
                "valid": False,
                "tier": "FREE",
                "error": err_body.get("error", "HTTP " + str(e.code)),
            }
        except Exception:
            return {"valid": False, "tier": "FREE", "error": "HTTP " + str(e.code)}
    except Exception as e:
        # Network error — degrade to FREE, don't block user
        return {"valid": False, "tier": "FREE", "error": "Network error: " + str(e)}


def get_config(key: str, default=None):
    cfg = load_config()
    return cfg.get(key, default)


def set_config(key: str, value):
    cfg = load_config()
    cfg[key] = value
    save_config(cfg)


# ─── Playwright Fetcher ────────────────────────────────────────────────────────
def fetch_page(url: str, platform: str = "xhs", timeout_ms: int = 20000) -> Optional[str]:
    """
    Fetch page content using Playwright (Node.js subprocess).
    Handles anti-detection with random UA and delays.
    """
    ua = random.choice(UA_POOL)

    # Platform-specific JS
    if platform == "xhs":
        script = f"""
        const {{ chromium }} = require('playwright');
        (async () => {{
            const browser = await chromium.launch({{ headless: true }});
            const ctx = await browser.newContext({{
                userAgent: {json.dumps(ua)},
                viewport: {{ width: 1280, height: 800 }},
                locale: 'zh-CN',
            }});
            const page = await ctx.newPage();
            await page.setExtraHTTPHeaders({{ 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8' }});
            // Random delay before request
            await page.waitForTimeout({random.randint(2000, 5000)});
            await page.goto({json.dumps(url)}, {{ waitUntil: 'networkidle', timeout: {timeout_ms} }});
            // Scroll to load dynamic content
            await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2));
            await page.waitForTimeout(2000);
            await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
            await page.waitForTimeout(2000);
            const content = await page.content();
            await browser.close();
            console.log(JSON.stringify({{ ok: true, content }}));
        }})().catch(e => {{ console.log(JSON.stringify({{ ok: false, error: e.message }})); process.exit(1); }});
        """
    elif platform == "douyin":
        script = f"""
        const {{ chromium }} = require('playwright');
        (async () => {{
            const browser = await chromium.launch({{ headless: true }});
            const ctx = await browser.newContext({{
                userAgent: {json.dumps(ua)},
                viewport: {{ width: 390, height: 844 }},
                locale: 'zh-CN',
                deviceScaleFactor: 3,
            }});
            const page = await ctx.newPage();
            await page.setExtraHTTPHeaders({{ 'Accept-Language': 'zh-CN,zh;q=0.9' }});
            await page.waitForTimeout({random.randint(3000, 6000)});
            await page.goto({json.dumps(url)}, {{ waitUntil: 'domcontentloaded', timeout: {timeout_ms} }});
            // Simulate scroll for infinite scroll
            for (let i = 0; i < 3; i++) {{
                await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * (i+1) / 3));
                await page.waitForTimeout(1500);
            }}
            const content = await page.content();
            await browser.close();
            console.log(JSON.stringify({{ ok: true, content }}));
        }})().catch(e => {{ console.log(JSON.stringify({{ ok: false, error: e.message }})); process.exit(1); }});
        """
    elif platform == "weibo":
        script = f"""
        const {{ chromium }} = require('playwright');
        (async () => {{
            const browser = await chromium.launch({{ headless: true }});
            const ctx = await browser.newContext({{
                userAgent: {json.dumps(ua)},
                viewport: {{ width: 1280, height: 800 }},
                locale: 'zh-CN',
            }});
            const page = await ctx.newPage();
            await page.setExtraHTTPHeaders({{ 'Accept-Language': 'zh-CN,zh;q=0.9' }});
            await page.waitForTimeout({random.randint(2000, 5000)});
            await page.goto({json.dumps(url)}, {{ waitUntil: 'networkidle', timeout: {timeout_ms} }});
            const content = await page.content();
            await browser.close();
            console.log(JSON.stringify({{ ok: true, content }}));
        }})().catch(e => {{ console.log(JSON.stringify({{ ok: false, error: e.message }})); process.exit(1); }});
        """
    elif platform == "wechat":
        script = f"""
        const {{ chromium }} = require('playwright');
        (async () => {{
            const browser = await chromium.launch({{ headless: true }});
            const ctx = await browser.newContext({{
                userAgent: {json.dumps(ua)},
                viewport: {{ width: 1280, height: 800 }},
                locale: 'zh-CN',
            }});
            const page = await ctx.newPage();
            await page.setExtraHTTPHeaders({{ 'Accept-Language': 'zh-CN,zh;q=0.9' }});
            await page.waitForTimeout({random.randint(2000, 5000)});
            await page.goto({json.dumps(url)}, {{ waitUntil: 'networkidle', timeout: {timeout_ms} }});
            const content = await page.content();
            await browser.close();
            console.log(JSON.stringify({{ ok: true, content }}));
        }})().catch(e => {{ console.log(JSON.stringify({{ ok: false, error: e.message }})); process.exit(1); }});
        """
    else:
        script = f"""
        const {{ chromium }} = require('playwright');
        (async () => {{
            const browser = await chromium.launch({{ headless: true }});
            const page = await browser.newPage();
            await page.setExtraHTTPHeaders({{ 'Accept-Language': 'zh-CN,zh;q=0.9' }});
            await page.waitForTimeout({random.randint(2000, 5000)});
            await page.goto({json.dumps(url)}, {{ waitUntil: 'networkidle', timeout: {timeout_ms} }});
            const content = await page.content();
            await browser.close();
            console.log(JSON.stringify({{ ok: true, content }}));
        }})().catch(e => {{ console.log(JSON.stringify({{ ok: false, error: e.message }})); process.exit(1); }});
        """

    try:
        result = subprocess.run(
            ["node", "-e", script],
            capture_output=True, text=True, timeout=45
        )
        if result.returncode != 0:
            _log("WARN", f"Playwright fetch failed for {url}: {result.stderr[:200]}")
            return None
        data = json.loads(result.stdout.strip())
        if data.get("ok"):
            return data["content"]
        else:
            _log("WARN", f"Playwright returned error for {url}: {data.get('error', '')}")
    except subprocess.TimeoutExpired:
        _log("WARN", f"Playwright timeout for {url}")
    except json.JSONDecodeError:
        _log("WARN", f"Playwright invalid JSON for {url}: {result.stdout[:200]}")
    except Exception as e:
        _log("ERROR", f"Playwright exception for {url}: {e}")
    return None


# ─── Content Parsers ──────────────────────────────────────────────────────────
def parse_xhs_posts(html: str, keyword: str) -> List[Post]:
    """Parse Xiaohongshu search results from HTML."""
    from bs4 import BeautifulSoup
    posts = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        # Note cards - different possible selectors
        cards = soup.select(".note-item") or soup.select(".feeds-page .note") or soup.select("[class*='note']")
        for card in cards:
            try:
                title_el = card.select_one(".title") or card.select_one("h2") or card.select_one("[class*='title']")
                content_el = card.select_one(".desc") or card.select_one(".abstract") or card.select_one("[class*='desc']")
                author_el = card.select_one(".author") or card.select_one(".nickname") or card.select_one("[class*='author']")
                like_el = card.select_one(".like") or card.select_one("[class*='like']")
                # Try to find links
                links = card.select("a[href*='/discovery/item/']")
                url = "https://www.xiaohongshu.com" + links[0]["href"] if links else ""
                post_id_match = re.search(r'/discovery/item/([a-f0-9]+)', url)
                post_id = post_id_match.group(1) if post_id_match else hashlib.md5((title_el.text if title_el else "").encode()).hexdigest()[:12]

                posts.append(Post(
                    keyword=keyword,
                    platform="xhs",
                    post_id=post_id,
                    title=title_el.get_text(strip=True) if title_el else "",
                    content=content_el.get_text(strip=True) if content_el else "",
                    author=author_el.get_text(strip=True) if author_el else "",
                    author_id="",
                    likes=_parse_number(like_el.get_text(strip=True) if like_el else "0"),
                    comments=0, shares=0,
                    published_at="",
                    fetched_at=datetime.now(timezone.utc).isoformat(),
                    url=url,
                ))
            except Exception:
                continue
    except Exception as e:
        _log("WARN", f"XHS parse error: {e}")
    return posts


def parse_douyin_posts(html: str, keyword: str) -> List[Post]:
    """Parse Douyin search results from HTML."""
    from bs4 import BeautifulSoup
    posts = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        video_items = soup.select(".video-feed-list .video-item") or \
                      soup.select("[class*='video']") or \
                      soup.select("li[data-e2e='video-list-item']")
        for item in video_items:
            try:
                title_el = item.select_one(".title") or item.select_one("h3") or item.select_one("[class*='title']")
                author_el = item.select_one(".author") or item.select_one("[class*='author']")
                like_el = item.select_one(".like-count") or item.select_one("[class*='like']")
                links = item.select("a[href*='/video/']")
                url = "https://www.douyin.com" + links[0]["href"] if links else ""
                post_id_match = re.search(r'/video/(\d+)', url)
                post_id = post_id_match.group(1) if post_id_match else hashlib.md5((title_el.text if title_el else "").encode()).hexdigest()[:12]

                posts.append(Post(
                    keyword=keyword,
                    platform="douyin",
                    post_id=post_id,
                    title=title_el.get_text(strip=True) if title_el else "",
                    content="",  # Douyin content requires video page
                    author=author_el.get_text(strip=True) if author_el else "",
                    author_id="",
                    likes=_parse_number(like_el.get_text(strip=True) if like_el else "0"),
                    comments=0, shares=0,
                    published_at="",
                    fetched_at=datetime.now(timezone.utc).isoformat(),
                    url=url,
                ))
            except Exception:
                continue
    except Exception as e:
        _log("WARN", f"Douyin parse error: {e}")
    return posts


def parse_weibo_posts(html: str, keyword: str) -> List[Post]:
    """Parse Weibo search results from HTML."""
    from bs4 import BeautifulSoup
    posts = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".card-feed") or soup.select(".wb-item") or soup.select("[class*='feed']")
        for item in items:
            try:
                content_el = item.select_one(".content") or item.select_one("[class*='content']")
                author_el = item.select_one(".name") or item.select_one("[class*='name']")
                like_el = item.select_one(".like") or item.select_one("[class*='like']")
                links = item.select("a[href*='/detail']")
                url = "https://weibo.com" + links[0]["href"] if links else ""
                post_id_match = re.search(r'/detail/(\w+)', url)

                # Get text content
                text_parts = []
                if content_el:
                    for p in content_el.select("p"):
                        text_parts.append(p.get_text(strip=True))
                title_text = text_parts[0][:80] if text_parts else ""

                posts.append(Post(
                    keyword=keyword,
                    platform="weibo",
                    post_id=post_id_match.group(1) if post_id_match else hashlib.md5((title_text).encode()).hexdigest()[:12],
                    title=title_text,
                    content="\n".join(text_parts),
                    author=author_el.get_text(strip=True) if author_el else "",
                    author_id="",
                    likes=_parse_number(like_el.get_text(strip=True) if like_el else "0"),
                    comments=0, shares=0,
                    published_at="",
                    fetched_at=datetime.now(timezone.utc).isoformat(),
                    url=url,
                ))
            except Exception:
                continue
    except Exception as e:
        _log("WARN", f"Weibo parse error: {e}")
    return posts


def parse_wechat_posts(html: str, keyword: str) -> List[Post]:
    """Parse WeChat public account articles from Sogou."""
    from bs4 import BeautifulSoup
    posts = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".news-box .news-list li") or \
                soup.select("[class*='article']") or \
                soup.select(".weui-article")
        for item in items:
            try:
                title_el = item.select_one(".tit") or item.select_one("h3") or item.select_one("[class*='title']")
                digest_el = item.select_one(".txt") or item.select_one(".abstract") or item.select_one("[class*='digest']")
                author_el = item.select_one(".account") or item.select_one("[class*='account']")
                date_el = item.select_one(".date") or item.select_one("[class*='date']")
                links = item.select("a[href]")
                url = links[0]["href"] if links else ""
                post_id = hashlib.md5((title_el.get_text(strip=True) if title_el else "").encode()).hexdigest()[:12]

                posts.append(Post(
                    keyword=keyword,
                    platform="wechat",
                    post_id=post_id,
                    title=title_el.get_text(strip=True) if title_el else "",
                    content=digest_el.get_text(strip=True) if digest_el else "",
                    author=author_el.get_text(strip=True) if author_el else "",
                    author_id="",
                    likes=0, comments=0, shares=0,
                    published_at=date_el.get_text(strip=True) if date_el else "",
                    fetched_at=datetime.now(timezone.utc).isoformat(),
                    url=url,
                ))
            except Exception:
                continue
    except Exception as e:
        _log("WARN", f"WeChat parse error: {e}")
    return posts


def _parse_number(text: str) -> int:
    """Parse Chinese number format (1.2万, 3.5万) to integer."""
    text = text.strip().replace(",", "")
    if not text:
        return 0
    if "万" in text:
        try:
            return int(float(text.replace("万", "")) * 10000)
        except ValueError:
            return 0
    try:
        return int(float(text))
    except ValueError:
        return 0


# ─── GLM-4 Sentiment Analysis ──────────────────────────────────────────────────
def analyze_with_glm4(text: str, api_key: str = "") -> Optional[SentimentResult]:
    """Call GLM-4 API for sentiment analysis."""
    if not api_key:
        api_key = get_config("glm_api_key", "")
    if not api_key:
        return None

    # Truncate text
    text = text.strip()[:1500]

    prompt = f"""你是一个专业的中文情感分析模型。请分析以下文本的情感倾向。

要求：
1. 只输出JSON格式，不要任何其他文字
2. JSON包含三个字段：sentiment（positive/neutral/negative）、score（-1.0到1.0之间的浮点数）、reason（简短原因，20字以内）
3. 正面：score > 0.1，中性：-0.1 <= score <= 0.1，负面：score < -0.1

待分析文本：
{text}

请直接输出JSON："""

    try:
        payload = {
            "model": GLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 256,
        }
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", GLM_API_URL,
             "-H", f"Authorization: Bearer {api_key}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload, ensure_ascii=False)],
            capture_output=True, text=True, timeout=30
        )
        resp = json.loads(result.stdout)
        content = resp["choices"][0]["message"]["content"].strip()
        # Try to extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        data = json.loads(content.strip())
        return SentimentResult(
            post_id=0,  # Will be set by caller
            sentiment=data["sentiment"],
            score=float(data["score"]),
            reason=data["reason"],
        )
    except Exception as e:
        _log("WARN", f"GLM-4 analysis failed: {e}")
        return None


def rule_based_sentiment(text: str) -> SentimentResult:
    """
    Rule-based fallback sentiment analysis (no API needed).
    Used when API key is not configured or fails.
    """
    text_lower = text.lower()

    # Positive keywords
    positive_words = [
        "好", "棒", "赞", "优秀", "出色", "完美", "喜欢", "爱", "推荐", "值得",
        "满意", "开心", "高兴", "漂亮", "美", "帅", "酷", "牛", "强", "实惠",
        "划算", "便宜", "性价比", "良心", "负责", "认真", "专业", "有用", "有效",
        "惊喜", "惊艳", "超值", "物超所值", "方便", "简单", "轻松", "舒适", "舒服",
        "喜欢", "爱了", "太爱", "强烈推荐", "种草", "安利的", "回购", "一直用",
        "很好", "真的不错", "太棒了", "绝了", "yyds", "永远的神",
    ]
    # Negative keywords
    negative_words = [
        "差", "烂", "垃圾", "废物", "骗", "骗人", "假", "假货", "坑", "坑人",
        "失望", "太差", "糟糕", "恶心", "难看", "丑", "后悔", "不值", "浪费",
        "麻烦", "难用", "太差", "劣质", "无良", "奸商", "欺骗", "欺诈", "虚假",
        "投诉", "曝光", "维权", "质量差", "服务差", "态度差", "骗子", "无赖",
        "垃圾", "废物", "有病", "神经病", "白痴", "智障", "无语", "醉了", "吐了",
        "再也不", "不会再来", "一生黑", "拉黑", "差评", "一分", "负分",
    ]
    # Intensifiers
    intensifiers = ["非常", "特别", "极其", "超级", "太", "真", "超", "巨", "无比", "相当"]

    # Count hits using character n-grams (fallback when jieba unavailable)
    pos_count = 0
    neg_count = 0
    intensifier = False

    try:
        import jieba
        words = jieba.lcut(text)
    except ImportError:
        # Fallback: character-based word matching
        words = []
        i = 0
        while i < len(text):
            matched = False
            # Try 2-char and 3-char words
            for length in [3, 2]:
                if i + length <= len(text):
                    word = text[i:i+length]
                    words.append(word)
                    i += length
                    matched = True
                    break
            if not matched:
                i += 1

    for i, word in enumerate(words):
        for iw in intensifiers:
            if iw in word:
                intensifier = True
                break
        for pw in positive_words:
            if pw in word:
                pos_count += 2 if intensifier else 1
        for nw in negative_words:
            if nw in word:
                neg_count += 2 if intensifier else 1

    # Negation check: only flip if actual negation phrase detected
    # Don't flip when negation char is part of another word (e.g. "非常" contains "非" but means "very")
    negation_phrases = [
        r"^不[好不好对行能错]",     # 不好/不对/不行/不能/不错 — actual negations
        r"^没[有得错好]",            # 没有/没得/没错/没好 — actual negations
        r"^无所谓",                  # 无所谓
        r"^别[买买|想|再]",          # 别买/别想/别再 — actual negations
        r"^休想",                    # 休想
        r"^未[经完成]",              # 未完成/未经 — actual negations
    ]
    # Anti-patterns: phrases that START with a negation char but are actually positive/intensifiers
    non_negation_starters = [
        r"^非常", r"^无比", r"^相当", r"^超级", r"^特别", r"^极其",
        r"^不但", r"^不仅", r"^除非", r"^无论", r"^莫非", r"^非凡",
    ]
    negated = False
    # Check if starts with a non-negation intensifier first
    for pattern in non_negation_starters:
        if re.search(pattern, text_lower):
            negated = False
            break
    else:
        # No intensifier found — check for actual negation patterns
        for pattern in negation_phrases:
            if re.search(pattern, text_lower):
                negated = True
                break
    if negated:
        pos_count, neg_count = neg_count, pos_count

    total = pos_count + neg_count
    if total == 0:
        return SentimentResult(post_id=0, sentiment="neutral", score=0.0, reason="无法判断情感倾向")

    score = (pos_count - neg_count) / total
    score = max(-1.0, min(1.0, score))

    if score > 0.1:
        sentiment = "positive"
    elif score < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    if pos_count > 0 and neg_count == 0:
        reason = f"检测到{pos_count}个正面词"
    elif neg_count > 0 and pos_count == 0:
        reason = f"检测到{neg_count}个负面词"
    else:
        reason = f"正面{pos_count}词 vs 负面{neg_count}词"

    return SentimentResult(post_id=0, sentiment=sentiment, score=score, reason=reason)


def batch_analyze_with_glm4(texts: List[str], api_key: str = "") -> List[dict]:
    """Batch analyze multiple texts with GLM-4 to save API calls."""
    if not api_key:
        api_key = get_config("glm_api_key", "")
    if not api_key:
        return [rule_based_sentiment(t).to_dict() for t in texts]

    # Prepare batch prompt
    items_text = "\n".join(
        f"[{i+1}] {t[:200]}" for i, t in enumerate(texts)
    )
    prompt = f"""你是一个专业的中文情感分析模型。请批量分析以下文本的情感倾向。

要求：
1. 只输出JSON格式数组，不要任何其他文字
2. 每个元素包含：index（从1开始）、sentiment（positive/neutral/negative）、score（-1.0到1.0）、reason（20字以内）
3. 正面：score > 0.1，中性：-0.1 <= score <= 0.1，负面：score < -0.1

待分析文本：
{items_text}

直接输出JSON数组："""

    try:
        payload = {
            "model": GLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 2048,
        }
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", GLM_API_URL,
             "-H", f"Authorization: Bearer {api_key}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload, ensure_ascii=False)],
            capture_output=True, text=True, timeout=60
        )
        resp = json.loads(result.stdout)
        content = resp["choices"][0]["message"]["content"].strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        results = json.loads(content.strip())
        return results
    except Exception as e:
        _log("WARN", f"GLM-4 batch analysis failed: {e}")
        return [{"index": i+1, "sentiment": "neutral", "score": 0.0, "reason": "API失败"} for i in range(len(texts))]


# ─── Logging ──────────────────────────────────────────────────────────────────
def _log(level: str, msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    line = f"[{ts}] [{level}] {msg}"
    print(line, flush=True)
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ─── SentimentCompass Class ────────────────────────────────────────────────────
class SentimentCompass:
    def __init__(self, tier: str = "FREE", api_key: str = ""):
        # Verify token if api_key provided; degrade to FREE on failure
        if api_key:
            result = verify_token(api_key)
            if result["valid"]:
                self.tier = result["tier"]
            else:
                self.tier = "FREE"
        else:
            self.tier = tier.upper()
        self.conn = _get_db()
        self.config = load_config()
        self.limits = TIER_LIMITS.get(self.tier, TIER_LIMITS["FREE"])

    # ── Task Management ──────────────────────────────────────────────────────

    def add_keyword(
        self,
        keyword: str,
        platforms: List[str],
        frequency: str = "daily",
        priority: int = 0,
        alert_threshold: int = 5,
        alert_channels: str = "",
    ) -> dict:
        """Add or update a monitoring keyword."""
        now = datetime.now(timezone.utc).isoformat()

        # Check tier limit
        existing = self.list_tasks()
        max_kw = self.limits["max_keywords"]
        if max_kw != -1 and len(existing) >= max_kw:
            return {"ok": False, "error": f"{self.tier} 套餐最多监控 {max_kw} 个关键词"}

        # Validate platforms
        allowed = self.limits["platforms"]
        for p in platforms:
            if p not in allowed:
                return {"ok": False, "error": f"{self.tier} 套餐不支持 {p}，可用平台：{allowed}"}

        platforms_str = ",".join(platforms)
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO tasks
                (keyword, platforms, frequency, priority, status, created_at, alert_threshold, alert_channels)
                VALUES (?, ?, ?, ?, 'active', ?, ?, ?)
            """, (keyword, platforms_str, frequency, priority, now, alert_threshold, alert_channels))
            self.conn.commit()
            return {"ok": True, "keyword": keyword, "platforms": platforms}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def remove_keyword(self, keyword: str) -> dict:
        self.conn.execute("DELETE FROM tasks WHERE keyword = ?", (keyword,))
        self.conn.commit()
        return {"ok": True, "keyword": keyword}

    def pause_keyword(self, keyword: str) -> dict:
        self.conn.execute("UPDATE tasks SET status='paused' WHERE keyword=?", (keyword,))
        self.conn.commit()
        return {"ok": True, "keyword": keyword}

    def resume_keyword(self, keyword: str) -> dict:
        self.conn.execute("UPDATE tasks SET status='active' WHERE keyword=?", (keyword,))
        self.conn.commit()
        return {"ok": True, "keyword": keyword}

    def list_tasks(self) -> List[dict]:
        rows = self.conn.execute(
            "SELECT keyword, platforms, frequency, priority, status, created_at, last_crawl_at, alert_threshold, alert_channels FROM tasks"
        ).fetchall()
        return [
            {
                "keyword": r[0], "platforms": r[1].split(","),
                "frequency": r[2], "priority": r[3], "status": r[4],
                "created_at": r[5], "last_crawl_at": r[6],
                "alert_threshold": r[7], "alert_channels": r[8],
            }
            for r in rows
        ]

    def get_task(self, keyword: str) -> Optional[dict]:
        for t in self.list_tasks():
            if t["keyword"] == keyword:
                return t
        return None

    # ── Crawling ──────────────────────────────────────────────────────────────

    def crawl_keyword(self, keyword: str, platforms: List[str] = None) -> dict:
        """Crawl all platforms for a keyword, save posts to DB."""
        task = self.get_task(keyword)
        if not task:
            return {"ok": False, "error": f"Keyword '{keyword}' not found"}
        if task["status"] != "active":
            return {"ok": False, "error": f"Task '{keyword}' is {task['status']}"}

        if platforms is None:
            platforms = task["platforms"]

        daily_limit = self.limits["daily_limit"]
        all_posts = []

        for platform in platforms:
            cfg = PLATFORM_CONFIG.get(platform, {})
            search_url = cfg.get("search_url", "").format(keyword=keyword)
            limit_per_platform = daily_limit // len(platforms) if daily_limit > 0 else 1000

            _log("INFO", f"Crawling {platform} for '{keyword}' from {search_url}")

            # Respect rate limits
            time.sleep(random.uniform(3, 8))

            html = fetch_page(search_url, platform=platform)

            if not html:
                _log("WARN", f"Failed to fetch {platform} for '{keyword}'")
                continue

            # Parse posts
            if platform == "xhs":
                posts = parse_xhs_posts(html, keyword)
            elif platform == "douyin":
                posts = parse_douyin_posts(html, keyword)
            elif platform == "weibo":
                posts = parse_weibo_posts(html, keyword)
            elif platform == "wechat":
                posts = parse_wechat_posts(html, keyword)
            else:
                posts = []

            # Limit posts
            posts = posts[:limit_per_platform]
            all_posts.extend(posts)

            _log("INFO", f"  {platform}: found {len(posts)} posts for '{keyword}'")

        # Save to DB
        saved_count = 0
        for post in all_posts:
            try:
                self.conn.execute("""
                    INSERT OR IGNORE INTO posts
                    (keyword, platform, post_id, title, content, author, author_id, likes, comments, shares, published_at, fetched_at, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (post.keyword, post.platform, post.post_id, post.title, post.content,
                      post.author, post.author_id, post.likes, post.comments, post.shares,
                      post.published_at, post.fetched_at, post.url))
                saved_count += 1
            except Exception:
                pass
        self.conn.commit()

        # Update last crawl time
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute("UPDATE tasks SET last_crawl_at=? WHERE keyword=?", (now, keyword))
        self.conn.commit()

        return {
            "ok": True, "keyword": keyword,
            "total_posts": len(all_posts),
            "saved": saved_count,
            "platforms": {p: len([x for x in all_posts if x.platform == p]) for p in platforms},
        }

    def crawl_all(self) -> dict:
        """Crawl all active tasks."""
        tasks = self.list_tasks()
        active = [t for t in tasks if t["status"] == "active"]
        results = []
        for task in active:
            r = self.crawl_keyword(task["keyword"])
            results.append(r)
        return {"ok": True, "total": len(active), "results": results}

    # ── Sentiment Analysis ───────────────────────────────────────────────────

    def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment of a single text."""
        api_key = self.config.get("glm_api_key", "")
        if api_key:
            result = analyze_with_glm4(text, api_key)
            if result:
                return result.to_dict()
        # Fallback to rule-based
        result = rule_based_sentiment(text)
        return result.to_dict()

    def batch_analyze(self, texts: List[str]) -> List[dict]:
        """Batch analyze multiple texts."""
        api_key = self.config.get("glm_api_key", "")
        if api_key:
            results = batch_analyze_with_glm4(texts, api_key)
            return results
        # Fallback
        return [rule_based_sentiment(t).to_dict() for t in texts]

    def analyze_pending_posts(self, keyword: str = None, batch_size: int = 20) -> dict:
        """Analyze all unanalyzed posts for a keyword."""
        api_key = self.config.get("glm_api_key", "")

        if keyword:
            rows = self.conn.execute("""
                SELECT p.id, p.title || ' ' || p.content
                FROM posts p
                LEFT JOIN analyses a ON p.id = a.post_id
                WHERE p.keyword = ? AND a.id IS NULL AND (p.title IS NOT NULL OR p.content IS NOT NULL)
                LIMIT ?
            """, (keyword, batch_size)).fetchall()
        else:
            rows = self.conn.execute("""
                SELECT p.id, p.title || ' ' || p.content
                FROM posts p
                LEFT JOIN analyses a ON p.id = a.post_id
                WHERE a.id IS NULL AND (p.title IS NOT NULL OR p.content IS NOT NULL)
                LIMIT ?
            """, (batch_size,)).fetchall()

        if not rows:
            return {"ok": True, "analyzed": 0, "message": "没有待分析的帖子"}

        ids = [r[0] for r in rows]
        texts = [r[1] if r[1] else "无内容" for r in rows]

        # Batch analyze
        analyses = self.batch_analyze(texts)

        now = datetime.now(timezone.utc).isoformat()
        analyzed_count = 0
        for i, row_id in enumerate(ids):
            try:
                a = analyses[i]
                sentiment = a.get("sentiment", "neutral")
                score = float(a.get("score", 0.0))
                reason = a.get("reason", "")
                self.conn.execute("""
                    INSERT INTO analyses (post_id, sentiment, score, reason, analyzed_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (row_id, sentiment, score, reason, now))
                analyzed_count += 1
            except Exception as e:
                _log("WARN", f"Failed to save analysis for post {row_id}: {e}")
        self.conn.commit()

        return {"ok": True, "analyzed": analyzed_count, "total": len(rows)}

    # ── Report Generation ─────────────────────────────────────────────────────

    def generate_report(self, keyword: str, days: int = 7) -> dict:
        """Generate a sentiment report for a keyword."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        # Get post counts by platform and sentiment
        stats_rows = self.conn.execute("""
            SELECT p.platform, a.sentiment, COUNT(*) as cnt
            FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword = ? AND p.fetched_at >= ?
            GROUP BY p.platform, a.sentiment
        """, (keyword, cutoff)).fetchall()

        # Total posts
        total = self.conn.execute("""
            SELECT COUNT(*) FROM posts WHERE keyword=? AND fetched_at >= ?
        """, (keyword, cutoff)).fetchone()[0]

        # Sentiment breakdown
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        platform_counts = {}
        for platform, sentiment, cnt in stats_rows:
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + cnt
            platform_counts[platform] = platform_counts.get(platform, 0) + cnt

        # Recent negative posts
        neg_posts = self.conn.execute("""
            SELECT p.title, p.platform, p.author, p.url, p.likes, a.score, a.reason
            FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword=? AND a.sentiment='negative' AND p.fetched_at >= ?
            ORDER BY p.fetched_at DESC LIMIT 10
        """, (keyword, cutoff)).fetchall()

        # Top positive posts
        pos_posts = self.conn.execute("""
            SELECT p.title, p.platform, p.author, p.url, p.likes, a.score, a.reason
            FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword=? AND a.sentiment='positive' AND p.fetched_at >= ?
            ORDER BY a.score DESC LIMIT 5
        """, (keyword, cutoff)).fetchall()

        # Build report
        total_analyzed = sum(sentiment_counts.values())
        neg_rate = (sentiment_counts["negative"] / total_analyzed * 100) if total_analyzed > 0 else 0
        pos_rate = (sentiment_counts["positive"] / total_analyzed * 100) if total_analyzed > 0 else 0
        neu_rate = (sentiment_counts["neutral"] / total_analyzed * 100) if total_analyzed > 0 else 0

        # Trend (daily counts)
        daily_rows = self.conn.execute("""
            SELECT DATE(p.fetched_at) as day, a.sentiment, COUNT(*) as cnt
            FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword=? AND p.fetched_at >= ?
            GROUP BY day, a.sentiment
            ORDER BY day
        """, (keyword, cutoff)).fetchall()

        trend = {}
        for day, sentiment, cnt in daily_rows:
            if day not in trend:
                trend[day] = {"positive": 0, "neutral": 0, "negative": 0}
            trend[day][sentiment] = cnt

        # AI summary
        summary_text = self._generate_ai_summary(keyword, sentiment_counts, total, neg_rate, trend)

        report = {
            "keyword": keyword,
            "period": f"最近{days}天",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stats": {
                "total_posts": total,
                "analyzed": total_analyzed,
                "sentiment": {
                    "positive": {"count": sentiment_counts["positive"], "rate": round(pos_rate, 1)},
                    "neutral": {"count": sentiment_counts["neutral"], "rate": round(neu_rate, 1)},
                    "negative": {"count": sentiment_counts["negative"], "rate": round(neg_rate, 1)},
                },
                "platform": platform_counts,
                "trend": trend,
            },
            "top_negative": [
                {"title": r[0], "platform": r[1], "author": r[2], "url": r[3],
                 "likes": r[4], "score": r[5], "reason": r[6]}
                for r in neg_posts
            ],
            "top_positive": [
                {"title": r[0], "platform": r[1], "author": r[2], "url": r[3],
                 "likes": r[4], "score": r[5], "reason": r[6]}
                for r in pos_posts
            ],
            "summary": summary_text,
        }
        return report

    def _generate_ai_summary(self, keyword: str, sentiment_counts: dict, total: int, neg_rate: float, trend: dict) -> str:
        """Generate AI-powered text summary using GLM-4 if available."""
        api_key = self.config.get("glm_api_key", "")
        if not api_key:
            return self._rule_summary(keyword, sentiment_counts, total, neg_rate)

        prompt = f"""请根据以下舆情数据，为关键词「{keyword}」生成一段简洁的舆情摘要（100字以内）。

数据：
- 最近7天总帖子数：{total}
- 正面帖子：{sentiment_counts['positive']}条
- 中性帖子：{sentiment_counts['neutral']}条
- 负面帖子：{sentiment_counts['negative']}条
- 负面率：{neg_rate:.1f}%

请直接输出中文摘要，不需要任何格式标记。"""

        try:
            payload = {
                "model": GLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "max_tokens": 200,
            }
            result = subprocess.run(
                ["curl", "-s", "-X", "POST", GLM_API_URL,
                 "-H", f"Authorization: Bearer {api_key}",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps(payload, ensure_ascii=False)],
                capture_output=True, text=True, timeout=20
            )
            resp = json.loads(result.stdout)
            return resp["choices"][0]["message"]["content"].strip()
        except Exception:
            return self._rule_summary(keyword, sentiment_counts, total, neg_rate)

    def _rule_summary(self, keyword: str, sentiment_counts: dict, total: int, neg_rate: float) -> str:
        """Rule-based summary when no API."""
        if total == 0:
            return f"暂无「{keyword}」的相关舆情数据。"
        neg = sentiment_counts["negative"]
        pos = sentiment_counts["positive"]
        if neg_rate > 30:
            return f"「{keyword}」近期{total}条舆情中，负面占{neg_rate:.1f}%，需重点关注。"
        elif neg_rate > 15:
            return f"「{keyword}」舆情整体平稳，负面率{neg_rate:.1f}%，正面{pos}条。"
        else:
            return f"「{keyword}」舆情正面向好，负面率仅{neg_rate:.1f}%，正面占主导。"

    # ── Alerting ──────────────────────────────────────────────────────────────

    def check_alerts(self, keyword: str) -> Optional[dict]:
        """Check if alert threshold is exceeded for a keyword."""
        task = self.get_task(keyword)
        if not task:
            return None

        threshold = task.get("alert_threshold", 5)
        today = datetime.now().strftime("%Y-%m-%d")
        cutoff = f"{today}T00:00:00+00:00"

        neg_count = self.conn.execute("""
            SELECT COUNT(*) FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword=? AND a.sentiment='negative' AND p.fetched_at>=?
        """, (keyword, cutoff)).fetchone()[0]

        total_today = self.conn.execute("""
            SELECT COUNT(*) FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword=? AND p.fetched_at>=?
        """, (keyword, cutoff)).fetchone()[0]

        neg_rate = (neg_count / total_today * 100) if total_today > 0 else 0

        if neg_count >= threshold:
            now = datetime.now(timezone.utc).isoformat()
            alert_type = "threshold"
            self.conn.execute("""
                INSERT INTO alerts (keyword, alert_type, threshold, negative_count, negative_rate, triggered_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (keyword, alert_type, threshold, neg_count, neg_rate, now))
            self.conn.commit()

            # Mark notification as pending
            self.conn.execute("""
                UPDATE alerts SET notification_sent=0
                WHERE keyword=? AND triggered_at=? AND notification_sent=0
            """, (keyword, now))
            self.conn.commit()

            return {
                "keyword": keyword,
                "alert_type": alert_type,
                "threshold": threshold,
                "negative_count": neg_count,
                "negative_rate": round(neg_rate, 1),
                "total_today": total_today,
                "triggered_at": now,
            }
        return None

    def check_all_alerts(self) -> List[dict]:
        """Check alerts for all active tasks."""
        tasks = self.list_tasks()
        alerts = []
        for task in tasks:
            if task["status"] != "active":
                continue
            alert = self.check_alerts(task["keyword"])
            if alert:
                alerts.append(alert)
        return alerts

    def send_feishu_alert(self, alert: dict):
        """Send alert via Feishu group bot."""
        webhook = self.config.get("feishu_webhook", "")
        if not webhook:
            _log("WARN", "Feishu webhook not configured")
            return {"ok": False, "error": "飞书 Webhook 未配置"}

        platform_emoji = {"xhs": "📕", "douyin": "🎵", "weibo": "🌐", "wechat": "💬"}
        platforms = self.get_task(alert["keyword"])["platforms"] if self.get_task(alert["keyword"]) else []

        emoji_map = {
            "positive": "🟢", "neutral": "🟡", "negative": "🔴"
        }
        rate = alert["negative_rate"]
        if rate < 10:
            color = "green"
            rate_emoji = "🟢"
        elif rate < 25:
            color = "yellow"
            rate_emoji = "🟡"
        else:
            color = "red"
            rate_emoji = "🔴"

        body = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": f"🔴 舆情预警 | {alert['keyword']}"},
                    "template": "red" if rate >= 25 else "orange" if rate >= 15 else "yellow"
                },
                "elements": [
                    {"tag": "div", "text": {"tag": "lark_md", "content": f"**关键词**：{alert['keyword']}\n**触发时间**：{alert['triggered_at'][:19]}\n**今日负面**：{alert['negative_count']} 条（阈值：{alert['threshold']}）\n**负面率**：{rate_emoji} {rate}%\n**监测平台**：{' '.join(platform_emoji.get(p, '📌') for p in platforms)}"}},
                    {"tag": "hr"},
                    {"tag": "div", "text": {"tag": "lark_md", "content": "**📌 最新负面帖子**"}},
                ]
            }
        }

        # Add top negative posts to card
        cutoff = alert["triggered_at"][:10] + "T00:00:00+00:00"
        neg_posts = self.conn.execute("""
            SELECT p.title, p.platform, p.author, p.url, p.likes, a.reason
            FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword=? AND a.sentiment='negative' AND p.fetched_at>=?
            ORDER BY p.fetched_at DESC LIMIT 5
        """, (alert["keyword"], cutoff)).fetchall()

        for post in neg_posts:
            title = post[0][:50] + "..." if len(post[0]) > 50 else post[0]
            body["card"]["elements"].append({
                "tag": "div",
                "text": {"tag": "lark_md",
                         "content": f"• [{platform_emoji.get(post[1], '📌')}] {title}\n  — {post[2]} | 👍{post[4]} | {post[5]}"}
            })

        body["card"]["elements"].append({"tag": "hr"})
        body["card"]["elements"].append({
            "tag": "note",
            "text": {"tag": "lark_md", "content": "由舆情罗盘 Sentiment Compass 自动推送"}
        })

        try:
            result = subprocess.run(
                ["curl", "-s", "-X", "POST", webhook,
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps(body, ensure_ascii=False)],
                capture_output=True, text=True, timeout=10
            )
            resp = json.loads(result.stdout)
            if resp.get("code") == 0 or resp.get("StatusCode") == 0:
                # Mark as sent
                self.conn.execute(
                    "UPDATE alerts SET notification_sent=1 WHERE keyword=? AND triggered_at=?",
                    (alert["keyword"], alert["triggered_at"])
                )
                self.conn.commit()
                return {"ok": True}
            return {"ok": False, "error": resp}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def send_email_alert(self, alert: dict, smtp_config: dict = None):
        """Send alert via email."""
        if smtp_config is None:
            smtp_config = self.config.get("smtp_config", {})
        if not smtp_config:
            return {"ok": False, "error": "SMTP 未配置"}

        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        subject = f"🔴 舆情预警 | {alert['keyword']} — 负面 {alert['negative_count']} 条"
        body_html = f"""
        <h2>舆情预警</h2>
        <p><strong>关键词：</strong>{alert['keyword']}</p>
        <p><strong>触发时间：</strong>{alert['triggered_at']}</p>
        <p><strong>今日负面：</strong>{alert['negative_count']} 条（阈值：{alert['threshold']}）</p>
        <p><strong>负面率：</strong>{alert['negative_rate']}%</p>
        <hr>
        <p>由舆情罗盘 Sentiment Compass 自动推送</p>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_config.get("from", "")
        msg["To"] = smtp_config.get("to", "")

        msg.attach(MIMEText(body_html, "html", "utf-8"))

        try:
            server = smtplib.SMTP(smtp_config["host"], smtp_config.get("port", 587))
            server.starttls()
            server.login(smtp_config["user"], smtp_config["pass"])
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
            server.quit()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── Data Query ────────────────────────────────────────────────────────────

    def get_posts(self, keyword: str = None, platform: str = None,
                  sentiment: str = None, days: int = 7, limit: int = 50) -> List[dict]:
        """Query posts with filters."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        query = "SELECT p.*, a.sentiment, a.score, a.reason FROM posts p LEFT JOIN analyses a ON p.id=a.post_id WHERE p.fetched_at>=?"
        params = [cutoff]

        if keyword:
            query += " AND p.keyword=?"
            params.append(keyword)
        if platform:
            query += " AND p.platform=?"
            params.append(platform)
        if sentiment:
            query += " AND a.sentiment=?"
            params.append(sentiment)

        query += " ORDER BY p.fetched_at DESC LIMIT ?"
        params.append(limit)

        rows = self.conn.execute(query, params).fetchall()
        return [
            {
                "id": r[0], "keyword": r[1], "platform": r[2], "post_id": r[3],
                "title": r[4], "content": r[5], "author": r[6], "author_id": r[7],
                "likes": r[8], "comments": r[9], "shares": r[10],
                "published_at": r[11], "fetched_at": r[12], "url": r[13],
                "sentiment": r[14], "score": r[15], "reason": r[16],
            }
            for r in rows
        ]

    def get_daily_stats(self, keyword: str, days: int = 7) -> dict:
        """Get daily statistics for a keyword."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        rows = self.conn.execute("""
            SELECT DATE(p.fetched_at) as day, a.sentiment, COUNT(*) as cnt
            FROM posts p
            JOIN analyses a ON p.id = a.post_id
            WHERE p.keyword=? AND p.fetched_at>=?
            GROUP BY day, a.sentiment
            ORDER BY day
        """, (keyword, cutoff)).fetchall()

        trend = {}
        for day, sentiment, cnt in rows:
            if day not in trend:
                trend[day] = {"positive": 0, "neutral": 0, "negative": 0}
            trend[day][sentiment] = cnt

        return {"keyword": keyword, "days": days, "trend": trend}

    # ── Cleanup ───────────────────────────────────────────────────────────────

    def cleanup_old_data(self):
        """Delete posts older than history_days limit."""
        history_days = self.limits["history_days"]
        if history_days < 0:
            return  # No limit for MAX
        cutoff = (datetime.now(timezone.utc) - timedelta(days=history_days)).isoformat()
        self.conn.execute("DELETE FROM analyses WHERE post_id IN (SELECT id FROM posts WHERE fetched_at<?)", (cutoff,))
        self.conn.execute("DELETE FROM posts WHERE fetched_at<?", (cutoff,))
        self.conn.commit()

    def get_stats_summary(self) -> dict:
        """Get overall stats."""
        total_posts = self.conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        total_analyzed = self.conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
        total_tasks = self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        total_alerts = self.conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]

        sent_breakdown = self.conn.execute("""
            SELECT sentiment, COUNT(*) FROM analyses GROUP BY sentiment
        """).fetchall()

        return {
            "total_posts": total_posts,
            "total_analyzed": total_analyzed,
            "total_tasks": total_tasks,
            "total_alerts": total_alerts,
            "sentiment_breakdown": {r[0]: r[1] for r in sent_breakdown},
            "tier": self.tier,
            "limits": self.limits,
        }


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 sentiment.py <command> [args...]"}))
        sys.exit(1)

    cmd = sys.argv[1]
    compass = SentimentCompass()

    if cmd == "add":
        # python3 sentiment.py add <keyword> <platforms_csv> [frequency] [alert_threshold]
        keyword = sys.argv[2] if len(sys.argv) > 2 else ""
        platforms_str = sys.argv[3] if len(sys.argv) > 3 else "xhs"
        frequency = sys.argv[4] if len(sys.argv) > 4 else "daily"
        threshold = int(sys.argv[5]) if len(sys.argv) > 5 else 5
        platforms = [p.strip() for p in platforms_str.split(",")]
        result = compass.add_keyword(keyword, platforms, frequency, alert_threshold=threshold)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "remove":
        keyword = sys.argv[2] if len(sys.argv) > 2 else ""
        result = compass.remove_keyword(keyword)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "list":
        tasks = compass.list_tasks()
        print(json.dumps({"ok": True, "tasks": tasks}, ensure_ascii=False))

    elif cmd == "crawl":
        keyword = sys.argv[2] if len(sys.argv) > 2 else ""
        platforms_str = sys.argv[3] if len(sys.argv) > 3 else None
        platforms = [p.strip() for p in platforms_str.split(",")] if platforms_str else None
        result = compass.crawl_keyword(keyword, platforms)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "crawl-all":
        result = compass.crawl_all()
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "analyze":
        # python3 sentiment.py analyze <text>
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        result = compass.analyze_sentiment(text)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "batch-analyze":
        # python3 sentiment.py batch-analyze <file.json>
        # File contains JSON array of texts
        filepath = sys.argv[2] if len(sys.argv) > 2 else ""
        try:
            texts = json.loads(Path(filepath).read_text(encoding="utf-8"))
            results = compass.batch_analyze(texts)
            print(json.dumps(results, ensure_ascii=False))
        except Exception as e:
            print(json.dumps({"error": str(e)}))

    elif cmd == "analyze-pending":
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        result = compass.analyze_pending_posts(keyword, batch_size)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "report":
        # python3 sentiment.py report <keyword> [days]
        keyword = sys.argv[2] if len(sys.argv) > 2 else ""
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        report = compass.generate_report(keyword, days)
        print(json.dumps(report, ensure_ascii=False))

    elif cmd == "check-alerts":
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        if keyword:
            alert = compass.check_alerts(keyword)
            print(json.dumps(alert, ensure_ascii=False))
        else:
            alerts = compass.check_all_alerts()
            print(json.dumps({"ok": True, "alerts": alerts}, ensure_ascii=False))

    elif cmd == "send-feishu":
        # python3 sentiment.py send-feishu <alert_json>
        alert_str = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "{}"
        try:
            alert = json.loads(alert_str)
            result = compass.send_feishu_alert(alert)
            print(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            print(json.dumps({"error": str(e)}))

    elif cmd == "posts":
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        platform = sys.argv[3] if len(sys.argv) > 3 else None
        sentiment = sys.argv[4] if len(sys.argv) > 4 else None
        posts = compass.get_posts(keyword=keyword, platform=platform, sentiment=sentiment)
        print(json.dumps({"ok": True, "posts": posts}, ensure_ascii=False))

    elif cmd == "stats":
        stats = compass.get_stats_summary()
        print(json.dumps(stats, ensure_ascii=False))

    elif cmd == "config-get":
        key = sys.argv[2] if len(sys.argv) > 2 else ""
        val = get_config(key)
        print(json.dumps({"ok": True, "key": key, "value": val}, ensure_ascii=False))

    elif cmd == "config-set":
        # python3 sentiment.py config-set <key> <value>
        key = sys.argv[2] if len(sys.argv) > 2 else ""
        value = sys.argv[3] if len(sys.argv) > 3 else ""
        # Try to parse JSON
        try:
            value = json.loads(value)
        except Exception:
            pass
        set_config(key, value)
        print(json.dumps({"ok": True, "key": key, "value": value}, ensure_ascii=False))

    elif cmd == "cleanup":
        compass.cleanup_old_data()
        print(json.dumps({"ok": True}))

    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
