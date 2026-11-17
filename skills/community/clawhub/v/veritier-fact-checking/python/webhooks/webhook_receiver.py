#!/usr/bin/env python3
"""
Webhook Receiver with HMAC-SHA256 Verification - Veritier Example (Python)
===========================================================================
Verifies X-Veritier-Signature against the raw body bytes, then processes
extract / verify / validate / attestation deliveries.

Retries send the same Idempotency-Key / X-Veritier-Idempotency-Key
(attest: attestation:{action_id}:{transaction_id}). HMAC is over the body only.

Setup:
  1. pip install flask python-dotenv
  2. Set VERITIER_WEBHOOK_SECRET in your .env (vtsec_... from the dashboard)
  3. python webhook_receiver.py
  4. Listen on http://localhost:5050/webhooks/veritier

Dashboard allows http://localhost for test webhooks. Production URLs need HTTPS.

Full webhook docs: https://veritier.ai/docs#webhooks
"""

import hmac
import hashlib
import os
from dotenv import load_dotenv
from flask import Flask, request, abort, jsonify

load_dotenv()

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("VERITIER_WEBHOOK_SECRET", "")
_seen_idem = set()

if not WEBHOOK_SECRET:
    print("Warning: VERITIER_WEBHOOK_SECRET is not set.")
    print("  Configure a webhook at https://veritier.ai/dashboard to get your secret.")


@app.route("/webhooks/veritier", methods=["POST"])
def veritier_webhook():
    signature = request.headers.get("X-Veritier-Signature", "")
    idem = request.headers.get("Idempotency-Key") or request.headers.get(
        "X-Veritier-Idempotency-Key", ""
    )
    action_id = request.headers.get("X-Veritier-Action-Id", "")

    if not WEBHOOK_SECRET:
        print("Webhook secret not configured - rejecting request")
        abort(500)

    raw_body = request.data
    expected_signature = "vtsec_" + hmac.new(
        key=WEBHOOK_SECRET.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        print("Invalid webhook signature - rejecting request")
        abort(401)

    if idem:
        if idem in _seen_idem:
            print(f"Duplicate Idempotency-Key {idem} - ignoring retry")
            return jsonify({"status": "ok", "duplicate": True}), 200
        _seen_idem.add(idem)

    payload = request.get_json(force=True)
    transaction_id = payload.get("transaction_id", "unknown")
    kind = payload.get("type", "event")
    is_test = payload.get("is_test", False)
    results = payload.get("results")

    print(f"\n{'─' * 50}")
    if is_test:
        print("[TEST MODE] No quota was consumed.")
    print(f"type={kind}  tx={transaction_id}  idem={idem or '(none)'}")
    if action_id:
        print(f"X-Veritier-Action-Id={action_id}")

    if kind == "attestation" and isinstance(results, dict):
        print(f"  decision={results.get('decision')}  credential_id={results.get('credential_id')}")
        print(f"  action_id={payload.get('action_id') or results.get('action_id')}")
    elif isinstance(results, list):
        print(f"  claims: {len(results)}")
        for res in results:
            print(f"    {res.get('claim')} -> {res.get('verdict')}")
    else:
        print(f"  results: {str(results)[:200]}")

    print(f"{'─' * 50}\n")
    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print("Veritier Webhook Receiver")
    print("  Listening on http://localhost:5050/webhooks/veritier")
    app.run(host="0.0.0.0", port=5050, debug=True)
