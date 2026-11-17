#!/usr/bin/env python3
"""站斧 WebDriver + Playwright 自动化 CLI。基于官方 demo 封装，含宽松等待与重试。"""

from __future__ import annotations

import argparse
import glob
import json
import os
import platform
import random
import socket
import subprocess
import sys
import time
from typing import Any, Optional

import requests

from headed_mode import ensure_headed_mode

API_RETRY = 5
API_RETRY_INTERVAL = 3
API_TIMEOUT = 30
CLIENT_POLL_INTERVAL = 0.5  # GetBrowserList 就绪轮询间隔
CLIENT_POLL_MAX = 16  # 约 8s（0.5s×16）
CHECK_CLIENT_OPEN_TIMEOUT_SEC = 8  # 兼容旧名；实际用 GetBrowserList
LOGIN_PROBE_INTERVAL = 0.5
LOGIN_PROBE_MAX = 16  # GetBrowserList 登录探测约 8s
HTTP_PROBE_TIMEOUT = 1.5  # 单次通断/列表探测超时
KILL_WAIT_MAX_SEC = 1.0  # taskkill 后最多等待进程退出
AFTER_OPEN_BROWSER_WAIT = 10
AFTER_CREATE_WAIT = 8
GET_MALL_RETRY = 15
GET_MALL_INTERVAL = 4
GET_WD_RETRY = 10
GET_WD_INTERVAL = 5
GET_WD_PROBE_TIMEOUT_SEC = 5  # OpenBrowser 前探测是否已开：只请求 1 次、超时 5s
CDP_RETRIES = 8
CDP_DELAY = 1.5
PORT_TCP_TIMEOUT_MS = 30_000  # 冷启动后等 API 端口，30s 足够
PORT_TCP_POLL_SEC = 0.4

API_DEFAULT_PORT = 12678

NOT_LOGGED_IN_MSG = "站斧未登录，请提供账号和密码"
OPEN_MALL_FAIL_HINT = "打开店铺失败，请确认该店铺是否已绑定 IP / 设备"

# macOS 目前不支持（对齐官方 Playwright demo / 客户端能力）
MAC_UNSUPPORTED_ACTIONS = (
    "SetDownLoadPath",
    "ClearCacheFolder",
    "ClearCache",
    "SetInstallPlugins",
)

# 快捷方式找不到时，按顺序尝试的安装目录（禁止全盘递归搜索）
_FALLBACK_INSTALL_FOLDERS = (
    r"C:\Program Files\ZhanFu",
)

# macOS：常见 .app 路径（供 open -a 使用）
_MAC_FALLBACK_APPS = (
    "/Applications/站斧.app",
)


def is_windows() -> bool:
    return platform.system() == "Windows"


def is_mac() -> bool:
    return platform.system() == "Darwin"


def assert_action_supported(action: str) -> None:
    """macOS 上拒绝当前不支持的 WebDriver action。"""
    if is_mac() and action in MAC_UNSUPPORTED_ACTIONS:
        raise RuntimeError(
            f"macOS 暂不支持 {action}（SetDownLoadPath / ClearCacheFolder / "
            "ClearCache / SetInstallPlugins）。请在 Windows 站斧上使用，或改用其他操作。"
        )


def _fallback_install_folders() -> list[str]:
    """收集备用安装目录：当前用户 AppData + Program Files（仅 Windows）。"""
    folders: list[str] = []
    seen: set[str] = set()

    def add(path: str) -> None:
        norm = os.path.normpath(path)
        if norm not in seen:
            seen.add(norm)
            folders.append(norm)

    username = os.environ.get("USERNAME") or os.path.basename(os.path.expanduser("~"))
    add(os.path.join(r"C:\Users", username, "AppData", "Local", "Programs", "ZhanFu"))

    for path in _FALLBACK_INSTALL_FOLDERS:
        add(path)

    return folders


def _mac_fallback_apps() -> list[str]:
    """收集 macOS 常见 站斧.app 路径。"""
    apps: list[str] = []
    seen: set[str] = set()

    def add(path: str) -> None:
        norm = os.path.normpath(os.path.expanduser(path))
        if norm not in seen:
            seen.add(norm)
            apps.append(norm)

    for path in _MAC_FALLBACK_APPS:
        add(path)
    add(os.path.join(os.path.expanduser("~"), "Applications", "站斧.app"))
    return apps


def _normalize_mac_app_path(folder_path: str) -> Optional[str]:
    """将客户提供的路径规范为可 open -a 的 .app 路径；无效返回 None。"""
    raw = os.path.normpath(os.path.expanduser(folder_path.strip()))
    if raw.endswith(".app") and os.path.isdir(raw):
        return raw
    candidate = os.path.join(raw, "站斧.app")
    if os.path.isdir(candidate):
        return candidate
    # 允许直接传应用名「站斧」（open -a 按 LaunchServices 查找）
    if raw in ("站斧", "站斧.app") or os.path.basename(raw) in ("站斧", "站斧.app"):
        return "站斧"
    return None


