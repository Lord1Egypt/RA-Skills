---
name: web3-dapp-builder
description: >
  Industry-standard Web3 DApp architecture skill (2026). Covers the full modern stack:
  Account Abstraction (ERC-4337/EIP-7702), embedded wallets (Privy/Dynamic), Permit2 gasless
  approvals, on-chain indexing (Ponder/Envio/The Graph), Foundry + Vitest testing, multicall
  batching, RPC health failover, encrypted vault key management, event-driven SSE architecture,
  BullMQ strategy orchestration. Supports EVM (Viem/Wagmi) + Solana + multi-chain.
license: Apache-2.0
metadata:
  version: "1.0.1"
  tags: [web3, dapp, fullstack, nextjs, fastify, viem, wagmi, account-abstraction, foundry, solana]
  categories: [dapp-development, web3-architecture, fullstack]
  compatibility: [openclaw, gemini-cli]
---

# Web3 DApp Builder v1.0.0

Industry-optimal patterns for production Web3 DApps. Combines battle-tested production patterns
with 2026 best practices: Account Abstraction, embedded wallets, Permit2, on-chain indexing,
invariant testing, and gasless UX.

## When To Use

- Scaffold / architect a Web3 DApp (full-stack)
- Implement wallet connection, signing, Account Abstraction
- Build DEX/swap/trading/DeFi features
- Design strategy orchestration with task queues
- Implement real-time event systems (SSE/WebSocket)
- Build encrypted vault / credential management
- Create on-chain data pipelines (indexer, scanner, listener)
- Design testing strategy (contract fuzz + app integration)

---

## I. 2026 Optimal Tech Stack

### Frontend
```
Framework:       Next.js 15+ App Router + React 19
State:           Zustand (client) + TanStack Query v5 (server cache)
Wallet:          Wagmi v2 + Viem (EVM) | @solana/web3.js (Solana)
Onboarding:      Privy or Dynamic (embedded wallets + social login)
                 OR RainbowKit/ConnectKit (wallet modal only)
Account Abstraction: ERC-4337 SDK (ZeroDev / Alchemy AA / Biconomy)
Local DB:        Dexie (IndexedDB) for offline/frontend-mode
Styling:         Tailwind CSS 4 + Framer Motion
Testing:         Vitest + Playwright (E2E)
```

### Backend
```
Framework:       Fastify (TypeScript ESM) or tRPC + Next.js API routes
Database:        PostgreSQL + Drizzle ORM
Queue:           BullMQ + Redis (strategy workers)
Auth:            JWT rotation + SIWE + Google OAuth + passkeys
Chain:           Viem (EVM) + @solana/web3.js
Events:          EventBus (ring buffer + JSONL) → SSE push
Encryption:      AES-256-GCM + PBKDF2 vault
Indexing:        Ponder (self-hosted) or Envio or The Graph
```

### Smart Contracts
```
Language:        Solidity 0.8.25+ (EVM) | Anchor/Rust (Solana)
Framework:       Foundry (test/deploy/verify)
Testing:         Unit → Fuzz → Invariant → Mainnet Fork
Static Analysis: Slither + custom detectors
Deployment:      Foundry script + CREATE2 (deterministic addresses)
Upgradeability:  UUPS proxy (prefer) or Transparent proxy (standard)
```

### Decision Matrix — When to use what

| Need                               | Choice                        | Reason                          |
| ---------------------------------- | ----------------------------- | ------------------------------- |
| Wallet connection UI only          | RainbowKit / ConnectKit       | Lightest, prettiest             |
| Social login + new user onboarding | Privy / Dynamic               | Embedded wallets, zero friction |
| Gasless UX                         | ERC-4337 Paymaster            | Users never see gas             |
| Batch approve+swap+stake           | Multicall / ERC-4337 bundling | 1 click, 1 tx                   |
| Self-hosted indexing               | Ponder                        | Full control, TypeScript        |
| Decentralized indexing             | The Graph                     | Censorship resistance           |
| Real-time streaming                | Goldsky / Envio               | Sub-second latency              |

