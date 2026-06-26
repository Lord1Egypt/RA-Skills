/**
 * SUIROLL Sui Client Wrapper
 * Helper functions for Sui blockchain interaction
 */
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { SuiClient } from '@mysten/sui/client';
export type Network = 'mainnet' | 'testnet';
/**
 * Get Sui client for a specific network
 */
export declare function getClient(network?: Network): SuiClient;
/**
 * Get keypair from environment or generate new one
 */
export declare function getKeypair(): Ed25519Keypair;
/**
 * Validate Sui address format
 */
export declare function isValidSuiAddress(address: string): boolean;
/**
 * Validate Object ID format
 */
export declare function isValidObjectId(id: string): boolean;
/**
 * Format MIST to SUI (1 SUI = 10^9 MIST)
 */
export declare function mistToSui(mist: number | string): string;
/**
 * Format SUI to MIST
 */
export declare function suiToMist(sui: number): string;
/**
 * Parse USDC amount (assuming 6 decimals)
 */
export declare function parseUSDC(amount: string): bigint;
/**
 * Format USDC amount
 */
export declare function formatUSDC(amount: bigint): string;
/**
 * Get configuration for a specific network
 */
export declare function getNetworkConfig(network: Network): import("./config.js").SuirollConfig;
//# sourceMappingURL=utils.d.ts.map