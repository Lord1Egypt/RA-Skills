/**
 * Torch Market SDK Types
 */
import { PublicKey, VersionedTransaction, Keypair } from '@solana/web3.js';
export type TokenStatus = 'bonding' | 'complete' | 'migrated' | 'reclaimed';
export interface TokenSummary {
    mint: string;
    name: string;
    symbol: string;
    status: TokenStatus;
    price_sol: number;
    market_cap_sol: number;
    progress_percent: number;
    holders: number | null;
    created_at: number;
    last_activity_at: number;
}
export interface TokenDetail {
    mint: string;
    name: string;
    symbol: string;
    description?: string;
    image?: string;
    status: TokenStatus;
    price_sol: number;
    price_usd?: number;
    market_cap_sol: number;
    market_cap_usd?: number;
    progress_percent: number;
    sol_raised: number;
    sol_target: number;
    total_supply: number;
    circulating_supply: number;
    tokens_in_curve: number;
    tokens_burned: number;
    treasury_sol_balance: number;
    treasury_token_balance: number;
    total_bought_back: number;
    buyback_count: number;
    creator: string;
    holders: number | null;
    stars: number;
    created_at: number;
    last_activity_at: number;
    twitter?: string;
    telegram?: string;
    website?: string;
    creator_verified?: boolean;
    creator_trust_tier?: 'high' | 'medium' | 'low' | null;
    creator_said_name?: string;
    creator_badge_url?: string;
    warnings?: string[];
}
export type TokenSortOption = 'newest' | 'volume' | 'marketcap';
export type TokenStatusFilter = 'bonding' | 'complete' | 'migrated' | 'reclaimed' | 'all';
export interface TokenListParams {
    limit?: number;
    offset?: number;
    status?: TokenStatusFilter;
    sort?: TokenSortOption;
}
export interface TokenListResult {
    tokens: TokenSummary[];
    total: number;
    limit: number;
    offset: number;
}
export interface Holder {
    address: string;
    balance: number;
    percentage: number;
}
export interface HoldersResult {
    holders: Holder[];
    total_holders: number;
}
export interface BuyQuoteResult {
    input_sol: number;
    output_tokens: number;
    tokens_to_user: number;
    protocol_fee_sol: number;
    price_per_token_sol: number;
    price_impact_percent: number;
    min_output_tokens: number;
    /** Where this quote came from: bonding curve or Raydium DEX pool */
    source: 'bonding' | 'dex';
}
export interface SellQuoteResult {
    input_tokens: number;
    output_sol: number;
    protocol_fee_sol: number;
    price_per_token_sol: number;
    price_impact_percent: number;
    min_output_sol: number;
    /** Where this quote came from: bonding curve or Raydium DEX pool */
    source: 'bonding' | 'dex';
}
export interface BorrowQuoteResult {
    max_borrow_sol: number;
    collateral_value_sol: number;
    ltv_max_sol: number;
    pool_available_sol: number;
    per_user_cap_sol: number;
    interest_rate_bps: number;
    liquidation_threshold_bps: number;
}
export interface VaultInfo {
    address: string;
    creator: string;
    authority: string;
    sol_balance: number;
    total_deposited: number;
    total_withdrawn: number;
    total_spent: number;
    total_received: number;
    linked_wallets: number;
    created_at: number;
}
export interface VaultWalletLinkInfo {
    address: string;
    vault: string;
    wallet: string;
    linked_at: number;
}
export interface CreateVaultParams {
    creator: string;
}
export interface DepositVaultParams {
    depositor: string;
    vault_creator: string;
    amount_sol: number;
}
export interface WithdrawVaultParams {
    authority: string;
    vault_creator: string;
    amount_sol: number;
}
export interface LinkWalletParams {
    authority: string;
    vault_creator: string;
    wallet_to_link: string;
}
export interface UnlinkWalletParams {
    authority: string;
    vault_creator: string;
    wallet_to_unlink: string;
}
export interface TransferAuthorityParams {
    authority: string;
    vault_creator: string;
    new_authority: string;
}
export interface WithdrawTokensParams {
    authority: string;
    vault_creator: string;
    mint: string;
    destination: string;
    amount: number;
}
export interface BuyParams {
    mint: string;
    buyer: string;
    amount_sol: number;
    slippage_bps?: number;
    message?: string;
    /** Vault creator pubkey. Vault pays for the buy. */
    vault: string;
    /** Pre-fetched quote from getBuyQuote. If provided, skips internal quote fetch
     *  and uses quote.source to route bonding vs DEX. */
    quote?: BuyQuoteResult;
}
export interface DirectBuyParams {
    mint: string;
    buyer: string;
    amount_sol: number;
    slippage_bps?: number;
    message?: string;
    /** Pre-fetched quote from getBuyQuote. If provided, skips internal quote fetch. */
    quote?: BuyQuoteResult;
}
export interface SellParams {
    mint: string;
    seller: string;
    amount_tokens: number;
    slippage_bps?: number;
    message?: string;
    /** Vault creator pubkey. SOL goes to vault, tokens sold from vault ATA. */
    vault?: string;
    /** Pre-fetched quote from getSellQuote. If provided, skips internal quote fetch
     *  and uses quote.source to route bonding vs DEX. */
    quote?: SellQuoteResult;
}
export interface CreateTokenParams {
    creator: string;
    name: string;
    symbol: string;
    metadata_uri: string;
    /** [V23] Bonding target in lamports. 0 or omitted = default 200 SOL. */
    sol_target?: number;
    /** [V35] Community token: 0% creator fees, all to treasury. Default true. */
    community_token?: boolean;
}
export interface StarParams {
    mint: string;
    user: string;
    /** Vault creator pubkey. Vault pays the 0.02 SOL star cost. */
    vault?: string;
}
export interface MigrateParams {
    /** Token mint address */
    mint: string;
    /** Wallet signing the transaction. Fronts ~1 SOL for Raydium costs
     *  (pool creation fee + account rent), reimbursed by treasury in the same transaction. */
    payer: string;
}
export interface VaultSwapParams {
    /** Token mint address */
    mint: string;
    /** Controller wallet (linked to vault, signs the tx) */
    signer: string;
    /** Vault creator pubkey (for PDA derivation) */
    vault_creator: string;
    /** Input amount (lamports for buy, token base units for sell) */
    amount_in: number;
    /** Minimum output for slippage protection */
    minimum_amount_out: number;
    /** true = SOL→Token (buy), false = Token→SOL (sell) */
    is_buy: boolean;
    /** Optional message bundled as SPL Memo instruction (max 500 chars) */
    message?: string;
}
export interface HarvestFeesParams {
    /** Token mint address */
    mint: string;
    /** Payer wallet (permissionless — anyone can trigger) */
    payer: string;
    /** Optional list of token account addresses to harvest from.
     *  If omitted, the SDK auto-discovers accounts with withheld fees. */
    sources?: string[];
}
export interface SwapFeesToSolParams {
    /** Token mint address */
    mint: string;
    /** Payer wallet (permissionless — anyone can trigger) */
    payer: string;
    /** Minimum SOL out from the swap (slippage protection, default 1) */
    minimum_amount_out?: number;
    /** Bundle harvest_fees in the same transaction (default true) */
    harvest?: boolean;
    /** Optional list of token account addresses to harvest from.
     *  Only used when harvest=true. If omitted, auto-discovers. */
    sources?: string[];
}
export interface TokenMetadataResult {
    /** Token name from on-chain metadata */
    name: string;
    /** Token symbol from on-chain metadata */
    symbol: string;
    /** Token metadata URI */
    uri: string;
    /** Mint address */
    mint: string;
}
/**
 * Minimal wallet interface for signAndSendTransaction flows.
 * Compatible with Phantom, Backpack, and other Solana wallets that
 * support atomic sign-and-send.
 */
