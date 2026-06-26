#!/usr/bin/env node
// memory-crystal/cc-hook.ts — Claude Code Stop hook (redundancy).
// Runs as a Stop hook in Claude Code settings.json. Acts as a final flush
// to catch anything the cron-based poller (cc-poller.ts) hasn't picked up yet.
//
// The cron job is the PRIMARY capture path (runs every minute).
// This hook is the BACKUP. If the poller already captured everything,
// this is a no-op (watermark is already current).
//
// Two modes:
//   LOCAL:  Ingests directly into local crystal (Mini)
//   RELAY:  Encrypts and drops at ephemeral relay Worker (Air/remote devices)
//
// Usage (Stop hook):
//   Receives JSON on stdin: { transcript_path, session_id, ... }
//
// Usage (CLI):
//   node cc-hook.js --on         Enable capture
//   node cc-hook.js --off        Disable capture
//   node cc-hook.js --status     Check state

import { Crystal, RemoteCrystal, resolveConfig, createCrystal, type Chunk } from './core.js';
import { loadRelayKey, encryptJSON } from './crypto.js';
import { ensureLdm, ldmPaths, resolveStatePath, stateWritePath, getAgentId } from './ldm.js';
import {
  readFileSync, writeFileSync, appendFileSync, existsSync, mkdirSync,
  statSync, openSync, readSync, closeSync, copyFileSync, readdirSync,
} from 'node:fs';
import { join, basename, dirname } from 'node:path';
import { createHash } from 'node:crypto';

const CC_AGENT_ID = getAgentId('claude-code');
const RELAY_URL = process.env.CRYSTAL_RELAY_URL || '';
const RELAY_TOKEN = process.env.CRYSTAL_RELAY_TOKEN || '';
const PRIVATE_MODE_PATH = resolveStatePath('memory-capture-state.json');
const WATERMARK_PATH = resolveStatePath('cc-capture-watermark.json');
const CC_ENABLED_PATH = resolveStatePath('cc-capture-enabled.json');
const MEMORY_SYNC_WATERMARK_PATH = resolveStatePath('cc-memory-sync-watermark.json');
const CLAUDE_PROJECTS_DIR = join(process.env.HOME || '', '.claude', 'projects');

// ── Mode detection ──

type CaptureMode = 'local' | 'relay';

function getCaptureMode(): CaptureMode {
  if (RELAY_URL && RELAY_TOKEN) return 'relay';
  return 'local';
}

// ── Private mode (shared with Lēsa's system) ──

function isPrivateMode(): boolean {
  try {
    if (existsSync(PRIVATE_MODE_PATH)) {
      const state = JSON.parse(readFileSync(PRIVATE_MODE_PATH, 'utf-8'));
      return state.enabled === false;
    }
  } catch {}
  return false;
}

// ── CC capture on/off switch ──

function isCaptureEnabled(): boolean {
  try {
    if (existsSync(CC_ENABLED_PATH)) {
      const state = JSON.parse(readFileSync(CC_ENABLED_PATH, 'utf-8'));
      return state.enabled !== false;
    }
  } catch {}
  return true; // Default: on
}

function setCaptureEnabled(enabled: boolean): void {
  const writePath = stateWritePath('cc-capture-enabled.json');
  writeFileSync(writePath, JSON.stringify({
    enabled,
    updatedAt: new Date().toISOString(),
  }, null, 2));
}

// ── Watermark ──

interface Watermark {
  files: Record<string, { lastByteOffset: number; lastTimestamp: string }>;
  lastRun: string | null;
}

function loadWatermark(): Watermark {
  try {
    if (existsSync(WATERMARK_PATH)) {
      return JSON.parse(readFileSync(WATERMARK_PATH, 'utf-8'));
    }
  } catch {}
  return { files: {}, lastRun: null };
}

function saveWatermark(wm: Watermark): void {
  const writePath = stateWritePath('cc-capture-watermark.json');
  wm.lastRun = new Date().toISOString();
  writeFileSync(writePath, JSON.stringify(wm, null, 2));
}

// ── Memory file sync watermark ──

interface MemorySyncWatermark {
  files: Record<string, { hash: string; syncedAt: string }>;
  lastRun: string | null;
}

function loadMemorySyncWatermark(): MemorySyncWatermark {
  try {
    if (existsSync(MEMORY_SYNC_WATERMARK_PATH)) {
      return JSON.parse(readFileSync(MEMORY_SYNC_WATERMARK_PATH, 'utf-8'));
    }
  } catch {}
  return { files: {}, lastRun: null };
}

