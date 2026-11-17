#!/usr/bin/env python3
"""Test client: purchase → key → call.

🔒 SECURITY (SkillSpector fix 20/8):
- The API key (credential) is ONLY sent to localhost (local test) or an
  explicit HTTPS endpoint via X402_BASE. Never to plain HTTP outside localhost.
"""
import json, os, urllib.request, urllib.error

# Default: local test. For production API: set X402_BASE=https://your-server.dk
BASE = os.environ.get("X402_BASE", "https://localhost:8791")  # lokal default; ekstern kun via eksplicit X402_BASE

# 🔒 Refuse to send credentials over plain HTTP to non-local hosts
if BASE.startswith("http://") and "localhost" not in BASE and "127.0.0.1" not in BASE:
    raise SystemExit("ERROR: Refusing to send API key over HTTP to " + BASE +
                     " — use HTTPS (X402_BASE=https://...)")


def call(path, method="GET", body=None, key=None):
    req = urllib.request.Request(BASE + path, method=method)
    if key: req.add_header("x-api-key", key)
    if body is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(body).encode()
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:150]


if __name__ == "__main__":
    st, res = call("/v1/purchase", "POST", {"txHash": "0x" + "ab"*24, "amountUsd": 0.005})
    print("purchase:", st, res.get("apiKey", "")[:10] + "..." if isinstance(res, dict) else res)
    key = res.get("apiKey", "") if isinstance(res, dict) else ""
    st2, res2 = call("/v1/signals", key=key)
    print("signals:", st2, str(res2)[:120])
    st3, _ = call("/v1/signals")
    print("without key:", st3, "(expected 401)")
