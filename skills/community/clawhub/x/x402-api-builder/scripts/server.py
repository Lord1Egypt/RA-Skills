#!/usr/bin/env python3
"""x402 API template — Northcap (simplified).

⚠️ SECURITY (SkillSpector fix 20/8):
- Purchase only issues keys AFTER ON-CHAIN verification of the txHash
  (PAYMENT_RPC_URL, default: Base mainnet RPC). No verification = no key.
- If the RPC is unreachable, purchases are DENIED (secure-by-default).
TODO: replace YOUR /v1/... endpoints with your own data.
"""
import json, os, hmac, hashlib
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException, Query
import urllib.request

# ⚠️ Replace with YOUR payment wallet (env-overridable, never ship a hardcoded one)
WALLET = os.environ.get("PAYMENT_WALLET", "0x0000000000000000000000000000000000000000")
PRICE_PER_CALL = 0.005
PRICE_PER_MONTH = 25.0
KEYS_FILE = Path(__file__).parent / "api_keys.json"    # gitignore this!

# On-chain verification (Ethereum mainnet RPC as default — no key without confirmed payment)
PAYMENT_RPC_URL = os.environ.get("PAYMENT_RPC_URL", "https://ethereum-rpc.publicnode.com")
PAYMENT_CHAIN_ID = int(os.environ.get("PAYMENT_CHAIN_ID", "1"))
# Chain NAME used for USDC verification (must match a key in USDC_TOKENS below)
PAYMENT_CHAIN = os.environ.get("PAYMENT_CHAIN", "ethereum")

app = FastAPI(title="My x402 API", version="1.0.1")


def load_keys():
    if KEYS_FILE.exists(): return json.loads(KEYS_FILE.read_text())
    return {}


def _rpc_call(chain, method, params):
    """JSON-RPC call against the chain's public RPC. Returns result or None."""
    rpc_map = {
        "ethereum": PAYMENT_RPC_URL if PAYMENT_CHAIN == "ethereum" else "https://ethereum-rpc.publicnode.com",
        "base": "https://mainnet.base.org",
        "bsc": "https://bsc-dataseed.binance.org",
    }
    url = rpc_map.get(chain)
    if not url:
        return None
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            return data.get("result")
    except Exception:
        return None


# USDC token addresses per chain (ETH + Base = 6 decimals, BSC = 18)
USDC_TOKENS = {
    "ethereum": ("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", 6),
    "base":     ("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", 6),
    "bsc":      ("0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d", 18),
}
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


def verify_payment_onchain(tx_hash, chain, wallet):
    """Verify a real USDC Transfer to the wallet. Secure-by-default.

    Checks the token Transfer event in the transaction receipt — NOT the
    native ETH value. Only a valid USDC transfer to WALLET with amount >=
    the requested price counts as payment.
    """
    if chain not in USDC_TOKENS:
        return False, "Unsupported chain for USDC verification"
    token_addr, decimals = USDC_TOKENS[chain]
    receipt = _rpc_call(chain, "eth_getTransactionReceipt", [tx_hash])
    if not receipt:
        return False, "Transaction not found on chain"
    if int(receipt.get("status") or "0x0", 16) != 1:
        return False, "Transaction not confirmed (status != success)"
    logs = receipt.get("logs") or []
    token_l = token_addr.lower()
    wallet_l = wallet.lower()
    for log in logs:
        if (log.get("address") or "").lower() != token_l:
            continue
        topics = log.get("topics") or []
        if not topics or topics[0].lower() != TRANSFER_TOPIC:
            continue
        if len(topics) < 3:
            continue
        to = "0x" + topics[2][-40:].lower()
        if to != wallet_l:
            continue
        try:
            amount_raw = int(log.get("data") or "0x0", 16)
        except Exception:
            continue
        amount_usd = amount_raw / (10 ** decimals)
        # ✅ CRITICAL FIX (20/8): return the ACTUAL transferred amount so the
        # purchase flow can verify it covers the required price. Previously any
        # USDC transfer (even $0.000001) passed as "verified" — underpayment attack.
        return True, amount_usd
    return False, 0.0

@app.get("/.well-known/x402")
@app.get("/x402-manifest")
def manifest():
    return {
        "name": "My API",
        "description": "Describe your service",
        "provider": {"name": "Your name", "wallet": WALLET, "chains": ["eth"]},
        "payment": {"currency": "USDC", "networks": ["eth"],
                    "pricePerCall": PRICE_PER_CALL, "pricePerMonth": PRICE_PER_MONTH,
                    "methods": ["onchain-usdc"]},
        "endpoints": {"signals": {"path": "/v1/signals", "method": "GET", "auth": "api-key"}},
    }


@app.post("/v1/purchase")
def purchase(req: dict):
    tx_hash = (req.get("txHash") or "").strip()
    amount = float(req.get("amountUsd") or 0)
    if not tx_hash.startswith("0x") or len(tx_hash) < 20:
        raise HTTPException(400, "Invalid txHash")
    if amount < PRICE_PER_CALL:
        raise HTTPException(400, f"Minimum ${PRICE_PER_CALL}")
    # 🔒 CRITICAL FIX (20/8): verify the payment ON-CHAIN before issuing a key.
    ok, paid = verify_payment_onchain(tx_hash, PAYMENT_CHAIN, WALLET)
    if not ok:
        raise HTTPException(402, f"Payment could not be verified")
    # ✅ CRITICAL FIX (20/8): the verified on-chain amount must cover the
    # claimed purchase amount — otherwise an attacker could send $0.000001
    # and claim a monthly key (underpayment attack).
    if paid < amount - 1e-9:
        raise HTTPException(402, f"Underpayment: {paid:.6f} USDC verified on-chain, but {amount:.6f} USDC was claimed")
    # ⚠️ Use a REAL secret from env (never a hardcoded default for production)
    key_secret = os.environ.get("KEY_SECRET", "change-me-in-production").encode()
    key = hmac.new(key_secret, tx_hash.encode(), hashlib.sha256).hexdigest()[:24]
    keys = load_keys()
    keys[key] = {"tx": tx_hash, "amount": amount,
                 "kind": "monthly" if amount >= PRICE_PER_MONTH else "per-call",
                 "created": datetime.now(timezone.utc).isoformat(), "calls": 0}
    KEYS_FILE.write_text(json.dumps(keys, indent=2))
    return {"apiKey": key, "kind": "monthly" if amount >= PRICE_PER_MONTH else "per-call",
            "status": "verified"}


def _auth(x_api_key: str):
    keys = load_keys()
    k = keys.get(x_api_key or "")
    if not k: raise HTTPException(401, "Missing/invalid key")
    if k["kind"] == "per-call" and k["calls"] >= 1:
        raise HTTPException(402, "Call usage exhausted — buy more")
    k["calls"] += 1
    KEYS_FILE.write_text(json.dumps(keys, indent=2))
    return k


@app.get("/v1/signals")
def signals(x_api_key: str = Header(None), symbol: str = Query(None)):
    _auth(x_api_key)
    return {"provider": "My API", "symbol": symbol,
            "data": "YOUR DATA HERE"}  # TODO: your data
