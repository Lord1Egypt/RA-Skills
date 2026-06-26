#!/usr/bin/env python3
"""
Fetch Weibo login QR code using OpenClaw browser tool.
Login cookies persist in the browser session after scanning.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

MEDIA_DIR = Path.home() / ".openclaw" / "media" / "browser"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Weibo login QR code (browser-session preserving)."
    )
    default_output = MEDIA_DIR / f"weibo-qr-{int(time.time())}.png"
    parser.add_argument(
        "-o",
        "--output",
        default=str(default_output),
        help=f"Output PNG path (default: {MEDIA_DIR}/weibo-qr-<timestamp>.png)",
    )
    parser.add_argument("--verbose", action="store_true", help="Print detailed logs")
    return parser.parse_args()


def log(verbose: bool, message: str) -> None:
    if verbose:
        print(f"[verbose] {message}")


def run_command(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(args, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def run_openclaw(
    oc_args: list[str], *, verbose: bool, retries: int = 3, retry_sleep_s: int = 2
) -> str:
    cmd = ["openclaw", *oc_args]
    last_output = ""

    for attempt in range(1, retries + 1):
        rc, out = run_command(cmd)
        last_output = out
        if rc == 0:
            return out

        if "gateway closed" in out.lower():
            log(verbose, f"Gateway closed on attempt {attempt}, waiting {retry_sleep_s}s …")
            time.sleep(retry_sleep_s)
            continue

        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n{out.strip() or '(no output)'}"
        )

    raise RuntimeError(
        f"Command failed after retries: {' '.join(cmd)}\n"
        f"{last_output.strip() or '(no output)'}"
    )


def extract_qr_url(raw: str) -> str:
    match = re.search(r"https://[^\s\"']*qr\.weibo\.cn/inf/gen[^\s\"']*", raw)
    return match.group(0) if match else ""


def ensure_png(path: Path) -> None:
    data = path.read_bytes()
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError("Downloaded file is not a valid PNG image.")


def download_qr_image(url: str, output_path: Path) -> None:
    req = Request(
        url,
        headers={
            "Referer": "https://weibo.com/",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
        },
    )
    with urlopen(req, timeout=30) as res:
        content = res.read()
    output_path.write_bytes(content)
    ensure_png(output_path)


def main() -> int:
    args = parse_args()
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Ensuring browser is running …")
    rc, status_out = run_command(["openclaw", "browser", "status"])
    if rc != 0 or "running: false" in status_out.lower():
        log(args.verbose, "Browser not running, starting …")
        run_openclaw(["browser", "start"], verbose=args.verbose)
    else:
        log(args.verbose, "Browser already running, skip start.")

    print("Opening Weibo login page …")
    run_openclaw(
        ["browser", "navigate", "https://passport.weibo.com/sso/signin"],
        verbose=args.verbose,
    )
    time.sleep(3)

    snapshot = ""
    for _ in range(3):
        snapshot = run_openclaw(["browser", "snapshot"], verbose=args.verbose)
        if "扫描二维码登录" in snapshot:
            break
        log(args.verbose, "QR section not found yet, retrying in 2s …")
        time.sleep(2)

    if "扫描二维码登录" not in snapshot:
        raise RuntimeError("Page did not load QR section (扫描二维码登录).")
    log(args.verbose, "Page loaded, QR section found.")

    eval_out = run_openclaw(
        [
            "browser", "evaluate", "--fn",
            "(document.querySelector('img[src*=\"qr.weibo.cn\"]') || "
            "document.querySelector('img[src*=\"gen?\"]') || "
            "document.querySelector('.qrcode_img img') || "
            "document.querySelectorAll('img')[1])"
            "?.src || ''",
        ],
        verbose=args.verbose,
    )
    qr_url = extract_qr_url(eval_out)
    if not qr_url:
        raise RuntimeError(
            "Could not extract QR URL. Weibo may have changed its page structure.\n"
            f"Evaluate output:\n{eval_out}"
        )
    log(args.verbose, f"QR URL: {qr_url}")

    download_qr_image(qr_url, output_path)
    size_kb = output_path.stat().st_size / 1024

    print("")
    print(f"QR code saved: {output_path}")
    print(f"Size: {size_kb:.1f} KB")
    print("")
    print("Scan this QR code with Weibo app (我 → 扫一扫) to log in.")
    print("After scanning, the browser session will hold the login cookies.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
