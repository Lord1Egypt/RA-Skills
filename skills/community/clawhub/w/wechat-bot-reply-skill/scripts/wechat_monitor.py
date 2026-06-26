#!/usr/bin/env python3
"""
WeChat Monitor Script v5 (Cross-Platform: Windows + macOS)
监控微信窗口变化，检测新消息并写入 pending 文件。

Windows: 使用 PeekabooWin (Node.js) 进行窗口截图
macOS:  使用 Peekaboo CLI (brew install) 进行窗口截图

Usage:
    python3 wechat_monitor.py [options]

Options:
    --contact NAME    监控的联系人名称（默认: mini）
    --interval SEC    截图间隔秒数（默认: 600=10分钟）
    --threshold BYTES 文件大小变化阈值（默认: 1000）
    --workdir PATH    工作目录（默认: 系统临时目录/wechat_mon）
    --pending PATH    pending 文件路径（默认: 系统临时目录/wechat_pending.txt）
    --wait SEC        等待主人回复的时间（默认: 600=10分钟）
    --engine ENGINE   自动化引擎: peekaboo(Mac) / peekaboo-win(Windows) / auto(自动检测, 默认)

Examples:
    python3 wechat_monitor.py --contact mini --interval 600
    python3 wechat_monitor.py --contact 老板 --interval 300 --threshold 2000 --engine peekaboo-win
"""

import subprocess, time, os, sys, platform, argparse, json, shutil

# ============================================================
# 跨平台工具函数
# ============================================================

def get_platform():
    """返回 'windows' 或 'macos'"""
    s = platform.system().lower()
    if s == "windows":
        return "windows"
    elif s == "darwin":
        return "macos"
    else:
        return s

def get_temp_dir():
    """返回系统临时目录"""
    return os.path.join(tempfile.gettempdir(), "wechat_mon") if 'tempfile' in dir() else (
        os.environ.get("TEMP", "/tmp") if get_platform() == "windows" else "/tmp"
    )

def get_default_workdir():
    """返回默认工作目录"""
    if get_platform() == "windows":
        tmp = os.environ.get("TEMP", "C:\\Temp")
        return os.path.join(tmp, "wechat_mon")
    else:
        return "/tmp/wechat_mon"

def get_default_pending():
    """返回默认 pending 文件路径"""
    if get_platform() == "windows":
        tmp = os.environ.get("TEMP", "C:\\Temp")
        return os.path.join(tmp, "wechat_pending.txt")
    else:
        return "/tmp/wechat_pending.txt"

# ============================================================
# 截图引擎抽象层
# ============================================================

class ScreenshotEngine:
    """截图引擎基类"""
    def take_screenshot(self, path, app_name="微信"):
        raise NotImplementedError

    def get_app_name(self):
        return "微信"

class PeekabooMacEngine(ScreenshotEngine):
    """macOS Peekaboo CLI 截图引擎"""
    def take_screenshot(self, path, app_name="微信"):
        r = subprocess.run(
            ["peekaboo", "image", "--mode", "window",
             "--app", app_name, "--retina", "--path", path],
            capture_output=True, text=True, timeout=15
        )
        if r.returncode != 0:
            print(f"  Peekaboo stderr: {r.stderr.strip()}", flush=True)
        return r.returncode == 0

