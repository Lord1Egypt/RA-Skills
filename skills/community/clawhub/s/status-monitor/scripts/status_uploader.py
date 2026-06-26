#!/usr/bin/env python3
"""
OpenClaw Agent Status Uploader
定时将 Agent 在线状态上传到监控平台
"""

import os
import sys
import json
import time
import signal
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path

# 配置
HOME = Path.home()
CREDENTIALS_FILE = HOME / ".openclaw/credentials/openclaw-status-monitor.json"
AGENTS_DIR = HOME / ".openclaw/agents"
OPENCLAW_JSON = HOME / ".openclaw/openclaw.json"
LOG_DIR = HOME / ".openclaw/logs"
PID_FILE = LOG_DIR / "status_uploader.pid"
LOG_FILE = LOG_DIR / "status_uploader.log"
ERROR_LOG_FILE = LOG_DIR / "status_uploader_error.log"
DEFAULT_SYNC_INTERVAL = 300  # 5分钟
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB 日志轮转阈值

# 确保日志目录存在
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_token():
    """加载 Token"""
    if os.environ.get("MONITOR_PLATFORM_TOKEN"):
        return os.environ["MONITOR_PLATFORM_TOKEN"]

    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE) as f:
            data = json.load(f)
            return data.get("agentToken")

    return None


def get_monitor_url():
    """获取监控平台 URL"""
    if os.environ.get("OPENCLAW_MONITOR_URL"):
        return os.environ["OPENCLAW_MONITOR_URL"]

    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE) as f:
            data = json.load(f)
            return data.get("monitorUrl", "https://openclaw-agent-monitor.vercel.app")

    return "https://openclaw-agent-monitor.vercel.app"


def load_sync_interval():
    """从配置文件加载同步间隔（秒）"""
    if CREDENTIALS_FILE.exists():
        try:
            with open(CREDENTIALS_FILE) as f:
                data = json.load(f)
                interval_minutes = data.get("syncIntervalMinutes")
                if interval_minutes:
                    return interval_minutes * 60
        except Exception:
            pass
    return DEFAULT_SYNC_INTERVAL


def save_sync_interval(minutes):
    """保存同步间隔到配置文件"""
    try:
        data = {}
        if CREDENTIALS_FILE.exists():
            with open(CREDENTIALS_FILE) as f:
                data = json.load(f)
        data["syncIntervalMinutes"] = minutes
        CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"已保存同步间隔: {minutes} 分钟")
        return True
    except Exception as e:
        logger.error(f"保存同步间隔失败: {e}")
        return False


def get_agent_ids():
    """从 openclaw.json 获取 agent ID 列表"""
    if not OPENCLAW_JSON.exists():
        return []

    try:
        with open(OPENCLAW_JSON) as f:
            data = json.load(f)
            return [a["id"] for a in data.get("agents", {}).get("list", [])]
    except Exception as e:
        logger.error(f"读取 openclaw.json 失败: {e}")
        return []


def get_all_agents():
    """获取所有 agent ID 列表"""
    return get_agent_ids()


def upload_status(agent_ids):
    """上传状态到监控平台"""
    import urllib.request
    import urllib.error

    token = load_token()
    if not token:
        logger.error("未找到 Token")
        return False

    url = f"{get_monitor_url()}/api/upload"

    # 转换为 API 期望的格式 [{id: "agentId"}, ...]
    agents = [{"id": aid} for aid in agent_ids]

    try:
        data = json.dumps(agents).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-agent-token": token
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                logger.info(f"上传成功: {agent_ids}")
                return True
            else:
                logger.error(f"上传失败: HTTP {response.status}")
                return False

    except urllib.error.HTTPError as e:
        logger.error(f"HTTP 错误: {e.code} - {e.reason}")
        with open(ERROR_LOG_FILE, "a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} - HTTP {e.code}: {e.reason}\n")
        return False
    except urllib.error.URLError as e:
        logger.error(f"网络错误: {e.reason}")
        with open(ERROR_LOG_FILE, "a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} - Network: {e.reason}\n")
        return False
    except Exception as e:
        logger.error(f"上传异常: {e}")
        with open(ERROR_LOG_FILE, "a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} - Exception: {e}\n")
        return False


def save_pid():
    """保存 PID"""
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))


def is_running():
    """检查进程是否在运行"""
    if not PID_FILE.exists():
        return False

    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())

        # 检查进程是否存在
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError, PermissionError):
        # 进程不存在或无权限
        PID_FILE.unlink(missing_ok=True)
        return False


def cleanup():
    """清理 PID 文件"""
    PID_FILE.unlink(missing_ok=True)


