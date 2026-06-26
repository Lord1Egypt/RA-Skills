/**
 * onboard — diagnose wallet readiness and guide first-time setup.
 *
 * Default mode (no flags): diagnose only. Prints a scorecard of what's
 * OK, what's missing, and the exact next command to run. Never spends
 * or writes anything.
 *
 * --setup: interactive. Offers to add the USDC Classic trustline if
 *   missing. Never auto-swaps — swapping costs money, so the user must
 *   ask for it explicitly with --swap <xlm>.
 *
 * --swap <xlm>: delegate to swap-xlm-to-usdc.ts with that amount.
 *   Implies --setup. Inherits that script's own confirmation prompts.
 *
 * --json: machine-readable report, no prompts.
 *
 * --i-know: ack the gitignore warning when a secret file lives inside
 *   a git repo without being ignored. Without this, --setup refuses to
 *   proceed; diagnose mode only warns.
 *
 * Base flags (secret file, network, etc.) via parseBase.
 */

import * as fs from "node:fs";
import * as path from "node:path";
import { Keypair } from "@stellar/stellar-sdk";
import { parseBase, type BaseConfig } from "../../scripts/src/cli-config.js";
import {
  loadSecretWithSourceFromBase,
  PREFERRED_SECRET_ENV_KEY,
  type SecretSource,
} from "../../scripts/src/secret.js";
import { readBalances, totalUsdc } from "../../scripts/src/balance.js";
import { runAddTrustline } from "../check-balance/add-trustline.js";
import { runSwap, type SwapArgs } from "../check-balance/swap-xlm-to-usdc.js";

const TRUSTLINE_RESERVE_XLM = 0.5;
const TXN_CUSHION_XLM = 0.1; // room for tx fees and a swap round-trip
const RECOMMENDED_MIN_XLM = 1 + TRUSTLINE_RESERVE_XLM + TXN_CUSHION_XLM; // 1.6

interface CmdArgs {
  setup: boolean;
  swapXlm?: number;
  json: boolean;
  iKnow: boolean;
  yes: boolean;
}

function parseCmdArgs(rest: string[]): CmdArgs {
  const a: CmdArgs = { setup: false, json: false, iKnow: false, yes: false };
  for (let i = 0; i < rest.length; i++) {
    const k = rest[i];
    if (k === "--setup") a.setup = true;
    else if (k === "--swap") {
      a.swapXlm = parseFloat(rest[++i]);
      a.setup = true;
    } else if (k === "--json") a.json = true;
    else if (k === "--i-know") a.iKnow = true;
    else if (k === "--yes" || k === "-y") a.yes = true;
  }
  return a;
}

type CheckStatus = "ok" | "warn" | "fail";

interface Check {
  id: string;
  status: CheckStatus;
  summary: string;
  next?: string;
}

interface Report {
  account: string;
  network: "testnet" | "pubnet";
  secretSource: SecretSource;
  checks: Check[];
  gitignoreWarning?: string;
  usdcTotal: number;
  xlmBalance: string;
  spendableXlm: string;
  hasTrustline: boolean;
  accountExists: boolean;
}

async function promptYes(msg: string): Promise<boolean> {
  const readline = await import("node:readline/promises");
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  const ans = await rl.question(msg);
  rl.close();
  return /^y(es)?$/i.test(ans.trim());
}


/**
 * Walk up from `startDir` looking for a `.git` directory. Returns the
 * repo root or null if none found within 20 levels.
 */
