#!/usr/bin/env node
// fetch-docs.js — Fetch and display the first 4000 chars of official web3 docs
// Usage: node fetch-docs.js <topic>
// No external dependencies — uses Node.js https built-in

const https = require('https');
const http  = require('http');

const SOURCES = {
  solidity:     'https://docs.soliditylang.org/en/latest/',
  foundry:      'https://book.getfoundry.sh/',
  viem:         'https://viem.sh/docs/getting-started',
  wagmi:        'https://wagmi.sh/react/getting-started',
  openzeppelin: 'https://docs.openzeppelin.com/contracts/5.x/',
  erc20:        'https://docs.openzeppelin.com/contracts/5.x/erc20',
  erc721:       'https://docs.openzeppelin.com/contracts/5.x/erc721',
  erc4626:      'https://docs.openzeppelin.com/contracts/5.x/erc4626',
  hardhat:      'https://hardhat.org/hardhat-runner/docs/getting-started',
  'uniswap-v3': 'https://docs.uniswap.org/contracts/v3/overview',
  aave:         'https://docs.aave.com/developers/',
  ethers:       'https://docs.ethers.org/v6/',
};

const topic = process.argv[2];
if (!topic) {
  console.log('Usage: node fetch-docs.js <topic>');
  console.log('Available topics:', Object.keys(SOURCES).join(', '));
  process.exit(0);
}

const url = SOURCES[topic.toLowerCase()];
if (!url) {
  console.error(`Unknown topic: ${topic}`);
  console.error('Available topics:', Object.keys(SOURCES).join(', '));
  process.exit(1);
}

// HTML entity decoding (common entities)
function decodeEntities(str) {
  return str
    .replace(/&amp;/g,  '&')
    .replace(/&lt;/g,   '<')
    .replace(/&gt;/g,   '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g,  "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#x([0-9a-fA-F]+);/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, dec) => String.fromCharCode(parseInt(dec, 10)));
}

// Strip all HTML tags, then clean up whitespace
function stripHTML(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, '')   // remove script blocks
    .replace(/<style[\s\S]*?<\/style>/gi, '')      // remove style blocks
    .replace(/<[^>]+>/g, ' ')                       // remove all tags
    .replace(/\s{2,}/g, ' ')                        // collapse whitespace
    .replace(/\n{3,}/g, '\n\n')                     // collapse blank lines
    .trim();
}

function fetchPage(targetUrl, redirectCount = 0) {
  return new Promise((resolve, reject) => {
    if (redirectCount > 5) return reject(new Error('Too many redirects'));

    const parsedUrl = new URL(targetUrl);
    const lib = parsedUrl.protocol === 'https:' ? https : http;

    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; web3-docs-fetcher/1.0)',
        'Accept': 'text/html,application/xhtml+xml',
      },
    };

    const timer = setTimeout(() => {
      req.destroy();
      reject(new Error(`Request timed out after 15s fetching ${targetUrl}`));
    }, 15000);

    const req = lib.get(options, res => {
      // Follow redirects
      if (res.statusCode === 301 || res.statusCode === 302 || res.statusCode === 307 || res.statusCode === 308) {
        clearTimeout(timer);
        const location = res.headers.location;
        if (!location) return reject(new Error('Redirect with no Location header'));
        // Handle relative redirects
        const nextUrl = location.startsWith('http') ? location : new URL(location, targetUrl).href;
        res.resume();
        return fetchPage(nextUrl, redirectCount + 1).then(resolve).catch(reject);
      }

      if (res.statusCode !== 200) {
        clearTimeout(timer);
        res.resume();
        return reject(new Error(`HTTP ${res.statusCode} for ${targetUrl}`));
      }

      let d = '';
      res.on('data', c => { d += c; });
      res.on('end', () => {
        clearTimeout(timer);
        resolve(d);
      });
    });

    req.on('error', e => { clearTimeout(timer); reject(e); });
  });
}

async function main() {
  console.error(`Fetching: ${url}`);
  let html;
  try {
    html = await fetchPage(url);
  } catch (e) {
    console.error(`Error fetching docs: ${e.message}`);
    console.error(`\nFallback: open ${url} in your browser, or use web_fetch tool.`);
    process.exit(1);
  }

  const text = decodeEntities(stripHTML(html));
  const output = text.slice(0, 4000);

  console.log(`\n=== ${topic.toUpperCase()} DOCS (${url}) ===\n`);
  console.log(output);
  if (text.length > 4000) {
    console.log(`\n[...truncated — ${text.length - 4000} more chars. Open ${url} for full content.]`);
  }
}

main().catch(e => { console.error(e.message); process.exit(1); });
