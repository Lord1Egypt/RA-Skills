#!/usr/bin/env python3
"""
SalesClaw MySQL 初始化工具
用法：
    python3 tools/init_mysql.py              # 初始化（首次）
    python3 tools/init_mysql.py --force      # 强制重建
    python3 tools/init_mysql.py --schema     # 仅建表结构
    python3 tools/init_mysql.py --check      # 检查状态
"""
import argparse, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from db import get_conn, close_conn, execute, query_all

SKILL_DIR = os.path.join(os.path.dirname(__file__), '..')
SCHEMA_FILE = os.path.join(SKILL_DIR, 'salesclaw_init.sql')
SEED_FILE = os.path.join(SKILL_DIR, 'salesclaw_seed_data.sql')


def count_tables():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'salesclaw' AND table_type = 'BASE TABLE'")
        n = cur.fetchone()[0]
        cur.close()
        return n
    finally:
        close_conn(conn)


def list_tables():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'salesclaw' AND table_type = 'BASE TABLE' ORDER BY table_name")
        rows = cur.fetchall()
        cur.close()
        return [r[0] for r in rows]
    finally:
        close_conn(conn)


def table_exists(table):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'salesclaw' AND table_name = %s", (table,))
        n = cur.fetchone()[0]
        cur.close()
        return n > 0
    finally:
        close_conn(conn)


def init_schema(verbose=False):
    """建表（仅结构，无数据）"""
    if not os.path.exists(SCHEMA_FILE):
        print(f"❌ Schema 文件不存在: {SCHEMA_FILE}")
        sys.exit(1)

    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        sql = f.read()

    # 逐条执行 CREATE TABLE（MySQL 不能一次 executescript 多语句）
    stmts = re.split(r';\s*\n', sql)
    executed = 0
    errors = []
    for stmt in stmts:
        stmt = stmt.strip()
        if not stmt:
            continue
        if not stmt.upper().startswith('CREATE TABLE'):
            continue
        try:
            execute(stmt)
            executed += 1
        except Exception as e:
            errors.append(f"{stmt[:60]}... → {e}")

    if errors and verbose:
        print(f"⚠️  {len(errors)} errors:")
        for e in errors:
            print(f"  {e}")

    return executed, len(errors)


def load_seed_data(verbose=False):
    """加载种子数据"""
    if not os.path.exists(SEED_FILE):
        print(f"❌ Seed 文件不存在: {SEED_FILE}")
        return 0, 0

    with open(SEED_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    total_rows = 0
    errors = 0

    # 按 "-- tablename" 分割块
    blocks = re.split(r'\n-- [\w_]+\n', content)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        try:
            conn = get_conn()
            cur = conn.cursor()
            # 多行 INSERT 可能用 \n 连接，需要还原
            cur.execute(block)
            conn.commit()
            # 统计 affected rows
            total_rows += cur.rowcount
            cur.close()
            close_conn(conn)
        except Exception as e:
            errors += 1
            if verbose:
                print(f"  ERROR: {e}")

    return total_rows, errors


def init_db(force=False, schema_only=False, verbose=False):
    if force:
        existing = count_tables()
        if existing > 0:
            print(f"⚠️  数据库已有 {existing} 张表，使用 --force 删除重建")
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute("DROP DATABASE IF EXISTS salesclaw")
                conn.commit()
                cur.close()
                print("🗑  已删除旧数据库")
            finally:
                close_conn(conn)

        # 重建库
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS salesclaw CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.commit()
            cur.close()
        finally:
            close_conn(conn)

    # 建表
    n_tables, n_errors = init_schema(verbose)
    print(f"✅ 建表完成: {n_tables} 张表" + (f", {n_errors} errors" if n_errors else ""))

    if not schema_only:
        n_rows, n_row_errors = load_seed_data(verbose)
        if n_row_errors == 0:
            print(f"✅ 种子数据加载完成: {n_rows} 行")
        else:
            print(f"⚠️  种子数据: {n_rows} 行, {n_row_errors} errors")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SalesClaw MySQL 初始化')
    parser.add_argument('--force', action='store_true', help='强制重建')
    parser.add_argument('--schema', action='store_true', help='仅建表结构（无数据）')
    parser.add_argument('--check', action='store_true', help='检查状态')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细信息')
    args = parser.parse_args()

    if args.check:
        n = count_tables()
        if n > 0:
            print(f"✅ salesclaw 数据库已初始化 ({n} 张表)")
            if args.verbose:
                for t in list_tables():
                    print(f"  • {t}")
        else:
            print("❌ salesclaw 数据库为空（尚未初始化）")
        sys.exit(0)

    init_db(force=args.force, schema_only=args.schema, verbose=args.verbose)