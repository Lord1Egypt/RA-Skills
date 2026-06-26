#!/usr/bin/env python3
"""
清除保存的友盟推送后台登录 Cookie
Usage: python clear_cookie.py
"""

import os
import sys
from pathlib import Path


def get_cookie_path():
    """获取 Cookie 文件路径"""
    script_dir = Path(__file__).parent
    return script_dir / 'cookie.json'


def main():
    cookie_path = get_cookie_path()
    
    if not cookie_path.exists():
        print("ℹ️  未找到 Cookie 文件，无需清除")
        sys.exit(0)
    
    try:
        # 读取 Cookie 文件（用于确认）
        with open(cookie_path, 'r', encoding='utf-8') as f:
            import json
            cookie_data = json.load(f)
        
        saved_at = cookie_data.get('saved_at', 'unknown')
        
        # 删除文件
        os.remove(cookie_path)
        
        print("✅ Cookie 已清除")
        print(f"🗑️  删除文件：{cookie_path}")
        print(f"🕐 上次保存：{saved_at}")
        print("\n💡 如需重新使用，请先登录并保存新 Cookie:")
        print("   python save_cookie.py \"你的 Cookie\"")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 清除失败：{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
