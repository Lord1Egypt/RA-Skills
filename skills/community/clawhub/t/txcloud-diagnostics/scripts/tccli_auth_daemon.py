#!/usr/bin/env python3
"""
tccli auth 守护进程: 启动 tccli 获取授权链接 → 轮询等待验证码文件 → 同进程内提交验证码。

使用方式（建议加 -u 禁用 Python 输出缓冲）:
    nohup python3 -u scripts/tccli_auth_daemon.py > /tmp/tccli_daemon.log 2>&1 &

工作原理:
    1. 通过 pty 伪终端启动 `tccli auth login --browser no`（交互式命令）
    2. 从输出中提取授权链接 → 保存到 /tmp/tccli_auth_link.txt
    3. 轮询等待 /tmp/tccli_auth_input_code.txt（最多 10 分钟）
    4. 检测到验证码后通过 pty fd 传入同一 tccli 进程完成授权
    5. 用 DescribeRegions 验证凭证是否生效

关键约束:
    - tccli auth login 每次启动生成唯一 state，验证码中的 state 必须匹配
    - 因此必须在同一个 pty 进程内完成链接获取和验证码提交（不能分两次命令执行）
"""
import os, sys, time, select, pty, subprocess

CODE_FILE = "/tmp/tccli_auth_input_code.txt"
LINK_FILE = "/tmp/tccli_auth_link.txt"
LOG_FILE = "/tmp/tccli_daemon.log"
POLL_TIMEOUT = 600  # 轮询等待验证码的最大秒数（10 分钟）
STARTUP_READ_TIMEOUT = 15  # 等待 tccli 输出授权链接的秒数


def log(msg):
    """打印日志并立即 flush，确保 nohup 后台运行时日志及时写入文件。"""
    print(msg)
    sys.stdout.flush()


def cleanup():
    """清理上次运行的残留文件。"""
    for f in [CODE_FILE, LINK_FILE]:
        if os.path.exists(f):
            os.remove(f)


def start_tccli():
    """通过 pty 伪终端启动 tccli auth login，返回 (master_fd, process)。"""
    master, slave = pty.openpty()
    proc = subprocess.Popen(
        ["tccli", "auth", "login", "--browser", "no"],
        stdin=slave, stdout=slave, stderr=slave
    )
    os.close(slave)
    return master, proc


def read_tccli_output(master, timeout=STARTUP_READ_TIMEOUT):
    """读取 tccli 输出，直到出现"验证码"关键词或超时。返回解码后的输出字符串。"""
    output = b""
    start = time.time()
    while time.time() - start < timeout:
        r, _, _ = select.select([master], [], [], 1)
        if r:
            try:
                chunk = os.read(master, 4096)
                if not chunk:
                    break
                output += chunk
                if "验证码".encode("utf-8") in output or b"code" in output.lower():
                    break
            except OSError:
                break
    return output.decode("utf-8", errors="replace")


def extract_and_save_link(output):
    """从 tccli 输出中提取授权链接并保存到文件。返回链接字符串或 None。"""
    for line in output.split("\n"):
        line = line.strip()
        if line.startswith("https://"):
            with open(LINK_FILE, "w") as f:
                f.write(line)
            log(f"LINK_SAVED:{line}")
            return line
    log("WARNING: 未能从 tccli 输出中提取到授权链接")
    return None


def wait_for_code():
    """轮询等待验证码文件，返回验证码字符串或 None（超时）。"""
    log("WAITING_FOR_CODE")
    for i in range(POLL_TIMEOUT):
        if os.path.exists(CODE_FILE):
            with open(CODE_FILE) as cf:
                code = cf.read().strip()
            if code:
                log(f"CODE_RECEIVED (len={len(code)})")
                return code
        time.sleep(1)
    log("TIMEOUT: 等待验证码超时（10 分钟）")
    return None


def submit_code(master, code):
    """通过 pty fd 将验证码传入 tccli 进程，返回 tccli 的响应输出。"""
    os.write(master, (code + "\n").encode())
    time.sleep(5)  # 等待 tccli 处理验证码

    result = b""
    while True:
        r, _, _ = select.select([master], [], [], 3)
        if r:
            try:
                chunk = os.read(master, 4096)
                if not chunk:
                    break
                result += chunk
            except OSError:
                break
        else:
            break
    return result.decode("utf-8", errors="replace")


def verify_credentials():
    """验证 tccli 凭证是否已生效。返回 True/False。"""
    try:
        v = subprocess.run(
            ["tccli", "cvm", "DescribeRegions", "--output", "json"],
            capture_output=True, text=True, timeout=15
        )
        return v.returncode == 0
    except Exception as e:
        log(f"VERIFY_ERROR: {e}")
        return False


def main():
    log(f"=== tccli auth daemon started at {time.strftime('%Y-%m-%d %H:%M:%S')} ===")

    # Step 1: 清理残留
    cleanup()

    # Step 2: 启动 tccli
    log("Starting tccli auth login --browser no ...")
    master, proc = start_tccli()

    try:
        # Step 3: 读取输出并提取链接
        output = read_tccli_output(master)
        log(output)
        link = extract_and_save_link(output)
        if not link:
            log("FAILED: 无法提取授权链接，退出")
            return

        # Step 4: 等待验证码
        code = wait_for_code()
        if not code:
            return

        # Step 5: 提交验证码
        result = submit_code(master, code)
        log(f"RESULT:{result}")

        # 清理验证码文件
        if os.path.exists(CODE_FILE):
            os.remove(CODE_FILE)

        # Step 6: 验证凭证
        if verify_credentials():
            log("AUTH_SUCCESS")
        else:
            log("AUTH_FAILED: 凭证验证未通过，请检查验证码是否正确或是否已过期")

    finally:
        try:
            os.close(master)
        except OSError:
            pass
        proc.wait()
        log(f"=== tccli auth daemon finished at {time.strftime('%Y-%m-%d %H:%M:%S')} ===")


if __name__ == "__main__":
    main()
