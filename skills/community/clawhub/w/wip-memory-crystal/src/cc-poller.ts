#!/usr/bin/env node
// memory-crystal/cc-poller.ts — Unified continuous capture.
// Watches Claude Code JSONL session files on disk and does everything:
// Crystal ingestion, MD session export, daily log, transcript archive.
//
// Primary capture path: cron job via LDM Dev Tools (every minute).
// Backup: cc-hook.ts Stop hook calls the same logic as redundancy.
//
// This replaces three separate tools that all read the same JSONL:
//   1. cc-hook.ts (Crystal ingestion, Stop-only) ... now redundancy wrapper
//   2. cc-session-export (MD export, Stop-only) ... now merged here
//   3. cc-poller.ts (this file) ... the unified capture
//
// Usage:
//   node cc-poller.js                Run once (scan all sessions, capture everything)
//   node cc-poller.js --status       Show sync status for all sessions
//   node cc-poller.js --health       Run three-file health check
//   node cc-poller.js --watch        Run continuously (poll every 30 sec)

import { Crystal, resolveConfig, createCrystal, type Chunk, type CrystalConfig } from './core.js';
import { ensureLdm, ldmPaths, resolveStatePath, stateWritePath } from './ldm.js';
import {
  readFileSync, writeFileSync, appendFileSync, existsSync, mkdirSync,
  statSync, openSync, readSync, closeSync, copyFileSync, readdirSync,
} from 'node:fs';
import { join, basename, dirname } from 'node:path';

const HOME = process.env.HOME || '';
const CC_AGENT_ID = process.env.CRYSTAL_AGENT_ID || 'cc-mini';
const PRIVATE_MODE_PATH = resolveStatePath('memory-capture-state.json');
const WATERMARK_PATH = resolveStatePath('cc-capture-watermark.json');
const CC_ENABLED_PATH = resolveStatePath('cc-capture-enabled.json');
const CC_PROJECTS_DIR = join(HOME, '.claude', 'projects');
const SESSION_EXPORT_DIR = process.env.CRYSTAL_SESSION_EXPORT_DIR || join(ldmPaths().agentRoot, 'memory', 'sessions');
const EXPORT_WATERMARK_PATH = resolveStatePath('cc-export-watermark.json');

// ── Kill switches ──

function isPrivateMode(): boolean {
  try {
    if (existsSync(PRIVATE_MODE_PATH)) {
      const state = JSON.parse(readFileSync(PRIVATE_MODE_PATH, 'utf-8'));
      return state.enabled === false;
    }
  } catch {}
  return false;
}

function isCaptureEnabled(): boolean {
  try {
    if (existsSync(CC_ENABLED_PATH)) {
      const state = JSON.parse(readFileSync(CC_ENABLED_PATH, 'utf-8'));
      return state.enabled !== false;
    }
  } catch {}
  return true;
}

// ── Watermark (shared with cc-hook.ts) ──

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

// ── JSONL parsing (same as cc-hook.ts) ──

interface ExtractedMessage {
  role: string;
  text: string;
  timestamp: string;
  sessionId: string;
  model?: string;
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
        model: typeof msg.model === 'string' ? msg.model : undefined,
      });
    } catch {}
  }

  return { messages, newByteOffset: fileSize };
}

// ── Discover all JSONL session files ──

function discoverSessionFiles(): string[] {
  const files: string[] = [];
  if (!existsSync(CC_PROJECTS_DIR)) return files;

  try {
    for (const projectDir of readdirSync(CC_PROJECTS_DIR)) {
      const projectPath = join(CC_PROJECTS_DIR, projectDir);
      try {
        if (!statSync(projectPath).isDirectory()) continue;
      } catch { continue; }

      try {
        for (const file of readdirSync(projectPath)) {
          if (file.endsWith('.jsonl') && !file.startsWith('.')) {
            files.push(join(projectPath, file));
          }
        }
      } catch { continue; }
    }
  } catch {}

  return files;
}

// ── Daily log breadcrumb ──

