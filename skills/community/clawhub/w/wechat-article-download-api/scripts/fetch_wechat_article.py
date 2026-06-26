#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_URL = "https://down.mptext.top/api/public/v1/download"
SUPPORTED_FORMATS = ("html", "markdown", "text", "json")
EXTENSIONS = {"html": "html", "markdown": "md", "text": "txt", "json": "json"}


def fetch(api_url: str, article_url: str, fmt: str, timeout: int):
    query = urllib.parse.urlencode({"url": article_url, "format": fmt})
    req = urllib.request.Request(
        f"{api_url}?{query}",
        method="GET",
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://mp.weixin.qq.com/",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            ctype = resp.headers.get("Content-Type", "")
            body = resp.read()
            return status, ctype, body, ""
    except urllib.error.HTTPError as err:
        body = err.read() if err.fp else b""
        return err.code, err.headers.get("Content-Type", ""), body, str(err)
    except Exception as err:  # pragma: no cover - defensive fallback
        return 0, "", b"", str(err)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch WeChat article content from down.mptext.top API."
    )
    parser.add_argument("--url", required=True, help="Target WeChat article URL")
    parser.add_argument(
        "--formats",
        nargs="+",
        default=["html"],
        help="One or more formats: html markdown text json",
    )
    parser.add_argument("--api-url", default=API_URL, help="Download API endpoint")
    parser.add_argument("--outdir", default=".", help="Output directory")
    parser.add_argument("--basename", default="wx_article", help="Output base name")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout seconds")
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop immediately when one format fails",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Print machine-readable summary JSON",
    )
    args = parser.parse_args()

    formats = [f.strip().lower() for f in args.formats if f.strip()]
    invalid = [f for f in formats if f not in SUPPORTED_FORMATS]
    if invalid:
        raise SystemExit(f"Unsupported format(s): {', '.join(invalid)}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    results = []
    failed = False

    for fmt in formats:
        status, ctype, body, err = fetch(args.api_url, args.url, fmt, args.timeout)
        ext = EXTENSIONS[fmt]
        output_path = outdir / f"{args.basename}.{ext}"
        ok = status == 200

        if ok:
            output_path.write_bytes(body)
            size = len(body)
            message = "ok"
        else:
            size = len(body)
            message = err or f"http {status}"
            failed = True

        record = {
            "format": fmt,
            "status": status,
            "content_type": ctype,
            "ok": ok,
            "size_bytes": size,
            "file": str(output_path),
            "message": message,
        }
        results.append(record)

        if args.print_json:
            continue
        print(
            f"[{fmt}] status={status} ok={ok} type='{ctype}' size={size} file='{output_path}' msg='{message}'"
        )

        if args.fail_fast and not ok:
            break

    if args.print_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))

    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
