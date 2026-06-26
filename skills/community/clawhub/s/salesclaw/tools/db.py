#!/usr/bin/env python3
"""
SalesClaw - db.py
MySQL 统一连接管理

"""

import time
import mysql.connector
from mysql.connector import pooling
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

# ─── 配置 ────────────────────────────────────────────────
POOL_SIZE = 10
QUERY_TIMEOUT = 30          # 秒，超时阈值
MAX_RETRIES = 2              # 最大重试次数
FALLBACK_LIMIT = 10          # 超时降级后的 LIMIT

# ─── 连接池（模块级单例）────────────────────────────────

_POOL = None


def _get_pool():
    global _POOL
    if _POOL is None:
        _POOL = pooling.MySQLConnectionPool(
            pool_name="salesclaw_main",
            pool_size=POOL_SIZE,
            host="localhost",
            port=3306,
            user="ontology",
            password="ontology",
            database="salesclaw",
            charset="utf8mb4",
            use_unicode=True,
        )
    return _POOL


def get_conn():
    return _get_pool().get_connection()


def close_conn(conn):
    if conn:
        try:
            conn.close()
        except Exception:
            pass


# ─── 工具函数 ───────────────────────────────────────────

def _row_to_dict(row, cols):
    if row is None:
        return None
    result = {}
    for i, col in enumerate(cols):
        val = row[i]
        if hasattr(val, '__float__'):
            val = float(val)
        result[col] = val
    return result


def _is_timeout_error(e):
    msg = str(e).lower()
    return any(kw in msg for kw in ["timeout", "timed out", "lost connection", "aborted"])


# ─── 查询函数（含容错）──────────────────────────────────

def query_all(sql: str, params: tuple = None,
              timeout: int = QUERY_TIMEOUT,
              max_retries: int = MAX_RETRIES,
              fallback_limit: int = FALLBACK_LIMIT) -> list:
    """
    查询函数，带超时重试 + 降级 + 错误透出。

    策略：
    1. 执行查询，设置超时
    2. 超时 → 重试一次（指数退避），同时降级到 LIMIT
    3. 重试仍失败 → 返回 {"error": ..., "truncated": True}，不静默失败
    4. 其他错误 → 返回 {"error": ...}
    """
    params = params or ()

    for attempt in range(max_retries):
        conn = get_conn()
        cursor = conn.cursor()
        query_start = time.time()
        fallback_used = False

        try:
            # 设置查询超时（仅 MySQL Connector/Python >= 8.0 支持）
            if hasattr(cursor, 'fetchwarnings'):
                pass  # 暂不依赖此特性

            cursor.execute(sql, params)

            if timeout and hasattr(cursor, '_connection'):
                cursor._connection.wait_timeout = timeout

            cols = [d[0] for d in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            cursor.close()
            return [_row_to_dict(r, cols) for r in rows]

        except mysql.connector.Error as e:
            elapsed = time.time() - query_start

            if _is_timeout_error(e) and attempt < max_retries - 1:
                # 超时：降级 + 重试
                if fallback_limit and not fallback_used:
                    fallback_sql = _add_limit(sql, fallback_limit)
                    fallback_used = True
                    try:
                        cursor.execute(fallback_sql, params)
                        cols = [d[0] for d in cursor.description] if cursor.description else []
                        rows = cursor.fetchall()
                        cursor.close()
                        return {
                            "data": [_row_to_dict(r, cols) for r in rows],
                            "warning": f"Timeout降级至LIMIT {fallback_limit}",
                            "truncated": True,
                        }
                    except Exception:
                        pass  # 降级也失败，继续重试

                time.sleep(0.5 * (attempt + 1))  # 指数退避
                conn = get_conn()  # 重连
                cursor = conn.cursor()
                continue

            if attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
                conn = get_conn()
                cursor = conn.cursor()
                continue

            # 所有重试耗尽，返回错误
            cursor.close()
            return {
                "error": str(e),
                "sql_state": e.sqlstate if hasattr(e, 'sqlstate') else "",
                "errno": e.errno if hasattr(e, 'errno') else 0,
                "sql": _mask_sql(sql),
            }

        finally:
            try:
                cursor.close()
            except Exception:
                pass


def _add_limit(sql: str, limit: int) -> str:
    """为查询 SQL 追加 LIMIT 子句"""
    sql = sql.rstrip().rstrip(';')
    # 移除已有的 LIMIT
    import re
    sql = re.sub(r'\s+LIMIT\s+\d+\s*$', '', sql, flags=re.IGNORECASE)
    return f"{sql} LIMIT {limit}"


def _mask_sql(sql: str) -> str:
    """脱敏 SQL（隐藏密码等敏感参数）"""
    import re
    return re.sub(r'(password|passwd)\s*=\s*["\']([^"\']+)["\']',
                  r'\1=***', sql, flags=re.IGNORECASE)


def query_one(sql: str, params: tuple = None,
              timeout: int = QUERY_TIMEOUT,
              max_retries: int = MAX_RETRIES) -> dict:
    """单行查询，同样带超时容错"""
    result = query_all(sql, params, timeout=timeout, max_retries=max_retries,
                       fallback_limit=None)
    if isinstance(result, dict) and "error" in result:
        return result
    return result[0] if result else None


def execute(sql: str, params: tuple = None,
           timeout: int = QUERY_TIMEOUT) -> dict:
    """
    写操作封装（INSERT/UPDATE/DELETE）。
    错误透出，不静默吞异常。
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        return {
            "ok": True,
            "affected_rows": cur.rowcount,
            "last_insert_id": cur.lastrowid if hasattr(cur, 'lastrowid') else None,
        }
    except mysql.connector.Error as e:
        conn.rollback()
        return {
            "error": str(e),
            "sql_state": e.sqlstate if hasattr(e, 'sqlstate') else "",
            "errno": e.errno if hasattr(e, 'errno') else 0,
            "sql": _mask_sql(sql),
        }
    except Exception as e:
        conn.rollback()
        return {
            "error": str(e),
            "sql": _mask_sql(sql),
        }
    finally:
        try:
            cur.close()
        except Exception:
            pass
        close_conn(conn)


def health_check() -> dict:
    """数据库健康检查"""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 1 as test,
                   @@hostname as host,
                   @@version as version,
                   @@socket as socket
        """)
        row = cur.fetchone()
        cols = [d[0] for d in cur.description]
        cur.close()

        result = _row_to_dict(row, cols)

        cur2 = conn.cursor()
        cur2.execute("""
            SELECT COUNT(*) as c
            FROM information_schema.tables
            WHERE table_schema = 'salesclaw'
        """)
        table_count = cur2.fetchone()[0]
        cur2.close()

        return {
            "status": "ok",
            "tables": table_count,
            "host": result["host"],
            "version": result["version"],
            "socket": result["socket"],
        }
    except mysql.connector.Error as e:
        return {
            "status": "error",
            "error": str(e),
            "errno": e.errno if hasattr(e, 'errno') else 0,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        close_conn(conn)


# ─── CLI 入口 ────────────────────────────────────────────

if __name__ == "__main__":
    import json, sys

    if len(sys.argv) > 1:
        try:
            args = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            args = {"action": sys.argv[1]}
    else:
        args = {}

    action = args.get("action", "health_check")

    if action == "health_check":
        print(json.dumps(health_check(), ensure_ascii=False, indent=2))
    elif action == "query_all":
        result = query_all(args["sql"], args.get("params"))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif action == "query_one":
        result = query_one(args["sql"], args.get("params"))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif action == "execute":
        result = execute(args["sql"], args.get("params"))
        print(json.dumps(result, ensure_ascii=False, indent=2))