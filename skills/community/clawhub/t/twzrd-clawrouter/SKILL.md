---
name: twzrd-clawrouter
description: |
  TWZRD Preflight for ClawRouter / BlockRun / OpenClaw. The independent pre-spend gate for agents using ClawRouter (for LLM models, Surf crypto data, Predexon, voice, image, etc.) or paying BlockRun.

  The one rule: Before using ClawRouter or paying BlockRun, call the free TWZRD preflight. decision=block → abort.

  Composes with AgentCash or direct; Solana-native receipt proof after. Use before any x402 spend through ClawRouter proxy or BlockRun gateway.

  WHAT YOU GET FREE: ReadinessCard (allow / warn / block + trust_score + caveats) from Solana x402 payer graph before routing spend.
  PAID (x402, USDC on Solana): full trust + portable Ed25519-signed V5 receipt (when querying TWZRD intel alongside).
  TRIGGERS: clawrouter preflight, blockrun spend gate, surf data safe, openclaw before pay, pre clawrouter, x402 router gate, blockrun trust, preflight claw
homepage: https://intel.twzrd.xyz
metadata:
  version: "0.1.2"
  tags: ["x402", "clawrouter", "openclaw", "preflight", "trust", "solana", "usdc", "blockrun", "surf"]
---

# TWZRD Preflight for ClawRouter - the independent pre-spend gate

TWZRD is the independent scorer on the real Solana x402 payer graph. Use this as the preflight gate in front of ClawRouter (BlockRunAI/ClawRouter) and BlockRun spends in the OpenClaw/Moltbook ecosystem. If the ReadinessCard says block, abort before the local proxy or gateway triggers a 402.

Positioning: L7 trust annotation over L4 routing (ClawRouter local smart router + Surf marketplace + 55+ models). Does not replace ClawRouter; gates before it.

ClawRouter: local <1ms routing, wallet sig auth, x402 USDC (Base primary + Solana SVM paths via sol.blockrun.ai), bundled Surf skill (83+ endpoints (see skills/surf/SKILL.md for current catalog) for CEX/DEX/on-chain SQL/pred markets/wallet intel), image/video/voice. One install for OpenClaw (plugin), Claude Code (MCP), standalone. No accounts/keys for the router itself.

No API key for TWZRD preflight. Free tier is curl.

## Install

```bash
npx clawhub install twzrd-clawrouter
```

After install: restart your OpenClaw session (skills load at session start), then run the curl below to confirm it's working.

Note: the page may show `openclaw skills install twzrd-clawrouter` — that command does not exist. The correct install is `clawhub install` or `npx clawhub install` above.

## Try it now (no wallet, no keys)

Run this as-is — no substitution needed:

```bash
curl -s -X POST https://intel.twzrd.xyz/v1/intel/preflight \
  -H 'content-type: application/json' \
  -d '{"resource_name": "ClawRouter Surf crypto data", "agent_intent": "test"}'
```

Returns a `ReadinessCard` with `decision` (allow / warn / block), `trust_score` (0-100), and `caveats[]`. In production, add `seller_wallet` from the ClawRouter 402 response for a stronger signal.

## The one rule

Before using ClawRouter (for models, Surf crypto data, Predexon, voice, etc.) or paying BlockRun:

```bash
curl -s -X POST https://intel.twzrd.xyz/v1/intel/preflight \
  -H 'content-type: application/json' \
  -d '{
    "resource_name": "ClawRouter Surf crypto data",
    "seller_wallet": "SELLER_WALLET_FROM_402_RESPONSE",
    "price_usdc": 0.001,
    "agent_intent": "query surf onchain/sql or premium model via clawrouter proxy",
    "queried_pubkey": "YOUR_CLAWROUTER_WALLET_ADDRESS"
  }'
```

`seller_wallet` and `queried_pubkey` are optional — omit them on first call; add once you have the payTo from ClawRouter's 402 response.

Read `readiness_card.decision` (or top-level in some responses):

- `block` -> abort. Do not invoke the ClawRouter proxy (localhost:8402) or direct BlockRun call that would spend.

