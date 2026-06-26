"""Cloudflare Pages 部署"""

import os, time, subprocess
from pathlib import Path

from lib.config import (
    CLOUDFLARE_API_TOKEN, REPORT_CF_PROJECT, SITE_URL,
    check_config, DIST_DIR
)

MAX_RETRIES = 2  # Total attempts = 1 + MAX_RETRIES


def deploy_to_cf(dist_dir=None, message=None):
    """将 dist/ 目录部署到 Cloudflare Pages。

    Args:
        dist_dir: 部署源目录，默认 DIST_DIR
        message: 部署 commit message
    """
    check_config()

    deploy_dir = dist_dir or DIST_DIR
    if not deploy_dir.exists():
        print(f"❌ 部署目录不存在: {deploy_dir}")
        return False

    token = CLOUDFLARE_API_TOKEN
    project = REPORT_CF_PROJECT

    env = {**os.environ, "CLOUDFLARE_API_TOKEN": token}
    cmd = [
        "npx", "wrangler", "pages", "deploy", str(deploy_dir),
        "--project-name", project,
        "--commit-dirty=true",
        "--branch", "main",
    ]
    if message:
        cmd.extend(["--commit-message", message])

    print(f"🚀 部署到 Cloudflare Pages...")
    print(f"   项目: {project}")
    print(f"   目录: {deploy_dir}")

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
        except subprocess.TimeoutExpired:
            print(f"❌ 部署超时（120秒），尝试 {attempt}/{MAX_RETRIES+1}")
            if attempt <= MAX_RETRIES:
                time.sleep(5)
                continue
            return False
        except FileNotFoundError:
            print("❌ 找不到 npx 命令，请确保 Node.js 已安装")
            return False

        print(result.stdout)
        if result.returncode != 0:
            # Sanitize stderr to prevent token leakage
            sanitized_stderr = result.stderr.replace(token, "***")
            print(sanitized_stderr)
            print(f"❌ 部署失败，尝试 {attempt}/{MAX_RETRIES+1}")
            if attempt <= MAX_RETRIES:
                time.sleep(5)
                continue
            return False

        print(f"✅ 部署成功 → {SITE_URL}")
        return True

    return False