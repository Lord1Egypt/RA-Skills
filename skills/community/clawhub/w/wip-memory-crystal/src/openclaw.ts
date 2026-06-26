// memory-crystal/openclaw.ts — OpenClaw plugin wrapper.
// Thin layer calling core.ts via api.registerTool() and api.on().
// Replaces context-embeddings plugin.

import { Crystal, resolveConfig, type Chunk, type Memory } from './core.js';
import { runDevUpdate } from './dev-update.js';
import { resolveStatePath, stateWritePath, ldmPaths, ensureLdm } from './ldm.js';
import {
  existsSync, readFileSync, writeFileSync, readdirSync, copyFileSync, statSync, mkdirSync,
} from 'node:fs';
import { join, basename } from 'node:path';
import { createHash } from 'node:crypto';

const PRIVATE_MODE_PATH = resolveStatePath('memory-capture-state.json');

function isPrivateMode(): boolean {
  try {
    if (existsSync(PRIVATE_MODE_PATH)) {
      const state = JSON.parse(readFileSync(PRIVATE_MODE_PATH, 'utf-8'));
      return state.enabled === false;
    }
  } catch {
    // corrupted file = default to enabled (capture on)
  }
  return false;
}

// getPrivateState and setPrivateMode moved to lesa-private-mode plugin.
// Only isPrivateMode() is needed here for agent_end and crystal_remember checks.

// ── Raw data sync to LDM ──
// Copies session JSONLs, workspace .md files, and daily logs to LDM after every turn.
// Non-blocking, non-fatal. Uses idempotent copy (skip if same size).

const OC_AGENT_ID = 'oc-lesa-mini';

function syncRawDataToLdm(logger: any): void {
  try {
    const paths = ensureLdm(OC_AGENT_ID);
    const HOME = process.env.HOME || '';
    const ocDir = join(HOME, '.openclaw');

    // 1. Sync session JSONLs from ~/.openclaw/agents/main/sessions/
    const sessionsDir = join(ocDir, 'agents', 'main', 'sessions');
    if (existsSync(sessionsDir)) {
      let copied = 0;
      for (const file of readdirSync(sessionsDir)) {
        if (!file.endsWith('.jsonl')) continue;
        const src = join(sessionsDir, file);
        const dest = join(paths.transcripts, file);
        if (idempotentCopy(src, dest)) copied++;
      }
      if (copied > 0) logger.info(`memory-crystal: synced ${copied} session files to LDM`);
    }

    // 2. Sync workspace .md files from ~/.openclaw/workspace/
    const workspaceDir = join(ocDir, 'workspace');
    if (existsSync(workspaceDir)) {
      syncDirRecursive(workspaceDir, paths.workspace, '.md');
    }

    // 3. Sync daily logs from ~/.openclaw/workspace/memory/ to LDM daily/
    const dailyDir = join(ocDir, 'workspace', 'memory');
    if (existsSync(dailyDir)) {
      for (const file of readdirSync(dailyDir)) {
        if (!file.endsWith('.md')) continue;
        // Only sync date-formatted daily logs (YYYY-MM-DD.md)
        if (/^\d{4}-\d{2}-\d{2}\.md$/.test(file)) {
          const src = join(dailyDir, file);
          const dest = join(paths.daily, file);
          idempotentCopy(src, dest);
        }
      }
    }
  } catch (err: any) {
    logger.warn(`memory-crystal: raw data sync failed (non-fatal): ${err.message}`);
  }
}

/** Copy file only if source is newer or destination doesn't exist. Returns true if copied. */
function idempotentCopy(src: string, dest: string): boolean {
  try {
    if (existsSync(dest)) {
      const srcStat = statSync(src);
      const destStat = statSync(dest);
      if (srcStat.size === destStat.size && srcStat.mtimeMs <= destStat.mtimeMs) return false;
    }
    const destDir = join(dest, '..');
    if (!existsSync(destDir)) mkdirSync(destDir, { recursive: true });
    copyFileSync(src, dest);
    return true;
  } catch {
    return false;
  }
}