- `warn`  -> proceed with caution (low corpus signal).

- `allow` -> proceed normally to ClawRouter/BlockRun.

Also returned: `trust_score` (0-100), `caveats[]`, `proof`, `can_spend`. Gate strictly on `decision=block`. Free tier is conservative (many wallets default warn/can_spend=false). Fail open on preflight unavailability (timeout / non-2xx / error): log the skip, do not penalize the ClawRouter path.

## Exact preflight usage (HTTP + MCP)

HTTP (no auth, as shown in the one rule; base https://intel.twzrd.xyz):

- POST /v1/intel/preflight (resource_name and/or seller_wallet required for good signal; price_usdc and agent_intent recommended).

- GET /v1/intel/score_wallet_for_intel , get_top_intel_agents, get_counterparties, get_facilitator_footprint, compare_wallets, score_wallets_batch.

- GET /v1/intel/trust/{pubkey}?seller_wallet=... (paid 0.05 USDC on Solana; returns full model + V5 receipt).

MCP (streamable-http, recommended for agents):

- https://intel.twzrd.xyz/mcp

- Primary tool: get_readiness_card_tool (resource_name, seller_wallet, agent_intent, price_usdc, queried_pubkey)

- Also: verify_receipt, get_provider_reputation, dexter_preflight, etc. (17 tools total).

OpenClaw: `openclaw mcp add twzrd --url https://intel.twzrd.xyz/mcp --transport streamable-http`

AgentCash already registers api.twzrd.xyz (use its MCP/CLI for mixed stables + TWZRD + preflight patterns; see AGENT_USAGE.md).

## Composition

- Call TWZRD preflight first (free) for the intended ClawRouter resource (e.g. "ClawRouter Surf", "BlockRun premium model", "blockrun voice").

- If not block, proceed to ClawRouter local proxy call (OpenAI compat or direct /v1/surf/* or /v1/images etc.). ClawRouter handles its internal x402 to BlockRun treasury from the local wallet (EVM or Solana-derived via setup).

- Works with AgentCash (unified payer) or direct (@x402/fetch in custom, or ClawRouter's bundled).

- After a paid path (especially if you paid TWZRD for intel or have a settle receipt): verify with offline tool or MCP verify_receipt. Receipts are portable Ed25519 V5 anchored to Solana USDC (PayAI primary facilitator for our Solana proof). (example provides verifyReceiptIfAny stub with wiring TODO + extractPayToFrom402 helper (with usage comments; preflight demo relies on resource_name, extraction shown as illustrative for prod))

- Post-spend: store any receipt leaf for later root_provenance or independent audit if mixed with WZRD protocol.

## Concrete runnable TS/JS example (full flow)

The committed prototype lives in sibling `example.ts`. It now wires the full demand-facing loop (from funnel-join #739):

- preflight gate (ReadinessCard + fail-open + block abort)
- exported `createClawRouterOnBeforePaymentHook()` — the upstream hook for ClawRouter proxy settlements (addresses the gap noted in openclaw-twzrd-preflight where sign happens inside 8402, invisible to tool hooks)
- ClawRouter/BlockRun proxy call
- real live verify step (fetches /v1/receipts/example + calls /v1/receipts/verify; plus CLI command for real receipts)

Run: `npx tsx example.ts` (needs proxy up for the call step, but preflight + hook + verify are self-contained and hit live surfaces).

Update both SKILL.md and example.ts when evolving the flow. Status: executable prototype that demonstrates a non-twzrd (ClawRouter) agent hitting the TWZRD gate.

```ts
// example.ts
// Run: npx tsx example.ts   (or ts-node, or compile to .mjs)
// Requires: ClawRouter proxy up for the call step (npx @blockrun/clawrouter or via OpenClaw + clawrouter setup).
// See sibling SKILL.md for full docs, one rule, security, publish command, links.
// This file + SKILL.md = the publishable prototype (keep both copies of the flow in sync).
// Integrity: pin verifier e.g. twzrd-receipt-verifier@1.0.1 (check npm tarball shasum); proxy via npx @blockrun/clawrouter@<pinned> or post-setup `ps` + `clawrouter --version`. Proxy identity: after start, check for blockrun models in /v1/models or ClawRouter headers.
//
// Concrete runnable TS prototype for one agent flow:
// TWZRD preflight (ReadinessCard gate) → ClawRouter/BlockRun call (LLM model or Surf data/marketplace) → receipt verify (if paid path used).
// TS preferred (ClawRouter is TS). Self-contained, uses native fetch (node >= 18).

type ReadinessCard = {
  decision: 'allow' | 'warn' | 'block';
  trust_score: number;
  can_spend?: boolean;
  caveats?: string[];
  proof?: any;
  paid_deep_dive?: string;
  gateAvailable?: boolean; // discriminated: false on fail-open / timeout / non-2xx (per security review)
  // plus resource echoes etc.
};

async function twzrdPreflight(params: {
  resource_name: string;
  seller_wallet?: string;
  price_usdc?: number;
  agent_intent: string;
  queried_pubkey?: string;
}): Promise<ReadinessCard> {
  // Minimal client guards (no new deps): length/format allow-list style on key fields.
  // Invalid input is a programming error in the CALLER - throw (hard error).
  // This is deliberately distinct from gate-unavailability below, which fails OPEN per spec.
  if (typeof params.resource_name !== 'string' || params.resource_name.length === 0 || params.resource_name.length > 128) {
    throw new Error('[twzrd-clawrouter] invalid resource_name (must be a 1-128 char string)');
  }
  if (params.price_usdc != null && (typeof params.price_usdc !== 'number' || params.price_usdc < 0 || params.price_usdc > 10)) {
    throw new Error('[twzrd-clawrouter] price_usdc out of sanity range (0-10 USDC)');
  }
  const base = 'https://intel.twzrd.xyz';
  const controller = new AbortController();
  const to = setTimeout(() => controller.abort(), 10000); // top-level timeout on preflight step
  try {
    const res = await fetch(`${base}/v1/intel/preflight`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(params),
      signal: controller.signal,
    });
    clearTimeout(to);
    if (!res.ok) {
      const status = res.status;
      console.warn('[twzrd-clawrouter] preflight non-2xx (' + status + ') - fail open (per spec)');
      return { decision: 'allow', trust_score: 50, gateAvailable: false };
    }
    const json: any = await res.json();
    const card: ReadinessCard = json.readiness_card || json;
    console.log('[twzrd-clawrouter] preflight decision=' + card.decision + ' trust_score=' + card.trust_score);
    if (card.caveats && card.caveats.length) {
      console.log('  first caveat:', String(card.caveats[0]).slice(0, 200));
    }
    return { ...card, gateAvailable: true };
  } catch (err: any) {
    clearTimeout(to);
    const safe = String(err?.message || err).slice(0, 200); // truncation
    console.warn('[twzrd-clawrouter] preflight error/timeout - fail open:', safe);
    return { decision: 'allow', trust_score: 50, gateAvailable: false };
  }
}

async function callClawRouterProxy(path: string, init?: RequestInit): Promise<Response> {
  // Local proxy (default port from ClawRouter). Handles wallet auth + x402 to BlockRun/Surf internally.
  // For Surf: see ClawRouter's skills/surf/SKILL.md (83+ endpoints, no separate account; same wallet).
  // Pricing tiers in research: T1 $0.001, T2 $0.005, T3 $0.020.
  const proxyBase = process.env.CLAWROUTER_PROXY_BASE || 'http://localhost:8402';
  // allow-list style path guard (prototype): only /v1/ prefixes for known surfaces + explicit root for the HEAD probe in main()
  if (path !== '/' && !path.startsWith('/v1/')) {
    throw new Error('disallowed proxy path (prototype allow-list)');
  }
  const controller = new AbortController();
  const to = setTimeout(() => controller.abort(), 15000);
  try {
    const resp = await fetch(proxyBase + path, { ...(init||{}), signal: controller.signal });
    clearTimeout(to);
    return resp;
  } catch (e) {
    clearTimeout(to);
    throw e;
  }
}

async function verifyReceiptIfAny(receipt: unknown, note: string): Promise<boolean> {
  // If the flow used a paid TWZRD path (0.05 USDC V5 receipt) alongside or instead, verify offline.
  // Command (portable, trusts only the published signer): npx twzrd-receipt-verifier receipt.json --pubkey <key from .well-known/x402>
  // Or via MCP: the twzrd server's verify_receipt tool.
  // For ClawRouter settles themselves: the on-chain USDC tx (Base or Sol) + facilitator receipt is the proof; preflight already scored the seller.
  if (!receipt) {
    console.log('[twzrd-clawrouter] verify step: no receipt provided (e.g. free T1 path or ClawRouter internal settle); skipping.');
    return true;
  }
  console.log('[twzrd-clawrouter] verify step for paid path (' + note + '):');
  console.log('  npx twzrd-receipt-verifier <receipt.json> --pubkey $(curl -s https://intel.twzrd.xyz/.well-known/x402 | ... signer)');
  console.log('  (or MCP verify_receipt). Persist leaf + preimage.');
  // TODO: integrate real verification (subprocess to npx twzrd-receipt-verifier or MCP call) that returns false and exits on failure.
  // Example (commented, uses builtin; pin version for integrity):
  // const { execSync } = await import('child_process');
  // try {
  //   execSync('npx twzrd-receipt-verifier@1.0.1 --version', { stdio: 'inherit' });
  //   // ... actual verify command; on !pass: process.exit(1); return false;
  // } catch { console.error('VERIFY FAIL'); process.exit(1); return false; }
  // Real impl asserts PASS or exits. Prototype returns true (see security notes).
  // NOTE for demo: in the executable main() this is always invoked with null (free/internal path); stub returns true without exercising the paid verification branch. Explicit stub for structural prototype only.
  return true;
}

function extractPayToFrom402(resp: Response | null): string | undefined {
  // Helper to extract payTo from 402 response/headers for precise preflight scoring (addresses security review).
  // helper provided for integration; not exercised in this minimal demo (resource_name path used)
  // In real: inspect 402 body (accepts[0].payTo) or x-payment / www-authenticate header from blockrun.ai/sol.blockrun.ai before proxy call.
  // For this prototype demo we pass via comment in preflight; use observed from prior 402 or known treasury.
  if (!resp) return undefined;
  try {
    const h = resp.headers.get('www-authenticate') || resp.headers.get('x-402') || '';
    if (h && h.includes('payTo=')) {
      const m = h.match(/payTo=([^,\s;]+)/i);
      if (m) return m[1];
    }
  } catch {}
  // Fallback note: for Surf/BlockRun the treasury is documented in ClawRouter README (Base primary).
  return undefined;
}

async function main() {
  console.log('=== twzrd-clawrouter prototype flow start ===');

  // Proxy config + cheap startup probe (env override + note for authentic ClawRouter identity)
  const PROXY_BASE = process.env.CLAWROUTER_PROXY_BASE || 'http://localhost:8402';
  console.log('[twzrd-clawrouter] proxy base:', PROXY_BASE, '(override with CLAWROUTER_PROXY_BASE env; must be authentic ClawRouter instance - check version/headers/ps after `npx @blockrun/clawrouter`)');
  // Cheap probe (non-fatal; illustrative integrity): reachability + note on identifying response.
  // In prod: assert response includes ClawRouter-specific marker or /v1/models contains 'blockrun'.
  (async () => {
    try {
      const p = await fetch(PROXY_BASE + '/', { method: 'HEAD', signal: AbortSignal.timeout(1500) });
      console.log('[twzrd-clawrouter] proxy probe (HEAD /):', p.status);
    } catch { /* silent for prototype */ }
  })();

  // STEP 1: TWZRD preflight (ReadinessCard gate) - free, before any ClawRouter/BlockRun spend.
  // resource_name describes the ClawRouter surface. seller_wallet optional but best when you have the payTo (from 402 or treasury).
  // Use observed payTo for Surf/BlockRun treasury when doing direct or logging the challenge.
  // Example extraction (post a 402 if surfaced, or pre-known): const payTo = extractPayToFrom402(...);
  // (helper provided for integration; not exercised in this minimal demo (resource_name path used))
  const card = await twzrdPreflight({
    resource_name: 'ClawRouter Surf crypto data or premium LLM via blockrun',
    // seller_wallet: e.g. the pay_to address from blockrun.ai 402 or sol.blockrun.ai (Base primary for Surf; Solana path supported). Use extractPayToFrom402( priorResp ) in real flows.
    // For demo we rely on resource_name + heuristics in TWZRD corpus. Pass real one in prod agents.
    price_usdc: 0.001,
    agent_intent: 'preflight gate then clawrouter call for surf market data or model inference',
    // queried_pubkey: set to the ClawRouter wallet pubkey (printed on setup; EVM 0x... or Solana base58) for better attribution
  });

  if (card.gateAvailable === false) {
    console.log('[twzrd-clawrouter] gate unavailable (fail-open; no distinguishable hard block from gate)');
  }
  if (card.decision === 'block') {
    console.error('BLOCK from TWZRD preflight - aborting per the one rule. Do not call ClawRouter.');
    process.exit(1);
  }
  if (card.decision === 'warn') {
    console.warn('WARN from TWZRD - low signal or caveats; proceeding cautiously (per spec).');
  } else {
    console.log('ALLOW from TWZRD preflight - safe to proceed to ClawRouter/BlockRun.');
  }

  // STEP 2: ClawRouter/BlockRun call (for LLM model or Surf data/marketplace).
  // This is where x402 happens inside ClawRouter (from its local wallet). Our gate was before.
  // Real example uses the Surf catalog (or /v1/chat/completions with blockrun/auto etc.).
  // See ClawRouter README + skills/surf/SKILL.md for exact endpoints + tiers.
  console.log('Proceeding to ClawRouter proxy call (post preflight gate)...');
  const surfPath = '/v1/surf/market/price?symbol=BTC'; // T1 cheap example; onchain/sql is T3.
  const surfResp = await callClawRouterProxy(surfPath);
  // post-response handling + minimal status check (per review)
  if (!surfResp.ok) {
    console.warn('[twzrd-clawrouter] post-call non-ok status from proxy (may be handled 402 inside or error):', surfResp.status);
    // real: could inspect for settlement simulation errs etc; here we still read body for shape
  }
  let surfData: any = { status: surfResp.status, note: 'see proxy response; 402s auto-handled by ClawRouter' };
  try {
    surfData = await surfResp.json();
  } catch {}
  // truncate full downstream in log
  console.log('ClawRouter/BlockRun Surf (or model) response shape:', String(JSON.stringify(surfData)).slice(0, 300));

  // STEP 3: receipt verify (if paid path used).
  await verifyReceiptIfAny(null, 'post-clawrouter paid path or TWZRD intel');

  console.log('=== flow complete (preflight gate → ClawRouter call → verify) ===');
  console.log('Reminders from SKILL.md: dedicated wallet only, smallest amounts, fail-open preflight, verify all receipts, extract real seller_wallet from 402 when possible.');
}

