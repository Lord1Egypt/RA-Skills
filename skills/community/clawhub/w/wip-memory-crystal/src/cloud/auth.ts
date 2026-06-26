// memory-crystal/cloud/auth.ts — OAuth 2.1 server with Dynamic Client Registration.
// Co-located in the same Worker. Handles DCR, authorization, token exchange.
// PKCE S256 required. No refresh tokens for v1.

import type { Env, OAuthClient, TokenRow, UserRow } from './types.js';

// ── Helpers ──

function json(data: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...headers },
  });
}

function html(body: string, status = 200): Response {
  return new Response(body, {
    status,
    headers: { 'Content-Type': 'text/html; charset=utf-8' },
  });
}

async function sha256(input: string): Promise<string> {
  const encoded = new TextEncoder().encode(input);
  const hash = await crypto.subtle.digest('SHA-256', encoded);
  return [...new Uint8Array(hash)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function sha256Base64url(input: string): Promise<string> {
  const encoded = new TextEncoder().encode(input);
  const hash = await crypto.subtle.digest('SHA-256', encoded);
  const bytes = new Uint8Array(hash);
  let binary = '';
  for (const b of bytes) binary += String.fromCharCode(b);
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function generateToken(): string {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return [...bytes].map(b => b.toString(16).padStart(2, '0')).join('');
}

function generateCode(): string {
  const bytes = crypto.getRandomValues(new Uint8Array(24));
  return [...bytes].map(b => b.toString(16).padStart(2, '0')).join('');
}

// ── Allowed Redirect URIs ──

const ALLOWED_REDIRECTS = [
  'https://chatgpt.com/connector_platform_oauth_redirect',
  'https://platform.openai.com/apps-manage/oauth',
  // Claude connector redirects (add as discovered)
];

function isAllowedRedirect(uri: string): boolean {
  // Allow registered redirects + localhost for dev
  if (ALLOWED_REDIRECTS.includes(uri)) return true;
  if (uri.startsWith('http://localhost:') || uri.startsWith('http://127.0.0.1:')) return true;
  return false;
}

// ── Discovery Endpoints ──

export function handleProtectedResource(serverUrl: string): Response {
  return json({
    resource: serverUrl,
    authorization_servers: [serverUrl],
    scopes_supported: ['memory:read', 'memory:write'],
    resource_documentation: 'https://github.com/wipcomputer/memory-crystal',
  });
}

export function handleAuthServerMetadata(serverUrl: string): Response {
  return json({
    issuer: serverUrl,
    authorization_endpoint: `${serverUrl}/oauth/authorize`,
    token_endpoint: `${serverUrl}/oauth/token`,
    registration_endpoint: `${serverUrl}/oauth/register`,
    code_challenge_methods_supported: ['S256'],
    response_types_supported: ['code'],
    grant_types_supported: ['authorization_code'],
    token_endpoint_auth_methods_supported: ['none'],
    scopes_supported: ['memory:read', 'memory:write'],
  });
}

// ── Dynamic Client Registration ──

export async function handleRegister(request: Request, env: Env): Promise<Response> {
  let body: any;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'invalid_request', error_description: 'Invalid JSON body' }, 400);
  }

  const redirectUris = body.redirect_uris;
  if (!Array.isArray(redirectUris) || redirectUris.length === 0) {
    return json({ error: 'invalid_request', error_description: 'redirect_uris required' }, 400);
  }

  // Validate redirect URIs
  for (const uri of redirectUris) {
    if (!isAllowedRedirect(uri)) {
      return json({ error: 'invalid_request', error_description: `Redirect URI not allowed: ${uri}` }, 400);
    }
  }

  const clientId = `mc_${crypto.randomUUID().replace(/-/g, '')}`;
  const now = new Date().toISOString();

  await env.DB.prepare(
    'INSERT INTO oauth_clients (client_id, redirect_uris, client_name, created_at) VALUES (?, ?, ?, ?)'
  ).bind(clientId, JSON.stringify(redirectUris), body.client_name || null, now).run();

  return json({
    client_id: clientId,
    redirect_uris: redirectUris,
    client_name: body.client_name || null,
    token_endpoint_auth_method: 'none',
  }, 201);
}

// ── Authorization Endpoint ──

