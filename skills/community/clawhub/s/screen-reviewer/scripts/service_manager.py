#!/usr/bin/env python3
"""
服务管理器 — screen-reviewer 的统一入口
用法:
    python service_manager.py start              启动截图守护进程
    python service_manager.py stop               停止守护进程
    python service_manager.py status             查看运行状态
    python service_manager.py pause              暂停截图（不停进程）
    python service_manager.py resume             恢复截图
    python service_manager.py report [日期]       生成复盘报告
    python service_manager.py cleanup [天数]      清理旧截图
    python service_manager.py install            安装 macOS 开机自启服务
    python service_manager.py uninstall          卸载开机自启服务
"""

import os
import sys
import signal
import subprocess
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import load_config, DATA_DIR, PID_FILE, PAUSE_FILE

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DAEMON_SCRIPT = os.path.join(SCRIPT_DIR, "capture_daemon.py")
REPORT_SCRIPT = os.path.join(SCRIPT_DIR, "report_generator.py")
VENV_PYTHON = os.path.join(DATA_DIR, "venv", "bin", "python")


def _python():
    """优先使用 venv 中的 Python，否则用当前解释器"""
    if os.path.isfile(VENV_PYTHON):
        return VENV_PYTHON
    return sys.executable

PLIST_LABEL_CAPTURE = "com.screen-reviewer.capture"
PLIST_LABEL_REPORT = "com.screen-reviewer.report"
PLIST_DIR = os.path.expanduser("~/Library/LaunchAgents")


# ── 进程管理 ──────────────────────────────────────────────


def _get_pid() -> int:
    """读取 PID 文件，返回 PID 或 0"""
    if not os.path.exists(PID_FILE):
        return 0
    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)  # 检查进程是否存活
        return pid
    except (ValueError, ProcessLookupError, PermissionError):
        os.remove(PID_FILE)
        return 0


def cmd_start():
    pid = _get_pid()
    if pid:
        print(f"守护进程已在运行 (PID={pid})")
        return

    python = _python()
    proc = subprocess.Popen(
        [python, DAEMON_SCRIPT],
        stdout=open(os.path.join(DATA_DIR, "logs", "daemon_stdout.log"), "a"),
        stderr=open(os.path.join(DATA_DIR, "logs", "daemon_stderr.log"), "a"),
        start_new_session=True,
    )
    time.sleep(1)
    new_pid = _get_pid()
    if new_pid:
        print(f"✅ 守护进程已启动 (PID={new_pid})")
    else:
        print(f"守护进程启动中... (子进程 PID={proc.pid})")


def cmd_stop():
    pid = _get_pid()
    if not pid:
        print("守护进程未运行")
        return
    os.kill(pid, signal.SIGTERM)
    for _ in range(10):
        time.sleep(0.5)
        if not _get_pid():
            print("✅ 守护进程已停止")
            return
    print("⚠️  进程未响应 SIGTERM，尝试 SIGKILL...")
    os.kill(pid, signal.SIGKILL)
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    print("已强制终止")


def cmd_status():
    pid = _get_pid()
    paused = os.path.exists(PAUSE_FILE)
    if pid:
        status = "暂停中" if paused else "运行中"
        print(f"状态: {status}  PID={pid}")
    else:
        print("状态: 未运行")

    # 统计今天的截图数量
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    shot_dir = os.path.join(DATA_DIR, "screenshots", today)
    if os.path.isdir(shot_dir):
        count = len([f for f in os.listdir(shot_dir) if f.endswith(".jpg")])
        print(f"今日截图: {count} 张")

    log_path = os.path.join(DATA_DIR, "logs", f"{today}.jsonl")
    if os.path.exists(log_path):
        with open(log_path) as f:
            lines = sum(1 for _ in f)
        print(f"今日日志: {lines} 条")


