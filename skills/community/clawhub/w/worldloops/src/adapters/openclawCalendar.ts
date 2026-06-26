import type { Signal } from '../types';

type UnknownRecord = Record<string, unknown>;

export interface OpenClawCalendarPayload {
  account?: string;
  calendarId?: string;
  events?: unknown[];
  items?: unknown[];
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

function pickItems(payload: OpenClawCalendarPayload): unknown[] {
  if (Array.isArray(payload.events)) return payload.events;
  if (Array.isArray(payload.items)) return payload.items;
  return [];
}

function buildText(record: UnknownRecord, index: number): string | undefined {
  const title = firstString(record, ['title', 'summary', 'name']);
  const description = firstString(record, ['description', 'notes', 'body', 'text']);
  const start = firstString(record, ['start', 'startTime', 'startsAt', 'start_at']);
  const end = firstString(record, ['end', 'endTime', 'endsAt', 'end_at']);
  const location = firstString(record, ['location']);
  const attendees = firstString(record, ['attendees', 'participants']);

  const parts = [
    title ? `title=${title}` : undefined,
    description ? `description=${description}` : undefined,
    start ? `start=${start}` : undefined,
    end ? `end=${end}` : undefined,
    location ? `location=${location}` : undefined,
    attendees ? `attendees=${attendees}` : undefined,
  ].filter((part): part is string => Boolean(part));

  if (parts.length === 0) return undefined;

  return `OpenClaw Calendar event ${index + 1}: ${parts.join(' | ')}`;
}

export function calendarEventsToSignals(payload: OpenClawCalendarPayload): Signal[] {
  const items = pickItems(payload);

  return items.flatMap((entry, index): Signal[] => {
    const record = asRecord(entry);
    if (!record) return [];

    const text = buildText(record, index);
    if (!text) return [];

    const createdAt = firstString(record, [
      'createdAt',
      'created_at',
      'updatedAt',
      'updated_at',
      'start',
      'startTime',
      'startsAt',
    ]);

    const url = firstString(record, ['url', 'htmlLink', 'link', 'permalink']);

    const signal: Signal = {
      source: 'calendar',
      text,
    };

    if (createdAt) signal.createdAt = createdAt;
    if (url) signal.url = url;

    return [signal];
  });
}
