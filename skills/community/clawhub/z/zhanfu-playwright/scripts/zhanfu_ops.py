#!/usr/bin/env python3
"""创建店铺 / 改账号 / 下载目录 / 插件 / 清缓存。"""

from __future__ import annotations

import argparse
import json
import platform
import time

import requests

from zhanfu_http import (
    call,
    configure_stdio,
    emit,
    get_mall_by_name,
    preferred_port,
    resolve_mall_id,
    resolve_mall_id_refresh_once,
)


def _need_win(action: str) -> int | None:
    if platform.system() == "Darwin":
        print(f"macOS 暂不支持 {action}")
        return emit({"ok": False, "status": "macos_unsupported", "action": action}, 1)
    return None


def cmd_create(ns: argparse.Namespace) -> int:
    if not ns.mall_name or not ns.platform:
        print("创建店铺需要 --mall-name 与 --platform")
        return emit({"ok": False, "status": "missing_args"}, 1)
    if ns.platform == "自定义平台" and not ns.platform_url:
        print("自定义平台必须提供 --platform-url")
        return emit({"ok": False, "status": "missing_platform_url"}, 1)
    params = {
        "mall_name": ns.mall_name,
        "mall_account": ns.mall_account or "",
        "mall_password": ns.mall_password or "",
        "platform": ns.platform,
        "platform_url": ns.platform_url or "",
        "mall_address": ns.mall_address or "",
        "tags": ns.tags or "",
        "authorizationMember": ns.authorization_member or "",
        "ip_content": ns.ip_content or "",
        "browser_kernel_version": ns.browser_kernel_version,
        "window_ua": "",
        "mac_ua": "",
        "android_ua": "",
        "remark": ns.remark or "",
    }
    port = preferred_port()
    try:
        data = call("CreateBrowser", args=json.dumps(params, ensure_ascii=False), timeout=30, port=port)
    except requests.RequestException:
        print("站斧未打开或无法通讯，请先运行 python scripts/open_zhanfu.py")
        return emit({"ok": False, "status": "zhanfu_down"}, 1)
    ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        msg = ro.get("msg") if isinstance(ro, dict) else data
        print(str(msg))
        return emit({"ok": False, "status": "create_failed", "msg": str(msg)}, 1)
    print("创建成功，等待列表同步 8s")
    time.sleep(8)
    mall_id = get_mall_by_name(ns.mall_name, port=port)
    print(f"店铺 {ns.mall_name} 已创建。mall_id={mall_id}")
    return emit({"ok": True, "status": "created", "mall_name": ns.mall_name, "mall_id": mall_id}, 0)


def cmd_update_account(ns: argparse.Namespace) -> int:
    if ns.username is None and ns.password is None:
        print("请提供 --username 和/或 --password（可显式传空字符串）")
        return emit({"ok": False, "status": "missing_args"}, 1)
    port = preferred_port()
    mall_id = resolve_mall_id(ns.mall_name, port=port)
    body = {
        "username": "" if ns.username is None else ns.username,
        "password": "" if ns.password is None else ns.password,
    }
    data = call(
        "UpdateAccount",
        browser_id=mall_id,
        args=json.dumps(body, ensure_ascii=False),
        timeout=15,
        port=port,
    )
    ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        drop = resolve_mall_id_refresh_once(ns.mall_name, port=port)
        data = call(
            "UpdateAccount",
            browser_id=drop,
            args=json.dumps(body, ensure_ascii=False),
            timeout=15,
            port=port,
        )
        ro = data.get("returnObj") or {}
        mall_id = drop
    if not isinstance(ro, dict) or ro.get("success") is not True:
        msg = ro.get("msg") if isinstance(ro, dict) else data
        print(str(msg))
        return emit({"ok": False, "status": "update_failed", "msg": str(msg)}, 1)
    print(f"已修改店铺 {ns.mall_name} 账号密码。mall_id={mall_id}")
    return emit({"ok": True, "status": "updated", "mall_id": mall_id}, 0)


def cmd_download(ns: argparse.Namespace) -> int:
    blocked = _need_win("SetDownLoadPath")
    if blocked is not None:
        return blocked
    if not ns.file_path:
        print("需要 --file-path")
        return emit({"ok": False, "status": "missing_args"}, 1)
    port = preferred_port()
    data = call(
        "SetDownLoadPath",
        args=json.dumps({"FilePath": ns.file_path}, ensure_ascii=False),
        timeout=15,
        port=port,
    )
    ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        msg = ro.get("msg") if isinstance(ro, dict) else data
        print(str(msg))
        return emit({"ok": False, "status": "failed", "msg": str(msg)}, 1)
    print(f"已设置下载目录: {ns.file_path}")
    return emit({"ok": True, "status": "ok", "FilePath": ns.file_path}, 0)


