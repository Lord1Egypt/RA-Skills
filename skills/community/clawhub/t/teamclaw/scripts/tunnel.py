#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare Tunnel 公网部署脚本
- 自动检测平台（Linux/macOS + amd64/arm64）
- 提示用户手动安装 cloudflared
- 启动两条隧道：前端 Web UI + Bark 推送服务
- 打印各自的公网地址
"""

import os
import sys
import re
import signal
import platform
import subprocess
import shutil
import threading
from dotenv import load_dotenv

# ── 项目路径 ──────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)

BIN_DIR = os.path.join(PROJECT_ROOT, "bin")
os.makedirs(BIN_DIR, exist_ok=True)

CLOUDFLARED_PATH = os.path.join(BIN_DIR, "cloudflared")
ENV_PATH = os.path.join(PROJECT_ROOT, "config", ".env")

# ── 加载配置 ──────────────────────────────────────────────
load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, "config", ".env"))
PORT_FRONTEND = os.getenv("PORT_FRONTEND", "51209")
PORT_BARK = os.getenv("PORT_BARK", "58010")

# ── 全局进程引用 ──────────────────────────────────────────
tunnel_procs = []
tunnel_urls = {}  # {"frontend": "https://...", "bark": "https://..."}
urls_lock = threading.Lock()
all_tunnels_ready = threading.Event()
expected_tunnels = 2


def detect_platform():
    """检测当前平台，返回 (os_name, arch)"""
    os_name = platform.system().lower()   # linux / darwin
    machine = platform.machine().lower()  # x86_64 / aarch64 / arm64

    if os_name not in ("linux", "darwin"):
        print(f"❌ 不支持的操作系统: {os_name}")
        sys.exit(1)

    if machine in ("x86_64", "amd64"):
        arch = "amd64"
    elif machine in ("aarch64", "arm64"):
        arch = "arm64"
    else:
        print(f"❌ 不支持的架构: {machine}")
        sys.exit(1)

    return os_name, arch


def download_url(os_name, arch):
    """根据平台返回 cloudflared 下载 URL（仅提供链接，不自动下载）"""
    if os_name == "linux":
        return f"https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-{arch}"
    elif os_name == "darwin":
        # macOS 只提供 amd64 版本（arm64 通过 Rosetta 2 兼容）
        return "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz"


def get_cloudflared_install_guide(os_name, arch):
    """返回 cloudflared 手动安装指南"""
    url = download_url(os_name, arch)
    
    if os_name == "linux":
        return f"""
📥 手动安装 cloudflared (Linux {arch}):

1. 下载二进制文件:
   wget {url} -O cloudflared

2. 添加执行权限:
   chmod +x cloudflared

3. 移动到系统路径或项目 bin/ 目录:
   sudo mv cloudflared /usr/local/bin/  # 系统路径
   或
   mv cloudflared {BIN_DIR}/           # 项目路径
"""
    elif os_name == "darwin":
        return f"""
📥 手动安装 cloudflared (macOS):

1. 下载压缩包:
   curl -L {url} -o cloudflared.tgz

2. 解压:
   tar -xzf cloudflared.tgz

3. 移动到系统路径或项目 bin/ 目录:
   sudo mv cloudflared /usr/local/bin/  # 系统路径
   或
   mv cloudflared {BIN_DIR}/           # 项目路径

4. 清理压缩包:
   rm cloudflared.tgz