/** Recursively sync files with a given extension from srcDir to destDir. */
function syncDirRecursive(srcDir: string, destDir: string, ext: string): void {
  if (!existsSync(destDir)) mkdirSync(destDir, { recursive: true });
  for (const entry of readdirSync(srcDir, { withFileTypes: true })) {
    const srcPath = join(srcDir, entry.name);
    const destPath = join(destDir, entry.name);
    if (entry.isDirectory()) {
      syncDirRecursive(srcPath, destPath, ext);
    } else if (entry.name.endsWith(ext)) {
      idempotentCopy(srcPath, destPath);
    }
  }
}

// ── Workspace memory sync ──
// After each agent_end, check if workspace .md files changed since last capture.
// For changed files, ingest content into Crystal via remember().
// Uses file mtime as watermark to avoid re-ingesting unchanged files.

const WORKSPACE_WATERMARK_FILE = 'workspace-memory-watermarks.json';

type WatermarkMap = Record<string, WatermarkEntry | number>; // legacy: number = raw mtimeMs

function loadWatermarks(): WatermarkMap {
  try {
    const path = resolveStatePath(WORKSPACE_WATERMARK_FILE);
    if (existsSync(path)) {
      return JSON.parse(readFileSync(path, 'utf-8'));
    }
  } catch {
    // corrupted or missing ... start fresh
  }
  return {};
}

function saveWatermarks(watermarks: WatermarkMap): void {
  const path = stateWritePath(WORKSPACE_WATERMARK_FILE);
  writeFileSync(path, JSON.stringify(watermarks, null, 2), 'utf-8');
}

/**
 * Durable skip-cursor metadata. Tracks per-file ingest state so failed files
 * do not retry on every cycle. Hash-gated so content changes force a retry;
 * ingestVersion-gated so logic changes (e.g. chunking rollout) force a retry too.
 */
const WATERMARK_INGEST_VERSION = 2;

interface WatermarkEntry {
  mtime: number;
  hash?: string;
  failedKind?: 'permanent' | 'transient';
  failedAt?: number;
  ingestVersion?: number;
}

function hashContent(content: string): string {
  return createHash('sha256').update(content).digest('hex').slice(0, 16);
}

function isPermanentIngestError(err: any): boolean {
  const msg = String(err?.message || err || '').toLowerCase();
  return msg.includes('maximum input length')
    || msg.includes('8192 tokens')
    || msg.includes('too large')
    || msg.includes('api key required')
    || msg.includes('api key is required')
    || msg.includes('invalid api key')
    || msg.includes('unauthorized');
}

function shouldSkipFile(
  entry: WatermarkEntry | number | undefined,
  currentMtime: number,
  currentHash: string,
): boolean {
  if (entry == null) return false;
  // Legacy format: raw mtimeMs number. Skip if unchanged.
  if (typeof entry === 'number') return currentMtime <= entry;
  // Ingest logic bumped since entry was written ... force one retry (e.g. chunking rollout
  // should let old "embedding-too-large" failures succeed under the new code path).
  if ((entry.ingestVersion ?? 1) < WATERMARK_INGEST_VERSION) return false;
  // Success (no failure recorded) AND mtime unchanged → already ingested, skip.
  if (!entry.failedKind) return currentMtime <= entry.mtime;
  // Content changed (different hash) → retry.
  if (entry.hash != null && entry.hash !== currentHash) return false;
  // Permanent failure with same content → skip.
  if (entry.failedKind === 'permanent') return true;
  // Transient failure with same content → backoff 1 hour.
  if (entry.failedKind === 'transient') {
    const ageMs = Date.now() - (entry.failedAt ?? 0);
    return ageMs < 60 * 60 * 1000;
  }
  return false;
}

