#!/home/robotli/.openclaw/venv/bin/python3
"""
侦察兵爬虫 - 六层反爬策略
架构:Fetcher(静态) → DynamicFetcher(动态) → StealthyFetcher(强反爬) → Obscura(Rust隐身) → Olostep(云端兜底) → Firecrawl(AI智能)
"""
import sys, os, json, time, random, re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# 环境
os.environ["SCRAPLING_PROXY"] = "http://127.0.0.1:7890"

# 已知的无效页面标记(HTTP 200 但内容无用)
_INVALID_MARKERS = [
    "Sina Visitor System",       # 微博访客验证页
    "passport.weibo.com",        # 微博登录页
    "passport.bilibili.com",     # B站登录页
    "accounts.google.com",       # Google 登录
    "Sign in to",                # 通用登录页
    "visitor.visitor",           # 微博访客系统 URL
]


def _is_valid_content(html: str) -> bool:
    """检查返回的 HTML 是否是有效内容(非登录页/验证页/错误页)"""
    if not html or len(html) < 500:
        return False
    for marker in _INVALID_MARKERS:
        if marker in html:
            return False
    return True


# ---- 第一层:快速 Fetcher(静态页/API) ----
def fetch_quick(url: str, timeout: int = 15) -> Optional[str]:
    """轻量级抓取:requests + cloudscraper 自动防检测"""
    from scrapling import Fetcher

    try:
        f = Fetcher()
        # Scrapling 自动处理:请求头伪装 + Cloudflare绕过 + 自适应延迟
        resp = f.get(url, timeout=timeout, follow_redirects=True)
        if resp and resp.status == 200:
            body = resp.body
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="replace")
            if _is_valid_content(body):
                return body
            print(f"    Fetcher: 返回验证页/登录页,降级...")
    except Exception as e:
        print(f"    Fetcher异常: {str(e)[:50]}")
    return None


# ---- 第二层:动态 Fetcher(SPA/JS渲染) ----
def fetch_dynamic(url: str, wait_selector: str = None, timeout: int = 20) -> Optional[str]:
    """Playwright 渲染:处理 JS 动态页面和 SPA"""
    from scrapling import DynamicFetcher

    try:
        f = DynamicFetcher()
        # fetch() timeout is in milliseconds
        resp = f.fetch(url, timeout=timeout * 1000)
        if resp and resp.status == 200:
            body = resp.body
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="replace")
            if _is_valid_content(body):
                return body
            print(f"    DynamicFetcher: 返回验证页/登录页,降级...")
    except Exception as e:
        print(f"    DynamicFetcher异常: {str(e)[:80]}")
    return None


# ---- 第三层:隐身 Fetcher(强反爬/登录墙) ----
def fetch_stealth(url: str, timeout: int = 30) -> Optional[str]:
    """全副武装:反检测 + 指纹伪装(Canvas/WebGL/WebDriver全覆盖)"""
    from scrapling import StealthyFetcher

    try:
        f = StealthyFetcher()
        # StealthyFetcher 默认已包含:
        # - 随机浏览器指纹
        # - Canvas/WebGL/Font 伪装
        # - navigator.webdriver 隐藏
        # - 真实 User-Agent 轮换
        # - Cloudflare Turnstile 绕过
        # fetch() timeout is in milliseconds
        resp = f.fetch(url, timeout=timeout * 1000)
        if resp and resp.status == 200:
            body = resp.body
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="replace")
            if _is_valid_content(body):
                return body
            print(f"    StealthyFetcher: 返回验证页/登录页,降级...")
    except Exception as e:
        print(f"    StealthyFetcher异常: {str(e)[:80]}")
    return None


