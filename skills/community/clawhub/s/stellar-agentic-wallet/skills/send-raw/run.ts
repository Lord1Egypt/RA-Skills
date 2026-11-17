/**
 * send-raw — submit a single Stellar Classic payment, exactly as specified.
 *
 * This is the low-level primitive the rest of the skill was missing. Every
 * other spending command in this repo *originates* a payment: send-payment
 * and bridge both POST a new Rozo intent and then fund the deposit address
 * Rozo hands back. There was no way to say "pay this address, this asset,
 * this amount, with this memo" when the address and memo came from
 * somewhere else — an invoice, a checkout skill, an exchange deposit slip.
 *
 * That gap forced callers into a hand-rolled `stellar tx new payment
 * --build-only` → decode → patch JSON to inject the memo → encode → sign →
 * send pipeline, because the Stellar CLI's `tx new payment` has no --memo
 * flag. Getting the memo wrong on a deposit means the funds land but are
 * never credited, so the hand-rolled path is exactly the wrong place to be
 * improvising.
 *
 * Flow:
 *   1. Resolve asset + memo from flags, validate both
 *   2. Preflight: source funded, source holds the asset, destination exists
 *      and (for non-native assets) trusts the asset, amount is affordable
 *   3. Show the full payment for review, confirm on mainnet (unless --yes)
 *   4. Build → sign → submit via Horizon
 *   5. Print tx hash + explorer link
 *
 * Usage:
 *   ./node_modules/.bin/tsx skills/send-raw/run.ts \
 *     --to <G...> --amount <decimal> [--asset USDC|XLM|CODE:ISSUER] \
 *     [--memo <value>] [--memo-type text|id|hash|return] [base flags]
 *
 * Base flags: --secret-file / --identity, --network, --horizon-url
 * (see cli-config.ts).
 */

import * as readline from "node:readline/promises";
import { parseBase, baseFlagsHelp, type BaseConfig } from "../../scripts/src/cli-config.js";
import { loadSecretFromBase } from "../../scripts/src/secret.js";
import { CLASSIC_USDC_ISSUERS } from "../../scripts/src/balance.js";

export type MemoType = "text" | "id" | "hash" | "return";

const MEMO_TYPES: MemoType[] = ["text", "id", "hash", "return"];

/** Stellar Classic amounts carry at most 7 decimal places (1 stroop). */
const MAX_DECIMALS = 7;

/** MEMO_TEXT is capped at 28 *bytes*, not characters. */
const MEMO_TEXT_MAX_BYTES = 28;

export interface CmdArgs {
  to?: string;
  amount?: string;
  asset: string;
  memo?: string;
  memoType: MemoType;
  json: boolean;
  yes: boolean;
}

export interface RunInputs {
  base: BaseConfig;
  secret: string;
  args: CmdArgs;
}

export function parseCmdArgs(rest: string[]): CmdArgs {
  const a: CmdArgs = { asset: "USDC", memoType: "text", json: false, yes: false };
  for (let i = 0; i < rest.length; i++) {
    const k = rest[i];
    if (k === "--to") a.to = rest[++i];
    else if (k === "--amount") a.amount = rest[++i];
    else if (k === "--asset") a.asset = rest[++i];
    else if (k === "--memo") a.memo = rest[++i];
    else if (k === "--memo-type") a.memoType = rest[++i]?.toLowerCase() as MemoType;
    else if (k === "--json") a.json = true;
    else if (k === "--yes" || k === "-y") a.yes = true;
    else if (k === "--help" || k === "-h") {
      printHelp();
      process.exit(0);
    } else throw new Error(`Unknown flag: ${k}`);
  }
  return a;
}

function printHelp(): void {
  console.log(
    [
      "send-raw — submit one Stellar Classic payment exactly as specified.",
      "",
      "Usage:",
      "  ./node_modules/.bin/tsx skills/send-raw/run.ts --to <G...> --amount <decimal> \\",
      "    [--asset USDC|XLM|CODE:ISSUER] [--memo <value>] [--memo-type text|id|hash|return] [-y]",
      "",
      "Flags:",
      "  --to <G...>             Destination Stellar account (required)",
      "  --amount <decimal>      Amount to send, max 7 decimals (required)",
      `  --asset <spec>          USDC (default), XLM, or CODE:ISSUER`,
      "  --memo <value>          Memo to attach — required by most deposit addresses",
      `  --memo-type <type>      ${MEMO_TYPES.join(" | ")} (default: text)`,
      "  --json                  Print a JSON result line after submission",
      "  --yes, -y               Skip the confirmation prompt (never do this on mainnet",
      "                          without independently verifying destination + memo)",
      "",
      baseFlagsHelp(),
    ].join("\n"),
  );
}

