#!/usr/bin/env node
// memory-crystal/crystal-serve.ts — Crystal Core gateway.
// Thin HTTP server that makes CC-Mini addressable on localhost.
// Runs in a tmux session. Localhost-only. Never exposed to network.
//
// Endpoints:
//   POST /v1/chat/completions   OpenAI-compatible (invoke claude -p)
//   POST /process               Trigger backfill/dream-weaver for an agent
//   GET  /status                Health check
//
// Usage:
//   crystal serve [--port 18790]
//   tmux new-session -s crystal-core -d 'crystal serve'

import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import { spawn } from 'node:child_process';
import { ldmPaths } from './ldm.js';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const DEFAULT_PORT = 18790;
const AUTH_TOKEN = process.env.CRYSTAL_SERVE_TOKEN || '';

// ── Auth ──

function checkAuth(req: IncomingMessage): boolean {
  if (!AUTH_TOKEN) return true; // No token configured = no auth required
  const authHeader = req.headers.authorization;
  if (!authHeader) return false;
  return authHeader === `Bearer ${AUTH_TOKEN}`;
}

function sendJson(res: ServerResponse, status: number, body: any): void {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(body));
}

function send401(res: ServerResponse): void {
  sendJson(res, 401, { error: 'Unauthorized' });
}

// ── Request body parsing ──

function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (chunk) => { body += chunk; });
    req.on('end', () => resolve(body));
    req.on('error', reject);
    // 1MB limit
    req.on('data', () => {
      if (body.length > 1_000_000) {
        req.destroy();
        reject(new Error('Request body too large'));
      }
    });
  });
}

// ── Claude invocation (OpenAI-compatible) ──

async function handleChatCompletions(req: IncomingMessage, res: ServerResponse): Promise<void> {
  const raw = await readBody(req);
  let parsed: any;
  try {
    parsed = JSON.parse(raw);
  } catch {
    sendJson(res, 400, { error: 'Invalid JSON' });
    return;
  }

  const messages = parsed.messages;
  if (!messages || !Array.isArray(messages) || messages.length === 0) {
    sendJson(res, 400, { error: 'messages array required' });
    return;
  }

  // Extract the last user message as the prompt
  const lastUser = [...messages].reverse().find((m: any) => m.role === 'user');
  if (!lastUser) {
    sendJson(res, 400, { error: 'No user message found' });
    return;
  }

  const prompt = typeof lastUser.content === 'string'
    ? lastUser.content
    : Array.isArray(lastUser.content)
      ? lastUser.content.filter((b: any) => b.type === 'text').map((b: any) => b.text).join('\n')
      : '';

  if (!prompt) {
    sendJson(res, 400, { error: 'Empty prompt' });
    return;
  }

  // Extract system message if present
  const systemMsg = messages.find((m: any) => m.role === 'system');
  const systemPrompt = systemMsg
    ? (typeof systemMsg.content === 'string' ? systemMsg.content : '')
    : undefined;

  try {
    const args = ['-p', prompt];
    if (systemPrompt) args.push('--system', systemPrompt);
    args.push('--output-format', 'text');

    const result = await new Promise<string>((resolve, reject) => {
      const proc = spawn('claude', args, {
        stdio: ['ignore', 'pipe', 'pipe'],
        env: { ...process.env },
        timeout: 300_000,
      });

      let stdout = '';
      let stderr = '';
      proc.stdout.on('data', (data: Buffer) => { stdout += data.toString(); });
      proc.stderr.on('data', (data: Buffer) => { stderr += data.toString(); });

      proc.on('close', (code) => {
        if (code === 0) resolve(stdout.trim());
        else reject(new Error(`claude exited ${code}: ${stderr.slice(0, 300)}`));
      });
      proc.on('error', reject);
    });

    // Return OpenAI-compatible response
    sendJson(res, 200, {
      id: `crystal-${Date.now()}`,
      object: 'chat.completion',
      created: Math.floor(Date.now() / 1000),
      model: 'claude-opus-4-6',
      choices: [{
        index: 0,
        message: { role: 'assistant', content: result },
        finish_reason: 'stop',
      }],
    });
  } catch (err: any) {
    sendJson(res, 500, { error: err.message });
  }
}

// ── Process trigger ──

