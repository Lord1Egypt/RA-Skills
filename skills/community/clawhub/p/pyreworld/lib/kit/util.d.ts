/**
 * Pyre Kit Actions
 *
 * Thin wrappers that call torchsdk functions and map params/results
 * into game-semantic Pyre types. No new on-chain logic.
 */
import { PublicKey } from '@solana/web3.js';
import { Intel } from './types/intel.types';
/** Add mints to the blacklist (call at startup with old mints) */
export declare function blacklistMints(mints: string[]): void;
/** Check if a mint is blacklisted */
export declare function isBlacklistedMint(mint: string): boolean;
/** Get all blacklisted mints */
export declare function getBlacklistedMints(): string[];
/** Create an ephemeral agent keypair (memory-only, zero key management) */
export { createEphemeralAgent } from 'torchsdk';
/** Get the Raydium pool state PDA for an ascended faction's DEX pool */
export declare function getDexPool(mint: string): PublicKey;
/** Get Raydium pool vault addresses for an ascended faction */
export declare function getDexVaults(mint: string): {
    solVault: string;
    tokenVault: string;
};
export declare const startVaultPnlTracker: (intel: Intel, wallet: string) => Promise<{
    finish: () => Promise<{
        spent: number;
        received: number;
    }>;
}>;
