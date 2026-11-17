"""fetch_artifacts.py — 运行环境大件下载（腾讯云镜像优先，双轨 fallback）

轨道1: Playwright 浏览器（Chromium/headless-shell/ffmpeg/winldd）
  镜像链: 腾讯云 campus-env → npmmirror → 官方 cdn.playwright.dev
  通过 PLAYWRIGHT_DOWNLOAD_HOST 切换，Playwright 自带断点续传 + sha256 校验

轨道2: pip 依赖
  镜像链: 清华 tuna → 阿里 → 官方 PyPI
  通过 pip --index-url 切换

CLI:
  fetch_artifacts.py --browsers            → 下载全部浏览器组件
  fetch_artifacts.py --pip                 → 安装 pip 依赖（requirements 优先）
  fetch_artifacts.py --all                 → 两者都做
  fetch_artifacts.py --dry-run             → 只打印会用到的源，不下载

AI 指导: 每次尝试输出 {source, status, error?}，AI 据 JSON 自动换源，最多 3 次。
"""
import sys
import os
import json
import argparse
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common

# 轨道1: Playwright 镜像链（HOST 用 None 表示官方默认源）
PLAYWRIGHT_HOSTS = [
    {"name": "tencent-campus-env", "host": "https://tool.tom-thu.cn/campus-env"},
    {"name": "npmmirror", "host": "https://cdn.npmmirror.com/binaries/playwright"},
    {"name": "official", "host": None},
]

# 轨道2: pip 镜像链
PIP_INDEXES = [
    {"name": "tuna", "url": "https://pypi.tuna.tsinghua.edu.cn/simple"},
    {"name": "aliyun", "url": "https://mirrors.aliyun.com/pypi/simple/"},
    {"name": "official", "url": "https://pypi.org/simple"},
]

REQUIREMENTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requirements.txt")

BROWSERS = ["chromium", "ffmpeg"]  # chromium 会自动拉 headless-shell/winldd


def _run(cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return r


def download_browsers(dry_run=False):
    """轨道1：Playwright 浏览器，逐源尝试。"""
    results = []
    for src in PLAYWRIGHT_HOSTS:
        if dry_run:
            results.append({"source": src["name"], "action": "would use", "host": src["host"] or "official"})
            continue
        env = os.environ.copy()
        if src["host"]:
            env["PLAYWRIGHT_DOWNLOAD_HOST"] = src["host"]
        common.log(f"[fetch] 尝试浏览器源: {src['name']}")
        try:
            for b in BROWSERS:
                r = _run([sys.executable, "-m", "playwright", "install", b], env=env)
                if r.returncode != 0:
                    raise RuntimeError(r.stderr or r.stdout or "install failed")
            results.append({"source": src["name"], "status": "ok"})
            common.output_json({"status": "ok", "stage": "browsers", "source_used": src["name"], "results": results})
            return results
        except Exception as e:
            results.append({"source": src["name"], "status": "error", "error": str(e)[:200]})
            common.log(f"[fetch] 源 {src['name']} 失败: {e}")
    if dry_run:
        return results
    common.output_json({"status": "error", "stage": "browsers", "results": results})
    sys.exit(1)


def install_pip(dry_run=False):
    """轨道2：pip 依赖，逐源尝试。"""
    if not os.path.exists(REQUIREMENTS):
        # 无 requirements 时至少保证关键包
        req_arg = ["requests", "playwright"]
    else:
        req_arg = ["-r", REQUIREMENTS]
    results = []
    for src in PIP_INDEXES:
        if dry_run:
            results.append({"source": src["name"], "action": "would use", "url": src["url"]})
            continue
        common.log(f"[fetch] 尝试 pip 源: {src['name']}")
        cmd = [sys.executable, "-m", "pip", "install", "--index-url", src["url"]] + req_arg
        r = _run(cmd)
        if r.returncode == 0:
            results.append({"source": src["name"], "status": "ok"})
            common.output_json({"status": "ok", "stage": "pip", "source_used": src["name"], "results": results})
            return results
        results.append({"source": src["name"], "status": "error", "error": (r.stderr or r.stdout)[-200:]})
        common.log(f"[fetch] pip 源 {src['name']} 失败")
    if dry_run:
        return results
    common.output_json({"status": "error", "stage": "pip", "results": results})
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="运行环境大件下载（镜像优先 + fallback）")
    ap.add_argument("--browsers", action="store_true", help="下载 Playwright 浏览器组件")
    ap.add_argument("--pip", action="store_true", help="安装 pip 依赖")
    ap.add_argument("--all", action="store_true", help="两者都做")
    ap.add_argument("--dry-run", action="store_true", help="只列出会用到的源")
    args = ap.parse_args()

    if args.dry_run:
        r1 = download_browsers(dry_run=True)
        r2 = install_pip(dry_run=True)
        common.output_json({"status": "ok", "mode": "dry-run", "browsers": r1, "pip": r2})
        return
    if args.all or (not args.browsers and not args.pip):
        download_browsers()
        install_pip()
        return
    if args.browsers:
        download_browsers()
    if args.pip:
        install_pip()


if __name__ == "__main__":
    main()
