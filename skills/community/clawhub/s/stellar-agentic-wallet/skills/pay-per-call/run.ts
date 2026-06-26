/**
 * pay-per-call — call a 402-gated endpoint and pay with Stellar USDC.
 *
 * Supports two 402 dialects:
 *   1. x402 — body contains { x402Version, accepts: [PaymentRequirements] }
 *   2. MPP  — WWW-Authenticate: Payment request=<base64-json> header
 *
 * Usage:
 *   npx tsx skills/pay-per-call/run.ts <url> [--method POST] [--body '{}'] [--yes]
 *                                        [--max-auto <usd>] [--receipt-out <path>]
 *                                        [--json] [base flags]
 *
 * Base flags: --secret-file, --network, --rpc-url (see cli-config.ts)
 */

import {
  parse402,
  buildRetryHeaders,
  baseUnitsToUsdc,
  validateChallenge,
  type ChallengeExpectations,
  type ParsedChallenge,
} from "../../scripts/src/pay-engine.js";
import type { SignerConfig } from "../../scripts/src/stellar-signer.js";
import { parseBase, type BaseConfig } from "../../scripts/src/cli-config.js";
import { loadSecretFromBase } from "../../scripts/src/secret.js";
import { Keypair } from "@stellar/stellar-sdk";
import { readBalances, totalUsdc } from "../../scripts/src/balance.js";

interface CmdArgs {
  url?: string;
  method: string;
  body?: string;
  json: boolean;
  yes: boolean;
  /** Session-only autopay ceiling. Payments ≤ this amount are signed without prompting. Not persisted. */
  maxAutoUsd?: number;
  receiptOut?: string;
  /** Expected 402 challenge fields. Any mismatch aborts before signing. */
  expectPayTo?: string;
  expectAsset?: string;
  expectAmountUsdc?: string;
  expectAmountTolerance?: number;
}

function parseCmdArgs(rest: string[]): CmdArgs {
  const a: CmdArgs = { method: "GET", json: false, yes: false };
  for (let i = 0; i < rest.length; i++) {
    const k = rest[i];
    if (k === "--method") a.method = rest[++i];
    else if (k === "--body") a.body = rest[++i];
    else if (k === "--json") a.json = true;
    else if (k === "--yes" || k === "-y") a.yes = true;
    else if (k === "--max-auto") {
      const v = parseFloat(rest[++i]);
      if (!Number.isFinite(v) || v < 0) {
        console.error("--max-auto must be a non-negative number");
        process.exit(1);
      }
      a.maxAutoUsd = v;
    } else if (k === "--receipt-out") a.receiptOut = rest[++i];
    else if (k === "--expect-pay-to") a.expectPayTo = rest[++i];
    else if (k === "--expect-asset") a.expectAsset = rest[++i];
    else if (k === "--expect-amount") a.expectAmountUsdc = rest[++i];
    else if (k === "--expect-amount-tolerance") {
      const v = parseFloat(rest[++i]);
      if (!Number.isFinite(v) || v < 0 || v > 1) {
        console.error("--expect-amount-tolerance must be between 0 and 1");
        process.exit(1);
      }
      a.expectAmountTolerance = v;
    } else if (!k.startsWith("--") && !a.url) a.url = k;
  }
  return a;
}

interface RunInputs {
  base: BaseConfig;
  args: CmdArgs;
  signerConfig: SignerConfig;
}

interface InvoiceNormalizationResult {
  body?: string;
  changed: boolean;
  notes: string[];
}

function resolveInputs(): RunInputs {
  const { base, rest } = parseBase(process.argv.slice(2));
  const args = parseCmdArgs(rest);
  if (!args.url) {
    console.error("Usage: pay-per-call.ts <url> [--method POST] [--body '{...}']");
    process.exit(1);
  }
  const secret = loadSecretFromBase(base);
  const signerConfig: SignerConfig = {
    secret,
    network: base.network,
    rpcUrl: base.rpcUrl,
  };
  return { base, args, signerConfig };
}

