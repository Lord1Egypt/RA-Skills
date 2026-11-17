#!/usr/bin/env python3
"""
Generate Entity-Relationship diagrams.

Accepts two model formats:

1. List-of-tables (preferred, matches the project's SQLParser / backend):
   [
     {
       "name": "t_student",
       "comment": "学生",
       "columns": [
         {"name": "student_id", "data_type": "INT", "is_primary": true, "is_foreign": false, ...},
         {"name": "class_id", "data_type": "INT", "is_foreign": true, "reference_table": "t_class_info", ...}
       ]
     },
     ...
   ]

2. Legacy YAML entities + relationships format (still supported).

Outputs:
  - Mermaid erDiagram
  - Graphviz DOT (crow's-foot style HTML tables)
  - PNG / SVG via Graphviz

Usage:
  python generate_erd.py model.json --out /tmp/erd --format all
  python generate_erd.py model.yaml --out /tmp/erd
  cat tables.json | python generate_erd.py --stdin --out /tmp/erd
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

try:
    import graphviz
except ImportError:
    graphviz = None


def load_raw(source: str | Path | list | dict) -> Any:
    if isinstance(source, (list, dict)):
        return source
    if isinstance(source, Path) or (isinstance(source, str) and "\n" not in source and Path(source).exists()):
        text = Path(source).read_text(encoding="utf-8")
    else:
        text = source  # stdin content
    text = text.strip()
    if text.startswith("[") or text.startswith("{"):
        return json.loads(text)
    if yaml is None:
        raise RuntimeError("PyYAML required for YAML input")
    return yaml.safe_load(text)


def normalize_model(raw: Any) -> dict:
    """
    Convert any supported input into the internal shape:
    {
      "entities": { name: {"comment": ..., "attributes": [ {name, type, pk, fk, ...}, ... ] } },
      "relationships": [ {"from", "to", "cardinality", "label"}, ... ]
    }
    """
    # Already in legacy shape
    if isinstance(raw, dict) and "entities" in raw:
        return raw

    # List of tables (from SQLParser / AI backend)
    if isinstance(raw, list):
        entities = {}
        relationships = []
        seen_rels = set()

        for table in raw:
            name = table.get("name") or table.get("table_name")
            if not name:
                continue
            comment = table.get("comment", "")
            attrs = []
            for col in table.get("columns") or []:
                aname = col.get("name")
                if not aname:
                    continue
                ainfo = {
                    "type": (col.get("data_type") or col.get("type") or "string").lower(),
                    "pk": bool(col.get("is_primary") or col.get("pk") or col.get("primary_key")),
                    "fk": bool(col.get("is_foreign") or col.get("fk") or col.get("foreign_key")),
                    "unique": bool(col.get("unique") or col.get("is_unique")),
                    "comment": col.get("comment", ""),
                }
                if ainfo["fk"] and col.get("reference_table"):
                    ainfo["fk"] = col["reference_table"]  # store target for convenience
                attrs.append({aname: ainfo})

                # Build relationship from FK
                if ainfo["fk"] and col.get("reference_table"):
                    ref = col["reference_table"]
                    key = (ref, name)
                    if key not in seen_rels:
                        seen_rels.add(key)
                        relationships.append({
                            "from": ref,
                            "to": name,
                            "cardinality": "one-to-many",
                            "label": "",
                        })

            entities[name] = {"comment": comment, "attributes": attrs}

        return {"entities": entities, "relationships": relationships}

    raise ValueError("Unsupported model format. Expect list-of-tables JSON or {entities, relationships} YAML/JSON.")


def _sanitize_mermaid_type(raw: str) -> str:
    """Mermaid erDiagram only accepts simple type tokens (no parentheses, commas, spaces)."""
    if not raw:
        return "string"
    t = str(raw).strip().upper()
    # Keep only the base type name, drop (11), (10,2), UNSIGNED, etc.
    t = t.split("(")[0].strip()
    t = t.split()[0] if t else "string"  # take first word
    # Common cleanups
    mapping = {
        "INT": "int",
        "INTEGER": "int",
        "BIGINT": "bigint",
        "SMALLINT": "smallint",
        "TINYINT": "tinyint",
        "VARCHAR": "varchar",
        "CHAR": "char",
        "TEXT": "text",
        "LONGTEXT": "text",
        "MEDIUMTEXT": "text",
        "DATETIME": "datetime",
        "TIMESTAMP": "timestamp",
        "DATE": "date",
        "TIME": "time",
        "DECIMAL": "decimal",
        "NUMERIC": "decimal",
        "FLOAT": "float",
        "DOUBLE": "double",
        "BOOLEAN": "bool",
        "BOOL": "bool",
        "JSON": "json",
        "BLOB": "blob",
        "BINARY": "binary",
        "VARBINARY": "varbinary",
        "ENUM": "enum",
        "SET": "set",
        "UUID": "uuid",
        "SERIAL": "serial",
        "BIGSERIAL": "bigserial",
    }
    return mapping.get(t, t.lower().replace("-", "_") or "string")


def _sanitize_mermaid_id(name: str) -> str:
    """Entity / attribute names must be valid Mermaid identifiers."""
    if not name:
        return "unknown"
    # Replace characters that break Mermaid
    cleaned = "".join(c if c.isalnum() or c == "_" else "_" for c in str(name))
    if cleaned and cleaned[0].isdigit():
        cleaned = "n_" + cleaned
    return cleaned or "unknown"


def to_mermaid(model: dict) -> str:
    lines = ["erDiagram"]
    entities = model.get("entities") or {}
    rels = model.get("relationships") or []

    for name, meta in entities.items():
        safe_name = _sanitize_mermaid_id(name)
        attrs = meta.get("attributes") or []
        lines.append(f"    {safe_name} {{")
        if not attrs:
            lines.append("    }")
            continue
        for attr in attrs:
            if isinstance(attr, str):
                lines.append(f"        string {_sanitize_mermaid_id(attr)}")
                continue
            if not isinstance(attr, dict):
                continue
            for aname, ainfo in attr.items():
                if not isinstance(ainfo, dict):
                    ainfo = {}
                typ = _sanitize_mermaid_type(ainfo.get("type", "string"))
                flags = []
                if ainfo.get("pk") or ainfo.get("primary_key"):
                    flags.append("PK")
                if ainfo.get("fk") or ainfo.get("foreign_key"):
                    flags.append("FK")
                if ainfo.get("unique"):
                    flags.append("UK")
                flag_str = f" {','.join(flags)}" if flags else ""
                lines.append(f"        {typ} {_sanitize_mermaid_id(aname)}{flag_str}")
        lines.append("    }")

    card_map = {
        "one-to-one": "||--||",
        "one-to-many": "||--o{",
        "many-to-one": "}o--||",
        "many-to-many": "}o--o{",
        "1:1": "||--||",
        "1:n": "||--o{",
        "n:1": "}o--||",
        "n:m": "}o--o{",
        "1:N": "||--o{",
        "N:1": "}o--||",
        "N:M": "}o--o{",
    }
    for rel in rels:
        frm = _sanitize_mermaid_id(rel["from"])
        to = _sanitize_mermaid_id(rel["to"])
        card = str(rel.get("cardinality", rel.get("type", "one-to-many"))).lower().replace(" ", "-")
        symbol = card_map.get(card, "||--o{")
        label = rel.get("label", rel.get("name", "")) or ""
        # Escape double quotes inside label
        label = str(label).replace('"', "'")
        lines.append(f'    {frm} {symbol} {to} : "{label}"')

    return "\n".join(lines) + "\n"


def to_dot(model: dict, style: str = "chen") -> str:
    """
    Generate Graphviz DOT.
    style='chen'  → classic Chen notation (entity box, attribute ellipses, relationship diamond)
    style='crow'  → crow's-foot table style (legacy)
    """
    if style == "crow":
        return _to_dot_crowfoot(model)
    return _to_dot_chen(model)


def _to_dot_chen(model: dict) -> str:
    """Classic Chen ER: Entity=rectangle, Attribute=ellipse, Relationship=diamond."""
    entities = model.get("entities") or {}
    rels = model.get("relationships") or []

    lines = [
        "graph ER {",
        "    layout=neato;",
        "    overlap=false;",
        "    splines=true;",
        '    sep="+0.5";',
        '    node [fontname="SimHei, Microsoft YaHei, DejaVu Sans, sans-serif", fontsize=11];',
        '    edge [fontname="SimHei, Microsoft YaHei, DejaVu Sans, sans-serif", fontsize=10];',
        "",
    ]

    # Entity nodes (rectangle) + Attribute nodes (ellipse)
    for name, meta in entities.items():
        comment = meta.get("comment") or ""
        # Prefer Chinese comment as display label (matches the web tool)
        entity_label = (comment if comment else name).replace('"', '\\"')
        lines.append(
            f'    "TABLE_{name}" [shape=box, style="filled,bold", fillcolor=white, '
            f'label="{entity_label}", width=1.2, height=0.6];'
        )

        attrs = meta.get("attributes") or []
        for attr in attrs:
            if isinstance(attr, str):
                aname, ainfo = attr, {}
            elif isinstance(attr, dict):
                aname = next(iter(attr.keys()))
                ainfo = attr[aname] if isinstance(attr[aname], dict) else {}
            else:
                continue

            col_comment = ainfo.get("comment") or ""
            attr_text = (col_comment if col_comment else aname).replace('"', '\\"')
            # Primary key: underline via HTML-like label
            if ainfo.get("pk") or ainfo.get("primary_key"):
                attr_label = f"<<u>{attr_text}</u>>"
            else:
                attr_label = f'"{attr_text}"'

            col_key = f"COL_{name}_{aname}"
            lines.append(
                f'    "{col_key}" [shape=ellipse, style=filled, fillcolor=white, label={attr_label}];'
            )
            lines.append(f'    "TABLE_{name}" -- "{col_key}" [len=1.2];')

    # Relationship diamonds
    for i, rel in enumerate(rels):
        frm = rel["from"]
        to = rel["to"]
        rel_label = (rel.get("label") or "(关联)").replace('"', '\\"')
        rel_key = f"REL_{frm}_{to}_{i}"

        lines.append(
            f'    "{rel_key}" [shape=diamond, style="filled,bold", fillcolor=white, '
            f'label="{rel_label}", width=1.0, height=0.7];'
        )
        # N side (FK-holding table) and 1 side (referenced table)
        # In normalize_model, "from" is the referenced table, "to" is the FK table
        lines.append(f'    "TABLE_{to}" -- "{rel_key}" [label="N", len=1.5];')
        lines.append(f'    "{rel_key}" -- "TABLE_{frm}" [label="1", len=1.5];')

    lines.append("}")
    return "\n".join(lines) + "\n"


def _to_dot_crowfoot(model: dict) -> str:
    """Crow's-foot style with HTML table nodes (previous implementation)."""
    entities = model.get("entities") or {}
    rels = model.get("relationships") or []

    lines = [
        "digraph ER {",
        "    rankdir=LR;",
        '    node [fontname="Helvetica", fontsize=11];',
        '    edge [fontname="Helvetica", fontsize=10];',
        "    graph [ranksep=1.2, nodesep=0.8];",
        "",
    ]

    for name, meta in entities.items():
        attrs = meta.get("attributes") or []
        comment = meta.get("comment") or ""
        title = f"{name}" + (f" ({comment})" if comment else "")
        label_parts = [
            '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">',
            f'<TR><TD BGCOLOR="#4A90D9" COLSPAN="2"><FONT COLOR="white"><B>{title}</B></FONT></TD></TR>',
        ]
        for attr in attrs:
            if isinstance(attr, str):
                aname, ainfo = attr, {}
            elif isinstance(attr, dict):
                aname = next(iter(attr.keys()))
                ainfo = attr[aname] if isinstance(attr[aname], dict) else {}
            else:
                continue
            typ = ainfo.get("type", "")
            markers = []
            if ainfo.get("pk") or ainfo.get("primary_key"):
                markers.append("PK")
            if ainfo.get("fk") or ainfo.get("foreign_key"):
                markers.append("FK")
            if ainfo.get("unique"):
                markers.append("UQ")
            marker = f" [{' '.join(markers)}]" if markers else ""
            type_str = f" : {typ}" if typ else ""
            label_parts.append(
                f'<TR><TD ALIGN="LEFT">{aname}{marker}</TD><TD ALIGN="LEFT">{type_str}</TD></TR>'
            )
        label_parts.append("</TABLE>>")
        label = "".join(label_parts)
        lines.append(f'    "{name}" [shape=none, label={label}];')

    lines.append("")
    for rel in rels:
        frm = rel["from"]
        to = rel["to"]
        label = rel.get("label", rel.get("name", "")) or ""
        card = str(rel.get("cardinality", rel.get("type", "one-to-many"))).lower()
        if "many-to-many" in card or card in ("n:m",):
            dir_attr = 'dir="both" arrowhead="crow" arrowtail="crow"'
        elif "one-to-many" in card or card in ("1:n", "1:N", "one-to-many"):
            dir_attr = 'dir="both" arrowhead="crow" arrowtail="none"'
        elif "many-to-one" in card or card in ("n:1", "N:1"):
            dir_attr = 'dir="both" arrowhead="none" arrowtail="crow"'
        else:
            dir_attr = 'dir="both" arrowhead="none" arrowtail="none"'
        label_attr = f' label="{label}"' if label else ""
        lines.append(f'    "{frm}" -> "{to}" [{dir_attr}{label_attr}];')

    lines.append("}")
    return "\n".join(lines) + "\n"


