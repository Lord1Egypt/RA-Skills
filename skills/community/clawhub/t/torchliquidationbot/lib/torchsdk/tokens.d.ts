/**
 * Token data fetching
 *
 * Read-only functions for querying token state from Solana.
 */
import { Connection, PublicKey } from '@solana/web3.js';
import { BondingCurve, Treasury } from './program';
import { TokenDetail, TokenListParams, TokenListResult, HoldersResult, MessagesResult, LendingInfo, LoanPositionInfo, ShortPositionInfo, AllLoanPositionsResult, VaultInfo, VaultWalletLinkInfo, UserStatsInfo, ProtocolTreasuryInfo, TreasuryInfo, TokenMetadataResult } from './types';
declare const fetchTokenRaw: (connection: Connection, mint: PublicKey) => Promise<{
    bondingCurve: BondingCurve;
    treasury: Treasury | null;
} | null>;
/**
 * List tokens with optional filtering and sorting.
 */
export declare const getTokens: (connection: Connection, params?: TokenListParams) => Promise<TokenListResult>;
/**
 * Get on-chain Token-2022 metadata for a token.
 *
 * Reads name, symbol, and uri directly from the mint's TokenMetadata extension.
 * Returns null if the mint has no metadata (legacy pre-V29 tokens).
 */
export declare const getTokenMetadata: (connection: Connection, mintStr: string) => Promise<TokenMetadataResult | null>;
/**
 * Get detailed info for a single token.
 */
export declare const getToken: (connection: Connection, mintStr: string) => Promise<TokenDetail>;
/**
 * Get top holders for a token.
 */
export declare const getHolders: (connection: Connection, mintStr: string, limit?: number) => Promise<HoldersResult>;
/**
 * Get messages (memos) for a token.
 */
export declare const getMessages: (connection: Connection, mintStr: string, limit?: number, opts?: {
    source?: "bonding" | "pool" | "all";
    enrich?: boolean;
}) => Promise<MessagesResult>;
/**
 * Get lending info for a migrated token.
 *
 * Returns interest rates, LTV limits, and active loan statistics.
 * Lending is available on all migrated tokens with treasury SOL.
 */
export declare const getLendingInfo: (connection: Connection, mintStr: string) => Promise<LendingInfo>;
/**
 * Get loan position for a wallet on a specific token.
 *
 * Returns collateral locked, SOL owed, health status, etc.
 * Returns health="none" if no active loan exists.
 */
export declare const getLoanPosition: (connection: Connection, mintStr: string, walletStr: string) => Promise<LoanPositionInfo>;
/**
 * Get a user's short position for a given token.
 *
 * Reads the ShortPosition PDA on-chain and computes health status
 * using the Raydium pool price to value the token debt against SOL collateral.
 */
export declare const getShortPosition: (connection: Connection, mintStr: string, walletStr: string) => Promise<ShortPositionInfo>;
/**
 * Get all active loan positions for a given token mint.
 *
 * Scans on-chain LoanPosition accounts, computes health for each,
 * and returns them sorted: liquidatable first, then at_risk, then healthy.
 */
export declare const getAllLoanPositions: (connection: Connection, mintStr: string) => Promise<AllLoanPositionsResult>;
/**
 * Get vault state by the vault creator's public key.
 *
 * Returns vault balance, authority, linked wallet count, etc.
 * Returns null if no vault exists for this creator.
 */
export declare const getVault: (connection: Connection, creatorStr: string) => Promise<VaultInfo | null>;
/**
 * Get vault state by looking up a linked wallet's VaultWalletLink.
 *
 * Useful when you have an agent wallet and need to find its vault.
 * Returns null if the wallet is not linked to any vault.
 */
export declare const getVaultForWallet: (connection: Connection, walletStr: string) => Promise<VaultInfo | null>;
/**
 * Get wallet link state for a specific wallet.
 *
 * Returns the link info (which vault it's linked to, when) or null if not linked.
 */
export declare const getVaultWalletLink: (connection: Connection, walletStr: string) => Promise<VaultWalletLinkInfo | null>;
export declare const getUserStats: (connection: Connection, walletStr: string) => Promise<UserStatsInfo | null>;
export declare const getProtocolTreasuryState: (connection: Connection) => Promise<ProtocolTreasuryInfo | null>;
export declare const getTreasuryState: (connection: Connection, mintStr: string) => Promise<TreasuryInfo | null>;
export { fetchTokenRaw };
//# sourceMappingURL=tokens.d.ts.map