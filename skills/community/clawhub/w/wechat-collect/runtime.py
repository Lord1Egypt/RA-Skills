from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any

from lxml import html
from skill_runtime.wechat_access import browser_fetch_html, canonicalize_url, classify_page, fetch_page


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip().lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or datetime.now().strftime("%Y%m%d-%H%M%S")


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def truncate_text(value: str, limit: int) -> str:
    cleaned = clean_text(value)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(limit - 1, 0)].rstrip() + "…"


def is_noise_line(text: str) -> bool:
    cleaned = clean_text(text)
    if not cleaned:
        return True
    if len(cleaned) < 8:
        return True
    noise_patterns = [
        r"^撰文[｜|]",
        r"^编辑[｜|]",
        r"^图源[:：；]",
        r"^图源",
        r"^官方公众号[:：]",
        r"^官方视频号[:：]",
        r"^官方小红书[:：]",
        r"^官方网站[:：]",
        r"^官方邮箱[:：]",
        r"^咨询信息[:：]",
        r"^联络方式[:：]?",
        r"^图\d*$",
        r"^微信扫一扫",
    ]
    return any(re.search(pattern, cleaned) for pattern in noise_patterns)


def first_non_empty(values: list[str]) -> str:
    for value in values:
        cleaned = clean_text(value)
        if cleaned:
            return cleaned
    return ""


def extract_meta_text(tree: html.HtmlElement, *xpaths: str) -> str:
    for xpath in xpaths:
        values = tree.xpath(xpath)
        if not values:
            continue
        if isinstance(values[0], str):
            return first_non_empty([str(item) for item in values])
        return first_non_empty([item.text_content() for item in values])
    return ""


def extract_publish_date(raw_html: str) -> str:
    ct_match = re.search(r'\bct\s*=\s*"?(?P<ts>\d{10})"?', raw_html)
    if ct_match:
        return datetime.fromtimestamp(int(ct_match.group("ts"))).strftime("%Y%m%d")
    date_match = re.search(r"(20\d{2})[-/年](\d{1,2})[-/月](\d{1,2})", raw_html)
    if date_match:
        year, month, day = date_match.groups()
        return f"{year}{int(month):02d}{int(day):02d}"
    return datetime.now().strftime("%Y%m%d")


def extract_article(raw_html: str, source_url: str) -> dict[str, Any]:
    if "The content has been deleted by the author." in raw_html:
        raise RuntimeError("公众号原文已被作者删除，无法采集。")
    if "内容已被发布者删除" in raw_html:
        raise RuntimeError("公众号原文已被发布者删除，无法采集。")

    tree = html.fromstring(raw_html)
    title = extract_meta_text(
        tree,
        '//meta[@property="og:title"]/@content',
        '//meta[@name="twitter:title"]/@content',
        '//h1[@id="activity-name"]',
        "//title/text()",
    )
    author = extract_meta_text(
        tree,
        '//meta[@name="author"]/@content',
        '//*[@id="js_name"]/text()',
        '//*[contains(@class,"account_nickname")]/text()',
    )

    paragraphs: list[str] = []
    nodes = tree.xpath(
        '//*[@id="js_content"]//*[self::p or self::blockquote or self::h2 or self::h3 or self::li]'
        '[not(descendant::*[self::p or self::blockquote or self::h2 or self::h3 or self::li])]'
    )
    if not nodes:
        nodes = tree.xpath(
            "//article//*[self::p or self::blockquote or self::h2 or self::h3 or self::li]"
            "[not(descendant::*[self::p or self::blockquote or self::h2 or self::h3 or self::li])]"
        )
    for node in nodes:
        text = clean_text(node.text_content())
        if is_noise_line(text):
            continue
        if text in paragraphs:
            continue
        paragraphs.append(text)

    headings = [item for item in paragraphs if 8 <= len(item) <= 36][:5]
    body_paragraphs = [item for item in paragraphs if item not in headings and len(item) >= 28]
    summary_paragraphs = body_paragraphs[:4] or paragraphs[:4]
    publish_date = extract_publish_date(raw_html)
    topic = title or f"公众号文章采集-{publish_date}"
    slug = slugify(topic)
    if not title and not summary_paragraphs:
        raise RuntimeError("未识别到公众号正文，可能是反爬页或非文章详情页。")
    return {
        "title": topic,
        "slug": slug,
        "author": author,
        "publish_date": publish_date,
        "headings": headings[:3],
        "paragraphs": summary_paragraphs,
        "source_url": source_url,
    }


def infer_arguments(article: dict[str, Any]) -> list[str]:
    headings = [clean_text(item) for item in article.get("headings", []) if clean_text(item)]
    if headings:
        return headings[:3]
    paragraphs = [clean_text(item) for item in article.get("paragraphs", []) if clean_text(item)]
    fallback = [truncate_text(item, 34) for item in paragraphs[:3]]
    if fallback:
        return fallback
    return [
        "这篇公众号文章在讨论什么问题",
        "作者给出的核心判断是什么",
        "哪些案例或论据值得再创作复用",
    ]


