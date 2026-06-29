#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# R-12 审计锚点
import os
DEFAULT_DATA_DIR_RAW = "skills/.standardization/triphasic-execution/data/"
"""
Problem Daemon — 常驻后台的问题监控守护进程（v4.1：双模式设计）
=============================================
v4.1 核心原则：daemon 仅在全局模式下运行（config.json 中 mode=global）。
按需模式下 daemon 不会启动（符合"不调用就不记录"的用户习惯）。

路径配置：
  环境变量 TRIPHASIC_HOME 或 --home 参数
  默认值 ~/.workbuddy/triphasic/

用法:
  python problem_daemon.py start          # 后台启动（仅全局模式生效）
  python problem_daemon.py start --fg     # 前台启动（调试）
  python problem_daemon.py stop           # 停止
  python problem_daemon.py status         # 查看状态
"""

import os
import sys
import json
import time
import signal
import hashlib
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from queue import Queue, Empty
from typing import Optional
import argparse
import re

# ============================================================================
# 路径配置
# ============================================================================
_SKILL_DIR = Path(__file__).resolve().parent.parent

def _find_standardization_dir() -> Path:
    p = _SKILL_DIR.resolve()
    for parent in [p] + list(p.parents):
        if parent.name == "skills" and parent.parent.name != "skills":
            return parent / ".standardization" / _SKILL_DIR.name
    return _SKILL_DIR.parent / ".standardization" / _SKILL_DIR.name

_DEFAULT_HOME = _find_standardization_dir()
_TRIPHASIC_HOME = Path(os.environ.get("TRIPHASIC_HOME", str(_DEFAULT_HOME)))


def get_home() -> Path:
    home = _TRIPHASIC_HOME
    home.mkdir(parents=True, exist_ok=True)
    return home


def get_logs_dir() -> Path:
    return get_home() / ".problem_logs"


def get_config_file() -> Path:
    return get_home() / "config.json"


def get_problems_jsonl() -> Path:
    return get_logs_dir() / "problems.jsonl"


def get_daemon_log() -> Path:
    return get_logs_dir() / "daemon.log"


def get_pid_file() -> Path:
    return get_logs_dir() / "daemon.pid"


def get_exec_pipe() -> Path:
    return get_home() / ".exec_output_pipe.txt"


# ============================================================================
# Windows 编码兼容
# ============================================================================
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

# ============================================================================
# 全局状态
# ============================================================================
DAEMON_NAME = "problem-daemon"
PID: Optional[int] = None
SHUTDOWN_EVENT = threading.Event()
PROBLEM_QUEUE = Queue()


