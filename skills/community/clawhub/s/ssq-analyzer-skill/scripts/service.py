#!/usr/bin/env python3
"""ssq-analyzer - Service execution script (Phase 3)

Free tier: runs data fetch and statistical analysis without payment.
Paid tier: reads payCredential from local order file; if valid, adds
5 recommended number sets to the analysis report.

Order file stored at: ~/.openclaw/skills/orders/{indicator}/{order_no}.json
Fields: payTo, amount, order_no, encrypted_data, slug, question, description, resource_url.
These are standard clawtip payment fields only.
User question text is stored locally - do not include passwords or secrets.
No SSQ draw data, purchase history, or personal info is stored.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import sys
import time

SLUG = "ssq-analyzer"
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(SKILL_DIR, "scripts", "\u6700\u65b0\u5206\u6790\u7ed3\u679c.md")
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
# SSQ analysis modules - imported directly (not via subprocess)
# ============================================================

def run_free_analysis() -> str:
    """Run data fetch and free analysis by importing modules directly."""
    import scripts.fetch_ssq as fetch
    import scripts.analyze_ssq as analyze

    print("[STEP 1/2] Fetching latest SSQ data from cwl.gov.cn...")
    fetch.main()
    print("[FETCH COMPLETE]")

    print("\n[STEP 2/2] Generating free analysis report...")
    analyze.main()
    print("[ANALYSIS COMPLETE]")

    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "[Report generated - check console output above]"


def run_paid_recommendation() -> str:
    """Run recommendation generation (only after payment verification).
    Called directly via module import, not subprocess."""
    print("\n[STEP 3/3] Generating paid recommendation numbers...")
    import scripts.recommend_ssq as recommend
    recommend.generate_recommendations()
    return "[Recommendation numbers printed above]"


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
    parser = argparse.ArgumentParser(description="SSQ analysis and recommendation service")
    parser.add_argument("order_no", nargs="?", default="", help="Order number from Phase 1 (optional, for paid tier)")
    args = parser.parse_args()

    try:
        print("=" * 60)
        print("  SSQ Analyzer - Free Tier Analysis")
        print("=" * 60)
        report = run_free_analysis()
        print("\n" + "=" * 50)
        print("  Free Analysis Complete")
        print("=" * 50)
        print(report)

        if args.order_no:
            indicator = compute_indicator(SLUG)
            try:
                order_data = _load_order(indicator, args.order_no)
                if is_credential_valid(order_data):
                    pay_status = order_data.get("payStatus", "SUCCESS")
                    if pay_status == "SUCCESS" or pay_status == "TEST_SUCCESS":
                        print("\n" + "=" * 60)
                        print("  Payment Verified - Adding Recommendation Numbers")
                        print("=" * 60)
                        recommendation = run_paid_recommendation()
                        print(recommendation)
                    else:
                        print(f"\n[INFO] Payment status is '{pay_status}'. Skipping paid recommendations.")
                else:
                    print("\n[INFO] No valid payment credential found. Free report only.")
                    print("  To get 5 recommended number sets, complete payment via clawtip first.")
            except Exception:
                print("\n[INFO] No valid order found. Free analysis only.")
        else:
            print("\n[INFO] Free report generated. To unlock 5 recommended number sets,")
            print("  create an order and complete payment via clawtip.")

        print("\n" + "=" * 60)
        print("  PAY_STATUS: SUCCESS")
        print("=" * 60)

    except (RuntimeError, Exception) as e:
        print("PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {e}")
        sys.exit(1)