def _configure_stdio() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


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
    """从桌面文件名含「站斧」的快捷方式解析安装目录与站斧.exe。

    只 glob *站斧*.lnk（及精确名 站斧.lnk / 站斧浏览器.lnk），
    禁止遍历桌面全部 .lnk 或解析无关快捷方式。
    """
    seen: set[str] = set()
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


def _resolve_from_install_folders(folders: list[str]) -> Optional[tuple[str, str]]:
    for folder in folders:
        exe = os.path.join(folder, "站斧.exe")
        if os.path.isfile(exe):
            return folder, exe
    return None


def _resolve_from_saved_install_dir() -> Optional[tuple[str, str]]:
    folder = load_saved_install_dir()
    if not folder:
        return None
    if is_mac():
        app = _normalize_mac_app_path(folder)
        if not app:
            return None
        return folder if folder != "站斧" else app, app
    return folder, os.path.join(folder, "站斧.exe")


def resolve_zhanfu_exe(folder_path: Optional[str] = None) -> tuple[str, str]:
    """自动解析站斧安装路径。

    Windows：api_port.json > 桌面快捷方式 > 常见安装路径 > CLI/客户提供。
    macOS：api_port.json > /Applications/站斧.app > ~/Applications/站斧.app > CLI/客户提供。

    未命中时抛出 FileNotFoundError，由调用方/Agent 向客户索要安装路径。
    """
    if is_windows():
        saved = _resolve_from_saved_install_dir()
        if saved:
            print(f"[路径] 从 api_port.json 读取: {saved[0]}")
            return saved

        shortcut = _resolve_from_desktop_shortcut()
        if shortcut:
            print(f"[路径] 从桌面快捷方式解析: {shortcut[0]}")
            save_install_dir(shortcut[0])
            return shortcut

        install_folders = _fallback_install_folders()
        fallback = _resolve_from_install_folders(install_folders)
        if fallback:
            print(f"[路径] 从安装目录解析: {fallback[0]}")
            save_install_dir(fallback[0])
            return fallback

        if folder_path:
            exe = os.path.join(folder_path, "站斧.exe")
            if os.path.isfile(exe):
                print(f"[路径] 从 --folder-path / 客户提供覆盖: {folder_path}")
                save_install_dir(folder_path)
                return folder_path, exe
            raise FileNotFoundError(
                f"客户提供的安装目录无效：{folder_path}（目录内未找到 站斧.exe）。"
                "请重新提供含 站斧.exe 的安装文件夹路径。"
            )

        searched = "\n  - ".join(install_folders)
        raise FileNotFoundError(
            "未找到站斧安装目录。已尝试：api_port.json、桌面「站斧」快捷方式、"
            f"以下常见安装目录均未命中：\n  - {searched}\n"
            "请向客户索要安装目录（folder_path，目录内需含 站斧.exe）。"
            "禁止全盘搜索或猜测路径。"
        )

    if is_mac():
        saved = _resolve_from_saved_install_dir()
        if saved:
            print(f"[路径] 从 api_port.json 读取: {saved[0]}")
            return saved

        for app in _mac_fallback_apps():
            if os.path.isdir(app):
                print(f"[路径] 从常见 Applications 解析: {app}")
                save_install_dir(app)
                return app, app

        if folder_path:
            app = _normalize_mac_app_path(folder_path)
            if app:
                print(f"[路径] 从 --folder-path / 客户提供覆盖: {app}")
                save_install_dir(app if app != "站斧" else folder_path)
                return (app if app != "站斧" else folder_path), app
            raise FileNotFoundError(
                f"客户提供的安装路径无效：{folder_path}（未找到 站斧.app）。"
                "请提供 /Applications/站斧.app 或含 站斧.app 的目录。"
            )

        searched = "\n  - ".join(_mac_fallback_apps())
        raise FileNotFoundError(
            "未找到站斧.app。已尝试：api_port.json、"
            f"以下常见路径均未命中：\n  - {searched}\n"
            "请向客户索要站斧.app 路径（如 /Applications/站斧.app）。"
            "禁止全盘搜索或猜测路径。"
        )

    raise FileNotFoundError("仅支持 Windows / macOS。")


def kill_zhanfu() -> None:
    """冷启动前关闭旧进程（API 已运行时勿调用）。杀完最多等 1s，进程没了立刻继续。"""
    if is_windows():
        print("[杀进程] 正在关闭 站斧.exe ...")
        os.system("taskkill /f /t /im 站斧.exe 2>nul")
        deadline = time.monotonic() + KILL_WAIT_MAX_SEC
        while time.monotonic() < deadline:
            # tasklist 退出码 0 且含 站斧.exe 才算仍在跑
            rc = os.system('tasklist /FI "IMAGENAME eq 站斧.exe" 2>nul | find /I "站斧.exe" >nul')
            if rc != 0:
                break
            time.sleep(0.2)
    elif is_mac():
        print("[杀进程] 正在关闭 站斧 (killall) ...")
        os.system("killall 站斧 2>/dev/null")
        time.sleep(min(KILL_WAIT_MAX_SEC, 1.0))
    print(f"[杀进程] 完成（最多等 {KILL_WAIT_MAX_SEC}s，已退出则立即可启动）")


def _skill_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def api_port_state_path() -> str:
    return os.path.join(_skill_dir(), "api_port.json")


