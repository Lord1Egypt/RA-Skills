"""init_wiki.py — 创建 wiki/ 骨架 + SCHEMA.md 草稿

用法:
    python init_wiki.py [--root <wiki-root>] [--force]

默认 wiki-root 由 _root.detect_wiki_root() 自动探测：
  - 编程助手环境（cwd 在项目内）→ <project-root>/.wiki-creator/
  - 办公智能体环境 → ~/.wiki-creator/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from _root import detect_wiki_root, normalize_path

DEFAULT_ROOT = detect_wiki_root()

SCHEMA_TEMPLATE = """---
schema_version: v1
---

# Wiki 知识库约束配置

> 本文件由 init_wiki.py 生成草稿，由用户编辑确认。LLM 编译前必须先读此文件。

## 主题边界

覆盖：（待 LLM 通读 raw/ 后归纳，由用户确认）
不覆盖：（待确认）

## 主题清单

> 首次创建时为空，LLM 通读 raw/ 后归纳主题填入，交用户确认。

| slug | 名称 | 简述 |
|------|------|------|

## 实体类型清单

- 概念
- 方法
- 模型
- 人物
- 机构
- 论文
- 数据集
- 事件

## 成页规则

1. 核心概念、重要方法、知名模型独立成页。
2. 子概念内容不足 200 字时，并入父概念页的子节，不单独建页。
3. 人物仅当在主题内有显著贡献时建页；否则在相关概念页以引用形式出现。
4. 论文仅当本身是里程碑（被反复引用、催生分支）时建页；其余作为来源出现在概念页的 `## 证据 / 来源`。
5. 同一实体有多个名称时，选最通用的作 slug，其余写入 `aliases`，不重复建页。

## 页面模板

见 pages/<topic>/<slug>.md 的统一结构。模板文件：assets/page-template.md。

## 写作风格

- 语言：中文为主，专有名词保留英文原文（如 Transformer、Raft）。
- 语气：客观陈述，不用第一人称，不用营销口吻。
- 引用格式：`## 证据 / 来源` 中每条形如「出自 [[相关概念]]；原文见 raw/<文件名> §<章节>」。
- 长度：单页目标 < 1500 字。
"""


def init_wiki(root: Path, force: bool = False) -> dict:
    """创建 wiki 骨架。返回创建/已存在的路径清单。"""
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)

    raw_dir = root / "raw"
    raw_dir.mkdir(exist_ok=True)

    wiki_dir = root / "wiki"
    if wiki_dir.exists() and not force:
        return {
            "status": "exists",
            "root": str(root),
            "wiki_dir": str(wiki_dir),
            "message": "wiki/ 已存在；如需重建请加 --force",
        }
    wiki_dir.mkdir(exist_ok=True)
    (wiki_dir / "topics").mkdir(exist_ok=True)
    (wiki_dir / "pages").mkdir(exist_ok=True)

    schema_path = wiki_dir / "SCHEMA.md"
    if not schema_path.exists() or force:
        schema_path.write_text(SCHEMA_TEMPLATE, encoding="utf-8")

    # 空索引文件（build_index.py 会覆盖）
    index_path = wiki_dir / "index.md"
    if not index_path.exists() or force:
        index_path.write_text(
            "<!-- 本文件由 build_index.py 自动生成，请勿手动编辑 -->\n# Wiki 索引\n\n"
            "（Wiki 尚未编译，无主题。）\n",
            encoding="utf-8",
        )

    # 空的元数据文件
    for name, default in [
        (".manifest.json", {"version": 1, "files": {}, "schema_version": "v1"}),
        (".graph.json", {"entities": {}, "page_to_sources": {}, "source_to_pages": {}}),
        (".backlinks.json", {}),
    ]:
        p = wiki_dir / name
        if not p.exists() or force:
            p.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "status": "created",
        "root": str(root),
        "wiki_dir": str(wiki_dir),
        "raw_dir": str(raw_dir),
        "schema": str(schema_path),
        "message": "wiki 骨架已创建。请上传文件到 raw/，再让 LLM 通读并归纳主题。",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化 wiki 骨架")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="wiki 根目录")
    parser.add_argument("--force", action="store_true", help="已存在时强制重建")
    args = parser.parse_args()

    result = init_wiki(normalize_path(args.root), force=args.force)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in ("created", "exists") else 1


if __name__ == "__main__":
    sys.exit(main())
