#!/usr/bin/env node
/**
 * mcp-server.mjs — IPC MCP Server
 *
 * Launched by Claude Code via stdio.
 * Connects to the IPC Hub via WebSocket and exposes ipc_send /
 * ipc_sessions tools through the MCP protocol via the official SDK.
 *
 * stdout: MCP SDK transport (Content-Length framed JSON-RPC)
 * stderr: all logging
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { createMessage } from './lib/protocol.mjs';
import {
  DEFAULT_PORT,
  HUB_AUTOSTART_TIMEOUT,
  HUB_AUTOSTART_RETRY_INTERVAL,
} from './lib/constants.mjs';
import { readFileSync, existsSync } from 'fs';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import http from 'http';

// ---------------------------------------------------------------------------
// Project directory (needed for hub autostart)
// ---------------------------------------------------------------------------
const PROJECT_DIR = dirname(fileURLToPath(import.meta.url));

// ---------------------------------------------------------------------------
// Environment
// ---------------------------------------------------------------------------
// Priority: IPC_NAME (system env, set by PowerShell) > IPC_DEFAULT_NAME (.mcp.json) > auto-generated
const IPC_NAME = process.env.IPC_NAME || process.env.IPC_DEFAULT_NAME || `session-${process.pid}`;
if (!process.env.IPC_NAME && !process.env.IPC_DEFAULT_NAME) {
  process.stderr.write(`[ipc] IPC_NAME not set, using auto-generated: ${IPC_NAME}\n`);
}

const IPC_PORT = parseInt(process.env.IPC_PORT ?? String(DEFAULT_PORT), 10);
const AUTH_TOKEN = process.env.IPC_AUTH_TOKEN || '';

// ---------------------------------------------------------------------------
// Host auto-detection (WSL2 support)
// ---------------------------------------------------------------------------
function detectHost() {
  if (process.env.IPC_HUB_HOST) return process.env.IPC_HUB_HOST;

  if (process.platform === 'linux' && existsSync('/etc/resolv.conf')) {
    try {
      const content = readFileSync('/etc/resolv.conf', 'utf8');
      for (const line of content.split('\n')) {
        const match = line.match(/^nameserver\s+([\d.]+)/);
        if (match) {
          process.stderr.write(`[ipc] WSL2 detected, using Windows host: ${match[1]}\n`);
          return match[1];
        }
      }
    } catch {
      // fall through to default
    }
  }

  return '127.0.0.1';
}

const HOST = detectHost();

// ---------------------------------------------------------------------------
// WebSocket state
// ---------------------------------------------------------------------------
let ws = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 10;
const RECONNECT_BASE_DELAY = 3000;
const RECONNECT_MAX_DELAY = 30000;

const pendingMessages = [];   // incoming messages (future use)
const outgoingQueue = [];     // queued while disconnected

// ---------------------------------------------------------------------------
// Create MCP Server with Channel capability
// ---------------------------------------------------------------------------
const server = new Server(
  { name: 'ipc', version: '0.1.0' },
  {
    capabilities: {
      tools: {},
      experimental: {
        'claude/channel': {},
      },
    },
    instructions:
      'IPC messages from other sessions arrive as <channel> tags. When you receive one, read the content and act on it. If the sender expects a reply, use ipc_send to respond.',
  },
);

// ---------------------------------------------------------------------------
// Tool handlers
// ---------------------------------------------------------------------------
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'ipc_send',
      description: "Send a message to another Claude Code session by name, or broadcast to all with '*'",
      inputSchema: {
        type: 'object',
        properties: {
          to: {
            type: 'string',
            description: "Target session name, or '*' for broadcast",
          },
          content: {
            type: 'string',
            description: 'Message content',
          },
          topic: {
            type: 'string',
            description: 'Optional topic tag for pub/sub',
          },
        },
        required: ['to', 'content'],
      },
    },
    {
      name: 'ipc_sessions',
      description: 'List all currently connected Claude Code sessions',
      inputSchema: {
        type: 'object',
        properties: {},
      },
    },
    {
      name: 'ipc_whoami',
      description: 'Show the current session name and connection status',
      inputSchema: {
        type: 'object',
        properties: {},
      },
    },
    {
      name: 'ipc_subscribe',
      description: 'Subscribe or unsubscribe to a topic channel. Messages sent with this topic will be delivered to all subscribers.',
      inputSchema: {
        type: 'object',
        properties: {
          topic: { type: 'string', description: 'Topic name to subscribe/unsubscribe' },
          action: { type: 'string', enum: ['subscribe', 'unsubscribe'], description: 'subscribe or unsubscribe' },
        },
        required: ['topic', 'action'],
      },
    },
    {
      name: 'ipc_spawn',
      description: 'Spawn a new Claude Code session. Background mode runs a one-shot task and reports back via IPC. Interactive mode opens a new terminal window.',
      inputSchema: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Session name for the new session' },
          task: { type: 'string', description: 'Task description or initial prompt for the session' },
          interactive: { type: 'boolean', description: 'If true, opens a new terminal window. If false (default), runs in background.' },
          model: { type: 'string', description: 'Optional model override (e.g. claude-sonnet-4-6)' },
        },
        required: ['name', 'task'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  // -------------------------------------------------------------------------
  // ipc_send
  // -------------------------------------------------------------------------
  if (name === 'ipc_send') {
    const { to, content, topic } = args ?? {};
    if (!to || content === undefined || content === null) {
      return {
        content: [{ type: 'text', text: 'ipc_send requires "to" and "content"' }],
        isError: true,
      };
    }

    const message = createMessage({
      from: IPC_NAME,
      to,
      content: String(content),
      topic: topic ?? null,
    });

    wsSend(message);
    return { content: [{ type: 'text', text: JSON.stringify({ delivered: true, id: message.id }) }] };
  }

  // -------------------------------------------------------------------------
  // ipc_sessions
  // -------------------------------------------------------------------------
  if (name === 'ipc_sessions') {
    try {
      const healthUrl = `http://${HOST}:${IPC_PORT}/health`;
      const response = await httpGet(healthUrl);
      return { content: [{ type: 'text', text: JSON.stringify(response.sessions ?? []) }] };
    } catch (err) {
      process.stderr.write(`[ipc] ipc_sessions error: ${err?.message ?? err}\n`);
      return {
        content: [{ type: 'text', text: `Failed to fetch sessions: ${err?.message ?? err}` }],
        isError: true,
      };
    }
  }

  // -------------------------------------------------------------------------
  // ipc_subscribe
  // -------------------------------------------------------------------------
  if (name === 'ipc_subscribe') {
    const { topic, action } = args ?? {};
    if (!topic || !action) {
      return { content: [{ type: 'text', text: 'ipc_subscribe requires "topic" and "action"' }], isError: true };
    }
    if (action !== 'subscribe' && action !== 'unsubscribe') {
      return { content: [{ type: 'text', text: 'action must be "subscribe" or "unsubscribe"' }], isError: true };
    }
    // Send subscribe/unsubscribe to hub via WebSocket
    wsSend({ type: action, topic });
    return { content: [{ type: 'text', text: JSON.stringify({ action, topic, ok: true }) }] };
  }

  if (name === 'ipc_whoami') {
    return { content: [{ type: 'text', text: JSON.stringify({
      name: IPC_NAME,
      hub_connected: ws?.readyState === 1,
      hub: `${HOST}:${IPC_PORT}`,
      pending_outgoing: outgoingQueue.length,
    }) }] };
  }

  // -------------------------------------------------------------------------
  // ipc_spawn
  // -------------------------------------------------------------------------
  if (name === 'ipc_spawn') {
    const { name: sessionName, task, interactive, model } = args ?? {};
    if (!sessionName || !task) {
      return { content: [{ type: 'text', text: 'ipc_spawn requires "name" and "task"' }], isError: true };
    }

    try {
      const result = spawnSession({ name: sessionName, task, interactive: !!interactive, model });
      return { content: [{ type: 'text', text: JSON.stringify(result) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Failed to spawn session: ${err?.message ?? err}` }], isError: true };
    }
  }

  return {
    content: [{ type: 'text', text: `Unknown tool: ${name}` }],
    isError: true,
  };
});

// ---------------------------------------------------------------------------
// spawnSession — launch a new Claude Code session (background or interactive)
// ---------------------------------------------------------------------------
function spawnSession({ name: sessionName, task, interactive, model }) {
  const ipcEnv = {
    ...process.env,
    IPC_NAME: sessionName,
    NO_PROXY: '127.0.0.1,localhost',
    no_proxy: '127.0.0.1,localhost',
  };

  // Build the system instruction that tells the spawned session about IPC
  const ipcInstruction = `Your IPC session name is "${sessionName}". You are connected to the IPC hub. When you complete your task, report back using ipc_send(to="${IPC_NAME}", content="your result"). You can also receive messages from other sessions.`;

  const fullPrompt = `${ipcInstruction}\n\nTask: ${task}`;

  if (interactive) {
    // Interactive mode: open a new terminal window with Claude Code
    // Patch Claude Code to skip dev channels warning, then launch
    const patchScript = join(PROJECT_DIR, 'bin', 'patch-channels.mjs').replace(/\\/g, '\\\\');
    const extraArgs = model ? ` --model ${model}` : '';
    const psCommand = `$env:IPC_NAME='${sessionName}'; node '${patchScript}'; claude --dangerously-skip-permissions --dangerously-load-development-channels server:ipc${extraArgs}`;

    if (process.platform === 'win32') {
      // Windows: use cmd /c start to open new PowerShell window
      spawn('cmd', ['/c', 'start', 'powershell', '-NoExit', '-Command', psCommand], {
        detached: true,
        stdio: 'ignore',
        env: ipcEnv,
      }).unref();
    } else {
      // Linux/WSL: try to open a new terminal
      const terminals = ['gnome-terminal', 'xterm', 'konsole'];
      let spawned = false;
      for (const term of terminals) {
        try {
          spawn(term, ['--', 'bash', '-c', `IPC_NAME='${sessionName}' claude --dangerously-skip-permissions --dangerously-load-development-channels server:ipc`], {
            detached: true,
            stdio: 'ignore',
            env: ipcEnv,
          }).unref();
          spawned = true;
          break;
        } catch { continue; }
      }
      if (!spawned) {
        // Fallback: just spawn in background
        spawn('bash', ['-c', `IPC_NAME='${sessionName}' claude --dangerously-skip-permissions --dangerously-load-development-channels server:ipc`], {
          detached: true,
          stdio: 'ignore',
          env: ipcEnv,
        }).unref();
      }
    }

    process.stderr.write(`[ipc] spawned interactive session "${sessionName}" in new terminal\n`);
    return { name: sessionName, mode: 'interactive', status: 'spawned' };

  } else {
    // Background mode: run claude -p (one-shot, non-interactive)
    const claudeArgs = ['-p', '--dangerously-skip-permissions'];
    if (model) claudeArgs.push('--model', model);
    claudeArgs.push(fullPrompt);

    const child = spawn('claude', claudeArgs, {
      detached: true,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: ipcEnv,
      shell: true,
    });
    child.unref();

    // Log stdout/stderr for debugging
    let output = '';
    child.stdout?.on('data', d => { output += d.toString(); });
    child.stderr?.on('data', d => {
      process.stderr.write(`[ipc:${sessionName}] ${d.toString()}`);
    });
    child.on('exit', (code) => {
      process.stderr.write(`[ipc] background session "${sessionName}" exited (code=${code})\n`);
    });

    process.stderr.write(`[ipc] spawned background session "${sessionName}" (pid=${child.pid})\n`);
    return { name: sessionName, mode: 'background', status: 'spawned', pid: child.pid };
  }
}

// ---------------------------------------------------------------------------
// Channel notification push
// ---------------------------------------------------------------------------
function pushChannelNotification(msg) {
  server.notification({
    method: 'notifications/claude/channel',
    params: {
      content: msg.content || JSON.stringify(msg),
      meta: {
        from: msg.from || 'unknown',
        message_id: msg.id || '',
        topic: msg.topic || '',
      },
    },
  }).catch((err) => {
    process.stderr.write(`[ipc] failed to push channel notification: ${err?.message ?? err}\n`);
  });
}

// ---------------------------------------------------------------------------
// Hub autostart
// ---------------------------------------------------------------------------
function autostartHub() {
  process.stderr.write('[ipc] attempting to autostart hub...\n');
  try {
    const child = spawn(process.execPath, [join(PROJECT_DIR, 'hub.mjs')], {
      cwd: PROJECT_DIR,
      detached: true,
      stdio: 'ignore',
    });
    child.unref();
    process.stderr.write(`[ipc] hub spawned (pid ${child.pid})\n`);
  } catch (err) {
    process.stderr.write(`[ipc] failed to spawn hub: ${err?.message ?? err}\n`);
  }
}

// ---------------------------------------------------------------------------
// WebSocket connection helpers
// ---------------------------------------------------------------------------
function buildWsUrl() {
  let url = `ws://${HOST}:${IPC_PORT}/ws?name=${encodeURIComponent(IPC_NAME)}`;
  if (AUTH_TOKEN) url += `&token=${encodeURIComponent(AUTH_TOKEN)}`;
  return url;
}

function flushOutgoingQueue() {
  while (outgoingQueue.length > 0 && ws?.readyState === 1 /* OPEN */) {
    const msg = outgoingQueue.shift();
    try {
      ws.send(msg);
    } catch (err) {
      process.stderr.write(`[ipc] failed to flush queued message: ${err?.message ?? err}\n`);
      outgoingQueue.unshift(msg); // put it back
      break;
    }
  }
}