# ---- 第四层:Obscura(Rust 隐身浏览器) ----
def fetch_obscura(url: str, timeout: int = 30) -> Optional[str]:
    """Obscura Rust 隐身浏览器:轻量(9MB内存) + 内置反检测 + CDP 兼容"""
    import subprocess

    obscura_bin = os.path.expanduser("~/.local/bin/obscura")
    if not os.path.isfile(obscura_bin):
        print("    Obscura未安装,跳过")
        return None

    try:
        # 用 --dump original 获取原始 HTML
        result = subprocess.run(
            [obscura_bin, "--proxy", "http://127.0.0.1:7890",
             "fetch", url, "--dump", "original", "--timeout", str(timeout)],
            capture_output=True, timeout=timeout + 10,
        )
        if result.returncode == 0 and result.stdout and len(result.stdout) > 500:
            body = result.stdout.decode("utf-8", errors="replace")
            if _is_valid_content(body):
                return body
            print(f"    Obscura: 返回验证页/登录页，降级...")
        # 降级：尝试不用 proxy
        result = subprocess.run(
            [obscura_bin, "fetch", url, "--dump", "original", "--timeout", str(timeout)],
            capture_output=True, timeout=timeout + 10,
        )
        if result.returncode == 0 and result.stdout and len(result.stdout) > 500:
            body = result.stdout.decode("utf-8", errors="replace")
            if _is_valid_content(body):
                return body
            print(f"    Obscura(无代理): 返回验证页/登录页，降级...")
    except Exception as e:
        print(f"    Obscura异常: {str(e)[:80]}")
    return None


# ---- 第六层:Firecrawl(AI 智能抓取) ----
def fetch_firecrawl(url: str, timeout: int = 30) -> Optional[str]:
    """Firecrawl CLI 抓取:输出干净 Markdown,LLM-ready"""
    import subprocess

    firecrawl_bin = "/vol1/@appcenter/nodejs_v24/bin/firecrawl"
    if not os.path.isfile(firecrawl_bin):
        print("    Firecrawl未安装,跳过")
        return None

    try:
        result = subprocess.run(
            [firecrawl_bin, "scrape", url, "--timeout", str(timeout * 1000)],
            capture_output=True, timeout=timeout + 15,
        )
        if result.returncode == 0 and result.stdout and len(result.stdout) > 100:
            return result.stdout.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"    Firecrawl异常: {str(e)[:80]}")
    return None


# ---- 第五层:Olostep API(住宅代理云端浏览器)----
def fetch_olostep(url: str, timeout: int = 30) -> Optional[str]:
    """Olostep 住宅代理云端浏览器:突破 WAF/CloudFront 强防护"""
    import requests

    OLOSTEP_API_KEY = "olostep_gGm6Y10wZgQpHKQsmqoaZaU24SHKkfPHMNef"

    try:
        headers = {"Authorization": f"Bearer {OLOSTEP_API_KEY}", "Content-Type": "application/json"}
        payload = {"url_to_scrape": url, "formats": ["html"], "wait_before_scraping": 3000}
        resp = requests.post(
            "https://api.olostep.com/v1/scrapes",
            json=payload, headers=headers,
            timeout=timeout,
            proxies={"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"},
        )
        if resp.status_code in (200, 201):
            data = resp.json()
            html = data.get("result", {}).get("html_content")
            if html and len(html) > 50:
                if _is_valid_content(html):
                    return html
                print(f"    Olostep: 返回验证页/登录页，降级...")
    except Exception as e:
        print(f"    Olostep异常: {str(e)[:80]}")
    return None

