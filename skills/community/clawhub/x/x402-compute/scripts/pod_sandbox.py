#!/usr/bin/env python3
"""
x402Compute, Agent Pods Sandbox: run commands, read and write files, and open ports on a pod
you own, through the /pods/v1 API.

Auth: an account API key with the `pods:control:write` scope, sent as X-API-Key. Pass it with
--api-key or the COMPUTE_API_KEY environment variable. Credentials are read ONLY from that
flag or variable. No .env auto-loading here.

Usage:
  python pod_sandbox.py exec <pod_id> "ls -la" [--timeout 60]
  python pod_sandbox.py ls <pod_id>
  python pod_sandbox.py cat <pod_id> notes.txt
  python pod_sandbox.py put <pod_id> notes.txt --content "hello"
  python pod_sandbox.py put <pod_id> notes.txt --from-file ./local.txt
  python pod_sandbox.py port-open <pod_id> 8080 [--private]
  python pod_sandbox.py port-list <pod_id>
  python pod_sandbox.py port-close <pod_id> 8080

See references/agent-pods-api.md (Sandbox section) for limits and response shapes.
"""

import argparse
import json
import os
import sys

import requests

BASE_URL = "https://compute.x402layer.cc/pods/v1"


def _headers(api_key: str) -> dict:
    return {"X-API-Key": api_key, "Content-Type": "application/json"}


def _call(method: str, path: str, api_key: str, body=None, params=None, timeout=60) -> dict:
    resp = requests.request(
        method,
        f"{BASE_URL}{path}",
        headers=_headers(api_key),
        data=json.dumps(body) if body is not None else None,
        params=params,
        timeout=timeout,
    )
    try:
        data = resp.json()
    except ValueError:
        data = {"raw": resp.text[:1000]}
    if resp.status_code >= 400:
        return {"error": f"HTTP {resp.status_code}", "response": data,
                "request_id": resp.headers.get("x-request-id")}
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent Pods Sandbox API (exec, files, ports)")
    parser.add_argument("--api-key", default=None,
                        help="Account API key with pods:control:write (default: COMPUTE_API_KEY env)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("exec", help="Run a shell command in the pod workspace")
    p.add_argument("pod_id")
    p.add_argument("command")
    p.add_argument("--timeout", type=int, default=60, help="Seconds, 1 to 300 (default 60)")

    p = sub.add_parser("ls", help="List workspace files")
    p.add_argument("pod_id")

    p = sub.add_parser("cat", help="Read one file")
    p.add_argument("pod_id")
    p.add_argument("path")

    p = sub.add_parser("put", help="Create or replace a text file")
    p.add_argument("pod_id")
    p.add_argument("path")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--content")
    g.add_argument("--from-file")

    p = sub.add_parser("port-open", help="Open (or rotate) a public URL to a pod port")
    p.add_argument("pod_id")
    p.add_argument("port", type=int)
    p.add_argument("--private", action="store_true", help="Require the one-time token header")

    p = sub.add_parser("port-list", help="List open ports")
    p.add_argument("pod_id")

    p = sub.add_parser("port-close", help="Close a port")
    p.add_argument("pod_id")
    p.add_argument("port", type=int)

    args = parser.parse_args()
    api_key = args.api_key or os.environ.get("COMPUTE_API_KEY")
    if not api_key:
        print(json.dumps({"error": "Set COMPUTE_API_KEY or pass --api-key (needs pods:control:write)."}))
        return 2

    pod = f"/pods/{args.pod_id}"
    if args.cmd == "exec":
        t = max(1, min(int(args.timeout), 300))
        out = _call("POST", f"{pod}/exec", api_key, {"command": args.command, "timeout_seconds": t},
                    timeout=t + 30)
    elif args.cmd == "ls":
        out = _call("GET", f"{pod}/files", api_key)
    elif args.cmd == "cat":
        out = _call("GET", f"{pod}/files", api_key, params={"path": args.path})
    elif args.cmd == "put":
        if args.from_file:
            with open(args.from_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = args.content
        out = _call("PUT", f"{pod}/files", api_key, {"path": args.path, "content": content})
    elif args.cmd == "port-open":
        out = _call("POST", f"{pod}/ports", api_key,
                    {"port": args.port, "visibility": "private" if args.private else "public"})
    elif args.cmd == "port-list":
        out = _call("GET", f"{pod}/ports", api_key)
    else:
        out = _call("DELETE", f"{pod}/ports/{args.port}", api_key)

    print(json.dumps(out, indent=2))
    return 1 if isinstance(out, dict) and "error" in out else 0


if __name__ == "__main__":
    sys.exit(main())
