/**
 * Transaction builders
 *
 * Build unsigned transactions for buy, sell, create, star, vault, and lending.
 * Agents sign these locally and submit to the network.
 */
import { Connection, PublicKey } from '@solana/web3.js';
import { BuyParams, DirectBuyParams, SellParams, CreateTokenParams, StarParams, MigrateParams, BorrowParams, RepayParams, LiquidateParams, OpenShortParams, CloseShortParams, LiquidateShortParams, EnableShortSellingParams, ClaimProtocolRewardsParams, HarvestFeesParams, SwapFeesToSolParams, AdvanceProtocolEpochParams, CreateVaultParams, DepositVaultParams, WithdrawVaultParams, WithdrawTokensParams, LinkWalletParams, UnlinkWalletParams, TransferAuthorityParams, ReclaimParams, TransactionResult, BuyTransactionResult, CreateTokenResult, WalletAdapter } from './types';
/**
 * Build an unsigned vault-funded buy transaction.
 *
 * The vault pays for the buy. This is the recommended path for AI agents.
 *
 * @param connection - Solana RPC connection
 * @param params - Buy parameters with required vault creator pubkey
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildBuyTransaction: (connection: Connection, params: BuyParams) => Promise<BuyTransactionResult>;
/**
 * Build an unsigned direct buy transaction (no vault).
 *
 * The buyer pays from their own wallet. Use this for human-operated wallets only.
 * For AI agents, use buildBuyTransaction with a vault instead.
 *
 * @param connection - Solana RPC connection
 * @param params - Buy parameters (no vault)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildDirectBuyTransaction: (connection: Connection, params: DirectBuyParams) => Promise<BuyTransactionResult>;
/**
 * Build, simulate, and submit a vault-funded buy via signAndSendTransaction.
 *
 * This is the recommended path for Phantom and other browser wallets.
 * The wallet receives the final, immutable transaction for atomic sign+send,
 * which avoids false-positive "malicious dapp" warnings.
 *
 * @returns Transaction signature on success
 */
export declare const sendBuy: (connection: Connection, wallet: WalletAdapter, params: Omit<BuyParams, "buyer">) => Promise<string>;
/**
 * Build, simulate, and submit a direct buy (no vault) via signAndSendTransaction.
 *
 * Same Phantom-friendly flow as sendBuy but buyer pays from their own wallet.
 *
 * @returns Transaction signature on success
 */
export declare const sendDirectBuy: (connection: Connection, wallet: WalletAdapter, params: Omit<DirectBuyParams, "buyer">) => Promise<string>;
/**
 * Build an unsigned sell transaction.
 *
 * @param connection - Solana RPC connection
 * @param params - Sell parameters (mint, seller, amount_tokens in raw units, optional slippage_bps)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildSellTransaction: (connection: Connection, params: SellParams) => Promise<TransactionResult>;
/**
 * Build an unsigned create token transaction.
 *
 * Returns the transaction (partially signed by the mint keypair) and the mint keypair
 * so the agent can extract the mint address.
 *
 * @param connection - Solana RPC connection
 * @param params - Create parameters (creator, name, symbol, metadata_uri)
 * @returns Partially-signed transaction, mint PublicKey, and mint Keypair
 */
export declare const buildCreateTokenTransaction: (connection: Connection, params: CreateTokenParams) => Promise<CreateTokenResult>;
/**
 * Build, simulate, and submit a create token via signAndSendTransaction.
 *
 * Phantom-friendly: simulates with sigVerify: false (mint keypair is already
 * partially signed), then hands the tx to the wallet for the creator signature.
 * Avoids the "malicious dapp" warning caused by Phantom trying to simulate a
 * partially-signed transaction.
 *
 * @returns { signature, mint } on success
 */
export declare const sendCreateToken: (connection: Connection, wallet: WalletAdapter, params: Omit<CreateTokenParams, "creator">) => Promise<{
    signature: string;
    mint: PublicKey;
}>;
/**
 * Build an unsigned star transaction (costs 0.05 SOL).
 *
 * @param connection - Solana RPC connection
 * @param params - Star parameters (mint, user)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildStarTransaction: (connection: Connection, params: StarParams) => Promise<TransactionResult>;
/**
 * Build an unsigned create vault transaction.
 *
 * Creates a TorchVault PDA and auto-links the creator's wallet.
 *
 * @param connection - Solana RPC connection
 * @param params - Creator public key
 * @returns Unsigned transaction
 */