async function handleProcess(req: IncomingMessage, res: ServerResponse): Promise<void> {
  const raw = await readBody(req);
  let parsed: any;
  try {
    parsed = JSON.parse(raw);
  } catch {
    sendJson(res, 400, { error: 'Invalid JSON' });
    return;
  }

  const agentId = parsed.agent_id || parsed.agentId;
  const action = parsed.action || 'dream-weave';

  if (!agentId) {
    sendJson(res, 400, { error: 'agent_id required' });
    return;
  }

  // Spawn the action as a child process
  const args: string[] = [];
  if (action === 'backfill') {
    args.push('backfill', '--agent', agentId);
  } else if (action === 'dream-weave') {
    args.push('dream-weave', '--agent', agentId, '--mode', parsed.mode || 'incremental');
  } else {
    sendJson(res, 400, { error: `Unknown action: ${action}` });
    return;
  }

  // Run asynchronously, return immediately
  try {
    const proc = spawn('crystal', args, {
      stdio: 'ignore',
      detached: true,
      env: { ...process.env },
    });
    proc.unref();

    sendJson(res, 202, {
      status: 'accepted',
      action,
      agent_id: agentId,
      message: `${action} started for ${agentId}`,
    });
  } catch (err: any) {
    sendJson(res, 500, { error: err.message });
  }
}

// ── Status ──

function handleStatus(_req: IncomingMessage, res: ServerResponse): void {
  const paths = ldmPaths();
  const hasDb = existsSync(paths.crystalDb);

  // Check Dream Weaver watermark
  let lastDreamWeaver: string | null = null;
  const agentId = process.env.CRYSTAL_AGENT_ID || 'cc-mini';
  const wmPath = join(paths.state, `dream-weaver-${agentId}.json`);
  if (existsSync(wmPath)) {
    try {
      const wm = JSON.parse(readFileSync(wmPath, 'utf-8'));
      lastDreamWeaver = wm.lastRunAt || null;
    } catch {}
  }

  // Check role
  let role = 'standalone';
  const rolePath = join(paths.state, 'role.json');
  if (existsSync(rolePath)) {
    try {
      const r = JSON.parse(readFileSync(rolePath, 'utf-8'));
      role = r.role || 'standalone';
    } catch {}
  }

  sendJson(res, 200, {
    status: 'ok',
    role,
    agentId,
    hasDatabase: hasDb,
    lastDreamWeaver,
    uptime: process.uptime(),
    version: '0.6.0',
  });
}

// ── Server ──

export function startServer(port: number = DEFAULT_PORT): void {
  const server = createServer(async (req, res) => {
    const url = req.url || '';
    const method = req.method || 'GET';

    // CORS headers (localhost only, but helpful for local dev)
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }

    // Auth check (skip for status)
    if (url !== '/status' && !checkAuth(req)) {
      send401(res);
      return;
    }

    try {
      if (method === 'POST' && url === '/v1/chat/completions') {
        await handleChatCompletions(req, res);
      } else if (method === 'POST' && url === '/process') {
        await handleProcess(req, res);
      } else if (method === 'GET' && url === '/status') {
        handleStatus(req, res);
      } else {
        sendJson(res, 404, { error: 'Not found' });
      }
    } catch (err: any) {
      sendJson(res, 500, { error: err.message });
    }
  });

  // Localhost only. Never bind to 0.0.0.0.
  server.listen(port, '127.0.0.1', () => {
    console.log(`Crystal Core gateway listening on http://127.0.0.1:${port}`);
    console.log(`  POST /v1/chat/completions   (OpenAI-compatible)`);
    console.log(`  POST /process               (trigger backfill/dream-weaver)`);
    console.log(`  GET  /status                (health check)`);
    if (AUTH_TOKEN) {
      console.log(`  Auth: bearer token required`);
    } else {
      console.log(`  Auth: none (set CRYSTAL_SERVE_TOKEN to enable)`);
    }
  });

  // Graceful shutdown
  process.on('SIGTERM', () => {
    console.log('Crystal Core gateway shutting down...');
    server.close();
    process.exit(0);
  });

  process.on('SIGINT', () => {
    console.log('Crystal Core gateway shutting down...');
    server.close();
    process.exit(0);
  });
}

// ── CLI entry point ──

const args = process.argv.slice(2);
if (args.includes('--help') || args.includes('-h')) {
  console.log(`crystal serve [--port <port>]

Crystal Core gateway. Localhost-only HTTP server.

Options:
  --port <port>    Port to listen on (default: ${DEFAULT_PORT})

Environment:
  CRYSTAL_SERVE_TOKEN    Bearer token for auth (optional)
  CRYSTAL_AGENT_ID       Agent identifier (default: cc-mini)
`);
  process.exit(0);
}

const portFlag = args.indexOf('--port');
const port = portFlag >= 0 ? parseInt(args[portFlag + 1], 10) : DEFAULT_PORT;

startServer(port);
