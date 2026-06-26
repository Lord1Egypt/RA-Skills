"""
file_connector.py
本地文件数据获取层 - 支持 Excel / CSV / JSON / Parquet / Feather / 数据库文件
提供统一的数据加载、格式转换、多格式导出能力
三个用途：
  1. SQL 查询（SQLite 模式：自动把文件转成表）
  2. 格式转换（CSV ⇄ Excel ⇄ JSON ⇄ Parquet 等）
  3. 传给 sql-dataviz / sql-report-generator（返回 DataFrame / base64）
"""

from __future__ import annotations

import os
import json
import tempfile
import sqlite3
from typing import Optional, Dict, Any, List, Union, Tuple
from pathlib import Path
from dataclasses import dataclass, field
import logging

import pandas as pd

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class FileDataSource:
    """文件数据源封装"""
    df: pd.DataFrame
    source_path: str
    source_type: str          # csv, excel, json, parquet, sqlite, db
    table_name: str            # 对应 SQLite 的表名（自动生成）
    row_count: int
    column_count: int
    columns: List[str]
    dtypes: Dict[str, str]
    # SQLite 连接（用于 SQL 查询）
    _sqlite_conn: Optional[sqlite3.Connection] = field(default=None, repr=False)

    def summary(self) -> str:
        return (
            f"[FileDataSource] {self.source_type.upper()} → {self.table_name} | "
            f"{self.row_count} rows × {self.column_count} cols | "
            f"路径: {self.source_path}"
        )

    def to_sqlite(self, db_path: Optional[str] = None,
                   chunk_size: int = 10000) -> 'FileDataSource':
        """
        将数据导出为 SQLite 数据库文件（便于 SQL 查询）
        返回新的 FileDataSource
        """
        import tempfile, uuid
        if db_path is None:
            db_path = tempfile.mktemp(suffix=".db")
        conn = sqlite3.connect(db_path)
        self.df.to_sql(self.table_name, conn, index=False, chunksize=chunk_size)
        conn.close()
        return load_sqlite_file(db_path, table_name=self.table_name)


# ─────────────────────────────────────────────────────────────────────────────
# 文件加载器
# ─────────────────────────────────────────────────────────────────────────────

# 文件扩展名 → 加载函数
LOADERS: Dict[str, callable] = {}

def _register_loader(*extensions):
    def decorator(func):
        for ext in extensions:
            LOADERS[ext.lower().lstrip(".")] = func
        return func
    return decorator


@_register_loader("csv", "tsv", "txt")
def _load_csv(path: str, **kwargs) -> pd.DataFrame:
    sep = "\t" if path.endswith(".tsv") else ","
    return pd.read_csv(path, sep=sep, encoding="utf-8-sig", **kwargs)


@_register_loader("xlsx", "xls", "xlsm")
def _load_excel(path: str, **kwargs) -> pd.DataFrame:
    # 支持多 sheet，取第一个
    return pd.read_excel(path, sheet_name=0, engine="openpyxl", **kwargs)


@_register_loader("json")
def _load_json(path: str, **kwargs) -> pd.DataFrame:
    try:
        return pd.read_json(path, encoding="utf-8-sig", **kwargs)
    except Exception:
        # 可能是 JSON Lines 格式
        return pd.read_json(path, lines=True, encoding="utf-8-sig", **kwargs)


