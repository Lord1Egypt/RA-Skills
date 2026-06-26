#!/usr/bin/env python3
# query-1688-product-detail: Query 1688 product detail via AlphaShop API
import sys
import json
import os
import re
import requests
import urllib.parse
import time
import jwt

API_URL = "https://api.alphashop.cn/alphashop.openclaw.offer.detail.query/1.0"

def get_api_key():
    """Generate JWT token using ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY."""
    ak = os.environ.get("ALPHASHOP_ACCESS_KEY", "").strip()
    sk = os.environ.get("ALPHASHOP_SECRET_KEY", "").strip()

    if not ak:
        print("Error: ALPHASHOP_ACCESS_KEY not set. Configure it in OpenClaw:\n"
              '  skills.entries.query-1688-product-detail.apiKey or\n'
              '  skills.entries.query-1688-product-detail.env.ALPHASHOP_ACCESS_KEY',
              file=sys.stderr)
        sys.exit(1)
    
    if not sk:
        print("Error: ALPHASHOP_SECRET_KEY not set. Configure it in OpenClaw:\n"
              '  skills.entries.query-1688-product-detail.env.ALPHASHOP_SECRET_KEY',
              file=sys.stderr)
        sys.exit(1)
    
    # Generate JWT token
    try:
        # Current time in seconds
        current_time = int(time.time())
        
        # Expired time: current time + 1800 seconds (30 minutes)
        expired_at = current_time + 1800
        
        # Not before time: current time - 5 seconds
        not_before = current_time - 5
        
        # Create JWT token with HS256 algorithm
        token = jwt.encode(
            payload={
                "iss": ak,                    # Issuer: Access Key
                "exp": expired_at,            # Expiration time
                "nbf": not_before             # Not before time
            },
            key=sk,                          # Secret Key for HMAC256
            algorithm="HS256",
            headers={"alg": "HS256"}
        )
        
        # PyJWT < 2.0 returns bytes, >= 2.0 returns str
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token
    except Exception as e:
        print(f"Error generating JWT token: {e}", file=sys.stderr)
        sys.exit(1)

def parse_input(arg):
    """Parse input: URL → extract productId; pure digits → use as ID; comma-separated → list."""
    arg = arg.strip()

    # Pure numeric string
    if arg.isdigit():
        return [arg]

    # Comma-separated IDs
    if ',' in arg and all(part.strip().isdigit() for part in arg.split(',')):
        return [part.strip() for part in arg.split(',')]

    # URL — extract offerId from path /offer/XXXX.html
    path_match = re.search(r'/offer/([0-9]+)\.html', arg)
    if path_match:
        return [path_match.group(1)]

    # URL — extract from query param ?offerId=XXXX
    parsed = urllib.parse.urlparse(arg)
    query_params = urllib.parse.parse_qs(parsed.query)
    if 'offerId' in query_params and query_params['offerId']:
        return [query_params['offerId'][0]]

    raise ValueError(f"Unrecognized input: '{arg}'. Expected a product URL or numeric productId(s).")

def main():
    if len(sys.argv) != 2:
        print("Usage: query-1688-product-detail <URL | productId | id1,id2,...>", file=sys.stderr)
        sys.exit(1)

    try:
        product_ids = parse_input(sys.argv[1])
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    results = []
    for pid in product_ids:
        payload = {"productId": pid}
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                data["input"] = pid
                results.append(data)
            else:
                results.append({
                    "input": pid,
                    "error": f"HTTP {resp.status_code}",
                    "response": resp.text[:200]
                })
        except Exception as e:
            results.append({"input": pid, "error": str(e)})

    if len(results) == 1:
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()