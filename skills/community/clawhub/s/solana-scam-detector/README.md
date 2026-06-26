# Solana Scam Detector

Read-only scam detection for Solana tokens.

## What It Does

- ✅ Token age check (via Solana RPC)
- ✅ Ticker pattern detection (fake stocks)
- ✅ Mint blacklist check
- ✅ Read-only — no signing required

## Setup

```bash
npm install @solana/web3.js
```

## Usage

```javascript
const { checkTokenSafety, isValidSolanaAddress } = require('./lib/scam_check.js');

// Check token
const result = await checkTokenSafety('TOKEN_MINT', 'SYMBOL');
console.log(result);
```

## Read-Only

| Needed | Not Needed |
|--------|-------------|
| RPC URL | Wallet key |
| | Telegram ID |
| | Trade history |

## Configuration

**Optional:**
- `RPC_URL` — Your RPC (default: public RPC)
- `MIN_TOKEN_AGE_HOURS` — Threshold (default: 4)

## Publish

```bash
clawhub publish
```

## License

MIT