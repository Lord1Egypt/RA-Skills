"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.gogGmailToSignals = gogGmailToSignals;
exports.gogCalendarToSignals = gogCalendarToSignals;
const threadHints_1 = require("./threadHints");
function asRecord(value) {
    if (typeof value !== 'object' || value === null || Array.isArray(value)) {
        return null;
    }
    return value;
}
function firstString(record, keys) {
    for (const key of keys) {
        const value = record[key];
        if (typeof value === 'string' && value.trim() !== '') {
            return value.trim();
        }
    }
    return undefined;
}
function pickArray(payload, keys) {
    for (const key of keys) {
        const value = payload[key];
        if (Array.isArray(value))
            return value;
    }
    return [];
}
function headerValue(record, name) {
    const headers = asRecord(record.payload)?.headers;
    if (!Array.isArray(headers))
        return undefined;
    const found = headers.find((entry) => {
        const header = asRecord(entry);
        return typeof header?.name === 'string' && header.name.toLowerCase() === name.toLowerCase();
    });
    const header = asRecord(found);
    const value = header?.value;
    return typeof value === 'string' && value.trim() !== '' ? value.trim() : undefined;
}
function normalizeGmailEntries(payload) {
    const direct = pickArray(payload, ['messages', 'items', 'results']);
    if (direct.length > 0)
        return direct;
    const thread = asRecord(payload.thread);
    if (thread) {
        const threadMessages = pickArray(thread, ['messages']);
        if (threadMessages.length > 0)
            return threadMessages;
    }
    const threads = pickArray(payload, ['threads']);
    if (threads.length > 0)
        return threads;
    return [];
}
function gogGmailToSignals(payload) {
    const record = payload;
    const messages = normalizeGmailEntries(record);
    return messages.flatMap((entry, index) => {
        const msg = asRecord(entry);
        if (!msg)
            return [];
        const subject = firstString(msg, ['subject', 'title']) ?? headerValue(msg, 'Subject');
        const from = firstString(msg, ['from', 'sender']) ?? headerValue(msg, 'From');
        const snippet = firstString(msg, ['snippet', 'body', 'text', 'summary']);
        const date = firstString(msg, ['date', 'receivedAt', 'internalDate', 'createdAt']) ??
            headerValue(msg, 'Date');
        const url = firstString(msg, ['url', 'link', 'permalink']);
        const hint = (0, threadHints_1.classifyThreadHint)({ subject: subject ?? undefined, snippet: snippet ?? undefined });
        const parts = [
            subject ? `subject=${subject}` : undefined,
            from ? `from=${from}` : undefined,
            snippet ? `snippet=${snippet}` : undefined,
            hint ? `thread_hint=${hint}` : undefined,
        ].filter((part) => Boolean(part));
        if (parts.length === 0)
            return [];
        const signal = {
            source: 'gmail',
            text: `gog Gmail message ${index + 1}: ${parts.join(' | ')}`,
        };
        if (date)
            signal.createdAt = date;
        if (url)
            signal.url = url;
        return [signal];
    });
}
function gogCalendarToSignals(payload) {
    const record = payload;
    const events = pickArray(record, ['events', 'items', 'results']);
    return events.flatMap((entry, index) => {
        const event = asRecord(entry);
        if (!event)
            return [];
        const title = firstString(event, ['summary', 'title', 'name']);
        const description = firstString(event, ['description', 'notes', 'body', 'text']);
        const start = firstString(event, ['start', 'startTime', 'startsAt']);
        const end = firstString(event, ['end', 'endTime', 'endsAt']);
        const location = firstString(event, ['location']);
        const url = firstString(event, ['htmlLink', 'url', 'link', 'permalink']);
        const parts = [
            title ? `title=${title}` : undefined,
            description ? `description=${description}` : undefined,
            start ? `start=${start}` : undefined,
            end ? `end=${end}` : undefined,
            location ? `location=${location}` : undefined,
        ].filter((part) => Boolean(part));
        if (parts.length === 0)
            return [];
        const signal = {
            source: 'calendar',
            text: `gog Calendar event ${index + 1}: ${parts.join(' | ')}`,
        };
        if (start)
            signal.createdAt = start;
        if (url)
            signal.url = url;
        return [signal];
    });
}
//# sourceMappingURL=gogSnapshot.js.map