def load_api_port_state() -> dict[str, Any]:
    path = api_port_state_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def load_saved_api_port() -> Optional[int]:
    try:
        port = int(load_api_port_state().get("api_port", 0))
        return port if port > 0 else None
    except (TypeError, ValueError):
        return None


def load_saved_install_dir() -> Optional[str]:
    install_dir = load_api_port_state().get("install_dir")
    if not install_dir:
        return None
    folder = os.path.normpath(str(install_dir))
    if is_mac():
        app = _normalize_mac_app_path(folder)
        return folder if app else None
    exe = os.path.join(folder, "站斧.exe")
    return folder if os.path.isfile(exe) else None


def _write_api_port_state(state: dict[str, Any]) -> None:
    path = api_port_state_path()
    state = dict(state)
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def save_install_dir(install_dir: str) -> None:
    state = load_api_port_state()
    if "api_port" not in state:
        state["api_port"] = API_DEFAULT_PORT
    state["install_dir"] = os.path.normpath(install_dir)
    _write_api_port_state(state)
    print(f"[路径] 已写入 api_port.json: install_dir={state['install_dir']}")


def save_api_port(port: int, install_dir: Optional[str] = None) -> None:
    state = load_api_port_state()
    state["api_port"] = port
    if install_dir:
        state["install_dir"] = os.path.normpath(install_dir)
    _write_api_port_state(state)
    path = api_port_state_path()
    print(f"[端口] 已写入 {path}: api_port={port}")


def mall_cache_path() -> str:
    return os.path.join(_skill_dir(), "mall_cache.json")


def load_mall_cache() -> dict[str, str]:
    path = mall_cache_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        mall_map = data.get("mall_map") if isinstance(data, dict) else None
        if not isinstance(mall_map, dict):
            return {}
        return {str(name): str(mall_id) for name, mall_id in mall_map.items()}
    except (OSError, json.JSONDecodeError):
        return {}


def _write_mall_cache(mall_map: dict[str, str]) -> None:
    path = mall_cache_path()
    payload = {
        "mall_map": dict(sorted(mall_map.items())),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def get_cached_mall_id(mall_name: str) -> Optional[str]:
    return load_mall_cache().get(mall_name)


def save_mall_to_cache(mall_name: str, mall_id: str) -> None:
    mall_map = load_mall_cache()
    mall_map[mall_name] = str(mall_id)
    _write_mall_cache(mall_map)
    print(f"[缓存] 已写入 mall_cache.json: {mall_name} → {mall_id}")


def save_malls_to_cache(malls: list[dict[str, Any]]) -> None:
    mall_map = load_mall_cache()
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
    if changed:
        _write_mall_cache(mall_map)
        print(f"[缓存] 已从列表更新 mall_cache.json（共 {len(mall_map)} 条）")


def remove_mall_from_cache(mall_name: str) -> None:
    mall_map = load_mall_cache()
    if mall_name not in mall_map:
        return
    del mall_map[mall_name]
    _write_mall_cache(mall_map)
    print(f"[缓存] 已删除过期条目: {mall_name}")


def opening_malls_path() -> str:
    return os.path.join(_skill_dir(), "opening_malls.json")


def load_opening_malls() -> list[str]:
    path = opening_malls_path()
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        malls = data.get("malls") if isinstance(data, dict) else None
        if not isinstance(malls, list):
            return []
        return [str(name) for name in malls if name]
    except (OSError, json.JSONDecodeError):
        return []


def _write_opening_malls(malls: list[str]) -> None:
    path = opening_malls_path()
    payload = {
        "malls": list(dict.fromkeys(malls)),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def is_mall_in_opening_intent(mall_name: str) -> bool:
    return mall_name in load_opening_malls()


def add_opening_mall(mall_name: str) -> None:
    malls = load_opening_malls()
    if mall_name in malls:
        print(f"[打开意图] 已存在: {mall_name}")
        return
    malls.append(mall_name)
    _write_opening_malls(malls)
    print(f"[打开意图] 已写入 opening_malls.json: {mall_name}")


def remove_opening_mall(mall_name: str) -> None:
    malls = load_opening_malls()
    if mall_name not in malls:
        return
    malls = [name for name in malls if name != mall_name]
    _write_opening_malls(malls)
    print(f"[打开意图] 已去掉: {mall_name}")


def clear_opening_malls() -> None:
    if not load_opening_malls():
        return
    _write_opening_malls([])
    print("[打开意图] 已清空 opening_malls.json")


def is_zhanfu_webdriver_payload(data: Any) -> bool:
    """判断 HTTP JSON 是否为站斧 WebDriverModule 响应（排除其他本地 Electron/控制台）。"""
    if not isinstance(data, dict):
        return False
    if data.get("module") == "WebDriverModule":
        return True
    # 部分错误响应仍带回 action + ret/returnObj
    if data.get("action") and ("returnObj" in data or "ret" in data):
        return True
    return False


def classify_api_port(port: int) -> str:
    """对端口做单次 GetBrowserList 探测，返回状态：

    - zhanfu_logged_in: 站斧 WebDriver 且能取到 mall_list
    - zhanfu_not_logged_in: 站斧 WebDriver 有响应但未取到 mall_list（可能未登录）
    - foreign: 有 HTTP 响应但不是站斧 WebDriver（如 Electron 本地打包控制台）
    - down: 连接拒绝 / 超时 / 无响应
    """
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
            timeout=HTTP_PROBE_TIMEOUT,
        )
        text = (resp.text or "").strip()
        if not text:
            return "foreign"
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return "foreign"
        if not is_zhanfu_webdriver_payload(data):
            return "foreign"
        ro = data.get("returnObj") or {}
        if isinstance(ro, dict) and ro.get("success") is True:
            malls = (ro.get("data") or {}).get("mall_list")
            if malls is not None:
                return "zhanfu_logged_in"
        return "zhanfu_not_logged_in"
    except requests.RequestException:
        return "down"


def is_zhanfu_http_alive(port: int) -> bool:
    """端口上是否为站斧 WebDriver HTTP（不含其他本地服务误判）。"""
    return classify_api_port(port) in ("zhanfu_logged_in", "zhanfu_not_logged_in")


def is_zhanfu_opened_by_browser_list(port: int) -> bool:
    """GetBrowserList 能取到 mall_list 数据 → 站斧已打开且已登录。"""
    return classify_api_port(port) == "zhanfu_logged_in"


def get_available_port(start: int = API_DEFAULT_PORT) -> int:
    """从 start 起递增绑定探测，返回首个空闲 TCP 端口（对齐官方 demo）。

    用于冷启动：首选 12678；若被占用（含非站斧服务）则自动用下一空闲端口。
    """
    port = max(1, int(start))
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"自 {start} 起未找到可用端口")


