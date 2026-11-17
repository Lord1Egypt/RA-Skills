#!/usr/bin/env python3
"""WPS/金山文档 连接器 — 授权脚本（Hermes 版）

流程（与 WorkBuddy kdocs 连接器一致，服务端同一套接口）：
  1. 生成 auth_code（uuid4）
  2. 打开 https://mcp-center.wps.cn/kdocs-auth/auth-guide?auth_code=<code>
  3. 用户用 **WPS 个人账号** 登录（企业账号会被拒，返回 403）
  4. 轮询 POST https://api.wps.cn/office/v5/ai/skill_hub/wps_auth/exchange 拿 token
  5. token 写入 ~/.hermes/.env 的 WPS_KDOCS_TOKEN=（0600）

用法：
  python3 wps_auth.py            # 授权并写入 token（自动开浏览器）
  python3 wps_auth.py --no-open  # 只打印链接，不自动开浏览器
  python3 wps_auth.py --url      # 只生成链接并退出（不轮询）

注意：企业 WPS 账号不支持；需切到个人账号。
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

AUTH_GUIDE = "https://mcp-center.wps.cn/kdocs-auth/auth-guide?auth_code={code}"
EXCHANGE = "https://api.wps.cn/office/v5/ai/skill_hub/wps_auth/exchange"
ENV_FILE = os.environ.get("WPS_KDOCS_ENV_FILE", "wps_kdocs.env")
TOKEN_KEY = "WPS_KDOCS_TOKEN"
TIMEOUT = 300
INTERVAL = 1


def exchange(code: str) -> dict:
    body = json.dumps({"code": code}).encode()
    req = urllib.request.Request(EXCHANGE, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8", "replace"))
        except Exception:  # noqa: BLE001
            return {"code": e.code}
    except Exception as e:  # noqa: BLE001
        return {"code": "neterr", "msg": str(e)}


def save_token(token: str) -> None:
    os.makedirs(os.path.dirname(ENV_FILE), exist_ok=True)
    lines: list[str] = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    out, replaced = [], False
    for line in lines:
        if re.match(rf"^{TOKEN_KEY}\s*=", line):
            out.append(f"{TOKEN_KEY}={token}")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(f"{TOKEN_KEY}={token}")
    with open(ENV_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    os.chmod(ENV_FILE, 0o600)


def open_url(url: str) -> bool:
    import webbrowser
    return webbrowser.open(url, autoraise=True)
    return False


def main() -> int:
    argv = sys.argv[1:]
    code = str(uuid.uuid4())
    url = AUTH_GUIDE.format(code=code)

    print("=" * 62)
    print("  WPS 授权 - 获取 skill_hub token（Hermes WPS 连接器）")
    print("=" * 62)
    print()
    print("请在浏览器打开并在 **WPS 个人账号** 下登录：")
    print()
    print(f"  {url}")
    print()
    print(f"auth_code: {code}")
    print("=" * 62)

    if "--url" in argv:
        return 0
    if "--no-open" not in argv:
        if open_url(url):
            print("已尝试自动打开浏览器…")
        else:
            print("未能自动打开浏览器，请手动复制上方链接。")
    print()
    print(f"等待登录…（轮询 {INTERVAL}s，最长 {TIMEOUT}s）")

    start = time.time()
    last_dot = -1
    while True:
        elapsed = int(time.time() - start)
        if elapsed >= TIMEOUT:
            print("\n超时未登录。可重跑：python3 wps_auth.py")
            return 1
        resp = exchange(code)
        code_field = str(resp.get("code", ""))
        data = resp.get("data") or {}
        token = data.get("token") or resp.get("token")
        if code_field == "200" and token:
            save_token(token)
            expires = data.get("expires_in") or resp.get("expires_in") or 0
            print("登录成功。")
            print(f"token 已写入 {ENV_FILE}（{TOKEN_KEY}）")
            print(f"有效期约 {int(expires) // 3600} 小时")
            print(f"token 摘要: {token[:8]}…")
            return 0
        if code_field == "403":
            print("\n授权被拒：当前是 WPS 企业账号，本连接器只支持个人账号。")
            print("请切换到 WPS 个人账号后重跑本脚本。")
            return 3
        if code_field == "409":
            print("\n授权已取消（409）。如需继续请重跑本脚本。")
            return 4
        if code_field == "202":
            if elapsed % 5 == 0 and elapsed != last_dot:
                print(".", end="", flush=True)
                last_dot = elapsed
        elif code_field and not code_field.startswith("5") and code_field != "neterr":
            print(f"\n授权失败：{resp}")
            return 1
        time.sleep(INTERVAL)


if __name__ == "__main__":
    sys.exit(main())
