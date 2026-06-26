#!/usr/bin/env python3
"""
RunBox skill script — autonomous code execution via x402 on Stellar.

Handles the full x402 payment flow:
  1. Call /exec/rent → receive 402 with payment requirements
  2. Sign + submit USDC payment on Stellar
  3. Retry /exec/rent with X-PAYMENT header → receive session token
  4. Call /exec/run with session token → receive execution result
"""

import argparse
import json
import os
import sys
import base64
import time

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests stellar-sdk", file=sys.stderr)
    sys.exit(1)

try:
    from stellar_sdk import Keypair, Network, Server, TransactionBuilder, Asset
    from stellar_sdk.exceptions import NotFoundError
except ImportError:
    print("Error: 'stellar-sdk' not installed. Run: pip install stellar-sdk", file=sys.stderr)
    sys.exit(1)


STELLAR_SECRET_KEY = os.environ.get("STELLAR_SECRET_KEY", "")
RUNBOX_ENDPOINT    = os.environ.get("RUNBOX_ENDPOINT", "http://46.101.74.170:4001").rstrip("/")
STELLAR_NETWORK    = os.environ.get("STELLAR_NETWORK", "mainnet")

HORIZON_URLS = {
    "testnet": "https://horizon-testnet.stellar.org",
    "mainnet": "https://horizon.stellar.org",
}

NETWORK_PASSPHRASES = {
    "testnet": Network.TESTNET_NETWORK_PASSPHRASE,
    "mainnet": Network.PUBLIC_NETWORK_PASSPHRASE,
}

# USDC asset on Stellar
USDC_ISSUERS = {
    "testnet": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
    "mainnet": "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
}


def check_env():
    if not STELLAR_SECRET_KEY:
        print("Error: STELLAR_SECRET_KEY is not set.", file=sys.stderr)
        print("  Set it as an environment variable: export STELLAR_SECRET_KEY=S...", file=sys.stderr)
        print("  Get a testnet key free: https://laboratory.stellar.org/#account-creator?network=test", file=sys.stderr)
        sys.exit(1)


def parse_x402_payment_required(response):
    """Parse the x402 402 response — handles both header-based and body-based formats."""
    body = {}
    try:
        body = response.json()
    except Exception:
        pass

    # Standard x402 header format (base64-encoded JSON with accepts[])
    payment_required_header = response.headers.get("payment-required", "")
    if payment_required_header:
        try:
            decoded = base64.b64decode(payment_required_header).decode()
            return json.loads(decoded)
        except Exception:
            pass

    # Our RunBox body format: {"payment": {"payTo", "amount", "asset", ...}}
    if "payment" in body and "accepts" not in body:
        p = body["payment"]
        body["accepts"] = [{
            "payTo": p.get("payTo", ""),
            "amount": p.get("amount", "0.01"),
            "network": p.get("network", "stellar:testnet"),
            "asset": p.get("asset", ""),
        }]

    return body


def submit_stellar_payment(pay_to: str, amount_usdc: str, memo: str = "") -> dict:
    """Submit USDC payment on Stellar and return the signed payment payload for x402."""
    horizon_url = HORIZON_URLS.get(STELLAR_NETWORK, HORIZON_URLS["testnet"])
    network_passphrase = NETWORK_PASSPHRASES.get(STELLAR_NETWORK, NETWORK_PASSPHRASES["testnet"])
    usdc_issuer = USDC_ISSUERS.get(STELLAR_NETWORK, USDC_ISSUERS["testnet"])

    keypair = Keypair.from_secret(STELLAR_SECRET_KEY)
    server = Server(horizon_url)

    try:
        account = server.load_account(keypair.public_key)
    except NotFoundError:
        print(f"Error: Stellar account {keypair.public_key} not found or unfunded.", file=sys.stderr)
        sys.exit(1)

    usdc = Asset("USDC", usdc_issuer)

    builder = TransactionBuilder(
        source_account=account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )

    builder.append_payment_op(destination=pay_to, asset=usdc, amount=amount_usdc)

    if memo:
        builder.add_text_memo(memo[:28])

    builder.set_timeout(30)
    tx = builder.build()
    tx.sign(keypair)

    response = server.submit_transaction(tx)
    return {
        "hash": response["hash"],
        "ledger": response.get("ledger"),
    }


