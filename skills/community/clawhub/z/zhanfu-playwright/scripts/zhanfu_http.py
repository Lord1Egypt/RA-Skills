#!/usr/bin/env python3
"""站斧 WebDriver HTTP 公共库。browserId 一律转成字符串。"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import requests

API_DEFAULT_PORT = 12678
HTTP_PROBE_TIMEOUT = 1.5
OPEN_MALL_FAIL_HINT = (
    "打开店铺失败，请确认该店铺是否已绑定 IP / 设备。"
    "首次使用请先在站斧客户端手动打开该店铺以下载内核。"
)
MAC_UNSUPPORTED = (
    "SetDownLoadPath",
    "ClearCacheFolder",
    "ClearCache",
    "SetInstallPlugins",
)


def configure_stdio() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def is_mac() -> bool:
    return platform.system() == "Darwin"


def skill_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def load_json(path: str) -> dict[str, Any]:
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_json(path: str, data: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def preferred_port() -> int:
    try:
        port = int(load_json(os.path.join(skill_dir(), "api_port.json")).get("api_port", API_DEFAULT_PORT))
        return port if port > 0 else API_DEFAULT_PORT
    except (TypeError, ValueError):
        return API_DEFAULT_PORT


def mall_cache_path() -> str:
    return os.path.join(skill_dir(), "mall_cache.json")


def load_mall_map() -> dict[str, str]:
    data = load_json(mall_cache_path())
    mall_map = data.get("mall_map")
    if not isinstance(mall_map, dict):
        return {}
    return {str(k): str(v) for k, v in mall_map.items()}


def save_mall_map(mall_map: dict[str, str]) -> None:
    write_json(mall_cache_path(), {"mall_map": mall_map, "updated_at": now_iso()})


def save_mall_to_cache(mall_name: str, mall_id: str) -> None:
    mall_map = load_mall_map()
    mall_map[mall_name] = str(mall_id)
    save_mall_map(mall_map)
    print(f"[缓存] {mall_name} → {mall_id}")


def save_malls_to_cache(malls: list[dict[str, Any]]) -> None:
    mall_map = load_mall_map()
    changed = False
    for mall in malls:
        name, mall_id = mall.get("mall_name"), mall.get("mall_id")
        if name is None or mall_id is None:
            continue
        key, value = str(name), str(mall_id)
        if mall_map.get(key) != value:
            mall_map[key] = value
            changed = True
    if changed:
        save_mall_map(mall_map)
        print(f"[缓存] 已从列表更新 mall_cache.json（共 {len(mall_map)} 条）")


def drop_mall_cache(mall_name: str) -> None:
    mall_map = load_mall_map()
    if mall_name in mall_map:
        del mall_map[mall_name]
        save_mall_map(mall_map)
        print(f"[缓存] 已删除过期条目: {mall_name}")


def opening_malls_path() -> str:
    return os.path.join(skill_dir(), "opening_malls.json")


def load_opening_malls() -> list[str]:
    malls = load_json(opening_malls_path()).get("malls")
    if not isinstance(malls, list):
        return []
    return [str(name) for name in malls if name]


def write_opening_malls(malls: list[str]) -> None:
    write_json(
        opening_malls_path(),
        {"malls": list(dict.fromkeys(malls)), "updated_at": now_iso()},
    )


def add_opening_mall(mall_name: str) -> None:
    malls = load_opening_malls()
    if mall_name in malls:
        return
    malls.append(mall_name)
    write_opening_malls(malls)
    print(f"[打开意图] 已写入: {mall_name}")


def remove_opening_mall(mall_name: str) -> None:
    malls = [n for n in load_opening_malls() if n != mall_name]
    write_opening_malls(malls)


def clear_opening_malls() -> None:
    write_opening_malls([])
    print("[打开意图] 已清空 opening_malls.json")


def emit(result: dict[str, Any], code: int) -> int:
    print("RESULT_JSON=" + json.dumps(result, ensure_ascii=False))
    return code


def call(
    action: str,
    *,
    browser_id: str = "",
    args: str = "",
    timeout: float = 8,
    port: Optional[int] = None,
) -> dict[str, Any]:
    if is_mac() and action in MAC_UNSUPPORTED:
        raise RuntimeError(f"macOS 暂不支持 {action}")
    api_port = preferred_port() if port is None else int(port)
    bid = "" if browser_id in (None, "") else str(browser_id)
    payload = {
        "module": "WebDriverModule",
        "action": action,
        "browserId": bid,
        "args": args,
    }
    resp = requests.post(
        f"http://127.0.0.1:{api_port}",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=timeout,
    )
    if not resp.text:
        raise RuntimeError(f"{action} 空响应 HTTP {resp.status_code}")
    return json.loads(resp.text)


def get_mall_by_name(mall_name: str, port: Optional[int] = None) -> str:
    data = call("GetMallByName", args=json.dumps({"mallName": mall_name}, ensure_ascii=False), port=port)
    ro = data.get("returnObj") or {}
    if not isinstance(ro, dict) or ro.get("success") is not True:
        msg = ro.get("msg") if isinstance(ro, dict) else data
        raise RuntimeError(f"GetMallByName 失败: {msg}")
    mall_id = (ro.get("data") or {}).get("mall_id")
    if mall_id is None:
        raise RuntimeError("GetMallByName 未返回 mall_id")
    mall_id_str = str(mall_id)
    save_mall_to_cache(mall_name, mall_id_str)
    return mall_id_str


def resolve_mall_id(mall_name: str, *, use_cache: bool = True, port: Optional[int] = None) -> str:
    if use_cache:
        cached = load_mall_map().get(mall_name)
        if cached:
            print(f"[店铺] 命中缓存 mall_id={cached} ({mall_name})")
            return cached
    mall_id = get_mall_by_name(mall_name, port=port)
    print(f"[店铺] mall_id={mall_id} ({mall_name})")
    return mall_id


def resolve_mall_id_refresh_once(mall_name: str, port: Optional[int] = None) -> str:
    drop_mall_cache(mall_name)
    return resolve_mall_id(mall_name, use_cache=False, port=port)
