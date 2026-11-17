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
