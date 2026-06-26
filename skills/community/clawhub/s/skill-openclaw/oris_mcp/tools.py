"""Oris MCP tool definitions.

13 tools covering the full Oris API surface:
    oris_pay                - Send stablecoin payment (all protocols, 10 chains)
    oris_check_balance      - Query wallet balances + tier info
    oris_get_spending       - Spending summary for a period
    oris_find_service       - Search agent marketplace
    oris_approve_pending    - Approve escalated payment
    oris_fiat_onramp        - Fiat to USDC conversion
    oris_fiat_offramp       - USDC to fiat conversion
    oris_exchange_rate      - Exchange rate query
    oris_cross_chain_quote  - Cross-chain transfer quote
    oris_place_order        - Marketplace order placement
    oris_get_tier_info      - KYA tier limits and usage
    oris_generate_attestation - ZKP KYA attestation proof
    oris_promotion_status   - Tier promotion eligibility
"""

from __future__ import annotations

ALL_CHAINS = ["base", "ethereum", "solana", "polygon", "arbitrum",
              "avalanche", "bsc", "optimism", "celo"]

ALL_PROTOCOLS = ["x402", "direct", "acp", "mcp", "ucp",
                 "visa_tap", "mc_agentic", "solana_pay", "cctp"]

TOOL_DEFINITIONS = [
    {
        "name": "oris_pay",
        "description": (
            "Send a stablecoin payment from an AI agent's wallet. "
            "Supports 10 blockchain networks and 9 payment protocols. "
            "The payment goes through KYA verification, spending policy check, "
            "and compliance screening before execution."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient wallet address (0x... for EVM, base58 for Solana).",
                },
                "amount": {
                    "type": "number",
                    "description": "Payment amount in stablecoin units.",
                },
                "stablecoin": {
                    "type": "string",
                    "enum": ["USDC", "USDT", "EURC"],
                    "default": "USDC",
                    "description": "Stablecoin to send.",
                },
                "chain": {
                    "type": "string",
                    "enum": ALL_CHAINS,
                    "default": "base",
                    "description": "Blockchain network.",
                },
                "purpose": {
                    "type": "string",
                    "description": "Payment purpose (for audit trail).",
                },
                "protocol": {
                    "type": "string",
                    "enum": ALL_PROTOCOLS,
                    "default": "x402",
                    "description": "Payment protocol to use.",
                },
            },
            "required": ["to", "amount"],
        },
    },
    {
        "name": "oris_check_balance",
        "description": (
            "Check the current stablecoin balances of an agent's wallets "
            "across all chains. Includes KYA tier information and spending limits."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "chain": {
                    "type": "string",
                    "enum": ALL_CHAINS,
                    "description": "Filter by specific chain. Omit to see all chains.",
                },
            },
        },
    },
    {
        "name": "oris_get_spending",
        "description": "Get a spending summary for the agent over a specific time period.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "period": {
                    "type": "string",
                    "enum": ["day", "week", "month"],
                    "default": "week",
                    "description": "Time period for the spending summary.",
                },
            },
        },
    },
    {
        "name": "oris_find_service",
        "description": (
            "Search the agent marketplace for services. "
            "Returns available agent capabilities with pricing and reputation scores."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "capability": {
                    "type": "string",
                    "description": "Service capability to search for (e.g., 'translation', 'code_review').",
                },
                "max_price": {
                    "type": "number",
                    "description": "Maximum price per unit in USDC.",
                },
            },
            "required": ["capability"],
        },
    },
    {
        "name": "oris_approve_pending",
        "description": "Approve a pending payment that was escalated for human review.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payment_id": {
                    "type": "string",
                    "description": "UUID of the pending payment to approve.",
                },
            },
            "required": ["payment_id"],
        },
    },
    {
        "name": "oris_fiat_onramp",
        "description": (
            "Convert fiat currency to USDC (on-ramp). Initiates a bank transfer "
            "or card payment to fund the agent's wallet with stablecoins."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_currency": {
                    "type": "string",
                    "description": "Source fiat currency (e.g., 'USD', 'EUR', 'GBP').",
                },
                "amount": {
                    "type": "number",
                    "description": "Amount in source currency to convert.",
                },
                "stablecoin": {
                    "type": "string",
                    "enum": ["USDC", "USDT", "EURC"],
                    "default": "USDC",
                    "description": "Destination stablecoin.",
                },
                "chain": {
                    "type": "string",
                    "enum": ALL_CHAINS,
                    "default": "base",
                    "description": "Destination blockchain.",
                },
                "payment_method": {
                    "type": "string",
                    "enum": ["bank_transfer", "card", "wire"],
                    "default": "bank_transfer",
                    "description": "Payment method for the fiat transfer.",
                },
            },
            "required": ["source_currency", "amount"],
        },
    },
    {
        "name": "oris_fiat_offramp",
        "description": (
            "Convert USDC to fiat currency (off-ramp). Initiates a withdrawal "
            "from the agent's stablecoin balance to a bank account."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount of stablecoin to convert.",
                },
                "stablecoin": {
                    "type": "string",
                    "enum": ["USDC", "USDT", "EURC"],
                    "default": "USDC",
                    "description": "Source stablecoin.",
                },
                "chain": {
                    "type": "string",
                    "enum": ALL_CHAINS,
                    "default": "base",
                    "description": "Source blockchain.",
                },
                "destination_currency": {
                    "type": "string",
                    "description": "Destination fiat currency (e.g., 'USD', 'EUR').",
                },
                "destination_account": {
                    "type": "string",
                    "description": "Bank account identifier for the withdrawal.",
                },
            },
            "required": ["amount", "destination_currency", "destination_account"],
        },
    },
    {
        "name": "oris_exchange_rate",
        "description": "Get the current exchange rate between a fiat currency and a stablecoin.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Source currency (e.g., 'USD', 'USDC').",
                },
                "destination": {
                    "type": "string",
                    "description": "Destination currency (e.g., 'USDC', 'EUR').",
                },
            },
            "required": ["source", "destination"],
        },
    },
    {
        "name": "oris_cross_chain_quote",
        "description": (
            "Get a quote for a cross-chain stablecoin transfer. Returns the optimal "
            "route, fees, and estimated completion time."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_chain": {
                    "type": "string",
                    "enum": ALL_CHAINS,
                    "description": "Source blockchain.",
                },
                "destination_chain": {
                    "type": "string",
                    "enum": ALL_CHAINS,
                    "description": "Destination blockchain.",
                },
                "stablecoin": {
                    "type": "string",
                    "enum": ["USDC", "USDT", "EURC"],
                    "default": "USDC",
                    "description": "Stablecoin to transfer.",
                },
                "amount": {
                    "type": "number",
                    "description": "Amount to transfer.",
                },
            },
            "required": ["source_chain", "destination_chain", "amount"],
        },
    },
    {
        "name": "oris_place_order",
        "description": (
            "Place an order on the agent marketplace. Creates an escrow-backed "
            "purchase of an agent service listing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "listing_id": {
                    "type": "string",
                    "description": "UUID of the marketplace listing to order.",
                },
                "quantity": {
                    "type": "integer",
                    "default": 1,
                    "description": "Number of units to order.",
                },
                "max_price": {
                    "type": "number",
                    "description": "Maximum total price in USDC.",
                },
                "escrow_required": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to use escrow for the order.",
                },
            },
            "required": ["listing_id"],
        },
    },
    {
        "name": "oris_get_tier_info",
        "description": (
            "Get the agent's current KYA tier, spending limits, and usage. "
            "Shows the maximum per-transaction, daily, and monthly limits "
            "based on the agent's verification level."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "oris_generate_attestation",
        "description": (
            "Generate a zero-knowledge proof (ZKP) attestation of the agent's KYA status. "
            "The attestation proves the agent holds a valid KYA credential without "
            "revealing private details. Uses Halo2 PLONK proofs suitable for "
            "on-chain verification."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "chain": {
                    "type": "string",
                    "enum": ALL_CHAINS,
                    "default": "base",
                    "description": "Target blockchain for the on-chain attestation.",
                },
            },
        },
    },
    {
        "name": "oris_promotion_status",
        "description": (
            "Check the agent's eligibility for KYA tier promotion. "
            "Returns the current level, promotion requirements, and progress "
            "toward the next tier."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]