"""


def ensure_cloudflared():
    """确保 cloudflared 可用，找不到时提示用户手动安装"""
    # 优先检查 bin/ 目录
    if os.path.isfile(CLOUDFLARED_PATH) and os.access(CLOUDFLARED_PATH, os.X_OK):
        print(f"✅ 已找到 cloudflared: {CLOUDFLARED_PATH}")
        return CLOUDFLARED_PATH

    # 检查系统 PATH
    system_cf = shutil.which("cloudflared")
    if system_cf:
        print(f"✅ 已找到系统 cloudflared: {system_cf}")
        return system_cf

    # 都没有，提示用户手动安装
    os_name, arch = detect_platform()
    
    print("❌ 未找到 cloudflared")
    print("=" * 60)
    print(get_cloudflared_install_guide(os_name, arch))
    print("=" * 60)
    print("\n💡 安装完成后，请重新运行此脚本")
    sys.exit(1)


def cleanup(signum=None, frame=None):
    """清理所有隧道进程"""
    for proc in tunnel_procs:
        if proc and proc.poll() is None:
            print(f"🛑 正在关闭隧道进程 (PID: {proc.pid})...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    if tunnel_procs:
        print("✅ 所有隧道已关闭")
    if signum is not None:
        sys.exit(0)


def write_env_key(key: str, value: str):
    """Write or update a single key in config/.env"""
    env_file = ENV_PATH

    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []

    key_found = False
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f"{key}=") or stripped.startswith(f"# {key}="):
            new_lines.append(f"{key}={value}\n")
            key_found = True
        else:
            new_lines.append(line)

    if not key_found:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f"{key}={value}\n")

    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def write_domains_to_env():
    """Write all captured tunnel URLs to config/.env"""
    with urls_lock:
        if "frontend" in tunnel_urls:
            write_env_key("PUBLIC_DOMAIN", tunnel_urls["frontend"])
        if "bark" in tunnel_urls:
            write_env_key("BARK_PUBLIC_URL", tunnel_urls["bark"])
    print(f"📝 已将公网域名写入 {ENV_PATH}")


def run_tunnel(cf_bin: str, name: str, local_port: str, env_key: str):
    """
    Start a single cloudflared tunnel in a thread.
    Captures the public URL and stores it in tunnel_urls.
    """
    print(f"🌐 [{name}] 正在启动隧道 (转发 → 127.0.0.1:{local_port})...")

    proc = subprocess.Popen(
        [cf_bin, "tunnel", "--url", f"http://127.0.0.1:{local_port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    tunnel_procs.append(proc)

    url_pattern = re.compile(r"(https://[a-zA-Z0-9-]+\.trycloudflare\.com)")
    public_url = None

    try:
        for line in proc.stdout:
            line = line.strip()
            if not public_url:
                match = url_pattern.search(line)
                if match:
                    public_url = match.group(1)
                    with urls_lock:
                        tunnel_urls[name] = public_url

                    print(f"  ✅ [{name}] 公网地址: {public_url}")

                    # Check if all tunnels are ready
                    with urls_lock:
                        if len(tunnel_urls) >= expected_tunnels:
                            all_tunnels_ready.set()

        # stdout closed => process exited
        proc.wait()
    except Exception as e:
        print(f"  ❌ [{name}] 隧道异常: {e}")


def start_tunnels():
    """启动所有 Cloudflare Tunnel 并等待公网地址就绪"""
    cf_bin = ensure_cloudflared()

    # 注册信号处理
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Define tunnels: (name, local_port, env_key)
    tunnel_configs = [
        ("frontend", PORT_FRONTEND, "PUBLIC_DOMAIN"),
        ("bark", PORT_BARK, "BARK_PUBLIC_URL"),
    ]

    # Start each tunnel in a background thread
    threads = []
    for name, port, env_key in tunnel_configs:
        t = threading.Thread(target=run_tunnel, args=(cf_bin, name, port, env_key), daemon=True)
        t.start()
        threads.append(t)

    # Wait for all tunnels to report their URLs (timeout 60s)
    print("\n⏳ 等待所有隧道就绪...")
    ready = all_tunnels_ready.wait(timeout=60)

    if ready:
        # Write all URLs to .env
        write_domains_to_env()

        print()
        print("============================================")
        print("  🎉 公网部署成功！")
        with urls_lock:
            if "frontend" in tunnel_urls:
                print(f"  🌍 前端地址: {tunnel_urls['frontend']}")
            if "bark" in tunnel_urls:
                print(f"  📱 Bark 推送地址: {tunnel_urls['bark']}")
                print(f"     (请在 Bark App 中设置此地址作为 Server URL)")
        print("  按 Ctrl+C 关闭所有隧道")
        print("============================================")
        print()
    else:
        print("⚠️  部分隧道未能在 60 秒内就绪")
        with urls_lock:
            if tunnel_urls:
                write_domains_to_env()
                for name, url in tunnel_urls.items():
                    print(f"  ✅ [{name}] {url}")
            else:
                print("❌ 所有隧道均启动失败")
                cleanup()
                sys.exit(1)

    # Keep main thread alive, waiting for tunnel threads
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()


if __name__ == "__main__":
    start_tunnels()
