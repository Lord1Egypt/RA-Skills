"""browser.py — Chromium CDP 常驻浏览器管理（跨平台）

核心架构：启动一个【常驻】Chromium 进程（带 --remote-debugging-port），
AI 通过 CDP 端口反复连接操纵同一个浏览器实例。
- 浏览器不随脚本退出 → 2FA 验证码不会因"重开浏览器"而失效
- 一律无头模式（--headless=new）：AI 自动流程 / WSL 无显示器 / 全新机器
- profile 复用（runtime/profiles/cdp_profile），CAS cookies 全校通用

端口默认 9222，pid 记录在 runtime/browser/cdp.pid，端口记录在 cdp.port。
"""
import sys
import os
import json
import time
import shutil
import signal
import subprocess
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common

CDP_PORT = 9222
DEBUG_PORT_RANGE = (9200, 9300)


def _playwright():
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        return None


def _shared_resolver():
    """调用 skills/_shared/opencode_paths.py 的统一浏览器解析器（全仓库唯一实现）。

    技能包若被拷出 skills/ 目录（不在 _shared 旁）则返回 None，由本模块兜底。"""
    for parent in list(Path(__file__).resolve().parents)[:8]:
        cand = parent / "_shared" / "opencode_paths.py"
        if cand.is_file():
            if str(cand.parent) not in sys.path:
                sys.path.insert(0, str(cand.parent))
            try:
                import opencode_paths
                return opencode_paths.chromium()
            except Exception:
                return None
    return None


