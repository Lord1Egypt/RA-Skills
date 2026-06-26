#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
切换公众号
"""

import json
import sys
from pathlib import Path

def switch_account(account_name):
    """切换到指定的公众号"""
    config_path = Path(__file__).parent.parent / "references" / "multi_account_config.json"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    for account in config['accounts']:
        if account['name'] == account_name:
            config['current_account'] = account['id']
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 已切换到 '{account_name}'")
            print(f"📂 工作目录: {account['base_dir']}/")
            return account
    
    print(f"❌ 未找到公众号: {account_name}")
    return None

def list_accounts():
    """列出所有公众号"""
    config_path = Path(__file__).parent.parent / "references" / "multi_account_config.json"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("\n✅ 已配置的公众号列表:\n")
    for i, account in enumerate(config['accounts'], 1):
        status = "激活" if account.get('active', True) else "停用"
        print(f"{i}️⃣ {account['name']}")
        print(f"   - 状态: {status}")
        print(f"   - 描述: {account.get('description', '无')}")
        print()
    
    print(f"📌 当前公众号: {get_current_account_name(config)}\n")

def get_current_account_name(config):
    """获取当前公众号名称"""
    current_id = config.get('current_account')
    for account in config['accounts']:
        if account['id'] == current_id:
            return account['name']
    return "未设置"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python switch_account.py <公众号名称>  # 切换公众号")
        print("  python switch_account.py --list       # 列出所有公众号")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        list_accounts()
    else:
        switch_account(sys.argv[1])
