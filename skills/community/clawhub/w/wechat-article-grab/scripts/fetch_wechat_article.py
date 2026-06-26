#!/usr/bin/env python3
"""
微信公众号文章内容提取脚本
用法: python3 fetch_wechat_article.py "<url>"
策略：requests + Cookie（优先） > curl 多UA兜底
"""

import sys
import re
import os

def fetch_wechat_article(url: str) -> str:
    """使用 requests + Cookie 获取微信文章全文内容"""
    title, content = fetch_wechat_article_with_title(url)
    if content.startswith("FETCH_FAILED"):
        return content
    return content


def fetch_wechat_article_with_title(url: str) -> tuple:
    """使用 requests + Cookie 获取微信文章全文内容和标题"""
    import re as regex_module

    cookie_file = os.path.expanduser("~/.openclaw/agents/xingchen/workspace/skills/wechat-article-reader/scripts/wechat_cookie.env")
    if os.path.exists(cookie_file):
        with open(cookie_file) as f:
            cookie = f.read().strip()
    else:
        cookie = ""

    # 策略1：requests + Cookie（成功率最高，能过大部分反爬）
    if cookie:
        try:
            import requests as req
            
            # 构造完整URL
            if url.startswith("http://mp.weixin.qq.com"):
                url = url.replace("http://", "https://")
            if not url.startswith("https://mp.weixin.qq.com"):
                url = "https://mp.weixin.qq.com/s/" + url.split("/s/")[-1]
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Cookie": cookie,
                "Referer": "https://mp.weixin.qq.com/",
                "Accept": "text/html,application/xhtml+xml,*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
            
            r = req.get(url, headers=headers, allow_redirects=True, timeout=30)
            html = r.text
            
            if len(html) > 1000 and "js_content" in html:
                idx = html.find('id="js_content"')
                idx2 = html.find('id="js_pc_qr_code"')
                if idx != -1 and idx2 != -1:
                    raw = html[idx + len('id="js_content"'):idx2]
                    text = re.sub(r'<[^>]+>', ' ', raw)
                    for e in [("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&mdash;", "—"), ("&ldquo;", '"'), ("&rdquo;", '"')]:
                        text = text.replace(e[0], e[1])
                    text = re.sub(r'\s+', ' ', text).strip()
                    text = re.sub(r'style="visibility: hidden; opacity: 0; "\s*>\s*', '', text)
                    text = re.sub(r'^©\s*[\w\s]*Photos\s*', '', text)
                    text = re.sub(r'预览时标签不可点.*', '', text)
                    text = re.sub(r'var\s+first_sceen__time.*', '', text)
                    text = re.sub(r'\s+', ' ', text).strip()
                    if len(text) >= 200:
                        # 从HTML提取og:title
                        title_match = regex_module.search(r'<meta property="og:title" content="([^"]+)"', html)
                        if not title_match:
                            title_match = regex_module.search(r'<title>([^<]+)</title>', html)
                        title = title_match.group(1) if title_match else ''
                        return title, text
        except Exception as e:
            pass

    # 策略2：curl 多 UA 兜底
    import subprocess
    
    strategies = [
        {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "referer": "https://mp.weixin.qq.com/",
        },
        {
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "referer": "https://www.google.com/",
        },
        {
            "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "referer": "https://www.google.com/",
        },
    ]

    for strat in strategies:
        cmd = [
            "curl", "-s", "-L",
            "-A", strat["ua"],
            "-H", f"Referer: {strat['referer']}",
            "--connect-timeout", "15",
            "--max-time", "30",
            url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        html_content = result.stdout

        if not html_content or len(html_content) < 1000:
            continue
        if "环境异常" in html_content or "请选择验证方式" in html_content:
            continue

        content_match = re.search(
            r'id="js_content"(.*?)id="js_pc_qr_code"',
            html_content,
            re.DOTALL
        )

        if not content_match:
            continue

        raw_html = content_match.group(1)
        text = re.sub(r'<[^>]+>', ' ', raw_html)
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        text = re.sub(r'style="visibility: hidden; opacity: 0; "\s*>\s*', '', text)
        text = re.sub(r'^©\s*[\w\s]*Photos\s*', '', text)
        text = re.sub(r'预览时标签不可点.*', '', text)
        text = re.sub(r'var\s+first_sceen__time.*', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) < 200:
            continue

        # 从HTML提取og:title
        title_match = regex_module.search(r'<meta property="og:title" content="([^"]+)"', html_content)
        if not title_match:
            title_match = regex_module.search(r'<title>([^<]+)</title>', html_content)
        title = title_match.group(1) if title_match else ''

        return title, text

    return "FETCH_FAILED: 所有策略均失败，文章可能被拦截或不存在", ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 fetch_wechat_article.py <微信文章URL>")
        sys.exit(1)

    url = sys.argv[1]
    content = fetch_wechat_article(url)

    if content.startswith("FETCH_FAILED"):
        print(content)
        sys.exit(1)
    else:
        print(content)