#!/usr/bin/env python3
"""
symx_payment - 支付成功后查询账户信息
在支付成功后自动调用 query.py 查询用户账户余额和使用情况
"""

import sys
import os
import subprocess

# 添加脚本路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def query_account_after_payment(phone):
    """
    支付成功后查询账户信息
    
    Args:
        phone: 充值账号（手机号）
    """
    print()
    print('=' * 80)
    print('💰 支付成功！正在查询账户信息...')
    print('=' * 80)
    print()
    
    # 使用 module 方式调用 query.py
    cmd = [
        sys.executable, '-m', 'scripts.query', phone
    ]
    
    print(f'执行命令：python -m scripts.query {phone}')
    print()
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=SCRIPT_DIR
    )
    
    # 输出查询结果
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print('错误信息：')
        print(result.stderr)
    
    print()
    print('=' * 80)
    if result.returncode == 0:
        print('✅ 账户信息查询成功！')
    else:
        print('⚠️  账户信息查询失败，请稍后重试')
    print('=' * 80)
    print()
    
    return result.returncode == 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法：python3 query_after_payment.py <手机号>')
        print('示例：python3 query_after_payment.py 13829295590')
        sys.exit(1)
    
    phone = sys.argv[1]
    query_account_after_payment(phone)
