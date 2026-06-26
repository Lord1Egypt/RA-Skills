#!/usr/bin/env python3
"""
友盟推送助手 - Cookie 管理脚本
用于保存、验证和管理 Cookie
"""

import os
import sys
import re

COOKIE_FILE = os.path.expanduser("~/.qoderwork/skills/umeng-push-helper/cookie.txt")

def save_cookie(cookie_value):
    """保存 Cookie 到文件"""
    os.makedirs(os.path.dirname(COOKIE_FILE), exist_ok=True)
    with open(COOKIE_FILE, 'w') as f:
        f.write(cookie_value.strip())
    print(f"✓ Cookie 已保存到：{COOKIE_FILE}")

def load_cookie():
    """从文件加载 Cookie"""
    if not os.path.exists(COOKIE_FILE):
        return None
    with open(COOKIE_FILE, 'r') as f:
        return f.read().strip()

def check_cookie_exists():
    """检查 Cookie 是否存在"""
    return os.path.exists(COOKIE_FILE)

def validate_cookie(cookie_value):
    """
    验证 Cookie 是否有效
    检查是否包含必需的 ctoken 字段
    """
    if not cookie_value:
        return False, "Cookie 为空"
    
    # 检查是否包含 ctoken
    if 'ctoken=' not in cookie_value:
        return False, "Cookie 中未找到 ctoken 字段，可能未登录或已过期"
    
    # 提取 ctoken 值进行验证
    match = re.search(r'ctoken=([^;]+)', cookie_value)
    if not match:
        return False, "无法从 Cookie 中提取 ctoken 值"
    
    ctoken = match.group(1).strip()
    if len(ctoken) < 10:
        return False, "ctoken 长度异常，可能已损坏"
    
    return True, f"Cookie 验证通过 (ctoken: {ctoken[:10]}...)"

def extract_ctoken(cookie_value):
    """从 Cookie 中提取 ctoken 值"""
    if not cookie_value:
        return None
    match = re.search(r'ctoken=([^;]+)', cookie_value)
    if match:
        return match.group(1).strip()
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "save" and len(sys.argv) > 2:
            # 先验证 Cookie
            is_valid, message = validate_cookie(sys.argv[2])
            if is_valid:
                save_cookie(sys.argv[2])
                print(f"✓ 验证：{message}")
            else:
                print(f"✗ 验证失败：{message}", file=sys.stderr)
                sys.exit(1)
        elif sys.argv[1] == "load":
            cookie = load_cookie()
            if cookie:
                print(cookie)
            else:
                print("NO_COOKIE", file=sys.stderr)
                sys.exit(1)
        elif sys.argv[1] == "check":
            if check_cookie_exists():
                print("EXISTS")
            else:
                print("NOT_EXISTS")
        elif sys.argv[1] == "validate" and len(sys.argv) > 2:
            is_valid, message = validate_cookie(sys.argv[2])
            if is_valid:
                print(f"VALID: {message}")
            else:
                print(f"INVALID: {message}", file=sys.stderr)
                sys.exit(1)
        elif sys.argv[1] == "extract-ctoken" and len(sys.argv) > 2:
            ctoken = extract_ctoken(sys.argv[2])
            if ctoken:
                print(ctoken)
            else:
                print("NO_CTOKEN", file=sys.stderr)
                sys.exit(1)
    else:
        print("用法：python manage_cookie.py <command> [arguments]")
        print("命令:")
        print("  save <cookie>     - 保存 Cookie（会自动验证）")
        print("  load              - 加载已保存的 Cookie")
        print("  check             - 检查 Cookie 文件是否存在")
        print("  validate <cookie> - 验证 Cookie 是否有效")
        print("  extract-ctoken <cookie> - 从 Cookie 中提取 ctoken 值")
