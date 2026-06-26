#!/usr/bin/env python3
"""
wechat-tietu-draft 技能主入口脚本
统一的环境检查、状态管理和草稿创建入口
"""

import os
import sys
import json
import base64
import subprocess
import time
import argparse
import asyncio
import concurrent.futures
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

import websockets

# 清除代理环境变量，避免websockets的SOCKS代理错误
proxy_vars = [
    'http_proxy', 'https_proxy', 'all_proxy',
    'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY',
    'no_proxy', 'NO_PROXY'
]

for var in proxy_vars:
    os.environ.pop(var, None)


def _looks_like_proxy_error(text):
    if not text:
        return False
    t = text.lower()
    if "python-socks" in t or "socks proxy" in t:
        return True
    if "connecting through" in t and "proxy" in t:
        return True
    if "socks" in t and "requires" in t:
        return True
    return False


def print_proxy_vpn_hint():
    """出现代理/WebSocket 相关错误时：提醒关 VPN，勿改代码凑修复。"""
    print("\n【代理/VPN 导致连接失败】请关闭 VPN 或系统代理后重试；勿改技能代码或装 python-socks。")
    print("  执行: python3 skill_main.py --file <文章.txt>\n")


# 环境状态定义
class EnvStatus:
    """环境状态常量"""
    UNKNOWN = "unknown"
    READY = "ready"                     # Chrome运行且已登录微信公众号
    CHROME_RUNNING_NOT_LOGGED = "chrome_running_not_logged"  # Chrome运行但未登录
    CHROME_RUNNING_LOGIN_STATUS_UNKNOWN = "chrome_running_login_status_unknown"  # Chrome运行，登录状态不确定
    CHROME_NOT_RUNNING = "chrome_not_running"                # Chrome未运行
    NO_WECHAT_PAGE = "no_wechat_page"   # Chrome运行但没有微信公众号页面
    PORT_OCCUPIED_NO_PAGES = "port_occupied_no_pages"  # 端口被占用但没有页面
    ERROR = "error"                     # 检测过程中出错

# 与 cdp 轮询、环境判定共用（已登录 URL 特征）
WECHAT_MP_HOME = "https://mp.weixin.qq.com/"
# 本技能默认 CDP 端口（避免与常见教程 9222 冲突；可用 --port 覆盖）
DEFAULT_CDP_PORT = 19222
# 等待登录/就绪：最长秒数、轮询间隔（可通过环境变量 TIETU_MAX_WAIT 覆盖，仅整数）
DEFAULT_MAX_WAIT_SECONDS = int(os.environ.get("TIETU_MAX_WAIT", "300"))
DEFAULT_CHECK_INTERVAL = 5
MP_LOGGED_IN_URL_MARKERS = (
    "token=",
    "cgi-bin/home",
    "cgi-bin/masssend",
    "cgi-bin/material",
    "cgi-bin/draft",
    "cgi-bin/appmsg",
)


def print_chrome_help():
    """Chrome / 微信公众平台 设置说明（cdp 脚本可复用）"""
    print(f"\n📋 CDP 模式：Chrome 需在端口 {DEFAULT_CDP_PORT} 运行并已登录公众号；由 skill_main.py --file 自动启动 Chrome。")
    print("   创建草稿: python3 skill_main.py --file 文章内容.txt\n")


def open_url_in_browser(url):
    """本机打开 URL（无 CDP 时打开 mp 首页等）"""
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", url], check=False, timeout=10)
        elif sys.platform == "win32":
            os.startfile(url)  # noqa: S606
        else:
            subprocess.run(["xdg-open", url], check=False, timeout=10)
    except Exception:
        pass


def validate_and_read_txt_file(file_path):
    """
    验证并读取 .txt：扩展名、存在、可读、UTF-8；
    第一行可选标题（≤100 字），其余为正文。
    返回 (title, content) 或 (None, None)。
    """
    if not str(file_path).lower().endswith(".txt"):
        print("❌ 错误：只接受.txt文本文件")
        print(f"   当前文件: {file_path}")
        return None, None
    if not os.path.exists(file_path):
        print("❌ 错误：文件不存在")
        print(f"   路径: {file_path}")
        return None, None
    if not os.access(file_path, os.R_OK):
        print("❌ 错误：文件不可读")
        print(f"   路径: {file_path}")
        return None, None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print("❌ 错误：文件为空")
            return None, None
        title_line = lines[0].strip()
        if title_line and len(title_line) <= 100:
            title = title_line
            content_lines = lines[1:]
        else:
            title = ""
            content_lines = lines
        content = "".join(content_lines).strip()
        if not content:
            print("❌ 错误：正文内容为空")
            return None, None
        print(f"✅ 文件验证通过 标题: {title or '(无标题)'} 正文: {len(content)} 字")
        return title, content
    except UnicodeDecodeError:
        print("❌ 错误：文件编码不是UTF-8")
        return None, None
    except Exception as e:
        print(f"❌ 错误：读取文件失败: {e}")
        return None, None


