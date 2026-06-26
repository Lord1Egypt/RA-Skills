/**
 * SUIROLL Signer Utilities
 * Helper functions for transaction signing using @mysten/sui v1 SDK
 */
import { SuiClient } from '@mysten/sui/client';
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { Transaction } from '@mysten/sui/transactions';
export type Network = 'mainnet' | 'testnet';
/**
 * Get Sui client for a specific network
 */
export declare function getClient(network?: Network): SuiClient;
/**
 * Get keypair from environment variable.
 * Supports:
 * - Sui bech32 private key (starts with `suiprivkey...`) [recommended]
 * - Hex string (optionally prefixed with 0x) representing 32-byte ed25519 secret key
 */
export declare function getKeypair(): Ed25519Keypair;
/**
 * Build, sign, and execute a transaction.
 */
export declare function executeTransaction(tx: Transaction, network?: Network): Promise<import("@mysten/sui/client").SuiTransactionBlockResponse>;
//# sourceMappingURL=signer.d.ts.map