---

## II. Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│  FRONTEND (Next.js + React)                         │
│  ┌──────────┐ ┌───────────┐ ┌─────────────────────┐ │
│  │ Wagmi/   │ │ TanStack  │ │ Zustand Store       │ │
│  │ Viem     │ │ Query     │ │ (auth, settings,    │ │
│  │ Hooks    │ │ Cache     │ │  execution mode)    │ │
│  └────┬─────┘ └─────┬─────┘ └──────────┬──────────┘ │
│       │             │                   │            │
│  ┌────▼─────────────▼───────────────────▼──────────┐ │
│  │  Execution Mode Router (frontend|backend|hybrid) │ │
│  └────┬────────────────────────────────────────────┘ │
└───────┼──────────────────────────────────────────────┘
        │ REST / SSE / WebSocket
┌───────▼──────────────────────────────────────────────┐
│  BACKEND (Fastify)                                   │
│  ┌──────────┐ ┌───────────┐ ┌────────────┐          │
│  │ Auth +   │ │ Services  │ │ EventBus   │          │
│  │ RBAC     │ │ (trade,   │ │ (dual-write│          │
│  │ Vault    │ │  strat,   │ │  ring+JSONL│          │
│  │          │ │  signal)  │ │  → SSE)    │          │
│  └────┬─────┘ └─────┬─────┘ └──────┬─────┘          │
│  ┌────▼─────────────▼──────────────▼──────────────┐  │
│  │  PostgreSQL + Drizzle   │  BullMQ Workers      │  │
│  └────┬────────────────────┴──────────────────────┘  │
└───────┼──────────────────────────────────────────────┘
        │ RPC (health-managed)
┌───────▼──────────────────────────────────────────────┐
│  BLOCKCHAIN                                          │
│  EVM (Ethereum, BSC, Base, Arbitrum, Polygon)        │
│  Solana | Sui | other L1/L2                          │
└──────────────────────────────────────────────────────┘
```

### Read/Write Separation (Critical)
- **Read path**: Indexer → PostgreSQL → API → frontend (fast, cached, no RPC)
- **Write path**: Frontend → sign → backend → broadcast → RPC → chain (gas, latency)
- Never use RPC for reads that can be served by indexed data

---

## III. Account Abstraction (ERC-4337 / EIP-7702)

The #1 UX improvement for 2026. Every consumer-facing DApp should implement AA.

### Core Components
```
Smart Account:  User's programmable contract wallet (session keys, social recovery)
EntryPoint:     Singleton contract managing UserOperation verification + execution
Bundler:        Service that collects UserOps and submits them on-chain
Paymaster:      Contract that sponsors gas or accepts ERC-20 fee payment
```

### Implementation Pattern
```typescript
// Using ZeroDev / Alchemy AA / Biconomy SDK
import { createKernelAccount, createKernelAccountClient } from '@zerodev/sdk'

const kernelAccount = await createKernelAccount(publicClient, {
  plugins: { sudo: ecdsaValidator },
  entryPoint: ENTRYPOINT_ADDRESS_V07,
})

const kernelClient = createKernelAccountClient({
  account: kernelAccount,
  chain, bundlerTransport: http(bundlerUrl),
  middleware: { sponsorUserOperation: pimlicoBundler.sponsorUserOperation },
})

// User does approve+swap in ONE click, gas paid by paymaster
await kernelClient.sendUserOperation({
  userOperation: { callData: encodeFunctionData({ abi, functionName: 'multicall', args: [...] }) },
})
```

### EIP-7702 (EOA → Smart Account bridge)
```
Existing EOA users can temporarily gain AA features (batching, paymaster)
without deploying new contract or moving funds.
Use when: migrating existing user base to AA gradually.
```

### Session Keys (Gaming / High-frequency)
```
Pre-approve specific actions for a time window:
- "Allow this game contract to call move() for 24 hours, max 0.1 ETH"
- User signs once → session key auto-signs subsequent txs
- Revocable at any time
```

---

## IV. Wallet & Onboarding Strategy

### Tier 1: Embedded Wallets (best for new users)
```typescript
// Privy — social login creates wallet automatically
import { PrivyProvider, usePrivy } from '@privy-io/react-auth'

