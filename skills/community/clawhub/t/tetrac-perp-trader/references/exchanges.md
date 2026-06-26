# Supported Exchanges

All exchanges are accessed via the TTC Box proxy at `https://ttc.box`. You never call exchange APIs directly.

## Exchange Names (use with `-e` flag)

| Name         | Type         | Passphrase Required | Notes                                      |
|--------------|--------------|---------------------|--------------------------------------------|
| `orderly`    | Futures      | Yes (`what_exchange`, `woofi_pro`, `ttc`, etc.) | BrokerID = passphrase |
| `binance`    | Spot/Futures | No                  |                                            |
| `bybit`      | Spot/Futures | No                  |                                            |
| `okx`        | Spot/Futures | Yes                 |                                            |
| `phemex`     | Futures      | No                  |                                            |
| `bitget`     | Futures      | Yes                 |                                            |
| `blofin`     | Futures      | Yes                 |                                            |
| `kucoin`     | Spot/Futures | Yes                 |                                            |
| `asterdex`   | Futures      | No                  | Requires funded account                    |
| `hyperliquid`| Futures      | No                  |                                            |
| `avr`        | Futures      | No                  | Aggregated virtual router                  |
| `bingx`      | Futures      | No                  |                                            |

## Exchange-Specific Quirks

### Orderly
- `passphrase` = broker ID (e.g. `what_exchange`), not an API passphrase
- `order_id` is returned as an **integer** from the API
- Stop/algo orders use a separate cancel endpoint (handled server-side)
- Symbol format: `NEARUSDT`, `BTCUSDT` (no prefix)
- Tick sizes vary per symbol — always check `market best-bid-ask` before placing

### Market Data Commands (no `-e` required)
These hit TTC Box aggregation endpoints directly:
- `market hybrid-tickers` — cross-exchange tickers, use `--source` to filter by exchange
- `market funding-rates` — funding rates across all exchanges
- `market open-interest` — open interest across all exchanges
- `market volume-snapshot` — 24h volume per exchange
- `market scanner` — technical analysis signal (requires `--symbol`, `--timeframe`)

## Credentials Setup

Credentials are loaded from `.env` in the working directory:

```env
# TTC Box session (written automatically by `register` and `login`)
TTC_AUTH_TOKEN=your_ttc_auth_token
TTC_PUBLIC_KEY=your_ttc_public_key
TTC_EMAIL=your_ttc_email
TTC_PASSKEY=your_generated_passkey
TTC_TOKEN_ISSUED_AT=unix_timestamp
TTC_EXCHANGE=orderly

# Orderly trading credentials
ORDERLY_API_KEY=your_orderly_api_key
ORDERLY_API_SECRET=your_orderly_api_secret
ORDERLY_API_PASSPHRASE=your_broker_id       # e.g. what_exchange, woofi_pro, ttc

# Required for email-registered CLI users (see note below)
ORDERLY_MAIN_WALLET_ADDRESS=your_orderly_wallet_public_key
```

### ORDERLY_MAIN_WALLET_ADDRESS

This is required if you registered your TTC Box account via **email** (not Web3).

- **Web3 users** — your `TTC_PUBLIC_KEY` IS your Orderly wallet, so this is not needed.
- **Email/CLI users** — your `TTC_PUBLIC_KEY` is a random generated key. You must set `ORDERLY_MAIN_WALLET_ADDRESS` to your real Orderly trading wallet public key so the server can derive the correct account credentials.

When set, it is sent as `walletAddress` in every Orderly request. The server uses `credentials.walletAddress || userWalletAddress`, so Web3 users are unaffected.

Or pass per-command:
```
skill-trading order limit --exchange orderly --api-key KEY --api-secret SECRET --passphrase PASS ...
```
