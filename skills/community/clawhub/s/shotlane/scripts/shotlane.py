#!/usr/bin/env python3
"""Minimal Shotlane CLI (no dependencies). Usage: shotlane.py {screenshot,read,pdf} ... (needs SHOTLANE_API_KEY)."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = os.environ.get("SHOTLANE_BASE_URL", "https://shotlane.dev")


def call(path: str, payload: dict) -> bytes:
    key = os.environ.get("SHOTLANE_API_KEY")
    if not key:
        sys.exit(f"Set SHOTLANE_API_KEY (get a free key at {BASE})")
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode(),
        headers={"X-API-Key": key, "Content-Type": "application/json", "User-Agent": "shotlane-cli/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read())["error"]
        except Exception:
            msg = str(e)
        sys.exit(f"Shotlane error {e.code}: {msg}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("screenshot")
    s.add_argument("url")
    s.add_argument("--out", default="screenshot.png")
    s.add_argument("--full-page", action="store_true")
    s.add_argument("--device")
    s.add_argument("--selector")
    s.add_argument("--delay", type=int, default=0)
    s.add_argument("--dark", action="store_true")
    s.add_argument("--clean", action="store_true", help="hide cookie banners and ads")
    r = sub.add_parser("read")
    r.add_argument("url")
    r.add_argument("--whole-page", action="store_true")
    r.add_argument("--selector")
    d = sub.add_parser("pdf")
    d.add_argument("--url")
    d.add_argument("--html", help="path to an HTML file")
    d.add_argument("--out", default="out.pdf")
    d.add_argument("--paper", default="A4")
    d.add_argument("--landscape", action="store_true")
    a = p.parse_args()

    if a.cmd == "screenshot":
        fmt = (
            "jpeg"
            if a.out.lower().endswith((".jpg", ".jpeg"))
            else "webp"
            if a.out.lower().endswith(".webp")
            else "png"
        )
        body = {
            "url": a.url,
            "format": fmt,
            "full_page": a.full_page,
            "dark_mode": a.dark,
            "delay": a.delay,
            "hide_cookie_banners": a.clean,
            "block_ads": a.clean,
        }
        body.update({k: v for k, v in (("device", a.device), ("selector", a.selector)) if v})
        Path(a.out).write_bytes(call("/v1/screenshot", body))
        print(f"saved {a.out}")
    elif a.cmd == "read":
        body = {"url": a.url, "main_content": not a.whole_page, "format": "markdown"}
        if a.selector:
            body["selector"] = a.selector
        sys.stdout.write(call("/v1/markdown", body).decode())
    else:
        if not (a.url or a.html):
            sys.exit("pdf needs --url or --html")
        body = {"paper": a.paper, "landscape": a.landscape}
        body.update({"url": a.url} if a.url else {"html": Path(a.html).read_text(encoding="utf-8")})
        Path(a.out).write_bytes(call("/v1/pdf", body))
        print(f"saved {a.out}")


if __name__ == "__main__":
    main()