class PeekabooWinEngine(ScreenshotEngine):
    """Windows PeekabooWin (Node.js) 截图引擎"""
    def __init__(self, peekaboo_win_dir=None):
        """
        Args:
            peekaboo_win_dir: PeekabooWin 安装目录。
                默认查找环境变量 PEEKABOO_WIN_DIR 或当前目录下的 peekaboo-win 文件夹
        """
        self.peekaboo_win_dir = peekaboo_win_dir or os.environ.get(
            "PEEKABOO_WIN_DIR", ""
        )
        self._resolved = False
        self._bin_path = None

    def _resolve_bin(self):
        """查找 peekaboo-win 可执行文件"""
        if self._resolved:
            return self._bin_path is not None

        candidates = []
        # 1. 指定目录
        if self.peekaboo_win_dir:
            candidates.append(os.path.join(self.peekaboo_win_dir, "bin", "peekaboo-win.js"))
            candidates.append(os.path.join(self.peekaboo_win_dir, "bin", "peekaboo-win.cmd"))

        # 2. 全局 node_modules
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            candidates.append(os.path.join(appdata, "npm", "node_modules",
                                           "peekaboo-win", "bin", "peekaboo-win.js"))

        # 3. PATH 中查找
        for p in os.environ.get("PATH", "").split(os.pathsep):
            candidates.append(os.path.join(p, "peekaboo-win"))
            candidates.append(os.path.join(p, "peekaboo-win.cmd"))

        for c in candidates:
            if os.path.isfile(c):
                self._bin_path = c
                self._resolved = True
                return True

        # 4. 尝试 npx
        self._bin_path = "npx"
        self._use_npx = True
        self._resolved = True
        return True

    def take_screenshot(self, path, app_name="微信"):
        if not self._resolve_bin():
            print("  PeekabooWin 未找到！请设置 PEEKABOO_WIN_DIR 环境变量", flush=True)
            return False

        cmd = []
        if hasattr(self, '_use_npx') and self._use_npx:
            cmd = ["npx", "peekaboo-win", "screen", "capture",
                   "--output", path]
        else:
            cmd = ["node", self._bin_path, "screen", "capture",
                   "--output", path]

        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if r.returncode != 0:
                print(f"  PeekabooWin stderr: {r.stderr.strip()}", flush=True)
            return r.returncode == 0
        except FileNotFoundError:
            print("  PeekabooWin 执行失败，请确认 Node.js 22+ 已安装", flush=True)
            return False

def create_engine(engine_name=None):
    """创建截图引擎实例"""
    plat = get_platform()

    if engine_name == "auto" or engine_name is None:
        engine_name = "peekaboo" if plat == "macos" else "peekaboo-win"

    if engine_name == "peekaboo":
        if plat == "windows":
            print("[警告] 在 Windows 上指定了 peekaboo (macOS)，尝试使用 peekaboo-win 替代", flush=True)
            return PeekabooWinEngine()
        return PeekabooMacEngine()

    elif engine_name == "peekaboo-win":
        if plat == "macos":
            print("[警告] 在 macOS 上指定了 peekaboo-win (Windows)，尝试使用 peekaboo 替代", flush=True)
            return PeekabooMacEngine()
        return PeekabooWinEngine()

    else:
        print(f"[错误] 未知的引擎: {engine_name}，可选: peekaboo / peekaboo-win / auto", flush=True)
        sys.exit(1)

# ============================================================
# 核心监控逻辑
# ============================================================

def parse_args():
    p = argparse.ArgumentParser(description="WeChat 新消息监控 v5 (跨平台)")
    p.add_argument("--contact", default="mini", help="监控的联系人")
    p.add_argument("--interval", type=int, default=600, help="截图间隔(秒, 默认600=10分钟)")
    p.add_argument("--threshold", type=int, default=1000, help="大小变化阈值(字节)")
    p.add_argument("--workdir", default=None, help="工作目录(默认自动)")
    p.add_argument("--pending", default=None, help="pending文件路径(默认自动)")
    p.add_argument("--wait", type=int, default=600, help="等待主人回复的时间(秒, 默认600=10分钟)")
    p.add_argument("--engine", default="auto",
                   choices=["auto", "peekaboo", "peekaboo-win"],
                   help="自动化引擎(默认auto自动检测)")
    p.add_argument("--peekaboo-win-dir", default=None,
                   help="PeekabooWin 安装目录(Windows), 也可用 PEEKABOO_WIN_DIR 环境变量")
    return p.parse_args()

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def write_pending(pending_path, screenshot_path, contact):
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(pending_path, "w", encoding="utf-8") as f:
        f.write(f"DETECTED:{ts}\n")
        f.write(f"SCREENSHOT:{screenshot_path}\n")
        f.write(f"CONTACT:{contact}\n")
    log(f"新消息已检测 | 时间:{ts} | 信号:{pending_path}")

def clear_pending(pending_path):
    if os.path.exists(pending_path):
        os.remove(pending_path)