export async function handleAuthorize(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const clientId = url.searchParams.get('client_id');
  const redirectUri = url.searchParams.get('redirect_uri');
  const responseType = url.searchParams.get('response_type');
  const codeChallenge = url.searchParams.get('code_challenge');
  const codeChallengeMethod = url.searchParams.get('code_challenge_method');
  const state = url.searchParams.get('state');
  const scope = url.searchParams.get('scope') || 'memory:read memory:write';

  // Validate required params
  if (!clientId || !redirectUri || responseType !== 'code' || !codeChallenge || codeChallengeMethod !== 'S256') {
    return html(errorPage('Missing or invalid authorization parameters. Ensure client_id, redirect_uri, response_type=code, code_challenge, and code_challenge_method=S256 are provided.'), 400);
  }

  // Verify client exists
  const client = await env.DB.prepare('SELECT * FROM oauth_clients WHERE client_id = ?').bind(clientId).first<OAuthClient>();
  if (!client) {
    return html(errorPage('Unknown client. Register first via /oauth/register.'), 400);
  }

  // Verify redirect URI is registered for this client
  const registeredUris: string[] = JSON.parse(client.redirect_uris);
  if (!registeredUris.includes(redirectUri)) {
    return html(errorPage('Redirect URI does not match registered URIs for this client.'), 400);
  }

  // Show consent page (GET) or process consent (POST)
  if (request.method === 'GET') {
    return html(consentPage(clientId, redirectUri, codeChallenge, codeChallengeMethod, state, scope));
  }

  // POST: process the consent form
  const formData = await request.formData();
  const email = formData.get('email') as string;
  const action = formData.get('action') as string;

  if (action !== 'approve' || !email) {
    // User denied or no email
    const params = new URLSearchParams({ error: 'access_denied' });
    if (state) params.set('state', state);
    return Response.redirect(`${redirectUri}?${params}`, 302);
  }

  // Find or create user
  const userId = await sha256(email.toLowerCase().trim());
  const now = new Date().toISOString();

  const existing = await env.DB.prepare('SELECT * FROM users WHERE user_id = ?').bind(userId).first<UserRow>();
  if (!existing) {
    await env.DB.prepare(
      'INSERT INTO users (user_id, email, tier, created_at) VALUES (?, ?, ?, ?)'
    ).bind(userId, email.toLowerCase().trim(), 'sovereign', now).run();
  }

  // Generate authorization code
  const code = generateCode();
  const expiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString(); // 10 min

  await env.DB.prepare(
    'INSERT INTO authorization_codes (code, client_id, user_id, code_challenge, code_challenge_method, redirect_uri, scope, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
  ).bind(code, clientId, userId, codeChallenge, codeChallengeMethod, redirectUri, scope, expiresAt).run();

  // Update client last_used_at
  await env.DB.prepare('UPDATE oauth_clients SET last_used_at = ? WHERE client_id = ?').bind(now, clientId).run();

  // Redirect back with code
  const params = new URLSearchParams({ code });
  if (state) params.set('state', state);
  return Response.redirect(`${redirectUri}?${params}`, 302);
}

// ── Token Endpoint ──

export async function handleToken(request: Request, env: Env): Promise<Response> {
  let body: URLSearchParams;
  try {
    const text = await request.text();
    body = new URLSearchParams(text);
  } catch {
    return json({ error: 'invalid_request' }, 400);
  }

  const grantType = body.get('grant_type');
  if (grantType !== 'authorization_code') {
    return json({ error: 'unsupported_grant_type' }, 400);
  }

  const code = body.get('code');
  const redirectUri = body.get('redirect_uri');
  const codeVerifier = body.get('code_verifier');
  const clientId = body.get('client_id');

  if (!code || !redirectUri || !codeVerifier || !clientId) {
    return json({ error: 'invalid_request', error_description: 'Missing required parameters' }, 400);
  }

  // Look up the authorization code
  const authCode = await env.DB.prepare(
    'SELECT * FROM authorization_codes WHERE code = ? AND used = 0'
  ).bind(code).first<any>();

  if (!authCode) {
    return json({ error: 'invalid_grant', error_description: 'Code not found or already used' }, 400);
  }

  // Check expiration
  if (new Date(authCode.expires_at) < new Date()) {
    return json({ error: 'invalid_grant', error_description: 'Code expired' }, 400);
  }

  // Verify client_id matches
  if (authCode.client_id !== clientId) {
    return json({ error: 'invalid_grant', error_description: 'Client mismatch' }, 400);
  }

  // Verify redirect_uri matches
  if (authCode.redirect_uri !== redirectUri) {
    return json({ error: 'invalid_grant', error_description: 'Redirect URI mismatch' }, 400);
  }

  // Verify PKCE: S256(code_verifier) must equal code_challenge
  const computedChallenge = await sha256Base64url(codeVerifier);
  if (computedChallenge !== authCode.code_challenge) {
    return json({ error: 'invalid_grant', error_description: 'PKCE verification failed' }, 400);
  }

  // Mark code as used
  await env.DB.prepare('UPDATE authorization_codes SET used = 1 WHERE code = ?').bind(code).run();

  // Get user tier
  const user = await env.DB.prepare('SELECT * FROM users WHERE user_id = ?').bind(authCode.user_id).first<UserRow>();
  const tier = user?.tier || 'sovereign';

  // Generate access token
  const accessToken = generateToken();
  const tokenHash = await sha256(accessToken);
  const now = new Date().toISOString();
  const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(); // 24h

  await env.DB.prepare(
    'INSERT INTO access_tokens (token_hash, client_id, user_id, scope, tier, expires_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
  ).bind(tokenHash, clientId, authCode.user_id, authCode.scope, tier, expiresAt, now).run();

  return json({
    access_token: accessToken,
    token_type: 'Bearer',
    expires_in: 86400,
    scope: authCode.scope,
  });
}

