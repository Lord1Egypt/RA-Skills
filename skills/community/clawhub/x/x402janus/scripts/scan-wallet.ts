#!/usr/bin/env npx tsx
/**
 * scan-wallet.ts — x402janus security scan
 *
 * Scans a wallet for risky token approvals, flagged contracts, and suspicious patterns.
 * Paid tiers use thirdweb x402 SDK for payment handling.
 *
 * Usage:
 *   npx tsx scripts/scan-wallet.ts <address> [options]
 *
 * Options:
 *   --tier <free|quick|standard|deep>  Scan tier (default: quick)
 *   --chain <base|ethereum>            Chain to scan (default: base)
 *   --json                             Output as JSON
 *   --help, -h                         Show this help
 *
 * Required env:
 *   JANUS_API_URL   — Janus API base URL (e.g. https://x402janus.com)
 *
 * Required for paid tiers (quick/standard/deep):
 *   PRIVATE_KEY         — Agent wallet key for x402 payment signing
 *
 * Optional:
 *   THIRDWEB_CLIENT_ID  — thirdweb client id (default: x402janus-skill)
 */

import { parseArgs } from "util";
import { createThirdwebClient } from "thirdweb";
import { base, type Chain } from "thirdweb/chains";
import { wrapFetchWithPayment } from "thirdweb/x402";
import { privateKeyToAccount, type Wallet } from "thirdweb/wallets";

// ── env ──────────────────────────────────────────────────────────────────────

function requireEnv(name: string, hint?: string): string {
  const val = process.env[name];
  if (!val) {
    console.error(`Error: ${name} is required but not set.`);
    if (hint) {
      console.error(`  ${hint}`);
    }
    process.exit(1);
  }
  return val;
}

// ── payment ──────────────────────────────────────────────────────────────────

function createPaidFetch(privateKey: string): typeof fetch {
  const clientId = process.env.THIRDWEB_CLIENT_ID || "x402janus-skill";
  const client = createThirdwebClient({ clientId });
  const account = privateKeyToAccount({ client, privateKey });

  // thirdweb x402 currently expects a Wallet interface.
  // For server-side CLI usage, we adapt a private-key Account into the minimal
  // wallet surface the x402 wrapper needs (getAccount/getChain/switchChain).
  let currentChain: Chain = base;
  const wallet = {
    getAccount: () => account,
    getChain: () => currentChain,
    switchChain: async (nextChain: Chain) => {
      currentChain = nextChain;
    },
  } as unknown as Wallet;

  return wrapFetchWithPayment(fetch, client, wallet) as typeof fetch;
}

// ── scan logic ────────────────────────────────────────────────────────────────

function isValidAddress(addr: string): boolean {
  return /^0x[a-fA-F0-9]{40}$/.test(addr);
}