def cmd_pause():
    with open(PAUSE_FILE, "w") as f:
        f.write("paused")
    print("⏸️  截图已暂停（守护进程仍在运行，resume 恢复）")


def cmd_resume():
    if os.path.exists(PAUSE_FILE):
        os.remove(PAUSE_FILE)
    print("▶️  截图已恢复")


def cmd_report(date_str=None):
    from report_generator import generate_report
    report = generate_report(date_str)
    print(report)


def cmd_cleanup(days=None):
    from cleanup import cleanup_old_screenshots
    keep = int(days) if days else None
    cleanup_old_screenshots(keep)


# ── launchd 服务安装 ──────────────────────────────────────


def _write_plist(label: str, content: str):
    os.makedirs(PLIST_DIR, exist_ok=True)
    path = os.path.join(PLIST_DIR, f"{label}.plist")
    with open(path, "w") as f:
        f.write(content)
    return path


def cmd_install():
    python = _python()
    log_dir = os.path.join(DATA_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 截图守护进程 — 开机自启 & 保活
    capture_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_LABEL_CAPTURE}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python}</string>
        <string>{DAEMON_SCRIPT}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{log_dir}/daemon_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{log_dir}/daemon_stderr.log</string>
</dict>
</plist>"""

    # 每日报告 — 每天早上 8 点执行
    config = load_config()
    hour = config["report"]["generation_hour"]
    report_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_LABEL_REPORT}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python}</string>
        <string>{REPORT_SCRIPT}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>{hour}</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{log_dir}/report_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{log_dir}/report_stderr.log</string>
</dict>
</plist>"""

    p1 = _write_plist(PLIST_LABEL_CAPTURE, capture_plist)
    p2 = _write_plist(PLIST_LABEL_REPORT, report_plist)

    subprocess.run(["launchctl", "unload", p1], capture_output=True)
    subprocess.run(["launchctl", "unload", p2], capture_output=True)
    subprocess.run(["launchctl", "load", p1])
    subprocess.run(["launchctl", "load", p2])

    print(f"✅ 已安装 launchd 服务:")
    print(f"   截图守护: {p1}")
    print(f"   每日报告: {p2} (每天 {hour}:00)")
    print(f"\n首次使用需授权「屏幕录制」和「辅助功能」权限:")
    print(f"   系统设置 → 隐私与安全性 → 屏幕录制 → 勾选 Terminal/Python")


def cmd_uninstall():
    for label in [PLIST_LABEL_CAPTURE, PLIST_LABEL_REPORT]:
        path = os.path.join(PLIST_DIR, f"{label}.plist")
        if os.path.exists(path):
            subprocess.run(["launchctl", "unload", path], capture_output=True)
            os.remove(path)
    cmd_stop()
    print("✅ 已卸载 launchd 服务")


# ── 入口 ──────────────────────────────────────────────────

COMMANDS = {
    "start": lambda args: cmd_start(),
    "stop": lambda args: cmd_stop(),
    "status": lambda args: cmd_status(),
    "pause": lambda args: cmd_pause(),
    "resume": lambda args: cmd_resume(),
    "report": lambda args: cmd_report(args[0] if args else None),
    "cleanup": lambda args: cmd_cleanup(args[0] if args else None),
    "install": lambda args: cmd_install(),
    "uninstall": lambda args: cmd_uninstall(),
}

HELP = """
screen-reviewer 服务管理器

用法: python service_manager.py <命令> [参数]

命令:
  start              启动截图守护进程
  stop               停止守护进程
  status             查看运行状态
  pause              暂停截图
  resume             恢复截图
  report [日期]       生成复盘报告 (默认昨天，格式: 2026-03-22)
  cleanup [天数]      清理旧截图 (默认读配置)
  install            安装 macOS 开机自启服务
  uninstall          卸载开机自启服务
"""

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(HELP)
        sys.exit(1)
    cmd = sys.argv[1]
    extra = sys.argv[2:]
    COMMANDS[cmd](extra)
