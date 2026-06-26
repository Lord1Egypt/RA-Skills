/**
 * hub.mjs — IPC WebSocket hub server
 *
 * Standalone process that routes messages between Claude Code sessions.
 * All logging goes to stderr. stdout is reserved for machine-readable output.
 *
 * Usage: node hub.mjs
 * Env:   IPC_PORT (overrides DEFAULT_PORT)
 */

import http from 'node:http';
import { WebSocketServer } from 'ws';
import {
  DEFAULT_HOST,
  DEFAULT_PORT,
  HEARTBEAT_INTERVAL,
  HEARTBEAT_TIMEOUT,
  INBOX_MAX_SIZE,
  INBOX_TTL,
  IDLE_SHUTDOWN_DELAY,
} from './lib/constants.mjs';
import { createMessage, createSystemEvent, validateMessage } from './lib/protocol.mjs';

const PORT = parseInt(process.env.IPC_PORT ?? DEFAULT_PORT, 10);
const AUTH_TOKEN = process.env.IPC_AUTH_TOKEN || null;

// ---------------------------------------------------------------------------
// Auth helper
// ---------------------------------------------------------------------------
function checkAuth(providedToken) {
  if (!AUTH_TOKEN) return true; // Auth disabled
  return providedToken === AUTH_TOKEN;
}

// ---------------------------------------------------------------------------
// Session registry
// Map<name, { name, ws, connectedAt, topics: Set<string>, inbox: Array }>
// ---------------------------------------------------------------------------
/** @type {Map<string, {name: string, ws: import('ws').WebSocket|null, connectedAt: number, topics: Set<string>, inbox: Array, inboxExpiry: ReturnType<typeof setTimeout>|null}>} */
const sessions = new Map();

// ---------------------------------------------------------------------------
// Idle shutdown timer
// ---------------------------------------------------------------------------
let idleTimer = null;

function resetIdleTimer() {
  if (idleTimer !== null) {
    clearTimeout(idleTimer);
    idleTimer = null;
  }
}

