/**
 * Shadow Binance Bot - Binance API Connection
 * Handles all communication with Binance API
 */

const crypto = require('crypto');
const https = require('https');

// API Configuration
const BASE_SPOT_URL = 'api.binance.com';
const BASE_FUTURES_URL = 'fapi.binance.com';

// Retry configuration
const MAX_RETRIES = 3;
const BASE_DELAY_MS = 500;

/**
 * Delay utility for retry backoff
 * @param {number} ms - Milliseconds to wait
 * @returns {Promise<void>}
 */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Generate signature for Binance API
 * @param {string} queryString - The query string to sign
 * @param {string} secret - Your API secret
 * @returns {string} - The signature
 */
function generateSignature(queryString, secret) {
  return crypto.createHmac('sha256', secret).update(queryString).digest('hex');
}

/**
 * Check if a Binance API response is an error
 * @param {object} data - Response data
 * @returns {boolean} - True if error
 */
function isBinanceError(data) {
  return data && typeof data === 'object' && typeof data.code === 'number' && data.msg;
}

/**
 * Determine if an error is retryable
 * @param {Error|object} error - Error or response data
 * @returns {boolean} - True if safe to retry
 */
function isRetryable(error) {
  // Network/transport errors are retryable
  if (error instanceof Error) {
    const msg = error.message.toLowerCase();
    if (msg.includes('timeout') || msg.includes('econnreset') || msg.includes('econnrefused') || msg.includes('socket')) {
      return true;
    }
  }
  // Binance error codes that are retryable
  // -1003 = RATE_LIMIT, -1023 = Maintenance, -1001 = DISCONNECTED
  if (error && error.code && [-1003, -1023, -1001].includes(error.code)) {
    return true;
  }
  return false;
}

/**
 * Make HTTP request to Binance API with automatic retry
 * @param {string} hostname - API hostname
 * @param {string} path - API path
 * @param {string} method - HTTP method
 * @param {object} headers - Request headers
 * @returns {Promise<object>} - API response
 */
async function makeRequest(hostname, path, method, headers = {}) {
  let lastError;

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      const result = await _doRequest(hostname, path, method, headers);

      // If Binance returned a retryable error, retry
      if (isRetryable(result)) {
        if (attempt < MAX_RETRIES) {
          const backoffMs = BASE_DELAY_MS * Math.pow(2, attempt - 1);
          console.error(`[Retry ${attempt}/${MAX_RETRIES}] Rate-limited. Waiting ${backoffMs}ms...`);
          await delay(backoffMs);
          continue;
        }
      }

      return result;
    } catch (err) {
      lastError = err;

      if (isRetryable(err) && attempt < MAX_RETRIES) {
        const backoffMs = BASE_DELAY_MS * Math.pow(2, attempt - 1);
        console.error(`[Retry ${attempt}/${MAX_RETRIES}] ${err.message}. Waiting ${backoffMs}ms...`);
        await delay(backoffMs);
      } else {
        throw err;
      }
    }
  }

  throw lastError;
}

/**
 * Internal: perform a single HTTP request
 * @param {string} hostname - API hostname
 * @param {string} path - API path
 * @param {string} method - HTTP method
 * @param {object} headers - Request headers
 * @returns {Promise<object>} - API response
 */
function _doRequest(hostname, path, method, headers = {}) {
  return new Promise((resolve, reject) => {
    const options = { hostname, path, method, headers };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed);
        } catch (e) {
          reject(new Error(`Failed to parse response: ${data}`));
        }
      });
    });

    req.on('error', (err) => {
      // Wrap as retryable if it's a network error
      if (isRetryable(err)) {
        reject(err);
      } else {
        reject(new Error(`Network error: ${err.message}`));
      }
    });

    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Request timed out after 10 seconds'));
    });

    req.end();
  });
}

/**
 * Get Spot Account Balance
 * @param {string} apiKey - Your Binance API Key
 * @param {string} apiSecret - Your Binance API Secret
 * @returns {Promise<object>} - Account balances
 */
async function getSpotBalance(apiKey, apiSecret) {
  const timestamp = Date.now();
  const queryString = `timestamp=${timestamp}`;
  const signature = generateSignature(queryString, apiSecret);

  const path = `/api/v3/account?${queryString}&signature=${signature}`;
  const data = await makeRequest(BASE_SPOT_URL, path, 'GET', {
    'X-MBX-APIKEY': apiKey
  });

  if (isBinanceError(data)) {
    throw new Error(`Binance API Error [${data.code}]: ${data.msg}`);
  }

  return data;
}