export interface WalletAdapter {
    publicKey: PublicKey;
    signAndSendTransaction: (tx: VersionedTransaction) => Promise<{
        signature: string;
    }>;
}
export interface TransactionResult {
    transaction: VersionedTransaction;
    /** Additional transactions when a single tx exceeds the size limit.
     *  When present, send all transactions in order: transaction first, then these. */
    additionalTransactions?: VersionedTransaction[];
    message: string;
}
export interface BuyTransactionResult extends TransactionResult {
    /** [V28] Follow-up migration transaction. Present when this buy completes
     *  bonding. Send immediately after the buy tx succeeds. The payer fronts
     *  ~1 SOL for Raydium costs, reimbursed by treasury in the same tx.
     *  If the caller can't afford it or it fails, anyone can trigger migration
     *  later via buildMigrateTransaction. */
    migrationTransaction?: VersionedTransaction;
}
export interface CreateTokenResult extends TransactionResult {
    mint: PublicKey;
    mintKeypair: Keypair;
}
export interface BorrowParams {
    mint: string;
    borrower: string;
    collateral_amount: number;
    sol_to_borrow: number;
    /** Vault creator pubkey. Collateral from vault ATA, SOL to vault. */
    vault?: string;
}
export interface RepayParams {
    mint: string;
    borrower: string;
    sol_amount: number;
    /** Vault creator pubkey. SOL repaid from vault, collateral returns to vault ATA. */
    vault?: string;
}
export interface LiquidateParams {
    mint: string;
    liquidator: string;
    borrower: string;
    /** Vault creator pubkey. SOL paid from vault, collateral received to vault ATA. */
    vault?: string;
}
export interface ClaimProtocolRewardsParams {
    user: string;
    /** Vault creator pubkey. Claimed SOL goes to vault instead of user. */
    vault?: string;
}
export interface ReclaimParams {
    /** Payer/caller wallet (permissionless — anyone can call) */
    payer: string;
    /** Token mint to reclaim */
    mint: string;
}
export interface OpenShortParams {
    mint: string;
    shorter: string;
    sol_collateral: number;
    tokens_to_borrow: number;
    /** Vault creator pubkey. SOL from vault, tokens to vault ATA. */
    vault?: string;
}
export interface CloseShortParams {
    mint: string;
    shorter: string;
    token_amount: number;
    /** Vault creator pubkey. Tokens from vault ATA, SOL to vault. */
    vault?: string;
}
export interface LiquidateShortParams {
    mint: string;
    liquidator: string;
    borrower: string;
    /** Vault creator pubkey. Tokens from vault ATA, SOL to vault. */
    vault?: string;
}
export interface EnableShortSellingParams {
    /** Protocol authority wallet */
    authority: string;
    /** Token mint to enable shorts for */
    mint: string;
}
export interface LendingInfo {
    interest_rate_bps: number;
    max_ltv_bps: number;
    liquidation_threshold_bps: number;
    liquidation_bonus_bps: number;
    utilization_cap_bps: number;
    borrow_share_multiplier: number;
    total_sol_lent: number | null;
    active_loans: number | null;
    treasury_sol_available: number;
    warnings?: string[];
}
export interface LoanPositionInfo {
    collateral_amount: number;
    borrowed_amount: number;
    accrued_interest: number;
    total_owed: number;
    collateral_value_sol: number | null;
    current_ltv_bps: number | null;
    health: 'healthy' | 'at_risk' | 'liquidatable' | 'none';
    warnings?: string[];
}
export interface LoanPositionWithKey extends LoanPositionInfo {
    borrower: string;
}
export interface AllLoanPositionsResult {
    positions: LoanPositionWithKey[];
    pool_price_sol: number | null;
}
export interface ShortPositionInfo {
    sol_collateral: number;
    tokens_borrowed: number;
    accrued_interest: number;
    total_owed_tokens: number;
    /** SOL value of the token debt (null if pool price unavailable) */
    debt_value_sol: number | null;
    /** Current LTV in basis points: debt_value_sol / sol_collateral (null if price unavailable) */
    current_ltv_bps: number | null;
    health: 'healthy' | 'at_risk' | 'liquidatable' | 'none';
    warnings?: string[];
}
export interface TokenMessage {
    signature: string;
    memo: string;
    sender: string;
    timestamp: number;
    sender_verified?: boolean;
    sender_trust_tier?: 'high' | 'medium' | 'low' | null;
    sender_said_name?: string;
    sender_badge_url?: string;
}
export interface MessagesResult {
    messages: TokenMessage[];
    total: number;
}
export interface SaidVerification {
    verified: boolean;
    trustTier: 'high' | 'medium' | 'low' | null;
    name?: string;
}
export interface ConfirmResult {
    confirmed: boolean;
    event_type: 'token_launch' | 'trade_complete' | 'governance_vote' | 'unknown';
}
//# sourceMappingURL=types.d.ts.map