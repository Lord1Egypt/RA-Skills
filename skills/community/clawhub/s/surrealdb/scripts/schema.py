# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "rich>=13.0.0",
#   "websockets>=12.0",
# ]
# ///
"""SurrealDB schema introspection and export tool.

Subcommands:
  introspect  -- Full schema dump of tables, fields, indexes, events, accesses.
  tables      -- Table summary with field/index/event counts.
  table       -- Detailed view of one table.
  export      -- Export the complete schema as SurrealQL DEFINE statements.
  inspect     -- Legacy alias for introspect.
  diff        -- Compare two SurrealQL schema files and show differences.
"""

from __future__ import annotations

import argparse
import asyncio
import difflib
import json
import os
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

stderr_console = Console(stderr=True)

DEFAULT_ENDPOINT = "http://localhost:8000"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _env(name: str) -> str | None:
    val = os.environ.get(name, "").strip()
    return val if val else None


import re as _re

_SAFE_IDENT = _re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _sanitize_identifier(name: str) -> str:
    """Validate that a name is a safe SurrealQL identifier.

    Prevents SurrealQL injection by rejecting names that contain
    anything other than alphanumeric characters and underscores.
    """
    name = name.strip()
    if not name or not _SAFE_IDENT.match(name):
        raise ValueError(
            f"Invalid identifier: {name!r}. "
            "Identifiers must match [a-zA-Z_][a-zA-Z0-9_]*."
        )
    return name


def _rpc_endpoint(endpoint: str) -> str:
    """Normalize a user-facing endpoint into a WebSocket RPC endpoint."""
    ep = endpoint.rstrip("/")
    if ep.startswith("http://"):
        ep = "ws://" + ep[len("http://"):]
    elif ep.startswith("https://"):
        ep = "wss://" + ep[len("https://"):]
    elif not ep.startswith(("ws://", "wss://")):
        ep = f"ws://{ep}"
    return ep + "/rpc"


async def _ws_query(endpoint: str, user: str, password: str, ns: str, db: str, query: str) -> Any:
    """Connect via WebSocket RPC, authenticate, USE ns/db, and execute a query."""
    import websockets  # type: ignore[import-untyped]

    ws_ep = _rpc_endpoint(endpoint)
    async with websockets.connect(ws_ep, open_timeout=10, close_timeout=5) as ws:
        # Sign in
        signin_msg = json.dumps({
            "id": "signin",
            "method": "signin",
            "params": [{"user": user, "pass": password}],
        })
        await ws.send(signin_msg)
        signin_resp = json.loads(await ws.recv())
        if signin_resp.get("error"):
            raise RuntimeError(f"Auth failed: {signin_resp['error']}")

        # USE
        use_msg = json.dumps({
            "id": "use",
            "method": "use",
            "params": [ns, db],
        })
        await ws.send(use_msg)
        use_resp = json.loads(await ws.recv())
        if use_resp.get("error"):
            raise RuntimeError(f"USE failed: {use_resp['error']}")

        # Query
        query_msg = json.dumps({
            "id": "query",
            "method": "query",
            "params": [query],
        })
        await ws.send(query_msg)
        query_resp = json.loads(await ws.recv())
        if query_resp.get("error"):
            raise RuntimeError(f"Query failed: {query_resp['error']}")
        return query_resp.get("result")


def run_query(endpoint: str, user: str, password: str, ns: str, db: str, query: str) -> Any:
    """Synchronous wrapper for WebSocket query."""
    return asyncio.run(_ws_query(endpoint, user, password, ns, db, query))


def _extract_result(raw: Any) -> Any:
    """Extract the inner result from a SurrealDB query response list."""
    if isinstance(raw, list) and raw:
        first = raw[0]
        if isinstance(first, dict) and "result" in first:
            return first["result"]
        return first
    return raw


def _normalize_db_info(db_info: Any) -> dict[str, dict[str, Any]]:
    key_aliases = {
        "ac": "accesses",
        "az": "analyzers",
        "fn": "functions",
        "ml": "models",
        "pa": "params",
        "tb": "tables",
        "us": "users",
    }
    normalized: dict[str, dict[str, Any]] = {}
    if isinstance(db_info, dict):
        for key, value in db_info.items():
            canon = key_aliases.get(key, key)
            if isinstance(value, dict):
                normalized[canon] = value
    return normalized


def _definition_text(value: Any) -> str:
    return value if isinstance(value, str) else json.dumps(value, default=str)


