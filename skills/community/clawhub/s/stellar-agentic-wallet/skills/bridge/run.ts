/**
 * bridge — move Stellar USDC to another chain (your own address).
 *
 * Thin wrapper around send-payment. Destination is always a wallet
 * owned by the user, not a counterparty.
 *
 * Pure in-process import of send-payment's main() — no subprocess spawning.
 *
 * Usage:
 *   npx tsx skills/bridge/run.ts --chain <chain> --amount <decimal> \
 *     --my-address <addr> [base flags]
 */

import { main as sendPaymentMain, type CmdArgs } from "../send-payment/run.js";

type Chain = "ethereum" | "arbitrum" | "base" | "bsc" | "polygon" | "solana";

const VALID_CHAINS: Chain[] = [
  "ethereum",
  "arbitrum",
  "base",
  "bsc",
  "polygon",
  "solana",
];

interface CliArgs {
  chain?: Chain;
  amount?: string;
  myAddress?: string;
  token: "USDC" | "USDT";
  yes: boolean;
}

function parseArgs(): CliArgs {
  const argv = process.argv.slice(2);
  const a: CliArgs = { token: "USDC", yes: false };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === "--chain") a.chain = argv[++i] as Chain;
    else if (k === "--amount") a.amount = argv[++i];
    else if (k === "--my-address") a.myAddress = argv[++i];
    else if (k === "--token") a.token = argv[++i] as "USDC" | "USDT";
    else if (k === "--yes" || k === "-y") a.yes = true;
  }
  return a;
}

async function main() {
  const args = parseArgs();

  if (!args.chain || !VALID_CHAINS.includes(args.chain)) {
    console.error(
      `--chain required. Valid: ${VALID_CHAINS.join(", ")} ` +
        `(Stellar excluded — that's a payment, not a bridge)`,
    );
    process.exit(1);
  }
  if (!args.amount) {
    console.error("--amount <decimal> required");
    process.exit(1);
  }
  if (!args.myAddress) {
    console.error(
      "--my-address <destination> required (your wallet on the target chain)",
    );
    process.exit(1);
  }

  console.log("=== Bridge Stellar USDC → " + args.chain + " ===");
  console.log("(delegating to send-payment)");
  console.log("");

  const sendArgs: CmdArgs = {
    to: args.myAddress,
    chain: args.chain,
    token: args.token,
    amount: args.amount,
    json: false,
    yes: args.yes,
  };

  await sendPaymentMain(sendArgs);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