function startIdleTimer() {
  resetIdleTimer();
  idleTimer = setTimeout(() => {
    stderr('[ipc-hub] no sessions connected — shutting down');
    process.exit(0);
  }, IDLE_SHUTDOWN_DELAY);
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function stderr(...args) {
  process.stderr.write(args.join(' ') + '\n');
}

function send(ws, payload) {
  try {
    if (ws && ws.readyState === ws.OPEN) {
      ws.send(JSON.stringify(payload));
    }
  } catch (err) {
    stderr(`[ipc-hub] send error: ${err.message}`);
  }
}

/** Broadcast a payload to all currently connected sessions except the sender */
function broadcast(payload, exceptName = null) {
  for (const [name, session] of sessions) {
    if (name === exceptName) continue;
    if (session.ws && session.ws.readyState === session.ws.OPEN) {
      send(session.ws, payload);
    }
  }
}

/** Push a message to a session's offline inbox (FIFO eviction at max size) */
function pushInbox(session, msg) {
  session.inbox.push(msg);
  if (session.inbox.length > INBOX_MAX_SIZE) {
    session.inbox.shift(); // evict oldest
  }
}

/** Flush buffered inbox to a newly connected session */
function flushInbox(session) {
  if (session.inbox.length === 0) return;
  const messages = session.inbox.splice(0);
  send(session.ws, { type: 'inbox', messages });
}

/** Schedule inbox cleanup after TTL */
function scheduleInboxCleanup(session) {
  if (session.inboxExpiry !== null) {
    clearTimeout(session.inboxExpiry);
  }
  session.inboxExpiry = setTimeout(() => {
    if (!session.ws) {
      // Session is still offline — remove entirely
      sessions.delete(session.name);
      stderr(`[ipc-hub] inbox expired, removed offline session: ${session.name}`);
    }
  }, INBOX_TTL);
}

// ---------------------------------------------------------------------------
// HTTP server (health endpoint)
// ---------------------------------------------------------------------------
const httpServer = http.createServer((req, res) => {
  // Auth check for all routes except /health
  if (AUTH_TOKEN) {
    const authHeader = req.headers.authorization;
    const providedToken = authHeader?.startsWith('Bearer ') ? authHeader.slice(7) : null;
    if (req.url !== '/health' && !checkAuth(providedToken)) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'unauthorized' }));
      return;
    }
  }

  if (req.method === 'GET' && req.url === '/health') {
    const sessionList = [];
    for (const [, s] of sessions) {
      if (s.ws) {
        sessionList.push({
          name: s.name,
          connectedAt: s.connectedAt,
          topics: [...s.topics],
        });
      }
    }
    const body = JSON.stringify({
      ok: true,
      sessions: sessionList,
      uptime: process.uptime(),
    });
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(body);
  } else if (req.method === 'POST' && req.url === '/send') {
    // HTTP API for sending messages — any tool (Codex, curl, scripts) can use this
    let body = '';
    let size = 0;
    const MAX_BODY = 1024 * 1024; // 1MB
    req.on('data', chunk => {
      size += chunk.length;
      if (size > MAX_BODY) {
        res.writeHead(413, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'payload too large' }));
        req.destroy();
        return;
      }
      body += chunk;
    });
    req.on('end', () => {
      let msg;
      try {
        msg = JSON.parse(body);
      } catch {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'invalid JSON' }));
        return;
      }

      if (!msg.from || !msg.to || !msg.content) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'requires "from", "to", and "content"' }));
        return;
      }

      // Build a full message if not already formatted
      if (!msg.type) {
        msg = createMessage({ from: msg.from, to: msg.to, content: msg.content, topic: msg.topic ?? null });
      }

      // Create a virtual sender session for routing
      const fakeSender = { name: msg.from };
      routeMessage(msg, fakeSender);

      const target = sessions.get(msg.to);
      const online = target?.ws?.readyState === target?.ws?.OPEN;
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, id: msg.id, online: !!online, buffered: !online }));
      stderr(`[ipc-hub] HTTP POST /send: ${msg.from} → ${msg.to}`);
    });
  } else if (req.method === 'GET' && req.url === '/sessions') {
    // Alias for /health — returns just sessions list
    const list = [];
    for (const [, s] of sessions) {
      if (s.ws) list.push({ name: s.name, connectedAt: s.connectedAt, topics: [...s.topics] });
    }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(list));
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

// ---------------------------------------------------------------------------
// WebSocket server
// ---------------------------------------------------------------------------
const wss = new WebSocketServer({ server: httpServer });

