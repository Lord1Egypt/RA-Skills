#!/usr/bin/env python3
"""
微信公众号文章 → 高质量 Markdown 转换工具

深度定制微信文章结构，智能去噪、代码块识别、富文本保留。
用法: python wechat_to_md.py <URL> [-o OUTPUT_DIR] [--no-images] [--no-frontmatter]

依赖: pip install playwright beautifulsoup4 markdownify requests
      playwright install chromium
"""

import argparse
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import urlparse, urljoin

try:
    from bs4 import BeautifulSoup, Tag, NavigableString
except ImportError:
    sys.exit("缺少依赖: pip install beautifulsoup4")

try:
    import markdownify
except ImportError:
    sys.exit("缺少依赖: pip install markdownify")

try:
    import requests
except ImportError:
    requests = None


# ─────────────────────────────────────────────
# 异常类
# ─────────────────────────────────────────────

class WeChatError(Exception):
    pass

class NetworkError(WeChatError):
    pass

class CaptchaError(WeChatError):
    pass

class ParseError(WeChatError):
    pass


# ─────────────────────────────────────────────
# 1. URL 标准化
# ─────────────────────────────────────────────

def html_unescape(text: str) -> str:
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&#x27;", "'")
    return text


def normalize_url(raw: str) -> str:
    raw = raw.strip()
    raw = html_unescape(raw)
    if raw.startswith("//"):
        raw = "https:" + raw
    if not raw.startswith("http"):
        raw = "https://" + raw
    return raw


# ─────────────────────────────────────────────
# 2. 页面抓取（Playwright 为主，requests 降级）
# ─────────────────────────────────────────────

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

DEFAULT_HEADERS = {
    "User-Agent": DEFAULT_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://mp.weixin.qq.com/",
}


MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)


