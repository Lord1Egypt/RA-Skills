#!/usr/bin/env python3
"""
采集单只股票的历史数据
支持A股和港股
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    import akshare as ak
    import pandas as pd
except ImportError:
    print("错误: 未安装必需的库")
    print("请运行: pip install akshare yfinance pandas")
    sys.exit(1)


def get_stock_name(code: str, market: str) -> str:
    """
    尝试获取股票名称
    
    Args:
        code: 股票代码
        market: 市场（A/HK）
    
    Returns:
        股票名称，如果获取失败则返回代码
    """
    try:
        if market == "A":
            # A股：尝试获取名称
            try:
                # 先尝试用日线接口获取
                df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20240101", end_date="20240131")
                if len(df) > 0 and "股票代码" in df.columns:
                    # 虽然akshare的返回可能没有直接的名称，但我们可以用代码
                    pass
            except:
                pass
            return f"A股{code}"
        
        elif market == "HK":
            # 港股
            try:
                df = ak.stock_hk_daily(symbol=code, start_date="20240101", end_date="20240131")
                if len(df) > 0:
                    pass
            except:
                pass
            return f"港股{code}"
    except:
        pass
    
    return code


def fetch_stock_data(code: str, market: str, period: str = "daily", 
                     start_date: str = None, end_date: str = None, 
                     output_dir: str = "stock_data", stock_name: str = None):
    """
    采集股票数据
    
    Args:
        code: 股票代码
        market: 市场（A/HK）
        period: 周期（daily/weekly/monthly）
        start_date: 开始日期（YYYYMMDD）
        end_date: 结束日期（YYYYMMDD）
        output_dir: 输出目录
        stock_name: 股票名称（可选）
    
    Returns:
        (success, data_file_path)
    """
    # 设置默认日期
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    if start_date is None:
        start_date = "20000101"
    
    # 获取股票名称
    if stock_name is None:
        stock_name = get_stock_name(code, market)
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"正在采集: {stock_name} ({code})")
    print(f"市场: {market}, 周期: {period}")
    print(f"时间范围: {start_date} 至 {end_date}")
    
    df = None
    data_source = ""
    
    try:
        if market == "A":
            # A股数据采集
            data_source = "akshare(A股)"
            print(f"使用数据源: {data_source}")
            
            # 映射周期参数
            period_map = {
                "daily": "daily",
                "weekly": "weekly",
                "monthly": "monthly"
            }
            ak_period = period_map.get(period, "daily")
            
            df = ak.stock_zh_a_hist(
                symbol=code,
                period=ak_period,
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"  # 前复权
            )
            
        elif market == "HK":
            # 港股数据采集
            data_source = "akshare(港股)"
            print(f"使用数据源: {data_source}")
            
            try:
                df = ak.stock_hk_daily(
                    symbol=code,
                    start_date=start_date,
                    end_date=end_date
                )
            except Exception as e:
                print(f"  akshare港股接口失败: {e}")
                print("  尝试使用yfinance...")
                
                # 备选：使用yfinance
                try:
                    import yfinance as yf
                    data_source = "yfinance"
                    
                    ticker = f"{code}.HK"
                    stock = yf.Ticker(ticker)
                    
                    # 映射周期
                    period_map = {
                        "daily": "1d",
                        "weekly": "1wk",
                        "monthly": "1mo"
                    }
                    yf_period = period_map.get(period, "1d")
                    
                    df = stock.history(period="max", interval=yf_period)
                    
                    # 重置索引，使日期成为列
                    df = df.reset_index()
                    
                except Exception as e2:
                    print(f"  yfinance也失败: {e2}")
                    raise
        else:
            print(f"错误: 不支持的市场: {market}")
            return False, None
        
        if df is None or len(df) == 0:
            print("错误: 未获取到数据")
            return False, None
        
        # 生成输出文件名
        safe_name = stock_name.replace(" ", "_").replace("/", "_")
        output_file = output_path / f"{safe_name}_{code}_{market}_{period}.csv"
        
        # 保存数据
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        
        print(f"✓ 采集成功!")
        print(f"  记录数: {len(df)}")
        
        # 显示时间范围
        if len(df) > 0:
            if "日期" in df.columns:
                print(f"  时间范围: {df.iloc[0]['日期']} 至 {df.iloc[-1]['日期']}")
            elif "Date" in df.columns:
                print(f"  时间范围: {df.iloc[0]['Date']} 至 {df.iloc[-1]['Date']}")
            elif hasattr(df, 'index') and len(df.index) > 0:
                print(f"  时间范围: {df.index[0]} 至 {df.index[-1]}")
        
        print(f"  保存文件: {output_file}")
        
        return True, str(output_file)
        
    except Exception as e:
        print(f"✗ 采集失败: {e}")
        return False, None


def main():
    parser = argparse.ArgumentParser(
        description="采集单只股票的历史数据（支持A股和港股）"
    )
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--market", required=True, choices=["A", "HK"], help="市场：A=A股，HK=港股")
    parser.add_argument("--period", default="daily", 
                       choices=["daily", "weekly", "monthly", "1min", "5min", "15min", "30min", "60min"],
                       help="时间周期（默认：daily）")
    parser.add_argument("--start", help="开始日期：YYYYMMDD（默认：20000101）")
    parser.add_argument("--end", help="结束日期：YYYYMMDD（默认：今天）")
    parser.add_argument("--output", default="stock_data", help="输出目录（默认：./stock_data）")
    parser.add_argument("--name", help="股票名称（可选）")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("股票历史数据采集")
    print("=" * 60)
    
    success, file_path = fetch_stock_data(
        code=args.code,
        market=args.market,
        period=args.period,
        start_date=args.start,
        end_date=args.end,
        output_dir=args.output,
        stock_name=args.name
    )
    
    print("\n" + "=" * 60)
    if success:
        print("完成!")
    else:
        print("采集失败，请检查股票代码和网络连接")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