def to_gojs_model(tables: list, english: bool = False) -> dict:
    """
    Produce the exact nodeDataArray + linkDataArray that the yanleaf.com
    GoJS frontend expects (classic Chen notation).
    """
    node_data = []
    link_data = []

    for t in tables:
        name = t.get("name")
        if not name:
            continue
        comment = t.get("comment") or ""
        table_label = name if english else (comment or name)

        node_data.append({
            "key": f"TABLE_{name}",
            "category": "Entity",
            "name": name,
            "comment": comment,
            "label": table_label,
        })

        for c in t.get("columns") or []:
            cname = c.get("name")
            if not cname:
                continue
            col_key = f"COL_{name}_{cname}"
            col_label = cname if english else (c.get("comment") or cname)

            node_data.append({
                "key": col_key,
                "category": "Attribute",
                "name": cname,
                "data_type": c.get("data_type") or c.get("type") or "",
                "is_primary": bool(c.get("is_primary")),
                "comment": c.get("comment") or "",
                "label": col_label,
            })
            link_data.append({"from": f"TABLE_{name}", "to": col_key, "text": ""})

            if c.get("is_foreign") and c.get("reference_table"):
                ref = c["reference_table"]
                rel_key = f"REL_{name}_{ref}_{cname}"
                node_data.append({
                    "key": rel_key,
                    "category": "RelationshipNode",
                    "text": "(关联)",
                })
                # N side (FK table) → diamond → 1 side (referenced table)
                link_data.append({
                    "from": f"TABLE_{name}",
                    "to": rel_key,
                    "category": "ERLink",
                    "text": "N",
                })
                link_data.append({
                    "from": rel_key,
                    "to": f"TABLE_{ref}",
                    "category": "ERLink",
                    "text": "1",
                })

    return {"nodeDataArray": node_data, "linkDataArray": link_data}


