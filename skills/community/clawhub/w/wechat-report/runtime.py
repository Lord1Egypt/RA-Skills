from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from skill_runtime.wechat_access import browser_fetch_html, classify_page, fetch_page
from skill_runtime.writing_core import (
    ENDING_TYPES,
    OPENING_TYPES,
    STRUCTURE_TYPES,
    TITLE_DRIVERS,
    TITLE_PATTERNS,
    classify_ending_type,
    classify_opening_type,
    classify_structure_type,
    detect_title_drivers,
    extract_share_hooks,
    infer_evidence_style,
    infer_reader_value_type,
    title_pattern_for,
)


DEFAULT_MAX_ARTICLES = 5
BING_RSS_ENDPOINT = "https://www.bing.com/search"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip().lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or datetime.now().strftime("%Y%m%d-%H%M%S")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def truncate_text(value: Any, limit: int) -> str:
    cleaned = clean_text(value)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(limit - 1, 0)].rstrip() + "…"


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = read_text(path)
    if not text.startswith("---"):
        return {}, text.strip()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, flags=re.DOTALL)
    if not match:
        return {}, text.strip()

    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Frontmatter must be a mapping: {path}")
    return frontmatter, match.group(2).strip()


def normalize_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = clean_text(value).lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def normalize_int(value: Any, default: int, *, minimum: int = 1, maximum: int = 20) -> int:
    if value in {None, ""}:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(parsed, maximum))


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [clean_text(item) for item in value if clean_text(item)]
    parts = re.split(r"[\n,]+", str(value))
    return [part.strip() for part in parts if part.strip()]


def fetch_text(url: str, *, timeout: int = 20) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="ignore")


def maybe_json(stdout: str) -> Any:
    stripped = stdout.strip()
    if not stripped:
        return {}
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        for start_char, end_char in (("{", "}"), ("[", "]")):
            start = stripped.find(start_char)
            end = stripped.rfind(end_char)
            if start != -1 and end != -1 and end > start:
                return json.loads(stripped[start : end + 1])
    raise ValueError("Expected JSON output from helper script.")


def canonicalize_url(url: str) -> str:
    normalized = html.unescape(clean_text(url))
    if not normalized:
        return ""
    parsed = urllib.parse.urlparse(normalized)
    scheme = parsed.scheme or "https"
    query = parsed.query
    fragment = parsed.fragment
    if parsed.netloc.endswith("mp.weixin.qq.com") and parsed.path.startswith("/s") and not fragment:
        fragment = "rd"
    return urllib.parse.urlunparse((scheme, parsed.netloc, parsed.path, "", query, fragment))