def chromium_executable():
    """定位本机 Chromium。

    顺序：① 统一解析器（_shared/opencode_paths.py：env → Playwright 自报 → 各安装根 glob）
          ② 本模块兜底 glob（技能包被拷出 skills/ 时用；已覆盖 chrome-linux64/chrome-win64）
    """
    exe = _shared_resolver()
    if exe and os.path.isfile(exe):
        return exe

    exe = os.environ.get("OPENCODE_CHROMIUM") or os.environ.get("CHROME_PATH")
    if exe and os.path.isfile(exe):
        return exe
    plat = common.detect_platform()
    import glob
    home = str(Path.home())
    roots = []
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        roots.append(os.environ["PLAYWRIGHT_BROWSERS_PATH"])
    data = os.environ.get("OPENCODE_DATA_DIR") or str(Path.home() / ".local" / "share" / "opencode")
    roots.append(os.path.join(data, "chromium"))
    if plat == "windows":
        roots.append(os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local"))
        pats = []
        for r in roots:
            pats += [os.path.join(r, "chromium-*", "chrome-win64", "chrome.exe"),
                     os.path.join(r, "chromium-*", "chrome-win", "chrome.exe"),
                     os.path.join(r, "ms-playwright", "chromium-*", "chrome-win64", "chrome.exe"),
                     os.path.join(r, "ms-playwright", "chromium-*", "chrome-win", "chrome.exe")]
    elif plat == "macos":
        pats = [f"{home}/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
                f"{home}/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium"]
        for r in roots:
            pats += [os.path.join(r, "chromium-*", "chrome-mac*", "Chromium.app", "Contents", "MacOS", "Chromium"),
                     os.path.join(r, "ms-playwright", "chromium-*", "chrome-mac*", "Chromium.app", "Contents", "MacOS", "Chromium")]
    else:
        pats = [f"{home}/.cache/ms-playwright/chromium-*/chrome-linux64/chrome",
                f"{home}/.cache/ms-playwright/chromium-*/chrome-linux/chrome"]
        for r in roots:
            pats += [os.path.join(r, "chromium-*", "chrome-linux64", "chrome"),
                     os.path.join(r, "chromium-*", "chrome-linux", "chrome"),
                     os.path.join(r, "openclaw-browser")]
    for pat in pats:
        cands = sorted(glob.glob(pat))
        if cands:
            return cands[-1]
    return None


def _default_profile():
    """profile 路径用环境变量索引（OPENCODE_CHROMIUM_PROFILE），否则回退 skill runtime。"""
    root = os.environ.get("OPENCODE_CHROMIUM_PROFILE")
    if root:
        return os.path.join(root, "tsinghua_cdp_profile")
    return str(common.runtime_dir("profiles", "cdp_profile"))


def _cdp_dir():
    return common.runtime_dir("browser")


def _pid_file():
    return os.path.join(str(_cdp_dir()), "cdp.pid")


def _port_file():
    return os.path.join(str(_cdp_dir()), "cdp.port")


# ---- 跨进程互斥锁：同一时刻只允许一个脚本操作共享 Chromium（2026-09-16） ----
# 背景：全部 CDP 脚本共用同一个常驻 Chromium，且 connect_cdp() 复用 context.pages[0]。
# 两个脚本并行 → 抢同一个标签页 → CAS 登录表单被重复提交 → CAS 回通用错误
# 「用户名或密码不正确」，两个进程一起失败（曾导致 cron 的两步都返回 status=error）。
# 本锁把「并行」降级为「串行排队」，对齐 SKILL.md 的"严禁两个 CDP 脚本并行，全部串行执行"。
_LOCK_FD = None
_LOCK_ENV = "CAMPUS_BROWSER_LOCK"   # 子进程继承此变量即视为「已持锁」，避免父等子、子抢父的自锁死


def _lock_timeout():
    try:
        return float(os.environ.get("CAMPUS_BROWSER_LOCK_TIMEOUT") or 600)
    except Exception:
        return 600.0


def _lock_file():
    return os.path.join(str(_cdp_dir()), "campus.lock")


def _lock_inherited():
    """父进程已持锁并 fork 出本进程（如 learn.py 子调用 login.py）→ 直接视为已持锁。

    flock/msvcrt 锁不可跨进程重入：父持锁等子进程、子进程再抢同一把锁 = 自锁死。
    """
    return os.environ.get(_LOCK_ENV) == _lock_file()


def acquire_run_lock(timeout=None):
    """获取共享浏览器的跨进程互斥锁。可重入（本进程已持锁 / 子进程继承）→ 直接 True。

    拿不到（超时）返回 False，由调用方报错。锁随进程退出由 OS 自动释放，不留死锁。
    """
    global _LOCK_FD
    if _LOCK_FD is not None or _lock_inherited():
        return True
    path = _lock_file()
    try:
        _cdp_dir().mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
        if os.fstat(fd).st_size == 0:
            os.write(fd, b"0")
        os.lseek(fd, 0, os.SEEK_SET)
    except Exception:
        # 锁文件不可用（runtime 只读 / 权限）→ 退回旧行为，不因锁本身打断脚本
        return True
    deadline = time.time() + (timeout if timeout is not None else _lock_timeout())
    while True:
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            _LOCK_FD = fd
            os.environ[_LOCK_ENV] = path
            common.log("[browser] 已获得共享浏览器互斥锁")
            return True
        except OSError:
            if time.time() >= deadline:
                try:
                    os.close(fd)
                except Exception:
                    pass
                return False
            time.sleep(1)


def _require_run_lock():
    """拿不到锁 → 输出 JSON 错误并退出（脚本间串行，不静默降级回并行）。"""
    if acquire_run_lock():
        return
    common.output_json({
        "status": "error",
        "error": "browser_busy",
        "message": "另一个校园脚本正在使用共享浏览器，等待 %d 秒仍未释放。请串行执行"
                   "（不要并行跑两个 campus 脚本，也不要把两条命令拆成并行的两次 exec）。" % int(_lock_timeout()),
    })
    sys.exit(1)


def _save_port(port):
    _cdp_dir().mkdir(parents=True, exist_ok=True)
    with open(_port_file(), "w") as f:
        f.write(str(port))


def _load_port():
    if os.path.exists(_port_file()):
        try:
            return int(open(_port_file()).read().strip())
        except Exception:
            pass
    return CDP_PORT


def _pid_alive(pid):
    if not pid:
        return False
    if os.name == "nt":
        # Windows 的 os.kill(pid, 0) 不支持信号 0，会对存活进程抛 OSError(22)
        # → 用 tasklist 精确判断进程是否存在
        try:
            r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True,
                               text=True, timeout=10)
            return str(pid) in r.stdout
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False
    except OSError:
        return False