function formatRisk(score: number): { level: string; emoji: string } {
  if (score >= 75) return { level: "critical", emoji: "🔴" };
  if (score >= 50) return { level: "high", emoji: "🟠" };
  if (score >= 25) return { level: "medium", emoji: "🟡" };
  return { level: "low", emoji: "🟢" };
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function printResults(result: any, json: boolean): void {
  if (json) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  const healthScore = result.summary?.healthScore ?? result.riskScore ?? 0;
  const risk = formatRisk(100 - healthScore);

  console.log("\n🔲  x402janus Security Scan\n");
  console.log("═══════════════════════════════════════");
  console.log(`Address:      ${result.address}`);
  console.log(`Scanned at:   ${result.scannedAt}`);
  console.log(`Coverage:     ${result.coverageLevel}`);
  console.log(`Payer:        ${result.payer ?? "n/a (free tier)"}`);
  console.log("───────────────────────────────────────");
  console.log(`Health Score: ${healthScore}/100 ${risk.emoji}`);
  console.log("───────────────────────────────────────");

  if (result.summary) {
    console.log("\n📊 Summary:");
    console.log(`  • Total Approvals:     ${result.summary.totalTokensApproved}`);
    console.log(`  • Unlimited Approvals: ${result.summary.unlimitedApprovals}`);
    console.log(`  • High Risk:           ${result.summary.highRiskApprovals}`);
  }

  if (result.approvals?.length > 0) {
    console.log("\n🔑 Approvals:");
    for (const a of result.approvals) {
      const emoji =
        a.riskLevel === "high" || a.riskLevel === "critical"
          ? "🔴"
          : a.riskLevel === "medium"
            ? "🟡"
            : "🟢";
      console.log(
        `  ${emoji} ${a.token.slice(0, 8)}…${a.token.slice(-4)} → ${a.spender.slice(0, 8)}…${a.spender.slice(-4)}`,
      );
      if (a.isUnlimited) console.log("     ⚠️  UNLIMITED");
      if (a.riskReasons?.length) console.log(`     ${a.riskReasons.join(", ")}`);
    }
  }

  if (result.recommendations?.length > 0) {
    console.log("\n💡 Recommendations:");
    for (const rec of result.recommendations) console.log(`  • ${rec}`);
  }

  if (result.revokeTransactions?.length > 0) {
    console.log(`\n🔧 ${result.revokeTransactions.length} revoke transaction(s) available`);
  }

  console.log("\n═══════════════════════════════════════\n");
}

// ── main ─────────────────────────────────────────────────────────────────────

async function main() {
  const { values, positionals } = parseArgs({
    args: process.argv.slice(2),
    options: {
      tier: { type: "string", default: "quick" },
      chain: { type: "string", default: "base" },
      json: { type: "boolean", default: false },
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
  });

  if (values.help) {
    console.log(`
x402janus — wallet security scan via x402 micropayment

Usage: npx tsx scripts/scan-wallet.ts <address> [options]

Arguments:
  address                                  Wallet address to scan (required, EVM 0x…)

Options:
  --tier <free|quick|standard|deep>        Scan tier (default: quick)
  --chain <base|ethereum>                  Chain to scan (default: base)
  --json                                   Output as JSON
  --help, -h                               Show this help

Required env:
  JANUS_API_URL      Janus API endpoint (e.g. https://x402janus.com)

Required for paid tiers (quick/standard/deep):
  PRIVATE_KEY        Agent wallet key (used by thirdweb x402 payment signer)

Optional env:
  THIRDWEB_CLIENT_ID thirdweb client id (default: x402janus-skill)

Pricing:
  free     $0.00         <5s    Address validation + tier preview
  quick    $0.01 USDC    <3s    Deterministic risk score, approval list
  standard $0.05 USDC    <10s   + AI threat analysis, deeper lookback
  deep     $0.25 USDC    <30s   + Full graph analysis, drainer fingerprinting

Exit codes:
  0  — safe (health score ≥ 75)
  1  — medium risk (health score 50–74)
  2  — high risk (health score < 50) or payment insufficient/rejected
  3  — critical risk (health score < 25)
`);
    process.exit(0);
  }

  const apiUrl = requireEnv(
    "JANUS_API_URL",
    "JANUS_API_URL is the Janus API endpoint (e.g. https://x402janus.com).",
  ).replace(/\/$/, "");

  const address = positionals[0];
  if (!address) {
    console.error("Error: wallet address required");
    console.error("Usage: npx tsx scripts/scan-wallet.ts <address>");
    process.exit(1);
  }
  if (!isValidAddress(address)) {
    console.error(`Error: invalid Ethereum address: ${address}`);
    process.exit(1);
  }

  const tier = (values.tier ?? "quick").toLowerCase();
  if (!["free", "quick", "standard", "deep"].includes(tier)) {
    console.error(`Error: invalid tier '${tier}' — use free, quick, standard, or deep`);
    process.exit(1);
  }

  const chain = (values.chain ?? "base").toLowerCase();
  if (!["base", "ethereum"].includes(chain)) {
    console.error(`Error: unsupported chain '${chain}' — use base or ethereum`);
    process.exit(1);
  }

  const isFreeTier = tier === "free";

  let scanFetch: typeof fetch = fetch;
  if (!isFreeTier) {
    const privateKey = requireEnv(
      "PRIVATE_KEY",
      "PRIVATE_KEY is required only for paid tiers and is used by thirdweb x402 signing.",
    );
    scanFetch = createPaidFetch(privateKey);
  }

  try {
    const url = `${apiUrl}/api/guardian/scan/${address}?tier=${tier}&chain=${chain}`;
    const response = await scanFetch(url, {
      method: "POST",
      headers: { Accept: "application/json" },
    });

    if (response.status === 402 && !isFreeTier) {
      console.error("\n⚠️  Payment was rejected by the server.");
      console.error("   Check: (1) USDC balance on Base, (2) sufficient amount for tier.");
      process.exit(2);
    }

    if (!response.ok) {
      const body = await response.text();
      console.error(`Error: scan failed (HTTP ${response.status})`);
      try {
        const err = JSON.parse(body);
        console.error(`  ${err.error || err.message || body.slice(0, 200)}`);
      } catch {
        console.error(`  ${body.slice(0, 200)}`);
      }
      process.exit(1);
    }

    const result = await response.json();
    printResults(result, values.json ?? false);

    const healthScore = result.summary?.healthScore ?? 50;
    if (healthScore < 25) process.exit(3);
    if (healthScore < 50) process.exit(2);
    if (healthScore < 75) process.exit(1);
    process.exit(0);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    if (msg.toLowerCase().includes("wallet not connected")) {
      console.error("Error: failed to initialize paid-tier wallet for x402 payment signing.");
      process.exit(2);
    }

    console.error("Error:", msg);
    process.exit(1);
  }
}

main();
