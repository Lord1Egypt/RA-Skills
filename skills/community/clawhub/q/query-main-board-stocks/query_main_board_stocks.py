#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询沪深主板股票（非创业板、非科创板）
使用 query_stock_basic 获取真实个股列表
"""

import baostock as bs
import pandas as pd
import json
from datetime import datetime

# ============== 配置 ==============
import os

# 输出到当前目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'main_board_stocks.json')
CSV_FILE = os.path.join(SCRIPT_DIR, 'main_board_stocks.csv')

# 创业板、科创板代码前缀
GEM_CODES = ['300', '301']  # 创业板
STAR_CODES = ['688']  # 科创板

# 主板代码前缀
MAIN_BOARD_CODES = ['600', '601', '603', '605',  # 沪市主板
                    '000', '001', '002', '003']  # 深市主板

# ============== 获取股票列表 ==============
def get_all_stocks():
    """获取所有 A 股个股列表"""
    bs.login()
    
    # 获取股票基本信息
    rs = bs.query_stock_basic()
    
    data_list = [rs.get_row_data() for _ in iter(rs.next, False)]
    df = pd.DataFrame(data_list, columns=rs.fields)
    bs.logout()
    
    return df

# ============== 过滤主板股票 ==============
def filter_main_board(df):
    """过滤出主板股票"""
    
    # type=1 是个股，type=2 是指数，type=4 是债券，type=5 是 ETF
    # 只保留 type=1 的个股
    df_stocks = df[df['type'] == '1'].copy()
    
    # 只保留上市状态的股票（status=1）
    df_stocks = df_stocks[df_stocks['status'] == '1'].copy()
    
    # 提取纯数字代码
    df_stocks['pure_code'] = df_stocks['code'].str.replace('sh.', '').str.replace('sz.', '')
    df_stocks['code_prefix'] = df_stocks['pure_code'].str[:3]
    
    # 过滤主板（排除创业板 300/301 和科创板 688）
    df_main = df_stocks[
        df_stocks['code_prefix'].isin(MAIN_BOARD_CODES)
    ].copy()
    
    return df_main

# ============== 主函数 ==============
def main():
    print("=" * 90)
    print("沪深主板股票查询（非创业板、非科创板）")
    print("=" * 90)
    print(f"运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    
    # 获取所有股票
    df_all = get_all_stocks()
    print(f"✅ 获取到 {len(df_all)} 只股票")
    
    # 过滤主板
    df_main = filter_main_board(df_all)
    print(f"✅ 主板股票：{len(df_main)} 只")
    
    # 统计
    sh_stocks = df_main[df_main['code'].str.startswith('sh.')]
    sz_stocks = df_main[df_main['code'].str.startswith('sz.')]
    
    print(f"\n{'='*90}")
    print(f"📊 统计结果")
    print(f"{'='*90}")
    print(f"\n市场分布:")
    print(f"  主板股票：{len(df_main)} 只")
    print(f"  沪市主板：{len(sh_stocks)} 只")
    print(f"  深市主板：{len(sz_stocks)} 只")
    
    # 代码前缀分布
    print(f"\n代码前缀分布:")
    prefix_stats = df_main['code_prefix'].value_counts().sort_index()
    for prefix, count in prefix_stats.items():
        board_type = '沪市主板' if prefix.startswith('6') else '深市主板'
        print(f"  {prefix} ({board_type}): {count} 只")
    
    # 导出
    print(f"\n{'='*90}")
    print(f"导出结果...")
    print(f"{'='*90}")
    
    # JSON
    output_data = {
        'query_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_main_board': len(df_main),
        'sh_count': len(sh_stocks),
        'sz_count': len(sz_stocks),
        'stocks': df_main[['code', 'code_name', 'pure_code']].to_dict('records')
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON 已保存：{OUTPUT_FILE}")
    
    # CSV
    df_export = df_main[['code', 'code_name', 'pure_code']].copy()
    df_export.columns = ['代码', '名称', '纯代码']
    df_export.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
    
    print(f"✅ CSV 已保存：{CSV_FILE}")
    
    # 显示前 30 只
    print(f"\n{'='*90}")
    print(f"📋 主板股票列表（前 30 只）")
    print(f"{'='*90}")
    print(f"\n{'代码':<12} {'名称':<12} {'纯代码':<10}")
    print(f"{'-'*90}")
    
    for _, row in df_main.head(30).iterrows():
        print(f"{row['code']:<12} {row['code_name']:<12} {row['pure_code']:<10}")
    
    print(f"\n... (共{len(df_main)}只)")
    print(f"\n{'='*90}")
    print(f"✅ 查询完成")
    print(f"{'='*90}")

if __name__ == '__main__':
    main()
