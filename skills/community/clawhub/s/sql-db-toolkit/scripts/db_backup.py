#!/usr/bin/env python3
"""Backup SQLite database or dump SQL for remote databases."""

import argparse, datetime, os, shutil, sqlite3, subprocess, sys

def backup_sqlite(db_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    base = os.path.splitext(os.path.basename(db_path))[0]
    
    # Binary copy
    backup_path = os.path.join(output_dir, f"{base}_{ts}.sqlite")
    shutil.copy2(db_path, backup_path)
    
    # SQL dump
    dump_path = os.path.join(output_dir, f"{base}_{ts}.sql")
    conn = sqlite3.connect(db_path)
    with open(dump_path, 'w') as f:
        for line in conn.iterdump():
            f.write(line + '\n')
    conn.close()
    
    size = os.path.getsize(backup_path)
    print(f"Backup created: {backup_path} ({size:,} bytes)")
    print(f"SQL dump: {dump_path}")
    return backup_path, dump_path

def main():
    p = argparse.ArgumentParser(description='Backup database')
    p.add_argument('--db', help='SQLite database file path')
    p.add_argument('--conn', help='Connection string (requires pg_dump/mysqldump)')
    p.add_argument('--output', '-o', default='./backups', help='Output directory')
    args = p.parse_args()
    
    if not args.db and not args.conn:
        p.error("specify --db or --conn")
    
    if args.db:
        backup_sqlite(args.db, args.output)
    else:
        print("Remote DB backup requires pg_dump/mysqldump CLI tools. Use --db for SQLite auto-backup.")

if __name__ == '__main__':
    main()