def check_dependencies(engine):
    """检查必要的依赖是否已安装"""
    plat = get_platform()

    if plat == "macos":
        # 检查 peekaboo 是否安装
        r = subprocess.run(["which", "peekaboo"], capture_output=True, text=True)
        if r.returncode != 0:
            print("[错误] Peekaboo CLI 未安装！", flush=True)
            print("  请执行: brew install steipete/peekaboo/peekaboo", flush=True)
            print("  官方文档: https://peekaboo.sh/install.html", flush=True)
            return False

        # 检查权限
        r = subprocess.run(["peekaboo", "permissions"], capture_output=True, text=True, timeout=10)
        if r.returncode != 0:
            print("[警告] Peekaboo 权限可能未完全授予", flush=True)
            print("  请检查: 系统设置 → 隐私与安全 → 屏幕录制 / 辅助功能", flush=True)

    elif plat == "windows":
        # 检查 Node.js
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if r.returncode != 0:
            print("[错误] Node.js 未安装！", flush=True)
            print("  请从 https://nodejs.org 下载安装 Node.js 22+", flush=True)
            return False
        ver = r.stdout.strip().lstrip("v")
        major = int(ver.split(".")[0])
        if major < 22:
            print(f"[警告] Node.js 版本为 {ver}，建议使用 22+", flush=True)

        # 检查 PeekabooWin
        if isinstance(engine, PeekabooWinEngine):
            if not engine._resolve_bin():
                print("[错误] PeekabooWin 未找到！", flush=True)
                print("  请执行以下步骤安装:", flush=True)
                print("    git clone https://github.com/FelixKruger/PeekabooWin", flush=True)
                print("    cd PeekabooWin && npm install", flush=True)
                print("  然后设置环境变量:", flush=True)
                print("    set PEEKABOO_WIN_DIR=C:\\path\\to\\PeekabooWin", flush=True)
                return False

    return True

def monitor(args, engine):
    workdir = args.workdir or get_default_workdir()
    pending_path = args.pending or get_default_pending()
    os.makedirs(workdir, exist_ok=True)
    latest = os.path.join(workdir, "latest.png")
    contact = args.contact

    plat = get_platform()
    engine_label = "PeekabooWin" if isinstance(engine, PeekabooWinEngine) else "Peekaboo"

    log(f"=== WeChat 监控已启动 (v5 跨平台) ===")
    log(f"  平台: {plat}")
    log(f"  引擎: {engine_label}")
    log(f"  联系人: {contact}")
    log(f"  间隔: {args.interval}s | 阈值: {args.threshold}B")
    log(f"  工作目录: {workdir}")
    log(f"  Pending: {pending_path}")
    log(f"  Ctrl+C 停止\n")

    round_num = 0
    prev_size = 0

    while True:
        round_num += 1

        # 如果 pending 文件存在，等待主 agent 处理
        if os.path.exists(pending_path):
            log(f"第{round_num}轮：等待回复处理中...")
            time.sleep(args.interval)
            if not os.path.exists(pending_path):
                log("回复已完成，重新设基准")
                engine.take_screenshot(latest)
                prev_size = os.path.getsize(latest) if os.path.exists(latest) else 0
            continue

        ok = engine.take_screenshot(latest)
        if not ok:
            log(f"第{round_num}轮截图失败")
            time.sleep(args.interval)
            continue

        cur_size = os.path.getsize(latest)
        diff = abs(cur_size - prev_size)

        if prev_size == 0:
            prev_size = cur_size
            log(f"第{round_num}轮：基准已设 | size={cur_size}")
            time.sleep(args.interval)
            continue

        if diff > args.threshold:
            log(f"第{round_num}轮：检测到变化！diff={diff}B")
            write_pending(pending_path, latest, contact)
            prev_size = cur_size
        else:
            prev_size = cur_size
            log(f"第{round_num}轮：无变化 | size={cur_size}")

        time.sleep(args.interval)

if __name__ == "__main__":
    try:
        args = parse_args()
        engine = create_engine(args.engine)

        # 如果指定了 peekaboo-win-dir，覆盖默认值
        if args.peekaboo_win_dir and isinstance(engine, PeekabooWinEngine):
            engine.peekaboo_win_dir = args.peekaboo_win_dir
            engine._resolved = False  # 强制重新查找

        if not check_dependencies(engine):
            sys.exit(1)

        monitor(args, engine)
    except KeyboardInterrupt:
        log("监控已停止")
        sys.exit(0)