async function promptConfirm(message: string): Promise<boolean> {
  const readline = await import("node:readline/promises");
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  const ans = await rl.question(message);
  rl.close();
  return ans.trim().toLowerCase() === "yes";
}

async function promptLine(message: string): Promise<string> {
  const readline = await import("node:readline/promises");
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  const ans = await rl.question(message);
  rl.close();
  return ans.trim();
}

/**
 * Decide whether this payment needs a human confirmation, and offer
 * to enroll the wallet in autopay after the first confirmed mainnet
 * payment.
 *
 * Ordering, least-surprising-first:
 *   1. Testnet or --yes → no prompt.
 *   2. --no-autopay → always prompt (defeats saved ceiling for one call).
 *   3. Explicit --max-auto N → auto-pay if amount ≤ N, else prompt.
 *      Does NOT touch the saved ceiling.
 *   4. Saved autopay-ceiling-usd in secret file → auto-pay if amount ≤ it.
 *   5. No ceiling → prompt. After user confirms, offer to save a
 *      ceiling so future small payments are silent.
 *
 * Auto-pay always logs `[autopay] $X to G...` to stderr so there is a
 * trail, even when silent.
 */
async function gateMainnetPayment(opts: {
  amountUsd: number;
  humanAmount: string;
  args: CmdArgs;
  network: "testnet" | "pubnet";
}): Promise<void> {
  const { amountUsd, humanAmount, args, network } = opts;

  if (network !== "pubnet") return;
  if (args.yes) return;

  if (args.maxAutoUsd !== undefined) {
    if (amountUsd <= args.maxAutoUsd) {
      console.error(
        `[autopay] $${humanAmount} USDC (≤ --max-auto $${args.maxAutoUsd.toFixed(2)})`,
      );
      return;
    }
  }

  const ok = await promptConfirm(
    `Pay $${humanAmount} USDC on mainnet? (yes/no) `,
  );
  if (!ok) {
    console.error("Aborted.");
    process.exit(0);
  }
}

async function preflightPayerReady(opts: {
  base: BaseConfig;
  signerConfig: SignerConfig;
  challenge: ParsedChallenge;
  amountUsd: number;
}): Promise<void> {
  const signerPubkey = Keypair.fromSecret(opts.signerConfig.secret).publicKey();
  const report = await readBalances(
    { ...opts.base, assetSac: opts.challenge.asset },
    signerPubkey,
  );
  const problems: string[] = [];
  if (!report.accountExists) {
    problems.push(
      `payer account ${signerPubkey} does not exist on ${opts.base.network}`,
    );
  }
  if (report.accountExists && !report.hasClassicUsdcTrustline) {
    problems.push("payer account is missing the Classic USDC trustline");
  }
  const usdc = totalUsdc(report);
  if (report.accountExists && usdc < opts.amountUsd) {
    problems.push(
      `payer USDC balance ${usdc.toFixed(7)} is below required ${opts.amountUsd.toFixed(7)}`,
    );
  }
  if (report.accountExists && Number(report.spendableXlm) < 0) {
    problems.push(
      `payer XLM balance is below reserve; spendable XLM is ${report.spendableXlm}`,
    );
  }
  if (problems.length === 0) return;

  console.error("❌ Payer wallet is not ready for this payment:");
  for (const p of problems) console.error(`   - ${p}`);
  console.error("");
  console.error("Use an existing funded wallet with --identity <name> or --secret-file <path>.");
  console.error("Check readiness with:");
  console.error(
    `   npx tsx skills/onboard/run.ts ${opts.base.identity ? `--identity ${opts.base.identity}` : `--secret-file ${opts.base.secretFile}`} --network ${opts.base.network}`,
  );
  process.exit(4);
}