def fetch_with_playwright(url: str, wait_for: str = "#js_content",
                          timeout: int = 30000) -> str:
    """
    使用 Playwright Chromium 移动端渲染页面，返回完整 HTML。
    支持 JS 动态渲染和微信临时链接（tempkey）。
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        raise NetworkError(
            "缺少 Playwright 依赖。请运行: pip install playwright && playwright install chromium"
        )

    with sync_playwright() as p:
        # 使用移动端 persistent_context（与 wechat_export.py 相同方案）
        context = p.chromium.launch_persistent_context(
            "",
            headless=True,
            viewport={"width": 393, "height": 852},
            device_scale_factor=3,
            user_agent=MOBILE_UA,
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
            is_mobile=True,
            has_touch=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox", "--disable-setuid-sandbox",
                "--disable-dev-shm-usage", "--disable-gpu",
                "--disable-infobars", "--disable-ipc-flooding-protection",
                "--disable-renderer-backgrounding",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-popup-blocking", "--disable-prompt-on-repost",
                "--disable-sync", "--enable-async-dns",
                "--use-mock-keychain",
                "--hide-scrollbars", "--mute-audio",
                "--disable-extensions",
            ],
        )
        try:
            page = context.new_page()

            # 导航到页面
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)

            # 等待正文容器出现
            for sel in [wait_for, ".rich_media_content", "#page-content", "article"]:
                try:
                    page.wait_for_selector(sel, timeout=8000)
                    break
                except PWTimeout:
                    continue

            # 懒加载图片处理（与 wechat_export.py 相同）
            page.evaluate("""
                () => {
                    document.querySelectorAll('img[data-src]').forEach(img => {
                        if (!img.src.startsWith('http') || img.src === img.dataset.src) {
                            img.src = img.dataset.src;
                        }
                    });
                    document.querySelectorAll('img').forEach(img => {
                        if (img.dataset && img.dataset.src) img.src = img.dataset.src;
                        if (!img.src || img.src === window.location.href) {
                            const parent = img.closest('div[data-src], section[data-src]');
                            if (parent) img.src = parent.dataset.src;
                        }
                    });
                }
            """)

            # 滚动页面触发懒加载
            import time as _time
            _time.sleep(1)
            total_height = page.evaluate(
                "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
            )
            page.evaluate(f"window.scrollTo(0, {total_height})")
            _time.sleep(2)

            # 检测验证码
            page_title = page.title()
            if "验证" in page_title or "verify" in page.url.lower():
                raise CaptchaError("页面被验证码拦截，请稍后重试")

            # 检测是否是错误页
            if "唔此页未找到" in page_title or "页面不存在" in page_title:
                raise ParseError("文章不存在或链接已失效")

            return page.content()
        finally:
            context.close()


def fetch_with_requests(url: str, retries: int = 3) -> str:
    """备用：使用 requests 抓取（部分文章可能正文为空）。"""
    if requests is None:
        raise NetworkError("缺少 requests 依赖: pip install requests")

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, timeout=20, allow_redirects=True)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding or "utf-8"
            return resp.text
        except Exception as e:
            if attempt < retries:
                time.sleep(2 ** attempt)
            else:
                raise NetworkError(f"requests 抓取失败: {e}")
    raise NetworkError(f"抓取失败: {url}")


def fetch_html(url: str, use_playwright: bool = True) -> str:
    """
    智能抓取：优先 Playwright（JS 渲染），失败后降级 requests。
    """
    if use_playwright:
        try:
            html = fetch_with_playwright(url)
            return html
        except (ImportError, NetworkError) as e:
            print(f"  [Playwright 不可用] 降级到 requests: {e}")
            return fetch_with_requests(url)
    else:
        return fetch_with_requests(url)


# ─────────────────────────────────────────────
# 3. 元数据提取
# ─────────────────────────────────────────────

def extract_metadata(soup: BeautifulSoup, url: str) -> dict:
    # 标题
    title = ""
    for sel in ["#activity-name", "#js_activity_name", "h1.rich_media_title",
                "h1#activity-name", ".rich_media_title", "#js_title"]:
        el = soup.select_one(sel)
        if el:
            title = el.get_text(strip=True)
            if title:
                break
    if not title:
        title = soup.title.string if soup.title else "未知标题"
    title = html_unescape(title).strip()

    # 作者/公众号
    author = ""
    for sel in ["#js_name", ".profile_nickname", "strong.rich_media_meta_text",
                "#js_author_name", "a.rich_media_meta_link", ".account_nickname_inner"]:
        el = soup.select_one(sel)
        if el:
            author = el.get_text(strip=True)
            if author:
                break
    author = html_unescape(author).strip() if author else "未知公众号"

    # 发布时间
    publish_date = ""
    for sel in ["#publish_time", "em#publish_time"]:
        el = soup.select_one(sel)
        if el:
            publish_date = el.get_text(strip=True)
            if publish_date:
                break
    if not publish_date:
        meta_time = soup.find("meta", attrs={"property": "article:published_time"})
        if meta_time:
            publish_date = meta_time.get("content", "")
    publish_date = html_unescape(publish_date).strip()

    # 描述
    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        description = meta_desc.get("content", "")

    return {
        "title": title,
        "author": author,
        "publish_date": publish_date,
        "description": description,
        "url": url,
    }


# ─────────────────────────────────────────────
# 4. 深度清洗（微信专属噪声移除）
# ─────────────────────────────────────────────

NOISE_SELECTORS = [
    # 脚本 / 样式
    "script", "style", "noscript",
    # 微信广告
    ".mp_profile_iframe", "#js_pc_close", ".qr_code_pc",
    ".ad_container", "#ad_content", ".mp-ad",
    # 赞赏 / 打赏
    ".reward_area", "#reward_area", ".rewards_area",
    ".reward_qrcode_area", ".reward_display",
    # 评论
    "#comment_container", ".discuss_container", "#js_cmt_area",
    ".rich_media_tool", "#js_tags_wrap",
    # 推荐阅读
    "#relation_article", ".relation_article",
    "#recommend_article", ".recommend",
    "#page_bottom",
    # 阅读统计
    ".rich_media_meta_nickname_extra",
    "#js_read_area3", "#js_like_area",
    ".rich_media_footer", "#js_bottom_ad_area",
    # 音视频
    "mpvoice", ".mp_voice_inner",
    "mpvideo", ".mp_video_inner",
    # 二维码
    ".scene_scene_card_qrcode", ".qr_code_pc_area",
    # 版权
    "#copyright_area", ".copyright_area",
    # 其他
    ".rich_media_extra", "#js_ip_wording_wrp",
    ".js_poi_popover", ".global_avatar_msg_card",
    ".rich_media_global_comment_confirm",
    # 音频播放条
    "[id*='audio']", "[class*='audio-player']",
    # 关注公众号提示
    "[class*='follow_tip']", "[class*='guide']",
    # 底部推广
    "[class*='promotion']", "[class*='advertise']",
]


def remove_noise_elements(soup: BeautifulSoup) -> None:
    for selector in NOISE_SELECTORS:
        for el in soup.select(selector):
            el.decompose()


def remove_hidden_elements(soup: BeautifulSoup) -> None:
    for el in list(soup.find_all(True)):
        try:
            if not hasattr(el, "attrs") or el.attrs is None:
                continue
            style = el.get("style", "") or ""
            style_compact = style.replace(" ", "").lower()
            if "display:none" in style_compact or "visibility:hidden" in style_compact:
                el.decompose()
        except Exception:
            continue


def remove_empty_spans(soup: BeautifulSoup) -> None:
    changed = True
    while changed:
        changed = False
        for span in soup.find_all("span"):
            text = span.get_text(strip=True)
            if not text and not span.find("img"):
                span.unwrap()
                changed = True


def fix_wechat_images(soup: BeautifulSoup) -> list:
    """修复微信懒加载图片，返回图片 URL 列表。"""
    img_urls = []
    seen = set()

    for img in soup.find_all("img"):
        # 优先使用 data-src（微信懒加载）
        data_src = img.get("data-src", "")
        if data_src and ("mmbiz" in data_src or data_src.startswith("http")):
            img["src"] = data_src
            if data_src not in seen:
                seen.add(data_src)
                img_urls.append(data_src)

        src = img.get("src", "")
        if src and src not in seen and ("mmbiz" in src or src.startswith("http")):
            seen.add(src)
            img_urls.append(src)

        # 保留 alt，清理 data-* 属性
        for attr in list(img.attrs):
            if attr.startswith("data-") and attr != "data-src":
                del img[attr]
        if not img.get("alt"):
            img["alt"] = ""

    return img_urls


# ─────────────────────────────────────────────
# 5. 代码块处理（精准识别 + 语言自动检测）
# ─────────────────────────────────────────────

LANG_HINTS = {
    "python":     ["def ", "import ", "from ", "class ", "self.", "print(", "if __name__"],
    "javascript": ["const ", "let ", "var ", "function", "=>", "console.log", "document."],
    "typescript": ["interface ", "type ", "enum ", ": string", ": number", "export default"],
    "java":       ["public class", "public static", "System.out", "private ", "protected "],
    "go":         ["func ", "package ", "import (", "fmt.Print", ":=", "chan "],
    "rust":       ["fn ", "let mut", "impl ", "pub fn", "use std::", "#[derive"],
    "c":          ["#include", "printf(", "malloc(", "free(", "int main", "void "],
    "cpp":        ["cout", "cin", "std::", "namespace", "vector<", "#include <"],
    "csharp":     ["using System", "namespace ", "Console.Write", "var ", "async Task"],
    "swift":      ["import UIKit", "guard let", "@IBOutlet", "override func"],
    "kotlin":     ["fun ", "val ", "when (", "companion object", "data class"],
    "ruby":       ["def ", "end\n", "puts ", "require ", "attr_accessor"],
    "php":        ["<?php", "$this", "echo ", "public function", "namespace "],
    "shell":      ["#!/bin/bash", "#!/bin/sh", "echo $", "apt-get", "yum ", "chmod "],
    "sql":        ["SELECT ", "INSERT ", "UPDATE ", "DELETE ", "CREATE TABLE", "ALTER TABLE"],
    "html":       ["<!DOCTYPE", "<html", "<div", "<head", "<body", "<script"],
    "css":        ["margin:", "padding:", "display:", "background:", "color:", "font-"],
    "json":       ['"key":', '"name":', '"type":', '"value":'],
    "yaml":       ["---\n", "key:", "  - ", "apiVersion:", "spec:"],
    "xml":        ["<?xml", "<root", "</root>", "xmlns"],
    "dockerfile": ["FROM ", "RUN ", "COPY ", "WORKDIR", "EXPOSE ", "ENTRYPOINT"],
    "bash":       ["#!/bin/bash", "echo ", "export ", "source ", "if [", "fi\n"],
    "lua":        ["local ", "function ", "require(", "table."],
    "r":          ["<- ", "library(", "ggplot(", "data.frame("],
    "dart":       ["void main()", "Widget", "StatelessWidget", "import 'package"],
    "vue":        ["<template>", "<script setup", "export default {", "defineProps"],
    "jsx":        ["return (", "className=", "import React", "useState("],
}


def detect_language(code_text: str, hint: str = "") -> str:
    """自动检测代码语言。hint 优先，无效时用特征分析。"""
    if hint:
        h = hint.strip().lower()
        if h not in ("text", "plain", "plaintext", "none", ""):
            return h

    first_line = code_text.strip().split("\n")[0] if code_text.strip() else ""
    if first_line.startswith("#!"):
        if "python" in first_line:
            return "python"
        if "bash" in first_line or "/sh" in first_line:
            return "bash"
        if "node" in first_line:
            return "javascript"
        if "ruby" in first_line:
            return "ruby"
        return "bash"

    scores = {}
    sample = code_text[:3000]
    for lang, hints in LANG_HINTS.items():
        score = sum(1 for h in hints if h in sample)
        if score > 0:
            scores[lang] = score

    if scores:
        return max(scores, key=scores.get)
    return ""


def process_code_blocks(soup: BeautifulSoup) -> list:
    """
    识别并提取微信文章代码块，用占位符替换原元素。
    返回 [{"lang": str, "code": str}, ...]
    """
    code_blocks = []
    processed = set()

    # 微信3种代码块格式
    selectors = [
        "pre.code-snippet",
        ".code-snippet__fix",
        "pre[data-lang]",
        "pre",
    ]

    for sel in selectors:
        for el in soup.select(sel):
            el_id = id(el)
            if el_id in processed:
                continue
            # 检查是否是父元素的子集（避免重复处理）
            already_child = False
            for pid in processed:
                pass  # 简化：通过 id 跟踪
            processed.add(el_id)
            _process_single_code(soup, el, code_blocks)

    return code_blocks


def _process_single_code(soup: BeautifulSoup, el: Tag, code_blocks: list) -> None:
    """处理单个代码块。"""
    # 检测语言
    lang = ""
    if el.get("data-lang"):
        lang = el.get("data-lang", "")
    for cls in el.get("class", []):
        cls_str = str(cls)
        if cls_str.startswith("language-") or cls_str.startswith("lang-"):
            lang = cls_str.split("-", 1)[1]
            break
        if cls_str in ("python", "javascript", "java", "go", "rust", "cpp", "c",
                       "css", "html", "json", "yaml", "sql", "bash", "shell",
                       "php", "ruby", "swift", "kotlin", "typescript", "csharp"):
            lang = cls_str
            break

    # 移除行号元素
    for line_el in el.select(".code-snippet__line-index, [class*='line-number'], .hljs-ln-n"):
        line_el.decompose()

    # 提取代码文本
    code_tag = el.find("code")
    if code_tag:
        raw_text = code_tag.get_text(separator="\n")
    else:
        raw_text = el.get_text(separator="\n")

    # 清理行 - 过滤 CSS counter 泄漏
    lines = []
    for line in raw_text.split("\n"):
        stripped = line.strip()
        if re.match(r"^[ce]?ounter\(line", stripped):
            continue
        lines.append(line)

    code_text = "\n".join(lines).strip()
    if not code_text:
        return

    detected_lang = detect_language(code_text, lang)
    idx = len(code_blocks)
    placeholder = f"__CODEBLOCK_{idx}__"

    code_blocks.append({"lang": detected_lang, "code": code_text})

    # 替换为占位段落
    p = _make_tag(soup, "p")
    if p is None:
        p = soup.new_tag("p")
    if p is None:
        return
    p.string = placeholder
    el.replace_with(p)


# ─────────────────────────────────────────────
# 6. 富文本优化
# ─────────────────────────────────────────────

def optimize_rich_text(soup) -> None:
    """优化列表、引用、加粗、斜体等富文本格式。"""
    # 找到根 BeautifulSoup 对象（用于创建新标签）
    root = soup
    while hasattr(root, "parent") and root.parent is not None:
        root = root.parent
    # 如果是 BeautifulSoup 对象则直接用，否则用 soup 自身
    tag_creator = root if hasattr(root, "new_tag") else soup

    # section 语义化
    for section in list(soup.find_all("section")):
        try:
            style = section.get("style", "") or ""
            style = style.replace(" ", "").lower()
            class_str = " ".join(str(c) for c in section.get("class", []))

            if "border-left" in style or "borderleft" in style or "blockquote" in class_str:
                section.name = "blockquote"
                continue

            if "background-color" in style and "font-family" in style:
                text = section.get_text(strip=True)
                if text and len(text) < 200 and not section.find("img"):
                    code = _make_tag(soup, "code")
                    if code is not None:
                        code.string = text
                        section.replace_with(code)
                    continue

            if "font-size" in style:
                m = re.search(r"font-size:\s*(\d+)px", section.get("style", "") or "")
                if m:
                    size = int(m.group(1))
                    if size >= 22:
                        section.name = "h2"
                    elif size >= 19:
                        section.name = "h3"
                    elif size >= 17:
                        section.name = "h4"
        except Exception:
            continue

    # b → strong, i → em
    for b in list(soup.find_all("b")):
        try:
            b.name = "strong"
        except Exception:
            pass
    for i_tag in list(soup.find_all("i")):
        try:
            if not i_tag.find_parent("em"):
                i_tag.name = "em"
        except Exception:
            pass

    # 微信列表特殊标记还原
    _fix_pseudo_lists(soup)

    # 清理空段落
    for p in list(soup.find_all("p")):
        try:
            if not p.get_text(strip=True) and not p.find("img"):
                p.decompose()
        except Exception:
            pass


def _make_tag(soup, name: str):
    """安全创建 BS4 标签，处理 new_tag 可能返回 None 的情况。"""
    try:
        tag = soup.new_tag(name)
        if tag is not None:
            return tag
    except Exception:
        pass
    # 降级：从字符串解析
    try:
        return BeautifulSoup(f"<{name}></{name}>", "html.parser").find(name)
    except Exception:
        return None


def _fix_pseudo_lists(soup) -> None:
    """将以列表符号开头的段落转为真正的列表项。"""
    LIST_MARKERS = set("•·◦▪▫●○◆◇►▸■□➤➢➣➡→✓✔✗✘")

    for p in list(soup.find_all("p")):
        try:
            text = p.get_text(strip=True)
            if not text:
                continue

            # 无序列表
            if text[0] in LIST_MARKERS:
                li = _make_tag(soup, "li")
                if li is None:
                    continue
                for child in list(p.children):
                    c = child
                    if isinstance(c, NavigableString):
                        stripped = str(c).lstrip()
                        if stripped and stripped[0] in LIST_MARKERS:
                            c = NavigableString(stripped[1:].lstrip())
                    li.append(c)
                p.replace_with(li)
                continue

            # 有序列表 "1. " "1) "
            m = re.match(r"^(\d+)[.)]\s+", text)
            if m:
                li = _make_tag(soup, "li")
                if li is None:
                    continue
                for child in list(p.children):
                    c = child
                    if isinstance(c, NavigableString):
                        s = str(c).lstrip()
                        mm = re.match(r"^\d+[.)]\s+", s)
                        if mm:
                            c = NavigableString(s[mm.end():])
                    li.append(c)
                p.replace_with(li)
        except Exception:
            continue


# ─────────────────────────────────────────────
# 7. HTML → Markdown
# ─────────────────────────────────────────────

def html_to_markdown(content_html: str, code_blocks: list) -> str:
    """转换 HTML 到 Markdown，还原代码块占位符。"""
    if not content_html.strip():
        return ""

    md = markdownify.markdownify(
        content_html,
        heading_style="ATX",
        bullets="-",
        newline_style="backslash",
        convert=[
            "p", "h1", "h2", "h3", "h4", "h5", "h6",
            "strong", "b", "em", "i", "a", "img",
            "ul", "ol", "li", "blockquote",
            "br", "hr",
            "table", "thead", "tbody", "tr", "th", "td",
            "pre", "code",
            "sup", "sub", "del", "s",
        ],
    )

    # 还原代码块
    for i, block in enumerate(code_blocks):
        placeholder = f"__CODEBLOCK_{i}__"
        lang = block.get("lang", "")
        code = block.get("code", "")
        fenced = f"\n\n```{lang}\n{code}\n```\n\n"
        md = md.replace(placeholder, fenced)
        md = md.replace(f"`{placeholder}`", fenced)
        md = md.replace(f"\\`{placeholder}\\`", fenced)

    return md


# ─────────────────────────────────────────────
# 8. Markdown 后处理
# ─────────────────────────────────────────────

def postprocess_markdown(md: str, metadata: dict, no_frontmatter: bool = False) -> str:
    # 清理特殊字符
    md = md.replace("\u00a0", " ")   # &nbsp;
    md = md.replace("\u200b", "")    # 零宽空格
    md = md.replace("\u200c", "")    # 零宽不连接
    md = md.replace("\u200d", "")    # 零宽连接
    md = md.replace("\u3000", "  ")  # 全角空格
    md = html_unescape(md)

    # 清理多余空行
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    # 清理行尾空格
    md = re.sub(r"[ \t]+$", "", md, flags=re.MULTILINE)
    # 代码块前后统一空行
    md = re.sub(r"\n{3,}(```)", r"\n\n```", md)
    md = re.sub(r"(```)\n{3,}", r"```\n\n", md)

    # 修复可能的 backslash 换行在普通文本中的滥用
    md = re.sub(r"\\\n\n", "\n\n", md)

    if no_frontmatter:
        return md.strip() + "\n"

    return _build_frontmatter(metadata) + "\n\n" + md.strip() + "\n"


def _build_frontmatter(meta: dict) -> str:
    def ey(s):
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()

    lines = [
        "---",
        f'title: "{ey(meta.get("title", ""))}"',
        f'author: "{ey(meta.get("author", ""))}"',
        f'date: "{ey(meta.get("publish_date", ""))}"',
        f'source: "{ey(meta.get("url", ""))}"',
    ]
    if meta.get("description"):
        lines.append(f'description: "{ey(meta["description"])}"')
    lines.append("---")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 9. 图片下载（可选）
# ─────────────────────────────────────────────

def sanitize_filename(name: str) -> str:
    name = unicodedata.normalize("NFKC", name)
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "", name)
    name = re.sub(r"\s+", "_", name)
    name = name.strip("._")
    return name[:80] if len(name) > 80 else name or "article"


def guess_image_ext(url: str) -> str:
    p = urlparse(url).path.lower()
    for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"]:
        if p.endswith(ext):
            return ext
    return ".jpg"


def download_images(img_urls: list, output_dir: Path, concurrency: int = 5,
                    timeout: int = 30, retries: int = 2) -> dict:
    """
    下载图片到本地，返回 URL 到本地路径的映射。
    增强版：支持重试、更详细的错误报告、Content-Type 检测。
    """
    if requests is None:
        print("  [警告] requests 不可用，跳过图片下载")
        return {}

    import concurrent.futures
    from time import sleep

    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    url_to_local = {}

    def _get_ext_from_content_type(resp) -> str:
        """从响应头检测图片格式"""
        content_type = resp.headers.get("Content-Type", "").lower()
        if "png" in content_type:
            return ".png"
        if "gif" in content_type:
            return ".gif"
        if "webp" in content_type:
            return ".webp"
        if "jpeg" in content_type or "jpg" in content_type:
            return ".jpg"
        if "svg" in content_type:
            return ".svg"
        if "bmp" in content_type:
            return ".bmp"
        return ""

    def _download_one(url: str, index: int):
        """下载单张图片，支持重试"""
        ext = guess_image_ext(url)
        filepath = images_dir / f"img_{index:03d}{ext}"

        for attempt in range(retries + 1):
            try:
                resp = requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS,
                                    stream=True, allow_redirects=True)
                resp.raise_for_status()

                # 检测 Content-Type 修正扩展名
                detected_ext = _get_ext_from_content_type(resp)
                if detected_ext and detected_ext != ext:
                    ext = detected_ext
                    filepath = images_dir / f"img_{index:03d}{ext}"

                # 检查文件是否已存在且大小正常
                if filepath.exists():
                    existing_size = filepath.stat().st_size
                    if existing_size > 100:  # 至少 100 字节
                        return url, str(filepath)

                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        if chunk:
                            f.write(chunk)

                # 验证文件大小
                if filepath.stat().st_size < 100:
                    filepath.unlink()
                    raise ValueError(f"图片太小 ({filepath.stat().st_size} bytes)")

                return url, str(filepath)

            except Exception as e:
                if attempt < retries:
                    sleep(0.5 * (attempt + 1))
                    continue
                return url, None

        return url, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as exe:
        futures = {exe.submit(_download_one, url, i): url
                   for i, url in enumerate(img_urls)}
        failed = 0
        failed_urls = []
        for future in concurrent.futures.as_completed(futures):
            url, local = future.result()
            if local:
                url_to_local[url] = local
            else:
                failed += 1
                failed_urls.append(url[:80] + "..." if len(url) > 80 else url)

    if failed:
        print(f"  [警告] {failed}/{len(img_urls)} 张图片下载失败")
        if failed <= 3:
            for url in failed_urls:
                print(f"      - {url}")
    else:
        print(f"  [OK] 全部 {len(img_urls)} 张图片下载成功")

    return url_to_local


def normalize_image_url(url: str) -> str:
    """标准化图片 URL，用于匹配不同格式的同一图片链接"""
    # 处理微信图片 URL 的常见变体
    url = url.strip()
    # 移除常见的查询参数差异
    url = re.sub(r'[?&](wx_fmt|tp|wxfrom|wx_lazy|wx_co)=[^&]*', '', url)
    # 移除末尾的 ? 或 &
    url = url.rstrip('?&')
    return url


def replace_image_urls(md: str, url_to_local: dict, obsidian_format: bool = False) -> str:
    """
    替换 Markdown 中的图片 URL 为本地相对路径。
    增强版：处理 URL 变体、HTML img 标签、多种 Markdown 格式。

    Args:
        md: Markdown 内容
        url_to_local: URL 到本地路径的映射
        obsidian_format: 是否使用 Obsidian Wiki 链接格式 ![[图片]]
    """
    if not url_to_local:
        return md

    # 构建 URL 到相对路径的映射
    url_to_relative = {}
    for orig, local in url_to_local.items():
        relative = "images/" + Path(local).name
        url_to_relative[orig] = relative
        # 同时存储标准化版本
        normalized = normalize_image_url(orig)
        if normalized != orig:
            url_to_relative[normalized] = relative

    # Obsidian 格式：使用 ![[文件名]]
    if obsidian_format:
        for orig, local in url_to_local.items():
            filename = Path(local).name
            # 替换标准 Markdown 图片格式 ![...](url)
            pattern = r'!\[([^\]]*)\]\(' + re.escape(orig) + r'\)'
            md = re.sub(pattern, lambda m, fn=filename: f'![[{fn}]]', md)
            # 替换 HTML img 标签
            pattern = r'<img[^>]+src=["\']' + re.escape(orig) + r'["\'][^>]*>'
            md = re.sub(pattern, lambda m, fn=filename: f'![[{fn}]]', md, flags=re.IGNORECASE)
        return md

    # 标准 Markdown 格式
    # 1. 直接替换原始 URL
    for orig, relative in list(url_to_relative.items()):
        md = md.replace(orig, relative)

    # 2. 处理微信图片 URL 的常见变体（mmbiz 链接）
    # 微信图片 URL 可能带有不同的查询参数但指向同一图片
    for orig, relative in url_to_local.items():
        # 提取基础 URL（不含查询参数）
        base_url = orig.split('?')[0]
        if base_url != orig:
            # 替换基础 URL
            md = md.replace(base_url, relative)
            # 替换带不同查询参数的变体 - 使用 lambda 避免转义问题
            pattern = re.escape(base_url) + r'(?:\?[^)"\]\s]*)?'
            md = re.sub(pattern, lambda m: relative, md)

    # 3. 处理 HTML img 标签
    # 匹配 <img src="..."> 或 <img src='...'>
    def replace_img_src(match):
        full_tag = match.group(0)
        src = match.group(1)
        for orig, relative in url_to_local.items():
            if src == orig or normalize_image_url(src) == normalize_image_url(orig):
                return full_tag.replace(src, relative)
        return full_tag

    md = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', replace_img_src, md, flags=re.IGNORECASE)

    # 4. 清理可能的重复路径（如 images/images/img_xxx.jpg）
    md = re.sub(r'images/images/', 'images/', md)

    return md


# ─────────────────────────────────────────────
# 10. 主流程
# ─────────────────────────────────────────────

def convert_article(url: str, output_dir: str = "./output",
                    download_imgs: bool = True,
                    no_frontmatter: bool = False,
                    use_playwright: bool = True,
                    obsidian_format: bool = False) -> str:
    """
    一键转换微信公众号文章为高质量 Markdown。
    返回生成的 Markdown 文件路径。
    """
    url = normalize_url(url)
    print(f"[*] 正在抓取: {url}")

    html = fetch_html(url, use_playwright=use_playwright)
    print(f"[OK] HTML 获取成功 ({len(html)} 字节)")

    soup = BeautifulSoup(html, "html.parser")
    metadata = extract_metadata(soup, url)
    print(f"[OK] 文章: {metadata['title']} | 作者: {metadata['author']}")

    # 定位正文容器
    content_el = None
    for sel in ["#js_content", ".rich_media_content", "#page-content", "article"]:
        content_el = soup.select_one(sel)
        if content_el and content_el.get_text(strip=True):
            break

    if not content_el or not content_el.get_text(strip=True):
        raise ParseError("无法找到文章正文（js_content 为空或不存在）")

    print(f"[OK] 正文容器: 约 {len(content_el.get_text())} 字符")

    # 深度清洗流水线
    remove_noise_elements(content_el)
    remove_hidden_elements(content_el)
    img_urls = fix_wechat_images(content_el)
    code_blocks = process_code_blocks(content_el)
    optimize_rich_text(content_el)
    remove_empty_spans(content_el)

    print(f"[OK] 清洗完成 | 代码块: {len(code_blocks)} | 图片: {len(img_urls)}")

    # 追加收集剩余图片
    seen_imgs = set(img_urls)
    for img in content_el.find_all("img", src=True):
        src = img["src"]
        if src not in seen_imgs and ("mmbiz" in src or src.startswith("http")):
            seen_imgs.add(src)
            img_urls.append(src)

    # HTML → Markdown
    content_html = str(content_el)
    md = html_to_markdown(content_html, code_blocks)
    result = postprocess_markdown(md, metadata, no_frontmatter=no_frontmatter)

    # 输出目录
    out_path = Path(output_dir)
    article_dir = out_path / sanitize_filename(metadata["title"])
    article_dir.mkdir(parents=True, exist_ok=True)

    # 下载图片
    if download_imgs and img_urls:
        print(f"[*] 下载 {len(img_urls)} 张图片...")
        url_to_local = download_images(img_urls, article_dir)
        if url_to_local:
            result = replace_image_urls(result, url_to_local, obsidian_format=obsidian_format)
        print(f"[OK] 图片: {len(url_to_local)}/{len(img_urls)}")

    # 保存
    md_path = article_dir / (sanitize_filename(metadata["title"]) + ".md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"[OK] 已保存: {md_path}")
    return str(md_path)


def convert_simple(url: str, use_playwright: bool = True,
                   download_imgs: bool = False, output_dir: str = None,
                   obsidian_format: bool = False) -> dict:
    """
    简化版：返回 {markdown, metadata, code_blocks, image_urls}。
    支持可选的图片下载，适合在 AI Agent 中内联调用。

    Args:
        url: 微信文章 URL
        use_playwright: 是否使用 Playwright 抓取
        download_imgs: 是否下载图片到本地
        output_dir: 图片下载目录（默认使用文章标题作为目录名）

    Returns:
        dict: {
            "markdown": str,          # Markdown 内容（已替换本地图片路径）
            "metadata": dict,         # {title, author, date, url, ...}
            "code_blocks": list,      # [{lang, code}, ...]
            "image_urls": list,       # 原始图片 URL 列表
            "image_mapping": dict,    # URL -> 本地路径映射（仅当 download_imgs=True）
            "output_dir": str,        # 输出目录（仅当 download_imgs=True）
        }
    """
    url = normalize_url(url)
    html = fetch_html(url, use_playwright=use_playwright)
    soup = BeautifulSoup(html, "html.parser")
    metadata = extract_metadata(soup, url)

    content_el = None
    for sel in ["#js_content", ".rich_media_content", "#page-content", "article"]:
        content_el = soup.select_one(sel)
        if content_el and content_el.get_text(strip=True):
            break

    if not content_el or not content_el.get_text(strip=True):
        raise ParseError("无法找到文章正文")

    remove_noise_elements(content_el)
    remove_hidden_elements(content_el)
    img_urls = fix_wechat_images(content_el)
    code_blocks = process_code_blocks(content_el)
    optimize_rich_text(content_el)
    remove_empty_spans(content_el)

    content_html = str(content_el)
    md = html_to_markdown(content_html, code_blocks)
    md = postprocess_markdown(md, metadata)

    result = {
        "markdown": md,
        "metadata": metadata,
        "code_blocks": code_blocks,
        "image_urls": img_urls,
    }

    # 可选：下载图片并替换链接
    if download_imgs and img_urls and requests:
        if output_dir is None:
            output_dir = f"./output/{sanitize_filename(metadata['title'])}"

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        print(f"[*] 下载 {len(img_urls)} 张图片到 {out_path}...")
        url_to_local = download_images(img_urls, out_path)

        if url_to_local:
            md = replace_image_urls(md, url_to_local, obsidian_format=obsidian_format)
            result["markdown"] = md
            result["image_mapping"] = url_to_local
            result["output_dir"] = str(out_path)
            print(f"[OK] 已替换 {len(url_to_local)}/{len(img_urls)} 张图片链接")

    return result


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser_cli = argparse.ArgumentParser(
        description="微信公众号文章 → 高质量 Markdown 转换工具",
        epilog="示例: python wechat_to_md.py https://mp.weixin.qq.com/s/xxxxx -o ./output",
    )
    parser_cli.add_argument("urls", nargs="+", help="微信文章 URL（支持多个）")
    parser_cli.add_argument("-o", "--output", default="./output", help="输出目录（默认: ./output）")
    parser_cli.add_argument("--no-images", action="store_true", help="不下载图片")
    parser_cli.add_argument("--no-frontmatter", action="store_true", help="不生成 YAML Frontmatter")
    parser_cli.add_argument("--no-playwright", action="store_true", help="不使用 Playwright（降级到 requests）")
    parser_cli.add_argument("--obsidian", action="store_true", help="使用 Obsidian Wiki 链接格式 ![[图片]]")

    args = parser_cli.parse_args()
    use_pw = not args.no_playwright

    success = 0
    for url in args.urls:
        try:
            convert_article(
                url,
                output_dir=args.output,
                download_imgs=not args.no_images,
                no_frontmatter=args.no_frontmatter,
                use_playwright=use_pw,
                obsidian_format=args.obsidian,
            )
            success += 1
        except CaptchaError as e:
            print(f"[FAIL] 验证码拦截: {e}")
        except NetworkError as e:
            print(f"[FAIL] 网络错误: {e}")
        except ParseError as e:
            print(f"[FAIL] 解析错误: {e}")
        except Exception as e:
            import traceback
            print(f"[FAIL] 未知错误: {type(e).__name__}: {e}")
            traceback.print_exc()

    print(f"\n完成: {success}/{len(args.urls)} 篇成功")
    if success < len(args.urls):
        sys.exit(1)


if __name__ == "__main__":
    main()
