#!/usr/bin/env python3
"""
ultra-memory: 知识库写入脚本
将重要信息追加写入 semantic/knowledge_base.jsonl，供未来相似任务检索。
写入前进行语义去重：BM25 相似度 >0.8 时强化已有条目而非重复插入。
"""

import os
import sys
import json
import math
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# 语义去重相似度阈值：超过此值视为重复，强化已有条目而非新增
_DEDUP_THRESHOLD = 0.8


def _tokenize(text: str) -> list[str]:
    """简单中英文分词"""
    words = re.findall(r'[a-zA-Z][a-zA-Z0-9_\-]*', text.lower())
    chinese = re.findall(r'[\u4e00-\u9fff]', text)
    return words + chinese


def _bm25_similarity(text_a: str, text_b: str) -> float:
    """计算两段文本的 BM25 相似度（0-1 近似归一化）。
    用于知识库去重：仅需相对比较，精确度要求低于检索场景。
    """
    tokens_a = _tokenize(text_a)
    tokens_b = _tokenize(text_b)
    if not tokens_a or not tokens_b:
        return 0.0
    set_a = set(tokens_a)
    set_b = set(tokens_b)
    overlap = set_a & set_b
    if not overlap:
        return 0.0
    # Jaccard-like 近似（对短文本等效于 BM25 排名相关性）
    return len(overlap) / (len(set_a | set_b))


def _find_similar_entry(
    title: str,
    content: str,
    entries: list[dict],
) -> tuple[int, float]:
    """返回最相似条目的 (行索引, 相似度)；未找到则返回 (-1, 0.0)"""
    query_text = title + " " + content
    best_idx, best_sim = -1, 0.0
    for i, e in enumerate(entries):
        if e.get("superseded"):
            continue
        cand_text = e.get("title", "") + " " + e.get("content", "")
        sim = _bm25_similarity(query_text, cand_text)
        if sim > best_sim:
            best_sim, best_idx = sim, i
    return best_idx, best_sim


def log_knowledge(
    title: str,
    content: str,
    project: str = "default",
    tags: list = None,
):
    """追加一条知识库条目（或强化相似已有条目）"""
    semantic_dir = ULTRA_MEMORY_HOME / "semantic"
    semantic_dir.mkdir(parents=True, exist_ok=True)
    kb_file = semantic_dir / "knowledge_base.jsonl"

    # 加载现有条目
    existing: list[dict] = []
    raw_lines: list[str] = []
    if kb_file.exists():
        for line in kb_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            raw_lines.append(line)
            try:
                existing.append(json.loads(line))
            except json.JSONDecodeError:
                existing.append({})

    # 语义去重检查
    similar_idx, similarity = _find_similar_entry(title, content, existing)
    if similarity >= _DEDUP_THRESHOLD and similar_idx >= 0:
        # 强化已有条目：更新 reinforced_count / last_reinforced / tags 合并
        old = existing[similar_idx]
        old["reinforced_count"] = old.get("reinforced_count", 0) + 1
        old["last_reinforced"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        merged_tags = list(set((old.get("tags") or []) + (tags or [])))
        if merged_tags:
            old["tags"] = merged_tags
        # 原子替换 kb 文件
        raw_lines[similar_idx] = json.dumps(old, ensure_ascii=False)
        tmp = kb_file.with_suffix(".tmp")
        tmp.write_text("\n".join(raw_lines) + "\n", encoding="utf-8")
        tmp.replace(kb_file)
        print(f"[ultra-memory] 知识库已强化（相似度 {similarity:.2f}）: {old.get('title', title)}")
        return old

    # 新增条目
    entry = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "project": project,
        "title": title[:100],
        "content": content[:200],
        "tags": tags or [],
        "reinforced_count": 0,
    }

    with open(kb_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"[ultra-memory] 知识库已写入: {title}")
    return entry


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="追加知识库条目")
    parser.add_argument("--title", required=True, help="知识标题（100字内）")
    parser.add_argument("--content", required=True, help="知识内容（200字内）")
    parser.add_argument("--project", default="default", help="关联项目名")
    parser.add_argument("--tags", default="", help="逗号分隔的标签")
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    log_knowledge(args.title, args.content, args.project, tags)
