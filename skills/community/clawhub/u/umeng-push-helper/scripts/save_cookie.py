#!/usr/bin/env python3
"""
保存友盟推送后台登录 Cookie
Usage: python save_cookie.py "your-cookie-string"
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


def validate_cookie(cookie_str):
    """验证 Cookie 格式"""
    if not cookie_str or len(cookie_str) < 20:
        return False, "Cookie 太短，格式可能不正确"
    
    # 检查是否包含典型的友盟 Cookie 字段
    required_fields = ['UMENG_TOKEN', 'umeng_token', 'PHPSESSID']
    has_any_field = any(field in cookie_str for field in required_fields)
    
    if not has_any_field:
        return False, "Cookie 中未找到关键字段 (UMENG_TOKEN/umeng_token/PHPSESSID)"
    
    # 检查格式是否正确（key=value; key=value）
    parts = cookie_str.split('; ')
    valid_parts = 0
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            if key.strip() and value.strip():
                valid_parts += 1
    
    if valid_parts < 1:
        return False, "Cookie 格式应为：key=value; key=value"
    
    return True, "Cookie 格式正确"


def mask_cookie(cookie_str):
    """脱敏显示 Cookie"""
    if not cookie_str:
        return "(empty)"
    
    parts = cookie_str.split('; ')
    masked_parts = []
    for part in parts[:3]:
        if '=' in part:
            key, value = part.split('=', 1)
            masked_value = value[:10] + '...' if len(value) > 10 else value
            masked_parts.append(f"{key}={masked_value}")
    
    return '; '.join(masked_parts)


def main():
    if len(sys.argv) < 2:
        print("❌ 缺少 Cookie 参数")
        print("\n📝 使用方法:")
        print("   python save_cookie.py \"你的 Cookie 字符串\"")
        print("\n💡 如何获取 Cookie:")
        print("   1. 访问 https://upush.umeng.com 并登录")
        print("   2. 按 F12 打开开发者工具")
        print("   3. 切换到 Console 标签")
        print("   4. 输入：document.cookie")
        print("   5. 复制完整的 Cookie 字符串")
        sys.exit(1)
    
    cookie = sys.argv[1].strip()
    
    # 验证 Cookie
    is_valid, message = validate_cookie(cookie)
    if not is_valid:
        print(f"❌ {message}")
        print(f"\n当前值：{mask_cookie(cookie)}")
        print("\n💡 请确保复制了完整的 Cookie 字符串")
        sys.exit(1)
    
    # 准备保存
    cookie_data = {
        'cookie': cookie,
        'saved_at': datetime.now().isoformat(),
        'version': '1.0'
    }
    
    cookie_path = get_cookie_path()
    
    try:
        # 保存 Cookie 到文件
        with open(cookie_path, 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, indent=2, ensure_ascii=False)
        
        # 设置文件权限为 600（仅所有者可读写）
        os.chmod(cookie_path, 0o600)
        
        print("✅ Cookie 保存成功!")
        print(f"\n📦 Cookie (脱敏): {mask_cookie(cookie)}")
        print(f"🕐 保存时间：{cookie_data['saved_at']}")
        print(f"📁 文件路径：{cookie_path}")
        print(f"🔒 文件权限：600 (仅所有者可读写)")
        print("\n💡 现在可以使用友盟推送助手功能了")
        print("   示例：查询消息详情 uluzms2177451692046001")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 保存失败：{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
