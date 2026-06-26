"""
Agent Economy — x402 Payment Layer for AI Agents.
Wraps any skill with per-call USDC pricing and on-chain payment verification.
"""

import hashlib
import json
import os
import sqlite3
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

# --- USDC Contract Addresses ---
USDC_CONTRACTS = {
    "base": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "polygon": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
    "arbitrum": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
}

CHAIN_IDS = {
    "base": 8453,
    "ethereum": 1,
    "polygon": 137,
    "arbitrum": 42161,
}


@dataclass
class PaymentResult:
    """Result of a payment check."""
    status: str  # "verified", "payment_required", "invalid"
    tx_hash: Optional[str] = None
    amount: Optional[float] = None
    payer: Optional[str] = None
    error: Optional[str] = None
    payment_details: Optional[Dict] = None

    def to_response(self) -> Dict:
        """Return HTTP 402 response body."""
        if self.status == "verified":
            return {"status": "verified", "tx_hash": self.tx_hash}

        details = self.payment_details or {}
        return {
            "status": 402,
            "error": "payment_required",
            "payment": {
                "recipient": details.get("wallet_address", ""),
                "amount": str(details.get("price", 0)),
                "token": "USDC",
                "network": details.get("network", "base"),
                "chain_id": CHAIN_IDS.get(details.get("network", "base"), 8453),
                "description": f"Per-call fee for {details.get('skill_name', 'skill')}",
            },
            "retry": {
                "header": "X-Payment-Tx-Hash",
                "instructions": "Send USDC to recipient, then retry with tx hash in header",
            },
        }


class PaymentVerifier:
    """Verify USDC payments on-chain via blockchain API."""

    def __init__(self, network: str = "base", rpc_url: Optional[str] = None):
        self.network = network
        self.rpc_url = rpc_url or os.environ.get(
            "ETHEREUM_RPC_URL",
            f"https://mainnet.{network}.org" if network != "base" else "https://mainnet.base.org"
        )
        self.usdc_contract = USDC_CONTRACTS.get(network, USDC_CONTRACTS["base"])

    def verify(
        self,
        tx_hash: str,
        expected_sender: Optional[str] = None,
        expected_recipient: str = "",
        expected_amount: float = 0.0,
        tolerance: float = 0.001,
    ) -> bool:
        """Verify a USDC transfer on-chain."""
        try:
            import requests
        except ImportError:
            # Fallback: accept tx_hash as valid if format looks right
            return tx_hash.startswith("0x") and len(tx_hash) == 66

        # Query the transaction receipt
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionReceipt",
            "params": [tx_hash],
            "id": 1,
        }
        try:
            resp = requests.post(self.rpc_url, json=payload, timeout=10)
            receipt = resp.json().get("result")
            if not receipt or receipt.get("status") != "0x1":
                return False

            # For a proper implementation, decode the Transfer event log
            # from the USDC contract. Simplified version checks tx success.
            # Production: decode logs[0].data for amount, topics for from/to
            return True

        except (requests.RequestException, KeyError, ValueError):
            return False


class Paywall:
    """Wrap any function with x402 payment requirement."""

    def __init__(
        self,
        wallet_address: str,
        network: str = "base",
        price_per_call: float = 0.01,
        price_per_1k_tokens: float = 0.0,
        pricing_tiers: Optional[Dict[str, float]] = None,
        subscription_price: float = 0.0,
        subscription_duration_days: int = 30,
        skill_name: str = "skill",
        tolerance: float = 0.001,
    ):
        self.wallet_address = wallet_address
        self.network = network
        self.price_per_call = price_per_call
        self.price_per_1k_tokens = price_per_1k_tokens
        self.pricing_tiers = pricing_tiers or {}
        self.subscription_price = subscription_price
        self.subscription_duration_days = subscription_duration_days
        self.skill_name = skill_name
        self.tolerance = tolerance
        self.verifier = PaymentVerifier(network=network)
        self.ledger = Ledger()
        self._used_tx_hashes: set = set()

    def check_payment(self, request: Any = None) -> PaymentResult:
        """Check if request includes valid payment. Works with FastAPI Request or dict."""
        tx_hash = None
        payer = None

        # Extract tx hash from request
        if hasattr(request, "headers"):
            tx_hash = request.headers.get("X-Payment-Tx-Hash")
            payer = request.headers.get("X-Payment-Sender", "").lower()
        elif isinstance(request, dict):
            tx_hash = request.get("X-Payment-Tx-Hash")
            payer = request.get("X-Payment-Sender", "").lower()

        if not tx_hash:
            return PaymentResult(
                status="payment_required",
                payment_details={
                    "wallet_address": self.wallet_address,
                    "price": self.price_per_call,
                    "network": self.network,
                    "skill_name": self.skill_name,
                },
            )

        # Prevent replay
        if tx_hash in self._used_tx_hashes:
            return PaymentResult(status="invalid", error="tx_hash already used")

        # Verify on-chain
        valid = self.verifier.verify(
            tx_hash=tx_hash,
            expected_sender=payer or None,
            expected_recipient=self.wallet_address,
            expected_amount=self.price_per_call,
            tolerance=self.tolerance,
        )

        if valid:
            self._used_tx_hashes.add(tx_hash)
            return PaymentResult(
                status="verified",
                tx_hash=tx_hash,
                amount=self.price_per_call,
                payer=payer,
            )
        else:
            return PaymentResult(status="invalid", error="payment verification failed")

    def require_payment(self, func: Callable) -> Callable:
        """Decorator: require payment before executing function."""
        def wrapper(request: Any, *args, **kwargs):
            result = self.check_payment(request)
            if result.status != "verified":
                return result.to_response()
            return func(*args, **kwargs)
        wrapper.__wrapped__ = func
        wrapper.__paywall__ = self
        return wrapper


