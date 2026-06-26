#!/usr/bin/env python3
"""
AI超脑 - 数据库初始化脚本
运行: python init_db.py [数据库路径]
默认路径: ./brain.db
"""

import sqlite3
import sys
import os

DEFAULT_DB_PATH = "brain.db"
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../references/schema.sql")

def init_database(db_path=DEFAULT_DB_PATH):
    """初始化超脑数据库"""
    
    # 检查数据库是否已存在
    if os.path.exists(db_path):
        print(f"⚠️  数据库已存在: {db_path}")
        response = input("是否重新初始化？(这将清空所有数据) [y/N]: ")
        if response.lower() != 'y':
            print("取消操作")
            return
        os.remove(db_path)
        print(f"🗑️  已删除旧数据库")
    
    # 创建目录
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 读取并执行Schema
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    cursor.executescript(schema)
    conn.commit()
    
    # 验证表创建
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    expected_tables = [
        'user_profile',
        'conversation_insights', 
        'response_patterns',
        'user_projects',
        'pending_reminders',
        'behavior_patterns',
        'super_brain_config'
    ]
    
    print(f"✅ 数据库初始化成功: {db_path}")
    print(f"📊 已创建 {len(tables)} 个表:")
    for table in expected_tables:
        status = "✓" if table in tables else "✗"
        print(f"  {status} {table}")
    
    # 显示配置
    cursor.execute("SELECT key, value FROM super_brain_config")
    configs = cursor.fetchall()
    print(f"\n⚙️  配置:")
    for key, value in configs:
        print(f"  {key}: {value}")
    
    conn.close()
    print(f"\n🚀 超脑已就绪！")

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB_PATH
    init_database(db_path)