function scheduleReconnect() {
  if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
    process.stderr.write('[ipc] max reconnect attempts reached, giving up\n');
    return;
  }

  const delay = Math.min(
    RECONNECT_BASE_DELAY * Math.pow(2, reconnectAttempts),
    RECONNECT_MAX_DELAY,
  );
  reconnectAttempts++;
  process.stderr.write(`[ipc] reconnecting in ${delay}ms (attempt ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})\n`);
  setTimeout(connect, delay);
}

// ---------------------------------------------------------------------------
// Shared WebSocket message handler
// ---------------------------------------------------------------------------
function handleWsMessage(event) {
  let msg;
  try {
    msg = JSON.parse(event.data);
  } catch {
    process.stderr.write('[ipc] received non-JSON message from hub\n');
    return;
  }

  if (msg.type === 'message') {
    pushChannelNotification(msg);
    process.stderr.write(`[ipc] pushed channel notification from ${msg.from ?? '(unknown)'}\n`);
  } else if (msg.type === 'inbox') {
    const messages = Array.isArray(msg.messages) ? msg.messages : [];
    for (const m of messages) {
      if (m.type === 'message') pushChannelNotification(m);
    }
    process.stderr.write(`[ipc] pushed ${messages.length} buffered messages\n`);
  }

  pendingMessages.push(msg);
  process.stderr.write(`[ipc] received message from ${msg.from ?? '(unknown)'}\n`);
}

