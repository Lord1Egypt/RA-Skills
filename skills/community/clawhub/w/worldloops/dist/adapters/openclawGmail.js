"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.gmailWebhookToSignals = gmailWebhookToSignals;
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
function pickItems(payload) {
    if (Array.isArray(payload.messages))
        return payload.messages;
    if (Array.isArray(payload.items))
        return payload.items;
    if (Array.isArray(payload.events))
        return payload.events;
    return [];
}
function buildText(record, index) {
    const subject = firstString(record, ['subject', 'title']);
    const from = firstString(record, ['from', 'sender', 'author']);
    const snippet = firstString(record, ['snippet', 'body', 'text', 'summary', 'preview']);
    const label = firstString(record, ['label', 'labelId']);
    const hint = (0, threadHints_1.classifyThreadHint)({ subject, snippet });
    const parts = [
        subject ? `subject=${subject}` : undefined,
        from ? `from=${from}` : undefined,
        snippet ? `snippet=${snippet}` : undefined,
        label ? `label=${label}` : undefined,
        hint ? `thread_hint=${hint}` : undefined,
    ].filter((part) => Boolean(part));
    if (parts.length === 0)
        return undefined;
    return `OpenClaw Gmail event ${index + 1}: ${parts.join(' | ')}`;
}
function gmailWebhookToSignals(payload) {
    const items = pickItems(payload);
    return items.flatMap((entry, index) => {
        const record = asRecord(entry);
        if (!record)
            return [];
        const text = buildText(record, index);
        if (!text)
            return [];
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
        const signal = {
            source: 'gmail',
            text,
        };
        if (createdAt)
            signal.createdAt = createdAt;
        if (url)
            signal.url = url;
        return [signal];
    });
}
//# sourceMappingURL=openclawGmail.js.map