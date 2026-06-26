#!/usr/bin/env python3
"""stocki-financial-reader diagnose: 4-check connectivity smoke test.

[1/4] Reachability        GET $STOCKI_GATEWAY_URL/api/v3/market/status?area=all (10s)
[2/4] Auth + read         POST /api/v3/quotes/get_latest_quotes for 600519
[3/4] Name-resolver asset POST /api/v1/match/assets for 贵州茅台 → 600519
[4/4] Name-resolver coll  POST /api/v1/match/collections for 中证500 → 000905.SH

Exit codes: 0 success / 1 auth / 2 unreachable / 3 unavailable / 4 rate.
stdlib-only.
"""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SAMPLE_SYMBOL = "600519"   # Kweichow Moutai (cn:stock); stable + always-trading
EXPECTED_FIELDS = ("symbol", "close")


def check_reachability(base, key, timeout=10):
    url = f"{base.rstrip('/')}/api/v3/market/status?area=all"
    req = Request(url, headers={"Authorization": f"Bearer {key}"}, method="GET")
    try:
        with urlopen(req, timeout=timeout) as resp:
            resp.read()
            return True, "200 OK"
    except HTTPError as e:
        if e.code == 401:
            return False, ("auth_invalid", "401 from gateway")
        if e.code == 429:
            return False, ("rate_limited", "429 from gateway")
        if e.code >= 500:
            return False, ("stocki_unavailable", f"HTTP {e.code}")
        return False, ("unknown", f"HTTP {e.code}")
    except (URLError, TimeoutError, OSError) as e:
        return False, ("unreachable", str(e))


def check_auth_read(base, key, timeout=15):
    url = f"{base.rstrip('/')}/api/v3/quotes/get_latest_quotes"
    body = json.dumps({
        "assets": [{"symbols": [SAMPLE_SYMBOL], "area": "cn", "asset_type": "stock"}],
        "include_fundamentals": False,
        "timeout": 5.0,
    }).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        if e.code == 401:
            return False, ("auth_invalid", "401")
        if e.code == 429:
            return False, ("rate_limited", "429")
        if e.code >= 500:
            return False, ("stocki_unavailable", f"HTTP {e.code}")
        return False, ("unknown", f"HTTP {e.code}")
    except (URLError, TimeoutError, OSError) as e:
        return False, ("unreachable", str(e))

    records = data.get("data") or []
    if not records:
        return False, ("shape_invalid", "response.data empty")
    sample = records[0]
    missing = [f for f in EXPECTED_FIELDS if f not in sample]
    if missing:
        return False, ("shape_invalid", f"missing fields: {missing}")
    return True, f"{SAMPLE_SYMBOL} -> symbol+close"


def check_name_resolver_asset(base, key, timeout=15):
    url = f"{base.rstrip('/')}/api/v1/match/assets"
    body = json.dumps({
        "keys": ["贵州茅台"],
        "area": "cn",
        "type": "stock",
    }).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        if e.code == 401:
            return False, ("auth_invalid", "401")
        if e.code == 404:
            return False, ("unreachable", "reverse-proxy 404 (not deployed?)")
        if e.code == 429:
            return False, ("rate_limited", "429")
        if e.code >= 500:
            return False, ("stocki_unavailable", f"HTTP {e.code}")
        return False, ("unknown", f"HTTP {e.code}")
    except (URLError, TimeoutError, OSError) as e:
        return False, ("unreachable", str(e))

    if not data.get("success"):
        return False, ("shape_invalid", "response.success != True")
    rows = data.get("data") or []
    if not rows:
        return False, ("shape_invalid", "response.data empty")
    asset = rows[0].get("asset") or {}
    if not asset:
        return False, ("shape_invalid", "response.data[0].asset missing")
    if asset.get("code") != "600519":
        return False, ("shape_invalid", f"expected code=600519, got {asset.get('code')}")
    return True, f"贵州茅台 -> {asset['code']} method={rows[0].get('method')}"