// ---------------------------------------------------------------------------
// Persistent reconnect loop (used after initial connection is established)
// ---------------------------------------------------------------------------
function connect() {
  const url = buildWsUrl();
  process.stderr.write(`[ipc] connecting to hub at ${url}\n`);

  let socket;
  try {
    socket = new WebSocket(url);
  } catch (err) {
    process.stderr.write(`[ipc] failed to create WebSocket: ${err?.message ?? err}\n`);
    scheduleReconnect();
    return;
  }

  socket.addEventListener('open', () => {
    process.stderr.write('[ipc] connected to hub\n');
    reconnectAttempts = 0;
    ws = socket;
    socket.send(JSON.stringify({ type: 'register', name: IPC_NAME }));
    flushOutgoingQueue();
  });

  socket.addEventListener('message', handleWsMessage);

  socket.addEventListener('close', (event) => {
    process.stderr.write(`[ipc] disconnected from hub (code=${event.code})\n`);
    ws = null;
    scheduleReconnect();
  });

  socket.addEventListener('error', (event) => {
    process.stderr.write(`[ipc] WebSocket error: ${event.message ?? 'unknown'}\n`);
    // 'close' fires after 'error', reconnect will be scheduled there
  });
}

// ---------------------------------------------------------------------------
// Initial connection with optional hub autostart
// ---------------------------------------------------------------------------
async function initialConnect() {
  return new Promise((resolve) => {
    let elapsed = 0;
    let autostartDone = false;

    function tryOnce() {
      let socket;
      try {
        socket = new WebSocket(buildWsUrl());
      } catch {
        handleFailure();
        return;
      }

      const cleanup = () => {
        socket.removeEventListener('open', onOpen);
        socket.removeEventListener('error', onError);
      };

      const onOpen = () => {
        cleanup();
        process.stderr.write('[ipc] initial connection to hub succeeded\n');
        reconnectAttempts = 0;
        ws = socket;

        socket.send(JSON.stringify({ type: 'register', name: IPC_NAME }));
        flushOutgoingQueue();

        socket.addEventListener('message', handleWsMessage);

        socket.addEventListener('close', (ev) => {
          process.stderr.write(`[ipc] disconnected from hub (code=${ev.code})\n`);
          ws = null;
          scheduleReconnect();
        });

        socket.addEventListener('error', (ev) => {
          process.stderr.write(`[ipc] WebSocket error: ${ev.message ?? 'unknown'}\n`);
        });

        resolve();
      };

      const onError = () => {
        cleanup();
        try { socket.close(); } catch { /* ignore */ }
        handleFailure();
      };

      socket.addEventListener('open', onOpen);
      socket.addEventListener('error', onError);
    }

    function handleFailure() {
      if (process.env.IPC_HUB_AUTOSTART !== 'false' && !autostartDone) {
        autostartDone = true;
        autostartHub();
      }

      elapsed += HUB_AUTOSTART_RETRY_INTERVAL;
      if (elapsed >= HUB_AUTOSTART_TIMEOUT) {
        process.stderr.write('[ipc] could not connect to hub within timeout, will retry in background\n');
        scheduleReconnect();
        resolve(); // continue starting the MCP server anyway
        return;
      }

      setTimeout(tryOnce, HUB_AUTOSTART_RETRY_INTERVAL);
    }

    tryOnce();
  });
}

