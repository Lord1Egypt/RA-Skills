"""Unified tool executor: bridges MCP tool definitions to API calls.

Refactored from tools.py to separate tool registration from execution.
The executor holds the authenticated HTTP client and dispatches tool
calls through the worker pool.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import secrets
import time
import uuid
from typing import Any

import httpx

from oris_mcp.worker_pool import WorkerPool

logger = logging.getLogger("oris.mcp.executor")


class OrisToolExecutor:
    """Authenticated tool executor for the Oris API.

    Registers all tool handlers with the WorkerPool for async dispatch.
    Each handler maps to one or more Oris API endpoints with HMAC-SHA256
    request signing.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        agent_id: str,
        base_url: str = "https://api.useoris.finance",
        worker_pool: WorkerPool | None = None,
    ) -> None:
        self._api_key = api_key
        self._signing_key = hashlib.sha256(api_secret.encode()).hexdigest()
        self._agent_id = agent_id
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(timeout=30.0)
        self._pool = worker_pool or WorkerPool()

        # Register all tool handlers.
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all tool handlers with the worker pool."""
        tools = {
            "oris_pay": self._pay,
            "oris_check_balance": self._check_balance,
            "oris_get_spending": self._get_spending,
            "oris_find_service": self._find_service,
            "oris_approve_pending": self._approve_pending,
            "oris_fiat_onramp": self._fiat_onramp,
            "oris_fiat_offramp": self._fiat_offramp,
            "oris_exchange_rate": self._exchange_rate,
            "oris_cross_chain_quote": self._cross_chain_quote,
            "oris_place_order": self._place_order,
            "oris_get_tier_info": self._get_tier_info,
            "oris_generate_attestation": self._generate_attestation,
            "oris_promotion_status": self._promotion_status,
        }

        for name, handler in tools.items():
            self._pool.register_tool(name, handler)

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool call through the worker pool."""
        return await self._pool.submit(tool_name, arguments)

    @property
    def pool(self) -> WorkerPool:
        """Access the underlying worker pool."""
        return self._pool

    # -----------------------------------------------------------------
    # Tool handlers
    # -----------------------------------------------------------------

    async def _pay(self, args: dict) -> dict:
        return await self._api_call("POST", "/api/v1/oris/payments/send", {
            "agent_id": self._agent_id,
            "counterparty_address": args["to"],
            "amount": args["amount"],
            "stablecoin": args.get("stablecoin", "USDC"),
            "chain": args.get("chain", "base"),
            "purpose": args.get("purpose"),
            "protocol": args.get("protocol", "x402"),
        })

    async def _check_balance(self, args: dict) -> dict:
        result = await self._api_call(
            "GET", f"/api/v1/oris/wallets/agent/{self._agent_id}"
        )
        wallets = result.get("items", [])
        chain_filter = args.get("chain")
        if chain_filter:
            wallets = [w for w in wallets if w.get("chain") == chain_filter]

        # Include tier information in balance response.
        tier_info = {}
        try:
            tier_info = await self._api_call(
                "GET", f"/api/v1/oris/kya/{self._agent_id}/tier-limits"
            )
        except Exception:
            pass

        return {"wallets": wallets, "tier": tier_info}

    async def _get_spending(self, args: dict) -> dict:
        return await self._api_call(
            "GET",
            f"/api/v1/oris/payments/agent/{self._agent_id}",
            params={"page": 1, "per_page": 100},
        )

    async def _find_service(self, args: dict) -> dict:
        params: dict[str, Any] = {"capability": args["capability"]}
        if "max_price" in args:
            params["max_price"] = args["max_price"]
        return await self._api_call(
            "GET", "/api/v1/oris/marketplace/listings", params=params
        )

    async def _approve_pending(self, args: dict) -> dict:
        return await self._api_call(
            "POST", f"/api/v1/oris/payments/approve/{args['payment_id']}"
        )

    async def _fiat_onramp(self, args: dict) -> dict:
        return await self._api_call("POST", "/api/v1/oris/fiat/onramp", {
            "agent_id": self._agent_id,
            "source_currency": args["source_currency"],
            "source_amount": args["amount"],
            "destination_stablecoin": args.get("stablecoin", "USDC"),
            "destination_chain": args.get("chain", "base"),
            "payment_method": args.get("payment_method", "bank_transfer"),
        })

    async def _fiat_offramp(self, args: dict) -> dict:
        return await self._api_call("POST", "/api/v1/oris/fiat/offramp", {
            "agent_id": self._agent_id,
            "source_stablecoin": args.get("stablecoin", "USDC"),
            "source_amount": args["amount"],
            "source_chain": args.get("chain", "base"),
            "destination_currency": args["destination_currency"],
            "destination_account": args["destination_account"],
        })

    async def _exchange_rate(self, args: dict) -> dict:
        return await self._api_call(
            "GET",
            "/api/v1/oris/fiat/exchange-rate",
            params={
                "source": args["source"],
                "destination": args["destination"],
            },
        )

    async def _cross_chain_quote(self, args: dict) -> dict:
        return await self._api_call("POST", "/api/v1/oris/routing/quote", {
            "agent_id": self._agent_id,
            "source_chain": args["source_chain"],
            "destination_chain": args["destination_chain"],
            "stablecoin": args.get("stablecoin", "USDC"),
            "amount": args["amount"],
        })

    async def _place_order(self, args: dict) -> dict:
        return await self._api_call("POST", "/api/v1/oris/marketplace/orders", {
            "buyer_agent_id": self._agent_id,
            "listing_id": args["listing_id"],
            "quantity": args.get("quantity", 1),
            "max_price": args.get("max_price"),
            "escrow_required": args.get("escrow_required", True),
        })

    async def _get_tier_info(self, args: dict) -> dict:
        return await self._api_call(
            "GET", f"/api/v1/oris/kya/{self._agent_id}/tier-limits"
        )

    async def _generate_attestation(self, args: dict) -> dict:
        # Delegate to ZKP tools if available.
        from oris_mcp.zkp_tools import ZKPAttestationService

        zkp = ZKPAttestationService()
        return await zkp.generate_attestation(
            self._agent_id,
            args.get("chain", "base"),
        )

    async def _promotion_status(self, args: dict) -> dict:
        return await self._api_call(
            "GET", f"/api/v1/oris/kya/{self._agent_id}/promotion"
        )

    # -----------------------------------------------------------------
    # HTTP client
    # -----------------------------------------------------------------

    async def _api_call(
        self,
        method: str,
        path: str,
        body: dict | None = None,
        params: dict | None = None,
    ) -> dict:
        """Make an authenticated API call with HMAC-SHA256 signing."""
        full_url = f"{self._base_url}{path}"
        body_bytes = json.dumps(body, default=str).encode() if body else None

        timestamp = str(int(time.time()))
        nonce = secrets.token_urlsafe(24)

        body_hash = hashlib.sha256(body_bytes or b"").hexdigest()
        canonical = f"{timestamp}.{method.upper()}.{path}.{body_hash}"
        signature = hmac.new(
            self._signing_key.encode(),
            canonical.encode(),
            hashlib.sha256,
        ).hexdigest()

        headers = {
            "Authorization": self._api_key,
            "X-Request-Signature": signature,
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Agent-ID": self._agent_id,
            "Content-Type": "application/json",
        }

        if method.upper() in ("POST", "PATCH"):
            headers["Idempotency-Key"] = str(uuid.uuid4())

        response = await self._client.request(
            method=method.upper(),
            url=full_url,
            content=body_bytes,
            params=params,
            headers=headers,
        )
        response.raise_for_status()

        if response.status_code == 204:
            return {"status": "success"}
        return response.json()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