def wait_for_local_port(port: int, host: str = "127.0.0.1", timeout_ms: int = PORT_TCP_TIMEOUT_MS) -> None:
    start = time.monotonic()
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        try:
            sock.connect((host, int(port)))
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            return
        except (OSError, TimeoutError):
            pass
        finally:
            try:
                sock.close()
            except OSError:
                pass
        if (time.monotonic() - start) * 1000 > timeout_ms:
            raise TimeoutError(f"等待 {host}:{port} 就绪超时（{timeout_ms}ms）")
        time.sleep(PORT_TCP_POLL_SEC)


class ZhanfuClient:
    def __init__(self, api_port: int):
        self.api_port = api_port
        self.base_url = f"http://127.0.0.1:{api_port}"

    def call(
        self,
        action: str,
        browser_id: str = "",
        args: str = "",
        retries: int = API_RETRY,
        timeout: float = API_TIMEOUT,
    ) -> dict[str, Any]:
        assert_action_supported(action)
        # OpenBrowser / GetBrowserWebDriver 等接口要求 browserId 为字符串，禁止 JSON 数字
        bid = "" if browser_id in (None, "") else str(browser_id)
        payload = {
            "module": "WebDriverModule",
            "action": action,
            "browserId": bid,
            "args": args,
        }
        last_err: Optional[Exception] = None
        for i in range(retries):
            try:
                resp = requests.post(
                    self.base_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=timeout,
                )
                if resp.status_code == 200 and resp.text:
                    return json.loads(resp.text)
                print(f"[API] {action} 状态码 {resp.status_code}，重试 {i + 1}/{retries}")
            except Exception as e:
                last_err = e
                print(f"[API] {action} 异常 {e}，重试 {i + 1}/{retries}")
            time.sleep(API_RETRY_INTERVAL)
        raise RuntimeError(f"API 调用失败: {action} ({last_err})")

    def wait_client_ready(
        self,
        max_attempts: int = CLIENT_POLL_MAX,
        interval: float = CLIENT_POLL_INTERVAL,
    ) -> bool:
        """轮询 GetBrowserList，最多 8s；能取到数据 = 站斧已打开。禁止用 LoadSuccess 判断。"""
        for attempt in range(1, max_attempts + 1):
            try:
                if self.is_logged_in():
                    print("[就绪] GetBrowserList 能取到数据，站斧已打开")
                    return True
                print(f"[就绪] GetBrowserList 第{attempt}次：尚未取到 mall_list")
            except Exception as exc:
                print(f"[就绪] GetBrowserList 第{attempt}次异常: {exc}")
            if attempt < max_attempts:
                time.sleep(interval)
        print(f"[警告] GetBrowserList {CHECK_CLIENT_OPEN_TIMEOUT_SEC}s 内未取到数据，继续向下执行")
        return False

    def login(self, username: str, password: str, isboss: bool) -> None:
        args = json.dumps({"username": username, "password": password, "isboss": isboss}, ensure_ascii=False)
        data = self.call("Login", args=args)
        ro = data.get("returnObj") or {}
        if not ro.get("success"):
            raise RuntimeError(f"登录失败: {ro.get('msg', data)}")
        print("[登录] 成功")
        self.wait_client_ready(max_attempts=CLIENT_POLL_MAX)

    def is_logged_in(self) -> bool:
        """通过 GetBrowserList 判断站斧是否已打开且已登录（能取到数据）。"""
        try:
            data = self.call(
                "GetBrowserList",
                args=json.dumps({"page": 1, "limit": 20}),
                retries=1,
                timeout=HTTP_PROBE_TIMEOUT,
            )
            ro = data.get("returnObj") or {}
            if ro.get("success") is not True:
                return False
            malls = (ro.get("data") or {}).get("mall_list")
            if malls is not None:
                if isinstance(malls, list) and malls:
                    save_malls_to_cache(malls)
                return True
            return False
        except Exception:
            return False

    def wait_for_logged_in(self, timeout_sec: float = 8) -> bool:
        """轮询 GetBrowserList，总计最多约 8s（间隔 0.5s）。"""
        interval = LOGIN_PROBE_INTERVAL
        max_attempts = max(1, int(timeout_sec / interval))
        for attempt in range(1, max_attempts + 1):
            if self.is_logged_in():
                print(f"[登录] GetBrowserList 成功（第{attempt}次）")
                return True
            print(f"[登录] GetBrowserList 第{attempt}次：未取到 mall_list")
            if attempt < max_attempts:
                time.sleep(interval)
        print(f"[登录] GetBrowserList {timeout_sec}s 内仍无法确认登录")
        return False

    def ensure_logged_in_or_prompt(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        force: bool = False,
    ) -> bool:
        """
        GetBrowserList 取得到则站斧已打开且已登录；
        取不到则提示客户提供账号密码后 Login（isboss 固定 true）。
        返回 True 表示本次执行了 Login。
        """
        if not force and self.wait_for_logged_in():
            print("[登录] 已登录，跳过 Login")
            return False

        if not username or not password:
            raise RuntimeError(NOT_LOGGED_IN_MSG)

        print("[登录] GetBrowserList 未登录，调用 Login ...")
        self.login(username, password, isboss=True)
        if not self.wait_for_logged_in():
            raise RuntimeError("Login 后仍无法获取店铺列表，请检查账号密码是否正确")
        return True

    def login_if_needed(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        force: bool = False,
        **_ignored: Any,
    ) -> bool:
        """兼容旧调用；请优先使用 ensure_logged_in_or_prompt。"""
        return self.ensure_logged_in_or_prompt(
            username=username,
            password=password,
            force=force,
        )

    def get_mall_by_name(self, mall_name: str) -> str:
        args = json.dumps({"mallName": mall_name}, ensure_ascii=False)
        data = self.call("GetMallByName", args=args)
        ro = data.get("returnObj") or {}
        if not ro.get("success"):
            raise RuntimeError(f"GetMallByName 失败: {ro.get('msg', '')}")
        mall_id = (ro.get("data") or {}).get("mall_id")
        if mall_id is None:
            raise RuntimeError("GetMallByName 未返回 mall_id")
        mall_id_str = str(mall_id)
        save_mall_to_cache(mall_name, mall_id_str)
        return mall_id_str

    def resolve_mall_id(self, mall_name: str, *, use_cache: bool = True) -> str:
        if use_cache:
            cached = get_cached_mall_id(mall_name)
            if cached:
                print(f"[店铺] 命中缓存 mall_id={cached} ({mall_name})")
                return cached
        mall_id = self.get_mall_by_name(mall_name)
        print(f"[店铺] mall_id={mall_id} ({mall_name})")
        return mall_id

    def get_mall_by_name_retry(self, mall_name: str) -> str:
        cached = get_cached_mall_id(mall_name)
        if cached:
            print(f"[店铺] 命中缓存 mall_id={cached} ({mall_name})")
            return cached
        last_err: Optional[Exception] = None
        for i in range(GET_MALL_RETRY):
            try:
                mall_id = self.get_mall_by_name(mall_name)
                print(f"[店铺] mall_id={mall_id} ({mall_name})")
                return mall_id
            except Exception as e:
                last_err = e
                print(f"[店铺] 查询重试 {i + 1}/{GET_MALL_RETRY}: {e}")
                time.sleep(GET_MALL_INTERVAL)
        raise RuntimeError(f"无法按名称获取店铺: {mall_name} ({last_err})")

    def fetch_default_ip(self) -> str:
        data = self.call("GetBrowserList", args=json.dumps({"page": 1, "limit": 5}))
        malls = (data.get("returnObj") or {}).get("data", {}).get("mall_list", [])
        for mall in malls:
            ip = mall.get("ip_address")
            if ip:
                return str(ip)
        raise RuntimeError("无法从已有店铺获取绑定 IP，请手动提供 --ip-content")

    def create_mall(self, params: dict[str, Any]) -> None:
        args = json.dumps(params, ensure_ascii=False)
        data = self.call("CreateBrowser", args=args)
        ro = data.get("returnObj") or {}
        if not ro.get("success"):
            raise RuntimeError(f"创建店铺失败: {ro.get('msg', data)}")
        print(f"[创建] 成功: {params.get('mall_name')}")
        time.sleep(AFTER_CREATE_WAIT)

    def open_browser(
        self,
        mall_id: str,
        is_download_confirm: bool = False,
        is_open_mall_index: bool = True,
        is_switch_dynamic_network: bool = False,
    ) -> None:
        args = json.dumps(
            {
                "isDownLoadConfirm": is_download_confirm,
                "isOpenMallIndex": is_open_mall_index,
                "isSwitchDynamicNetwork": is_switch_dynamic_network,
            },
            ensure_ascii=False,
        )
        data = self.call("OpenBrowser", browser_id=mall_id, args=args)
        ro = data.get("returnObj")
        if data.get("ret") != 200 or ro is not True:
            msg = ro if isinstance(ro, str) else data
            raise RuntimeError(f"OpenBrowser 失败: {msg}。{OPEN_MALL_FAIL_HINT}")
        print(f"[打开] mall_id={mall_id}，等待 {AFTER_OPEN_BROWSER_WAIT}s")
        time.sleep(AFTER_OPEN_BROWSER_WAIT)

    def get_webdriver_port_if_open(
        self,
        mall_id: str,
        *,
        mall_name: Optional[str] = None,
    ) -> Optional[int]:
        """OpenBrowser 前探测：目标店铺已打开时返回 WebDriverPort，否则 None。

        一律只请求 1 次、超时 5s；超时/异常视为未开（返回 None），调用方应继续 OpenBrowser。
        """
        label = mall_name or mall_id
        print(f"[探测] GetBrowserWebDriver 单次 timeout={GET_WD_PROBE_TIMEOUT_SEC}s ({label})")
        try:
            data = self.call(
                "GetBrowserWebDriver",
                browser_id=mall_id,
                retries=1,
                timeout=GET_WD_PROBE_TIMEOUT_SEC,
            )
            ro = data.get("returnObj") or {}
            port = ro.get("WebDriverPort")
            if ro.get("success") and port:
                return int(port)
        except Exception as exc:
            print(f"[探测] GetBrowserWebDriver 超时/异常，视为未开，将 OpenBrowser: {exc}")
        return None

    def get_webdriver_port(self, mall_id: str) -> tuple[int, int]:
        last_err: Optional[Exception] = None
        for i in range(GET_WD_RETRY):
            try:
                data = self.call("GetBrowserWebDriver", browser_id=mall_id, retries=2)
                ro = data.get("returnObj") or {}
                port = ro.get("WebDriverPort")
                kernel = ro.get("KernalNumber", 0)
                if port:
                    print(f"[端口] WebDriverPort={port}, KernalNumber={kernel}")
                    return int(port), int(kernel)
            except Exception as e:
                last_err = e
            print(f"[端口] 重试 {i + 1}/{GET_WD_RETRY}")
            time.sleep(GET_WD_INTERVAL)
        raise RuntimeError(f"无法获取 WebDriverPort: {last_err}。{OPEN_MALL_FAIL_HINT}")

    def close_browser(self, mall_id: str, mall_name: Optional[str] = None) -> None:
        self.call("CloseBrowser", browser_id=mall_id)
        print(f"[关闭店铺] mall_id={mall_id}")
        if mall_name:
            remove_opening_mall(mall_name)

    def exit_client(self) -> None:
        self.call("ExitClient")
        clear_opening_malls()
        print("[退出] ExitClient")


