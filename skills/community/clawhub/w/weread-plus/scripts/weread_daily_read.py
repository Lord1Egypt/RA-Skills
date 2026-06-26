#!/usr/bin/env python3
"""Build a daily WeRead book briefing from popular highlights and public signals."""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from weread_common import (
    WeReadError,
    api_post,
    bestbookmark_link,
    book_author,
    book_id,
    book_title,
    compact_text,
    extract_book,
    fail,
    json_dumps,
    rating_text,
    reading_link,
    resolve_book,
    timestamp_to_date,
    write_or_print,
)
from weread_reviews import clean_review_item


HIGHLIGHT_TAG_RULES = {
    "theory": (
        "理论",
        "模型",
        "框架",
        "机制",
        "结构",
        "系统",
        "概念",
        "定义",
        "原则",
        "规律",
        "因果",
        "逻辑",
        "假设",
        "theory",
        "model",
        "framework",
        "principle",
        "mechanism",
    ),
    "viewpoint": (
        "认为",
        "应该",
        "不是",
        "而是",
        "关键",
        "本质",
        "重要",
        "必须",
        "真正",
        "其实",
        "因为",
        "所以",
        "意味着",
        "观点",
        "态度",
        "看法",
        "argue",
        "claim",
        "means",
        "because",
    ),
    "plot_or_case": (
        "故事",
        "情节",
        "人物",
        "主人公",
        "他们",
        "当时",
        "后来",
        "终于",
        "开始",
        "发生",
        "回到",
        "案例",
        "实验",
        "研究",
        "story",
        "case",
        "experiment",
    ),
    "conclusion": (
        "因此",
        "所以",
        "总之",
        "最终",
        "结论",
        "结果",
        "可见",
        "归根结底",
        "由此",
        "最后",
        "conclusion",
        "therefore",
        "finally",
        "result",
    ),
    "practice": (
        "方法",
        "步骤",
        "建议",
        "实践",
        "行动",
        "训练",
        "练习",
        "如何",
        "可以",
        "需要",
        "做",
        "practice",
        "method",
        "step",
        "habit",
    ),
}

BOOK_TYPE_RULES = {
    "fiction": ("小说", "文学", "悬疑", "推理", "科幻", "奇幻", "故事", "fiction", "novel"),
    "nonfiction": (
        "社科",
        "历史",
        "哲学",
        "心理",
        "经济",
        "管理",
        "科学",
        "传记",
        "思想",
        "商业",
        "文化",
        "nonfiction",
    ),
}

STOP_TERMS = {
    "一个",
    "一种",
    "这个",
    "这些",
    "我们",
    "他们",
    "自己",
    "没有",
    "不是",
    "因为",
    "所以",
    "但是",
    "如果",
    "只是",
    "可以",
    "需要",
    "the",
    "and",
    "with",
    "that",
    "this",
}


def parse_day(raw: str | None) -> date:
    if not raw:
        return date.today()
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise WeReadError("--date must use YYYY-MM-DD") from exc


def load_book_requests(book_names: list[str], book_ids: list[str], books_file: str | None) -> list[dict[str, str]]:
    requests: list[dict[str, str]] = []
    for name in book_names:
        name = name.strip()
        if name:
            requests.append({"book": name})
    for bid in book_ids:
        bid = bid.strip()
        if bid:
            requests.append({"bookId": bid})
    if books_file:
        try:
            lines = Path(books_file).expanduser().read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise WeReadError(f"Unable to read --books-file: {books_file}") from exc
        for line in lines:
            item = line.strip()
            if not item or item.startswith("#"):
                continue
            if item.startswith("bookId:"):
                requests.append({"bookId": item.split(":", 1)[1].strip()})
            else:
                requests.append({"book": item})
    if not requests:
        raise WeReadError("Provide --book, --book-id, or --books-file")
    return requests


def choose_daily_request(requests: list[dict[str, str]], day: date, pick: str) -> tuple[dict[str, str], int]:
    if pick == "first" or len(requests) == 1:
        return requests[0], 0
    index = day.toordinal() % len(requests)
    return requests[index], index


