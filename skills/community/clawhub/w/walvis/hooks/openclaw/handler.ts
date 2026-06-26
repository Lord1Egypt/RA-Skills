import type { OpenClawEvent } from '@openclaw/types';
import { existsSync, readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const WALVIS_MANIFEST = join(homedir(), '.walvis', 'manifest.json');
const FASTPATH_STATE = join(homedir(), '.walvis', 'fastpath-state.json');
const URL_REGEX = /^https?:\/\/[^\s]+$/;
const WALVIS_CMD_REGEX = /^\/walvis(?:@[A-Za-z0-9_]+)?(?:\s+(.*))?$/i;

type WalvisManifest = {
  agent: string;
  autoSave?: boolean;
  fastPathEnabled?: boolean;
  activeSpace?: string;
};

type FastpathState = {
  pending?: Record<string, { type: string; itemId: string; updatedAt?: string }>;
};

function readManifestSafe(): WalvisManifest | null {
  try {
    if (!existsSync(WALVIS_MANIFEST)) return null;
    return JSON.parse(readFileSync(WALVIS_MANIFEST, 'utf-8'));
  } catch {
    return null;
  }
}

function readStateSafe(): FastpathState {
  try {
    if (!existsSync(FASTPATH_STATE)) return { pending: {} };
    const state = JSON.parse(readFileSync(FASTPATH_STATE, 'utf-8'));
    if (!state.pending || typeof state.pending !== 'object') state.pending = {};
    return state;
  } catch {
    return { pending: {} };
  }
}

function tokenize(input: string): string[] {
  const out: string[] = [];
  const re = /"([^"]*)"|'([^']*)'|(\S+)/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(input ?? '')) !== null) {
    out.push(match[1] ?? match[2] ?? match[3]);
  }
  return out;
}

function getIncomingText(event: OpenClawEvent): string | null {
  const context = (event as { context?: { content?: unknown; bodyForAgent?: unknown } }).context;
  if (context) {
    if (typeof context.bodyForAgent === 'string' && context.bodyForAgent.trim()) return context.bodyForAgent.trim();
    if (typeof context.content === 'string' && context.content.trim()) return context.content.trim();
  }

  const maybeMessages = (event as { messages?: Array<{ content?: string }> }).messages;
  if (Array.isArray(maybeMessages) && maybeMessages.length > 0) {
    return maybeMessages[maybeMessages.length - 1]?.content?.trim() ?? null;
  }

  return null;
}

function setIncomingText(event: OpenClawEvent, text: string): void {
  const context = (event as {
    context?: { content?: unknown; bodyForAgent?: unknown; body?: unknown };
  }).context;
  if (context) {
    if (typeof context.content === 'string') context.content = text;
    if (typeof context.bodyForAgent === 'string') context.bodyForAgent = text;
    if (typeof context.body === 'string') context.body = text;
  }

  const maybeMessages = (event as { messages?: Array<{ content?: string }> }).messages;
  if (Array.isArray(maybeMessages) && maybeMessages.length > 0) {
    maybeMessages[maybeMessages.length - 1].content = text;
  }
}

function buildParticipantKey(event: OpenClawEvent): string {
  const context = (event as {
    context?: {
      from?: string;
      channelId?: string;
      accountId?: string;
      metadata?: { senderId?: string };
    };
  }).context;
  const channel = context?.channelId ?? 'unknown';
  const account = context?.accountId ?? 'default';
  const sender = context?.metadata?.senderId ?? context?.from ?? 'unknown';
  return `${channel}:${account}:${sender}`;
}

function maybeRewritePending(event: OpenClawEvent): void {
  const incoming = getIncomingText(event);
  if (!incoming || incoming.startsWith('/')) return;
  const pending = readStateSafe().pending?.[buildParticipantKey(event)];
  if (!pending) return;
  setIncomingText(event, `/walvis-pending ${incoming}`);
}

function normalizeLegacyCallback(text: string): string | null {
  const trimmed = text.trim();
  if (!trimmed.startsWith('w:')) return null;
  if (trimmed.startsWith('w:page:') || trimmed.startsWith('w:sp:') || trimmed.startsWith('w:tags:') || trimmed.startsWith('w:note:') || trimmed.startsWith('w:del:') || trimmed.startsWith('w:ss:') || trimmed === 'w:cron:sync') {
    return `/walvis-callback ${trimmed}`;
  }
  return null;
}

function normalizeFastPathCommand(text: string): string | null {
  const legacy = normalizeLegacyCallback(text);
  if (legacy) return legacy;

  const match = text.trim().match(WALVIS_CMD_REGEX);
  if (!match) return null;

  const body = (match[1] ?? '').trim();
  if (!body) return '/walvis-list';

  const tokens = tokenize(body);
  const head = (tokens[0] ?? '').toLowerCase();
  const tail = body.slice(tokens[0]?.length ?? 0).trim();
  const push = (cmd: string, args?: string) => `/${cmd}${args ? ` ${args}` : ''}`;

  if (head === 'list' || head === '-ls') return push('walvis-list', tail);
  if (head === 'search' || head === '-q') return push('walvis-search', tail);
  if (head === 'fastpath' || head === 'fast' || head === 'fp') return push('walvis-fastpath', tail);
  if (head === 'new' || head === '-new' || head === '--new') return push('walvis-new', tail);
  if (head === 'use' || head === '-use' || head === '--use') return push('walvis-use', tail);
  if (head === 'sync' || head === '-s' || head === '--sync') return push('walvis-sync');
  if (head === 'spaces' || head === '-spaces') return push('walvis-spaces');
  if (head === 'status' || head === '-status' || head === '--status') return push('walvis-status');
  if (head === 'balance' || head === '-balance' || head === '--balance') return push('walvis-balance');
  if (head === 'web' || head === '-web' || head === '--web') return push('walvis-web');
  if (head === 'help' || head === '--help') return push('walvis-help');
  if (head === 'encrypt' || head === '-encrypt' || head === 'seal') return push('walvis-encrypt');
  if (head === 'share' || head === '-share') return push('walvis-share', tail);
  if (head === 'unshare' || head === '-unshare') return push('walvis-unshare', tail);
  if (head === 'seal-status' || head === '-seal') return push('walvis-seal-status');
  if (head === '+tag' || head === '+t') return push('walvis-tags-add', tail);
  if (head === '+note' || head === '+n') return push('walvis-note-add', tail);
  if (head === 'cancel') return push('walvis-cancel');

  return null;
}

function maybeRewriteFastPath(event: OpenClawEvent, fastPathEnabled: boolean): void {
  maybeRewritePending(event);
  const incoming = getIncomingText(event);
  if (!incoming) return;
  const rewritten = normalizeFastPathCommand(incoming);
  if (!rewritten) return;
  const isControlCommand = rewritten.startsWith('/walvis-fastpath');
  if (!fastPathEnabled && !isControlCommand) return;
  setIncomingText(event, rewritten);
}

export async function handler(event: OpenClawEvent): Promise<void> {
  if (event.type !== 'message:received' && event.type !== 'message:preprocessed') return;

  const manifest = readManifestSafe();
  const fastPathEnabled = process.env.WALVIS_FASTPATH === '1' || (manifest?.fastPathEnabled ?? true);
  maybeRewriteFastPath(event, fastPathEnabled);

  if (event.type !== 'message:received') return;
  if (!manifest?.autoSave) return;

  const text = getIncomingText(event);
  if (!text || !URL_REGEX.test(text)) return;
  setIncomingText(event, `@${manifest.agent} ${text}`);
}

export default handler;
