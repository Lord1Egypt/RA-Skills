// Scam detection module for Solana tokens
// READ-ONLY: Fetches token data from blockchain, no signing/wallet needed

const { Connection, PublicKey } = require('@solana/web3.js');
const cfg = require('./config');

// Initialize connection with timeout
const conn = new Connection(cfg.RPC_URL, {
  timeout: 10000,
  commitment: 'confirmed'
});

// === PARAMETRIC BLACKLISTS ===
// User can populate these (optional)

const BLACKLIST_EXACT = [];   // User adds bad tickers
const BLACKLIST_PATTERNS = [
  // Fake stock tickers (static sample, not exhaustive)
  'PIXEL', 'META', 'GOOGL', 'GOOGLUSDT', 'AAPL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'AAPLUSDT'
];
const BLACKLIST_MINTS = [];   // User adds known scam mints

// === CONFIG ===
const CONFIG = {
  MIN_TOKEN_AGE_HOURS: cfg.MIN_TOKEN_AGE_HOURS || 4,
  MIN_LIQUIDITY_USD: cfg.MIN_LIQUIDITY_USD || 1000
};

// === VALIDATE ADDRESS ===
function isValidSolanaAddress(address) {
  if (!address || typeof address !== 'string') return false;
  try {
    new PublicKey(address);
    return true;
  } catch {
    return false;
  }
}

// === MAIN CHECK FUNCTION ===
async function checkTokenSafety(mint, symbol) {
  const issues = [];
  
  // Validate mint address
  if (!isValidSolanaAddress(mint)) {
    return { safe: false, issues: ['Invalid Solana address'] };
  }
  
  // Normalize symbol
  const safeSymbol = (symbol || '').toUpperCase();
  
  // 1. Check blacklist (exact match)
  if (BLACKLIST_EXACT.includes(safeSymbol)) {
    issues.push(`Blacklisted ticker: ${symbol}`);
  }
  
  // 2. Check patterns
  if (BLACKLIST_PATTERNS.includes(safeSymbol)) {
    issues.push(`Suspicious ticker pattern: ${symbol}`);
  }
  
  // 3. Check known scam mints
  if (BLACKLIST_MINTS.includes(mint)) {
    issues.push('Known scam mint in blacklist');
  }
  
  // 4. Check token age
  try {
    const sigs = await conn.getSignaturesForAddress(new PublicKey(mint), { limit: 1 });
    if (sigs.length > 0 && sigs[0].blockTime) {
      const ageHours = (Date.now() / 1000 - sigs[0].blockTime) / 3600;
      
      if (ageHours < CONFIG.MIN_TOKEN_AGE_HOURS) {
        issues.push(`Token is <${CONFIG.MIN_TOKEN_AGE_HOURS}h old - high risk`);
      }
    }
  } catch (e) {
    issues.push('Could not verify token age');
  }
  
  return {
    safe: issues.length === 0,
    issues,
    config: CONFIG
  };
}

// === ADD TO BLACKLIST (for agents that want this) ===
function addToBlacklist(type, value) {
  if (type === 'ticker') BLACKLIST_EXACT.push((value || '').toUpperCase());
  if (type === 'mint' && isValidSolanaAddress(value)) BLACKLIST_MINTS.push(value);
  if (type === 'pattern') BLACKLIST_PATTERNS.push((value || '').toUpperCase());
}

module.exports = { 
  checkTokenSafety, 
  addToBlacklist,
  isValidSolanaAddress,
  BLACKLIST_EXACT,
  BLACKLIST_PATTERNS,
  BLACKLIST_MINTS,
  CONFIG
};

/*
  AGENT INSTRUCTIONS:
  
  This is a READ-ONLY module. It only fetches blockchain data.
  
  Required: RPC_URL (or use default public RPC)
  
  NOT required: wallet key, Telegram ID, trade history
  
  Optional for agent:
  - Ask user to add tickers to BLACKLIST_EXACT
  - Ask user to add mints to BLACKLIST_MINTS
  - Ask user for MIN_TOKEN_AGE_HOURS preference
*/