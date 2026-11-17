#!/usr/bin/env python3
"""打开站斧（WebDriver HTTP）。已打开则复用；未打开则冷启动并轮询就绪。"""

from __future__ import annotations

import argparse
import glob
import json
import os
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import requests

API_DEFAULT_PORT = 12678
HTTP_PROBE_TIMEOUT = 1.5
POLL_INTERVAL = 0.5
WAIT_DEFAULT_SEC = 8
KILL_WAIT_MAX_SEC = 1.0
NOT_LOGGED_IN_MSG = "站斧未登录，请提供账号和密码"

COMM_FAIL_TEMPLATE = (
    "站斧启动后 {wait} 秒内未能建立 WebDriver 通讯，已按技能规则停止操作，未重复尝试。\n"
    "安装位置已确认：{install_path}。请确认站斧版本要求（Windows ≥ 5.2.12，macOS > 5.2.10）无误；"
    "若电脑因卡顿导致启动有延迟，可尝试再次打开站斧，请告诉我“打开站斧”。"
)

NEED_PATH_WIN = "未找到站斧安装目录，请提供站斧安装路径（含 站斧.exe 的文件夹）"
NEED_PATH_MAC = "未找到站斧.app，请提供路径（如 /Applications/站斧.app）"


def is_windows() -> bool:
    return platform.system() == "Windows"


def is_mac() -> bool:
    return platform.system() == "Darwin"


def _skill_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def _load_json(path: str) -> dict[str, Any]:
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _write_json(path: str, data: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def api_port_state_path() -> str:
    return os.path.join(_skill_dir(), "api_port.json")


def load_api_port_state() -> dict[str, Any]:
    return _load_json(api_port_state_path())


def save_api_port(port: int, install_dir: Optional[str] = None) -> None:
    state = load_api_port_state()
    state["api_port"] = int(port)
    if install_dir:
        state["install_dir"] = os.path.normpath(install_dir)
    state["updated_at"] = _now_iso()
    _write_json(api_port_state_path(), state)
    print(f"[端口] 已写入 api_port.json: api_port={port}")


def save_install_dir(install_dir: str) -> None:
    state = load_api_port_state()
    if "api_port" not in state:
        state["api_port"] = API_DEFAULT_PORT
    state["install_dir"] = os.path.normpath(install_dir)
    state["updated_at"] = _now_iso()
    _write_json(api_port_state_path(), state)
    print(f"[路径] 已写入 api_port.json: install_dir={state['install_dir']}")


def preferred_port() -> int:
    try:
        port = int(load_api_port_state().get("api_port", API_DEFAULT_PORT))
        return port if port > 0 else API_DEFAULT_PORT
    except (TypeError, ValueError):
        return API_DEFAULT_PORT


def clear_opening_malls() -> None:
    path = os.path.join(_skill_dir(), "opening_malls.json")
    if not os.path.isfile(path):
        return
    _write_json(path, {"malls": [], "updated_at": _now_iso()})
    print("[打开意图] 已清空 opening_malls.json")


def save_malls_to_cache(malls: list[dict[str, Any]]) -> None:
    path = os.path.join(_skill_dir(), "mall_cache.json")
    cache = _load_json(path)
    mall_map = cache.get("mall_map") if isinstance(cache.get("mall_map"), dict) else {}
    changed = False
    for mall in malls:
        name = mall.get("mall_name")
        mall_id = mall.get("mall_id")
        if name is None or mall_id is None:
            continue
        key, value = str(name), str(mall_id)
        if mall_map.get(key) != value:
            mall_map[key] = value
            changed = True
    if changed or not os.path.isfile(path):
        _write_json(path, {"mall_map": mall_map, "updated_at": _now_iso()})
        if changed:
            print(f"[缓存] 已更新 mall_cache.json（共 {len(mall_map)} 条）")


def get_available_port(start: int = API_DEFAULT_PORT) -> int:
    port = max(1, int(start))
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"自 {start} 起未找到可用端口")


