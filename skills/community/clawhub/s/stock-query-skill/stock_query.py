#!/usr/bin/env python3
"""股票查詢技能
查詢指定股票代碼的30天每日股價資料
"""

import yfinance as yf
import pandas as pd
import sys

def query_stock_prices(ticker):
    """查詢30天每日股價"""
    try:
        # 創建 Ticker 物件
        stock = yf.Ticker(ticker)
        
        # 查詢過去30天的每日資料
        history = stock.history(
            period='30d',  # 過去30天
            interval='1d'  # 每天資料
        )
        
        if history.empty:
            return None, f"未找到 {ticker} 的股價資料"
        
        return history, None
        
    except Exception as e:
        return None, str(e)

def main():
    """主程式"""
    if len(sys.argv) < 2:
        print("Usage: python stock_query.py [ticker]")
        print("Example: python stock_query.py TSM")
        return
    
    ticker = sys.argv[1].strip().upper()
    
    print(f"正在查詢 {ticker} 的過去30天每日股價...")
    history, error = query_stock_prices(ticker)
    
    if error:
        print(f"錯誤: {error}")
        return
    
    print(f"
{ticker} 過去30天每日股價資料:")
    print("-" * 50)
    print(history)
    
    # 保存為 CSV 檔案
    csv_filename = f"{ticker}_30days.csv"
    history.to_csv(csv_filename)
    print(f"
資料已保存為 {csv_filename}")


if __name__ == "__main__":
    main()