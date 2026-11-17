/**
 * pay-per-call — call a 402-gated endpoint and pay with Stellar USDC.
 *
 * Supports two 402 dialects:
 *   1. x402 — body contains { x402Version, accepts: [PaymentRequirements] }
 *   2. MPP  — WWW-Authenticate: Payment request=<base64-json> header
 *
 * Usage:
 *   ./node_modules/.bin/tsx skills/pay-per-call/run.ts <url> [--method POST] [--body '{}'] [--yes]
 *                                        [--max-auto <usd>] [--receipt-out <path>]
 *                                        [--dialect mpp|x402]
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
import { decodeReceipt, explorerUrl } from "../../scripts/src/receipt.js";
import { parseRefundHeaders, formatRefundLines } from "../../scripts/src/refund.js";

/** Consecutive ownership-proof failures tolerated before giving up on a poll loop. */
const MAX_AUTH_FAILURES = 3;

/** Domain tag the router binds job-ownership proofs to. Must match
 * rozo-mpprouter src/routes/job-status.ts. */
const OWNERSHIP_DOMAIN = "mpprouter-job-ownership-v1";

interface CmdArgs {
  url?: string;
  method: string;
  body?: string;
  json: boolean;
  yes: boolean;
  /** Session-only autopay ceiling. Payments ≤ this amount are signed without prompting. Not persisted. */
  maxAutoUsd?: number;
  receiptOut?: string;
  /** Force a 402 dialect when the server offers both. Default: prefer MPP. */
  dialect?: "mpp" | "x402";
  /** Expected 402 challenge fields. Any mismatch aborts before signing. */
  expectPayTo?: string;
  expectAsset?: string;
  expectAmountUsdc?: string;
  expectAmountTolerance?: number;
}

/**
 * Hard upper bound on the session-only `--max-auto` ceiling, in USD.
 *
 * Unattended signing is a convenience for scripted pipelines paying
 * per-call API prices (fractions of a cent to a few cents). Anything
 * approaching real money should cost a human confirmation, so the flag
 * refuses values above this cap rather than silently honouring them.
 */
export const MAX_AUTO_CEILING_USD = 5;

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
      if (v > MAX_AUTO_CEILING_USD) {
        console.error(
          `❌ --max-auto $${v.toFixed(2)} exceeds the hard cap of $${MAX_AUTO_CEILING_USD.toFixed(2)}.`,
        );
        console.error(
          "   Unattended signing is capped on purpose: a wide ceiling lets a",
        );
        console.error(
          "   compromised or misconfigured 402 server drain the wallet without",
        );
        console.error(
          "   a single prompt. Lower the value, or confirm each payment manually.",
        );
        process.exit(1);
      }
      a.maxAutoUsd = v;
    } else if (k === "--receipt-out") a.receiptOut = rest[++i];
    else if (k === "--dialect") {
      const v = rest[++i];
      if (v !== "mpp" && v !== "x402") {
        console.error(`--dialect must be "mpp" or "x402" (got ${v ?? "nothing"})`);
        process.exit(1);
      }
      a.dialect = v;
    }
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

/**
 * Decide whether this payment needs a human confirmation.
 *
 * Ordering, least-surprising-first:
 *   1. Testnet or --yes → no prompt.
 *   2. Explicit --max-auto N → auto-pay if amount ≤ N, else prompt.
 *      Session-only: never read from or written to disk.
 *   3. Otherwise → prompt.
 *
 * There is no persistent autopay ceiling. Unattended signing is opt-in
 * per process, bounded by MAX_AUTO_CEILING_USD, and every auto-signed
 * payment logs a `[autopay]` line to stderr so there is always a trail.
 */
