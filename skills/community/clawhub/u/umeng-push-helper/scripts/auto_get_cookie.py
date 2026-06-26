#!/usr/bin/env python3
"""
友盟推送助手 - 自动获取浏览器 Cookie 脚本
通过 MCP 浏览器工具访问友盟后台并读取 Cookie
"""

import subprocess
import sys
import os
import re

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from manage_cookie import save_cookie, validate_cookie

def get_browser_cookie():
    """
    使用 MCP 浏览器工具访问友盟推送后台并读取 Cookie
    
    返回:
        tuple: (success: bool, cookie: str or None, message: str)
    """
    try:
        # 步骤 1: 导航到友盟推送后台
        print("正在打开浏览器访问友盟推送后台...")
        
        # 使用 mcp__builtin_browser__navigate 工具
        navigate_result = subprocess.run(
            ['mcp', 'tool', 'call', 'mcp__builtin_browser__navigate', 
             '{"url": "https://upush.umeng.com/apps/list"}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if navigate_result.returncode != 0:
            return False, None, f"打开浏览器失败：{navigate_result.stderr}"
        
        print("✓ 页面已加载")
        
        # 等待页面完全加载
        import time
        time.sleep(2)
        
        # 步骤 2: 执行 JavaScript 获取 Cookie
        print("正在读取浏览器 Cookie...")
        
        js_code = "document.cookie"
        cookie_result = subprocess.run(
            ['mcp', 'tool', 'call', 'mcp__builtin_browser__evaluate',
             f'{{"expression": "{js_code}"}}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if cookie_result.returncode != 0:
            return False, None, f"读取 Cookie 失败：{cookie_result.stderr}"
        
        cookie_value = cookie_result.stdout.strip()
        
        if not cookie_value:
            return False, None, "Cookie 为空，可能未登录"
        
        # 步骤 3: 验证 Cookie
        print("正在验证 Cookie...")
        is_valid, message = validate_cookie(cookie_value)
        
        if not is_valid:
            # 特殊处理：如果缺少 umplus_uc_loginid，提示用户需要登录
            if 'umplus_uc_loginid' in message:
                return False, None, f"检测到您尚未登录友盟账号。请先访问 https://upush.umeng.com 完成登录，然后重试。"
            return False, None, f"Cookie 验证失败：{message}"
        
        print(f"✓ Cookie 验证通过：{message}")
        
        # 步骤 4: 保存 Cookie
        save_cookie(cookie_value)
        
        return True, cookie_value, "Cookie 已成功获取并保存"
        
    except subprocess.TimeoutExpired:
        return False, None, "操作超时，请重试"
    except Exception as e:
        return False, None, f"发生错误：{str(e)}"

def check_login_status():
    """
    检查用户是否已登录友盟后台
    
    返回:
        bool: 是否已登录
    """
    try:
        # 检查当前页面的 URL 或内容
        check_result = subprocess.run(
            ['mcp', 'tool', 'call', 'mcp__builtin_browser__snapshot'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if check_result.returncode == 0:
            snapshot = check_result.stdout
            # 检查是否包含登录相关的元素
            if '登录' in snapshot or 'login' in snapshot.lower():
                return False
        
        return True
        
    except Exception:
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("友盟推送助手 - Cookie 自动获取工具")
    print("=" * 60)
    print()
    
    # 检查是否已保存 Cookie
    cookie_file = os.path.expanduser("~/.qoderwork/skills/umeng-push-helper/cookie.txt")
    if os.path.exists(cookie_file):
        print(f"提示：已存在保存的 Cookie 文件：{cookie_file}")
        response = input("是否重新获取？(y/n): ").strip().lower()
        if response != 'y':
            print("已取消操作")
            sys.exit(0)
    
    print()
    print("请确保：")
    print("1. 您已登录友盟账号 (https://upush.umeng.com)")
    print("2. 浏览器可以正常访问该网站")
    print()
    
    input("按回车键继续...")
    print()
    
    # 获取 Cookie
    success, cookie, message = get_browser_cookie()
    
    print()
    print("=" * 60)
    if success:
        print(f"✓ 成功：{message}")
        print()
        print("Cookie 已保存到：", cookie_file)
        print()
        print("您现在可以使用以下命令：")
        print("  python scripts/get_app_list.py     - 获取应用列表")
        print("  python scripts/query_app_data.py <appkey> - 查询应用数据")
    else:
        print(f"✗ 失败：{message}")
        print()
        print("您可以尝试：")
        print("1. 手动登录 https://upush.umeng.com")
        print("2. 在浏览器控制台执行：document.cookie")
        print("3. 复制输出结果并使用以下命令保存：")
        print("   python scripts/manage_cookie.py save \"<cookie_value>\"")
    print("=" * 60)