function appendDailyLog(messages: ExtractedMessage[], sessionFile: string): void {
  try {
    const paths = ldmPaths();
    if (!existsSync(paths.root)) return;
    if (!existsSync(paths.daily)) mkdirSync(paths.daily, { recursive: true });

    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);
    const timeStr = now.toLocaleTimeString('en-US', {
      hour: '2-digit', minute: '2-digit', hour12: false,
      timeZone: 'America/Los_Angeles',
    });
    const logPath = join(paths.daily, `${dateStr}.md`);

    const userMsg = messages.find(m => m.role === 'user');
    if (!userMsg) return;
    const snippet = userMsg.text.slice(0, 120).replace(/\n/g, ' ').trim();

    const sessionId = basename(sessionFile, '.jsonl').slice(0, 8);
    const line = `- **${timeStr}** [${sessionId}] ${snippet}${userMsg.text.length > 120 ? '...' : ''}\n`;

    if (!existsSync(logPath)) {
      writeFileSync(logPath, `# ${dateStr} - CC Daily Log\n\n`);
    }

    appendFileSync(logPath, line);
  } catch {}
}

// ── JSONL transcript archive ──

function archiveTranscript(transcriptPath: string): void {
  try {
    if (isPrivateMode()) return;
    const paths = ensureLdm();
    const dest = join(paths.transcripts, basename(transcriptPath));
    if (existsSync(dest)) {
      const srcMtime = statSync(transcriptPath).mtimeMs;
      const dstMtime = statSync(dest).mtimeMs;
      if (srcMtime <= dstMtime) return;
    }
    copyFileSync(transcriptPath, dest);
  } catch {}
}

// ── MD session export (ported from cc-session-export) ──

function loadExportWatermark(): Record<string, number> {
  try {
    if (existsSync(EXPORT_WATERMARK_PATH)) {
      return JSON.parse(readFileSync(EXPORT_WATERMARK_PATH, 'utf-8'));
    }
  } catch {}
  return {};
}

function saveExportWatermark(data: Record<string, number>): void {
  const writePath = stateWritePath('cc-export-watermark.json');
  writeFileSync(writePath, JSON.stringify(data, null, 2));
}

function formatTimestamp(ts: string | null): string {
  if (!ts) return '';
  return new Date(ts).toLocaleString('en-US', {
    weekday: 'short', year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit', timeZoneName: 'short',
  });
}

function exportSessionToMarkdown(filePath: string): void {
  try {
    const exportWm = loadExportWatermark();
    const fileName = basename(filePath);
    const currentSize = statSync(filePath).size;
    const lastSize = exportWm[fileName] || 0;

    // Skip if unchanged
    if (currentSize === lastSize) return;

    if (!existsSync(SESSION_EXPORT_DIR)) mkdirSync(SESSION_EXPORT_DIR, { recursive: true });

    // Read full file for MD export (not incremental, full session each time)
    const content = readFileSync(filePath, 'utf-8');
    const lines = content.split('\n').filter(l => l.trim());

    const sessionId = basename(filePath, '.jsonl');
    let firstTs: string | null = null;
    let lastTs: string | null = null;
    let model = 'unknown';
    const turns: { role: string; content: string; timestamp: string | null }[] = [];

    for (const line of lines) {
      let entry: any;
      try { entry = JSON.parse(line); } catch { continue; }

      if (entry.type === 'file-history-snapshot') continue;

      if (entry.type === 'summary') {
        turns.push({ role: 'system', content: `*[Session continued. Summary provided.]*\n\n${entry.summary || ''}`, timestamp: entry.timestamp });
        continue;
      }

      const ts = entry.timestamp;
      if (ts && !firstTs) firstTs = ts;
      if (ts) lastTs = ts;
      if (entry.message?.model) model = entry.message.model;

      if (entry.type === 'user') {
        const text = extractContentText(entry.message?.content);
        if (text && !text.startsWith('<system-reminder>')) {
          turns.push({ role: 'human', content: text, timestamp: ts });
        }
      } else if (entry.type === 'assistant') {
        const text = extractContentText(entry.message?.content);
        if (text) turns.push({ role: 'assistant', content: text, timestamp: ts });
      }
    }

    let md = `# Claude Code Session\n\n`;
    md += `**Session ID:** \`${sessionId}\`\n`;
    md += `**Model:** ${model}\n`;
    md += `**Started:** ${formatTimestamp(firstTs)}\n`;
    md += `**Ended:** ${formatTimestamp(lastTs)}\n`;
    md += `**Turns:** ${turns.length}\n\n---\n\n`;

    for (const t of turns) {
      const time = t.timestamp ? `*${formatTimestamp(t.timestamp)}*` : '';
      if (t.role === 'human') {
        md += `## Parker\n${time ? time + '\n\n' : ''}${t.content}\n\n`;
      } else if (t.role === 'assistant') {
        md += `## Claude Code\n${time ? time + '\n\n' : ''}${t.content}\n\n`;
      } else {
        md += `---\n\n${t.content}\n\n---\n\n`;
      }
    }

    const mtime = statSync(filePath).mtime;
    const date = mtime.toISOString().split('T')[0];
    const shortId = sessionId.slice(0, 8);
    const outPath = join(SESSION_EXPORT_DIR, `${date}-session-${shortId}.md`);
    writeFileSync(outPath, md);

    exportWm[fileName] = currentSize;
    saveExportWatermark(exportWm);
  } catch {} // Non-fatal
}

