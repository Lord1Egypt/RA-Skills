#!/usr/bin/env python3
"""
Webhook Receiver with HMAC-SHA256 Verification - Veritier Example (Python)
===========================================================================
A minimal Flask server that receives async webhook deliveries from Veritier
and verifies their HMAC-SHA256 signatures before processing.

When you enable webhooks in your Veritier dashboard and set `use_webhook: true`
in API requests, results are delivered asynchronously to this endpoint.

Setup:
  1. pip install flask python-dotenv
  2. Set VERITIER_WEBHOOK_SECRET in your .env (the vtsec_... value from the dashboard)
  3. python webhook_receiver.py
  4. The server listens on http://localhost:5050/webhooks/veritier

For production:
  - Use HTTPS (required by Veritier for non-localhost URLs)
  - Deploy behind a reverse proxy (nginx, Caddy, etc.)
  - Use a WSGI server (gunicorn, waitress)

Full webhook docs: https://veritier.ai/docs
"""

import hmac
import hashlib
import os
from dotenv import load_dotenv
from flask import Flask, request, abort, jsonify

load_dotenv()

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("VERITIER_WEBHOOK_SECRET", "")

if not WEBHOOK_SECRET:
    print("⚠ Warning: VERITIER_WEBHOOK_SECRET is not set.")
    print("  Configure a webhook at https://veritier.ai/dashboard to get your secret.")


@app.route("/webhooks/veritier", methods=["POST"])
def veritier_webhook():
    """
    Receive and verify a Veritier webhook delivery.

    Security flow:
      1. Read the raw request body BEFORE any JSON parsing
      2. Compute HMAC-SHA256 of the raw bytes using your webhook secret
      3. Compare against the X-Veritier-Signature header (timing-safe)
      4. Only then parse and process the payload
    """
    signature = request.headers.get("X-Veritier-Signature", "")

    if not WEBHOOK_SECRET:
        print("✗ Webhook secret not configured - rejecting request")
        abort(500)

    # ── Step 1: Verify the signature ────────────────────────────────────
    # IMPORTANT: Use request.data (raw bytes), NOT request.get_json()
    # Re-serializing JSON may change whitespace/key order and break the HMAC
    raw_body = request.data

    expected_signature = "vtsec_" + hmac.new(
        key=WEBHOOK_SECRET.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256,
    ).hexdigest()

    # Timing-safe comparison prevents signature oracle attacks
    if not hmac.compare_digest(signature, expected_signature):
        print("✗ Invalid webhook signature - rejecting request")
        abort(401)

    # ── Step 2: Parse and process the payload ───────────────────────────
    payload = request.get_json()

    transaction_id = payload.get("transaction_id", "unknown")
    results = payload.get("results", [])

    print(f"\n{'─' * 50}")
    print(f"✓ Webhook received - Transaction: {transaction_id}")
    print(f"  Claims verified: {len(results)}")

    for res in results:
        verdict = res.get("verdict")
        icon = {True: "✅", False: "❌", None: "❓"}.get(verdict, "❓")
        print(f"  {icon} {res.get('claim')} → {verdict}")

    print(f"{'─' * 50}\n")

    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Veritier Webhook Receiver")
    print("  Listening on http://localhost:5050/webhooks/veritier")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    app.run(host="0.0.0.0", port=5050, debug=True)
