import type { AdapterSignal } from '../types/adapterSignal';
import { classifyThreadHint } from './threadHints';

type UnknownRecord = Record<string, unknown>;

export interface GogGmailPayload {
  messages?: unknown[];
  count?: number;
}

const ACTIONABLE_KEYWORDS = [
  'reply',
  'callback',
  'call back',
  'deadline',
  'follow-up',
  'follow up',
  'followup',
  'claim',
  'approval',
  'approve',
  'review',
  'request',
  'please',
  'can you',
  'could you',
  'check',
  'action required',
  'response needed',
];

function asRecord(value: unknown): UnknownRecord | null {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return null;
  return value as UnknownRecord;
}

function firstString(record: UnknownRecord, keys: string[]): string | undefined {
  for (const key of keys) {
    const value = record[key];
    if (typeof value === 'string' && value.trim() !== '') return value.trim();
  }
  return undefined;
}

function scoreMessage(record: UnknownRecord): number {
  const subject = firstString(record, ['subject']) ?? '';
  const snippet = firstString(record, ['snippet', 'body']) ?? '';
  const combined = `${subject} ${snippet}`.toLowerCase();
  let score = 0;
  for (const kw of ACTIONABLE_KEYWORDS) {
    if (combined.includes(kw)) score++;
  }
  return score;
}

function buildText(record: UnknownRecord): string {
  const subject = firstString(record, ['subject']);
  const from = firstString(record, ['from', 'sender']);
  const snippet = firstString(record, ['snippet', 'body']);
  const hint = classifyThreadHint({ subject, snippet });

  const parts: string[] = [];
  if (subject) parts.push(`subject=${subject}`);
  if (from) parts.push(`from=${from}`);
  if (snippet) parts.push(`snippet=${snippet}`);
  if (hint) parts.push(`thread_hint=${hint}`);

  return parts.length > 0 ? `gog Gmail: ${parts.join(' | ')}` : 'gog Gmail message';
}

export function isGogGmailPayload(raw: unknown): raw is GogGmailPayload {
  if (typeof raw !== 'object' || raw === null || Array.isArray(raw)) return false;
  const obj = raw as UnknownRecord;
  return (
    Array.isArray(obj.messages) &&
    typeof obj.text !== 'string' &&
    typeof obj.source === 'undefined'
  );
}

export function gogGmailToAdapterSignal(payload: GogGmailPayload): AdapterSignal {
  const messages = (payload.messages ?? [])
    .map(asRecord)
    .filter((m): m is UnknownRecord => m !== null);

  if (messages.length === 0) {
    return {
      source: 'gmail',
      sourceType: 'message',
      externalWrite: false,
      text: 'gog Gmail: no messages',
      observedAt: new Date().toISOString(),
    };
  }

  let best = messages[0];
  let bestScore = scoreMessage(messages[0]);
  for (let i = 1; i < messages.length; i++) {
    const score = scoreMessage(messages[i]);
    if (score > bestScore) {
      bestScore = score;
      best = messages[i];
    }
  }

  const threadId = firstString(best, ['threadId', 'thread_id']);
  const sourceType = threadId ? 'thread' : 'message';
  const text = buildText(best);
  const observedAt =
    firstString(best, ['date', 'receivedAt', 'timestamp']) ?? new Date().toISOString();

  const metadata: Record<string, unknown> = {};
  const id = firstString(best, ['id']);
  if (id) metadata.messageId = id;
  if (threadId) metadata.threadId = threadId;
  if (Array.isArray(best.labelIds)) metadata.labels = best.labelIds;
  const from = firstString(best, ['from', 'sender']);
  if (from) metadata.from = from;
  const to = firstString(best, ['to', 'recipient', 'recipients']);
  if (to) metadata.to = to;
  const subject = firstString(best, ['subject']);
  if (subject) metadata.subject = subject;

  return {
    source: 'gmail',
    sourceType,
    externalWrite: false,
    text,
    observedAt,
    metadata,
  };
}
