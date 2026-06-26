#!/usr/bin/env python3
"""
网络安全新闻爬虫 - 每小时运行，从各大安全社区RSS拉取最新文章
每条新闻单独一篇笔记，存入「网络安全新闻」笔记本
"""

import json
import os
import sys
import time
import re
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ── 配置 ──────────────────────────────────────────────────────────────────

IMA_CLIENT_ID  = os.environ.get("IMA_OPENAPI_CLIENTID", "")
IMA_API_KEY    = os.environ.get("IMA_OPENAPI_APIKEY", "")
IMA_BASE_URL   = "https://ima.qq.com/openapi/note/v1"

# 「网络安全新闻」笔记本（直接用默认笔记本，不再尝试创建 KB 文件夹）
DEFAULT_FOLDER  = "folder84710a47636688ed"   # Openclaw生成

RSS_FEEDS = [
    # ✅ 可用的 RSS 订阅
    {"name": "嘶吼",     "url": "https://www.4hou.com/feed",     "type": "rss"},
    {"name": "先知社区", "url": "https://xz.aliyun.com/feed",    "type": "rss"},
    {"name": "Seebug",   "url": "https://paper.seebug.org/rss/", "type": "rss"},
]

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
DATA_DIR      = os.path.join(BASE_DIR, "..", "data")
SEEN_DB_FILE  = os.path.join(DATA_DIR, "sec_news_seen_v2.json")
KB_ID_CACHE   = os.path.join(DATA_DIR, "sec_news_kb_folder.json")
LAST_RUN_FILE = os.path.join(DATA_DIR, "sec_news_last_run.json")

# ── 工具函数 ───────────────────────────────────────────────────────────────

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def http_get(url, timeout=15):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 SecurityNewsBot/1.0"})
    try:
        resp = urlopen(req, timeout=timeout)
        raw  = resp.read()
        for enc in ("utf-8", "gbk", "gb2312", "latin-1"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"    [WARN] 获取失败 {url}: {e}", file=sys.stderr)
        return ""

def strip_html(text):
    text = re.sub(r"<![^>]*>", "", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    for ent in ("&nbsp;", "&amp;", "&lt;", "&gt;", "&quot;", "&#39;", "&#x27;", "&#x2F;"):
        text = text.replace(ent, {"&nbsp;":" ","&amp;":"&","&lt;":"<","&gt;":">","&quot;":'"',"&#39;":"'","&#x27;":"'","&#x2F;":"/"}.get(ent, ent))
    return text.strip()

def parse_feed(raw, source_name):
    articles = []
    try:
        import feedparser
        fp = feedparser.parse(raw)
        for entry in fp.entries:
            title   = strip_html(entry.get("title", ""))
            url     = entry.get("link") or entry.get("id", "")
            summary = strip_html(entry.get("description", "") or entry.get("summary", ""))[:400]
            pub_date = ""
            for t in ("published_parsed", "updated_parsed", "created_parsed"):
                if getattr(entry, t, None):
                    pub_date = time.strftime("%Y-%m-%d", getattr(entry, t))
                    break
            articles.append({"title": title, "url": url, "summary": summary, "date": pub_date, "source": source_name})
        if articles:
            return articles
    except Exception:
        pass

    # 兜底正则
    for pat in (
        re.compile(r"<item[^>]*>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>.*?<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>.*?<pubDate>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</pubDate>.*?</item>", re.S),
        re.compile(r"<entry[^>]*>.*?<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>.*?<link[^>]*href=[\"'](.*?)[\"']*.*?<summary>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</summary>.*?<published>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</published>.*?</entry>", re.S),
    ):
        for m in pat.finditer(raw):
            title, url, desc, pub = m.groups()
            title = strip_html(title); url = strip_html(url); desc = strip_html(desc)[:400]
            pub_date = ""
            if pub:
                try:
                    from email.utils import parsedate_to_datetime
                    pub_date = parsedate_to_datetime(pub).strftime("%Y-%m-%d")
                except Exception:
                    pass
            if title and url:
                articles.append({"title": title, "url": url, "summary": desc, "date": pub_date, "source": source_name})
    return articles

# ── IMA API ────────────────────────────────────────────────────────────────

def ima_headers():
    return {
        "ima-openapi-clientid": IMA_CLIENT_ID,
        "ima-openapi-apikey":   IMA_API_KEY,
        "Content-Type":         "application/json",
    }

def ima_post(endpoint, payload):
    data = json.dumps(payload).encode("utf-8")
    req  = Request(f"{IMA_BASE_URL}/{endpoint}", data=data,
                    headers=ima_headers(), method="POST")
    try:
        with urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"    [ERROR] IMA API {endpoint}: {e}", file=sys.stderr)
        return {"code": -1, "msg": str(e)}

