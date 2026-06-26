#!/usr/bin/env python3
import argparse
from common import get_token, request_json, print_json, is_success_response
from config import claw_search_path
from claw_search import normalize_search_payload


def main():
    ap = argparse.ArgumentParser(description="WotoHub auth check for user-state operations")
    ap.add_argument("--token")
    args = ap.parse_args()

    token = get_token(args.token, required=True, feature="preflight")

    # Use clawSearch as preflight check instead of selUserInfo
    preflight_payload = normalize_search_payload({
        "platform": "tiktok",
        "pageNum": 1,
        "pageSize": 1,
    })
    auth_check = request_json("POST", claw_search_path(), token, preflight_payload)

    result = {
        "authCheck": auth_check,
        "ok": is_success_response(auth_check),
        "note": "Token validated via clawSearch. Required for user-state operations such as send/inbox/reply.",
    }
    print_json(result)


if __name__ == "__main__":
    main()
