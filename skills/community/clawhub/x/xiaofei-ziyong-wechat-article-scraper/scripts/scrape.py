#!/usr/bin/env python3
"""
WeChat Article Scraper
Bypasses WeChat anti-bot detection using browser fingerprint伪装技术抓取微信公众号文章。
"""

import sys
import json
import re
import subprocess
import os
import tempfile

def scrape_wechat_article(url: str) -> dict:
    """抓取微信公众号文章"""
    
    if not url or "mp.weixin.qq.com" not in url:
        raise ValueError("请提供有效的微信公众号文章链接（mp.weixin.qq.com）")

    # 伪造真实浏览器 UA，绕过微信检测
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    # 确保使用系统 Chrome（ subprocess 可能没有 PATH）
    chrome_path = "/usr/bin/google-chrome"
    if not os.path.exists(chrome_path):
        chrome_path = "google-chrome"

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--user-agent={ua}",
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
        "--virtual-time-budget=20000",
        "--dump-dom",
        url
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=40
        )
        html = result.stdout
    except FileNotFoundError:
        raise RuntimeError("未找到 google-chrome，请确认已安装 Google Chrome")
    except subprocess.TimeoutExpired:
        raise RuntimeError("页面加载超时（40秒），请重试")
    except Exception as e:
        raise RuntimeError(f"Chrome 执行失败: {str(e)}")

    if not html or len(html) < 1000:
        raise RuntimeError("页面内容为空，可能被反爬拦截或链接无效")

    # 检查是否触发了验证码（环境异常页面）
    if "当前环境异常" in html and "完成验证后即可继续访问" in html:
        raise RuntimeError("微信检测到异常环境，请尝试在真实浏览器中打开验证")

    # 提取标题
    title_match = re.search(r'<title>(.*?)</title>', html)
    title = title_match.group(1).strip() if title_match else ""
    # 微信标题在 JS 里
    if not title or title == "Weixin Official Accounts Platform":
        js_title = re.search(r"title\s*:\s*JsDecode\('([^']+)'\)", html)
        title = js_title.group(1) if js_title else ""

    # 提取作者/公众号名
    author = ""
    author_match = re.search(r'id="js_name">([^<]+)<', html)
    if author_match:
        author = author_match.group(1).strip()
    
    # 提取发布时间
    publish_time = ""
    time_match = re.search(r'class="rich_media_content[^"]*".*?(\d{4}年\d{1,2}月\d{1,2}日)', html, re.DOTALL)
    if not time_match:
        time_match = re.search(r'(\d{4}-\d{2}-\d{2})', html)

    # 提取正文内容（从 js_content 或 rich_media_content）
    content_start = html.find('id="js_content"')
    if content_start == -1:
        content_start = html.find('id="js_content"')
    if content_start == -1:
        content_start = html.find('rich_media_content')
    
    if content_start == -1:
        raise RuntimeError("无法定位文章正文区域（js_content），可能页面结构已变更")

    # 向前找到section开始，向后找足够长
    section_start = html.rfind('<section', 0, content_start)
    if section_start == -1:
        section_start = content_start

    content_end = min(content_start + 1000000, len(html))
    article_html = html[section_start:content_end]

    # 剥掉所有标签，保留纯文本
    # 先去掉 script 和 style
    article_html = re.sub(r'<script[^>]*>.*?</script>', '', article_html, flags=re.DOTALL)
    article_html = re.sub(r'<style[^>]*>.*?</style>', '', article_html, flags=re.DOTALL)
    
    # 去掉所有 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', article_html)
    
    # HTML 实体解码
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&#39;', "'").replace('&quot;', '"')
    text = text.replace('&ensp;', ' ').replace('&emsp;', ' ')
    
    # 清理多余空白
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    content = '\n'.join(lines)
    
    # 去掉底部干扰（赞赏、留言、推荐阅读等）
    for keyword in ['赞赏', '留言', '推荐阅读', '更多相关文章', '写出你的看法']:
        idx = content.find(keyword)
        if idx > 0 and idx < len(content) - 50:
            content = content[:idx]
    
    word_count = len(content.replace('\n', '').replace(' ', ''))

    return {
        "title": title,
        "author": author,
        "publish_time": publish_time,
        "content": content[:50000],  # 限制最大50000字符
        "url": url,
        "word_count": word_count,
        "raw_length": len(html)
    }


def main():
    if len(sys.argv) < 2:
        # 作为 OpenClaw tool 被调用，从 stdin 读取 JSON 输入
        try:
            input_data = json.load(sys.stdin)
            url = input_data.get("url") or input_data.get("query") or ""
            if not url:
                print(json.dumps({"status": "error", "message": "缺少 url 参数"}, ensure_ascii=False))
                sys.exit(1)
        except Exception:
            # 兼容直接传 URL 的方式
            url = ""
    else:
        url = sys.argv[1]

    # 支持 url= 格式
    if not url and len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("http"):
            url = arg
        elif "url=" in arg:
            url = arg.split("url=")[-1].strip()

    try:
        result = scrape_wechat_article(url)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
