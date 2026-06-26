#!/usr/bin/env node
// memory-crystal/poller.ts ... Mini-side relay poller.
// Polls the ephemeral relay Worker for new drops from remote devices.
// Handles two channels:
//   conversations ... original CC/Lesa relay drops (bulk messages)
//   chatgpt       ... cloud MCP drops (individual: conversation, remember, forget, attachment)
// Verifies HMAC, decrypts, ingests into master crystal.
// Also pushes encrypted mirror snapshots for remote devices.
//
// Usage:
//   node poller.js                    Poll once (cron mode)
//   node poller.js --watch            Poll continuously (every 2 min)
//   node poller.js --push-delta       Export + encrypt + push delta chunks
//   node poller.js --push-delta --full Push all chunks (cold start / new node)
//   node poller.js --push-mirror      Legacy alias for --push-delta --full
//   node poller.js --status           Show relay status

import { Crystal, resolveConfig, type Chunk, type ExportedChunk } from './core.js';
import { loadRelayKey, decryptJSON, encryptJSON, encrypt, hashBuffer, type EncryptedPayload } from './crypto.js';
import { ensureLdm, ldmPaths, resolveStatePath, stateWritePath } from './ldm.js';
import { generateSessionSummary, writeSummaryFile, type SummaryMessage } from './summarize.js';
import { isNewAgent, ensureStaging, markReady } from './staging.js';
import { pushFileSync } from './file-sync.js';
import { readFileSync, writeFileSync, appendFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { createDecipheriv } from 'node:crypto';

const RELAY_URL = process.env.CRYSTAL_RELAY_URL || '';
const RELAY_TOKEN = process.env.CRYSTAL_RELAY_TOKEN || '';
const POLLER_STATE_PATH = resolveStatePath('relay-poller-state.json');

interface PollerState {
  lastPoll: string | null;
  totalIngested: number;
  totalChatgptIngested: number;
  totalAttachments: number;
  lastMirrorPush: string | null;
  /** Watermark: highest chunk ID pushed to mirror channel (delta sync) */
  lastDeltaChunkId: number;
}

function loadState(): PollerState {
  try {
    if (existsSync(POLLER_STATE_PATH)) {
      const raw = JSON.parse(readFileSync(POLLER_STATE_PATH, 'utf-8'));
      return {
        lastPoll: raw.lastPoll ?? null,
        totalIngested: raw.totalIngested ?? 0,
        totalChatgptIngested: raw.totalChatgptIngested ?? 0,
        totalAttachments: raw.totalAttachments ?? 0,
        lastMirrorPush: raw.lastMirrorPush ?? null,
        lastDeltaChunkId: raw.lastDeltaChunkId ?? 0,
      };
    }
  } catch {}
  return { lastPoll: null, totalIngested: 0, totalChatgptIngested: 0, totalAttachments: 0, lastMirrorPush: null, lastDeltaChunkId: 0 };
}

function saveState(state: PollerState): void {
  const writePath = stateWritePath('relay-poller-state.json');
  writeFileSync(writePath, JSON.stringify(state, null, 2));
}

// ── Relay message types (original conversations channel) ──

interface LegacyRelayDrop {
  agent_id: string;
  dropped_at: string;
  messages: Array<{
    text: string;
    role: string;
    timestamp: string;
    sessionId: string;
  }>;
}

// ── Cloud MCP drop types (chatgpt channel) ──

interface CloudDrop {
  type: 'remember' | 'forget' | 'conversation' | 'attachment';
  agent_id: string;
  user_id: string;
  timestamp: string;
  data: CloudRememberData | CloudForgetData | CloudConversationData | CloudAttachmentData;
}

interface CloudRememberData {
  text: string;
  category: string;
  source: string;
  surface: string;
}

interface CloudForgetData {
  memory_id: number;
  reason?: string;
}

interface CloudConversationData {
  role: string;
  content: string;
  source: string;
  surface: string;
  session_id?: string;
  turn_index?: number;
  model?: string;
  raw_json?: string;
  tool_calls?: Array<{ tool_name: string; arguments: string; result?: string }>;
  attachments?: Array<{ type: string; url?: string; filename?: string; mime_type?: string; data_base64?: string }>;
}

interface CloudAttachmentData {
  filename: string;
  mime_type: string;
  size_bytes: number;
  r2_key: string;
  source: string;
  surface: string;
  context?: string;
  session_id?: string;
}

interface BlobInfo {
  id: string;
  size: number;
  dropped_at: string;
  agent_id: string;
}

// ── Poll and ingest (original conversations channel) ──

async function pollConversations(crystal: Crystal, relayKey: Buffer): Promise<{ ingested: number; errors: number }> {
  let ingested = 0;
  let errors = 0;

  const listResp = await fetch(`${RELAY_URL}/pickup/conversations`, {
    headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
  });

  if (!listResp.ok) {
    throw new Error(`Relay list failed: ${listResp.status} ${await listResp.text()}`);
  }

  const listData = await listResp.json() as { count: number; blobs: BlobInfo[] };

  if (listData.count === 0) return { ingested: 0, errors: 0 };

  process.stderr.write(`[relay-poller] conversations: ${listData.count} blob(s) waiting\n`);

  for (const blob of listData.blobs) {
    try {
      const blobResp = await fetch(`${RELAY_URL}/pickup/conversations/${blob.id}`, {
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });

      if (!blobResp.ok) {
        process.stderr.write(`[relay-poller] failed to fetch blob ${blob.id}: ${blobResp.status}\n`);
        errors++;
        continue;
      }

      const encryptedText = await blobResp.text();
      const encrypted = JSON.parse(encryptedText) as EncryptedPayload;

      let drop: LegacyRelayDrop;
      try {
        drop = decryptJSON<LegacyRelayDrop>(encrypted, relayKey);
      } catch (err: any) {
        process.stderr.write(`[relay-poller] blob ${blob.id} failed verification: ${err.message} ... DISCARDED\n`);
        await fetch(`${RELAY_URL}/confirm/conversations/${blob.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
        });
        errors++;
        continue;
      }

      // Staging detection: if this is a new agent, route to staging
      if (isNewAgent(drop.agent_id)) {
        process.stderr.write(`[relay-poller] new agent "${drop.agent_id}" detected, routing to staging\n`);
        const staging = ensureStaging(drop.agent_id);
        // Write transcript to staging
        const jsonlPath = join(staging.transcripts, `relay-${blob.id}.jsonl`);
        const jsonlLines = drop.messages.map(m => JSON.stringify(m)).join('\n') + '\n';
        writeFileSync(jsonlPath, jsonlLines);
        // Mark as ready after all blobs for this agent are processed
        // (for now, mark ready on each blob; processStagedAgent handles idempotency)
        markReady(drop.agent_id);
        // Confirm receipt
        await fetch(`${RELAY_URL}/confirm/conversations/${blob.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
        });
        process.stderr.write(`[relay-poller] staged ${drop.messages.length} messages for ${drop.agent_id}\n`);
        continue;
      }

      // Build chunks from decrypted messages
      const maxSingleChunkChars = 2000 * 4;
      const chunks: Chunk[] = [];

      for (const msg of drop.messages) {
        if (msg.text.length <= maxSingleChunkChars) {
          chunks.push({
            text: msg.text,
            role: msg.role as 'user' | 'assistant',
            source_type: 'conversation',
            source_id: `cc:${msg.sessionId}`,
            agent_id: drop.agent_id,
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
              agent_id: drop.agent_id,
              token_count: Math.ceil(ct.length / 4),
              created_at: msg.timestamp,
            });
          }
        }
      }

      const count = await crystal.ingest(chunks);
      ingested += count;

      await fetch(`${RELAY_URL}/confirm/conversations/${blob.id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });

      process.stderr.write(`[relay-poller] blob ${blob.id}: ${count} chunks ingested from ${drop.agent_id}\n`);

      // Reconstruct remote agent's file tree on Mini
      try {
        const remotePaths = ensureLdm(drop.agent_id);

        const jsonlPath = join(remotePaths.transcripts, `relay-${blob.id}.jsonl`);
        const jsonlLines = drop.messages.map(m => JSON.stringify(m)).join('\n') + '\n';
        writeFileSync(jsonlPath, jsonlLines);

        const summaryMsgs: SummaryMessage[] = drop.messages.map(m => ({
          role: m.role,
          text: m.text,
          timestamp: m.timestamp,
          sessionId: m.sessionId,
        }));
        const summary = await generateSessionSummary(summaryMsgs);
        const sessionId = drop.messages[0]?.sessionId || 'unknown';
        writeSummaryFile(remotePaths.sessions, summary, drop.agent_id, sessionId);

        appendDailyBreadcrumb(drop.agent_id, drop.messages.find(m => m.role === 'user')?.text || '');
      } catch (fileErr: any) {
        process.stderr.write(`[relay-poller] file tree write failed (non-fatal): ${fileErr.message}\n`);
      }
    } catch (err: any) {
      process.stderr.write(`[relay-poller] error processing blob ${blob.id}: ${err.message}\n`);
      errors++;
    }
  }

  // Also poll commands channel and deliver to Crystal Core gateway
  try {
    await pollCommands();
  } catch (err: any) {
    process.stderr.write(`[relay-poller] commands poll failed (non-fatal): ${err.message}\n`);
  }

  return { ingested, errors };
}

// ── Poll ChatGPT channel (cloud MCP drops) ──

async function pollChatgpt(crystal: Crystal, relayKey: Buffer): Promise<{ ingested: number; attachments: number; errors: number }> {
  let ingested = 0;
  let attachments = 0;
  let errors = 0;

  // Poll metadata drops
  const listResp = await fetch(`${RELAY_URL}/pickup/chatgpt`, {
    headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
  });

  if (!listResp.ok) {
    process.stderr.write(`[relay-poller] chatgpt list failed: ${listResp.status}\n`);
    return { ingested: 0, attachments: 0, errors: 1 };
  }

  const listData = await listResp.json() as { count: number; blobs: BlobInfo[] };

  if (listData.count > 0) {
    process.stderr.write(`[relay-poller] chatgpt: ${listData.count} drop(s) waiting\n`);
  }

  for (const blob of listData.blobs) {
    try {
      const blobResp = await fetch(`${RELAY_URL}/pickup/chatgpt/${blob.id}`, {
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });

      if (!blobResp.ok) {
        process.stderr.write(`[relay-poller] chatgpt: failed to fetch ${blob.id}: ${blobResp.status}\n`);
        errors++;
        continue;
      }

      const encryptedText = await blobResp.text();
      const encrypted = JSON.parse(encryptedText) as EncryptedPayload;

      let drop: CloudDrop;
      try {
        drop = decryptJSON<CloudDrop>(encrypted, relayKey);
      } catch (err: any) {
        process.stderr.write(`[relay-poller] chatgpt: ${blob.id} failed verification: ${err.message} ... DISCARDED\n`);
        await confirmBlob('chatgpt', blob.id);
        errors++;
        continue;
      }

      // Route by drop type
      switch (drop.type) {
        case 'conversation': {
          const data = drop.data as CloudConversationData;
          const result = await ingestConversationDrop(crystal, drop, data);
          ingested += result;
          break;
        }
        case 'remember': {
          const data = drop.data as CloudRememberData;
          await crystal.remember(data.text, data.category as any);
          ingested++;
          process.stderr.write(`[relay-poller] chatgpt: remembered "${data.text.slice(0, 60)}..." (${data.category}) from ${drop.agent_id}\n`);
          break;
        }
        case 'forget': {
          const data = drop.data as CloudForgetData;
          const ok = crystal.forget(data.memory_id);
          process.stderr.write(`[relay-poller] chatgpt: forget memory #${data.memory_id} from ${drop.agent_id}: ${ok ? 'done' : 'not found'}\n`);
          break;
        }
        case 'attachment': {
          const data = drop.data as CloudAttachmentData;
          const result = await fetchAndSaveAttachment(data, drop.agent_id, relayKey);
          if (result) attachments++;
          break;
        }
        default:
          process.stderr.write(`[relay-poller] chatgpt: unknown drop type "${drop.type}" ... skipping\n`);
      }

      await confirmBlob('chatgpt', blob.id);
    } catch (err: any) {
      process.stderr.write(`[relay-poller] chatgpt: error processing ${blob.id}: ${err.message}\n`);
      errors++;
    }
  }

  // Also poll for attachment blobs that are standalone (not referenced by a metadata drop)
  // These get cleaned up separately since their metadata drops reference them
  const attResp = await fetch(`${RELAY_URL}/pickup/chatgpt-attachments`, {
    headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
  });

  if (attResp.ok) {
    const attData = await attResp.json() as { count: number; blobs: BlobInfo[] };
    if (attData.count > 0) {
      process.stderr.write(`[relay-poller] chatgpt-attachments: ${attData.count} blob(s) (cleaned up after metadata processing)\n`);
    }
    // Attachment blobs are fetched when processing their metadata drops.
    // Any orphaned blobs here get cleaned up by the 24h TTL cron.
  }

  return { ingested, attachments, errors };
}

