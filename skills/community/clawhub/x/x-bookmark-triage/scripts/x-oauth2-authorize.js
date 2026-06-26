#!/usr/bin/env node
/**
 * x-oauth2-authorize.js
 * 
 * Interactive X OAuth 2.0 authorization flow with PKCE.
 * Sets up a local HTTP server to capture the callback, exchanges code for tokens,
 * and saves refresh_token + access_token to data/x-oauth2-token-cache.json.
 * 
 * Requires env vars:
 *   X_OAUTH2_CLIENT_ID
 *   X_OAUTH2_CLIENT_SECRET
 * 
 * Usage:
 *   node scripts/x-oauth2-authorize.js
 * 
 * Then set the refresh token from the output in your plist or env var.
 */

const http = require('http');
const https = require('https');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const { URL, URLSearchParams } = require('url');

const CLIENT_ID = process.env.X_OAUTH2_CLIENT_ID;
const CLIENT_SECRET = process.env.X_OAUTH2_CLIENT_SECRET;

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error('Error: Missing X_OAUTH2_CLIENT_ID or X_OAUTH2_CLIENT_SECRET');
  console.error('Set these env vars and try again.');
  process.exit(1);
}

const CALLBACK_PORT = 3456;
const CALLBACK_URL = `http://localhost:${CALLBACK_PORT}/callback`;
const STATE = crypto.randomBytes(16).toString('hex');
const SCOPES = ['bookmark.read', 'bookmark.write', 'tweet.read', 'users.read'];

// PKCE code challenge
const codeVerifier = crypto.randomBytes(32).toString('base64url');
const codeChallenge = crypto.createHash('sha256').update(codeVerifier).digest('base64url');

// Build auth URL
const authUrl = new URL('https://twitter.com/i/oauth2/authorize');
authUrl.searchParams.append('response_type', 'code');
authUrl.searchParams.append('client_id', CLIENT_ID);
authUrl.searchParams.append('redirect_uri', CALLBACK_URL);
authUrl.searchParams.append('scope', SCOPES.join(' '));
authUrl.searchParams.append('state', STATE);
authUrl.searchParams.append('code_challenge', codeChallenge);
authUrl.searchParams.append('code_challenge_method', 'S256');

console.log('\n═══ X OAuth 2.0 Authorization ═══\n');
console.log('Opening browser for authorization...\n');
console.log('If the browser doesn\'t open, visit this URL manually:\n');
console.log(authUrl.toString());
console.log('\n');

// Open browser (best-effort)
const open = require('child_process').spawn;
try {
  open('open', [authUrl.toString()]);
} catch (e) {
  // Fail silently if no browser
}

// Start callback server
let authCode;
let receivedState;
const server = http.createServer((req, res) => {
  const callbackUrl = new URL('http://localhost' + req.url);
  
  authCode = callbackUrl.searchParams.get('code');
  receivedState = callbackUrl.searchParams.get('state');
  
  if (authCode && receivedState === STATE) {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`<html><body>
      <h1>✅ Authorization Successful</h1>
      <p>You can close this window and return to the terminal.</p>
    </body></html>`);
    server.close(() => exchangeCode());
  } else {
    res.writeHead(400);
    res.end('Authorization failed or state mismatch');
    server.close(() => process.exit(1));
  }
});

server.listen(CALLBACK_PORT, () => {
  console.log(`Waiting for authorization callback on port ${CALLBACK_PORT}...`);
});

function exchangeCode() {
  const tokenUrl = 'https://api.x.com/2/oauth2/token';
  const params = new URLSearchParams({
    grant_type: 'authorization_code',
    code: authCode,
    redirect_uri: CALLBACK_URL,
    code_verifier: codeVerifier,
    client_id: CLIENT_ID
  });

  const body = params.toString();
  const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64');

  const req = https.request(tokenUrl, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(body)
    }
  }, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
      try {
        const tokens = JSON.parse(data);
        
        if (tokens.error) {
          console.error('Token exchange failed:', tokens.error_description);
          process.exit(1);
        }

        if (!tokens.refresh_token) {
          console.error('No refresh_token in response. Check scopes.');
          process.exit(1);
        }

        // Save tokens
        const dataDir = path.join(__dirname, '..', 'data');
        fs.mkdirSync(dataDir, { recursive: true });
        
        const cacheFile = path.join(dataDir, 'x-oauth2-token-cache.json');
        fs.writeFileSync(cacheFile, JSON.stringify({
          access_token: tokens.access_token,
          refresh_token: tokens.refresh_token,
          token_type: tokens.token_type,
          expires_in: tokens.expires_in,
          cached_at: Date.now()
        }, null, 2), { mode: 0o600 });

        console.log('\n✅ Authorization successful!\n');
        console.log('Tokens saved to: data/x-oauth2-token-cache.json');
        console.log('\nNext step: Set X_OAUTH2_REFRESH_TOKEN in your environment:\n');
        console.log('  cat data/x-oauth2-token-cache.json | node -e "const d=require(\'fs\').readFileSync(\'/dev/stdin\',\'utf8\'); console.log(JSON.parse(d).refresh_token)"');
        console.log('\n⚠️  Never paste tokens into console commands or share terminal output.');
        console.log('');
        process.exit(0);
      } catch (e) {
        console.error('Failed to parse token response:', e.message);
        process.exit(1);
      }
    });
  });

  req.on('error', (e) => {
    console.error('Token exchange error:', e.message);
    process.exit(1);
  });

  req.write(body);
  req.end();
}
