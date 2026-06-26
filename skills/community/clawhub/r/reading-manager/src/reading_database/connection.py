"""
数据库连接管理
"""
import sqlite3
import os
from pathlib import Path
from .schema import SCHEMAS, DEFAULT_CONFIG

DATA_DIR = Path.home() / ".config" / "reading-manager"
DB_PATH = DATA_DIR / "reading.db"


def init_data_dir():
    """初始化数据目录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    """获取数据库连接"""
    init_data_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """初始化数据库"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 创建表和索引
    for schema in SCHEMAS:
        # 分割多个 SQL 语句
        statements = [s.strip() for s in schema.split(';') if s.strip()]
        for stmt in statements:
            cursor.execute(stmt)
    
    # 插入默认配置
    for key, value, description in DEFAULT_CONFIG:
        cursor.execute(
            "INSERT OR IGNORE INTO config (key, value, description) VALUES (?, ?, ?)",
            (key, value, description)
        )
    
    conn.commit()
    conn.close()


def get_db_path():
    """获取数据库路径"""
    return str(DB_PATH)