def rotate_logs_if_needed():
    """检查并轮转日志文件（超过 MAX_LOG_SIZE 时）"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for log_file in [LOG_FILE, ERROR_LOG_FILE]:
        if log_file.exists() and log_file.stat().st_size > MAX_LOG_SIZE:
            rotated = log_file.with_suffix(f".{timestamp}.log")
            log_file.rename(rotated)
            logger.info(f"日志已轮转: {rotated.name}")


def daemon_mode(interval_seconds=None, fork=False):
    """守护进程模式

    Args:
        interval_seconds: 上传间隔（秒）
        fork: 是否 fork 到后台（用于外部启动守护进程）
    """
    # 如果需要 fork
    if fork:
        try:
            pid = os.fork()
            if pid > 0:
                # 父进程退出
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(f"Fork 失败: {e}\n")
            sys.exit(1)

        # 子进程：创建新会话
        os.setsid()
        # 再次 fork 防止再次获取控制终端
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
        # 重定向标准文件描述符
        sys.stdout.flush()
        sys.stderr.flush()
        with open('/dev/null', 'r') as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open(LOG_FILE, 'a') as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
            os.dup2(f.fileno(), sys.stderr.fileno())

    # 首次检查
    token = load_token()
    if not token:
        logger.error("未配置 Token，请先运行 'openclaw skills enable status-monitor' 配置")
        sys.exit(1)

    # 如果没有指定间隔，从配置文件加载
    if interval_seconds is None:
        interval_seconds = load_sync_interval()

    # 保存 PID
    save_pid()
    logger.info(f"状态上传服务启动，PID: {os.getpid()}")
    logger.info(f"上传间隔: {interval_seconds} 秒 ({interval_seconds // 60} 分钟)")

    # 设置信号处理
    def signal_handler(signum, frame):
        logger.info("收到停止信号，正在退出...")
        cleanup()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    last_upload_success = True
    recovery_check_interval = 30  # 网络恢复检测间隔（秒）

    while True:
        try:
            # 检查并轮转日志
            rotate_logs_if_needed()

            agents = get_all_agents()
            if agents:
                success = upload_status(agents)
                last_upload_success = success
            else:
                logger.info("无 Agent，跳过本次上传")
        except Exception as e:
            logger.error(f"执行异常: {e}")
            with open(ERROR_LOG_FILE, "a") as f:
                f.write(f"{datetime.now(timezone.utc).isoformat()} - Loop Exception: {e}\n")
            last_upload_success = False

        # 根据上次上传状态决定等待时间
        if last_upload_success:
            time.sleep(interval_seconds)
        else:
            # 上次失败，等待较短时间后重试（网络恢复检测）
            time.sleep(recovery_check_interval)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        # start 命令支持 --interval 参数
        if cmd == "start":
            interval_seconds = None
            fork_mode = False
            # 解析 --interval 或 -i 参数
            i = 2
            while i < len(sys.argv):
                if sys.argv[i] == "--interval" and i + 1 < len(sys.argv):
                    interval_seconds = int(sys.argv[i + 1]) * 60
                    i += 2
                elif sys.argv[i] == "-i" and i + 1 < len(sys.argv):
                    interval_seconds = int(sys.argv[i + 1]) * 60
                    i += 2
                elif sys.argv[i] == "--fork":
                    fork_mode = True
                    i += 1
                else:
                    i += 1

            # 如果指定了间隔，保存到配置
            if interval_seconds is not None:
                save_sync_interval(interval_seconds // 60)

            if is_running():
                print("服务已在运行中，如需新间隔请先停止再启动")
                sys.exit(0)
            daemon_mode(interval_seconds, fork=fork_mode)

        elif cmd == "stop":
            if PID_FILE.exists():
                with open(PID_FILE) as f:
                    pid = int(f.read().strip())
                try:
                    os.kill(pid, signal.SIGTERM)
                    print(f"已发送停止信号到 PID {pid}")
                except ProcessLookupError:
                    print("进程不存在")
                    cleanup()
            else:
                print("服务未运行")

        elif cmd == "status":
            if is_running():
                with open(PID_FILE) as f:
                    pid = f.read().strip()
                current_interval = load_sync_interval()
                print(f"服务正在运行，PID: {pid}")
                print(f"上传间隔: {current_interval} 秒 ({current_interval // 60} 分钟)")
            else:
                print("服务未运行")

        elif cmd == "set-interval":
            if len(sys.argv) > 2:
                minutes = int(sys.argv[2])
                interval_seconds = minutes * 60
                save_sync_interval(minutes)
                print(f"已设置同步间隔: {minutes} 分钟")
                if is_running():
                    print("请重启服务使设置生效: stop && start")
            else:
                print("用法: status_uploader.py set-interval <分钟>")

        elif cmd == "test":
            agents = get_all_agents()
            print(f"所有 Agent: {agents}")
            if agents:
                upload_status(agents)

        else:
            print(f"未知命令: {cmd}")
            print("用法: status_uploader.py [start|stop|status|set-interval|test]")
            print("      start [--interval|-i <分钟>]")
    else:
        # 单次执行
        agents = get_all_agents()
        if agents:
            upload_status(agents)
        else:
            print("无 Agent")
