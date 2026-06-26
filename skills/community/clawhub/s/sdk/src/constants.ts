import type { Sport } from './types';

/**
 * EdgeBets API base URL
 */
export const EDGEBETS_API_URL = 'https://api.edgebets.fun/api/v1';

/**
 * Treasury wallet for receiving payments
 */
export const TREASURY_WALLET = 'DuDLnnPzzRo8Yi9AKFEE7rsESVyTzQVPgC6h3FXYaDB4';

/**
 * USDC token mint on Solana mainnet
 */
export const USDC_MINT = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';

/**
 * USDC decimals
 */
export const USDC_DECIMALS = 6;

/**
 * Price per simulation in USDC (human-readable)
 */
export const PRICE_USDC = 0.5;

/**
 * Price per simulation in raw USDC units (with 6 decimals)
 */
export const PRICE_USDC_RAW = 500000;

/**
 * Default Solana RPC endpoint
 */
export const DEFAULT_RPC_ENDPOINT = 'https://api.mainnet-beta.solana.com';

/**
 * Default polling interval in milliseconds
 */
export const DEFAULT_POLLING_INTERVAL = 3000;

/**
 * Default polling timeout in milliseconds
 */
export const DEFAULT_POLLING_TIMEOUT = 120000;

/**
 * Default simulation count
 */
export const DEFAULT_SIMULATION_COUNT = 10000;

/**
 * Games endpoint mapping by sport
 */
export const GAMES_ENDPOINTS: Record<Sport, string> = {
  nba: 'games/basketball',
  nfl: 'games/football',
  mlb: 'games/baseball',
  mls: 'games/soccer',
};

/**
 * Simulation endpoint mapping by sport
 */
export const SIMULATION_ENDPOINTS: Record<Sport, string> = {
  nba: 'x402/simulate/nba',
  nfl: 'x402/simulate/nfl',
  mlb: 'x402/simulate/mlb',
  mls: 'x402/simulate/mls',
};

/**
 * x402 protocol version
 */
export const X402_VERSION = 1;

/**
 * Solana network identifier
 */
export const SOLANA_NETWORK = 'solana-mainnet';
