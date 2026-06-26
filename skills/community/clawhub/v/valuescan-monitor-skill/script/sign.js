'use strict';

const crypto = require('crypto');

/**
 * Build stream SSE authentication query parameters.
 * Auth: HMAC-SHA256(key=secretKey, message=timestamp+'{}')
 *
 * @param {string} apiKey
 * @param {string} secretKey
 * @returns {{ apiKey: string, timestamp: string, nonce: string, sign: string }}
 */
function buildStreamParams(apiKey, secretKey) {
    const timestamp = Date.now().toString();
    const nonce = crypto.randomUUID();
    const sign = crypto.createHmac('sha256', secretKey)
        .update(timestamp + nonce)
        .digest('hex');
    return { apiKey, timestamp, nonce, sign };
}

/**
 * Build main API authentication headers.
 * Auth: HMAC-SHA256(key=secretKey, message=timestamp+body)
 *
 * @param {string} apiKey
 * @param {string} secretKey
 * @param {string} body  Raw POST body string
 * @returns {Record<string, string>}
 */
function buildApiHeaders(apiKey, secretKey, body) {
    const timestamp = Date.now().toString();
    const sign = crypto.createHmac('sha256', secretKey)
        .update(timestamp + body)
        .digest('hex');
    return {
        'X-API-KEY': apiKey,
        'X-TIMESTAMP': timestamp,
        'X-SIGN': sign,
        'Content-Type': 'application/json; charset=utf-8',
    };
}

module.exports = { buildStreamParams, buildApiHeaders };
