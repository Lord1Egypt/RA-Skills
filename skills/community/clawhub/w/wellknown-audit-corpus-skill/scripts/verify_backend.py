#!/usr/bin/env python3
"""Verify this ClawMart package points at live production x402 backends.

No payment is made. Paid routes are checked for an HTTP 402 payment envelope only.
"""
import json
import sys
import urllib.error
import urllib.request

CHECKS = [('https://wellknown-audit-corpus.mtree.workers.dev', '/v1/wellknowns/readiness_report', {'url': 'https://evm-tx-toolkit.mtree.workers.dev'})]
USER_AGENT = "MoneyTreeClawMartVerifier/1.0"


def request(url, method="GET", body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"content-type": "application/json", "user-agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def main():
    failures = []
    for backend, paid_path, payload in CHECKS:
        root_status, _ = request(backend + "/")
        if root_status >= 500:
            failures.append(f"{backend} root returned {root_status}")
        mcp_status, _ = request(backend + "/.well-known/mcp.json")
        if mcp_status >= 500 or mcp_status == 404:
            failures.append(f"{backend} .well-known/mcp.json returned {mcp_status}")
        status, text = request(backend + paid_path, "POST", payload)
        if status != 402 or "payTo" not in text or "x402" not in text.lower():
            failures.append(f"{backend}{paid_path} expected x402 402 envelope, got {status}")
        else:
            print(f"OK {backend}{paid_path} returns x402 402 envelope")
    if failures:
        print("FAIL")
        for failure in failures:
            print("-", failure)
        return 1
    print("BACKEND_VERIFY_OK: no payment made")
    return 0


if __name__ == "__main__":
    sys.exit(main())