def probe_zhanfu_api(default_port: int = API_DEFAULT_PORT) -> Optional[int]:
    """读取 api_port.json（无则用 default_port），单次探测是否为站斧 WebDriver。

    返回可用站斧 API 端口；若端口 down / 被非站斧服务占用，返回 None（须冷启动并改用空闲端口）。
    返回 None 时，调用方须立刻 clear_opening_malls() 再冷启动。
    """
    saved = load_saved_api_port()
    port = saved if saved is not None else default_port
    label = "本地记录" if saved is not None else "默认"
    status = classify_api_port(port)
    if status == "zhanfu_logged_in":
        print(f"[探测] 站斧 API 已打开(能取到数据) ({label}): {port}")
        save_api_port(port)
        return port
    if status == "zhanfu_not_logged_in":
        print(f"[探测] 站斧 API HTTP可达(可能未登录) ({label}): {port}")
        save_api_port(port)
        return port
    if status == "foreign":
        print(
            f"[探测] {label}端口 {port} 被其他本地服务占用（非站斧 WebDriver），"
            "将改用空闲端口冷启动站斧（不停止占用方）"
        )
        return None
    print(f"[探测] {label}端口 {port} 无 HTTP 响应，站斧未打开 → 须清空 opening_malls 后冷启动")
    return None


