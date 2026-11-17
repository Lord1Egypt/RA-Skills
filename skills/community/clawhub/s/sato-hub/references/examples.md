# Worked examples — real outputs

Captured 2026-09-08 with `scripts/query.sh` against the live endpoint, trimmed.
Numbers will have moved; re-run before quoting.

## 1. Search: what supports x402?

```sh
scripts/query.sh search_resources '{"query":"x402","limit":3}'
```

```
# Search: "x402"

Showing 3 of 71 (more available — next_offset: 3)

- **Agent Payments Protocol (AP2)** (`agent-payments-protocol-ap2`) — Tool/Service · Ethereum, Base, Multichain · Quiet · 4mo ago · ★2937 · 100% of 57 daily checks ok
  Open protocol from Google for secure agent-led payments across traditional and crypto rails, with a crypto-native x402 extension built with Coinbase, Ethereum Foundation, and MetaMask.
- **x402** (`x402`) — Tool/Service · Base, Ethereum, Multichain, Solana · Active · 5d ago · ★150 · ✓ install verified · 100% of 57 daily checks ok
  Open payment protocol enabling agents and apps to pay for APIs over HTTP using stablecoins.
- **Zerion** (`zerion`) — Tool/Service · Ethereum, Base, Arbitrum, ... · Active · today · ★59 · ✓ install verified · 100% of 57 daily checks ok
  Wallet and DeFi data provider offering portfolio, positions, transactions, PnL, and prices across many chains, with an agent-accessible API.

— Source: Sato Hub · https://satohub.ai/directory?utm_source=mcp&utm_medium=agent
```

"100% of 57 daily checks ok" is the share of Sato Hub's own checks that
succeeded over 57 days — not uptime.

## 2. Detail: is x402 real, maintained, open source?

```sh
scripts/query.sh get_resource '{"slug":"x402","include_activity":false,"response_format":"json"}' \
  | jq '.resource | {name,status,open_source_status,liveness,last_commit_at,github_stars,trust_score,trust_tier,verification_status,creator_name,deployment_options,sato_url,verify_url}'
```

```json
{
  "name": "x402",
  "status": "Early",
  "open_source_status": "Yes",
  "liveness": "Active",
  "last_commit_at": "2026-09-03T23:44:57.000Z",
  "github_stars": 150,
  "trust_score": 86,
  "trust_tier": "High",
  "verification_status": "Unverified",
  "creator_name": "x402 Foundation",
  "deployment_options": ["npm", "pip"],
  "sato_url": "https://satohub.ai/resources/x402?utm_source=mcp&utm_medium=agent",
  "verify_url": "https://satohub.ai/verify/x402?utm_source=mcp&utm_medium=agent"
}
```

How to phrase it: open source, active (last commit 2026-09-03), Sato Score 86
(High) for openness/activity/verifiability; `verification_status` is
Unverified, so no independent review is on record. Cite the `sato_url`.

## 3. Recommend a stack

```sh
scripts/query.sh recommend_stack '{"goal":"agent that pays for APIs with USDC on Base","chain":"Base","max_per_slot":1}'
```

```
# Recommended stack — agent that pays for APIs with USDC on Base
**Chain:** Base

## Agent framework
- **Almanak** (`almanak`) — Sato Score 83 (High) · liveness: live · deploy spec: yes · chains: Multichain, Ethereum, Arbitrum, Optimism, Base, ...
  Sato Score 83 (High) · site live · 100% of 57 daily checks answered · install reproduced by Sato Hub 2026-09-07 · Base supported

## Wallet & keys
- **Trust Wallet Agent Kit (TWAK)** (`trust-wallet-agent-kit`) — Sato Score 86 (High) · liveness: live · deploy spec: yes · chains: Ethereum, Base, Solana, ...

## MCP tooling
- **Monad Agent Kit** (`monad-agent-kit`) — Sato Score 72 (High) · liveness: live · deploy spec: yes · chains: Monad

## Gaps
- No mcp tooling pick explicitly lists Base support — verify chain fit before committing.

_Ranked by Sato Score (openness/activity/verifiability), liveness, whether the documented install was reproduced by Sato Hub, and the share of our daily checks answered. ... Not a safety, quality, or returns judgment._
```

Carry the "Gaps" line into your answer.

## 4. Trend: one series, one venue, one chain, one stage

