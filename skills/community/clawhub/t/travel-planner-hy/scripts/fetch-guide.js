'use strict';
const dns = require('node:dns').promises;
const https = require('node:https');
const ipaddr = require('ipaddr.js');
const { validateGuideUrl } = require('./safety');
const MAX_BYTES = 1024 * 1024;
const TIMEOUT = 10000;
function isPublicAddress(value) {
  try {
    const ip = ipaddr.parse(value);
    // Reject mapped IPv4 and all special-purpose, private, reserved and transition ranges.
    return ip.range() === 'unicast' && (ip.kind() !== 'ipv6' || ip.match(ipaddr.parse('2000::'), 3));
  } catch { return false; }
}
function fetchGuide(value) {
  return new Promise((resolve, reject) => {
    let active, stopped = false;
    const timer = setTimeout(() => finish(new Error('Guide request timed out.')), TIMEOUT);
    function finish(error, result) {
      if (stopped) return;
      stopped = true; clearTimeout(timer);
      if (error) { active?.destroy(); reject(error); } else resolve(result);
    }
    async function visit(value, redirects) {
      if (stopped) return;
      const url = new URL(validateGuideUrl(value));
      const addresses = await dns.lookup(url.hostname, { all: true, verbatim: true });
      if (stopped) return;
      if (!addresses.length || addresses.some(a => !isPublicAddress(a.address))) throw new Error('Non-public DNS address blocked.');
      const chosen = addresses[0];
      active = https.get(url, {
        agent: false, family: chosen.family, rejectUnauthorized: true,
        // Pin the validated address to the connection to prevent a second DNS lookup/rebinding.
        lookup: (_host, options, callback) => options?.all ? callback(null, [chosen]) : callback(null, chosen.address, chosen.family),
        headers: { Accept: 'text/html,text/plain', 'Accept-Encoding': 'identity', 'User-Agent': 'travel-planner-hy/1.3.2' }
      }, response => {
        if (stopped) { response.destroy(); return; }
        response.on('error', () => finish(new Error('Guide response failed.')));
        const status = response.statusCode;
        if ([301,302,303,307,308].includes(status)) {
          // Do not drain an unbounded redirect body while following its Location.
          response.destroy();
          if (redirects >= 3 || !response.headers.location) return finish(new Error('Guide redirect limit or invalid redirect.'));
          let next;
          try { next = new URL(response.headers.location, url).href; } catch { return finish(new Error('Invalid redirect.')); }
          visit(next, redirects + 1).catch(() => finish(new Error('Guide redirect blocked or failed.'))); return;
        }
        const type = (response.headers['content-type'] || '').split(';')[0].trim().toLowerCase();
        if (status !== 200 || !['text/html','text/plain'].includes(type) ||
          (response.headers['content-encoding'] && response.headers['content-encoding'] !== 'identity') ||
          Number(response.headers['content-length'] || 0) > MAX_BYTES) {
          response.destroy(); finish(new Error('Unsupported guide response.')); return;
        }
        const chunks = []; let size = 0;
        response.on('data', chunk => {
          size += chunk.length;
          if (size > MAX_BYTES) { response.destroy(); finish(new Error('Guide response exceeds 1 MiB.')); }
          else chunks.push(chunk);
        });
        response.on('end', () => finish(null, { url: url.href, contentType: type, untrustedContent: Buffer.concat(chunks).toString('utf8') }));
        response.on('aborted', () => finish(new Error('Guide response interrupted.')));
      });
      active.on('error', () => finish(new Error('Guide request failed.')));
    }
    visit(value, 0).catch(() => finish(new Error('Guide URL blocked or request failed.')));
  });
}
if (require.main === module) {
  if (process.argv.length !== 3) { console.error('Usage: node scripts/fetch-guide.js HTTPS_PUBLIC_GUIDE_URL'); process.exitCode = 1; }
  else fetchGuide(process.argv[2]).then(result => console.log(JSON.stringify(result)))
    .catch(e => { console.error(e.message); process.exitCode = 1; });
}
module.exports = { fetchGuide, isPublicAddress };
