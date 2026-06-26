#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查akshare版本和可用函数
"""

import akshare as ak
import inspect

print(f"akshare版本: {ak.__version__}")
print("\n检查常用数据类型的接口...")

# 检查期货相关接口
print("\n1. 期货相关接口:")
futures_functions = [func for func in dir(ak) if 'futures' in func or 'Future' in func]
print(futures_functions[:20])  # 只显示前20个

# 检查债券相关接口
print("\n2. 债券相关接口:")
bond_functions = [func for func in dir(ak) if 'bond' in func or 'Bond' in func]
print(bond_functions[:20])  # 只显示前20个

# 检查外汇相关接口
print("\n3. 外汇相关接口:")
forex_functions = [func for func in dir(ak) if 'forex' in func or 'Forex' in func]
print(forex_functions[:20])  # 只显示前20个

# 检查指数相关接口
print("\n4. 指数相关接口:")
index_functions = [func for func in dir(ak) if 'index' in func or 'Index' in func]
print(index_functions[:20])  # 只显示前20个

# 检查银行相关接口
print("\n5. 银行相关接口:")
bank_functions = [func for func in dir(ak) if 'bank' in func or 'Bank' in func]
print(bank_functions[:20])  # 只显示前20个
