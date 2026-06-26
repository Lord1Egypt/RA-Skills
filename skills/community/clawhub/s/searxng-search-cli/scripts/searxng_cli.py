#!/usr/bin/env python3
"""
SearXNG CLI for OpenClaw
Usage: searxng-search <command> [options]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

# 配置
SEARXNG_DIR = Path.home() / "projects" / "searxng"
SEARXNG_PORT = os.environ.get("SEARXNG_PORT", "8888")
SEARXNG_HOST = os.environ.get("SEARXNG_HOST", "127.0.0.1")
SEARXNG_SECRET = os.environ.get("SEARXNG_SECRET", "")

# Bot detection bypass: 127.0.0.1 is in trusted_proxies by default
FORWARDED_FOR = {"X-Forwarded-For": "127.0.0.1"}


def log(msg):
    print(f"[searxng] {msg}", file=sys.stderr)


def run(cmd, check=True, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        log(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def is_installed():
    return SEARXNG_DIR.exists() and (SEARXNG_DIR / ".venv").exists()


def is_running():
    # Try multiple times with short timeout (service may be slow to respond)
    for _ in range(3):
        try:
            req = urllib.request.Request(
                f"http://{SEARXNG_HOST}:{SEARXNG_PORT}",
                headers=FORWARDED_FOR
            )
            resp = urllib.request.urlopen(req, timeout=3)
            return resp.status == 200
        except:
            import time
            time.sleep(1)
    return False


def _ensure_settings():
    """Ensure JSON format is enabled and limiter.toml is configured."""
    settings_file = SEARXNG_DIR / "searx" / "settings.yml"
    limiter_src = SEARXNG_DIR / "searx" / "limiter.toml"
    limiter_dst = Path("/etc/searxng/limiter.toml")

    # Enable JSON format
    if settings_file.exists():
        with open(settings_file) as f:
            content = f.read()
        # Check if json is in formats list
        if "formats:" in content:
            formats_section = content.split("formats:")[1].split("\n")[0:5]
            formats_text = "\n".join(formats_section)
            if "- json" not in formats_text:
                # Replace formats section
                import re
                content = re.sub(
                    r"formats:\n(\s+-\s+\w+\n)*",
                    "formats:\n    - html\n    - json\n    - csv\n    - rss\n",
                    content
                )
                with open(settings_file, "w") as f:
                    f.write(content)
                log("已启用 JSON API")

    # Copy limiter.toml if missing
    if not limiter_dst.exists() and limiter_src.exists():
        limiter_dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            import shutil
            shutil.copy(limiter_src, limiter_dst)
            log("已配置 limiter.toml")
        except PermissionError:
            log(f"⚠ 需要手动复制: sudo cp {limiter_src} {limiter_dst}")


def cmd_install(args):
    """一键安装 SearXNG"""
    log("开始安装 SearXNG...")

    # 1. 安装 uv
    if not subprocess.run("which uv", shell=True, capture_output=True).returncode == 0:
        log("安装 uv...")
        run('curl -LsSf https://astral.sh/uv/install.sh | sh')
        uv_path = Path.home() / ".local" / "bin" / "uv"
        if uv_path.exists():
            os.environ["PATH"] = f"{uv_path.parent}:{os.environ['PATH']}"

    # 2. 克隆 SearXNG
    if not SEARXNG_DIR.exists():
        log("克隆 SearXNG...")
        SEARXNG_DIR.parent.mkdir(parents=True, exist_ok=True)
        run(f"git clone --depth 1 https://github.com/searxng/searxng.git {SEARXNG_DIR}")

    # 3. 创建虚拟环境 + 安装依赖
    venv_dir = SEARXNG_DIR / ".venv"
    log("创建虚拟环境 + 安装依赖...")
    run(f"cd {SEARXNG_DIR} && uv venv .venv --clear")
    run(f"cd {SEARXNG_DIR} && uv pip install -r requirements.txt")

    # 4. 配置 settings.yml（启用 JSON）和 limiter.toml
    log("配置 SearXNG...")
    _ensure_settings()

    # 5. 生成 secret
    if not SEARXNG_SECRET:
        secret = subprocess.run(
            "python3 -c 'import secrets; print(secrets.token_hex(32))'",
            shell=True, capture_output=True, text=True
        ).stdout.strip()
        os.environ["SEARXNG_SECRET"] = secret
        log(f"生成的密钥: {secret[:16]}...")

    # 6. 启动服务
    cmd_start(args)

    log("安装完成！")


def cmd_start(args):
    """启动服务"""
    if is_running():
        log("服务已在运行")
        return

    log("启动服务...")
    env = os.environ.copy()
    env["SEARXNG_SECRET"] = SEARXNG_SECRET or env.get("SEARXNG_SECRET", "devsecret")

    cmd = (
        f'cd {SEARXNG_DIR} && '
        f'SEARXNG_SECRET={env["SEARXNG_SECRET"]} '
        f'{SEARXNG_DIR}/.venv/bin/python -m searx.webapp '
        f'--host {SEARXNG_HOST} --port {SEARXNG_PORT}'
    )
    subprocess.Popen(cmd, shell=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    import time
    for _ in range(15):
        time.sleep(1)
        if is_running():
            log(f"服务已启动: http://{SEARXNG_HOST}:{SEARXNG_PORT}")
            return

    log("启动失败，请检查日志")


def cmd_stop(args):
    """停止服务"""
    log("停止服务...")
    run("pkill -f 'searx.webapp'", check=False)
    log("服务已停止")


def cmd_restart(args):
    """重启服务"""
    cmd_stop(args)
    cmd_start(args)


def cmd_status(args):
    """查看状态"""
    if is_running():
        print(f"✓ 服务运行中: http://{SEARXNG_HOST}:{SEARXNG_PORT}")
    else:
        print("✗ 服务未运行")


def cmd_enable(args):
    """开机自启"""
    service_file = Path.home() / ".config" / "systemd" / "user" / "searxng.service"
    service_file.parent.mkdir(parents=True, exist_ok=True)

    secret = SEARXNG_SECRET or "devsecret"
    content = f"""[Unit]