wss.on('connection', (ws, req) => {
  // Parse session name and token from query string
  const url = new URL(req.url, `http://localhost`);
  const name = url.searchParams.get('name');
  const token = url.searchParams.get('token');

  if (!checkAuth(token)) {
    ws.close(4003, 'unauthorized');
    return;
  }

  if (!name) {
    ws.close(4000, 'name query param required');
    return;
  }

  // Check if name is already taken by a live connection
  const existing = sessions.get(name);
  if (existing && existing.ws && existing.ws.readyState === existing.ws.OPEN) {
    ws.close(4001, 'name taken');
    return;
  }

  // Cancel pending inbox expiry if session is reconnecting
  if (existing && existing.inboxExpiry !== null) {
    clearTimeout(existing.inboxExpiry);
    existing.inboxExpiry = null;
  }

  // Register or update session
  const session = existing ?? {
    name,
    ws: null,
    connectedAt: Date.now(),
    topics: new Set(),
    inbox: [],
    inboxExpiry: null,
  };
  session.ws = ws;
  session.connectedAt = Date.now();
  sessions.set(name, session);

  // Cancel idle timer — we have a live session now
  resetIdleTimer();

  stderr(`[ipc-hub] session connected: ${name} (total: ${countLive()})`);

  // Notify other sessions
  broadcast(createSystemEvent({ event: 'session_joined', session: name }), name);

  // Flush any buffered inbox immediately
  flushInbox(session);

  // Heartbeat tracking
  ws.isAlive = true;
  ws.on('pong', () => { ws.isAlive = true; });

  // ---------------------------------------------------------------------------
  // Message handler
  // ---------------------------------------------------------------------------
  ws.on('message', (raw) => {
    let msg;
    try {
      msg = JSON.parse(raw.toString());
    } catch {
      send(ws, { type: 'error', error: 'invalid JSON' });
      return;
    }

    const { valid, error } = validateMessage(msg);
    if (!valid) {
      send(ws, { type: 'error', error });
      return;
    }

    switch (msg.type) {
      case 'ping':
        send(ws, { type: 'pong' });
        break;

      case 'register':
        // Re-register with optional channelPort; name already set from URL
        // channelPort is informational — stored for future use
        session.channelPort = msg.channelPort ?? null;
        send(ws, { type: 'registered', name: session.name });
        break;

      case 'subscribe':
        session.topics.add(msg.topic);
        send(ws, { type: 'subscribed', topic: msg.topic });
        break;

      case 'unsubscribe':
        session.topics.delete(msg.topic);
        send(ws, { type: 'unsubscribed', topic: msg.topic });
        break;

      case 'message':
        routeMessage(msg, session);
        break;

      default:
        send(ws, { type: 'error', error: `unknown message type: ${msg.type}` });
    }
  });

  // ---------------------------------------------------------------------------
  // Disconnect handler
  // ---------------------------------------------------------------------------
  ws.on('close', () => {
    session.ws = null;
    stderr(`[ipc-hub] session disconnected: ${name} (inbox: ${session.inbox.length} msgs)`);

    broadcast(createSystemEvent({ event: 'session_left', session: name }), name);

    // Keep inbox alive for TTL, then remove session record
    scheduleInboxCleanup(session);

    // Start idle timer if no live sessions remain
    if (countLive() === 0) {
      startIdleTimer();
    }
  });

  ws.on('error', (err) => {
    stderr(`[ipc-hub] ws error on session ${name}: ${err.message}`);
  });
});

// ---------------------------------------------------------------------------
// OpenClaw adapter — deliver messages to OpenClaw via Gateway HTTP API
// ---------------------------------------------------------------------------
const OPENCLAW_URL = process.env.OPENCLAW_URL || 'http://127.0.0.1:18789';
const OPENCLAW_TOKEN = process.env.OPENCLAW_TOKEN || '';

function isOpenClawSession(name) {
  return name.startsWith('openclaw');
}

async function deliverToOpenClaw(msg) {
  const content = `[IPC from ${msg.from}] ${msg.content}`;

  try {
    const headers = { 'Content-Type': 'application/json' };
    if (OPENCLAW_TOKEN) headers['Authorization'] = `Bearer ${OPENCLAW_TOKEN}`;

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);

    const res = await fetch(`${OPENCLAW_URL}/v1/chat/completions`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        model: 'openclaw',
        messages: [{ role: 'user', content }],
      }),
      signal: controller.signal,
    });
    clearTimeout(timeout);

    const data = await res.json();
    const reply = data.choices?.[0]?.message?.content || '';
    stderr(`[ipc-hub] openclaw adapter: delivered to ${msg.to}, reply: ${reply.substring(0, 200)}`);

    // If OpenClaw replied and the sender is online, forward the reply back
    if (reply && msg.from) {
      const sender = sessions.get(msg.from);
      if (sender?.ws?.readyState === sender?.ws?.OPEN) {
        send(sender.ws, createMessage({ from: msg.to, to: msg.from, content: reply }));
        stderr(`[ipc-hub] openclaw adapter: forwarded reply to ${msg.from}`);
      }
    }
    return true;
  } catch (err) {
    stderr(`[ipc-hub] openclaw adapter: failed: ${err?.message ?? err}`);
    return false;
  }
}