// ── Ingest a single conversation turn from cloud MCP ──

async function ingestConversationDrop(crystal: Crystal, drop: CloudDrop, data: CloudConversationData): Promise<number> {
  const maxSingleChunkChars = 2000 * 4;
  const chunks: Chunk[] = [];
  const sessionTag = data.session_id ? `cloud:${data.session_id}` : `cloud:${drop.timestamp.slice(0, 10)}`;

  // Main text content
  const text = data.content;
  if (text.length <= maxSingleChunkChars) {
    chunks.push({
      text,
      role: data.role as 'user' | 'assistant',
      source_type: 'conversation',
      source_id: sessionTag,
      agent_id: drop.agent_id,
      token_count: Math.ceil(text.length / 4),
      created_at: drop.timestamp,
    });
  } else {
    for (const ct of crystal.chunkText(text)) {
      chunks.push({
        text: ct,
        role: data.role as 'user' | 'assistant',
        source_type: 'conversation',
        source_id: sessionTag,
        agent_id: drop.agent_id,
        token_count: Math.ceil(ct.length / 4),
        created_at: drop.timestamp,
      });
    }
  }

  // If there are tool calls, ingest those as separate chunks too
  if (data.tool_calls?.length) {
    for (const tc of data.tool_calls) {
      const toolText = `[Tool: ${tc.tool_name}] Args: ${tc.arguments}${tc.result ? `\nResult: ${tc.result}` : ''}`;
      chunks.push({
        text: toolText,
        role: 'assistant',
        source_type: 'tool_call',
        source_id: sessionTag,
        agent_id: drop.agent_id,
        token_count: Math.ceil(toolText.length / 4),
        created_at: drop.timestamp,
      });
    }
  }

  const count = await crystal.ingest(chunks);

  // Write raw JSON transcript
  try {
    const remotePaths = ensureLdm(drop.agent_id);
    const jsonlPath = join(remotePaths.transcripts, `cloud-${drop.timestamp.replace(/[:.]/g, '-')}.jsonl`);
    const line = JSON.stringify({
      type: 'conversation',
      agent_id: drop.agent_id,
      timestamp: drop.timestamp,
      role: data.role,
      content: data.content,
      session_id: data.session_id,
      turn_index: data.turn_index,
      model: data.model,
      tool_calls: data.tool_calls,
      raw_json: data.raw_json,
    });
    appendFileSync(jsonlPath, line + '\n');

    // Daily breadcrumb
    appendDailyBreadcrumb(drop.agent_id, data.role === 'user' ? data.content : `[${data.model || 'assistant'}] ${data.content.slice(0, 80)}`);
  } catch (fileErr: any) {
    process.stderr.write(`[relay-poller] chatgpt file tree write failed (non-fatal): ${fileErr.message}\n`);
  }

  if (count > 0) {
    process.stderr.write(`[relay-poller] chatgpt: ${count} chunk(s) from ${drop.agent_id} (${data.role}, turn ${data.turn_index ?? '?'})\n`);
  }

  return count;
}