/**
 * Turn an --asset spec into an SDK Asset.
 *
 * "XLM"/"native" is the native asset. A bare "USDC" resolves to the Circle
 * issuer for the selected network, which is the only bare code we special-case
 * — every other asset must be written CODE:ISSUER so there is no ambiguity
 * about which issuer's token is being sent.
 */
export async function resolveAsset(
  spec: string,
  network: "testnet" | "pubnet",
): Promise<import("@stellar/stellar-sdk").Asset> {
  const { Asset, StrKey } = await import("@stellar/stellar-sdk");
  const s = spec.trim();

  if (s.toUpperCase() === "XLM" || s.toLowerCase() === "native") {
    return Asset.native();
  }
  if (s.toUpperCase() === "USDC") {
    return new Asset("USDC", CLASSIC_USDC_ISSUERS[network]);
  }
  // Exactly two components. Destructuring a longer split would silently
  // ignore the tail, so "EURC:ISSUER_A:ISSUER_B" would pay ISSUER_A's asset —
  // the wrong token, irreversibly, from a flag the user believed was explicit.
  const parts = s.split(":");
  if (parts.length !== 2 || !parts[0] || !parts[1]) {
    throw new Error(
      `--asset "${spec}" not understood. Use XLM, USDC, or CODE:ISSUER ` +
        `(e.g. EURC:GDHU6WRG4IEQXM5NZ4BMPKOXHW76MZM4Y2IEMFDVXBSDP6SJY4ITNPP2).`,
    );
  }
  const [code, issuer] = parts;
  if (!/^[A-Za-z0-9]{1,12}$/.test(code)) {
    throw new Error(
      `--asset code "${code}" is not a valid Stellar asset code ` +
        `(1-12 alphanumeric characters).`,
    );
  }
  if (!StrKey.isValidEd25519PublicKey(issuer)) {
    throw new Error(`--asset issuer "${issuer}" is not a valid Stellar public key.`);
  }
  return new Asset(code, issuer);
}

/**
 * Validate the amount as a Stellar Classic amount string.
 *
 * Returned verbatim (not re-formatted via Number) so that an exact amount
 * like "1.0500" survives the round trip. Deposit addresses that reconcile
 * on an exact match will reject a payment that drifts by a stroop.
 */
export function normalizeAmount(raw: string): string {
  const s = raw.trim();
  if (!/^\d+(\.\d+)?$/.test(s)) {
    throw new Error(`--amount "${raw}" is not a positive decimal number.`);
  }
  const decimals = s.includes(".") ? s.split(".")[1].length : 0;
  if (decimals > MAX_DECIMALS) {
    throw new Error(
      `--amount "${raw}" has ${decimals} decimal places; Stellar allows at most ${MAX_DECIMALS}.`,
    );
  }
  if (Number(s) <= 0) throw new Error(`--amount "${raw}" must be greater than zero.`);
  return s;
}

/** Build the SDK Memo for the requested type, enforcing each type's limits. */
export async function resolveMemo(
  value: string | undefined,
  type: MemoType,
): Promise<import("@stellar/stellar-sdk").Memo | undefined> {
  if (value === undefined) return undefined;
  const { Memo } = await import("@stellar/stellar-sdk");

  if (!MEMO_TYPES.includes(type)) {
    throw new Error(`--memo-type must be one of ${MEMO_TYPES.join(", ")}, got "${type}".`);
  }

  switch (type) {
    case "text": {
      // Memos routinely arrive from an external system (a checkout order, an
      // exchange deposit slip). The confirmation prompt is the human's last
      // chance to verify the destination, so a memo carrying ANSI escapes or
      // control characters could scroll or rewrite that display after the
      // destination has been printed. No legitimate deposit memo needs them.
      if (/[\u0000-\u001f\u007f-\u009f]/.test(value)) {
        throw new Error(
          "MEMO_TEXT contains control characters. These can rewrite the " +
            "confirmation display and hide what is actually being signed.",
        );
      }
      const bytes = Buffer.byteLength(value, "utf8");
      if (bytes > MEMO_TEXT_MAX_BYTES) {
        throw new Error(
          `MEMO_TEXT is limited to ${MEMO_TEXT_MAX_BYTES} bytes; "${value}" is ${bytes}.`,
        );
      }
      return Memo.text(value);
    }
    case "id": {
      if (!/^\d+$/.test(value)) {
        throw new Error(`MEMO_ID must be an unsigned integer, got "${value}".`);
      }
      return Memo.id(value);
    }
    case "hash":
    case "return": {
      if (!/^[0-9a-fA-F]{64}$/.test(value)) {
        throw new Error(
          `MEMO_${type.toUpperCase()} must be 64 hex characters (32 bytes), got "${value}".`,
        );
      }
      return type === "hash" ? Memo.hash(value) : Memo.return(value);
    }
  }
}