function saveMemorySyncWatermark(wm: MemorySyncWatermark): void {
  const writePath = stateWritePath('cc-memory-sync-watermark.json');
  wm.lastRun = new Date().toISOString();
  writeFileSync(writePath, JSON.stringify(wm, null, 2));
}

function hashFileContent(content: string): string {
  return createHash('sha256').update(content).digest('hex');
}

// ── YAML frontmatter parser (no external deps) ──

interface MemoryFrontmatter {
  name?: string;
  description?: string;
  type?: string;
}

function parseFrontmatter(content: string): { frontmatter: MemoryFrontmatter; body: string } {
  const frontmatter: MemoryFrontmatter = {};

  // Check for --- delimited YAML frontmatter
  if (!content.startsWith('---')) {
    return { frontmatter, body: content };
  }

  const endIdx = content.indexOf('---', 3);
  if (endIdx === -1) {
    return { frontmatter, body: content };
  }

  const yamlBlock = content.slice(3, endIdx).trim();
  const body = content.slice(endIdx + 3).trim();

  // Parse simple key: value pairs
  for (const line of yamlBlock.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    const value = line.slice(colonIdx + 1).trim();
    if (key === 'name') frontmatter.name = value;
    else if (key === 'description') frontmatter.description = value;
    else if (key === 'type') frontmatter.type = value;
  }

  return { frontmatter, body };
}

// Valid CC memory categories (must match Memory['category'] in core.ts)
const VALID_CATEGORIES = new Set([
  'fact', 'preference', 'event', 'opinion', 'skill',
  'user', 'feedback', 'project', 'reference',
]);

type MemoryCategory = 'fact' | 'preference' | 'event' | 'opinion' | 'skill' | 'user' | 'feedback' | 'project' | 'reference';

// ── Memory file sync: scan and ingest CC auto-memory files ──

function discoverMemoryFiles(): string[] {
  const files: string[] = [];
  try {
    if (!existsSync(CLAUDE_PROJECTS_DIR)) return files;
    for (const project of readdirSync(CLAUDE_PROJECTS_DIR)) {
      const memDir = join(CLAUDE_PROJECTS_DIR, project, 'memory');
      if (!existsSync(memDir)) continue;
      try {
        for (const file of readdirSync(memDir)) {
          if (!file.endsWith('.md')) continue;
          files.push(join(memDir, file));
        }
      } catch {} // Skip unreadable dirs
    }
  } catch {} // Skip if projects dir unreadable
  return files;
}

async function syncMemoryFiles(): Promise<number> {
  if (isPrivateMode()) return 0;

  const files = discoverMemoryFiles();
  if (files.length === 0) return 0;

  const wm = loadMemorySyncWatermark();
  const changed: Array<{ path: string; content: string; hash: string; frontmatter: MemoryFrontmatter; body: string }> = [];

  for (const filePath of files) {
    try {
      const content = readFileSync(filePath, 'utf-8');
      if (content.trim().length === 0) continue;

      const hash = hashFileContent(content);

      // Skip if unchanged since last sync
      if (wm.files[filePath] && wm.files[filePath].hash === hash) continue;

      const { frontmatter, body } = parseFrontmatter(content);
      changed.push({ path: filePath, content, hash, frontmatter, body });
    } catch {} // Skip unreadable files
  }

  if (changed.length === 0) {
    saveMemorySyncWatermark(wm);
    return 0;
  }

  // Local mode: use crystal.remember() directly
  // Relay mode: not supported yet for memory files (only conversations)
  const mode = getCaptureMode();
  if (mode === 'relay') {
    // For relay mode, just update watermarks so we don't re-process.
    // Memory file relay support can be added later.
    process.stderr.write(`[cc-memory-sync] skipping ${changed.length} files (relay mode not yet supported)\n`);
    for (const item of changed) {
      wm.files[item.path] = { hash: item.hash, syncedAt: new Date().toISOString() };
    }
    saveMemorySyncWatermark(wm);
    return 0;
  }

  const config = resolveConfig();
  const crystal = createCrystal(config);
  await crystal.init();

  let ingested = 0;
  for (const item of changed) {
    try {
      // Determine category from frontmatter type, default to 'reference'
      const rawType = item.frontmatter.type || 'reference';
      const category: MemoryCategory = VALID_CATEGORIES.has(rawType) ? rawType as MemoryCategory : 'reference';

      // Build the text to remember: include name/description for context
      let text = '';
      if (item.frontmatter.name) {
        text += `[${item.frontmatter.name}] `;
      }
      if (item.body.length > 0) {
        text += item.body;
      } else {
        text += item.content;
      }

      if (text.trim().length < 10) continue;

      await crystal.remember(text.trim(), category);
      ingested++;

      // Update watermark for this file
      wm.files[item.path] = { hash: item.hash, syncedAt: new Date().toISOString() };
    } catch (err: any) {
      process.stderr.write(`[cc-memory-sync] error ingesting ${basename(item.path)}: ${err.message}\n`);
    }
  }

  saveMemorySyncWatermark(wm);
  return ingested;
}

