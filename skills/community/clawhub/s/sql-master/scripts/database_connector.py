"""
database_connector.py
数据库连接执行层 - 支持 SQLite / MySQL / PostgreSQL / SQL Server / ClickHouse / Oracle
提供统一的连接管理、SQL 执行、事务控制能力
"""

from __future__ import annotations

import sqlite3
import os
from typing import Optional, Dict, Any, List, Tuple, Union
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
import logging

import pandas as pd

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class QueryResult:
    """查询结果封装"""
    columns: List[str]
    rows: List[Tuple]
    rowcount: int
    execution_time_ms: float
    affected_rows: int = 0
    engine: str = ""
    sql_dialect: str = ""
    # DataFrame 形式（便捷访问）
    _df: Optional[pd.DataFrame] = field(default=None, repr=False)

    @property
    def df(self) -> pd.DataFrame:
        """lazy 加载 DataFrame"""
        if self._df is None:
            self._df = pd.DataFrame(self.rows, columns=self.columns)
        return self._df

    def to_dict(self, orient: str = "records") -> Union[List[Dict], Dict]:
        return self.df.to_dict(orient=orient)

    def to_csv(self, path: str, **kwargs) -> str:
        """导出为 CSV"""
        self.df.to_csv(path, index=False, **kwargs)
        return os.path.abspath(path)

    def to_excel(self, path: str, **kwargs) -> str:
        """导出为 Excel"""
        self.df.to_excel(path, index=False, engine='openpyxl', **kwargs)
        return os.path.abspath(path)

    def to_json(self, path: str, **kwargs) -> str:
        """导出为 JSON"""
        self.df.to_json(path, orient="records", force_ascii=False, **kwargs)
        return os.path.abspath(path)

    def summary(self) -> str:
        """返回可读摘要"""
        shape = self.df.shape
        dtypes = self.df.dtypes.value_counts().to_dict()
        return (
            f"[QueryResult] {shape[0]} rows × {shape[1]} cols | "
            f"执行: {self.execution_time_ms:.1f}ms | "
            f"引擎: {self.engine} | "
            f"列类型: {dtypes}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 连接管理器（支持多种数据库）
# ─────────────────────────────────────────────────────────────────────────────

class DatabaseConnector:
    """
    统一数据库连接器
    支持: SQLite, MySQL, PostgreSQL, SQL Server, ClickHouse, Oracle

    用法示例:
        # SQLite（本地文件）
        conn = DatabaseConnector(dialect="sqlite", database="data.db")
        result = conn.execute("SELECT * FROM users LIMIT 10")
        print(result.df)

        # MySQL
        conn = DatabaseConnector(
            dialect="mysql+pymysql",
            host="localhost", port=3306,
            username="root", password="xxx",
            database="mydb"
        )

        # PostgreSQL
        conn = DatabaseConnector(
            dialect="postgresql",
            host="localhost", port=5432,
            username="postgres", password="xxx",
            database="mydb"
        )

        # 文件路径（自动识别为 SQLite）
        conn = DatabaseConnector(dialect="sqlite", database="./data/my.db")
    """

    SUPPORTED_DIALECTS = {
        "sqlite": "sqlite:///{}",
        "sqlite3": "sqlite:///{}",
        "mysql+pymysql": "mysql+pymysql://{}:{}@{}:{}/{}",
        "postgresql": "postgresql://{}:{}@{}:{}/{}",
        "postgresql+psycopg2": "postgresql+psycopg2://{}:{}@{}:{}/{}",
        "mssql+pymssql": "mssql+pymssql://{}:{}@{}:{}/{}",
        "oracle+cx_oracle": "oracle+cx_oracle://{}:{}@{}:{}/{}",
        "clickhouse": "clickhouse://{}:{}@{}:{}/{}",
    }

    def __init__(
        self,
        dialect: str = "sqlite",
        database: Optional[str] = None,
        host: str = "localhost",
        port: int = 3306,
        username: str = "",
        password: str = "",
        filename: Optional[str] = None,   # SQLite 专用：直接传文件路径
        connection_string: Optional[str] = None,  # 完整连接字符串
        **kwargs
    ):
        self.dialect = dialect.lower()
        self.kwargs = kwargs
        self._engine = None
        self._connection = None

        # 如果传了文件路径，自动用 SQLite
        if filename or (database and self.dialect in ("sqlite", "sqlite3")):
            db_path = filename or database
            # 支持绝对路径和相对路径
            if not os.path.isabs(db_path):
                db_path = os.path.abspath(db_path)
            self._url = f"sqlite:///{db_path}"
            if not os.path.exists(os.path.dirname(db_path) or "."):
                os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        elif connection_string:
            self._url = connection_string
        else:
            template = self.SUPPORTED_DIALECTS.get(self.dialect, "")
            self._url = template.format(
                username, password, host, port, database
            )

    # ──────────────────────────────── 引擎管理 ──────────────────────────────

    def _get_engine(self):
        if self._engine is None:
            try:
                from sqlalchemy import create_engine
                self._engine = create_engine(
                    self._url,
                    pool_pre_ping=True,
                    echo=False,
                    **self.kwargs
                )
            except ImportError as e:
                logger.warning(f"SQLAlchemy 导入失败，降级为内置驱动: {e}")
                self._engine = None
        return self._engine

    def _get_connection(self):
        if self._connection is None:
            engine = self._get_engine()
            if engine is not None:
                self._connection = engine.connect()
            else:
                # 降级：使用内置 sqlite3
                if self.dialect in ("sqlite", "sqlite3"):
                    # 从 URL 提取路径: sqlite:///path/to/file.db
                    db_path = self._url.replace("sqlite:///", "").replace("sqlite:///", "")
                    self._connection = sqlite3.connect(db_path)
        return self._connection

    # ──────────────────────────────── 上下文管理器 ──────────────────────────

    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    # ──────────────────────────────── 执行接口 ──────────────────────────────

    def execute(
        self,
        sql: str,
        params: Optional[Dict] = None,
        timeout: int = 30
    ) -> QueryResult:
        """
        执行 SQL 查询，返回 QueryResult

        Args:
            sql: SQL 语句（支持 ? / %(name)s 占位符）
            params: 查询参数 dict
            timeout: 超时秒数

        Returns:
            QueryResult: 列名、行数据、执行时间等
        """
        import time
        t0 = time.perf_counter()

        conn = self._get_connection()
        engine = self._get_engine()

        try:
            if engine is not None:
                # SQLAlchemy 模式
                cursor = conn.execute(sql, params or {})
            else:
                # sqlite3 内置模式
                cursor = conn.execute(sql, params or {})

            # DDL / DML（CREATE/INSERT/UPDATE/DELETE）不返回行
            # 判断是否为写操作（DDL/DML 不返回行）
            try:
                has_result = cursor.returns_rows
            except AttributeError:
                has_result = getattr(cursor, 'description', None) is not None

            if not has_result:
                # 写操作：INSERT/UPDATE/DELETE/CREATE 等
                conn.commit() if hasattr(conn, 'commit') else None
                affected = cursor.rowcount if cursor.rowcount >= 0 else 0
                elapsed_ms = (time.perf_counter() - t0) * 1000
                return QueryResult(
                    columns=[],
                    rows=[],
                    rowcount=0,
                    execution_time_ms=elapsed_ms,
                    affected_rows=affected,
                    engine=type(engine).__name__ if engine else "sqlite3",
                    sql_dialect=self.dialect,
                )
            else:
                rows = cursor.fetchall()
                # 兼容 SQLAlchemy 1.x LegacyCursorResult 和标准 cursor.description
                try:
                    columns = list(cursor.keys())
                except (AttributeError, TypeError):
                    columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rowcount = cursor.rowcount
                affected = rowcount if rowcount >= 0 else 0
                elapsed_ms = (time.perf_counter() - t0) * 1000
                return QueryResult(
                    columns=columns,
                    rows=list(rows),
                    rowcount=len(rows),
                    execution_time_ms=elapsed_ms,
                    affected_rows=affected,
                    engine=type(engine).__name__ if engine else "sqlite3",
                    sql_dialect=self.dialect,
                )
        except Exception as e:
            elapsed_ms = (time.perf_counter() - t0) * 1000
            logger.error(f"SQL 执行失败 [{self.dialect}]: {e}\nSQL: {sql[:200]}")
            raise

    def execute_many(self, sql: str, batch: List[Dict]) -> int:
        """批量执行（INSERT/UPDATE）"""
        conn = self._get_connection()
        cursor = conn.cursor()
        for params in batch:
            cursor.execute(sql, params)
        conn.commit()
        return cursor.rowcount

    def get_tables(self) -> List[str]:
        """获取所有表名"""
        if self.dialect in ("sqlite", "sqlite3"):
            sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        elif self.dialect in ("mysql+pymysql", "mysql"):
            sql = "SHOW TABLES"
        elif "postgresql" in self.dialect:
            sql = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"
        elif "mssql" in self.dialect:
            sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
        else:
            sql = "SELECT table_name FROM information_schema.tables"
        return [r[0] for r in self.execute(sql).rows]

    def get_schema(self, table: str) -> pd.DataFrame:
        """获取表结构"""
        if self.dialect in ("sqlite", "sqlite3"):
            sql = f"PRAGMA table_info({table})"
        elif "postgresql" in self.dialect:
            sql = f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table}'
                ORDER BY ordinal_position
            """
        elif "mysql" in self.dialect:
            sql = f"DESCRIBE `{table}`"
        else:
            sql = f"""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table}'
            """
        return self.execute(sql).df

    def table_preview(self, table: str, limit: int = 5) -> pd.DataFrame:
        """预览表数据"""
        sql = f"SELECT * FROM `{table}` LIMIT {limit}"
        return self.execute(sql).df

    def close(self):
        """关闭连接"""
        if self._connection:
            self._connection.close()
            self._connection = None
        if self._engine:
            self._engine.dispose()
            self._engine = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return f"<DatabaseConnector dialect={self.dialect} url={self._url[:50]}>"


# ─────────────────────────────────────────────────────────────────────────────
# 便捷工厂函数
# ─────────────────────────────────────────────────────────────────────────────

def connect_sqlite(path: str, **kwargs) -> DatabaseConnector:
    """连接 SQLite 数据库"""
    return DatabaseConnector(dialect="sqlite", filename=path, **kwargs)


def connect_mysql(host="localhost", port=3306, username="root",
                   password="", database="", **kwargs) -> DatabaseConnector:
    """连接 MySQL"""
    return DatabaseConnector(
        dialect="mysql+pymysql", host=host, port=port,
        username=username, password=password, database=database, **kwargs
    )


def connect_postgresql(host="localhost", port=5432, username="postgres",
                       password="", database="", **kwargs) -> DatabaseConnector:
    """连接 PostgreSQL"""
    return DatabaseConnector(
        dialect="postgresql", host=host, port=port,
        username=username, password=password, database=database, **kwargs
    )


def connect_mssql(host="localhost", port=1433, username="sa",
                  password="", database="", **kwargs) -> DatabaseConnector:
    """连接 SQL Server"""
    return DatabaseConnector(
        dialect="mssql+pymssql", host=host, port=port,
        username=username, password=password, database=database, **kwargs
    )


if __name__ == "__main__":
    # 快速测试 - 创建内存 SQLite 并执行查询
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    conn = connect_sqlite(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            region TEXT, product TEXT,
            amount REAL, quantity INTEGER
        )
    """)
    conn.execute("""
        INSERT INTO sales (region, product, amount, quantity) VALUES
        ('华东', '产品A', 1200.5, 10),
        ('华北', '产品B', 800.0, 5),
        ('华南', '产品A', 1500.0, 12)
    """)

    result = conn.execute("SELECT * FROM sales WHERE amount > 1000")
    print(result.summary())
    print(result.df)

    os.unlink(db_path)
    print("SQLite 测试通过")