def allocate_cold_start_port(preferred: int = API_DEFAULT_PORT) -> int:
    """冷启动用端口：优先 preferred（默认 12678）；占用则递增找空闲端口。"""
    port = get_available_port(preferred)
    if port != preferred:
        print(f"[端口] {preferred} 已被占用，改用空闲端口 {port}")
    else:
        print(f"[端口] 使用空闲端口 {port}")
    return port


def start_zhanfu(exe_path: str, api_port: int) -> None:
    """冷启动站斧 WebDriver 模式。

    Windows: 站斧.exe --multip --run_type=web_driver --ipc_type=http --httpport=...
             （四项缺一不可，禁止减少）
    macOS:   open -a 站斧.app --args --multip --run_type=web_driver --ipc_type=http --httpport=...
             （四项缺一不可，禁止减少；与 Windows 相同）
    """
    if is_mac():
        # exe_path 为 .app 路径或应用名「站斧」
        if exe_path != "站斧" and not (
            exe_path.endswith(".app") and os.path.isdir(exe_path)
        ):
            raise FileNotFoundError(f"未找到站斧.app: {exe_path}")
        # macOS：四项参数禁止减少（含 --multip）
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
        print(f"[启动] open -a {exe_path} api_port={api_port}")
    else:
        if not os.path.isfile(exe_path):
            raise FileNotFoundError(f"未找到站斧: {exe_path}")
        # Windows：四项参数禁止减少
        args = [
            exe_path,
            "--multip",
            "--run_type=web_driver",
            "--ipc_type=http",
            f"--httpport={api_port}",
        ]
        subprocess.Popen(args)
        print(f"[启动] 站斧 api_port={api_port}")
    wait_for_local_port(api_port)


