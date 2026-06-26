#!/usr/bin/env python3
"""Execute SQL queries with formatted output."""

import argparse, csv, json, sqlite3, sys, os, textwrap
from datetime import datetime
from urllib.parse import urlparse

def connect_sqlite(path):
    return sqlite3.connect(path)

def connect_pg(conn_str):
    import importlib
    try:
        psycopg = importlib.import_module('psycopg2')
        return psycopg.connect(conn_str)
    except ImportError:
        print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
        sys.exit(1)

def connect_mysql(conn_str):
    import importlib
    try:
        pymysql = importlib.import_module('pymysql')
        return pymysql.connect(conn_str)
    except ImportError:
        print("ERROR: pymysql not installed. Install with: pip install pymysql")
        sys.exit(1)

def connect(conn_str, db_path):
    if db_path:
        return connect_sqlite(db_path)
    if conn_str.startswith('postgresql://'):
        return connect_pg(conn_str)
    if conn_str.startswith('mysql'):
        return connect_mysql(conn_str)
    if conn_str.startswith('sqlite:///'):
        return connect_sqlite(conn_str.replace('sqlite:///', ''))
    print("ERROR: Unsupported connection string. Use --db for SQLite or --conn for PostgreSQL/MySQL.")
    sys.exit(1)

def format_rows(rows, cols, fmt):
    if fmt == 'json':
        return json.dumps([dict(zip(cols, r)) for r in rows], indent=2)
    elif fmt == 'csv':
        out = [cols]
        out.extend(rows)
        return '\n'.join([','.join(str(c) for c in row) for row in out])
    else:  # table
        if not rows:
            return "(no results)"
        widths = [len(c) for c in cols]
        for row in rows:
            for i, v in enumerate(row):
                widths[i] = max(widths[i], len(str(v)))
        sep = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'
        header = '| ' + ' | '.join(c.ljust(w) for c, w in zip(cols, widths)) + ' |'
        lines = [sep, header, sep]
        for row in rows:
            lines.append('| ' + ' | '.join(str(v).ljust(w) for v, w in zip(row, widths)) + ' |')
        lines.append(sep)
        lines.append(f"({len(rows)} row{'s' if len(rows)!=1 else ''})")
        return '\n'.join(lines)

def main():
    p = argparse.ArgumentParser(description='Execute SQL queries with formatted output')
    p.add_argument('--db', help='SQLite database file path')
    p.add_argument('--conn', help='SQLAlchemy connection string')
    p.add_argument('--sql', required=True, help='SQL query to execute')
    p.add_argument('--format', choices=['table', 'json', 'csv'], default='table')
    p.add_argument('--verbose', action='store_true', help='Show execution time and row count')
    args = p.parse_args()

    if not args.db and not args.conn:
        p.error("specify --db (SQLite) or --conn (connection string)")

    import time
    start = time.time()
    conn = connect(args.conn, args.db)
    cursor = conn.cursor()
    try:
        cursor.execute(args.sql)
    except Exception as e:
        print(f"SQL Error: {e}")
        sys.exit(1)

    if args.sql.strip().upper().startswith(('SELECT', 'WITH', 'PRAGMA', 'EXPLAIN')):
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        print(format_rows(rows, cols, args.format))
        if args.verbose:
            elapsed = time.time() - start
            print(f"\n-- {len(rows)} rows in {elapsed:.3f}s")
    else:
        conn.commit()
        changed = cursor.rowcount
        if args.verbose:
            print(f"OK ({changed} row{'s' if changed != 1 else ''} affected)")

    conn.close()

if __name__ == '__main__':
    main()