def post_browser_list(port: int, timeout: float = HTTP_PROBE_TIMEOUT) -> tuple[str, Optional[dict[str, Any]]]:
    """返回 (status, payload)。status: logged_in / not_logged_in / foreign / down"""
    url = f"http://127.0.0.1:{port}"
    payload = {
        "module": "WebDriverModule",
        "action": "GetBrowserList",
        "args": json.dumps({"page": 1, "limit": 20}),
    }
    try:
        resp = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        text = (resp.text or "").strip()
        if not text:
            return "foreign", None
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return "foreign", None
        if not isinstance(data, dict):
            return "foreign", None
        is_wd = data.get("module") == "WebDriverModule" or (
            data.get("action") and ("returnObj" in data or "ret" in data)
        )
        if not is_wd:
            return "foreign", None
        ro = data.get("returnObj") or {}
        if isinstance(ro, dict) and ro.get("success") is True:
            malls = (ro.get("data") or {}).get("mall_list")
            if malls is not None:
                return "logged_in", data
        return "not_logged_in", data
    except requests.RequestException:
        return "down", None


def _windows_desktop_dirs() -> list[str]:
    dirs: list[str] = []
    home = os.path.expanduser("~")
    for rel in ("Desktop", "桌面", os.path.join("OneDrive", "Desktop"), os.path.join("OneDrive", "桌面")):
        p = os.path.join(home, rel)
        if os.path.isdir(p) and p not in dirs:
            dirs.append(p)
    public = os.environ.get("PUBLIC")
    if public:
        for rel in ("Desktop", "桌面"):
            p = os.path.join(public, rel)
            if os.path.isdir(p) and p not in dirs:
                dirs.append(p)
    return dirs


def _resolve_lnk_target(lnk_path: str) -> Optional[str]:
    try:
        esc = os.path.abspath(lnk_path).replace("'", "''")
        ps = f"(New-Object -ComObject WScript.Shell).CreateShortcut('{esc}').TargetPath"
        kw: dict[str, Any] = dict(capture_output=True, text=True, timeout=15)
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            kw["creationflags"] = subprocess.CREATE_NO_WINDOW
        r = subprocess.run(["powershell", "-NoProfile", "-NoLogo", "-Command", ps], **kw)
        if r.returncode != 0:
            return None
        t = (r.stdout or "").strip().strip('"')
        return t if t and os.path.isfile(t) else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


def _resolve_from_desktop_shortcut() -> Optional[tuple[str, str]]:
    ordered_lnks: list[str] = []
    for desktop in _windows_desktop_dirs():
        for exact in ("站斧.lnk", "站斧浏览器.lnk"):
            c = os.path.join(desktop, exact)
            if os.path.isfile(c):
                ordered_lnks.append(os.path.normpath(c))
        for c in sorted(glob.glob(os.path.join(desktop, "*站斧*.lnk"))):
            np = os.path.normpath(c)
            if np not in ordered_lnks:
                ordered_lnks.append(np)
    seen: set[str] = set()
    for lnk in ordered_lnks:
        if lnk in seen:
            continue
        seen.add(lnk)
        tgt = _resolve_lnk_target(lnk)
        if not tgt:
            continue
        folder = os.path.dirname(os.path.normpath(tgt))
        if os.path.basename(tgt).lower() == "站斧.exe":
            return folder, tgt
        candidate = os.path.join(folder, "站斧.exe")
        if os.path.isfile(candidate):
            return folder, candidate
    return None


def _normalize_mac_app_path(folder_path: str) -> Optional[str]:
    raw = os.path.normpath(os.path.expanduser(folder_path.strip()))
    if raw.endswith(".app") and os.path.isdir(raw):
        return raw
    candidate = os.path.join(raw, "站斧.app")
    if os.path.isdir(candidate):
        return candidate
    if raw in ("站斧", "站斧.app") or os.path.basename(raw) in ("站斧", "站斧.app"):
        return "站斧"
    return None


