#!/usr/bin/env node
/**
 * fx-fetch.mjs — Fetch X/Twitter content via FxTwitter public API.
 * Usage: node fx-fetch.mjs <x-url> [--thread]
 * Output: JSON tweet object(s) to stdout.
 */
import https from 'https';

const API = 'https://api.fxtwitter.com';
const MAX_THREAD = 50;

const get = url => new Promise((resolve, reject) => {
  https.get(url, { headers: { 'User-Agent': 'x-reader/1.0' } }, res => {
    let d = ''; res.on('data', c => d += c);
    res.on('end', () => res.statusCode === 200
      ? resolve(JSON.parse(d))
      : reject(new Error(`${res.statusCode}: ${(() => { try { return JSON.parse(d).message; } catch { return d.slice(0, 100); } })()}`)));
  }).on('error', reject).setTimeout(15000, function() { this.destroy(); reject(new Error('timeout')); });
});

function parseUrl(url) {
  try {
    const u = new URL(url);
    if (!['x.com', 'twitter.com'].includes(u.hostname.replace('www.', ''))) return null;
    const m = u.pathname.match(/\/(?:([^/]+)\/)?status\/(\d+)/);
    return m ? { user: m[1] || '_', id: m[2] } : null;
  } catch { return null; }
}

async function fetchTweet(user, id) {
  const { tweet } = await get(`${API}/${user}/status/${id}`);
  return tweet;
}

async function fetchThread(user, id) {
  const tweets = [];
  let cur = { user, id };
  while (cur.id && tweets.length < MAX_THREAD) {
    const t = await fetchTweet(cur.user, cur.id);
    tweets.unshift(t);
    if (!t.replying_to_status || t.replying_to?.toLowerCase() !== t.author.screen_name.toLowerCase()) break;
    cur = { user: t.replying_to, id: t.replying_to_status };
  }
  return tweets;
}

const args = process.argv.slice(2);
const url = args.find(a => !a.startsWith('-'));
const parsed = url && parseUrl(url);
if (!parsed) { console.error('Usage: fx-fetch.mjs <x.com-url> [--thread]'); process.exit(1); }

try {
  const result = args.includes('--thread')
    ? await fetchThread(parsed.user, parsed.id)
    : [await fetchTweet(parsed.user, parsed.id)];
  console.log(JSON.stringify(result, null, 2));
} catch (e) { console.error(`Error: ${e.message}`); process.exit(1); }