async function dumpResponse(res: Response, jsonMode: boolean) {
  if (!res.ok && res.status !== 202) {
    console.error(`❌ ${res.status} ${res.statusText}`);
    console.error(await res.text());
    process.exit(1);
  }
  const ctype = res.headers.get("content-type") ?? "";
  if (ctype.includes("application/json")) {
    const json = await res.json();
    console.log(jsonMode ? JSON.stringify(json) : JSON.stringify(json, null, 2));
  } else {
    console.log(await res.text());
  }
}

/**
 * Poll an async job until it completes or times out.
 * Uses the same auth headers from the initial request so the
 * router can verify the caller is the original payer.
 */
async function pollJobStatus(
  pollUrl: string,
  authHeaders: HeadersInit,
  jsonMode: boolean,
  intervalMs = 5000,
  timeoutMs = 600000, // 10 minutes
): Promise<boolean> {
  const start = Date.now();
  let attempt = 0;

  while (Date.now() - start < timeoutMs) {
    attempt++;
    await new Promise((r) => setTimeout(r, intervalMs));

    const res = await fetch(pollUrl, { headers: authHeaders });

    if (res.status === 202 || res.status === 200) {
      let body: any;
      try {
        body = await res.json();
      } catch {
        console.error(`   Attempt ${attempt}: non-JSON response (${res.status})`);
        continue;
      }

      const status = body.status ?? body.state ?? "";
      if (
        status === "pending" ||
        status === "processing" ||
        status === "in_progress"
      ) {
        console.error(`   Attempt ${attempt}: ${status}...`);
        continue;
      }

      // Job completed (or unknown status) — dump result
      console.error(`✅ Job completed after ${attempt} polls`);
      console.log(
        jsonMode ? JSON.stringify(body) : JSON.stringify(body, null, 2),
      );
      return true;
    }

    if (res.status === 404) {
      console.error(`❌ Job not found (expired or invalid)`);
      process.exit(1);
    }

    console.error(
      `   Attempt ${attempt}: unexpected status ${res.status}, retrying...`,
    );
  }

  console.error(`❌ Timeout after ${timeoutMs / 1000}s waiting for job`);
  process.exit(1);
}

function buildInit(method: string, body?: string): RequestInit {
  const canHaveBody = !["GET", "HEAD"].includes(method.toUpperCase());
  return {
    method,
    headers: body && canHaveBody ? { "Content-Type": "application/json" } : undefined,
    body: canHaveBody ? body : undefined,
  };
}

function tryParseJsonObject(body?: string): Record<string, unknown> | null {
  if (!body) return null;
  try {
    const parsed = JSON.parse(body);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return null;
    return parsed as Record<string, unknown>;
  } catch {
    return null;
  }
}

function extractPaymentIdFromUrl(value: string): string | null {
  const m = value.match(/\/payment-links\/(pl_[a-zA-Z0-9]+)/);
  return m?.[1] ?? null;
}

function normalizeInvoicePayload(body?: string): InvoiceNormalizationResult {
  const parsed = tryParseJsonObject(body);
  if (!parsed) return { body, changed: false, notes: [] };

  const notes: string[] = [];
  let changed = false;

  const asString = (v: unknown): string | undefined =>
    typeof v === "string" && v.trim() ? v.trim() : undefined;

  let url = asString(parsed.url);
  let paymentId = asString(parsed.payment_id);

  // Common aliases used by callers across providers.
  if (!url) {
    const aliasUrl =
      asString(parsed.payment_link) ??
      asString(parsed.link) ??
      asString(parsed.invoice_url);
    if (aliasUrl) {
      url = aliasUrl;
      parsed.url = aliasUrl;
      changed = true;
      notes.push("mapped alias key to `url`");
    }
  }

  if (!paymentId) {
    const aliasId =
      asString(parsed.id) ??
      asString(parsed.invoice_id) ??
      asString(parsed.paymentLinkId);
    if (aliasId?.startsWith("pl_")) {
      paymentId = aliasId;
      parsed.payment_id = aliasId;
      changed = true;
      notes.push("mapped alias key to `payment_id`");
    }
  }

  if (!paymentId && url) {
    const derived = extractPaymentIdFromUrl(url);
    if (derived) {
      parsed.payment_id = derived;
      changed = true;
      notes.push("derived `payment_id` from Coinbase URL");
    }
  }

  return {
    body: JSON.stringify(parsed),
    changed,
    notes,
  };
}