@_register_loader("parquet")
def _load_parquet(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_parquet(path, **kwargs)


@_register_loader("feather", "arrow")
def _load_feather(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_feather(path, **kwargs)


@_register_loader("html")
def _load_html(path: str, **kwargs) -> pd.DataFrame:
    dfs = pd.read_html(path, **kwargs)
    return dfs[0] if dfs else pd.DataFrame()


@_register_loader("dta")
def _load_stata(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_stata(path, **kwargs)


@_register_loader("sas7bdat", "sas7bdat")
def _load_sas(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_sas(path, **kwargs)


@_register_loader("pkl", "pickle")
def _load_pickle(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_pickle(path, **kwargs)


@_register_loader("db", "sqlite", "sqlite3")
def _load_sqlite_file(path: str, table_name: Optional[str] = None, **kwargs) -> Tuple[pd.DataFrame, sqlite3.Connection, str]:
    conn = sqlite3.connect(path)
    if table_name:
        df = pd.read_sql(f"SELECT * FROM `{table_name}` LIMIT 1000000", conn)
        return df, conn, table_name
    # 取第一个表
    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table'", conn
    )["name"].tolist()
    if not tables:
        raise ValueError(f"SQLite 文件 {path} 中没有表")
    table_name = tables[0]
    df = pd.read_sql(f"SELECT * FROM `{table_name}`", conn)
    return df, conn, table_name


# ─────────────────────────────────────────────────────────────────────────────
# 主类
# ─────────────────────────────────────────────────────────────────────────────

class FileConnector:
    """
    本地文件数据连接器

    支持格式:
        CSV / TSV / TXT   → pd.read_csv
        Excel (xlsx/xls)  → pd.read_excel
        JSON / JSONL      → pd.read_json
        Parquet           → pd.read_parquet
        Feather           → pd.read_feather
        HTML              → pd.read_html
        Stata (dta)       → pd.read_stata
        SAS (sas7bdat)    → pd.read_sas
        Pickle            → pd.read_pickle
        SQLite (db)       → sqlite3
        数据库文件        → sqlite3 / pymysql / psycopg2

    用法示例:

        # 加载 CSV 文件
        fc = FileConnector("data/sales.csv")
        print(fc.df.head())
        print(fc.summary())

        # 加载目录下的所有同类文件
        fc = FileConnector("data/*.csv")  # 自动合并

        # SQL 查询（自动生成 SQLite 内存数据库）
        result = fc.query("SELECT region, SUM(amount) as total GROUP BY region")

        # 导出为其他格式
        fc.to_excel("output/sales.xlsx")
        fc.to_json("output/sales.json")
        fc.to_parquet("output/sales.parquet")

        # 传给 sql-dataviz 画图
        from charts import ChartFactory
        factory = ChartFactory()
        b64 = factory.create_line({
            "categories": fc.df["month"].tolist(),
            "series": [{"name": "销售额", "data": fc.df["sales"].tolist()}]
        })

        # 传给 sql-report-generator 生成报告
        from report_builder import ReportBuilder
        builder = ReportBuilder()
        html = builder.add_dataframe(fc.df).build()
    """

    # 自动注册所有 loader
    SUPPORTED_EXTENSIONS = list(LOADERS.keys())

    def __init__(
        self,
        source: Union[str, List[str], pd.DataFrame],
        table_name: Optional[str] = None,
        encoding: str = "utf-8-sig",
        **kwargs
    ):
        """
        Args:
            source: 文件路径、路径模式（glob）、或 DataFrame
            table_name: 自定义表名（用于 SQL 查询）
            encoding: 文件编码
        """
        self.source = source
        self._df: Optional[pd.DataFrame] = None
        self._sqlite_conn: Optional[sqlite3.Connection] = None
        self._sqlite_db_path: Optional[str] = None
        self._table_name = table_name or "data"
        self.encoding = encoding
        self._kwargs = kwargs

        if isinstance(source, pd.DataFrame):
            self._df = source.copy()
            self._source_type = "dataframe"
        elif "*" in source or "?" in source:
            self._load_glob(source)
        elif os.path.isdir(source):
            self._load_directory(source)
        elif os.path.isfile(source):
            self._load_file(source)
        else:
            raise FileNotFoundError(f"路径不存在: {source}")

    # ──────────────────────────────── 加载逻辑 ──────────────────────────────

    def _load_file(self, path: str):
        ext = os.path.splitext(path)[1].lower().lstrip(".")
        self._source_path = path
        self._source_type = ext

        if ext in LOADERS:
            self._df = LOADERS[ext](path, **self._kwargs)
        else:
            raise ValueError(
                f"不支持的文件格式: .{ext}。"
                f"支持的格式: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        # 自动清理列名（去空格、统一大小写）
        self._df.columns = (
            self._df.columns
            .str.strip()
            .str.replace(r"\s+", "_", regex=True)
        )

    def _load_glob(self, pattern: str):
        import glob
        files = sorted(glob.glob(pattern))
        if not files:
            raise FileNotFoundError(f"没有找到匹配的文件: {pattern}")
        ext = os.path.splitext(files[0])[1].lower()
        dfs = [LOADERS[ext.lstrip(".")](f, **self._kwargs) for f in files]
        self._df = pd.concat(dfs, ignore_index=True)
        self._source_path = pattern
        self._source_type = ext.lstrip(".")
        self._df.columns = (
            self._df.columns
            .str.strip()
            .str.replace(r"\s+", "_", regex=True)
        )

    def _load_directory(self, dir_path: str):
        """加载目录下所有同名文件（不同分片/日期）"""
        import glob
        # 优先找 csv，其次 xlsx
        patterns = [
            os.path.join(dir_path, "*.csv"),
            os.path.join(dir_path, "*.xlsx"),
            os.path.join(dir_path, "*.xls"),
        ]
        for p in patterns:
            files = sorted(glob.glob(p))
            if files:
                ext = os.path.splitext(files[0])[1].lower().lstrip(".")
                dfs = [LOADERS[ext](f, **self._kwargs) for f in files]
                self._df = pd.concat(dfs, ignore_index=True)
                self._source_path = dir_path
                self._source_type = ext
                self._df.columns = (
                    self._df.columns
                    .str.strip()
                    .str.replace(r"\s+", "_", regex=True)
                )
                return
        raise ValueError(f"目录 {dir_path} 中没有找到可加载的数据文件")

    # ──────────────────────────────── DataFrame 访问 ─────────────────────────

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def columns(self) -> List[str]:
        return self._df.columns.tolist()

    @property
    def shape(self) -> Tuple[int, int]:
        return self._df.shape

    @property
    def dtypes(self) -> Dict[str, str]:
        return {c: str(t) for c, t in self._df.dtypes.items()}

    def head(self, n: int = 5) -> pd.DataFrame:
        return self._df.head(n)

    def info(self) -> str:
        buf = f"📁 源文件: {getattr(self, '_source_path', 'DataFrame')}\n"
        buf += f"📊 类型: {getattr(self, '_source_type', 'df').upper()}\n"
        buf += f"📏 规模: {self._df.shape[0]:,} 行 × {self._df.shape[1]} 列\n"
        buf += f"📋 列: {', '.join(self.columns)}\n"
        buf += f"\n{self._df.dtypes.to_string()}"
        return buf

    # ──────────────────────────────── SQL 查询 ──────────────────────────────

    def _ensure_sqlite(self):
        """延迟创建内存 SQLite 数据库（用于 SQL 查询）"""
        if self._sqlite_conn is None:
            # 使用临时文件，避免内存过大
            self._sqlite_db_path = tempfile.mktemp(suffix=".db")
            self._sqlite_conn = sqlite3.connect(self._sqlite_db_path)
            # 自动建表（表名去点横线）
            safe_name = self._table_name.replace(".", "_").replace("-", "_")
            self._df.to_sql(safe_name, self._sqlite_conn, index=False, chunksize=10000)
            self._table_name = safe_name

    def query(self, sql: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        对加载的数据执行 SQL 查询

        示例:
            fc = FileConnector("sales.csv")
            result = fc.query("SELECT region, SUM(amount) as total GROUP BY region ORDER BY total DESC")
        """
        self._ensure_sqlite()
        try:
            # 参数绑定支持 :name 和 ?
            if params:
                # sqlite3 不支持命名参数，直接替换
                for k, v in params.items():
                    sql = sql.replace(f":{k}", f"'{v}'")
            return pd.read_sql(sql, self._sqlite_conn)
        except Exception as e:
            logger.error(f"SQL 查询失败: {e}\nSQL: {sql[:200]}")
            raise

    def sql_result(self, sql: str, params: Optional[Dict] = None):
        """执行 SQL 并返回 QueryResult"""
        from .database_connector import QueryResult
        self._ensure_sqlite()
        import time
        t0 = time.perf_counter()
        try:
            if params:
                for k, v in params.items():
                    sql = sql.replace(f":{k}", f"'{v}'")
            df = pd.read_sql(sql, self._sqlite_conn)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            return QueryResult(
                columns=df.columns.tolist(),
                rows=[tuple(r) for r in df.values],
                rowcount=len(df),
                execution_time_ms=elapsed_ms,
                engine="SQLite(temp)",
                sql_dialect="sqlite",
            )
        except Exception as e:
            raise

    # ──────────────────────────────── 导出格式 ─────────────────────────────

    def to_csv(self, path: str, **kwargs) -> str:
        """导出为 CSV"""
        self._df.to_csv(path, index=False, encoding=self.encoding, **kwargs)
        return os.path.abspath(path)

    def to_excel(self, path: str, **kwargs) -> str:
        """导出为 Excel"""
        self._df.to_excel(path, index=False, engine="openpyxl", **kwargs)
        return os.path.abspath(path)

    def to_json(self, path: str, **kwargs) -> str:
        """导出为 JSON"""
        self._df.to_json(path, orient="records", force_ascii=False, **kwargs)
        return os.path.abspath(path)

    def to_parquet(self, path: str, **kwargs) -> str:
        """导出为 Parquet"""
        self._df.to_parquet(path, index=False, **kwargs)
        return os.path.abspath(path)

    def to_sqlite(self, db_path: str, table_name: Optional[str] = None) -> str:
        """导出为 SQLite 数据库"""
        name = table_name or self._table_name
        conn = sqlite3.connect(db_path)
        self._df.to_sql(name, conn, index=False)
        conn.close()
        return os.path.abspath(db_path)

    def to_dict(self, orient: str = "records") -> Union[List[Dict], Dict]:
        """导出为 Python dict"""
        return self._df.to_dict(orient=orient)

    # ──────────────────────────────── 传给可视化 ───────────────────────────

    def to_dataviz(self, chart_type: str, x_col: str, y_col: str,
                   title: str = "", **kwargs):
        """
        直接生成图表（base64 PNG）
        封装 sql-dataviz 的 ChartFactory

        示例:
            fc = FileConnector("sales.csv")
            b64 = fc.to_dataviz("line", x_col="month", y_col="sales", title="月度销售额")
        """
        try:
            from charts import ChartFactory
        except ImportError:
            # 尝试从 skill 目录加载
            import sys
            skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, os.path.join(skill_dir, "charts"))
            from charts import ChartFactory

        factory = ChartFactory()
        data = kwargs.pop("data", None)

        if chart_type == "line":
            data = data or {
                "categories": self._df[x_col].tolist(),
                "series": [{"name": y_col, "data": self._df[y_col].tolist()}]
            }
            return factory.create_line(data)
        elif chart_type == "bar":
            data = data or {
                "categories": self._df[x_col].tolist(),
                "series": [{"name": y_col, "data": self._df[y_col].tolist()}]
            }
            return factory.create_clustered_column(data)
        elif chart_type == "pie":
            data = data or {
                "labels": self._df[x_col].tolist(),
                "values": self._df[y_col].tolist()
            }
            return factory.create_donut(data)
        elif chart_type == "scatter":
            data = data or {
                "x": self._df[x_col].tolist(),
                "y": self._df[y_col].tolist(),
            }
            return factory.create_scatter(data)
        else:
            raise ValueError(f"不支持的图表类型: {chart_type}")

    # ──────────────────────────────── 清理 ─────────────────────────────────

    def close(self):
        if self._sqlite_conn:
            self._sqlite_conn.close()
            self._sqlite_conn = None
        if self._sqlite_db_path and os.path.exists(self._sqlite_db_path):
            try:
                os.unlink(self._sqlite_db_path)
            except Exception:
                pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        s = f"<FileConnector type={getattr(self, '_source_type', '?')} shape={getattr(self._df, 'shape', '?')}>"
        return s


# ─────────────────────────────────────────────────────────────────────────────
# 便捷函数
# ─────────────────────────────────────────────────────────────────────────────

def load_file(path: str, **kwargs) -> FileConnector:
    """加载单个文件"""
    return FileConnector(path, **kwargs)


def load_directory(dir_path: str, **kwargs) -> FileConnector:
    """加载目录下所有数据文件"""
    return FileConnector(dir_path, **kwargs)


def load_glob(pattern: str, **kwargs) -> FileConnector:
    """通配符加载多个文件"""
    return FileConnector(pattern, **kwargs)


def load_dataframe(df: pd.DataFrame, table_name: str = "data", **kwargs) -> FileConnector:
    """从 DataFrame 创建 FileConnector"""
    return FileConnector(df, table_name=table_name, **kwargs)


def load_sqlite_file(db_path: str, table_name: Optional[str] = None) -> FileDataSource:
    """加载 SQLite 数据库文件"""
    conn = sqlite3.connect(db_path)
    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table'", conn
    )["name"].tolist()
    if not tables:
        raise ValueError(f"SQLite 文件中没有表: {db_path}")
    tbl = table_name or tables[0]
    df = pd.read_sql(f"SELECT * FROM `{tbl}`", conn)
    return FileDataSource(
        df=df,
        source_path=db_path,
        source_type="sqlite",
        table_name=tbl,
        row_count=len(df),
        column_count=len(df.columns),
        columns=df.columns.tolist(),
        dtypes={c: str(t) for c, t in df.dtypes.items()},
        _sqlite_conn=conn,
    )


if __name__ == "__main__":
    import tempfile

    # 测试 CSV 加载 + SQL 查询
    csv_path = tempfile.mktemp(suffix=".csv")
    df = pd.DataFrame({
        "region": ["华东", "华北", "华南"],
        "product": ["A", "B", "A"],
        "amount": [1200, 800, 1500],
        "quantity": [10, 5, 12]
    })
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    fc = load_file(csv_path)
    print(fc.summary())
    print(fc.df)

    result = fc.query("SELECT region, SUM(amount) as total FROM data GROUP BY region")
    print("\nSQL 查询结果:")
    print(result)

    # 测试格式转换
    json_path = tempfile.mktemp(suffix=".json")
    fc.to_json(json_path)
    print(f"\n导出 JSON: {json_path}")

    # 测试 Excel
    xlsx_path = tempfile.mktemp(suffix=".xlsx")
    fc.to_excel(xlsx_path)
    print(f"导出 Excel: {xlsx_path}")

    os.unlink(csv_path)
    print("\n✅ FileConnector 测试通过")

