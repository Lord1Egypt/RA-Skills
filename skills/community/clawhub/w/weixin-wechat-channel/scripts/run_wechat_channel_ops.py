#!/usr/bin/env python3
from __future__ import annotations

"""
微信公众号技能入口：先校验卡密，再执行后续自动化。

联网验证模式：连接授权服务器校验卡密有效性。
"""

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from license_gate import ensure_license, machine_fingerprint, LicenseError


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="WeChat public account skill — license check (日/月/年卡)"
    )
    p.add_argument(
        "--license-file",
        default="",
        help="授权文件路径（默认：<本技能根目录>/license/license.json）",
    )
    p.add_argument(
        "--card-key",
        default="",
        help="首次激活时传入卡密（无授权文件且未传此参数时会提示输入）",
    )
    p.add_argument(
        "--show-machine-id",
        action="store_true",
        help="仅打印本机指纹（用于排查换机等问题）后退出",
    )
    p.add_argument(
        "--license-status",
        action="store_true",
        help="查看当前授权状态",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    default_license = skill_root / "license" / "license.json"
    license_file = Path(args.license_file).resolve() if args.license_file else default_license

    if args.show_machine_id:
        print("Machine ID:", machine_fingerprint())
        return 0

    try:
        activation = ensure_license(license_file, key_from_cli=args.card_key)
        print(f"License OK — file: {license_file}")
        print(f"Plan: {activation.get('plan')}  expires_at: {activation.get('expires_at')}")
        return 0
    except LicenseError as exc:
        print(f"[ERROR] {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n[ABORT] 已取消")
        raise SystemExit(1)
