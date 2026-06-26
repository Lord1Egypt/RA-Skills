import type { Signal, SignalSource } from '../types';

type UnknownRecord = Record<string, unknown>;

export interface OpenClawMessagesPayload {
  messages?: unknown[];
  items?: unknown[];
  results?: unknown[];
  payload?: {
    messages?: unknown[];
    items?: unknown[];
    results?: unknown[];
  };
  count?: number;
  channel?: string;
  target?: string;
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

function sourceFromChannel(channel: string | undefined): SignalSource {
  switch ((channel ?? '').toLowerCase()) {
    case 'slack':
      return 'slack';
    case 'gmail':
      return 'gmail';
    case 'calendar':
      return 'calendar';
    case 'github':
      return 'github';
    default:
      return 'manual';
  }
}

function pickMessageArray(payload: OpenClawMessagesPayload): unknown[] {
  if (Array.isArray(payload.messages)) return payload.messages;
  if (Array.isArray(payload.items)) return payload.items;
  if (Array.isArray(payload.results)) return payload.results;

  if (payload.payload) {
    if (Array.isArray(payload.payload.messages)) return payload.payload.messages;
    if (Array.isArray(payload.payload.items)) return payload.payload.items;
    if (Array.isArray(payload.payload.results)) return payload.payload.results;
  }

  return [];
}

export function messagesToSignals(
  payload: OpenClawMessagesPayload,
  options: {
    channel?: string;
    target?: string;
  } = {}
): Signal[] {
  const messages = pickMessageArray(payload);
  const source = sourceFromChannel(options.channel ?? payload.channel);

  return messages.flatMap((entry, index): Signal[] => {
    const record = asRecord(entry);
    if (!record) return [];

    const text =
      firstString(record, ['text', 'message', 'body', 'content', 'plainText']) ??
      firstString(record, ['summary', 'title']);

    if (!text) return [];

    const sender = firstString(record, ['sender', 'from', 'author', 'user', 'username', 'displayName']);
    const createdAt = firstString(record, ['createdAt', 'created_at', 'timestamp', 'ts', 'time', 'date']);
    const url = firstString(record, ['url', 'permalink', 'link']);

    const signalText = sender
      ? `OpenClaw message from ${sender}: ${text}`
      : `OpenClaw message ${index + 1}: ${text}`;

    const signal: Signal = {
      source,
      text: signalText,
    };

    if (createdAt) signal.createdAt = createdAt;
    if (url) signal.url = url;

    return [signal];
  });
}
