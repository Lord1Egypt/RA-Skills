#!/usr/bin/env python3
"""
Training Lab over x402 — fine-tune a model with nothing but a wallet.

Flow:
  1. GET  /training/x402/catalog                 → base models, GPUs, prices (no auth)
  2. POST /training/x402/runs  (signed by owner)  → 402 + quote for one training block
  3. POST /training/x402/runs  (X-Payment)       → 202 { quote_id, status_url, claim_token, run_id? }
  4. GET  /training/x402/orders/<quote_id>       → status (Authorization: Bearer <claim_token>)

The paying wallet must OWN an APPROVED dataset (buy one with POST /datasets/x402/synth,
or upload one with a wallet-signed /training/datasets/presign, then approve it).

Usage:
  python train_x402.py catalog
  python train_x402.py run --dataset-id <id> --base-model qwen2.5-0.5b-instruct \
      --gpu-plan-id <id> --hours 1 [--network base|robinhood|solana] [--yes]
  python train_x402.py status --quote-id <id> --claim-token <token>
  python train_x402.py resume --quote-id <id>   (lost response: resend the SAME payment)

Env: EVM (base, robinhood): PRIVATE_KEY + WALLET_ADDRESS.
     Solana: SOLANA_SECRET_KEY (SOLANA_WALLET_ADDRESS optional; derived from the key).
Training is paid on the networks in `catalog.networks` (base, robinhood, solana).
COMPUTE_MAX_SPEND_USD caps one payment (default 500). Credentials are read only
from explicit environment variables; nothing is auto-loaded.
"""

import argparse
import base64
import math
import json
import os
import re
import sys
import time
from typing import Optional

import requests

from wallet_signing import create_compute_auth_headers, load_payment_signer, load_wallet_address

BASE_URL = os.getenv("COMPUTE_API_BASE", "https://compute.x402layer.cc")
MAX_SPEND_USD = float(os.getenv("COMPUTE_MAX_SPEND_USD", "500"))
STABLECOIN = {"base": "USDC", "robinhood": "USDG", "solana": "USDC"}


def catalog() -> dict:
    r = requests.get(f"{BASE_URL}/training/x402/catalog", timeout=30, allow_redirects=False)
    if r.status_code != 200:
        return {"error": f"catalog returned {r.status_code}", "response": r.text[:500]}
    return r.json()


def _owner_wallet(network: str) -> str:
    if network == "solana":
        from solana_signing import load_solana_wallet_address
        return load_solana_wallet_address()
    return load_wallet_address(required=True)


PENDING_DIR = os.path.expanduser(os.getenv("SGL_TRAIN_PENDING_DIR", "~/.sgl-train/pending"))


UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


def _pending_path(quote_id: str, suffix: str = ".json") -> str:
    """The saved-payment path for a quote. quote_id comes from the server, so it must be
    a canonical UUID: nothing else may name a file (no ../, no absolute paths)."""
    if not isinstance(quote_id, str) or not UUID_RE.fullmatch(quote_id):
        raise ValueError(f"invalid quote_id {quote_id!r}")
    return os.path.join(PENDING_DIR, quote_id + suffix)


def _write_durable(path: str, data: dict) -> None:
    """Owner-only, atomic (temp + rename) and fsynced, directory included: it must
    survive a crash, because it is written BEFORE the payment is sent."""
    tmp = path + ".tmp"
    fd = _open_private(tmp)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    _fsync_dir(os.path.dirname(path))


def _fsync_dir(path: str) -> None:
    dfd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)


def _makedirs_durable(path: str) -> None:
    """Create the directory chain (0700) and fsync each new entry's parent, so a
    first-run power loss after paying cannot lose the whole recovery directory."""
    path = os.path.abspath(path)
    missing = []
    while not os.path.isdir(path):
        missing.append(path)
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    for d in reversed(missing):
        os.mkdir(d, 0o700)
        _fsync_dir(os.path.dirname(d))
        _fsync_dir(d)


def _open_private(path: str):
    """Create/replace an owner-only file, refusing to follow a symlink."""
    return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), 0o600)


def _save_pending(quote_id: str, body: dict, x_payment: str) -> str:
    """Store the signed payment (owner-only file) so a lost response can be resent as-is."""
    path = _pending_path(quote_id)
    _makedirs_durable(PENDING_DIR)
    _write_durable(path, {"body": body, "x_payment": x_payment})
    return path


def _save_receipt(pending: str, out: dict) -> None:
    """Write the paid answer next to the saved payment (owner-only, atomic rename)."""
    if not out.get("claim_token"):
        return  # a replayed answer: keep the first receipt, if any
    _write_durable(pending[:-len(".json")] + ".receipt.json", out)


