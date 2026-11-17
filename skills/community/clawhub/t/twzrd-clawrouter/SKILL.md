---
name: twzrd-clawrouter
description: |
  TWZRD Preflight for ClawRouter / BlockRun / OpenClaw. The independent pre-spend gate for agents using ClawRouter (for LLM models, Surf crypto data, Predexon, voice, image, etc.) or paying BlockRun.

  The one rule: Before using ClawRouter or paying BlockRun, call free TWZRD preflight
  (decision=block → abort) and free merchant_card (wash_flagged → do not pay).

  Composes with AgentCash or direct; Solana-native receipt proof after. Use before any x402 spend through ClawRouter proxy or BlockRun gateway.

  WHAT YOU GET FREE: ReadinessCard (allow / warn / block + trust_score + caveats) from Solana x402 payer graph before routing spend.
  PAID (x402, USDC on Solana): full trust + portable Ed25519-signed v6 receipt (when querying TWZRD intel alongside).
  TRIGGERS: clawrouter preflight, blockrun spend gate, surf data safe, openclaw before pay, pre clawrouter, x402 router gate, blockrun trust, preflight claw
homepage: https://intel.twzrd.xyz
metadata:
  version: "0.2.1"
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

1. Call free TWZRD preflight.
2. If `decision=block`, abort.
3. If you know the `payTo` / `seller_wallet`, call free `merchant_card`. If `wash_flagged: true`, do not pay.
4. Otherwise execute `next_action.command` (do not stop after the free card).

Both checks are the rule, not just the first. `example.ts` implements both as of 0.2.1; through 0.2.0 it performed only step 1 while this document called both mandatory.


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

Also returned: `trust_score` (0-100), `caveats[]`, `proof`, `can_spend`. Gate strictly on `decision=block`. Free tier is conservative (many wallets default warn/can_spend=false). On preflight unavailability (timeout / non-2xx / error) the default `enforce` mode returns `decision=block` with `gateAvailable: false` - an outage stops the spend. Pass `{ mode: 'advisory' }` to proceed instead; every bypass logs `TWZRD-GATE-BYPASS`.

When you have `seller_wallet` / payTo, also:

```bash
curl -s "https://intel.twzrd.xyz/v1/intel/merchant_card/SELLER_WALLET_FROM_402_RESPONSE"
```

**Default:** `wash_flagged: true` → do not pay. If the card is unreachable, treat it as unresolved: `enforce` blocks, `advisory` proceeds and logs the bypass.
`twzrd-x402-gate` enforces this by default (`refuseWashFlagged: true`).

## Exact preflight usage (HTTP + MCP)

