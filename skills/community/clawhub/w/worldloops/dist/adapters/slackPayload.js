"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.isSlackHostPayload = isSlackHostPayload;
exports.slackPayloadToAdapterSignal = slackPayloadToAdapterSignal;
const ACTIONABLE_KEYWORDS = [
    'review',
    'please check',
    'can you respond',
    'deadline',
    'approval',
    'approve',
    'follow-up',
    'follow up',
    'followup',
    'mention',
    'waiting',
    'action required',
    'please',
    'can you',
    'could you',
    'need',
    'urgent',
    'asap',
    'by eod',
    'by end of day',
];
function asRecord(value) {
    if (typeof value !== 'object' || value === null || Array.isArray(value))
        return null;
    return value;
}
function firstString(record, keys) {
    for (const key of keys) {
        const value = record[key];
        if (typeof value === 'string' && value.trim() !== '')
            return value.trim();
    }
    return undefined;
}
function scoreMessage(record) {
    const text = firstString(record, ['text', 'message', 'body']) ?? '';
    const lower = text.toLowerCase();
    let score = 0;
    for (const kw of ACTIONABLE_KEYWORDS) {
        if (lower.includes(kw))
            score++;
    }
    return score;
}
function tsToIso(ts) {
    const numeric = parseFloat(ts);
    if (isNaN(numeric))
        return undefined;
    return new Date(numeric * 1000).toISOString();
}
function buildTextFromMessage(record, channel) {
    const text = firstString(record, ['text', 'message', 'body']);
    const user = firstString(record, ['user', 'username', 'display_name']);
    const thread_ts = firstString(record, ['thread_ts']);
    const parts = [];
    if (text)
        parts.push(`text=${text}`);
    if (channel)
        parts.push(`channel=${channel}`);
    if (user)
        parts.push(`user=${user}`);
    if (thread_ts)
        parts.push(`thread=yes`);
    return parts.length > 0 ? `Slack: ${parts.join(' | ')}` : 'Slack message';
}
function isSlackHostPayload(raw) {
    if (typeof raw !== 'object' || raw === null || Array.isArray(raw))
        return false;
    const obj = raw;
    // Slack host payload: no source field, and has channel, ts, or messages array without text at top level
    if (typeof obj.source !== 'undefined')
        return false;
    const hasMessages = Array.isArray(obj.messages) || Array.isArray(obj.items);
    const hasSlackFields = typeof obj.channel === 'string' ||
        typeof obj.channel_id === 'string' ||
        typeof obj.ts === 'string';
    return hasMessages || hasSlackFields;
}
function slackPayloadToAdapterSignal(payload) {
    const channel = payload.channel_name ??
        payload.channel ??
        payload.channel_id ??
        undefined;
    const rawItems = Array.isArray(payload.messages)
        ? payload.messages
        : Array.isArray(payload.items)
            ? payload.items
            : [];
    const messages = rawItems.map(asRecord).filter((m) => m !== null);
    if (messages.length > 0) {
        let best = messages[0];
        let bestScore = scoreMessage(messages[0]);
        for (let i = 1; i < messages.length; i++) {
            const score = scoreMessage(messages[i]);
            if (score > bestScore) {
                bestScore = score;
                best = messages[i];
            }
        }
        const rawTs = firstString(best, ['ts', 'timestamp']);
        const observedAt = (rawTs ? tsToIso(rawTs) : undefined) ??
            firstString(best, ['date', 'receivedAt']) ??
            new Date().toISOString();
        const metadata = {};
        if (channel)
            metadata.channel = channel;
        const user = firstString(best, ['user', 'username', 'display_name']);
        if (user)
            metadata.user = user;
        const ts = firstString(best, ['ts']);
        if (ts)
            metadata.ts = ts;
        const thread_ts = firstString(best, ['thread_ts']);
        if (thread_ts)
            metadata.thread_ts = thread_ts;
        const permalink = firstString(best, ['permalink', 'url', 'link']);
        if (permalink)
            metadata.permalink = permalink;
        const sourceType = thread_ts ? 'thread' : 'message';
        const text = buildTextFromMessage(best, channel);
        return {
            source: 'slack',
            sourceType,
            externalWrite: false,
            text,
            observedAt,
            metadata,
        };
    }
    // Single message at top level
    const rawTs = payload.ts;
    const observedAt = rawTs ? tsToIso(rawTs) ?? new Date().toISOString() : new Date().toISOString();
    const text = payload.text
        ? `Slack: text=${payload.text}${channel ? ` | channel=${channel}` : ''}${payload.user ? ` | user=${payload.user}` : ''}`
        : channel
            ? `Slack: channel=${channel}`
            : 'Slack message';
    const metadata = {};
    if (channel)
        metadata.channel = channel;
    if (payload.user)
        metadata.user = payload.user;
    if (rawTs)
        metadata.ts = rawTs;
    if (payload.thread_ts)
        metadata.thread_ts = payload.thread_ts;
    if (payload.permalink)
        metadata.permalink = payload.permalink;
    const sourceType = payload.thread_ts ? 'thread' : 'message';
    return {
        source: 'slack',
        sourceType,
        externalWrite: false,
        text,
        observedAt,
        metadata,
    };
}
//# sourceMappingURL=slackPayload.js.map