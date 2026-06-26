#!/usr/bin/env python3
"""
批量采集多只股票的历史数据
支持从文件或命令行读取股票列表
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# 导入单只股票采集功能
sys.path.insert(0, str(Path(__file__).parent))

try:
    from fetch_stock import fetch_stock_data
except ImportError:
    print("错误: 无法导入 fetch_stock 模块")
    sys.exit(1)


def parse_stock_file(file_path: str) -> list:
    """
    解析股票列表文件
    
    文件格式：
    # 注释行
    股票代码,市场,名称（名称可选）
    600519,A,贵州茅台
    00700,HK
    
    Args:
        file_path: 文件路径
    
    Returns:
        股票列表 [(code, market, name), ...]
    """
    stocks = []
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"错误: 文件不存在: {file_path}")
        return stocks
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith("#"):
                continue
            
            parts = [p.strip() for p in line.split(",")]
            
            if len(parts) < 2:
                print(f"警告: 第 {line_num} 行格式错误，跳过: {line}")
                continue
            
            code = parts[0]
            market = parts[1].upper()
            name = parts[2] if len(parts) > 2 else None
            
            if market not in ["A", "HK"]:
                print(f"警告: 第 {line_num} 行市场错误，跳过: {market}")
                continue
            
            stocks.append((code, market, name))
    
    return stocks


def batch_fetch(stocks: list, period: str = "daily", output_dir: str = "stock_data"):
    """
    批量采集股票数据
    
    Args:
        stocks: 股票列表 [(code, market, name), ...]
        period: 时间周期
        output_dir: 输出目录
    
    Returns:
        (success_count, fail_count, result_files)
    """
    if not stocks:
        print("错误: 没有股票需要采集")
        return 0, 0, []
    
    print("=" * 60)
    print(f"批量采集 {len(stocks)} 只股票")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    result_files = []
    
    for i, (code, market, name) in enumerate(stocks, 1):
        print(f"\n[{i}/{len(stocks)}] " + "-" * 50)
        
        success, file_path = fetch_stock_data(
            code=code,
            market=market,
            period=period,
            output_dir=output_dir,
            stock_name=name
        )
        
        if success:
            success_count += 1
            if file_path:
                result_files.append(file_path)
        else:
            fail_count += 1
    
    # 输出汇总
    print("\n" + "=" * 60)
    print("批量采集完成!")
    print("=" * 60)
    print(f"成功: {success_count} 只")
    print(f"失败: {fail_count} 只")
    
    if result_files:
        print(f"\n生成的文件:")
        for f in result_files:
            print(f"  - {Path(f).name}")
    
    return success_count, fail_count, result_files


def main():
    parser = argparse.ArgumentParser(
        description="批量采集多只股票的历史数据"
    )
    
    # 输入方式：文件或命令行
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", help="股票列表文件")
    input_group.add_argument("--codes", help="股票代码列表，逗号分隔")
    
    parser.add_argument("--markets", help="市场列表，逗号分隔（A=A股，HK=港股）")
    parser.add_argument("--names", help="股票名称列表，逗号分隔（可选）")
    parser.add_argument("--period", default="daily", 
                       choices=["daily", "weekly", "monthly"],
                       help="时间周期（默认：daily）")
    parser.add_argument("--output", default="stock_data", help="输出目录（默认：./stock_data）")
    
    args = parser.parse_args()
    
    stocks = []
    
    if args.file:
        # 从文件读取
        print(f"从文件读取股票列表: {args.file}")
        stocks = parse_stock_file(args.file)
        
        if not stocks:
            print("错误: 未找到有效的股票")
            sys.exit(1)
        
        print(f"已加载 {len(stocks)} 只股票")
    
    elif args.codes:
        # 从命令行读取
        codes = [c.strip() for c in args.codes.split(",")]
        
        if not args.markets:
            print("错误: 使用 --codes 时必须同时指定 --markets")
            sys.exit(1)
        
        markets = [m.strip().upper() for m in args.markets.split(",")]
        
        if len(codes) != len(markets):
            print(f"错误: 代码数量({len(codes)})与市场数量({len(markets)})不匹配")
            sys.exit(1)
        
        names = []
        if args.names:
            names = [n.strip() for n in args.names.split(",")]
            if len(names) != len(codes):
                print(f"警告: 名称数量({len(names)})与代码数量({len(codes)})不匹配，将忽略名称")
                names = [None] * len(codes)
        else:
            names = [None] * len(codes)
        
        stocks = list(zip(codes, markets, names))
    
    # 执行批量采集
    success_count, fail_count, result_files = batch_fetch(
        stocks=stocks,
        period=args.period,
        output_dir=args.output
    )
    
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
