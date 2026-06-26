#!/usr/bin/env python3
"""
SalesClaw - knowledge.py
知识消费统一 API

提供：
- load_sql_template(template_id)  - 加载 SQL 模板
- load_entity_schema(table_name)    - 加载表结构文档
- load_concept(concept_name)       - 加载业务概念文档
- list_templates()                 - 列出所有可用模板

"""

import json
import re
from pathlib import Path
from typing import Optional

SKILL_DIR = Path(__file__).parent.parent
KNOWLEDGE_DIR = SKILL_DIR / "knowledge"
TOOLS_DIR = SKILL_DIR / "tools"

# ─────────────────────────────────────────
# 模板缓存（避免重复读文件）
# ─────────────────────────────────────────

_TEMPLATE_CACHE: dict = {}
_ENTITY_CACHE: dict = {}


# ─────────────────────────────────────────
# SQL 模板加载
# ─────────────────────────────────────────

def load_sql_template(template_id: str) -> dict:
    """
    根据模板 ID 加载 SQL 模板文件。

    返回：
      {
        "template_id": str,
        "metadata": {"title": ..., "created": ..., "tags": [...]},
        "sql": str,           # 主 SQL（第一个 ```sql 块）
        "sqls": [str, ...],   # 所有 SQL 块（主SQL + 衍生查询）
        "适用问题": str,
        "优先级": str
      }
    """
    if template_id in _TEMPLATE_CACHE:
        return _TEMPLATE_CACHE[template_id]

    path = KNOWLEDGE_DIR / "sql_templates" / f"{template_id}.md"
    if not path.exists():
        return {"error": f"Template not found: {template_id}"}

    content = path.read_text()
    result = _parse_template_file(content, template_id)
    _TEMPLATE_CACHE[template_id] = result
    return result


def _parse_template_file(content: str, template_id: str) -> dict:
    """解析模板文件：提取 metadata + SQL 代码块"""
    metadata = {
        "template_id": template_id,
        "title": "",
        "created": "",
        "tags": [],
    }

    # 提取 frontmatter（key: value 格式，简单解析）
    frontmatter_end = content.find("\n---\n", 4)
    if frontmatter_end > 0 and content.startswith("---"):
        frontmatter = content[4:frontmatter_end]
        for line in frontmatter.split("\n"):
            if ": " in line:
                k, v = line.split(": ", 1)
                k = k.strip()
                v = v.strip()
                if k == "tags":
                    metadata["tags"] = [t.strip() for t in v.strip("[]").split(",")]
                elif k in ("title", "created"):
                    metadata[k] = v

    # 提取引用问题（从标题行或 # 行）
    title_match = re.search(r"^#+ (.+)$", content, re.MULTILINE)
    if title_match:
        metadata["title"] = title_match.group(1).strip()

    # 提取引用问题（## 模板元数据 块）
    for kw in ["适用问题", "优先级", "参数说明"]:
        m = re.search(rf"\*\*?{kw}\*\*?:?\s*(.+?)(?:\n|$)", content)
        if m:
            metadata[kw] = m.group(1).strip()

    # 提取引用问题（从 metadata 行）
    if "适用问题" not in metadata:
        m = re.search(r"- \*\*模板ID\*\*:.*?\n.*?适用问题\*\*:?\s*(.+?)(?:\n|$)", content, re.DOTALL)
        if m:
            metadata["适用问题"] = m.group(1).strip()

    # 提所有 SQL 代码块
    sql_blocks = re.findall(r"```sql\n(.*?)```", content, re.DOTALL)
    sql_blocks = [sql.strip() for sql in sql_blocks]

    return {
        "template_id": template_id,
        "metadata": metadata,
        "sql": sql_blocks[0] if sql_blocks else "",
        "sqls": sql_blocks,
    }


def list_templates() -> list:
    """列出所有可用的 SQL 模板 ID"""
    tpl_dir = KNOWLEDGE_DIR / "sql_templates"
    if not tpl_dir.exists():
        return []
    return [p.stem for p in tpl_dir.glob("*.md")]


