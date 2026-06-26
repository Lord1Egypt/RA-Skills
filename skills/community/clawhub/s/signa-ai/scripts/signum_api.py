#!/usr/bin/env python3
"""
Signum API Client — base layer for all Signum skill scripts.
Handles node communication, NQT conversion, and error handling.
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_DOWN

# ── Constants ────────────────────────────────────────────────────────────────
NQT = 100_000_000          # 1 SIGNA = 100,000,000 NQT (Nano-Quant)
FEE_STANDARD  = 2_000_000   # 0.02 SIGNA — standard transaction fee
FEE_MESSAGE   = 5_000_000   # 0.05 SIGNA — minimum for message transactions (node raised minimum)
FEE_ALIAS     = 20_000_000  # 0.2 SIGNA — alias registration fee
FEE_AT        = 2_000_000   # 0.02 SIGNA — minimum fee for AT (smart contract) transactions

def fee_message(message=""):
    """Dynamic message fee: 0.05 SIGNA base + 0.01 per 1KB. Min 0.05 (current node minimum)."""
    msg_bytes = len(message.encode("utf-8")) if message else 0
    chunks = max(1, -(-msg_bytes // 1024))  # ceiling division
    return max(FEE_MESSAGE, chunks * 1_000_000)
DEADLINE      = 1440       # minutes — max transaction validity window
USER_AGENT    = "SignaAI/0.1.0"

EXPLORER_URL = "https://explorer.signum.network"

NODES = {
    "mainnet": [
        "https://europe.signum.network",
        "https://us.signum.network",
        "https://brazil.signum.network",
    ],
    "testnet": [
        "https://europe3.testnet.signum.network",
    ]
}

# ── Client ───────────────────────────────────────────────────────────────────
class SignumAPI:
    def __init__(self, network="testnet"):
        self.network = network
        self.nodes = NODES[network]
        self.active_node = self.nodes[0]

    def _call(self, params, method="GET", retries=2):
        if "secretPhrase" in params:
            return {"error": "Refusing to send secretPhrase to node; local signing is required"}

        url = f"{self.active_node}/api"
        for attempt in range(retries):
            try:
                if method == "GET":
                    query = urllib.parse.urlencode(params)
                    req = urllib.request.Request(
                        f"{url}?{query}",
                        headers={"User-Agent": USER_AGENT}
                    )
                else:
                    data = urllib.parse.urlencode(params).encode()
                    req = urllib.request.Request(
                        url, data=data,
                        headers={"User-Agent": USER_AGENT,
                                 "Content-Type": "application/x-www-form-urlencoded"}
                    )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    result = json.loads(resp.read())
                    if "errorDescription" in result:
                        return {"error": result["errorDescription"], "errorCode": result.get("errorCode")}
                    return result
            except Exception as e:
                if attempt == retries - 1:
                    # Try next node
                    idx = self.nodes.index(self.active_node)
                    if idx + 1 < len(self.nodes):
                        self.active_node = self.nodes[idx + 1]
                        return self._call(params, method, retries=1)
                    return {"error": str(e)}
        return {"error": "All nodes failed"}

    def get(self, request_type, **params):
        params["requestType"] = request_type
        return self._call(params, "GET")

    def post(self, request_type, **params):
        params["requestType"] = request_type
        params["deadline"] = DEADLINE
        # If secretPhrase is present, sign locally and broadcast instead of sending passphrase
        if "secretPhrase" in params:
            return self._sign_and_broadcast(request_type, params)
        return self._call(params, "POST")

    def _sign_and_broadcast(self, request_type, params):
        """Local signing flow — passphrase never leaves this machine."""
        try:
            from signum_crypto import generate_sign_keys, generate_signature, generate_signed_transaction_bytes
        except ImportError as exc:
            return {"error": f"Local signing unavailable: {exc}"}

        passphrase = params.pop("secretPhrase")
        keys = generate_sign_keys(passphrase)
        params["publicKey"] = keys["publicKey"]

        # Get unsigned transaction bytes from node
        result = self._call(params, "POST")
        if "error" in result:
            return result
        unsigned_hex = result.get("unsignedTransactionBytes")
        if not unsigned_hex:
            return result  # Some calls return directly (e.g. broadcastTransaction)

        # Sign locally and broadcast
        signature = generate_signature(unsigned_hex, keys["signPrivateKey"])
        signed_hex = generate_signed_transaction_bytes(unsigned_hex, signature)
        broadcast = self._call({"requestType": "broadcastTransaction",
                                "transactionBytes": signed_hex}, "POST")
        if "error" in broadcast:
            return broadcast
        # Return same shape callers expect
        result.update(broadcast)
        return result

# ── Helpers ──────────────────────────────────────────────────────────────────
def signa(nqt):
    """Convert NQT to SIGNA float."""
    return int(nqt) / NQT if nqt else 0

def nqt(amount_signa):
    """Convert SIGNA to NQT int. Uses Decimal to avoid float precision errors."""
    try:
        amount = Decimal(str(amount_signa))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Invalid SIGNA amount: {amount_signa!r}") from exc
    if amount < 0:
        raise ValueError("SIGNA amount cannot be negative")
    amount = amount.quantize(Decimal("0.00000001"), rounding=ROUND_DOWN)
    return int(amount * NQT)

def ts(timestamp_signum):
    """Convert Signum genesis-relative timestamp to datetime string.
    Signum genesis: 2014-08-11 02:00:00 UTC"""
    genesis = 1407715200  # Unix timestamp of Signum genesis
    if not timestamp_signum:
        return "—"
    try:
        unix = genesis + int(timestamp_signum)
        return datetime.fromtimestamp(unix).strftime("%Y-%m-%d %H:%M")
    except:
        return str(timestamp_signum)

def fmt_address(addr):
    """Ensure address has SIGNA- prefix."""
    if addr and not str(addr).startswith("SIGNA-"):
        return f"SIGNA-{addr}"
    return addr

def ok(result):
    """Check if API result is successful."""
    return result and "error" not in result

# ── Singleton ────────────────────────────────────────────────────────────────
_api_instance = None

def get_api(network=None):
    global _api_instance
    if _api_instance is None or (network and _api_instance.network != network):
        import os
        net = network or os.environ.get("SIGNUM_NETWORK", "testnet")
        _api_instance = SignumAPI(net)
    return _api_instance

if __name__ == "__main__":
    api = get_api("mainnet")
    status = api.get("getBlockchainStatus")
    print(f"Network:  {api.network}")
    print(f"Node:     {api.active_node}")
    print(f"Blocks:   {status.get('numberOfBlocks', '?'):,}")
    print(f"Version:  {status.get('version', '?')}")