// ── Fetch and save binary attachment ──

async function fetchAndSaveAttachment(data: CloudAttachmentData, agentId: string, relayKey: Buffer): Promise<boolean> {
  try {
    // The r2_key is in chatgpt-attachments/{id} format. Extract the blob ID.
    const blobId = data.r2_key.split('/').pop();
    if (!blobId) {
      process.stderr.write(`[relay-poller] chatgpt: invalid attachment r2_key: ${data.r2_key}\n`);
      return false;
    }

    // Fetch the encrypted binary from relay
    const blobResp = await fetch(`${RELAY_URL}/pickup/chatgpt-attachments/${blobId}`, {
      headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
    });

    if (!blobResp.ok) {
      process.stderr.write(`[relay-poller] chatgpt: failed to fetch attachment ${blobId}: ${blobResp.status}\n`);
      return false;
    }

    const encryptedText = await blobResp.text();
    const encryptedPayload = JSON.parse(encryptedText) as { v: number; nonce: string; data: string };

    // Decrypt: the cloud relay.ts uses AES-GCM with concatenated ciphertext+tag (Web Crypto format).
    // The "data" field is base64 of the raw AES-GCM encrypt() output (ciphertext + 16-byte auth tag).
    const nonce = Buffer.from(encryptedPayload.nonce, 'base64');
    const encryptedData = Buffer.from(encryptedPayload.data, 'base64');
    // Last 16 bytes are the GCM auth tag
    const ciphertext = encryptedData.subarray(0, encryptedData.length - 16);
    const tag = encryptedData.subarray(encryptedData.length - 16);

    const decipher = createDecipheriv('aes-256-gcm', relayKey, nonce);
    decipher.setAuthTag(tag);
    const decryptedBuf = Buffer.concat([decipher.update(ciphertext), decipher.final()]);

    // Save to agent's attachments directory
    const remotePaths = ensureLdm(agentId);
    const attachmentsDir = join(remotePaths.agentRoot, 'memory', 'attachments');
    if (!existsSync(attachmentsDir)) mkdirSync(attachmentsDir, { recursive: true });

    const safeFilename = data.filename.replace(/[^a-zA-Z0-9._-]/g, '_');
    const filePath = join(attachmentsDir, `${blobId}-${safeFilename}`);
    writeFileSync(filePath, decryptedBuf);

    // Write metadata sidecar
    const metaPath = filePath + '.meta.json';
    writeFileSync(metaPath, JSON.stringify({
      filename: data.filename,
      mime_type: data.mime_type,
      size_bytes: data.size_bytes,
      source: data.source,
      surface: data.surface,
      context: data.context,
      session_id: data.session_id,
      agent_id: agentId,
      saved_at: new Date().toISOString(),
    }, null, 2));

    // Confirm pickup of attachment blob
    await confirmBlob('chatgpt-attachments', blobId);

    process.stderr.write(`[relay-poller] chatgpt: saved attachment ${data.filename} (${data.mime_type}, ${(data.size_bytes / 1024).toFixed(1)}KB) from ${agentId}\n`);
    return true;
  } catch (err: any) {
    process.stderr.write(`[relay-poller] chatgpt: attachment save failed: ${err.message}\n`);
    return false;
  }
}

