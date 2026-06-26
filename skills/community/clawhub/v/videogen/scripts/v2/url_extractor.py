#!/usr/bin/env python3
"""
videogen v2 — URL 内容提取器
从网页 URL 提取干净的正文内容，用于后续视频生成。

支持：
- 微信公众号文章
- 知乎文章/回答
- 知乎专栏
- 通用网页（通过 readability 风格提取）

用法:
    python url_extractor.py "https://mp.weixin.qq.com/s/xxx"
    python url_extractor.py "https://zhuanlan.zhihu.com/p/xxx"
    python url_extractor.py "https://news.example.com/article" --llm-summarize
"""

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

# ─── 依赖检查 ───

try:
    import requests
except ImportError:
    print("⚠️  requests 未安装，正在安装...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"], check=True)
    import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("⚠️  beautifulsoup4 未安装，正在安装...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "beautifulsoup4", "-q"], check=True)
    from bs4 import BeautifulSoup

try:
    import trafilatura
    HAS_TRAFILATURA = True
except ImportError:
    HAS_TRAFILATURA = False

# ─── 数据结构 ───

@dataclass
class ExtractedContent:
    url: str
    title: str
    author: Optional[str]
    publish_date: Optional[str]
    source_name: str          # 微信公众号 / 知乎 / 通用
    full_text: str            # 原始正文（中文）
    summary: str              # LLM 摘要（如启用）
    key_points: list[str]     # 关键要点列表
    word_count: int
    extraction_method: str    # "wechat" / "zhihu" / "trafilatura" / "bs4_fallback"


# ─── 微信公众号提取 ───

def extract_wechat(url: str) -> ExtractedContent:
    """提取微信公众号文章"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.encoding = "utf-8"

    soup = BeautifulSoup(resp.text, "html.parser")

    # 标题
    title_tag = soup.find("h1", class_="rich_media_title")
    if not title_tag:
        title_tag = soup.find("meta", property="og:title")
        title = title_tag["content"].strip() if title_tag and title_tag.get("content") else "未知标题"
    else:
        title = title_tag.get_text(strip=True)

    # 作者
    author_tag = soup.find("a", class_="rich_media_meta rich_media_meta_link rich_media_meta_nickname")
    if not author_tag:
        author_tag = soup.find("span", class_="rich_media_meta rich_media_meta_nickname")
    author = author_tag.get_text(strip=True) if author_tag else None

    # 发布日期
    date_tag = soup.find("em", id="publish_time")
    if not date_tag:
        date_tag = soup.find("span", class_="rich_media_meta rich_media_meta_text")
    publish_date = date_tag.get_text(strip=True) if date_tag else None

    # 正文
    content_tag = soup.find("div", id="js_content") or soup.find("div", class_="rich_media_content")
    if content_tag:
        # 移除 script/style/images
        for tag in content_tag.find_all(["script", "style", "img", "svg", "iframe"]):
            tag.decompose()
        text = content_tag.get_text(separator="\n", strip=True)
    else:
        text = ""

    # 清理多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)

    return ExtractedContent(
        url=url,
        title=title,
        author=author,
        publish_date=publish_date,
        source_name="微信公众号",
        full_text=text,
        summary="",  # 暂不生成，等待 LLM
        key_points=[],
        word_count=len(text),
        extraction_method="wechat",
    )


# ─── 知乎提取 ───

def extract_zhihu(url: str) -> ExtractedContent:
    """提取知乎文章/回答"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    # 标题
    title_tag = soup.find("h1") or soup.find("meta", property="og:title")
    title = title_tag.get_text(strip=True) if title_tag else "未知标题"
    if title_tag and title_tag.get("content"):
        title = title_tag["content"].strip()

    # 作者
    author_tag = soup.find("span", class_="AuthorInfo-name")
    author = author_tag.get_text(strip=True) if author_tag else None

    # 发布日期
    date_tag = soup.find("span", class_="ContentItem-time")
    publish_date = None
    if date_tag:
        publish_date = date_tag.get_text(strip=True)
        # 提取数字日期
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", publish_date)
        if date_match:
            publish_date = date_match.group()

    # 正文（知乎文章页）
    content_tag = soup.find("div", class_="RichText") or soup.find("div", class_="Post-RichText")
    if not content_tag:
        content_tag = soup.find("div", {"data-pid": True})  # 回答类

    if content_tag:
        for tag in content_tag.find_all(["script", "style", "img", "svg"]):
            tag.decompose()
        text = content_tag.get_text(separator="\n", strip=True)
    else:
        text = ""

    text = re.sub(r"\n{3,}", "\n\n", text)

    return ExtractedContent(
        url=url,
        title=title,
        author=author,
        publish_date=publish_date,
        source_name="知乎",
        full_text=text,
        summary="",
        key_points=[],
        word_count=len(text),
        extraction_method="zhihu",
    )


# ─── 通用网页提取 ───

def extract_generic(url: str) -> ExtractedContent:
    """通用网页提取（优先 trafilatura，次选 BS4 readability 风格）"""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    }

    text = ""
    method = "bs4_fallback"
    title = "未知标题"
    author = None
    publish_date = None

    # 尝试 trafilatura（最干净的正文提取）
    if HAS_TRAFILATURA:
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded, include_comments=False)
                method = "trafilatura"
        except Exception:
            pass

    # BS4 fallback
    if not text:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = resp.apparent_encoding or "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        # 标题
        title_tag = (
            soup.find("h1") or
            soup.find("meta", property="og:title") or
            soup.find("title")
        )
        if title_tag:
            title = title_tag.get("content", title_tag.get_text(strip=True))

        # 正文容器猜测
        content_tag = (
            soup.find("article") or
            soup.find("main") or
            soup.find("div", class_=re.compile(r"content|article|post|text|body", re.I)) or
            soup.find("div", id=re.compile(r"content|article|post|text|body", re.I))
        )
        if content_tag:
            for tag in content_tag.find_all(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            text = content_tag.get_text(separator="\n", strip=True)
            text = re.sub(r"\n{3,}", "\n\n", text)

    text = text.strip()

    return ExtractedContent(
        url=url,
        title=title,
        author=author,
        publish_date=publish_date,
        source_name="通用网页",
        full_text=text,
        summary="",
        key_points=[],
        word_count=len(text),
        extraction_method=method,
    )


# ─── 智能路由 ───

def extract_content(url: str) -> ExtractedContent:
    """根据 URL 类型自动选择提取方法"""
    url_lower = url.lower()

    if "mp.weixin.qq.com" in url_lower:
        return extract_wechat(url)
    elif "zhihu.com" in url_lower or "zhuanlan.zhihu.com" in url_lower:
        return extract_zhihu(url)
    else:
        return extract_generic(url)


# ─── 内容摘要生成（可选，需 API Key）───

def generate_summary(content: ExtractedContent, api_key: str = "") -> ExtractedContent:
    """调用 LLM 生成摘要和关键要点"""
    if not api_key:
        api_key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY", "")

    if not api_key or not content.full_text:
        return content

    try:
        import openai
    except ImportError:
        try:
            import sys
            subprocess.run([sys.executable, "-m", "pip", "install", "openai", "-q"], check=True)
            import openai
        except Exception:
            return content

    # 取前 3000 字（避免 token 浪费）
    text_input = content.full_text[:3000]

    try:
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.openai.com/v1" if "sk-" in api_key else "https://api.minimax.io/v1"
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo" if "sk-" in api_key else "MiniMax-Text-01",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个内容分析助手。请分析以下文章，生成简洁的中文摘要（100字内）和3-5个关键要点。输出JSON格式：{\"summary\": \"...\", \"key_points\": [\"要点1\", \"要点2\", ...]}"
                },
                {"role": "user", "content": text_input}
            ],
            temperature=0.3,
            max_tokens=500,
        )
        result_text = response.choices[0].message.content
        # 解析 JSON
        import json
        data = json.loads(result_text)
        content.summary = data.get("summary", "")
        content.key_points = data.get("key_points", [])
    except Exception as e:
        print(f"  ⚠️  摘要生成失败: {e}")

    return content


