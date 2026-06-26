# Xerolite REST API Reference

This document describes the Xerolite API endpoints used by the skill CLI (`scripts/xerolite.mjs`).

## Base Configuration

- **Base URL**: Optional. Set `XEROLITE_API_URL` to the Xerolite host (e.g. `http://your-xerolite-host`). If not set, the CLI uses `http://localhost`. No `/api` suffix; the script appends the path.
- **Authentication (required)**: Agentic endpoints require header `X-Agentic-Api-Key`. Set `XEROLITE_AGENTIC_API_KEY` or pass `--api-key` in the CLI.

## Endpoints

### Place order

- **Path**: `POST /api/agentic/order/place-order`
- **Used by**: `node xerolite.mjs order place ...`
- **Header**: `X-Agentic-Api-Key: <your-api-key>`

Request body (required: `action`, `qty`, `symbol`; optional with defaults: `currency`, `asset_class`, `exch`):

```json
{
  "name": "Agent",
  "action": "BUY",
  "qty": "10",
  "symbol": "AAPL",
  "currency": "USD",
  "asset_class": "STOCK",
  "exch": "SMART"
}
```

### Contract search

- **Path**: `POST /api/agentic/contract/search`
- **Used by**: `node xerolite.mjs contract search ...`
- **Header**: `X-Agentic-Api-Key: <your-api-key>`

Request body (required: `symbol`; optional with defaults: `currency`, `xeroAssetClass`; script sends fixed `brokerName: "IBKR"`):

```json
{
  "brokerName": "IBKR",
  "symbol": "AAPL",
  "currency": "USD",
  "xeroAssetClass": "STOCK"
}
```

### Portfolio (positions)

- **Path**: `POST /api/agentic/portfolio`
- **Used by**: `node xerolite.mjs portfolio get ...`
- **Header**: `X-Agentic-Api-Key: <your-api-key>`

No request parameters. The CLI sends an empty JSON object `{}` as the body for consistency with other POST calls; the server does not require a body.

Response: JSON array of portfolio rows (broker, ticker, position size, market value, PnL fields, etc.—see server `PortfolioDTO`).

### Defaults (CLI)

When flags are omitted, the script uses: `currency=USD`, `asset-class=STOCK`, `exch=SMART`.

### Response Format

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400  | Bad Request |
| 401  | Unauthorized |
| 404  | Not Found |
| 500  | Server Error |