def resolve_zhanfu(folder_path: Optional[str] = None) -> tuple[str, str]:
    if folder_path:
        if is_mac():
            app = _normalize_mac_app_path(folder_path)
            if not app:
                raise FileNotFoundError(NEED_PATH_MAC)
            save_install_dir(app if app != "站斧" else folder_path)
            return (app if app != "站斧" else folder_path), app
        folder = os.path.normpath(os.path.expanduser(folder_path))
        exe = folder if folder.lower().endswith("站斧.exe") else os.path.join(folder, "站斧.exe")
        if not os.path.isfile(exe):
            raise FileNotFoundError(NEED_PATH_WIN)
        save_install_dir(os.path.dirname(exe))
        return os.path.dirname(exe), exe

    saved = load_api_port_state().get("install_dir")
    if saved:
        if is_mac():
            app = _normalize_mac_app_path(str(saved))
            if app:
                print(f"[路径] 从 api_port.json 读取: {saved}")
                return str(saved) if app != "站斧" else app, app
        else:
            folder = os.path.normpath(str(saved))
            exe = os.path.join(folder, "站斧.exe")
            if os.path.isfile(exe):
                print(f"[路径] 从 api_port.json 读取: {folder}")
                return folder, exe

    if is_mac():
        for app in ("/Applications/站斧.app", os.path.expanduser("~/Applications/站斧.app")):
            if os.path.isdir(app):
                save_install_dir(app)
                print(f"[路径] 命中: {app}")
                return app, app
        raise FileNotFoundError(NEED_PATH_MAC)

    shortcut = _resolve_from_desktop_shortcut()
    if shortcut:
        save_install_dir(shortcut[0])
        print(f"[路径] 从桌面快捷方式解析: {shortcut[0]}")
        return shortcut

    username = os.environ.get("USERNAME") or os.path.basename(os.path.expanduser("~"))
    for folder in (
        os.path.join(r"C:\Users", username, r"AppData\Local\Programs\ZhanFu"),
        r"C:\Program Files\ZhanFu",
    ):
        exe = os.path.join(folder, "站斧.exe")
        if os.path.isfile(exe):
            save_install_dir(folder)
            print(f"[路径] 命中: {folder}")
            return folder, exe
    raise FileNotFoundError(NEED_PATH_WIN)


def kill_zhanfu() -> None:
    if is_windows():
        print("[杀进程] taskkill 站斧.exe")
        subprocess.run(["taskkill", "/f", "/t", "/im", "站斧.exe"], capture_output=True)
        deadline = time.monotonic() + KILL_WAIT_MAX_SEC
        while time.monotonic() < deadline:
            r = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq 站斧.exe"],
                capture_output=True,
                text=True,
            )
            if "站斧.exe" not in (r.stdout or ""):
                break
            time.sleep(0.2)
    elif is_mac():
        print("[杀进程] killall 站斧")
        subprocess.run(["killall", "站斧"], capture_output=True)
        time.sleep(min(KILL_WAIT_MAX_SEC, 1.0))


def start_zhanfu(exe_path: str, api_port: int) -> None:
    if is_mac():
        cmd = [
            "open",
            "-a",
            exe_path,
            "--args",
            "--multip",
            "--run_type=web_driver",
            "--ipc_type=http",
            f"--httpport={api_port}",
        ]
        subprocess.Popen(cmd)
        print(f"[启动] open -a {exe_path} --multip --run_type=web_driver --ipc_type=http --httpport={api_port}")
        return
    if not os.path.isfile(exe_path):
        raise FileNotFoundError(f"未找到站斧: {exe_path}")
    args = [
        exe_path,
        "--multip",
        "--run_type=web_driver",
        "--ipc_type=http",
        f"--httpport={api_port}",
    ]
    subprocess.Popen(args, cwd=os.path.dirname(exe_path) or None)
    print(f"[启动] 站斧.exe --multip --run_type=web_driver --ipc_type=http --httpport={api_port}")


def poll_ready(port: int, wait_sec: float) -> tuple[str, Optional[dict[str, Any]]]:
    deadline = time.monotonic() + wait_sec
    last = "down"
    data: Optional[dict[str, Any]] = None
    while time.monotonic() < deadline:
        last, data = post_browser_list(port)
        if last in ("logged_in", "not_logged_in"):
            return last, data
        time.sleep(POLL_INTERVAL)
    return last, data


def do_login(port: int, username: str, password: str) -> tuple[bool, str]:
    payload = {
        "module": "WebDriverModule",
        "action": "Login",
        "args": json.dumps({"username": username, "password": password, "isboss": True}),
    }
    try:
        resp = requests.post(
            f"http://127.0.0.1:{port}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=8,
        )
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        return False, str(exc)
    ro = data.get("returnObj") or {}
    if isinstance(ro, dict) and ro.get("success") is True:
        return True, ""
    msg = ""
    if isinstance(ro, dict):
        msg = str(ro.get("msg") or "")
    return False, msg or json.dumps(data, ensure_ascii=False)


