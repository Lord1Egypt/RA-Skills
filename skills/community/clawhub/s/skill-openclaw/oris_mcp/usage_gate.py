"""Fail-closed usage gate for OpenClaw MCP tool calls.

Checks the tenant's current transaction count against their plan limit
before allowing financial tool execution. If the API is unreachable and
the local cache has expired, the gate BLOCKS the request. Autonomous agents
must not be allowed to transact without verified usage limits.

Warning injection: when the tenant is between 80 and 99 transactions on the
free tier, a usage warning dict is attached to the response for the LLM to
surface to the user.
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger("oris.mcp.usage_gate")

FINANCIAL_TOOLS = {
    "oris_pay",
    "oris_fiat_onramp",
    "oris_fiat_offramp",
    "oris_place_order",
    "oris_cross_chain_quote",
    "oris_approve_pending",
}


class UsageGate:
    """Pre-execution gate that enforces OpenClaw usage limits.

    FAIL-CLOSED: if the usage API is unreachable and the local cache
    has expired, financial tool calls are rejected.
    """

    def __init__(self, executor: Any) -> None:
        self._executor = executor
        self._cached_usage: dict | None = None
        self._cache_ts: float = 0
        self._cache_ttl: float = 10.0  # 10 second local cache

    async def check(self, tool_name: str) -> tuple[dict | None, dict | None]:
        """Return (block_error, usage_snapshot).

        block_error is a dict if the tool call should be rejected, None otherwise.
        usage_snapshot is the fetched usage data (used by get_warning).
        Returning the snapshot eliminates race conditions between check and warning.
        """
        if tool_name not in FINANCIAL_TOOLS:
            return None, None

        usage = await self._get_usage()

        # FAIL-CLOSED: if usage data is unavailable, block financial operations.
        if usage is None:
            return {
                "code": "USAGE_SERVICE_UNAVAILABLE",
                "message": "Cannot verify usage limits. Try again in a few seconds.",
            }, None

        tier = usage.get("tier", "")
        if not tier.startswith("openclaw_"):
            return None, usage  # Non-OpenClaw plans use existing billing.

        tx_used = usage.get("transactions_used", 0)
        tx_limit = usage.get("transactions_included")
        has_billing = usage.get("has_billing", False)

        # Free tier with limit reached and no payment method on file.
        if tx_limit is not None and tx_used >= tx_limit and not has_billing:
            return {
                "code": "FREE_TIER_LIMIT_REACHED",
                "message": (
                    f"Monthly free limit reached ({tx_limit} transactions). "
                    f"Your agent cannot make payments until billing is added. "
                    f"Takes 2 minutes: useoris.finance/billing"
                ),
                "upgrade_url": "https://useoris.finance/billing",
                "resets_at": usage.get("resets_at", ""),
            }, usage

        return None, usage

    @staticmethod
    def get_warning(usage: dict | None) -> dict | None:
        """Return a usage warning dict if the tenant is between 80-99 TX on free tier.

        Accepts the usage snapshot returned by check() to avoid stale cache reads.
        """
        if usage is None:
            return None

        tier = usage.get("tier", "")
        if not tier.startswith("openclaw_free"):
            return None

        tx_used = usage.get("transactions_used", 0)
        tx_limit = usage.get("transactions_included", 100)

        if tx_limit and 80 <= tx_used < tx_limit:
            return {
                "transactions_used": tx_used,
                "transactions_included": tx_limit,
                "tier": "free",
                "warning": (
                    f"{tx_used} of {tx_limit} free transactions used this month. "
                    f"Add billing before you hit the limit to avoid interruption: "
                    f"useoris.finance/billing"
                ),
            }

        return None

    async def _get_usage(self) -> dict | None:
        """Fetch usage from the API with a 10-second local cache.

        If the cache is valid, returns cached data. If the cache has expired,
        a fresh fetch is required. Stale cache is never trusted.
        """
        now = time.time()
        if self._cached_usage and (now - self._cache_ts) < self._cache_ttl:
            return self._cached_usage

        try:
            result = await self._executor._api_call(
                "GET", "/api/v1/oris/billing/mcp-usage"
            )
            self._cached_usage = result
            self._cache_ts = now
            return result
        except Exception:
            # Cache expired and API unreachable. Clear stale data.
            self._cached_usage = None
            self._cache_ts = 0
            return None
