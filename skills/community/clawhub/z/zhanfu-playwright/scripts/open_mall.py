#!/usr/bin/env python3
"""打开店铺：已开则跳过 OpenBrowser，未开则打开并返回 WebDriverPort。"""

from __future__ import annotations

import argparse
import json
import time

import requests

from zhanfu_http import (
    OPEN_MALL_FAIL_HINT,
    add_opening_mall,
    call,
    configure_stdio,
    emit,
    preferred_port,
    resolve_mall_id,
    resolve_mall_id_refresh_once,
)


def probe_webdriver(mall_id: str, port: int) -> tuple[bool, dict]:
    print(f"[探测] GetBrowserWebDriver 单次 timeout=5s mall_id={mall_id}")
    try:
        data = call("GetBrowserWebDriver", browser_id=mall_id, timeout=5, port=port)
    except (requests.RequestException, json.JSONDecodeError, RuntimeError) as exc:
        print(f"[探测] 超时/异常，视为未开: {exc}")
        return False, {}
    ro = data.get("returnObj") or {}
    wd = ro.get("WebDriverPort") if isinstance(ro, dict) else None
    if isinstance(ro, dict) and ro.get("success") is True and wd:
        return True, ro
    return False, ro if isinstance(ro, dict) else {}


def open_browser(mall_id: str, port: int) -> None:
    args = json.dumps(
        {
            "isDownLoadConfirm": False,
            "isOpenMallIndex": True,
            "isSwitchDynamicNetwork": False,
        },
        ensure_ascii=False,
    )
    data = call("OpenBrowser", browser_id=mall_id, args=args, timeout=30, port=port)
    if data.get("ret") != 200 or data.get("returnObj") is not True:
        raise RuntimeError(f"OpenBrowser 失败: {data.get('returnObj')!r}。{OPEN_MALL_FAIL_HINT}")
    print("[打开] OpenBrowser 成功，等待 10s")
    time.sleep(10)


def fetch_webdriver(mall_id: str, port: int) -> dict:
    data = call("GetBrowserWebDriver", browser_id=mall_id, timeout=15, port=port)
    ro = data.get("returnObj") or {}
    wd = ro.get("WebDriverPort") if isinstance(ro, dict) else None
    if not (isinstance(ro, dict) and ro.get("success") is True and wd):
        raise RuntimeError(f"未获取到 WebDriverPort: {ro}。{OPEN_MALL_FAIL_HINT}")
    return ro


def run(mall_name: str) -> int:
    port = preferred_port()
    try:
        mall_id = resolve_mall_id(mall_name, port=port)
    except requests.RequestException:
        print("站斧未打开或无法通讯，请先运行 python scripts/open_zhanfu.py")
        return emit({"ok": False, "status": "zhanfu_down"}, 1)
    except RuntimeError as exc:
        print(str(exc))
        return emit({"ok": False, "status": "resolve_failed", "msg": str(exc)}, 1)

    add_opening_mall(mall_name)
    opened, ro = probe_webdriver(mall_id, port)
    if opened:
        wd = int(ro["WebDriverPort"])
        kernel = ro.get("KernalNumber")
        print(f"店铺 {mall_name} 已打开，未重复执行 OpenBrowser。")
        print(f"mall_id={mall_id}")
        print(f"WebDriverPort={wd}")
        return emit(
            {
                "ok": True,
                "status": "already_open",
                "mall_name": mall_name,
                "mall_id": mall_id,
                "WebDriverPort": wd,
                "KernalNumber": kernel,
            },
            0,
        )

    try:
        open_browser(mall_id, port)
    except RuntimeError as exc:
        print(str(exc))
        try:
            mall_id = resolve_mall_id_refresh_once(mall_name, port=port)
            open_browser(mall_id, port)
        except Exception as exc2:
            print(str(exc2))
            return emit({"ok": False, "status": "open_failed", "msg": str(exc2)}, 1)

    try:
        ro = fetch_webdriver(mall_id, port)
    except RuntimeError as exc:
        print(str(exc))
        return emit({"ok": False, "status": "no_webdriver_port", "msg": str(exc)}, 1)

    wd = int(ro["WebDriverPort"])
    kernel = ro.get("KernalNumber")
    print(f"店铺 {mall_name} 已打开。")
    print(f"mall_id={mall_id}")
    print(f"WebDriverPort={wd}")
    return emit(
        {
            "ok": True,
            "status": "opened",
            "mall_name": mall_name,
            "mall_id": mall_id,
            "WebDriverPort": wd,
            "KernalNumber": kernel,
        },
        0,
    )


def main() -> int:
    configure_stdio()
    p = argparse.ArgumentParser(description="打开店铺并返回 WebDriverPort；已开则跳过 OpenBrowser")
    p.add_argument("--mall-name", required=True, help="店铺名")
    ns = p.parse_args()
    return run(ns.mall_name.strip())


if __name__ == "__main__":
    raise SystemExit(main())