// ── Helpers ──

async function confirmBlob(channel: string, id: string): Promise<void> {
  await fetch(`${RELAY_URL}/confirm/${channel}/${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
  });
}

function appendDailyBreadcrumb(agentId: string, text: string): void {
  try {
    const remotePaths = ensureLdm(agentId);
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);
    const dailyPath = join(remotePaths.daily, `${dateStr}.md`);
    if (!existsSync(dailyPath)) {
      writeFileSync(dailyPath, `# ${dateStr} - ${agentId} Daily Log (via relay)\n\n`);
    }
    if (text) {
      const snippet = text.slice(0, 120).replace(/\n/g, ' ').trim();
      appendFileSync(dailyPath, `- **${now.toISOString().slice(11, 16)}** [relay] ${snippet}\n`);
    }
  } catch {}
}

// ── Main poll (both channels) ──

async function pollOnce(): Promise<{ ingested: number; errors: number; chatgptIngested: number; chatgptAttachments: number }> {
  if (!RELAY_URL || !RELAY_TOKEN) {
    throw new Error('CRYSTAL_RELAY_URL and CRYSTAL_RELAY_TOKEN must be set');
  }

  const relayKey = loadRelayKey();
  const config = resolveConfig();
  const crystal = new Crystal(config);
  await crystal.init();

  // Poll both channels
  const conv = await pollConversations(crystal, relayKey);
  const chatgpt = await pollChatgpt(crystal, relayKey);

  return {
    ingested: conv.ingested + chatgpt.ingested,
    errors: conv.errors + chatgpt.errors,
    chatgptIngested: chatgpt.ingested,
    chatgptAttachments: chatgpt.attachments,
  };
}