<PrivyProvider appId={PRIVY_APP_ID} config={{
  loginMethods: ['email', 'google', 'apple', 'twitter', 'passkey'],
  embeddedWallets: { createOnLogin: 'users-without-wallets' },
  appearance: { theme: 'dark' },
}}>
  <App />
</PrivyProvider>

// User signs in with email → gets wallet → never sees "MetaMask" popup
```

### Tier 2: Wallet Connection (crypto-native users)
```typescript
// Wagmi + RainbowKit / ConnectKit
import { WagmiProvider, createConfig, http } from 'wagmi'
import { mainnet, base, bsc, arbitrum } from 'wagmi/chains'
import { RainbowKitProvider, connectorsForWallets } from '@rainbow-me/rainbowkit'

const config = createConfig({
  chains: [mainnet, base, bsc, arbitrum],
  transports: { [mainnet.id]: http(), [base.id]: http(), ... },
})
```

### Tier 3: SIWE (Sign-In With Ethereum)
```
For apps needing persistent auth (not just wallet connection):
1. Backend generates nonce → frontend creates SIWE message → wallet signs
2. Backend verifies signature → issues JWT + refresh token
3. Session stored in DB with userId ↔ walletAddress binding
```

### Decision: Privy vs Dynamic vs RainbowKit

|                       | Privy         | Dynamic    | RainbowKit    |
| --------------------- | ------------- | ---------- | ------------- |
| Social login          | ✅ Best        | ✅ Great    | ❌ No          |
| Embedded wallet       | ✅             | ✅          | ❌             |
| Multi-chain (EVM+Sol) | ✅             | ✅ Best     | EVM only      |
| Customization         | Medium        | High       | High          |
| Cost                  | Paid          | Paid       | Free          |
| Best for              | Consumer apps | Enterprise | Crypto-native |

---

## V. Gasless Patterns & Transaction Optimization

### Permit2 (Universal Gasless Approvals)
```typescript
// Instead of: approve(spender, amount) → swap()   [2 transactions]
// Now:        sign permit → swap(permit, signature) [1 transaction]

// Using Uniswap Permit2 contract (universal, any ERC-20)
const permit2Address = '0x000000000022D473030F116dDEE9F6B43aC78BA3'

// 1. User signs EIP-712 message off-chain (no gas)
const permitData = {
  details: { token, amount, expiration, nonce },
  spender: routerAddress,
  sigDeadline: deadline,
}
const signature = await walletClient.signTypedData({ ... })

// 2. Contract uses signature to transfer tokens (1 tx)
await router.write.swap([permitData, signature, swapParams])
```

### EIP-2612 Permit (native token permit)
```
For tokens that natively implement permit():
sign off-chain → contract calls permit() + action() in same tx
Saves 1 full transaction (~46k gas)
```

### Multicall Batching
```typescript
// Batch multiple reads into 1 RPC call
const results = await publicClient.multicall({
  contracts: [
    { address: tokenA, abi: erc20Abi, functionName: 'balanceOf', args: [user] },
    { address: tokenB, abi: erc20Abi, functionName: 'balanceOf', args: [user] },
    { address: pool,   abi: poolAbi,  functionName: 'getReserves' },
  ],
})

// Batch multiple writes into 1 tx (via multicall contract or AA bundling)
// approve + swap + stake = 1 transaction
```

### Gas-Efficient Patterns
```
1. Use calldata > memory for function inputs
2. Pack storage slots (uint128 + uint128 fits in 1 slot)
3. unchecked{} blocks where overflow impossible
4. Minimize SSTORE operations (21k gas each)
5. Use events for data that doesn't need on-chain access
6. Deploy on L2 (Base/Arbitrum) for 10-100x cheaper gas
7. Dynamic gas pricing: queue non-urgent txs for low-fee windows
```

---

## VI. Authentication & Session Management

### Multi-Provider Auth Architecture
```
users (id, email, role, masterKeyHash, settings)
  └→ user_auth_providers (provider: password|google|wallet|passkey, providerId, credential)
  └→ sessions (refreshTokenHash, tokenPrefix, expiresAt, ipAddress)
