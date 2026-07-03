"""
Safe SQL query executor.
- Read-only by default
- Uses parameterized queries
- Result preview (first N rows)
- Error handling
"""
import logging
from typing import Optional, Dict, List, Any

from security import is_read_only_query, mask_connection_string

logger = logging.getLogger(__name__)


class QueryResult:
    """Result of a SQL query execution."""
    
    def __init__(self, columns: list, rows: list, execution_time_ms: float,
                 rows_affected: int = 0, truncated: bool = False,
                 error: Optional[str] = None):
        self.columns = columns
        self.rows = rows
        self.execution_time_ms = execution_time_ms
        self.rows_affected = rows_affected
        self.truncated = truncated
        self.error = error
    
    def to_dict(self) -> Dict:
        return {
            "executed": self.error is None,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "rows_returned": len(self.rows),
            "rows_affected": self.rows_affected,
            "columns": self.columns,
            "results": self.rows[:20],
            "truncated": self.truncated,
            "error": self.error,
        }
    
    @property
    def row_count(self) -> int:
        return len(self.rows)
    
    @property
    def success(self) -> bool:
        return self.error is None


def execute_query(sql: str, config: Dict, limit: int = 20,
                  allow_write: bool = False) -> QueryResult:
    """
    Execute a SQL query safely.
    
    Args:
        sql: SQL statement to execute.
        config: Database connection config.
        limit: Max rows to return.
        allow_write: Allow write operations (default False).
        
    Returns:
        QueryResult with columns, rows, and metadata.
    """
    import time
    
    # Security: check if query is read-only
    if not allow_write and not security.is_read_only_query(sql):
        return QueryResult(
            columns=[],
            rows=[],
            execution_time_ms=0,
            error="Write operation blocked. Use --allow-write to enable INSERT/UPDATE/DELETE.",
        )
    
    db_type = config.get("type", "sqlite")
    
    start_time = time.time()
    
    try:
        if db_type == "sqlite":
            result = _execute_sqlite(sql, config, limit)
        elif db_type == "postgresql":
            result = _execute_postgresql(sql, config, limit)
        elif db_type == "mysql":
            result = _execute_mysql(sql, config, limit)
        else:
            return QueryResult(
                columns=[], rows=[], execution_time_ms=0,
                error=f"Unsupported database type: {db_type}",
            )
        
        elapsed = (time.time() - start_time) * 1000
        result.execution_time_ms = elapsed
        return result
        
    except Exception as e:
        elapsed = (time.time() - start_time) * 1000
        return QueryResult(
            columns=[], rows=[], execution_time_ms=elapsed,
            error=str(e),
        )


def _execute_sqlite(sql: str, config: Dict, limit: int) -> QueryResult:
    """Execute query on SQLite."""
    import sqlite3
    
    path = config.get("sqlite_path", config.get("database", ""))
    if not path:
        return QueryResult(columns=[], rows=[], execution_time_ms=0,
                          error="SQLite path not specified")
    
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        
        # For SELECT statements
        if sql.strip().upper().startswith("SELECT") or sql.strip().upper().startswith("WITH"):
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            raw_rows = cursor.fetchmany(limit + 1)
            truncated = len(raw_rows) > limit
            rows = [list(row) for row in raw_rows[:limit]]
            
            # Convert types for JSON serialization
            for row in rows:
                for i, val in enumerate(row):
                    if isinstance(val, bytes):
                        row[i] = val.hex()
                    elif isinstance(val, memoryview):
                        row[i] = val.tobytes().hex()
            
            return QueryResult(
                columns=columns,
                rows=rows,
                execution_time_ms=0,
                truncated=truncated,
            )
        else:
            # Non-SELECT (INSERT/UPDATE/DELETE)
            conn.commit()
            return QueryResult(
                columns=[],
                rows=[],
                execution_time_ms=0,
                rows_affected=cursor.rowcount,
            )
    finally:
        conn.close()