export declare const buildCreateVaultTransaction: (connection: Connection, params: CreateVaultParams) => Promise<TransactionResult>;
/**
 * Build an unsigned deposit vault transaction.
 *
 * Anyone can deposit SOL into any vault.
 *
 * @param connection - Solana RPC connection
 * @param params - Depositor, vault creator, amount in lamports
 * @returns Unsigned transaction
 */
export declare const buildDepositVaultTransaction: (connection: Connection, params: DepositVaultParams) => Promise<TransactionResult>;
/**
 * Build an unsigned withdraw vault transaction.
 *
 * Only the vault authority can withdraw.
 *
 * @param connection - Solana RPC connection
 * @param params - Authority, vault creator, amount in lamports
 * @returns Unsigned transaction
 */
export declare const buildWithdrawVaultTransaction: (connection: Connection, params: WithdrawVaultParams) => Promise<TransactionResult>;
/**
 * Build an unsigned link wallet transaction.
 *
 * Only the vault authority can link wallets.
 *
 * @param connection - Solana RPC connection
 * @param params - Authority, vault creator, wallet to link
 * @returns Unsigned transaction
 */
export declare const buildLinkWalletTransaction: (connection: Connection, params: LinkWalletParams) => Promise<TransactionResult>;
/**
 * Build an unsigned unlink wallet transaction.
 *
 * Only the vault authority can unlink wallets. Rent returns to authority.
 *
 * @param connection - Solana RPC connection
 * @param params - Authority, vault creator, wallet to unlink
 * @returns Unsigned transaction
 */
export declare const buildUnlinkWalletTransaction: (connection: Connection, params: UnlinkWalletParams) => Promise<TransactionResult>;
/**
 * Build an unsigned transfer authority transaction.
 *
 * Transfers vault admin control to a new wallet.
 *
 * @param connection - Solana RPC connection
 * @param params - Current authority, vault creator, new authority
 * @returns Unsigned transaction
 */
export declare const buildTransferAuthorityTransaction: (connection: Connection, params: TransferAuthorityParams) => Promise<TransactionResult>;
/**
 * Build an unsigned borrow transaction.
 *
 * Lock tokens as collateral in the collateral vault and receive SOL from treasury.
 * Token must be migrated (has Raydium pool for price calculation).
 *
 * @param connection - Solana RPC connection
 * @param params - Borrow parameters (mint, borrower, collateral_amount, sol_to_borrow)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildBorrowTransaction: (connection: Connection, params: BorrowParams) => Promise<TransactionResult>;
/**
 * Build an unsigned repay transaction.
 *
 * Repay SOL debt. Interest is paid first, then principal.
 * Full repay returns all collateral and closes the position.
 *
 * @param connection - Solana RPC connection
 * @param params - Repay parameters (mint, borrower, sol_amount)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildRepayTransaction: (connection: Connection, params: RepayParams) => Promise<TransactionResult>;
/**
 * Build an unsigned liquidate transaction.
 *
 * Permissionless — anyone can call when a borrower's LTV exceeds the
 * liquidation threshold. Liquidator pays SOL and receives collateral + bonus.
 *
 * @param connection - Solana RPC connection
 * @param params - Liquidate parameters (mint, liquidator, borrower)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildLiquidateTransaction: (connection: Connection, params: LiquidateParams) => Promise<TransactionResult>;
/**
 * Build an unsigned claim protocol rewards transaction.
 *
 * Claims the user's proportional share of protocol treasury rewards
 * based on trading volume in the previous epoch. Requires >= 2 SOL volume. Min claim: 0.1 SOL.
 *
 * @param connection - Solana RPC connection
 * @param params - Claim parameters (user, optional vault)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildClaimProtocolRewardsTransaction: (connection: Connection, params: ClaimProtocolRewardsParams) => Promise<TransactionResult>;
/**
 * Build an unsigned reclaim-failed-token transaction.
 *
 * Permissionless — anyone can reclaim a failed token that has been
 * inactive for 7+ days and hasn't completed bonding.
 * SOL from both bonding curve and token treasury goes to protocol treasury.
 */
