#!/usr/bin/env node
'use strict';
const { CSP, escapeHtml, validatePlatformUrl, writeOutput } = require('./lib/safety');
async function renderQRCodeHTML(value) {
  const url = validatePlatformUrl(value);
  const qrCodeBase64 = await require('qrcode').toDataURL(url, { margin: 2, width: 300 });
  const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">${CSP}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Platform homepage / 平台首页</title>
<style>body{font:16px system-ui,sans-serif;max-width:520px;margin:48px auto;padding:24px;text-align:center}img{max-width:100%}a{overflow-wrap:anywhere}</style></head>
<body><h1>Platform homepage / 平台首页</h1>
<img src="${escapeHtml(qrCodeBase64)}" alt="Platform homepage QR code">
<p><a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(url)}</a></p>
<p>Search and book independently on the platform. This QR opens only its public homepage.</p>
<p>此二维码仅打开平台公开首页，请在平台内自行搜索及预订。</p></body></html>`;
  return { html, qrCodeBase64, url };
}
async function generateQRCodeHTML(url, options = {}) {
  if (!options || typeof options !== 'object' || Object.keys(options).some(k => k !== 'desktop') ||
      (options.desktop !== undefined && typeof options.desktop !== 'boolean')) throw new Error('Only the desktop option is supported.');
  const result = await renderQRCodeHTML(url);
  const outputPath = writeOutput(result.html, 'platform-qr', 'html', options.desktop === true);
  return { success: true, outputPath, qrCodeBase64: result.qrCodeBase64 };
}
if (require.main === module) {
  const args = process.argv.slice(2);
  if (!args.length || args.length > 2 || (args[1] && args[1] !== '--desktop')) {
    console.error('Usage: node scripts/qrcode.js https://www.tuniu.com/ [--desktop]'); process.exitCode = 1;
  } else generateQRCodeHTML(args[0], { desktop: args[1] === '--desktop' }).then(r => console.log('QR page saved:', r.outputPath))
    .catch(() => { console.error('QR generation failed. Use an approved public homepage URL and install local dependencies.'); process.exitCode = 1; });
}
module.exports = { renderQRCodeHTML, generateQRCodeHTML };
