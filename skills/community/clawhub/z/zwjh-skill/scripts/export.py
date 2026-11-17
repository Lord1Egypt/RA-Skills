# -*- coding: utf-8 -*-
"""
记忆导出 —— 多格式、可选中、可迁移。

支持格式：
  - markdown  人类可读的 MD 文档（默认）
  - json      结构化 JSON（供程序消费）
  - cypher    Neo4j Cypher 脚本（直接导入图数据库）
  - csv       Excel 兼容
  - obsidian  Obsidian vault 格式（含 frontmatter）
  - logseq    Logseq 格式

支持筛选：按实体类型 / 时间范围 / 重要度阈值。

所有导出均为「只读」操作，不修改源数据。
"""

from __future__ import annotations

import csv
import io
import json
import os
from dataclasses import dataclass, field
from datetime import datetime

from . import config, store, graph


# ── 筛选参数 ──────────────────────────────────────────────────────────────
@dataclass
class ExportFilter:
    """导出筛选条件。"""
    types: list[str] | None = None          # 实体类型白名单
    day_from: str | None = None             # 起始日期
    day_to: str | None = None               # 结束日期
    importance_min: float = 0.0             # 最低重要度
    limit: int = 5000                       # 最多导出实体数


# ── 导出器 ────────────────────────────────────────────────────────────────
class Exporter:
    """多格式导出器。"""

    def __init__(self, export_filter: ExportFilter | None = None):
        self.f = export_filter or ExportFilter()

    def _load_data(self) -> dict:
        """加载并筛选图谱数据。"""
        entities = store.list_entities(limit=self.f.limit)
        if self.f.types:
            entities = [e for e in entities if e["type"] in self.f.types]
        if self.f.importance_min > 0:
            entities = [e for e in entities if e["importance"] >= self.f.importance_min]
        if self.f.day_from:
            entities = [e for e in entities if (e["created_at"] or "")[:10] >= self.f.day_from]
        if self.f.day_to:
            entities = [e for e in entities if (e["created_at"] or "")[:10] <= self.f.day_to]

        entity_ids = {e["id"] for e in entities}
        relations = []
        for e in entities:
            for r in store.relations_of(e["id"], direction="out"):
                if r["to_id"] in entity_ids:
                    relations.append(r)

        facts = []
        for e in entities:
            for f in store.current_facts(e["id"]):
                facts.append({**f, "entity_name": e["name"]})

        return {"entities": entities, "relations": relations, "facts": facts}

    def export_markdown(self) -> str:
        """导出为人类可读的 Markdown。"""
        d = self._load_data()
        lines = []
        lines.append(f"# 知识图谱导出\n")
        lines.append(f"> 导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        lines.append(f"> 实体数：{len(d['entities'])}　关系数：{len(d['relations'])}　事实数：{len(d['facts'])}\n")
        lines.append("\n---\n")

        # 按类型分组
        by_type: dict[str, list] = {}
        for e in d["entities"]:
            by_type.setdefault(e["type"], []).append(e)

        for t, ents in sorted(by_type.items()):
            lines.append(f"\n## {t}\n")
            for e in ents:
                lines.append(f"\n### {e['name']}\n")
                lines.append(f"- 重要度：{e['importance']}")
                lines.append(f"- 更新时间：{e['updated_at']}")
                # 事实
                ent_facts = [f for f in d["facts"] if f["entity_name"] == e["name"]]
                if ent_facts:
                    lines.append(f"\n**属性：**\n")
                    for f in ent_facts:
                        lines.append(f"- {f['predicate']}：{f['value']}")
                # 关系
                ent_rels = [r for r in d["relations"] if r.get("from_id") == e["id"] or r.get("to_id") == e["id"]]
                if ent_rels:
                    lines.append(f"\n**关联：**\n")
                    for r in ent_rels:
                        if r.get("from_id") == e["id"]:
                            lines.append(f"- → {r.get('to_name', '?')} ({r['relation']})")
                        else:
                            lines.append(f"- ← {r.get('from_name', '?')} ({r['relation']})")

        return "\n".join(lines)

    def export_json(self) -> str:
        """导出为结构化 JSON。"""
        d = self._load_data()
        return json.dumps(d, ensure_ascii=False, indent=2)

    def export_cypher(self) -> str:
        """导出为 Neo4j Cypher 脚本。"""
        d = self._load_data()
        lines = []
        lines.append(f"// zwjh-skill 知识图谱导出")
        lines.append(f"// 导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"// 实体数：{len(d['entities'])}　关系数：{len(d['relations'])}\n")

        # 创建实体节点
        for e in d["entities"]:
            name_escaped = e["name"].replace("'", "\\'")
            cypher = "CREATE (n:%s {name: '%s', importance: %s})" % (e['type'], name_escaped, e['importance'])
            lines.append(cypher)

        lines.append("\n// 创建关系\n")

        # 创建关系
        for r in d["relations"]:
            rel_escaped = r["relation"].replace("'", "\\'")
            cypher = "MATCH (a), (b) WHERE a.id = %s AND b.id = %s CREATE (a)-[:%s]->(b)" % (r['from_id'], r['to_id'], rel_escaped)
            lines.append(cypher)

        return "\n".join(lines)

    def export_csv(self) -> str:
        """导出为 CSV（Excel 兼容）。"""
        d = self._load_data()
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["type", "name", "importance", "updated_at", "predicate", "value"])
        for e in d["entities"]:
            ent_facts = [f for f in d["facts"] if f["entity_name"] == e["name"]]
            if ent_facts:
                for f in ent_facts:
                    writer.writerow([e["type"], e["name"], e["importance"], e["updated_at"],
                                     f["predicate"], f["value"]])
            else:
                writer.writerow([e["type"], e["name"], e["importance"], e["updated_at"], "", ""])
        return buf.getvalue()

    def export_obsidian(self, vault_path: str | None = None) -> str:
        """导出为 Obsidian vault 目录结构。"""
        d = self._load_data()
        if vault_path is None:
            vault_path = str(config.ZWJH_DIR / "obsidian_export")

        os.makedirs(vault_path, exist_ok=True)

        # 每个实体一个 MD 文件
        for e in d["entities"]:
            filename = "%s_%s.md" % (e['type'], e['name'])
            filename = filename.replace("/", "_").replace("\\", "_")
            filepath = os.path.join(vault_path, filename)

            lines = []
            lines.append("---")
            lines.append("type: %s" % e['type'])
            lines.append("importance: %s" % e['importance'])
            lines.append("tags: [memory, %s]" % e['type'])
            lines.append("---\n")
            lines.append("# %s\n" % e['name'])

            # 事实
            ent_facts = [f for f in d["facts"] if f["entity_name"] == e["name"]]
            if ent_facts:
                lines.append("## 属性\n")
                for f in ent_facts:
                    lines.append("- **%s**: %s" % (f['predicate'], f['value']))

            # 关系
            ent_rels_out = [r for r in d["relations"] if r.get("from_id") == e["id"]]
            ent_rels_in = [r for r in d["relations"] if r.get("to_id") == e["id"]]
            if ent_rels_out or ent_rels_in:
                lines.append("\n## 关联\n")
                for r in ent_rels_out:
                    target = r.get("to_name", "?")
                    lines.append("- [[%s]] --(%s)--> " % (target, r['relation']))
                for r in ent_rels_in:
                    source = r.get("from_name", "?")
                    lines.append("- [[%s]] --(←%s)-- " % (source, r["relation"]))

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

        # 索引文件
        index_path = os.path.join(vault_path, "index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("# 知识图谱索引\n\n")
            for e in d["entities"]:
                filename = "%s_%s.md" % (e['type'], e['name'])
                filename = filename.replace("/", "_").replace("\\", "_")
                f.write("- [[%s|%s]]\n" % (e['name'], filename))

        return vault_path

    def export_logseq(self, pages_path: str | None = None) -> str:
        """导出为 Logseq 格式。"""
        d = self._load_data()
        if pages_path is None:
            pages_path = str(config.ZWJH_DIR / "logseq_export" / "pages")

        os.makedirs(pages_path, exist_ok=True)

        for e in d["entities"]:
            filename = "%s__%s.md" % (e['type'], e['name'])
            filename = filename.replace("/", "_").replace("\\", "_")
            filepath = os.path.join(pages_path, filename)

            lines = []
            lines.append("type:: %s" % e['type'])
            lines.append("importance:: %s" % e['importance'])
            lines.append("updated-at:: %s" % e['updated_at'])
            lines.append("\n# %s\n" % e['name'])

            ent_facts = [f for f in d["facts"] if f["entity_name"] == e["name"]]
            if ent_facts:
                for f in ent_facts:
                    lines.append("- **%s**:: %s" % (f['predicate'], f['value']))

            ent_rels_out = [r for r in d["relations"] if r.get("from_id") == e["id"]]
            if ent_rels_out:
                lines.append("")
                for r in ent_rels_out:
                    target = r.get("to_name", "?")
                    lines.append("- [[%s]] : %s" % (target, r['relation']))

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

        return pages_path


def selective_export(format: str, types: list[str] | None = None,
                     day_from: str | None = None, day_to: str | None = None,
                     importance_min: float = 0.0, output_dir: str | None = None) -> dict:
    """
    选择性导出（统一入口）。

    format: markdown / json / cypher / csv / obsidian / logseq
    """
    export_filter = ExportFilter(
        types=types, day_from=day_from, day_to=day_to,
        importance_min=importance_min,
    )
    exporter = Exporter(export_filter)

    if format == "markdown":
        content = exporter.export_markdown()
        path = _write_file(output_dir, "zwjh_graph.md", content)
    elif format == "json":
        content = exporter.export_json()
        path = _write_file(output_dir, "zwjh_graph.json", content)
    elif format == "cypher":
        content = exporter.export_cypher()
        path = _write_file(output_dir, "zwjh_graph.cypher", content)
    elif format == "csv":
        content = exporter.export_csv()
        path = _write_file(output_dir, "zwjh_graph.csv", content)
    elif format == "obsidian":
        path = exporter.export_obsidian(output_dir)
        content = f"已导出 {path}"
    elif format == "logseq":
        path = exporter.export_logseq(output_dir)
        content = f"已导出 {path}"
    else:
        return {"status": "error", "reason": f"不支持的格式: {format}"}

    return {"status": "ok", "format": format, "path": path, "content": content}


def _write_file(output_dir: str | None, filename: str, content: str) -> str:
    """写入文件并返回路径。"""
    if output_dir is None:
        output_dir = str(config.ZWJH_DIR / "exports")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


if __name__ == "__main__":
    r = selective_export("markdown")
    print(r)
