#!/usr/bin/env python3
"""
动态导入工具 - 消除硬编码的 skills.smyx_payment. 路径前缀
根据当前文件位置动态计算模块路径，实现相对位置的动态导入
"""

import importlib
import os
import sys


def _get_package_root():
    """获取 smyx_payment 包的根目录路径"""
    current_file = os.path.abspath(__file__)
    # _dynamic_import.py 位于 skills/smyx_payment/scripts/
    # 向上两级就是 smyx_payment 包根目录
    scripts_dir = os.path.dirname(current_file)
    package_root = os.path.dirname(scripts_dir)
    return package_root


def _get_module_path(relative_module_name):
    """
    根据相对模块名，动态构建完整的模块路径
    
    Args:
        relative_module_name: 相对于 scripts 目录的模块名，如 'pay_with_cloud_order'
    
    Returns:
        完整的模块导入路径，如 'skills.smyx_payment.scripts.pay_with_cloud_order'
    """
    # 获取当前包的父目录，动态计算包路径
    package_root = _get_package_root()
    parent_dir = os.path.dirname(package_root)  # skills 目录
    
    # 动态获取包名（根据目录结构）
    package_name = os.path.basename(package_root)  # smyx_payment
    parent_package = os.path.basename(parent_dir)  # skills
    
    return f"{parent_package}.{package_name}.scripts.{relative_module_name}"


def import_script_module(module_name):
    """
    动态导入 scripts 目录下的模块
    
    Args:
        module_name: 模块名（不含 .py 后缀），如 'pay_with_cloud_order'
    
    Returns:
        导入的模块对象
    """
    full_module_path = _get_module_path(module_name)
    return importlib.import_module(full_module_path)


def import_from_script(module_name, *names):
    """
    从指定脚本模块中导入指定的名称（函数、类等）
    
    Args:
        module_name: 脚本模块名，如 'pay_with_cloud_order'
        *names: 要导入的名称，如 'query_alipay_trade_status', 'create_payment_with_cloud_order'
    
    Returns:
        如果只有一个名称，返回该对象；如果有多个，返回元组
    """
    module = import_script_module(module_name)
    results = []
    for name in names:
        if hasattr(module, name):
            results.append(getattr(module, name))
        else:
            raise ImportError(f"cannot import name '{name}' from '{module.__name__}'")
    
    return results[0] if len(results) == 1 else tuple(results)


# 便捷的导入函数，使用方式：
# query_alipay_trade_status = import_from('pay_with_cloud_order', 'query_alipay_trade_status')
# create_payment, query_status = import_from('pay_with_cloud_order', 'create_payment_with_cloud_order', 'query_alipay_trade_status')
import_from = import_from_script

