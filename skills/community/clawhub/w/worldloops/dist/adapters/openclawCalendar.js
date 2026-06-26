"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.calendarEventsToSignals = calendarEventsToSignals;
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
    if (Array.isArray(payload.events))
        return payload.events;
    if (Array.isArray(payload.items))
        return payload.items;
    return [];
}
function buildText(record, index) {
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
    ].filter((part) => Boolean(part));
    if (parts.length === 0)
        return undefined;
    return `OpenClaw Calendar event ${index + 1}: ${parts.join(' | ')}`;
}
function calendarEventsToSignals(payload) {
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
            'updatedAt',
            'updated_at',
            'start',
            'startTime',
            'startsAt',
        ]);
        const url = firstString(record, ['url', 'htmlLink', 'link', 'permalink']);
        const signal = {
            source: 'calendar',
            text,
        };
        if (createdAt)
            signal.createdAt = createdAt;
        if (url)
            signal.url = url;
        return [signal];
    });
}
//# sourceMappingURL=openclawCalendar.js.map