# ---- 主入口:自动降级调度 ----
def fetch(url: str, wait_selector: str = None, min_layer: int = 1) -> dict:
    """
    自动调度六层 Fetcher:
    0. 平台专用 API(B站等,直接获取结构化数据)
    1. Fetcher(快速 HTTP)
    2. DynamicFetcher(浏览器渲染)
    3. StealthyFetcher(隐身)
    4. Obscura(Rust 隐身浏览器,轻量 + 内置反检测)
    5. Olostep(住宅代理云端浏览器兜底)
    6. Firecrawl(AI 智能抓取)
    """
    result = {"url": url, "content": None, "method": None, "error": None}

    # 第零层:平台专用 API(始终尝试)
    bvid = _extract_bilibili_bvid(url)
    if bvid:
        print(f"  ▶ 尝试 B站API(结构化) ...")
        content = fetch_bilibili_video(bvid)
        if content:
            result["content"] = content
            result["method"] = "bilibili-api"
            return result

    # 第一层
    if min_layer <= 1:
        print(f"  ▶ 尝试 Fetcher(快速) ...")
        content = fetch_quick(url)
        if content:
            result["content"] = _to_str(content)
            result["method"] = "quick"
            return result

    # 第二层
    if min_layer <= 2:
        print(f"  ▶ 尝试 DynamicFetcher(浏览器) ...")
        content = fetch_dynamic(url, wait_selector)
        if content:
            result["content"] = _to_str(content)
            result["method"] = "dynamic"
            return result

    # 第三层
    if min_layer <= 3:
        print(f"  ▶ 尝试 StealthyFetcher(隐身) ...")
        content = fetch_stealth(url)
        if content:
            result["content"] = _to_str(content)
            result["method"] = "stealth"
            return result

    # 第四层:Obscura(Rust 隐身浏览器)
    if min_layer <= 4:
        print(f"  ▶ 尝试 Obscura(Rust隐身) ...")
        content = fetch_obscura(url)
        if content:
            result["content"] = _to_str(content)
            result["method"] = "obscura"
            return result

    # 第五层:Olostep(住宅代理云端浏览器兜底)
    if min_layer <= 5:
        print(f"  ▶ 尝试 Olostep(住宅代理云端) ...")
        content = fetch_olostep(url)
        if content:
            result["content"] = _to_str(content)
            result["method"] = "olostep"
            return result

    # 第六层:Firecrawl(AI 智能抓取兜底)
    if min_layer <= 6:
        print(f"  ▶ 尝试 Firecrawl(AI智能) ...")
        content = fetch_firecrawl(url)
        if content:
            result["content"] = _to_str(content)
            result["method"] = "firecrawl"
            return result

    result["error"] = "六层全部失败"
    return result


def _to_str(data) -> str:
    """确保输出是字符串"""
    if isinstance(data, bytes):
        return data.decode("utf-8", errors="replace")
    return str(data)