def _execute_postgresql(sql: str, config: Dict, limit: int) -> QueryResult:
    """Execute query on PostgreSQL."""
    try:
        import psycopg2
        import psycopg2.extras
        
        conn = psycopg2.connect(
            host=config.get("host", "localhost"),
            port=config.get("port", 5432),
            dbname=config.get("database"),
            user=config.get("username"),
            password=config.get("password"),
            connect_timeout=10,
        )
        
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            if config.get("readonly", True):
                conn.set_session(readonly=True)
            
            cursor.execute(sql)
            
            if cursor.description:
                columns = [desc.name for desc in cursor.description]
                raw_rows = cursor.fetchmany(limit + 1)
                truncated = len(raw_rows) > limit
                rows = [list(row.values()) for row in raw_rows[:limit]]
                
                return QueryResult(columns=columns, rows=rows, execution_time_ms=0, truncated=truncated)
            else:
                conn.commit()
                return QueryResult(columns=[], rows=[], execution_time_ms=0, rows_affected=cursor.rowcount)
        finally:
            conn.close()
    except ImportError:
        return QueryResult(columns=[], rows=[], execution_time_ms=0,
                          error="psycopg2 not installed. Install with: pip install psycopg2-binary")


def _execute_mysql(sql: str, config: Dict, limit: int) -> QueryResult:
    """Execute query on MySQL."""
    try:
        import pymysql
        
        conn = pymysql.connect(
            host=config.get("host", "localhost"),
            port=config.get("port", 3306),
            database=config.get("database"),
            user=config.get("username"),
            password=config.get("password"),
            connect_timeout=10,
            cursorclass=pymysql.cursors.DictCursor,
        )
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                raw_rows = cursor.fetchmany(limit + 1)
                truncated = len(raw_rows) > limit
                rows = []
                for row_dict in raw_rows[:limit]:
                    rows.append([row_dict.get(col) for col in columns])
                
                return QueryResult(columns=columns, rows=rows, execution_time_ms=0, truncated=truncated)
            else:
                conn.commit()
                return QueryResult(columns=[], rows=[], execution_time_ms=0, rows_affected=cursor.rowcount)
        finally:
            conn.close()
    except ImportError:
        return QueryResult(columns=[], rows=[], execution_time_ms=0,
                          error="pymysql not installed. Install with: pip install pymysql")


def explain_query(sql: str, config: Dict) -> Optional[Dict]:
    """
    Get the EXPLAIN plan for a SQL query.
    
    Args:
        sql: SQL statement to explain.
        config: Database connection config.
        
    Returns:
        EXPLAIN output as dict, or None on failure.
    """
    db_type = config.get("type", "sqlite")
    
    try:
        if db_type == "sqlite":
            return _explain_sqlite(sql, config)
        elif db_type == "postgresql":
            return _explain_postgresql(sql, config)
        elif db_type == "mysql":
            return _explain_mysql(sql, config)
    except Exception as e:
        logger.warning("EXPLAIN failed: %s", e)
        return None


def _explain_sqlite(sql: str, config: Dict) -> Dict:
    import sqlite3
    path = config.get("sqlite_path", config.get("database", ""))
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN QUERY PLAN {sql}")
        rows = cursor.fetchall()
        details = [{"select_id": r[0], "order": r[1], "detail": r[2]} for r in rows]
        return {"raw_plan": details}
    finally:
        conn.close()


def _explain_postgresql(sql: str, config: Dict) -> Dict:
    import psycopg2
    conn = psycopg2.connect(
        host=config.get("host", "localhost"),
        port=config.get("port", 5432),
        dbname=config.get("database"),
        user=config.get("username"),
        password=config.get("password"),
    )
    try:
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN (FORMAT JSON) {sql}")
        rows = cursor.fetchall()
        return {"raw_plan": rows}
    finally:
        conn.close()


def _explain_mysql(sql: str, config: Dict) -> Dict:
    import pymysql
    conn = pymysql.connect(
        host=config.get("host", "localhost"),
        port=config.get("port", 3306),
        database=config.get("database"),
        user=config.get("username"),
        password=config.get("password"),
    )
    try:
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN {sql}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return {"columns": columns, "rows": [dict(zip(columns, r)) for r in rows]}
    finally:
        conn.close()
