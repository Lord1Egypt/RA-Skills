# x402 Lotto

API client for x402.lotto — lottery services via the x402 payment protocol.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/lotteries` | GET | List lotteries |
| `/api/jackpot/:name` | GET | Current jackpot |
| `/api/tickets` | POST | Purchase ticket |
| `/api/tickets/:id` | GET | Ticket status |
| `/api/results/:name` | GET | Draw results |

## Usage

```javascript
import { wrapFetchWithPayment, decryptKey } from '@x402/evm';

const wallet = decryptKey(process.env.KEY);
const fetch = wrapFetchWithPayment(wallet);

const res = await fetch('https://x402.lotto/api/jackpot/eurojackpot');
```

## Payment

Uses x402 protocol — EIP-712 off-chain signing, no gas fees. USDC on Base (8453).

## Install

```bash
clawhub install x402-lotto
```