function findGitRoot(startDir: string): string | null {
  let dir = path.resolve(startDir);
  for (let i = 0; i < 20; i++) {
    if (fs.existsSync(path.join(dir, ".git"))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
  return null;
}

function readGitignorePatterns(repoRoot: string): string[] {
  const p = path.join(repoRoot, ".gitignore");
  try {
    return fs
      .readFileSync(p, "utf8")
      .split(/\r?\n/)
      .map((l) => l.trim())
      .filter((l) => l && !l.startsWith("#"));
  } catch {
    return [];
  }
}

/**
 * Lightweight gitignore check — matches a basename or literal path
 * against the patterns. Intentionally simple; full gitignore semantics
 * are not needed here, since we only care about a handful of known
 * secret-carrying filenames.
 */
function isIgnored(filePath: string, repoRoot: string, patterns: string[]): boolean {
  const rel = path.relative(repoRoot, filePath);
  const base = path.basename(filePath);
  for (const raw of patterns) {
    const pat = raw.replace(/^\//, "").replace(/\/$/, "");
    if (pat === base || pat === rel || pat === `*${path.extname(base)}`) return true;
    // Simple glob: "*.env" style
    if (pat.startsWith("*.") && base.endsWith(pat.slice(1))) return true;
    if (pat.startsWith(".env") && base.startsWith(".env")) return true;
  }
  return false;
}

interface GitignoreStatus {
  inRepo: boolean;
  repoRoot: string | null;
  unignored: string[];
}

function auditGitignore(secretSource: SecretSource): GitignoreStatus {
  const candidates = [
    secretSource.path,
    path.join(path.dirname(secretSource.path), ".stellar-secret"),
    path.join(path.dirname(secretSource.path), ".env"),
    path.join(path.dirname(secretSource.path), ".env.prod"),
  ].filter((p, i, arr) => arr.indexOf(p) === i && fs.existsSync(p));

  const repoRoot = candidates.length > 0 ? findGitRoot(path.dirname(candidates[0])) : null;
  if (!repoRoot) {
    return { inRepo: false, repoRoot: null, unignored: [] };
  }
  const patterns = readGitignorePatterns(repoRoot);
  const unignored = candidates.filter((c) => !isIgnored(c, repoRoot, patterns));
  return { inRepo: true, repoRoot, unignored };
}

function buildChecks(opts: {
  secretSource: SecretSource;
  accountExists: boolean;
  xlmBalance: string;
  spendableXlm: string;
  hasTrustline: boolean;
  usdcTotal: number;
  network: "testnet" | "pubnet";
  gitignore: GitignoreStatus;
}): Check[] {
  const checks: Check[] = [];

  // 1. Secret source
  if (opts.secretSource.kind === "env" && opts.secretSource.envKey !== PREFERRED_SECRET_ENV_KEY) {
    checks.push({
      id: "secret",
      status: "warn",
      summary: `Secret loaded from legacy key ${opts.secretSource.envKey} in ${opts.secretSource.path}`,
      next: `Rename the env var to ${PREFERRED_SECRET_ENV_KEY} (keep the same value). The old name still works but is deprecated.`,
    });
  } else {
    checks.push({
      id: "secret",
      status: "ok",
      summary: `Secret loaded from ${opts.secretSource.path} (${opts.secretSource.kind})`,
    });
  }

  // 2. Account funded
  if (!opts.accountExists) {
    checks.push({
      id: "account",
      status: "fail",
      summary: `Account not created on ${opts.network}`,
      next:
        opts.network === "testnet"
          ? `Fund it: curl "https://friendbot.stellar.org?addr=<your pubkey>"`
          : `Send at least ${RECOMMENDED_MIN_XLM} XLM to this account from any Stellar wallet or exchange.`,
    });
    return checks; // Nothing else is meaningful until the account exists.
  }

  // 3. XLM reserve headroom
  const xlm = Number(opts.xlmBalance);
  if (xlm < RECOMMENDED_MIN_XLM) {
    const shortfall = (RECOMMENDED_MIN_XLM - xlm).toFixed(2);
    checks.push({
      id: "xlm",
      status: xlm < 1 ? "fail" : "warn",
      summary: `XLM balance ${xlm} is below recommended ${RECOMMENDED_MIN_XLM} (1 base reserve + 0.5 trustline + 0.1 cushion)`,
      next: `Top up at least ${shortfall} more XLM before adding the trustline.`,
    });
  } else {
    checks.push({
      id: "xlm",
      status: "ok",
      summary: `XLM balance ${xlm} (spendable ${opts.spendableXlm})`,
    });
  }

  // 4. Trustline
  if (!opts.hasTrustline) {
    checks.push({
      id: "trustline",
      status: "fail",
      summary: "USDC Classic trustline not set",
      next: `Run: npx tsx skills/check-balance/add-trustline.ts --network ${opts.network}  (costs 0.5 XLM reserve + a few stroops for the tx fee)`,
    });
  } else {
    checks.push({
      id: "trustline",
      status: "ok",
      summary: "USDC Classic trustline present",
    });
  }

  // 5. USDC balance
  if (opts.usdcTotal <= 0) {
    const lines = [
      "You can get USDC by:",
      "  (a) receiving a transfer to this address from another wallet or exchange, OR",
      `  (b) swapping XLM → USDC on the Stellar DEX: npx tsx skills/check-balance/swap-xlm-to-usdc.ts --usdc <amount> --network ${opts.network}`,
    ].join("\n       ");
    checks.push({
      id: "usdc",
      status: "fail",
      summary: "USDC balance is zero — can't pay for anything yet",
      next: lines,
    });
  } else {
    checks.push({
      id: "usdc",
      status: "ok",
      summary: `USDC balance ${opts.usdcTotal.toFixed(4)}`,
    });
  }

  // 6. gitignore hygiene
  if (opts.gitignore.inRepo && opts.gitignore.unignored.length > 0) {
    checks.push({
      id: "gitignore",
      status: "warn",
      summary: `Secret files inside a git repo are NOT gitignored: ${opts.gitignore.unignored.join(", ")}`,
      next: `Add to ${opts.gitignore.repoRoot}/.gitignore:\n    .stellar-secret\n    .env\n    .env.prod\n    .env.*\n   Never commit these — they control your funds.`,
    });
  }

  return checks;
}

function statusIcon(s: CheckStatus): string {
  return s === "ok" ? "✅" : s === "warn" ? "⚠️" : "❌";
}

function renderReport(report: Report): void {
  console.log(`Account: ${report.account}`);
  console.log(`Network: ${report.network}`);
  console.log(`Secret:  ${report.secretSource.path} (${report.secretSource.kind}${report.secretSource.envKey ? `, ${report.secretSource.envKey}` : ""})`);
  console.log("");
  for (const c of report.checks) {
    console.log(`  ${statusIcon(c.status)} [${c.id}] ${c.summary}`);
    if (c.next) {
      for (const line of c.next.split("\n")) console.log(`       ${line}`);
    }
  }
  console.log("");
  console.log("🔐 Never commit .stellar-secret, .env, .env.prod, or .secrets/*.");
  console.log("   This wallet's secret key controls real USDC. Treat it like a password.");
}

async function maybeAddTrustline(
  report: Report,
  args: CmdArgs,
  base: BaseConfig,
  secret: string,
): Promise<void> {
  if (report.hasTrustline) return;
  if (Number(report.xlmBalance) < 1 + TRUSTLINE_RESERVE_XLM) {
    console.error("⏸  Not enough XLM to add trustline. Top up first.");
    return;
  }
  const proceed =
    args.yes ||
    (await promptYes(
      `Add USDC Classic trustline on ${report.network}? Costs 0.5 XLM reserve. (yes/no) `,
    ));
  if (!proceed) {
    console.error("Skipped trustline.");
    return;
  }
  // In-process call — uses the exported runAddTrustline function
  // so there's no subprocess, no extra startup cost, and nothing
  // for a scanner to flag.
  try {
    await runAddTrustline({ base, secret });
  } catch (err) {
    console.error(`add-trustline failed: ${(err as Error).message}`);
    process.exit(1);
  }
}

async function maybeSwap(
  report: Report,
  args: CmdArgs,
  base: BaseConfig,
  secret: string,
): Promise<void> {
  if (args.swapXlm === undefined) return;
  if (!(args.swapXlm > 0)) {
    console.error("--swap <xlm> must be a positive number");
    process.exit(1);
  }
  const swapArgs: SwapArgs = {
    mode: "xlm",
    amount: String(args.swapXlm),
    slippage: 0.01,
    yes: args.yes,
  };
  try {
    await runSwap({ base, secret, args: swapArgs });
  } catch (err) {
    console.error(`swap-xlm-to-usdc failed: ${(err as Error).message}`);
    process.exit(1);
  }
}

async function main() {
  const { base, rest } = parseBase(process.argv.slice(2));
  const args = parseCmdArgs(rest);

  const { secret, source } = loadSecretWithSourceFromBase(base);
  const pubkey = Keypair.fromSecret(secret).publicKey();

  const balance = await readBalances(base, pubkey);
  const xlmBalance =
    balance.balances.find((b) => b.asset === "XLM")?.amount ?? "0";
  const gitignore = auditGitignore(source);

  const report: Report = {
    account: pubkey,
    network: base.network,
    secretSource: source,
    accountExists: balance.accountExists,
    xlmBalance,
    spendableXlm: balance.spendableXlm,
    hasTrustline: balance.hasClassicUsdcTrustline,
    usdcTotal: totalUsdc(balance),
    checks: [],
    gitignoreWarning: gitignore.unignored.join(",") || undefined,
  };
  report.checks = buildChecks({
    secretSource: source,
    accountExists: balance.accountExists,
    xlmBalance,
    spendableXlm: balance.spendableXlm,
    hasTrustline: balance.hasClassicUsdcTrustline,
    usdcTotal: report.usdcTotal,
    network: base.network,
    gitignore,
  });

  if (args.json) {
    console.log(JSON.stringify(report, null, 2));
    return;
  }

  renderReport(report);

  if (!args.setup) return;

  if (gitignore.inRepo && gitignore.unignored.length > 0 && !args.iKnow) {
    console.error("");
    console.error(
      "⛔ Refusing --setup: secret files in a git repo are not gitignored (see warning above).",
    );
    console.error("   Add them to .gitignore, or re-run with --i-know to proceed anyway.");
    process.exit(2);
  }

  await maybeAddTrustline(report, args, base, secret);
  await maybeSwap(report, args, base, secret);

  console.log("");
  console.log("Re-running diagnosis…");
  const after = await readBalances(base, pubkey);
  const afterReport: Report = {
    ...report,
    accountExists: after.accountExists,
    xlmBalance: after.balances.find((b) => b.asset === "XLM")?.amount ?? "0",
    spendableXlm: after.spendableXlm,
    hasTrustline: after.hasClassicUsdcTrustline,
    usdcTotal: totalUsdc(after),
    checks: [],
  };
  afterReport.checks = buildChecks({
    secretSource: source,
    accountExists: after.accountExists,
    xlmBalance: afterReport.xlmBalance,
    spendableXlm: after.spendableXlm,
    hasTrustline: after.hasClassicUsdcTrustline,
    usdcTotal: afterReport.usdcTotal,
    network: base.network,
    gitignore,
  });
  renderReport(afterReport);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