# ---------------------------------------------------------------------------
# CDP / 会话过期 / 统一等待（与 wechat_tietu_draft 共用一套逻辑）
# ---------------------------------------------------------------------------


async def _cdp_session_expired_need_login(ws_url):
    """页面存在 a#jumpUrl 文案「登录」→ 会话过期。"""
    expr = r"""(function(){var a=document.querySelector('a#jumpUrl');if(!a)return false;return (a.textContent||'').trim()==='\u767b\u5f55';})()"""
    msg_id = 99
    try:
        async with websockets.connect(ws_url, proxy=None) as ws:
            await ws.send(
                json.dumps(
                    {
                        "id": msg_id,
                        "method": "Runtime.evaluate",
                        "params": {"expression": expr, "returnByValue": True},
                    }
                )
            )
            while True:
                raw = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(raw)
                if data.get("id") != msg_id:
                    continue
                if data.get("error"):
                    return None
                val = data.get("result", {}).get("result", {}).get("value")
                return bool(val)
    except Exception:
        return None


async def _cdp_capture_screenshot_png(ws_url):
    """
    CDP Page.captureScreenshot → PNG bytes。需可连 WebSocket 的调试页。
    """
    cap_id = 77
    try:
        async with websockets.connect(
            ws_url, max_size=50 * 1024 * 1024, proxy=None
        ) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            await ws.send(
                json.dumps(
                    {
                        "id": cap_id,
                        "method": "Page.captureScreenshot",
                        "params": {"format": "png", "captureBeyondViewport": True},
                    }
                )
            )
            while True:
                raw = await asyncio.wait_for(ws.recv(), timeout=30)
                data = json.loads(raw)
                if data.get("method") == "Page.loadEventFired":
                    continue
                if data.get("id") == 1:
                    continue
                if data.get("id") != cap_id:
                    continue
                if data.get("error"):
                    return None
                b64 = data.get("result", {}).get("data")
                if not b64:
                    return None
                return base64.b64decode(b64)
    except Exception:
        return None
    return None


def _pick_page_for_screenshot(pages):
    """优先 mp 登录/首页，否则任意 page。"""
    if not pages:
        return None
    candidates = [p for p in pages if p.get("type") == "page" and p.get("webSocketDebuggerUrl")]
    if not candidates:
        return None

    def score(p):
        u = (p.get("url") or "").lower()
        t = p.get("title") or ""
        s = 0
        if "mp.weixin.qq.com" in u:
            s += 10
        if "扫码" in t or "login" in u or "login" in t.lower():
            s += 5
        return s

    candidates.sort(key=score, reverse=True)
    return candidates[0]


def capture_wechat_mp_screenshot(port=DEFAULT_CDP_PORT, output_path=None):
    """
    对当前调试实例中优先选取的公众号相关标签页截图（PNG）。
    成功返回绝对路径字符串，失败返回 None。
    """
    try:
        r = subprocess.run(
            ["curl", "-s", f"http://127.0.0.1:{port}/json/list"],
            capture_output=True,
            text=True,
            timeout=8,
        )
        if r.returncode != 0:
            return None
        pages = json.loads(r.stdout)
        page = _pick_page_for_screenshot(pages)
        if not page:
            return None
        ws_url = page.get("webSocketDebuggerUrl")
        if not ws_url:
            return None
        script_dir = Path(__file__).resolve().parent
        if output_path is None:
            output_path = script_dir / "mp_login_screenshot.png"
        else:
            output_path = Path(output_path).expanduser().resolve()

        def _run():
            return asyncio.run(_cdp_capture_screenshot_png(ws_url))

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            png = ex.submit(_run).result(timeout=45)
        if not png:
            return None
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(png)
        return str(output_path)
    except Exception:
        return None