// ── Commands channel polling ──

interface RelayCommand {
  action: string;
  agent_id?: string;
  mode?: string;
  from_agent?: string;
  payload?: any;
}

async function pollCommands(): Promise<void> {
  const relayKey = loadRelayKey();

  const listResp = await fetch(`${RELAY_URL}/pickup/commands`, {
    headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
  });

  if (!listResp.ok) return;

  const listData = await listResp.json() as { count: number; blobs: BlobInfo[] };
  if (listData.count === 0) return;

  process.stderr.write(`[relay-poller] ${listData.count} command(s) waiting\n`);

  for (const blob of listData.blobs) {
    try {
      const blobResp = await fetch(`${RELAY_URL}/pickup/commands/${blob.id}`, {
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });

      if (!blobResp.ok) continue;

      const encryptedText = await blobResp.text();
      const encrypted = JSON.parse(encryptedText) as EncryptedPayload;

      let cmd: RelayCommand;
      try {
        cmd = decryptJSON<RelayCommand>(encrypted, relayKey);
      } catch {
        // Bad blob, delete and skip
        await fetch(`${RELAY_URL}/confirm/commands/${blob.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
        });
        continue;
      }

      // Deliver to Crystal Core gateway
      const gatewayPort = process.env.CRYSTAL_SERVE_PORT || '18790';
      try {
        const resp = await fetch(`http://127.0.0.1:${gatewayPort}/process`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: cmd.action || 'dream-weave',
            agent_id: cmd.agent_id,
            mode: cmd.mode,
          }),
        });

        if (resp.ok) {
          process.stderr.write(`[relay-poller] delivered command: ${cmd.action} for ${cmd.agent_id}\n`);
        } else {
          process.stderr.write(`[relay-poller] gateway rejected command: ${resp.status}\n`);
        }
      } catch (err: any) {
        // Gateway might not be running, that's ok
        process.stderr.write(`[relay-poller] gateway not available (non-fatal): ${err.message}\n`);
      }

      // Confirm receipt
      await fetch(`${RELAY_URL}/confirm/commands/${blob.id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });
    } catch (err: any) {
      process.stderr.write(`[relay-poller] command processing error: ${err.message}\n`);
    }
  }
}

// ── Push delta chunks (replaces full mirror) ──

interface DeltaPayload {
  version: number;
  sinceId: number;
  maxId: number;
  chunkCount: number;
  pushedAt: string;
  chunks: ExportedChunk[];
}

async function pushDelta(force?: boolean): Promise<void> {
  if (!RELAY_URL || !RELAY_TOKEN) {
    throw new Error('CRYSTAL_RELAY_URL and CRYSTAL_RELAY_TOKEN must be set');
  }

  const relayKey = loadRelayKey();
  const config = resolveConfig();
  const crystal = new Crystal(config);
  await crystal.init();

  const state = loadState();
  const sinceId = force ? 0 : (state.lastDeltaChunkId || 0);
  const maxId = crystal.getMaxChunkId();

  if (maxId <= sinceId) {
    process.stderr.write(`[relay-poller] no new chunks since ID ${sinceId}\n`);
    return;
  }

  const chunks = crystal.exportChunksSince(sinceId);
  if (chunks.length === 0) {
    process.stderr.write(`[relay-poller] no new chunks to push\n`);
    return;
  }

  const deltaPayload: DeltaPayload = {
    version: Crystal.DELTA_VERSION,
    sinceId,
    maxId,
    chunkCount: chunks.length,
    pushedAt: new Date().toISOString(),
    chunks,
  };

  // Encrypt the delta payload
  const encrypted = encryptJSON(deltaPayload, relayKey);

  // Drop at Worker mirror channel
  const resp = await fetch(`${RELAY_URL}/drop/mirror`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${RELAY_TOKEN}`,
      'Content-Type': 'application/octet-stream',
    },
    body: JSON.stringify(encrypted),
  });

  if (!resp.ok) {
    throw new Error(`Delta push failed: ${resp.status} ${await resp.text()}`);
  }

  // Update watermark
  state.lastDeltaChunkId = maxId;
  state.lastMirrorPush = new Date().toISOString();
  saveState(state);

  const payloadSize = JSON.stringify(encrypted).length;
  process.stderr.write(
    `[relay-poller] delta pushed: ${chunks.length} chunks (ID ${sinceId + 1}..${maxId}), ` +
    `${(payloadSize / 1024).toFixed(1)}KB\n`
  );
}

