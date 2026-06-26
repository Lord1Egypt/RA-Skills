import type { Signal } from '../types';

type UnknownRecord = Record<string, unknown>;

export interface OpenClawCommitmentsPayload {
  count?: number;
  status?: string | null;
  agentId?: string | null;
  store?: string;
  commitments?: unknown[];
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

function compact(parts: Array<string | undefined>): string {
  return parts.filter((part): part is string => Boolean(part && part.trim())).join(' | ');
}

export function commitmentsToSignals(payload: OpenClawCommitmentsPayload): Signal[] {
  const commitments = Array.isArray(payload.commitments) ? payload.commitments : [];

  return commitments.flatMap((entry, index): Signal[] => {
    const record = asRecord(entry);
    if (!record) return [];

    const title =
      firstString(record, ['title', 'summary', 'text', 'message', 'description', 'body']) ??
      `OpenClaw commitment ${index + 1}`;

    const status = firstString(record, ['status']);
    const dueAt = firstString(record, ['dueAt', 'due', 'deadline']);
    const source = firstString(record, ['source', 'channel', 'provider']);
    const createdAt = firstString(record, ['createdAt', 'created_at', 'timestamp', 'time']);

    const text = compact([
      `OpenClaw commitment: ${title}`,
      status ? `status=${status}` : undefined,
      dueAt ? `due=${dueAt}` : undefined,
      source ? `source=${source}` : undefined,
    ]);

    const signal: Signal = {
      source: 'manual',
      text,
    };

    if (createdAt) {
      signal.createdAt = createdAt;
    }

    return [signal];
  });
}
