#!/usr/bin/env python3
"""
x402 Webhook Payment Verifier (Python)

Purpose:
- Verify webhook HMAC signature (X-X402-Signature / X-X402-Timestamp)
- Optionally verify receipt JWT (RS256/JWKS) via PyJWT
- Cross-check payload fields against receipt claims

Current Studio seller webhook deliveries also include:
- X-X402-Event
- X-X402-Event-Id

Verification model:
- payload = "<timestamp>.<raw_request_body>"
- algorithm = HMAC-SHA256
- secret = webhook signing_secret

Legacy raw-secret header auth may still exist in older receivers, but
current Studio deliveries should be validated with the signed headers first.

Install:
  pip install -r requirements.txt   # pyjwt + cryptography already included

Usage:
  python verify_webhook_payment.py \
    --body-file ./webhook.json \
    --signature 't=1700000000,v1=<hex>' \
    --secret '<SIGNING_SECRET>' \
    --required-source-slug my-api \
    --require-receipt
"""

import argparse
import hashlib
import hmac
import json
import sys
from typing import Any, Dict, List, Optional, Tuple


# Default JWKS endpoint for x402 receipt tokens
DEFAULT_JWKS_URL = "https://api.x402layer.cc/.well-known/jwks.json"


def parse_signature(header_value: str) -> Tuple[str, List[str]]:
    """Parse X-X402-Signature header into (timestamp, [v1_signatures])."""
    if not header_value:
        raise ValueError("Missing --signature")

    timestamp: Optional[str] = None
    signatures: List[str] = []

    for part in header_value.split(","):
        kv = part.strip().split("=", 1)
        if len(kv) != 2:
            continue
        k, v = kv[0].strip(), kv[1].strip()
        if not k or not v:
            continue
        if k == "t":
            timestamp = v
        elif k == "v1":
            signatures.append(v)

    if not timestamp or not signatures:
        raise ValueError("Invalid --signature format. Expected: t=<timestamp>,v1=<hex>")

    return timestamp, signatures


def verify_webhook_hmac(
    secret: str, timestamp: str, raw_body: str, received_sigs: List[str]
) -> Tuple[bool, str]:
    """Verify HMAC-SHA256 webhook signature using timing-safe comparison."""
    signed_payload = f"{timestamp}.{raw_body}"
    expected = hmac.new(
        secret.encode("utf-8"),
        signed_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    for sig in received_sigs:
        if hmac.compare_digest(expected, sig):
            return True, expected

    return False, expected


def verify_receipt_token(
    token: str,
    required_source_slug: Optional[str] = None,
    jwks_url: str = DEFAULT_JWKS_URL,
) -> Dict[str, Any]:
    """Verify receipt JWT using RS256/JWKS and return decoded claims."""
    try:
        import jwt
        from jwt import PyJWKClient
    except ImportError:
        raise ImportError(
            "Missing dependency PyJWT. Run: pip install pyjwt[crypto]"
        )

    jwks_client = PyJWKClient(jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    claims = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        options={"verify_aud": False},
    )

    if required_source_slug and claims.get("source_slug") != required_source_slug:
        raise ValueError(
            f"Receipt source_slug mismatch: "
            f"expected={required_source_slug} got={claims.get('source_slug')}"
        )

    return claims


def first_defined(*values: Any) -> Any:
    """Return the first value that is not None and not empty string."""
    for v in values:
        if v is not None and v != "":
            return v
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="x402 Webhook Payment Verifier"
    )
    parser.add_argument(
        "--body-file", help="Path to raw webhook JSON body"
    )
    parser.add_argument(
        "--body", help="Raw JSON body string (instead of --body-file)"
    )
    parser.add_argument(
        "--signature",
        required=True,
        help="X-X402-Signature header, format: t=<ts>,v1=<hex>",
    )
    parser.add_argument(
        "--secret",
        required=True,
        help="Webhook signing_secret from create/manage webhook",
    )
    parser.add_argument(
        "--receipt-token", help="Receipt JWT (if omitted, tries body.data.receipt_token)"
    )
    parser.add_argument(
        "--required-source-slug",
        help="Enforce source_slug when verifying receipt token",
    )
    parser.add_argument(
        "--expected-event",
        default="payment.succeeded",
        help="Expected event type (default: payment.succeeded)",
    )
    parser.add_argument(
        "--require-receipt",
        action="store_true",
        help="Fail when receipt token is missing or invalid",
    )
    parser.add_argument(
        "--jwks-url",
        default=DEFAULT_JWKS_URL,
        help="JWKS endpoint URL (default: x402 production)",
    )
    args = parser.parse_args()

    # Load body
    if args.body is not None:
        raw_body = args.body
    elif args.body_file is not None:
        with open(args.body_file, "r") as f:
            raw_body = f.read()
    else:
        parser.error("One of --body-file or --body is required")
        return  # unreachable, keeps type checker happy

    parsed_body = json.loads(raw_body)

    # Step 1: HMAC signature verification
    timestamp, signatures = parse_signature(args.signature)
    ok, expected = verify_webhook_hmac(args.secret, timestamp, raw_body, signatures)

    if not ok:
        raise ValueError("Invalid webhook signature")

    # Step 2: Event type check
    if args.expected_event and parsed_body.get("type") != args.expected_event:
        raise ValueError(
            f"Unexpected event type. got={parsed_body.get('type')} "
            f"expected={args.expected_event}"
        )

    # Step 3: Receipt token verification
    token = first_defined(
        args.receipt_token,
        (parsed_body.get("data") or {}).get("receipt_token"),
        parsed_body.get("receipt_token"),
        (parsed_body.get("payment") or {}).get("receipt_token"),
    )

    receipt_claims: Optional[Dict[str, Any]] = None
    if token:
        receipt_claims = verify_receipt_token(
            token, args.required_source_slug, args.jwks_url
        )

        # Cross-check: tx_hash
        payload_tx = (parsed_body.get("data") or {}).get("tx_hash")
        if payload_tx and receipt_claims.get("tx_hash") and payload_tx != receipt_claims["tx_hash"]:
            raise ValueError("Receipt tx_hash does not match webhook payload tx_hash")

        # Cross-check: source_slug
        payload_slug = (parsed_body.get("data") or {}).get("source_slug")
        if payload_slug and receipt_claims.get("source_slug") and payload_slug != receipt_claims["source_slug"]:
            raise ValueError("Receipt source_slug does not match webhook payload source_slug")

        # Cross-check: amount
        payload_amount = (parsed_body.get("data") or {}).get("amount")
        if payload_amount is not None and receipt_claims.get("amount") is not None:
            try:
                left = float(payload_amount)
                right = float(receipt_claims["amount"])
                if left != right:
                    raise ValueError("Receipt amount does not match webhook payload amount")
            except (TypeError, ValueError) as e:
                if "does not match" in str(e):
                    raise
    elif args.require_receipt:
        raise ValueError("Missing receipt token (--receipt-token or body.data.receipt_token)")

    data = parsed_body.get("data") or {}
    result = {
        "ok": True,
        "verified": {
            "webhook_signature": True,
            "receipt_token": receipt_claims is not None,
        },
        "event": parsed_body.get("type"),
        "source_slug": first_defined(data.get("source_slug"), (receipt_claims or {}).get("source_slug")),
        "tx_hash": first_defined(data.get("tx_hash"), (receipt_claims or {}).get("tx_hash")),
        "amount": first_defined(data.get("amount"), (receipt_claims or {}).get("amount")),
        "currency": first_defined(data.get("currency"), (receipt_claims or {}).get("currency")),
        "receipt_claims": receipt_claims,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        sys.exit(1)
