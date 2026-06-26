#!/usr/bin/env python3
"""
content-engine 平台适配器模块

将通用内容适配为各平台特定格式，支持 Twitter、LinkedIn、微信公众号、博客、Medium。
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    count_chars,
    format_platform_name,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    sanitize_html,
    truncate_text,
    validate_platform,
    write_json_file,
    PLATFORMS,
    PLATFORM_CHAR_LIMITS,
)


# ============================================================
# Obsidian 格式处理
# ============================================================

def _convert_obsidian_wikilinks(text: str, mode: str = "plain") -> str:
    """转换 Obsidian [[wikilinks]] 为目标格式。

    Args:
        text: 包含 wikilinks 的文本。
        mode: 转换模式 — "plain" 转纯文本，"hyperlink" 转 Markdown 链接。

    Returns:
        转换后的文本。
    """
    # [[显示文本|链接目标]] 格式
    if mode == "hyperlink":
        text = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"[\2](\1)", text)
        text = re.sub(r"\[\[([^\]]+)\]\]", r"[\1](\1)", text)
    else:
        text = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", text)
        text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    return text


def _add_image_prompt_placeholders(text: str, image_prompts: list) -> str:
    """在适配内容中插入配图提示词占位符。

    Args:
        text: 适配后的内容文本。
        image_prompts: 图片提示词列表，每项包含 position, prompt 字段。

    Returns:
        插入占位符后的文本。
    """
    if not image_prompts:
        return text
    # 在文本末尾追加配图建议
    parts = [text, "", "---", ""]
    for i, img in enumerate(image_prompts, 1):
        prompt = img.get("prompt", img.get("description", ""))
        position = img.get("position", f"位置{i}")
        parts.append(f"[建议配图 {i} ({position}): {prompt}]")
    return "\n".join(parts)


def _generate_seo_metadata(content: Dict[str, Any]) -> Dict[str, Any]:
    """为博客内容生成 SEO 元数据。

    Args:
        content: 内容字典，包含 title, body, tags, summary 等字段。

    Returns:
        包含 meta_description, keywords, og_title, og_description 的字典。
    """
    title = content.get("title", "")
    body = content.get("body", "")
    summary = content.get("summary", "")
    tags = content.get("tags", [])

    # meta description: 优先使用摘要，否则截取正文前 160 字符
    meta_desc = summary if summary else ""
    if not meta_desc:
        # 清理 Markdown 标记
        clean_body = re.sub(r"[#*`\[\]()>]", "", body)
        clean_body = re.sub(r"\s+", " ", clean_body).strip()
        meta_desc = clean_body[:160]
        if len(clean_body) > 160:
            meta_desc = meta_desc[:157] + "..."

    # keywords: 基于标签和标题
    keywords = list(tags[:10])

    # 从标题提取额外关键词
    title_words = re.findall(r"[\w\u4e00-\u9fff]{2,}", title)
    for w in title_words:
        if w not in keywords and len(keywords) < 15:
            keywords.append(w)

    # Open Graph 数据
    og_title = title
    og_description = meta_desc[:200] if meta_desc else title

    return {
        "meta_description": meta_desc,
        "keywords": keywords,
        "og_title": og_title,
        "og_description": og_description,
    }


# ============================================================
# 数据文件路径
# ============================================================

CONTENTS_FILE = "contents.json"
ADAPTED_FILE = "adapted_contents.json"


def _get_contents() -> List[Dict[str, Any]]:
    """读取所有内容数据。"""
    return read_json_file(get_data_file(CONTENTS_FILE))


def _find_content(contents: List[Dict], content_id: str) -> Optional[Dict]:
    """根据 ID 查找内容。"""
    for c in contents:
        if c.get("id") == content_id:
            return c
    return None


def _get_adapted() -> List[Dict[str, Any]]:
    """读取所有已适配内容。"""
    return read_json_file(get_data_file(ADAPTED_FILE))


def _save_adapted(adapted: List[Dict[str, Any]]) -> None:
    """保存已适配内容到文件。"""
    write_json_file(get_data_file(ADAPTED_FILE), adapted)


# ============================================================
# Twitter 适配
# ============================================================

def _adapt_twitter(content: Dict[str, Any]) -> Dict[str, Any]:
    """将内容适配为 Twitter 格式。

    规则:
    - 单条推文限 280 字符（中文字符占 2 位）
    - 超长内容自动拆分为 thread
    - 图片转为 alt text 描述
    - 自动添加 hashtag

    Args:
        content: 原始内容字典。

    Returns:
        适配后的 Twitter 格式数据。
    """
    body = content.get("body", "")
    tags = content.get("tags", [])
    title = content.get("title", "")

    # 移除 Markdown 图片，转为 alt text
    body = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"[\1]", body)

    # 移除其他 Markdown 格式标记
    body = re.sub(r"\*\*(.+?)\*\*", r"\1", body)
    body = re.sub(r"\*(.+?)\*", r"\1", body)
    body = re.sub(r"#{1,6}\s+", "", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"```[\s\S]*?```", "[代码块]", body)
    body = re.sub(r"`([^`]+)`", r"\1", body)
    body = re.sub(r">\s+(.+)", r"\1", body)
    body = re.sub(r"\n{3,}", "\n\n", body)

    # 生成 hashtag 字符串
    hashtags = " ".join(f"#{t.replace(' ', '')}" for t in tags[:5])

    # 计算单条推文可用字符数
    max_chars = 280
    # 预留 hashtag 空间
    hashtag_chars = count_chars(hashtags, "twitter") + 1 if hashtags else 0
    available_chars = max_chars - hashtag_chars

    # 拆分为 thread
    text = f"{title}\n\n{body}".strip() if title else body.strip()
    tweets = _split_twitter_thread(text, available_chars)

    # 在最后一条推文末尾添加 hashtag
    if hashtags and tweets:
        last = tweets[-1]
        if count_chars(last + "\n\n" + hashtags, "twitter") <= max_chars:
            tweets[-1] = last + "\n\n" + hashtags
        else:
            tweets.append(hashtags)

    # 如果是 thread，添加编号
    if len(tweets) > 1:
        numbered = []
        for i, tweet in enumerate(tweets, 1):
            prefix = f"({i}/{len(tweets)}) "
            # 确保编号后不超限
            prefix_chars = count_chars(prefix, "twitter")
            if count_chars(tweet, "twitter") + prefix_chars > max_chars:
                tweet = truncate_text(tweet, max_chars - prefix_chars - 3)
            numbered.append(prefix + tweet)
        tweets = numbered

    return {
        "platform": "twitter",
        "platform_name": format_platform_name("twitter"),
        "format": "thread" if len(tweets) > 1 else "tweet",
        "tweets": tweets,
        "tweet_count": len(tweets),
        "hashtags": tags[:5],
        "char_counts": [count_chars(t, "twitter") for t in tweets],
    }


def _split_twitter_thread(text: str, max_chars: int) -> List[str]:
    """将文本拆分为 Twitter thread。

    按段落拆分，每段不超过 max_chars 字符。

    Args:
        text: 原始文本。
        max_chars: 每条推文最大字符数。

    Returns:
        推文列表。
    """
    if count_chars(text, "twitter") <= max_chars:
        return [text]

    # 按段落拆分
    paragraphs = text.split("\n\n")
    tweets = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        test_text = (current + "\n\n" + para).strip() if current else para
        if count_chars(test_text, "twitter") <= max_chars:
            current = test_text
        else:
            if current:
                tweets.append(current)
            # 如果单个段落超限，按句子拆分
            if count_chars(para, "twitter") > max_chars:
                sentences = re.split(r"([。！？.!?])", para)
                current = ""
                for i in range(0, len(sentences) - 1, 2):
                    sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
                    test_s = (current + sentence).strip() if current else sentence
                    if count_chars(test_s, "twitter") <= max_chars:
                        current = test_s
                    else:
                        if current:
                            tweets.append(current)
                        current = sentence
                # 处理最后未配对的部分
                if len(sentences) % 2 == 1 and sentences[-1].strip():
                    test_s = (current + sentences[-1]).strip() if current else sentences[-1]
                    if count_chars(test_s, "twitter") <= max_chars:
                        current = test_s
                    else:
                        if current:
                            tweets.append(current)
                        current = sentences[-1]
            else:
                current = para

    if current:
        tweets.append(current)

    return tweets if tweets else [text[:max_chars]]


# ============================================================
# LinkedIn 适配
# ============================================================

def _adapt_linkedin(content: Dict[str, Any]) -> Dict[str, Any]:
    """将内容适配为 LinkedIn 格式。

    规则:
    - 专业语气格式
    - 3000 字符限制
    - 适当的换行和段落
    - 添加行动号召

    Args:
        content: 原始内容字典。

    Returns:
        适配后的 LinkedIn 格式数据。
    """
    title = content.get("title", "")
    body = content.get("body", "")
    tags = content.get("tags", [])
    summary = content.get("summary", "")

    # 移除 Markdown 格式但保留结构
    text = body
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", "", text)  # 移除图片
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)       # 粗体
    text = re.sub(r"\*(.+?)\*", r"\1", text)            # 斜体
    text = re.sub(r"#{1,6}\s+(.+)", r"\1", text)        # 标题转纯文本
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)  # 链接
    text = re.sub(r"```[\s\S]*?```", "", text)           # 移除代码块
    text = re.sub(r"`([^`]+)`", r"\1", text)             # 行内代码

    # 构建 LinkedIn 帖子
    parts = []

    # 标题（粗体效果用大写或符号标记）
    if title:
        parts.append(title)
        parts.append("")

    # 摘要或正文
    if summary:
        parts.append(summary)
        parts.append("")

    parts.append(text.strip())

    # 添加 hashtag
    if tags:
        parts.append("")
        parts.append(" ".join(f"#{t.replace(' ', '')}" for t in tags[:10]))

    result_text = "\n".join(parts)

    # 截断到 3000 字符
    char_count = count_chars(result_text, "linkedin")
    if char_count > 3000:
        result_text = truncate_text(result_text, 3000)
        char_count = count_chars(result_text, "linkedin")

    return {
        "platform": "linkedin",
        "platform_name": format_platform_name("linkedin"),
        "format": "post",
        "text": result_text,
        "char_count": char_count,
        "char_limit": 3000,
        "hashtags": tags[:10],
    }


# ============================================================
# 微信公众号适配
# ============================================================

def _adapt_wechat(content: Dict[str, Any]) -> Dict[str, Any]:
    """将内容适配为微信公众号文章格式。

    规则:
    - HTML 文章格式
    - 图片引用保留
    - 作者信息卡片
    - 富文本排版

    Args:
        content: 原始内容字典。

    Returns:
        适配后的微信公众号格式数据。
    """
    title = content.get("title", "")
    body = content.get("body", "")
    author = content.get("author", "")
    summary = content.get("summary", "")
    tags = content.get("tags", [])

    # Markdown 转 HTML
    html = _markdown_to_html(body)

    # 清理危险 HTML
    html = sanitize_html(html)

    # 构建完整的微信文章 HTML
    article_parts = []

    # 文章标题
    article_parts.append(f"<h1>{_escape_html(title)}</h1>")

    # 作者信息卡片
    if author:
        article_parts.append(
            f'<div class="author-card">'
            f'<span class="author-name">{_escape_html(author)}</span>'
            f"</div>"
        )

    # 摘要
    if summary:
        article_parts.append(
            f'<blockquote class="summary">{_escape_html(summary)}</blockquote>'
        )

    # 正文
    article_parts.append(f'<div class="content">{html}</div>')

    # 标签
    if tags:
        tag_html = " ".join(
            f'<span class="tag">#{_escape_html(t)}</span>' for t in tags
        )
        article_parts.append(f'<div class="tags">{tag_html}</div>')

    full_html = "\n".join(article_parts)
    char_count = count_chars(body, "wechat")

    # 提取图片引用
    images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content.get("body", ""))
    image_refs = [{"alt": alt, "url": url} for alt, url in images]

    return {
        "platform": "wechat",
        "platform_name": format_platform_name("wechat"),
        "format": "article",
        "title": title,
        "html": full_html,
        "digest": truncate_text(summary or body, 120),
        "author": author,
        "char_count": char_count,
        "image_refs": image_refs,
        "tags": tags,
    }


def _markdown_to_html(md: str) -> str:
    """简单的 Markdown 转 HTML。

    仅处理常用格式，不依赖第三方库。

    Args:
        md: Markdown 文本。

    Returns:
        HTML 字符串。
    """
    html = md

    # 代码块
    html = re.sub(
        r"```(\w*)\n([\s\S]*?)```",
        r'<pre><code class="language-\1">\2</code></pre>',
        html,
    )

    # 行内代码
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

    # 标题
    html = re.sub(r"^######\s+(.+)$", r"<h6>\1</h6>", html, flags=re.MULTILINE)
    html = re.sub(r"^#####\s+(.+)$", r"<h5>\1</h5>", html, flags=re.MULTILINE)
    html = re.sub(r"^####\s+(.+)$", r"<h4>\1</h4>", html, flags=re.MULTILINE)
    html = re.sub(r"^###\s+(.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^##\s+(.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^#\s+(.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)

    # 粗体和斜体
    html = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", html)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

    # 图片
    html = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        r'<img src="\2" alt="\1" />',
        html,
    )

    # 链接
    html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', html)

    # 引用
    html = re.sub(r"^>\s+(.+)$", r"<blockquote>\1</blockquote>", html, flags=re.MULTILINE)

    # 无序列表
    html = re.sub(r"^[-*+]\s+(.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)

    # 段落（连续空行分隔）
    paragraphs = html.split("\n\n")
    processed = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        # 已经被标签包裹的不再加 <p>
        if re.match(r"^<(h[1-6]|pre|blockquote|li|ul|ol|div|img)", p):
            processed.append(p)
        else:
            processed.append(f"<p>{p}</p>")
    html = "\n".join(processed)

    return html


def _escape_html(text: str) -> str:
    """转义 HTML 特殊字符。

    Args:
        text: 原始文本。

    Returns:
        转义后的文本。
    """
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


# ============================================================
# 博客适配
# ============================================================

def _adapt_blog(content: Dict[str, Any]) -> Dict[str, Any]:
    """将内容适配为博客格式。

    支持 Hugo、Jekyll、Hexo 三种博客引擎，通过 CE_BLOG_TYPE 环境变量指定。

    Args:
        content: 原始内容字典。

    Returns:
        适配后的博客格式数据。
    """
    blog_type = os.environ.get("CE_BLOG_TYPE", "hugo").lower()
    title = content.get("title", "")
    body = content.get("body", "")
    tags = content.get("tags", [])
    author = content.get("author", "")
    summary = content.get("summary", "")
    now = now_iso()

    if blog_type == "jekyll":
        # Jekyll frontmatter 使用 YAML
        frontmatter = _build_jekyll_frontmatter(title, tags, author, summary, now)
    elif blog_type == "hexo":
        # Hexo frontmatter
        frontmatter = _build_hexo_frontmatter(title, tags, author, summary, now)
    else:
        # Hugo frontmatter（默认）
        frontmatter = _build_hugo_frontmatter(title, tags, author, summary, now)

    markdown = frontmatter + "\n" + body

    # 生成文件名建议
    slug = re.sub(r"[^\w\u4e00-\u9fff-]", "-", title.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_prefix}-{slug}.md" if blog_type == "jekyll" else f"{slug}.md"

    return {
        "platform": "blog",
        "platform_name": format_platform_name("blog"),
        "format": f"markdown-{blog_type}",
        "blog_type": blog_type,
        "markdown": markdown,
        "suggested_filename": filename,
        "char_count": len(body),
    }


def _build_hugo_frontmatter(title: str, tags: List[str], author: str, summary: str, date: str) -> str:
    """生成 Hugo 格式的 frontmatter。"""
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f"date: {date}")
    if author:
        lines.append(f'author: "{author}"')
    if summary:
        lines.append(f'description: "{summary}"')
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f'  - "{t}"')
    lines.append("draft: false")
    lines.append("---")
    return "\n".join(lines)


def _build_jekyll_frontmatter(title: str, tags: List[str], author: str, summary: str, date: str) -> str:
    """生成 Jekyll 格式的 frontmatter。"""
    lines = ["---"]
    lines.append("layout: post")
    lines.append(f'title: "{title}"')
    lines.append(f"date: {date}")
    if author:
        lines.append(f'author: "{author}"')
    if summary:
        lines.append(f'excerpt: "{summary}"')
    if tags:
        tags_str = ", ".join(tags)
        lines.append(f"tags: [{tags_str}]")
    lines.append("---")
    return "\n".join(lines)


def _build_hexo_frontmatter(title: str, tags: List[str], author: str, summary: str, date: str) -> str:
    """生成 Hexo 格式的 frontmatter。"""
    lines = ["---"]
    lines.append(f"title: {title}")
    lines.append(f"date: {date}")
    if author:
        lines.append(f"author: {author}")
    if summary:
        lines.append(f"description: {summary}")
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f"  - {t}")
    lines.append("---")
    return "\n".join(lines)


# ============================================================
# Medium 适配
# ============================================================

def _adapt_medium(content: Dict[str, Any]) -> Dict[str, Any]:
    """将内容适配为 Medium 兼容的 Markdown 格式。

    规则:
    - Medium 兼容 Markdown
    - 保留图片和链接
    - 添加标签

    Args:
        content: 原始内容字典。

    Returns:
        适配后的 Medium 格式数据。
    """
    title = content.get("title", "")
    body = content.get("body", "")
    tags = content.get("tags", [])

    # Medium Markdown 基本兼容，只需微调
    parts = []

    # 标题
    if title:
        parts.append(f"# {title}")
        parts.append("")

    # 正文
    parts.append(body)

    # 标签（Medium 最多 5 个标签）
    if tags:
        parts.append("")
        parts.append("---")
        parts.append("")
        parts.append("Tags: " + ", ".join(tags[:5]))

    markdown = "\n".join(parts)
    char_count = len(markdown)

    return {
        "platform": "medium",
        "platform_name": format_platform_name("medium"),
        "format": "markdown",
        "title": title,
        "markdown": markdown,
        "tags": tags[:5],
        "char_count": char_count,
    }


# ============================================================
# 适配入口
# ============================================================

# 平台适配器注册表
_ADAPTERS = {
    "twitter": _adapt_twitter,
    "linkedin": _adapt_linkedin,
    "wechat": _adapt_wechat,
    "blog": _adapt_blog,
    "medium": _adapt_medium,
}


def adapt_content(data: Dict[str, Any]) -> None:
    """将内容适配到指定平台。

    必填字段: id, platform

    Args:
        data: 包含内容 ID 和目标平台的字典。
    """
    content_id = data.get("id")
    platform = data.get("platform", "")

    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    if not platform:
        output_error("目标平台（platform）为必填字段", code="VALIDATION_ERROR")
        return

    try:
        platform = validate_platform(platform)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    # 微信公众号需要付费版
    if platform == "wechat":
        if not require_paid_feature("wechat", "微信公众号适配"):
            return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    adapter = _ADAPTERS.get(platform)
    if not adapter:
        output_error(f"暂不支持平台: {platform}", code="UNSUPPORTED_PLATFORM")
        return

    # 预处理: 转换 Obsidian wikilinks
    processed_content = dict(content)
    if processed_content.get("body"):
        processed_content["body"] = _convert_obsidian_wikilinks(
            processed_content["body"],
            "hyperlink" if platform in ("blog", "medium") else "plain",
        )

    result = adapter(processed_content)

    # 添加配图提示词占位符（如果内容中有 image_prompts）
    image_prompts = content.get("image_prompts", [])
    if image_prompts:
        result["image_prompts"] = image_prompts

    # 为博客平台生成 SEO 元数据
    if platform == "blog":
        result["seo_metadata"] = _generate_seo_metadata(content)

    # 保存适配结果
    adapted = _get_adapted()
    result["content_id"] = content_id
    result["adapted_at"] = now_iso()
    # 替换已有的同内容同平台适配
    adapted = [
        a for a in adapted
        if not (a.get("content_id") == content_id and a.get("platform") == platform)
    ]
    adapted.append(result)
    _save_adapted(adapted)

    output_success({
        "message": f"已将内容适配为 {format_platform_name(platform)} 格式",
        "adapted": result,
    })


def preview_content(data: Dict[str, Any]) -> None:
    """预览内容在指定平台的适配效果。

    必填字段: id, platform

    Args:
        data: 包含内容 ID 和目标平台的字典。
    """
    content_id = data.get("id")
    platform = data.get("platform", "")

    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    if not platform:
        output_error("目标平台（platform）为必填字段", code="VALIDATION_ERROR")
        return

    try:
        platform = validate_platform(platform)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    adapter = _ADAPTERS.get(platform)
    if not adapter:
        output_error(f"暂不支持平台: {platform}", code="UNSUPPORTED_PLATFORM")
        return

    result = adapter(content)

    output_success({
        "message": f"{format_platform_name(platform)} 预览",
        "preview": result,
    })


def validate_content(data: Dict[str, Any]) -> None:
    """校验内容是否满足指定平台的要求。

    必填字段: id, platform

    Args:
        data: 包含内容 ID 和目标平台的字典。
    """
    content_id = data.get("id")
    platform = data.get("platform", "")

    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    if not platform:
        output_error("目标平台（platform）为必填字段", code="VALIDATION_ERROR")
        return

    try:
        platform = validate_platform(platform)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    issues = []
    warnings = []
    body = content.get("body", "")
    title = content.get("title", "")
    char_count = count_chars(body, platform)
    limit = PLATFORM_CHAR_LIMITS.get(platform, 0)

    # 通用校验
    if not title:
        issues.append("缺少标题")
    if not body:
        issues.append("缺少正文内容")

    # 平台特定校验
    if platform == "twitter":
        if char_count > 280 * 25:  # 超过 25 条推文的 thread
            warnings.append(f"内容过长（{char_count} 字符），将拆分为较长的 thread")
        if not content.get("tags"):
            warnings.append("建议添加标签以生成 hashtag")

    elif platform == "linkedin":
        if limit > 0 and char_count > limit:
            issues.append(f"内容超过 LinkedIn 限制（{char_count}/{limit} 字符）")
        if not content.get("summary"):
            warnings.append("建议添加摘要以提升专业度")

    elif platform == "wechat":
        if not content.get("author"):
            warnings.append("建议设置作者信息")
        if not content.get("summary"):
            warnings.append("建议添加摘要作为文章描述")
        if limit > 0 and char_count > limit:
            issues.append(f"内容超过微信公众号限制（{char_count}/{limit} 字符）")

    elif platform == "blog":
        blog_type = os.environ.get("CE_BLOG_TYPE", "hugo")
        if blog_type not in ("hugo", "jekyll", "hexo"):
            warnings.append(f"未识别的博客类型: {blog_type}，将使用 Hugo 格式")

    elif platform == "medium":
        if not content.get("tags"):
            warnings.append("建议添加标签（Medium 最多 5 个）")
        if len(content.get("tags", [])) > 5:
            warnings.append("Medium 最多支持 5 个标签，多余标签将被忽略")

    is_valid = len(issues) == 0

    output_success({
        "content_id": content_id,
        "platform": platform,
        "platform_name": format_platform_name(platform),
        "is_valid": is_valid,
        "issues": issues,
        "warnings": warnings,
        "char_count": char_count,
        "char_limit": limit if limit > 0 else "无限制",
    })


def batch_adapt_content(data: Dict[str, Any]) -> None:
    """批量适配内容到多个平台。

    必填字段: id
    可选字段: platforms（默认使用内容已设置的平台列表）

    Args:
        data: 包含内容 ID 和可选平台列表的字典。
    """
    if not require_paid_feature("batch_adapt", "批量适配"):
        return

    content_id = data.get("id")
    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    # 确定目标平台
    target_platforms = data.get("platforms", content.get("platforms", []))
    if isinstance(target_platforms, str):
        target_platforms = [p.strip() for p in target_platforms.split(",") if p.strip()]

    if not target_platforms:
        output_error("未指定目标平台，请在内容中设置 platforms 或通过参数指定", code="VALIDATION_ERROR")
        return

    results = []
    errors = []
    adapted = _get_adapted()

    for platform in target_platforms:
        try:
            platform = validate_platform(platform)
        except ValueError as e:
            errors.append({"platform": platform, "error": str(e)})
            continue

        adapter = _ADAPTERS.get(platform)
        if not adapter:
            errors.append({"platform": platform, "error": f"暂不支持平台: {platform}"})
            continue

        try:
            result = adapter(content)
            result["content_id"] = content_id
            result["adapted_at"] = now_iso()

            # 更新已适配列表
            adapted = [
                a for a in adapted
                if not (a.get("content_id") == content_id and a.get("platform") == platform)
            ]
            adapted.append(result)

            results.append({
                "platform": platform,
                "platform_name": format_platform_name(platform),
                "status": "success",
            })
        except Exception as e:
            errors.append({"platform": platform, "error": str(e)})

    _save_adapted(adapted)

    output_success({
        "message": f"批量适配完成: {len(results)} 成功, {len(errors)} 失败",
        "content_id": content_id,
        "results": results,
        "errors": errors,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("content-engine 平台适配器")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "adapt": lambda: adapt_content(data or {}),
        "preview": lambda: preview_content(data or {}),
        "validate": lambda: validate_content(data or {}),
        "batch-adapt": lambda: batch_adapt_content(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
