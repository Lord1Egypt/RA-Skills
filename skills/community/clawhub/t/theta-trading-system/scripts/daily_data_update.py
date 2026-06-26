#!/usr/bin/env python3
"""
Theta系统 - 每日收盘后自动更新数据
功能：每日15:30自动获取当日涨停股数据并保存
"""

import akshare as ak
import sqlite3
from datetime import datetime
import os

DB_PATH = "/root/.openclaw/workspace/data/real_stock_data.db"
LOG_PATH = "/root/.openclaw/workspace/logs/daily_update.log"

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

def is_st_stock(code, name):
    """判断是否为ST股票"""
    if code.startswith('688') or code.startswith('300'):
        return True
    
    st_keywords = ['ST', '*ST', 'S*ST', 'SST', 'S', '退市', '暂停上市']
    for keyword in st_keywords:
        if keyword in name:
            return True
    
    return False

def main():
    log("=" * 80)
    log("📊 每日数据自动更新")
    log("=" * 80)
    
    today = datetime.now().strftime('%Y%m%d')
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    try:
        # 获取涨停股数据
        log(f"📊 获取 {today_str} 涨停股数据...")
        df = ak.stock_zt_pool_em(date=today)
        
        if df is None or len(df) == 0:
            log("  ⚠️ 无数据（可能是非交易日）")
            return
        
        log(f"  ✅ 获取到 {len(df)} 只涨停股")
        
        # 保存到数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        saved_count = 0
        filtered_count = 0
        
        for idx, row in df.iterrows():
            code = row['代码']
            name = row['名称']
            close = row.get('最新价', 0)
            amount = row.get('成交额', 0)
            
            # 过滤ST股票
            if is_st_stock(code, name):
                filtered_count += 1
                continue
            
            # 过滤异常数据
            if close <= 0 or amount <= 0:
                filtered_count += 1
                continue
            
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO limit_up_stocks 
                    (date, code, name, close, change_pct, turnover_rate, amount, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    today_str,
                    code,
                    name,
                    close,
                    row.get('涨跌幅', 0),
                    row.get('换手率', 0),
                    amount,
                    datetime.now().isoformat()
                ))
                saved_count += 1
            except:
                continue
        
        conn.commit()
        conn.close()
        
        log(f"  ✅ 保存 {saved_count} 条，过滤 {filtered_count} 条")
        
        # 显示最近3天数据
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, COUNT(*) as cnt 
            FROM limit_up_stocks 
            GROUP BY date 
            ORDER BY date DESC 
            LIMIT 3
        """)
        recent = cursor.fetchall()
        conn.close()
        
        log(f"\n📅 最近3天数据:")
        for date, cnt in recent:
            log(f"  {date}: {cnt} 只涨停股")
        
        log("\n✅ 每日更新完成！")
        
    except Exception as e:
        log(f"❌ 更新失败: {e}")

if __name__ == "__main__":
    main()
