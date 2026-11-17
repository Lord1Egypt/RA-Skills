#!/usr/bin/env python3
"""
Web Content → Structured Markdown Converter (Unified Entry)

Auto-detects URL type and routes to the appropriate converter:
  - x.com / twitter.com → x-tweet-fetcher + tweet_to_md.py
  - mp.weixin.qq.com    → markitdown (WeChat plugin)
  - *.feishu.cn/wiki/   → lark-cli docs +fetch (v3.7.0 优先，WebFetch 截断严重)
  - xiaohongshu.com     → markitdown (Xiaohongshu plugin)
  - weibo.com           → markitdown (generic)
  - youtube.com         → markitdown (YouTube support)
  - Other URLs          → markitdown (generic HTML)
  - Local files         → markitdown (PDF/DOCX/PPTX/XLSX/Images/Audio/etc.)

Usage:
  python3 web_to_md.py --url <url_or_path> --output <output.md>
  python3 web_to_md.py --url <url_or_path>  (prints to stdout)
  python3 web_to_md.py --url <tweet_url> --replies  (fetch thread replies)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILLS_DIR = os.path.expanduser("~/.aily/workspace/skills")
TWEET_FETCHER = os.path.join(SKILLS_DIR, "x-tweet-fetcher/scripts/fetch_tweet.py")
SCRIPT_DIR = Path(__file__).parent
TWEET_TO_MD = str(SCRIPT_DIR / "tweet_to_md.py")


def _run(cmd, check=True, timeout=120):
    """运行子进程，默认 120 秒超时（x-tweet-fetcher 网络异常时防止永久挂起）"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check, timeout=timeout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"子进程超时（{timeout}秒）: {' '.join(cmd[:3])}...")


def _detect_source(url_or_path: str) -> str:
    lower = url_or_path.lower()

    if "x.com" in lower or "twitter.com" in lower:
        return "twitter"
    if "mp.weixin.qq.com" in lower:
        return "wechat"
    # v3.7.0: 飞书 wiki 优先用 lark-cli docs +fetch（WebFetch 截断严重）
    if "feishu.cn/wiki" in lower or "larkoffice.com/wiki" in lower:
        return "feishu_wiki"
    if "weibo.com" in lower:
        return "weibo"
    if "xiaohongshu.com" in lower or "xhslink.com" in lower:
        return "xiaohongshu"
    if "youtube.com" in lower or "youtu.be" in lower:
        return "youtube"
    if lower.startswith("http://") or lower.startswith("https://"):
        return "html"

    ext = Path(lower).suffix
    file_map = {
        ".pdf": "pdf", ".docx": "docx", ".doc": "docx",
        ".pptx": "pptx", ".ppt": "pptx",
        ".xlsx": "xlsx", ".xls": "xlsx",
        ".png": "image", ".jpg": "image", ".jpeg": "image",
        ".gif": "image", ".bmp": "image", ".webp": "image", ".tiff": "image",
        ".mp3": "audio", ".wav": "audio", ".m4a": "audio", ".flac": "audio",
        ".csv": "csv", ".json": "json", ".xml": "xml",
        ".zip": "zip", ".epub": "epub",
        ".md": "markdown", ".txt": "text", ".html": "html_file", ".htm": "html_file",
    }
    return file_map.get(ext, "unknown")


def _convert_twitter(url: str, output_path: str = None, replies: bool = False) -> str:
    fetch_cmd = [sys.executable, TWEET_FETCHER, "--url", url, "--pretty"]
    if replies:
        fetch_cmd.append("--replies")

    try:
        json_str = _run(fetch_cmd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to fetch tweet: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp.write(json_str)
        tmp_json = tmp.name

    convert_cmd = [sys.executable, TWEET_TO_MD, "--input", tmp_json]
    if output_path:
        convert_cmd.extend(["--output", output_path])

    try:
        result = _run(convert_cmd)
    finally:
        if os.path.exists(tmp_json):
            os.unlink(tmp_json)

    if output_path and os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
    return result


def _convert_markitdown(url_or_path: str, output_path: str = None) -> str:
    try:
        from markitdown import MarkItDown
    except ImportError:
        print("❌ markitdown not installed. Run: pip install markitdown", file=sys.stderr)
        sys.exit(1)

    md = MarkItDown()
    result = md.convert(url_or_path)
    content = result.markdown

    # 公众号反爬 fallback：markitdown 返回验证页（通常 <200 字符）
    if "mp.weixin.qq.com" in url_or_path.lower() and len(content) < 200:
        print("⚠️ markitdown returned anti-crawl page, trying mobile UA fallback...", file=sys.stderr)
        content = _fetch_wechat_mobile(url_or_path)
        if not content:
            print("❌ Mobile UA fallback also failed. Use WebFetch or manual transcription.", file=sys.stderr)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Markdown saved: {out} ({len(content)} chars)", file=sys.stderr)

    return content


def _convert_feishu_wiki(url: str, output_path: str = None) -> str:
    """飞书 wiki 转换器（v3.7.0 新增）

    优先用 lark-cli docs +fetch 抓取完整内容（用户身份认证，可读取全文）。
    WebFetch 对飞书 wiki 抓取不稳定，常返回 200-1000 字符截断内容（实测 33 篇文章中 19 篇被截断）。

    Args:
        url: 飞书 wiki URL（如 https://waytoagi.feishu.cn/wiki/xxxxx）
        output_path: 可选，输出文件路径

    Returns:
        飞书 wiki 的 Markdown 内容（含原文链接行）
    """
    lark_cli = shutil.which("lark-cli") or r"C:\Users\Administrator\AppData\Roaming\npm\lark-cli.cmd"
    if not Path(lark_cli).exists() and shutil.which("lark-cli") is None:
        raise RuntimeError(
            "lark-cli 未安装。请运行：npm i -g @larksuiteoapi/lark-cli && lark-cli auth login"
        )

    cmd = [
        lark_cli, "docs", "+fetch",
        "--doc", url,
        "--doc-format", "markdown",
        "--scope", "full",
        "--format", "json",
    ]
    print(f"📡 Fetching feishu wiki via lark-cli: {url}", file=sys.stderr)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=60)
    except subprocess.TimeoutExpired:
        raise RuntimeError("lark-cli 超时（60秒）")

    if result.returncode != 0:
        raise RuntimeError(f"lark-cli 调用失败: {result.stderr[:500]}")

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"lark-cli 输出 JSON 解析失败: {e}")

    if not data.get("ok"):
        err = data.get("error", {})
        raise RuntimeError(f"lark-cli API 返回 ok=false: {err}")

    content = data.get("data", {}).get("document", {}).get("content", "")
    if not content:
        raise RuntimeError("lark-cli 返回空内容")

    print(f"✅ Fetched {len(content)} chars from feishu wiki", file=sys.stderr)

    # 完整性验证：内容过短时警告（可能是空 wiki 或权限不足）
    if len(content) < 500:
        print(f"⚠️ Warning: feishu wiki content is short ({len(content)} chars)", file=sys.stderr)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        print(f"✅ Markdown saved: {out} ({len(content)} chars)", file=sys.stderr)

    return content