```

### JWT Flow (Production Pattern)
```
1. Login → issue accessToken (15min) + refreshToken (7d)
2. refreshToken stored as bcrypt hash + plaintext prefix (first 16 chars)
3. Prefix indexed for O(1) lookup (avoids full-table bcrypt scan)
4. On refresh: find by prefix → bcrypt.compare → rotate → new pair
5. Logout: delete session row → old refresh invalidated
```

### Passkey Authentication (2026 Standard)
```
WebAuthn / FIDO2 authenticator:
1. Registration: user creates passkey (biometric/hardware key)
2. Challenge-response: server sends challenge → authenticator signs
3. No passwords, no seed phrases, phishing-resistant
4. Works with AA smart accounts as signer
```

---

## VII. Vault & Encrypted Key Management

### AES-256-GCM + PBKDF2
```
Key Derivation: PBKDF2(password, randomSalt, 100_000 iterations, sha512) → 32-byte AES key
Encryption:     AES-256-GCM(plaintext, key, randomIV) → { ciphertext, iv, authTag }
Per-user:       Each user has own masterKey derived from their password + unique salt
Auto-lock:      8h inactivity → zero-fill key buffer → delete from memory
```

### What Gets Encrypted
```
1. Wallet private keys (EVM hex / Solana base58)
2. CEX API keys (apiKey, secret, passphrase — each field encrypted independently)
3. Stored as: encryptedBlob + iv + authTag in PostgreSQL columns
4. UNIQUE(userId, exchange) — one credential set per exchange per user
```

### Security Rules
```
- Zero-fill Buffer on lock: key.fill(0) before delete
- Vault MUST be unlocked for any write/decrypt operation
- List operations NEVER return decrypted values
- Approve only required token amounts (never maxUint256)
- Never log/print raw private keys or API secrets (mask: first5***last4)
```

---

## VIII. Chain Configuration (Single Source of Truth)

```typescript
// chains.ts — THE ONLY place chain data is defined
// All services import from here. Never define chain constants elsewhere.

export const VIEM_CHAINS: Record<string, Chain> = { bsc, eth: mainnet, base, arb: arbitrum }
export const WRAPPED_NATIVE: Record<string, `0x${string}`> = {
  bsc:  '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
  eth:  '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
  base: '0x4200000000000000000000000000000000000006',
}
export const EXPLORER_API: Record<string, { url: string; key: string }> = { ... }
export const CHAIN_DISPLAY: Record<string, string> = { ... }
```

**Rule**: Adding a new chain = edit chains.ts ONLY. All consumers auto-discover.

---

## IX. Database Design (Drizzle ORM)

### Schema Patterns
```typescript
// 1. Enums for bounded values
export const chainEnum = pgEnum('chain', ['bsc', 'eth', 'base', 'arb', 'sol'])
export const statusEnum = pgEnum('status', ['created', 'running', 'paused', 'stopped', 'failed'])

// 2. text for big numbers (never float for money)
amountIn: text('amount_in').notNull(),        // "1000000000000000000" not 1.0
price:    text('price').notNull(),             // "0.00000456" exact

// 3. jsonb for extensible config
params:   jsonb('params').default({}).notNull(), // strategy config, user settings

// 4. Indexes on every FK + query pattern
(t) => ({ userIdx: index('idx_user').on(t.userId), statusIdx: index('idx_status').on(t.status) })

// 5. Unique constraints for business rules
(t) => ({ uniq: uniqueIndex('idx_uniq').on(t.userId, t.exchange) })

// 6. Separate tables per exchange (not polymorphic)
binancePositions, gatePositions, hyperliquidPositions  // each with exchange-specific fields
```

### Core Tables
```
users → auth → sessions → wallets → credentials
                               ↓
                          strategies → trades → audit_logs