def connect_playwright(webdriver_port: int):
    from playwright.sync_api import sync_playwright

    ensure_headed_mode()
    wait_for_local_port(webdriver_port, timeout_ms=PORT_TCP_TIMEOUT_MS)
    playwright = sync_playwright().start()
    endpoint = f"http://127.0.0.1:{webdriver_port}"
    last_err: Optional[Exception] = None
    for _ in range(CDP_RETRIES):
        browser = None
        try:
            browser = playwright.chromium.connect_over_cdp(endpoint)
            for _ in range(10):
                for ctx in browser.contexts:
                    is_closed = getattr(ctx, "is_closed", None)
                    if is_closed is None or not is_closed():
                        for page in ctx.pages:
                            if "check.html" in page.url:
                                return playwright, browser, ctx, page
                        page = ctx.pages[0] if ctx.pages else ctx.new_page()
                        return playwright, browser, ctx, page
                time.sleep(0.5)
            ctx = browser.new_context()
            page = ctx.new_page()
            return playwright, browser, ctx, page
        except Exception as e:
            last_err = e
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass
            time.sleep(CDP_DELAY)
    raise RuntimeError(f"Playwright CDP 连接失败: {last_err}")


def build_create_args(ns: argparse.Namespace, ip_content: str) -> dict[str, Any]:
    return {
        "mall_name": ns.mall_name,
        "mall_account": ns.mall_account or "test_account",
        "mall_password": ns.mall_password or "test_password",
        "platform": ns.platform or "自定义平台",
        "platform_url": ns.platform_url or "https://www.baidu.com",
        "mall_address": ns.mall_address or "",
        "tags": ns.tags or "",
        "authorizationMember": ns.authorization_member or "",
        "ip_content": ip_content,
        "browser_kernel_version": ns.browser_kernel_version,
        "window_ua": "",
        "mac_ua": "",
        "android_ua": "",
        "remark": ns.remark or "Playwright 自动化创建",
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="站斧 WebDriver + Playwright")
    p.add_argument(
        "--action",
        choices=["run", "close-browser", "exit-client"],
        default="run",
        help="run=完整流程；close-browser/exit-client=仅调用 API 收尾",
    )
    p.add_argument("--folder-path", help="站斧安装目录（自动查找失败时由客户提供）")
    p.add_argument("--api-port", type=int, default=API_DEFAULT_PORT, help="API 端口（默认 12678）")
    p.add_argument("--mall-id", help="店铺 ID（close-browser 时必填）")
    p.add_argument("--bootstrap-only", action="store_true", help="仅启动并登录，输出 api_port")
    p.add_argument("--username", help="站斧用户名（GetBrowserList 未登录时由客户提供）")
    p.add_argument("--password", help="站斧密码（GetBrowserList 未登录时由客户提供）")
    p.add_argument("--force-login", action="store_true", help="强制 Login（切换账号时使用，会关闭已开店铺）")
    p.add_argument("--no-login", action="store_true", help="永不调用 Login API")
    p.add_argument("--create", action="store_true", help="创建店铺")
    p.add_argument("--mall-name", help="店铺名称")
    p.add_argument("--platform", default="自定义平台")
    p.add_argument("--platform-url", default="https://www.baidu.com")
    p.add_argument("--ip-content", help="绑定设备 IP（创建时必填，或用 --ip-from-list）")
    p.add_argument("--ip-from-list", action="store_true", help="创建店铺时从已有店铺复用 IP")
    p.add_argument("--mall-account")
    p.add_argument("--mall-password")
    p.add_argument("--mall-address")
    p.add_argument("--tags")
    p.add_argument("--authorization-member")
    p.add_argument("--browser-kernel-version", type=int, default=0)
    p.add_argument("--remark")
    p.add_argument("--open-mall-index", action="store_true", default=True)
    p.add_argument("--no-open-mall-index", action="store_false", dest="open_mall_index")
    p.add_argument("--connect-cdp", action="store_true", help="获取端口后连接 Playwright CDP")
    p.add_argument("--force-restart", action="store_true", help="强制杀进程并冷启动站斧")
    p.add_argument("--force-open", action="store_true", help="店铺已打开时仍重新 OpenBrowser（CLI 无交互确认时用；对话中应先询问是否关闭）")
    return p.parse_args()