function isMpprouterPayInvoice(url: string): boolean {
  try {
    const u = new URL(url);
    return (
      u.host.endsWith("mpprouter.dev") &&
      u.pathname.endsWith("/v1/services/rozo-agent-api/pay-invoice")
    );
  } catch {
    return false;
  }
}

async function preflightQuoteInvoice(url: string, init: RequestInit): Promise<void> {
  try {
    const u = new URL(url);
    const quoteUrl = `${u.origin}/v1/services/rozo-agent-api/quote-invoice`;
    const res = await fetch(quoteUrl, init);
    if (!res.ok) {
      const detail = await res.text();
      // Backward-compatible fallback: some public router deployments do not
      // expose /quote-invoice even when /pay-invoice exists.
      if (
        res.status === 400 &&
        detail.includes("Unknown public service route")
      ) {
        console.error("⚠️  quote-invoice route not publicly available; continuing without preflight.");
        return;
      }
      console.error("⚠️  quote-invoice preflight failed:");
      console.error(`   ${res.status} ${res.statusText}`);
      if (detail) console.error(`   ${detail}`);
      console.error("   Aborting before payment.");
      process.exit(2);
    }
    console.error("✓ quote-invoice preflight OK");
  } catch (err) {
    console.error(`⚠️  quote-invoice preflight error: ${(err as Error).message}`);
    console.error("   Aborting before payment.");
    process.exit(2);
  }
}

/**
 * Ask the response whether the path exists under a different HTTP method.
 * Modern router replies 405 with `allowed_methods`; older deployments
 * reply 400 with the legacy "Unknown public service route" string and
 * no hint, so we fall back to probing the catalog by public_path.
 */
async function detectMethodMismatch(
  url: string,
  res: Response,
): Promise<string | null> {
  if (res.status === 405) {
    try {
      const j = (await res.clone().json()) as { allowed_methods?: string[] };
      const m = j.allowed_methods?.[0];
      if (m) return m;
    } catch {}
    const allow = res.headers.get("allow");
    if (allow) return allow.split(",")[0].trim();
  }
  if (res.status === 400) {
    const u = new URL(url);
    if (!u.host.endsWith("mpprouter.dev")) return null;
    let body: string;
    try { body = await res.clone().text(); } catch { return null; }
    if (!body.includes("Unknown public service route")) return null;
    try {
      const cat = await fetch(`${u.origin}/v1/services/catalog`);
      if (!cat.ok) return null;
      const j = (await cat.json()) as { services?: Array<{ public_path: string; method: string }> };
      const hit = j.services?.find(s => s.public_path === u.pathname);
      return hit?.method ?? null;
    } catch { return null; }
  }
  return null;
}

function printStartupWarnings(inputs: RunInputs): void {
  const { base, args } = inputs;
  if (base.network === "pubnet" && !args.yes) {
    console.error("⚠️  MAINNET: real USDC will move. Pass --network testnet to prototype.");
  }
}

