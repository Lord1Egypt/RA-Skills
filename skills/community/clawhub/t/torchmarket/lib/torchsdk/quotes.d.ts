/**
 * Quote calculations
 *
 * Get expected output for buy/sell operations.
 * Works for both bonding curve tokens and migrated (Raydium DEX) tokens.
 */
import { Connection } from '@solana/web3.js';
import { BuyQuoteResult, SellQuoteResult, BorrowQuoteResult } from './types';
export declare const getBuyQuote: (connection: Connection, mintStr: string, amountSolLamports: number) => Promise<BuyQuoteResult>;
export declare const getSellQuote: (connection: Connection, mintStr: string, amountTokens: number) => Promise<SellQuoteResult>;
export declare const getBorrowQuote: (connection: Connection, mintStr: string, collateralAmount: number) => Promise<BorrowQuoteResult>;
//# sourceMappingURL=quotes.d.ts.map