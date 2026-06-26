#!/usr/bin/env python3
"""
微信公众号文章抓取工具（整合版）
用法:
  python3 wechat_article.py list "公众号名称" [文章数]    # 搜索文章列表
  python3 wechat_article.py fetch "<url>"                 # 抓取单篇文章正文
  python3 wechat_article.py full "公众号名称" [文章数]    # 获取列表+全文摘要
"""

import requests
import json
import sys
import re
import time
import os
from urllib.parse import urlparse, parse_qs

# Skill env file path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ENV_FILE = os.path.join(SCRIPT_DIR, "skill.env")

# Load env variables from skill.env
from dotenv import load_dotenv
load_dotenv(SKILL_ENV_FILE)

# Cookie file path (now uses skill.env)
COOKIE_FILE = os.path.join(SCRIPT_DIR, "skill.env")

def load_cookie():
    """从 skill.env 加载 Cookie（按 key=value 格式存储）"""
    import os
    cookie_parts = [
        '_qimei_fingerprint', '_qimei_uuid42', 'ua_id', 'uuid', 'RK',
        '_qimei_i_3', 'mm_lang', 'rand_info', '_qimei_i_1', 'slave_sid',
        'appmsglist_action_3948383292', 'slave_bizuin', 'bizuin', 'data_bizuin',
        '_clck', '_clsk', '_ga', '_ga_0KGGHBND6H', '_qimei_h38', 'data_ticket',
        'omgid', 'pac_uid', 'personAgree_3948383292', 'ptcz', 'slave_user',
        'wxtokenkey', 'wxuin', 'xid'
    ]
    cookie_value = ''
    for key in cookie_parts:
        val = os.getenv(key, '')
        if val:
            cookie_value += ('; ' if cookie_value else '') + val
    if not cookie_value:
        print("❌ 未找到 Cookie 配置，请检查 skill.env")
        return None
    return cookie_value

