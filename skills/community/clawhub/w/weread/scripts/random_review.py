#!/usr/bin/env python3
"""从读书笔记库中随机抽取笔记，用于晨报/日报回顾。

用法:
  random_review.py [--count N] [--min-length L] [--format json|text]

输出:
  随机抽取 N 条有质量的读书想法（默认 3 条），附带书名、作者、划线原文。
"""

import json
import os
import random
import sys
import time

INDEX_PATH = os.path.expanduser("~/.weread/notes_index.json")
LEGACY_PATH = os.path.expanduser("~/.weread/reading_notes.json")


def load_notes(min_length: int = 20) -> list:
    """加载所有有质量的笔记（过滤太短的）"""
    # 优先使用新索引
    path = INDEX_PATH if os.path.exists(INDEX_PATH) else LEGACY_PATH
    if not os.path.exists(path):
        print(f"❌ 笔记文件不存在", file=sys.stderr)
        print("请先运行 export_notes.py 导出笔记。", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        data = json.load(f)

    all_notes = []
    # 新索引格式：扁平列表
    if "notes" in data:
        for n in data["notes"]:
            content = n.get("content", "").strip()
            if len(content) >= min_length:
                all_notes.append({
                    "title": n.get("title", ""),
                    "author": n.get("author", ""),
                    "content": content,
                    "highlight": n.get("highlight", "").strip(),
                    "createTime": n.get("createTime", 0),
                })
    # 旧格式兼容
    elif "books" in data:
        for book in data["books"]:
            for review in book.get("reviews", []):
                content = review.get("content", "").strip()
                if len(content) >= min_length:
                    all_notes.append({
                        "title": book.get("title", ""),
                        "author": book.get("author", ""),
                        "content": content,
                        "highlight": review.get("abstract", "").strip(),
                        "createTime": review.get("createTime", 0),
                    })
    return all_notes


def pick_random(notes: list, count: int = 3) -> list:
    """加权随机抽取：内容更长、更有深度的笔记权重更高"""
    if not notes:
        return []

    # Weight by content length (longer = more thoughtful)
    weights = [min(len(n["content"]), 500) for n in notes]
    
    count = min(count, len(notes))
    selected = []
    remaining = list(range(len(notes)))
    remaining_weights = list(weights)

    for _ in range(count):
        if not remaining:
            break
        choices = random.choices(range(len(remaining)), weights=remaining_weights, k=1)
        idx = choices[0]
        selected.append(notes[remaining[idx]])
        remaining.pop(idx)
        remaining_weights.pop(idx)

    return selected


def format_text(notes: list) -> str:
    """格式化为纯文本"""
    parts = []
    for i, n in enumerate(notes, 1):
        date_str = ""
        if n["createTime"]:
            date_str = time.strftime("%Y-%m-%d", time.localtime(n["createTime"]))
        
        part = f"📖 《{n['title']}》— {n['author']}"
        if date_str:
            part += f"（{date_str}）"
        part += "\n"
        
        if n["highlight"]:
            # Truncate highlight if too long
            hl = n["highlight"]
            if len(hl) > 150:
                hl = hl[:147] + "..."
            part += f"📌 「{hl}」\n"
        
        part += f"💭 {n['content']}"
        parts.append(part)

    return "\n\n".join(parts)


def main():
    count = 3
    min_length = 20
    fmt = "text"

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--count" and i + 1 < len(args):
            count = int(args[i + 1])
            i += 2
        elif args[i] == "--min-length" and i + 1 < len(args):
            min_length = int(args[i + 1])
            i += 2
        elif args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        else:
            i += 1

    notes = load_notes(min_length)
    selected = pick_random(notes, count)

    if fmt == "json":
        print(json.dumps(selected, ensure_ascii=False, indent=2))
    else:
        print(format_text(selected))


if __name__ == "__main__":
    main()
