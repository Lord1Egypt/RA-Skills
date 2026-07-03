"""build_index.py — 生成 index.md + topics/*.md + 反链 + graph + manifest

用法:
    python build_index.py [--root <wiki-root>] [--raw-hashes]

扫描 wiki/pages/**/*.md，提取 frontmatter（title/topic/entity_type/aliases/sources/summary），
按主题分组、组内按 entity_type 排序，生成两级索引；扫描 [[wikilink]] 计算反链；
更新 manifest（raw 哈希）与 graph（实体→页面、页面→源、源→页面）。

脚本只做收集、分组、排序、格式化；不做语义创作。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from _root import detect_wiki_root, normalize_path

DEFAULT_ROOT = detect_wiki_root()

WIKILINK_RE = re.compile(r"\[\[([a-z0-9][a-z0-9-/]*)\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

# entity_type 排序权重（未知类型放最后）
ENTITY_ORDER = {
    "概念": 1,
    "方法": 2,
    "模型": 3,
    "数据集": 4,
    "事件": 5,
    "论文": 6,
    "人物": 7,
    "机构": 8,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """简易 YAML frontmatter 解析（只支持平铺键值与 list）。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            if inner:
                items = [x.strip().strip("'\"") for x in inner.split(",")]
            else:
                items = []
            fm[k] = items
        else:
            fm[k] = v.strip("'\"")
    return fm, body


def extract_summary(body: str) -> str:
    """从正文中提取 ## 摘要 章节的第一段。"""
    m = re.search(r"^##\s*摘要\s*$(.*?)(?=^##\s|\Z)", body, re.MULTILINE | re.DOTALL)
    if not m:
        return ""
    summary = m.group(1).strip()
    # 取第一段
    return summary.split("\n\n")[0].strip()


def extract_wikilinks(body: str) -> list[str]:
    """提取 [[wikilink]]，支持 [[slug]] 和 [[topic/slug]] 两种格式。

    返回的 slug 已去除 topic 前缀（取 / 后的部分），便于反链按 slug 统一索引。
    """
    raw_links = WIKILINK_RE.findall(body)
    slugs = []
    for link in raw_links:
        # [[topic/slug]] → 取 slug 部分；[[slug]] → 保持不变
        slug = link.rsplit("/", 1)[-1] if "/" in link else link
        slugs.append(slug)
    return slugs