```sh
scripts/query.sh get_trend '{"venue":"x402","chain":"Base","stage":"gasless_usdc_attribution_rate","points":4}'
```

```
# x402 · Base · gasless_usdc_attribution_rate — weekly trend

Unit: percent of sampled gasless USDC settlements attributable to a catalogued x402 seller. 2 point(s), oldest first. First known → last known: **down**.

| date | value | n | method |
|---|---|---|---|
| 2026-08-31 | 22 | 4471 | 12 stratified windows of 200 blocks spread across the trailing 7 days; AuthorizationUsed transactions counted, then joined against the exact-lane transfers by transaction hash. ... |
| 2026-09-07 | 7.8 | 9187 | (same method) |

One series only — never add it to another. A null point is unknown, not zero.

— Source: Sato Hub · https://satohub.ai/agent-economy/x402
```

Stage names come from `get_agent_economy` (e.g. for x402 on Base:
`settlements_by_facilitator`, `seller_paid`, `gasless_usdc_attribution_rate`).
An unknown stage returns an error that says so.

## 5. Compare two listings

```sh
scripts/query.sh compare_listings '{"a":"x402","b":"agent-payments-protocol-ap2"}'
```

```
| | x402 | Agent Payments Protocol (AP2) |
|---|---|---|
| Chains | Base, Ethereum, Multichain, Solana | Ethereum, Base, Multichain |
| Standards | x402 | x402, mcp, a2a |
| Open source | Yes | Yes |
| Last activity | 2026-09-03 | 2026-04-28 |
| Install proof | Reproduced install | Self-reported install |
| Verification | Unverified | Verified |
| Sato Score | 86 | 72 |
| GitHub stars | 150 | 2,937 |

No winner is declared. Cite the comparison page, not a verdict.
— Source: Sato Hub · https://satohub.ai/compare/x402-vs-ap2
```

## 6. REST slice

```sh
scripts/query.sh rest '/api/export/index.json?standard=x402' \
  | jq '{schema_version, total: (.resources|length), first: .resources[0] | {slug,trust_score,trust_tier,detail_url}}'
```

```json
{
  "schema_version": "1",
  "total": 50,
  "first": { "slug": "agent-payments-protocol-ap2", "trust_score": 72, "trust_tier": "High",
             "detail_url": "https://satohub.ai/resources/agent-payments-protocol-ap2" }
}
```

---

# Before you act — Preflight and Sato Route

Captured 2026-09-12 against the live endpoint, trimmed. Numbers and verdicts
move; re-run before quoting. Every one of these is read-only: **nothing signs,
holds a key, deploys, relays or moves funds.**

Each example shows equivalent calls — raw curl (JSON-RPC over the MCP
endpoint), the bundled script, and the plain REST route.

## 7. Preflight a repo before you install it

```sh
# curl — MCP JSON-RPC
curl -sS https://satohub.ai/api/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
       "name":"onchain_agent_preflight",
       "arguments":{"repo":"coinbase/agentkit","response_format":"json"}}}'

# script
scripts/query.sh preflight '{"repo":"coinbase/agentkit","response_format":"json"}'

# REST
curl -sS 'https://satohub.ai/api/preflight?repo=coinbase/agentkit'
```

```json
{
  "verdict": "go",
  "rule": "R5",
  "target": { "kind": "repo", "value": "coinbase/agentkit", "slug": "coinbase-agentkit",
              "sato_url": "https://satohub.ai/resources/coinbase-agentkit",
              "verify_url": "https://satohub.ai/verify/coinbase-agentkit" },
  "evidence": [
    { "check": "Directory record", "result": "Listed as Coinbase AgentKit (Developer Tool).",
      "source_field": "resources.slug", "checked_at": "2026-09-12" },
    { "check": "Sato Score", "result": "88 of 100, tier High. The score measures how open, active and verifiable the project is, not safety or quality.",
      "source_field": "resources.trust_score", "checked_at": "2026-09-12" },
    { "check": "Reproduced install", "result": "The documented install path was re-run in an isolated container and completed. Proves installability, not runtime behaviour.",
      "source_field": "resources.deploy_spec.deploy_status", "checked_at": "2026-09-07" }
  ],
  "checked_at": "2026-09-12T18:24:54.074Z"
}
```

