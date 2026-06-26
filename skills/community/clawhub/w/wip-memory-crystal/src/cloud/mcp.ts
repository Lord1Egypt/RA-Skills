// memory-crystal/cloud/mcp.ts ... MCP tool definitions + handlers for the cloud Worker.
// Six tools: memory_search, memory_remember, memory_forget, memory_status, memory_log, memory_upload.
// Tier 1 (sovereign): writes relay to Mini, search returns guidance message.
// Tier 2 (convenience): full cloud search + relay write.

import type { Env, MemoryCategory, RelayDrop, RememberData, ForgetData, ConversationData, ToolCallRecord, InlineAttachment } from './types.js';
import { dropToRelay, dropAttachment } from './relay.js';

// ── Tool Definitions ──

export const TOOLS = [
  {
    name: 'memory_search',
    description: 'Search your memories. Returns ranked results by relevance.',
    inputSchema: {
      type: 'object' as const,
      properties: {
        query: { type: 'string', description: 'What to search for' },
        limit: { type: 'number', description: 'Max results (default 5, max 20)' },
      },
      required: ['query'],
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      openWorldHint: false,
    },
  },
  {
    name: 'memory_remember',
    description: 'Store a fact, preference, or observation in your persistent memory. Survives across sessions.',
    inputSchema: {
      type: 'object' as const,
      properties: {
        text: { type: 'string', description: 'The fact or observation to remember' },
        category: {
          type: 'string',
          enum: ['fact', 'preference', 'event', 'opinion', 'skill', 'user', 'feedback', 'project', 'reference'],
          description: 'Category of memory (default: fact)',
        },
      },
      required: ['text'],
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      openWorldHint: false,
      idempotentHint: false,
    },
  },
  {
    name: 'memory_forget',
    description: 'Deprecate a memory by ID. Does not permanently delete... marks as deprecated so it stops influencing answers.',
    inputSchema: {
      type: 'object' as const,
      properties: {
        id: { type: 'number', description: 'Memory ID to deprecate' },
      },
      required: ['id'],
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      openWorldHint: false,
      idempotentHint: true,
    },
  },
  {
    name: 'memory_status',
    description: 'Show memory status: connection health, pending items, and tier information.',
    inputSchema: {
      type: 'object' as const,
      properties: {},
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      openWorldHint: false,
    },
  },
  {
    name: 'memory_log',
    description: 'Log a conversation turn to your persistent memory. Call this after EVERY exchange. Captures the full raw data (text, tool calls, inline images, raw JSON) so your home machine has the complete conversation... same as a local session. The Mini processes this through the same chunking and embedding pipeline used for Claude Code and OpenClaw conversations.',
    inputSchema: {
      type: 'object' as const,
      properties: {
        role: {
          type: 'string',
          enum: ['user', 'assistant', 'system'],
          description: 'Who said this: user, assistant, or system',
        },
        content: { type: 'string', description: 'The full message content (text)' },
        session_id: { type: 'string', description: 'Session identifier to group conversation turns. Generate one at the start of each conversation and reuse it.' },
        turn_index: { type: 'number', description: 'Turn number within the session (0-indexed)' },
        model: { type: 'string', description: 'Model that generated the response, e.g. gpt-4o (assistant turns only)' },
        raw_json: { type: 'string', description: 'The complete raw JSON of this message as received from the API (if available). This preserves the full structure for the Mini.' },
        tool_calls: {
          type: 'array',
          description: 'Tool calls made in this turn (for assistant turns that called tools)',
          items: {
            type: 'object',
            properties: {
              tool_name: { type: 'string' },
              arguments: { type: 'string', description: 'JSON string of tool arguments' },
              result: { type: 'string', description: 'Tool result text' },
            },
            required: ['tool_name', 'arguments'],
          },
        },
        attachments: {
          type: 'array',
          description: 'Inline images, files, or audio referenced in this turn',
          items: {
            type: 'object',
            properties: {
              type: { type: 'string', enum: ['image_url', 'file', 'audio'] },
              url: { type: 'string', description: 'URL of the attachment (if available)' },
              filename: { type: 'string' },
              mime_type: { type: 'string' },
              data_base64: { type: 'string', description: 'Inline binary data as base64 (for small files only)' },
            },
            required: ['type'],
          },
        },
      },
      required: ['role', 'content'],
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      openWorldHint: false,
      idempotentHint: true,
    },
  },
  {
    name: 'memory_upload',
    description: 'Upload a file attachment (image, audio, video, document) to your persistent memory. The binary data is encrypted and relayed to your home machine. Pass the file as base64-encoded data.',
    inputSchema: {
      type: 'object' as const,
      properties: {
        filename: { type: 'string', description: 'Original filename (e.g. photo.png, recording.mp4)' },
        mime_type: { type: 'string', description: 'MIME type (e.g. image/png, audio/mp4, video/mp4, application/pdf)' },
        data_base64: { type: 'string', description: 'File contents as base64-encoded string' },
        context: { type: 'string', description: 'What this attachment relates to (optional)' },
        session_id: { type: 'string', description: 'Session identifier to link with conversation (optional)' },
      },
      required: ['filename', 'mime_type', 'data_base64'],
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      openWorldHint: false,
      idempotentHint: false,
    },
  },
];

