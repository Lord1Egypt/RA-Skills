#!/usr/bin/env python3
"""Build hot-note article list from TikHub search_notes JSON response.

Features:
1) Merge multi-page responses (from local files or direct API pagination)
2) Rank by custom hot score (likes/collects/comments/shares)
3) Generate publish-ready markdown templates
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SEARCH_NOTES_WEB_URL = "https://api.tikhub.io/api/v1/xiaohongshu/web/search_notes"


def extract_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = (
        payload.get("data", {})
        .get("data", {})
        .get("items", [])
    )
    if not isinstance(items, list):
        return []
    return [x for x in items if isinstance(x, dict)]


def fetch_pages_from_api(
    *,
    token: str,
    keyword: str,
    pages: int,
    sort: str,
    note_type: str,
    timeout: int,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for page in range(1, max(1, pages) + 1):
        params = {
            "keyword": keyword,
            "page": str(page),
            "sort": sort,
            "noteType": note_type,
        }
        url = f"{SEARCH_NOTES_WEB_URL}?{urlencode(params)}"
        req = Request(url, headers={"Authorization": f"Bearer {token}"}, method="GET")
        with urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
        out.extend(extract_items(payload))
    return out


def build_rows(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in items:
        note = item.get("note", {})
        if not isinstance(note, dict):
            continue
        user = note.get("user", {})
        if not isinstance(user, dict):
            user = {}
        note_id = str(note.get("id") or "").strip()
        xsec_token = str(note.get("xsec_token") or "").strip()
        url = ""
        if note_id:
            url = f"https://www.xiaohongshu.com/explore/{note_id}"
            if xsec_token:
                url += f"?xsec_token={xsec_token}&xsec_source=pc_search"
        rows.append(
            {
                "id": note_id,
                "title": str(note.get("title") or "").strip(),
                "author": str(user.get("nickname") or "").strip(),
                "liked_count": int(note.get("liked_count") or 0),
                "collected_count": int(note.get("collected_count") or 0),
                "comments_count": int(note.get("comments_count") or 0),
                "shared_count": int(note.get("shared_count") or 0),
                "desc": str(note.get("desc") or "").strip(),
                "url": url,
            }
        )
    return rows


def hot_score(row: Dict[str, Any], w_like: float, w_collect: float, w_comment: float, w_share: float) -> float:
    return (
        row["liked_count"] * w_like
        + row["collected_count"] * w_collect
        + row["comments_count"] * w_comment
        + row["shared_count"] * w_share
    )


def write_markdown(rows: List[Dict[str, Any]], out: Path, keyword: str, min_likes: int) -> None:
    lines = [
        f"# 小红书文章列表（点赞 > {min_likes}）",
        "",
        f"- 关键词: {keyword}",
        f"- 命中数量: {len(rows)}",
        "",
    ]
    if not rows:
        lines.append("暂无符合条件的文章。")
    else:
        for idx, r in enumerate(rows, start=1):
            lines.extend(
                [
                    f"{idx}. {r['title'] or 'Untitled'}",
                    f"- 作者: {r['author'] or 'N/A'}",
                    f"- 点赞: {r['liked_count']}",
                    f"- 收藏: {r['collected_count']}",
                    f"- 评论: {r['comments_count']}",
                    f"- 分享: {r['shared_count']}",
                    f"- 链接: {r['url'] or 'N/A'}",
                    "",
                ]
            )
    out.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_publish_templates(rows: List[Dict[str, Any]], out: Path, keyword: str) -> None:
    lines = [
        f"# 可发布文章模板（关键词：{keyword}）",
        "",
    ]
    if not rows:
        lines.append("暂无可生成模板的数据。")
        out.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        return
    for idx, r in enumerate(rows, start=1):
        title = r["title"] or "未命名笔记"
        desc = (r.get("desc") or "").replace("\n", " ").strip()
        if len(desc) > 120:
            desc = desc[:120].rstrip() + "..."
        if not desc:
            desc = "这篇内容聚焦实用经验与真实体验，适合做同主题选题参考。"
        lines.extend(
            [
                f"## 模板 {idx}",
                f"建议标题：{title}",
                f"导语：围绕“{keyword}”筛选到一篇高互动笔记，适合做选题延展。",
                f"内容摘要：{desc}",
                f"原笔记作者：{r.get('author') or '未知'}",
                f"数据参考：点赞 {r['liked_count']} / 收藏 {r['collected_count']} / 评论 {r['comments_count']} / 分享 {r['shared_count']}",
                f"原链接：{r.get('url') or 'N/A'}",
                "",
            ]
        )
    out.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_csv(rows: List[Dict[str, Any]], out: Path) -> None:
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "title",
                "author",
                "liked_count",
                "collected_count",
                "comments_count",
                "shared_count",
                "hot_score",
                "url",
                "desc",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build filtered article list from TikHub JSON response.")
    parser.add_argument("--input", action="append", default=[], help="Path to TikHub response JSON file. Repeatable.")
    parser.add_argument("--input-dir", default="", help="Directory containing page JSON files.")
    parser.add_argument("--input-glob", default="*.json", help="Glob pattern when --input-dir is set.")
    parser.add_argument("--token", default="", help="TikHub token for direct API pagination mode.")
    parser.add_argument("--keyword", default="", help="Keyword for direct API pagination mode.")
    parser.add_argument("--pages", type=int, default=0, help="Fetch N pages directly from API when token+keyword provided.")
    parser.add_argument("--sort", default="general", help="Sort for API mode, default general.")
    parser.add_argument("--note-type", default="_0", help="noteType for API mode, default _0.")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout seconds for API mode.")
    parser.add_argument("--min-likes", type=int, default=1000, help="Like threshold. Default 1000.")
    parser.add_argument("--top", type=int, default=0, help="Keep top N after sorting desc. 0 means all.")
    parser.add_argument("--rank-by", choices=["likes", "hot"], default="likes", help="Ranking strategy.")
    parser.add_argument("--w-like", type=float, default=1.0, help="Hot-score weight for likes.")
    parser.add_argument("--w-collect", type=float, default=1.2, help="Hot-score weight for collects.")
    parser.add_argument("--w-comment", type=float, default=2.0, help="Hot-score weight for comments.")
    parser.add_argument("--w-share", type=float, default=1.5, help="Hot-score weight for shares.")
    parser.add_argument("--md-output", default="xhs_article_list.md", help="Markdown output path.")
    parser.add_argument("--csv-output", default="xhs_article_list.csv", help="CSV output path.")
    parser.add_argument("--json-output", default="xhs_article_list.json", help="Filtered JSON output path.")
    parser.add_argument(
        "--template-output",
        default="xhs_publish_templates.md",
        help="Publish-ready template markdown output path.",
    )
    args = parser.parse_args()

    items: List[Dict[str, Any]] = []
    keyword = args.keyword or ""

    if args.token and args.keyword and args.pages > 0:
        items.extend(
            fetch_pages_from_api(
                token=args.token,
                keyword=args.keyword,
                pages=args.pages,
                sort=args.sort,
                note_type=args.note_type,
                timeout=args.timeout,
            )
        )
    else:
        input_paths: List[Path] = []
        input_paths.extend([Path(p) for p in args.input if p.strip()])
        if args.input_dir:
            input_paths.extend(sorted(Path(args.input_dir).glob(args.input_glob)))
        if not input_paths:
            raise SystemExit("Provide --input/--input-dir or token+keyword+pages.")
        for p in input_paths:
            payload = json.loads(p.read_text(encoding="utf-8"))
            if not keyword:
                keyword = str(payload.get("params", {}).get("keyword") or "")
            items.extend(extract_items(payload))

    rows = build_rows(items)
    # de-dup by id
    dedup: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        key = r["id"] or r["url"] or str(len(dedup))
        old = dedup.get(key)
        if old is None or r["liked_count"] > old["liked_count"]:
            dedup[key] = r
    rows = list(dedup.values())

    for r in rows:
        r["hot_score"] = round(
            hot_score(r, args.w_like, args.w_collect, args.w_comment, args.w_share),
            2,
        )
    rows = [r for r in rows if r["liked_count"] > args.min_likes]
    if args.rank_by == "likes":
        rows.sort(key=lambda x: x["liked_count"], reverse=True)
    else:
        rows.sort(key=lambda x: x["hot_score"], reverse=True)
    if args.top and args.top > 0:
        rows = rows[: args.top]

    md_path = Path(args.md_output).resolve()
    csv_path = Path(args.csv_output).resolve()
    json_path = Path(args.json_output).resolve()
    tpl_path = Path(args.template_output).resolve()

    write_markdown(rows, md_path, keyword=keyword, min_likes=args.min_likes)
    write_csv(rows, csv_path)
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_publish_templates(rows, tpl_path, keyword=keyword)

    print(f"Saved MD:   {md_path}")
    print(f"Saved CSV:  {csv_path}")
    print(f"Saved JSON: {json_path}")
    print(f"Saved TPL:  {tpl_path}")
    print(f"Rows: {len(rows)}")
    print("\nOutput guide:")
    print(f"- {md_path.name}: 给用户快速浏览的文章清单（标题/作者/互动数据/链接）。")
    print(f"- {csv_path.name}: 适合 Excel 或 BI 二次筛选、排序、透视分析。")
    print(f"- {json_path.name}: 标准结构化结果，可用于后续脚本或系统接口。")
    print(f"- {tpl_path.name}: 基于结果自动生成的发布文案模板，可直接改写使用。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
