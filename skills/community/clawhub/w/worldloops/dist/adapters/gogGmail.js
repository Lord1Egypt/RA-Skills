"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.isGogGmailPayload = isGogGmailPayload;
exports.gogGmailToAdapterSignal = gogGmailToAdapterSignal;
const threadHints_1 = require("./threadHints");
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
    const subject = firstString(record, ['subject']) ?? '';
    const snippet = firstString(record, ['snippet', 'body']) ?? '';
    const combined = `${subject} ${snippet}`.toLowerCase();
    let score = 0;
    for (const kw of ACTIONABLE_KEYWORDS) {
        if (combined.includes(kw))
            score++;
    }
    return score;
}
function buildText(record) {
    const subject = firstString(record, ['subject']);
    const from = firstString(record, ['from', 'sender']);
    const snippet = firstString(record, ['snippet', 'body']);
    const hint = (0, threadHints_1.classifyThreadHint)({ subject, snippet });
    const parts = [];
    if (subject)
        parts.push(`subject=${subject}`);
    if (from)
        parts.push(`from=${from}`);
    if (snippet)
        parts.push(`snippet=${snippet}`);
    if (hint)
        parts.push(`thread_hint=${hint}`);
    return parts.length > 0 ? `gog Gmail: ${parts.join(' | ')}` : 'gog Gmail message';
}
function isGogGmailPayload(raw) {
    if (typeof raw !== 'object' || raw === null || Array.isArray(raw))
        return false;
    const obj = raw;
    return (Array.isArray(obj.messages) &&
        typeof obj.text !== 'string' &&
        typeof obj.source === 'undefined');
}
function gogGmailToAdapterSignal(payload) {
    const messages = (payload.messages ?? [])
        .map(asRecord)
        .filter((m) => m !== null);
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
    const observedAt = firstString(best, ['date', 'receivedAt', 'timestamp']) ?? new Date().toISOString();
    const metadata = {};
    const id = firstString(best, ['id']);
    if (id)
        metadata.messageId = id;
    if (threadId)
        metadata.threadId = threadId;
    if (Array.isArray(best.labelIds))
        metadata.labels = best.labelIds;
    const from = firstString(best, ['from', 'sender']);
    if (from)
        metadata.from = from;
    const to = firstString(best, ['to', 'recipient', 'recipients']);
    if (to)
        metadata.to = to;
    const subject = firstString(best, ['subject']);
    if (subject)
        metadata.subject = subject;
    return {
        source: 'gmail',
        sourceType,
        externalWrite: false,
        text,
        observedAt,
        metadata,
    };
}
//# sourceMappingURL=gogGmail.js.map