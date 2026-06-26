#!/usr/bin/env python3
"""
scaffold.py — 引导新的 Wiki 知识库目录树

用法:
    python3 scaffold.py /path/to/wiki "Wiki 主题名称"
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime


def create_wiki_structure(wiki_root: Path, topic: str):
    """Create wiki directory structure."""

    # Create directories
    dirs = [
        "raw/articles",
        "raw/papers",
        "raw/notes",
        "raw/assets",
        "wiki/concepts",
        "wiki/entities",
        "wiki/summaries",
        "outputs/queries",
    ]

    for d in dirs:
        (wiki_root / d).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {d}")

    today = datetime.now().strftime("%Y-%m-%d")

    # Create CLAUDE.md
    claude_md = f"""# {topic} — LLM Wiki Schema

**Version**: 1.0 (基于 Karpathy LLM Wiki 模式)
**Created**: {today}
**Scope**: <定义 Wiki 范围>

---

## 核心定位

<描述这个 Wiki 的核心主题和覆盖领域>

---

## 三层架构

```
<wiki-root>/
├── CLAUDE.md          ← Schema 定义（本文件）
├── log.md             ← 只增不减的时间线日志
│
├── raw/               ← 原始资料层（LLM 只读，永不修改）
│   ├── articles/      ← 网页文章
│   ├── papers/        ← 学术论文
│   └── notes/         ← 个人笔记
│
└── wiki/              ← Wiki 知识层（LLM 编写，用户阅读）
    ├── index.md       ← 主目录
    ├── concepts/      ← 概念页面
    ├── entities/      ← 实体页面
    └── summaries/     ← 摘要页面
```

---

## 核心操作

### 1. Ingest（摄取）
用户保存新资料到 `raw/` → LLM 编译为 Wiki 页面

### 2. Query（查询）
用户针对 Wiki 提问 → LLM 综合答案 → 好的答案晋升为 Wiki 页面

### 3. Lint（健康检查）
定期运行 `python3 scripts/lint_wiki.py .` — 检查死链接、孤立页面、矛盾陈述

---

## 命名规范

| 类型 | 位置 | 格式 |
|------|------|------|
| Concepts | `wiki/concepts/` | Title Case（中文术语/主题） |
| Entities | `wiki/entities/` | Proper Name（专有名词） |
| Summaries | `wiki/summaries/` | kebab-case（来源 slug） |

---

## Frontmatter（所有页面必需）

```yaml
---
title: "页面标题"
type: concept | entity | summary | output | meta
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [raw/ slug 列表]
tags: [tag1, tag2]
---
```

---

## Wikilink 规则

1. **每个实体/概念的首次提及都要链接**
2. **同一页面最多链接两次**
3. **链接存在的概念** — 创建新链接前检查 `wiki/index.md`
4. **反向链接审计** — 写完新文章后补充入站链接

---

## 来源矛盾处理

当两个来源矛盾时：
1. 明确陈述两个主张
2. 注明每个主张由哪个来源支持
3. 加入"Open questions"部分
4. **不要沉默地选择其一**

---

## Session 启动检查清单

每个新 Session：
1. [ ] 读取本 CLAUDE.md
2. [ ] 读取 `log.md` 最近 5 条：`grep "^## \\[" log.md | tail -5`
3. [ ] 如有新 raw/ 资料，执行 Ingest
4. [ ] 如用户提问，执行 Query（先查 index.md）
5. [ ] 如 ingest 超过 10 次未 lint，执行 Lint

---

## 开放研究问题

<你想更好地理解什么？驱动未来的 ingest/query>
"""

    (wiki_root / "CLAUDE.md").write_text(claude_md, encoding="utf-8")
    print(f"  ✓ Created: CLAUDE.md")

    # Create log.md
    log_md = f"""# Log

Append-only chronological record of all wiki operations.
Format: `## [YYYY-MM-DD] <op> | <description>`
Ops: `ingest`, `compile`, `query`, `lint`, `promote`, `split`

Quick grep: `grep "^## \\[" log.md | tail -5`

---

## [{today}] scaffold | Initialized {topic} using synapse-wiki skill
"""

    (wiki_root / "log.md").write_text(log_md, encoding="utf-8")
    print(f"  ✓ Created: log.md")

    # Create wiki/index.md
    index_md = f"""# Index — {topic}

> Master catalog of all wiki pages. Updated after every ingest.

## Concepts（概念）

*(none yet)*

## Entities（实体）

*(none yet)*

## Summaries（资料摘要）

*(none yet)*

## Outputs（探索产出）

*(none yet)*
"""

    (wiki_root / "wiki" / "index.md").write_text(index_md, encoding="utf-8")
    print(f"  ✓ Created: wiki/index.md")

    print("\n" + "="*60)
    print(f" Wiki 知识库已初始化：{wiki_root}")
    print("="*60)
    print("\nNext steps:")
    print(f"  1. Edit CLAUDE.md to define scope and naming conventions")
    print(f"  2. Save sources to raw/articles/ or raw/papers/")
    print(f"  3. Run: /synapse-wiki ingest {wiki_root} <source-file>")
    print()


def main():
    parser = argparse.ArgumentParser(description="引导新的 Wiki 知识库目录树")
    parser.add_argument("path", help="Wiki 根目录路径")
    parser.add_argument("topic", nargs="?", default="Knowledge Base", help="Wiki 主题名称")
    args = parser.parse_args()

    wiki_root = Path(args.path).resolve()
    topic = args.topic

    if not wiki_root.exists():
        wiki_root.mkdir(parents=True, exist_ok=True)

    create_wiki_structure(wiki_root, topic)


if __name__ == "__main__":
    main()
