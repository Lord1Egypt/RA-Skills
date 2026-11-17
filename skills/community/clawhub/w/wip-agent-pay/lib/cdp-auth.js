// lib/cdp-auth.js
// Ed25519 JWT generation for Coinbase CDP Server Wallets v2.
// Uses Web Crypto API ... works in Cloudflare Workers and Node 20+.
//
// CDP requires two JWTs per request:
//   1. Bearer token (API auth) ... signed with API Key Secret
//   2. X-Wallet-Auth (wallet auth) ... signed with Wallet Secret
//
// Both use Ed25519 (EdDSA).

/**
 * Base64url encode a buffer.
 */
function base64url(buffer) {
  const bytes = new Uint8Array(buffer);
  let str = '';
  for (const b of bytes) str += String.fromCharCode(b);
  return btoa(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

/**
 * Import an Ed25519 private key from base64-encoded raw bytes.
 */
async function importEd25519Key(base64Secret) {
  const raw = Uint8Array.from(atob(base64Secret), c => c.charCodeAt(0));
  // Ed25519 PKCS8 wrapping: OID prefix + raw 32-byte key
  // PKCS8 header for Ed25519: 302e020100300506032b657004220420
  const pkcs8Prefix = new Uint8Array([
    0x30, 0x2e, 0x02, 0x01, 0x00, 0x30, 0x05, 0x06,
    0x03, 0x2b, 0x65, 0x70, 0x04, 0x22, 0x04, 0x20
  ]);
  const pkcs8 = new Uint8Array(pkcs8Prefix.length + raw.length);
  pkcs8.set(pkcs8Prefix);
  pkcs8.set(raw, pkcs8Prefix.length);

  return crypto.subtle.importKey(
    'pkcs8', pkcs8, { name: 'Ed25519' }, false, ['sign']
  );
}

/**
 * Sign a JWT payload with Ed25519.
 */
async function signJWT(payload, key) {
  const header = { alg: 'EdDSA', typ: 'JWT' };
  const enc = new TextEncoder();
  const headerB64 = base64url(enc.encode(JSON.stringify(header)));
  const payloadB64 = base64url(enc.encode(JSON.stringify(payload)));
  const signingInput = `${headerB64}.${payloadB64}`;
  const signature = await crypto.subtle.sign('Ed25519', key, enc.encode(signingInput));
  return `${signingInput}.${base64url(signature)}`;
}

/**
 * Generate the Bearer token (API auth JWT).
 *
 * @param {string} apiKeyId - CDP API Key ID
 * @param {string} apiKeySecret - CDP API Key Secret (base64 Ed25519)
 * @param {string} method - HTTP method (GET, POST, etc.)
 * @param {string} url - Full request URL
 */
export async function createBearerToken(apiKeyId, apiKeySecret, method, url) {
  const key = await importEd25519Key(apiKeySecret);
  const now = Math.floor(Date.now() / 1000);
  const parsed = new URL(url);
  const uri = `${method.toUpperCase()} ${parsed.host}${parsed.pathname}`;

  const payload = {
    sub: apiKeyId,
    iss: 'cdp',
    aud: ['cdp_service'],
    nbf: now,
    exp: now + 120,
    uris: [uri],
  };

  return signJWT(payload, key);
}

/**
 * Generate the X-Wallet-Auth JWT.
 *
 * @param {string} walletSecret - Wallet Secret (base64 Ed25519)
 * @param {string} method - HTTP method
 * @param {string} url - Full request URL
 * @param {string} body - Request body (JSON string) or empty
 */
export async function createWalletAuth(walletSecret, method, url, body = '') {
  const key = await importEd25519Key(walletSecret);
  const now = Math.floor(Date.now() / 1000);
  const parsed = new URL(url);
  const uri = `${method.toUpperCase()} ${parsed.host}${parsed.pathname}`;

  // SHA-256 hash of canonical request body
  const enc = new TextEncoder();
  const bodyHash = await crypto.subtle.digest('SHA-256', enc.encode(body));
  const reqHash = base64url(bodyHash);

  const jti = crypto.randomUUID();

  const payload = {
    iat: now,
    nbf: now,
    exp: now + 120,
    jti,
    uris: [uri],
    reqHash,
  };

  return signJWT(payload, key);
}

/**
 * Generate both auth headers for a CDP API request.
 *
 * @param {object} creds - { apiKeyId, apiKeySecret, walletSecret }
 * @param {string} method - HTTP method
 * @param {string} url - Full request URL
 * @param {string} body - Request body JSON string
 * @returns {{ authorization: string, walletAuth: string }}
 */
export async function createAuthHeaders(creds, method, url, body = '') {
  const [bearer, walletAuth] = await Promise.all([
    createBearerToken(creds.apiKeyId, creds.apiKeySecret, method, url),
    createWalletAuth(creds.walletSecret, method, url, body),
  ]);
  return {
    authorization: `Bearer ${bearer}`,
    walletAuth,
  };
}
