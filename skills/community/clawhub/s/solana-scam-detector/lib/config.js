// config.js - Minimal config for read-only scam detection

module.exports = {
  // RPC endpoint for reading blockchain data
  // Note: Public RPCs log IP addresses and query patterns. Use a private RPC if privacy is a concern.
  RPC_URL: process.env.RPC_URL || 'https://api.mainnet-beta.solana.com',
  
  // Optional configurable thresholds
  MIN_TOKEN_AGE_HOURS: 4,
  MIN_LIQUIDITY_USD: 1000,
};

/*
  AGENT INSTRUCTIONS:
  
  This module is READ-ONLY. Only requires RPC_URL.
  
  Optional config:
  - MIN_TOKEN_AGE_HOURS (default: 4)
  - MIN_LIQUIDITY_USD (default: $1000)
*/