def ensure_kb_folder():
    """直接返回默认笔记本 folder_id"""
    return DEFAULT_FOLDER

def search_note_by_url(url):
    """按正文内容搜索已存在的笔记（URL 去重）"""
    result = ima_post("search_note_book", {
        "search_type": 1,           # 1 = 正文检索
        "query_info":  {"content": url},
        "start": 0, "end": 5,
    })
    if result.get("code") != 0:
        return None
    docs = result.get("data", {}).get("docs", [])
    return docs[0]["doc"]["basic_info"]["docid"] if docs else None

def import_doc(content, title, folder_id):
    """新建笔记，返回 doc_id 或空"""
    result = ima_post("import_doc", {
        "content":        content,
        "content_format": 1,
        "title":         title,
        "folder_id":     folder_id,
    })
    doc_id = result.get("data", {}).get("doc_id", result.get("doc_id", ""))
    if result.get("code") != 0:
        print(f"    [WARN] import_doc 失败(code={result.get('code')}): {result.get('msg','unknown')}", file=sys.stderr)
    return doc_id

def build_daily_note_content(articles, date_str):
    """渲染同一天所有文章为一篇笔记"""
    lines = [
        f"# 📰 网络安全新闻 {date_str}",
        f"",
        f"> 自动抓取 · 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} · 共 {len(articles)} 篇文章",
        "",
    ]
    for i, article in enumerate(articles, 1):
        lines.append(f"## {i}. {article['title']}")
        lines.append(f"- 来源：{article['source']} | [原文链接]({article['url']})")
        if article.get("date"):
            lines.append(f"- 日期：{article['date']}")
        if article.get("summary"):
            lines.append(f"- 摘要：{article['summary']}")
        lines.append("")
    return "\n".join(lines)

# ── 核心逻辑 ───────────────────────────────────────────────────────────────

def run():
    if not IMA_CLIENT_ID or not IMA_API_KEY:
        print("[ERROR] 缺少 IMA 凭证", file=sys.stderr)
        sys.exit(1)

    today_str     = datetime.now().strftime("%Y-%m-%d")
    allowed_dates  = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    seen_db = load_json(SEEN_DB_FILE, {})
    folder_id = ensure_kb_folder()

    print(f"[{datetime.now().isoformat()}] 开始抓取安全新闻...")
    new_count = 0
    skip_count = 0
    daily_articles = {}   # { date_str: [article, ...] }

    for feed in RSS_FEEDS:
        source = feed["name"]
        url    = feed["url"]
        print(f"  ► {source} ...", end=" ", flush=True)

        raw = http_get(url)
        if not raw:
            print("失败（无内容）")
            continue

        articles = parse_feed(raw, source)
        print(f"获得 {len(articles)} 条", end=" | ", flush=True)

        src_new = 0
        for article in articles:
            article_url = article["url"]
            if not article_url or not article["title"]:
                continue
            # 去重
            if article_url in seen_db:
                skip_count += 1
                continue
            # 日期过滤（只保留近7天的）
            date_str = article.get("date", "")
            if date_str and date_str not in allowed_dates:
                skip_count += 1
                continue

            seen_db[article_url] = date_str

            # 按日期分组
            key = date_str or today_str
            if key not in daily_articles:
                daily_articles[key] = []
            daily_articles[key].append(article)
            src_new += 1

        print(f"新增 {src_new} 条")

    # 全部抓完后，每天一篇笔记
    for date_str, articles in sorted(daily_articles.items()):
        note_title = f"📰 安全日报 {date_str}"
        content = build_daily_note_content(articles, date_str)
        doc_id = import_doc(content, note_title, folder_id)
        if doc_id:
            new_count += len(articles)
            print(f"  ► 写入：{note_title}（{len(articles)} 篇）doc_id={doc_id}")
        else:
            # 写入失败，不记入 seen_db，下次重试
            for a in articles:
                seen_db.pop(a["url"], None)

    save_json(SEEN_DB_FILE, seen_db)
    save_json(LAST_RUN_FILE, {
        "last_run":   datetime.now().isoformat(),
        "new_count":  new_count,
        "skip_count": skip_count,
    })

    print(f"\n完成！本期新增 {new_count} 条（跳过 {skip_count} 条）")
    if new_count == 0:
        print("(无新增，cron 将在下一小时再次尝试)")

if __name__ == "__main__":
    run()
