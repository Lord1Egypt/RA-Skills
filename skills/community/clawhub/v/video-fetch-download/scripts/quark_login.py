#!/usr/bin/env python3
"""
夸克网盘 Cookie 配置向导
用法: python3 quark_login.py
"""
import os
import sys
import requests

COOKIE_DIR = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
    "video-fetch"
)
COOKIE_FILE = os.path.join(COOKIE_DIR, "quark_cookie.txt")

BASE_URL = "https://drive-pc.quark.cn"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) quark-cloud-drive/3.14.2 Chrome/112.0.5615.165 "
    "Electron/24.1.3.8 Safari/537.36 Channel/pckk_other_ch"
)


# Security note:
# - The Quark cookie is stored locally at ~/.config/video-fetch/quark_cookie.txt (chmod 600)
# - The cookie is NEVER transmitted to any third party — only used to authenticate with Quark Pan API
# - The cookie is extracted manually by the user from their own browser session
# - No credentials are logged or printed to console

def verify_cookie(cookie):
    """验证 Cookie 是否有效"""
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT, "Cookie": cookie})
    try:
        r = s.get(f"{BASE_URL}/1/clouddrive/config",
                  params={"pr": "ucpro", "fr": "pc"}, timeout=10)
        data = r.json()
        if data.get("code") == 0:
            # 尝试获取用户信息
            account = data.get("data", {}).get("account", {})
            nickname = account.get("nickname", "") or account.get("phone", "未知用户")
            return True, nickname
        return False, data.get("message", "验证失败")
    except Exception as e:
        return False, str(e)


def save_cookie(cookie):
    os.makedirs(COOKIE_DIR, exist_ok=True)
    with open(COOKIE_FILE, "w") as f:
        f.write(cookie.strip())
    os.chmod(COOKIE_FILE, 0o600)  # 仅当前用户可读


def main():
    print()
    print("══════════════════════════════════════")
    print("  夸克网盘 Cookie 配置向导")
    print("══════════════════════════════════════")
    print()
    print("夸克网盘不支持扫码登录，需要手动提取 Cookie。")
    print("Cookie 有效期通常为数月，无需频繁更新。")
    print()
    print("获取步骤：")
    print("  1. 浏览器打开 https://pan.quark.cn 并登录")
    print("  2. 按 F12 → Network 标签")
    print("  3. 刷新页面，点击任意 quark.cn 请求")
    print("  4. 在 Request Headers 里找到 'cookie' 字段")
    print("  5. 复制完整 cookie 值（很长，包含多个 key=value）")
    print()

    # 检查是否已有 Cookie
    if os.path.exists(COOKIE_FILE):
        print(f"[提示] 已有 Cookie 文件: {COOKIE_FILE}")
        ans = input("是否重新配置? [y/N] ").strip().lower()
        if ans != "y":
            ok, info = verify_cookie(open(COOKIE_FILE).read().strip())
            if ok:
                print(f"✓ Cookie 有效，用户: {info}")
            else:
                print(f"✗ Cookie 已失效: {info}，请重新配置")
                main()
            return

    print("请粘贴 Cookie 内容（回车确认）：")
    print("> ", end="", flush=True)
    cookie = input().strip()

    if not cookie:
        print("未输入 Cookie，退出")
        sys.exit(1)

    print()
    print("验证 Cookie...", flush=True)
    ok, info = verify_cookie(cookie)

    if ok:
        save_cookie(cookie)
        print(f"✓ Cookie 有效，用户: {info}")
        print(f"✓ 已保存到: {COOKIE_FILE}")
        print()
        print("现在可以使用:")
        print("  python3 scripts/quark_offline.py 'magnet:?xt=...'")
    else:
        print(f"✗ Cookie 无效: {info}")
        print("请检查是否复制完整，然后重试")
        sys.exit(1)


if __name__ == "__main__":
    main()
