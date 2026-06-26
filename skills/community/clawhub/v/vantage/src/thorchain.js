/**
 * thorchain.js — THORChain routing module
 * Wraps NineRealms THORNode REST API for swap quoting and memo formatting.
 */

'use strict';

require('dotenv').config();
const axios = require('axios');

const THORNODE_URL = process.env.THORNODE_URL || 'https://thornode.ninerealms.com';

const client = axios.create({
  baseURL: THORNODE_URL,
  timeout: 10_000,
  headers: { 'Accept': 'application/json' },
});

/**
 * Get a swap quote from THORChain.
 *
 * @param {string} fromAsset  e.g. "ETH.ETH"
 * @param {string} toAsset    e.g. "BTC.BTC"
 * @param {string} amount     amount in base units (8 decimals, no decimal point)
 * @param {string} [destination] optional destination address
 * @returns {Promise<object>} quote response
 */
async function getQuote(fromAsset, toAsset, amount, destination = '') {
  const params = {
    from_asset: fromAsset,
    to_asset: toAsset,
    amount,
  };
  if (destination) params.destination = destination;

  const { data } = await client.get('/thorchain/quote/swap', { params });
  return data;
}

/**
 * Fetch current inbound addresses (vault + chain metadata).
 * Use these to determine which vault to send funds to.
 *
 * @returns {Promise<Array>} array of inbound address objects per chain
 */
async function getInboundAddresses() {
  const { data } = await client.get('/thorchain/inbound_addresses');
  return data;
}

/**
 * Format a THORChain SWAP memo string.
 *
 * @param {string} toAsset        e.g. "BTC.BTC"
 * @param {string} destAddress    receiving address on target chain
 * @param {number} [limitBps]     optional slippage limit in basis points (e.g. 300 = 3%)
 * @param {string} [affiliate]    optional affiliate address
 * @param {number} [feeBps]       optional affiliate fee in basis points
 * @returns {string} memo string
 *
 * Format: SWAP:ASSET:DESTADDR:LIMIT:AFFILIATE:FEE
 */
function formatSwapMemo(toAsset, destAddress, limitBps = 0, affiliate = '', feeBps = 0) {
  const parts = ['SWAP', toAsset, destAddress];

  if (limitBps || affiliate || feeBps) {
    parts.push(String(limitBps));
  }
  if (affiliate || feeBps) {
    parts.push(affiliate);
    parts.push(String(feeBps));
  }

  return parts.join(':');
}

module.exports = { getQuote, getInboundAddresses, formatSwapMemo };
