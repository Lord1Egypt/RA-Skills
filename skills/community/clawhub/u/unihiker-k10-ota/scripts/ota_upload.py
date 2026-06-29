#!/usr/bin/env python3
"""Upload firmware to a K10 board via HTTP OTA.

This script uses only the Python standard library, so it runs on Windows,
macOS, and Linux anywhere Python 3 is available.
"""

import argparse
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request


def build_ota_url(host_or_url: str, endpoint: str) -> str:
    host_or_url = host_or_url.strip()
    if "://" not in host_or_url:
        host_or_url = f"http://{host_or_url}"

    parsed = urllib.parse.urlparse(host_or_url)
    if parsed.path and parsed.path != "/":
        return host_or_url
    return urllib.parse.urljoin(host_or_url.rstrip("/") + "/", endpoint.lstrip("/"))


def upload(host_or_url: str, bin_path: Path, endpoint: str, timeout: int) -> bool:
    url = build_ota_url(host_or_url, endpoint)
    firmware_name = bin_path.name
    print(f"Uploading {bin_path} to {url} ...")

    data = bin_path.read_bytes()

    boundary = "----WebKitFormBoundaryK10OTA"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{firmware_name}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode("utf-8")
    body += data
    body += f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
            "Connection": "close",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = resp.read().decode("utf-8", errors="replace").strip()
            print(f"Response: {result}")
            if result == "OK":
                print("OTA upload successful. Device will restart in ~1.2s.")
                return True
            print("OTA upload failed.")
            return False
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace").strip()
        print(f"HTTP {e.code}: {body or e.reason}")
        return False
    except OSError as e:
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="K10 HTTP OTA uploader")
    parser.add_argument("bin", type=Path, help="Path to .bin firmware file")
    parser.add_argument(
        "--ip",
        "--host",
        dest="host",
        default="192.168.9.42",
        help="Device IP, host name, or full OTA URL",
    )
    parser.add_argument("--endpoint", default="/ota", help="OTA endpoint path")
    parser.add_argument("--timeout", type=int, default=60, help="Upload timeout in seconds")
    args = parser.parse_args()

    bin_path = args.bin.expanduser().resolve()
    if not bin_path.is_file():
        print(f"Firmware file not found: {bin_path}")
        sys.exit(2)

    if not upload(args.host, bin_path, args.endpoint, args.timeout):
        sys.exit(1)


if __name__ == "__main__":
    main()