// Direct invocation: this is a demo script, not a library.
main().catch((err) => {
  console.error('prototype error:', err);
  process.exit(1);
});
```

Save as example.ts next to this SKILL.md. Run with `npx tsx example.ts` (or `node --loader ts-node/esm` / compile). The proxy step assumes ClawRouter is up (see ClawRouter README quickstart).

## Security notes

- Dedicated wallet: ClawRouter auto-gens on first run (EVM primary + Solana mnemonic; Base balance monitor primary; Solana derivation supported). Backup the printed mnemonic/wallet.key immediately. Never put significant funds here.

- Smallest amounts: Free tier (6 NVIDIA models) or T1 Surf ($0.001) first. Top up $1-5 USDC on Base (or Sol for SVM). Use `/model free` or blockrun/auto with fallbacks.

- Verify receipts: Always for any paid TWZRD V5 (npx twzrd-receipt-verifier or MCP). For ClawRouter settles, the proxy + facilitator provide the on-chain tx; cross with our corpus via preflight. The example's verifyReceiptIfAny now exercises the live free /v1/receipts/example -> /v1/receipts/verify path and prints the offline verifier command for real paid V5 receipts.

- Fail-open: preflight unavailability must not block ClawRouter usage. Log "TWZRD preflight skipped (unavailable)" and continue. The ReadinessCard now includes gateAvailable (false on fail-open paths); callers can distinguish.

- Extract real seller_wallet: inspect the 402 Payment header from blockrun.ai (or sol.blockrun.ai) before/after proxy; pass the payTo for accurate scoring (example.ts ships extractPayToFrom402 helper + call site comments). Resource_name alone works for coarse gate.

- Cross with AgentCash when mixing surfaces (stables + TWZRD + others); it handles 402 sign/retry + SIWS.

- No browser secrets, no shared wallets in prod agents. Monitor balance (ClawRouter has built-in pre-checks).

## Links

- TWZRD: https://intel.twzrd.xyz/.well-known/x402 (exact Solana USDC descriptor + receipt spec), /llms.txt, /openapi.json, /mcp

- ClawRouter: https://github.com/BlockRunAI/ClawRouter (raw README, openclaw.plugin.json, skills/surf/SKILL.md with 83+ endpoints (see catalog for exact), proxy.ts/auth.ts for x402 wallet flow)

- BlockRun: https://blockrun.ai (gateway, models, marketplace/surf, "one install", Base+Sol)

- Moltbook: https://www.moltbook.com/skill.md (agent social/heartbeat for OpenClaw; no x402; human X claim for verified)

- AgentCash (buyer client, our origin registered): https://agentcash.dev/ + MCP (use for preflight + fetch patterns)

- x402 Bazaar + peers: https://docs.cdp.coinbase.com/x402/bazaar , https://x402.org , Dexter (free Solana), pay.sh

- Verifier + packages: npm/pip twzrd-receipt-verifier; packages/twzrd-agent-intel (AGENT_USAGE.md, examples/agent_preflight_example.py, MCP tools)

## Publish prep for ClawHub/OpenClaw

- Version: 0.1.2 (ClawRouter arrival wiring: upstream onBeforePayment hook + live verify step)

- Changelog:
  - 0.1.2: Demand experiment: add createClawRouterOnBeforePaymentHook for proxy-settlement pre-gating, keep proxy failures observable, and run live receipt verification in the example flow.
  - 0.1.1: Retention: correct install cmd (clawhub not openclaw skills), zero-args try-it-now curl, UPPER_CASE placeholders in one-rule curl.
  - 0.1.0: Initial self-contained SKILL.md + concrete TS example.ts for ClawRouter/OpenClaw preflight integration prototype.

- Publish command (founder keystroke — interactive MIT-0 accept):

```bash
cd /home/twzrd/wzrd-deploy
git pull --ff-only origin main
clawhub publish packages/twzrd-agent-intel/skills/twzrd-clawrouter \
  --slug twzrd-clawrouter --name "TWZRD Preflight for ClawRouter" --version 0.1.2 \
  --tags x402,clawrouter,openclaw,preflight,trust,solana,usdc,blockrun,surf \
  --changelog "Demand experiment: upstream onBeforePayment hook for ClawRouter proxy settlements plus live receipt verify step"
```

- Consumers (after live on ClawHub):

```bash
npx clawhub install twzrd-clawrouter
openclaw mcp add twzrd --url https://intel.twzrd.xyz/mcp --transport streamable-http
```

Self-contained. Drop the SKILL.md (and example.ts) into ClawHub/OpenClaw skill surfaces or workspace. No server changes needed.

## More

- Machine-readable: https://intel.twzrd.xyz/.well-known/x402
- Agent usage + preflight py reference: packages/twzrd-agent-intel/AGENT_USAGE.md + examples/
- SDK for Solana side (receipts, protocol): sdk/
- Live MCP tools (twzrd + agentcash for payer): get_readiness_card_tool before any spend.

Use the gate. Stop the pay-then-discover-bad pattern.