function extractContentText(content: any): string {
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    return content.map((b: any) => {
      if (typeof b === 'string') return b;
      if (b.type === 'text') return b.text;
      if (b.type === 'tool_use') return `\`[Tool: ${b.name}]\``;
      return '';
    }).filter(Boolean).join('\n\n');
  }
  return '';
}

// ── Local ingest (same as cc-hook.ts) ──

const BATCH_SIZE = 200;

function isPermanentError(err: any): boolean {
  const msg = String(err?.message || err || '').toLowerCase();
  return msg.includes('api key required') || msg.includes('api key is required') || msg.includes('no llm provider') || msg.includes('no embedding provider') || msg.includes('no provider configured');
}

async function ingestLocal(messages: ExtractedMessage[], crystal: any): Promise<number> {
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
        model_id: msg.model,
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
          model_id: msg.model,
        });
      }
    }
  }

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

// ── Main: scan all sessions and ingest new turns ──

async function pollOnce(): Promise<{ filesScanned: number; chunksIngested: number; errors: string[] }> {
  if (isPrivateMode() || !isCaptureEnabled()) {
    return { filesScanned: 0, chunksIngested: 0, errors: [] };
  }

  const wm = loadWatermark();
  const sessionFiles = discoverSessionFiles();
  let totalChunks = 0;
  let filesScanned = 0;
  const errors: string[] = [];

  // Initialize Crystal once for all files
  let crystal: any = null;

  for (const filePath of sessionFiles) {
    filesScanned++;

    // CRITICAL FIX: On first encounter, start from byte 0 (ingest everything).
    // The old cc-hook seeds at file end, which SKIPS all existing history.
    // The poller must capture everything.
    if (!wm.files[filePath]) {
      wm.files[filePath] = { lastByteOffset: 0, lastTimestamp: new Date().toISOString() };
    }

    const lastOffset = wm.files[filePath].lastByteOffset;
    const fileSize = statSync(filePath).size;

    // Skip if no new data
    if (lastOffset >= fileSize) continue;

    const { messages, newByteOffset } = extractMessages(filePath, lastOffset);

    if (messages.length === 0) {
      wm.files[filePath] = { lastByteOffset: newByteOffset, lastTimestamp: new Date().toISOString() };
      continue;
    }

    const totalTokens = messages.reduce((sum, m) => sum + Math.ceil(m.text.length / 4), 0);

    // Lower threshold than cc-hook (100 tokens vs 500) for more responsive capture
    if (totalTokens < 100) {
      wm.files[filePath] = { lastByteOffset: newByteOffset, lastTimestamp: new Date().toISOString() };
      continue;
    }

    try {
      // Lazy init Crystal (only if we have something to ingest)
      if (!crystal) {
        const config = resolveConfig();
        crystal = createCrystal(config);
        await crystal.init();
      }

      const count = await ingestLocal(messages, crystal);
      totalChunks += count;

      wm.files[filePath] = { lastByteOffset: newByteOffset, lastTimestamp: new Date().toISOString() };

      // Archive transcript, write daily log, export MD session
      archiveTranscript(filePath);
      appendDailyLog(messages, filePath);
      exportSessionToMarkdown(filePath);

      process.stderr.write(`[cc-poller] ${count} chunks (${totalTokens} tokens) from ${basename(filePath)}\n`);
    } catch (err: any) {
      errors.push(`${basename(filePath)}: ${err.message}`);
      process.stderr.write(`[cc-poller] error on ${basename(filePath)}: ${err.message}\n`);
      // Don't update watermark on error so we retry next run
    }
  }

  saveWatermark(wm);
  return { filesScanned, chunksIngested: totalChunks, errors };
}