def run_maintenance(action: str, api_port: int, mall_id: Optional[str], mall_name: Optional[str] = None) -> int:
    client = ZhanfuClient(api_port)
    if action == "close-browser":
        if not mall_id:
            print("close-browser 需要 --mall-id", file=sys.stderr)
            return 1
        client.close_browser(mall_id, mall_name=mall_name)
    else:
        client.exit_client()
    print(json.dumps({"action": action, "api_port": api_port, "mall_id": mall_id}, ensure_ascii=False))
    return 0


def main() -> int:
    _configure_stdio()
    ensure_headed_mode()
    ns = parse_args()

    if ns.action != "run":
        return run_maintenance(ns.action, ns.api_port, ns.mall_id, mall_name=ns.mall_name)

    if not is_windows() and not is_mac():
        print("仅支持 Windows / macOS", file=sys.stderr)
        return 1

    api_port = probe_zhanfu_api(default_port=ns.api_port)
    if ns.force_restart or api_port is None:
        # 打开站斧 / 探测未打开 / 端口被非站斧占用：立刻清空店铺名，再查目录冷启动
        clear_opening_malls()
        kill_zhanfu()
        try:
            folder, exe = resolve_zhanfu_exe(ns.folder_path)
        except FileNotFoundError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        # 优先 ns.api_port（默认 12678）；被占用则自动递增换空闲端口（对齐官方 demo）
        api_port = allocate_cold_start_port(ns.api_port)
        start_zhanfu(exe, api_port)
        save_api_port(api_port, install_dir=folder)
    else:
        try:
            folder, exe = resolve_zhanfu_exe(ns.folder_path)
        except FileNotFoundError:
            # 复用已运行实例时可不强求本地 exe；仅打印警告
            folder, exe = "", ""
            print("[复用] 站斧已打开，跳过本地 exe 解析")
        print(f"[复用] 跳过杀进程，使用 api_port={api_port}")

    client = ZhanfuClient(api_port)
    client.wait_client_ready()

    if ns.no_login:
        if client.is_logged_in():
            print("[登录] --no-login：GetBrowserList 成功，已登录，继续")
        else:
            print(f"[登录] --no-login：{NOT_LOGGED_IN_MSG}")
            return 1
    else:
        client.ensure_logged_in_or_prompt(
            username=ns.username,
            password=ns.password,
            force=ns.force_login,
        )

    if ns.bootstrap_only:
        print(json.dumps({"api_port": api_port, "folder": folder, "exe": exe}, ensure_ascii=False))
        return 0

    mall_name = ns.mall_name
    if ns.create:
        if not mall_name:
            mall_name = f"测试WebDriver随机{random.randint(0, 999999)}"
            ns.mall_name = mall_name
        ip_content = ns.ip_content
        if not ip_content and ns.ip_from_list:
            ip_content = client.fetch_default_ip()
            print(f"[IP] 复用已有设备: {ip_content}")
        if not ip_content:
            print("创建店铺需要 --ip-content 或 --ip-from-list", file=sys.stderr)
            return 1
        client.create_mall(build_create_args(ns, ip_content))
        mall_id = client.get_mall_by_name_retry(mall_name)
    else:
        if not mall_name:
            print("需要 --mall-name 或 --create", file=sys.stderr)
            return 1
        mall_id = client.get_mall_by_name_retry(mall_name)

    # 写入打开意图后，OpenBrowser 前单次 5s 探测是否已开
    add_opening_mall(mall_name)

    existing_port = client.get_webdriver_port_if_open(mall_id, mall_name=mall_name)
    if existing_port is not None:
        if ns.force_open:
            print(f"[打开] 店铺已打开 (port={existing_port})，--force-open 重新 OpenBrowser")
            client.open_browser(mall_id, is_open_mall_index=ns.open_mall_index)
            wd_port, kernel = client.get_webdriver_port(mall_id)
        else:
            print(
                f"[打开] 店铺 {mall_name} 已打开 (WebDriverPort={existing_port})，"
                "跳过 OpenBrowser；对话中应先询问客户是否需要关闭店铺；CLI 重开请加 --force-open"
            )
            wd_port, kernel = existing_port, 0
    else:
        print(f"[打开] 探测未确认已开（≤5s），继续 OpenBrowser: {mall_name}")
        client.open_browser(mall_id, is_open_mall_index=ns.open_mall_index)
        wd_port, kernel = client.get_webdriver_port(mall_id)

    result = {
        "api_port": api_port,
        "mall_id": mall_id,
        "mall_name": mall_name,
        "webdriver_port": wd_port,
        "kernel": kernel,
    }

    if ns.connect_cdp:
        playwright, browser, context, page = connect_playwright(wd_port)
        print(f"[Playwright] 已连接 CDP 端口 {wd_port}，当前页: {page.url}")
        result["cdp_connected"] = True
        result["current_url"] = page.url
        if ns.close:
            try:
                browser.close()
            except Exception:
                pass
            try:
                playwright.stop()
            except Exception:
                pass

    print(json.dumps(result, ensure_ascii=False))

    if ns.close:
        client.close_browser(mall_id, mall_name=mall_name)
        client.exit_client()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