def search_templates(query: str) -> list:
    """根据问题关键词搜索相关模板"""
    results = []
    for template_id in list_templates():
        tpl = load_sql_template(template_id)
        if "error" in tpl:
            continue
        meta = tpl["metadata"]
        tags = meta.get("tags", [])
        title = meta.get("title", "")
        适用问题 = meta.get("适用问题", "")

        score = 0
        for kw in query.lower().split():
            if kw in tags:
                score += 3
            if kw in title.lower():
                score += 2
            if kw in 适用问题.lower():
                score += 2

        if score > 0:
            results.append({
                "template_id": template_id,
                "title": title,
                "score": score,
                "适用问题": 适用问题,
                "优先级": meta.get("优先级", "P2"),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ─────────────────────────────────────────
# 实体 Schema 加载
# ─────────────────────────────────────────

def load_entity_schema(table_name: str) -> dict:
    """加载表结构文档"""
    if table_name in _ENTITY_CACHE:
        return _ENTITY_CACHE[table_name]

    # 精确匹配
    path = KNOWLEDGE_DIR / "entities" / f"{table_name}.md"

    # 模糊匹配（stem 包含 table_name）
    if not path.exists():
        for f in (KNOWLEDGE_DIR / "entities").glob("*.md"):
            if table_name in f.stem:
                path = f
                break

    if not path.exists():
        return {"error": f"Entity not found: {table_name}"}

    content = path.read_text()
    result = _parse_entity_file(content, table_name, path.stem)
    _ENTITY_CACHE[table_name] = result
    _ENTITY_CACHE[path.stem] = result
    return result


def _parse_entity_file(content: str, table_name: str, file_stem: str) -> dict:
    """解析实体文档：提取字段表 + 关联关系"""
    fields = []

    # 尝试提取字段表格（| 字段 | 类型 | 示例 |）
    table_match = re.search(
        r"\|字段\|类型\|示例\/\|\n\|[-| :]+\|\|[-| :]+\|\|[-| :]+\|"
        r"(.*?)(?:\n\n|\n## |^#)",
        content, re.DOTALL | re.MULTILINE
    )
    if table_match:
        rows = table_match.group(1).strip().split("\n")
        for row in rows:
            cols = [c.strip() for c in row.split("|")]
            if len(cols) >= 3 and cols[1]:
                fields.append({
                    "name": cols[0].strip("`*"),
                    "type": cols[1],
                    "note": cols[2] if len(cols) > 2 else "",
                })

    # 尝试关联关系
    rel_match = re.search(r"## 关联关系\s*\n(.*?)(?:\n## |\n### |\n\n#|\Z)",
                          content, re.DOTALL)
    relations = []
    if rel_match:
        for line in rel_match.group(1).strip().split("\n"):
            if "→" in line or "→" in line or "→" in line:
                parts = re.split(r"\s*[→\-\>]\s*", line)
                if len(parts) >= 2:
                    relations.append({
                        "from": parts[0].strip(),
                        "to": parts[1].strip(),
                        "type": parts[2].strip() if len(parts) > 2 else "FK",
                    })

    return {
        "table_name": table_name,
        "file_stem": file_stem,
        "fields": fields,
        "relations": relations,
        "content": content[:500],  # 截取前500字符供调试
    }


# ─────────────────────────────────────────
# 业务概念加载
# ─────────────────────────────────────────

def load_concept(concept_name: str) -> dict:
    """加载业务概念文档"""
    path = KNOWLEDGE_DIR / "concepts" / f"{concept_name}.md"
    if not path.exists():
        return {"error": f"Concept not found: {concept_name}"}
    content = path.read_text()
    title_match = re.search(r"^#+ (.+)$", content, re.MULTILINE)
    return {
        "concept": concept_name,
        "title": title_match.group(1) if title_match else concept_name,
        "content": content,
    }


# ─────────────────────────────────────────
# SQL 渲染（参数替换）
# ─────────────────────────────────────────

def render_sql(template_id: str, params: dict) -> dict:
    """
    加载模板并将 :param 参数替换为实际值。
    支持两种格式：:param_name 和 {{param_name}}
    """
    tpl = load_sql_template(template_id)
    if "error" in tpl:
        return tpl

    sql = tpl["sql"]
    rendered = sql

    # :param_name 格式
    for k, v in params.items():
        rendered = re.sub(rf":{k}\b", str(v), rendered)
        rendered = re.sub(rf"{{{{{k}}}}}", str(v), rendered)

    return {
        "template_id": template_id,
        "rendered_sql": rendered,
        "sql": sql,
        "params_used": list(params.keys()),
    }


# ─────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────

if __name__ == "__main__":
    import sys, json

    if len(sys.argv) == 1:
        print(json.dumps({
            "templates": list_templates(),
            "usage": "python knowledge.py <template_id> [params_json]"
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    action = sys.argv[1]

    if action == "list":
        print(json.dumps(list_templates(), ensure_ascii=False, indent=2))
    elif action == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        print(json.dumps(search_templates(query), ensure_ascii=False, indent=2))
    else:
        template_id = action
        params = {}
        if len(sys.argv) > 2:
            try:
                params = json.loads(sys.argv[2])
            except json.JSONDecodeError:
                pass

        if params:
            result = render_sql(template_id, params)
        else:
            result = load_sql_template(template_id)

        print(json.dumps(result, ensure_ascii=False, indent=2))