def _emit(result: dict[str, Any], code: int) -> int:
    print("RESULT_JSON=" + json.dumps(result, ensure_ascii=False))
    return code


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    p = argparse.ArgumentParser(description="打开站斧（已开则复用，未开则冷启动）")
    p.add_argument("--folder-path", default="", help="客户提供的安装路径")
    p.add_argument("--wait-seconds", type=float, default=WAIT_DEFAULT_SEC, help="冷启动后轮询秒数（默认 8）")
    p.add_argument("--username", default="", help="仅未登录且客户已提供时使用")
    p.add_argument("--password", default="", help="仅未登录且客户已提供时使用")
    ns = p.parse_args()

    if not is_windows() and not is_mac():
        print("仅支持 Windows / macOS", file=sys.stderr)
        return _emit({"ok": False, "status": "unsupported_os"}, 1)

    port = preferred_port()
    status, data = post_browser_list(port)
    print(f"[探测] api_port={port} status={status}")

    if status == "logged_in":
        save_api_port(port)
        malls = ((data or {}).get("returnObj") or {}).get("data") or {}
        save_malls_to_cache(malls.get("mall_list") or [])
        print("站斧已打开且已登录。")
        return _emit({"ok": True, "status": "already_open", "api_port": port}, 0)

    if status == "not_logged_in":
        save_api_port(port)
        if ns.username and ns.password:
            ok, msg = do_login(port, ns.username, ns.password)
            if not ok:
                print(msg or "Login 失败")
                return _emit({"ok": False, "status": "login_failed", "api_port": port, "msg": msg}, 1)
            st2, data2 = post_browser_list(port)
            if st2 == "logged_in":
                malls = ((data2 or {}).get("returnObj") or {}).get("data") or {}
                save_malls_to_cache(malls.get("mall_list") or [])
                print("站斧已登录。")
                return _emit({"ok": True, "status": "logged_in", "api_port": port}, 0)
        print(NOT_LOGGED_IN_MSG)
        return _emit({"ok": False, "status": "need_login", "api_port": port, "msg": NOT_LOGGED_IN_MSG}, 2)

    clear_opening_malls()
    try:
        folder, exe = resolve_zhanfu(ns.folder_path or None)
    except FileNotFoundError as exc:
        print(str(exc))
        return _emit({"ok": False, "status": "need_install_path", "msg": str(exc)}, 3)

    kill_zhanfu()
    api_port = get_available_port(port)
    if api_port != port:
        print(f"[端口] {port} 已被占用，改用空闲端口 {api_port}")
    start_zhanfu(exe, api_port)

    wait = max(0.5, float(ns.wait_seconds))
    status, data = poll_ready(api_port, wait)
    install_path = exe if is_windows() else exe
    if status not in ("logged_in", "not_logged_in"):
        text = COMM_FAIL_TEMPLATE.format(wait=int(wait) if wait == int(wait) else wait, install_path=install_path)
        print(text)
        return _emit(
            {
                "ok": False,
                "status": "comm_fail",
                "api_port": api_port,
                "install_path": install_path,
                "msg": text,
            },
            4,
        )

    save_api_port(api_port, install_dir=folder if is_windows() else exe)
    if status == "logged_in":
        malls = ((data or {}).get("returnObj") or {}).get("data") or {}
        save_malls_to_cache(malls.get("mall_list") or [])
        print("站斧已打开且已登录。")
        return _emit({"ok": True, "status": "started", "api_port": api_port, "install_path": install_path}, 0)

    if ns.username and ns.password:
        ok, msg = do_login(api_port, ns.username, ns.password)
        if not ok:
            print(msg or "Login 失败")
            return _emit({"ok": False, "status": "login_failed", "api_port": api_port, "msg": msg}, 1)
        st2, data2 = poll_ready(api_port, min(8.0, wait))
        if st2 == "logged_in":
            malls = ((data2 or {}).get("returnObj") or {}).get("data") or {}
            save_malls_to_cache(malls.get("mall_list") or [])
            print("站斧已打开且已登录。")
            return _emit({"ok": True, "status": "started", "api_port": api_port}, 0)

    print(NOT_LOGGED_IN_MSG)
    return _emit({"ok": False, "status": "need_login", "api_port": api_port, "msg": NOT_LOGGED_IN_MSG}, 2)


if __name__ == "__main__":
    raise SystemExit(main())