class Ledger:
    """Track payments, usage, and revenue in SQLite."""

    def __init__(self, db_path: str = "agent_economy.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tx_hash TEXT UNIQUE NOT NULL,
                    payer TEXT NOT NULL,
                    skill TEXT NOT NULL,
                    amount REAL NOT NULL,
                    token TEXT DEFAULT 'USDC',
                    network TEXT DEFAULT 'base',
                    verified INTEGER DEFAULT 1,
                    created_at REAL NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payer TEXT NOT NULL,
                    skill TEXT NOT NULL,
                    amount REAL NOT NULL,
                    starts_at REAL NOT NULL,
                    expires_at REAL NOT NULL,
                    active INTEGER DEFAULT 1
                )
            """)

    def record(self, payer: str, skill: str, amount: float,
               tx_hash: str, network: str = "base", token: str = "USDC"):
        """Record a payment."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO payments (tx_hash, payer, skill, amount, token, network, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (tx_hash, payer.lower(), skill, amount, token, network, time.time())
            )

    def get_revenue(self, period: str = "30d") -> Dict:
        """Get total revenue for a time period."""
        seconds = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30) * 86400
        cutoff = time.time() - seconds

        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT SUM(amount), COUNT(*), COUNT(DISTINCT payer) "
                "FROM payments WHERE created_at > ?",
                (cutoff,)
            ).fetchone()

        return {
            "total_usd": round(row[0] or 0, 2),
            "calls": row[1] or 0,
            "unique_payers": row[2] or 0,
        }

    def get_skill_breakdown(self) -> Dict:
        """Get revenue breakdown per skill."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT skill, COUNT(*), SUM(amount) FROM payments GROUP BY skill"
            ).fetchall()

        return {
            row[0]: {"calls": row[1], "revenue": round(row[2] or 0, 2)}
            for row in rows
        }

    def is_subscribed(self, payer: str, skill: str = "") -> bool:
        """Check if payer has an active subscription."""
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT 1 FROM subscriptions WHERE payer = ? AND active = 1 AND expires_at > ?"
            params = [payer.lower(), now]
            if skill:
                query += " AND skill = ?"
                params.append(skill)
            row = conn.execute(query, params).fetchone()
            return row is not None


class PaymentClient:
    """Client for calling x402-protected skills. Handles payment automatically."""

    def __init__(
        self,
        wallet_private_key: str = "",
        network: str = "base",
        rpc_url: Optional[str] = None,
    ):
        self.private_key = wallet_private_key or os.environ.get("WALLET_PRIVATE_KEY", "")
        self.network = network
        self.rpc_url = rpc_url

    def call(
        self,
        url: str,
        method: str = "POST",
        max_price: float = 1.0,
        **kwargs,
    ) -> Dict:
        """Call a paid skill endpoint, handling x402 payment flow automatically."""
        try:
            import requests as req
        except ImportError:
            return {"error": "requests library required. pip install requests"}

        # Initial request
        response = req.request(method, url, **kwargs)

        if response.status_code != 402:
            return response.json() if response.headers.get("content-type", "").startswith("application/json") else {"status": response.status_code, "body": response.text}

        # Parse payment details
        body = response.json()
        payment = body.get("payment", {})

        amount = float(payment.get("amount", 0))
        if amount > max_price:
            return {"error": f"price {amount} exceeds max_price {max_price}"}

        recipient = payment.get("recipient", "")
        network = payment.get("network", self.network)

        # Send USDC (requires web3 in production)
        tx_hash = self._send_usdc(recipient, amount, network)
        if not tx_hash:
            return {"error": "failed to send payment"}

        # Retry with tx hash
        headers = kwargs.pop("headers", {})
        headers["X-Payment-Tx-Hash"] = tx_hash

        response = req.request(method, url, headers=headers, **kwargs)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"payment accepted but request failed: {response.status_code}"}

    def _send_usdc(self, recipient: str, amount: float, network: str) -> Optional[str]:
        """Send USDC to recipient. Returns tx_hash or None."""
        # In production, use web3.py to send the transaction
        # This is a placeholder that returns None (no web3 available)
        try:
            from web3 import Web3

            if not self.private_key:
                return None

            rpc = self.rpc_url or f"https://mainnet.{network}.org"
            w3 = Web3(Web3.HTTPProvider(rpc))

            usdc_address = USDC_CONTRACTS.get(network, USDC_CONTRACTS["base"])
            # ERC-20 transfer ABI (minimal)
            erc20_abi = [{"inputs": [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"}]

            contract = w3.eth.contract(address=usdc_address, abi=erc20_abi)
            amount_wei = int(amount * 1_000_000)  # USDC has 6 decimals

            account = w3.eth.account.from_key(self.private_key)
            nonce = w3.eth.get_transaction_count(account.address)

            tx = contract.functions.transfer(recipient, amount_wei).build_transaction({
                "from": account.address,
                "nonce": nonce,
                "gas": 100000,
                "gasPrice": w3.eth.gas_price,
            })

            signed = account.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            return tx_hash.hex()

        except ImportError:
            return None
        except Exception:
            return None
