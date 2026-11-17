#!/usr/bin/env python3
"""登录站斧。仅使用命令行当场提供的账号密码，isboss 固定 true。"""

from __future__ import annotations

import argparse
import json

import requests

from zhanfu_http import call, configure_stdio, emit, preferred_port, save_malls_to_cache


def main() -> int:
    configure_stdio()
    p = argparse.ArgumentParser(description="Login（禁止猜测账号）")
    p.add_argument("--username", required=True)
    p.add_argument("--password", required=True)
    ns = p.parse_args()
    if not ns.username or not ns.password:
        print("缺少账号或密码")
        return emit({"ok": False, "status": "missing_credentials"}, 1)
    port = preferred_port()
    try:
        data = call(
            "Login",
            args=json.dumps(
                {"username": ns.username, "password": ns.password, "isboss": True},
                ensure_ascii=False,
            ),
            timeout=15,
            port=port,
        )
    except requests.RequestException:
        print("站斧未打开或无法通讯，请先运行 python scripts/open_zhanfu.py")
        return emit({"ok": False, "status": "zhanfu_down"}, 1)

    ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        msg = ro.get("msg") if isinstance(ro, dict) else data
        print(str(msg))
        return emit({"ok": False, "status": "login_failed", "msg": str(msg)}, 1)

    listed = call("GetBrowserList", args=json.dumps({"page": 1, "limit": 20}), timeout=8, port=port)
    info = ((listed.get("returnObj") or {}).get("data") or {})
    save_malls_to_cache(info.get("mall_list") or [])
    print("登录成功。")
    return emit({"ok": True, "status": "logged_in", "api_port": port}, 0)


if __name__ == "__main__":
    raise SystemExit(main())