/**
 * Get Futures Account Balance
 * @param {string} apiKey - Your Binance API Key
 * @param {string} apiSecret - Your Binance API Secret
 * @returns {Promise<object>} - Futures account data
 */
async function getFuturesBalance(apiKey, apiSecret) {
  const timestamp = Date.now();
  const queryString = `timestamp=${timestamp}`;
  const signature = generateSignature(queryString, apiSecret);

  const path = `/fapi/v2/account?${queryString}&signature=${signature}`;
  const data = await makeRequest(BASE_FUTURES_URL, path, 'GET', {
    'X-MBX-APIKEY': apiKey
  });

  if (isBinanceError(data)) {
    throw new Error(`Binance API Error [${data.code}]: ${data.msg}`);
  }

  return data;
}

/**
 * Get Futures Income/PNL History
 * @param {string} apiKey - Your Binance API Key
 * @param {string} apiSecret - Your Binance API Secret
 * @param {number} daysBack - How many days back to fetch
 * @returns {Promise<array>} - Income history
 */
async function getFuturesIncome(apiKey, apiSecret, daysBack = 365) {
  const timestamp = Date.now();
  const startTime = timestamp - (daysBack * 24 * 60 * 60 * 1000);
  const queryString = `startTime=${startTime}&timestamp=${timestamp}&limit=1000`;
  const signature = generateSignature(queryString, apiSecret);

  const path = `/fapi/v1/income?${queryString}&signature=${signature}`;
  const data = await makeRequest(BASE_FUTURES_URL, path, 'GET', {
    'X-MBX-APIKEY': apiKey
  });

  if (isBinanceError(data)) {
    throw new Error(`Binance API Error [${data.code}]: ${data.msg}`);
  }

  return data;
}

/**
 * Get Spot Trade History
 * @param {string} apiKey - Your Binance API Key
 * @param {string} apiSecret - Your Binance API Secret
 * @param {string} symbol - Trading pair (e.g., 'BTCUSDT')
 * @param {number} limit - Number of trades to fetch (max 1000)
 * @returns {Promise<array>} - Trade history
 */
async function getSpotTrades(apiKey, apiSecret, symbol = 'BTCUSDT', limit = 100) {
  const timestamp = Date.now();
  const queryString = `symbol=${symbol}&timestamp=${timestamp}&limit=${limit}`;
  const signature = generateSignature(queryString, apiSecret);

  const path = `/api/v3/myTrades?${queryString}&signature=${signature}`;
  const data = await makeRequest(BASE_SPOT_URL, path, 'GET', {
    'X-MBX-APIKEY': apiKey
  });

  if (isBinanceError(data)) {
    throw new Error(`Binance API Error [${data.code}]: ${data.msg}`);
  }

  return data;
}

/**
 * Get all Spot trades for multiple symbols
 * @param {string} apiKey - Your Binance API Key
 * @param {string} apiSecret - Your Binance API Secret
 * @param {array} symbols - Array of trading pairs to fetch
 * @returns {Promise<object>} - All trades grouped by symbol, plus errors array
 */
async function getAllSpotTrades(apiKey, apiSecret, symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']) {
  const allTrades = {};
  const errors = [];

  for (const symbol of symbols) {
    try {
      const trades = await getSpotTrades(apiKey, apiSecret, symbol, 100);
      if (Array.isArray(trades) && trades.length > 0) {
        allTrades[symbol] = trades;
      }
    } catch (e) {
      errors.push({ symbol, error: e.message });
      console.error(`Failed to fetch trades for ${symbol}: ${e.message}`);
    }
  }

  return { trades: allTrades, errors };
}

/**
 * Test API Connection
 * @param {string} apiKey - Your Binance API Key
 * @param {string} apiSecret - Your Binance API Secret
 * @returns {Promise<boolean>} - Connection successful?
 */
async function testConnection(apiKey, apiSecret) {
  try {
    const balance = await getSpotBalance(apiKey, apiSecret);
    return balance && !balance.code;
  } catch (e) {
    console.error('Connection test failed:', e.message);
    return false;
  }
}

module.exports = {
  getSpotBalance,
  getFuturesBalance,
  getFuturesIncome,
  getSpotTrades,
  getAllSpotTrades,
  testConnection,
  generateSignature
};