# ---- 工具:B站 API 直接提取(绕过 HTML 噪音) ----
def fetch_bilibili_video(bvid: str) -> Optional[str]:
    """通过 B站 API 直接获取视频信息,返回干净文本"""
    import requests
    import json

    try:
        # 用 web 页面的 __INITIAL_STATE__ 获取结构化数据
        url = f"https://www.bilibili.com/video/{bvid}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com/",
        }
        resp = requests.get(url, headers=headers, timeout=15,
                          proxies={"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
        if resp.status_code != 200:
            return None

        body = resp.text
        init_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', body[:200000], re.DOTALL)
        if not init_match:
            return None

        data = json.loads(init_match.group(1))
        vd = data.get("videoData", {})

        title = vd.get("title", "")
        desc = vd.get("desc", "") or vd.get("desc_v2", "")
        owner = vd.get("owner", {}).get("name", "")
        duration = vd.get("duration", 0)
        stat = vd.get("stat", {})
        view = stat.get("view", 0)
        like = stat.get("like", 0)
        coin = stat.get("coin", 0)
        fav = stat.get("favorite", 0)
        pubdate = vd.get("pubdate", 0)
        tname = vd.get("tname", "")

        # 组装干净文本
        lines = []
        if title:
            lines.append(f"标题: {title}")
        if owner:
            lines.append(f"UP主: {owner}")
        if tname:
            lines.append(f"分区: {tname}")
        if pubdate:
            from datetime import datetime
            lines.append(f"发布时间: {datetime.fromtimestamp(pubdate).strftime('%Y-%m-%d %H:%M')}")
        if duration:
            m, s = divmod(duration, 60)
            lines.append(f"时长: {m}分{s}秒")
        lines.append(f"播放: {view} | 点赞: {like} | 投币: {coin} | 收藏: {fav}")
        if desc:
            lines.append(f"\n简介:\n{desc}")

        return "\n".join(lines) if lines else None
    except Exception as e:
        print(f"    B站API提取异常: {str(e)[:80]}")
        return None


def _extract_bilibili_bvid(url: str) -> Optional[str]:
    """从 URL 中提取 B站 BV 号"""
    m = re.search(r'(BV[a-zA-Z0-9]+)', url)
    return m.group(1) if m else None


# ---- 工具:从 HTML 提取纯文本 ----

# 平台专用内容选择器(按优先级)
_PLATFORM_SELECTORS = {
    "bilibili.com": [
        ".basic-desc-info",           # 视频简介
        "#v-desc",                     # 旧版视频描述
        ".video-desc",                 # 视频描述
        ".info-content",               # 信息内容
    ],
    "weibo.com": [
        ".wbpro-feed-content",         # 微博正文
        ".detail_wbtext_4CRf9",        # 微博详情文本
        "[node-type='feed_list_content']",  # feed 内容
        ".WB_text",                    # 旧版微博文本
    ],
    "zhihu.com": [
        ".RichContent-inner",          # 知乎回答内容
        ".Post-RichText",              # 知乎文章
        ".AnswerItem-text",            # 回答文本
    ],
    "xiaohongshu.com": [
        "#detail-desc",                # 小红书详情
        ".note-text",                  # 笔记文本
        ".content",                    # 内容区
    ],
    "douyin.com": [
        ".video-info-detail",          # 抖音视频详情
        ".desc",                       # 描述
    ],
}

# 通用噪声选择器(需要移除的元素)
_NOISE_SELECTORS = [
    "nav", "header", "footer", ".nav", ".header", ".footer",
    ".sidebar", ".comment", ".recommend", ".ad", ".popup",
    ".login", ".share", ".toolbar", ".breadcrumb",
    "#comment", "#recommend", "#ad",
]


def extract_text(html_str: str, selector: str = "body", url: str = "") -> str:
    """从 HTML 提取纯文本,支持平台专用选择器"""
    from scrapling import Selector
    import re

    # 确定平台选择器
    platform_sels = []
    if url:
        for domain, sels in _PLATFORM_SELECTORS.items():
            if domain in url:
                platform_sels = sels
                break

    try:
        sel = Selector(html_str)

        # 如果用户指定了选择器,直接用
        if selector != "body":
            els = sel.css(selector)
            if isinstance(els, list):
                return "\n".join(e.get_all_text() or "" for e in els)
            return els.get_all_text() or ""

        # 优先尝试平台专用选择器
        for psel in platform_sels:
            els = sel.css(psel)
            if els:
                if isinstance(els, list):
                    texts = [e.get_all_text().strip() for e in els if e.get_all_text()]
                else:
                    texts = [els.get_all_text().strip()] if els.get_all_text() else []
                combined = "\n".join(t for t in texts if t)
                if len(combined) > 50:  # 有实质内容
                    return combined

        # 降级:尝试 article / main / .content
        for fallback_sel in ["article", "main", ".content", ".post-content", ".article-content"]:
            els = sel.css(fallback_sel)
            if els:
                if isinstance(els, list):
                    texts = [e.get_all_text().strip() for e in els if e.get_all_text()]
                else:
                    texts = [els.get_all_text().strip()] if els.get_all_text() else []
                combined = "\n".join(t for t in texts if t)
                if len(combined) > 100:
                    return combined

        # 最后兜底:body 全文(带噪声过滤)
        text = sel.get_all_text() or ""
        return _clean_extracted_text(text)
    except Exception:
        # fallback: strip HTML tags
        return re.sub(r'<[^>]+>', '', html_str).strip()


def _clean_extracted_text(text: str) -> str:
    """清理提取的文本:移除常见噪声行"""
    lines = text.split("\n")
    noise_patterns = [
        r"^\s*$",                        # 空行
        r"^(首页|番剧|直播|游戏中心|会员购|漫画|赛事|投稿)$",  # B站导航
        r"^(关注|粉丝|播放|弹幕|点赞|收藏|分享|转发)$",  # B站按钮
        r"^(登录|注册|搜索|首页|热门|消息|动态)$",  # 通用导航
        r"^\d+$",                        # 纯数字行
        r"^(发消息|关注|私信|更多)$",     # 社交按钮
        r"^(展开|收起|查看全部|加载更多)$",  # 交互按钮
        r"^(接下来播放|自动连播|相关推荐|推荐视频|猜你喜欢)$",  # B站推荐区标题
        r"^(广告|推广|赞助)$",            # 广告标记
        r"^.*>>$",                        # B站分区链接
    ]
    cleaned = []
    for line in lines:
        line_s = line.strip()
        if not line_s or len(line_s) < 3:
            continue
        if any(re.match(p, line_s) for p in noise_patterns):
            continue
        cleaned.append(line_s)
    return "\n".join(cleaned)


# ---- 工具:搜索关键词(配合搜狗微信) ----
def search_wechat(keyword: str, max_results: int = 8) -> list:
    """搜狗微信搜索公众号文章"""
    from playwright.sync_api import sync_playwright

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            proxy={"server": "http://127.0.0.1:7890"},
        )
        page = ctx.new_page()
        page.goto(f"https://weixin.sogou.com/weixin?type=2&query={keyword}",
                   wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(2000)

        items = page.query_selector_all('.news-box')
        for item in items[:max_results]:
            title_el = item.query_selector('h3 a')
            if not title_el:
                continue
            link = title_el.get_attribute('href') or ""
            full_link = link if link.startswith("http") else f"https://weixin.sogou.com{link}"
            results.append({
                "title": title_el.inner_text().strip(),
                "link": full_link,
                "account": (item.query_selector('.account') or item).inner_text().strip(),
                "summary": (item.query_selector('.txt-info') or item).inner_text().strip()[:120],
            })
        browser.close()
    return results


# ---- 命令行入口 ----
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="侦察兵爬虫")
    parser.add_argument("url", nargs="?", help="要抓取的 URL")
    parser.add_argument("--search", help="搜狗微信搜索关键词")
    parser.add_argument("--selector", default="body", help="CSS 选择器")
    parser.add_argument("--wait", help="等待选择器出现")
    parser.add_argument("--save", help="保存到文件")
    parser.add_argument("--min-layer", type=int, default=1, help="从第几层开始(跳过前几层,1-6)")
    parser.add_argument("--text", action="store_true", help="仅提取纯文本")

    args = parser.parse_args()

    if args.search:
        print(f"🔍 搜狗微信搜索: {args.search}\n")
        results = search_wechat(args.search)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']}")
            print(f"   来源: {r['account']}")
            print(f"   摘要: {r['summary'][:80]}...")
            print(f"   链接: {r['link']}\n")
        sys.exit(0)

    if not args.url:
        parser.print_help()
        sys.exit(1)

    print(f"🌐 抓取: {args.url}")
    result = fetch(args.url, args.wait, min_layer=args.min_layer)

    if result["error"]:
        print(f"❌ {result['error']}")
        sys.exit(1)

    print(f"✅ 成功 (via {result['method']})")
    content = result["content"]

    if args.text:
        text = extract_text(content, args.selector, url=args.url)
        # 过滤太短的内容(可能是空页面)
        if len(text.strip()) < 100:
            print(f"⚠️ 提取内容过短({len(text.strip())}字),可能不是有效页面")
            sys.exit(1)
        output = text.strip()[:5000]
        print(f"\n--- 文本内容 (前5000字) ---\n{output}")
    else:
        output = content

    if args.save:
        path = args.save
        with open(path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"💾 已保存: {path}")
