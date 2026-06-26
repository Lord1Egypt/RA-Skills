/**
 * Coin utilities for SUIROLL
 */
import { TokenType } from '../config.js';
export type { TokenType } from '../config.js';
/**
 * Get the coin type string for a given token
 * @param token - Token type (SUI or USDC)
 * @returns Coin type string for Sui Move call
 */
export declare function getCoinType(token: TokenType): string;
/**
 * Get the function name for creating a lottery with a specific token
 * @param token - Token type (SUI or USDC)
 * @returns Function name for creating lottery
 */
export declare function getCreateFunctionName(token: TokenType): string;
/**
 * Get minimum prize amount for a token type
 * @param token - Token type (SUI or USDC)
 * @returns Minimum prize amount in smallest units (mist for SUI, micro for USDC)
 */
export declare function getMinPrize(token: TokenType): number;
/**
 * Parse prize amount to appropriate units
 * @param amount - Amount in whole units (e.g., 100 USDC)
 * @param token - Token type
 * @returns Amount in smallest units
 */
export declare function parsePrizeAmount(amount: number, token: TokenType): number;
/**
 * Format prize amount from smallest units to human readable
 * @param amount - Amount in smallest units
 * @param token - Token type
 * @returns Formatted amount with token symbol
 */
export declare function formatPrizeAmount(amount: number, token: TokenType): string;
//# sourceMappingURL=coin.d.ts.map