def resolve_request(request: dict[str, str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if request.get("bookId"):
        return resolve_book(bookid=request["bookId"])
    return resolve_book(book=request.get("book"))


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def chapter_lookup(chapters: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    mapping = {}
    for chapter in chapters:
        uid = str(chapter.get("chapterUid") or "")
        if uid:
            mapping[uid] = chapter
    return mapping


def chapter_outline(chapters: list[dict[str, Any]], *, limit: int = 18) -> list[dict[str, Any]]:
    top_level = [chapter for chapter in chapters if safe_int(chapter.get("level"), 1) <= 1]
    selected = top_level or chapters
    outline = []
    for chapter in selected[:limit]:
        outline.append(
            {
                "chapterUid": chapter.get("chapterUid"),
                "chapterIdx": chapter.get("chapterIdx"),
                "title": chapter.get("title"),
                "level": chapter.get("level"),
                "wordCount": chapter.get("wordCount"),
            }
        )
    return outline


def classify_book_type(book: dict[str, Any], chapters: list[dict[str, Any]]) -> str:
    blob = " ".join(
        str(value).lower()
        for value in [
            book.get("category"),
            book.get("title"),
            book.get("intro"),
            " ".join(str(chapter.get("title") or "") for chapter in chapters[:24]),
        ]
        if value
    )
    fiction_hits = sum(1 for cue in BOOK_TYPE_RULES["fiction"] if cue in blob)
    nonfiction_hits = sum(1 for cue in BOOK_TYPE_RULES["nonfiction"] if cue in blob)
    if fiction_hits > nonfiction_hits:
        return "fiction"
    if nonfiction_hits > fiction_hits:
        return "nonfiction"
    return "mixed"


def classify_highlight_text(text: str, *, book_type: str = "mixed") -> list[str]:
    lowered = str(text or "").lower()
    tags = [tag for tag, cues in HIGHLIGHT_TAG_RULES.items() if any(cue in lowered for cue in cues)]
    if book_type == "fiction" and "plot_or_case" not in tags:
        story_cues = ("他", "她", "我", "我们", "说", "走", "看见", "想到", "回忆")
        if any(cue in lowered for cue in story_cues):
            tags.append("plot_or_case")
    if not tags:
        tags.append("general")
    return tags


def keyword_candidates(texts: list[str], *, limit: int = 12) -> list[str]:
    counter: Counter[str] = Counter()
    for text in texts:
        normalized = str(text or "").lower()
        for token in re.findall(r"[A-Za-z][A-Za-z-]{2,}", normalized):
            if token in STOP_TERMS:
                continue
            counter[token] += 1
        for block in re.findall(r"[\u4e00-\u9fff]{2,}", normalized):
            if len(block) <= 4 and block not in STOP_TERMS:
                counter[block] += 1
            for size in (2, 3, 4):
                for index in range(0, max(0, len(block) - size + 1)):
                    token = block[index : index + size]
                    if token not in STOP_TERMS:
                        counter[token] += 1
    return [term for term, _ in counter.most_common(limit)]


def clean_highlight(
    item: dict[str, Any],
    *,
    book: dict[str, Any],
    chapters_by_uid: dict[str, dict[str, Any]],
    book_type: str,
    quote_limit: int,
    source: str,
) -> dict[str, Any]:
    chapter_uid = item.get("chapterUid")
    chapter = chapters_by_uid.get(str(chapter_uid), {})
    mark_text = compact_text(item.get("markText"), quote_limit)
    return {
        "bookmarkId": item.get("bookmarkId"),
        "chapterUid": chapter_uid,
        "chapterIdx": chapter.get("chapterIdx"),
        "chapterTitle": chapter.get("title"),
        "range": item.get("range"),
        "markText": mark_text,
        "markTextLength": len(str(item.get("markText") or "")),
        "totalCount": item.get("totalCount"),
        "userVid": item.get("userVid"),
        "tags": classify_highlight_text(mark_text, book_type=book_type),
        "source": source,
        "link": bestbookmark_link(book_id(book), chapter_uid, item.get("range"), item.get("userVid")),
    }


def highlight_key(item: dict[str, Any]) -> str:
    bookmark_id = str(item.get("bookmarkId") or "").strip()
    if bookmark_id:
        return f"bookmark:{bookmark_id}"
    text_key = re.sub(r"\s+", "", str(item.get("markText") or ""))[:80]
    return f"{item.get('chapterUid')}|{item.get('range')}|{text_key}"


def fetch_chapters(book: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    data = api_post("/book/chapterinfo", {"bookId": book_id(book)})
    return data.get("chapters") or [], data


def fetch_bestbookmarks(book: dict[str, Any], chapter_uid: Any = 0) -> dict[str, Any]:
    return api_post("/book/bestbookmarks", {"bookId": book_id(book), "chapterUid": chapter_uid})


def collect_popular_highlights(
    book: dict[str, Any],
    chapters: list[dict[str, Any]],
    *,
    book_type: str,
    scope: str,
    max_chapters: int,
    limit: int,
    quote_limit: int,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    chapters_by_uid = chapter_lookup(chapters)
    warnings: list[str] = []
    raw_items: list[tuple[dict[str, Any], str]] = []
    whole_book_data = fetch_bestbookmarks(book, 0)
    for item in whole_book_data.get("items") or []:
        raw_items.append((item, "book"))

    should_fetch_chapters = scope == "chapters" or (scope == "auto" and len(chapters) <= max_chapters)
    chapter_pages_fetched = 0
    if should_fetch_chapters:
        for chapter in chapters[:max_chapters]:
            chapter_uid = chapter.get("chapterUid")
            if chapter_uid in (None, ""):
                continue
            try:
                data = fetch_bestbookmarks(book, chapter_uid)
            except WeReadError as exc:
                warnings.append(f"章节 {chapter.get('title') or chapter_uid} 热门划线读取失败：{exc}")
                continue
            chapter_pages_fetched += 1
            for item in data.get("items") or []:
                raw_items.append((item, "chapter"))
        if len(chapters) > max_chapters:
            warnings.append(f"目录共有 {len(chapters)} 章，已按 --max-chapters={max_chapters} 截断逐章抓取")
    elif scope == "auto" and len(chapters) > max_chapters:
        warnings.append(f"目录共有 {len(chapters)} 章，auto 模式只抓取全书热门榜；可调高 --max-chapters 或使用 --highlight-scope chapters")

    deduped: dict[str, dict[str, Any]] = {}
    for raw, source in raw_items:
        key = highlight_key(raw)
        cleaned = clean_highlight(
            raw,
            book=book,
            chapters_by_uid=chapters_by_uid,
            book_type=book_type,
            quote_limit=quote_limit,
            source=source,
        )
        existing = deduped.get(key)
        if not existing or safe_int(cleaned.get("totalCount")) > safe_int(existing.get("totalCount")):
            deduped[key] = cleaned

    highlights = sorted(
        deduped.values(),
        key=lambda item: (safe_int(item.get("totalCount")), -safe_int(item.get("chapterIdx"), 999999)),
        reverse=True,
    )
    stats = {
        "bookLevelTotalCount": whole_book_data.get("totalCount"),
        "bookLevelReturned": len(whole_book_data.get("items") or []),
        "chapterPagesFetched": chapter_pages_fetched,
        "rawHighlightRows": len(raw_items),
        "dedupedHighlights": len(highlights),
        "returnedHighlights": min(limit, len(highlights)),
        "highlightScope": scope,
    }
    return highlights[:limit], stats, warnings


def fetch_public_review_signal(book: dict[str, Any], *, count: int) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    result: dict[str, Any] = {}
    for label, review_type in (("all", 0), ("recommend", 1), ("bad", 2)):
        try:
            data = api_post("/review/list", {"bookId": book_id(book), "reviewListType": review_type, "count": count})
        except WeReadError as exc:
            warnings.append(f"{label} 公开点评读取失败：{exc}")
            continue
        result[label] = {
            "summary": {
                "reviewsCnt": data.get("reviewsCnt"),
                "recentTotalCnt": data.get("recentTotalCnt"),
                "reviewsHasMore": data.get("reviewsHasMore"),
                "reviewsHas5Star": data.get("reviewsHas5Star"),
                "reviewsHas1Star": data.get("reviewsHas1Star"),
                "friendCommentCount": data.get("friendCommentCount"),
                "friendUniqueCount": data.get("friendUniqueCount"),
                "deepVRecommendInfo": data.get("deepVRecommendInfo"),
                "deepVRecommendValue": data.get("deepVRecommendValue"),
                "deepVUniqueCount": data.get("deepVUniqueCount"),
            },
            "reviews": [clean_review_item(item) for item in data.get("reviews") or []],
        }
    return result, warnings


def evidence_for(highlights: list[dict[str, Any]], tag: str, *, limit: int) -> list[dict[str, Any]]:
    selected = [item for item in highlights if tag in (item.get("tags") or [])]
    if not selected and tag == "plot_or_case":
        selected = [item for item in highlights if "general" in (item.get("tags") or [])]
    return [
        {
            "text": item.get("markText"),
            "chapterTitle": item.get("chapterTitle"),
            "totalCount": item.get("totalCount"),
            "link": item.get("link"),
        }
        for item in selected[:limit]
    ]


def section_summary(label: str, items: list[dict[str, Any]], fallback: str) -> str:
    if not items:
        return fallback
    chapters = [item.get("chapterTitle") for item in items if item.get("chapterTitle")]
    chapter_hint = ""
    if chapters:
        common = [name for name, _ in Counter(chapters).most_common(2)]
        chapter_hint = f" 证据主要出现在：{'、'.join(common)}。"
    return f"热门划线中有 {len(items)} 条可作为“{label}”的入口。{chapter_hint}".strip()


def build_content_analysis(
    *,
    book: dict[str, Any],
    chapters: list[dict[str, Any]],
    highlights: list[dict[str, Any]],
    reviews: dict[str, Any],
    book_type: str,
) -> dict[str, Any]:
    intro = compact_text(book.get("intro"), 360)
    texts = [book_title(book), book_author(book), str(book.get("category") or ""), intro]
    texts.extend(str(chapter.get("title") or "") for chapter in chapters[:40])
    texts.extend(str(item.get("markText") or "") for item in highlights[:40])

    theory = evidence_for(highlights, "theory", limit=6)
    viewpoints = evidence_for(highlights, "viewpoint", limit=8)
    plot_or_cases = evidence_for(highlights, "plot_or_case", limit=8)
    conclusions = evidence_for(highlights, "conclusion", limit=6)
    practice = evidence_for(highlights, "practice", limit=5)
    review_summary = (reviews.get("all") or {}).get("summary") or {}

    questions = [
        "这本书最想解决的问题是什么？",
        "热门划线反复强调的是事实、判断，还是行动建议？",
        "哪些观点只在特定情境下成立？",
    ]
    if book_type == "fiction":
        questions.append("人物选择和情节转折背后的核心冲突是什么？")
    else:
        questions.append("作者的理论框架能否迁移到你自己的工作或生活场景？")

    return {
        "dataBoundary": "基于微信读书书籍信息、目录、热门划线和公开点评生成；不是全文替代阅读。",
        "bookType": book_type,
        "mainThesis": intro or "书籍简介缺失；请结合目录和热门划线判断核心主题。",
        "keywords": keyword_candidates(texts),
        "structure": chapter_outline(chapters),
        "theory": {
            "summary": section_summary("理论/框架", theory, "热门划线中没有足够明确的理论/框架信号，可先看目录和简介。"),
            "evidence": theory,
        },
        "viewpoints": {
            "summary": section_summary("核心观点", viewpoints, "热门划线中没有足够明确的观点句，建议结合公开点评补充判断。"),
            "evidence": viewpoints,
        },
        "plotOrCases": {
            "summary": section_summary("故事情节/案例线索", plot_or_cases, "热门划线中故事情节或案例信号较弱。"),
            "evidence": plot_or_cases,
        },
        "conclusions": {
            "summary": section_summary("主要结论", conclusions, "热门划线中没有足够明确的结论句，需通过完整阅读收束。"),
            "evidence": conclusions,
        },
        "practice": {
            "summary": section_summary("可执行方法", practice, "热门划线中方法论信号较弱；可以把它当作理解型阅读。"),
            "evidence": practice,
        },
        "publicReviewSignal": review_summary,
        "readingQuestions": questions,
    }


def build_daily_brief(
    *,
    book_requests: list[dict[str, str]],
    day: date,
    pick: str,
    highlight_scope: str,
    max_chapters: int,
    highlight_limit: int,
    quote_limit: int,
    review_count: int,
) -> dict[str, Any]:
    selected_request, selected_index = choose_daily_request(book_requests, day, pick)
    book, candidates = resolve_request(selected_request)
    chapters, chapter_data = fetch_chapters(book)
    book_type = classify_book_type(book, chapters)
    highlights, highlight_stats, highlight_warnings = collect_popular_highlights(
        book,
        chapters,
        book_type=book_type,
        scope=highlight_scope,
        max_chapters=max_chapters,
        limit=highlight_limit,
        quote_limit=quote_limit,
    )
    reviews, review_warnings = fetch_public_review_signal(book, count=review_count)
    analysis = build_content_analysis(book=book, chapters=chapters, highlights=highlights, reviews=reviews, book_type=book_type)

    return {
        "date": day.isoformat(),
        "selection": {
            "strategy": pick,
            "selectedIndex": selected_index,
            "candidateCount": len(book_requests),
            "request": selected_request,
        },
        "book": book,
        "searchCandidates": candidates,
        "chapterInfo": {
            "synckey": chapter_data.get("synckey"),
            "chapterUpdateTime": chapter_data.get("chapterUpdateTime"),
            "chapterCount": len(chapters),
        },
        "highlightStats": highlight_stats,
        "highlights": highlights,
        "reviews": reviews,
        "analysis": analysis,
        "warnings": highlight_warnings + review_warnings,
    }


def review_consensus_text(reviews: dict[str, Any]) -> list[str]:
    lines = []
    summary = (reviews.get("all") or {}).get("summary") or {}
    if summary.get("reviewsCnt") not in (None, ""):
        lines.append(f"公开点评数：{summary['reviewsCnt']}")
    deep_v = summary.get("deepVRecommendInfo")
    if isinstance(deep_v, dict):
        text = " ".join(str(deep_v.get(key) or "") for key in ("title", "subtitle")).strip()
        if text:
            lines.append(f"资深会员：{text}")
    for label, title in (("recommend", "推荐样本"), ("bad", "保留意见样本")):
        samples = (reviews.get(label) or {}).get("reviews") or []
        if samples:
            first = samples[0]
            author = (first.get("author") or {}).get("name") or "匿名用户"
            content = compact_text(first.get("content"), 120)
            if content:
                lines.append(f"{title}：{author}，{content}")
    return lines


def markdown_section_from_evidence(title: str, section: dict[str, Any]) -> list[str]:
    lines = [f"### {title}", section.get("summary") or ""]
    for item in section.get("evidence") or []:
        meta = []
        if item.get("chapterTitle"):
            meta.append(str(item["chapterTitle"]))
        if item.get("totalCount") not in (None, ""):
            meta.append(f"{item['totalCount']} 人划线")
        prefix = f"- {' / '.join(meta)}：" if meta else "- "
        lines.append(prefix + compact_text(item.get("text"), 180))
    lines.append("")
    return lines


def markdown_daily(result: dict[str, Any]) -> str:
    book = result["book"]
    analysis = result["analysis"]
    lines = [f"# 每日读书：{book_title(book)}", ""]
    meta = [f"日期：{result['date']}"]
    if book_author(book):
        meta.append(f"作者：{book_author(book)}")
    if book.get("category"):
        meta.append(f"分类：{book.get('category')}")
    if book.get("newRating"):
        meta.append(f"评分：{rating_text(book.get('newRating'))}")
    lines.append(" / ".join(meta))
    lines.append("")
    lines.append(f"> {analysis['dataBoundary']}")
    lines.append("")

    lines.append("## 今日结论")
    lines.append(f"- 核心主题：{analysis.get('mainThesis')}")
    if analysis.get("keywords"):
        lines.append(f"- 高频线索：{'、'.join(analysis['keywords'][:10])}")
    if result.get("highlightStats"):
        stats = result["highlightStats"]
        lines.append(
            f"- 热门划线：返回 {stats.get('returnedHighlights')} 条，去重后 {stats.get('dedupedHighlights')} 条，抓取范围 {stats.get('highlightScope')}"
        )
    link = reading_link(book_id(book))
    if link:
        lines.append(f"- 打开：{link}")
    lines.append("")

    lines.append("## 内容地图")
    for item in analysis.get("structure") or []:
        title = item.get("title")
        if not title:
            continue
        level = max(1, safe_int(item.get("level"), 1))
        indent = "  " * (level - 1)
        word_count = f"（{item.get('wordCount')} 字）" if item.get("wordCount") else ""
        lines.append(f"- {indent}{title}{word_count}")
    lines.append("")

    lines.append("## 主要内容分析")
    lines.extend(markdown_section_from_evidence("理论/框架", analysis.get("theory") or {}))
    lines.extend(markdown_section_from_evidence("核心观点", analysis.get("viewpoints") or {}))
    lines.extend(markdown_section_from_evidence("故事情节/案例线索", analysis.get("plotOrCases") or {}))
    lines.extend(markdown_section_from_evidence("主要结论", analysis.get("conclusions") or {}))
    lines.extend(markdown_section_from_evidence("可执行方法", analysis.get("practice") or {}))

    lines.append("## 热门划线")
    for index, item in enumerate(result.get("highlights") or [], 1):
        meta = []
        if item.get("totalCount") not in (None, ""):
            meta.append(f"{item['totalCount']} 人划线")
        if item.get("chapterTitle"):
            meta.append(str(item["chapterTitle"]))
        if item.get("tags"):
            meta.append("、".join(item["tags"]))
        lines.append(f"### {index}. {' / '.join(meta) if meta else '热门划线'}")
        if item.get("markText"):
            lines.append(f"> {item['markText']}")
        if item.get("link"):
            lines.append(f"- 打开划线：{item['link']}")
        lines.append("")

    consensus = review_consensus_text(result.get("reviews") or {})
    if consensus:
        lines.append("## 公开点评信号")
        for item in consensus:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## 今日读法")
    for question in analysis.get("readingQuestions") or []:
        lines.append(f"- {question}")
    if result.get("warnings"):
        lines.append("")
        lines.append("## 注意")
        for warning in result["warnings"]:
            lines.append(f"- {warning}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a daily WeRead book briefing")
    parser.add_argument("--book", action="append", default=[], help="Book title. Repeat to provide a daily rotation list.")
    parser.add_argument("--book-id", action="append", default=[], help="Book ID. Repeat to provide a daily rotation list.")
    parser.add_argument("--books-file", help="UTF-8 file with one book title per line; use bookId:ID for explicit IDs.")
    parser.add_argument("--date", help="Reading date in YYYY-MM-DD. Defaults to today.")
    parser.add_argument("--pick", choices=("date", "first"), default="date", help="How to pick from multiple provided books.")
    parser.add_argument("--highlight-scope", choices=("auto", "book", "chapters"), default="auto")
    parser.add_argument("--max-chapters", type=int, default=60)
    parser.add_argument("--highlight-count", type=int, default=40)
    parser.add_argument("--quote-limit", type=int, default=220, help="Maximum characters shown for each popular highlight.")
    parser.add_argument("--review-count", type=int, default=6)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    try:
        day = parse_day(args.date)
        requests = load_book_requests(args.book, args.book_id, args.books_file)
        result = build_daily_brief(
            book_requests=requests,
            day=day,
            pick=args.pick,
            highlight_scope=args.highlight_scope,
            max_chapters=max(0, args.max_chapters),
            highlight_limit=max(1, args.highlight_count),
            quote_limit=max(60, min(500, args.quote_limit)),
            review_count=max(1, min(20, args.review_count)),
        )
    except WeReadError as exc:
        fail(str(exc))

    content = json_dumps(result) if args.format == "json" else markdown_daily(result)
    write_or_print(content, args.output)


if __name__ == "__main__":
    main()