# ─── 入口 ───

def main():
    parser = argparse.ArgumentParser(description="URL 内容提取器")
    parser.add_argument("url", help="文章 URL")
    parser.add_argument("--summarize", action="store_true", help="生成 LLM 摘要和关键要点")
    parser.add_argument("--output", "-o", help="保存结果到 JSON 文件")
    args = parser.parse_args()

    print(f"🔍 正在抓取: {args.url}")
    content = extract_content(args.url)
    print(f"  ✅ 提取完成")
    print(f"  标题: {content.title}")
    print(f"  来源: {content.source_name}")
    print(f"  作者: {content.author or '未知'}")
    print(f"  字数: {content.word_count} 字")
    print(f"  方法: {content.extraction_method}")

    if args.summarize:
        print(f"\n📝 正在生成摘要...")
        content = generate_summary(content)
        print(f"  ✅ 摘要: {content.summary[:80]}...")
        print(f"  ✅ 要点:")
        for i, p in enumerate(content.key_points, 1):
            print(f"    {i}. {p[:60]}")

    # 保存
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(content), f, ensure_ascii=False, indent=2)
        print(f"\n💾 已保存: {args.output}")

    # 也打印纯文本（方便管道传递）
    print(f"\n─── 正文内容（前500字）───")
    print(content.full_text[:500])


if __name__ == "__main__":
    import os
    main()