def rent_session(language: str) -> dict:
    """Perform the full x402 rent flow and return a session."""
    rent_url = f"{RUNBOX_ENDPOINT}/api/exec/rent"

    print("Requesting RunBox session...", file=sys.stderr)
    r = requests.post(rent_url, json={"language": language}, timeout=15)

    if r.status_code == 200:
        return r.json()

    if r.status_code != 402:
        print(f"Unexpected response {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)

    payment_info = parse_x402_payment_required(r)
    accepts = payment_info.get("accepts", [])

    if not accepts:
        print("No payment options in 402 response", file=sys.stderr)
        sys.exit(1)

    offer = accepts[0]
    pay_to = offer.get("payTo", offer.get("destination", ""))
    amount = offer.get("price", offer.get("amount", "0.01"))
    network = offer.get("network", "stellar:testnet")

    print(f"Payment required: {amount} USDC on {network}", file=sys.stderr)
    print(f"  → Paying to: {pay_to}", file=sys.stderr)

    tx = submit_stellar_payment(pay_to, str(amount), memo="runbox")

    print(f"  ✓ Payment submitted: {tx['hash']}", file=sys.stderr)

    # Retry with payment proof
    # For x402, the client would normally include a signed auth entry.
    # Here we include the tx hash as proof for the server to verify.
    retry = requests.post(
        rent_url,
        json={"language": language},
        headers={"X-Payment-Hash": tx["hash"], "X-Payment-Network": network},
        timeout=15,
    )

    if retry.status_code == 200:
        return retry.json()

    print(f"Session creation failed after payment: {retry.status_code} {retry.text}", file=sys.stderr)
    sys.exit(1)


def run_code(session_token: str, language: str, code: str) -> dict:
    """Execute code using a valid session token."""
    r = requests.post(
        f"{RUNBOX_ENDPOINT}/api/exec/run",
        json={"language": language, "code": code},
        headers={"Authorization": f"Bearer {session_token}"},
        timeout=60,
    )

    if r.status_code == 401:
        print("Session expired or invalid.", file=sys.stderr)
        sys.exit(1)

    if not r.ok:
        print(f"Execution error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)

    return r.json()


def main():
    global RUNBOX_ENDPOINT, STELLAR_NETWORK

    parser = argparse.ArgumentParser(description="RunBox — remote code execution via x402 on Stellar")
    parser.add_argument("--language", required=True, help="Language: python, javascript, bash, go, rust, etc.")
    parser.add_argument("--code", required=True, help="Code to execute")
    parser.add_argument("--json", action="store_true", help="Output full JSON result instead of just stdout")
    parser.add_argument("--session-token", default="", help="Reuse an existing session token (skip payment)")
    parser.add_argument("--endpoint", default="", help="Override RunBox server URL")
    parser.add_argument("--testnet", action="store_true", help="Use Stellar testnet instead of mainnet")
    args = parser.parse_args()

    if args.endpoint:
        RUNBOX_ENDPOINT = args.endpoint.rstrip("/")
    if args.testnet:
        STELLAR_NETWORK = "testnet"

    check_env()

    if args.session_token:
        token = args.session_token
        print(f"  ↩  Reusing session token", file=sys.stderr)
    else:
        session = rent_session(args.language)
        token = session["session_token"]
        expires_at = session.get("expires_at", "")
        tx_hash = session.get("tx_hash", "")
        print(f"  ✓ Session active until {expires_at}", file=sys.stderr)
        if tx_hash:
            network = "testnet" if STELLAR_NETWORK == "testnet" else "mainnet"
            print(f"  🔗 Stellar tx: https://stellar.expert/explorer/{network}/tx/{tx_hash}", file=sys.stderr)
        print(f"  💾 Reuse this session: --session-token {token}", file=sys.stderr)

    result = run_code(token, args.language, args.code)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("stdout"):
            print(result["stdout"], end="")
        if result.get("stderr"):
            print(result["stderr"], end="", file=sys.stderr)
        sys.exit(result.get("exit_code", 0))


if __name__ == "__main__":
    main()
