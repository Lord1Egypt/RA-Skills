#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
探索Akshare库的API结构和功能
"""

import akshare as ak
import re

# 打印akshare库的版本
print(f"Akshare版本: {ak.__version__}")

# 获取akshare库的所有属性
all_attrs = dir(ak)

# 按类别分组函数
print("\n=== Akshare API 分类 ===")

# 股票相关函数
stock_functions = [attr for attr in all_attrs if re.match(r'stock_', attr)]
print(f"\n股票相关函数 ({len(stock_functions)}个):")
for func in sorted(stock_functions)[:30]:  # 只显示前30个
    print(f"  - {func}")

# 基金相关函数
fund_functions = [attr for attr in all_attrs if re.match(r'fund_', attr)]
print(f"\n基金相关函数 ({len(fund_functions)}个):")
for func in sorted(fund_functions)[:30]:  # 只显示前30个
    print(f"  - {func}")

# 宏观经济相关函数
macro_functions = [attr for attr in all_attrs if re.match(r'macro_', attr)]
print(f"\n宏观经济相关函数 ({len(macro_functions)}个):")
for func in sorted(macro_functions)[:20]:  # 只显示前20个
    print(f"  - {func}")

# 债券相关函数
bond_functions = [attr for attr in all_attrs if re.match(r'bond_', attr)]
print(f"\n债券相关函数 ({len(bond_functions)}个):")
for func in sorted(bond_functions)[:20]:  # 只显示前20个
    print(f"  - {func}")

# 期货相关函数
futures_functions = [attr for attr in all_attrs if re.match(r'futures_', attr)]
print(f"\n期货相关函数 ({len(futures_functions)}个):")
for func in sorted(futures_functions)[:20]:  # 只显示前20个
    print(f"  - {func}")

# 外汇相关函数
forex_functions = [attr for attr in all_attrs if re.match(r'forex_', attr)]
print(f"\n外汇相关函数 ({len(forex_functions)}个):")
for func in sorted(forex_functions)[:20]:  # 只显示前20个
    print(f"  - {func}")

# 加密货币相关函数
crypto_functions = [attr for attr in all_attrs if re.match(r'crypto_', attr)]
print(f"\n加密货币相关函数 ({len(crypto_functions)}个):")
for func in sorted(crypto_functions)[:20]:  # 只显示前20个
    print(f"  - {func}")

# 测试一些常用的接口
print("\n=== 测试常用接口 ===")

# 测试股票列表接口
try:
    print("\n测试股票列表接口:")
    stock_list = ak.stock_info_a_code_name()
    print(f"成功获取股票列表，共 {len(stock_list)} 条数据")
    print(stock_list.head())
except Exception as e:
    print(f"获取股票列表失败: {e}")

# 测试股票实时行情接口
try:
    print("\n测试股票实时行情接口:")
    stock_spot = ak.stock_zh_a_spot()
    print(f"成功获取股票实时行情，共 {len(stock_spot)} 条数据")
    print(stock_spot.head())
except Exception as e:
    print(f"获取股票实时行情失败: {e}")

# 测试行业板块接口
try:
    print("\n测试行业板块接口:")
    industry = ak.stock_board_industry_spot_em()
    print(f"成功获取行业板块数据，共 {len(industry)} 条数据")
    print(industry.head())
except Exception as e:
    print(f"获取行业板块数据失败: {e}")

# 测试宏观经济接口
try:
    print("\n测试宏观经济接口:")
    cpi = ak.macro_china_cpi()
    print(f"成功获取CPI数据，共 {len(cpi)} 条数据")
    print(cpi.tail())
except Exception as e:
    print(f"获取CPI数据失败: {e}")