Pass exactly one target: `repo`, `package`, `endpoint`, `agent` (`base:42`), or
`token` + `chain`. Report the verdict **with its rule and the dates on the
evidence lines** — a verdict names what was checked and when, and `unknown`
means Sato Hub holds no record, not that something is wrong.

## 8. Preflight a token before you trade it

```sh
scripts/query.sh preflight '{"token":"0x1bc0c42215582d5A085795f4baDbaC3ff36d1Bcb","chain":"Base","response_format":"json"}'
curl -sS 'https://satohub.ai/api/preflight?token=0x1bc0c42215582d5A085795f4baDbaC3ff36d1Bcb&chain=base'
```

Keyless EVM chain reads: bytecode presence and size, the ERC-20 views, the
Clanker v4 factory's **own** deployment record (`tokenDeploymentInfo`, not a
bytecode heuristic), and the Uniswap v3 factory across the four standard fee
tiers against wrapped native.

Carry these into the answer, because the payload does:

- **Holder concentration is permanently null** — there is no keyless public
  source, and explorer HTML is not a method Sato Hub will cite.
- **Uniswap v4 and non-Uniswap liquidity are permanently null** — a v4 poolId
  cannot be reconstructed from a token address, so any answer would be a guess
  dressed as a reading.
- **A pool existing is existence, not depth.** No reserves, no TVL, no price.
- Nothing in this lane says safe, audited, rug or scam. Those are not readings.

## 9. Route a swap, with the fee disclosed before anything is signed

```sh
scripts/query.sh route_swap '{"chain":"Solana","token_in":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v","token_out":"So11111111111111111111111111111111111111112","amount":"1000000","response_format":"json"}'
curl -sS 'https://satohub.ai/api/route/swap?chain=Solana&token_in=USDC&token_out=SOL&amount=1000000'
```

```json
{
  "route": { "slug": "jupiter-aggregator", "name": "Jupiter", "listed": true,
             "sato_url": "https://satohub.ai/resources/jupiter-aggregator",
             "liveness": "Active", "observed_success_pct": 100, "observed_days": 60,
             "install_verified": true, "listing_verification": "Verified" },
  "quote": { "venue": "jupiter-aggregator", "amount_in": "1000000", "amount_out": "9820792",
             "chain": "Solana", "source_url": "https://developers.jup.ag/docs/swap-api/add-fees-to-swap" },
  "sato_fee_bps": 0,
  "disclosure": "No Sato fee is charged on this quote: Jupiter takes its platform fee into an on-chain referral token account, and none is configured for this deployment … The schedule, when a referral account exists: Stable-to-stable pairs are 3 bps; a pair of majors (a chain's native coin such as ETH or SOL, its wrapped form, or a stablecoin) is 15 bps; a pair with any other token is 75 bps; cross-chain is 25 bps, or 75 bps when either side is any other token. Sato Hub does not sign, hold or move funds.",
  "chosen_by": [
    { "signal": "Observed record", "value": "100% of Sato Hub's own daily checks succeeded over 60 day(s). This is the share of OUR checks that succeeded, never uptime — a failure can be on our side.",
      "source_field": "resources.uptime_observed.success_rate_pct" }
  ],
  "checked_at": "2026-09-12T18:25:25.491Z"
}
```

Adapters asked in parallel: Jupiter, 0x, 1inch, Odos. The response carries the
calldata; **the caller signs it.** The fee is a parameter on the aggregator's
own quote, taken inside the swap transaction by the router — a failed, reverted
or unsigned trade pays nothing. Use the framing the payload uses:
**"Jupiter was chosen by Sato Route on 2026-09-12, because …"** — never "best
venue" or "best price".

## 10. Route a token launch, and read the config before signing it

```sh
scripts/query.sh route_launch '{"chain":"Base","goal":"agent_token","name":"Example Agent","symbol":"EXMPL","deployer":"0x…","response_format":"json"}'
curl -sS 'https://satohub.ai/api/route/launch?chain=Base&goal=agent_token&name=Example%20Agent&symbol=EXMPL&deployer=0x…'
```

