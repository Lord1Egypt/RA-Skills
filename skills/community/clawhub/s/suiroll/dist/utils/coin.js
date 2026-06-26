/**
 * Coin utilities for SUIROLL
 */
import { config } from '../config.js';
/**
 * Get the coin type string for a given token
 * @param token - Token type (SUI or USDC)
 * @returns Coin type string for Sui Move call
 */
export function getCoinType(token) {
    if (token === 'USDC') {
        return config.testnet.usdcAddress;
    }
    // Default to SUI
    return '0x2::sui::SUI';
}
/**
 * Get the function name for creating a lottery with a specific token
 * @param token - Token type (SUI or USDC)
 * @returns Function name for creating lottery
 */
export function getCreateFunctionName(token) {
    if (token === 'USDC') {
        return 'create_lottery_usdc';
    }
    return 'create_lottery_sui';
}
/**
 * Get minimum prize amount for a token type
 * @param token - Token type (SUI or USDC)
 * @returns Minimum prize amount in smallest units (mist for SUI, micro for USDC)
 */
export function getMinPrize(token) {
    if (token === 'USDC') {
        return 1000000; // 1 USDC (6 decimals)
    }
    return 1000000000; // 1 SUI (9 decimals)
}
/**
 * Parse prize amount to appropriate units
 * @param amount - Amount in whole units (e.g., 100 USDC)
 * @param token - Token type
 * @returns Amount in smallest units
 */
export function parsePrizeAmount(amount, token) {
    if (token === 'USDC') {
        // USDC has 6 decimals
        return amount * 1000000;
    }
    // SUI has 9 decimals (mist)
    return amount * 1000000000;
}
/**
 * Format prize amount from smallest units to human readable
 * @param amount - Amount in smallest units
 * @param token - Token type
 * @returns Formatted amount with token symbol
 */
export function formatPrizeAmount(amount, token) {
    if (token === 'USDC') {
        return `${(amount / 1000000).toFixed(2)} USDC`;
    }
    return `${(amount / 1000000000).toFixed(2)} SUI`;
}
//# sourceMappingURL=coin.js.map