def _authorization_dead(path: str) -> bool:
    """True once the saved authorization's validBefore + 5 min has passed: it can no
    longer settle anywhere, and the server's replay lock has been released."""
    try:
        with open(path) as f:
            x_payment = json.load(f)["x_payment"]
        payload = json.loads(base64.b64decode(x_payment + "=" * (-len(x_payment) % 4)))
        if payload.get("payload", {}).get("transaction"):
            # Solana: never inferred locally. A stalled cluster can keep a blockhash valid
            # longer than any wall-clock guess; only the server's answer is final.
            return False
        valid_before = int(payload["payload"]["authorization"]["validBefore"])
    except Exception:
        return False  # unknown: assume it can still settle
    return time.time() > valid_before + 300


def _solana_conclusive_refusal(path: str, out: dict) -> bool:
    """A Solana 409 that is a decision, not 'still in flight'."""
    if out.get("code") == "settlement_pending":
        return False
    msg = str(out.get("error") or "").lower()
    if "already being processed" in msg:
        return False
    try:
        with open(path) as f:
            x_payment = json.load(f)["x_payment"]
        payload = json.loads(base64.b64decode(x_payment + "=" * (-len(x_payment) % 4)))
    except Exception:
        return False
    if not payload.get("payload", {}).get("transaction"):
        return False
    return any(k in msg for k in ("quote has expired", "no longer payable", "inconsistent"))


def _send_payment(body: dict, x_payment: str, attempts: int = 3):
    """POST the paid leg; on a transport error resend the SAME payment. None = no answer."""
    # No auth headers here: the payment authenticates the payer, and the auth nonce
    # was consumed by the quote.
    for n in range(attempts):
        try:
            return requests.post(f"{BASE_URL}/training/x402/runs", json=body,
                                 headers={"X-Payment": x_payment}, timeout=180, allow_redirects=False)
        except requests.RequestException:
            time.sleep(5 * (n + 1))
    return None


def run(dataset_id: str, base_model: str, gpu_plan_id: str, hours: int,
        network: str = "base", recipe: Optional[dict] = None, skip_confirm: bool = False) -> dict:
    owner = _owner_wallet(network)
    body = {
        "owner_wallet": owner,
        "dataset_id": dataset_id,
        "base_model": base_model,
        "gpu_plan_id": gpu_plan_id,
        "budget_hours": hours,
        "network": network,
    }
    if recipe:
        body["recipe"] = recipe

    # Step 1: quote, SIGNED by the owner wallet (the quote binds owner_wallet, so the
    # server requires proof of control). The signature covers the exact body bytes, so
    # send that string. It is an EVM wallet signature, so it uses the EVM auth scheme
    # ("base") whichever EVM network pays.
    body_json = json.dumps(body, separators=(",", ":"))
    try:
        auth_headers = create_compute_auth_headers("POST", "/training/x402/runs", body_json,
                                                   chain="solana" if network == "solana" else "base")
    except Exception as exc:
        return {"error": f"Failed to sign the quote request: {exc}"}
    q = requests.post(f"{BASE_URL}/training/x402/runs", data=body_json,
                      headers={"Content-Type": "application/json", **auth_headers}, timeout=60, allow_redirects=False)
    if q.status_code != 402:
        return {"error": f"expected a 402 quote, got {q.status_code}", "response": q.text[:800]}
    challenge = q.json()
    info = challenge.get("singularity", {})
    option = next((a for a in challenge.get("accepts", []) if a.get("network") == network), None)
    if not option:
        return {"error": f"no payment option for network {network}", "accepts": challenge.get("accepts")}
    # The cap is checked against the amount that will actually be SIGNED (atomic
    # units, 6 decimals for USDC and USDG), never the display price alone.
    raw_amount = str(option.get("maxAmountRequired", ""))
    if not raw_amount.isdigit() or int(raw_amount) <= 0:
        return {"error": f"Malformed payment amount in the quote: {raw_amount!r}. Nothing was signed."}
    amount = int(raw_amount)
    cost = amount / 1_000_000
    try:
        shown = float(info.get("price_usd"))
    except (TypeError, ValueError):
        shown = float("nan")
    if not math.isfinite(shown) or abs(shown - cost) > 0.000001:
        return {"error": f"The quote is inconsistent (price ${info.get('price_usd')} vs signed amount ${cost:.6f}). Nothing was signed."}
    if not UUID_RE.fullmatch(str(info.get("quote_id") or "")):
        return {"error": f"Malformed quote_id in the quote: {info.get('quote_id')!r}. Nothing was signed."}
    if not math.isfinite(MAX_SPEND_USD) or cost > MAX_SPEND_USD:
        return {"error": f"Cost ${cost:.4f} exceeds max spend ${MAX_SPEND_USD:.2f}. Set COMPUTE_MAX_SPEND_USD to override."}

    print("\n--- Training run quote ---")
    print(f"  Model:    {info.get('base_model')}")
    print(f"  GPU:      {info.get('gpu')}  x {info.get('billed_hours')}h (prepaid block, no refund for finishing early)")
    print(f"  Dataset:  {dataset_id}")
    print(f"  Cost:     ${cost:.4f} {STABLECOIN.get(network, 'USDC')} on {network}")
    print(f"  Pay to:   {option['payTo']}")
    print(f"  Expires:  {info.get('quote_expires_at')}")
    if not skip_confirm:
        if input("\nPay and start training? [y/N] ").strip().lower() not in ("y", "yes"):
            return {"error": "Payment cancelled by user"}

    # Step 2: sign EXACTLY the quoted amount and pay with the same body + quote_id.
    if network == "solana":
        # A signed transaction whose recent blockhash expires in ~1-2 minutes.
        from solana_signing import create_solana_xpayment_from_accept, ensure_solana_destination_ready
        ensure_solana_destination_ready(option)   # same setup the Solana provision/extend flows do
        x_payment = create_solana_xpayment_from_accept(option)
    else:
        signer = load_payment_signer()
        x_payment = signer.create_x402_payment_header(pay_to=option["payTo"], amount=amount, network=network)

    # Save the exact signed payment BEFORE sending it. If the response is lost, the
    # only safe retry is this same payment (the server recognises it and never
    # charges twice). A new quote would be a new authorization: a second charge.
    quote_id = info.get("quote_id")
    pending = _save_pending(quote_id, {**body, "quote_id": quote_id}, x_payment)
    print(f"\n  Quote ID: {quote_id}  (signed payment saved to {pending})")
    paid = _send_payment({**body, "quote_id": quote_id}, x_payment)
    return _handle_paid(paid, quote_id, pending)