def is_running():
    """CDP 浏览器是否已在运行（以调试端口响应为准）。"""
    try:
        import urllib.request
        port = _load_port()
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2)
        return True
    except Exception:
        return False


def _load_pid():
    if os.path.exists(_pid_file()):
        try:
            return int(open(_pid_file()).read().strip())
        except Exception:
            pass
    return None


def _free_port(start):
    import socket
    for port in range(start, DEBUG_PORT_RANGE[1]):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start


def _kill_port_process(port):
    """杀掉占用指定端口的进程（孤儿残留 Chrome 清理）。"""
    if os.name != "nt":
        return
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess"],
            capture_output=True, text=True, timeout=15)
        for pid in r.stdout.split():
            pid = pid.strip()
            if pid.isdigit():
                subprocess.run(["taskkill", "/F", "/T", "/PID", pid], capture_output=True)
    except Exception:
        pass


def _clean_broken_cache(profile_path):
    """清理 Chromium profile 中可能导致启动崩溃的损坏缓存目录。

    新机/残留场景下，GPU 缓存（GraphiteDawnCache 等）损坏会使 Chrome 启动即
    崩溃退出（CDP 端口无响应，login 报 ECONNRESET）。删除这些目录可自愈。
    只清理可再生的缓存目录，不碰 cookies/login 数据。
    """
    for name in ("GraphiteDawnCache", "old_GraphiteDawnCache_000",
                 "GPUCache", "GrShaderCache", "ShaderCache",
                 "DawnCache", "DawnGraphiteCache"):
        p = os.path.join(profile_path, name)
        if os.path.isdir(p):
            try:
                shutil.rmtree(p)
                common.log(f"[browser] 已清理损坏缓存: {name}")
            except Exception as e:
                common.log(f"[browser] 清理缓存失败 {name}: {e}")


def _launch_browser(cmd, port, profile_path):
    """启动 Chromium 并等待 CDP 端口就绪。失败则杀进程并返回 None。"""
    flags = 0
    if os.name == "nt":
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | 0x08000000  # CREATE_NO_WINDOW
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            creationflags=flags, close_fds=True)
    _cdp_dir().mkdir(parents=True, exist_ok=True)
    with open(_pid_file(), "w") as f:
        f.write(str(proc.pid))

    # 等调试端口就绪
    for _ in range(30):
        time.sleep(0.5)
        if _cdp_ready(port):
            return proc
    # 未就绪：杀掉残留进程，避免孤儿 chrome 占用端口
    try:
        if proc.poll() is None:
            if os.name == "nt":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
            else:
                os.kill(proc.pid, signal.SIGTERM)
    except Exception:
        pass
    return None


