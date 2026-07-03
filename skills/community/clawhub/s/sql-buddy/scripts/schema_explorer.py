"""
Database Schema Explorer
- Discovers tables, columns, primary keys, foreign keys
- Infers column semantics from naming and data types
- Generates ER relationship overview
- Smart schema pruning for large databases
"""
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def _connect_sqlite(path: str):
    """Connect to a SQLite database."""
    import sqlite3
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def _connect_remote(config: Dict):
    """Connect to a remote database based on type."""
    db_type = config.get("type", "")
    
    if db_type == "postgresql":
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=config.get("host", "localhost"),
                port=config.get("port", 5432),
                dbname=config.get("database"),
                user=config.get("username"),
                password=config.get("password"),
                connect_timeout=10,
            )
            return conn
        except ImportError:
            logger.error("psycopg2 not installed. Install with: pip install psycopg2-binary")
            return None
    
    elif db_type == "mysql":
        try:
            import pymysql
            conn = pymysql.connect(
                host=config.get("host", "localhost"),
                port=config.get("port", 3306),
                database=config.get("database"),
                user=config.get("username"),
                password=config.get("password"),
                connect_timeout=10,
            )
            return conn
        except ImportError:
            logger.error("pymysql not installed. Install with: pip install pymysql")
            return None
    
    return None


def _get_db_connection(config: Dict):
    """Get a database connection."""
    db_type = config.get("type", "sqlite")
    
    if db_type == "sqlite":
        path = config.get("sqlite_path", config.get("database", ""))
        if not path:
            return None
        return _connect_sqlite(path)
    else:
        return _connect_remote(config)


def discover_schema(config: Dict, max_tables: int = 100) -> List[Dict]:
    """
    Discover database schema: tables, columns, PKs, FKs, and comments.
    
    Args:
        config: Database connection config.
        max_tables: Maximum tables to return (prevents context overflow).
        
    Returns:
        List of table schema dicts.
    """
    db_type = config.get("type", "sqlite")
    conn = _get_db_connection(config)
    
    if not conn:
        return []
    
    try:
        if db_type == "sqlite":
            return _discover_sqlite(conn, max_tables)
        elif db_type == "postgresql":
            return _discover_postgresql(conn, max_tables)
        elif db_type == "mysql":
            return _discover_mysql(conn, max_tables)
        else:
            logger.warning("Unsupported database type: %s", db_type)
            return []
    finally:
        try:
            conn.close()
        except Exception:
            pass


def _discover_sqlite(conn, max_tables: int) -> List[Dict]:
    """Discover SQLite schema."""
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()][:max_tables]
    
    schema = []
    for table_name in tables:
        # Get columns
        cursor.execute(f'PRAGMA table_info("{table_name}")')
        columns = []
        for row in cursor.fetchall():
            col = {
                "column_name": row[1],
                "type": row[2],
                "not_null": bool(row[3]),
                "default_value": row[4],
                "is_pk": bool(row[5]),
            }
            # Infer semantics from name
            col["semantic_hint"] = _infer_column_semantic(row[1], row[2])
            columns.append(col)
        
        # Get foreign keys
        cursor.execute(f'PRAGMA foreign_key_list("{table_name}")')
        foreign_keys = []
        for row in cursor.fetchall():
            foreign_keys.append({
                "column": row[3],
                "references_table": row[2],
                "references_column": row[4],
            })
        
        # Get indexes
        cursor.execute(f'PRAGMA index_list("{table_name}")')
        indexes = [{"name": row[1], "unique": bool(row[2])} for row in cursor.fetchall()]
        
        schema.append({
            "table_name": table_name,
            "columns": columns,
            "foreign_keys": foreign_keys,
            "indexes": indexes,
        })
    
    return schema