def render_graphviz(dot_source: str, out_path: Path, fmt: str = "png", engine: str | None = None) -> Path:
    if graphviz is None:
        raise RuntimeError("graphviz Python package required")
    # Auto-detect engine: neato for classic Chen (undirected graph), dot for crow's-foot
    if engine is None:
        engine = "neato" if "layout=neato" in dot_source or dot_source.strip().startswith("graph ") else "dot"
    src = graphviz.Source(dot_source, engine=engine)
    out = src.render(filename=str(out_path.with_suffix("")), format=fmt, cleanup=True)
    return Path(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate ER diagrams")
    parser.add_argument("input", nargs="?", help="Path to model file (JSON list-of-tables or YAML)")
    parser.add_argument("--stdin", action="store_true", help="Read model from stdin")
    parser.add_argument(
        "--format",
        choices=["mermaid", "dot", "png", "svg", "gojs", "all"],
        default="all",
        help="Output format. 'gojs' emits the exact node/link JSON used by the yanleaf GoJS frontend.",
    )
    parser.add_argument("--out", default="erd", help="Output file prefix")
    parser.add_argument(
        "--style",
        choices=["chen", "crow"],
        default="chen",
        help="DOT/PNG style: 'chen' = classic (entity box + attribute ovals + diamond), 'crow' = crow's-foot tables",
    )
    parser.add_argument("--english", action="store_true", help="Use English table/column names instead of Chinese comments")
    args = parser.parse_args()

    if args.stdin:
        raw = load_raw(sys.stdin.read())
    elif args.input:
        raw = load_raw(args.input)
    else:
        parser.error("Provide a model file or --stdin")

    # Keep original list-of-tables for GoJS path
    tables_raw = raw if isinstance(raw, list) else None
    model = normalize_model(raw)
    out_prefix = Path(args.out)
    formats = ["mermaid", "dot", "png", "svg", "gojs"] if args.format == "all" else [args.format]

    if "mermaid" in formats:
        mmd = to_mermaid(model)
        mmd_path = out_prefix.with_suffix(".mmd")
        mmd_path.write_text(mmd, encoding="utf-8")
        print(f"[OK] Mermaid → {mmd_path}")
        if args.format == "mermaid":
            print(mmd)

    if "gojs" in formats:
        if tables_raw is None:
            # Reconstruct a minimal list-of-tables from the normalized model
            tables_raw = []
            for ename, meta in (model.get("entities") or {}).items():
                cols = []
                for attr in meta.get("attributes") or []:
                    if isinstance(attr, dict):
                        aname = next(iter(attr.keys()))
                        ainfo = attr[aname] if isinstance(attr[aname], dict) else {}
                        cols.append({
                            "name": aname,
                            "data_type": ainfo.get("type", ""),
                            "comment": ainfo.get("comment", ""),
                            "is_primary": bool(ainfo.get("pk")),
                            "is_foreign": bool(ainfo.get("fk")),
                            "reference_table": ainfo.get("fk") if isinstance(ainfo.get("fk"), str) else None,
                        })
                tables_raw.append({"name": ename, "comment": meta.get("comment", ""), "columns": cols})
        gojs = to_gojs_model(tables_raw, english=args.english)
        gojs_path = out_prefix.with_suffix(".gojs.json")
        gojs_path.write_text(json.dumps(gojs, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] GoJS    → {gojs_path}")
        if args.format == "gojs":
            print(json.dumps(gojs, ensure_ascii=False, indent=2))

    if any(f in formats for f in ("dot", "png", "svg")):
        dot = to_dot(model, style=args.style)
        if "dot" in formats:
            dot_path = out_prefix.with_suffix(".dot")
            dot_path.write_text(dot, encoding="utf-8")
            print(f"[OK] DOT     → {dot_path}")
            if args.format == "dot":
                print(dot)

        if "png" in formats:
            try:
                png_path = render_graphviz(dot, out_prefix, "png")
                print(f"[OK] PNG     → {png_path}")
            except Exception as e:
                print(f"[WARN] PNG render failed: {e}", file=sys.stderr)

        if "svg" in formats:
            try:
                svg_path = render_graphviz(dot, out_prefix, "svg")
                print(f"[OK] SVG     → {svg_path}")
            except Exception as e:
                print(f"[WARN] SVG render failed: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