def mp_identity(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    biz = clean_text((query.get("__biz") or query.get("biz") or [""])[0])
    mid = clean_text((query.get("mid") or [""])[0])
    idx = clean_text((query.get("idx") or [""])[0])
    sn = clean_text((query.get("sn") or [""])[0])
    if any([biz, mid, idx, sn]):
        return "|".join([biz, mid, idx, sn])
    return canonicalize_url(url)


def is_mp_article_url(url: str) -> bool:
    normalized = canonicalize_url(url)
    parsed = urllib.parse.urlparse(normalized)
    return parsed.netloc.endswith("mp.weixin.qq.com") and parsed.path.startswith("/s")


def extract_mp_urls_from_text(text: str) -> list[str]:
    candidates: list[str] = []
    decoded = html.unescape(text or "").replace("\\/", "/")
    decoded = decoded.replace("\\u0026", "&").replace("\\x26", "&").replace("%5Cu0026", "&")
    patterns = [
        r"https?://mp\.weixin\.qq\.com/s\?[^\s\"'<>()]+",
        r"https?%3A%2F%2Fmp\.weixin\.qq\.com%2Fs%3F[^\s\"'<>()]+",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, decoded, flags=re.IGNORECASE):
            candidate = urllib.parse.unquote(match)
            candidate = canonicalize_url(candidate)
            if is_mp_article_url(candidate):
                candidates.append(candidate)
    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        identity = mp_identity(candidate)
        if identity in seen:
            continue
        seen.add(identity)
        deduped.append(candidate)
    return deduped


def search_bing_rss(query: str, *, limit: int = 10) -> list[dict[str, str]]:
    params = urllib.parse.urlencode({"format": "rss", "q": query, "count": str(limit)})
    xml_text = fetch_text(f"{BING_RSS_ENDPOINT}?{params}", timeout=20)
    root = ET.fromstring(xml_text)
    items: list[dict[str, str]] = []
    for item in root.findall("./channel/item"):
        items.append(
            {
                "title": clean_text(item.findtext("title")),
                "link": canonicalize_url(item.findtext("link") or ""),
                "description": clean_text(item.findtext("description")),
            }
        )
    return items


def discover_topic_urls(topic: str, *, max_articles: int) -> tuple[list[str], dict[str, Any]]:
    queries = [
        f"\"{topic}\" 微信公众号",
        f"{topic} site:mp.weixin.qq.com",
        f"{topic} Agent 公众号",
    ]
    collected: list[str] = []
    discovery_log: list[dict[str, Any]] = []
    seen_identities: set[str] = set()
    scanned_results = 0

    for query in queries:
        search_items = search_bing_rss(query, limit=max(max_articles * 3, 8))
        query_log = {"query": query, "results": []}
        for item in search_items:
            if len(collected) >= max_articles * 2:
                break
            scanned_results += 1
            link = canonicalize_url(item["link"])
            resolved_urls: list[str] = []
            error_text = ""
            if is_mp_article_url(link):
                resolved_urls = [link]
            else:
                try:
                    page_text = fetch_text(link, timeout=20)
                    resolved_urls = extract_mp_urls_from_text(page_text)
                except Exception as error:  # noqa: BLE001
                    error_text = clean_text(error)
            query_log["results"].append(
                {
                    "title": item["title"],
                    "link": link,
                    "description": item["description"],
                    "resolved_mp_urls": resolved_urls,
                    "error": error_text,
                }
            )
            for url in resolved_urls:
                identity = mp_identity(url)
                if identity in seen_identities:
                    continue
                seen_identities.add(identity)
                collected.append(url)
                if len(collected) >= max_articles * 2:
                    break
        discovery_log.append(query_log)
        if len(collected) >= max_articles * 2:
            break

    return collected[: max_articles * 2], {"queries": queries, "results": discovery_log, "scanned_results": scanned_results}


def resolve_request(path: Path) -> dict[str, Any]:
    frontmatter, notes = parse_frontmatter(path)

    topic = clean_text(frontmatter.get("topic"))
    if not topic:
        raise ValueError("`topic` is required for wechat-report.")

    max_articles = normalize_int(frontmatter.get("max_articles"), default=DEFAULT_MAX_ARTICLES, maximum=10)
    seed_urls = [canonicalize_url(item) for item in normalize_list(frontmatter.get("seed_urls")) if canonicalize_url(item)]
    collect_engagement = normalize_bool(frontmatter.get("collect_engagement"), default=True)
    discovery_mode = clean_text(frontmatter.get("discovery_mode") or "topic_compare")
    slug = slugify(topic)
    today = datetime.now()

    return {
        "topic": topic,
        "slug": slug,
        "max_articles": max_articles,
        "seed_urls": seed_urls,
        "collect_engagement": collect_engagement,
        "discovery_mode": discovery_mode,
        "notes": notes,
        "date": today.strftime("%Y%m%d"),
        "raw_date": today.strftime("%Y-%m-%d"),
    }


def require_node() -> str:
    node_path = shutil.which("node")
    if not node_path:
        raise RuntimeError("未找到 `node`。请先安装 Node.js，再运行 `wechat-report`。")
    return node_path


def run_node_script(script_path: Path, *args: str, cwd: Path) -> Any:
    command = [require_node(), str(script_path), *args]
    completed = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(clean_text(completed.stderr) or clean_text(completed.stdout) or f"Helper script failed: {script_path.name}")
    return maybe_json(completed.stdout)


def run_extract_script(script_path: Path, *, vendor_root: Path, source_url: str, html_file_path: str | None = None) -> Any:
    args = [str(vendor_root), source_url]
    if html_file_path:
        args.append(html_file_path)
    return run_node_script(script_path, *args, cwd=vendor_root)


def classify_extraction_failure(message: str) -> str:
    cleaned = clean_text(message)
    if any(marker in cleaned for marker in ["链接已过期", "已被发布者删除", "因违规无法查看", "涉嫌侵权"]):
        return "expired_or_deleted"
    return "unknown_extract_failure"


def build_failure_entry(
    *,
    stage: str,
    url: str,
    failure_type: str,
    error: str,
    canonical_url: str = "",
    final_url: str = "",
    note: str = "",
    page_excerpt: str = "",
    should_browser_retry: bool = False,
    title: str = "",
) -> dict[str, Any]:
    return {
        "stage": stage,
        "url": canonicalize_url(url),
        "canonical_url": canonicalize_url(canonical_url or url),
        "final_url": canonicalize_url(final_url),
        "failure_type": clean_text(failure_type) or "unknown_extract_failure",
        "error": clean_text(error) or "未知错误",
        "note": clean_text(note),
        "page_excerpt": truncate_text(page_excerpt, 220),
        "should_browser_retry": bool(should_browser_retry),
        "title": clean_text(title),
    }


def merge_engagement(public_data: dict[str, Any], browser_data: dict[str, Any] | None) -> dict[str, Any]:
    merged = {
        "read_count": public_data.get("read_count"),
        "like_count": public_data.get("like_count"),
        "old_like_count": public_data.get("old_like_count"),
        "comment_count": public_data.get("comment_count"),
        "reward_total_count": public_data.get("reward_total_count"),
        "comment_id": public_data.get("comment_id"),
        "appmsg_id": public_data.get("appmsg_id"),
        "comment_enabled": public_data.get("comment_enabled"),
        "friend_comment_enabled": public_data.get("friend_comment_enabled"),
        "status": public_data.get("status") or "unavailable",
        "note": clean_text(public_data.get("note")),
    }

    if browser_data:
        for key in [
            "read_count",
            "like_count",
            "old_like_count",
            "comment_count",
            "reward_total_count",
            "comment_id",
            "appmsg_id",
            "comment_enabled",
            "friend_comment_enabled",
        ]:
            if merged.get(key) is None and browser_data.get(key) is not None:
                merged[key] = browser_data.get(key)
        if browser_data.get("status"):
            if browser_data.get("metrics_visible"):
                merged["status"] = browser_data["status"]
            elif merged["status"] != "visible_in_public_html":
                merged["status"] = browser_data["status"]
        notes = [merged["note"], clean_text(browser_data.get("note"))]
        merged["note"] = " ".join(item for item in notes if item).strip()

    merged["metrics_visible"] = any(
        merged.get(key) is not None
        for key in ["read_count", "like_count", "old_like_count", "comment_count", "reward_total_count"]
    )
    return merged


def normalize_article_entry(
    *,
    original_source_url: str,
    source_url: str,
    extraction: dict[str, Any],
    browser_engagement: dict[str, Any] | None,
    discovery_source: dict[str, Any],
) -> dict[str, Any]:
    data = extraction["data"]
    content_insights = data.get("content_insights") or {}
    public_engagement = data.get("engagement") or {}
    merged_engagement = merge_engagement(public_engagement, browser_engagement)
    normalized_url = canonicalize_url(data.get("msg_link") or source_url)
    title = clean_text(data.get("msg_title"))
    summary = clean_text(data.get("msg_desc"))
    preview_text = " ".join(content_insights.get("paragraphs_preview") or [])
    heading_preview = content_insights.get("headings_preview") or []
    rhetoric_tags = {
        "title_pattern": title_pattern_for(title) if title else "unknown",
        "title_pattern_label": TITLE_PATTERNS.get(title_pattern_for(title), "unknown") if title else "unknown",
        "title_drivers": detect_title_drivers(title) if title else [],
        "title_driver_labels": [TITLE_DRIVERS[item] for item in detect_title_drivers(title)] if title else [],
        "opening_type": classify_opening_type(title, preview_text) if preview_text or title else "unknown",
        "opening_type_label": OPENING_TYPES.get(classify_opening_type(title, preview_text), "unknown") if preview_text or title else "unknown",
        "structure_type": classify_structure_type(title, heading_preview, int(content_insights.get("plain_text_length") or 0)),
        "structure_type_label": STRUCTURE_TYPES.get(
            classify_structure_type(title, heading_preview, int(content_insights.get("plain_text_length") or 0)),
            "unknown",
        ),
        "ending_type": classify_ending_type(title, summary),
        "ending_type_label": ENDING_TYPES.get(classify_ending_type(title, summary), "unknown"),
        "share_hooks": extract_share_hooks(title, summary),
        "reader_value_type": infer_reader_value_type(title, summary),
        "evidence_style": infer_evidence_style(summary, int(content_insights.get("plain_text_length") or 0)),
    }

    return {
        "original_source_url": canonicalize_url(original_source_url),
        "source_url": normalized_url,
        "identity": mp_identity(normalized_url),
        "account_name": clean_text(data.get("account_name")),
        "author": clean_text(data.get("msg_author") or data.get("account_name")),
        "title": clean_text(data.get("msg_title")),
        "summary": clean_text(data.get("msg_desc")),
        "published_at": clean_text(data.get("msg_publish_time_str")),
        "is_original": bool(data.get("msg_has_copyright")),
        "message_type": clean_text(data.get("msg_type")),
        "cover_image": canonicalize_url(data.get("msg_cover") or ""),
        "source_link": canonicalize_url(data.get("msg_source_url") or ""),
        "content_html_length": len(str(data.get("msg_content") or "")),
        "plain_text_length": int(content_insights.get("plain_text_length") or 0),
        "paragraph_count": int(content_insights.get("paragraph_count") or 0),
        "heading_count": int(content_insights.get("heading_count") or 0),
        "list_item_count": int(content_insights.get("list_item_count") or 0),
        "image_count": int(content_insights.get("image_count") or 0),
        "external_link_count": int(content_insights.get("external_link_count") or 0),
        "mp_link_count": int(content_insights.get("mp_link_count") or 0),
        "paragraphs_preview": content_insights.get("paragraphs_preview") or [],
        "headings_preview": content_insights.get("headings_preview") or [],
        "image_urls": content_insights.get("image_urls") or [],
        "external_links": content_insights.get("external_links") or [],
        "mp_links": content_insights.get("mp_links") or [],
        "engagement": merged_engagement,
        "engagement_public": public_engagement,
        "engagement_browser": browser_engagement or {},
        "discovery_source": discovery_source,
        "rhetoric_tags": rhetoric_tags,
    }


def markdown_escape(value: Any) -> str:
    return clean_text(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    if not rows:
        return ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(cell) for cell in row) + " |")
    return lines


