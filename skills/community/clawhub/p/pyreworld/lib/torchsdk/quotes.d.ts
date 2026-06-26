/**
 * Quote calculations
 *
 * Get expected output for buy/sell operations.
 * Works for both bonding curve tokens and migrated (Raydium DEX) tokens.
 */
import { Connection } from '@solana/web3.js';
import { BuyQuoteResult, SellQuoteResult, BorrowQuoteResult } from './types';
/**
 * Get a buy quote: how many tokens for a given SOL amount.
 *
 * Works for both bonding curve and migrated (Raydium DEX) tokens.
 */
export declare const getBuyQuote: (connection: Connection, mintStr: string, amountSolLamports: number) => Promise<BuyQuoteResult>;
/**
 * Get a sell quote: how much SOL for a given token amount.
 *
 * Works for both bonding curve and migrated (Raydium DEX) tokens.
 */
export declare const getSellQuote: (connection: Connection, mintStr: string, amountTokens: number) => Promise<SellQuoteResult>;
/**
 * Get a borrow quote: maximum borrowable SOL for a given collateral amount on a migrated token.
 *
 * @param collateralAmount - Collateral in token base units (with 6 decimals)
 */
export declare const getBorrowQuote: (connection: Connection, mintStr: string, collateralAmount: number) => Promise<BorrowQuoteResult>;
//# sourceMappingURL=quotes.d.ts.map