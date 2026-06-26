#!/usr/bin/env python3
"""
友盟推送助手 - 浏览器 Cookie 获取脚本
通过浏览器自动化访问友盟后台并读取 Cookie
"""

import subprocess
import sys
import re

def get_browser_cookie():
    """
    使用浏览器访问友盟推送后台并读取 Cookie
    返回 Cookie 字符串，如果失败则返回 None
    """
    try:
        # 使用浏览器访问页面并执行 JavaScript 获取 Cookie
        js_code = """
        var cookie = document.cookie;
        if (cookie && cookie.includes('ctoken=')) {
            console.log('COOKIE_FOUND:' + cookie);
        } else {
            console.log('NO_CTOKEN_IN_COOKIE');
        }
        """
        
        # 这里需要使用浏览器的 automation API
        # 由于 Python 无法直接调用 MCP 浏览器工具，我们通过标准输出告知调用者
        print("BROWSER_NEEDED", file=sys.stdout)
        print("请访问：https://upush.umeng.com/apps/list")
        print("然后在浏览器控制台执行：document.cookie")
        print("检查是否包含 ctoken 字段")
        
        return None
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        return None

def validate_cookie(cookie_value):
    """
    验证 Cookie 是否有效
    检查是否包含必需的 ctoken 和 umplus_uc_loginid 字段
    """
    if not cookie_value:
        return False, "Cookie 为空"
    
    # 检查是否包含 ctoken
    if 'ctoken=' not in cookie_value:
        return False, "Cookie 中未找到 ctoken 字段，可能未登录或已过期"
    
    # 检查是否包含 umplus_uc_loginid（登录标识）
    if 'umplus_uc_loginid=' not in cookie_value:
        return False, "Cookie 中未找到 umplus_uc_loginid 字段，需要登录后才能使用。请访问 https://upush.umeng.com 登录"
    
    # 提取 ctoken 值进行验证
    match = re.search(r'ctoken=([^;]+)', cookie_value)
    if not match:
        return False, "无法从 Cookie 中提取 ctoken 值"
    
    ctoken = match.group(1).strip()
    if len(ctoken) < 10:
        return False, "ctoken 长度异常，可能已损坏"
    
    return True, "Cookie 验证通过"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "validate":
            cookie = sys.argv[2] if len(sys.argv) > 2 else ""
            is_valid, message = validate_cookie(cookie)
            if is_valid:
                print(f"VALID: {message}")
                sys.exit(0)
            else:
                print(f"INVALID: {message}", file=sys.stderr)
                sys.exit(1)
        elif sys.argv[1] == "get":
            get_browser_cookie()
    else:
        print("用法：python browser_cookie.py [validate|get] [cookie_value]")
        print("  validate <cookie> - 验证 Cookie 是否有效")
        print("  get - 获取浏览器中的 Cookie（需要浏览器支持）")