def load_pages(wiki_dir: Path) -> list[dict]:
    pages_dir = wiki_dir / "pages"
    if not pages_dir.exists():
        return []
    pages = []
    for md in sorted(pages_dir.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm.get("topic"):
            continue
        slug = md.stem
        pages.append(
            {
                "path": md.relative_to(wiki_dir).as_posix(),
                "abs_path": str(md),
                "slug": slug,
                "title": fm.get("title", slug),
                "topic": fm.get("topic", ""),
                "entity_type": fm.get("entity_type", ""),
                "aliases": fm.get("aliases", []),
                "sources": fm.get("sources", []),
                "schema_version": fm.get("schema_version", ""),
                "summary": extract_summary(body),
                "wikilinks": extract_wikilinks(body),
            }
        )
    return pages


def load_topics_from_schema(wiki_dir: Path) -> dict[str, dict]:
    """从 SCHEMA.md 主题清单解析 slug → {name, desc}。"""
    schema_path = wiki_dir / "SCHEMA.md"
    if not schema_path.exists():
        return {}
    text = schema_path.read_text(encoding="utf-8")
    topics = {}
    in_topics = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## 主题清单"):
            in_topics = True
            continue
        if in_topics and s.startswith("## "):
            in_topics = False
            continue
        if not in_topics:
            continue
        if s.startswith("|") and not s.startswith("|-") and not s.startswith("| slug"):
            parts = [p.strip() for p in s.strip("|").split("|")]
            if len(parts) >= 3 and parts[0]:
                topics[parts[0]] = {"name": parts[1], "desc": parts[2]}
    return topics


def write_index(wiki_dir: Path, pages: list[dict], topics: dict[str, dict]) -> None:
    """生成 wiki/index.md。"""
    by_topic = defaultdict(list)
    for p in pages:
        by_topic[p["topic"]].append(p)

    lines = [
        "<!-- 本文件由 build_index.py 自动生成，请勿手动编辑 -->",
        "# Wiki 索引",
        "",
        "## 主题",
        "",
    ]
    if not by_topic:
        lines.append("（Wiki 尚未编译，无主题。）")
    else:
        for slug in sorted(by_topic.keys()):
            t = topics.get(slug, {})
            name = t.get("name", slug)
            desc = t.get("desc", "")
            count = len(by_topic[slug])
            desc_str = f"{desc}。" if desc else ""
            lines.append(f"### [[{slug}]] {name}")
            lines.append(f"{desc_str}共 {count} 页。")
            lines.append(f"→ 详见 topics/{slug}.md")
            lines.append("")
    (wiki_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def write_topic_indexes(wiki_dir: Path, pages: list[dict], topics: dict[str, dict]) -> None:
    """生成 wiki/topics/<slug>.md。"""
    topics_dir = wiki_dir / "topics"
    topics_dir.mkdir(exist_ok=True)

    by_topic = defaultdict(list)
    for p in pages:
        by_topic[p["topic"]].append(p)

    # 清理旧索引
    for old in topics_dir.glob("*.md"):
        old.unlink()

    for slug, group in by_topic.items():
        t = topics.get(slug, {})
        name = t.get("name", slug)
        # 组内按 entity_type 排序，再按 title
        group.sort(key=lambda p: (ENTITY_ORDER.get(p["entity_type"], 99), p["title"]))

        # 按 entity_type 分组
        by_type = defaultdict(list)
        for p in group:
            by_type[p["entity_type"] or "其他"].append(p)

        lines = [
            f"<!-- 本文件由 build_index.py 自动生成，请勿手动编辑 -->",
            f"# {name}",
            "",
            f"共 {len(group)} 页。",
            "",
        ]
        for et in sorted(by_type.keys(), key=lambda x: ENTITY_ORDER.get(x, 99)):
            lines.append(f"## {et}")
            for p in by_type[et]:
                summary = p["summary"]
                summary_str = f" — {summary}" if summary else ""
                lines.append(f"- [[{p['slug']}]] {p['title']}{summary_str}")
            lines.append("")
        (topics_dir / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")


def build_backlinks(pages: list[dict]) -> dict:
    """计算反链：target_slug → [source_slug, ...]"""
    backlinks = defaultdict(list)
    page_slugs = {p["slug"] for p in pages}
    for p in pages:
        for link in p["wikilinks"]:
            if link == p["slug"]:
                continue
            backlinks[link].append(p["slug"])
    # 去重
    return {k: sorted(set(v)) for k, v in backlinks.items()}


def build_graph(pages: list[dict]) -> dict:
    """构建 graph：实体→页面、页面→源文件、源文件→页面。"""
    entities = {}
    page_to_sources = {}
    source_to_pages = defaultdict(list)
    for p in pages:
        slug = p["slug"]
        entities[slug] = {
            "title": p["title"],
            "topic": p["topic"],
            "aliases": p["aliases"],
            "page": p["path"],
        }
        # 用 aliases 也建立索引
        for alias in p["aliases"]:
            if alias and alias not in entities:
                entities[alias] = {"redirect": slug}
        page_to_sources[slug] = p["sources"]
        for src in p["sources"]:
            source_to_pages[src].append(p["path"])
    return {
        "entities": entities,
        "page_to_sources": page_to_sources,
        "source_to_pages": dict(source_to_pages),
    }


def update_manifest(root: Path, wiki_dir: Path, pages: list[dict]) -> dict:
    """刷新 manifest：raw 文件 sha256 + 编译记录 + schema 版本。"""
    raw_dir = root / "raw"
    files = {}
    if raw_dir.exists():
        for f in sorted(raw_dir.iterdir()):
            if not f.is_file() or f.name.startswith("."):
                continue
            rel = f"raw/{f.name}"
            files[rel] = {"sha256": sha256(f), "compiled_at": None}

    # 标记哪些文件产出了页面
    page_sources = set()
    for p in pages:
        for s in p["sources"]:
            page_sources.add(s)
    for rel in files:
        if rel in page_sources:
            files[rel]["compiled"] = True

    # schema 版本
    schema_path = wiki_dir / "SCHEMA.md"
    schema_version = "v1"
    if schema_path.exists():
        for line in schema_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("schema_version:"):
                schema_version = line.split(":", 1)[1].strip()
                break

    return {"version": 1, "schema_version": schema_version, "files": files, "page_count": len(pages)}


def build_index(root: Path) -> dict:
    wiki_dir = root / "wiki"
    if not wiki_dir.exists():
        return {"error": "wiki/ 不存在，请先运行 init_wiki.py"}

    pages = load_pages(wiki_dir)
    topics = load_topics_from_schema(wiki_dir)

    write_index(wiki_dir, pages, topics)
    write_topic_indexes(wiki_dir, pages, topics)

    backlinks = build_backlinks(pages)
    (wiki_dir / ".backlinks.json").write_text(
        json.dumps(backlinks, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    graph = build_graph(pages)
    (wiki_dir / ".graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    manifest = update_manifest(root, wiki_dir, pages)
    (wiki_dir / ".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return {
        "status": "ok",
        "page_count": len(pages),
        "topics": sorted({p["topic"] for p in pages}),
        "backlinks_count": sum(len(v) for v in backlinks.values()),
        "raw_files": len(manifest["files"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 wiki 两级索引 + 元数据")
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    args = parser.parse_args()
    result = build_index(normalize_path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