```

---

## X. Event-Driven Architecture

### EventBus (Dual-Write Pattern)
```
Emit → Ring Buffer (500, in-memory) + JSONL File (append-only, crash recovery)
    → Notify all SSE subscribers
    → Notify typed listeners (service-to-service)
```

### Event Types
```typescript
type EventType =
  | 'trade:pending' | 'trade:confirmed' | 'trade:failed'
  | 'strategy:started' | 'strategy:stopped' | 'strategy:error'
  | 'signal:detected' | 'health:rpc' | 'scanner:buy'
  | 'price:update' | 'ai:decision' | 'system:info'
```

### SSE (Server-Sent Events)
```typescript
// Auth: JWT via query param (EventSource doesn't support headers)
// Heartbeat: every 30s
// Reconnect: auto (EventSource default behavior)
// Frontend: useServerEvents(types[], callback) hook with mode-awareness
```

---

## XI. On-Chain Indexing

### Self-Hosted (Ponder)
```typescript
// ponder.config.ts
export default createConfig({
  networks: { mainnet: { chainId: 1, transport: http(RPC_URL) } },
  contracts: {
    Router: { network: 'mainnet', abi: routerAbi, address: ROUTER, startBlock: 12345678 },
  },
})

// src/Router.ts — event handler
ponder.on('Router:Swap', async ({ event, context }) => {
  await context.db.Swap.create({ id: event.log.id, data: { ... } })
})
```

### Hybrid Indexing Architecture
```
Canonical (Ponder/Envio):  Poll-based, reorg-safe, source of truth
Real-time (WebSocket/SSE): Push-based, for instant UI updates, NOT authoritative
Reconciliation:            Periodically compare real-time state with canonical
```

---

## XII. Strategy Orchestration (BullMQ)

### Flow
```
REST API → Service → BullMQ Queue → Worker → DB + EventBus
```

### Worker Template
```typescript
const worker = new Worker('dca', async (job) => {
  const { strategyId, userId, params } = job.data
  try {
    const wallet = await vault.getDecryptedKey(userId, params.walletId)
    const result = await tradeExecutor.execute({ ... })
    await db.insert(trades).values({ userId, strategyId, status: 'confirmed', txHash: result.hash })
    emitEvent('trade:confirmed', { strategyId, txHash: result.hash })
  } catch (err) {
    emitEvent('trade:failed', { strategyId, error: err.message })
    throw err  // BullMQ handles retry
  }
}, { connection: redis, concurrency: 5 })
```

### Lifecycle: `created → running → paused → stopped/completed/failed`
### Emergency: `POST /api/strategies/stop-all` → kill all jobs + update DB

---

## XIII. RPC Health Manager

```typescript
// Per-chain: [{ url, healthy, latencyMs, failCount }]
function getBestRpc(chain: string): string {
  const healthy = nodes.filter(n => n.healthy).sort((a,b) => a.latencyMs - b.latencyMs)
  if (healthy.length > 0) return healthy[0].url
  return nodes.sort((a,b) => a.failCount - b.failCount)[0].url  // graceful degradation
}
// Success: failCount=0, update latency
// Failure: failCount++; ≥3 → mark unhealthy
// Probe: eth_blockNumber every 30s, 5s timeout
```

---

## XIV. Trade Execution

### Smart Router (V2/V3 parallel)
```
1. Query all V2 routers: getAmountsOut()
2. Query all V3 quoters: quoteExactInputSingle() × [100, 500, 3000, 10000] fee tiers
3. Sort by amountOut descending → select best
4. Turbo mode: direct pool.swap() bypasses router, saves 15-30k gas
```

### Safety (non-negotiable)
```
✓ Approve ONLY required amount (never maxUint256)
✓ getAmountsOut fails → BLOCK trade (prevent sandwich)
✓ amountOutMin = expectedOut × (10000 - slippageBps) / 10000
✓ Insert trade row BEFORE execution (audit trail)
✓ Emit event after completion (trade:confirmed / trade:failed)
```

---

## XV. Testing Strategy

### Split Architecture
```
Smart Contracts:  Foundry (forge test)
  - Unit tests:     Individual function tests
  - Fuzz tests:     Property-based, random inputs
  - Invariant tests: Stateful fuzzing, protocol properties
  - Fork tests:     Test against mainnet state (Anvil)

