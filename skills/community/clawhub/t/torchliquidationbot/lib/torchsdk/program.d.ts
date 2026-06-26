import { Program, AnchorProvider, BN } from '@coral-xyz/anchor';
import { PublicKey } from '@solana/web3.js';
import { PROGRAM_ID } from './constants';
export { PROGRAM_ID };
export interface BondingCurve {
    mint: PublicKey;
    creator: PublicKey;
    virtual_sol_reserves: BN;
    virtual_token_reserves: BN;
    real_sol_reserves: BN;
    real_token_reserves: BN;
    vote_vault_balance: BN;
    permanently_burned_tokens: BN;
    bonding_complete: boolean;
    bonding_complete_slot: BN;
    votes_return: BN;
    votes_burn: BN;
    total_voters: BN;
    vote_finalized: boolean;
    vote_result_return: boolean;
    migrated: boolean;
    is_token_2022: boolean;
    last_activity_slot: BN;
    reclaimed: boolean;
    name: number[];
    symbol: number[];
    uri: number[];
    bump: number;
    treasury_bump: number;
    bonding_target: BN;
    migration_announced_slot: BN;
    pending_token_destination: PublicKey;
    pending_sol_destination: PublicKey;
}
export interface GlobalConfig {
    authority: PublicKey;
    treasury: PublicKey;
    dev_wallet: PublicKey;
    _deprecated_platform_treasury: PublicKey;
    protocol_fee_bps: number;
    paused: boolean;
    total_tokens_launched: BN;
    total_volume_sol: BN;
    bump: number;
}
export interface Treasury {
    bonding_curve: PublicKey;
    mint: PublicKey;
    sol_balance: BN;
    total_bought_back: BN;
    total_burned_from_buyback: BN;
    tokens_held: BN;
    last_buyback_slot: BN;
    buyback_count: BN;
    harvested_fees: BN;
    baseline_sol_reserves: BN;
    baseline_token_reserves: BN;
    ratio_threshold_bps: number;
    reserve_ratio_bps: number;
    buyback_percent_bps: number;
    min_buyback_interval_slots: BN;
    baseline_initialized: boolean;
    total_stars: BN;
    star_sol_balance: BN;
    creator_paid_out: boolean;
    bump: number;
}
export interface TorchVault {
    creator: PublicKey;
    authority: PublicKey;
    sol_balance: BN;
    total_deposited: BN;
    total_withdrawn: BN;
    total_spent: BN;
    total_received: BN;
    linked_wallets: number;
    created_at: BN;
    bump: number;
}
export interface VaultWalletLink {
    vault: PublicKey;
    wallet: PublicKey;
    linked_at: BN;
    bump: number;
}
export interface LoanPosition {
    user: PublicKey;
    mint: PublicKey;
    collateral_amount: BN;
    borrowed_amount: BN;
    accrued_interest: BN;
    last_update_slot: BN;
    bump: number;
}
export interface ShortPosition {
    user: PublicKey;
    mint: PublicKey;
    sol_collateral: BN;
    tokens_borrowed: BN;
    accrued_interest: BN;
    last_update_slot: BN;
    bump: number;
}
export interface ShortConfig {
    mint: PublicKey;
    total_tokens_lent: BN;
    active_positions: BN;
    total_interest_collected: BN;
    bump: number;
}
export interface UserStats {
    user: PublicKey;
    total_volume: BN;
    volume_current_epoch: BN;
    volume_previous_epoch: BN;
    last_epoch_claimed: BN;
    total_rewards_claimed: BN;
    last_volume_epoch: BN;
    bump: number;
}
export interface ProtocolTreasury {
    authority: PublicKey;
    current_balance: BN;
    reserve_floor: BN;
    total_fees_received: BN;
    total_distributed: BN;
    current_epoch: BN;
    last_epoch_ts: BN;
    total_volume_current_epoch: BN;
    total_volume_previous_epoch: BN;
    distributable_amount: BN;
    bump: number;
}
export declare const decodeString: (bytes: number[]) => string;
export declare const getGlobalConfigPda: () => [PublicKey, number];
export declare const getBondingCurvePda: (mint: PublicKey) => [PublicKey, number];
export declare const getTreasuryTokenAccount: (mint: PublicKey, treasury: PublicKey) => PublicKey;
export declare const getUserPositionPda: (bondingCurve: PublicKey, user: PublicKey) => [PublicKey, number];
export declare const getTokenTreasuryPda: (mint: PublicKey) => [PublicKey, number];
export declare const getProtocolTreasuryPda: () => [PublicKey, number];
export declare const getUserStatsPda: (user: PublicKey) => [PublicKey, number];
export declare const getStarRecordPda: (user: PublicKey, mint: PublicKey) => [PublicKey, number];
export declare const getLoanPositionPda: (mint: PublicKey, borrower: PublicKey) => [PublicKey, number];
export declare const getCollateralVaultPda: (mint: PublicKey) => [PublicKey, number];
export declare const getTorchVaultPda: (creator: PublicKey) => [PublicKey, number];
export declare const getVaultWalletLinkPda: (wallet: PublicKey) => [PublicKey, number];
export declare const getTreasuryLockPda: (mint: PublicKey) => [PublicKey, number];
export declare const getShortPositionPda: (mint: PublicKey, shorter: PublicKey) => [PublicKey, number];
export declare const getShortConfigPda: (mint: PublicKey) => [PublicKey, number];
export declare const getTreasuryLockTokenAccount: (mint: PublicKey, treasuryLock: PublicKey) => PublicKey;
export declare const getProgram: (provider: AnchorProvider) => Program;
export declare const calculateTokensOut: (solAmount: bigint, virtualSolReserves: bigint, virtualTokenReserves: bigint, realSolReserves?: bigint, // V2.3: needed for dynamic rate calculation
protocolFeeBps?: number, // [V4.0] 0.5% protocol fee (90% protocol treasury, 10% dev)
treasuryFeeBps?: number, // [V10] 0% token treasury fee (removed — treasury funded by dynamic SOL rate + transfer fees)
bondingTarget?: bigint) => {
    tokensOut: bigint;
    tokensToUser: bigint;
    protocolFee: bigint;
    treasuryFee: bigint;
    solToCurve: bigint;
    solToTreasury: bigint;
    solToCreator: bigint;
    treasuryRateBps: number;
    creatorRateBps: number;
};
export declare const calculateSolOut: (tokenAmount: bigint, virtualSolReserves: bigint, virtualTokenReserves: bigint) => {
    solOut: bigint;
    solToUser: bigint;
};
export declare const calculatePrice: (virtualSolReserves: bigint, virtualTokenReserves: bigint) => number;
export declare const calculateBondingProgress: (realSolReserves: bigint) => number;
export declare const orderTokensForRaydium: (tokenA: PublicKey, tokenB: PublicKey) => {
    token0: PublicKey;
    token1: PublicKey;
    isToken0First: boolean;
};
export declare const getRaydiumAuthorityPda: () => [PublicKey, number];
export declare const getRaydiumPoolStatePda: (ammConfig: PublicKey, token0Mint: PublicKey, token1Mint: PublicKey) => [PublicKey, number];
export declare const getRaydiumLpMintPda: (poolState: PublicKey) => [PublicKey, number];
export declare const getRaydiumVaultPda: (poolState: PublicKey, tokenMint: PublicKey) => [PublicKey, number];
export declare const getRaydiumObservationPda: (poolState: PublicKey) => [PublicKey, number];
export declare const getRaydiumMigrationAccounts: (tokenMint: PublicKey) => {
    token0: PublicKey;
    token1: PublicKey;
    isWsolToken0: boolean;
    raydiumAuthority: PublicKey;
    poolState: PublicKey;
    lpMint: PublicKey;
    token0Vault: PublicKey;
    token1Vault: PublicKey;
    observationState: PublicKey;
};
//# sourceMappingURL=program.d.ts.map