def _handle_paid(paid, quote_id: str, pending: str) -> dict:
    resume = f"python train_x402.py resume --quote-id {quote_id}"
    if paid is None or paid.status_code >= 500:
        # No answer, or a server error AFTER the payment was sent: the money MAY
        # have moved. The only safe next step is resending this same payment.
        print("\nNo clear answer from the server. The payment MAY have gone through. DO NOT pay again.")
        print(f"Resend the SAME payment safely: {resume}")
        return {"error": "payment outcome unknown", "quote_id": quote_id,
                "http_status": None if paid is None else paid.status_code,
                "payment_accepted": True, "resume": resume}
    out = {}
    try:
        out = paid.json()
    except Exception:
        out = {"raw": paid.text[:800]}
    # Any answer carrying the one-time claim token (202, 409 settlement_pending,
    # 200 credited_not_started) is saved BEFORE anything is printed.
    try:
        _save_receipt(pending, out)
    except Exception as exc:  # never lose the one-time token to a disk error
        if out.get("claim_token"):
            print(f"\n!! Could not save the receipt ({exc}). WRITE THIS CLAIM TOKEN DOWN NOW: {out['claim_token']}")
            out["receipt_save_error"] = str(exc)
    if paid.status_code == 409 and out.get("code") == "settlement_pending":
        print("\nPayment submitted; its outcome is not confirmed yet. DO NOT pay again.")
        print(f"Poll the status URL with your claim token, or resend the same payment: {resume}")
        out["payment_accepted"] = True  # NOT a failure: never retry with a new payment
        return out
    if paid.status_code == 200 and out.get("code") == "credited_not_started":
        print("\nPaid, but the GPU did not start. Your payment becomes credits on this wallet's account.")
        print("Check `refund` with the status command: once it is 'returned' or 'not_charged', start a run with a")
        print("wallet-signed POST /training/runs. While it says returning/unknown, wait. Do not pay again.")
        out["payment_accepted"] = True
        return out
    if paid.status_code == 409 and _solana_conclusive_refusal(pending, out):
        # The server re-checks for a paid order before any of these refusals, so on Solana
        # "quote expired / no longer payable / inconsistent" means this payment was not
        # taken for this order.
        return {"error": f"payment returned 409", "response": out, "saved_payment": pending, "check": resume}
    if paid.status_code == 409 and not _authorization_dead(pending):
        # A 409 can mean another attempt with this same payment is still in flight
        # (the replay lock). Until the signed authorization has expired it may still
        # settle, so keep it and never treat this as "nothing was charged".
        print("\nThis payment is still being processed or its outcome is not known yet. DO NOT pay again.")
        print(f"Try again in a minute with the SAME payment: {resume}")
        return {"error": out.get("error") or "payment in progress", "quote_id": quote_id,
                "payment_accepted": True, "resume": resume, "response": out}
    if paid.status_code != 202:
        # Training refused this payment. A payment this order already took is always
        # recognised first and answered with the order's outcome, so a refusal here
        # means training did not charge it. The saved payment is kept anyway (never
        # deleted): `resume` re-asks the server at any time and never charges twice.
        return {"error": f"payment returned {paid.status_code}", "response": out,
                "saved_payment": pending, "check": resume}

    # Persist the receipt (claim token) BEFORE printing it: a crash or a broken
    # stdout must not lose the only handle to a paid order.
    out["payment_accepted"] = True
    if out.get("run_id"):
        print("\n✅ Training started")
        print(f"   Run:          {out.get('run_id')}")
    else:
        print("\n✅ Payment accepted; the run is being set up. Poll the status URL, do NOT pay again.")
    print(f"   Quote:        {out.get('quote_id')}")
    if out.get("claim_token"):
        print(f"   Claim token:  {out.get('claim_token')}  (shown once, store it)")
        print(f"   Status:       python train_x402.py status --quote-id {out.get('quote_id')} --claim-token <token>")
    else:
        # A replayed answer carries no claim token (it is shown only once).
        print(f"   Status:       {resume}  (resends the same payment; never charges twice)")
        print("                 or a wallet-signed GET /training/runs once the run exists")
    return out


