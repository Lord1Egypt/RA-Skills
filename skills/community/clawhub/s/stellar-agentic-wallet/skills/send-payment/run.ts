/**
 * send-payment — cross-chain USDC/USDT payout from Stellar via Rozo.
 *
 * Flow:
 *   1. Validate destination chain + token pairing
 *   2. Create payment intent via the Rozo client library
 *   3. Show quote to user, confirm on mainnet (always unless --yes)
 *   4. Submit the Stellar Classic USDC payment to the deposit address
 *   5. Print Stellar tx hash; point at status.ts for polling
 *
 * Usage:
 *   npx tsx skills/send-payment/run.ts \
 *     --to <address> --chain <chain> [--token USDC|USDT] --amount <decimal> \
 *     [base flags]
 *
 * Base flags: --secret-file, --network, --horizon-url (see cli-config.ts)
 *
 * NOTE: Rozo operates on mainnet only. --network testnet will error.
 */

import * as readline from "node:readline/promises";
import { createPayment } from "../../scripts/src/rozo-client.js";
import type { RozoCreateRequest } from "../../scripts/src/rozo-client.js";
import { parseBase, type BaseConfig } from "../../scripts/src/cli-config.js";
import { loadSecretFromBase } from "../../scripts/src/secret.js";

const CHAIN_IDS: Record<string, number> = {
  ethereum: 1,
  arbitrum: 42161,
  base: 8453,
  bsc: 56,
  polygon: 137,
  solana: 900,
  stellar: 1500,
};

const PAYOUT_TOKEN_ADDRESSES: Record<
  string,
  Record<"USDC" | "USDT", string | null>
> = {
  ethereum: {
    USDC: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    USDT: "0xdac17f958d2ee523a2206206994597c13d831ec7",
  },
  arbitrum: {
    USDC: "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
    USDT: "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
  },
  base: {
    USDC: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    USDT: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
  },
  bsc: {
    USDC: "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
    USDT: "0x55d398326f99059ff775485246999027b3197955",
  },
  polygon: {
    USDC: "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
    USDT: "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
  },
  solana: {
    USDC: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    USDT: null,
  },
  stellar: {
    USDC: "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
    USDT: null,
  },
};

const STELLAR_USDC_PAYIN =
  "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN";
const MAX_AMOUNT_USD = 10_000;
const MIN_AMOUNT_USD = 0.01;

type Chain = keyof typeof CHAIN_IDS;

export interface CmdArgs {
  to?: string;
  chain?: Chain;
  token: "USDC" | "USDT";
  amount?: string;
  memo?: string;
  json: boolean;
  yes: boolean;
  orderId?: string;
  title?: string;
  description?: string;
}

interface RunInputs {
  base: BaseConfig;
  secret: string;
  args: CmdArgs;
}

function parseCmdArgs(rest: string[]): CmdArgs {
  const a: CmdArgs = { token: "USDC", json: false, yes: false };
  for (let i = 0; i < rest.length; i++) {
    const k = rest[i];
    if (k === "--to") a.to = rest[++i];
    else if (k === "--chain") a.chain = rest[++i].toLowerCase() as Chain;
    else if (k === "--token") a.token = rest[++i].toUpperCase() as "USDC" | "USDT";
    else if (k === "--amount") a.amount = rest[++i];
    else if (k === "--memo") a.memo = rest[++i];
    else if (k === "--order-id") a.orderId = rest[++i];
    else if (k === "--title") a.title = rest[++i];
    else if (k === "--description") a.description = rest[++i];
    else if (k === "--json") a.json = true;
    else if (k === "--yes" || k === "-y") a.yes = true;
  }
  return a;
}

function validateAmount(args: CmdArgs) {
  if (!args.to) throw new Error("--to <address> is required");
  if (!args.chain || !(args.chain in CHAIN_IDS)) {
    throw new Error(
      `--chain <chain> required. Valid: ${Object.keys(CHAIN_IDS).join(", ")}`,
    );
  }
  if (!args.amount) throw new Error("--amount <decimal> is required");

  const token = args.token;
  if (!PAYOUT_TOKEN_ADDRESSES[args.chain][token]) {
    throw new Error(`${token} payout is not supported on ${args.chain}. Use USDC.`);
  }

  const amount = parseFloat(args.amount);
  if (!Number.isFinite(amount) || amount <= 0) {
    throw new Error(`Invalid amount: ${args.amount}`);
  }
  if (amount < MIN_AMOUNT_USD) throw new Error(`Minimum amount is $${MIN_AMOUNT_USD}`);
  if (amount > MAX_AMOUNT_USD) throw new Error(`Maximum per tx is $${MAX_AMOUNT_USD}`);

  return {
    to: args.to,
    chain: args.chain,
    chainId: CHAIN_IDS[args.chain],
    token,
    tokenAddress: PAYOUT_TOKEN_ADDRESSES[args.chain][token]!,
    amount: amount.toFixed(2),
    memo: args.memo,
  };
}