// ── JSONL parsing ──

interface ExtractedMessage {
  role: string;
  text: string;
  timestamp: string;
  sessionId: string;
}

function extractMessages(filePath: string, lastByteOffset: number): {
  messages: ExtractedMessage[];
  newByteOffset: number;
} {
  const fileSize = statSync(filePath).size;
  if (lastByteOffset >= fileSize) {
    return { messages: [], newByteOffset: fileSize };
  }

  const fd = openSync(filePath, 'r');
  const bufSize = fileSize - lastByteOffset;
  const buf = Buffer.alloc(bufSize);
  readSync(fd, buf, 0, bufSize, lastByteOffset);
  closeSync(fd);

  const lines = buf.toString('utf-8').split('\n').filter(Boolean);
  const messages: ExtractedMessage[] = [];

  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      if (obj.type !== 'user' && obj.type !== 'assistant') continue;

      const msg = obj.message;
      if (!msg) continue;

      let text = '';
      if (typeof msg.content === 'string') {
        text = msg.content;
      } else if (Array.isArray(msg.content)) {
        const parts: string[] = [];
        for (const block of msg.content) {
          if (block.type === 'text' && block.text) parts.push(block.text);
          if (block.type === 'thinking' && block.thinking) parts.push(`[thinking] ${block.thinking}`);
        }
        text = parts.join('\n\n');
      }

      if (text.length < 20) continue;

      messages.push({
        role: msg.role || obj.type,
        text,
        timestamp: obj.timestamp || new Date().toISOString(),
        sessionId: obj.sessionId || 'unknown',
      });
    } catch {}
  }

  return { messages, newByteOffset: fileSize };
}

// ── JSONL transcript archive ──

function archiveTranscript(transcriptPath: string, agentId?: string): void {
  try {
    if (isPrivateMode()) return;
    const paths = ensureLdm(agentId);
    const dest = join(paths.transcripts, basename(transcriptPath));
    // Only copy if source is newer than destination (mtime check)
    if (existsSync(dest)) {
      const srcMtime = statSync(transcriptPath).mtimeMs;
      const dstMtime = statSync(dest).mtimeMs;
      if (srcMtime <= dstMtime) return;
    }
    // copyFileSync imported at top of file
    copyFileSync(transcriptPath, dest);
  } catch {} // Non-fatal
}

// archiveTranscript: copies JSONL to ~/.ldm/agents/{id}/transcripts/
// Called early in main(), after kill-switch checks, before watermark logic.

// ── Daily log breadcrumb ──

function appendDailyLog(messages: ExtractedMessage[], agentId?: string): void {
  try {
    const paths = ldmPaths(agentId);
    if (!existsSync(paths.root)) return; // LDM not scaffolded
    if (!existsSync(paths.daily)) mkdirSync(paths.daily, { recursive: true });

    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);
    const timeStr = now.toLocaleTimeString('en-US', {
      hour: '2-digit', minute: '2-digit', hour12: false,
      timeZone: 'America/Los_Angeles',
    });
    const logPath = join(paths.daily, `${dateStr}.md`);

    // Extract first user message as snippet
    const userMsg = messages.find(m => m.role === 'user');
    if (!userMsg) return;
    const snippet = userMsg.text.slice(0, 120).replace(/\n/g, ' ').trim();

    const line = `- **${timeStr}** ${snippet}${userMsg.text.length > 120 ? '...' : ''}\n`;

    // Create file with header if new
    if (!existsSync(logPath)) {
      writeFileSync(logPath, `# ${dateStr} - CC Daily Log\n\n`);
    }

    appendFileSync(logPath, line);
  } catch {} // Fail silently
}

// ── Relay mode: encrypt and drop at Worker ──

