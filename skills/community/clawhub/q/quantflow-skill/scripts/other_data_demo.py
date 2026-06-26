#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
其他数据类型获取示例脚本
"""

import akshare as ak
import pandas as pd
import os
import datetime


def get_crypto_data():
    """
    获取加密货币数据
    """
    try:
        # 获取加密货币实时行情
        data = ak.crypto_js_spot()
        print("加密货币实时行情获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取加密货币数据失败：{e}")
        return None


def get_bitcoin_cme():
    """
    获取CME比特币期货数据
    """
    try:
        # 获取CME比特币期货数据
        data = ak.crypto_bitcoin_cme()
        print("CME比特币期货数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取CME比特币期货数据失败：{e}")
        return None


def get_bitcoin_hold_report():
    """
    获取比特币持仓报告
    """
    try:
        # 获取比特币持仓报告
        data = ak.crypto_bitcoin_hold_report()
        print("比特币持仓报告获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取比特币持仓报告失败：{e}")
        return None


def get_futures_contract_detail():
    """
    获取期货合约详情
    """
    try:
        # 获取期货合约详情（使用不同的接口）
        data = ak.futures_contract_info_shfe()
        print("期货合约详情获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取期货合约详情失败：{e}")
        return None


def get_bond_cb_jsl():
    """
    获取可转债数据
    """
    try:
        # 获取可转债数据
        data = ak.bond_cb_jsl()
        print("可转债数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取可转债数据失败：{e}")
        return None


def get_forex_spot():
    """
    获取外汇实时行情
    """
    try:
        # 获取外汇实时行情
        data = ak.forex_spot_em()
        print("外汇实时行情获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取外汇实时行情失败：{e}")
        return None


def get_forex_hist():
    """
    获取外汇历史数据
    """
    try:
        # 获取外汇历史数据（使用不同的参数格式）
        data = ak.forex_hist_em(symbol="美元/人民币")
        print("外汇历史数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取外汇历史数据失败：{e}")
        return None


def get_index_all_cni():
    """
    获取指数数据
    """
    try:
        # 获取指数数据
        data = ak.index_all_cni()
        print("指数数据获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取指数数据失败：{e}")
        return None


def get_bank_interest_rate():
    """
    获取银行基准利率
    """
    try:
        # 获取银行基准利率
        data = ak.macro_bank_china_interest_rate()
        print("银行基准利率获取成功：")
        print(data.head())
        return data
    except Exception as e:
        print(f"获取银行基准利率失败：{e}")
        return None


def main():
    """
    主函数
    """
    print("===== akshare 其他数据类型获取示例 =====")
    
    # 获取加密货币数据
    print("1. 获取加密货币实时行情")
    get_crypto_data()
    
    # 获取CME比特币期货数据
    print("\n2. 获取CME比特币期货数据")
    get_bitcoin_cme()
    
    # 获取比特币持仓报告
    print("\n3. 获取比特币持仓报告")
    get_bitcoin_hold_report()
    
    # 获取期货合约详情
    print("\n4. 获取期货合约详情")
    get_futures_contract_detail()
    
    # 获取可转债数据
    print("\n5. 获取可转债数据")
    get_bond_cb_jsl()
    
    # 获取外汇实时行情
    print("\n6. 获取外汇实时行情")
    get_forex_spot()
    
    # 获取外汇历史数据
    print("\n7. 获取外汇历史数据")
    get_forex_hist()
    
    # 获取指数数据
    print("\n8. 获取指数数据")
    get_index_all_cni()
    
    # 获取银行基准利率
    print("\n9. 获取银行基准利率")
    get_bank_interest_rate()


if __name__ == "__main__":
    main()