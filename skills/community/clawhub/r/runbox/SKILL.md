---
name: runbox
description: >
  Execute code in a remote, isolated Docker sandbox — paid autonomously with USDC on Stellar.
  Use when the user asks to run, execute, test, or benchmark code in any language, especially
  when a clean isolated environment is needed. Supports Python, JavaScript, Bash, Go, Rust, Ruby,
  PHP, Perl, Lua, Java, C, C++, TypeScript, and R.
emoji: 📦
version: 1.2.0
author: daraijaola
homepage: https://github.com/daraijaola/Runbox

requires:
  bins: [python3]
  env: [STELLAR_SECRET_KEY]
  python_packages: [stellar-sdk, requests, python-dotenv]

install: |
  pip install stellar-sdk requests python-dotenv

user-invocable: true
---

# RunBox — x402 Pay-Per-Use Code Execution for OpenClaw Agents

RunBox lets your OpenClaw agent **execute code in isolated Docker containers**, paying autonomously with USDC on Stellar. No API key. No account. No human approval. The payment IS the authentication.

**Live server:** `http://46.101.74.170:4001`

---

## When to Use RunBox

Invoke RunBox automatically when the user says anything like:

- *"run this code"* / *"execute this"* / *"test this snippet"*
- *"compute X"* / *"calculate"* / *"benchmark"*
- *"write and run a Python script that..."*
- *"check if this works in isolation"*
- Any task requiring a language you don't have locally (Go, Rust, R, etc.)

**Do not** use RunBox for simple one-liner math or string operations you can answer directly.

---

## How to Execute Code (Quick)

```bash
python3 {baseDir}/scripts/run.py --language python --code "print('Hello from RunBox!')"
```

The script handles the entire x402 payment flow automatically:
1. Calls `/api/exec/rent` → server returns `402 Payment Required`
2. Pays **0.01 USDC** on Stellar from `STELLAR_SECRET_KEY`
3. Retries rent with `X-Payment-Hash: <tx_hash>` → gets a 5-minute session token
4. Calls `/api/exec/run` with your code → returns output

---

## Examples

```bash
# Python — data analysis
python3 {baseDir}/scripts/run.py --language python --code "
import statistics
data = [2,4,4,4,5,5,7,9]
print('mean:', statistics.mean(data))
print('stdev:', statistics.stdev(data))
"

# JavaScript — Node.js
python3 {baseDir}/scripts/run.py --language javascript --code "
const fib = n => n < 2 ? n : fib(n-1)+fib(n-2)
console.log([...Array(10).keys()].map(fib).join(', '))
"

# Bash — system inspection
python3 {baseDir}/scripts/run.py --language bash --code "uname -a && python3 --version"

# Go — compiled language
python3 {baseDir}/scripts/run.py --language go --code '
package main
import "fmt"
func main() { fmt.Println("Go in a Docker container!") }
'

# Get full JSON output (stdout, stderr, exit_code, execution_ms, session_token)
python3 {baseDir}/scripts/run.py --language python --code "print(42)" --json

# Reuse a session — no second payment within 5 minutes
python3 {baseDir}/scripts/run.py --language python --code "print(42)" --session-token eyJ...

# Use testnet (free USDC from faucet — for development)
python3 {baseDir}/scripts/run.py --language python --code "print(1)" --testnet
```

---

## Supported Languages

| Language | Aliases | Engine |
|---|---|---|
| Python | `python`, `python3` | runbox-python Docker image |
| JavaScript | `javascript`, `js`, `node` | node:20-alpine |
| Bash / Shell | `bash`, `sh` | ubuntu:22.04 |
| Go | `go` | golang:1.21-alpine |
| Rust | `rust` | rust:1.73-slim |
| Ruby | `ruby` | ruby:3.2-alpine |
| PHP | `php` | php:8.2-cli-alpine |
| Perl | `perl` | perl:5.38 |
| Lua | `lua` | nickblah/lua:5.4 |
| Java | `java` | openjdk:21-slim |
| C / C++ | `c`, `cpp` | gcc:13 |
| TypeScript | `typescript`, `ts` | node:20-alpine + ts-node |
| R | `r` | r-base:4.3.0 |

---

## Session Reuse (Run Multiple Times Without Re-paying)

A session is valid for **5 minutes**. Run multiple executions for free within that window:

