#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据获取示例脚本
"""

import akshare as ak
import pandas as pd
import os
import datetime


def get_stock_list():
    """
    获取股票列表
    """
    try:
        data = ak.stock_info_a_code_name()
        print("股票列表获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取股票列表失败：{e}")
        return None


def get_daily_data(symbol, start_date, end_date):
    """
    获取股票日线数据
    """
    try:
        # 尝试使用不同的接口获取日线数据
        data = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        print(f"{symbol}日线数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取日线数据失败：{e}")
        return None


def get_spot_data():
    """
    获取股票实时行情数据
    """
    try:
        data = ak.stock_zh_a_spot()
        print("股票实时行情数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取实时行情数据失败：{e}")
        return None


def get_financial_data(symbol):
    """
    获取财务指标数据
    """
    try:
        # 尝试使用不同的接口获取财务数据
        data = ak.stock_financial_analysis_indicator(symbol=symbol)
        print(f"{symbol}财务指标数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取财务指标数据失败：{e}")
        return None


def get_news(symbol):
    """
    获取股票新闻
    """
    try:
        data = ak.stock_news_em(symbol=symbol)
        print(f"{symbol}新闻获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取股票新闻失败：{e}")
        return None


def main():
    """
    主函数
    """
    print("===== akshare 股票数据获取示例 =====")
    
    # 获取股票列表
    stock_list = get_stock_list()
    
    if stock_list is not None:
        # 获取第一只股票的代码
        symbol = stock_list['code'].iloc[0]
        print(f"\n使用股票代码：{symbol}")
        
        # 获取日线数据（最近30天）
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        print(f"\n1. 获取日线数据：{start_date} 至 {end_date}")
        get_daily_data(symbol, start_date, end_date)
        
        # 获取实时行情数据
        print("\n2. 获取股票实时行情数据")
        get_spot_data()
        
        # 获取财务数据
        print(f"\n3. 获取财务指标数据：{symbol}")
        get_financial_data(symbol)
        
        # 获取股票新闻
        print(f"\n4. 获取股票新闻：{symbol}")
        get_news(symbol)


if __name__ == "__main__":
    main()