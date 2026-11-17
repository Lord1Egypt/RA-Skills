#!/usr/bin/env python3
"""获取店铺列表（GetBrowserList），并写入 mall_cache.json。"""

from __future__ import annotations

import argparse
import json

import requests

from zhanfu_http import call, configure_stdio, emit, preferred_port, save_malls_to_cache


def main() -> int:
    configure_stdio()
    p = argparse.ArgumentParser(description="获取店铺列表")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--limit", type=int, default=10)
    ns = p.parse_args()
    port = preferred_port()
    try:
        data = call(
            "GetBrowserList",
            args=json.dumps({"page": ns.page, "limit": ns.limit}),
            timeout=8,
            port=port,
        )
    except requests.RequestException:
        print("站斧未打开或无法通讯，请先运行 python scripts/open_zhanfu.py")
        return emit({"ok": False, "status": "zhanfu_down"}, 1)

    ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        msg = ro.get("msg") if isinstance(ro, dict) else data
        print(f"GetBrowserList 失败: {msg}")
        return emit({"ok": False, "status": "list_failed", "msg": str(msg)}, 1)

    info = ro.get("data") or {}
    malls = info.get("mall_list")
    if malls is None:
        print("站斧未登录，请提供账号和密码")
        return emit({"ok": False, "status": "need_login", "msg": "站斧未登录，请提供账号和密码"}, 2)

    save_malls_to_cache(malls if isinstance(malls, list) else [])
    total = info.get("total")
    print(f"店铺列表 第{ns.page}页 每页{ns.limit} 共{total}个")
    for mall in malls or []:
        print(
            f"- {mall.get('mall_name')}  id={mall.get('mall_id')}  "
            f"平台={mall.get('platform_name')}  IP={mall.get('ip_address')}"
        )
    return emit(
        {
            "ok": True,
            "status": "ok",
            "page": ns.page,
            "limit": ns.limit,
            "total": total,
            "mall_list": malls,
        },
        0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