Application:      Vitest
  - Unit:          Business logic, utils, hooks
  - Integration:   API routes, DB queries, service logic
  - E2E:           Playwright for wallet flows

Static Analysis:  Slither → CI pipeline

CI Pipeline:
  1. forge test --fuzz-runs 1000
  2. slither .
  3. vitest run
  4. playwright test (E2E)
```

### Invariant Testing Pattern (Foundry)
```solidity
// Define protocol properties that must ALWAYS hold
function invariant_totalSupplyMatchesBalances() public {
    assertEq(token.totalSupply(), sumOfAllBalances);
}
// Handler contracts guide fuzzer through realistic user journeys
```

---

## XVI. Security Checklist

| #   | Rule                                      | Why                             |
| --- | ----------------------------------------- | ------------------------------- |
| 1   | AES-256-GCM + PBKDF2 for all keys at rest | Industry standard encryption    |
| 2   | Zero-fill key buffers on vault lock       | Prevent memory scanning         |
| 3   | Approve exact amount, never maxUint256    | Prevent unlimited drain         |
| 4   | Block trade on quote failure              | Prevent sandwich attacks        |
| 5   | JWT + refresh token rotation              | Prevent token reuse             |
| 6   | tokenPrefix index for O(1) lookup         | Prevent full-table bcrypt scan  |
| 7   | Rate limit all endpoints (IP + user)      | Prevent DoS                     |
| 8   | Audit log all mutations                   | Forensic trail                  |
| 9   | SSE requires JWT auth                     | Prevent unauthorized streaming  |
| 10  | User isolation on ALL queries             | Prevent data leaks              |
| 11  | Timelocks on privileged operations        | Detection window                |
| 12  | Pin dependencies + lockfile               | Prevent supply chain attacks    |
| 13  | Invariant tests + fuzz in CI              | Catch edge cases automatically  |
| 14  | Slither static analysis in CI             | Automated vulnerability scan    |
| 15  | Passkey/hardware key for admin            | Phishing-resistant admin access |

---

## XVII. Deployment

```
Frontend:   Vercel (Next.js native) or Cloudflare Pages
Backend:    Docker on VPS + Nginx reverse proxy
Database:   Managed PostgreSQL (Neon / Supabase / RDS)
Redis:      Managed Redis (Upstash serverless / ElastiCache)
Indexer:    Ponder on VPS or managed service
Contracts:  forge script + CREATE2 for deterministic addresses
Monitoring: Prometheus + Grafana (self-hosted) or Datadog
Logs:       Structured JSON → aggregation pipeline

Environment:
  NEXT_PUBLIC_CHAIN_ID, API_BASE_URL
  DATABASE_URL, REDIS_URL
  JWT_SECRET, VAULT_TIMEOUT_MS
  BUNDLER_URL, PAYMASTER_URL
  RPC_ETH, RPC_BSC, RPC_BASE (multiple per chain for failover)