def build_report(
    *,
    request: dict[str, Any],
    raw_path: Path,
    articles: list[dict[str, Any]],
    failures: list[dict[str, Any]],
) -> str:
    article_rows = [
        [
            article["account_name"] or "未识别",
            article["author"] or "未识别",
            article["title"] or "未命名文章",
            article["published_at"] or "未识别",
            "是" if article["is_original"] else "否",
            f"[原文]({article['source_url']})",
        ]
        for article in articles
    ]
    engagement_rows = [
        [
            article["account_name"] or "未识别",
            article["title"] or "未命名文章",
            article["engagement"].get("read_count") if article["engagement"].get("read_count") is not None else "未暴露",
            article["engagement"].get("like_count") if article["engagement"].get("like_count") is not None else "未暴露",
            article["engagement"].get("comment_count") if article["engagement"].get("comment_count") is not None else "未暴露",
            article["engagement"].get("reward_total_count") if article["engagement"].get("reward_total_count") is not None else "未暴露",
            article["engagement"].get("comment_id") or "未识别",
            article["engagement"].get("status") or "unavailable",
        ]
        for article in articles
    ]
    structure_rows = [
        [
            article["account_name"] or "未识别",
            article["title"] or "未命名文章",
            article["plain_text_length"],
            article["paragraph_count"],
            article["image_count"],
            article["external_link_count"],
            article["mp_link_count"],
            article["heading_count"],
        ]
        for article in articles
    ]
    rhetoric_rows = [
        [
            article["account_name"] or "未识别",
            article["title"] or "未命名文章",
            article["rhetoric_tags"].get("title_pattern_label", "unknown"),
            article["rhetoric_tags"].get("opening_type_label", "unknown"),
            article["rhetoric_tags"].get("structure_type_label", "unknown"),
            article["rhetoric_tags"].get("ending_type_label", "unknown"),
            " / ".join(article["rhetoric_tags"].get("share_hooks") or ["无"]),
        ]
        for article in articles
    ]

    summary_cards: list[str] = []
    if articles:
        for index, article in enumerate(articles, start=1):
            preview = article["paragraphs_preview"][:2] or [article["summary"] or "该文章未提取到可展示的正文预览。"]
            summary_cards.extend(
                [
                    f"### {index}. {article['title'] or '未命名文章'}",
                    "",
                    f"- 公众号：{article['account_name'] or '未识别'}",
                    f"- 作者：{article['author'] or '未识别'}",
                    f"- 互动状态：{article['engagement'].get('status') or 'unavailable'}",
                    f"- 互动说明：{article['engagement'].get('note') or '无'}",
                    f"- 图片数量：{article['image_count']}",
                    f"- 原文链接：{article['source_url']}",
                    "",
                    *[f"> {truncate_text(item, 160)}" for item in preview],
                    "",
                ]
            )
    else:
        summary_cards = ["- 当前没有可生成摘要卡的成功文章。", ""]

    opening_breakdown: list[str] = []
    hook_summary: list[str] = []
    if articles:
        for index, article in enumerate(articles, start=1):
            tags = article["rhetoric_tags"]
            opening_breakdown.extend(
                [
                    f"### {index}. {article['title'] or '未命名文章'}",
                    "",
                    f"- `title_pattern`：{tags.get('title_pattern_label', 'unknown')}",
                    f"- `title_drivers`：{' / '.join(tags.get('title_driver_labels') or ['无'])}",
                    f"- `opening_type`：{tags.get('opening_type_label', 'unknown')}",
                    f"- `reader_value_type`：{tags.get('reader_value_type', 'unknown')}",
                    "",
                ]
            )
            hook_summary.extend(
                [
                    f"### {index}. {article['title'] or '未命名文章'}",
                    "",
                    f"- `ending_type`：{tags.get('ending_type_label', 'unknown')}",
                    f"- `share_hooks`：{' / '.join(tags.get('share_hooks') or ['无'])}",
                    f"- `evidence_style`：{tags.get('evidence_style', 'unknown')}",
                    "",
                ]
            )
    else:
        opening_breakdown = ["- 当前没有足够文章可做标题与开头拆解。"]
        hook_summary = ["- 当前没有足够文章可做结尾与转发钩子总结。"]

    common_summary = []
    if articles:
        opening_types = [article["rhetoric_tags"].get("opening_type_label", "unknown") for article in articles]
        structure_types = [article["rhetoric_tags"].get("structure_type_label", "unknown") for article in articles]
        common_summary = [
            f"- 开头最常见的是：{max(set(opening_types), key=opening_types.count)}",
            f"- 结构最常见的是：{max(set(structure_types), key=structure_types.count)}",
            "- 真正可复用的不是具体句子，而是“标题先给钩子、开头马上交代价值、结尾留下可转发动机”这套组合。",
        ]
    else:
        common_summary = ["- 当前没有足够成功样本做共性总结。"]

    failure_lines: list[str] = []
    if failures:
        failure_rows = [
            [
                item.get("failure_type") or "unknown_extract_failure",
                item.get("title") or item.get("canonical_url") or item.get("url") or "未识别",
                item.get("final_url") or "未跳转",
                item.get("note") or item.get("error") or "未知错误",
                "是" if item.get("should_browser_retry") else "否",
            ]
            for item in failures
        ]
        failure_lines = markdown_table(["失败分类", "原公众号入口 / 标题", "最终跳转", "说明", "建议浏览器补抓"], failure_rows)
    else:
        failure_lines = ["- 本次采集未出现失败项。"]

    lines = [
        f"# 公众号对比采集报告：{request['topic']}",
        "",
        "## 基础信息",
        "",
        f"- `date`：{request['date']}",
        f"- `slug`：{request['slug']}",
        f"- `topic`：{request['topic']}",
        f"- `max_articles`：{request['max_articles']}",
        f"- `collect_engagement`：{'true' if request['collect_engagement'] else 'false'}",
        f"- `discovery_mode`：{request['discovery_mode']}",
        f"- `request_path`：{request['request_path']}",
        "",
        "## 文章总表",
        "",
        *markdown_table(["公众号", "作者", "标题", "发布时间", "原创", "原文链接"], article_rows),
        "",
        "## 互动数据对比表",
        "",
        *markdown_table(["公众号", "标题", "阅读数", "点赞数", "评论数", "打赏数", "comment_id", "采集状态"], engagement_rows),
        "",
        "## 内容结构对比表",
        "",
        *markdown_table(["公众号", "标题", "正文纯文本长度", "段落数", "图片数", "外链数", "公众号内链数", "小标题数"], structure_rows),
        "",
        "## 爆款写法标签表",
        "",
        *markdown_table(["公众号", "标题", "标题结构", "开头类型", "主结构", "结尾类型", "转发钩子"], rhetoric_rows),
        "",
        "## 单篇摘要卡",
        "",
        *summary_cards,
        "## 标题与开头拆解",
        "",
        *opening_breakdown,
        "## 结尾与转发钩子",
        "",
        *hook_summary,
        "## 共性写法总结",
        "",
        *common_summary,
        "",
        "## 失败与缺口",
        "",
        *failure_lines,
        "",
        "## 原始数据位置",
        "",
        f"- Raw JSON：{raw_path}",
        "- 飞书同步状态：`awaiting_user_confirmation`",
        "- 阅读完成后，如需发送到飞书，请确认后运行 `feishu-bitable-sync`，输入本报告或 Raw JSON 路径均可。",
    ]
    if request["notes"]:
        lines.extend(["", f"- 采集备注：{truncate_text(request['notes'], 180)}"])
    return "\n".join(lines).rstrip() + "\n"