def check_name_resolver_collection(base, key, timeout=15):
    url = f"{base.rstrip('/')}/api/v1/match/collections"
    body = json.dumps({
        "keys": ["中证500"],
        "area": "cn",
        "type": "index",
    }).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        if e.code == 401:
            return False, ("auth_invalid", "401")
        if e.code == 404:
            return False, ("unreachable", "reverse-proxy 404 (not deployed?)")
        if e.code == 429:
            return False, ("rate_limited", "429")
        if e.code >= 500:
            return False, ("stocki_unavailable", f"HTTP {e.code}")
        return False, ("unknown", f"HTTP {e.code}")
    except (URLError, TimeoutError, OSError) as e:
        return False, ("unreachable", str(e))

    if not data.get("success"):
        return False, ("shape_invalid", "response.success != True")
    rows = data.get("data") or []
    if not rows:
        return False, ("shape_invalid", "response.data empty")
    col = rows[0].get("collection") or {}
    if not col:
        return False, ("shape_invalid", "response.data[0].collection missing")
    if col.get("symbol") != "000905.SH":
        return False, ("shape_invalid", f"expected symbol=000905.SH, got {col.get('symbol')}")
    return True, f"中证500 -> {col['symbol']} method={rows[0].get('method')}"


def main():
    print("stocki-financial-reader Diagnose")
    print("=" * 48)
    base = os.environ.get("STOCKI_GATEWAY_URL", "")
    key = os.environ.get("STOCKI_API_KEY", "")
    if not base or not key:
        print("[ERROR] STOCKI_GATEWAY_URL or STOCKI_API_KEY missing", file=sys.stderr)
        sys.exit(1)

    passed = 0
    error_class = None

    # 1/4 Reachability
    ok, info = check_reachability(base, key)
    if ok:
        print(f"[1/4] Reachability        OK    {info}")
        passed += 1
    else:
        cls, detail = info
        print(f"[1/4] Reachability        FAIL  {cls}: {detail}")
        error_class = cls

    # 2/4 Auth + read (only if reachable)
    if ok:
        ok2, info2 = check_auth_read(base, key)
        if ok2:
            print(f"[2/4] Auth + read         OK    {info2}")
            passed += 1
        else:
            cls, detail = info2
            print(f"[2/4] Auth + read         FAIL  {cls}: {detail}")
            error_class = cls
    else:
        print("[2/4] Auth + read         SKIP  (reachability failed)")

    # 3/4 Name-resolver asset (only if reachable)
    if ok:
        ok3, info3 = check_name_resolver_asset(base, key)
        if ok3:
            print(f"[3/4] Name-resolver asset OK    {info3}")
            passed += 1
        else:
            cls, detail = info3
            print(f"[3/4] Name-resolver asset FAIL  {cls}: {detail}")
            if error_class is None:
                error_class = cls
    else:
        print("[3/4] Name-resolver asset SKIP  (reachability failed)")

    # 4/4 Name-resolver collection (only if reachable)
    if ok:
        ok4, info4 = check_name_resolver_collection(base, key)
        if ok4:
            print(f"[4/4] Name-resolver coll  OK    {info4}")
            passed += 1
        else:
            cls, detail = info4
            print(f"[4/4] Name-resolver coll  FAIL  {cls}: {detail}")
            if error_class is None:
                error_class = cls
    else:
        print("[4/4] Name-resolver coll  SKIP  (reachability failed)")

    print("=" * 48)
    print(f"Result: {passed}/4 passed")

    code_map = {
        "auth_invalid": 1,
        "unreachable": 2,
        "stocki_unavailable": 3,
        "rate_limited": 4,
        "unknown": 3,        # unrecognized upstream 4xx → treat as service-side anomaly, not auth (review I-2)
        "shape_invalid": 3,  # response missing expected fields → upstream contract drift, same class
    }
    sys.exit(code_map.get(error_class, 0 if passed == 4 else 1))


if __name__ == "__main__":
    main()
