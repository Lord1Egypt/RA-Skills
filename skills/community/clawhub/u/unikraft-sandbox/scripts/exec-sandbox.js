#!/usr/bin/env node
// exec-sandbox.js — run a command inside a UKC sandbox via the exec API
// Usage: exec-sandbox.js <fqdn> <cmd>
// Exit code mirrors the remote command's exit code.

const https = require('https');

const [,, fqdn, ...cmdParts] = process.argv;
if (!fqdn || cmdParts.length === 0) {
  console.error('Usage: exec-sandbox.js <fqdn> <cmd>');
  process.exit(1);
}
const cmd = cmdParts.join(' ');

const body = JSON.stringify({ cmd });
const options = {
  hostname: fqdn,
  port: 443,
  path: '/exec',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body),
  },
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    if (res.statusCode !== 200) {
      console.error(`HTTP ${res.statusCode}: ${data}`);
      process.exit(1);
    }
    let parsed;
    try { parsed = JSON.parse(data); } catch {
      console.error('Failed to parse response:', data);
      process.exit(1);
    }
    if (parsed.stdout) process.stdout.write(parsed.stdout);
    if (parsed.stderr) process.stderr.write(parsed.stderr);
    process.exit(parsed.code ?? 0);
  });
});

req.on('error', (err) => { console.error('Request error:', err.message); process.exit(1); });
req.write(body);
req.end();