async function dropAtRelay(messages: ExtractedMessage[]): Promise<number> {
  const relayKey = loadRelayKey();

  // Package messages for relay
  const payload = {
    agent_id: CC_AGENT_ID,
    dropped_at: new Date().toISOString(),
    messages: messages.map(m => ({
      text: m.text,
      role: m.role,
      timestamp: m.timestamp,
      sessionId: m.sessionId,
    })),
  };

  // Encrypt
  const encrypted = encryptJSON(payload, relayKey);
  const body = JSON.stringify(encrypted);

  // Drop at Worker with retry
  let retries = 0;
  while (retries < 4) {
    try {
      const resp = await fetch(`${RELAY_URL}/drop/conversations`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${RELAY_TOKEN}`,
          'Content-Type': 'application/octet-stream',
        },
        body,
      });

      if (!resp.ok) {
        const err = await resp.text();
        throw new Error(`Relay drop failed: ${resp.status} ${err}`);
      }

      const result = await resp.json() as any;
      return messages.length;
    } catch (err: any) {
      retries++;
      if (retries >= 4) throw err;
      const delay = Math.min(1000 * 2 ** retries, 30000);
      process.stderr.write(`  [relay retry ${retries}] ${err.message}, waiting ${delay}ms\n`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  return 0;
}

// ── Relay commands: send commands to Core ──

export async function sendCommand(command: {
  action: string;
  agent_id?: string;
  mode?: string;
}): Promise<void> {
  if (!RELAY_URL || !RELAY_TOKEN) {
    throw new Error('Relay not configured. Set CRYSTAL_RELAY_URL and CRYSTAL_RELAY_TOKEN.');
  }

  const relayKey = loadRelayKey();
  const payload = {
    ...command,
    from_agent: CC_AGENT_ID,
    sent_at: new Date().toISOString(),
  };

  const encrypted = encryptJSON(payload, relayKey);
  const body = JSON.stringify(encrypted);

  const resp = await fetch(`${RELAY_URL}/drop/commands`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${RELAY_TOKEN}`,
      'Content-Type': 'application/octet-stream',
    },
    body,
  });

  if (!resp.ok) {
    throw new Error(`Command relay failed: ${resp.status} ${await resp.text()}`);
  }
}

// ── Local mode: direct ingest with batched retry ──

const BATCH_SIZE = 200;

function isPermanentError(err: any): boolean {
  const msg = String(err?.message || err || '').toLowerCase();
  return msg.includes('api key required') || msg.includes('api key is required') || msg.includes('no llm provider') || msg.includes('no embedding provider') || msg.includes('no provider configured');
}