```

---

## XVIII. Credential & Environment Variable Declaration

This skill recommends many third-party services. Below is the **complete registry** of environment
variables, their purpose, which service needs them, and when the agent should request them.

### Required Environment Variables

| Variable               | Service/Purpose                | Required When              | Sensitivity |
| ---------------------- | ------------------------------ | -------------------------- | ----------- |
| `DATABASE_URL`         | PostgreSQL connection string   | Backend init               | 🔴 Secret    |
| `REDIS_URL`            | Redis/BullMQ connection string | Backend init               | 🔴 Secret    |
| `JWT_SECRET`           | Auth token signing             | Backend init               | 🔴 Secret    |
| `VAULT_TIMEOUT_MS`     | Vault auto-lock duration       | Backend init               | ⚪ Config    |
| `RPC_ETH`              | Ethereum RPC endpoint          | Chain interaction          | 🟡 Sensitive |
| `RPC_BSC`              | BSC RPC endpoint               | Chain interaction          | 🟡 Sensitive |
| `RPC_BASE`             | Base RPC endpoint              | Chain interaction          | 🟡 Sensitive |
| `RPC_ARB`              | Arbitrum RPC endpoint          | Chain interaction          | 🟡 Sensitive |
| `BUNDLER_URL`          | AA UserOp bundler endpoint     | Account Abstraction        | 🟡 Sensitive |
| `PAYMASTER_URL`        | Gas sponsorship endpoint       | Gasless UX                 | 🟡 Sensitive |
| `PRIVY_APP_ID`         | Privy embedded wallet          | Social login onboarding    | 🟡 Sensitive |
| `PRIVY_APP_SECRET`     | Privy server-side auth         | Backend Privy verification | 🔴 Secret    |
| `DYNAMIC_ENV_ID`       | Dynamic embedded wallet        | Alt onboarding provider    | 🟡 Sensitive |
| `NEXT_PUBLIC_CHAIN_ID` | Default chain for frontend     | Frontend init              | ⚪ Config    |
| `API_BASE_URL`         | Backend URL for frontend       | Frontend init              | ⚪ Config    |
| `EXPLORER_API_KEY_ETH` | Etherscan API key              | Contract verification      | 🟡 Sensitive |
| `EXPLORER_API_KEY_BSC` | BscScan API key                | Contract verification      | 🟡 Sensitive |
| `PONDER_RPC_URL_*`     | RPC for Ponder indexer         | Indexer setup              | 🟡 Sensitive |
| `DEPLOYER_PRIVATE_KEY` | Contract deployment signer     | `forge script` deploys     | 🔴 Critical  |

### Sensitivity Levels

```
⚪ Config:     Safe to commit to .env.example as placeholder values
🟡 Sensitive:  Must be in .env (gitignored), contains API keys or endpoints
🔴 Secret:     Must NEVER appear in logs, code, or git history
🔴 Critical:   Private keys — highest security, see §XIX rules
```

### Agent Behavior: When to Request Credentials

```
Rule 1: NEVER invent, generate, or hardcode real secrets. Use placeholder values only.
Rule 2: When scaffolding, create .env.example with descriptive placeholders:
        DATABASE_URL=postgresql://user:password@localhost:5432/dbname
        JWT_SECRET=change-me-to-a-64-char-random-string
        DEPLOYER_PRIVATE_KEY=0x_DO_NOT_COMMIT_REAL_KEY
Rule 3: Add .env to .gitignore BEFORE any .env file is created.
Rule 4: When a feature requires a credential not yet configured:
        → Inform the user which variable is needed and why
        → Provide the service's signup URL
        → Ask the user to set it in .env
        → NEVER ask the user to paste secrets into chat
Rule 5: For DEPLOYER_PRIVATE_KEY, always recommend:
        → cast wallet new (Foundry) to generate locally
        → Hardware wallet / Ledger for mainnet deploys
        → NEVER use a funded mainnet key in .env on a dev machine
```

---

## XIX. Security: Sensitive Key Handling for Agents

This section defines **mandatory rules** for any AI agent following this skill when handling
private keys, API secrets, and credential material during development, testing, and deployment.

### Agent MUST Rules (Non-Negotiable)

```
1. NEVER echo, log, or print private keys or API secrets to stdout/stderr.
2. NEVER include real secrets in code, comments, commit messages, or artifacts.
3. NEVER store secrets in source-controlled files (only .env, which is gitignored).
4. NEVER transmit secrets over unencrypted channels.
5. When writing code that handles secrets at runtime:
   → Use environment variables (process.env.XXX)
   → Validate presence at startup: if (!process.env.JWT_SECRET) throw new Error(...)
   → Mask in logs: key.slice(0,5) + '***' + key.slice(-4)
6. When writing Foundry deploy scripts:
   → Use --private-key only on testnets
   → For mainnet: use --ledger or --trezor flags
   → NEVER pass private keys as CLI arguments in production