def get_token(cookie):
    """获取微信 token"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": cookie,
        "Referer": "https://mp.weixin.qq.com/"
    }
    r = requests.get("https://mp.weixin.qq.com/", headers=headers, allow_redirects=True)
    parsed = urlparse(r.url)
    params = parse_qs(parsed.query)
    return params.get('token', [None])[0]

def search_fakeid(cookie, token, name):
    """搜索公众号 fakeid"""
    url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
    params = {
        "action": "search_biz",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "random": str(time.time()),
        "query": name
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": cookie,
        "Referer": "https://mp.weixin.qq.com/"
    }
    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    if data.get("base_resp", {}).get("ret") == 0 and data.get("list"):
        return data["list"][0]["fakeid"], data["list"][0]["nickname"]
    return None, None

def get_account_by_biz(cookie, token, biz):
    """通过 biz 获取公众号信息（fakeid 和 nickname）"""
    url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
    params = {
        "action": "search_biz",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "random": str(time.time()),
        "fakeid": biz  # biz can be used as fakeid for account lookup
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": cookie,
        "Referer": "https://mp.weixin.qq.com/"
    }
    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    if data.get("base_resp", {}).get("ret") == 0 and data.get("list"):
        return data["list"][0]["fakeid"], data["list"][0]["nickname"]
    return None, None

def get_article_list(cookie, token, fakeid, count=10, start_date=None, end_date=None):
    """获取公众号文章列表，按时间倒序排列（获取足够多再排序），支持时间范围筛选"""
    import datetime
    # 解析时间范围
    start_ts = None
    end_ts = None
    if start_date:
        try:
            start_ts = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        except ValueError:
            pass
    if end_date:
        try:
            end_ts = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp()) + 86399  # 当天23:59:59
        except ValueError:
            pass
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    all_articles = []
    for begin in range(0, 500, 20):
        params = {
            "action": "list_ex",
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
            "random": str(time.time()),
            "fakeid": fakeid,
            "type": "9",
            "count": 20,
            "begin": str(begin)
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": cookie,
            "Referer": "https://mp.weixin.qq.com/"
        }
        r = requests.get(url, params=params, headers=headers)
        data = r.json()
        
        if data.get("base_resp", {}).get("ret") != 0:
            break
        items = data.get("app_msg_list", [])
        if not items:
            break
        all_articles.extend(items)
        if len(items) < 20:
            break

    # 按发布时间倒序
    all_articles.sort(key=lambda x: x.get("create_time", 0), reverse=True)

    # 时间范围筛选
    if start_ts or end_ts:
        filtered = []
        for art in all_articles:
            ct = art.get("create_time", 0)
            if start_ts and ct < start_ts:
                continue
            if end_ts and ct > end_ts:
                continue
            filtered.append(art)
        filtered_articles = filtered
    else:
        filtered_articles = all_articles

    return filtered_articles[:count]

def fetch_article_by_url(url):
    """通过 fetch_wechat_article.py 抓取单篇文章正文和标题"""
    try:
        from fetch_wechat_article import fetch_wechat_article_with_title
        title, content = fetch_wechat_article_with_title(url)
        if content.startswith("FETCH_FAILED"):
            return None, None
        return title, content
    except Exception:
        return None, None

def cmd_list(name, count=10, start_date=None, end_date=None):
    """列出公众号文章，可按时间范围筛选"""
    cookie = load_cookie()
    if not cookie:
        sys.exit(1)

    print(f"🔑 获取 token...")
    token = get_token(cookie)
    if not token:
        print("❌ 获取 token 失败，Cookie 可能已失效")
        sys.exit(1)
    print(f"✅ Token 获取成功")

    print(f"🔍 搜索公众号: {name}")
    fakeid, nickname = search_fakeid(cookie, token, name)
    if not fakeid:
        print(f"❌ 未找到公众号: {name}")
        sys.exit(1)
    print(f"✅ 找到公众号: {nickname}")

    date_hint = ""
    if start_date and end_date:
        date_hint = f"，时间范围 {start_date} ~ {end_date}"
    elif start_date:
        date_hint = f"，{start_date} 之后"
    elif end_date:
        date_hint = f"，{end_date} 之前"
    print(f"📄 获取文章列表 (前{count}篇{date_hint})...")
    articles = get_article_list(cookie, token, fakeid, count, start_date, end_date)

    if not articles:
        print("⚠️  没有找到文章")
        sys.exit(1)

    print(f"\n✅ 获取到 {len(articles)} 篇文章:\n")
    for i, art in enumerate(articles, 1):
        print(f"{i}. {art.get('title', '无标题')}")
        print(f"   链接: {art.get('link', '无链接')}")
        print()
    
    return articles

def cmd_fetch(url):
    """抓取单篇文章正文"""
    title, content = fetch_article_by_url(url)
    if not content:
        print("❌ 抓取失败，可能是被拦截或内容为空")
        sys.exit(1)
    if title:
        print(f"📄 {title}\n")
    print(content)
    return title, content

def cmd_full(name, count=5):
    """获取公众号文章列表 + 每篇全文摘要"""
    cookie = load_cookie()
    if not cookie:
        sys.exit(1)

    token = get_token(cookie)
    if not token:
        print("❌ 获取 token 失败，Cookie 可能已失效")
        sys.exit(1)

    fakeid, nickname = search_fakeid(cookie, token, name)
    if not fakeid:
        print(f"❌ 未找到公众号: {name}")
        sys.exit(1)
    print(f"✅ 找到公众号: {nickname}\n")

    articles = get_article_list(cookie, token, fakeid, count)
    if not articles:
        print("⚠️  没有找到文章")
        sys.exit(1)

    for i, art in enumerate(articles, 1):
        title = art.get('title', '无标题')
        link = art.get('link', '')
        print(f"{'='*60}")
        print(f"{i}. {title}")
        print(f"   链接: {link}")
        print()
        
        if link:
            content = fetch_article_by_url(link)
            if content:
                # 截取前800字作为预览
                preview = content[:800].strip()
                print(f"   [正文预览，前800字]\n   {preview}")
                if len(content) > 800:
                    print(f"   ...（共 {len(content)} 字）")
            else:
                print("   ⚠️  正文抓取失败")
        print()

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 wechat_article.py list  \"公众号名称\" [文章数]  # 列出文章列表")
        print("  python3 wechat_article.py fetch \"<url>\"                 # 抓取单篇文章")
        print("  python3 wechat_article.py full  \"公众号名称\" [文章数]   # 列出+抓取全文")
        sys.exit(1)

    cmd = sys.argv[1]
    start_date = None
    end_date = None

    # 解析通用参数
    for i, arg in enumerate(sys.argv):
        if arg == "--start-date" and i + 1 < len(sys.argv):
            start_date = sys.argv[i + 1]
        if arg == "--end-date" and i + 1 < len(sys.argv):
            end_date = sys.argv[i + 1]

    if cmd == "list" and len(sys.argv) >= 3:
        name = sys.argv[2]
        count = 10
        for i, arg in enumerate(sys.argv[3:]):
            if not arg.startswith("--") and arg.isdigit():
                count = int(arg)
                break
        cmd_list(name, count, start_date, end_date)
    elif cmd == "fetch" and len(sys.argv) >= 3:
        url = sys.argv[2]
        cmd_fetch(url)
    elif cmd == "full" and len(sys.argv) >= 3:
        name = sys.argv[2]
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        cmd_full(name, count)
    else:
        print("参数错误")
        print("用法:")
        print("  python3 wechat_article.py list  \"公众号名称\" [文章数]")
        print("  python3 wechat_article.py fetch \"<url>\"")
        print("  python3 wechat_article.py full  \"公众号名称\" [文章数]")
        sys.exit(1)

if __name__ == "__main__":
    main()