// ---------------------------------------------------------------------------
// Message routing
// ---------------------------------------------------------------------------
function routeMessage(msg, senderSession) {
  const { to, topic } = msg;
  const delivered = new Set(); // Track who already received the message

  // Topic-based fanout (can combine with direct addressing)
  if (topic) {
    for (const [, s] of sessions) {
      if (s.name === senderSession.name) continue;
      if (s.topics.has(topic)) {
        if (s.ws && s.ws.readyState === s.ws.OPEN) {
          send(s.ws, msg);
        } else {
          pushInbox(s, msg);
        }
        delivered.add(s.name); // Mark as delivered via topic
      }
    }
  }

  // Direct or broadcast routing
  if (to === '*') {
    // Broadcast to all except sender
    for (const [, s] of sessions) {
      if (s.name === senderSession.name) continue;
      if (delivered.has(s.name)) continue; // Skip if already got via topic
      if (s.ws && s.ws.readyState === s.ws.OPEN) {
        send(s.ws, msg);
      } else {
        pushInbox(s, msg);
      }
    }
  } else if (to && to !== '*') {
    // Direct message — skip if already delivered via topic
    if (!delivered.has(to)) {
      const target = sessions.get(to);
      if (target) {
        if (target.ws && target.ws.readyState === target.ws.OPEN) {
          send(target.ws, msg);
        } else {
          pushInbox(target, msg);
          // Try OpenClaw adapter for openclaw sessions
          if (isOpenClawSession(to)) {
            deliverToOpenClaw(msg);
          }
          stderr(`[ipc-hub] ${senderSession.name} → ${to}: session offline, buffered`);
        }
      } else {
        // Unknown target
        if (isOpenClawSession(to)) {
          // Don't create stub, try OpenClaw adapter directly
          deliverToOpenClaw(msg);
          stderr(`[ipc-hub] ${senderSession.name} → ${to}: routing to OpenClaw adapter`);
        } else {
          // Create stub for non-OpenClaw targets
          const stub = {
            name: to,
            ws: null,
            connectedAt: 0,
            topics: new Set(),
            inbox: [msg],
            inboxExpiry: null,
          };
          sessions.set(to, stub);
          scheduleInboxCleanup(stub);
          stderr(`[ipc-hub] ${senderSession.name} → ${to}: unknown session, created stub with buffered msg`);
        }
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Heartbeat loop
// ---------------------------------------------------------------------------
function countLive() {
  let count = 0;
  for (const [, s] of sessions) {
    if (s.ws && s.ws.readyState === s.ws.OPEN) count++;
  }
  return count;
}

const heartbeatInterval = setInterval(() => {
  for (const [name, session] of sessions) {
    const { ws } = session;
    if (!ws) continue;
    if (ws.isAlive === false) {
      stderr(`[ipc-hub] heartbeat timeout: terminating ${name}`);
      ws.terminate();
      continue;
    }
    ws.isAlive = false;
    ws.ping();
    // Set a timeout to check for pong
    setTimeout(() => {
      if (ws.isAlive === false && ws.readyState === ws.OPEN) {
        stderr(`[ipc-hub] no pong from ${name}, terminating`);
        ws.terminate();
      }
    }, HEARTBEAT_TIMEOUT);
  }
}, HEARTBEAT_INTERVAL);

heartbeatInterval.unref(); // Don't block process exit

// ---------------------------------------------------------------------------
// Start listening
// ---------------------------------------------------------------------------
httpServer.listen(PORT, DEFAULT_HOST, () => {
  stderr(`[ipc-hub] listening on :${PORT}`);
  stderr(`[ipc-hub] auth: ${AUTH_TOKEN ? 'enabled (token required)' : 'disabled (open access)'}`);
});

httpServer.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    stderr(`[ipc-hub] port ${PORT} already in use — another hub may be running`);
    stderr(`[ipc-hub] check with: curl http://127.0.0.1:${PORT}/health`);
  } else {
    stderr(`[ipc-hub] http server error: ${err.message}`);
  }
  process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  stderr('[ipc-hub] SIGTERM received, shutting down');
  clearInterval(heartbeatInterval);
  wss.close(() => httpServer.close(() => process.exit(0)));
});

process.on('SIGINT', () => {
  stderr('[ipc-hub] SIGINT received, shutting down');
  clearInterval(heartbeatInterval);
  wss.close(() => httpServer.close(() => process.exit(0)));
});
