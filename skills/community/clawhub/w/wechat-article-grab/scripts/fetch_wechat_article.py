#!/usr/bin/env python3
"""
微信公众号文章内容提取脚本
用法: python3 fetch_wechat_article.py "<url>"
策略：requests + Cookie + js_content 提取 > curl 多UA兜底
"""

import sys
import re
import os
import html


def fetch_wechat_article(url: str) -> str:
    """使用 requests + Cookie 获取微信文章全文内容"""
    title, content = fetch_wechat_article_with_title(url)
    if content.startswith("FETCH_FAILED"):
        return content
    return content


def _extract_title_from_html(html_text: str) -> str:
    """从 HTML 中提取文章标题"""
    m = re.search(r'<meta property="og:title" content="([^"]+)"', html_text)
    if m:
        return html.unescape(m.group(1))
    m = re.search(r'<title>([^<]+)</title>', html_text)
    return html.unescape(m.group(1)) if m else ""


def _extract_js_content(html_text: str) -> str:
    """
    从微信文章 HTML 中提取正文。
    
    新版微信：id="js_content" 是 visibility:hidden 的占位符，
    实际正文紧跟其后，到 js_pc_qr_code 截止。
    """
    # 检查 js_content 是否是隐藏的（新版微信特征）
    js_idx = html_text.find('id="js_content"')
    if js_idx != -1:
        snippet = html_text[js_idx:js_idx + 300]
        if 'visibility: hidden' in snippet or 'visibility:hidden' in snippet:
            # 新版结构：从 js_content 起点到 js_pc_qr_code 之前，都是正文区域
            # 找正文真正的结束位置（公众号信息区之前）
            # js_pc_qr_code 在 492K，但之前还有 content_bottom_area、预览提示等非正文内容
            # 正确的截止点是 js_pc_qr_code 之前最近的 </section>（最后一个 section 闭合）
            snippet = html_text[js_idx:]
            qr_pos = snippet.find('id="js_pc_qr_code"')
            # 找 js_pc_qr_code 之前最近的 </section>
            before_qr = snippet[:qr_pos] if qr_pos != -1 else snippet
            last_section_close = before_qr.rfind('</section>')
            if last_section_close != -1:
                content_end = js_idx + last_section_close + len('</section>')
            elif qr_pos != -1:
                content_end = js_idx + qr_pos
            else:
                content_end = len(html_text)
            content_html = html_text[js_idx:content_end]
            # 先过滤 <script> 和 <style> 再去标签，防止 JS/CSS 代码残留混入正文
            content_html = re.sub(r'<script[^>]*>.*?</script>', '', content_html, flags=re.DOTALL)
            content_html = re.sub(r'<style[^>]*>.*?</style>', '', content_html, flags=re.DOTALL)
            # 过滤属性
            content_html = re.sub(r'style="[^"]*"', '', content_html)
            content_html = re.sub(r'class="[^"]*"', '', content_html)
            content_html = re.sub(r'data-[a-z-]+="[^"]*"', '', content_html)
            text = re.sub(r'<[^>]+>', ' ', content_html)
            for entity, char in [("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"),
                                  ("&gt;", ">"), ("&mdash;", "—"), ("&ldquo;", '"'),
                                  ("&rdquo;", '"'), ("&lsquo;", "'"), ("&rsquo;", "'"),
                                  ("&#xa0;", " "), ("&shy;", "")]:
                text = text.replace(entity, char)
            text = re.sub(r'\s+', ' ', text).strip()
            # 清理 js_content 开头残留
            text = re.sub(r'^[a-z_]+="[^"]*"(\s+[a-z_]+="[^"]*")*\s*>?\s*', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) >= 200:
                return text

    # 旧版或其他结构
    content_sections = [
        'id="img-content"',
        'id="js_content"',
        'class="rich_media_content"',
        'id="rich_media_content"',
    ]

    for section in content_sections:
        idx = html_text.find(section)
        if idx == -1:
            continue

        snippet = html_text[idx:idx + 500000]
        end_markers = ['id="js_pc_qr_code"', 'id="runtime_config"']
        end_pos = len(snippet)
        for marker in end_markers:
            pos = snippet.find(marker)
            if pos != -1 and pos < end_pos:
                end_pos = pos

        raw = snippet[:end_pos]
        text = re.sub(r'<[^>]+>', ' ', raw)
        for entity, char in [("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"),
                              ("&gt;", ">"), ("&mdash;", "—"), ("&ldquo;", '"'),
                              ("&rdquo;", '"'), ("&lsquo;", "'"), ("&rsquo;", "'")]:
            text = text.replace(entity, char)
        text = re.sub(r'style="visibility: hidden; opacity: 0; "\s*>\s*', '', text)
        text = re.sub(r'预览时标签不可点.*', '', text)
        text = re.sub(r'var\s+first_sceen__time.*', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) >= 200:
            return text

    return ""