async function gateMainnetPayment(opts: {
  amountUsd: number;
  humanAmount: string;
  payTo: string;
  args: CmdArgs;
  network: "testnet" | "pubnet";
}): Promise<void> {
  const { amountUsd, humanAmount, payTo, args, network } = opts;

  if (network !== "pubnet") return;
  if (args.yes) return;

  if (args.maxAutoUsd !== undefined) {
    if (amountUsd <= args.maxAutoUsd) {
      console.error(
        `[autopay] $${humanAmount} USDC → ${payTo} auto-signed ` +
          `(--max-auto $${args.maxAutoUsd.toFixed(2)}, session-only, ` +
          `no confirmation asked — drop the flag to restore prompts)`,
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
    `   ./node_modules/.bin/tsx skills/onboard/run.ts ${opts.base.identity ? `--identity ${opts.base.identity}` : `--secret-file ${opts.base.secretFile}`} --network ${opts.base.network}`,
  );
  process.exit(4);
}

/**
 * Print what was actually paid and where to verify it. Falls back to the
 * 402 challenge for amount/recipient when the receipt does not carry them,
 * so the summary is always populated after a successful payment.
 */
function reportReceipt(opts: {
  receipt: string;
  challenge: ParsedChallenge;
  network: "testnet" | "pubnet";
  showRaw: boolean;
  jsonMode: boolean;
}): void {
  const { receipt, challenge, network, showRaw, jsonMode } = opts;
  const decoded = decodeReceipt(receipt);

  const amount = decoded.amount ?? baseUnitsToUsdc(challenge.amount);
  const payTo = decoded.payTo ?? challenge.payTo;
  const when = decoded.timestamp ? ` (${decoded.timestamp})` : "";
  console.error(`📝 Payment: ${amount} USDC → ${payTo}${when}`);

  if (decoded.txHash) {
    console.error(`🔗 Explorer: ${explorerUrl(decoded.txHash, network)}`);
  } else {
    console.error("   (receipt carried no transaction reference)");
  }

  if (showRaw) {
    console.error(`   Payment-Receipt: ${receipt}`);
  }

  // Machine-readable line for calling agents. Stays on stderr so stdout
  // remains exactly the merchant response body.
  if (jsonMode) {
    console.error(
      `PAYMENT_RECEIPT_JSON ${JSON.stringify({
        amount,
        payTo,
        txHash: decoded.txHash ?? null,
        timestamp: decoded.timestamp ?? null,
        explorer: decoded.txHash ? explorerUrl(decoded.txHash, network) : null,
        receipt,
      })}`,
    );
  }
}

/**
 * Surface an automatic refund. The router reports it only in headers, so a
 * client that prints just the body strands the payer without the id needed
 * to fetch the signed receipt from `GET /v1/refunds/{id}`.
 */
function reportRefund(res: Response, jsonMode: boolean): void {
  const refund = parseRefundHeaders(res.headers, res.url);
  if (!refund) return;
  for (const line of formatRefundLines(refund)) console.error(line);
  if (jsonMode) console.error(`REFUND_JSON ${JSON.stringify(refund)}`);
}

async function dumpResponse(res: Response, jsonMode: boolean) {
  reportRefund(res, jsonMode);
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
 * Fetch a fresh ownership challenge for a job and sign it.
 *
 * The router burns the nonce on every successful poll (single-use, short TTL),
 * so this has to run before each poll — the payment headers from the original
 * request are NOT accepted here.
 */
async function buildJobAuthHeaders(
  pollUrl: string,
  jobId: string,
  keypair: Keypair,
): Promise<Record<string, string> | { error: string }> {
  const owner = keypair.publicKey();

  // The payment has already settled by the time we get here, so a blip
  // fetching or parsing the challenge must never abort the run — it has to
  // come back as an error the poll loop can retry and eventually report.
  let res: Response;
  try {
    res = await fetch(`${pollUrl}/challenge`, {
      headers: { "X-Stellar-Owner": owner },
    });
  } catch (err) {
    return { error: `challenge request failed — ${(err as Error).message}` };
  }

  if (!res.ok) {
    let detail = "";
    try {
      detail = ((await res.json()) as any)?.error ?? "";
    } catch {
      /* non-JSON body */
    }
    return { error: `challenge ${res.status}${detail ? ` — ${detail}` : ""}` };
  }

  let body: { nonce?: string };
  try {
    body = (await res.json()) as { nonce?: string };
  } catch {
    return { error: "challenge response was not JSON" };
  }
  if (!body.nonce) return { error: "challenge response had no nonce" };

  // NEVER sign the bare nonce bytes. This is the payer's spending key, and
  // every Stellar signing payload — transactions, Soroban auth entries — is a
  // bare 32-byte hash. A service that could choose the raw bytes we sign could
  // hand back a transaction hash as the "nonce" and walk away with a valid
  // signature over a transfer out of this wallet. Signing a printable,
  // job-bound preimage instead makes the signature useless for anything else.
  const message = new TextEncoder().encode(
    `${OWNERSHIP_DOMAIN}:${jobId}:${body.nonce}`,
  );
  if (message.length === 32) {
    return { error: "refusing to sign a 32-byte payload" };
  }

  const signature = keypair.sign(Buffer.from(message)).toString("base64");

  return {
    "X-Stellar-Owner": owner,
    "X-Stellar-Nonce": body.nonce,
    "X-Stellar-Signature": signature,
  };
}

/**
 * Poll an async job until it completes or times out.
 *
 * Each poll proves ownership of the paying Stellar account by signing a
 * one-shot nonce from the router's /challenge endpoint.
 */
async function pollJobStatus(
  pollUrl: string,
  jobId: string,
  keypair: Keypair,
  jsonMode: boolean,
  intervalMs = 15000,
  timeoutMs = 600000, // 10 minutes
): Promise<boolean> {
  const start = Date.now();
  let attempt = 0;
  let lastLine = "";
  /** Consecutive auth failures. A few are transient (nonce race); a wall of
   * them means the client and router disagree and retrying will never help. */
  let authFailures = 0;

  // Only narrate when something actually changed, so a long job does not
  // scroll a wall of identical lines past the payer.
  const say = (line: string) => {
    if (line === lastLine) return;
    lastLine = line;
    console.error(`   ${line}`);
  };

  while (Date.now() - start < timeoutMs) {
    attempt++;
    await new Promise((r) => setTimeout(r, intervalMs));

    const authHeaders = await buildJobAuthHeaders(pollUrl, jobId, keypair);
    if ("error" in authHeaders) {
      authFailures++;
      say(`ownership challenge failed (${authHeaders.error})`);
      if (authFailures >= MAX_AUTH_FAILURES) {
        console.error(
          `❌ Could not prove job ownership after ${authFailures} attempts. ` +
            `The payment settled — check the refund with verify-refund.mjs.`,
        );
        process.exit(1);
      }
      continue;
    }

    let res: Response;
    try {
      res = await fetch(pollUrl, { headers: authHeaders });
    } catch (err) {
      say(`poll request failed (${(err as Error).message}), retrying...`);
      continue;
    }

    if (res.status === 202 || res.status === 200) {
      authFailures = 0;
      let body: any;
      try {
        body = await res.json();
      } catch {
        say(`non-JSON response (${res.status})`);
        continue;
      }

      const status = body.status ?? body.state ?? "";
      if (
        status === "pending" ||
        status === "processing" ||
        status === "in_progress"
      ) {
        say(`${status}...`);
        continue;
      }

      // Job completed (or unknown status) — dump result
      console.error(`✅ Job completed after ${attempt} polls`);
      reportRefund(res, jsonMode);
      console.log(
        jsonMode ? JSON.stringify(body) : JSON.stringify(body, null, 2),
      );
      return true;
    }

    if (res.status === 404) {
      console.error(`❌ Job not found (expired or invalid)`);
      process.exit(1);
    }

    // An async job that failed after payment is refunded by the router, which
    // reports it in headers on the (non-2xx) poll response. Terminal — stop
    // polling and hand the payer the refund id.
    if (parseRefundHeaders(res.headers, res.url)) {
      await dumpResponse(res, jsonMode);
      return true;
    }

    if (res.status === 401 || res.status === 403) {
      authFailures++;
      say(`poll rejected (${res.status}) — ownership proof not accepted`);
      if (authFailures >= MAX_AUTH_FAILURES) {
        console.error(
          `❌ Router rejected ownership proof ${authFailures} times in a row. ` +
            `The payment settled — check the refund with verify-refund.mjs.`,
        );
        process.exit(1);
      }
      continue;
    }

    authFailures = 0;
    say(`unexpected status ${res.status}, retrying...`);
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

  const challenge: ParsedChallenge | null = await parse402(res, {
    prefer: args.dialect,
  });
  if (!challenge) {
    console.error("❌ Got 402 but could not parse challenge.");
    console.error("   Body:", await res.text());
    process.exit(1);
  }

  const humanAmount = baseUnitsToUsdc(challenge.amount);
  console.error(
    `💸 Payment required (${challenge.dialect}${args.dialect ? ", forced by --dialect" : ""})`,
  );
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
    payTo: challenge.payTo,
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
  if (receipt) {
    if (args.receiptOut) {
      const fs = await import("node:fs/promises");
      await fs.writeFile(args.receiptOut, receipt);
      console.error(`📝 Receipt saved to ${args.receiptOut}`);
    }
    reportReceipt({
      receipt,
      challenge,
      network: signerConfig.network,
      showRaw: args.receiptOut === undefined,
      jsonMode: args.json,
    });
  }

  // Handle async 202 — poll until job completes
  if (res.status === 202) {
    const pollUrl = res.headers.get("x-job-poll-url");
    const jobId = res.headers.get("x-job-id");
    if (pollUrl) {
      console.error(`⏳ Async job started (id=${jobId ?? "unknown"})`);
      console.error(`   Poll URL: ${pollUrl}`);
      // The router binds the proof to the job id in the poll path, so take it
      // from there rather than the (optional) X-Job-Id header.
      const result = await pollJobStatus(
        pollUrl,
        new URL(pollUrl).pathname.split("/").pop() ?? "",
        Keypair.fromSecret(signerConfig.secret),
        args.json,
      );
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
