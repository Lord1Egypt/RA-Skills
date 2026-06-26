#!/usr/bin/env python3
"""
RoadShow Capture — 统一入口

自动检测 URL 域名，路由到对应平台的捕获脚本：
  - netroadshow.com → NetRoadShow 流程
  - dealroadshow.com → DealRoadShow 流程

用法:
  python roadshow-capture.py --url "https://www.netroadshow.com/nrs/home/#!/?show=SHOW_ID"
  python roadshow-capture.py --url "https://dealroadshow.com/e/MTNA2026"
  python roadshow-capture.py --url "..." --email "your@email.com" --output /path/to/out
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="RoadShow Capture — 统一入口")
    p.add_argument("--url", required=True, help="路演 URL（自动识别平台）")
    p.add_argument("--email", default=None, help="邮箱（默认 NRS_EMAIL 环境变量）")
    p.add_argument("--output", "-o", default=None, help="输出目录（默认自动生成）")
    p.add_argument("--wait", type=float, default=None, help="翻页后等待秒数")
    p.add_argument("--max-pages", type=int, default=None, help="最大页数限制")
    p.add_argument("--list", action="store_true", help="列出支持的平台")
    return p.parse_args()


def get_script_dir():
    return Path(__file__).parent


def main():
    args = parse_args()

    if args.list:
        print("支持的平台：")
        print("  netroadshow.com  — NetRoadShow 路演")
        print("  dealroadshow.com — DealRoadShow 路演")
        return

    url = args.url.lower()

    if "netroadshow.com" in url:
        script = get_script_dir() / "netroadshow-capture.py"
    elif "dealroadshow.com" in url or "dealroadshow.finsight.com" in url:
        script = get_script_dir() / "dealroadshow-capture.py"
    else:
        print(f"❌ 无法识别的路演平台：{args.url}")
        print("支持的平台：netroadshow.com, dealroadshow.com")
        sys.exit(1)

    if not script.exists():
        print(f"❌ 脚本不存在：{script}")
        sys.exit(1)

    # Build command
    cmd = [sys.executable, str(script), "--url", args.url]

    if args.email:
        cmd += ["--email", args.email]
    if args.output:
        cmd += ["--output", args.output]
    if args.wait is not None:
        cmd += ["--wait", str(args.wait)]
    if args.max_pages is not None:
        cmd += ["--max-pages", str(args.max_pages)]

    print(f"→ 检测到平台: {'NetRoadShow' if 'netroadshow' in url else 'DealRoadShow'}")
    print(f"→ 调用: {' '.join(str(c) for c in cmd)}")
    print()

    # Run
    env = os.environ.copy()
    proc = subprocess.run(cmd, env=env)
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
