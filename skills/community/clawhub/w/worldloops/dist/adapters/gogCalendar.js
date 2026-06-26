"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.isGogCalendarPayload = isGogCalendarPayload;
exports.gogCalendarToAdapterSignal = gogCalendarToAdapterSignal;
const PREPARATION_KEYWORDS = [
    'prepare',
    'preparation',
    'prep',
    'materials',
    'follow-up',
    'follow up',
    'followup',
    'deadline',
    'action item',
    'review',
    'approval',
    'before the meeting',
    'agenda',
    'send',
    'submit',
    'recap',
    'needed',
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
function scoreEvent(record) {
    const summary = firstString(record, ['summary', 'title', 'name']) ?? '';
    const description = firstString(record, ['description', 'notes']) ?? '';
    const combined = `${summary} ${description}`.toLowerCase();
    let score = 0;
    for (const kw of PREPARATION_KEYWORDS) {
        if (combined.includes(kw))
            score++;
    }
    return score;
}
function buildText(record) {
    const title = firstString(record, ['summary', 'title', 'name']);
    const description = firstString(record, ['description', 'notes', 'body']);
    const start = firstString(record, ['start', 'startTime']);
    const end = firstString(record, ['end', 'endTime']);
    const location = firstString(record, ['location']);
    const attendees = firstString(record, ['attendees', 'participants']);
    const parts = [];
    if (title)
        parts.push(`title=${title}`);
    if (description)
        parts.push(`description=${description}`);
    if (start)
        parts.push(`start=${start}`);
    if (end)
        parts.push(`end=${end}`);
    if (location)
        parts.push(`location=${location}`);
    if (attendees)
        parts.push(`attendees=${attendees}`);
    return parts.length > 0 ? `gog Calendar: ${parts.join(' | ')}` : 'gog Calendar event';
}
function isGogCalendarPayload(raw) {
    if (typeof raw !== 'object' || raw === null || Array.isArray(raw))
        return false;
    const obj = raw;
    return (Array.isArray(obj.events) &&
        typeof obj.text !== 'string' &&
        typeof obj.source === 'undefined');
}
function gogCalendarToAdapterSignal(payload) {
    const events = (payload.events ?? [])
        .map(asRecord)
        .filter((e) => e !== null);
    if (events.length === 0) {
        return {
            source: 'calendar',
            sourceType: 'event',
            externalWrite: false,
            text: 'gog Calendar: no events',
            observedAt: new Date().toISOString(),
        };
    }
    let best = events[0];
    let bestScore = scoreEvent(events[0]);
    for (let i = 1; i < events.length; i++) {
        const score = scoreEvent(events[i]);
        if (score > bestScore) {
            bestScore = score;
            best = events[i];
        }
    }
    const text = buildText(best);
    const observedAt = firstString(best, ['updatedAt', 'updated_at', 'createdAt', 'created_at', 'start']) ??
        new Date().toISOString();
    const metadata = {};
    const id = firstString(best, ['id']);
    if (id)
        metadata.eventId = id;
    const calendarId = firstString(best, ['calendarId', 'calendar_id']);
    if (calendarId)
        metadata.calendarId = calendarId;
    const start = firstString(best, ['start', 'startTime']);
    if (start)
        metadata.start = start;
    const end = firstString(best, ['end', 'endTime']);
    if (end)
        metadata.end = end;
    const attendees = firstString(best, ['attendees', 'participants']);
    if (attendees)
        metadata.attendees = attendees;
    const location = firstString(best, ['location']);
    if (location)
        metadata.location = location;
    return {
        source: 'calendar',
        sourceType: 'event',
        externalWrite: false,
        text,
        observedAt,
        metadata,
    };
}
//# sourceMappingURL=gogCalendar.js.map