function resolveInputs(externalArgs?: CmdArgs): RunInputs {
  const { base, rest } = parseBase(process.argv.slice(2));
  const args = externalArgs ?? parseCmdArgs(rest);
  if (base.network !== "pubnet") {
    console.error(
      "⚠️  Rozo intent API operates on mainnet. Pass --network pubnet.",
    );
    process.exit(1);
  }
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

async function runSendFlow(inputs: RunInputs): Promise<void> {
  const { base, secret, args } = inputs;
  const v = validateAmount(args);

  const { Keypair } = await import("@stellar/stellar-sdk");
  const sourcePubkey = Keypair.fromSecret(secret).publicKey();

  console.log(
    "=== Rozo cross-chain payment (Stellar USDC → " +
      v.chain +
      " " +
      v.token +
      ") ===",
  );
  console.log(`  From wallet: ${sourcePubkey}`);
  console.log(`  To:          ${v.to}`);
  console.log(`  Destination: ${v.chain} (chainId ${v.chainId})`);
  console.log(`  Token:       ${v.token}`);
  console.log(`  Amount:      ${v.amount} USD (recipient receives exact)`);
  console.log("");

  const body: RozoCreateRequest = {
    appId: "rozoAgent",
    orderId: args.orderId,
    type: "exactOut",
    display: {
      title: args.title ?? `Payment to ${v.to.slice(0, 8)}...`,
      description: args.description,
      currency: "USD",
    },
    source: {
      chainId: CHAIN_IDS.stellar,
      tokenSymbol: "USDC",
      tokenAddress: STELLAR_USDC_PAYIN,
    },
    destination: {
      chainId: v.chainId,
      receiverAddress: v.to,
      receiverMemo: v.memo,
      tokenSymbol: v.token,
      tokenAddress: v.tokenAddress,
      amount: v.amount,
    },
  };

  console.log("Creating Rozo payment intent...");
  const intent = await createPayment(body);

  const fee = intent.source.fee ?? "0";
  const totalSource = intent.source.amount;

  console.log("");
  console.log(`✅ Intent created`);
  console.log(`   Payment ID:  ${intent.id}`);
  console.log(`   Status:      ${intent.status}`);
  console.log(`   Expires:     ${intent.expiresAt}`);
  console.log("");
  console.log(`   You will send:     ${totalSource} USDC on Stellar`);
  console.log(
    `   Recipient gets:    ${intent.destination.amount} ${v.token} on ${v.chain}`,
  );
  console.log(`   Fee:               ${fee} USDC`);
  console.log("");
  console.log(`   Deposit address:   ${intent.source.receiverAddress}`);
  if (intent.source.receiverMemo) {
    console.log(`   Deposit memo:      ${intent.source.receiverMemo}   ⚠️ REQUIRED`);
  }

  if (args.json) {
    console.log("");
    console.log(JSON.stringify(intent, null, 2));
  }

  if (!args.yes) {
    console.log("");
    const ok = await confirm(
      `Send ${totalSource} USDC from your Stellar wallet to the deposit address above? (yes/no) `,
    );
    if (!ok) {
      console.log(
        "Aborted. Payment ID retained — you can fund it later before " +
          intent.expiresAt,
      );
      process.exit(0);
    }
  }

  console.log("");
  console.log("Sending Stellar USDC to deposit address...");

  const { Horizon, Asset, Networks, Operation, TransactionBuilder, BASE_FEE, Memo } =
    await import("@stellar/stellar-sdk");
  const horizon = new Horizon.Server(base.horizonUrl);
  const account = await horizon.loadAccount(sourcePubkey);

  const usdcAsset = new Asset(
    "USDC",
    "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
  );

  const txBuilder = new TransactionBuilder(account, {
    fee: BASE_FEE,
    networkPassphrase: Networks.PUBLIC,
  })
    .addOperation(
      Operation.payment({
        destination: intent.source.receiverAddress,
        asset: usdcAsset,
        amount: totalSource,
      }),
    )
    .setTimeout(60);

  if (intent.source.receiverMemo) {
    txBuilder.addMemo(Memo.text(intent.source.receiverMemo));
  }

  const tx = txBuilder.build();
  tx.sign(Keypair.fromSecret(secret));

  const result = await horizon.submitTransaction(tx);

  console.log("");
  console.log(`✅ Stellar payment submitted`);
  console.log(`   Stellar tx hash: ${result.hash}`);
  console.log(
    `   View:            https://stellar.expert/explorer/public/tx/${result.hash}`,
  );
  console.log("");
  console.log(`Poll status: npx tsx skills/send-payment/status.ts ${intent.id}`);
}

/**
 * Exported entry point used by skills/bridge/run.ts, which wants to
 * construct CmdArgs in-process and reuse this module's logic.
 */
export async function main(externalArgs?: CmdArgs) {
  const inputs = resolveInputs(externalArgs);
  await runSendFlow(inputs);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((err) => {
    console.error(`❌ ${err.message}`);
    if (err?.response?.data) {
      console.error("Horizon error:", JSON.stringify(err.response.data, null, 2));
    }
    process.exit(1);
  });
}
