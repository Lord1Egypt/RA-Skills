import type { Signal } from '../types';
import { classifyThreadHint } from './threadHints';

type UnknownRecord = Record<string, unknown>;

export interface OpenClawGmailWebhookPayload {
  account?: string;
  email?: string;
  label?: string;
  messages?: unknown[];
  items?: unknown[];
  events?: unknown[];
  count?: number;
}

function asRecord(value: unknown): UnknownRecord | null {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    return null;
  }
  return value as UnknownRecord;
}

function firstString(record: UnknownRecord, keys: string[]): string | undefined {
  for (const key of keys) {
    const value = record[key];
    if (typeof value === 'string' && value.trim() !== '') {
      return value.trim();
    }
  }
  return undefined;
}

function pickItems(payload: OpenClawGmailWebhookPayload): unknown[] {
  if (Array.isArray(payload.messages)) return payload.messages;
  if (Array.isArray(payload.items)) return payload.items;
  if (Array.isArray(payload.events)) return payload.events;
  return [];
}

function buildText(record: UnknownRecord, index: number): string | undefined {
  const subject = firstString(record, ['subject', 'title']);
  const from = firstString(record, ['from', 'sender', 'author']);
  const snippet = firstString(record, ['snippet', 'body', 'text', 'summary', 'preview']);
  const label = firstString(record, ['label', 'labelId']);
  const hint = classifyThreadHint({ subject, snippet });

  const parts = [
    subject ? `subject=${subject}` : undefined,
    from ? `from=${from}` : undefined,
    snippet ? `snippet=${snippet}` : undefined,
    label ? `label=${label}` : undefined,
    hint ? `thread_hint=${hint}` : undefined,
  ].filter((part): part is string => Boolean(part));

  if (parts.length === 0) return undefined;

  return `OpenClaw Gmail event ${index + 1}: ${parts.join(' | ')}`;
}

export function gmailWebhookToSignals(payload: OpenClawGmailWebhookPayload): Signal[] {
  const items = pickItems(payload);

  return items.flatMap((entry, index): Signal[] => {
    const record = asRecord(entry);
    if (!record) return [];

    const text = buildText(record, index);
    if (!text) return [];

    const createdAt = firstString(record, [
      'createdAt',
      'created_at',
      'receivedAt',
      'internalDate',
      'timestamp',
      'time',
      'date',
    ]);

    const url = firstString(record, ['url', 'link', 'permalink']);

    const signal: Signal = {
      source: 'gmail',
      text,
    };

    if (createdAt) signal.createdAt = createdAt;
    if (url) signal.url = url;

    return [signal];
  });
}