Description=SearXNG Search Engine

[Service]
Type=simple
WorkingDirectory={SEARXNG_DIR}
ExecStart={SEARXNG_DIR}/.venv/bin/python -m searx.webapp --host {SEARXNG_HOST} --port {SEARXNG_PORT}
Environment=SEARXNG_SECRET={secret}
Restart=on-failure

[Install]
WantedBy=default.target
"""
    with open(service_file, "w") as f:
        f.write(content)

    run("systemctl --user daemon-reload", check=False)
    run("systemctl --user enable searxng", check=False)
    log("已启用开机自启")


def cmd_disable(args):
    """取消开机自启"""
    run("systemctl --user disable searxng", check=False)
    log("已取消开机自启")


def cmd_search(args):
    """搜索"""
    if not is_running():
        log("服务未运行，请先执行: searxng-search start")
        sys.exit(1)

    query = args.query
    params = {
        "q": query,
        "format": "json"
    }

    if args.engine:
        params["engines"] = args.engine
    if args.lang:
        params["lang"] = args.lang
    if args.page:
        params["pageno"] = args.page
    if args.time_range:
        params["time_range"] = args.time_range
    if args.safe_search:
        params["safesearch"] = args.safe_search

    from urllib.parse import urlencode
    url = f"http://{SEARXNG_HOST}:{SEARXNG_PORT}/search?{urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers=FORWARDED_FOR)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)

        results = data.get("results", [])
        if not results:
            print("未找到结果")
            return

        for r in results[:args.limit]:
            title = r.get("title", "")
            r_url = r.get("url", "")
            content = r.get("content", "")[:100]
            print(f"【{title}】")
            print(f"{r_url}")
            print(f"{content}...")
            print()
    except Exception as e:
        log(f"搜索失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="searxng-search")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    subparsers.add_parser("install", help="一键安装 SearXNG")
    subparsers.add_parser("start", help="启动服务")
    subparsers.add_parser("stop", help="停止服务")
    subparsers.add_parser("restart", help="重启服务")
    subparsers.add_parser("status", help="查看服务状态")
    subparsers.add_parser("enable", help="开机自启")
    subparsers.add_parser("disable", help="取消开机自启")

    search_parser = subparsers.add_parser("search", help="搜索")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("-e", "--engine", help="指定引擎")
    search_parser.add_argument("-l", "--lang", help="语言")
    search_parser.add_argument("-p", "--page", type=int, help="页码")
    search_parser.add_argument("-t", "--time-range", help="时间范围")
    search_parser.add_argument("-s", "--safe-search", help="安全搜索")
    search_parser.add_argument("--limit", type=int, default=5, help="结果数量")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    {
        "install": cmd_install,
        "start": cmd_start,
        "stop": cmd_stop,
        "restart": cmd_restart,
        "status": cmd_status,
        "enable": cmd_enable,
        "disable": cmd_disable,
        "search": cmd_search,
    }[args.command](args)


if __name__ == "__main__":
    main()
