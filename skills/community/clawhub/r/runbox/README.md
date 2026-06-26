# RunBox

> Pay-per-use code execution for AI agents. No account. No API key. No human in the loop.

RunBox is an HTTP API that lets AI agents rent isolated code execution sandboxes using micropayments over the [x402 protocol](https://x402.org) on Stellar. An agent hits an endpoint, gets a `402 Payment Required` back with a price and a Stellar address, pays **0.01 USDC**, and immediately gets a live sandbox to run code in.

**The payment is the authentication.**

**Live server:** `http://46.101.74.170:4001`

---

## Try It Right Now

```bash
# See what RunBox can do
curl http://46.101.74.170:4001/api/exec/.well-known/runbox.json

# Hit the payment wall (returns 402 with price + Stellar address)
curl -X POST http://46.101.74.170:4001/api/exec/rent
```

---

## How the Payment Flow Works

```
Agent → POST /api/exec/rent
         ← 402  { payTo: "G...", amount: "0.01", asset: "USDC" }

Agent pays 0.01 USDC to that Stellar address → gets tx hash

Agent → POST /api/exec/rent
         X-Payment-Hash: <tx_hash>
         ← 200  { session_token, expires_at }

Agent → POST /api/exec/run
         Authorization: Bearer <session_token>
         { "language": "python", "code": "print('hello')" }
         ← 200  { stdout, stderr, exit_code, execution_ms }
```

Payment is verified on-chain via Stellar Horizon. No intermediary. No API key. ~5 second settlement.

---

## Use With Any AI Agent

### Option 1 — Give your agent a system prompt

Paste this into your agent's system prompt (Claude, GPT-4, etc.):

```
You have access to RunBox, a remote code execution API.
Endpoint: http://46.101.74.170:4001

To run code:
1. POST /api/exec/rent → you'll get 402 with { payTo, amount, asset }
2. Pay 0.01 USDC to the Stellar address using your STELLAR_SECRET_KEY
3. Retry POST /api/exec/rent with header X-Payment-Hash: <tx_hash>
4. You receive a session_token (valid 5 min)
5. POST /api/exec/run with Authorization: Bearer <session_token>
   Body: { "language": "python", "code": "..." }

Use RunBox whenever the user asks you to run, execute, or compute code.
Pay autonomously — the user has already funded your Stellar wallet.
```

### Option 2 — Use the skill script (OpenClaw, Claude Desktop, any tool-calling agent)

```bash
# Install dependencies
pip install stellar-sdk requests

# Set your Stellar wallet secret key (only thing you need)
export STELLAR_SECRET_KEY=S...

# Run code — pays automatically, no other config needed
python3 skill/scripts/run.py --language python --code "print(sum(range(100)))"

# Reuse the session (no second payment)
python3 skill/scripts/run.py --language python --code "import math; print(math.pi)" --session-token eyJ...

# Full JSON output
python3 skill/scripts/run.py --language javascript --code "console.log(2**32)" --json

# Use testnet (free USDC from Friendbot)
python3 skill/scripts/run.py --language python --code "print('test')" --testnet
```

The script handles the full x402 flow: 402 → Stellar payment → session token → execute.

### Option 3 — OpenClaw

```bash
clawhub install runbox
```

Then configure once in `openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "runbox": {
        "enabled": true,
        "env": {
          "STELLAR_SECRET_KEY": "S...",
          "STELLAR_NETWORK": "mainnet"
        }
      }
    }
  }
}
```

---

## Getting a Stellar Wallet

**Testnet (free — for testing):**
1. Go to [Stellar Laboratory](https://laboratory.stellar.org/#account-creator?network=test) → Generate Keypair
2. Fund with Friendbot (free XLM)
3. Get free testnet USDC at [ultrastellar.com/faucet](https://ultrastellar.com/faucet)

**Mainnet (real USDC, ~$0.01 per run):**
1. Generate a keypair or use any Stellar wallet (Lobstr, Solar)
2. Send USDC to your address from Coinbase/Binance/Kraken — select **Stellar network**
3. Keep ~1 XLM in the wallet for transaction fees

---

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/exec/.well-known/runbox.json` | — | Machine-readable capabilities & pricing |
| `POST` | `/api/exec/rent` | — | Request a session. Returns `402`. Retry with `X-Payment-Hash` after paying. |
| `POST` | `/api/exec/run` | `Bearer <token>` | Execute code in your session |
| `POST` | `/api/exec/extend` | `Bearer <token>` | Pay to extend session time |
| `GET` | `/api/exec/status/:id` | — | Check session time remaining |

---

## Supported Languages

Python · Node.js · JavaScript · Bash · Go · Rust · Ruby · PHP · Perl · Lua · Java · C · C++ · TypeScript · R

Each run executes in a fresh, **network-isolated** Docker container.

---

## Pricing

| | |
|---|---|
| Price | **0.01 USDC per session** |
| Duration | 5 minutes |
| Multiple runs | Free within one session |
| Protocol | [x402](https://x402.org) — HTTP 402 |
| Settlement | ~5 seconds on Stellar |

---

## Self-Hosting

```bash
git clone https://github.com/daraijaola/Runbox.git
cd Runbox
cp .env.example .env   # fill in STELLAR_RECEIVE_ADDRESS and SESSION_JWT_SECRET
pnpm install
pnpm --filter @workspace/api-server run build
pnpm --filter @workspace/api-server run start
```

**Environment variables:**

| Variable | Required | Description |
|----------|----------|-------------|
| `PORT` | yes | Port to listen on |
| `STELLAR_RECEIVE_ADDRESS` | yes | Your Stellar wallet that receives USDC (G...) |
| `SESSION_JWT_SECRET` | yes | Random string for signing session JWTs |
| `STELLAR_NETWORK` | no | `mainnet` (default) or `testnet` |
| `RUNBOX_PRICE` | no | USDC per session (default: `0.01`) |
| `RUNBOX_DEFAULT_MINUTES` | no | Session length in minutes (default: `5`) |

**Generate a receiving wallet:**
```bash
node -e "const {Keypair}=require('@stellar/stellar-sdk'); const k=Keypair.random(); console.log('Address:', k.publicKey()); console.log('Secret:', k.secret())"
```

---

## Architecture

```
┌──────────────┐     HTTP x402      ┌────────────────────┐
│   AI Agent   │ ──────────────────▶│  RunBox API        │
│              │ ◀──────────────────│  Express + TS      │
└──────────────┘                    └─────────┬──────────┘
       │                                      │
       │  0.01 USDC on Stellar                │  verify on Horizon
       ▼                                      ▼
┌──────────────┐                    ┌────────────────────┐
│ Stellar Net  │                    │  Docker Sandbox    │
│ testnet/main │                    │  network-isolated  │
└──────────────┘                    └────────────────────┘
```

---

## Repository Layout

```
artifacts/api-server/
  src/routes/exec.ts      x402 payment gating + session + execution
  src/lib/payment.ts      On-chain USDC verification via Stellar Horizon
  src/lib/sessions.ts     JWT session management
  src/lib/sandbox.ts      Docker execution

skill/
  SKILL.md                Agent skill definition (works with any framework)
  scripts/run.py          Autonomous x402 payment + execution script
  requirements.txt        Python dependencies

demo/
  telegram_agent.py       Live Telegram demo bot (@Runbox1_bot)
  demo_agent.py           CLI demo of the full x402 flow
```

---

## Live Demo

Send any code task to **[@Runbox1_bot](https://t.me/Runbox1_bot)** on Telegram. The agent:
1. Uses Claude to generate the code
2. Pays 0.01 USDC autonomously on Stellar
3. Executes the code in Docker
4. Returns the result with a Stellar Explorer link

---

Built for [Stellar Hacks: Agents](https://dorahacks.io/hackathon/stellar-hacks-agents).

MIT License
