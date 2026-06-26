#!/usr/bin/env python3
"""Export SQL query results to CSV, JSON, or SQL dump format."""

import argparse, csv, json, sqlite3, sys

def connect_db(db_path, conn_str):
    if db_path:
        return sqlite3.connect(db_path)
    print("Remote DB export not yet supported. Use --db for SQLite.")
    sys.exit(1)

def main():
    p = argparse.ArgumentParser(description='Export query results')
    p.add_argument('--db', help='SQLite database file path')
    p.add_argument('--conn', help='Connection string (future)')
    p.add_argument('--sql', required=True, help='SELECT query to export')
    p.add_argument('--output', '-o', required=True, help='Output file path')
    p.add_argument('--format', choices=['csv', 'json', 'sql'], help='Output format (auto-detected from extension)')
    args = p.parse_args()

    fmt = args.format
    if not fmt:
        if args.output.endswith('.csv'): fmt = 'csv'
        elif args.output.endswith('.json'): fmt = 'json'
        elif args.output.endswith('.sql'): fmt = 'sql'
        else: fmt = 'csv'

    conn = connect_db(args.db, args.conn)
    cursor = conn.cursor()
    try:
        cursor.execute(args.sql)
    except Exception as e:
        print(f"SQL Error: {e}")
        sys.exit(1)

    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description]

    if fmt == 'csv':
        with open(args.output, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)
    elif fmt == 'json':
        data = [dict(zip(cols, r)) for r in rows]
        with open(args.output, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    elif fmt == 'sql':
        # Get table name hint from query
        table_hint = 'exported_table'
        with open(args.output, 'w') as f:
            f.write(f"-- Exported {len(rows)} rows\n-- {args.sql}\n\n")
            for row in rows:
                vals = []
                for v in row:
                    if v is None:
                        vals.append('NULL')
                    elif isinstance(v, (int, float)):
                        vals.append(str(v))
                    else:
                        vals.append(repr(str(v)))
                f.write(f"INSERT INTO {table_hint} ({', '.join(cols)}) VALUES ({', '.join(vals)});\n")

    conn.close()
    print(f"Exported {len(rows)} rows to {args.output} ({fmt})")

if __name__ == '__main__':
    main()
