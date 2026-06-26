#!/usr/bin/env python3
"""微信读书笔记导出工具 — 结构化存储

存储结构:
  ~/.weread/
  ├── books.json          # 书籍索引（bookId → 元信息）
  ├── notes/
  │   ├── <bookId>.json   # 每本书一个文件（笔记+划线+章节）
  │   └── ...
  └── notes_index.json    # 全量笔记索引（按时间排序，方便检索）

用法:
  export_notes.py                  # 全量导出
  export_notes.py --incremental    # 增量导出（仅新书/新笔记）
  export_notes.py --stats          # 显示统计信息
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from weread_api import (
    get_bookshelf, get_notebooks, get_book_info,
    get_reviews, get_bookmarks, get_chapter_infos,
    get_reading_progress
)

BASE_DIR = os.path.expanduser("~/.weread")
BOOKS_PATH = os.path.join(BASE_DIR, "books.json")
NOTES_DIR = os.path.join(BASE_DIR, "notes")
INDEX_PATH = os.path.join(BASE_DIR, "notes_index.json")


def _fmt_time(ts: int) -> str:
    if not ts:
        return ""
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))


def _fmt_duration(seconds: int) -> str:
    if not seconds:
        return "0分钟"
    h, m = divmod(seconds // 60, 60)
    if h:
        return f"{h}小时{m}分钟" if m else f"{h}小时"
    return f"{m}分钟"


def load_existing_books() -> dict:
    if os.path.exists(BOOKS_PATH):
        with open(BOOKS_PATH) as f:
            return json.load(f)
    return {}


def export_full():
    """全量导出"""
    os.makedirs(NOTES_DIR, exist_ok=True)
    log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", file=sys.stderr)

    # 1. 拉取书架
    log("拉取书架...")
    shelf = get_bookshelf()
    shelf_books = shelf.get("books", [])
    progress_list = shelf.get("bookProgress", [])
    progress_map = {p["bookId"]: p for p in progress_list}

    # 2. 拉取有笔记的书
    log("拉取笔记列表...")
    notebooks = get_notebooks()
    log(f"共 {len(notebooks)} 本有笔记的书")

    # 3. 构建书籍索引
    books_index = {}
    for b in shelf_books:
        bid = b.get("bookId", "")
        prog = progress_map.get(bid, {})
        books_index[bid] = {
            "bookId": bid,
            "title": b.get("title", ""),
            "author": b.get("author", ""),
            "translator": b.get("translator", ""),
            "cover": b.get("cover", ""),
            "category": "",  # 需要单独查询
            "publisher": b.get("publisher", ""),
            "publishTime": b.get("publishTime", ""),
            "progress": prog.get("progress", 0),
            "readingTime": prog.get("readingTime", 0),
            "readingTimeFormatted": _fmt_duration(prog.get("readingTime", 0)),
            "finishReading": b.get("finishReading", 0) == 1,
            "lastReadTime": _fmt_time(prog.get("updateTime", 0)),
        }

    # 4. 逐本导出笔记
    all_notes_flat = []
    count = 0
    for nb in notebooks:
        book = nb.get("book", {})
        bid = book.get("bookId", "")
        title = book.get("title", "")
        author = book.get("author", "")
        note_count = nb.get("reviewCount", 0)
        mark_count = nb.get("bookmarkCount", 0)

        if note_count == 0 and mark_count == 0:
            continue

        count += 1
        if count % 20 == 0:
            log(f"  进度: {count}/{len(notebooks)}...")

        # 获取笔记
        reviews = []
        if note_count > 0:
            try:
                raw = get_reviews(bid)
                for r in raw:
                    ct = r.get("createTime", 0)
                    review_item = {
                        "type": "thought",
                        "content": r.get("content", ""),
                        "highlight": r.get("abstract", ""),
                        "chapterUid": r.get("chapterUid", 0),
                        "createTime": ct,
                        "createDate": _fmt_time(ct),
                    }
                    reviews.append(review_item)
                    # 加入扁平索引
                    all_notes_flat.append({
                        "bookId": bid,
                        "title": title,
                        "author": author,
                        **review_item,
                    })
            except Exception as e:
                log(f"  ⚠ 获取 {title} 笔记失败: {e}")

        # 划线和章节信息：跳过全量导出（太慢），按需获取
        bookmarks = []
        chapters = {}

        # 写入单书文件
        book_file = {
            "bookId": bid,
            "title": title,
            "author": author,
            "noteCount": len(reviews),
            "highlightCount": len(bookmarks),
            "chapters": chapters,
            "notes": reviews,
            "highlights": bookmarks,
            "exportTime": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        with open(os.path.join(NOTES_DIR, f"{bid}.json"), "w") as f:
            json.dump(book_file, f, ensure_ascii=False, indent=2)

    # 5. 保存书籍索引
    with open(BOOKS_PATH, "w") as f:
        json.dump(books_index, f, ensure_ascii=False, indent=2)
    log(f"书籍索引: {len(books_index)} 本 → {BOOKS_PATH}")

    # 6. 保存笔记索引（按时间倒序）
    all_notes_flat.sort(key=lambda x: x.get("createTime", 0), reverse=True)
    with open(INDEX_PATH, "w") as f:
        json.dump({
            "exportTime": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "totalNotes": len(all_notes_flat),
            "notes": all_notes_flat,
        }, f, ensure_ascii=False, indent=2)
    log(f"笔记索引: {len(all_notes_flat)} 条 → {INDEX_PATH}")

    log("✅ 全量导出完成")
    print(f"书籍: {len(books_index)} | 有笔记: {count} | 笔记: {len(all_notes_flat)}")


def show_stats():
    """显示统计信息"""
    if not os.path.exists(BOOKS_PATH):
        print("❌ 未导出，请先运行 export_notes.py")
        return

    with open(BOOKS_PATH) as f:
        books = json.load(f)
    with open(INDEX_PATH) as f:
        index = json.load(f)

    total = len(books)
    finished = sum(1 for b in books.values() if b.get("finishReading"))
    reading = sum(1 for b in books.values() if b.get("progress", 0) > 0 and not b.get("finishReading"))
    total_time = sum(b.get("readingTime", 0) for b in books.values())
    notes = index["totalNotes"]

    print(f"📚 书架: {total} 本 (读完 {finished} / 在读 {reading} / 未读 {total - finished - reading})")
    print(f"⏱ 总阅读时长: {_fmt_duration(total_time)}")
    print(f"✏️ 笔记: {notes} 条")
    print(f"📁 存储: {NOTES_DIR}/ ({len(os.listdir(NOTES_DIR))} 个文件)")
    print(f"🕐 上次导出: {index['exportTime']}")

    # Notes per year
    from collections import Counter
    years = Counter()
    for n in index["notes"]:
        if n.get("createTime"):
            y = time.strftime("%Y", time.localtime(n["createTime"]))
            years[y] += 1
    print("\n📊 笔记年度分布:")
    for y in sorted(years):
        bar = "█" * (years[y] // 10)
        print(f"  {y}: {years[y]:>4} 条 {bar}")


def main():
    if "--stats" in sys.argv:
        show_stats()
    else:
        export_full()


if __name__ == "__main__":
    main()
