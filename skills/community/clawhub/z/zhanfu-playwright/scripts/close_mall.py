#!/usr/bin/env python3
"""关闭指定店铺（CloseBrowser）。HTTP 正常时不重启站斧。"""

from __future__ import annotations

import argparse

import requests

from zhanfu_http import (
    call,
    configure_stdio,
    emit,
    preferred_port,
    remove_opening_mall,
    resolve_mall_id,
    resolve_mall_id_refresh_once,
)


def close_one(mall_name: str, mall_id: str, port: int) -> object:
    data = call("CloseBrowser", browser_id=mall_id, timeout=15, port=port)
    return data.get("returnObj")


def main() -> int:
    configure_stdio()
    p = argparse.ArgumentParser(description="关闭店铺")
    p.add_argument("--mall-name", required=True)
    ns = p.parse_args()
    mall_name = ns.mall_name.strip()
    port = preferred_port()
    try:
        mall_id = resolve_mall_id(mall_name, port=port)
    except requests.RequestException:
        print("站斧未打开或无法通讯，请先运行 python scripts/open_zhanfu.py")
        return emit({"ok": False, "status": "zhanfu_down"}, 1)
    except RuntimeError as exc:
        print(str(exc))
        return emit({"ok": False, "status": "resolve_failed", "msg": str(exc)}, 1)

    ro = close_one(mall_name, mall_id, port)
    if ro is False:
        mall_id = resolve_mall_id_refresh_once(mall_name, port=port)
        ro = close_one(mall_name, mall_id, port)
    if ro is not None:
        print(f"关闭店铺失败: returnObj={ro!r}")
        return emit({"ok": False, "status": "close_failed", "mall_id": mall_id, "returnObj": ro}, 1)

    remove_opening_mall(mall_name)
    print(f"店铺 {mall_name} 已关闭。mall_id={mall_id}")
    return emit({"ok": True, "status": "closed", "mall_name": mall_name, "mall_id": mall_id}, 0)


if __name__ == "__main__":
    raise SystemExit(main())
