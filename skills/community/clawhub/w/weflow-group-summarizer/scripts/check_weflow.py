#!/usr/bin/env python3
"""Check WeFlow API connectivity."""

import argparse
import json
import sys
import urllib.request
import urllib.error


def main():
    parser = argparse.ArgumentParser(description="Check WeFlow API connectivity")
    parser.add_argument(
        "--host",
        default="http://127.0.0.1:5031",
        help="WeFlow API host (default: http://127.0.0.1:5031)",
    )
    args = parser.parse_args()

    host = args.host.rstrip("/")
    url = f"{host}/health"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
            if data.get("status") == "ok":
                print(host)
                sys.exit(0)
            else:
                print(f"Unexpected response: {data}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection failed: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
