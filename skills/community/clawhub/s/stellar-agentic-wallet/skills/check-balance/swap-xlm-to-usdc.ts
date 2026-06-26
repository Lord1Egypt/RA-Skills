/**
 * swap-xlm-to-usdc — swap XLM for USDC on the Stellar Classic DEX.
 *
 * Two modes:
 *   1. "I want to spend N XLM"   → --xlm <amount>   (strict send)
 *   2. "I want to receive N USDC" → --usdc <amount>  (strict receive)
 *
 * Usage:
 *   npx tsx skills/check-balance/swap-xlm-to-usdc.ts --xlm 10 [base flags]
 *   npx tsx skills/check-balance/swap-xlm-to-usdc.ts --usdc 1
 *   npx tsx skills/check-balance/swap-xlm-to-usdc.ts --usdc 5 --slippage 0.02
 *
 * Confirmation gates:
 *   - Mainnet always prompts unless --yes.
 *   - Any swap above 50,000 XLM or 10,000 USDC always prompts even on testnet.
 *
 * Default slippage: 1%.
 *
 * Base flags: --secret-file, --network, --horizon-url (see cli-config.ts)
 */

import {
  Asset,
  Horizon,
  Keypair,
  Networks,
  Operation,
  TransactionBuilder,
  BASE_FEE,
} from "@stellar/stellar-sdk";
import * as readline from "node:readline/promises";
import { parseBase, type BaseConfig } from "../../scripts/src/cli-config.js";
import { loadSecretFromBase } from "../../scripts/src/secret.js";

const USDC_ISSUERS: Record<string, string> = {
  testnet: "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
  pubnet: "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
};

const LARGE_XLM_THRESHOLD = 50_000;
const LARGE_USDC_THRESHOLD = 10_000;

export interface SwapArgs {
  mode: "xlm" | "usdc";
  amount: string;
  slippage: number;
  yes: boolean;
}

interface RunInputs {
  base: BaseConfig;
  secret: string;
  args: SwapArgs;
}

function parseCmdArgs(rest: string[]): SwapArgs {
  let mode: "xlm" | "usdc" | null = null;
  let amount: string | null = null;
  let slippage = 0.01;
  let yes = false;

  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === "--xlm") {
      mode = "xlm";
      amount = rest[++i];
    } else if (a === "--usdc") {
      mode = "usdc";
      amount = rest[++i];
    } else if (a === "--slippage") {
      slippage = parseFloat(rest[++i]);
    } else if (a === "--yes" || a === "-y") {
      yes = true;
    } else if (!a.startsWith("--") && !amount) {
      mode = "xlm";
      amount = a;
    }
  }

  if (!amount || !mode) {
    console.error("Usage:");
    console.error("  swap-xlm-to-usdc.ts --xlm <amount>      # spend N XLM");
    console.error("  swap-xlm-to-usdc.ts --usdc <amount>     # receive N USDC");
    console.error("");
    console.error("Options:");
    console.error("  --slippage 0.01     # default 1%");
    console.error("  --yes               # skip confirmation (large-amount gate still fires)");
    process.exit(1);
  }

  const n = parseFloat(amount);
  if (!Number.isFinite(n) || n <= 0) {
    console.error(`Invalid amount: ${amount}`);
    process.exit(1);
  }

  return { mode, amount, slippage, yes };
}

function resolveInputs(): RunInputs {
  const { base, rest } = parseBase(process.argv.slice(2));
  const args = parseCmdArgs(rest);
  const secret = loadSecretFromBase(base);
  return { base, secret, args };
}

async function confirm(prompt: string): Promise<boolean> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  const ans = await rl.question(prompt);
  rl.close();
  return ans.trim().toLowerCase() === "yes";
}

/**
 * Execute the XLM↔USDC swap. Exported so callers (e.g. onboard)
 * can invoke this in-process instead of spawning a child tsx call.
 * The CLI entry point at the bottom wraps this for direct
 * `npx tsx swap-xlm-to-usdc.ts` invocations.
 */
