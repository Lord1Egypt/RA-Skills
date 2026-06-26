#!/usr/bin/env python3
import argparse
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


class ProxmoxAPI:
    def __init__(self, host: str, user: str, token_id: str, token_secret: str, verify_ssl: bool = False):
        self.host = host
        self.base_url = f"https://{host}:8006/api2/json"
        self.verify_ssl = verify_ssl
        self.auth_header = f"PVEAPIToken={user}!{token_id}={token_secret}"

    def _context(self):
        if self.verify_ssl:
            return None
        return ssl._create_unverified_context()

    def request(self, method: str, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        payload = None
        headers = {"Authorization": self.auth_header}
        if data is not None:
            payload = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        req = urllib.request.Request(url, data=payload, headers=headers, method=method.upper())
        with urllib.request.urlopen(req, context=self._context(), timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def get(self, path: str) -> Dict[str, Any]:
        return self.request("GET", path)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.request("POST", path, data)


def env_or_die(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        sys.exit(2)
    return value


def build_client(verify_ssl: bool = False) -> ProxmoxAPI:
    return ProxmoxAPI(
        host=env_or_die("PVE_HOST"),
        user=env_or_die("PVE_USER"),
        token_id=env_or_die("PVE_TOKEN_ID"),
        token_secret=env_or_die("PVE_TOKEN_SECRET"),
        verify_ssl=verify_ssl,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal Proxmox VE API client")
    parser.add_argument("path", help="API path, e.g. /nodes or /cluster/resources")
    parser.add_argument("--method", default="GET", choices=["GET", "POST"])
    parser.add_argument("--data", action="append", default=[], help="Form field in key=value format")
    parser.add_argument("--verify-ssl", action="store_true", help="Verify TLS certificates")
    args = parser.parse_args()

    data = {}
    for item in args.data:
        if "=" not in item:
            parser.error(f"Invalid --data value: {item}")
        key, value = item.split("=", 1)
        data[key] = value

    client = build_client(verify_ssl=args.verify_ssl)
    if args.method == "GET":
        result = client.get(args.path)
    else:
        result = client.post(args.path, data)
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
