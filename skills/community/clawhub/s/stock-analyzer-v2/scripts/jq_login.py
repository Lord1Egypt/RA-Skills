#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽账号配置脚本（交互式安全存储）

使用方法:
    python jq_login.py           # 交互式配置
    python jq_login.py --show     # 查看已配置的账号（不显示密码）
    python jq_login.py --clear    # 清除已配置的账号
    python jq_login.py --test     # 测试账号是否有效
"""

import argparse
import getpass
import json
import os
import sys

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '.jq_config.json')

def load_config():
    """加载已保存的配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(phone, password):
    """安全保存配置（文件权限设为600）"""
    config = {'phone': phone}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    # 保存密码到环境变量（不落盘）
    os.environ['JQDATA_PHONE'] = phone
    os.environ['JQDATA_PASSWORD'] = password
    # 设置文件权限（仅本人可读写）
    os.chmod(CONFIG_FILE, 0o600)
    print(f"✅ 账号 {phone} 已配置")

def clear_config():
    """清除配置"""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    print("✅ 配置已清除")

def show_config():
    """显示当前配置"""
    config = load_config()
    if config.get('phone'):
        print(f"已配置账号: {config['phone']}")
        print("密码: [已通过环境变量设置，不显示]")
    else:
        print("未配置聚宽账号")

def test_login():
    """测试登录"""
    phone = os.environ.get('JQDATA_PHONE')
    password = os.environ.get('JQDATA_PASSWORD')
    
    if not phone or not password:
        # 尝试从配置文件加载
        config = load_config()
        if not config.get('phone'):
            print("❌ 未配置账号，请先运行 jq_login.py 进行配置")
            sys.exit(1)
        print("❌ 环境变量未设置，请重新配置: python jq_login.py")
        sys.exit(1)
    
    try:
        import jqdatasdk as jq
        jq.auth(phone, password)
        print(f"✅ 账号 {phone} 登录成功！")
        
        # 显示积分信息
        count = jq.get_query_count()
        print(f"   总积分: {count.get('total', 'N/A')}")
        print(f"   剩余:   {count.get('spare', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='聚宽账号配置')
    parser.add_argument('--show', action='store_true', help='显示已配置的账号')
    parser.add_argument('--clear', action='store_true', help='清除已配置的账号')
    parser.add_argument('--test', action='store_true', help='测试账号登录')
    args = parser.parse_args()
    
    if args.show:
        show_config()
        return
    
    if args.clear:
        clear_config()
        return
    
    if args.test:
        test_login()
        return
    
    # 交互式配置
    print("\n" + "="*50)
    print("   聚宽 JQData 账号配置")
    print("="*50)
    print()
    print("请输入聚宽账号信息（手机号和密码）")
    print("凭证仅保存在当前会话环境变量中，不落盘存储")
    print()
    
    phone = input("手机号: ").strip()
    if not phone:
        print("❌ 手机号不能为空")
        sys.exit(1)
    
    password = getpass.getpass("密码: ")
    if not password:
        print("❌ 密码不能为空")
        sys.exit(1)
    
    # 保存配置
    save_config(phone, password)
    
    # 询问是否测试登录
    print()
    test = input("是否测试登录? (y/n): ").strip().lower()
    if test == 'y':
        test_login()

if __name__ == '__main__':
    main()
