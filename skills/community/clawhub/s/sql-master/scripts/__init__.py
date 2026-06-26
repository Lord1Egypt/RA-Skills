# sql-master scripts module
# 包含: 数据库连接执行层 | 本地文件数据获取层 | SQL Pipeline 流水线

from .database_connector import (
    DatabaseConnector,
    QueryResult,
    connect_sqlite,
    connect_mysql,
    connect_postgresql,
    connect_mssql,
)
from .file_connector import (
    FileConnector,
    FileDataSource,
    load_file,
    load_directory,
    load_glob,
    load_dataframe,
    load_sqlite_file,
)
from .pipeline import (
    SQLPipeline,
    from_file,
    from_db,
    from_dataframe,
)

__all__ = [
    # 数据库连接
    'DatabaseConnector',
    'QueryResult',
    'connect_sqlite',
    'connect_mysql',
    'connect_postgresql',
    'connect_mssql',
    # 文件连接
    'FileConnector',
    'FileDataSource',
    'load_file',
    'load_directory',
    'load_glob',
    'load_dataframe',
    'load_sqlite_file',
    # Pipeline
    'SQLPipeline',
    'from_file',
    'from_db',
    'from_dataframe',
]
