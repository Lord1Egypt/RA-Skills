#!/usr/bin/env python3
"""
检查友盟推送后台登录状态
Usage: python check_auth.py [--verbose]
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def get_cookie_path():
    """获取 Cookie 文件路径"""
    script_dir = Path(__file__).parent
    return script_dir / 'cookie.json'


def check_cookie_valid(cookie_str):
    """简单验证 Cookie 格式"""
    if not cookie_str or len(cookie_str) < 20:
        return False
    
    # 友盟后台 Cookie 通常包含多个字段
    required_fields = ['UMENG_TOKEN', 'umeng_token', 'PHPSESSID']
    has_any_field = any(field in cookie_str for field in required_fields)
    
    return has_any_field


def mask_cookie(cookie_str):
    """脱敏显示 Cookie（仅显示前缀）"""
    if not cookie_str:
        return "(empty)"
    
    # 按分号分割，显示每个字段的 key 和 value 的前 10 个字符
    parts = cookie_str.split('; ')
    masked_parts = []
    for part in parts[:3]:  # 只显示前 3 个字段
        if '=' in part:
            key, value = part.split('=', 1)
            masked_value = value[:10] + '...' if len(value) > 10 else value
            masked_parts.append(f"{key}={masked_value}")
    
    return '; '.join(masked_parts)


def main():
    cookie_path = get_cookie_path()
    verbose = '--verbose' in sys.argv
    
    # 检查 Cookie 文件是否存在
    if not cookie_path.exists():
        print("❌ 未检测到登录信息")
        print("\n📝 请先登录并保存 Cookie:")
        print("   1. 访问 https://upush.umeng.com 并登录")
        print("   2. 按 F12 打开开发者工具，在 Console 中输入：document.cookie")
        print("   3. 复制完整的 Cookie 字符串")
        print("   4. 运行：python save_cookie.py \"你的 Cookie\"")
        sys.exit(1)
    
    try:
        # 读取 Cookie 文件
        with open(cookie_path, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)
        
        cookie = cookie_data.get('cookie', '')
        saved_at = cookie_data.get('saved_at', 'unknown')
        
        # 验证 Cookie 有效性
        if not check_cookie_valid(cookie):
            print("⚠️  Cookie 格式可能不正确")
            print(f"   当前值：{mask_cookie(cookie)}")
            print("\n💡 建议重新保存 Cookie")
            sys.exit(1)
        
        # 显示登录状态
        print("✅ 已登录")
        
        if verbose:
            print(f"\n📦 Cookie (脱敏): {mask_cookie(cookie)}")
            print(f"🕐 保存时间：{saved_at}")
            print(f"📁 文件路径：{cookie_path}")
            
            # 检查文件权限
            file_stat = os.stat(cookie_path)
            perms = oct(file_stat.st_mode)[-3:]
            print(f"🔒 文件权限：{perms}")
            
            if perms != '600':
                print(f"\n⚠️  警告：建议设置权限为 600")
                print(f"   运行：chmod 600 {cookie_path}")
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        print("❌ Cookie 文件格式错误")
        print(f"   文件：{cookie_path}")
        print("\n💡 请重新保存 Cookie:")
        print("   python save_cookie.py \"你的 Cookie\"")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ 检查失败：{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