// ---------------------------------------------------------------------------
// HTTP helper for /health endpoint
// ---------------------------------------------------------------------------
function httpGet(url) {
  return new Promise((resolve, reject) => {
    const headers = {};
    if (AUTH_TOKEN) headers['Authorization'] = `Bearer ${AUTH_TOKEN}`;
    const req = http.get(url, { headers }, (res) => {
      let body = '';
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch { reject(new Error(`invalid JSON from ${url}: ${body}`)); }
      });
    });
    req.on('error', reject);
    req.setTimeout(5000, () => { req.destroy(new Error('timeout')); });
  });
}

// ---------------------------------------------------------------------------
// WebSocket send (with queueing on disconnect)
// ---------------------------------------------------------------------------
function wsSend(payload) {
  const serialized = typeof payload === 'string' ? payload : JSON.stringify(payload);
  if (ws?.readyState === 1 /* OPEN */) {
    ws.send(serialized);
  } else {
    outgoingQueue.push(serialized);
    if (outgoingQueue.length > 100) {
      outgoingQueue.shift(); // Drop oldest
      process.stderr.write('[ipc] outgoing queue full, dropped oldest message\n');
    }
    process.stderr.write('[ipc] hub not connected, message queued\n');
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
async function main() {
  process.stderr.write(`[ipc] starting MCP server as "${IPC_NAME}"\n`);

  // Start MCP transport FIRST so Claude Code handshake doesn't timeout
  const transport = new StdioServerTransport();
  await server.connect(transport);

  process.stderr.write('[ipc] MCP server ready, connecting to hub in background...\n');

  // Connect to hub in background (non-blocking)
  initialConnect().then(() => {
    process.stderr.write(`[ipc] hub connection established (session="${IPC_NAME}", hub=${HOST}:${IPC_PORT})\n`);
  }).catch((err) => {
    process.stderr.write(`[ipc] hub connection failed: ${err?.message ?? err}\n`);
  });
}

main().catch((err) => {
  process.stderr.write(`[ipc] fatal: ${err?.message ?? err}\n`);
  process.exit(1);
});
