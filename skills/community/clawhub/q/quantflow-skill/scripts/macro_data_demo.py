#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宏观经济数据获取示例脚本
"""

import akshare as ak
import pandas as pd
import os
import datetime


def get_cpi_data():
    """
    获取中国CPI数据
    """
    try:
        data = ak.macro_china_cpi()
        print("中国CPI数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取中国CPI数据失败：{e}")
        return None


def get_pmi_data():
    """
    获取中国PMI数据
    """
    try:
        data = ak.macro_china_pmi()
        print("中国PMI数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取中国PMI数据失败：{e}")
        return None


def get_interest_rate_data():
    """
    获取中国基准利率数据
    """
    try:
        data = ak.macro_bank_china_interest_rate()
        print("中国基准利率数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取中国基准利率数据失败：{e}")
        return None


def get_us_stock_spot():
    """
    获取美股实时行情数据
    """
    try:
        data = ak.stock_us_spot()
        print("美股实时行情数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取美股实时行情数据失败：{e}")
        return None


def get_hk_stock_spot():
    """
    获取港股实时行情数据
    """
    try:
        data = ak.stock_hk_spot()
        print("港股实时行情数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取港股实时行情数据失败：{e}")
        return None


def main():
    """
    主函数
    """
    print("===== akshare 宏观经济数据获取示例 =====")
    
    # 获取中国CPI数据
    print("1. 获取中国CPI数据")
    get_cpi_data()
    
    # 获取中国PMI数据
    print("\n2. 获取中国PMI数据")
    get_pmi_data()
    
    # 获取中国基准利率数据
    print("\n3. 获取中国基准利率数据")
    get_interest_rate_data()
    
    # 获取美股实时行情数据
    print("\n4. 获取美股实时行情数据")
    get_us_stock_spot()
    
    # 获取港股实时行情数据
    print("\n5. 获取港股实时行情数据")
    get_hk_stock_spot()


if __name__ == "__main__":
    main()