def _discover_postgresql(conn, max_tables: int) -> List[Dict]:
    """Discover PostgreSQL schema via information_schema."""
    cursor = conn.cursor()
    
    # Get tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name 
        LIMIT %s
    """, (max_tables,))
    tables = [row[0] for row in cursor.fetchall()]
    
    schema = []
    for table_name in tables:
        # Columns
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default, 
                   character_maximum_length
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        columns = []
        for row in cursor.fetchall():
            col = {
                "column_name": row[0],
                "type": row[1],
                "not_null": row[2] == "NO",
                "default_value": row[3],
                "max_length": row[4],
            }
            col["semantic_hint"] = _infer_column_semantic(row[0], row[1])
            columns.append(col)
        
        # Foreign keys
        cursor.execute("""
            SELECT kcu.column_name, ccu.table_name AS foreign_table_name, 
                   ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu 
                ON tc.constraint_name = ccu.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_schema = 'public' AND tc.table_name = %s
        """, (table_name,))
        foreign_keys = [
            {"column": r[0], "references_table": r[1], "references_column": r[2]}
            for r in cursor.fetchall()
        ]
        
        schema.append({
            "table_name": table_name,
            "columns": columns,
            "foreign_keys": foreign_keys,
            "indexes": [],
        })
    
    return schema


def _discover_mysql(conn, max_tables: int) -> List[Dict]:
    """Discover MySQL schema."""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = DATABASE() 
        ORDER BY table_name 
        LIMIT %s
    """, (max_tables,))
    tables = [row[0] for row in cursor.fetchall()]
    
    schema = []
    for table_name in tables:
        cursor.execute("""
            SELECT column_name, column_type, is_nullable, column_default,
                   column_comment
            FROM information_schema.columns 
            WHERE table_schema = DATABASE() AND table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        columns = []
        for row in cursor.fetchall():
            col = {
                "column_name": row[0],
                "type": row[1],
                "not_null": row[2] == "NO",
                "default_value": row[3],
                "comment": row[4],
            }
            col["semantic_hint"] = _infer_column_semantic(row[0], row[1])
            columns.append(col)
        
        schema.append({
            "table_name": table_name,
            "columns": columns,
            "foreign_keys": [],
            "indexes": [],
        })
    
    return schema


def _infer_column_semantic(column_name: str, data_type: str) -> str:
    """Infer the semantic meaning of a column from its name and type."""
    name_lower = column_name.lower()
    type_lower = data_type.lower()
    
    # ID fields
    if name_lower == "id":
        return "primary_key"
    if name_lower.endswith("_id") or name_lower.endswith("id"):
        return "foreign_key"
    
    # Temporal fields
    if any(kw in name_lower for kw in ["date", "time", "created", "updated", "timestamp"]):
        if "at" in name_lower or name_lower.endswith("date") or name_lower.endswith("time"):
            return "timestamp"
        return "date"
    
    # Status/type fields
    if name_lower.endswith("_status") or name_lower == "status":
        return "status_enum"
    if name_lower.endswith("_type") or name_lower == "type":
        return "type_enum"
    
    # Boolean fields
    if name_lower.startswith("is_") or name_lower.startswith("has_") or name_lower.startswith("can_") or name_lower.startswith("flag"):
        return "boolean_flag"
    
    # Numeric
    if any(kw in type_lower for kw in ["int", "float", "double", "decimal", "numeric"]):
        return "numeric_field"
    
    # Text
    if any(kw in type_lower for kw in ["char", "text", "varchar"]):
        return "text_field"
    
    # Email
    if "email" in name_lower:
        return "email_address"
    
    # Name
    if name_lower in ("name", "title", "caption", "label"):
        return "display_name"
    
    return "unknown"


def build_er_overview(schema: List[Dict]) -> str:
    """Build a human-readable ER relationship overview from schema."""
    if not schema:
        return "No tables found."
    
    lines = []
    table_names = [t["table_name"] for t in schema]
    
    for table in schema:
        name = table["table_name"]
        cols = table["columns"]
        fks = table.get("foreign_keys", [])
        
        # Column summary
        col_details = ", ".join(
            f"{c['column_name']} ({c['type']})"
            for c in cols[:8]  # Show first 8 columns
        )
        if len(cols) > 8:
            col_details += f"... +{len(cols) - 8} more"
        
        lines.append(f"- **{name}** ({len(cols)} cols)")
        lines.append(f"  - Columns: {col_details}")
        
        if fks:
            fk_str = ", ".join(
                f"{fk['column']} → {fk['references_table']}.{fk['references_column']}"
                for fk in fks
            )
            lines.append(f"  - References: {fk_str}")
    
    # Build relationship summary
    all_refs = []
    for table in schema:
        for fk in table.get("foreign_keys", []):
            all_refs.append((table["table_name"], fk["column"], 
                            fk["references_table"], fk["references_column"]))
    
    if all_refs:
        lines.append("\nRelationships:")
        for src, src_col, dst, dst_col in all_refs:
            lines.append(f"- {src}.{src_col} → {dst}.{dst_col}")
    
    return "\n".join(lines)


def trim_schema_for_query(schema: List[Dict], query: str, max_tables: int = 5) -> List[Dict]:
    """
    Smart schema pruning: keep only tables relevant to a query.
    
    Args:
        schema: Full schema list.
        query: The natural language query.
        max_tables: Max tables to keep.
        
    Returns:
        Pruned schema list sorted by relevance.
    """
    if len(schema) <= max_tables:
        return schema
    
    # Score each table by keyword overlap with the query
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    scored_tables = []
    for table in schema:
        score = 0
        table_lower = table["table_name"].lower()
        
        # Direct table name match
        if table_lower in query_lower:
            score += 100
        
        # Column name matches
        for col in table["columns"]:
            col_lower = col["column_name"].lower()
            if col_lower in query_lower:
                score += 10
            if col_lower in query_words:
                score += 5
        
        # Semantic matches
        for col in table["columns"]:
            hint = col.get("semantic_hint", "")
            if hint == "foreign_key":
                score += 2
        
        scored_tables.append((score, table))
    
    scored_tables.sort(key=lambda x: -x[0])
    return [t for _, t in scored_tables[:max_tables]]


def format_schema_for_prompt(schema: List[Dict]) -> str:
    """
    Format schema information for use in an LLM prompt.
    Only table names, column names, types, and comments are included (no actual data).
    """
    lines = ["Database Schema:", ""]
    
    for table in schema:
        lines.append(f"Table: {table['table_name']}")
        
        # Columns
        for col in table["columns"]:
            pk = "PK" if col.get("is_pk") else ""
            nullable = "NULL" if not col.get("not_null") else "NOT NULL"
            hint = col.get("semantic_hint", "")
            default = col.get("default_value", "")
            
            col_line = f"  - {col['column_name']} ({col.get('type', 'unknown')}) {nullable}"
            if pk:
                col_line += " [PK]"
            if default:
                col_line += f" default={default}"
            if hint and hint != "unknown":
                col_line += f" // {hint}"
            lines.append(col_line)
        
        # Foreign keys
        for fk in table.get("foreign_keys", []):
            lines.append(f"  - FK: {fk['column']} → {fk['references_table']}.{fk['references_column']}")
        
        # Indexes
        for idx in table.get("indexes", []):
            lines.append(f"  - INDEX: {idx.get('name', 'unnamed')}" + 
                        f"{' (UNIQUE)' if idx.get('unique') else ''}")
        
        lines.append("")
    
    return "\n".join(lines)
