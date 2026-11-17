#!/usr/bin/env python3
"""soft-ip-full-lifecycle-delivery-pro - Service execution script (Phase 3)

Reads payCredential from local order file. If valid, authorizes AI to
draft software copyright registration documents in conversation.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import sys
import time

SLUG = "soft-ip-full-lifecycle-delivery-pro"
CREDENTIAL_TTL = 86400

# ============================================================
# Order file management (local persistence for clawtip payment)
# ============================================================

_INDICATOR_RE = re.compile(r"^[a-fA-F0-9]{32}$")
_ORDER_NO_RE = re.compile(r"^[0-9]{14,32}$")


def _validate_indicator(indicator):
    if not _INDICATOR_RE.fullmatch(indicator):
        raise ValueError("Invalid indicator format")


def _validate_order_no(order_no):
    if not _ORDER_NO_RE.fullmatch(order_no):
        raise ValueError("Invalid order_no format")


def _get_orders_dir(indicator):
    _validate_indicator(indicator)
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home, "openclaw", "skills", "orders", indicator)
    else:
        return os.path.join(home, ".openclaw", "skills", "orders", indicator)


def _load_order(indicator, order_no):
    _validate_order_no(order_no)
    path = os.path.join(_get_orders_dir(indicator), f"{order_no}.json")
    if not os.path.isfile(path):
        raise RuntimeError(f"Order file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ============================================================


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def is_credential_valid(order_data: dict) -> bool:
    credential = order_data.get("payCredential")
    if not credential:
        return False
    credential_ts = order_data.get("credentialTimestamp")
    if credential_ts and time.time() - credential_ts > CREDENTIAL_TTL:
        return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify payment and authorize document drafting service"
    )
    parser.add_argument("order_no", help="Order number from Phase 1")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)

    try:
        order_data = _load_order(indicator, args.order_no)
    except Exception as e:
        print("PAY_STATUS: ERROR")
        print(f"ERROR_INFO: Order file read failed: {e}")
        sys.exit(1)

    if not is_credential_valid(order_data):
        print("PAY_STATUS: ERROR")
        print("ERROR_INFO: No valid payment credential found. Complete payment via clawtip first.")
        sys.exit(1)

    pay_status = order_data.get("payStatus", "SUCCESS")
    print(f"PAY_STATUS: {pay_status}")

    if pay_status != "SUCCESS":
        print(f"ERROR_INFO: Payment status is '{pay_status}', cannot proceed")
        sys.exit(1)

    print("AUTHORIZATION_RESULT=verified")
    print("\n" + "=" * 60)
    print("  Service Authorized - Document Drafting")
    print("=" * 60)
    print("Payment verified. The AI model will now draft the following")
    print("8 documents for software copyright registration:\n")
    print("  1. 软件著作权登记申请表 (Application Form)")
    print("  2. 软件说明书 (Software Specification)")
    print("  3. 用户操作手册 (User Manual)")
    print("  4. 源程序代码文档 - 前30页 (Source Code - First 30 Pages)")
    print("  5. 源程序代码文档 - 后30页 (Source Code - Last 30 Pages)")
    print("  6. 文档材料目录 (Document Index)")
    print("  7. 权利归属证明 (Rights Attribution Certificate)")
    print("  8. 申请材料汇总表 (Submission Summary)")
    print("=" * 60)

    _jr = json.dumps({
        "pay_status": pay_status,
        "authorization": "verified",
        "order_no": args.order_no,
        "service": "soft-ip-delivery-pro",
        "documents": 8,
    })
    print(f"JSON_RESULT={_jr}")