7. When creating Docker/CI configs:
   → Use secrets managers (Docker secrets, GitHub Actions secrets)
   → NEVER bake secrets into Docker images or CI YAML
```

### Credential Lifecycle

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  GENERATION  │──▶│   STORAGE    │──▶│    USAGE     │
│              │   │              │   │              │
│ cast wallet  │   │ .env file    │   │ process.env  │
│ openssl rand │   │ Vault table  │   │ Vault decrypt│
│ Service UI   │   │ HW wallet    │   │ --ledger     │
└──────────────┘   └──────────────┘   └──────────────┘
                          │
                    ┌─────▼─────┐
                    │ ROTATION  │
                    │ JWT: 15m  │
                    │ Refresh:7d│
                    │ API keys: │
                    │  90d max  │
                    └───────────┘
```

### .env.example Template

The agent should always generate this file when scaffolding a new project:

```bash
# === Core Infrastructure ===
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
REDIS_URL=redis://localhost:6379
JWT_SECRET=CHANGE_ME_run_openssl_rand_hex_32
VAULT_TIMEOUT_MS=28800000

# === Blockchain RPC (get from: https://alchemy.com or https://infura.io) ===
RPC_ETH=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
RPC_BSC=https://bsc-dataseed1.binance.org
RPC_BASE=https://base-mainnet.g.alchemy.com/v2/YOUR_KEY
RPC_ARB=https://arb-mainnet.g.alchemy.com/v2/YOUR_KEY

# === Account Abstraction (get from: https://zerodev.app or https://pimlico.io) ===
BUNDLER_URL=https://api.pimlico.io/v2/YOUR_CHAIN/rpc?apikey=YOUR_KEY
PAYMASTER_URL=https://api.pimlico.io/v2/YOUR_CHAIN/rpc?apikey=YOUR_KEY

# === Embedded Wallet (choose one: https://privy.io or https://dynamic.xyz) ===
PRIVY_APP_ID=your-privy-app-id
PRIVY_APP_SECRET=your-privy-app-secret
# DYNAMIC_ENV_ID=your-dynamic-env-id

# === Frontend ===
NEXT_PUBLIC_CHAIN_ID=1
API_BASE_URL=http://localhost:3001

# === Contract Deployment (NEVER commit a funded mainnet key) ===
DEPLOYER_PRIVATE_KEY=
# ↑ This is Foundry's default Anvil key #0 — safe for local dev only

# === Block Explorer APIs (for contract verification) ===
EXPLORER_API_KEY_ETH=your-etherscan-key
EXPLORER_API_KEY_BSC=your-bscscan-key
```

---

## XX. Quick Start

```
 1. Init: Next.js 15+ (frontend) + Fastify (backend) + Foundry (contracts)
 2. Copy .env.example → .env, fill in real values (see §XVIII for each variable)
 3. Ensure .env is in .gitignore
 4. Define chains.ts (single source of truth)
 5. Design DB schema: users, auth_providers, sessions, wallets, credentials, strategies, trades
 6. Build Vault: AES-256-GCM + PBKDF2, auto-lock, zero-fill
 7. Implement auth: JWT rotation + SIWE + social login (Privy/Dynamic)
 8. Choose wallet strategy: embedded (Privy) for consumer, RainbowKit for crypto-native
 9. Implement AA: Paymaster for gasless UX, Permit2 for gasless approvals
10. Build EventBus: ring buffer + JSONL + SSE
11. Set up BullMQ workers for async strategies
12. Build RPC health manager (30s probe, 3-fail threshold)
13. Implement trade executor: smart router, slippage protection, exact approvals
14. Set up indexer: Ponder (self-hosted) or The Graph (decentralized)
15. Testing: Foundry (fuzz+invariant) + Vitest + Playwright
16. CI: forge test → slither → vitest → playwright → deploy
17. Deploy: Vercel (frontend) + Docker (backend) + managed DB/Redis
```

---

*Web3 DApp Builder v1.1.0 — Industry best practices, 2026*
