"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.messagesToSignals = messagesToSignals;
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
function sourceFromChannel(channel) {
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
function pickMessageArray(payload) {
    if (Array.isArray(payload.messages))
        return payload.messages;
    if (Array.isArray(payload.items))
        return payload.items;
    if (Array.isArray(payload.results))
        return payload.results;
    if (payload.payload) {
        if (Array.isArray(payload.payload.messages))
            return payload.payload.messages;
        if (Array.isArray(payload.payload.items))
            return payload.payload.items;
        if (Array.isArray(payload.payload.results))
            return payload.payload.results;
    }
    return [];
}
function messagesToSignals(payload, options = {}) {
    const messages = pickMessageArray(payload);
    const source = sourceFromChannel(options.channel ?? payload.channel);
    return messages.flatMap((entry, index) => {
        const record = asRecord(entry);
        if (!record)
            return [];
        const text = firstString(record, ['text', 'message', 'body', 'content', 'plainText']) ??
            firstString(record, ['summary', 'title']);
        if (!text)
            return [];
        const sender = firstString(record, ['sender', 'from', 'author', 'user', 'username', 'displayName']);
        const createdAt = firstString(record, ['createdAt', 'created_at', 'timestamp', 'ts', 'time', 'date']);
        const url = firstString(record, ['url', 'permalink', 'link']);
        const signalText = sender
            ? `OpenClaw message from ${sender}: ${text}`
            : `OpenClaw message ${index + 1}: ${text}`;
        const signal = {
            source,
            text: signalText,
        };
        if (createdAt)
            signal.createdAt = createdAt;
        if (url)
            signal.url = url;
        return [signal];
    });
}
//# sourceMappingURL=openclawMessages.js.map