def _section_data(tbl_info: Any, *keys: str) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    if not isinstance(tbl_info, dict):
        return merged
    for key in keys:
        value = tbl_info.get(key)
        if isinstance(value, dict):
            merged.update(value)
    return merged


def _match_clause(pattern: str, definition: str) -> str | None:
    match = _re.search(pattern, definition, flags=_re.IGNORECASE | _re.DOTALL)
    if not match:
        return None
    return " ".join(match.group(1).strip().split())


def _parse_field(name: str, definition: Any) -> dict[str, Any]:
    text = _definition_text(definition)
    return {
        "name": name,
        "type": _match_clause(r"\bTYPE\s+(.+?)(?=\s+(?:VALUE|ASSERT|DEFAULT|PERMISSIONS)\b|;|$)", text),
        "default": _match_clause(r"\bDEFAULT\s+(.+?)(?=\s+(?:VALUE|ASSERT|PERMISSIONS)\b|;|$)", text),
        "assert": _match_clause(r"\bASSERT\s+(.+?)(?=\s+(?:DEFAULT|VALUE|PERMISSIONS)\b|;|$)", text),
    }


def _parse_index(name: str, definition: Any) -> dict[str, Any]:
    text = _definition_text(definition)
    fields_raw = _match_clause(
        r"\bFIELDS\s+(.+?)(?=\s+(?:UNIQUE|SEARCH|HNSW|MTREE|COMMENT|CONCURRENTLY|;)|$)",
        text,
    ) or ""
    fields = [field.strip() for field in fields_raw.split(",") if field.strip()]
    upper = text.upper()
    return {
        "name": name,
        "fields": fields,
        "unique": " UNIQUE" in upper,
        "search": " SEARCH" in upper,
        "vector": " HNSW" in upper or " MTREE" in upper,
    }


def _parse_permissions(table_definition: str) -> dict[str, str]:
    permissions = {action: "FULL" for action in ("select", "create", "update", "delete")}
    upper = table_definition.upper()
    if "PERMISSIONS NONE" in upper:
        return {action: "NONE" for action in permissions}
    if "PERMISSIONS FULL" in upper or " PERMISSIONS" not in upper:
        return permissions

    matches = _re.findall(
        r"FOR\s+(select|create|update|delete)\s+WHERE\s+(.+?)(?=\s+FOR\s+(?:select|create|update|delete)\b|;|$)",
        table_definition,
        flags=_re.IGNORECASE | _re.DOTALL,
    )
    for action, clause in matches:
        permissions[action.lower()] = " ".join(clause.strip().split())
    return permissions


def _table_type(table_definition: str) -> str:
    return "relation" if "TYPE RELATION" in table_definition.upper() else "normal"


def _schema_mode(table_definition: str) -> str | None:
    upper = table_definition.upper()
    if "SCHEMAFULL" in upper:
        return "schemafull"
    if "SCHEMALESS" in upper:
        return "schemaless"
    return None


def _build_table_record(name: str, table_definition: Any, table_info: Any) -> dict[str, Any]:
    table_def = _definition_text(table_definition)
    fields = [_parse_field(field_name, field_def) for field_name, field_def in sorted(_section_data(table_info, "fields", "fd").items())]
    indexes = [_parse_index(index_name, index_def) for index_name, index_def in sorted(_section_data(table_info, "indexes", "ix").items())]
    events = [
        {"name": event_name, "definition": _definition_text(event_def)}
        for event_name, event_def in sorted(_section_data(table_info, "events", "ev").items())
    ]
    accesses = [
        {"name": access_name, "definition": _definition_text(access_def)}
        for access_name, access_def in sorted(_section_data(table_info, "accesses", "ac").items())
    ]
    return {
        "name": name,
        "type": _table_type(table_def),
        "schema_mode": _schema_mode(table_def),
        "definition": table_def,
        "fields": fields,
        "indexes": indexes,
        "events": events,
        "accesses": accesses,
        "permissions": _parse_permissions(table_def),
    }


def _load_connection(args: argparse.Namespace) -> tuple[str, str, str, str, str]:
    ep = args.endpoint or _env("SURREAL_ENDPOINT") or DEFAULT_ENDPOINT
    user = args.user or _env("SURREAL_USER") or "root"
    password = args.password or _env("SURREAL_PASS") or "root"
    ns = args.ns or _env("SURREAL_NS") or "test"
    db = args.db or _env("SURREAL_DB") or "test"
    return ep, user, password, ns, db