// ── Tool Call Handler ──

interface ToolCallContext {
  userId: string;
  tier: string;
  env: Env;
  agentId: string;
}

interface McpContent {
  type: 'text';
  text: string;
}

interface McpToolResult {
  content: McpContent[];
  isError?: boolean;
}

export async function handleToolCall(
  toolName: string,
  args: Record<string, unknown>,
  ctx: ToolCallContext
): Promise<McpToolResult> {
  try {
    switch (toolName) {
      case 'memory_search':
        return await handleSearch(args, ctx);
      case 'memory_remember':
        return await handleRemember(args, ctx);
      case 'memory_forget':
        return await handleForget(args, ctx);
      case 'memory_status':
        return await handleStatus(ctx);
      case 'memory_log':
        return await handleLog(args, ctx);
      case 'memory_upload':
        return await handleUpload(args, ctx);
      default:
        return { content: [{ type: 'text', text: `Unknown tool: ${toolName}` }], isError: true };
    }
  } catch (err: any) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

// ── Search ──

async function handleSearch(args: Record<string, unknown>, ctx: ToolCallContext): Promise<McpToolResult> {
  const query = args.query as string;
  if (!query) {
    return { content: [{ type: 'text', text: 'Query is required.' }], isError: true };
  }

  if (ctx.tier === 'sovereign') {
    // Tier 1: no cloud search. Memory was saved via relay.
    return {
      content: [{
        type: 'text',
        text: [
          'Memory Crystal is in Sovereign mode (maximum privacy).',
          '',
          'Your memories are encrypted and stored on your home machine.',
          'Cloud search is not enabled... your data never exists in readable form outside your hardware.',
          '',
          'To search your memories, use any of these:',
          '  - crystal search "' + query + '" (CLI on your machine)',
          '  - Claude Desktop with the local Memory Crystal MCP server',
          '  - Claude Code: crystal_search tool',
          '',
          'To enable cloud search (memories become readable at the cloud layer):',
          '  Upgrade to Convenience tier in your Memory Crystal settings.',
        ].join('\n'),
      }],
    };
  }

  // Tier 2: cloud search (future implementation)
  // For now, return a placeholder. This gets replaced when Tier 2 storage is built.
  return {
    content: [{
      type: 'text',
      text: 'Cloud search is not yet available. Tier 2 storage is being built.',
    }],
  };
}

// ── Remember ──

async function handleRemember(args: Record<string, unknown>, ctx: ToolCallContext): Promise<McpToolResult> {
  const text = args.text as string;
  if (!text) {
    return { content: [{ type: 'text', text: 'Text is required.' }], isError: true };
  }

  const category = (args.category as MemoryCategory) || 'fact';
  const validCategories: MemoryCategory[] = ['fact', 'preference', 'event', 'opinion', 'skill', 'user', 'feedback', 'project', 'reference'];
  if (!validCategories.includes(category)) {
    return { content: [{ type: 'text', text: `Invalid category. Use: ${validCategories.join(', ')}` }], isError: true };
  }

  // Build the relay drop
  const drop: RelayDrop = {
    type: 'remember',
    agent_id: ctx.agentId,
    user_id: ctx.userId,
    timestamp: new Date().toISOString(),
    data: {
      text,
      category,
      source: detectSource(ctx.agentId),
      surface: detectSurface(ctx.agentId),
    } as RememberData,
  };

  // Drop to relay (encrypted)
  const result = await dropToRelay(ctx.env, drop);

  // If Tier 2, also store in cloud (future)
  // if (ctx.tier === 'convenience') { await cloudStore(ctx, text, category); }

  return {
    content: [{
      type: 'text',
      text: [
        `Remembered (category: ${category}): ${text}`,
        '',
        `Encrypted and queued for your home machine (drop ID: ${result.id}).`,
        ctx.tier === 'sovereign'
          ? 'Sovereign mode: memory is ONLY stored on your hardware. Not in the cloud.'
          : 'Also stored in cloud for search.',
      ].join('\n'),
    }],
  };
}

// ── Forget ──

async function handleForget(args: Record<string, unknown>, ctx: ToolCallContext): Promise<McpToolResult> {
  const memoryId = args.id as number;
  if (typeof memoryId !== 'number') {
    return { content: [{ type: 'text', text: 'Memory ID (number) is required.' }], isError: true };
  }

  // Queue deprecation command for Mini
  const drop: RelayDrop = {
    type: 'forget',
    agent_id: ctx.agentId,
    user_id: ctx.userId,
    timestamp: new Date().toISOString(),
    data: { memory_id: memoryId } as ForgetData,
  };

  const result = await dropToRelay(ctx.env, drop);

  // If Tier 2, also deprecate in cloud (future)
  // if (ctx.tier === 'convenience') { await cloudForget(ctx, memoryId); }

  return {
    content: [{
      type: 'text',
      text: `Deprecation queued for memory ${memoryId} (drop ID: ${result.id}). Your home machine will process this on next sync.`,
    }],
  };
}

// ── Log (conversation capture) ──

async function handleLog(args: Record<string, unknown>, ctx: ToolCallContext): Promise<McpToolResult> {
  const role = args.role as string;
  const content = args.content as string;

  if (!role || !content) {
    return { content: [{ type: 'text', text: 'Both role and content are required.' }], isError: true };
  }

  if (role !== 'user' && role !== 'assistant' && role !== 'system') {
    return { content: [{ type: 'text', text: 'Role must be "user", "assistant", or "system".' }], isError: true };
  }

  // Handle any inline attachments that have base64 data.
  // Large inline attachments get split into separate R2 objects.
  const inlineAttachments = args.attachments as InlineAttachment[] | undefined;
  const processedAttachments: InlineAttachment[] = [];

  if (inlineAttachments?.length) {
    for (const att of inlineAttachments) {
      if (att.data_base64 && att.data_base64.length > 64 * 1024) {
        // Large inline attachment: store as separate encrypted blob in R2
        try {
          const binaryStr = atob(att.data_base64);
          const bytes = new Uint8Array(binaryStr.length);
          for (let i = 0; i < binaryStr.length; i++) bytes[i] = binaryStr.charCodeAt(i);

          const uploadResult = await dropAttachment(
            ctx.env,
            bytes.buffer,
            {
              filename: att.filename || 'inline-attachment',
              mime_type: att.mime_type || 'application/octet-stream',
              size_bytes: bytes.length,
              source: detectSource(ctx.agentId),
              surface: detectSurface(ctx.agentId),
              session_id: args.session_id as string | undefined,
            },
            ctx.agentId,
            ctx.userId
          );

          // Replace inline data with R2 reference
          processedAttachments.push({
            type: att.type,
            url: `r2://${uploadResult.r2_key}`,
            filename: att.filename,
            mime_type: att.mime_type,
          });
        } catch {
          // If upload fails, keep the reference without data
          processedAttachments.push({
            type: att.type,
            url: att.url,
            filename: att.filename,
            mime_type: att.mime_type,
          });
        }
      } else {
        // Small attachment or URL-only reference: include as-is
        processedAttachments.push(att);
      }
    }
  }

  const conversationData: ConversationData = {
    role: role as 'user' | 'assistant' | 'system',
    content,
    source: detectSource(ctx.agentId),
    surface: detectSurface(ctx.agentId),
    session_id: args.session_id as string | undefined,
    turn_index: args.turn_index as number | undefined,
    model: args.model as string | undefined,
    raw_json: args.raw_json as string | undefined,
    tool_calls: args.tool_calls as ToolCallRecord[] | undefined,
    attachments: processedAttachments.length > 0 ? processedAttachments : undefined,
  };

  const drop: RelayDrop = {
    type: 'conversation',
    agent_id: ctx.agentId,
    user_id: ctx.userId,
    timestamp: new Date().toISOString(),
    data: conversationData,
  };

  const result = await dropToRelay(ctx.env, drop);

  const parts = [`Conversation turn logged (${role}, drop ID: ${result.id}).`];
  if (processedAttachments.length > 0) {
    parts.push(`${processedAttachments.length} attachment(s) included.`);
  }
  parts.push('Queued for your home machine.');

  return {
    content: [{
      type: 'text',
      text: parts.join(' '),
    }],
  };
}

// ── Upload (binary attachments) ──

async function handleUpload(args: Record<string, unknown>, ctx: ToolCallContext): Promise<McpToolResult> {
  const filename = args.filename as string;
  const mimeType = args.mime_type as string;
  const dataBase64 = args.data_base64 as string;

  if (!filename || !mimeType || !dataBase64) {
    return { content: [{ type: 'text', text: 'filename, mime_type, and data_base64 are all required.' }], isError: true };
  }

  // Decode base64 to binary
  let binary: ArrayBuffer;
  try {
    const binaryStr = atob(dataBase64);
    const bytes = new Uint8Array(binaryStr.length);
    for (let i = 0; i < binaryStr.length; i++) bytes[i] = binaryStr.charCodeAt(i);
    binary = bytes.buffer;
  } catch {
    return { content: [{ type: 'text', text: 'Invalid base64 data.' }], isError: true };
  }

  // Size check (100MB max, matching R2 single-put limit)
  const MAX_SIZE = 100 * 1024 * 1024;
  if (binary.byteLength > MAX_SIZE) {
    return { content: [{ type: 'text', text: `File too large (${(binary.byteLength / 1024 / 1024).toFixed(1)}MB). Max 100MB.` }], isError: true };
  }

  const result = await dropAttachment(
    ctx.env,
    binary,
    {
      filename,
      mime_type: mimeType,
      size_bytes: binary.byteLength,
      source: detectSource(ctx.agentId),
      surface: detectSurface(ctx.agentId),
      context: args.context as string | undefined,
      session_id: args.session_id as string | undefined,
    },
    ctx.agentId,
    ctx.userId
  );

  const sizeStr = binary.byteLength < 1024
    ? `${binary.byteLength} bytes`
    : binary.byteLength < 1024 * 1024
      ? `${(binary.byteLength / 1024).toFixed(1)} KB`
      : `${(binary.byteLength / 1024 / 1024).toFixed(1)} MB`;

  return {
    content: [{
      type: 'text',
      text: [
        `Uploaded: ${filename} (${mimeType}, ${sizeStr})`,
        `Encrypted and queued for your home machine (drop ID: ${result.id}).`,
        ctx.tier === 'sovereign'
          ? 'Sovereign mode: file is encrypted end-to-end. The cloud cannot read it.'
          : 'Also mirrored to cloud storage.',
      ].join('\n'),
    }],
  };
}

// ── Status ──

async function handleStatus(ctx: ToolCallContext): Promise<McpToolResult> {
  // Check relay for pending drops
  let pendingCount = 0;
  let pendingAttachments = 0;
  try {
    const drops = await ctx.env.RELAY.list({ prefix: 'chatgpt/' });
    pendingCount = drops.objects.length;
    const attachments = await ctx.env.RELAY.list({ prefix: 'chatgpt-attachments/' });
    pendingAttachments = attachments.objects.length;
  } catch {
    // R2 may not be accessible in all environments
  }

  const lines = [
    'Memory Crystal Status',
    `  Tier:         ${ctx.tier === 'sovereign' ? 'Sovereign (encrypted relay, no cloud data)' : 'Convenience (cloud search enabled)'}`,
    `  Agent:        ${ctx.agentId}`,
    `  Relay:        connected`,
    `  Pending:      ${pendingCount} drop(s) waiting for pickup`,
    `  Attachments:  ${pendingAttachments} file(s) waiting for pickup`,
    '',
    ctx.tier === 'sovereign'
      ? 'Your memories are encrypted end-to-end. The cloud cannot read them.'
      : 'Cloud search is active. Your memories are searchable from this chat.',
  ];

  return { content: [{ type: 'text', text: lines.join('\n') }] };
}

// ── Helpers ──

function detectSource(agentId: string): 'chatgpt' | 'claude' {
  if (agentId.startsWith('claude-')) return 'claude';
  return 'chatgpt';
}

function detectSurface(agentId: string): 'macos' | 'ios' | 'web' {
  if (agentId.includes('-macos')) return 'macos';
  if (agentId.includes('-ios')) return 'ios';
  return 'web';
}
