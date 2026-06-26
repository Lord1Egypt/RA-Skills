#!/usr/bin/env python3
"""
根据建表 SQL 与慢 SQL，生成索引优化建议（MySQL/Oracle/PostgreSQL）。

输入：
  --dialect mysql|oracle|postgresql
  --ddl-file 建表语句文件
  --slow-sql-file 慢 SQL 文件（可多条，分号分隔）
  --out 输出建议文件（md/json）

说明：
- 纯规则启发式，不依赖数据库连接。
- 目标是给出“可执行的候选索引 DDL + 原因”，供 DBA/研发复核。
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


DIALECTS = {"mysql", "oracle", "postgresql"}


def clean_ident(x: str) -> str:
    x = x.strip()
    return x.strip("`\"[]")


def split_sql_statements(text: str) -> List[str]:
    parts = [p.strip() for p in text.split(";")]
    return [p for p in parts if p]


def parse_ddl_tables(ddl_text: str) -> Dict[str, Dict[str, Any]]:
    """
    返回：
      {
        table_name: {
          "columns": set(...),
          "pk": [col1, col2],
          "existing_indexes": [(name, [cols...]), ...]
        }
      }
    """
    tables: Dict[str, Dict[str, Any]] = {}

    # CREATE TABLE ... ( ... )
    create_pat = re.compile(
        r"create\s+table\s+([`\"\[\]\w\.]+)\s*\((.*?)\)\s*",
        re.IGNORECASE | re.DOTALL,
    )
    for m in create_pat.finditer(ddl_text):
        raw_table = clean_ident(m.group(1).split(".")[-1])
        body = m.group(2)
        cols: Set[str] = set()
        pk_cols: List[str] = []

        # 粗粒度按逗号切（对复杂 DDL 不完美，但足够启发）
        lines = [x.strip() for x in body.split(",") if x.strip()]
        for line in lines:
            l = line.lower()
            # 表级主键
            pm = re.search(r"primary\s+key\s*\((.*?)\)", line, re.IGNORECASE)
            if pm:
                pk_cols.extend([clean_ident(c) for c in pm.group(1).split(",")])
                continue
            # 跳过约束定义
            if l.startswith(("constraint ", "unique ", "key ", "index ", "primary key", "foreign key")):
                continue
            # 列定义第一段是列名
            head = line.split()[0]
            col = clean_ident(head)
            if col:
                cols.add(col)

        tables[raw_table] = {
            "columns": cols,
            "pk": pk_cols,
            "existing_indexes": [],
        }

    # 解析独立 CREATE INDEX
    idx_pat = re.compile(
        r"create\s+(?:unique\s+)?index\s+([`\"\[\]\w]+)\s+on\s+([`\"\[\]\w\.]+)\s*\((.*?)\)",
        re.IGNORECASE | re.DOTALL,
    )
    for m in idx_pat.finditer(ddl_text):
        idx_name = clean_ident(m.group(1))
        table = clean_ident(m.group(2).split(".")[-1])
        cols = [clean_ident(x) for x in m.group(3).split(",")]
        if table in tables:
            tables[table]["existing_indexes"].append((idx_name, cols))
        else:
            tables[table] = {
                "columns": set(cols),
                "pk": [],
                "existing_indexes": [(idx_name, cols)],
            }

    return tables


def extract_where_cols(sql: str) -> Dict[str, Set[str]]:
    out: Dict[str, Set[str]] = defaultdict(set)
    m = re.search(r"\bwhere\b(.*?)(\bgroup\s+by\b|\border\s+by\b|\blimit\b|$)", sql, re.IGNORECASE | re.DOTALL)
    if not m:
        return out
    where_clause = m.group(1)

    # table.col = ? / > / < / like / in (...)
    for tm, cm, _op in re.findall(
        r"([a-zA-Z_]\w*)\.([a-zA-Z_]\w*)\s*(=|>|<|>=|<=|like|in\b)",
        where_clause,
        re.IGNORECASE,
    ):
        out[tm].add(cm)

    # 无表别名前缀：col = ?
    for cm, _op in re.findall(r"\b([a-zA-Z_]\w*)\s*(=|>|<|>=|<=|like|in\b)", where_clause, re.IGNORECASE):
        out[""].add(cm)
    return out


def extract_join_cols(sql: str) -> Dict[str, Set[str]]:
    out: Dict[str, Set[str]] = defaultdict(set)
    for t1, c1, t2, c2 in re.findall(
        r"([a-zA-Z_]\w*)\.([a-zA-Z_]\w*)\s*=\s*([a-zA-Z_]\w*)\.([a-zA-Z_]\w*)",
        sql,
        re.IGNORECASE,
    ):
        out[t1].add(c1)
        out[t2].add(c2)
    return out


def extract_order_cols(sql: str) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = defaultdict(list)
    m = re.search(r"\border\s+by\b(.*?)(\blimit\b|$)", sql, re.IGNORECASE | re.DOTALL)
    if not m:
        return out
    seg = m.group(1)
    for token in seg.split(","):
        token = token.strip()
        if not token:
            continue
        mm = re.match(r"([a-zA-Z_]\w*)\.([a-zA-Z_]\w*)", token)
        if mm:
            out[mm.group(1)].append(mm.group(2))
        else:
            cm = re.match(r"([a-zA-Z_]\w*)", token)
            if cm:
                out[""].append(cm.group(1))
    return out


def parse_aliases(sql: str) -> Dict[str, str]:
    """
    返回 alias -> table
    """
    alias_map: Dict[str, str] = {}
    # FROM table t / JOIN table t
    for kw, table, alias in re.findall(
        r"\b(from|join)\s+([`\"\[\]\w\.]+)\s+([a-zA-Z_]\w*)",
        sql,
        re.IGNORECASE,
    ):
        t = clean_ident(table.split(".")[-1])
        alias_map[alias] = t
        alias_map[t] = t
    return alias_map


def resolve_table(alias_or_table: str, alias_map: Dict[str, str]) -> Optional[str]:
    if alias_or_table in alias_map:
        return alias_map[alias_or_table]
    return alias_or_table or None


def build_candidate_indexes(
    ddl_tables: Dict[str, Dict[str, Any]],
    slow_sqls: List[str],
) -> List[Dict[str, Any]]:
    """
    产出候选索引：
      [{"table":"orders","columns":["tenant_id","status","created_at"],"reason":"..."}, ...]
    """
    acc: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: {
        "where": set(),
        "join": set(),
        "order": set(),
    })

    for sql in slow_sqls:
        alias_map = parse_aliases(sql)
        where_cols = extract_where_cols(sql)
        join_cols = extract_join_cols(sql)
        order_cols = extract_order_cols(sql)

        for t_alias, cols in where_cols.items():
            t = resolve_table(t_alias, alias_map)
            if not t:
                continue
            acc[t]["where"].update(cols)

        for t_alias, cols in join_cols.items():
            t = resolve_table(t_alias, alias_map)
            if not t:
                continue
            acc[t]["join"].update(cols)

        for t_alias, cols in order_cols.items():
            t = resolve_table(t_alias, alias_map)
            if not t:
                continue
            acc[t]["order"].update(cols)

    candidates: List[Dict[str, Any]] = []
    for table, usage in acc.items():
        if table not in ddl_tables:
            # 未在 DDL 中找到，跳过
            continue
        cols_defined: Set[str] = ddl_tables[table]["columns"]
        where_cols = [c for c in usage["where"] if c in cols_defined]
        join_cols = [c for c in usage["join"] if c in cols_defined]
        order_cols = [c for c in usage["order"] if c in cols_defined]

        # 组合策略：where(等值/范围) + join + order
        ordered = []
        for c in where_cols + join_cols + order_cols:
            if c not in ordered:
                ordered.append(c)
        if not ordered:
            continue

        reason_parts = []
        if where_cols:
            reason_parts.append(f"WHERE 高频列: {', '.join(where_cols)}")
        if join_cols:
            reason_parts.append(f"JOIN 连接列: {', '.join(join_cols)}")
        if order_cols:
            reason_parts.append(f"ORDER BY 列: {', '.join(order_cols)}")

        candidates.append(
            {
                "table": table,
                "columns": ordered[:4],  # 控制长度，避免过宽索引
                "reason": "；".join(reason_parts),
            }
        )
    return dedupe_with_existing(candidates, ddl_tables)


def dedupe_with_existing(
    candidates: List[Dict[str, Any]],
    ddl_tables: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out = []
    seen = set()
    for c in candidates:
        table = c["table"]
        cols = tuple(c["columns"])
        key = (table, cols)
        if key in seen:
            continue
        seen.add(key)

        exists = False
        for _idx_name, idx_cols in ddl_tables.get(table, {}).get("existing_indexes", []):
            if tuple(idx_cols[: len(cols)]) == cols:
                exists = True
                break
        if exists:
            continue
        out.append(c)
    return out


def ddl_for_index(dialect: str, table: str, cols: List[str], seq: int) -> str:
    idx_name = f"idx_{table}_{'_'.join(cols)}_{seq}"
    if dialect == "mysql":
        return f"CREATE INDEX `{idx_name}` ON `{table}` ({', '.join(f'`{c}`' for c in cols)});"
    if dialect == "oracle":
        return f"CREATE INDEX {idx_name.upper()} ON {table.upper()} ({', '.join(c.upper() for c in cols)});"
    # postgresql
    quoted_cols = ", ".join(f'"{c}"' for c in cols)
    return f'CREATE INDEX "{idx_name}" ON "{table}" ({quoted_cols});'


def render_markdown(
    dialect: str,
    ddl_tables: Dict[str, Dict[str, Any]],
    slow_sqls: List[str],
    candidates: List[Dict[str, Any]],
) -> str:
    lines = [
        f"# 慢 SQL 索引优化建议（{dialect}）",
        "",
        f"- 解析到表数量：`{len(ddl_tables)}`",
        f"- 慢 SQL 条数：`{len(slow_sqls)}`",
        f"- 建议索引数：`{len(candidates)}`",
        "",
        "## 建议清单",
        "",
    ]
    if not candidates:
        lines.append("- 未生成候选索引（可能 SQL 未命中可解析的 WHERE/JOIN/ORDER 列，或索引已存在）。")
        lines.append("")
        return "\n".join(lines)

    for i, c in enumerate(candidates, start=1):
        ddl = ddl_for_index(dialect, c["table"], c["columns"], i)
        lines.extend(
            [
                f"### {i}. `{c['table']}` -> `({', '.join(c['columns'])})`",
                f"- 原因：{c['reason']}",
                "- 建议 DDL：",
                "```sql",
                ddl,
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## 注意事项",
            "- 这是静态规则建议，需结合执行计划（EXPLAIN / AWR / pg_stat_statements）复核。",
            "- 复合索引列顺序应优先等值过滤，再范围过滤，再排序列。",
            "- 写入频繁表请评估新增索引的写放大成本与维护成本。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="根据 DDL + 慢 SQL 生成索引优化建议")
    p.add_argument("--dialect", required=True, choices=sorted(DIALECTS))
    p.add_argument("--ddl-file", required=True)
    p.add_argument("--slow-sql-file", required=True)
    p.add_argument("--out", default="")
    p.add_argument("--format", choices=["md", "json"], default="md")
    args = p.parse_args()

    ddl_text = Path(args.ddl_file).expanduser().resolve().read_text(encoding="utf-8")
    slow_text = Path(args.slow_sql_file).expanduser().resolve().read_text(encoding="utf-8")
    slow_sqls = split_sql_statements(slow_text)

    ddl_tables = parse_ddl_tables(ddl_text)
    candidates = build_candidate_indexes(ddl_tables, slow_sqls)

    payload = {
        "dialect": args.dialect,
        "table_count": len(ddl_tables),
        "slow_sql_count": len(slow_sqls),
        "candidates": candidates,
    }

    out = args.out.strip()
    if not out:
        ext = "json" if args.format == "json" else "md"
        out = f"index_optimization.{args.dialect}.{ext}"
    out_path = Path(out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "json":
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        out_path.write_text(
            render_markdown(args.dialect, ddl_tables, slow_sqls, candidates),
            encoding="utf-8",
        )
    print(str(out_path))


if __name__ == "__main__":
    main()
