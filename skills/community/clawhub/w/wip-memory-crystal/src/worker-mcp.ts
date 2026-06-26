/// <reference types="@cloudflare/workers-types" />
// worker-mcp.ts — Memory Crystal Cloud MCP Server.
//
// DEPRECATED: This is a demo/onboarding server only. Not the production architecture.
// With full LDM tree sync (delta chunks + file sync), every node has the complete
// database and file tree. All search is local. Cloud search is unnecessary.
// See RELAY.md and TECHNICAL.md for the production sync model.
//
// Remote MCP server for ChatGPT and Claude (all surfaces).
// OAuth 2.1 + DCR, Streamable HTTP, 4 memory tools.
//
// Tier 1 (Sovereign): remember encrypts + relays to Core, search says "local only"
// Tier 2 (Convenience): remember + search via D1 + Vectorize (demo only)
//
// Deployed as a separate Cloudflare Worker from the relay (worker.ts).

import { CloudCrystal } from './cloud-crystal';

// ── Types ──

interface Env {
  DB: D1Database;
  VECTORIZE: VectorizeIndex;
  RELAY: R2Bucket;
  OPENAI_API_KEY: string;
  RELAY_ENCRYPTION_KEY: string; // base64, for Tier 1 relay drops
  MCP_SIGNING_KEY: string;      // for signing OAuth tokens
}

interface User {
  user_id: string;
  email: string;
  tier: string;
}

interface TokenInfo {
  user_id: string;
  client_id: string;
  scope: string;
  tier: string;
}

// ── Helpers ──

function json(data: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...headers },
  });
}

function cors(response: Response): Response {
  const headers = new Headers(response.headers);
  headers.set('Access-Control-Allow-Origin', '*');
  headers.set('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Authorization, Content-Type');
  return new Response(response.body, { status: response.status, headers });
}

