/**
 * add-trustline — add a USDC Classic trustline to this account.
 *
 * You need a Classic trustline to HOLD USDC on Stellar. SAC balances
 * (Soroban token contract) do NOT need a trustline — but if you want
 * to receive Classic USDC payments, swap on the DEX, or cash out, you do.
 *
 * Usage:
 *   npx tsx skills/check-balance/add-trustline.ts [base flags]
 *
 * Base flags: --secret-file, --network, --horizon-url  (see cli-config.ts)
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
import { parseBase, type BaseConfig } from "../../scripts/src/cli-config.js";
import { loadSecretFromBase } from "../../scripts/src/secret.js";

const USDC_ISSUERS: Record<string, string> = {
  testnet: "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
  pubnet: "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
};

interface RunInputs {
  base: BaseConfig;
  secret: string;
}

function resolveInputs(): RunInputs {
  const { base } = parseBase(process.argv.slice(2));
  const secret = loadSecretFromBase(base);
  return { base, secret };
}

/**
 * Add a USDC Classic trustline. Exported so callers (e.g. onboard)
 * can invoke this in-process instead of spawning a child tsx call.
 * The CLI entry point at the bottom of this file wraps the same
 * function for direct `npx tsx add-trustline.ts` invocations.
 */
export async function runAddTrustline(inputs: RunInputs): Promise<void> {
  const { base, secret } = inputs;
  const passphrase =
    base.network === "pubnet" ? Networks.PUBLIC : Networks.TESTNET;
  const keypair = Keypair.fromSecret(secret);
  const pubkey = keypair.publicKey();
  const horizon = new Horizon.Server(base.horizonUrl);

  const issuer = USDC_ISSUERS[base.network];
  const usdc = new Asset("USDC", issuer);

  const account = await horizon.loadAccount(pubkey);

  const already = account.balances.some(
    (b) =>
      "asset_code" in b &&
      b.asset_code === "USDC" &&
      b.asset_issuer === issuer,
  );
  if (already) {
    console.log(`Trustline to USDC (${base.network}) already exists.`);
    console.log(`  Issuer: ${issuer}`);
    return;
  }

  console.log(`Adding USDC trustline on ${base.network}...`);
  console.log(`  Account: ${pubkey}`);
  console.log(`  Issuer:  ${issuer}`);

  const tx = new TransactionBuilder(account, {
    fee: BASE_FEE,
    networkPassphrase: passphrase,
  })
    .addOperation(Operation.changeTrust({ asset: usdc }))
    .setTimeout(60)
    .build();

  tx.sign(keypair);
  const result = await horizon.submitTransaction(tx);

  console.log("");
  console.log(`✅ Trustline added`);
  console.log(`   Tx hash: ${result.hash}`);
  console.log(
    `   View:    https://stellar.expert/explorer/${base.network === "pubnet" ? "public" : "testnet"}/tx/${result.hash}`,
  );
  console.log("");
  console.log("Minimum balance increased by 0.5 XLM (one new subentry).");
}

async function main() {
  const inputs = resolveInputs();
  await runAddTrustline(inputs);
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