def resume(quote_id: str) -> dict:
    """Resend the exact saved payment for a quote. The server never charges it twice."""
    try:
        path = _pending_path(quote_id)
    except ValueError as exc:
        return {"error": str(exc)}
    if not os.path.exists(path):
        return {"error": f"no saved payment for quote {quote_id} (nothing to resend)"}
    with open(path) as f:
        saved = json.load(f)
    out = _handle_paid(_send_payment(saved["body"], saved["x_payment"]), quote_id, path)
    receipt = path[:-len(".json")] + ".receipt.json"
    if os.path.exists(receipt):
        with open(receipt) as f:
            out["first_receipt"] = json.load(f)  # holds the claim token for status
    return out


def status(quote_id: str, claim_token: str) -> dict:
    r = requests.get(
        f"{BASE_URL}/training/x402/orders/{quote_id}",
        headers={"Authorization": f"Bearer {claim_token}"},
        timeout=30,
        allow_redirects=False,
    )
    try:
        return r.json()
    except Exception:
        return {"error": f"status returned {r.status_code}", "response": r.text[:500]}


def main() -> None:
    global MAX_SPEND_USD
    p = argparse.ArgumentParser(description="Training Lab over x402")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("catalog", help="List base models, GPUs and prices")
    r = sub.add_parser("run", help="Quote, pay and start a training run")
    r.add_argument("--dataset-id", required=True)
    r.add_argument("--base-model", required=True)
    r.add_argument("--gpu-plan-id", required=True)
    r.add_argument("--hours", type=int, default=1)
    r.add_argument("--network", default="base", choices=["base", "robinhood", "solana"])
    r.add_argument("--recipe", help="JSON recipe, e.g. '{\"epochs\":2,\"seed\":7}'")
    r.add_argument("--max-spend", type=float)
    r.add_argument("--yes", action="store_true", help="Skip the confirmation prompt")
    s = sub.add_parser("status", help="Check a paid order")
    s.add_argument("--quote-id", required=True)
    s.add_argument("--claim-token", required=True)
    rs = sub.add_parser("resume", help="Resend the SAME saved payment after a lost response (never charges twice)")
    rs.add_argument("--quote-id", required=True)
    a = p.parse_args()
    if a.cmd == "catalog":
        out = catalog()
    elif a.cmd == "run":
        if a.max_spend is not None:
            if not math.isfinite(a.max_spend) or a.max_spend < 0:
                p.error("--max-spend must be a finite number >= 0")
            MAX_SPEND_USD = a.max_spend
        recipe = json.loads(a.recipe) if a.recipe else None
        out = run(a.dataset_id, a.base_model, a.gpu_plan_id, a.hours, a.network, recipe, a.yes)
    elif a.cmd == "resume":
        out = resume(a.quote_id)
    else:
        out = status(a.quote_id, a.claim_token)
    print(json.dumps(out, indent=2))
    # A paid/pending order is never a failure, even when the body carries an
    # `error` message: exiting non-zero would invite automation to pay again.
    if isinstance(out, dict) and out.get("error") and not out.get("payment_accepted"):
        sys.exit(1)


if __name__ == "__main__":
    main()
