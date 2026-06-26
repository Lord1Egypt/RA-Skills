// memory-crystal/worker.ts ... Cloudflare Worker (Ephemeral Relay).
// Dead drop for encrypted blobs. No search, no database, no intelligence.
// Data passes through encrypted, gets picked up, gets deleted.
// The Worker cannot read what it holds.
//
// Channels:
//   conversations         ... devices drop encrypted conversation chunks for Core to pick up
//   mirror                ... Core drops encrypted delta chunks for Nodes to pick up
//   files                 ... Core drops encrypted file tree deltas for Nodes to pick up
//   commands              ... Node sends commands to Core ("process my data", "run Dream Weaver")
//                             Core sends results back ("processing complete", "mirror ready")
//   chatgpt               ... cloud MCP server drops (conversations, memories, commands)
//   chatgpt-attachments   ... cloud MCP server drops binary files (images, audio, video)
//
// Endpoints:
//   POST   /drop/:channel       — deposit encrypted blob
//   GET    /pickup/:channel     — list available blobs
//   GET    /pickup/:channel/:id — retrieve specific blob
//   DELETE /confirm/:channel/:id — confirm receipt, delete blob
//   GET    /health              — alive check (no auth)

export interface Env {
  RELAY: R2Bucket;
  AUTH_TOKEN_CC_AIR: string;
  AUTH_TOKEN_CC_MINI: string;
  AUTH_TOKEN_LESA: string;
}

// ── Auth ──

interface AuthResult {
  agentId: string;
}

function authenticate(request: Request, env: Env): AuthResult | Response {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) {
    return json({ error: 'Missing Authorization header' }, 401);
  }

  const token = auth.slice(7);
  const tokenMap: Record<string, string> = {};
  if (env.AUTH_TOKEN_CC_AIR) tokenMap[env.AUTH_TOKEN_CC_AIR] = 'cc-air';
  if (env.AUTH_TOKEN_CC_MINI) tokenMap[env.AUTH_TOKEN_CC_MINI] = 'cc-mini';
  if (env.AUTH_TOKEN_LESA) tokenMap[env.AUTH_TOKEN_LESA] = 'lesa-mini';

  const agentId = tokenMap[token];
  if (!agentId) {
    return json({ error: 'Invalid token' }, 403);
  }

  return { agentId };
}

// ── Channel validation ──

const VALID_CHANNELS = ['conversations', 'mirror', 'commands', 'files', 'chatgpt', 'chatgpt-attachments'];

function isValidChannel(channel: string): boolean {
  return VALID_CHANNELS.includes(channel);
}

// ── Handlers ──

async function handleDrop(request: Request, env: Env, agentId: string, channel: string): Promise<Response> {
  if (!isValidChannel(channel)) {
    return json({ error: `Invalid channel: ${channel}. Valid: ${VALID_CHANNELS.join(', ')}` }, 400);
  }

  const body = await request.arrayBuffer();
  if (body.byteLength === 0) {
    return json({ error: 'Empty payload' }, 400);
  }

  // Max 100MB per blob (DB snapshots can be large)
  if (body.byteLength > 100 * 1024 * 1024) {
    return json({ error: 'Payload too large (max 100MB)' }, 413);
  }

  const id = crypto.randomUUID();
  const key = `${channel}/${id}`;
  const now = new Date().toISOString();

  await env.RELAY.put(key, body, {
    customMetadata: {
      agent_id: agentId,
      dropped_at: now,
      size: String(body.byteLength),
    },
  });

  return json({ ok: true, id, channel, size: body.byteLength, dropped_at: now });
}

async function handlePickupList(env: Env, channel: string): Promise<Response> {
  if (!isValidChannel(channel)) {
    return json({ error: `Invalid channel: ${channel}` }, 400);
  }

  const listed = await env.RELAY.list({ prefix: `${channel}/` });
  const blobs = listed.objects.map(obj => ({
    id: obj.key.split('/')[1],
    size: obj.size,
    dropped_at: obj.customMetadata?.dropped_at || obj.uploaded.toISOString(),
    agent_id: obj.customMetadata?.agent_id || 'unknown',
  }));

  return json({ channel, count: blobs.length, blobs });
}

async function handlePickup(env: Env, channel: string, id: string): Promise<Response> {
  if (!isValidChannel(channel)) {
    return json({ error: `Invalid channel: ${channel}` }, 400);
  }

  const key = `${channel}/${id}`;
  const obj = await env.RELAY.get(key);

  if (!obj) {
    return json({ error: 'Blob not found (already picked up or expired)' }, 404);
  }

  return new Response(obj.body, {
    headers: {
      'Content-Type': 'application/octet-stream',
      'X-Agent-Id': obj.customMetadata?.agent_id || 'unknown',
      'X-Dropped-At': obj.customMetadata?.dropped_at || '',
    },
  });
}

async function handleConfirm(env: Env, channel: string, id: string): Promise<Response> {
  if (!isValidChannel(channel)) {
    return json({ error: `Invalid channel: ${channel}` }, 400);
  }

  const key = `${channel}/${id}`;
  const obj = await env.RELAY.head(key);

  if (!obj) {
    return json({ error: 'Blob not found (already confirmed or expired)' }, 404);
  }

  await env.RELAY.delete(key);
  return json({ ok: true, deleted: key });
}

// ── Response helper ──

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

// ── Router ──

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const parts = url.pathname.split('/').filter(Boolean);

    // Health check (no auth)
    if (parts[0] === 'health' && request.method === 'GET') {
      return json({ ok: true, service: 'memory-crystal-relay', mode: 'ephemeral' });
    }

    // Everything else requires auth
    const authResult = authenticate(request, env);
    if (authResult instanceof Response) return authResult;
    const { agentId } = authResult;

    try {
      // POST /drop/:channel
      if (parts[0] === 'drop' && parts[1] && request.method === 'POST') {
        return handleDrop(request, env, agentId, parts[1]);
      }

      // GET /pickup/:channel (list) or GET /pickup/:channel/:id (retrieve)
      if (parts[0] === 'pickup' && parts[1] && request.method === 'GET') {
        if (parts[2]) {
          return handlePickup(env, parts[1], parts[2]);
        }
        return handlePickupList(env, parts[1]);
      }

      // DELETE /confirm/:channel/:id
      if (parts[0] === 'confirm' && parts[1] && parts[2] && request.method === 'DELETE') {
        return handleConfirm(env, parts[1], parts[2]);
      }

      return json({ error: 'Not found' }, 404);
    } catch (err: any) {
      return json({ error: err.message || 'Internal error' }, 500);
    }
  },

  // Scheduled cleanup: delete blobs older than 24h (TTL safety net)
  async scheduled(event: ScheduledEvent, env: Env): Promise<void> {
    const cutoff = Date.now() - 24 * 60 * 60 * 1000;

    for (const channel of VALID_CHANNELS) {
      const listed = await env.RELAY.list({ prefix: `${channel}/` });
      for (const obj of listed.objects) {
        const droppedAt = obj.customMetadata?.dropped_at;
        if (droppedAt && new Date(droppedAt).getTime() < cutoff) {
          await env.RELAY.delete(obj.key);
        }
      }
    }
  },
};