def check_wechat_session_expired_via_cdp(ws_url):
    """True=过期；False=未判定过期；None=无法检测。线程内 asyncio.run 避免嵌套 loop。"""
    if not ws_url:
        return None

    def _run():
        return asyncio.run(_cdp_session_expired_need_login(ws_url))

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            return ex.submit(_run).result(timeout=20)
    except Exception:
        return None


async def _cdp_navigate_url(ws_url, url):
    nav_id = 88
    try:
        async with websockets.connect(ws_url, proxy=None) as ws:
            await ws.send(
                json.dumps(
                    {
                        "id": nav_id,
                        "method": "Page.navigate",
                        "params": {"url": url},
                    }
                )
            )
            while True:
                raw = await asyncio.wait_for(ws.recv(), timeout=20)
                data = json.loads(raw)
                if data.get("id") == nav_id:
                    return not bool(data.get("error"))
    except Exception:
        return False
    return False


def _mp_page_logged_in_ready(page):
    """可发草稿：mp + URL 特征 + 非扫码页 + 非会话过期(CDP)。"""
    if not page or "mp.weixin.qq.com" not in (page.get("url") or ""):
        return False
    url = (page.get("url") or "").lower()
    title = page.get("title") or ""
    if "扫码登录" in title or "Login" in title:
        return False
    if not any(m in url for m in MP_LOGGED_IN_URL_MARKERS):
        return False
    if check_wechat_session_expired_via_cdp(page.get("webSocketDebuggerUrl")) is True:
        return False
    return True


