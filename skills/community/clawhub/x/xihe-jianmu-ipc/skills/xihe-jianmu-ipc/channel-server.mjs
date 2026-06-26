#!/usr/bin/env node
/**
 * channel-server.mjs — IPC Channel Server (receiving side)
 *
 * Connects to the Hub via WebSocket and pushes incoming messages to an
 * external endpoint (e.g. Claude Code Channels webhook) via HTTP POST.
 *
 * stdout: (reserved, not used)
 * stderr: all logging
 *
 * Env:
 *   IPC_NAME         (required) — session display name
 *   IPC_PORT         — Hub port (default: DEFAULT_PORT)
 *   IPC_HUB_HOST     — Hub host (auto-detects WSL2)
 *   IPC_CHANNEL_URL  — HTTP endpoint to POST messages to (optional)
 */

import { readFileSync, existsSync } from 'node:fs';
import { DEFAULT_PORT } from './lib/constants.mjs';

// ---------------------------------------------------------------------------
// Environment
// ---------------------------------------------------------------------------
const name = process.env.IPC_NAME;
if (!name) {
  process.stderr.write('[ipc-channel] ERROR: IPC_NAME env var required\n');
  process.exit(1);
}

const port = parseInt(process.env.IPC_PORT || String(DEFAULT_PORT), 10);
const channelUrl = process.env.IPC_CHANNEL_URL || null;
const authToken = process.env.IPC_AUTH_TOKEN || '';

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
          process.stderr.write(`[ipc-channel] WSL2 detected, using Windows host: ${match[1]}\n`);
          return match[1];
        }
      }
    } catch {
      // fall through to default
    }
  }

  return '127.0.0.1';
}

const host = detectHost();

// ---------------------------------------------------------------------------
// HTTP POST helper
// ---------------------------------------------------------------------------
async function postToChannel(body) {
  try {
    const res = await fetch(channelUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    process.stderr.write(`[ipc-channel] POST to ${channelUrl} → ${res.status}\n`);
  } catch (err) {
    process.stderr.write(`[ipc-channel] POST failed: ${err?.message ?? err}\n`);
  }
}

// ---------------------------------------------------------------------------
// Message handler
// ---------------------------------------------------------------------------
function handleMessage(msg) {
  if (msg.type === 'message') {
    const text = `From ${msg.from ?? '(unknown)'}: ${msg.content ?? ''}`;
    process.stderr.write(`[ipc-channel] received: ${text}\n`);

    if (channelUrl) {
      postToChannel({ message: text });
    }
  } else if (msg.type === 'inbox') {
    // Buffered messages delivered on reconnect
    const messages = Array.isArray(msg.messages) ? msg.messages : [];
    process.stderr.write(`[ipc-channel] inbox flush: ${messages.length} buffered message(s)\n`);
    for (const m of messages) {
      handleMessage(m);
    }
  } else if (msg.type === 'system') {
    process.stderr.write(`[ipc-channel] system event: ${msg.event} (session=${msg.session})\n`);
  }
}

// ---------------------------------------------------------------------------
// WebSocket connection with reconnect
// ---------------------------------------------------------------------------
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 10;
const RECONNECT_BASE_DELAY = 3000;
const RECONNECT_MAX_DELAY = 30000;

function buildWsUrl() {
  let url = `ws://${host}:${port}/ws?name=${encodeURIComponent(name)}`;
  if (authToken) url += `&token=${encodeURIComponent(authToken)}`;
  return url;
}

function scheduleReconnect() {
  if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
    process.stderr.write('[ipc-channel] max reconnect attempts reached, giving up\n');
    process.exit(1);
    return;
  }

  const delay = Math.min(
    RECONNECT_BASE_DELAY * Math.pow(2, reconnectAttempts),
    RECONNECT_MAX_DELAY,
  );
  reconnectAttempts++;
  process.stderr.write(`[ipc-channel] reconnecting in ${delay}ms (attempt ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})\n`);
  setTimeout(connect, delay);
}

function connect() {
  const url = buildWsUrl();
  process.stderr.write(`[ipc-channel] connecting to hub at ${url}\n`);

  let socket;
  try {
    socket = new WebSocket(url);
  } catch (err) {
    process.stderr.write(`[ipc-channel] failed to create WebSocket: ${err?.message ?? err}\n`);
    scheduleReconnect();
    return;
  }

  socket.addEventListener('open', () => {
    process.stderr.write(`[ipc-channel] connected to hub as "${name}"\n`);
    reconnectAttempts = 0;

    // Register with the hub
    socket.send(JSON.stringify({ type: 'register', name }));
  });

  socket.addEventListener('message', (event) => {
    let msg;
    try {
      msg = JSON.parse(event.data);
    } catch {
      process.stderr.write('[ipc-channel] received non-JSON message from hub\n');
      return;
    }
    handleMessage(msg);
  });

  socket.addEventListener('close', (event) => {
    process.stderr.write(`[ipc-channel] disconnected from hub (code=${event.code})\n`);
    scheduleReconnect();
  });

  socket.addEventListener('error', (event) => {
    process.stderr.write(`[ipc-channel] WebSocket error: ${event.message ?? 'unknown'}\n`);
    // 'close' fires after 'error' — reconnect scheduled there
  });
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
process.stderr.write(`[ipc-channel] starting as "${name}" (hub=${host}:${port})\n`);
if (channelUrl) {
  process.stderr.write(`[ipc-channel] channel URL: ${channelUrl}\n`);
} else {
  process.stderr.write('[ipc-channel] no IPC_CHANNEL_URL set — messages will be logged only\n');
}

connect();
