#!/usr/bin/env python3
"""
SQL-Linker CLI - Command-line interface for database operations
Supports MySQL, PostgreSQL, SQLite with cloud audit sync

Usage:
    python main.py --help
    python main.py bootstrap
    python main.py query "SELECT * FROM users"
    python main.py insert users --data '{"name": "test", "email": "test@example.com"}'
    python main.py update users --data '{"status": "active"}' --where "id = 1"
    python main.py delete users --where "id = 1"
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add service_layer to path
SCRIPT_DIR = Path(__file__).parent
SKILL_ROOT = SCRIPT_DIR.parent.parent
WORKSPACE = SKILL_ROOT.parent.parent

sys.path.insert(0, str(SCRIPT_DIR))

from db_bridge import DBBridge, TableAccessDenied, SystemTableWriteDenied, BootstrapConfirmationRequired


def cmd_bootstrap(args):
    """Bootstrap configuration files."""
    print("[Security] ⚠️  Bootstrap creates config files in .sql_linker/ directory.")
    print("            set_env.ps1/sh generate encrypted credentials for OS environment.")
    print("            Run only in trusted environments.")
    print("")
    db = DBBridge(user_label="cli", session_id="bootstrap")
    preview = db.bootstrap(dry_run=True)
    print("\n[Preview] Files to be created:")
    for f in preview:
        print(f"  - {f}")

    if args.dry_run:
        print("\nDry-run mode. Run without --dry-run to create files.")
        return

    try:
        created = db.bootstrap(dry_run=False, explicit_confirm=True)
        print(f"\n[OK] Created {len(created)} files:")
        for f in created:
            print(f"  - {f}")
    except BootstrapConfirmationRequired:
        print("\n[ERROR] Bootstrap requires explicit confirmation.")
        print("Run: python main.py bootstrap --dry-run false")
    except Exception as e:
        print(f"\n[ERROR] Bootstrap failed: {e}")


def cmd_query(args):
    """Execute SELECT query."""
    print("[Security] ⚠️  The query command accepts arbitrary SQL (not limited to SELECT).")
    print("            Use parameterized queries (--params) to prevent injection attacks.")
    print("")
    db = DBBridge(user_label="cli", session_id="query", approved=getattr(args, 'approve', False))
    try:
        # Verify cloud API key if configured
        try:
            db.require_cloud_api_key()
        except PermissionError as e:
            print(f"[WARN] Cloud API key not configured: {e}")

        db.connect()

        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                sql = f.read()
        else:
            sql = args.sql

        params = None
        if args.params:
            params = tuple(json.loads(args.params))

        print(f"\n[Query] {sql[:100]}{'...' if len(sql) > 100 else ''}")
        if params:
            print(f"[Params] {params}")

        results = db.query(sql, params)

        if args.json:
            print(json.dumps(results, indent=2, default=str))
        else:
            print(f"\n[Results] {len(results)} rows")
            if results:
                # Print header
                headers = list(results[0].keys())
                print(" | ".join(headers))
                print("-" * (len(" | ".join(headers))))

                # Print rows (limit to 20)
                for row in results[:20]:
                    print(" | ".join(str(row.get(h, "")) for h in headers))

                if len(results) > 20:
                    print(f"... and {len(results) - 20} more rows")

    except TableAccessDenied as e:
        print(f"[ERROR] Access denied: {e}")
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")


def cmd_insert(args):
    """Insert record."""
    db = DBBridge(user_label="cli", session_id="insert", approved=getattr(args, 'approve', False))
    try:
        try:
            db.require_cloud_api_key()
        except PermissionError as e:
            print(f"[WARN] Cloud API key not configured: {e}")

        db.connect()

        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.loads(args.data)

        print(f"\n[Insert] {args.table}")
        print(f"[Data] {data}")

        row_id = db.insert(args.table, data)
        print(f"\n[OK] Inserted row ID: {row_id}")

    except TableAccessDenied as e:
        print(f"[ERROR] Access denied: {e}")
    except Exception as e:
        print(f"[ERROR] Insert failed: {e}")


def cmd_update(args):
    """Update records."""
    db = DBBridge(user_label="cli", session_id="update", approved=getattr(args, 'approve', False))
    try:
        try:
            db.require_cloud_api_key()
        except PermissionError as e:
            print(f"[WARN] Cloud API key not configured: {e}")

        db.connect()

        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.loads(args.data)

        params = None
        if args.params:
            params = tuple(json.loads(args.params))

        print(f"\n[Update] {args.table}")
        print(f"[Data] {data}")
        print(f"[Where] {args.where}")
        if params:
            print(f"[Params] {params}")

        rows = db.update(args.table, data, args.where, params)
        print(f"\n[OK] Updated {rows} rows")

    except TableAccessDenied as e:
        print(f"[ERROR] Access denied: {e}")
    except SystemTableWriteDenied as e:
        print(f"[ERROR] System table write denied: {e}")
    except Exception as e:
        print(f"[ERROR] Update failed: {e}")


def cmd_delete(args):
    """Delete records."""
    db = DBBridge(user_label="cli", session_id="delete", approved=getattr(args, 'approve', False))
    try:
        try:
            db.require_cloud_api_key()
        except PermissionError as e:
            print(f"[WARN] Cloud API key not configured: {e}")

        db.connect()

        params = None
        if args.params:
            params = tuple(json.loads(args.params))

        print(f"\n[Delete] {args.table}")
        print(f"[Where] {args.where}")
        if params:
            print(f"[Params] {params}")

        rows = db.delete(args.table, args.where, params)
        print(f"\n[OK] Deleted {rows} rows")

    except TableAccessDenied as e:
        print(f"[ERROR] Access denied: {e}")
    except SystemTableWriteDenied as e:
        print(f"[ERROR] System table write denied: {e}")
    except Exception as e:
        print(f"[ERROR] Delete failed: {e}")


def cmd_apikey_status(args):
    """Show current API key cloud status (no DB connection required)."""
    sys.path.insert(0, str(Path(__file__).parent))
    from sql_linker import SQLLinker
    linker = SQLLinker()
    try:
        info = linker.fetch_api_key_info()
        print("\n[API Key Status]")
        print(f"  status     : OK")
        print(f"  agent_name : {info.get('agent_name', '(none)')}")
        print(f"  key_name   : {info.get('key_name', '(none)')}")
        print(f"  key_id     : {info.get('id', '(none)')}")
        print(f"  key_masked : {info.get('key_masked', '(none)')}")
        print(f"  dbpw_key   : {info.get('dbpw_key', '(none)')}")
    except PermissionError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except ConnectionError as e:
        print(f"[ERROR] Cloud unreachable: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"[ERROR] Unexpected: {e}")
        sys.exit(3)


def cmd_config(args):
    """Show configuration."""
    from db_bridge import CONFIG_YAML, AUDIT_CONFIG, TABLE_DICT, EXTRA_TABLES

    print("\n[Configuration]")
    print(f"  Config: {CONFIG_YAML}")
    print(f"  Audit:  {AUDIT_CONFIG}")
    print(f"  Tables: {TABLE_DICT}")
    print(f"  Extra:  {EXTRA_TABLES}")

    # Load and show current config
    import yaml
    if CONFIG_YAML.exists():
        with open(CONFIG_YAML, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
        print("\n[DB Config]")
        for k, v in cfg.items():
            if k == "password" or "pw" in k.lower():
                print(f"  {k}: ********")
            else:
                print(f"  {k}: {v}")

    if AUDIT_CONFIG.exists():
        with open(AUDIT_CONFIG, 'r', encoding='utf-8') as f:
            audit = json.load(f)
        print("\n[Audit Config]")
        print(json.dumps(audit, indent=2, default=str))


def cmd_tables(args):
    """List available tables."""
    print("[Security] ⚠️  Tables listing exposes database structure (table names, fields).")
    print("            This aids reconnaissance — use only in trusted environments.")
    print("")
    db = DBBridge(user_label="cli", session_id="tables", approved=getattr(args, 'approve', False))

    print("\n[Normal Tables]")
    for t in db.tables():
        print(f"  - {t}")

    print("\n[Privileged Tables]")
    for t in db.extra_tables():
        print(f"  - {t}")

    print("\n[System Tables]")
    for t in db.system_tables():
        print(f"  - {t}")

    if args.table:
        fields = db.fields(args.table)
        if fields:
            print(f"\n[{args.table} Fields]")
            for f in fields:
                print(f"  - {f}")
        else:
            print(f"\n[INFO] No field info for '{args.table}' (privileged table?)")


def main():
    parser = argparse.ArgumentParser(
        description="SQL-Linker CLI - Database operations with cloud audit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py bootstrap
  python main.py query "SELECT * FROM users WHERE status = %s" --params '["active"]'
  python main.py insert users --data '{"name": "test", "email": "test@example.com"}'
  python main.py update users --data '{"status": "active"}' --where "id = 1"
  python main.py delete users --where "id = 1"
  python main.py tables
  python main.py tables --table users
  python main.py config
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # bootstrap
    p_bootstrap = subparsers.add_parser('bootstrap', help='Bootstrap configuration files')
    p_bootstrap.add_argument('--dry-run', dest='dry_run', nargs='?', const='false', default='true',
                             help='Dry-run mode (default: true)')

    # query
    p_query = subparsers.add_parser('query', help='Execute SELECT query')
    p_query.add_argument('sql', help='SQL query (use %s for params)')
    p_query.add_argument('--params', help='JSON array of params')
    p_query.add_argument('--file', help='Read SQL from file')
    p_query.add_argument('--json', action='store_true', help='Output as JSON')
    p_query.add_argument('--approve', action='store_true',
                         help='Explicitly approve credential access for this invocation')

    # insert
    p_insert = subparsers.add_parser('insert', help='Insert record')
    p_insert.add_argument('table', help='Table name')
    p_insert.add_argument('--data', help='JSON object of data')
    p_insert.add_argument('--file', help='Read data from JSON file')
    p_insert.add_argument('--approve', action='store_true',
                         help='Explicitly approve credential access for this invocation')

    # update
    p_update = subparsers.add_parser('update', help='Update records')
    p_update.add_argument('table', help='Table name')
    p_update.add_argument('--data', help='JSON object of data')
    p_update.add_argument('--file', help='Read data from JSON file')
    p_update.add_argument('--where', required=True, help='WHERE clause')
    p_update.add_argument('--params', help='JSON array of params')
    p_update.add_argument('--approve', action='store_true',
                         help='Explicitly approve credential access for this invocation')

    # delete
    p_delete = subparsers.add_parser('delete', help='Delete records')
    p_delete.add_argument('table', help='Table name')
    p_delete.add_argument('--where', required=True, help='WHERE clause')
    p_delete.add_argument('--params', help='JSON array of params')
    p_delete.add_argument('--approve', action='store_true',
                         help='Explicitly approve credential access for this invocation')

    # tables
    p_tables = subparsers.add_parser('tables', help='List available tables')
    p_tables.add_argument('--table', help='Show fields for specific table')
    p_tables.add_argument('--approve', action='store_true',
                          help='Explicitly approve credential access for this invocation')

    # config
    p_config = subparsers.add_parser('config', help='Show configuration')

    # apikey
    p_apikey = subparsers.add_parser('apikey', help='API key management')
    sub_apikey = p_apikey.add_subparsers(dest='apikey_command')
    sub_apikey.add_parser('status', help='Show current API key cloud status (no DB connection)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Route to command handlers
    if args.command == 'bootstrap':
        cmd_bootstrap(args)
    elif args.command == 'query':
        cmd_query(args)
    elif args.command == 'insert':
        cmd_insert(args)
    elif args.command == 'update':
        cmd_update(args)
    elif args.command == 'delete':
        cmd_delete(args)
    elif args.command == 'tables':
        cmd_tables(args)
    elif args.command == 'config':
        cmd_config(args)
    elif args.command == 'apikey':
        if getattr(args, 'apikey_command', None) == 'status':
            cmd_apikey_status(args)
        else:
            p_apikey.print_help()


if __name__ == '__main__':
    main()