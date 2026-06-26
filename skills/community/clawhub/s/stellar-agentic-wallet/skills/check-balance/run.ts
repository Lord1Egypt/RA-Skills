/**
 * check-balance — read Stellar USDC + XLM for an account.
 *
 * Usage:
 *   npx tsx skills/check-balance/run.ts [G... pubkey] [--json] [base flags]
 *
 * If no pubkey given, derives it from the --secret-file (default
 * .stellar-secret in cwd).
 *
 * Base flags (from scripts/src/cli-config.ts):
 *   --secret-file <path>    default: .stellar-secret
 *   --network <name>        testnet|pubnet, default: pubnet
 *   --horizon-url <url>     override Horizon endpoint
 *   --rpc-url <url>         override Soroban RPC endpoint
 *   --asset-sac <addr>      Stellar Asset Contract address
 */

import { Keypair } from "@stellar/stellar-sdk";
import { parseBase, type BaseConfig } from "../../scripts/src/cli-config.js";
import { loadSecretFromBase } from "../../scripts/src/secret.js";
import {
  readBalances,
  type BalanceReport,
} from "../../scripts/src/balance.js";

interface RunInputs {
  base: BaseConfig;
  pubkey: string;
  jsonOutput: boolean;
}

function resolveInputs(): RunInputs {
  const { base, rest } = parseBase(process.argv.slice(2));
  const jsonOutput = rest.includes("--json");
  const positional = rest.filter((a) => a !== "--json");

  let pubkey = positional[0];
  if (!pubkey) {
    const secret = loadSecretFromBase(base);
    pubkey = Keypair.fromSecret(secret).publicKey();
  }

  return { base, pubkey, jsonOutput };
}

function renderReport(report: BalanceReport, jsonOutput: boolean) {
  if (jsonOutput) {
    console.log(JSON.stringify(report, null, 2));
    return;
  }
  console.log(`Account: ${report.account}`);
  console.log(`Network: ${report.network}`);
  if (!report.accountExists) {
    console.log("");
    console.log(`Account not found on ${report.network}.`);
    if (report.network === "testnet") {
      console.log(
        `Fund it: curl "https://friendbot.stellar.org?addr=${report.account}"`,
      );
    }
    return;
  }
  console.log("");
  for (const b of report.balances) {
    const tag = b.source === "sac" ? "(SAC — Soroban)" : "(Classic)";
    console.log(`  ${b.asset.padEnd(6)} ${b.amount.padStart(14)}    ${tag}`);
  }
  console.log("");
  console.log(`Reserves: ${report.reserveXlm} XLM`);
  console.log(`Spendable XLM: ${report.spendableXlm}`);
}

async function main() {
  const inputs = resolveInputs();
  const report = await readBalances(inputs.base, inputs.pubkey);
  if (!report.accountExists && !inputs.jsonOutput) {
    renderReport(report, false);
    process.exit(1);
  }
  renderReport(report, inputs.jsonOutput);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
