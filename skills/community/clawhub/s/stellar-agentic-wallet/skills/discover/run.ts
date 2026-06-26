/**
 * discover — query the MPP Router service catalog.
 *
 * Usage:
 *   npx tsx skills/discover/run.ts
 *   npx tsx skills/discover/run.ts --category search
 *   npx tsx skills/discover/run.ts --query "web search"
 *   npx tsx skills/discover/run.ts --query "scrape" --pick-one
 *   npx tsx skills/discover/run.ts --json
 *
 * Takes no authentication. All config is hardcoded in the library.
 */

import {
  fetchCatalog,
  scoreService,
  type ServiceRecord,
} from "../../scripts/src/mpprouter-client.js";

/**
 * Label for `verified_mode`, used in both text and JSON output so users
 * can see whether a service has been verified to work end-to-end on
 * Stellar charge flow.
 *
 * - "charge" → green, known-working with this skill
 * - "session" → yellow, upstream is session-only; Stellar charge-mode
 *   client will pay but upstream rejects the receipt (pay-but-404).
 *   See references/session-mode-status.md for the list of affected
 *   services and tracking status.
 * - anything else (including unset / literal "false") → grey, untested
 *   but not known-broken. Majority of the 489-service catalog lives
 *   here today; most work but we can't prove it without a paid probe.
 */
/**
 * Coerce the catalog's free-form `price` string ("$0.01", "0.01 USDC",
 * "$0.005 per call", etc.) into a decimal USDC string that pay-per-call
 * can feed into --expect-amount.
 *
 * If the price isn't recognizable (e.g. "varies", "see docs"), returns
 * undefined — consumers should skip amount validation in that case
 * rather than guess.
 */
function parsePriceToUsdc(price: string | undefined): string | undefined {
  if (!price) return undefined;
  const m = price.match(/([0-9]+(?:\.[0-9]+)?)/);
  if (!m) return undefined;
  const n = parseFloat(m[1]);
  if (!Number.isFinite(n) || n < 0) return undefined;
  return n.toFixed(7);
}

function modeLabel(
  mode: string | undefined,
): { tag: string; human: string } {
  if (mode === "charge") return { tag: "charge", human: "✓ verified charge" };
  if (mode === "session")
    return { tag: "session", human: "⚠ session-only (charge flow fails after payment — awaiting router fix)" };
  return { tag: "unverified", human: "· unverified (not labeled by router; usually works)" };
}

interface CliOpts {
  category?: string;
  query?: string;
  pickOne: boolean;
  json: boolean;
}

function parseArgs(): CliOpts {
  const args = process.argv.slice(2);
  const result: CliOpts = { pickOne: false, json: false };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--category") result.category = args[++i];
    else if (a === "--query") result.query = args[++i];
    else if (a === "--pick-one") result.pickOne = true;
    else if (a === "--json") result.json = true;
  }
  return result;
}

function applyFilters(
  services: ServiceRecord[],
  opts: CliOpts,
): ServiceRecord[] {
  let out = services.filter((s) => s.status === "active");
  if (opts.category) {
    out = out.filter(
      (s) => s.category.toLowerCase() === opts.category!.toLowerCase(),
    );
  }
  if (opts.query) {
    out = out
      .map((s) => ({ s, score: scoreService(s, opts.query!) }))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .map((x) => x.s);
  }
  if (opts.pickOne) {
    out = out.slice(0, 1);
  }
  return out;
}

async function main() {
  const opts = parseArgs();
  const catalog = await fetchCatalog();
  const services = applyFilters(catalog.services, opts);

  // Enrich each record with a `payment_mode` tag so JSON consumers can
  // branch on it without re-deriving from `verified_mode` (which is the
  // router's raw string and may include spurious values like "false").
  //
  // Also project the catalog's advertised price and asset into an
  // `expect` block consumable by pay-per-call's --expect-* flags. This
  // is the trust anchor: when a user pipes discover → pay-per-call,
  // pay-per-call will refuse to sign a 402 whose amount or asset drift
  // from what the catalog advertised, protecting against a compromised
  // upstream rewriting the challenge.
  const enriched = services.map((s) => {
    const { tag } = modeLabel(s.verified_mode);
    // Some services advertise the exact on-chain `pay_to` in
    // methods.stellar_x402 — expose it when available so pay-per-call
    // can validate. When the catalog only has a symbolic asset name
    // ("USDC") rather than the SAC contract ID, we omit expect.asset
    // since the 402 challenge will carry the SAC, not the symbol.
    const stellarMethod =
      (s as any).methods?.stellar_x402 ??
      (s as any).methods?.stellar ??
      undefined;
    const payTo =
      stellarMethod && typeof stellarMethod.pay_to === "string"
        ? (stellarMethod.pay_to as string)
        : undefined;
    const catalogAsset =
      stellarMethod && typeof stellarMethod.asset_sac === "string"
        ? (stellarMethod.asset_sac as string)
        : undefined;
    return {
      ...s,
      payment_mode: tag,
      expect: {
        amount_usdc: parsePriceToUsdc(s.price),
        pay_to: payTo,
        asset: catalogAsset,
      },
    };
  });

  if (opts.json) {
    if (opts.pickOne && enriched.length === 1) {
      console.log(JSON.stringify(enriched[0], null, 2));
    } else {
      console.log(
        JSON.stringify(
          {
            base_url: catalog.base_url,
            services: enriched,
            version: catalog.version,
          },
          null,
          2,
        ),
      );
    }
    return;
  }

  console.log(`MPP Router catalog v${catalog.version}`);
  console.log(`Base URL: ${catalog.base_url}`);
  console.log(`Services: ${services.length}`);
  console.log("");
  for (const s of services) {
    const { human } = modeLabel(s.verified_mode);
    console.log(`  ${s.id}  [${s.category}]  ${human}`);
    console.log(`    ${s.name} — ${s.price}`);
    console.log(`    ${s.method} ${catalog.base_url}${s.public_path}`);
    console.log(`    ${s.description.slice(0, 100)}`);
    const docs = (s as any).docs as { homepage?: string; llms_txt?: string; api_reference?: string } | undefined;
    if (docs) {
      if (docs.llms_txt) console.log(`    📖 LLM docs: ${docs.llms_txt}`);
      if (docs.api_reference) console.log(`    📋 API ref:  ${docs.api_reference}`);
      if (docs.homepage && !docs.llms_txt) console.log(`    🏠 Docs:     ${docs.homepage}`);
    }
    console.log("");
  }
  if (services.length === 0) {
    console.log("  (no matches — try without --query or --category)");
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
