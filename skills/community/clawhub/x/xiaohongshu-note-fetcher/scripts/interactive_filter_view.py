#!/usr/bin/env python3
"""Interactive filter & view tool for Xiaohongshu note JSON."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List


def extract_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = payload.get("data", {}).get("data", {}).get("items", [])
    if not isinstance(items, list):
        return []
    return [x for x in items if isinstance(x, dict)]


def build_rows(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in items:
        note = item.get("note", {})
        if not isinstance(note, dict):
            continue
        user = note.get("user", {}) if isinstance(note.get("user"), dict) else {}
        rows.append(
            {
                "id": str(note.get("id") or ""),
                "title": str(note.get("title") or "").strip(),
                "author": str(user.get("nickname") or "").strip(),
                "liked_count": int(note.get("liked_count") or 0),
                "collected_count": int(note.get("collected_count") or 0),
                "comments_count": int(note.get("comments_count") or 0),
                "shared_count": int(note.get("shared_count") or 0),
                "desc": str(note.get("desc") or "").strip(),
            }
        )
    return rows


def hot_score(r: Dict[str, Any]) -> float:
    return (
        r["liked_count"] * 1.0
        + r["collected_count"] * 1.2
        + r["comments_count"] * 2.0
        + r["shared_count"] * 1.5
    )


def ask(prompt: str, default: str) -> str:
    value = input(f"{prompt} [默认: {default}]：").strip()
    return value or default


def write_md(rows: List[Dict[str, Any]], out: Path, keyword: str, min_likes: int, rank_by: str) -> None:
    lines = [
        "# 小红书文章列表",
        "",
        f"- 关键词: {keyword}",
        f"- 筛选: 点赞 > {min_likes}",
        f"- 排序: {rank_by}",
        f"- 数量: {len(rows)}",
        "",
    ]
    for i, r in enumerate(rows, 1):
        lines.extend(
            [
                f"{i}. {r['title'] or 'Untitled'}",
                f"- 作者: {r['author'] or 'N/A'}",
                f"- 点赞: {r['liked_count']}",
                f"- 收藏: {r['collected_count']}",
                f"- 评论: {r['comments_count']}",
                f"- 分享: {r['shared_count']}",
                f"- 热度分: {r['hot_score']}",
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
                "desc",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Interactive filter and view for TikHub JSON.")
    parser.add_argument("--input", required=True, help="Path to JSON response file.")
    parser.add_argument("--non-interactive", action="store_true", help="Use default scheme directly.")
    parser.add_argument("--min-likes", type=int, default=1000)
    parser.add_argument("--rank-by", choices=["likes", "hot"], default="hot")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--view", choices=["summary", "full", "export"], default="summary")
    parser.add_argument("--md-output", default="xhs_article_list.md")
    parser.add_argument("--csv-output", default="xhs_article_list.csv")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    keyword = str(payload.get("params", {}).get("keyword") or "")
    rows = build_rows(extract_items(payload))
    for r in rows:
        r["hot_score"] = round(hot_score(r), 2)

    min_likes = args.min_likes
    rank_by = args.rank_by
    top = args.top
    view_mode = args.view

    if not args.non_interactive:
        min_likes = int(ask("点赞阈值（仅保留大于此值）", str(min_likes)))
        rank_by = ask("排序方式（likes/hot）", rank_by)
        top = int(ask("最多显示条数", str(top)))
        view_mode = ask("查看方式（summary/full/export）", view_mode)

    rows = [r for r in rows if r["liked_count"] > min_likes]
    if rank_by == "likes":
        rows.sort(key=lambda x: x["liked_count"], reverse=True)
    else:
        rows.sort(key=lambda x: x["hot_score"], reverse=True)
    if top > 0:
        rows = rows[:top]

    # default scheme: summary + export files
    if view_mode in ("summary", "full", "export"):
        print(f"\n关键词: {keyword} | 条数: {len(rows)} | 筛选: 点赞>{min_likes} | 排序:{rank_by}\n")
        for i, r in enumerate(rows, 1):
            print(f"{i}. {r['title']} | 点赞:{r['liked_count']} | 作者:{r['author']}")
            if view_mode == "full":
                print(f"   收藏:{r['collected_count']} 评论:{r['comments_count']} 分享:{r['shared_count']} 热度:{r['hot_score']}")
                if r["desc"]:
                    print(f"   摘要:{r['desc'][:120]}")
    write_md(rows, Path(args.md_output), keyword=keyword, min_likes=min_likes, rank_by=rank_by)
    write_csv(rows, Path(args.csv_output))
    print(f"\n已导出: {Path(args.md_output).resolve()}")
    print(f"已导出: {Path(args.csv_output).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
