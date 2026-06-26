/**
 * sizing.js — Kelly Criterion Position Sizing
 *
 * Sizes every trade based on live account balance and signal confidence.
 * Uses quarter-Kelly by default (KELLY_FRACTION=0.25) for conservative sizing.
 *
 * Formula:
 *   Kelly %          = confidence × edge / odds  (simplified: confidence, odds ≈ 1)
 *   Conservative Kelly = Kelly % × KELLY_FRACTION
 *   Position size    = min(Conservative Kelly × balance, MAX_ACCOUNT_RISK_PCT%, MAX_POSITION_SIZE_USD)
 *
 * If balance fetch fails → aborts trade. Never defaults to an arbitrary size.
 */

'use strict';

const { getAccountBalance } = require('./hyperliquid');

/**
 * Calculate the USD position size for a trade.
 *
 * @param {number} confidence  Signal confidence 0–1 (used as edge proxy)
 * @param {string} walletAddress  Hyperliquid wallet address
 * @returns {Promise<{ sizeUsd: number, balance: number, kellySizePct: number }>}
 * @throws {Error} if balance fetch fails (caller must abort the trade)
 */
async function calculatePositionSize(confidence, walletAddress) {
  if (confidence <= 0 || confidence > 1) {
    throw new Error(`Invalid confidence value: ${confidence} (must be 0–1)`);
  }

  const maxPositionUsd  = parseFloat(process.env.MAX_POSITION_SIZE_USD)  || 500;
  const maxRiskPct      = parseFloat(process.env.MAX_ACCOUNT_RISK_PCT)   || 2;
  const kellyFraction   = parseFloat(process.env.KELLY_FRACTION)         || 0.25;

  // Fetch live balance — hard abort if this fails
  const balance = await getAccountBalance(walletAddress);

  // Kelly formula: edge proxy = confidence, odds ≈ 1 (symmetric crypto payoff)
  const kellyPct             = confidence;
  const conservativeKellyPct = kellyPct * kellyFraction;

  const kellySize    = conservativeKellyPct * balance;
  const riskCapSize  = (maxRiskPct / 100) * balance;
  const sizeUsd      = Math.min(kellySize, riskCapSize, maxPositionUsd);

  return {
    sizeUsd:       parseFloat(sizeUsd.toFixed(2)),
    balance:       parseFloat(balance.toFixed(2)),
    kellySizePct:  parseFloat((conservativeKellyPct * 100).toFixed(3)),
  };
}

module.exports = { calculatePositionSize };
