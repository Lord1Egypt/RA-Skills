#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金数据获取示例脚本
"""

import akshare as ak
import pandas as pd
import os
import datetime


def get_etf_fund_list():
    """
    获取ETF基金列表
    """
    try:
        data = ak.fund_etf_category_sina()
        print("ETF基金列表获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取ETF基金列表失败：{e}")
        return None


def get_fund_info(fund_code):
    """
    获取基金信息
    """
    try:
        # 尝试使用ETF基金信息接口
        data = ak.fund_etf_fund_info_em(fund=fund_code)
        print(f"{fund_code}基金信息获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取基金信息失败：{e}")
        return None


def main():
    """
    主函数
    """
    print("===== akshare 基金数据获取示例 =====")
    
    # 获取ETF基金列表
    print("1. 获取ETF基金列表")
    etf_list = get_etf_fund_list()
    
    # 测试基金代码
    fund_code = "510050"
    print(f"\n使用测试基金代码：{fund_code}")
    
    # 获取基金信息
    print(f"\n2. 获取基金信息：{fund_code}")
    get_fund_info(fund_code)


if __name__ == "__main__":
    main()