async function runPayFlow(inputs: RunInputs): Promise<void> {
  const { args, signerConfig } = inputs;
  printStartupWarnings(inputs);
  if (isMpprouterPayInvoice(args.url!) && args.method.toUpperCase() === "POST") {
    const normalized = normalizeInvoicePayload(args.body);
    if (normalized.changed) {
      args.body = normalized.body;
      console.error(`🧭 Normalized invoice payload: ${normalized.notes.join("; ")}`);
    }
    const quoteInit = buildInit(args.method, args.body);
    await preflightQuoteInvoice(args.url!, quoteInit);
  }

  let init = buildInit(args.method, args.body);

  let res = await fetch(args.url!, init);

  const correctMethod = await detectMethodMismatch(args.url!, res);
  if (correctMethod && correctMethod.toUpperCase() !== args.method.toUpperCase()) {
    console.error(
      `⚠️  ${args.method} rejected; router says use ${correctMethod}. Retrying.`,
    );
    args.method = correctMethod;
    init = buildInit(args.method, args.body);
    res = await fetch(args.url!, init);
  }

  if (res.status !== 402) {
    await dumpResponse(res, args.json);
    return;
  }

  const challenge: ParsedChallenge | null = await parse402(res);
  if (!challenge) {
    console.error("❌ Got 402 but could not parse challenge.");
    console.error("   Body:", await res.text());
    process.exit(1);
  }

  const humanAmount = baseUnitsToUsdc(challenge.amount);
  console.error(`💸 Payment required (${challenge.dialect})`);
  console.error(`   Amount: ${humanAmount} USDC`);
  console.error(`   To:     ${challenge.payTo}`);
  console.error(`   Asset:  ${challenge.asset}`);
  console.error("");

  // Challenge validation. If the caller passed --expect-* flags (typically
  // piped through from `discover --pick-one --json`), verify the 402
  // response matches. Any mismatch means a server or intermediary is
  // attempting to redirect funds, inflate the price, or swap the asset.
  // Refuse to sign.
  const expectations: ChallengeExpectations = {
    payTo: args.expectPayTo,
    asset: args.expectAsset,
    amountUsdc: args.expectAmountUsdc,
    amountTolerance: args.expectAmountTolerance,
  };
  const hasAnyExpectation =
    expectations.payTo !== undefined ||
    expectations.asset !== undefined ||
    expectations.amountUsdc !== undefined;
  if (hasAnyExpectation) {
    const mismatches = validateChallenge(challenge, expectations);
    if (mismatches) {
      console.error("❌ Challenge does not match expected values:");
      for (const m of mismatches) console.error(`   - ${m}`);
      console.error("");
      console.error("   Refusing to sign. The 402 server may be compromised,");
      console.error("   the URL may be wrong, or the catalog is stale.");
      process.exit(3);
    }
    console.error("✓ Challenge matches --expect-* values.");
    console.error("");
  }

  const amountUsd = parseFloat(humanAmount);
  await preflightPayerReady({
    base: inputs.base,
    signerConfig,
    challenge,
    amountUsd,
  });
  await gateMainnetPayment({
    amountUsd,
    humanAmount,
    args,
    network: signerConfig.network,
  });

  const retryHeaders = await buildRetryHeaders({
    challenge,
    signerConfig,
    baseHeaders: init.headers,
  });
  res = await fetch(args.url!, { ...init, headers: retryHeaders });

  const receipt = res.headers.get("payment-receipt");
  if (receipt && args.receiptOut) {
    const fs = await import("node:fs/promises");
    await fs.writeFile(args.receiptOut, receipt);
    console.error(`📝 Receipt saved to ${args.receiptOut}`);
  } else if (receipt) {
    console.error(`📝 Payment-Receipt: ${receipt}`);
  }

  // Handle async 202 — poll until job completes
  if (res.status === 202) {
    const pollUrl = res.headers.get("x-job-poll-url");
    const jobId = res.headers.get("x-job-id");
    if (pollUrl) {
      console.error(`⏳ Async job started (id=${jobId ?? "unknown"})`);
      console.error(`   Poll URL: ${pollUrl}`);
      const result = await pollJobStatus(pollUrl, retryHeaders, args.json);
      if (result) return;
    } else {
      // No poll URL — just dump the 202 body
      await dumpResponse(res, args.json);
      return;
    }
  }

  await dumpResponse(res, args.json);
}

async function main() {
  const inputs = resolveInputs();
  await runPayFlow(inputs);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