```bash
# First call — pays 0.01 USDC and returns session info via --json
python3 {baseDir}/scripts/run.py --language python --code "x = 42" --json
# Captures: SESSION_TOKEN from JSON output → session_token field

# Second, third call — reuse the session at no cost
python3 {baseDir}/scripts/run.py --language python --code "print(x*2)" --session-token $SESSION_TOKEN
```

---

## Configuration

| Variable | Required | Default | Notes |
|---|---|---|---|
| `STELLAR_SECRET_KEY` | **YES** | — | Starts with `S`. Your Stellar wallet secret. |
| `RUNBOX_ENDPOINT` | no | `http://46.101.74.170:4001` | Override to point to testnet or self-hosted |
| `STELLAR_NETWORK` | no | `mainnet` | Set to `testnet` for free test payments |

---

## Getting Your Stellar Wallet (First Time Setup)

### Testnet — Free, for development
```bash
# 1. Generate a keypair
python3 -c "from stellar_sdk import Keypair; k=Keypair.random(); print('Public:',k.public_key); print('Secret:',k.secret)"

# 2. Fund with free XLM
curl "https://friendbot.stellar.org?addr=YOUR_PUBLIC_KEY"

# 3. Get free testnet USDC at: https://ultrastellar.com/faucet
#    Or via xlm402.com testnet USDC faucet

# 4. Add to OpenClaw
openclaw set-env STELLAR_SECRET_KEY=YOUR_SECRET_KEY
openclaw set-env STELLAR_NETWORK=testnet
```

### Mainnet — Real USDC (~$0.01 per run)
1. Generate keypair (same command above)
2. Send 0.10+ USDC to your public key via any Stellar wallet (Lobstr, Solar, Freighter)
3. `openclaw set-env STELLAR_SECRET_KEY=YOUR_SECRET_KEY`

---

## x402 Payment Flow (What Happens Behind the Scenes)

```
OpenClaw Agent                    RunBox Server              Stellar Network
      │                                │                           │
      │  POST /api/exec/rent           │                           │
      │ ─────────────────────────────▶ │                           │
      │                                │                           │
      │  ◀── 402 Payment Required ──── │                           │
      │       X-Payment-Required: ...  │                           │
      │                                │                           │
      │  ── pay 0.01 USDC ────────────────────────────────────▶   │
      │  ← tx_hash ─────────────────────────────────────────────── │
      │                                │                           │
      │  POST /api/exec/rent           │                           │
      │  X-Payment-Hash: <tx_hash>     │                           │
      │ ─────────────────────────────▶ │                           │
      │                                │  verify on Horizon ──▶    │
      │  ◀── 200 session_token ─────── │                           │
      │                                │                           │
      │  POST /api/exec/run            │                           │
      │  Authorization: Bearer <tok>   │                           │
      │  { language, code }            │                           │
      │ ─────────────────────────────▶ │                           │
      │                                │  docker run --network none│
      │  ◀── { stdout, stderr, ... } ── │                           │
```

---

## Self-Hosting RunBox

```bash
git clone https://github.com/daraijaola/Runbox
cd Runbox
pnpm install && pnpm build
cp .env.example artifacts/api-server/.env
# Edit .env: set STELLAR_RECEIVE_ADDRESS, SESSION_JWT_SECRET
pm2 start artifacts/api-server/ecosystem.config.cjs
```

Install the skill pointing to your own server:
```bash
clawhub install runbox
openclaw set-env RUNBOX_ENDPOINT=http://YOUR_SERVER:4001
```

---

## Security Notes

- Code runs in Docker containers with **no network access** (`--network none`)
- Memory limited to **256–512 MB** per run
- CPU limited to **1–1.5 cores** per run
- Execution timeout: **60 seconds**
- Each session is scoped to a single JWT — sessions cannot be shared between agents

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `STELLAR_SECRET_KEY not set` | Missing env var | `openclaw set-env STELLAR_SECRET_KEY=S...` |
| `Account not found` | Account not created on Stellar | Fund via friendbot (testnet) or send XLM (mainnet) |
| `Insufficient payment` | Not enough USDC | Add USDC to your Stellar wallet |
| `Transaction already used` | Replay attack prevention | Each tx hash can only buy one session |
| `Session not found or expired` | Session > 5 min old | Pay for a new session |
| `Unsupported language` | Wrong language name | Use exact names from the table above |
