"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.commitmentsToSignals = commitmentsToSignals;
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
function compact(parts) {
    return parts.filter((part) => Boolean(part && part.trim())).join(' | ');
}
function commitmentsToSignals(payload) {
    const commitments = Array.isArray(payload.commitments) ? payload.commitments : [];
    return commitments.flatMap((entry, index) => {
        const record = asRecord(entry);
        if (!record)
            return [];
        const title = firstString(record, ['title', 'summary', 'text', 'message', 'description', 'body']) ??
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
        const signal = {
            source: 'manual',
            text,
        };
        if (createdAt) {
            signal.createdAt = createdAt;
        }
        return [signal];
    });
}
//# sourceMappingURL=openclawCommitments.js.map