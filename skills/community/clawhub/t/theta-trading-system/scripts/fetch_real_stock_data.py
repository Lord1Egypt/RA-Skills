#!/usr/bin/env python3
"""
真实数据获取与更新系统
- 从腾讯财经API获取A股实时数据
- 存储到本地数据库
- 支持增量更新
"""

import akshare as ak
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import time
import os

# 配置
DB_PATH = "/root/.openclaw/workspace/data/real_stock_data.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建股票日K线表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_daily (
            date TEXT,
            code TEXT,
            name TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            amount REAL,
            change_pct REAL,
            turnover_rate REAL,
            main_flow REAL,
            retail_flow REAL,
            created_at TEXT,
            PRIMARY KEY (date, code)
        )
    ''')
    
    # 创建涨停股表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS limit_up_stocks (
            date TEXT,
            code TEXT,
            name TEXT,
            close REAL,
            change_pct REAL,
            limit_time TEXT,
            turnover_rate REAL,
            main_flow REAL,
            amount REAL,
            continuous_days INTEGER,
            sector TEXT,
            created_at TEXT,
            PRIMARY KEY (date, code)
        )
    ''')
    
    # 创建数据更新记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS update_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_time TEXT,
            table_name TEXT,
            records_added INTEGER,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ 数据库初始化完成")

def fetch_real_time_stocks():
    """获取A股实时行情数据"""
    print("\n📊 获取A股实时行情数据...")
    
    try:
        # 使用AkShare获取实时行情
        df = ak.stock_zh_a_spot_em()
        
        print(f"✅ 获取到 {len(df)} 只股票实时数据")
        print(f"列: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return None

def fetch_limit_up_stocks():
    """获取涨停股数据"""
    print("\n📊 获取涨停股数据...")
    
    try:
        # 使用AkShare获取涨停股
        df = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
        
        print(f"✅ 获取到 {len(df)} 只涨停股")
        print(f"列: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return None

def save_to_database(df, table_name):
    """保存数据到数据库"""
    if df is None or len(df) == 0:
        print(f"⚠️ 无数据可保存")
        return 0
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取现有记录数
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    before_count = cursor.fetchone()[0]
    
    # 保存数据（如果存在则更新）
    today = datetime.now().strftime('%Y-%m-%d')
    saved_count = 0
    
    for idx, row in df.iterrows():
        try:
            if table_name == 'limit_up_stocks':
                cursor.execute('''
                    INSERT OR REPLACE INTO limit_up_stocks 
                    (date, code, name, close, change_pct, turnover_rate, main_flow, amount, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    today,
                    row.get('代码', row.get('code', '')),
                    row.get('名称', row.get('name', '')),
                    row.get('最新价', row.get('close', 0)),
                    row.get('涨跌幅', row.get('change_pct', 0)),
                    row.get('换手率', row.get('turnover_rate', 0)),
                    row.get('主力净流入', row.get('main_flow', 0)),
                    row.get('成交额', row.get('amount', 0)),
                    datetime.now().isoformat()
                ))
                saved_count += 1
        except Exception as e:
            print(f"  ⚠️ 保存失败: {e}")
            continue
    
    conn.commit()
    
    # 获取更新后记录数
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    after_count = cursor.fetchone()[0]
    
    # 记录更新日志
    cursor.execute('''
        INSERT INTO update_log (update_time, table_name, records_added, status)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().isoformat(), table_name, after_count - before_count, 'success'))
    
    conn.commit()
    conn.close()
    
    print(f"✅ 保存到数据库: {saved_count}条记录")
    
    return saved_count

def get_database_stats():
    """获取数据库统计信息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("📊 数据库统计信息")
    print("=" * 80)
    
    # 涨停股统计
    cursor.execute("SELECT COUNT(*) FROM limit_up_stocks")
    limit_up_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT date) FROM limit_up_stocks")
    limit_up_dates = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT code) FROM limit_up_stocks")
    limit_up_stocks = cursor.fetchone()[0]
    
    print(f"\n涨停股数据:")
    print(f"  总记录数: {limit_up_count}")
    print(f"  日期数: {limit_up_dates}")
    print(f"  股票数: {limit_up_stocks}")
    
    # 最新数据
    cursor.execute("""
        SELECT date, code, name, close, change_pct, main_flow, amount 
        FROM limit_up_stocks 
        ORDER BY date DESC, change_pct DESC 
        LIMIT 5
    """)
    latest = cursor.fetchall()
    
    print(f"\n最新5条涨停股:")
    for row in latest:
        print(f"  {row[0]} | {row[1]} {row[2]} | 价格:{row[3]} | 涨幅:{row[4]:.2f}% | 主力:{row[5]:.0f} | 成交额:{row[6]:.0f}")
    
    # 更新日志
    cursor.execute("SELECT * FROM update_log ORDER BY id DESC LIMIT 5")
    logs = cursor.fetchall()
    
    print(f"\n最近5次更新:")
    for log in logs:
        print(f"  {log[1]} | {log[2]} | +{log[3]}条 | {log[4]}")
    
    conn.close()

def main():
    """主函数"""
    print("=" * 80)
    print("🚀 真实数据获取与更新系统")
    print("=" * 80)
    
    # 初始化数据库
    init_database()
    
    # 获取涨停股数据
    df_limit_up = fetch_limit_up_stocks()
    
    # 保存到数据库
    if df_limit_up is not None:
        save_to_database(df_limit_up, 'limit_up_stocks')
    
    # 显示统计信息
    get_database_stats()
    
    print("\n" + "=" * 80)
    print("✅ 数据更新完成")
    print("=" * 80)

if __name__ == "__main__":
    main()
