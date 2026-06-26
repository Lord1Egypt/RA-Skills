/**
 * trader.js — Live Order Execution via Hyperliquid REST API
 *
 * Signs orders with the buyer's private key using Hyperliquid's EIP-712
 * signing scheme (msgpack action hash → keccak256 → typed-data sign).
 *
 * Security rules:
 *   - Private key is NEVER logged or included in error output
 *   - Key is validated before any API call
 *   - --paper mode is enforced when key is absent
 *
 * Supported order types:
 *   - Market order (IoC limit with 5% slippage tolerance)
 *   - Limit order (GTC)
 *   - Close position (reduce-only market order)
 */

'use strict';

const https = require('https');

const HL_EXCHANGE_URL  = 'https://api.hyperliquid.xyz/exchange';
const HL_INFO_URL      = 'https://api.hyperliquid.xyz/info';
const MARKET_SLIPPAGE  = 0.05; // 5% — generous buffer for perp markets

// ── Lazy-loaded deps (optional at require time, fail clearly at call time) ────

let _ethers   = null;
let _msgpack  = null;

function _loadEthers() {
  if (!_ethers) {
    try { _ethers = require('ethers'); }
    catch (_) { throw new Error('Run: npm install ethers @msgpack/msgpack'); }
  }
  return _ethers;
}

function _loadMsgpack() {
  if (!_msgpack) {
    try { _msgpack = require('@msgpack/msgpack'); }
    catch (_) { throw new Error('Run: npm install ethers @msgpack/msgpack'); }
  }
  return _msgpack;
}

// ── Key Validation ────────────────────────────────────────────────────────────

/**
 * Validate a Hyperliquid private key without making any network calls.
 * @param {string} key
 * @returns {{ valid: boolean, address?: string, error?: string }}
 */
function validatePrivateKey(key) {
  if (!key) return { valid: false, error: 'HYPERLIQUID_PRIVATE_KEY is not set in .env' };

  if (!/^0x[0-9a-fA-F]{64}$/.test(key)) {
    return {
      valid: false,
      error: 'HYPERLIQUID_PRIVATE_KEY must be a 0x-prefixed 64-character hex string (32 bytes)',
    };
  }

  try {
    const { Wallet } = _loadEthers();
    const wallet = new Wallet(key);
    return { valid: true, address: wallet.address };
  } catch (err) {
    return { valid: false, error: `Key failed cryptographic validation: ${err.message}` };
  }
}

// ── Price / Size Formatting ───────────────────────────────────────────────────

/**
 * Convert a number to Hyperliquid wire format string.
 * Up to 8 significant figures, no trailing zeros, no scientific notation.
 */
function _floatToWire(x) {
  if (!x || x === 0) return '0';
  const rounded = parseFloat(x.toPrecision(8));
  // toFixed(10) avoids scientific notation; strip trailing zeros
  return rounded.toFixed(10).replace(/\.?0+$/, '') || '0';
}

// ── Signing ───────────────────────────────────────────────────────────────────

/**
 * Compute the Hyperliquid action hash.
 * actionHash = keccak256( msgpack(action) | nonce_8bytes_be | 0x00 [| 0x01 + vaultAddr] )
 */
function _computeActionHash(action, nonce, vaultAddress) {
  const { encode } = _loadMsgpack();
  const { keccak256 } = _loadEthers();

  const packed  = Buffer.from(encode(action));
  const nonceBuf = Buffer.alloc(8);
  nonceBuf.writeBigUInt64BE(BigInt(nonce));

  let data;
  if (!vaultAddress) {
    data = Buffer.concat([packed, nonceBuf, Buffer.from([0x00])]);
  } else {
    data = Buffer.concat([
      packed, nonceBuf,
      Buffer.from([0x01]),
      Buffer.from(vaultAddress.slice(2), 'hex'),
    ]);
  }

  return keccak256(data); // returns 0x-prefixed hex string
}

/**
 * Sign a Hyperliquid L1 action using EIP-712 typed data.
 * Returns { r, s, v } components expected by the exchange API.
 */
async function _signL1Action(privateKey, action, nonce, isMainnet, vaultAddress) {
  const { Wallet } = _loadEthers();
  const wallet = new Wallet(privateKey);

  const connectionId = _computeActionHash(action, nonce, vaultAddress || null);

  const domain = {
    chainId:         1337,
    name:            'Exchange',
    verifyingContract: '0x0000000000000000000000000000000000000000',
    version:         '1',
  };

  const types = {
    Agent: [
      { name: 'source',       type: 'string'  },
      { name: 'connectionId', type: 'bytes32' },
    ],
  };

  const value = {
    source:       isMainnet ? 'a' : 'b',
    connectionId,
  };

  const sig = await wallet.signTypedData(domain, types, value);

  // sig is 65-byte hex: 32 (r) + 32 (s) + 1 (v)
  return {
    r: '0x' + sig.slice(2, 66),
    s: '0x' + sig.slice(66, 130),
    v: parseInt(sig.slice(130, 132), 16),
  };
}

// ── HTTP ──────────────────────────────────────────────────────────────────────