async function ingestLocal(messages: ExtractedMessage[]): Promise<number> {
  const config = resolveConfig();
  const crystal = createCrystal(config);
  await crystal.init();

  // Turn-boundary chunking: one message = one chunk.
  // Only fall back to chunkText() for very long messages (>2000 tokens).
  const maxSingleChunkChars = 2000 * 4;
  const chunks: Chunk[] = [];
  for (const msg of messages) {
    if (msg.text.length <= maxSingleChunkChars) {
      chunks.push({
        text: msg.text,
        role: msg.role as 'user' | 'assistant',
        source_type: 'conversation',
        source_id: `cc:${msg.sessionId}`,
        agent_id: CC_AGENT_ID,
        token_count: Math.ceil(msg.text.length / 4),
        created_at: msg.timestamp,
      });
    } else {
      for (const ct of crystal.chunkText(msg.text)) {
        chunks.push({
          text: ct,
          role: msg.role as 'user' | 'assistant',
          source_type: 'conversation',
          source_id: `cc:${msg.sessionId}`,
          agent_id: CC_AGENT_ID,
          token_count: Math.ceil(ct.length / 4),
          created_at: msg.timestamp,
        });
      }
    }
  }

  // Batched ingest with retry
  let total = 0;
  for (let i = 0; i < chunks.length; i += BATCH_SIZE) {
    const batch = chunks.slice(i, i + BATCH_SIZE);
    let retries = 0;
    while (retries < 4) {
      try {
        total += await crystal.ingest(batch);
        break;
      } catch (err: any) {
        if (isPermanentError(err)) throw err;
        retries++;
        if (retries >= 4) throw err;
        const delay = Math.min(1000 * 2 ** retries, 30000);
        process.stderr.write(`  [retry ${retries}] ${err.message}, waiting ${delay}ms\n`);
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }
  return total;
}

// ── CLI commands ──

const args = process.argv.slice(2);

if (args.includes('--on')) {
  setCaptureEnabled(true);
  console.log('(*) Claude Code memory capture ON');
  process.exit(0);
}

if (args.includes('--off')) {
  setCaptureEnabled(false);
  console.log('( ) Claude Code memory capture OFF');
  process.exit(0);
}

if (args.includes('--status')) {
  const mode = getCaptureMode();
  console.log(isCaptureEnabled() ? '(*) CC capture: ON' : '( ) CC capture: OFF');
  console.log(isPrivateMode() ? '( ) Private mode: ON (blocks all capture)' : '(*) Private mode: OFF');
  console.log(`    Mode: ${mode}${mode === 'relay' ? ` (${RELAY_URL})` : ''}`);
  console.log(`    Agent ID: ${CC_AGENT_ID}`);
  process.exit(0);
}

// ── Stop hook handler ──

async function main(): Promise<void> {
  // Read hook JSON from stdin
  let input = '';
  for await (const chunk of process.stdin) {
    input += chunk;
  }

  let hookData: any;
  try {
    hookData = JSON.parse(input);
  } catch {
    process.exit(0);
  }

  const transcriptPath = hookData.transcript_path;
  if (!transcriptPath || !existsSync(transcriptPath)) process.exit(0);

  // Kill switches
  if (isPrivateMode() || !isCaptureEnabled()) process.exit(0);

  // Archive JSONL transcript to LDM (copy if newer)
  archiveTranscript(transcriptPath);

  const wm = loadWatermark();
  const fileKey = transcriptPath;

  // First encounter: start from byte 0 (capture everything).
  // The old behavior seeded at end-of-file, which SKIPPED all existing history.
  // The cron poller is the primary path and always starts from 0.
  // The Stop hook should match that behavior.
  if (!wm.files[fileKey]) {
    wm.files[fileKey] = { lastByteOffset: 0, lastTimestamp: new Date().toISOString() };
  }

  const lastOffset = wm.files[fileKey].lastByteOffset || 0;
  const { messages, newByteOffset } = extractMessages(transcriptPath, lastOffset);

  if (messages.length === 0) {
    wm.files[fileKey] = { lastByteOffset: newByteOffset, lastTimestamp: new Date().toISOString() };
    saveWatermark(wm);
    process.exit(0);
  }

  const totalTokens = messages.reduce((sum, m) => sum + Math.ceil(m.text.length / 4), 0);

  // Min threshold (matches poller)
  if (totalTokens < 100) {
    wm.files[fileKey] = { lastByteOffset: newByteOffset, lastTimestamp: new Date().toISOString() };
    saveWatermark(wm);
    process.exit(0);
  }

  const mode = getCaptureMode();

  try {
    if (mode === 'relay') {
      // Relay mode: encrypt and drop at Worker
      const count = await dropAtRelay(messages);
      process.stderr.write(`[cc-memory-capture] relayed ${count} messages (${totalTokens} tokens) from ${basename(transcriptPath)}\n`);
    } else {
      // Local mode: direct ingest into crystal
      const count = await ingestLocal(messages);
      process.stderr.write(`[cc-memory-capture] ${count} chunks (${totalTokens} tokens) from ${basename(transcriptPath)}\n`);
    }

    wm.files[fileKey] = { lastByteOffset: newByteOffset, lastTimestamp: new Date().toISOString() };
    saveWatermark(wm);

    // Append breadcrumb to LDM daily log
    appendDailyLog(messages);

    // Generate MD session summary (non-fatal)
    try {
      const { generateSessionSummary, writeSummaryFile } = await import('./summarize.js');
      const paths = ldmPaths();
      const summaryMsgs = messages.map(m => ({ role: m.role, text: m.text, timestamp: m.timestamp, sessionId: m.sessionId }));
      const summary = await generateSessionSummary(summaryMsgs);
      const sessionId = messages[0]?.sessionId || 'unknown';
      writeSummaryFile(paths.sessions, summary, CC_AGENT_ID, sessionId);
    } catch {} // Summary failure is non-fatal

    // Sync CC auto-memory files into Crystal (non-fatal)
    try {
      const syncCount = await syncMemoryFiles();
      if (syncCount > 0) {
        process.stderr.write(`[cc-memory-sync] ingested ${syncCount} changed memory file(s)\n`);
      }
    } catch (err: any) {
      process.stderr.write(`[cc-memory-sync] error: ${err.message}\n`);
    }

    // Dev updates disabled (2026-02-28). Was auto-generating files in every repo's
    // ai/ folder after each session. Created noise, not signal. If we bring this back,
    // it should be opt-in per repo, not a blanket scan.
  } catch (err: any) {
    if (isPermanentError(err)) {
      process.stderr.write(`[cc-memory-capture] skipped: ${err.message} (ensure OP_SERVICE_ACCOUNT_TOKEN is in env or set OPENAI_API_KEY)\n`);
      process.exit(0);
    }
    process.stderr.write(`[cc-memory-capture] error: ${err.message}\n`);
    process.exit(1);
  }
}

main();