export declare const buildReclaimFailedTokenTransaction: (connection: Connection, params: ReclaimParams) => Promise<TransactionResult>;
/**
 * Build an unsigned withdraw tokens transaction.
 *
 * Withdraw tokens from a vault ATA to any destination token account.
 * Authority only. Composability escape hatch for external DeFi.
 *
 * @param connection - Solana RPC connection
 * @param params - Authority, vault creator, mint, destination, amount in raw units
 * @returns Unsigned transaction
 */
export declare const buildWithdrawTokensTransaction: (connection: Connection, params: WithdrawTokensParams) => Promise<TransactionResult>;
export declare const buildMigrateTransaction: (connection: Connection, params: MigrateParams) => Promise<TransactionResult>;
export declare const buildAdvanceProtocolEpochTransaction: (connection: Connection, params: AdvanceProtocolEpochParams) => Promise<TransactionResult>;
/**
 * Build an unsigned harvest-fees transaction.
 *
 * Permissionless crank — harvests accumulated Token-2022 transfer fees
 * from token accounts into the mint, then withdraws from the mint into
 * the treasury's token account.
 *
 * If `params.sources` is provided, uses those accounts directly.
 * Otherwise auto-discovers token accounts with withheld fees.
 */
export declare const buildHarvestFeesTransaction: (connection: Connection, params: HarvestFeesParams) => Promise<TransactionResult>;
/**
 * [V20] Harvest transfer fees AND swap them to SOL.
 *
 * Tries to bundle: create_idempotent(treasury_wsol) + harvest_fees + swap_fees_to_sol.
 * If the combined transaction exceeds the 1232-byte limit (many source accounts),
 * automatically splits into a harvest-only tx + swap-only tx via additionalTransactions.
 * Set harvest=false to skip harvest (if already harvested separately).
 */
export declare const buildSwapFeesToSolTransaction: (connection: Connection, params: SwapFeesToSolParams) => Promise<TransactionResult>;
/**
 * Build an unsigned open_short transaction.
 *
 * Post SOL collateral and borrow tokens from treasury.
 * Mirror of borrow: same LTV, same liquidation, opposite direction.
 *
 * @param connection - Solana RPC connection
 * @param params - Open short parameters (mint, shorter, sol_collateral, tokens_to_borrow)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildOpenShortTransaction: (connection: Connection, params: OpenShortParams) => Promise<TransactionResult>;
/**
 * Build an unsigned close_short transaction.
 *
 * Return tokens to close or partially repay a short position.
 * Interest paid first (in tokens), then principal.
 * Full close returns all SOL collateral.
 *
 * @param connection - Solana RPC connection
 * @param params - Close short parameters (mint, shorter, token_amount)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildCloseShortTransaction: (connection: Connection, params: CloseShortParams) => Promise<TransactionResult>;
/**
 * Build an unsigned liquidate_short transaction.
 *
 * Permissionless — anyone can call when a short position's LTV exceeds the
 * liquidation threshold (65%). Liquidator sends tokens and receives SOL + bonus.
 *
 * @param connection - Solana RPC connection
 * @param params - Liquidate short parameters (mint, liquidator, borrower)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildLiquidateShortTransaction: (connection: Connection, params: LiquidateShortParams) => Promise<TransactionResult>;
/**
 * Build an unsigned enable_short_selling transaction.
 *
 * Admin-only. For pre-V5 tokens that weren't created with the short selling
 * sentinel. New tokens (V5+) have shorts auto-enabled at creation.
 *
 * @param connection - Solana RPC connection
 * @param params - Enable short selling parameters (authority, mint)
 * @returns Unsigned transaction and descriptive message
 */
export declare const buildEnableShortSellingTransaction: (connection: Connection, params: EnableShortSellingParams) => Promise<TransactionResult>;
//# sourceMappingURL=transactions.d.ts.map