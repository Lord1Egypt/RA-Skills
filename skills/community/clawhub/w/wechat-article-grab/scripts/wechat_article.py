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
        'wxtokenkey', 'wxuin', 'xid', 'poc_sid', 'wetest_lang'
    ]
    cookie_parts_formatted = []
    for key in cookie_parts:
        val = os.getenv(key, '')
        if val:
            cookie_parts_formatted.append(f'{key}={val}')
    cookie_value = '; '.join(cookie_parts_formatted)
    if not cookie_value:
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
    """根据 biz（Base64 fakeid）获取公众号 fakeid 和 nickname。

    biz 就是 fakeid 的 Base64 编码。直接用 biz 作为 fakeid 调用 list_ex，
    从 app_msg_list 获取公众号昵称。
    """
    import datetime
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    params = {
        "action": "list_ex",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "random": str(time.time()),
        "fakeid": biz,  # biz == base64(numeric_fakeid)
        "type": "9",
        "count": 20,  # Must use >=5, API returns empty otherwise
        "begin": "0",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": cookie,
        "Referer": "https://mp.weixin.qq.com/"
    }
    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    if data.get("base_resp", {}).get("ret") == 0 and data.get("app_msg_list"):
        nickname = data["app_msg_list"][0].get("nickname", "")
        if not nickname:
            nickname = data["app_msg_list"][0].get("title", "")[:20] + "..."
        return biz, nickname
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
    """列出公众号文章，可按时间范围筛选，支持 mptext → Cookie 降级"""
    cookie = load_cookie()

    # 策略1：mptext API（key，优先）
    try:
        from mptext_api import get_client as get_mptext_client
        mp_client = get_mptext_client()
        print(f"🔍 通过 mptext 搜索公众号: {name}")
        accounts = mp_client.search_account(name, size=5)
        if accounts:
            acc = accounts[0]
            print(f"✅ 找到公众号: {acc.nickname}\n")
            print(f"📄 获取文章列表 (前{count}篇)...")
            articles = mp_client.get_articles(acc.fakeid, begin=0, size=min(count, 20))
            if articles:
                print(f"\n✅ 获取到 {len(articles)} 篇文章:\n")
                for i, art in enumerate(articles, 1):
                    print(f"{i}. {art.title}")
                    print(f"   摘要: {art.digest}")
                    print(f"   链接: {art.link}")
                    print()
                return [{'title': a.title, 'link': a.link, 'digest': getattr(a, 'digest', '')} for a in articles]
        raise Exception("mptext无结果")
    except Exception as e:
        print(f"⚠️  mptext 方案失败，尝试 Cookie...\n")

    # 策略2：原生 API（Cookie，最后备用）
    if cookie:
        try:
            print(f"🔑 获取 token...")
            token = get_token(cookie)
            if not token:
                print("❌ 获取 token 失败")
                sys.exit(1)
            print(f"✅ Token 获取成功")

            print(f"🔍 搜索公众号: {name}")
            fakeid, nickname = search_fakeid(cookie, token, name)
            if not fakeid:
                print(f"❌ 未找到公众号: {name}")
                sys.exit(1)
            print(f"✅ 找到公众号: {nickname}\n")

            date_hint = ""
            if start_date and end_date:
                date_hint = f"，时间范围 {start_date} ~ {end_date}"
            elif start_date:
                date_hint = f"，{start_date} 之后"
            elif end_date:
                date_hint = f"，{end_date} 之前"
            print(f"📄 获取文章列表 (前{count}篇{date_hint})...")
            articles = get_article_list(cookie, token, fakeid, count, start_date, end_date)

            if articles:
                print(f"\n✅ 获取到 {len(articles)} 篇文章:\n")
                for i, art in enumerate(articles, 1):
                    print(f"{i}. {art.get('title', '无标题')}")
                    print(f"   链接: {art.get('link', '无链接')}")
                    print()
                return articles
            else:
                print("⚠️  没有找到文章")
                sys.exit(1)
        except Exception as e:
            print(f"❌ 所有方案均失败: {e}")
            sys.exit(1)
    else:
        print("❌ 所有方案均失败")
        sys.exit(1)

    try:
        from mptext_api import get_client as get_mptext_client
        mp_client = get_mptext_client()
        print(f"🔍 通过 mptext 搜索公众号: {name}")
        accounts = mp_client.search_account(name, size=5)
        if not accounts:
            print(f"❌ 未找到公众号: {name}")
            sys.exit(1)
        acc = accounts[0]
        print(f"✅ 找到公众号: {acc.nickname}\n")
        print(f"📄 获取文章列表 (前{count}篇)...")
        articles = mp_client.get_articles(acc.fakeid, begin=0, size=min(count, 20))
        if articles:
            print(f"\n✅ 获取到 {len(articles)} 篇文章:\n")
            for i, art in enumerate(articles, 1):
                print(f"{i}. {art.title}")
                print(f"   摘要: {art.digest}")
                print(f"   链接: {art.link}")
                print()
            return [{'title': a.title, 'link': a.link, 'digest': getattr(a, 'digest', '')} for a in articles]
        else:
            print("⚠️  没有找到文章")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 所有方案均失败: {e}")
        sys.exit(1)

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
    """获取公众号文章列表 + 每篇全文摘要，支持 mptext → Cookie 降级"""
    cookie = load_cookie()
    articles = []

    # 策略1：mptext API（key，优先）
    try:
        from mptext_api import get_client as get_mptext_client
        mp_client = get_mptext_client()
        print(f"🔍 通过 mptext 搜索公众号: {name}")
        accounts = mp_client.search_account(name, size=5)
        if accounts:
            acc = accounts[0]
            print(f"✅ 找到公众号: {acc.nickname}\n")
            arts = mp_client.get_articles(acc.fakeid, begin=0, size=min(count, 20))
            articles = [{'title': a.title, 'link': a.link} for a in arts]
    except Exception:
        pass

    # 策略2：原生 API（Cookie，最后备用）
    if not articles and cookie:
        try:
            token = get_token(cookie)
            if not token:
                raise Exception("token failed")
            fakeid, nickname = search_fakeid(cookie, token, name)
            if not fakeid:
                raise Exception("account not found")
            print(f"✅ 找到公众号: {nickname}\n")
            articles = get_article_list(cookie, token, fakeid, count)
        except Exception:
            articles = []

    if not articles:
        print("❌ 所有方案均失败")
        sys.exit(1)

    for i, art in enumerate(articles, 1):
        title = art.get('title', '无标题')
        link = art.get('link', '')
        print(f"{'='*60}")
        print(f"{i}. {title}")
        print(f"   链接: {link}")
        print()

        if link:
            _, content = fetch_article_by_url(link)
            if content:
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