function _postExchange(payload) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(payload);
    const req  = https.request({
      hostname: 'api.hyperliquid.xyz',
      path:     '/exchange',
      method:   'POST',
      headers:  { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
    }, (res) => {
      let raw = '';
      res.on('data', (c) => (raw += c));
      res.on('end', () => {
        try { resolve(JSON.parse(raw)); }
        catch (e) { reject(new Error(`JSON parse: ${e.message}`)); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function _postInfo(body) {
  return new Promise((resolve, reject) => {
    const bodyStr = JSON.stringify(body);
    const req = https.request({
      hostname: 'api.hyperliquid.xyz',
      path:     '/info',
      method:   'POST',
      headers:  { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(bodyStr) },
    }, (res) => {
      let raw = '';
      res.on('data', (c) => (raw += c));
      res.on('end', () => {
        try { resolve(JSON.parse(raw)); }
        catch (e) { reject(new Error(`JSON parse: ${e.message}`)); }
      });
    });
    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

// Cache asset universe to avoid repeated meta calls within a session
let _assetUniverse = null;

async function _getAssetIndex(coin) {
  if (!_assetUniverse) {
    const data     = await _postInfo({ type: 'meta' });
    _assetUniverse = data.universe || [];
  }
  const idx = _assetUniverse.findIndex((a) => a.name.toUpperCase() === coin.toUpperCase());
  if (idx === -1) throw new Error(`Coin ${coin} not listed on Hyperliquid`);
  return idx;
}

// ── Public: Order Execution ───────────────────────────────────────────────────

/**
 * Place a live order on Hyperliquid.
 *
 * @param {object} params
 * @param {string}           params.coin        e.g. 'RUNE'
 * @param {boolean}          params.isBuy       true = long, false = short
 * @param {number}           params.sizeUsd     USD notional size
 * @param {number}           params.markPrice   Current mark price (for sizing + slippage)
 * @param {'market'|'limit'} [params.orderType] Default: 'market'
 * @param {number}           [params.limitPrice] Required if orderType='limit'
 * @param {boolean}          [params.reduceOnly] Default: false
 *
 * @returns {Promise<{ success, orderId, coin, side, size, fillPrice, error }>}
 */
async function placeOrder({ coin, isBuy, sizeUsd, markPrice, orderType = 'market', limitPrice, reduceOnly = false }) {
  const privateKey = process.env.HYPERLIQUID_PRIVATE_KEY;
  const isMainnet  = process.env.HYPERLIQUID_TESTNET !== 'true';

  // Gate: enforce paper mode if no key
  if (!privateKey) {
    return {
      success: false,
      error:   'HYPERLIQUID_PRIVATE_KEY not set. Use --paper flag for paper trading.',
    };
  }

  const keyCheck = validatePrivateKey(privateKey);
  if (!keyCheck.valid) {
    return { success: false, error: keyCheck.error };
  }

  // Enforce config limits before touching the exchange
  const maxPositionUsd = parseFloat(process.env.MAX_POSITION_SIZE_USD) || 500;
  if (sizeUsd > maxPositionUsd) {
    return {
      success: false,
      error:   `Order size $${sizeUsd} exceeds MAX_POSITION_SIZE_USD $${maxPositionUsd}`,
    };
  }

  try {
    const assetIndex = await _getAssetIndex(coin);
    const sizeCoins  = sizeUsd / markPrice;

    let price;
    if (orderType === 'market') {
      price = isBuy
        ? markPrice * (1 + MARKET_SLIPPAGE)
        : markPrice * (1 - MARKET_SLIPPAGE);
    } else {
      if (!limitPrice) throw new Error('limitPrice is required for limit orders');
      price = limitPrice;
    }

    const tif = orderType === 'market' ? 'Ioc' : 'Gtc';

    // Key ordering MUST match Hyperliquid Python SDK for identical msgpack bytes
    const action = {
      type:     'order',
      orders:   [{
        a: assetIndex,
        b: isBuy,
        p: _floatToWire(price),
        s: _floatToWire(sizeCoins),
        r: reduceOnly,
        t: { limit: { tif } },
      }],
      grouping: 'na',
    };

    const nonce     = Date.now();
    const signature = await _signL1Action(privateKey, action, nonce, isMainnet, null);
    const result    = await _postExchange({ action, nonce, signature });

    if (result.status === 'ok') {
      const statuses  = result.response?.data?.statuses || [];
      const status    = statuses[0] || {};

      if (status.error) {
        return { success: false, error: status.error, coin, side: isBuy ? 'long' : 'short' };
      }

      const filled    = status.filled || {};
      const orderId   = filled.oid   ?? status.resting?.oid ?? null;
      const fillPrice = parseFloat(filled.avgPx || price);

      console.log(`[trader] ${new Date().toISOString()} | ${coin.toUpperCase()} ${isBuy ? 'LONG' : 'SHORT'} | size: ${sizeCoins.toFixed(6)} | price: $${fillPrice} | orderId: ${orderId}`);

      return {
        success:    true,
        orderId,
        coin:       coin.toUpperCase(),
        side:       isBuy ? 'long' : 'short',
        size:       parseFloat(sizeCoins.toFixed(6)),
        fillPrice,
        error:      null,
      };

    } else {
      const errMsg = typeof result.response === 'string' ? result.response : JSON.stringify(result);
      return { success: false, error: errMsg, coin, side: isBuy ? 'long' : 'short' };
    }

  } catch (err) {
    // Sanitize: strip private key from error text (belt-and-suspenders)
    const safeMsg = err.message.replace(privateKey || '', '[REDACTED]');
    return { success: false, error: safeMsg, coin };
  }
}

/**
 * Close an open position for a coin (reduce-only market order).
 *
 * @param {string} coin
 * @param {number} positionSize  Size in coins (from getPositions)
 * @param {'long'|'short'} positionSide
 * @param {number} markPrice
 * @returns {Promise<{ success, orderId, coin, side, size, fillPrice, error }>}
 */
async function closePosition(coin, positionSize, positionSide, markPrice) {
  const isBuy = positionSide === 'short'; // close short = buy
  const sizeUsd = positionSize * markPrice;

  return placeOrder({
    coin,
    isBuy,
    sizeUsd,
    markPrice,
    orderType: 'market',
    reduceOnly: true,
  });
}

module.exports = { placeOrder, closePosition, validatePrivateKey };