// ── Legacy: Push full mirror (for cold start / new nodes) ──

async function pushMirror(): Promise<void> {
  // Full mirror is now just a delta with sinceId=0
  await pushDelta(true);
}

// ── CLI ──

const args = process.argv.slice(2);

if (args.includes('--status')) {
  const state = loadState();
  const mode = (RELAY_URL && RELAY_TOKEN) ? 'configured' : 'not configured';
  console.log(`Relay poller status:`);
  console.log(`  Relay URL:         ${RELAY_URL || '(not set)'}`);
  console.log(`  Mode:              ${mode}`);
  console.log(`  Last poll:         ${state.lastPoll || 'never'}`);
  console.log(`  Total ingested:    ${state.totalIngested} (conversations)`);
  console.log(`  ChatGPT ingested:  ${state.totalChatgptIngested} (cloud MCP)`);
  console.log(`  Attachments saved: ${state.totalAttachments}`);
  console.log(`  Last delta:        ${state.lastMirrorPush || 'never'}`);
  console.log(`  Delta watermark:   chunk ID ${state.lastDeltaChunkId || 0}`);
  process.exit(0);
}

if (args.includes('--push-mirror') || args.includes('--push-delta')) {
  const full = args.includes('--full');
  pushDelta(full)
    .then(() => {
      process.exit(0);
    })
    .catch(err => {
      process.stderr.write(`[relay-poller] mirror push error: ${err.message}\n`);
      process.exit(1);
    });
} else if (args.includes('--watch')) {
  // Continuous polling mode
  const POLL_INTERVAL = 2 * 60 * 1000; // 2 minutes

  async function loop() {
    process.stderr.write(`[relay-poller] watching (every ${POLL_INTERVAL / 1000}s)...\n`);
    while (true) {
      try {
        const result = await pollOnce();
        const state = loadState();
        state.lastPoll = new Date().toISOString();
        state.totalIngested += result.ingested;
        state.totalChatgptIngested += result.chatgptIngested;
        state.totalAttachments += result.chatgptAttachments;
        saveState(state);

        const totalNew = result.ingested + result.chatgptAttachments;
        if (totalNew > 0) {
          process.stderr.write(`[relay-poller] poll complete: ${result.ingested} ingested, ${result.chatgptAttachments} attachments, ${result.errors} errors\n`);
          // Push delta chunks after successful ingestion
          try {
            await pushDelta();
          } catch (deltaErr: any) {
            process.stderr.write(`[relay-poller] delta push failed (non-fatal): ${deltaErr.message}\n`);
          }
        }

        // Push file tree sync (runs even without new chunks ... files change independently)
        try {
          const { manifest, files } = await pushFileSync();
          if (files > 0) {
            process.stderr.write(`[relay-poller] file sync pushed: ${files} files\n`);
          }
        } catch (fileSyncErr: any) {
          process.stderr.write(`[relay-poller] file sync failed (non-fatal): ${fileSyncErr.message}\n`);
        }
      } catch (err: any) {
        process.stderr.write(`[relay-poller] poll error: ${err.message}\n`);
      }
      await new Promise(r => setTimeout(r, POLL_INTERVAL));
    }
  }
  loop();
} else {
  // Single poll (cron mode)
  pollOnce()
    .then((result) => {
      const state = loadState();
      state.lastPoll = new Date().toISOString();
      state.totalIngested += result.ingested;
      state.totalChatgptIngested += result.chatgptIngested;
      state.totalAttachments += result.chatgptAttachments;
      saveState(state);

      const totalNew = result.ingested + result.chatgptAttachments;
      if (totalNew > 0) {
        process.stderr.write(`[relay-poller] ${result.ingested} chunks ingested, ${result.chatgptAttachments} attachments, ${result.errors} errors\n`);
      }
      process.exit(result.errors > 0 ? 1 : 0);
    })
    .catch(err => {
      process.stderr.write(`[relay-poller] error: ${err.message}\n`);
      process.exit(1);
    });
}