def start_cdp(headed=False, profile=None, extra_args=None):
    """启动 CDP 常驻 Chromium（若已运行则复用）。返回 (port, profile_path)。

    若端口有响应但非本进程（孤儿/残留），先尝试杀掉再启动，避免端口冲突。
    extra_args: 额外 Chrome 启动参数（如移除 --disable-blink-features=AutomationControlled
                以解决某些站点 ERR_BLOCKED_BY_CLIENT）。
    """
    _require_run_lock()

    # 孤儿清理：端口有响应但 pid 不匹配 → 杀掉残留进程
    if is_running():
        pid = _load_pid()
        if _pid_alive(pid):
            return _load_port(), (profile or _default_profile())
        common.log("[browser] 检测到孤儿浏览器（端口响应但进程不匹配），清理")
        _kill_port_process(_load_port())
        try:
            os.remove(_pid_file())
        except Exception:
            pass

    exe = chromium_executable()
    if not exe:
        raise RuntimeError("Chromium 未找到，先运行 install 模块")

    profile_path = profile or _default_profile()
    os.makedirs(profile_path, exist_ok=True)

    # 选一个当前空闲端口
    port = _free_port(CDP_PORT)
    _save_port(port)

    # 一律无头模式（headless）:
    # - AI 自动流程 / WSL 无显示器 / 全新机器（产品决策：全部 headless，不需人工浏览器）
    # - --headed 参数保留仅向后兼容，但忽略（恒 headless）
    base_flags = ["--no-first-run", "--no-default-browser-check",
                  "--disable-gpu", "--disable-dev-shm-usage",
                  "--no-sandbox"]
    if extra_args is None:
        # 默认保留自动化 flag（常规场景）
        base_flags.append("--disable-blink-features=AutomationControlled")
    else:
        base_flags = [f for f in base_flags if f != "--disable-blink-features=AutomationControlled"]
        base_flags += extra_args
    cmd = [exe, "--headless=new"] + [
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_path}",
    ] + base_flags + ["about:blank"]

    proc = _launch_browser(cmd, port, profile_path)
    if proc is None:
        # 启动失败（常见：profile 损坏 GPU 缓存导致 Chrome 崩溃）→ 清缓存重试一次
        common.log("[browser] CDP 启动失败，清理损坏缓存后重试")
        _clean_broken_cache(profile_path)
        proc = _launch_browser(cmd, port, profile_path)
    if proc is None:
        raise RuntimeError(f"CDP 浏览器启动失败，端口 {port} 未就绪（清缓存重试仍失败）")
    return port, profile_path


def is_port_in_use(port):
    import socket
    with socket.socket() as s:
        try:
            s.bind(("127.0.0.1", port))
            return False
        except OSError:
            return True


def _cdp_ready(port):
    try:
        import urllib.request
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2)
        return True
    except Exception:
        return False


def connect_cdp(port=None):
    """通过 CDP 连接常驻浏览器。返回 (pw, browser, context, page)。"""
    _require_run_lock()
    sp = _playwright()
    if sp is None:
        raise RuntimeError("playwright 未安装，先运行 install 模块")
    port = port or _load_port()
    pw = sp().start()
    browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    page = context.pages[0] if context.pages else context.new_page()
    return pw, browser, context, page


def stop_cdp():
    """关闭 CDP 浏览器进程。

    双保险：按 pid 文件杀 + 按调试端口杀（pid 文件可能因 Chrome 子进程
    重建/重启而过期，端口监听者才是真实浏览器进程）。
    """
    pid = _load_pid()
    if pid and _pid_alive(pid):
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
            else:
                os.kill(pid, signal.SIGTERM)
        except Exception:
            pass
    # 端口兜底：pid 文件过期/缺失时，杀端口监听进程
    if os.name == "nt":
        port = _load_port()
        if is_port_in_use(port):
            _kill_port_process(port)
    for f in (_pid_file(), _port_file()):
        try:
            os.remove(f)
        except Exception:
            pass


def ensure_ready():
    """检查 playwright + chromium 是否可用，供 install/selfcheck 调用。"""
    sp = _playwright()
    if sp is None:
        return {"ok": False, "missing": "playwright"}
    exe = chromium_executable()
    if not exe:
        return {"ok": False, "missing": "chromium"}
    return {"ok": True, "chromium": exe, "cdp_running": is_running()}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--start", action="store_true", help="启动 CDP 浏览器")
    ap.add_argument("--stop", action="store_true", help="关闭 CDP 浏览器")
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()
    if args.check:
        r = ensure_ready()
        r["status"] = "ok" if r["ok"] else "error"
        common.output_json(r)
        sys.exit(0 if r["ok"] else 1)
    if args.start:
        port, prof = start_cdp(headed=args.headed)
        common.output_json({"status": "ok", "port": port, "profile": prof})
    elif args.stop:
        stop_cdp()
        common.output_json({"status": "ok", "message": "CDP 浏览器已关闭"})
