#!/usr/bin/env node

/**
 * X API v2 CLI Tool (OAuth 1.0a User Context)
 * Template: x-autopilot
 *
 * Uses Node.js built-in 'https' module (NOT fetch) to avoid ByteString errors
 * in Docker containers. Mirrors the proven x-growth working template.
 *
 * Usage:
 *   node x-api.js post "Tweet text"
 *   node x-api.js thread "Tweet 1" "Tweet 2" "Tweet 3"
 *   node x-api.js reply <id> "Reply text"
 *   node x-api.js quote <id> "Quote text"
 *   node x-api.js like <id>
 *   node x-api.js delete <id>
 *   node x-api.js timeline <count>
 *
 * Required env vars:
 *   X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
 */

'use strict';
const crypto = require('crypto');
const https = require('https');

// ── OAuth 1.0a Helpers ───────────────────────────────────────────────────────

function percentEncode(str) {
  return encodeURIComponent(String(str))
    .replace(/!/g, '%21')
    .replace(/'/g, '%27')
    .replace(/\(/g, '%28')
    .replace(/\)/g, '%29')
    .replace(/\*/g, '%2A');
}

function getCredentials() {
  const apiKey = process.env.X_API_KEY;
  const apiSecret = process.env.X_API_SECRET;
  const accessToken = process.env.X_ACCESS_TOKEN;
  const accessSecret = process.env.X_ACCESS_SECRET;

  if (!apiKey || !apiSecret || !accessToken || !accessSecret) {
    console.error('Error: Missing X API credentials.');
    console.error('Ensure X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET are set.');
    process.exit(1);
  }
  return { apiKey, apiSecret, accessToken, accessSecret };
}

function buildOAuthHeader(method, url, params, credentials) {
  const oauthParams = {
    oauth_consumer_key: credentials.apiKey,
    oauth_nonce: crypto.randomBytes(16).toString('hex'),
    oauth_signature_method: 'HMAC-SHA1',
    oauth_timestamp: Math.floor(Date.now() / 1000).toString(),
    oauth_token: credentials.accessToken,
    oauth_version: '1.0',
  };

  const allParams = { ...params, ...oauthParams };
  const sortedParams = Object.keys(allParams).sort().map(k =>
    `${percentEncode(k)}=${percentEncode(allParams[k])}`
  ).join('&');

  const baseString = [method.toUpperCase(), percentEncode(url), percentEncode(sortedParams)].join('&');
  const signingKey = `${percentEncode(credentials.apiSecret)}&${percentEncode(credentials.accessSecret)}`;
  const signature = crypto.createHmac('sha1', signingKey).update(baseString).digest('base64');

  oauthParams.oauth_signature = signature;

  const headerParts = Object.keys(oauthParams).sort().map(k =>
    `${percentEncode(k)}="${percentEncode(oauthParams[k])}"`
  ).join(', ');

  return `OAuth ${headerParts}`;
}

// ── Request Helper (uses https, NOT fetch, to avoid ByteString errors) ────────

function request(method, path, body, queryParams) {
  if (!queryParams) queryParams = {};
  return new Promise(function(resolve, reject) {
    const credentials = getCredentials();
    const urlObj = new URL('https://api.twitter.com/2' + path);
    Object.keys(queryParams).forEach(function(k) {
      urlObj.searchParams.append(k, queryParams[k]);
    });

    // Only query params go into OAuth base string (JSON body excluded per Twitter v2 spec)
    const oauthQueryParams = {};
    urlObj.searchParams.forEach(function(v, k) { oauthQueryParams[k] = v; });
    const authHeader = buildOAuthHeader(method, urlObj.origin + urlObj.pathname, oauthQueryParams, credentials);

    const options = {
      method: method,
      headers: {
        'Authorization': authHeader,
        'Content-Type': 'application/json',
        'User-Agent': 'ModelFitAI-Bot/1.0',
      },
    };

    const req = https.request(urlObj, options, function(res) {
      let data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        try {
          const json = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(json);
          } else {
            reject(new Error(json.detail || json.title || ('HTTP ' + res.statusCode)));
          }
        } catch (e) {
          reject(new Error('Invalid JSON: ' + data));
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ── Commands ──────────────────────────────────────────────────────────────────

async function post(text) {
  if (!text) throw new Error('Text required');
  const res = await request('POST', '/tweets', { text: text });
  const id = res.data.id;
  console.log(JSON.stringify({ success: true, id: id, url: 'https://x.com/i/web/status/' + id, text: res.data.text }));
}

async function thread(tweets) {
  if (!tweets || tweets.length < 2) throw new Error('Need at least 2 tweets for a thread');
  const postedIds = [];
  let replyToId = null;
  for (let i = 0; i < tweets.length; i++) {
    const body = replyToId ? { text: tweets[i], reply: { in_reply_to_tweet_id: replyToId } } : { text: tweets[i] };
    const res = await request('POST', '/tweets', body);
    replyToId = res.data.id;
    postedIds.push(replyToId);
    if (i < tweets.length - 1) await new Promise(function(r) { setTimeout(r, 1000); });
  }
  console.log(JSON.stringify({ success: true, ids: postedIds, url: 'https://x.com/i/web/status/' + postedIds[0], count: postedIds.length }));
}

async function reply(id, text) {
  if (!id || !text) throw new Error('ID and text required');
  const res = await request('POST', '/tweets', { text: text, reply: { in_reply_to_tweet_id: id } });
  const newId = res.data.id;
  console.log(JSON.stringify({ success: true, id: newId, url: 'https://x.com/i/web/status/' + newId, reply_to: id }));
}

async function quote(id, text) {
  if (!id || !text) throw new Error('ID and text required');
  const res = await request('POST', '/tweets', { text: text, quote_tweet_id: id });
  const newId = res.data.id;
  console.log(JSON.stringify({ success: true, id: newId, url: 'https://x.com/i/web/status/' + newId, quote_of: id }));
}

async function like(id) {
  if (!id) throw new Error('Tweet ID required');
  const me = await request('GET', '/users/me');
  const userId = me.data.id;
  await request('POST', '/users/' + userId + '/likes', { tweet_id: id });
  console.log(JSON.stringify({ success: true, liked: id }));
}

async function remove(id) {
  if (!id) throw new Error('ID required');
  await new Promise(function(resolve, reject) {
    const credentials = getCredentials();
    const urlObj = new URL('https://api.twitter.com/2/tweets/' + id);
    const authHeader = buildOAuthHeader('DELETE', urlObj.origin + urlObj.pathname, {}, credentials);
    const req = https.request(urlObj, {
      method: 'DELETE',
      headers: { 'Authorization': authHeader, 'User-Agent': 'ModelFitAI-Bot/1.0' }
    }, function(res) {
      let data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        if (res.statusCode >= 200 && res.statusCode < 300) resolve();
        else reject(new Error('Delete failed: HTTP ' + res.statusCode + ' - ' + data));
      });
    });
    req.on('error', reject);
    req.end();
  });
  console.log(JSON.stringify({ success: true, deleted: id }));
}

async function timeline(count) {
  if (!count) count = 10;
  const me = await request('GET', '/users/me');
  const userId = me.data.id;
  const res = await request('GET', '/users/' + userId + '/tweets', null, {
    max_results: String(Math.min(count, 100)),
    'tweet.fields': 'created_at,public_metrics',
  });
  const tweets = (res.data || []).map(function(t) {
    return {
      id: t.id,
      text: t.text.slice(0, 120) + (t.text.length > 120 ? '...' : ''),
      likes: (t.public_metrics && t.public_metrics.like_count) || 0,
      retweets: (t.public_metrics && t.public_metrics.retweet_count) || 0,
      replies: (t.public_metrics && t.public_metrics.reply_count) || 0,
      url: 'https://x.com/i/web/status/' + t.id,
      createdAt: t.created_at,
    };
  });
  console.log(JSON.stringify({ success: true, count: tweets.length, tweets: tweets }));
}

// ── Main ─────────────────────────────────────────────────────────────────────

const cmd = process.argv[2];
const args = process.argv.slice(3);

(async function() {
  try {
    if (cmd === 'post')          await post(args.join(' '));
    else if (cmd === 'thread')   await thread(args);
    else if (cmd === 'reply')    await reply(args[0], args.slice(1).join(' '));
    else if (cmd === 'quote')    await quote(args[0], args.slice(1).join(' '));
    else if (cmd === 'like')     await like(args[0]);
    else if (cmd === 'delete')   await remove(args[0]);
    else if (cmd === 'timeline') await timeline(parseInt(args[0]) || 10);
    else {
      console.log('Usage: node x-api.js <post|thread|reply|quote|like|delete|timeline> [args...]');
      process.exit(1);
    }
  } catch (err) {
    console.error(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  }
})();