def _extract_via_requests(url: str, cookie: str) -> tuple:
    """策略2：requests + Cookie 提取正文"""
    import requests as req

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
    html_text = r.text

    if len(html_text) < 1000 or "环境异常" in html_text:
        return "", ""

    title = _extract_title_from_html(html_text)

    # 优先：用 js_content 提取正文
    content = _extract_js_content(html_text)

    return title, content


def _extract_via_curl(url: str) -> tuple:
    """策略1：curl 多 UA 提取正文（无 Cookie）"""
    import subprocess

    strategies = [
        {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36", "referer": "https://mp.weixin.qq.com/"},
        {"ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1", "referer": "https://www.google.com/"},
        {"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", "referer": "https://www.google.com/"},
    ]

    for strat in strategies:
        cmd = ["curl", "-s", "-L", "-A", strat["ua"],
               "-H", f"Referer: {strat['referer']}",
               "--connect-timeout", "15", "--max-time", "30", url]

        result = subprocess.run(cmd, capture_output=True, text=False)
        html_text = result.stdout.decode("utf-8", errors="replace")

        if len(html_text) < 1000:
            continue
        if "环境异常" in html_text or "请选择验证方式" in html_text:
            continue

        title = _extract_title_from_html(html_text)
        content = _extract_js_content(html_text)

        if len(content) >= 200:
            return title, content

    return "", ""


def fetch_wechat_article_with_title(url: str) -> tuple:
    """
    获取微信文章正文和标题
    优先级：curl多UA > mptext下载 > requests+Cookie
    提取策略：js_content 正文
    返回：(title, content)，content 最短 200 字符才算成功
    """
    # 加载 Cookie
    cookie = ""
    cookie_file = os.path.join(os.path.dirname(__file__), "skill.env")
    if os.path.exists(cookie_file):
        sys.path.insert(0, os.path.dirname(__file__))
        try:
            from wechat_article import load_cookie
            cookie = load_cookie() or ""
        except Exception:
            cookie = ""

    # 策略1：curl 多 UA（免费，优先）
    try:
        title, content = _extract_via_curl(url)
        if len(content) >= 200:
            return title, content
    except Exception:
        pass

    # 策略2：mptext API 下载（付费，备用）
    try:
        from mptext_api import get_client as get_mptext_client
        mp_client = get_mptext_client()
        content = mp_client.download_article(url, format='text')
        if content and len(content) >= 200:
            # mptext 下载不带标题，从 HTML 提取标题
            try:
                import subprocess
                result = subprocess.run(
                    ['curl', '-s', '-L', '-A',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                     url, '--connect-timeout', '15', '--max-time', '30'],
                    capture_output=True, text=False
                )
                html = result.stdout.decode('utf-8', errors='replace')
                title = _extract_title_from_html(html)
            except Exception:
                title = ""
            return title, content
    except Exception:
        pass

    # 策略3：requests + Cookie（最后备用）
    if cookie:
        try:
            title, content = _extract_via_requests(url, cookie)
            if len(content) >= 200:
                return title, content
        except Exception:
            pass

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