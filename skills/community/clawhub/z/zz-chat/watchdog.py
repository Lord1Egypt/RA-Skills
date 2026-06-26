#!/usr/bin/env python3
"""爪爪看门狗 — launchd 管 watchdog，watchdog 管 bridge"""
import subprocess, time, os, signal, sys

BRIDGE_SCRIPT = os.path.expanduser("~/.openclaw/workspace/openchat/bridge/bridge.py")
BRIDGE_LOG = os.path.expanduser("~/.openclaw/workspace/openchat/bridge/bridge.log")
CHECK_INTERVAL = 10  # 每10秒检查一次
STALE_TIMEOUT = 90   # 90秒没心跳就重启（bridge每30秒写心跳）

process = None
last_log_time = 0

def get_last_log_time():
    """读取 bridge.log 最后一行的时间戳"""
    try:
        with open(BRIDGE_LOG, "r") as f:
            lines = f.readlines()
            if lines:
                return os.path.getmtime(BRIDGE_LOG)
    except:
        pass
    return 0

def start_bridge():
    global process, last_log_time
    log = open(BRIDGE_LOG, "a")
    process = subprocess.Popen(
        [sys.executable, "-u", BRIDGE_SCRIPT],
        stdout=log,
        stderr=log,
        cwd=os.path.dirname(BRIDGE_SCRIPT)
    )
    last_log_time = time.time()
    print(f"[看门狗] bridge 启动 (PID={process.pid})", flush=True)

def stop_bridge():
    global process
    if process and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except:
            process.kill()
        print("[看门狗] bridge 已停止", flush=True)
    process = None

def is_process_alive():
    return process is not None and process.poll() is None

def is_connection_stale():
    """检查 bridge 是否长时间没活动（进程在但连接断了）"""
    if not is_process_alive():
        return False
    mtime = get_last_log_time()
    if mtime == 0:
        return False
    idle = time.time() - mtime
    return idle > STALE_TIMEOUT

def cleanup(sig, frame):
    print("[看门狗] 收到停止信号", flush=True)
    stop_bridge()
    sys.exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

print("[看门狗] 启动", flush=True)
start_bridge()

while True:
    time.sleep(CHECK_INTERVAL)

    # 进程挂了 → 重启
    if not is_process_alive():
        print(f"[看门狗] bridge 进程已停止，重启中...", flush=True)
        stop_bridge()
        time.sleep(2)
        start_bridge()
        continue

    # 进程在但连接断了（60秒没日志）→ 重启
    if is_connection_stale():
        print(f"[看门狗] bridge 连接疑似断开（{STALE_TIMEOUT}秒无活动），重启中...", flush=True)
        stop_bridge()
        time.sleep(2)
        start_bridge()
        continue