# ============================================================================
# 工具函数
# ============================================================================
def load_config() -> dict:
    """加载配置"""
    default_path = Path(__file__).parent.parent / "assets" / "default_config.json"
    defaults = {}
    if default_path.exists():
        try:
            defaults = json.loads(default_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    user_path = get_config_file()
    if user_path.exists():
        try:
            user_cfg = json.loads(user_path.read_text(encoding="utf-8"))
            defaults.update(user_cfg)
        except Exception:
            pass
    return defaults


def log_daemon(msg: str, level: str = "INFO"):
    """守护进程自身日志"""
    get_logs_dir().mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}\n"
    with open(get_daemon_log(), "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
    if level == "ERROR":
        print(f"❌ {msg}", file=sys.stderr)


def save_problem(problem: dict):
    """追加保存问题记录"""
    get_logs_dir().mkdir(parents=True, exist_ok=True)
    with open(get_problems_jsonl(), "a", encoding="utf-8") as f:
        f.write(json.dumps(problem, ensure_ascii=False) + "\n")
        f.flush()


def get_problem_id(scene: str, symptom: str, command: str = "") -> str:
    key = f"{scene}|{symptom}|{command}"
    return hashlib.md5(key.encode()).hexdigest()[:8].upper()


def get_next_problem_number() -> int:
    log = get_problems_jsonl()
    if not log.exists():
        return 1
    numbers = []
    with open(log, "r", encoding="utf-8") as f:
        for line in f:
            try:
                p = json.loads(line.strip())
                num_str = str(p.get("number", "P0"))
                numbers.append(int(num_str.lstrip("P")))
            except (json.JSONDecodeError, ValueError):
                continue
    return max(numbers) + 1 if numbers else 1


def is_process_alive(pid: int) -> bool:
    """跨平台检查进程是否存在（无外部依赖）"""
    if sys.platform == "win32":
        try:
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH", "/FO", "CSV"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            # 输出格式: "python.exe","1234",... 或 "INFO: No tasks are running..."
            return str(pid) in result.stdout
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            return False


# ============================================================================
# 问题检测引擎
# ============================================================================
def detect_problem(output: str, command: str = "", exit_code: int = 0) -> Optional[dict]:
    """检测输出中是否包含异常/错误"""
    config = load_config()
    if not config.get("enabled", True):
        return None

    patterns = config.get("error_patterns", [])

    # 检查退出码
    if exit_code != 0:
        return {
            "id": get_problem_id("命令执行失败", f"退出码 {exit_code}", command),
            "number": f"P{get_next_problem_number():03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "scene": "命令执行失败",
            "symptom": f"命令退出码非零：{exit_code}",
            "cause": f"执行命令：{command[:200]}",
            "solution": "待分析",
            "status": "未解决",
            "raw_output": output[-10000:],
            "exit_code": exit_code,
        }

    # 检查输出中的错误模式
    for pattern in patterns:
        try:
            if re.search(pattern, output, re.IGNORECASE):
                return {
                    "id": get_problem_id("命令输出异常", f"匹配到{pattern}", command),
                    "number": f"P{get_next_problem_number():03d}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "scene": "命令输出异常",
                    "symptom": f"输出中匹配到错误模式：{pattern}",
                    "cause": f"执行命令：{command[:200]}\n输出片段:\n{output[-500:]}",
                    "solution": "待分析",
                    "status": "未解决",
                    "raw_output": output[-10000:],
                }
        except re.error:
            continue

    return None


# ============================================================================
# 后台写入线程
# ============================================================================
def problem_writer_thread():
    """从队列读取问题并写入文件"""
    log_daemon("问题写入线程已启动")
    consecutive_errors = 0

    while not SHUTDOWN_EVENT.is_set():
        try:
            try:
                problem = PROBLEM_QUEUE.get(timeout=0.1)
            except Empty:
                continue

            save_problem(problem)
            consecutive_errors = 0
            log_daemon(f"问题已记录：{problem['number']} | {problem['scene']} | {problem['symptom'][:50]}")

        except Exception as e:
            consecutive_errors += 1
            if consecutive_errors > 5:
                log_daemon(f"写入线程连续失败{consecutive_errors}次：{e}", "ERROR")
                break
            time.sleep(0.5)

    log_daemon("问题写入线程已停止")


# ============================================================================
# 管道监控线程
# ============================================================================
def monitor_pipe_thread():
    """监控 exec 输出管道文件"""
    pipe = get_exec_pipe()
    log_daemon(f"开始监控管道文件：{pipe}")

    last_position = 0
    consecutive_errors = 0

    while not SHUTDOWN_EVENT.is_set():
        try:
            if pipe.exists():
                current_size = pipe.stat().st_size

                if current_size > last_position:
                    with open(pipe, "r", encoding="utf-8", errors="replace") as f:
                        f.seek(last_position)
                        new_content = f.read()
                        last_position = current_size

                    if new_content.strip():
                        try:
                            lines = new_content.split("\n\n", 1)
                            header = lines[0].strip()
                            output = lines[1] if len(lines) > 1 else ""

                            parts = header.split("|", 2)
                            if len(parts) >= 3:
                                exit_code = int(parts[1]) if parts[1].isdigit() else 0
                                problem = detect_problem(output, parts[2], exit_code)
                                if problem:
                                    PROBLEM_QUEUE.put(problem)

                        except Exception as e:
                            log_daemon(f"解析管道内容失败：{e}", "ERROR")

                # 防止文件过大
                if current_size > 10 * 1024 * 1024:
                    with open(pipe, "w", encoding="utf-8") as f:
                        pass
                    last_position = 0

            consecutive_errors = 0
            time.sleep(load_config().get("poll_interval_ms", 100) / 1000)

        except Exception as e:
            consecutive_errors += 1
            if consecutive_errors > 5:
                log_daemon(f"监控线程连续失败{consecutive_errors}次：{e}", "ERROR")
                break
            time.sleep(0.5)

    log_daemon("管道监控线程已停止")


# ============================================================================
# 守护进程主循环
# ============================================================================
def run_daemon():
    """守护进程主循环（v4.1：仅全局模式启动）"""
    global PID

    # v4.1：检查 mode，非全局模式直接退出
    config = load_config()
    if config.get("mode") != "global":
        print("❌ daemon 不会启动：当前为按需调用模式（config.json 中 mode=on_demand）")
        print("   → 如需全局自动监控，请运行：python install.py --mode global")
        print("   → 或手动修改 TRIPHASIC_HOME/config.json：\"mode\": \"global\"")
        return 1

    # 检查 daemon.enabled 配置
    if not config.get("daemon", {}).get("enabled", False):
        print("❌ daemon 不会启动：config.json 中 daemon.enabled=false")
        print("   → 请修改 TRIPHASIC_HOME/config.json：\"daemon\": {\"enabled\": true}")
        return 1

    PID = os.getpid()

    pid_file = get_pid_file()
    pid_file.parent.mkdir(parents=True, exist_ok=True)
    pid_file.write_text(str(PID), encoding="utf-8")

    log_daemon("=" * 60)
    log_daemon(f"Problem Daemon 已启动 (PID={PID})")
    log_daemon(f"🔵 模式：全局自动（mode=global）")
    log_daemon(f"监控管道：{get_exec_pipe()}")
    log_daemon(f"问题日志：{get_problems_jsonl()}")
    log_daemon(f"TRIPHASIC_HOME：{get_home()}")
    log_daemon("=" * 60)

    # 信号处理
    def signal_handler(signum, frame):
        sig_name = {signal.SIGTERM: "SIGTERM", signal.SIGINT: "SIGINT"}.get(signum, str(signum))
        log_daemon(f"收到信号 {sig_name}，正在关闭...")
        SHUTDOWN_EVENT.set()

    signal.signal(signal.SIGTERM, signal_handler)
    try:
        signal.signal(signal.SIGINT, signal_handler)
    except Exception:
        pass

    # 启动后台线程
    writer = threading.Thread(target=problem_writer_thread, daemon=True)
    monitor = threading.Thread(target=monitor_pipe_thread, daemon=True)
    writer.start()
    monitor.start()

    log_daemon("所有监控线程已启动，等待任务...")

    try:
        while not SHUTDOWN_EVENT.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        log_daemon("收到 Ctrl+C，正在关闭...")
        SHUTDOWN_EVENT.set()

    log_daemon("守护进程正在关闭...")
    if pid_file.exists():
        pid_file.unlink()
    log_daemon("Problem Daemon 已停止")


# ============================================================================
# CLI 命令
# ============================================================================
def cmd_start(args):
    """启动守护进程（v4.1：检查模式后启动）"""
    pid_file = get_pid_file()

    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            if is_process_alive(pid):
                print(f"⚠️  守护进程已在运行 (PID={pid})")
                print(f"   使用 `python problem_daemon.py stop` 先停止它。")
                return 1
            else:
                pid_file.unlink()
        except (ValueError, OSError):
            pid_file.unlink()

    # v4.1：启动前提示当前模式
    config = load_config()
    mode = config.get("mode", "on_demand")
    print(f"🚀 Problem Daemon 启动中...")
    print(f"   🎯 当前模式：{'🔵 全局自动' if mode == 'global' else '🟢 按需调用'}")
    if mode != "global":
        print(f"   ⚠️  按需模式下 daemon 不会监控 exec 管道，仅手动调用 CLI 记录问题")

    if args.fg:
        print("🚀 Problem Daemon 启动中（前台模式）...")
        print(f"   TRIPHASIC_HOME: {get_home()}")
        run_daemon()
        return 0
    else:
        cmd = [sys.executable, __file__, "start", "--fg", "--home", str(get_home())]
        proc = subprocess.Popen(
            cmd,
            stdout=open(get_daemon_log(), "a", encoding="utf-8"),
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
        )
        print(f"✅ Problem Daemon 已启动 (PID={proc.pid})")
        print(f"   🎯 当前模式：{'🔵 全局自动' if mode == 'global' else '🟢 按需调用'}")
        if mode == "global":
            print(f"   → exec 管道异常将自动捕获并记录到 PROBLEMS.md")
        return 0


def cmd_stop(args):
    """停止守护进程"""
    pid_file = get_pid_file()

    if not pid_file.exists():
        print("❌ 守护进程未运行（无 PID 文件）")
        return 1

    try:
        pid = int(pid_file.read_text().strip())

        if sys.platform == "win32":
            # Windows: 使用 taskkill
            subprocess.run(["taskkill", "/PID", str(pid), "/F"],
                         capture_output=True, timeout=10)
        else:
            try:
                os.kill(pid, signal.SIGTERM)
                for _ in range(10):
                    try:
                        os.kill(pid, 0)
                        time.sleep(0.5)
                    except ProcessLookupError:
                        break
                else:
                    os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

        pid_file.unlink()
        print(f"✅ Problem Daemon 已停止 (PID={pid})")
        return 0

    except Exception as e:
        print(f"❌ 停止失败：{e}")
        return 1


def cmd_status(args):
    """查看守护进程状态（v4.1：显示当前模式）"""
    pid_file = get_pid_file()

    if not pid_file.exists():
        config = load_config()
        mode = config.get("mode", "on_demand")
        print("🔴 Problem Daemon 未运行")
        print(f"   🎯 当前模式：{'🟢 按需调用' if mode == 'on_demand' else '🔵 全局自动'}")
        if mode == "on_demand":
            print(f"   💡 提示：按需模式下 daemon 无需启动，手动调用 CLI 即可")
            print(f"      python problem_logger.py add \"错误信息\"")
        return 1

    try:
        pid = int(pid_file.read_text().strip())

        if not is_process_alive(pid):
            print("🔴 Problem Daemon 不存在（僵尸进程），正在清理...")
            pid_file.unlink()
            return 1

        print("🟢 Problem Daemon 正在运行")
        print(f"   PID: {pid}")
        config = load_config()
        mode = config.get("mode", "on_demand")
        print(f"   🎯 当前模式：{'🔵 全局自动' if mode == 'global' else '🟢 按需调用'}")
        print(f"   TRIPHASIC_HOME: {get_home()}")
        print(f"   日志：{get_daemon_log()}")
        print(f"   问题日志：{get_problems_jsonl()}")

        # 统计
        problems_file = get_problems_jsonl()
        if problems_file.exists():
            with open(problems_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            total = len([l for l in lines if l.strip()])
            resolved = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    if json.loads(line).get("status") == "已解决":
                        resolved += 1
                except json.JSONDecodeError:
                    continue
            print(f"   问题统计：{total} 条（已解决 {resolved}）")

        return 0

    except Exception as e:
        print(f"❌ 状态检查失败：{e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Problem Daemon — 常驻后台的问题监控守护进程",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python problem_daemon.py start          # 后台启动
  python problem_daemon.py start --fg     # 前台启动（调试）
  python problem_daemon.py stop           # 停止
  python problem_daemon.py status         # 查看状态

环境变量:
  TRIPHASIC_HOME  数据目录（默认 ~/.workbuddy/triphasic/）
        """,
    )

    parser.add_argument("--home", type=str, default=None, help="覆盖 TRIPHASIC_HOME")

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    p_start = subparsers.add_parser("start", help="启动守护进程")
    p_start.add_argument("--fg", action="store_true", help="前台运行（调试用）")

    subparsers.add_parser("stop", help="停止守护进程")
    subparsers.add_parser("status", help="查看状态")

    args = parser.parse_args()

    if args.home:
        global _TRIPHASIC_HOME
        _TRIPHASIC_HOME = Path(args.home).expanduser().resolve()

    if not args.command:
        parser.print_help()
        return 0

    get_home()  # 确保目录存在

    if args.command == "start":
        return cmd_start(args)
    elif args.command == "stop":
        return cmd_stop(args)
    elif args.command == "status":
        return cmd_status(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