// ── Token Validation ──

export async function validateToken(request: Request, env: Env): Promise<{ userId: string; tier: string } | null> {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) return null;

  const token = auth.slice(7);
  const tokenHash = await sha256(token);

  const row = await env.DB.prepare(
    'SELECT * FROM access_tokens WHERE token_hash = ?'
  ).bind(tokenHash).first<TokenRow>();

  if (!row) return null;
  if (new Date(row.expires_at) < new Date()) return null;

  return { userId: row.user_id, tier: row.tier };
}

// ── HTML Pages ──

function consentPage(
  clientId: string,
  redirectUri: string,
  codeChallenge: string,
  codeChallengeMethod: string,
  state: string | null,
  scope: string
): string {
  // Build the form action URL with all OAuth params so POST goes to the same endpoint
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: 'code',
    code_challenge: codeChallenge,
    code_challenge_method: codeChallengeMethod,
    scope,
  });
  if (state) params.set('state', state);

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Memory Crystal</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
    .card { background: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 2rem; max-width: 400px; width: 90%; }
    h1 { font-size: 1.5rem; margin-bottom: 0.5rem; color: #fff; }
    .subtitle { color: #888; margin-bottom: 1.5rem; font-size: 0.9rem; }
    .scope { background: #222; border: 1px solid #333; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem; }
    .scope-item { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }
    .scope-item:last-child { margin-bottom: 0; }
    .scope-icon { color: #4ade80; }
    label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; color: #aaa; }
    input[type="email"] { width: 100%; padding: 0.75rem; background: #222; border: 1px solid #444; border-radius: 8px; color: #fff; font-size: 1rem; margin-bottom: 1rem; }
    input[type="email"]:focus { outline: none; border-color: #6366f1; }
    .buttons { display: flex; gap: 0.75rem; }
    button { flex: 1; padding: 0.75rem; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; font-weight: 500; }
    .approve { background: #6366f1; color: #fff; }
    .approve:hover { background: #5558e6; }
    .deny { background: #333; color: #aaa; }
    .deny:hover { background: #444; }
    .footer { margin-top: 1rem; font-size: 0.75rem; color: #666; text-align: center; }
    .footer a { color: #888; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Memory Crystal</h1>
    <p class="subtitle">Persistent memory for your AI conversations</p>

    <div class="scope">
      <div class="scope-item"><span class="scope-icon">&#10003;</span> Store memories you ask it to remember</div>
      <div class="scope-item"><span class="scope-icon">&#10003;</span> Search your stored memories</div>
      <div class="scope-item"><span class="scope-icon">&#10003;</span> Deprecate memories you want to forget</div>
    </div>

    <form method="POST" action="/oauth/authorize?${params.toString()}">
      <label for="email">Your email (creates your account)</label>
      <input type="email" id="email" name="email" required placeholder="you@example.com" autocomplete="email">

      <div class="buttons">
        <button type="submit" name="action" value="approve" class="approve">Connect</button>
        <button type="submit" name="action" value="deny" class="deny">Cancel</button>
      </div>
    </form>

    <p class="footer">
      By connecting, you agree to the <a href="/docs/privacy">Privacy Policy</a>.<br>
      Your memories are encrypted in transit. <a href="/docs/security">Learn more</a>.
    </p>
  </div>
</body>
</html>`;
}

function errorPage(message: string): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Memory Crystal - Error</title>
  <style>
    body { font-family: -apple-system, sans-serif; background: #0a0a0a; color: #e0e0e0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
    .card { background: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 2rem; max-width: 400px; }
    h1 { color: #ef4444; margin-bottom: 1rem; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Error</h1>
    <p>${message}</p>
  </div>
</body>
</html>`;
}
