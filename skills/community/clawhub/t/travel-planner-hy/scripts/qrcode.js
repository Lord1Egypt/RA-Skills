#!/usr/bin/env node
'use strict';
// Local QR encoding of approved public homepages only; no fetch or payment flow.
const QRCode = require('qrcode');
const { validatePlatformUrl, writeOutput } = require('./safety');
const OPTIONS = { width: 300, margin: 2, errorCorrectionLevel: 'M' };
async function generateQRBase64(value) {
  const url = validatePlatformUrl(value);
  return QRCode.toDataURL(url, OPTIONS);
}
async function generateQR(value, filename) {
  const url = validatePlatformUrl(value);
  const buffer = await QRCode.toBuffer(url, { ...OPTIONS, type: 'png' });
  return writeOutput(buffer, 'qr', 'png', filename);
}
if (require.main === module) {
  const args = process.argv.slice(2);
  if (!args.length || args.length > 2) {
    console.error('Usage: node scripts/qrcode.js https://www.tuniu.com/ [safe-name.png]'); process.exitCode = 1;
  } else generateQR(args[0], args[1]).then(file => console.log('QR saved:', file))
    .catch(e => { console.error(e.message); process.exitCode = 1; });
}
module.exports = { generateQR, generateQRBase64 };