def run_wechat_report(input_path: Path, *, workspace_root: Path, vendor_root: Path) -> dict[str, Any]:
    request = resolve_request(input_path)
    request["request_path"] = str(input_path)
    candidate_urls = list(request["seed_urls"])
    discovery: dict[str, Any] = {"queries": [], "results": [], "scanned_results": 0}
    failures: list[dict[str, Any]] = []

    if not candidate_urls:
        try:
            candidate_urls, discovery = discover_topic_urls(request["topic"], max_articles=request["max_articles"])
        except Exception as error:  # noqa: BLE001
            failures.append({"stage": "discover", "query": request["topic"], "error": clean_text(error)})
            candidate_urls = []

    deduped_urls: list[str] = []
    seen: set[str] = set()
    for url in candidate_urls:
        identity = mp_identity(url)
        if identity in seen:
            continue
        seen.add(identity)
        deduped_urls.append(url)

    extract_script = workspace_root / "skills" / "wechat-report" / "scripts" / "extract_article.js"
    engagement_script = workspace_root / "skills" / "wechat-report" / "scripts" / "collect_engagement.js"
    browser_profile_dir = workspace_root / ".cache" / "wechat-report-playwright"
    articles: list[dict[str, Any]] = []

    for url in deduped_urls:
        if len(articles) >= request["max_articles"]:
            break
        access_meta: dict[str, Any] | None = None
        browser_html_path: Path | None = None
        extraction_source_url = canonicalize_url(url)

        try:
            probe = fetch_page(url, timeout=20)
            access_meta = classify_page(source_url=url, html_text=probe["html"], final_url=probe["final_url"])
        except Exception as error:  # noqa: BLE001
            failures.append(
                build_failure_entry(
                    stage="prefetch",
                    url=url,
                    failure_type="unknown_extract_failure",
                    error=clean_text(error),
                    note="HTTP 预抓取失败，未能判断公众号页面类型。",
                )
            )
            continue

        extraction_source_url = access_meta.get("canonical_url") or extraction_source_url

        if access_meta["status"] == "param_error":
            failures.append(
                build_failure_entry(
                    stage="prefetch",
                    url=url,
                    failure_type="param_error",
                    error="公众号链接返回参数错误页",
                    canonical_url=access_meta.get("canonical_url", ""),
                    final_url=access_meta.get("final_url", ""),
                    note=access_meta.get("note", ""),
                    page_excerpt=access_meta.get("page_excerpt", ""),
                    should_browser_retry=False,
                )
            )
            continue

        if access_meta["status"] == "expired_or_deleted":
            failures.append(
                build_failure_entry(
                    stage="prefetch",
                    url=url,
                    failure_type="expired_or_deleted",
                    error="公众号链接已过期、被删除或因违规不可见",
                    canonical_url=access_meta.get("canonical_url", ""),
                    final_url=access_meta.get("final_url", ""),
                    note=access_meta.get("note", ""),
                    page_excerpt=access_meta.get("page_excerpt", ""),
                    should_browser_retry=False,
                )
            )
            continue

        if access_meta["status"] == "captcha_blocked":
            browser_html_path = workspace_root / ".cache" / "wechat-report-browser-html" / f"{request['slug']}-{len(articles)+len(failures)+1}.html"
            try:
                browser_result = browser_fetch_html(
                    workspace_root=workspace_root,
                    source_url=access_meta.get("canonical_url") or url,
                    profile_dir=browser_profile_dir,
                    output_html_path=browser_html_path,
                    headless=False,
                )
            except Exception as error:  # noqa: BLE001
                failures.append(
                    build_failure_entry(
                        stage="browser_fetch",
                        url=url,
                        failure_type="captcha_blocked",
                        error=clean_text(error),
                        canonical_url=access_meta.get("canonical_url", ""),
                        final_url=access_meta.get("final_url", ""),
                        note=access_meta.get("note", ""),
                        page_excerpt=access_meta.get("page_excerpt", ""),
                        should_browser_retry=True,
                    )
                )
                continue

            if not browser_result.get("done") or not browser_result.get("output_html_path"):
                failures.append(
                    build_failure_entry(
                        stage="browser_fetch",
                        url=url,
                        failure_type=clean_text(browser_result.get("status")) or "captcha_blocked",
                        error=clean_text(browser_result.get("note")) or "浏览器会话未拿到文章正文 HTML。",
                        canonical_url=access_meta.get("canonical_url", ""),
                        final_url=browser_result.get("final_url", access_meta.get("final_url", "")),
                        note=browser_result.get("note", access_meta.get("note", "")),
                        page_excerpt=browser_result.get("page_excerpt", access_meta.get("page_excerpt", "")),
                        should_browser_retry=True,
                    )
                )
                continue

            extraction_source_url = canonicalize_url(browser_result.get("final_url") or access_meta.get("canonical_url") or url)
            browser_html_path = Path(browser_result["output_html_path"])

        try:
            extraction = run_extract_script(
                extract_script,
                vendor_root=vendor_root,
                source_url=extraction_source_url,
                html_file_path=str(browser_html_path) if browser_html_path else None,
            )
        except Exception as error:  # noqa: BLE001
            failures.append(
                build_failure_entry(
                    stage="extract",
                    url=url,
                    failure_type=access_meta["status"] if access_meta else "unknown_extract_failure",
                    error=clean_text(error),
                    canonical_url=extraction_source_url,
                    final_url=(access_meta or {}).get("final_url", ""),
                    note=(access_meta or {}).get("note", ""),
                    page_excerpt=(access_meta or {}).get("page_excerpt", ""),
                    should_browser_retry=bool((access_meta or {}).get("should_browser_retry")),
                )
            )
            continue

        if not isinstance(extraction, dict) or not extraction.get("done") or "data" not in extraction:
            error_text = clean_text(extraction.get("msg") if isinstance(extraction, dict) else extraction) or "提取器未返回可用文章数据。"
            failures.append(
                build_failure_entry(
                    stage="extract",
                    url=url,
                    failure_type=classify_extraction_failure(error_text),
                    error=error_text,
                    canonical_url=extraction_source_url,
                    final_url=(access_meta or {}).get("final_url", ""),
                    note=(access_meta or {}).get("note", ""),
                    page_excerpt=(access_meta or {}).get("page_excerpt", ""),
                    should_browser_retry=bool((access_meta or {}).get("should_browser_retry")),
                )
            )
            continue

        browser_engagement: dict[str, Any] | None = None
        public_engagement = extraction["data"].get("engagement") or {}
        if request["collect_engagement"] and not public_engagement.get("metrics_visible_in_public_html"):
            try:
                browser_engagement = run_node_script(
                    engagement_script,
                    str(workspace_root),
                    url,
                    str(browser_profile_dir),
                    cwd=workspace_root,
                )
            except Exception as error:  # noqa: BLE001
                browser_engagement = {
                    "status": "unavailable",
                    "note": f"未能完成 Playwright 互动抓取：{clean_text(error)}",
                    "metrics_visible": False,
                }

        articles.append(
            normalize_article_entry(
                original_source_url=url,
                source_url=extraction_source_url,
                extraction=extraction,
                browser_engagement=browser_engagement,
                discovery_source={
                    "kind": "seed_url" if url in request["seed_urls"] else "topic_search",
                    "original_source_url": canonicalize_url(url),
                    "canonical_url": extraction_source_url,
                },
            )
        )

    inbox_dir = workspace_root / "content-production" / "inbox"
    raw_path = inbox_dir / "raw" / "wechat-report" / request["raw_date"] / f"{request['slug']}.json"
    report_path = inbox_dir / f"{request['date']}-{request['slug']}-wechat-report.md"

    raw_payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "request": {
            "topic": request["topic"],
            "slug": request["slug"],
            "max_articles": request["max_articles"],
            "seed_urls": request["seed_urls"],
            "collect_engagement": request["collect_engagement"],
            "discovery_mode": request["discovery_mode"],
            "notes": request["notes"],
            "request_path": str(input_path),
        },
        "vendor_skill_path": str(vendor_root),
        "discovery": {
            **discovery,
            "candidate_urls": deduped_urls,
        },
        "articles": articles,
        "failures": failures,
        "feishu_sync": {
            "status": "awaiting_user_confirmation",
            "auth_mode": "user",
            "synced_at": "",
            "manifest_path": "",
            "csv_path": "",
            "error": "",
            "user_auth_cache_path": "",
            "table": {
                "app_token_env": "FEISHU_BITABLE_APP_TOKEN",
                "table_id_env": "FEISHU_BITABLE_TABLE_ID",
            },
        },
    }

    write_text(raw_path, json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n")
    write_text(
        report_path,
        build_report(
            request=request,
            raw_path=raw_path,
            articles=articles,
            failures=failures,
        ),
    )

    return {
        "slug": request["slug"],
        "topic": request["topic"],
        "article_count": len(articles),
        "candidate_count": len(deduped_urls),
        "raw_path": raw_path,
        "report_path": report_path,
    }