def cmd_plugins(ns: argparse.Namespace) -> int:
    blocked = _need_win("SetInstallPlugins")
    if blocked is not None:
        return blocked
    if ns.clear:
        plugins: list[dict] = []
    else:
        names = ns.plugin_name or []
        if not names:
            print("需要 --plugin-name，或使用 --clear 清空")
            return emit({"ok": False, "status": "missing_args"}, 1)
        chrome_ids = ns.chrome_id or []
        plugins = []
        for i, name in enumerate(names):
            item: dict = {"plugin_name": name}
            if i < len(chrome_ids):
                item["chrome_id"] = chrome_ids[i]
            plugins.append(item)
    port = preferred_port()
    data = call(
        "SetInstallPlugins",
        args=json.dumps({"installPlugins": plugins}, ensure_ascii=False),
        timeout=15,
        port=port,
    )
    ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        msg = ro.get("msg") if isinstance(ro, dict) else data
        print(str(msg))
        return emit({"ok": False, "status": "failed", "msg": str(msg)}, 1)
    print("已设置店铺插件列表。")
    return emit({"ok": True, "status": "ok", "installPlugins": plugins}, 0)


def cmd_clear_cache(ns: argparse.Namespace) -> int:
    if ns.all:
        blocked = _need_win("ClearCacheFolder")
        if blocked is not None:
            return blocked
        from zhanfu_http import clear_opening_malls

        port = preferred_port()
        data = call("ClearCacheFolder", args="{}", timeout=30, port=port)
        ro = data.get("returnObj") or {}
        if not isinstance(ro, dict) or ro.get("success") is not True:
            msg = ro.get("msg") if isinstance(ro, dict) else data
            print(str(msg))
            return emit({"ok": False, "status": "failed", "msg": str(msg)}, 1)
        clear_opening_malls()
        print("已清除全部店铺缓存。")
        return emit({"ok": True, "status": "cleared_all"}, 0)

    blocked = _need_win("ClearCache")
    if blocked is not None:
        return blocked
    if not ns.mall_name:
        print("单店清缓存需要 --mall-name，或使用 --all")
        return emit({"ok": False, "status": "missing_args"}, 1)
    from zhanfu_http import remove_opening_mall

    port = preferred_port()
    mall_id = resolve_mall_id(ns.mall_name, port=port)
    data = call("ClearCache", browser_id=mall_id, args="", timeout=30, port=port)
    ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        mall_id = resolve_mall_id_refresh_once(ns.mall_name, port=port)
        data = call("ClearCache", browser_id=mall_id, args="", timeout=30, port=port)
        ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        msg = ro.get("msg") if isinstance(ro, dict) else data
        print(str(msg))
        return emit({"ok": False, "status": "failed", "msg": str(msg)}, 1)
    remove_opening_mall(ns.mall_name)
    print(f"已清除店铺 {ns.mall_name} 缓存。mall_id={mall_id}")
    return emit({"ok": True, "status": "cleared", "mall_id": mall_id}, 0)


def main() -> int:
    configure_stdio()
    p = argparse.ArgumentParser(description="站斧其它 HTTP 操作")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create-mall")
    c.add_argument("--mall-name", required=True)
    c.add_argument("--platform", required=True)
    c.add_argument("--platform-url", default="")
    c.add_argument("--ip-content", default="")
    c.add_argument("--mall-account", default="")
    c.add_argument("--mall-password", default="")
    c.add_argument("--mall-address", default="")
    c.add_argument("--tags", default="")
    c.add_argument("--authorization-member", default="")
    c.add_argument("--browser-kernel-version", type=int, default=0)
    c.add_argument("--remark", default="")

    u = sub.add_parser("update-account")
    u.add_argument("--mall-name", required=True)
    u.add_argument("--username", default=None)
    u.add_argument("--password", default=None)

    d = sub.add_parser("set-download")
    d.add_argument("--file-path", required=True)

    g = sub.add_parser("set-plugins")
    g.add_argument("--plugin-name", action="append")
    g.add_argument("--chrome-id", action="append")
    g.add_argument("--clear", action="store_true")

    k = sub.add_parser("clear-cache")
    k.add_argument("--mall-name", default="")
    k.add_argument("--all", action="store_true")

    ns = p.parse_args()
    if ns.cmd == "create-mall":
        return cmd_create(ns)
    if ns.cmd == "update-account":
        return cmd_update_account(ns)
    if ns.cmd == "set-download":
        return cmd_download(ns)
    if ns.cmd == "set-plugins":
        return cmd_plugins(ns)
    if ns.cmd == "clear-cache":
        return cmd_clear_cache(ns)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
