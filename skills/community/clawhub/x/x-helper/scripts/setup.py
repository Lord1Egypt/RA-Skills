"""
X Helper — 环境检查脚本。

检查：
1. Python 3 可用
2. x_client.py / x_auth.py 存在
3. 认证状态（读取本地 token 文件 + 发送 API 请求验证 token 有效性）
4. 网络连通性（可选）

只读检查，不修改任何文件。认证验证会向 api.x.com 发送 HTTPS 请求。
"""

import json
import os
import shutil
import subprocess
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUTH_SCRIPT = os.path.join(SCRIPT_DIR, "x_auth.py")
CLIENT_SCRIPT = os.path.join(SCRIPT_DIR, "x_client.py")
AUTH_FILE = os.path.expanduser("~/.x-helper/auth.json")


def check(label, ok, hint=""):
    icon = "✓" if ok else "✗"
    print(f"  {icon} {label}")
    if not ok and hint:
        print(f"     {hint}")


def main():
    print("X Helper — Setup Check")
    print()

    # 1. Python 3
    py_ok = sys.version_info >= (3, 7)
    check(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
          py_ok, "需要 Python 3.7+")

    # 2. Script files exist
    check("x_auth.py 存在", os.path.isfile(AUTH_SCRIPT))
    check("x_client.py 存在", os.path.isfile(CLIENT_SCRIPT))

    # 3. npx (optional, for reference)
    npx_path = shutil.which("npx")
    check("npx 可用（可选）", npx_path is not None, "不需要 npx，本 skill 使用纯 Python 实现")

    # 4. Auth status
    auth_ok = False
    if os.path.isfile(AUTH_FILE):
        try:
            with open(AUTH_FILE) as f:
                auth = json.load(f)
            has_token = bool(auth.get("access_token"))
            has_refresh = bool(auth.get("refresh_token"))
            has_user = bool(auth.get("username"))
            auth_ok = has_token and has_refresh and has_user
            check("已认证", auth_ok)
            if auth_ok:
                print(f"     用户: @{auth.get('username')} ({auth.get('user_name')})")
                expires = auth.get("expires_at", 0)
                remaining = max(0, expires - int(__import__('time').time()))
                print(f"     Token 剩余: {remaining // 60} 分钟")
            else:
                missing = []
                if not has_token: missing.append("access_token")
                if not has_refresh: missing.append("refresh_token（建议重新授权）")
                if not has_user: missing.append("用户信息")
                if auth:
                    check("认证文件不完整", False, f"缺少: {', '.join(missing)}")
                else:
                    check("认证文件格式错误", False, "请重新运行 auth authorize")
        except (json.JSONDecodeError, OSError) as e:
            check("认证文件读取失败", False, str(e))
    else:
        check("未认证", False, "运行: python3 scripts/x_client.py auth authorize --client-id YOUR_CLIENT_ID")

    # 5. Check env for CLIENT_ID
    env_id = os.environ.get("X_CLIENT_ID", "")
    if env_id:
        check("X_CLIENT_ID 环境变量已设置", True)
    else:
        check("X_CLIENT_ID 环境变量未设置", True,
              "授权时通过 --client-id 传入即可，不需要设置环境变量")

    # 6. Test auth if authenticated
    if auth_ok:
        print()
        print("  测试认证...")
        try:
            result = subprocess.run(
                [sys.executable, CLIENT_SCRIPT, "auth", "status"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print(f"  ✓ 认证有效")
            else:
                print(f"  ✗ 认证无效: {result.stderr.strip()}")
        except Exception as e:
            print(f"  ✗ 检查失败: {e}")

    print()
    if auth_ok:
        print("  ✅ 一切就绪，开始使用 X Helper！")
        print("     试试: python3 scripts/x_client.py user me")
    else:
        print("  ❌ 需要先完成授权")
        print("     运行: python3 scripts/x_client.py auth authorize --client-id YOUR_CLIENT_ID")
    print()


if __name__ == "__main__":
    main()
