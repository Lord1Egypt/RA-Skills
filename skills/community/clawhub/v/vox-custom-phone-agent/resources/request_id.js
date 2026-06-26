'use strict';

const crypto = require('crypto');

function createRequestId(prefix = 'req') {
  const now = new Date();
  const stamp = now.toISOString().replace(/[-:TZ.]/g, '').slice(0, 14);
  const suffix = crypto.randomBytes(3).toString('hex');
  return `${prefix}_${stamp}_${suffix}`;
}

module.exports = { createRequestId };