// ── Status command ──

function showStatus(): void {
  const wm = loadWatermark();
  const sessionFiles = discoverSessionFiles();

  console.log('CC Poller Status');
  console.log('================\n');
  console.log(`Capture: ${isCaptureEnabled() ? 'ON' : 'OFF'}`);
  console.log(`Private mode: ${isPrivateMode() ? 'ON (blocks capture)' : 'OFF'}`);
  console.log(`Agent ID: ${CC_AGENT_ID}`);
  console.log(`Last run: ${wm.lastRun || 'never'}`);
  console.log(`\nSession files: ${sessionFiles.length}\n`);

  for (const filePath of sessionFiles) {
    const fileSize = statSync(filePath).size;
    const wmEntry = wm.files[filePath];
    const lastOffset = wmEntry?.lastByteOffset || 0;
    const behind = fileSize - lastOffset;
    const mtime = statSync(filePath).mtime;
    const age = Date.now() - mtime.getTime();
    const ageStr = age < 60000 ? `${Math.round(age / 1000)}s ago`
      : age < 3600000 ? `${Math.round(age / 60000)}m ago`
      : age < 86400000 ? `${Math.round(age / 3600000)}h ago`
      : `${Math.round(age / 86400000)}d ago`;

    const status = behind === 0 ? 'IN SYNC'
      : behind < 1024 ? `${behind}B behind`
      : behind < 1048576 ? `${(behind / 1024).toFixed(1)}KB behind`
      : `${(behind / 1048576).toFixed(1)}MB behind`;

    const statusIcon = behind === 0 ? 'OK' : behind > 1048576 ? 'CRITICAL' : 'BEHIND';

    console.log(`  ${basename(filePath, '.jsonl').slice(0, 8)}  ${(fileSize / 1048576).toFixed(1)}MB  modified ${ageStr}  ${status}  ${statusIcon}`);
  }
}

// ── Health check ──