```json
{
  "venue": { "slug": "clanker", "name": "Clanker v4", "lane": "prepared_config",
             "pool_fee_pct": 1, "creator_share_pct": 80, "protocol_share_pct": 20,
             "programmable_fee_split": true,
             "facts": [{ "fact": "Deploy config takes `rewards.recipients`, an array of { recipient, admin, bps, token } entries whose `bps` must total 10000.",
                         "source_url": "https://clanker.gitbook.io/documentation/sdk-reference/v4", "as_of": "2026-09-11" }] },
  "reason": "Clanker v4 was chosen by Sato Route on 2026-09-12, because it documents a programmable reward-recipient split, so the deploy config below can be signed as-is, it documents agent token launches, and it publishes a 80% creator share of its 1% pool fee. Read the sources in chosen_by and check them yourself — this is a recommendation, not a verdict.",
  "fee": { "bps": 0, "recipient": null, "basis": "creator_lp_share", "disclosed": true,
           "note": "Sato Route takes no share of this launch: ROUTE_LAUNCH_FEE_BPS is 0, so no Sato recipient appears in the deploy config at all and the deployer holds the full 10000 bps of the reward split." },
  "prepared_deploy": { "sdk": "clanker-sdk/v4",
    "how_to_use": "Pass this object to the clanker-sdk v4 `deploy()` with your own signer. Sato Hub ships no SDK dependency, holds no key and never deploys; read the config — the reward split included — before you sign it.",
    "config": { "name": "Example Agent", "symbol": "EXMPL", "chainId": 8453,
      "rewards": { "recipients": [{ "recipient": "0x…", "admin": "0x…", "bps": 10000, "token": "Both" }] } } },
  "facts_as_of": "2026-09-11"
}
```

Four venues are covered — Clanker v4, Bankr, Virtuals, Zora creator coins — and
only Clanker documents a programmable recipient split, so only it gets a
prepared config. The others come back as alternatives with `behind_on` saying
exactly what they lost on. **Zora's `creator_share_pct` is `null` because Zora
publishes a 1% fee but not the per-party split: unread, not generous — and it
ranks last for that reason.** `facts_as_of` says how stale the venue table is;
re-read each `source_url` before signing. A fee schedule says nothing about what
a token will do after it launches.

## 11. Route an agent — and an honest "unknown"

```sh
scripts/query.sh route_agent '{"capability":"trading","chain":"Base","response_format":"json"}'
curl -sS 'https://satohub.ai/api/route/agent?capability=trading&chain=Base'
```

```json
{
  "route": { "unknown": true,
             "reason": "No candidate declares the capability \"trading\"." },
  "candidates_considered": 2,
  "probed": 0,
  "coverage": { "sources": ["sato_agent_passports"],
    "note": "Candidates are the listed Sato Agent Passports. ERC-8004 registrations are not enumerable keyless from a request — the registry sampler is a weekly batch job — so an agent registered on-chain but not holding a passport is absent from this pool. Absent means unseen, not unqualified." }
}
```

Report the `unknown` as the answer. It is the designed behaviour when nothing
qualifies — never substitute a low-confidence pick, and never read an absent
agent as a disqualified one.

## 12. Build plan — a goal in words, a plan out

```sh
scripts/query.sh build_plan '{"goal":"a Base trading agent that swaps USDC to ETH on a signal","chain":"Base"}'
curl -sS 'https://satohub.ai/api/satobot/plan?goal=a%20Base%20trading%20agent%20that%20swaps%20USDC%20to%20ETH%20on%20a%20signal&chain=Base'
```

```
restatement : You want: a Base trading agent that swaps USDC to ETH on a signal.
              Chain: Base. Read as a swap build.
intent      : swap   (chain_source: given)
stack       : framework almanak (83, preflight go) · framework elizaos (87, go)
              wallet trust-wallet-agent-kit (86, go) · wallet privy (83, go)
              trading 1inch (75, go) · trading cloddsbot · mcp sodax-builders-mcp
              mcp bybit-trading-mcp
first_action: swap, ready:false — missing "a live quote — re-run the route for
              your own size". Quoted at a nominal 1 USDC so the route can be
              read; it is a quote, not an order and not a fill.
open_qs     : Who holds the keys, and what is the agent allowed to sign without
              you? · What triggers a trade, what size, and what happens when the
              signal is wrong? · …
```

Every component is a real listing with its own `sato_url` — the plan invents
nothing. A stack item with `preflight: null` was not checked, which is unknown
and not a failure. The first action is quoted at a **nominal** size, never the
user's; the user re-quotes for its own size, reads the disclosed fee, and signs
with its own key.
