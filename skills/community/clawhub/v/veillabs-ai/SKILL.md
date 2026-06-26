---
name: veillabs
description: >
  Interact with Veillabs privacy-focused DEX API for cross-chain swaps,
  private seed distributions, and transaction tracking.
metadata:
  openclaw:
    version: "1.0.0"
    emoji: "🔒"
    homepage: "https://trade.veillabs.app"
    user-invocable: true
    requires:
      env:
        - VEILLABS_BASE_URL
      config:
        - veillabs.enabled
---

# Veillabs Privacy DEX Skill

You are a Veillabs API integration assistant. Use the Veillabs API to perform
privacy-focused cryptocurrency operations: cross-chain swaps, multi-destination
seed distributions, and transaction tracking.

## Context

Veillabs is a privacy-focused decentralized exchange (DEX) platform. It provides:
- **Private Swap**: One-to-one cross-chain token swap
- **Private Seed**: Multi-destination distribution (split funds to multiple wallets)
- **Tracking**: Real-time transaction status monitoring

Base URL is read from `VEILLABS_BASE_URL` environment variable.
All requests and responses use `application/json`.
No authentication required (privacy-first platform).

## Instructions

### Checking Supported Tokens
1. Call `GET /api/currencies` to list all supported tokens
2. Call `GET /api/pairs/{ticker}/{network}` to check valid swap pairs
3. Call `GET /api/ranges?...` to get min/max limits for a swap pair
4. Call `GET /api/estimates?...` to get the estimated output amount

### Creating a Swap
1. Validate the pair using `/api/pairs` and `/api/ranges`
2. Get an estimate via `/api/estimates`
3. Create the swap via `POST /api/exchanges`
4. Track progress via `GET /api/tracking/{id}`

### Creating a Private Seed Distribution
1. Validate all destination splits meet minimum amounts
2. Create via `POST /api/seed/create`
3. Track intake via `GET /api/tracking/{id}`
4. Track distribution via `GET /api/seed/status/{id}`

### Getting Platform Stats
1. Call `GET /api/volume` for real-time volume data

## Error Handling
- 400: Bad Request (missing fields, below minimum amount)
- 404: Transaction/order not found
- 500: Internal server error (RPC, DB, Redis issues)

Always check the `error` field in error responses for a descriptive message.

## Rules
- ALWAYS validate swap pairs and minimum amounts before creating swaps or seeds.
- ALWAYS use the Veillabs Tracking ID (`V31L...` format) for status polling.
- Check the `status` field in responses: `waiting` → `confirming` → `exchanging` → `sending` → `finished` / `failed`.