export interface Preflight {
  sourcePubkey: string;
  destExists: boolean;
  destTrustsAsset: boolean;
  sourceAssetBalance: string;
  spendableXlm: string;
}

/** One XLM = 10,000,000 stroops. */
const STROOPS_PER_UNIT = 10_000_000n;

/** Base reserve (1 XLM) + 0.5 XLM per subentry, in stroops. */
const BASE_RESERVE_STROOPS = 10_000_000n;
const PER_SUBENTRY_STROOPS = 5_000_000n;

/** Network fee for a 1-operation transaction, in stroops (BASE_FEE = 100). */
const FEE_STROOPS = 100n;

/**
 * Convert a Stellar decimal amount string to stroops, exactly.
 *
 * All affordability math runs in stroops. Doing it in JS floats invites
 * classic binary-fraction errors — `0.1 + 0.2 > 0.3` is true — which at the
 * boundary means either refusing a payment the wallet can afford or, worse,
 * submitting one it cannot. A transaction that fails on-chain still burns
 * its fee.
 */
export function toStroops(amount: string): bigint {
  const [whole, frac = ""] = amount.trim().split(".");
  return BigInt(whole || "0") * STROOPS_PER_UNIT + BigInt(frac.padEnd(7, "0").slice(0, 7));
}

function fromStroops(stroops: bigint): string {
  const neg = stroops < 0n;
  const abs = neg ? -stroops : stroops;
  const whole = abs / STROOPS_PER_UNIT;
  const frac = (abs % STROOPS_PER_UNIT).toString().padStart(7, "0");
  return `${neg ? "-" : ""}${whole}.${frac}`;
}

/**
 * Read both accounts before building anything.
 *
 * Every check here maps to a Horizon rejection we would otherwise only
 * discover after signing: op_no_destination (dest missing), op_no_trust
 * (dest has no trustline or it is unauthorized), op_line_full (destination
 * at its trustline limit), op_underfunded (source short), and the
 * below-reserve failures for the XLM fee.
 *
 * Balances are read net of `selling_liabilities` — XLM or tokens already
 * committed to open DEX offers are not spendable, and Horizon reports the
 * gross balance.
 */