HTTP (no auth, as shown in the one rule; base https://intel.twzrd.xyz):

- POST /v1/intel/preflight (resource_name and/or seller_wallet required for good signal; price_usdc and agent_intent recommended).

- GET /v1/intel/score_wallet_for_intel , get_top_intel_agents, get_counterparties, get_facilitator_footprint, compare_wallets, score_wallets_batch.

- GET /v1/intel/trust/{pubkey}?seller_wallet=... (paid 0.05 USDC on Solana; returns full model + v6 receipt).

MCP (streamable-http, recommended for agents):

- https://intel.twzrd.xyz/mcp

- Primary tool: get_readiness_card_tool (resource_name, seller_wallet, agent_intent, price_usdc, queried_pubkey)

- Also: verify_receipt, get_provider_reputation, get_merchant_card, low_level_preflight, etc. (full list: read tools/list).

OpenClaw: `openclaw mcp add twzrd --url https://intel.twzrd.xyz/mcp --transport streamable-http`

AgentCash registers intel.twzrd.xyz (the trust + paid /v1/intel/* surface) -- use its MCP/CLI for mixed stables + TWZRD + preflight patterns; see AGENT_USAGE.md. Note: api.twzrd.xyz is the private protocol backend and does NOT expose the paid trust endpoints; agents discover/pay via intel.twzrd.xyz.

## Composition

- Call TWZRD preflight first (free) for the intended ClawRouter resource (e.g. "ClawRouter Surf", "BlockRun premium model", "blockrun voice").

- If not block, proceed to ClawRouter local proxy call (OpenAI compat or direct /v1/surf/* or /v1/images etc.). ClawRouter handles its internal x402 to BlockRun treasury from the local wallet (EVM or Solana-derived via setup).

- Works with AgentCash (unified payer) or direct (@x402/fetch in custom, or ClawRouter's bundled).

- After a paid path (especially if you paid TWZRD for intel or have a settle receipt): verify with offline tool or MCP verify_receipt. Receipts are portable Ed25519 v6 anchored to Solana USDC (PayAI primary facilitator for our Solana proof). (example provides `verifyReceipt(receipt, note)`, which verifies the receipt you pass and fails closed, plus the sample-only `demoVerifySampleReceipt()` and the `extractPayToFrom402` helper (with usage comments; preflight demo relies on resource_name, extraction shown as illustrative for prod))

- Post-spend: store any receipt leaf for later root_provenance or independent audit if mixed with WZRD protocol.

## Concrete runnable TS/JS example (full flow)

The committed prototype lives in sibling `example.ts`. It now wires the full demand-facing loop (from funnel-join #739):

- preflight gate (ReadinessCard + enforce-by-default + block abort)
- `twzrdMerchantCard()` wash refuse - step 2 of the one rule, wired into the exported hook so a `wash_flagged` merchant is refused before any spend (enforce mode also refuses an unresolved card; `in_corpus: false` is not a refusal)
- exported `createClawRouterOnBeforePaymentHook()` — an app-level pre-pay adapter for ClawRouter proxy settlements (addresses the gap noted in openclaw-twzrd-preflight where sign happens inside 8402, invisible to tool hooks). Upstream reality check (2026-07-23): ClawRouter exposes NO such registration — our generic `startProxy({ beforePayment })` seam (BlockRunAI/ClawRouter PR #205) was closed unmerged 2026-07-15 (they prefer native `spend-control.ts`, which models amount windows only, no counterparty dimension). Until a seam lands, call this hook explicitly in agent code BEFORE invoking the proxy; it cannot intercept the signing inside 8402. Refreshed re-file artifacts: docs/strategy/clawrouter/ (founder-gated, unfiled)
- ClawRouter/BlockRun proxy call
- `verifyReceipt(receipt, note)` - verifies the receipt you pass, fails closed on null/malformed/failed/unreachable; plus the offline CLI command for real receipts. `demoVerifySampleReceipt()` is the separate sample-only path and is not payment proof

Run: `npx tsx example.ts` (needs proxy up for the call step, but preflight + hook + verify are self-contained and hit live surfaces).

Update both SKILL.md and example.ts when evolving the flow. Status: executable prototype that demonstrates a non-twzrd (ClawRouter) agent hitting the TWZRD gate.

```ts
// example.ts
// Run: npx tsx example.ts   (or ts-node, or compile to .mjs)
// Requires: ClawRouter proxy up for the call step (npx @blockrun/clawrouter or via OpenClaw + clawrouter setup).
// See sibling SKILL.md for full docs, one rule, security, publish command, links.
// This file + SKILL.md = the publishable prototype (keep both copies of the flow in sync).
// Integrity: pin verifier (check npm tarball shasum). JS (npx) 1.3.1+ has full security bounds + V6; Python (pip) at 1.2.4 is partial. See docs/audits/2026-08-02-receipt-verifier-reconciliation.md
//
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

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
  gateAvailable?: boolean; // false when the gate could not be reached (timeout / non-2xx / error)
  gateError?: string;      // short reason when gateAvailable === false
  // plus resource echoes etc.
};

/**
 * Gate mode. Default is 'enforce'.
 *
 *   enforce  - the gate is a spend-authorizing control. If it cannot be reached,
 *              the decision is `block`. An outage stops spending; it does not
 *              silently permit it.
 *   advisory - the gate is informational. If it cannot be reached the call is
 *              allowed and every bypass is logged with a TWZRD-GATE-BYPASS audit
 *              line. Opt in explicitly; never the default.
 *
 * This used to fail open unconditionally, which meant a timeout, a DNS blip, or
 * any non-2xx silently produced `decision: 'allow'` on a path documented as a
 * mandatory pre-spend gate. A control that permits the action it exists to
 * gate whenever it is unavailable is not a control.
 */
export type GateMode = 'enforce' | 'advisory';

async function twzrdPreflight(params: {
  resource_name: string;
  seller_wallet?: string;
  price_usdc?: number;
  agent_intent: string;
  queried_pubkey?: string;
}, options: { mode?: GateMode; endpoint?: string } = {}): Promise<ReadinessCard> {
  const mode: GateMode = options.mode ?? 'enforce';

  // Gate could not be reached. Shape the result from the mode, never from convenience.
  const unreachable = (why: string): ReadinessCard => {
    if (mode === 'advisory') {
      console.warn(
        '[twzrd-clawrouter] TWZRD-GATE-BYPASS advisory mode: preflight unavailable (' + why + '), allowing unverified spend'
      );
      return { decision: 'allow', trust_score: 50, gateAvailable: false, gateError: why };
    }
    console.error('[twzrd-clawrouter] preflight unavailable (' + why + ') - blocking (mode=enforce)');
    return { decision: 'block', trust_score: 0, can_spend: false, gateAvailable: false, gateError: why };
  };

  // Minimal client guards (no new deps): length/format allow-list style on key fields.
  // Invalid input is a programming error in the CALLER - throw (hard error).
  // This is deliberately distinct from gate-unavailability below, which fails OPEN per spec.
  if (typeof params.resource_name !== 'string' || params.resource_name.length === 0 || params.resource_name.length > 128) {
    throw new Error('[twzrd-clawrouter] invalid resource_name (must be a 1-128 char string)');
  }
  if (params.price_usdc != null && (typeof params.price_usdc !== 'number' || params.price_usdc < 0 || params.price_usdc > 10)) {
    throw new Error('[twzrd-clawrouter] price_usdc out of sanity range (0-10 USDC)');
  }
  const base = options.endpoint ?? 'https://intel.twzrd.xyz';
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
      return unreachable('non-2xx ' + res.status);
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
    return unreachable('error/timeout: ' + safe);
  }
}

type MerchantCard = {
  wash_flagged?: boolean;
  in_corpus?: boolean;
  cardAvailable?: boolean; // false when the card could not be fetched
  cardError?: string;
};

/**
 * Step 2 of the one rule: free merchant_card, `wash_flagged` -> do not pay.
 *
 * This step was documented from 0.1.0 and never implemented. SKILL.md states a
 * two-step gate (preflight AND merchant_card) as mandatory before any spend,
 * while the example performed preflight only and went straight to the payment
 * path. A reader following the example paid counterparties the documentation
 * says to refuse.
 *
 * `in_corpus: false` is NOT a block - most wallets are not in the corpus. Only
 * `wash_flagged === true` refuses. An unreachable card is unresolved, and
 * unresolved is a block in enforce mode.
 */
async function twzrdMerchantCard(
  wallet: string,
  options: { mode?: GateMode; endpoint?: string } = {}
): Promise<MerchantCard> {
  const mode: GateMode = options.mode ?? 'enforce';
  const base = options.endpoint ?? 'https://intel.twzrd.xyz';

  try {
    const res = await fetch(`${base}/v1/intel/merchant_card/${encodeURIComponent(wallet)}`, {
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error('non-2xx ' + res.status);
    const json: any = await res.json();
    const card = json.merchant_card || json;
    return {
      wash_flagged: card.wash_flagged === true,
      in_corpus: card.in_corpus === true,
      cardAvailable: true,
    };
  } catch (err: any) {
    const why = String(err?.message || err).slice(0, 120);
    if (mode === 'advisory') {
      console.warn('[twzrd-clawrouter] TWZRD-GATE-BYPASS advisory mode: merchant_card unavailable (' + why + '), wash status unresolved');
      return { cardAvailable: false, cardError: why };
    }
    console.error('[twzrd-clawrouter] merchant_card unavailable (' + why + ') - treating as unresolved and blocking (mode=enforce)');
    return { cardAvailable: false, cardError: why };
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

/**
 * Verify a receipt you actually received. Fails closed.
 *
 * This previously ignored its `receipt` argument entirely and verified a
 * public sample receipt fetched from /v1/receipts/example instead, then
 * returned `true` from its catch block. So it reported PASS whether or not the
 * caller's real receipt was valid, and reported PASS when verification could
 * not run at all. Any caller treating it as proof of payment was verifying
 * known-good data supplied by us, not the artifact from their transaction.
 *
 * Returns true only when the supplied receipt verifies. Null, malformed, a
 * failed verify, and an unreachable verifier all return false.
 */
async function verifyReceipt(
  receipt: unknown,
  note: string,
  options: { endpoint?: string } = {}
): Promise<boolean> {
  const base = options.endpoint ?? 'https://intel.twzrd.xyz';

  if (receipt == null || typeof receipt !== 'object') {
    console.error('[twzrd-clawrouter] verify (' + note + '): no receipt supplied - FAIL (nothing was verified)');
    return false;
  }

  try {
    const vres = await fetch(`${base}/v1/receipts/verify`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ twzrd_receipt: receipt }),
      signal: AbortSignal.timeout(10000),
    });
    if (!vres.ok) {
      console.error('[twzrd-clawrouter] verify (' + note + '): verifier non-2xx ' + vres.status + ' - FAIL');
      return false;
    }
    const vjson: any = await vres.json();
    const ok = !!vjson?.ok;
    console.log('  /receipts/verify result:', ok ? 'PASS' : 'FAIL');
    if (!ok) return false;

    console.log('  Offline equivalent: npx twzrd-receipt-verifier@^1.3.0 <receipt.json> --pubkey 9V6Pn19kiUA5Rn6JpQfNduanvGt2aXGwsarosNfa2Ldf');
    console.log('  (or MCP twzrd verify_receipt). Always persist leaf + preimage.');
    return true;
  } catch (e: any) {
    // Fail closed. An unreachable verifier is an unverified receipt, not a valid one.
    console.error('[twzrd-clawrouter] verify (' + note + ') could not complete - FAIL:', String(e?.message || e).slice(0, 120));
    return false;
  }
}

/**
 * Demo only. Fetches the public sample receipt and verifies it, to show the
 * call shape when you have no real receipt to hand.
 *
 * Deliberately named so it cannot be mistaken for verifying a caller's
 * receipt. Do not wire this into a payment path: it proves our sample is
 * well-formed and nothing about your transaction.
 */
async function demoVerifySampleReceipt(options: { endpoint?: string } = {}): Promise<boolean> {
  const base = options.endpoint ?? 'https://intel.twzrd.xyz';
  try {
    const ex = await fetch(`${base}/v1/receipts/example`, { signal: AbortSignal.timeout(10000) });
    if (!ex.ok) throw new Error('example receipt fetch failed');
    const exJson: any = await ex.json();
    const sampleReceipt = exJson.twzrd_receipt || exJson;
    console.log('[twzrd-clawrouter] DEMO verify of the public sample receipt (not a payment proof):');
    return await verifyReceipt(sampleReceipt, 'public sample', { endpoint: base });
  } catch (e: any) {
    console.error('[twzrd-clawrouter] demo sample verify could not complete:', String(e?.message || e).slice(0, 120));
    return false;
  }
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

/**
 * ClawRouter pre-pay adapter (app-level; the upstream seam does not exist yet).
 *
 * ClawRouter proxy settlements (signing inside localhost:8402) are invisible to OpenClaw
 * tool hooks. Call this explicitly in your agent flow before any callClawRouterProxy so a
 * non-twzrd agent hits the TWZRD preflight gate. It CANNOT intercept the signing inside
 * the proxy - upstream ClawRouter exposes no registration for that. Our generic
 * `startProxy({ beforePayment })` seam (BlockRunAI/ClawRouter PR #205) was closed unmerged
 * 2026-07-15; refreshed re-file artifacts live in docs/strategy/clawrouter/ (unfiled).
 *
 * Base caveat: the proxy pre-signs from a per-endpoint pre-auth cache on Base (no fresh 402
 * on cache hits), so fetch-level 402 sniffing goes blind there. The Solana leg skips
 * pre-auth (fresh 402 each payment) and stays sighted.
 *
 * Direct usage in agent code (as in main() below):
 *   const decision = await (await createClawRouterOnBeforePaymentHook())({ payTo, amount: 0.001, resource: '...' });
 *   if (!decision.allow) throw new Error(decision.reason);
 *
 * If the upstream seam lands, its contract is abort-shaped, not allow-shaped - adapt like:
 *   const hook = await createClawRouterOnBeforePaymentHook();
 *   await startProxy({
 *     beforePayment: async ({ selectedRequirements }) => {
 *       const d = await hook({ payTo: selectedRequirements.payTo,
 *         amount: Number(selectedRequirements.amount) / 1_000_000, resource: 'clawrouter x402' });
 *       if (!d.allow) return { abort: true, reason: d.reason };
 *     },
 *   });
 */
export async function createClawRouterOnBeforePaymentHook(
  options: { endpoint?: string; mode?: GateMode; failOpen?: boolean } = {}
) {
  const endpoint = options.endpoint ?? 'https://intel.twzrd.xyz';
  // `endpoint` and `failOpen` were previously destructured and then never used:
  // the hook always hit the hardcoded default endpoint, and `failOpen` did
  // nothing at all while defaulting to true. Both are now wired.
  // `failOpen: true` maps to advisory mode and is retained only for callers
  // that already pass it; prefer `mode`.
  const mode: GateMode = options.mode ?? (options.failOpen === true ? 'advisory' : 'enforce');
  return async function onBeforePayment(payment: {
    payTo?: string;
    amount?: string | number;
    resource?: string;
    metadata?: any;
  }) {
    const priceUsdc = typeof payment.amount === 'number'
      ? payment.amount
      : (typeof payment.amount === 'string' ? Number(payment.amount) : undefined);

    const card = await twzrdPreflight({
      resource_name: payment.resource || 'ClawRouter/BlockRun payment',
      seller_wallet: payment.payTo,
      price_usdc: priceUsdc && priceUsdc > 0 ? priceUsdc : undefined,
      agent_intent: 'clawrouter:onBeforePayment',
    }, { mode, endpoint });

    if (card.decision === 'block') {
      // In enforce mode an unreachable gate arrives here as a block, so an
      // outage stops the payment instead of waving it through.
      const why = card.gateAvailable === false
        ? `preflight unavailable (${card.gateError || 'unknown'}) and mode=enforce`
        : `${card.caveats?.[0] || 'low trust counterparty'}`;
      return {
        allow: false,
        reason: `TWZRD preflight block (trust_score=${card.trust_score}): ${why}`,
        card,
      };
    }
    // Step 2 of the one rule. Only runs when we know who is being paid; with no
    // payTo there is no merchant to look up, and preflight alone is the gate.
    let merchant: MerchantCard | undefined;
    if (payment.payTo) {
      merchant = await twzrdMerchantCard(payment.payTo, { mode, endpoint });

      if (merchant.wash_flagged === true) {
        return {
          allow: false,
          reason: `TWZRD merchant_card wash_flagged (${payment.payTo}): documented rule is do not pay`,
          card,
          merchant,
        };
      }
      if (merchant.cardAvailable === false && mode === 'enforce') {
        return {
          allow: false,
          reason: `TWZRD merchant_card unresolved (${merchant.cardError || 'unknown'}) and mode=enforce`,
          card,
          merchant,
        };
      }
    }

    // warn/allow, and merchant not wash_flagged. An unavailable preflight or
    // card can only reach here in advisory mode.
    const bypassed = card.gateAvailable === false || merchant?.cardAvailable === false;
    return {
      allow: true,
      card,
      merchant,
      note: bypassed
        ? 'ADVISORY BYPASS: preflight and/or merchant_card unavailable, spend not verified'
        : undefined,
    };
  };
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
    console.error('[twzrd-clawrouter] gate unavailable (' + (card.gateError || 'unknown') + '); enforce mode treats this as block');
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

  // STEP 1b: merchant_card - the SECOND half of the one rule, and the half this
  // example omitted through 0.2.0 while the docs called it mandatory.
  // Only runs when the payTo is known (use extractPayToFrom402 in real flows).
  const DEMO_PAY_TO = process.env.CLAWROUTER_DEMO_PAY_TO; // unset in the plain demo
  if (DEMO_PAY_TO) {
    const merchant = await twzrdMerchantCard(DEMO_PAY_TO);
    if (merchant.wash_flagged === true) {
      console.error('WASH FLAGGED merchant_card for ' + DEMO_PAY_TO + ' - do not pay. Aborting per the one rule.');
      process.exit(1);
    }
    if (merchant.cardAvailable === false) {
      console.error('merchant_card unresolved - enforce mode treats this as block. Aborting.');
      process.exit(1);
    }
    console.log('[twzrd-clawrouter] merchant_card clean (wash_flagged=false, in_corpus=' + merchant.in_corpus + ')');
  } else {
    console.log('[twzrd-clawrouter] no payTo in this demo, so step 2 (merchant_card) has nothing to look up. Set CLAWROUTER_DEMO_PAY_TO to exercise it. The exported hook always runs it when payTo is present.');
  }

  // Demo the exported ClawRouter-compatible onBeforePayment hook (the wiring for proxy flows at 8402).
  // This is what ClawRouter can call (or agent code before proxy) to hit the gate for settlements that
  // are invisible to OpenClaw tool hooks. Provides the upstream hook the openclaw-twzrd-preflight plugin notes as missing.
  const hook = await createClawRouterOnBeforePaymentHook();
  const hookRes = await hook({
    payTo: undefined,
    amount: 0.001,
    resource: 'ClawRouter Surf crypto data or premium LLM via blockrun',
  });
  console.log('[twzrd-clawrouter] onBeforePayment hook result:', hookRes.allow ? 'ALLOW' : 'BLOCK', hookRes.note || hookRes.reason || '');

  // STEP 2: ClawRouter/BlockRun call (for LLM model or Surf data/marketplace).
  // This is where x402 happens inside ClawRouter (from its local wallet). Our gate was before.
  // Real example uses the Surf catalog (or /v1/chat/completions with blockrun/auto etc.).
  // See ClawRouter README + skills/surf/SKILL.md for exact endpoints + tiers.
  console.log('Proceeding to ClawRouter proxy call (post preflight gate + hook)...');
  let surfData: any = { note: 'proxy step (may be unavailable in this env; preflight+hook+verify are the wired gate parts)' };
  try {
    const surfPath = '/v1/surf/market/price?symbol=BTC'; // T1 cheap example; onchain/sql is T3.
    const surfResp = await callClawRouterProxy(surfPath);
    // post-response handling + minimal status check (per review)
    if (!surfResp.ok) {
      console.warn('[twzrd-clawrouter] post-call non-ok status from proxy (may be handled 402 inside or error):', surfResp.status);
    }
    try {
      surfData = await surfResp.json();
    } catch {}
    console.log('ClawRouter/BlockRun Surf (or model) response shape:', String(JSON.stringify(surfData)).slice(0, 300));
  } catch (e: any) {
    console.log('[twzrd-clawrouter] proxy unavailable (expected in this env without running ClawRouter):', String(e?.message || e).slice(0, 80));
    // Continue to verify step — the gate wiring (preflight + hook + verify) is what matters for the demand experiment.
  }

  // (LLM example would be similar: POST /v1/chat/completions with model blockrun/..., apiKey x402 at proxy)
  // const chatResp = await callClawRouterProxy('/v1/chat/completions', { method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify({model: 'blockrun/auto', messages: [{role:'user', content: 'hi via gated clawrouter'}] }) });

  // STEP 3: receipt verify (wires the post-pay half of the funnel join into ClawRouter flow).
  // Pass the receipt you actually received. `verifyReceipt` fails closed on a
  // null/malformed receipt, a failed verify, and an unreachable verifier.
  // This demo holds no real receipt, so it runs the clearly-named sample demo
  // rather than passing null and reporting PASS.
  const realReceipt: unknown = null; // e.g. json.twzrd_receipt from a paid /v1/intel/trust call
  if (realReceipt != null) {
    const verified = await verifyReceipt(realReceipt, 'ClawRouter post-call + funnel verify step');
    if (!verified) {
      console.error('RECEIPT VERIFY FAILED - do not treat this spend as proven.');
      process.exit(1);
    }
  } else {
    console.log('[twzrd-clawrouter] no real receipt in this demo; sample demo only (proves nothing about a payment)');
    await demoVerifySampleReceipt();
  }

  console.log('=== flow complete (preflight gate -> ClawRouter call -> verify) ===');
  console.log('Reminders from SKILL.md: dedicated wallet only, smallest amounts, enforce-mode preflight (unreachable gate = block), verify every real receipt, extract real seller_wallet from 402 when possible.');
}

// Run the demo only when this file is executed directly, never on import.
//
// This file is BOTH a demo and a library: SKILL.md documents
// `createClawRouterOnBeforePaymentHook` as the integration point for agent
// code. Previously `main()` was called unconditionally at module load, so
// importing the hook ran the whole demo - live network calls to
// intel.twzrd.xyz, a proxy probe, and `process.exit(1)` if the demo's own
// preflight returned block. Importing a gate must not be able to terminate
// the process that imports it.
//
// The prior comment was right that `import.meta.main` is not portable (Bun /
// Deno / node >= 24.2 only, silently skipping main() on node 18/20/22). This
// uses the portable ESM idiom instead: compare argv[1] to this module's path,
// which works on every supported runtime.
const _isDirectRun = (() => {
  try {
    const entry = process.argv[1];
    if (!entry) return false;
    return fileURLToPath(import.meta.url) === resolve(entry);
  } catch {
    return false;
  }
})();

if (_isDirectRun) {
  main().catch((err) => {
    console.error('prototype error:', err);
    process.exit(1);
  });
}
```

Save as example.ts next to this SKILL.md. Run with `npx tsx example.ts` (or `node --loader ts-node/esm` / compile). The proxy step assumes ClawRouter is up (see ClawRouter README quickstart).

## Capabilities and permissions

This skill ships executable examples. Everything they can reach is listed here; there is nothing else.

**Network egress (allowlist).** The examples contact exactly these hosts:

| Host | Why | Auth |
|------|-----|------|
| `intel.twzrd.xyz` | `POST /v1/intel/preflight`, `GET /v1/intel/merchant_card/*`, `POST /v1/receipts/verify`, `GET /v1/receipts/example` | none (free tier, no key) |
| `$CLAWROUTER_PROXY_BASE` (default `http://localhost:8402`) | the local ClawRouter proxy call step | wallet auth handled inside the proxy |

Paid TWZRD routes (`/v1/intel/trust`, `/v1/intel/quick`) are x402 and are **not** called by these examples.

**Environment.** One variable, read once, never transmitted:

- `CLAWROUTER_PROXY_BASE` - overrides the local proxy base URL. Point it only at a proxy you run. It is a request destination, so treating it as untrusted input is the whole reason the path allowlist below exists.

**No secret access.** The examples read no wallet key, mnemonic, seed, private key, or API token, and no other environment variable. TWZRD's free tier needs no credential. Signing happens inside ClawRouter, not here.

**Local constraints.** Proxy paths are allowlisted to `/` and `/v1/*`. Preflight has a 10s timeout, proxy calls 15s, receipt verify 10s. Wallet addresses passed to preflight are public chain identifiers.

**What this skill cannot do.** It cannot move funds, sign a transaction, or authorize a payment. It returns a decision; enforcing it is the caller's job. See the gate-mode note below for what happens when the gate cannot be reached.

## Security notes

- Dedicated wallet: ClawRouter auto-gens on first run (EVM primary + Solana mnemonic; Base balance monitor primary; Solana derivation supported). Backup the printed mnemonic/wallet.key immediately. Never put significant funds here.

- Smallest amounts: Free tier (6 NVIDIA models) or T1 Surf ($0.001) first. Top up $1-5 USDC on Base (or Sol for SVM). Use `/model free` or blockrun/auto with fallbacks.

- Verify receipts: Always for any paid TWZRD v6 (npx twzrd-receipt-verifier or MCP). For ClawRouter settles, the proxy + facilitator provide the on-chain tx; cross with our corpus via preflight. `verifyReceipt(receipt, note)` verifies the receipt **you pass it** and fails closed: a null or malformed receipt, a failed verify, and an unreachable verifier all return `false`. The separate `demoVerifySampleReceipt()` fetches our public sample and proves only that the sample is well-formed - it says nothing about your payment, so never wire it into a payment path.

  Corrected in 0.2.0: through 0.1.4 the example's `verifyReceiptIfAny` ignored its `receipt` argument, verified our public sample instead, and returned `true` from its catch block. It therefore reported PASS whether or not the caller's real receipt was valid, and reported PASS when verification could not run at all.

- Gate mode: `enforce` (default) or `advisory`. In **enforce**, an unreachable gate (timeout, non-2xx, network error) yields `decision: 'block'` - an outage stops spending rather than silently permitting it. In **advisory**, the call proceeds and every bypass logs a `TWZRD-GATE-BYPASS` line. Opt into advisory explicitly; it is never the default. `ReadinessCard.gateAvailable` is `false` on those paths and `gateError` carries the reason.

  Changed in 0.2.0: earlier versions failed **open** unconditionally, so any timeout or non-2xx produced `decision: 'allow'` on a path this document calls a mandatory pre-spend gate. A control that permits the action it exists to gate whenever it is unavailable is not a control. If you depend on the old behavior, pass `{ mode: 'advisory' }` deliberately.

- Extract real seller_wallet: inspect the 402 Payment header from blockrun.ai (or sol.blockrun.ai) before/after proxy; pass the payTo for accurate scoring (example.ts ships extractPayToFrom402 helper + call site comments). Resource_name alone works for coarse gate.

- Base pre-auth cache blind spot: ClawRouter caches payment requirements per endpoint on Base (payment-preauth.ts) and pre-signs + attaches the payment header on the FIRST request — no 402 round trip. Any fetch-level 402 interceptor (including extractPayToFrom402 on responses) goes blind on that cached path. The Solana leg sets skipPreAuth (per-tx blockhashes expire ~60-90s), so it surfaces a fresh 402 every time — that is the sighted leg. Only a client-level onBeforePaymentCreation hook inside the proxy (the unmerged #205 seam) sees every signature on both chains; until then, gate BEFORE the proxy call and prefer known payTo (BlockRun treasury) over 402 sniffing on Base.

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

- Version: 0.2.1 (the example now implements BOTH halves of the one rule: preflight AND merchant_card wash refuse)

- Changelog:
  - 0.2.1: Implement step 2 of the one rule. This document has stated a two-step mandatory gate since 0.1.0 - free preflight AND free merchant_card (`wash_flagged` -> do not pay) - but `example.ts` only ever called preflight and then proceeded to the payment path. It never fetched merchant_card at all, so anyone following the example paid counterparties this document says to refuse. Caught by the ClawHub scanner on 0.2.0 (TP4, HIGH, confidence 0.93) after the 0.2.0 pass fixed the other five findings. `twzrdMerchantCard()` is added and wired into `createClawRouterOnBeforePaymentHook`: `wash_flagged: true` refuses, and in enforce mode an unreachable card is unresolved and therefore also refuses. `in_corpus: false` does not refuse - most wallets are not in the corpus. Verified: a wash-flagged merchant is now refused where 0.2.0 allowed it, and the clean warn control still passes.
  - 0.2.0: Security pass on findings from the ClawHub scanner (0.1.2 scored CRITICAL / DO_NOT_INSTALL, 5 issues). **Breaking:** preflight now fails **closed**. An unreachable gate (timeout / non-2xx / network error) returns `decision=block` instead of `allow`; pass `{ mode: 'advisory' }` for the old behavior, which logs `TWZRD-GATE-BYPASS` on every bypass. `verifyReceiptIfAny` is replaced by `verifyReceipt(receipt, note)`, which verifies the receipt you pass and returns `false` on null/malformed/failed-verify/unreachable-verifier - the old function ignored its argument, verified our public sample, and returned `true` from its catch block. Sample-only checking moved to the clearly-named `demoVerifySampleReceipt()`. `createClawRouterOnBeforePaymentHook` now actually uses its `endpoint` option and its `failOpen` option, both of which were previously destructured and discarded. Added a Capabilities and permissions section declaring network allowlist, the single env var, and the absence of secret access. The `example.ts` copy embedded in this document is now byte-identical to the sibling file rather than an abridged snapshot that drifted. Also found while testing the above, not reported by the scanner: `main()` was invoked unconditionally at module load, so `import { createClawRouterOnBeforePaymentHook }` - the integration path this document recommends - ran the whole demo, made live network calls, and could `process.exit(1)` the importing process when the demo's own preflight returned block. The demo now runs only on direct execution, via an argv comparison that works on node 18/20/22 (the prior comment was right that `import.meta.main` is not portable).
  - 0.1.3: Reality sync vs ClawRouter main (0.12.x): mark createClawRouterOnBeforePaymentHook as app-level (upstream startProxy beforePayment seam = PR #205, closed unmerged 2026-07-15); document the Base pre-auth cache blind spot for fetch-level 402 gates (Solana skipPreAuth leg stays sighted); correct example.ts registration comments to the real {abort} contract shape.
  - 0.1.2: Demand experiment: add createClawRouterOnBeforePaymentHook for proxy-settlement pre-gating, keep proxy failures observable, and run live receipt verification in the example flow. **Correction (0.2.0):** the receipt-verification claim in this entry was false. The step ran a live call, but against our own public sample receipt - it ignored the caller's receipt and returned success on error. It verified nothing about any real payment. Corrected in 0.2.0.
  - 0.1.1: Retention: correct install cmd (clawhub not openclaw skills), zero-args try-it-now curl, UPPER_CASE placeholders in one-rule curl.
  - 0.1.0: Initial self-contained SKILL.md + concrete TS example.ts for ClawRouter/OpenClaw preflight integration prototype.

- Publish command (founder keystroke — interactive MIT-0 accept):

```bash
cd /home/twzrd/wzrd-deploy
git pull --ff-only origin main
clawhub publish packages/twzrd-agent-intel/skills/twzrd-clawrouter \
  --slug twzrd-clawrouter --name "TWZRD Preflight for ClawRouter" --version 0.2.0 \
  --tags x402,clawrouter,openclaw,preflight,trust,solana,usdc,blockrun,surf \
  --changelog "Security pass: preflight fails closed by default (unreachable gate = block, advisory mode is opt-in and audited); verifyReceipt verifies the caller's receipt and fails closed instead of always-passing on our own sample; capabilities and network allowlist declared; embedded example.ts synced byte-for-byte"
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
