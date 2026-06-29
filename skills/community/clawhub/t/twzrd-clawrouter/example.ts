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
  // Wires the "after pay → verify" half of the funnel (from #739 join work) into the ClawRouter flow.
  // For ClawRouter's own settles: on-chain USDC tx + facilitator receipt is the proof; preflight scored the seller.
  // For any TWZRD paid intel used in the same session (e.g. /v1/intel/trust for deep trust), verify the V5 receipt.
  //
  // Real implementation: fetch the free public example receipt (stand-in for a post-pay V5), POST to the
  // live free /v1/receipts/verify (or use npx twzrd-receipt-verifier / MCP verify_receipt for offline).
  // Persist leaf+preimage in prod. This exercises a live verify call as part of the gated ClawRouter path.
  console.log('[twzrd-clawrouter] verify step for paid path / sample (' + note + '):');

  try {
    // Fetch the canonical free example receipt (zero-wallet sample from the public surface; models a real V5 after pay).
    const ex = await fetch('https://intel.twzrd.xyz/v1/receipts/example');
    if (!ex.ok) throw new Error('example receipt fetch failed');
    const exJson: any = await ex.json();
    const sampleReceipt = exJson.twzrd_receipt || exJson;

    // Real server-side verify (free, no x402). In prod use the offline verifier for air-gapped / portable.
    const vres = await fetch('https://intel.twzrd.xyz/v1/receipts/verify', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ twzrd_receipt: sampleReceipt }),
    });
    const vjson: any = await vres.json();
    const ok = !!vjson?.ok;
    console.log('  live /receipts/verify result:', ok ? 'PASS' : 'FAIL', vjson);
    if (!ok) {
      console.error('VERIFY FAIL on sample receipt');
      return false;
    }

    // Also surface the offline CLI command for the agent to run on real receipts they receive.
    console.log('  For real paid receipts: npx twzrd-receipt-verifier@1.0.5 <receipt.json> --pubkey 9V6Pn19kiUA5Rn6JpQfNduanvGt2aXGwsarosNfa2Ldf');
    console.log('  (or MCP twzrd verify_receipt). Always persist leaf + preimage.');
    return true;
  } catch (e: any) {
    console.warn('[twzrd-clawrouter] verify step error (fail open for prototype):', String(e?.message || e).slice(0, 120));
    // In a strict agent: process.exit(1) on !ok. Prototype logs and continues (consistent with fail-open preflight).
    return true;
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
 * ClawRouter onBeforePayment compatible hook (the missing upstream piece for proxy settlements).
 *
 * ClawRouter proxy settlements (signing inside localhost:8402) are invisible to OpenClaw
 * tool hooks. Wire this as the onBeforePayment (or call it explicitly in your agent flow
 * before any callClawRouterProxy) so a non-twzrd agent hits the TWZRD preflight gate.
 *
 * Usage (when ClawRouter exposes onBeforePayment):
 *   const hook = await createClawRouterOnBeforePaymentHook();
 *   clawrouter.onBeforePayment(hook);  // or equivalent registration
 *
 * Or direct in agent code (as in main() below):
 *   const decision = await (await createClawRouterOnBeforePaymentHook())({ payTo, amount: 0.001, resource: '...' });
 *   if (!decision.allow) throw new Error(decision.reason);
 */
export async function createClawRouterOnBeforePaymentHook(options: { endpoint?: string; failOpen?: boolean } = {}) {
  const { endpoint = 'https://intel.twzrd.xyz', failOpen = true } = options;
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
    });

    if (card.decision === 'block') {
      return {
        allow: false,
        reason: `TWZRD preflight block (trust_score=${card.trust_score}): ${card.caveats?.[0] || 'low trust counterparty'}`,
        card,
      };
    }
    // warn/allow or fail-open (gateAvailable=false) → allow with note
    return {
      allow: true,
      card,
      note: card.gateAvailable === false ? 'fail-open (preflight unavailable)' : undefined,
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
  // The function now actually fetches the live free /v1/receipts/example and calls /v1/receipts/verify
  // (real server verify, free). In prod: run on real V5 receipts from paid /trust or other TWZRD intel,
  // plus use offline npx twzrd-receipt-verifier for portable proof. ClawRouter settles use their on-chain tx.
  await verifyReceiptIfAny(null, 'ClawRouter post-call + funnel verify step');

  console.log('=== flow complete (preflight gate → ClawRouter call → verify) ===');
  console.log('Reminders from SKILL.md: dedicated wallet only, smallest amounts, fail-open preflight, verify all receipts, extract real seller_wallet from 402 when possible.');
}

// Direct invocation: this is a demo script, not a library.
// Do NOT gate on import.meta.main - it is Bun/Deno/node>=24.2 only and silently
// skips main() on node 18/20/22 (the stated supported runtimes).
main().catch((err) => {
  console.error('prototype error:', err);
  process.exit(1);
});