export async function preflight(
  base: BaseConfig,
  sourcePubkey: string,
  destination: string,
  asset: import("@stellar/stellar-sdk").Asset,
  amount: string,
): Promise<Preflight> {
  const { Horizon } = await import("@stellar/stellar-sdk");
  const horizon = new Horizon.Server(base.horizonUrl);

  let sourceAccount;
  try {
    sourceAccount = await horizon.loadAccount(sourcePubkey);
  } catch (err: any) {
    if (err?.response?.status === 404) {
      throw new Error(
        `Source account ${sourcePubkey} does not exist on ${base.network}. Fund it first.`,
      );
    }
    throw err;
  }

  const matches = (b: any) =>
    asset.isNative()
      ? b.asset_type === "native"
      : b.asset_code === asset.getCode() && b.asset_issuer === asset.getIssuer();

  const sourceLine = sourceAccount.balances.find(matches);
  if (!sourceLine) {
    throw new Error(
      `Source wallet has no ${assetLabel(asset)} trustline. ` +
        `Add one with: ./node_modules/.bin/tsx skills/check-balance/add-trustline.ts --network ${base.network}`,
    );
  }

  // A trustline can exist but be unauthorized by the issuer, in which case
  // the payment fails with op_src_not_authorized.
  if (!asset.isNative() && (sourceLine as any).is_authorized === false) {
    throw new Error(
      `Source wallet's ${assetLabel(asset)} trustline is not authorized by the issuer.`,
    );
  }

  const xlmLine: any = sourceAccount.balances.find((b: any) => b.asset_type === "native");
  const reserveStroops =
    BASE_RESERVE_STROOPS + PER_SUBENTRY_STROOPS * BigInt(sourceAccount.subentry_count);
  const xlmStroops = toStroops(xlmLine?.balance ?? "0");
  const xlmSellingLiabilities = toStroops(xlmLine?.selling_liabilities ?? "0");
  const spendableXlmStroops = xlmStroops - reserveStroops - xlmSellingLiabilities;
  const spendableXlm = fromStroops(spendableXlmStroops);

  const amountStroops = toStroops(amount);
  const assetSellingLiabilities = toStroops((sourceLine as any).selling_liabilities ?? "0");
  const availableStroops = toStroops(sourceLine.balance) - assetSellingLiabilities;

  // XLM is the only asset where the amount and the fee come out of the same
  // pot, and it is also the only one constrained by the minimum reserve.
  const neededStroops = asset.isNative() ? amountStroops + FEE_STROOPS : amountStroops;
  const affordableStroops = asset.isNative() ? spendableXlmStroops : availableStroops;

  if (affordableStroops < neededStroops) {
    const liabilityNote =
      assetSellingLiabilities > 0n || (asset.isNative() && xlmSellingLiabilities > 0n)
        ? ` (some is reserved by open DEX offers)`
        : "";
    throw new Error(
      `Insufficient ${assetLabel(asset)}: need ${fromStroops(neededStroops)}` +
        `${asset.isNative() ? " including the network fee" : ""}, ` +
        `wallet has ${fromStroops(affordableStroops)} available${liabilityNote}.`,
    );
  }

  // The fee is paid in XLM regardless of which asset is being sent, and it
  // cannot dip into the account's minimum reserve.
  if (spendableXlmStroops < FEE_STROOPS) {
    throw new Error(
      `Not enough spendable XLM to pay the network fee (balance ` +
        `${xlmLine?.balance ?? "0"}, reserve ${fromStroops(reserveStroops)}, ` +
        `spendable ${spendableXlm}). Top up XLM before sending.`,
    );
  }

  let destExists = true;
  let destTrustsAsset = false;
  try {
    const destAccount = await horizon.loadAccount(destination);
    if (asset.isNative()) {
      destTrustsAsset = true;
    } else {
      const destLine: any = destAccount.balances.find(matches);
      if (destLine) {
        if (destLine.is_authorized === false) {
          throw new Error(
            `Destination's ${assetLabel(asset)} trustline is not authorized by the issuer ` +
              `— the payment would fail with op_not_authorized.`,
          );
        }
        // A trustline has a ceiling. Exceeding it fails with op_line_full.
        if (destLine.limit) {
          const headroom =
            toStroops(destLine.limit) -
            toStroops(destLine.balance) -
            toStroops(destLine.buying_liabilities ?? "0");
          if (headroom < amountStroops) {
            throw new Error(
              `Destination cannot receive ${amount} ${asset.getCode()} — its trustline ` +
                `has only ${fromStroops(headroom)} of headroom left (op_line_full).`,
            );
          }
        }
        destTrustsAsset = true;
      }
    }
  } catch (err: any) {
    if (err?.response?.status === 404) destExists = false;
    else throw err;
  }

  return {
    sourcePubkey,
    destExists,
    destTrustsAsset,
    sourceAssetBalance: sourceLine.balance,
    spendableXlm,
  };
}