/** Valid memory categories from the Memory interface. */
const VALID_CATEGORIES: ReadonlySet<string> = new Set([
  'fact', 'preference', 'event', 'opinion', 'skill',
  'user', 'feedback', 'project', 'reference',
]);

/**
 * Parse YAML frontmatter from markdown content.
 * Looks for --- delimiters and extracts the `type` field.
 * No external YAML parser needed... just splits on `---`.
 */
function parseFrontmatterType(content: string): Memory['category'] | null {
  const trimmed = content.trimStart();
  if (!trimmed.startsWith('---')) return null;

  const endIdx = trimmed.indexOf('---', 3);
  if (endIdx === -1) return null;

  const frontmatter = trimmed.slice(3, endIdx);
  // Find the type field in the frontmatter block
  for (const line of frontmatter.split('\n')) {
    const match = line.match(/^\s*type\s*:\s*(.+?)\s*$/);
    if (match) {
      const value = match[1].replace(/^["']|["']$/g, ''); // strip quotes
      if (VALID_CATEGORIES.has(value)) {
        return value as Memory['category'];
      }
    }
  }
  return null;
}

/**
 * Collect workspace memory files to check:
 * ~/.openclaw/workspace/MEMORY.md and ~/.openclaw/workspace/memory/*.md
 */
function collectWorkspaceMemoryFiles(): string[] {
  const HOME = process.env.HOME || '';
  const workspaceDir = join(HOME, '.openclaw', 'workspace');
  const files: string[] = [];

  // Top-level MEMORY.md
  const memoryMd = join(workspaceDir, 'MEMORY.md');
  if (existsSync(memoryMd)) files.push(memoryMd);

  // All .md files in workspace/memory/
  const memoryDir = join(workspaceDir, 'memory');
  if (existsSync(memoryDir)) {
    for (const entry of readdirSync(memoryDir)) {
      if (entry.endsWith('.md')) {
        files.push(join(memoryDir, entry));
      }
    }
  }

  return files;
}

/**
 * Sync changed workspace memory files into Crystal.
 * Called from agent_end after conversation capture.
 * Returns the number of files ingested.
 */
async function syncWorkspaceMemory(
  crystal: Crystal,
  agentId: string,
  logger: any,
): Promise<number> {
  const watermarks = loadWatermarks();
  const files = collectWorkspaceMemoryFiles();
  let ingested = 0;

  for (const filePath of files) {
    try {
      const stat = statSync(filePath);
      const lastEntry = watermarks[filePath];
      const lastMtime = typeof lastEntry === 'number' ? lastEntry : 0;

      // Skip if file hasn't changed since last capture
      if (stat.mtimeMs <= lastMtime) continue;

      const content = readFileSync(filePath, 'utf-8');
      if (!content || content.trim().length < 50) continue; // Skip near-empty files
      const currentHash = hashContent(content);
      // Hash + failure-state gated skip (handles new-format WatermarkEntry; legacy mtime check above handles old entries).
      if (shouldSkipFile(watermarks[filePath], stat.mtimeMs, currentHash)) continue;

      // Determine category from frontmatter, default to 'fact'
      const category = parseFrontmatterType(content) || 'fact';

      // Ingest via remember() ... Crystal deduplicates internally via text_hash,
      // but we use the mtime watermark to avoid unnecessary embedding API calls.
      await crystal.remember(content, category);
      ingested++;

      // Update watermark for this file
      watermarks[filePath] = {
        mtime: stat.mtimeMs,
        hash: currentHash,
        ingestVersion: WATERMARK_INGEST_VERSION,
      };
    } catch (err: any) {
      logger.warn(`memory-crystal: workspace sync skipped ${basename(filePath)}: ${err.message}`);
      // N1 durable skip-cursor: record the failure so unchanged content isn't retried every cycle.
      try {
        const stat = statSync(filePath);
        const content = readFileSync(filePath, 'utf-8');
        const failedKind: 'permanent' | 'transient' = isPermanentIngestError(err) ? 'permanent' : 'transient';
        watermarks[filePath] = {
          mtime: stat.mtimeMs,
          hash: hashContent(content),
          failedKind,
          failedAt: Date.now(),
          ingestVersion: WATERMARK_INGEST_VERSION,
        };
      } catch { /* file re-read failed; leave watermark unchanged */ }
    }
  }

  // Always save watermarks ... N1 durable skip-cursor may have recorded failure state even when ingested === 0.
  saveWatermarks(watermarks);
  if (ingested > 0) {
    logger.info(`memory-crystal: synced ${ingested} workspace memory file(s) to Crystal`);
  }

  return ingested;
}

export default {
  register(api: any) {
    const crystal = new Crystal(resolveConfig());
    let initialized = false;

    async function ensureInit() {
      if (!initialized) {
        await crystal.init();
        initialized = true;
      }
    }

    // ── Hook: agent_end (continuous conversation ingestion) ──

    api.on('agent_end', async (event: any, ctx: any) => {
      // Private mode check
      if (isPrivateMode()) return;

      await ensureInit();

      const messages = event.messages;
      if (!messages || messages.length === 0) return;

      const agentId = ctx.agentId || OC_AGENT_ID;
      const sessionKey = ctx.sessionKey || 'unknown';

      // Check capture state
      const state = crystal.getCaptureState(agentId, sessionKey);
      const storedCount = state.lastMessageCount;

      // Detect compaction: messages array shrank below stored counter
      let startIndex = storedCount;
      if (messages.length < storedCount) {
        api.logger.info(`memory-crystal: compaction detected (${storedCount} → ${messages.length} messages), resetting capture position`);
        startIndex = 0;
      }

      if (messages.length <= startIndex) return; // Nothing new

      // Extract new conversation turns
      const newTurns: Chunk[] = [];
      for (let i = startIndex; i < messages.length; i++) {
        const msg = messages[i];
        if (!msg.content) continue;

        const role = msg.role;
        if (role !== 'user' && role !== 'assistant') continue;
        const model_id = typeof msg.model === 'string' ? msg.model : undefined;

        // Extract text from content (string or array)
        let text = '';
        if (typeof msg.content === 'string') {
          text = msg.content;
        } else if (Array.isArray(msg.content)) {
          text = msg.content
            .filter((b: any) => b.type === 'text')
            .map((b: any) => b.text)
            .join('\n');
        }

        if (!text || text.length < 50) continue; // Skip tiny messages

        // Turn-boundary chunking: one message = one chunk.
        // Only fall back to chunkText() for very long messages (>2000 tokens).
        const maxSingleChunkChars = 2000 * 4;
        if (text.length <= maxSingleChunkChars) {
          newTurns.push({
            text,
            role: role as 'user' | 'assistant',
            source_type: 'conversation',
            source_id: sessionKey,
            agent_id: agentId,
            token_count: Math.ceil(text.length / 4),
            created_at: new Date().toISOString(),
            model_id,
          });
        } else {
          // Very long message: chunk it, but preserve turn context
          const chunks = crystal.chunkText(text);
          for (const chunkText of chunks) {
            newTurns.push({
              text: chunkText,
              role: role as 'user' | 'assistant',
              source_type: 'conversation',
              source_id: sessionKey,
              agent_id: agentId,
              token_count: Math.ceil(chunkText.length / 4),
              created_at: new Date().toISOString(),
              model_id,
            });
          }
        }
      }

      // Skip if not enough new content
      const totalTokens = newTurns.reduce((sum, c) => sum + c.token_count, 0);
      if (totalTokens < 500) return;

      // Ingest
      try {
        const count = await crystal.ingest(newTurns);
        crystal.setCaptureState(agentId, sessionKey, messages.length, state.captureCount + 1);
        api.logger.info(`memory-crystal: ingested ${count} chunks from ${sessionKey} (cycle ${state.captureCount + 1})`);
      } catch (err: any) {
        api.logger.error(`memory-crystal: ingest error: ${err.message}`);
      }

      // Workspace memory sync (non-blocking, non-fatal)
      try {
        await syncWorkspaceMemory(crystal, agentId, api.logger);
      } catch (err: any) {
        api.logger.warn(`memory-crystal: workspace memory sync failed (non-fatal): ${err.message}`);
      }

      // Raw data sync to LDM (non-blocking, non-fatal)
      syncRawDataToLdm(api.logger);
    });

    // ── Tools ──
    // OpenClaw expects { content: [{ type: "text", text }] } return format

    function toolResult(text: string, isError = false) {
      return {
        content: [{ type: 'text' as const, text }],
        ...(isError ? { isError: true } : {}),
      };
    }

    api.registerTool(
      {
        name: 'crystal_search',
        label: 'Search Memory Crystal',
        description: 'Search memory crystal — semantic search across all conversations and stored memories.',
        parameters: {
          type: 'object',
          properties: {
            query: { type: 'string', description: 'What to search for' },
            limit: { type: 'number', description: 'Max results (default: 5)' },
            agent_id: { type: 'string', description: 'Filter by agent' },
          },
          required: ['query'],
        },
        async execute(_id: string, params: any) {
          try {
            await ensureInit();
            const results = await crystal.search(
              params.query,
              params.limit || 5,
              params.agent_id ? { agent_id: params.agent_id } : undefined
            );
            if (results.length === 0) return toolResult('No results found.');
            const formatted = results.map((r, i) => {
              const score = (r.score * 100).toFixed(1);
              const date = r.created_at?.slice(0, 10) || 'unknown';
              return `[${i + 1}] (${score}%, ${r.agent_id}, ${date}, ${r.role})\n${r.text}`;
            }).join('\n\n---\n\n');
            return toolResult(formatted);
          } catch (err: any) {
            return toolResult(`crystal_search error: ${err.message}`, true);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: 'crystal_remember',
        label: 'Remember in Crystal',
        description: 'Store a fact, preference, or observation in memory crystal.',
        parameters: {
          type: 'object',
          properties: {
            text: { type: 'string', description: 'The fact to remember' },
            category: { type: 'string', enum: ['fact', 'preference', 'event', 'opinion', 'skill', 'user', 'feedback', 'project', 'reference'] },
          },
          required: ['text'],
        },
        async execute(_id: string, params: any) {
          // Private mode blocks explicit memory writes too
          if (isPrivateMode()) {
            return toolResult('Private mode is on. No memories are being stored. Use /private-mode off to resume.');
          }
          try {
            await ensureInit();
            const id = await crystal.remember(params.text, params.category || 'fact');
            return toolResult(`Remembered (id: ${id}): ${params.text}`);
          } catch (err: any) {
            return toolResult(`crystal_remember error: ${err.message}`, true);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: 'crystal_forget',
        label: 'Forget Memory',
        description: 'Deprecate a memory by ID.',
        parameters: {
          type: 'object',
          properties: {
            id: { type: 'number', description: 'Memory ID to deprecate' },
          },
          required: ['id'],
        },
        async execute(_id: string, params: any) {
          try {
            await ensureInit();
            const ok = crystal.forget(params.id);
            return toolResult(ok ? `Forgot memory ${params.id}` : `Memory ${params.id} not found`);
          } catch (err: any) {
            return toolResult(`crystal_forget error: ${err.message}`, true);
          }
        },
      },
      { optional: true }
    );

    // ── Hook: before_compaction (auto dev updates) ──

    api.on('before_compaction', (_event: any, _ctx: any) => {
      try {
        const result = runDevUpdate('lesa');
        if (result.reposUpdated > 0) {
          api.logger.info(`memory-crystal: auto-dev-update wrote ${result.reposUpdated} updates before compaction`);
        }
      } catch (err: any) {
        api.logger.warn(`memory-crystal: auto-dev-update failed: ${err.message}`);
      }
    });

    api.logger.info('memory-crystal plugin registered');
  }
};