export async function runSwap(inputs: RunInputs): Promise<void> {
  const { base, secret, args } = inputs;
  const passphrase =
    base.network === "pubnet" ? Networks.PUBLIC : Networks.TESTNET;
  const keypair = Keypair.fromSecret(secret);
  const pubkey = keypair.publicKey();
  const horizon = new Horizon.Server(base.horizonUrl);

  const issuer = USDC_ISSUERS[base.network];
  const usdc = new Asset("USDC", issuer);

  const account = await horizon.loadAccount(pubkey);
  const hasTrustline = account.balances.some(
    (b) =>
      "asset_code" in b && b.asset_code === "USDC" && b.asset_issuer === issuer,
  );
  if (!hasTrustline) {
    console.error("❌ No USDC trustline on this account.");
    console.error("   Run: npx tsx skills/check-balance/add-trustline.ts");
    process.exit(1);
  }

  let xlmAmount: string;
  let usdcAmount: string;
  let hops: any[] = [];
  let opBuilder: any;

  if (args.mode === "xlm") {
    console.log(
      `Quoting swap: spend ${args.amount} XLM → receive USDC on ${base.network}...`,
    );
    const paths = await horizon
      .strictSendPaths(Asset.native(), args.amount, [usdc])
      .call();
    if (paths.records.length === 0) {
      console.error("❌ No swap path found — insufficient DEX liquidity.");
      process.exit(1);
    }
    const best = paths.records.sort(
      (a, b) => parseFloat(b.destination_amount) - parseFloat(a.destination_amount),
    )[0];

    xlmAmount = args.amount;
    const quoted = parseFloat(best.destination_amount);
    usdcAmount = quoted.toFixed(7);
    const minUsdc = (quoted * (1 - args.slippage)).toFixed(7);
    hops = best.path;

    console.log("");
    console.log(`  Send:         ${xlmAmount} XLM`);
    console.log(`  Quote:        ${usdcAmount} USDC`);
    console.log(`  Min receive:  ${minUsdc} USDC (${(args.slippage * 100).toFixed(1)}% slippage)`);
    console.log(`  Path hops:    ${hops.length}`);
    console.log("");

    opBuilder = () =>
      Operation.pathPaymentStrictSend({
        sendAsset: Asset.native(),
        sendAmount: xlmAmount,
        destination: pubkey,
        destAsset: usdc,
        destMin: minUsdc,
        path: hops.map((p: any) =>
          p.asset_type === "native"
            ? Asset.native()
            : new Asset(p.asset_code, p.asset_issuer),
        ),
      });
  } else {
    console.log(
      `Quoting swap: receive exactly ${args.amount} USDC → send XLM on ${base.network}...`,
    );
    const paths = await horizon
      .strictReceivePaths([Asset.native()], usdc, args.amount)
      .call();
    if (paths.records.length === 0) {
      console.error("❌ No swap path found — insufficient DEX liquidity.");
      process.exit(1);
    }
    const best = paths.records.sort(
      (a, b) => parseFloat(a.source_amount) - parseFloat(b.source_amount),
    )[0];

    usdcAmount = args.amount;
    const quoted = parseFloat(best.source_amount);
    xlmAmount = quoted.toFixed(7);
    const maxXlm = (quoted * (1 + args.slippage)).toFixed(7);
    hops = best.path;

    console.log("");
    console.log(`  Receive:      ${usdcAmount} USDC (exact)`);
    console.log(`  Quote:        ${xlmAmount} XLM`);
    console.log(`  Max spend:    ${maxXlm} XLM (${(args.slippage * 100).toFixed(1)}% slippage)`);
    console.log(`  Path hops:    ${hops.length}`);
    console.log("");

    opBuilder = () =>
      Operation.pathPaymentStrictReceive({
        sendAsset: Asset.native(),
        sendMax: maxXlm,
        destination: pubkey,
        destAsset: usdc,
        destAmount: usdcAmount,
        path: hops.map((p: any) =>
          p.asset_type === "native"
            ? Asset.native()
            : new Asset(p.asset_code, p.asset_issuer),
        ),
      });
  }

  const xlmNum = parseFloat(xlmAmount);
  const usdcNum = parseFloat(usdcAmount);
  const isLarge =
    xlmNum >= LARGE_XLM_THRESHOLD || usdcNum >= LARGE_USDC_THRESHOLD;

  if (isLarge) {
    console.log(
      `⚠️  Large swap threshold hit (> ${LARGE_XLM_THRESHOLD} XLM or > ${LARGE_USDC_THRESHOLD} USDC).`,
    );
    const ok = await confirm("Confirm large swap? (yes/no) ");
    if (!ok) {
      console.log("Aborted.");
      process.exit(0);
    }
  } else if (base.network === "pubnet" && !args.yes) {
    const ok = await confirm("Confirm mainnet swap? (yes/no) ");
    if (!ok) {
      console.log("Aborted.");
      process.exit(0);
    }
  }

  const tx = new TransactionBuilder(account, {
    fee: BASE_FEE,
    networkPassphrase: passphrase,
  })
    .addOperation(opBuilder())
    .setTimeout(60)
    .build();

  tx.sign(keypair);
  const result = await horizon.submitTransaction(tx);

  console.log("");
  console.log(`✅ Swap executed`);
  console.log(`   Tx hash: ${result.hash}`);
  console.log(
    `   View:    https://stellar.expert/explorer/${base.network === "pubnet" ? "public" : "testnet"}/tx/${result.hash}`,
  );
}

async function main() {
  const inputs = resolveInputs();
  await runSwap(inputs);
}

// Run as CLI only when invoked directly (not when imported by
// another skill such as onboard).
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((err) => {
    if (err?.response?.data) {
      console.error("Horizon error:", JSON.stringify(err.response.data, null, 2));
    } else {
      console.error(err);
    }
    process.exit(1);
  });
}