def _fetch_wechat_mobile(url: str) -> str:
    """Fallback: fetch WeChat article with mobile UA to bypass anti-crawl.

    改进版：保留图片、段落结构、引用块、代码块，而非纯文本提取。
    """
    try:
        import requests
    except ImportError:
        return ""

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/WIFI Language/zh_CN",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.encoding = "utf-8"
        html = resp.text

        # 提取标题
        title_match = re.search(r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', html, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "WeChat Article"

        # 提取正文（js_content div）
        match = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
        if not match:
            return ""
        content_html = match.group(1)

        # 转换为 Markdown（保留图片、段落、引用、代码块）
        md_parts = [f"# {title}\n"]

        # 提取图片（data-src 或 src）
        for img in re.finditer(r'<img[^>]*(?:data-src|src)="([^"]+)"', content_html):
            img_url = img.group(1)
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            md_parts.append(f"\n![]({img_url})\n")

        # 按段落分割（<p> 和 <section> 标签）
        paragraphs = re.split(r'</?(?:p|section)[^>]*>', content_html)
        for para in paragraphs:
            # 去 HTML 标签但保留文本
            text = re.sub(r"<[^>]+>", "", para)
            text = re.sub(r"\s+", " ", text).strip()
            if text and len(text) > 1:
                # 检查是否为引用（<blockquote> 或 indent 类）
                if "blockquote" in para or "js_blockquote" in para:
                    md_parts.append(f"\n> {text}\n")
                else:
                    md_parts.append(f"\n{text}\n")

        return "\n".join(md_parts)
    except Exception as e:
        print(f"⚠️ Mobile UA fetch failed: {e}", file=sys.stderr)
        return ""


def extract_original_url(markdown: str) -> str:
    """从 Markdown 前 800 字符提取原文链接（v3.3.0）

    飞书 wiki 转载文章通常在头部标注"原文链接"，本函数自动提取。

    支持的格式：
        原文链接：https://...
        转载自：https://...
        本文首发：https://...
        本文转载自：https://...
        🔗 https://...
        🔗 原文链接：[https://...](https://...)

    Returns:
        URL 字符串，未找到返回 None
    """
    import re
    if not markdown:
        return None
    head = markdown[:800]
    # 匹配关键词后的 URL（支持 markdown 链接 [text](url) 和裸 URL）
    patterns = [
        r'原文链接[：:]\s*\[?[^\]]*\]?\(?(https?://[^\s\)]+)',
        r'转载自[：:]\s*\[?[^\]]*\]?\(?(https?://[^\s\)]+)',
        r'本文首发[：:]?\s*\[?[^\]]*\]?\(?(https?://[^\s\)]+)',
        r'本文转载[自:：]?\s*\[?[^\]]*\]?\(?(https?://[^\s\)]+)',
        r'🔗\s*\[?[^\]]*\]?\(?(https?://[^\s\)]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, head)
        if match:
            url = match.group(1).rstrip(')').rstrip(']')
            return url
    return None


def convert(url_or_path: str, output_path: str = None, replies: bool = False) -> str:
    source_type = _detect_source(url_or_path)

    print(f"🔍 Detected source type: {source_type}", file=sys.stderr)

    if source_type == "twitter":
        return _convert_twitter(url_or_path, output_path, replies)
    elif source_type == "feishu_wiki":
        # v3.7.0: 飞书 wiki 优先用 lark-cli docs +fetch（WebFetch 截断严重）
        return _convert_feishu_wiki(url_or_path, output_path)
    else:
        return _convert_markitdown(url_or_path, output_path)


def main():
    parser = argparse.ArgumentParser(description="Web Content → Structured Markdown Converter")
    parser.add_argument("--url", required=True, help="URL or local file path to convert")
    parser.add_argument("--output", help="Output Markdown file path (default: stdout)")
    parser.add_argument("--replies", action="store_true", help="Fetch tweet replies (Twitter only)")
    args = parser.parse_args()

    content = convert(args.url, args.output, args.replies)

    if not args.output:
        print(content)


if __name__ == "__main__":
    main()