async function healthCheck(): Promise<void> {
  const wm = loadWatermark();
  const sessionFiles = discoverSessionFiles();

  console.log('Memory Crystal Health Check');
  console.log('===========================\n');

  // 1. Check JSONL files
  console.log('JSONL Sessions:');
  let activeFiles = 0;
  let totalBehind = 0;

  for (const filePath of sessionFiles) {
    const fileSize = statSync(filePath).size;
    const mtime = statSync(filePath).mtime;
    const age = Date.now() - mtime.getTime();
    const isActive = age < 7200000; // Modified in last 2 hours
    if (isActive) activeFiles++;

    const wmEntry = wm.files[filePath];
    const lastOffset = wmEntry?.lastByteOffset || 0;
    const behind = fileSize - lastOffset;
    totalBehind += behind;

    if (isActive || behind > 0) {
      const ageStr = age < 3600000 ? `${Math.round(age / 60000)}m ago` : `${Math.round(age / 3600000)}h ago`;
      const statusIcon = behind === 0 ? 'OK' : behind > 1048576 ? 'CRITICAL' : 'WARNING';
      console.log(`  ${basename(filePath, '.jsonl').slice(0, 8)}  ${(fileSize / 1048576).toFixed(1)}MB  last write: ${ageStr}  ${statusIcon}`);
    }
  }

  // 2. Check daily MD logs
  console.log('\nDaily MD Logs:');
  const paths = ldmPaths();
  const today = new Date().toISOString().slice(0, 10);
  const todayLog = join(paths.daily, `${today}.md`);

  if (existsSync(todayLog)) {
    const content = readFileSync(todayLog, 'utf-8');
    const lineCount = content.split('\n').filter(l => l.startsWith('- ')).length;
    console.log(`  ${today}.md exists, ${lineCount} entries  OK`);
  } else if (activeFiles > 0) {
    console.log(`  ${today}.md MISSING  WARNING: active sessions but no daily log`);
  } else {
    console.log(`  ${today}.md not created (no active sessions)  OK`);
  }

  // 3. Check Crystal chunks
  console.log('\nCrystal Chunks:');
  try {
    const config = resolveConfig();
    const crystal = createCrystal(config);
    await crystal.init();
    const status = await crystal.status();
    console.log(`  Total chunks: ${status.chunks}`);
    console.log(`  Total memories: ${status.memories}`);

    // Check for recent chunks
    // @ts-ignore - accessing internal db for health check
    if (crystal.db) {
      const recentRow = (crystal as any).db.prepare(
        "SELECT COUNT(*) as cnt FROM chunks WHERE created_at > datetime('now', '-2 hours')"
      ).get() as any;
      const latestRow = (crystal as any).db.prepare(
        "SELECT MAX(created_at) as latest FROM chunks"
      ).get() as any;

      if (recentRow.cnt > 0) {
        console.log(`  Chunks in last 2h: ${recentRow.cnt}  OK`);
      } else if (activeFiles > 0) {
        console.log(`  Chunks in last 2h: 0  CRITICAL: active sessions but no recent chunks`);
      }
      console.log(`  Latest chunk: ${latestRow.latest || 'none'}`);
    }
  } catch (err: any) {
    console.log(`  Error checking Crystal: ${err.message}  CRITICAL`);
  }

  // 4. Sync status
  console.log('\nSync Status:');
  if (totalBehind === 0) {
    console.log('  All sessions in sync  OK');
  } else {
    const behindStr = totalBehind > 1048576
      ? `${(totalBehind / 1048576).toFixed(1)}MB`
      : `${(totalBehind / 1024).toFixed(1)}KB`;
    console.log(`  Total data behind: ${behindStr}  ${totalBehind > 1048576 ? 'CRITICAL' : 'WARNING'}`);
  }

  console.log(`\nLast poller run: ${wm.lastRun || 'never'}`);
}

// ── Watch mode (continuous polling) ──

async function watchMode(): Promise<void> {
  const intervalMs = parseInt(process.env.CRYSTAL_POLL_INTERVAL || '30000', 10);
  process.stderr.write(`[cc-poller] watching every ${intervalMs / 1000}s. Ctrl+C to stop.\n`);

  while (true) {
    try {
      const result = await pollOnce();
      if (result.chunksIngested > 0) {
        process.stderr.write(`[cc-poller] ingested ${result.chunksIngested} chunks from ${result.filesScanned} files\n`);
      }
    } catch (err: any) {
      process.stderr.write(`[cc-poller] poll error: ${err.message}\n`);
    }
    await new Promise(r => setTimeout(r, intervalMs));
  }
}

// ── CLI ──

const args = process.argv.slice(2);

if (args.includes('--status')) {
  showStatus();
  process.exit(0);
}

if (args.includes('--health')) {
  healthCheck().then(() => process.exit(0)).catch(err => {
    console.error(err.message);
    process.exit(1);
  });
} else if (args.includes('--watch')) {
  watchMode().catch(err => {
    process.stderr.write(`[cc-poller] fatal: ${err.message}\n`);
    process.exit(1);
  });
} else {
  // Single run (for LaunchAgent)
  pollOnce().then(result => {
    if (result.chunksIngested > 0 || result.errors.length > 0) {
      process.stderr.write(`[cc-poller] done: ${result.chunksIngested} chunks, ${result.filesScanned} files, ${result.errors.length} errors\n`);
    }
    process.exit(result.errors.length > 0 ? 1 : 0);
  }).catch(err => {
    process.stderr.write(`[cc-poller] fatal: ${err.message}\n`);
    process.exit(1);
  });
}