function assetLabel(asset: import("@stellar/stellar-sdk").Asset): string {
  return asset.isNative() ? "XLM" : `${asset.getCode()}:${asset.getIssuer()}`;
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

export interface SendResult {
  hash: string;
  ledger?: number;
  from: string;
  to: string;
  asset: string;
  amount: string;
  memo?: string;
  memoType?: MemoType;
  network: "testnet" | "pubnet";
}

export async function sendRaw(inputs: RunInputs): Promise<SendResult> {
  const { base, secret, args } = inputs;

  if (!args.to) throw new Error("--to <G...> is required");
  if (!args.amount) throw new Error("--amount <decimal> is required");

  const {
    Keypair,
    StrKey,
    Networks,
    Operation,
    TransactionBuilder,
    Horizon,
    BASE_FEE,
  } = await import("@stellar/stellar-sdk");

  if (!StrKey.isValidEd25519PublicKey(args.to)) {
    if (args.to.startsWith("C")) {
      throw new Error(
        `--to "${args.to}" is a Soroban contract address (C...). ` +
          `Classic payments cannot fund a contract — the recipient must invoke its pay() function.`,
      );
    }
    throw new Error(`--to "${args.to}" is not a valid Stellar account address (G...).`);
  }

  const amount = normalizeAmount(args.amount);
  const asset = await resolveAsset(args.asset, base.network);
  const memo = await resolveMemo(args.memo, args.memoType);

  const sourcePubkey = Keypair.fromSecret(secret).publicKey();
  if (sourcePubkey === args.to) {
    throw new Error("--to is this wallet's own address; a self-payment is a no-op.");
  }

  const pf = await preflight(base, sourcePubkey, args.to, asset, amount);

  if (!pf.destExists) {
    throw new Error(
      `Destination ${args.to} does not exist on ${base.network}. ` +
        `A payment to an unfunded account fails (op_no_destination) — it must be created first.`,
    );
  }
  if (!pf.destTrustsAsset) {
    throw new Error(
      `Destination ${args.to} has no ${assetLabel(asset)} trustline. ` +
        `The payment would fail with op_no_trust.`,
    );
  }

  console.log(`=== Stellar Classic payment (${base.network}) ===`);
  console.log(`  From:    ${sourcePubkey}`);
  console.log(`  To:      ${args.to}`);
  console.log(`  Asset:   ${assetLabel(asset)}`);
  console.log(`  Amount:  ${amount}`);
  if (args.memo !== undefined) {
    console.log(`  Memo:    ${args.memo}   (MEMO_${args.memoType.toUpperCase()})`);
  } else {
    console.log(
      `  Memo:    (none)   ⚠️  Deposit addresses at exchanges and payment ` +
        `processors usually require one — without it funds may not be credited.`,
    );
  }
  console.log(`  Balance: ${pf.sourceAssetBalance} ${asset.isNative() ? "XLM" : asset.getCode()}`);

  if (!args.yes) {
    console.log("");
    const ok = await confirm(
      base.network === "pubnet"
        ? "Send this MAINNET payment? Verify destination and memo above. (yes/no) "
        : "Send this testnet payment? (yes/no) ",
    );
    if (!ok) {
      console.log("Aborted — nothing was signed or submitted.");
      process.exit(0);
    }
  }

  const horizon = new Horizon.Server(base.horizonUrl);
  const account = await horizon.loadAccount(sourcePubkey);

  const builder = new TransactionBuilder(account, {
    fee: BASE_FEE,
    networkPassphrase:
      base.network === "pubnet" ? Networks.PUBLIC : Networks.TESTNET,
  })
    .addOperation(Operation.payment({ destination: args.to, asset, amount }))
    .setTimeout(60);

  if (memo) builder.addMemo(memo);

  const tx = builder.build();
  tx.sign(Keypair.fromSecret(secret));

  const submitted: any = await horizon.submitTransaction(tx);

  const explorer =
    base.network === "pubnet"
      ? `https://stellar.expert/explorer/public/tx/${submitted.hash}`
      : `https://stellar.expert/explorer/testnet/tx/${submitted.hash}`;

  console.log("");
  console.log("✅ Payment submitted");
  console.log(`   Tx hash: ${submitted.hash}`);
  console.log(`   Ledger:  ${submitted.ledger}`);
  console.log(`   View:    ${explorer}`);

  const result: SendResult = {
    hash: submitted.hash,
    ledger: submitted.ledger,
    from: sourcePubkey,
    to: args.to,
    asset: assetLabel(asset),
    amount,
    memo: args.memo,
    memoType: args.memo !== undefined ? args.memoType : undefined,
    network: base.network,
  };

  if (args.json) {
    console.log(JSON.stringify(result, null, 2));
  }
  return result;
}

export async function main(externalArgs?: CmdArgs): Promise<SendResult> {
  const { base, rest } = parseBase(process.argv.slice(2));
  const args = externalArgs ?? parseCmdArgs(rest);
  const secret = loadSecretFromBase(base);
  return sendRaw({ base, secret, args });
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((err) => {
    console.error(`❌ ${err.message}`);
    const horizonExtras = err?.response?.data?.extras;
    if (horizonExtras) {
      console.error("Horizon error:", JSON.stringify(horizonExtras, null, 2));
    }
    process.exit(1);
  });
}