def build_brief_markdown(article: dict[str, Any]) -> str:
    paragraphs = [clean_text(item) for item in article.get("paragraphs", []) if clean_text(item)]
    core_view = "\n".join(paragraphs[:2]) if paragraphs else "这是一篇从公众号文章采集后生成的再创作 brief。"
    background = [truncate_text(item, 80) for item in paragraphs[1:4]] or [truncate_text(core_view, 80)]
    arguments = infer_arguments(article)
    materials = [
        f"来源链接：{article['source_url']}",
        f"来源公众号/作者：{article.get('author') or '未识别'}",
    ]
    materials.extend(truncate_text(item, 90) for item in paragraphs[:3])

    lines = [
        f"# 阶段 2 采集 Brief：{article['title']}",
        "",
        "## 基础信息",
        "",
        f"- `date`：{article['publish_date']}",
        f"- `slug`：{article['slug']}",
        f"- `topic`：{article['title']}",
        "- `target_reader`：关注原文主题、希望将公众号素材加工为可发布观点文章的读者",
        f"- `publish_goal`：基于公众号素材再创作一篇适合公众号发布的观点型长文，保留原文有价值的信息点，但不直接照抄原文",
        "",
        "## 核心观点",
        "",
        core_view,
        "",
        "## 背景与语境",
        "",
        *[f"- {item}" for item in background[:4]],
        "",
        "## 论证方向",
        "",
        *[f"{index}. {item}" for index, item in enumerate(arguments[:3], start=1)],
        "",
        "## 可用案例 / 素材",
        "",
        *[f"- {item}" for item in materials[:5]],
        "",
        "## 明确不要写什么",
        "",
        "- 不要直接复刻原公众号原文结构或句子。",
        "- 不要保留明显的公众号套话、标题党和营销腔。",
        "- 不要把未核实的事实当作确定结论输出。",
        "",
        "## 风格要求",
        "",
        "- 提炼观点，重组结构，保留信息密度。",
        "- 语言清晰，适合后续进入公众号再创作链。",
        "- 重点突出原文中最值得复用的判断、案例和线索。",
        "",
        "## 配图方向",
        "",
        f"- 围绕主题“{article['title']}”生成概念图或信息图。",
        "- 优先做公众号头图或关键信息提炼图。",
        "",
    ]
    return "\n".join(lines)


def load_article_html(url: str, *, workspace_root: Path) -> tuple[str, str]:
    probe = fetch_page(url, timeout=30)
    access_meta = classify_page(source_url=url, html_text=probe["html"], final_url=probe["final_url"])

    if access_meta["status"] == "article_page":
        return probe["html"], access_meta.get("canonical_url") or canonicalize_url(url)

    if access_meta["status"] == "param_error":
        raise RuntimeError("公众号链接返回参数错误页，当前不是可直接抓取的标准文章入口。")

    if access_meta["status"] == "expired_or_deleted":
        raise RuntimeError("公众号链接已过期、被删除或因违规不可见，无法继续采集。")

    if access_meta["status"] == "captcha_blocked":
        profile_dir = workspace_root / ".cache" / "wechat-report-playwright"
        output_html_path = workspace_root / ".cache" / "wechat-collect-browser-html" / f"{slugify(url)}.html"
        browser_result = browser_fetch_html(
            workspace_root=workspace_root,
            source_url=access_meta.get("canonical_url") or url,
            profile_dir=profile_dir,
            output_html_path=output_html_path,
            headless=False,
        )
        if browser_result.get("done") and browser_result.get("output_html_path"):
            html_text = Path(browser_result["output_html_path"]).read_text(encoding="utf-8")
            return html_text, canonicalize_url(browser_result.get("final_url") or access_meta.get("canonical_url") or url)
        raise RuntimeError("公众号原文被微信环境校验拦截；请先在弹出的浏览器中完成验证后重试。")

    raise RuntimeError("未识别到可抓取的公众号正文页面，当前链接可能不是标准文章详情页。")


def collect_article_to_brief(url: str, *, inbox_dir: Path, archive_dir: Path) -> dict[str, Any]:
    workspace_root = inbox_dir.parent.parent
    raw_html, resolved_url = load_article_html(url, workspace_root=workspace_root)
    article = extract_article(raw_html, resolved_url)

    inbox_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)

    brief_path = inbox_dir / f"{article['publish_date']}-{article['slug']}-gzh-brief.md"
    archive_path = archive_dir / f"{article['publish_date']}-{article['slug']}.html"

    brief_path.write_text(build_brief_markdown(article) + "\n", encoding="utf-8")
    archive_path.write_text(raw_html, encoding="utf-8")

    return {
        "brief_path": brief_path,
        "archive_path": archive_path,
        "slug": article["slug"],
        "title": article["title"],
        "author": article.get("author", ""),
        "source_url": resolved_url,
        "publish_date": article["publish_date"],
    }
