/**
 * CLI setup — creates viem clients from resolved config.
 * Ported from x402r-sdk/examples/dev-tools/shared/cli-setup.ts with config file support.
 */
import { type PublicClient, type WalletClient } from "viem";
import { type PrivateKeyAccount } from "viem/accounts";
import { type ResolvedAddresses } from "@x402r/core";
export interface CliSetup {
    account: PrivateKeyAccount;
    publicClient: PublicClient;
    walletClient: WalletClient;
    networkId: string;
    addresses: ResolvedAddresses;
    operatorAddress: `0x${string}`;
    arbiterUrl: string;
}
/**
 * Initialize CLI: validates config, creates viem clients.
 * Auto-discovers operator and network from arbiter if not set locally.
 */
export declare function initCli(): Promise<CliSetup>;
/**
 * Read-only setup — no private key required.
 * Auto-discovers operator and network from arbiter if not set locally.
 */
export declare function initReadOnly(): Promise<Pick<CliSetup, "publicClient" | "networkId" | "addresses" | "arbiterUrl" | "operatorAddress">>;
