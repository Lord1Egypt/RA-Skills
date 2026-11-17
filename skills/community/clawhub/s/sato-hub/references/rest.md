# Keyless REST fallback

All endpoints are plain `GET`, no auth, on `https://satohub.ai`. Machine spec:
`GET /api/openapi.json`. Catalog data is CC-BY-4.0 ("data by satohub.ai");
scores and liveness are informational signals, not safety or quality
guarantees. The free export is catalog fields only — no score history,
provenance, trust components or commercial fields; depth lives behind the MCP.

```sh
scripts/query.sh rest '/api/export/index.json?chain=Base&standard=x402'
```

## Directory export

`/api/export/index.json` · `/api/export/index.csv` · `/api/export/index.ndjson`

Filters (all optional, combinable): `?category=` `?chain=` `?standard=`
`?use_case=` `?integration=` `?deploys_as=` `?min_observed_success=` (implies
≥14 observed days).

Fields per entry (`schema_version` "1"): `slug`, `name`, `category`,
`subcategory`, `entity_class`, `resource_type`, `interfaces[]`, `standards[]`,
`use_cases[]`, `description_short`, `website_url`, `github_url`, `docs_url`,
`chains_supported[]`, `tags[]`, `status`, `open_source_status`, `trust_score`,
`trust_tier`, `provisional`, `liveness`, `last_activity_at`, `github_stars`,
`verified_install`, `verification_status`, `creator_name`,
`deployment_options[]`, `supported_integrations[]`, `observed_success_pct`,
`observed_days`, `install_verified_at`, `date_added`, `detail_url`.

## Skills export

`/api/export/skills.json` · `.csv` · `.ndjson` — filters `?q=` `?registry=`
(clawhub|skillssh|github) `?flag=` `?slug=`. Each skill carries its disclosure
flags with evidence.

## Adoption export (current week only)

`/api/export/adoption.json` · `.csv` · `.ndjson` — filters `?venue=` `?chain=`
`?stage=` `?slug=`. One row per venue × chain × stage. Never sum rows; `null`
is unknown. The weekly series is not in the free export — use the MCP
`get_trend` tool.

## Change feed

`/api/changes?since=YYYY-MM-DD` — `added`, `updated` (field-level diff of the
export fields vs. the baseline snapshot), `changed` (event log), `removed`.
Mirror from added + updated + removed. 90-day window.

## Resolve a repo or package to a listing (new)

`/api/resolve?repo=<github url>` or `/api/resolve?package=<npm name>` →
`{slug, name, sato_score, verify_url, sato_url}` or `404` when nothing in the
index matches. Being added at the time of writing; a 404 today may mean the
route is not live yet, not that the project is unlisted — fall back to
`search_resources`.

## Badges

- `/api/badge/<slug>` — Sato Score badge SVG, links to `/verify/<slug>`.
- `/api/badge/<slug>.json` — shields.io endpoint schema (new; same caveat as
  `/api/resolve`).
- `/api/agents/<slug>/badge` — "Registered on Sato Hub" SVG for a passport.
  It never says verified.

## Agent Passports

- `/api/registry/search?q=&chain=&type=` — listed passports.
- `/api/agents/<slug>/manifest` — the `sato.agent.manifest/v1` document.

## Citable pages

`/resources/<slug>` (listing) · `/verify/<slug>` (Sato Score report) ·
`/compare/<a>-vs-<b>` · `/agent-economy/<venue>` · `/numbers/<slug>` ·
`/skills/<id>` · `/agents/<slug>` · `/sato-score` (methodology).

## Preflight and Sato Route (REST)

The same pure engines the MCP tools call, over plain keyless `GET`. Read-only:
**nothing here signs, holds a key, deploys, relays or moves funds.**

- `/api/preflight?repo=` · `?package=` · `?endpoint=` · `?agent=<chain>:<id>` ·
  `?token=<0x…>&chain=base|ethereum|arbitrum` — exactly one target. Returns
  `{ verdict, rule, target, evidence[], checked_at, caveat }` (+ `token` for the
  token lane). Human page:
  https://satohub.ai/preflight
- `/api/route/swap?chain=&token_in=&token_out=&amount=&slippage_bps=&taker=` —
  the chosen venue's quote and calldata, `sato_fee_bps` and `disclosure` stated
  before anything is signed. Fee schedule: Sato Route swaps cost 3 bps stable-to-stable, 15 bps between majors (a chain's native coin such as ETH or SOL, its wrapped form, or a stablecoin), 75 bps with any other token and 25 bps cross-chain (75 bps when either side is any other token), taken as a parameter on the aggregator's own quote inside the transaction you sign; a failed, reverted or unsigned trade pays nothing. A token launch carries a disclosed share of the creator's LP fee, stated as fee.bps on every launch response, including when it is 0. Sato OS charges 3 / 15 bps on its own spot swap rail and a 3 bps perp builder fee, with no cross-chain tier. Some venues keep a share or pay later, and every quote says which.
- `/api/token/resolve?input=<address|mint|link>&chain=base|solana` — what an
  address, a Solana mint or a link (DexScreener, GeckoTerminal, Birdeye,
  pump.fun, GMGN, Basescan, Solscan, Jupiter, Uniswap, Aerodrome, Zora, Clanker)
  is: chain, name, symbol, decimals, token program, the main pool with its own
  liquidity and the USD price, each figure with its source and time; on Solana
  the mint's authorities and Token-2022 extensions. A pool link resolves to the
  pool's base token. Describes only; `null` is unknown and `gaps` says why.
- `/api/route/agent?capability=&chain=&requires_mcp=&requires_x402=` — the
  chosen Sato Agent Passport with `chosen_by`, or `404 { unknown, reason }`.
- `/api/route/launch?chain=&goal=&name=&symbol=&deployer=` — the chosen launch
  venue with its published facts, the fee disclosed at every value including 0,
  and a prepared `clanker-sdk/v4` config for the one lane that documents a
  programmable recipient split.
- `/api/route/x402?capability=&chain=` — which declared x402 endpoint Sato Hub
  would route a request to, from the daily verification lane. A verified 402 is
  a protocol observation on its check date: the URL answered HTTP 402 with a
  payload a client could parse. No payment was sent to find out. A verification
  older than 7 days is not standing and is not routed to. Sato Hub does not
  relay, pay, sign or settle — the buyer settles the seller's own 402 with its
  own wallet.
- `/api/satobot/plan?goal=&chain=&budget_usd=` (`GET` or `POST`) — the build
  plan, same engine as `onchain_agent_build_plan`.

Route pages for humans: https://satohub.ai/route · https://satohub.ai/preflight
· https://satohub.ai/x402/verified · https://satohub.ai/docs/deploy-spec