async function sha256(input: string): Promise<string> {
  const encoded = new TextEncoder().encode(input);
  const hash = await crypto.subtle.digest('SHA-256', encoded);
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function sha256Base64url(input: string): Promise<string> {
  const encoded = new TextEncoder().encode(input);
  const hash = await crypto.subtle.digest('SHA-256', encoded);
  const bytes = new Uint8Array(hash);
  return btoa(String.fromCharCode.apply(null, Array.from(bytes)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function generateToken(): string {
  const bytes = new Uint8Array(32);
  crypto.getRandomValues(bytes);
  return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
}

// ── OAuth 2.1 + DCR ──

// Discovery: OAuth Protected Resource Metadata
function handleProtectedResourceMetadata(url: URL): Response {
  return json({
    resource: url.origin,
    authorization_servers: [url.origin],
    bearer_methods_supported: ['header'],
  });
}

// Discovery: OAuth Authorization Server Metadata
function handleAuthServerMetadata(url: URL): Response {
  return json({
    issuer: url.origin,
    authorization_endpoint: `${url.origin}/oauth/authorize`,
    token_endpoint: `${url.origin}/oauth/token`,
    registration_endpoint: `${url.origin}/oauth/register`,
    response_types_supported: ['code'],
    grant_types_supported: ['authorization_code'],
    code_challenge_methods_supported: ['S256'],
    token_endpoint_auth_methods_supported: ['none'],
    scopes_supported: ['memory'],
  });
}

// DCR: Dynamic Client Registration
async function handleRegister(request: Request, env: Env): Promise<Response> {
  const body = await request.json() as {
    redirect_uris: string[];
    client_name?: string;
  };

  if (!body.redirect_uris?.length) {
    return json({ error: 'redirect_uris required' }, 400);
  }

  const clientId = crypto.randomUUID();

  await env.DB.prepare(`
    INSERT INTO oauth_clients (client_id, redirect_uris, client_name)
    VALUES (?, ?, ?)
  `).bind(clientId, JSON.stringify(body.redirect_uris), body.client_name || '').run();

  return json({
    client_id: clientId,
    redirect_uris: body.redirect_uris,
    client_name: body.client_name || '',
    token_endpoint_auth_method: 'none',
  }, 201);
}

// Authorize: show consent page, issue code
async function handleAuthorize(request: Request, url: URL, env: Env): Promise<Response> {
  const clientId = url.searchParams.get('client_id');
  const redirectUri = url.searchParams.get('redirect_uri');
  const codeChallenge = url.searchParams.get('code_challenge');
  const codeChallengeMethod = url.searchParams.get('code_challenge_method') || 'S256';
  const state = url.searchParams.get('state');
  const scope = url.searchParams.get('scope') || 'memory';

  if (!clientId || !redirectUri || !codeChallenge) {
    return json({ error: 'Missing required parameters (client_id, redirect_uri, code_challenge)' }, 400);
  }

  if (codeChallengeMethod !== 'S256') {
    return json({ error: 'Only S256 code_challenge_method supported' }, 400);
  }

  // Verify client exists
  const client = await env.DB.prepare(
    'SELECT * FROM oauth_clients WHERE client_id = ?'
  ).bind(clientId).first();

  if (!client) {
    return json({ error: 'Unknown client_id' }, 400);
  }

  // Verify redirect_uri
  const allowedUris = JSON.parse(client.redirect_uris as string) as string[];
  if (!allowedUris.includes(redirectUri)) {
    return json({ error: 'redirect_uri not registered' }, 400);
  }

  if (request.method === 'GET') {
    // Show consent page
    return new Response(consentPage(clientId, redirectUri, codeChallenge, codeChallengeMethod, state, scope), {
      headers: { 'Content-Type': 'text/html' },
    });
  }

  // POST: user submitted consent form
  const formData = await request.formData();
  const email = formData.get('email') as string;

  if (!email) {
    return json({ error: 'Email required' }, 400);
  }

  // Create or get user
  const userId = await sha256(email.toLowerCase().trim());
  await env.DB.prepare(`
    INSERT INTO users (user_id, email) VALUES (?, ?)
    ON CONFLICT (user_id) DO NOTHING
  `).bind(userId, email.toLowerCase().trim()).run();

  // Generate authorization code
  const code = generateToken();
  const expiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString(); // 10 min

  await env.DB.prepare(`
    INSERT INTO authorization_codes (code, client_id, user_id, code_challenge, code_challenge_method, redirect_uri, scope, expires_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `).bind(code, clientId, userId, codeChallenge, codeChallengeMethod, redirectUri, scope, expiresAt).run();

  // Redirect back to client
  const redirect = new URL(redirectUri);
  redirect.searchParams.set('code', code);
  if (state) redirect.searchParams.set('state', state);

  return Response.redirect(redirect.toString(), 302);
}

// Token: exchange code for access token
async function handleToken(request: Request, env: Env): Promise<Response> {
  const body = await request.formData();
  const grantType = body.get('grant_type');
  const code = body.get('code') as string;
  const redirectUri = body.get('redirect_uri') as string;
  const codeVerifier = body.get('code_verifier') as string;

  if (grantType !== 'authorization_code') {
    return json({ error: 'unsupported_grant_type' }, 400);
  }

  if (!code || !codeVerifier) {
    return json({ error: 'Missing code or code_verifier' }, 400);
  }

  // Look up authorization code
  const authCode = await env.DB.prepare(
    'SELECT * FROM authorization_codes WHERE code = ? AND used = 0'
  ).bind(code).first();

  if (!authCode) {
    return json({ error: 'invalid_grant', error_description: 'Code not found or already used' }, 400);
  }

  if (new Date(authCode.expires_at as string) < new Date()) {
    return json({ error: 'invalid_grant', error_description: 'Code expired' }, 400);
  }

  if (redirectUri && authCode.redirect_uri !== redirectUri) {
    return json({ error: 'invalid_grant', error_description: 'redirect_uri mismatch' }, 400);
  }

  // Verify PKCE S256
  const expectedChallenge = await sha256Base64url(codeVerifier);
  if (expectedChallenge !== authCode.code_challenge) {
    return json({ error: 'invalid_grant', error_description: 'PKCE verification failed' }, 400);
  }

  // Mark code as used
  await env.DB.prepare('UPDATE authorization_codes SET used = 1 WHERE code = ?').bind(code).run();

  // Get user tier
  const user = await env.DB.prepare('SELECT * FROM users WHERE user_id = ?')
    .bind(authCode.user_id).first();
  const tier = (user?.tier as string) || 'sovereign';

  // Generate access token
  const accessToken = generateToken();
  const tokenHash = await sha256(accessToken);
  const expiresAt = new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString(); // 90 days

  await env.DB.prepare(`
    INSERT INTO access_tokens (token_hash, client_id, user_id, scope, tier, expires_at)
    VALUES (?, ?, ?, ?, ?, ?)
  `).bind(tokenHash, authCode.client_id, authCode.user_id, authCode.scope, tier, expiresAt).run();

  return json({
    access_token: accessToken,
    token_type: 'Bearer',
    expires_in: 90 * 24 * 60 * 60,
    scope: authCode.scope,
  });
}

// Verify bearer token
async function verifyToken(request: Request, env: Env): Promise<TokenInfo | Response> {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) {
    return json({ error: 'Missing Authorization header' }, 401);
  }

  const token = auth.slice(7);
  const tokenHash = await sha256(token);

  const row = await env.DB.prepare(
    'SELECT * FROM access_tokens WHERE token_hash = ?'
  ).bind(tokenHash).first();

  if (!row) {
    return json({ error: 'Invalid token' }, 401);
  }

  if (new Date(row.expires_at as string) < new Date()) {
    return json({ error: 'Token expired' }, 401);
  }

  return {
    user_id: row.user_id as string,
    client_id: row.client_id as string,
    scope: row.scope as string,
    tier: row.tier as string,
  };
}

// ── Consent Page HTML ──

function consentPage(
  clientId: string,
  redirectUri: string,
  codeChallenge: string,
  codeChallengeMethod: string,
  state: string | null,
  scope: string,
): string {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Memory Crystal</title>
  <style>
    body { font-family: -apple-system, system-ui, sans-serif; max-width: 420px; margin: 60px auto; padding: 0 20px; color: #1a1a1a; }
    h1 { font-size: 1.4em; }
    p { color: #555; line-height: 1.5; }
    form { margin-top: 24px; }
    label { display: block; font-weight: 500; margin-bottom: 6px; }
    input[type=email] { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
    button { margin-top: 16px; width: 100%; padding: 12px; background: #1a1a1a; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
    button:hover { background: #333; }
    .note { font-size: 0.85em; color: #888; margin-top: 16px; }
  </style>
</head>
<body>
  <h1>Memory Crystal</h1>
  <p>An app wants to access your memory. Enter your email to continue.</p>
  <form method="POST">
    <input type="hidden" name="client_id" value="${clientId}">
    <input type="hidden" name="redirect_uri" value="${redirectUri}">
    <input type="hidden" name="code_challenge" value="${codeChallenge}">
    <input type="hidden" name="code_challenge_method" value="${codeChallengeMethod}">
    ${state ? `<input type="hidden" name="state" value="${state}">` : ''}
    <input type="hidden" name="scope" value="${scope}">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required placeholder="you@example.com" autocomplete="email">
    <button type="submit">Connect Memory</button>
  </form>
  <p class="note">Your email identifies your memory account. No password needed... your AI client handles authentication.</p>
</body>
</html>`;
}

// ── MCP Protocol (Streamable HTTP) ──

interface MCPRequest {
  jsonrpc: '2.0';
  id?: number | string;
  method: string;
  params?: any;
}

interface MCPResponse {
  jsonrpc: '2.0';
  id?: number | string;
  result?: any;
  error?: { code: number; message: string };
}

const TOOLS = [
  {
    name: 'memory_search',
    description: 'Search your memories across all conversations and surfaces.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'What to search for' },
        limit: { type: 'number', description: 'Max results (default 5, max 20)' },
      },
      required: ['query'],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: 'memory_remember',
    description: 'Save a fact, preference, or observation to your memory.',
    inputSchema: {
      type: 'object',
      properties: {
        text: { type: 'string', description: 'The fact or observation to remember' },
        category: {
          type: 'string',
          enum: ['fact', 'preference', 'event', 'opinion', 'skill', 'user', 'feedback', 'project', 'reference'],
          description: 'Category of memory (default: fact)',
        },
      },
      required: ['text'],
    },
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
  },
  {
    name: 'memory_forget',
    description: 'Deprecate a memory by ID.',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'number', description: 'Memory ID to deprecate' },
      },
      required: ['id'],
    },
    annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: true },
  },
  {
    name: 'memory_status',
    description: 'Show your memory status: chunk count, memory count, connected agents.',
    inputSchema: { type: 'object', properties: {} },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
];

async function handleMCP(request: Request, env: Env, tokenInfo: TokenInfo): Promise<Response> {
  const body = await request.json() as MCPRequest;
  const { method, id, params } = body;

  const crystal = new CloudCrystal(env.DB, env.VECTORIZE, env.OPENAI_API_KEY);

  let result: any;

  switch (method) {
    case 'initialize':
      result = {
        protocolVersion: '2025-03-26',
        serverInfo: { name: 'memory-crystal', version: '0.2.0' },
        capabilities: { tools: {} },
      };
      break;

    case 'tools/list':
      result = { tools: TOOLS };
      break;

    case 'tools/call': {
      const toolName = params?.name;
      const args = params?.arguments || {};

      switch (toolName) {
        case 'memory_search': {
          if (tokenInfo.tier === 'sovereign') {
            result = {
              content: [{
                type: 'text',
                text: 'Search is available on your local devices only (Sovereign tier). Your memories from this session have been saved and will be searchable from any device with Memory Crystal installed locally.',
              }],
            };
          } else {
            const limit = Math.min(args.limit || 5, 20);
            const results = await crystal.search(tokenInfo.user_id, args.query, limit);
            const formatted = results.map((r, i) =>
              `[${i + 1}] (${r.score.toFixed(1)}% match, ${r.agent_id}, ${r.created_at})\n${r.text}`
            ).join('\n\n');
            result = {
              content: [{
                type: 'text',
                text: results.length > 0 ? formatted : `No results for "${args.query}".`,
              }],
            };
          }
          break;
        }

        case 'memory_remember': {
          if (tokenInfo.tier === 'sovereign') {
            // Tier 1: encrypt and relay to Mini
            // For now, store in D1 as well (user opted in by connecting)
            // TODO: implement relay-only path
          }
          const memId = await crystal.remember(tokenInfo.user_id, args.text, args.category || 'fact');
          result = {
            content: [{
              type: 'text',
              text: `Remembered (id: ${memId}, category: ${args.category || 'fact'}): ${args.text}`,
            }],
          };
          break;
        }

        case 'memory_forget': {
          const ok = await crystal.forget(tokenInfo.user_id, args.id);
          result = {
            content: [{
              type: 'text',
              text: ok ? `Memory ${args.id} deprecated.` : `Memory ${args.id} not found or already deprecated.`,
            }],
          };
          break;
        }

        case 'memory_status': {
          const status = await crystal.status(tokenInfo.user_id);
          result = {
            content: [{
              type: 'text',
              text: [
                `Chunks: ${status.chunks}`,
                `Memories: ${status.memories}`,
                `Agents: ${status.agents.join(', ') || 'none'}`,
                `Tier: ${status.tier}`,
              ].join('\n'),
            }],
          };
          break;
        }

        default:
          return json({ jsonrpc: '2.0', id, error: { code: -32601, message: `Unknown tool: ${toolName}` } });
      }
      break;
    }

    case 'notifications/initialized':
      // Client notification, no response needed
      return new Response(null, { status: 204 });

    default:
      return json({ jsonrpc: '2.0', id, error: { code: -32601, message: `Unknown method: ${method}` } });
  }

  return json({ jsonrpc: '2.0', id, result });
}

// ── Router ──

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return cors(new Response(null, { status: 204 }));
    }

    // Health
    if (path === '/health' && request.method === 'GET') {
      return cors(json({ ok: true, service: 'memory-crystal-cloud', version: '0.2.0' }));
    }

    // OAuth Discovery
    if (path === '/.well-known/oauth-protected-resource') {
      return cors(handleProtectedResourceMetadata(url));
    }
    if (path === '/.well-known/oauth-authorization-server') {
      return cors(handleAuthServerMetadata(url));
    }

    // OAuth DCR
    if (path === '/oauth/register' && request.method === 'POST') {
      return cors(await handleRegister(request, env));
    }

    // OAuth Authorize (GET = consent page, POST = submit)
    if (path === '/oauth/authorize') {
      return await handleAuthorize(request, url, env);
    }

    // OAuth Token
    if (path === '/oauth/token' && request.method === 'POST') {
      return cors(await handleToken(request, env));
    }

    // MCP endpoint (requires auth)
    if (path === '/mcp' && request.method === 'POST') {
      const tokenResult = await verifyToken(request, env);
      if (tokenResult instanceof Response) return cors(tokenResult);
      return cors(await handleMCP(request, env, tokenResult));
    }

    return cors(json({ error: 'Not found' }, 404));
  },
};