def _load_schema(ep: str, user: str, password: str, ns: str, db: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    db_info_raw = run_query(ep, user, password, ns, db, "INFO FOR DB")
    normalized = _normalize_db_info(_extract_result(db_info_raw))
    tables: list[dict[str, Any]] = []
    for table_name, table_definition in sorted(normalized.get("tables", {}).items()):
        table_info = _extract_result(
            run_query(ep, user, password, ns, db, f"INFO FOR TABLE {_sanitize_identifier(table_name)}")
        )
        tables.append(_build_table_record(table_name, table_definition, table_info))
    return normalized, tables


# ---------------------------------------------------------------------------
# export subcommand
# ---------------------------------------------------------------------------

def cmd_export(args: argparse.Namespace) -> None:
    """Export the complete database schema as SurrealQL DEFINE statements."""
    ep = args.endpoint or _env("SURREAL_ENDPOINT") or DEFAULT_ENDPOINT
    user = args.user or _env("SURREAL_USER") or "root"
    password = args.password or _env("SURREAL_PASS") or "root"
    ns = args.ns or _env("SURREAL_NS") or "test"
    db = args.db or _env("SURREAL_DB") or "test"

    stderr_console.print(f"Exporting schema from {ep} / {ns} / {db} ...")

    try:
        db_info_raw = run_query(ep, user, password, ns, db, "INFO FOR DB")
    except Exception as exc:
        stderr_console.print(f"[red]Failed to query database:[/red] {exc}")
        print(json.dumps({"error": str(exc)}))
        sys.exit(1)

    db_info = _extract_result(db_info_raw)
    statements: list[str] = []

    # Header
    statements.append(f"-- Schema export for namespace: {ns}, database: {db}")
    statements.append(f"-- Endpoint: {ep}")
    statements.append("")

    if not isinstance(db_info, dict):
        stderr_console.print("[yellow]Unexpected INFO FOR DB format. Dumping raw result.[/yellow]")
        raw_str = json.dumps(db_info_raw, indent=2, default=str)
        statements.append(f"-- Raw INFO FOR DB:\n-- {raw_str}")
        _output_schema(statements, args)
        return

    # Iterate over known schema categories
    category_order = ["accesses", "analyzers", "functions", "models", "params", "tables", "users"]
    # Some versions use shorthand keys
    key_aliases = {"ac": "accesses", "az": "analyzers", "fn": "functions", "ml": "models",
                   "pa": "params", "tb": "tables", "us": "users"}

    normalized: dict[str, dict] = {}
    for k, v in db_info.items():
        canon = key_aliases.get(k, k)
        if isinstance(v, dict):
            normalized[canon] = v

    for category in category_order:
        items = normalized.get(category, {})
        if not items:
            continue
        statements.append(f"-- {category.upper()}")
        for name, definition in sorted(items.items()):
            if isinstance(definition, str):
                stmt = definition.rstrip(";") + ";"
                statements.append(stmt)
            else:
                statements.append(f"-- {name}: {json.dumps(definition, default=str)}")
        statements.append("")

    # Per-table detail
    tables = normalized.get("tables", {})
    for tbl_name in sorted(tables.keys()):
        statements.append(f"-- TABLE: {tbl_name}")
        try:
            tbl_info_raw = run_query(ep, user, password, ns, db, f"INFO FOR TABLE {_sanitize_identifier(tbl_name)}")
            tbl_info = _extract_result(tbl_info_raw)
            if isinstance(tbl_info, dict):
                for section_key in ("fields", "fd", "indexes", "ix", "events", "ev", "lives", "lv"):
                    section = tbl_info.get(section_key)
                    if isinstance(section, dict) and section:
                        for item_name, item_def in sorted(section.items()):
                            if isinstance(item_def, str):
                                statements.append(item_def.rstrip(";") + ";")
                            else:
                                statements.append(f"-- {item_name}: {json.dumps(item_def, default=str)}")
            else:
                statements.append(f"-- (raw) {json.dumps(tbl_info, default=str)}")
        except Exception as exc:
            statements.append(f"-- Error fetching table info: {exc}")
        statements.append("")

    _output_schema(statements, args)


def _output_schema(statements: list[str], args: argparse.Namespace) -> None:
    """Write schema to stderr (pretty), stdout (JSON), and optionally to a file."""
    schema_text = "\n".join(statements)

    # Rich syntax highlighting on stderr
    stderr_console.print(Syntax(schema_text, "sql", theme="monokai", line_numbers=True))

    # Machine-readable JSON on stdout
    output = {"schema": schema_text, "line_count": len(statements)}

    if hasattr(args, "output_dir") and args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "schema.surql"
        out_file.write_text(schema_text)
        stderr_console.print(f"Schema written to {out_file}")
        output["file"] = str(out_file)

    print(json.dumps(output, indent=2))


# ---------------------------------------------------------------------------
# introspect subcommands
# ---------------------------------------------------------------------------

def cmd_introspect(args: argparse.Namespace) -> None:
    """Emit a structured full-schema dump."""
    ep, user, password, ns, db = _load_connection(args)
    stderr_console.print(f"Introspecting schema on {ep} / {ns} / {db} ...")

    try:
        normalized, tables = _load_schema(ep, user, password, ns, db)
    except Exception as exc:
        stderr_console.print(f"[red]Failed:[/red] {exc}")
        print(json.dumps({"error": str(exc)}))
        sys.exit(1)

    summary = Table(title="Schema Summary", show_lines=True)
    summary.add_column("Metric", style="bold")
    summary.add_column("Value")
    summary.add_row("Namespace", ns)
    summary.add_row("Database", db)
    summary.add_row("Tables", str(len(tables)))
    summary.add_row("Fields", str(sum(len(table["fields"]) for table in tables)))
    summary.add_row("Indexes", str(sum(len(table["indexes"]) for table in tables)))
    stderr_console.print(summary)

    tree = Tree(f"[bold]Database: {ns}/{db}[/bold]")
    for table in tables:
        branch = tree.add(f"[cyan]{table['name']}[/cyan] ({table['type']}, {table['schema_mode'] or 'unspecified'})")
        if table["fields"]:
            field_branch = branch.add("[yellow]fields[/yellow]")
            for field in table["fields"]:
                field_branch.add(f"{field['name']}: {field.get('type') or 'unknown'}")
        if table["indexes"]:
            index_branch = branch.add("[yellow]indexes[/yellow]")
            for index in table["indexes"]:
                index_branch.add(
                    f"{index['name']}: fields={', '.join(index['fields']) or '-'} "
                    f"unique={index['unique']} search={index['search']} vector={index['vector']}"
                )
    stderr_console.print(tree)

    output = {
        "namespace": ns,
        "database": db,
        "tables": tables,
        "accesses": sorted(normalized.get("accesses", {}).keys()),
        "users": sorted(normalized.get("users", {}).keys()),
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_tables(args: argparse.Namespace) -> None:
    """Emit a table summary only."""
    ep, user, password, ns, db = _load_connection(args)
    stderr_console.print(f"Listing tables on {ep} / {ns} / {db} ...")
    try:
        _, tables = _load_schema(ep, user, password, ns, db)
    except Exception as exc:
        stderr_console.print(f"[red]Failed:[/red] {exc}")
        print(json.dumps({"error": str(exc)}))
        sys.exit(1)

    summary_rows = [
        {
            "name": table["name"],
            "type": table["type"],
            "fields": len(table["fields"]),
            "indexes": len(table["indexes"]),
            "events": len(table["events"]),
        }
        for table in tables
    ]

    table_view = Table(title="Tables", show_lines=True)
    table_view.add_column("Table", style="bold")
    table_view.add_column("Type")
    table_view.add_column("Fields")
    table_view.add_column("Indexes")
    table_view.add_column("Events")
    for row in summary_rows:
        table_view.add_row(row["name"], row["type"], str(row["fields"]), str(row["indexes"]), str(row["events"]))
    stderr_console.print(table_view)
    print(json.dumps({"tables": summary_rows}, indent=2, default=str))


def cmd_table(args: argparse.Namespace) -> None:
    """Emit detailed information for one table."""
    ep, user, password, ns, db = _load_connection(args)
    table_name = _sanitize_identifier(args.name)
    stderr_console.print(f"Inspecting table {table_name} on {ep} / {ns} / {db} ...")
    try:
        normalized, tables = _load_schema(ep, user, password, ns, db)
    except Exception as exc:
        stderr_console.print(f"[red]Failed:[/red] {exc}")
        print(json.dumps({"error": str(exc)}))
        sys.exit(1)

    table = next((item for item in tables if item["name"] == table_name), None)
    if table is None:
        stderr_console.print(f"[red]Table not found:[/red] {table_name}")
        print(json.dumps({"error": f"Table not found: {table_name}", "available_tables": [item['name'] for item in tables]}, indent=2))
        sys.exit(1)

    detail = Tree(f"[bold]{table['name']}[/bold]")
    detail.add(f"type: {table['type']}")
    detail.add(f"schema_mode: {table['schema_mode'] or 'unspecified'}")
    if table["fields"]:
        fields = detail.add("[yellow]fields[/yellow]")
        for field in table["fields"]:
            fields.add(f"{field['name']}: {field.get('type') or 'unknown'}")
    if table["indexes"]:
        indexes = detail.add("[yellow]indexes[/yellow]")
        for index in table["indexes"]:
            indexes.add(
                f"{index['name']}: fields={', '.join(index['fields']) or '-'} "
                f"unique={index['unique']} search={index['search']} vector={index['vector']}"
            )
    stderr_console.print(detail)
    print(json.dumps({"namespace": ns, "database": db, "table": table, "accesses": sorted(normalized.get("accesses", {}).keys())}, indent=2, default=str))


def cmd_inspect(args: argparse.Namespace) -> None:
    """Legacy alias for older callers."""
    cmd_introspect(args)


# ---------------------------------------------------------------------------
# diff subcommand
# ---------------------------------------------------------------------------

def cmd_diff(args: argparse.Namespace) -> None:
    """Compare two SurrealQL schema files."""
    file1 = Path(args.file1)
    file2 = Path(args.file2)

    if not file1.exists():
        stderr_console.print(f"[red]File not found:[/red] {file1}")
        print(json.dumps({"error": f"File not found: {file1}"}))
        sys.exit(1)
    if not file2.exists():
        stderr_console.print(f"[red]File not found:[/red] {file2}")
        print(json.dumps({"error": f"File not found: {file2}"}))
        sys.exit(1)

    lines1 = file1.read_text().splitlines(keepends=True)
    lines2 = file2.read_text().splitlines(keepends=True)

    diff_lines = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=str(file1),
        tofile=str(file2),
        lineterm="",
    ))

    # Categorize changes
    additions = [l for l in diff_lines if l.startswith("+") and not l.startswith("+++")]
    removals = [l for l in diff_lines if l.startswith("-") and not l.startswith("---")]

    diff_text = "\n".join(diff_lines) if diff_lines else "(no differences)"

    # Rich output on stderr
    if diff_lines:
        stderr_console.print(Panel(f"Differences: {file1.name} vs {file2.name}", style="bold"))
        stderr_console.print(Syntax(diff_text, "diff", theme="monokai"))
        stderr_console.print(f"\n[green]+{len(additions)} additions[/green], [red]-{len(removals)} removals[/red]")
    else:
        stderr_console.print("[green]Schemas are identical.[/green]")

    # JSON on stdout
    output = {
        "file1": str(file1),
        "file2": str(file2),
        "identical": len(diff_lines) == 0,
        "additions": len(additions),
        "removals": len(removals),
        "diff": diff_text,
    }
    print(json.dumps(output, indent=2))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="schema",
        description="SurrealDB schema introspection and export tool.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Shared connection args
    def add_connection_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("--endpoint", type=str, default=None, help="SurrealDB endpoint (default: SURREAL_ENDPOINT or ws://localhost:8000)")
        p.add_argument("--user", type=str, default=None, help="Username (default: SURREAL_USER or root)")
        p.add_argument("--pass", dest="password", type=str, default=None, help="Password (default: SURREAL_PASS or root)")
        p.add_argument("--ns", type=str, default=None, help="Namespace (default: SURREAL_NS or test)")
        p.add_argument("--db", type=str, default=None, help="Database (default: SURREAL_DB or test)")

    # export
    export_parser = subparsers.add_parser("export", help="Export the complete schema as SurrealQL")
    add_connection_args(export_parser)
    export_parser.add_argument("--output-dir", type=str, default=None, help="Directory to write schema.surql file")

    introspect_parser = subparsers.add_parser("introspect", help="Full schema dump")
    add_connection_args(introspect_parser)

    tables_parser = subparsers.add_parser("tables", help="List tables with field/index/event counts")
    add_connection_args(tables_parser)

    table_parser = subparsers.add_parser("table", help="Inspect a single table in detail")
    add_connection_args(table_parser)
    table_parser.add_argument("name", type=str, help="Table name")

    # inspect (legacy alias)
    inspect_parser = subparsers.add_parser("inspect", help="Legacy alias for introspect")
    add_connection_args(inspect_parser)

    # diff
    diff_parser = subparsers.add_parser("diff", help="Compare two SurrealQL schema files")
    diff_parser.add_argument("--file1", type=str, required=True, help="First schema file")
    diff_parser.add_argument("--file2", type=str, required=True, help="Second schema file")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    dispatch = {
        "introspect": cmd_introspect,
        "tables": cmd_tables,
        "table": cmd_table,
        "export": cmd_export,
        "inspect": cmd_inspect,
        "diff": cmd_diff,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
