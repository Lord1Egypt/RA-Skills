#!/usr/bin/env python3
"""微信读书 Cookie 登录工具

方式 1（推荐）：从 Chrome 浏览器提取已登录的 Cookie
  weread_login.py chrome [--profile <profile_path>]

方式 2：手动粘贴 Cookie
  weread_login.py paste

Cookie 存储位置: ~/.weread/cookie
"""

import json
import os
import sys
import sqlite3
import shutil
import tempfile

COOKIE_DIR = os.path.expanduser("~/.weread")
COOKIE_PATH = os.path.join(COOKIE_DIR, "cookie")

DOMAIN = ".weread.qq.com"


def save_cookie(cookie: str):
    os.makedirs(COOKIE_DIR, exist_ok=True)
    with open(COOKIE_PATH, "w") as f:
        f.write(cookie.strip())
    os.chmod(COOKIE_PATH, 0o600)
    print(f"✅ Cookie 已保存到 {COOKIE_PATH}")


def extract_chrome_cookies(profile_path: str | None = None) -> str:
    """从 Chrome Cookies SQLite 提取 weread.qq.com 的 cookie。
    
    注意: macOS 上 Chrome 的 cookie 值是加密的（AES-128-CBC with Keychain），
    这里只能提取未加密的字段。如果值为空则需要用浏览器方式获取。
    """
    if profile_path is None:
        # macOS default Chrome profile
        profile_path = os.path.expanduser(
            "~/Library/Application Support/Google/Chrome/Default"
        )
    
    cookies_db = os.path.join(profile_path, "Cookies")
    if not os.path.exists(cookies_db):
        print(f"❌ Chrome Cookies 数据库不存在: {cookies_db}", file=sys.stderr)
        print("请确认 Chrome 已安装且路径正确。", file=sys.stderr)
        sys.exit(1)

    # 复制到临时文件（Chrome 可能锁定原文件）
    tmp = tempfile.mktemp(suffix=".db")
    shutil.copy2(cookies_db, tmp)

    try:
        conn = sqlite3.connect(tmp)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, value, encrypted_value FROM cookies "
            "WHERE host_key LIKE '%weread.qq.com%'"
        )
        rows = cursor.fetchall()
        conn.close()
    finally:
        os.unlink(tmp)

    if not rows:
        print("❌ 未在 Chrome 中找到 weread.qq.com 的 Cookie。", file=sys.stderr)
        print("请先在 Chrome 中登录 https://weread.qq.com", file=sys.stderr)
        sys.exit(1)

    # macOS Chrome 的 cookie 值通常是加密的
    # 检查是否有未加密的值可用
    parts = []
    encrypted_count = 0
    for name, value, encrypted_value in rows:
        if value:
            parts.append(f"{name}={value}")
        elif encrypted_value:
            encrypted_count += 1
    
    if encrypted_count > 0 and not parts:
        print("⚠️ Chrome Cookie 值已加密（macOS Keychain 保护）。", file=sys.stderr)
        print("请使用以下方式之一获取 Cookie:", file=sys.stderr)
        print("  1. 运行 weread_login.py paste  — 手动从浏览器 DevTools 粘贴", file=sys.stderr)
        print("  2. 运行 weread_login.py browser — 通过 OpenClaw 浏览器自动提取", file=sys.stderr)
        sys.exit(1)

    cookie_str = "; ".join(parts)
    return cookie_str


def paste_cookie():
    """手动粘贴 Cookie"""
    print("请从浏览器 DevTools (F12 → Network → 任意请求 → Headers → Cookie) 复制 Cookie：")
    print("（粘贴后按 Enter）")
    cookie = input().strip()
    if not cookie:
        print("❌ Cookie 不能为空", file=sys.stderr)
        sys.exit(1)
    return cookie


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  weread_login.py chrome [--profile <path>]  从 Chrome 提取 Cookie")
        print("  weread_login.py paste                      手动粘贴 Cookie")
        print("  weread_login.py browser                    通过 OpenClaw 浏览器提取")
        print(f"\nCookie 存储: {COOKIE_PATH}")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "chrome":
        profile = None
        if "--profile" in sys.argv:
            idx = sys.argv.index("--profile")
            if idx + 1 < len(sys.argv):
                profile = sys.argv[idx + 1]
        cookie = extract_chrome_cookies(profile)
        save_cookie(cookie)
        # 验证
        sys.path.insert(0, os.path.dirname(__file__))
        from weread_api import verify_cookie
        if verify_cookie(cookie):
            print("✅ Cookie 验证通过")
        else:
            print("⚠️ Cookie 已保存但验证未通过，可能需要重新登录")

    elif cmd == "paste":
        cookie = paste_cookie()
        save_cookie(cookie)
        sys.path.insert(0, os.path.dirname(__file__))
        from weread_api import verify_cookie
        if verify_cookie(cookie):
            print("✅ Cookie 验证通过")
        else:
            print("⚠️ Cookie 已保存但验证未通过，请检查 Cookie 是否完整")

    elif cmd == "browser":
        # 此模式由 SKILL.md 中 Jarvis 的浏览器工具流程处理
        print("browser 模式需要通过 OpenClaw 浏览器工具执行。")
        print("请让 Jarvis 执行「微信读书登录」流程。")
        sys.exit(0)

    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
