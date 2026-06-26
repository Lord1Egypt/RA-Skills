'use strict';

const { sm3 } = require('sm-crypto');

/**
 * SM3 哈希
 * @param {string|Buffer} data
 * @returns {string} hex hash
 */
function hash(data) {
  const input = typeof data === 'string' ? data : data.toString('hex');
  return sm3(input);
}

module.exports = { hash };
