#!/usr/bin/env python3
"""Generate Quark QR login and send PNG to Telegram via OpenClaw message tool.

This script is intended to be invoked by the main agent when JJ requests login in Telegram.
It does NOT contain bot tokens; OpenClaw routes sending.

Usage:
  ./quark_login_send_qr.py --chat <channel:chat_id>

Outputs:
  - writes qr_code.png under skills/quark-netdisk/references/
  - prints qr_url to stdout
"""

from __future__ import annotations

import argparse
from pathlib import Path

from quark_api import QuarkSession, save_png_qr


ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chat", required=True)
    args = ap.parse_args()

    qr_png = REF / "qr_code.png"

    with QuarkSession(timeout_s=60) as s:
        token = s.get_qr_token()
        qr_url = s.build_qr_url(token)
        save_png_qr(qr_url, qr_png)

    print(qr_url)
    print(qr_png)
    print(args.chat)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
