#!/usr/bin/env python3
"""Inspect database schema: tables, columns, indexes, foreign keys, triggers."""

import argparse, sqlite3, sys

def inspect_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get all tables
    c.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view') ORDER BY name")
    objects = c.fetchall()
    
    output = []
    output.append(f"Database: {db_path}")
    output.append(f"Objects: {len(objects)}")
    output.append("")
    
    for name, obj_type in objects:
        if obj_type == 'table':
            output.append(f"TABLE: {name}")
        else:
            output.append(f"VIEW: {name}")
        
        # Columns
        c.execute(f"PRAGMA table_info('{name}')")
        cols = c.fetchall()
        output.append(f"  Columns ({len(cols)}):")
        for col in cols:
            cid, cname, ctype, notnull, default, pk = col
            flags = []
            if pk: flags.append("PK")
            if notnull: flags.append("NOT NULL")
            flag_str = f" [{', '.join(flags)}]" if flags else ""
            default_str = f" default={default}" if default else ""
            output.append(f"    {cname:20s} {ctype:15s}{flag_str}{default_str}")
        
        # Indexes
        c.execute(f"PRAGMA index_list('{name}')")
        idxs = c.fetchall()
        if idxs:
            output.append(f"  Indexes ({len(idxs)}):")
            for idx in idxs:
                seq, iname, unique = idx[:3]
                c.execute(f"PRAGMA index_info('{iname}')")
                icols = [r[2] for r in c.fetchall()]
                u = "UNIQUE " if unique else ""
                output.append(f"    {iname:25s} ({', '.join(icols)}) [{u}]")
        
        # Foreign Keys
        c.execute(f"PRAGMA foreign_key_list('{name}')")
        fks = c.fetchall()
        if fks:
            output.append(f"  Foreign Keys:")
            for fk in fks:
                _, seq, ftable, fcol, pcol, *rest = fk
                output.append(f"    {name}.{fcol} -> {ftable}.{pcol}")
        
        # Triggers
        c.execute(f"SELECT name, sql FROM sqlite_master WHERE type='trigger' AND tbl_name='{name}'")
        triggers = c.fetchall()
        if triggers:
            output.append(f"  Triggers:")
            for tname, tsql in triggers:
                output.append(f"    {tname}")
        output.append("")
    
    conn.close()
    return '\n'.join(output)

def inspect_generic(conn_str):
    """Generic schema inspection using SQL standard queries."""
    import importlib
    if conn_str.startswith('postgresql://'):
        pg = importlib.import_module('psycopg2')
        conn = pg.connect(conn_str)
        output = [f"Connection: {conn_str}"]
        c = conn.cursor()
        c.execute("""
            SELECT table_schema, table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('pg_catalog','information_schema')
            ORDER BY table_schema, table_name
        """)
        tables = c.fetchall()
        output.append(f"Tables/Views: {len(tables)}")
        for schema, tname, ttype in tables:
            output.append(f"\n{ttype}: {schema}.{tname}")
            c.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema=%s AND table_name=%s
                ORDER BY ordinal_position
            """, (schema, tname))
            cols = c.fetchall()
            for col in cols:
                null_str = "" if col[2] == "YES" else " NOT NULL"
                default_str = f" default={col[3]}" if col[3] else ""
                output.append(f"  {col[0]:25s} {col[1]:20s}{null_str}{default_str}")
        conn.close()
        return '\n'.join(output)
    else:
        return "Generic inspection not yet supported for this database type."

def main():
    p = argparse.ArgumentParser(description='Inspect database schema')
    p.add_argument('--db', help='SQLite database file path')
    p.add_argument('--conn', help='SQLAlchemy connection string')
    args = p.parse_args()
    if not args.db and not args.conn:
        p.error("specify --db or --conn")
    
    if args.db:
        print(inspect_sqlite(args.db))
    else:
        print(inspect_generic(args.conn))

if __name__ == '__main__':
    main()
