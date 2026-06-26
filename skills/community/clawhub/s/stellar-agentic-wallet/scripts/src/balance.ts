/**
 * Shared balance reader for Stellar accounts.
 *
 * Used by check-balance and onboard. Reads Classic XLM + USDC via
 * Horizon and (optionally) SAC USDC via Soroban simulation.
 */

import {
  Account,
  Address,
  Contract,
  Horizon,
  Networks,
  TransactionBuilder,
  nativeToScVal,
  rpc,
  scValToNative,
} from "@stellar/stellar-sdk";
import type { BaseConfig } from "./cli-config.js";

export interface BalanceLine {
  asset: string;
  amount: string;
  source: "classic" | "sac";
}

export interface BalanceReport {
  account: string;
  network: "testnet" | "pubnet";
  accountExists: boolean;
  balances: BalanceLine[];
  hasClassicUsdcTrustline: boolean;
  subentryCount: number;
  reserveXlm: string;
  spendableXlm: string;
}

export const CLASSIC_USDC_ISSUERS: Record<"testnet" | "pubnet", string> = {
  testnet: "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
  pubnet: "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
};

/** Base reserve (1 XLM) + 0.5 XLM per subentry — Stellar minimum balance rule. */
export function computeReserveXlm(subentryCount: number): string {
  return (1 + 0.5 * subentryCount).toFixed(7);
}

export async function readBalances(
  base: BaseConfig,
  pubkey: string,
): Promise<BalanceReport> {
  const horizon = new Horizon.Server(base.horizonUrl);
  const balances: BalanceLine[] = [];
  let xlmClassic = "0";
  let subentryCount = 0;
  let hasTrustline = false;
  let accountExists = true;

  try {
    const account = await horizon.loadAccount(pubkey);
    subentryCount = account.subentry_count;
    for (const b of account.balances) {
      if (b.asset_type === "native") {
        xlmClassic = b.balance;
        balances.push({ asset: "XLM", amount: b.balance, source: "classic" });
      } else if (
        "asset_code" in b &&
        b.asset_code === "USDC" &&
        b.asset_issuer === CLASSIC_USDC_ISSUERS[base.network]
      ) {
        hasTrustline = true;
        balances.push({ asset: "USDC", amount: b.balance, source: "classic" });
      }
    }
  } catch (err: any) {
    if (err?.response?.status === 404) {
      accountExists = false;
    } else {
      throw err;
    }
  }

  if (accountExists && base.assetSac) {
    try {
      const sacAmount = await readSacBalance(
        base.rpcUrl,
        base.assetSac,
        pubkey,
        base.network,
      );
      if (sacAmount !== null) {
        const humanAmount = (Number(sacAmount) / 10_000_000).toFixed(7);
        balances.push({ asset: "USDC", amount: humanAmount, source: "sac" });
      }
    } catch {
      // SAC read failures are non-fatal — account may simply never have
      // interacted with the SAC, or the RPC endpoint is down.
    }
  }

  const reserveXlm = computeReserveXlm(subentryCount);
  const spendableXlm = (Number(xlmClassic) - Number(reserveXlm)).toFixed(7);

  return {
    account: pubkey,
    network: base.network,
    accountExists,
    balances,
    hasClassicUsdcTrustline: hasTrustline,
    subentryCount,
    reserveXlm,
    spendableXlm,
  };
}

async function readSacBalance(
  rpcUrl: string,
  sacAddress: string,
  accountPubkey: string,
  network: "testnet" | "pubnet",
): Promise<bigint | null> {
  const server = new rpc.Server(rpcUrl, { allowHttp: false });
  const networkPassphrase =
    network === "pubnet" ? Networks.PUBLIC : Networks.TESTNET;
  const contract = new Contract(sacAddress);

  const op = contract.call(
    "balance",
    nativeToScVal(Address.fromString(accountPubkey), { type: "address" }),
  );

  const source = new Account(accountPubkey, "0");
  const tx = new TransactionBuilder(source, { fee: "0", networkPassphrase })
    .addOperation(op)
    .setTimeout(30)
    .build();

  const sim = await server.simulateTransaction(tx);
  if (rpc.Api.isSimulationError(sim)) return null;
  const retval = (sim as any).result?.retval;
  if (!retval) return null;
  const native = scValToNative(retval);
  return typeof native === "bigint" ? native : BigInt(native);
}

export function totalUsdc(report: BalanceReport): number {
  let total = 0;
  for (const b of report.balances) {
    if (b.asset === "USDC") total += Number(b.amount);
  }
  return total;
}