def wait_until_ready_for_draft(port=DEFAULT_CDP_PORT, max_seconds=None, interval=DEFAULT_CHECK_INTERVAL):
    """
    统一等待：轮询直到存在「可发草稿」的 mp 标签页（含 CDP 会话未过期）。
    交互 / 非交互 / skill_main / cdp 子进程前均用同一套标准。
    """
    if max_seconds is None:
        max_seconds = DEFAULT_MAX_WAIT_SECONDS
    print("\n⏳ 等待微信公众平台就绪（自动检测）…")
    checks = max(1, max_seconds // interval)
    for i in range(checks):
        elapsed = i * interval
        try:
            r = subprocess.run(
                ["curl", "-s", f"http://127.0.0.1:{port}/json/list"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if r.returncode != 0:
                time.sleep(interval)
                continue
            pages = json.loads(r.stdout)
            for p in pages:
                if _mp_page_logged_in_ready(p):
                    print("STAGE: LOGIN_CONFIRMED")
                    print(f"✅ 已就绪（约 {elapsed} 秒），可创建草稿\n")
                    return True
        except Exception:
            pass
        if elapsed > 0 and elapsed % 60 == 0:
            print(f"   … 等待中 {elapsed}/{max_seconds}s")
        time.sleep(interval)
    print("STAGE: LOGIN_TIMEOUT")
    print(f"\n❌ 等待超时（{max_seconds} 秒）。长时间未检测到登录，可能未扫码或会话被踢出。")
    print_chrome_help()
    return False


def refetch_best_wechat_page(port=DEFAULT_CDP_PORT):
    try:
        r = subprocess.run(
            ["curl", "-s", f"http://127.0.0.1:{port}/json/list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if r.returncode != 0:
            return None
        pages = json.loads(r.stdout)
        best = None
        for p in pages:
            if not _mp_page_logged_in_ready(p):
                continue
            u = p.get("url") or ""
            if "token=" in u.lower():
                return p
            if best is None:
                best = p
        return best
    except Exception:
        return None


def prompt_session_expired_scan_login(ws_url=None, will_auto_continue=True):
    """会话过期：3 秒 → CDP/系统浏览器打开 mp 首页 → 再进入 wait_until_ready_for_draft。"""
    print("\n⚠️ 会话已过期，请重新扫码登录。正在打开首页…")
    time.sleep(3)
    opened = False
    if ws_url:
        try:

            def _nav():
                return asyncio.run(_cdp_navigate_url(ws_url, WECHAT_MP_HOME))

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
                opened = bool(ex.submit(_nav).result(timeout=25))
        except Exception:
            pass
    if not opened:
        open_url_in_browser(WECHAT_MP_HOME)
    print("  请在浏览器内扫码登录，将自动检测就绪。\n")
    print_chrome_help()


def ensure_chrome_ready_for_draft(port=DEFAULT_CDP_PORT):
    """
    创建草稿前统一闸门：端口、mp 页、扫码页、会话过期 → 必要时提示并 wait_until_ready_for_draft。
    """
    print("\n🔍 检查 Chrome / 公众号…")
    try:
        r = subprocess.run(
            ["curl", "-s", f"http://127.0.0.1:{port}/json/list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if r.returncode != 0:
            print("❌ Chrome 调试端口不可用")
            print_chrome_help()
            return False
        pages = json.loads(r.stdout)
        if not pages:
            print("❌ 无页面")
            print_chrome_help()
            return False
        wechat = None
        for p in pages:
            if "mp.weixin.qq.com" in (p.get("url") or ""):
                wechat = p
                break
        if not wechat:
            print("❌ 未找到 mp.weixin.qq.com 标签页，正在打开首页…")
            open_url_in_browser(WECHAT_MP_HOME)
            return wait_until_ready_for_draft(port=port, max_seconds=DEFAULT_MAX_WAIT_SECONDS, interval=DEFAULT_CHECK_INTERVAL)
        t = wechat.get("title") or ""
        if "扫码登录" in t or "Login" in t:
            print("❌ 当前为扫码登录页，等待登录完成…")
            return wait_until_ready_for_draft(port=port, max_seconds=DEFAULT_MAX_WAIT_SECONDS, interval=DEFAULT_CHECK_INTERVAL)
        ws = wechat.get("webSocketDebuggerUrl")
        if check_wechat_session_expired_via_cdp(ws) is True:
            print("❌ 会话已过期（a#jumpUrl「登录」）")
            prompt_session_expired_scan_login(ws, will_auto_continue=True)
            return wait_until_ready_for_draft(port=port, max_seconds=DEFAULT_MAX_WAIT_SECONDS, interval=DEFAULT_CHECK_INTERVAL)
        if _mp_page_logged_in_ready(wechat):
            print("✅ 已登录且会话有效")
            return True
        for p in pages:
            if _mp_page_logged_in_ready(p):
                print("✅ 已登录且会话有效")
                return True
        print("⚠️ 登录状态未确认，等待就绪…")
        return wait_until_ready_for_draft(port=port, max_seconds=DEFAULT_MAX_WAIT_SECONDS, interval=DEFAULT_CHECK_INTERVAL)
    except subprocess.TimeoutExpired:
        print("❌ 连接 Chrome 超时")
        print_chrome_help()
        return False
    except json.JSONDecodeError:
        print("❌ Chrome 返回异常")
        print_chrome_help()
        return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        print_chrome_help()
        return False


def print_header():
    """打印技能标题"""
    print("wechat-tietu-draft v1.0.0")

def check_environment_status(port=DEFAULT_CDP_PORT):
    """
    检查当前环境状态
    返回: (状态, 详细信息)
    """
    try:
        # 1. 检查调试端口是否响应
        try:
            result = subprocess.run(
                ["curl", "-s", f"http://127.0.0.1:{port}/json/version"],
                capture_output=True,
                text=True,
                timeout=3
            )
            port_responding = (result.returncode == 0)
        except Exception:
            port_responding = False
        
        if not port_responding:
            print("   ❌ Chrome调试端口未响应")
            return EnvStatus.CHROME_NOT_RUNNING, {"port": port, "reason": "port_not_responding"}
        
        # 2. 获取页面列表
        try:
            result = subprocess.run(
                ["curl", "-s", f"http://127.0.0.1:{port}/json/list"],
                capture_output=True,
                text=True,
                timeout=3
            )
            
            if result.returncode != 0:
                print("   ❌ 无法获取页面列表")
                return EnvStatus.PORT_OCCUPIED_NO_PAGES, {"port": port, "reason": "cannot_get_pages"}
            
            pages = json.loads(result.stdout)
            
            if not pages:
                print("   ⚠️ 端口被占用但没有页面")
                return EnvStatus.PORT_OCCUPIED_NO_PAGES, {"port": port, "pages": 0}
            
            # 3. 检查微信公众号页面和登录状态
            wechat_page_found = False
            wechat_logged_in = False
            wechat_page_info = None
            
            for page in pages:
                if page.get("type") == "page":
                    url = page.get("url", "")
                    title = page.get("title", "")
                    
                    if "mp.weixin.qq.com" in url:
                        wechat_page_found = True
                        wechat_page_info = page
                        
                        # 智能登录状态判断
                        # 1. 检查是否为登录页面
                        login_keywords = ["login", "扫码", "二维码", "qrcode", "登录"]
                        is_login_page = any(keyword in url.lower() or keyword in title.lower() 
                                          for keyword in login_keywords)
                        
                        # 2. 检查是否为已登录状态（包含token参数）
                        # 微信公众号登录后URL通常包含token参数
                        is_logged_in = any(
                            indicator in url.lower()
                            for indicator in MP_LOGGED_IN_URL_MARKERS
                        )
                        
                        # 3. 综合判断
                        if is_login_page:
                            wechat_logged_in = False
                        elif is_logged_in:
                            wechat_logged_in = True
                        else:
                            wechat_logged_in = False  # 不确定状态
                        break
            
            if not wechat_page_found:
                print("   ⚠️ 没有找到微信公众号页面")
                return EnvStatus.NO_WECHAT_PAGE, {"pages": len(pages), "first_page": pages[0] if pages else None}
            
            if wechat_logged_in:
                print("   ✅ 环境就绪")
                return EnvStatus.READY, {"page": wechat_page_info, "port": port}
            elif is_login_page:
                print("   ⚠️ 需要登录公众号")
                return EnvStatus.CHROME_RUNNING_NOT_LOGGED, {"page": wechat_page_info, "port": port}
            else:
                print("   ⚠️ 登录状态不确定")
                return EnvStatus.CHROME_RUNNING_LOGIN_STATUS_UNKNOWN, {"page": wechat_page_info, "port": port}
                
        except json.JSONDecodeError:
            print("   ❌ 无法解析页面数据")
            return EnvStatus.ERROR, {"reason": "json_decode_error"}
        except Exception as e:
            print(f"   ❌ 检查页面时出错: {e}")
            return EnvStatus.ERROR, {"reason": str(e)}
            
    except Exception as e:
        print(f"❌ 环境检查失败: {e}")
        return EnvStatus.ERROR, {"reason": str(e)}

# ---------- 内置原 start_real_chrome.py（已删除独立文件）----------


def _chrome_kill_port_pids(port=DEFAULT_CDP_PORT):
    """释放调试端口（macOS/Linux：lsof + kill）。"""
    try:
        r = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0 or not r.stdout.strip():
            return False
        for pid in r.stdout.strip().split():
            try:
                subprocess.run(["kill", "-9", pid], capture_output=True, timeout=2)
            except Exception:
                pass
        time.sleep(2)
        return True
    except Exception as e:
        print(f"  释放端口时: {e}")
        return False


def _chrome_launch_debug(port=DEFAULT_CDP_PORT):
    """启动带 remote-debugging-port 的 Chrome，返回 info 字典或 None。"""
    _chrome_kill_port_pids(port)
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
    ]
    chrome_cmd = None
    for p in chrome_paths:
        if os.path.exists(p):
            chrome_cmd = p
            break
    if not chrome_cmd:
        r = subprocess.run(["which", "google-chrome"], capture_output=True, text=True)
        chrome_cmd = r.stdout.strip() if r.returncode == 0 else "google-chrome"
    ts = int(time.time())
    user_data = os.path.expanduser(f"~/.chrome-real-wechat-{ts}")
    os.makedirs(user_data, exist_ok=True)
    cmd = [
        chrome_cmd,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data}",
        "--no-first-run",
        "--no-default-browser-check",
        "--new-window",
        "--window-size=1200,800",
        "--window-position=100,100",
        WECHAT_MP_HOME,
    ]
    try:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        time.sleep(3)
        for i in range(15):
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/json/version", timeout=3
                ) as resp:
                    if resp.status == 200:
                        return {"port": port, "user_data_dir": user_data}
            except Exception:
                pass
            time.sleep(2)
        print("  调试端口未响应，请查看是否弹出 Chrome 窗口")
        return {"port": port, "user_data_dir": user_data}
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return None


def _sr_list_has_page(port):
    try:
        r = subprocess.run(
            ["curl", "-s", f"http://127.0.0.1:{port}/json/list"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if r.returncode != 0:
            return False
        for p in json.loads(r.stdout):
            if p.get("type") == "page":
                return True
        return False
    except Exception:
        return False


def _sr_find_wechat_page(port):
    try:
        r = subprocess.run(
            ["curl", "-s", f"http://127.0.0.1:{port}/json/list"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if r.returncode != 0:
            return False, None
        for p in json.loads(r.stdout):
            if p.get("type") == "page" and "mp.weixin.qq.com" in (p.get("url") or ""):
                return True, p
        return False, None
    except Exception:
        return False, None


def _sr_navigate_first_tab_to_mp(port):
    try:
        r = subprocess.run(
            ["curl", "-s", f"http://127.0.0.1:{port}/json/list"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if r.returncode != 0:
            return False
        first = None
        for p in json.loads(r.stdout):
            if p.get("type") == "page":
                first = p
                break
        if not first or not first.get("id"):
            return False
        pid = first["id"]
        body = json.dumps(
            {"id": 1, "method": "Page.navigate", "params": {"url": WECHAT_MP_HOME}}
        ).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/json/session/{pid}",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


def _sr_print_targets(port):
    """仅用于调试；为减噪默认不打印目标列表。"""
    pass


def _sr_after_launch_hints():
    """Chrome 启动后统一提示：扫码登录后由自动检测就绪，交互/非交互一致。"""
    print("\n📱 请在 Chrome 内扫码登录公众号；将自动检测就绪。")


def run_start_chrome_flow(port=DEFAULT_CDP_PORT):
    """
    原 start_real_chrome.py main：尽量复用已有调试实例；否则杀端口再起新 Chrome。
    返回是否已尽力拉起可用调试端口（Popen 成功即 True）。
    """
    debug_ok = False
    try:
        r = subprocess.run(
            ["curl", "-s", f"http://127.0.0.1:{port}/json/version"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        debug_ok = r.returncode == 0
    except Exception:
        pass

    if debug_ok and _sr_list_has_page(port):
        ok, _ = _sr_find_wechat_page(port)
        if ok:
            print("STAGE: CHROME_STARTED")
            print("✅ 已有调试 Chrome 且含公众号页")
            _sr_after_launch_hints()
            return True
        print("⚠️ 有页面但无公众号页 → 尝试导航到 mp…")
        if _sr_navigate_first_tab_to_mp(port):
            time.sleep(3)
        _sr_after_launch_hints()
        print("STAGE: CHROME_STARTED")
        return True

    if debug_ok:
        print("⚠️ 调试端口可用但无可用页 → 释放端口并启动新 Chrome…")
    else:
        print("⚠️ 调试端口不可用 → 启动 Chrome…")

    info = _chrome_launch_debug(port)
    if not info:
        print("❌ 无法启动 Chrome；可手动:")
        print(
            f"   open -a 'Google Chrome' --args --remote-debugging-port={port} {WECHAT_MP_HOME}"
        )
        return False
    _sr_after_launch_hints()
    print("STAGE: CHROME_STARTED")
    return True


def start_chrome_environment(port=DEFAULT_CDP_PORT):
    """兼容旧名：等同 run_start_chrome_flow。"""
    return run_start_chrome_flow(port)

def wait_for_login_confirmation(port=DEFAULT_CDP_PORT, max_wait_seconds=None, check_interval=DEFAULT_CHECK_INTERVAL):
    """
    统一等待登录/就绪。交互与非交互均走自动检测，不再等待回车。
    """
    if max_wait_seconds is None:
        max_wait_seconds = DEFAULT_MAX_WAIT_SECONDS
    print("\n⏳ 等待登录 / 就绪（自动检测）…")
    shot = capture_wechat_mp_screenshot(port=port)
    if shot:
        print(f"📷 截图: {shot}")
    return wait_until_ready_for_draft(
        port=port,
        max_seconds=max_wait_seconds,
        interval=check_interval,
    )

def create_draft_from_file(file_path, port=None):
    """从文件创建草稿"""
    if port is None:
        port = DEFAULT_CDP_PORT
    print("\n📝 创建贴图草稿…")
    script_dir = Path(__file__).parent
    log_file = script_dir / "skill.log"
    
    # 标准文件输入版本 (唯一推荐版本)
    draft_script = script_dir / "wechat_tietu_draft.py"
    if not draft_script.exists():
        print(f"❌ 找不到文件输入脚本: {draft_script}")
        return False
    
    title, content = validate_and_read_txt_file(str(file_path))
    if title is None or content is None:
        print_chrome_help()
        return False
    
    if not ensure_chrome_ready_for_draft(port):
        return False
    try:
        child_env = os.environ.copy()
        child_env["CDP_TIETU_CHILD"] = "1"
        child_env["CDP_TIETU_PORT"] = str(port)
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"# Run at {datetime.now().isoformat(timespec='seconds')} file={Path(file_path).name}\n")
            f.flush()
            result = subprocess.run(
                [sys.executable, str(draft_script), str(file_path)],
                stdout=f,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
                env=child_env,
            )
        if result.returncode == 0:
            print("STAGE: DRAFT_CREATED_OK")
            print("✅ 草稿创建完成")
            return True
        else:
            print("STAGE: DRAFT_FAILED")
            print(f"❌ 草稿创建失败 (退出码: {result.returncode})")
            try:
                with open(log_file, "r", encoding="utf-8", errors="replace") as lf:
                    tail = lf.read(8000)
                if _looks_like_proxy_error(tail):
                    print_proxy_vpn_hint()
            except Exception:
                pass
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 草稿创建超时")
        return False
    except Exception as e:
        print(f"❌ 创建草稿时出错: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='微信公众号贴图草稿创建工具')
    parser.add_argument('--file', type=str, help='从.txt文件创建草稿')
    parser.add_argument(
        '--port',
        type=int,
        default=DEFAULT_CDP_PORT,
        help=f'Chrome 调试端口 (默认: {DEFAULT_CDP_PORT}，避免与常见 9222 冲突)',
    )
    
    args = parser.parse_args()
    
    # 打印标题
    print_header()
    
    # 验证参数
    if not args.file:
        print("\n❌ 请指定 --file 参数:")
        print("   python3 skill_main.py --file 文章.txt")
        return
    
    success = False
    try:
        status, details = check_environment_status(args.port)
        blocked = False

        # STAGE: ENV_* 用于 OpenClaw/上游做稳定状态汇总（不影响人类可读输出）
        env_stage = {
            EnvStatus.READY: "ENV_READY",
            EnvStatus.CHROME_RUNNING_NOT_LOGGED: "ENV_CHROME_RUNNING_NOT_LOGGED",
            EnvStatus.CHROME_RUNNING_LOGIN_STATUS_UNKNOWN: "ENV_CHROME_RUNNING_LOGIN_STATUS_UNKNOWN",
            EnvStatus.CHROME_NOT_RUNNING: "ENV_CHROME_NOT_RUNNING",
            EnvStatus.NO_WECHAT_PAGE: "ENV_NO_WECHAT_PAGE",
            EnvStatus.PORT_OCCUPIED_NO_PAGES: "ENV_PORT_OCCUPIED_NO_PAGES",
            EnvStatus.ERROR: "ENV_ERROR",
            EnvStatus.UNKNOWN: "ENV_UNKNOWN",
        }.get(status, "ENV_UNKNOWN")
        print(f"STAGE: {env_stage}")

        # 步骤 2：任何「需拉起调试 Chrome」的状态都走同一套内置启动（原 start_real_chrome）
        need_launch = status in (
            EnvStatus.CHROME_NOT_RUNNING,
            EnvStatus.PORT_OCCUPIED_NO_PAGES,
            EnvStatus.ERROR,
        )
        if need_launch:
            if not run_start_chrome_flow(args.port):
                blocked = True
            else:
                status = None  # 刚启动或已复用实例，后面统一等待

        if not blocked:
            if status == EnvStatus.NO_WECHAT_PAGE:
                open_url_in_browser(WECHAT_MP_HOME)

            # 统一等待就绪，再创建草稿
            if not wait_for_login_confirmation(
                args.port,
                max_wait_seconds=DEFAULT_MAX_WAIT_SECONDS,
                check_interval=DEFAULT_CHECK_INTERVAL,
            ):
                success = False
            else:
                success = create_draft_from_file(args.file, port=args.port)
    except KeyboardInterrupt:
        print("\n👋 已中断")
        raise
    except Exception as e:
        err = str(e)
        print(f"\n❌ 执行异常: {err}")
        if _looks_like_proxy_error(err):
            print_proxy_vpn_hint()
        else:
            import traceback
            traceback.print_exc()
        success = False

    if success:
        print("STAGE: RESULT_OK")
        print("🎉 贴图草稿创建完成")
    else:
        print("STAGE: RESULT_FAILED")
        print("❌ 贴图草稿创建失败")

if __name__ == "__main__":
    main()