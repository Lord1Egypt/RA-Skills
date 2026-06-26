"""
重要公告检测 — 基于 Web 搜索关键词识别 HIGH/MED 利空。

v2.4 升级：
- 主源升级到 TinyFish Search (中文准确率大幅提升，能抓雪球/知乎/新浪/东财)
- gsk web_search 作为兜底
- 强日期提取：从 snippet/URL/title 中识别"公告日期"、东财公告号、X月Y日 等
- 严格 14 日时效过滤（避免 2-3 月旧公告混入)

环境变量:
    TINYFISH_API_KEY        从 https://docs.tinyfish.ai 获取（可选）
    TINYFISH_SEARCH_URL     默认 https://api.search.tinyfish.ai
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

# 关键词分级
KEYWORDS_HIGH = [
    "减持股份", "减持计划", "减持资产", "减股", "拟转让",
    "立案", "被调查", "证监会", "警示",
    "业绩预减", "业绩老", "诉讼",
    # v2.6: 解禁系列升级到 HIGH（含未来事件）
    "解禁", "限售解禁", "限售股解禁", "可流通", "限售股上市", "解禁股", "解禁日",
]
KEYWORDS_MED = [
    "限售股", "收购", "重组", "股东大会",
    "定增", "发行", "业绩预告", "终止", "处罚",
    "调查", "震荡", "出售",
]

# TinyFish 配置（环境变量 + secrets 文件 兜底）
def _load_tinyfish_key() -> str | None:
    """加载 TinyFish API key，优先环境变量，其次 secrets 文件"""
    key = os.environ.get("TINYFISH_API_KEY")
    if key:
        return key
    # 兜底：~/.openclaw/secrets/tinyfish.env 格式 KEY=VALUE
    secrets_paths = [
        os.path.expanduser("~/.openclaw/secrets/tinyfish.env"),
        os.path.expanduser("~/.config/tinyfish/api.env"),
    ]
    for p in secrets_paths:
        if os.path.exists(p):
            try:
                with open(p) as f:
                    for line in f:
                        if line.startswith("TINYFISH_API_KEY="):
                            return line.split("=", 1)[1].strip()
            except Exception:
                continue
    return None


def _extract_announcement_date(snippet: str, url: str, title: str) -> datetime | None:
    """从 snippet / URL / title 中提取公告真实日期。
    
    支持的格式：
    1. '公告日期：2026-04-14'
    2. 东财公告号 AN20260414XXXXX (前 8 位是日期)
    3. 'X月Y日'（年份按当前年推断）
    4. 标准 ISO 'YYYY-MM-DD'
    
    返回 datetime 或 None
    """
    combined = f"{title} {snippet} {url}"
    if not combined.strip():
        return None

    # 1. '公告日期：2026-04-14'
    m = re.search(r"公告日期[：:]\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})", combined)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass

    # 2. 东财公告号 AN20260414XXXXX
    m = re.search(r"AN(\d{8})", combined)
    if m:
        s = m.group(1)
        try:
            return datetime(int(s[:4]), int(s[4:6]), int(s[6:8]))
        except ValueError:
            pass

    # 3. 'X月Y日'（按当前年推断）
    m = re.search(r"(\d{1,2})月(\d{1,2})日", combined)
    if m:
        try:
            now = datetime.now()
            d = datetime(now.year, int(m.group(1)), int(m.group(2)))
            if d > now:
                d = datetime(now.year - 1, int(m.group(1)), int(m.group(2)))
            return d
        except ValueError:
            pass

    # 4. 标准 ISO 'YYYY-MM-DD'
    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", combined)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass

    return None


def _is_within_days(date_str: str, days: int) -> bool:
    """判断 'X days ago' / 'X hours ago' / 'YYYY-MM-DD' 等是否在 days 内"""
    if not date_str:
        return False
    ds_low = str(date_str).lower().strip()
    if "ago" in ds_low:
        digits = "".join(c for c in date_str if c.isdigit())
        if not digits:
            return False
        try:
            n = int(digits)
        except ValueError:
            return False
        if "hour" in ds_low or "minute" in ds_low:
            return True
        if "day" in ds_low:
            return n <= days
        if "week" in ds_low:
            return n * 7 <= days
        if "month" in ds_low:
            return n * 30 <= days
        if "year" in ds_low:
            return False
        return n <= days
    # 尝试解析 ISO / 英文日期
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y"):
        try:
            d = datetime.strptime(date_str[:11].strip(), fmt)
            return 0 <= (datetime.now() - d).days <= days
        except ValueError:
            continue
    return False


def _is_within_days_v26(date_str: str, days: int, level: str) -> bool:
    """v2.6: HIGH 级支持双向窗口（未来 30 天 + 过去 days 天）
    
    解禁、定增上市等是未来事件，不应被"过去 N 天"窗口过滤掉。
    """
    if not date_str:
        return False
    ds_low = str(date_str).lower().strip()
    if "ago" in ds_low:
        return _is_within_days(date_str, days)
    from datetime import datetime as _dt
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y"):
        try:
            d = _dt.strptime(date_str[:11].strip(), fmt)
            delta = (_dt.now() - d).days
            if level == "HIGH":
                return -30 <= delta <= days
            else:
                return 0 <= delta <= days
        except ValueError:
            continue
    return False


def _classify_title(title: str) -> tuple[str, str]:
    """识别公告等级 (HIGH/MED/LOW) 和触发关键词"""
    for kw in KEYWORDS_HIGH:
        if kw in title:
            return "HIGH", kw
    for kw in KEYWORDS_MED:
        if kw in title:
            return "MED", kw
    return "LOW", ""


def _tinyfish_search(query: str, timeout: int = 20) -> list[dict]:
    """通过 TinyFish Search API 搜索（中文优化，能跨 Cloudflare/反爬）"""
    key = _load_tinyfish_key()
    if not key:
        return []
    try:
        url = f"https://api.search.tinyfish.ai?query={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={"X-API-Key": key})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = []
        for r in data.get("results", []):
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            url_str = r.get("url", "")
            # TinyFish 不返回原生日期 → 主动提取
            date_obj = _extract_announcement_date(snippet, url_str, title)
            date_str = date_obj.strftime("%Y-%m-%d") if date_obj else ""
            items.append({
                "title": title,
                "link": url_str,
                "snippet": snippet,
                "site": r.get("site_name", ""),
                "date": date_str,
            })
        return items
    except Exception:
        return []


def _gsk_search(query: str, timeout: int = 20) -> list[dict]:
    """通过 gsk CLI 搜索（OpenClaw/Hermes 环境提供，兜底）"""
    if not shutil.which("gsk"):
        return []
    try:
        r = subprocess.run(
            ["gsk", "search", query, "--output", "json"],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode != 0 or not r.stdout:
            return []
        res = json.loads(r.stdout)
        data = res.get("data", res) if isinstance(res, dict) else {}
        return data.get("organic_results") or res.get("organic_results") or []
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        return []


def _search(query: str) -> list[dict]:
    """搜索：优先 TinyFish (中文准确率高)，没拿到结果则 gsk 兜底"""
    items = _tinyfish_search(query)
    if items:
        return items
    return _gsk_search(query)


def fetch_announcements(code: str, days: int = 14, max_results: int = 6) -> list[dict]:
    """拉取个股近 N 天重要公告。
    
    返回 list of dict {date, title, level, tag, url}
    
    数据源优先级：TinyFish Search → gsk web_search
    """
    out: list[dict] = []
    seen_titles = set()

    # v2.6: 升级查询，提升解禁/未来事件召回
    queries = [
        f"{code} 减持 计划",
        f"{code} 业绩 预告 OR 预减",
        f"{code} 解禁",                      # v2.6 简化
        f"{code} 限售股 解禁 日期",          # v2.6 找解禁日期
        f"{code} 限售股 上市 可流通",        # v2.6 未来解禁
        f"{code} 处罚 OR 调查 OR 警示",
    ]

    for q in queries:
        for item in _search(q)[:8]:
            title = item.get("title", "")
            if not title or title in seen_titles:
                continue
            level, tag = _classify_title(title)
            if level == "LOW":
                continue
            date_str = str(item.get("date", "")).strip()
            # v2.6: HIGH 级支持"未来 30 天 + 过去 days 天"双向窗口
            # 因为解禁、定增上市等是未来事件，不应被"过去 N 天"过滤掉
            if not _is_within_days_v26(date_str, days, level):
                continue
            out.append({
                "date": date_str,
                "title": title,
                "level": level,
                "tag": tag,
                "url": item.get("link", ""),
            })
            seen_titles.add(title)

    # HIGH 排前
    out.sort(key=lambda x: 0 if x["level"] == "HIGH" else 1)
    return out[:max_results]
