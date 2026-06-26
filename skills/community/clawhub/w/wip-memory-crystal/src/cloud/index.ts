// memory-crystal/cloud/index.ts ... Cloudflare Worker entry point.
// Routes: OAuth discovery, auth flows, MCP endpoint, health check.
// MCP uses JSON-RPC over Streamable HTTP (no external MCP SDK dependency for Workers).
// Six tools: memory_search, memory_remember, memory_forget, memory_status, memory_log, memory_upload.

import type { Env } from './types.js';
import {
  handleProtectedResource,
  handleAuthServerMetadata,
  handleRegister,
  handleAuthorize,
  handleToken,
  validateToken,
} from './auth.js';
import { TOOLS, handleToolCall } from './mcp.js';

// ── Helpers ──

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function getServerUrl(request: Request): string {
  const url = new URL(request.url);
  return `${url.protocol}//${url.host}`;
}

// ── MCP JSON-RPC Handler ──
// Implements the minimal subset of MCP over Streamable HTTP:
// - tools/list: returns tool definitions
// - tools/call: executes a tool
// - initialize: handshake (returns server info)

interface JsonRpcRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: Record<string, unknown>;
}

interface JsonRpcResponse {
  jsonrpc: '2.0';
  id: string | number;
  result?: unknown;
  error?: { code: number; message: string };
}

async function handleMcpRequest(
  rpcRequest: JsonRpcRequest,
  userId: string,
  tier: string,
  env: Env
): Promise<JsonRpcResponse> {
  const { id, method, params } = rpcRequest;

  switch (method) {
    case 'initialize': {
      return {
        jsonrpc: '2.0',
        id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: {
            name: env.MCP_SERVER_NAME || 'memory-crystal',
            version: env.MCP_SERVER_VERSION || '0.1.0',
          },
        },
      };
    }

    case 'notifications/initialized': {
      // Client acknowledgment, no response needed for notifications
      // But since we're in request/response mode, return empty result
      return { jsonrpc: '2.0', id, result: {} };
    }

    case 'tools/list': {
      return { jsonrpc: '2.0', id, result: { tools: TOOLS } };
    }

    case 'tools/call': {
      const toolName = params?.name as string;
      const toolArgs = (params?.arguments || {}) as Record<string, unknown>;

      if (!toolName) {
        return {
          jsonrpc: '2.0',
          id,
          error: { code: -32602, message: 'Tool name required in params.name' },
        };
      }

      // Detect agent ID from tool call context
      // ChatGPT and Claude don't send agent metadata, so we infer from headers later
      const agentId = 'gpt-web'; // Default; could be refined with request headers

      const result = await handleToolCall(toolName, toolArgs, {
        userId,
        tier,
        env,
        agentId,
      });

      return { jsonrpc: '2.0', id, result };
    }

    default: {
      return {
        jsonrpc: '2.0',
        id,
        error: { code: -32601, message: `Method not found: ${method}` },
      };
    }
  }
}

// ── Main Router ──

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;

    // ── CORS preflight ──
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    const serverUrl = getServerUrl(request);

    try {
      // ── Health Check ──
      if (path === '/health' && request.method === 'GET') {
        return json({ ok: true, service: 'memory-crystal-cloud', version: '0.1.0' });
      }

      // ── OAuth Discovery ──
      if (path === '/.well-known/oauth-protected-resource') {
        return handleProtectedResource(serverUrl);
      }
      if (path === '/.well-known/oauth-authorization-server' || path === '/.well-known/openid-configuration') {
        return handleAuthServerMetadata(serverUrl);
      }

      // ── OAuth Endpoints ──
      if (path === '/oauth/register' && request.method === 'POST') {
        return handleRegister(request, env);
      }
      if (path === '/oauth/authorize' && (request.method === 'GET' || request.method === 'POST')) {
        return handleAuthorize(request, env);
      }
      if (path === '/oauth/token' && request.method === 'POST') {
        return handleToken(request, env);
      }

      // ── MCP Endpoint (auth required) ──
      if (path === '/mcp' && request.method === 'POST') {
        const auth = await validateToken(request, env);
        if (!auth) {
          return new Response(JSON.stringify({
            error: 'unauthorized',
            error_description: 'Valid Bearer token required',
          }), {
            status: 401,
            headers: {
              'Content-Type': 'application/json',
              'WWW-Authenticate': `Bearer resource="${serverUrl}", error="invalid_token"`,
            },
          });
        }

        // Parse JSON-RPC request
        let rpcRequest: JsonRpcRequest;
        try {
          rpcRequest = await request.json() as JsonRpcRequest;
        } catch {
          return json({ jsonrpc: '2.0', id: null, error: { code: -32700, message: 'Parse error' } }, 400);
        }

        if (rpcRequest.jsonrpc !== '2.0' || !rpcRequest.method) {
          return json({ jsonrpc: '2.0', id: rpcRequest?.id ?? null, error: { code: -32600, message: 'Invalid JSON-RPC request' } }, 400);
        }

        const response = await handleMcpRequest(rpcRequest, auth.userId, auth.tier, env);

        return new Response(JSON.stringify(response), {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      // ── SSE Endpoint (for clients that expect /sse/) ──
      if (path === '/sse' || path === '/sse/') {
        // Redirect to /mcp with a hint
        return json({
          message: 'This server uses Streamable HTTP. POST JSON-RPC requests to /mcp',
          mcp_endpoint: `${serverUrl}/mcp`,
        });
      }

      // ── Docs (static) ──
      if (path === '/docs/privacy') {
        return new Response('Privacy policy coming soon. Your data in Sovereign mode is encrypted end-to-end.', {
          headers: { 'Content-Type': 'text/plain' },
        });
      }
      if (path === '/docs/security') {
        return new Response('Security disclosure coming soon. Sovereign tier: AES-256-GCM encrypted, cloud cannot read. Convenience tier: data at rest in Cloudflare D1 with infrastructure encryption.', {
          headers: { 'Content-Type': 'text/plain' },
        });
      }

      // ── 404 ──
      return json({ error: 'Not found', docs: `${serverUrl}/health` }, 404);
    } catch (err: any) {
      return json({ error: 'Internal server error', message: err.message }, 500);
    }
  },
};
