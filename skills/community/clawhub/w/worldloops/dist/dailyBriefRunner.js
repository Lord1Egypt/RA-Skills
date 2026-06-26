"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.SOURCES = exports.DEFAULT_INBOX_DIR = void 0;
exports.isPromotionalText = isPromotionalText;
exports.hasNegativeIntent = hasNegativeIntent;
exports.isTravelContextEvent = isTravelContextEvent;
exports.buildSummaryLines = buildSummaryLines;
exports.processSource = processSource;
exports.processAllSources = processAllSources;
exports.buildBriefLines = buildBriefLines;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const brief_1 = require("./brief");
const validateAdapterSignal_1 = require("./adapter/validateAdapterSignal");
const toWorldLoopsSignal_1 = require("./adapter/toWorldLoopsSignal");
const gogGmail_1 = require("./adapters/gogGmail");
const gogCalendar_1 = require("./adapters/gogCalendar");
const slackPayload_1 = require("./adapters/slackPayload");
exports.DEFAULT_INBOX_DIR = '.worldloops/inbox';
const KOREAN_ACTION_PHRASES = [
    '검토해주세요', '확인해주세요', '다시 검토', '회신 부탁드립니다',
    '답변 부탁드립니다', '승인 부탁드립니다', '공유 부탁드립니다',
    '보내주세요', '수정해주세요', '확인 요청', '검토 요청',
    '요청드립니다', '부탁드립니다',
];
const NEGATIVE_INTENT_PHRASES = [
    'no action required',
    'no reply needed',
    'no response needed',
    'no need to reply',
    'fyi only',
    'for your information',
    'informational only',
    'no action needed',
];
const PROMOTIONAL_INDICATORS = [
    'unsubscribe', 'discount', '% off', 'sale ends', 'limited offer',
    'promo code', 'special offer', 'free shipping', 'daily digest',
    'newsletter', 'weekly digest', 'opt out', 'manage preferences',
    'earn double', 'earn miles', 'earn points', 'earn bonus',
    'save up to', 'limited time', 'exclusive deal', 'exclusive offer',
    'reward points', 'rewards program', 'miles offer',
    'view in browser', 'manage subscription', 'manage email preferences',
];
const TRAVEL_CONTEXT_KEYWORDS = [
    'flight', 'travel', 'hotel', 'airport', 'workshop',
    'board meeting', 'interview', 'customer meeting', 'executive meeting',
    '항공', '비행편', '출장', '호텔',
    'departure', 'arrival', 'airline', 'boarding',
    'itinerary', 'reservation', 'trip',
    'terminal', 'gate',
    'sfo', 'icn', 'jfk', 'lax', 'korean air',
];
function hasKoreanActionPhrase(text) {
    return KOREAN_ACTION_PHRASES.some(phrase => text.includes(phrase));
}
function isPromotionalText(text) {
    const lower = text.toLowerCase();
    return PROMOTIONAL_INDICATORS.some(phrase => lower.includes(phrase));
}
function hasNegativeIntent(text) {
    const lower = text.toLowerCase();
    return NEGATIVE_INTENT_PHRASES.some(phrase => lower.includes(phrase));
}
function isTravelContextEvent(title, description, location) {
    const combined = `${title ?? ''} ${description ?? ''} ${location ?? ''}`.toLowerCase();
    return TRAVEL_CONTEXT_KEYWORDS.some(kw => combined.includes(kw));
}
function formatCalendarTime(isoString) {
    try {
        if (/^\d{4}-\d{2}-\d{2}$/.test(isoString)) {
            const [, m, d] = isoString.split('-').map(Number);
            const ref = new Date(Date.UTC(2000, m - 1, d));
            const monthName = ref.toLocaleString('en-US', { month: 'long', timeZone: 'UTC' });
            return `${monthName} ${d}`;
        }
        const date = new Date(isoString);
        if (isNaN(date.getTime()))
            return 'unavailable';
        const month = date.toLocaleString('en-US', { month: 'long', timeZone: 'UTC' });
        const day = date.getUTCDate();
        const hours = date.getUTCHours();
        const minutes = date.getUTCMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        const hour12 = hours % 12 || 12;
        const minuteStr = minutes.toString().padStart(2, '0');
        return `${month} ${day}, ${hour12}:${minuteStr} ${ampm} local time`;
    }
    catch {
        return 'unavailable';
    }
}
function detectLocalCandidate(sourceId, evidence) {
    if (sourceId === 'gmail') {
        const textToCheck = [evidence.subject ?? '', evidence.snippet ?? ''].join(' ');
        if (hasKoreanActionPhrase(textToCheck)) {
            return {
                idempotencyKey: `local-gmail-korean-review`,
                entityType: 'email',
                source: 'gmail',
                currentState: 'unread',
                proposedState: 'reviewed',
                reason: 'review request detected',
                approvalRequired: true,
                actionHint: 'Review the submitted document or reply if needed',
            };
        }
    }
    if (sourceId === 'slack') {
        const text = evidence.text ?? '';
        if (hasKoreanActionPhrase(text)) {
            return {
                idempotencyKey: `local-slack-korean-review`,
                entityType: 'message',
                source: 'slack',
                currentState: 'unread',
                proposedState: 'reviewed',
                reason: 'review request detected',
                approvalRequired: true,
                actionHint: 'Review the message and reply if needed',
            };
        }
    }
    return null;
}
exports.SOURCES = [
    { id: 'gmail', file: 'openclaw-gmail-live.json', label: 'Gmail', emoji: '⚠️' },
    { id: 'calendar', file: 'openclaw-calendar-live.json', label: 'Calendar', emoji: '📅' },
    { id: 'slack', file: 'openclaw-slack-live.json', label: 'Slack', emoji: '💬' },
];
function truncate(s, maxLen = 120) {
    return s.length <= maxLen ? s : s.slice(0, maxLen - 1) + '…';
}
function extractEvidence(sourceId, raw) {
    if (typeof raw !== 'object' || raw === null || Array.isArray(raw))
        return {};
    const obj = raw;
    if (sourceId === 'gmail') {
        const messages = Array.isArray(obj.messages) ? obj.messages : [];
        const first = messages[0];
        if (typeof first === 'object' && first !== null && !Array.isArray(first)) {
            const msg = first;
            const subject = typeof msg.subject === 'string' ? msg.subject : undefined;
            const from = typeof msg.from === 'string' ? msg.from : undefined;
            const raw_snippet = typeof msg.snippet === 'string' ? msg.snippet :
                typeof msg.body === 'string' ? msg.body : undefined;
            const snippet = raw_snippet ? truncate(raw_snippet) : undefined;
            const messageId = typeof msg.id === 'string' ? msg.id : undefined;
            const threadId = typeof msg.threadId === 'string' ? msg.threadId : undefined;
            const sampleMessages = messages.slice(0, 3).map((m) => {
                if (typeof m !== 'object' || m === null)
                    return {};
                const item = m;
                return {
                    from: typeof item.from === 'string' ? item.from : undefined,
                    subject: typeof item.subject === 'string' ? item.subject : undefined,
                };
            });
            return { subject, from, snippet, itemCount: messages.length, messageId, threadId, sampleMessages };
        }
        return { itemCount: messages.length };
    }
    if (sourceId === 'calendar') {
        const events = Array.isArray(obj.events) ? obj.events : [];
        const sampleEvents = events.slice(0, 3).map((e) => {
            if (typeof e !== 'object' || e === null)
                return {};
            const ev = e;
            return {
                title: typeof ev.summary === 'string' ? ev.summary :
                    typeof ev.title === 'string' ? ev.title : undefined,
                start: typeof ev.start === 'string' ? ev.start : undefined,
                location: typeof ev.location === 'string' ? ev.location : undefined,
            };
        });
        const first = events[0];
        if (typeof first === 'object' && first !== null && !Array.isArray(first)) {
            const evt = first;
            const title = typeof evt.summary === 'string' ? evt.summary :
                typeof evt.title === 'string' ? evt.title : undefined;
            const start = typeof evt.start === 'string' ? evt.start : undefined;
            const end = typeof evt.end === 'string' ? evt.end : undefined;
            const location = typeof evt.location === 'string' ? evt.location : undefined;
            const raw_description = typeof evt.description === 'string' ? evt.description : undefined;
            const description = raw_description ? truncate(raw_description) : undefined;
            const eventId = typeof evt.id === 'string' ? evt.id : undefined;
            return { title, start, end, location, description, eventId, itemCount: events.length, sampleEvents };
        }
        return { itemCount: events.length, sampleEvents };
    }
    if (sourceId === 'slack') {
        const messages = Array.isArray(obj.messages) ? obj.messages :
            Array.isArray(obj.items) ? obj.items : [];
        const topChannel = typeof obj.channel === 'string' ? obj.channel : undefined;
        const first = messages[0];
        if (typeof first === 'object' && first !== null && !Array.isArray(first)) {
            const msg = first;
            const raw_text = typeof msg.text === 'string' ? msg.text : undefined;
            const text = raw_text ? truncate(raw_text) : undefined;
            const user = typeof msg.user === 'string' ? msg.user :
                typeof msg.username === 'string' ? msg.username : undefined;
            const channel = typeof msg.channel === 'string' ? msg.channel : topChannel;
            const ts = typeof msg.ts === 'string' ? msg.ts : undefined;
            const thread_ts = typeof msg.thread_ts === 'string' ? msg.thread_ts : undefined;
            const permalink = typeof msg.permalink === 'string' ? msg.permalink : undefined;
            return { text, channel, user, itemCount: messages.length, ts, thread_ts, permalink };
        }
        return { channel: topChannel, itemCount: messages.length };
    }
    return {};
}
function buildSummaryLines(sourceId, label, _emoji, candidates, evidence, details = false) {
    if (candidates.length === 0) {
        const lines = [];
        // Calendar zero-event case
        if (sourceId === 'calendar' && evidence.itemCount === 0) {
            lines.push(`📅 ${label} — No events found`);
            lines.push(`Checked: 0 events`);
            lines.push(`Reason: calendar payload was present, but contained no events`);
            lines.push(`Next: read events for today through the next 14 days`);
            if (details && evidence.eventId)
                lines.push(`eventId: ${evidence.eventId}`);
            return lines;
        }
        // Calendar important context — travel/flight events
        if (sourceId === 'calendar' && isTravelContextEvent(evidence.title, evidence.description, evidence.location)) {
            lines.push(`📅 ${label} — Important context`);
            if (evidence.title)
                lines.push(`Event: ${evidence.title}`);
            if (evidence.start)
                lines.push(`When: ${formatCalendarTime(evidence.start)}`);
            if (evidence.location)
                lines.push(`Location: ${evidence.location}`);
            lines.push(`Reason: travel event detected, no action proposed`);
            if (details && evidence.eventId)
                lines.push(`eventId: ${evidence.eventId}`);
            return lines;
        }
        const noActionEmoji = sourceId === 'gmail' ? '📧' :
            sourceId === 'calendar' ? '📅' : '💬';
        lines.push(`${noActionEmoji} ${label} — No actionable loop detected`);
        if (evidence.itemCount !== undefined) {
            const unit = sourceId === 'calendar' ? 'event' : 'message';
            const plural = evidence.itemCount === 1 ? unit : `${unit}s`;
            lines.push(`Checked: ${evidence.itemCount} ${plural}`);
        }
        if (sourceId === 'calendar') {
            if (evidence.sampleEvents && evidence.sampleEvents.length > 0) {
                for (const evt of evidence.sampleEvents) {
                    if (evt.title)
                        lines.push(`Event: ${evt.title}`);
                    if (evt.start)
                        lines.push(`When: ${formatCalendarTime(evt.start)}`);
                    if (evt.location)
                        lines.push(`Location: ${evt.location}`);
                }
            }
            else if (evidence.title) {
                lines.push(`Event: ${evidence.title}`);
            }
        }
        if (sourceId === 'gmail' && evidence.sampleMessages && evidence.sampleMessages.length > 0) {
            lines.push(`Sample:`);
            for (const m of evidence.sampleMessages) {
                const parts = [];
                if (m.from)
                    parts.push(`From: ${m.from}`);
                if (m.subject)
                    parts.push(`Subject: ${m.subject}`);
                if (parts.length > 0)
                    lines.push(`- ${parts.join(' / ')}`);
            }
        }
        if (sourceId === 'gmail') {
            const promoText = [
                evidence.subject ?? '',
                evidence.snippet ?? '',
                ...(evidence.sampleMessages ?? []).map(m => `${m.from ?? ''} ${m.subject ?? ''}`),
            ].join(' ');
            if (isPromotionalText(promoText) || hasNegativeIntent(promoText)) {
                lines.push(`Reason: promotional or informational message; no reply, approval, review, deadline, or follow-up request detected`);
            }
            else {
                lines.push(`Reason: no reply, deadline, approval, review, or follow-up request detected`);
            }
        }
        else {
            lines.push(`Reason: no prep, deadline, approval, or follow-up language detected`);
        }
        if (details) {
            if (sourceId === 'gmail') {
                if (evidence.messageId)
                    lines.push(`messageId: ${evidence.messageId}`);
                if (evidence.threadId)
                    lines.push(`threadId: ${evidence.threadId}`);
            }
            else if (sourceId === 'calendar') {
                if (evidence.eventId)
                    lines.push(`eventId: ${evidence.eventId}`);
            }
            else if (sourceId === 'slack') {
                if (evidence.ts)
                    lines.push(`ts: ${evidence.ts}`);
                if (evidence.thread_ts)
                    lines.push(`thread_ts: ${evidence.thread_ts}`);
                if (evidence.permalink)
                    lines.push(`permalink: ${evidence.permalink}`);
            }
        }
        return lines;
    }
    const first = candidates[0];
    const lines = [];
    let headerLabel;
    let activeEmoji;
    if (sourceId === 'gmail') {
        headerLabel = (first.reason && /review/i.test(first.reason)) ? 'Review requested' : 'Follow-up needed';
        activeEmoji = '⚠️';
    }
    else if (sourceId === 'calendar') {
        headerLabel = 'Prep needed';
        activeEmoji = '📅';
    }
    else {
        headerLabel = 'Action requested';
        activeEmoji = '💬';
    }
    lines.push(`${activeEmoji} ${label} — ${headerLabel}`);
    if (sourceId === 'gmail') {
        lines.push(`From: ${evidence.from ?? 'unavailable'}`);
        lines.push(`Subject: ${evidence.subject ?? 'unavailable'}`);
    }
    else if (sourceId === 'calendar') {
        lines.push(`Event: ${evidence.title ?? 'unavailable'}`);
        if (evidence.start)
            lines.push(`When: ${formatCalendarTime(evidence.start)}`);
        if (evidence.location)
            lines.push(`Location: ${evidence.location}`);
    }
    else if (sourceId === 'slack') {
        lines.push(`From: ${evidence.user ?? 'unavailable'}`);
        lines.push(`Channel: ${evidence.channel ?? 'unavailable'}`);
    }
    const whyDefault = sourceId === 'gmail' ? 'follow-up or reply request detected' :
        sourceId === 'calendar' ? 'preparation or action item detected' :
            'review or approval request detected';
    lines.push(`Why: ${first.reason || whyDefault}`);
    let evidenceText;
    if (sourceId === 'gmail') {
        evidenceText = evidence.snippet;
    }
    else if (sourceId === 'calendar') {
        evidenceText = evidence.description ?? (evidence.title
            ? `${evidence.title}${evidence.start ? ` at ${formatCalendarTime(evidence.start)}` : ''}`
            : undefined);
    }
    else if (sourceId === 'slack') {
        evidenceText = evidence.text;
    }
    lines.push(`Evidence: ${evidenceText ? `"${evidenceText}"` : 'not available in payload'}`);
    const actionDefault = sourceId === 'gmail' ? 'Draft a reply or follow-up' :
        sourceId === 'calendar' ? 'Prepare agenda or review action items' :
            'Review the referenced item and add comments or approval';
    lines.push(`Action: ${first.actionHint || actionDefault}`);
    lines.push(`Adjudication: ${first.approvalRequired ? 'requires_approval' : 'informational'}`);
    if (details) {
        if (sourceId === 'gmail') {
            if (evidence.messageId)
                lines.push(`messageId: ${evidence.messageId}`);
            if (evidence.threadId)
                lines.push(`threadId: ${evidence.threadId}`);
        }
        else if (sourceId === 'calendar') {
            if (evidence.eventId)
                lines.push(`eventId: ${evidence.eventId}`);
        }
        else if (sourceId === 'slack') {
            if (evidence.ts)
                lines.push(`ts: ${evidence.ts}`);
            if (evidence.thread_ts)
                lines.push(`thread_ts: ${evidence.thread_ts}`);
            if (evidence.permalink)
                lines.push(`permalink: ${evidence.permalink}`);
        }
    }
    return lines;
}
function normalizePayload(sourceId, raw) {
    if (typeof raw !== 'object' || raw === null || Array.isArray(raw))
        return raw;
    if (sourceId === 'gmail' && (0, gogGmail_1.isGogGmailPayload)(raw)) {
        return (0, gogGmail_1.gogGmailToAdapterSignal)(raw);
    }
    if (sourceId === 'calendar' && (0, gogCalendar_1.isGogCalendarPayload)(raw)) {
        return (0, gogCalendar_1.gogCalendarToAdapterSignal)(raw);
    }
    if (sourceId === 'slack' && (0, slackPayload_1.isSlackHostPayload)(raw)) {
        return (0, slackPayload_1.slackPayloadToAdapterSignal)(raw);
    }
    const obj = raw;
    if (!obj.source)
        obj.source = sourceId;
    if (!obj.sourceType)
        obj.sourceType = 'message';
    if (obj.externalWrite === undefined)
        obj.externalWrite = false;
    if (!obj.observedAt)
        obj.observedAt = new Date().toISOString();
    return raw;
}
async function processSource(sourceId, file, label, emoji, inboxDir, details = false) {
    const filePath = path.join(inboxDir, file);
    const found = fs.existsSync(filePath);
    if (!found) {
        if (sourceId === 'slack') {
            const summaryLines = [
                `⬜ Slack — not connected`,
                `Reason: no Slack payload found`,
                `Next: configure OpenClaw channels.slack, then save payload to:`,
                `${exports.DEFAULT_INBOX_DIR}/openclaw-slack-live.json`,
            ];
            return { id: sourceId, label, emoji, file, found: false, ok: false, candidates: [], summaryLines };
        }
        return { id: sourceId, label, emoji, file, found: false, ok: false, candidates: [], summaryLines: [] };
    }
    let raw;
    try {
        raw = JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
    }
    catch {
        return {
            id: sourceId, label, emoji, file, found: true, ok: false, candidates: [],
            summaryLines: [`❌ ${label} — Error reading payload`],
        };
    }
    const evidence = extractEvidence(sourceId, raw);
    const normalized = normalizePayload(sourceId, raw);
    const validation = (0, validateAdapterSignal_1.validateAdapterSignal)(normalized);
    if (!validation.ok) {
        return {
            id: sourceId, label, emoji, file, found: true, ok: false, candidates: [],
            summaryLines: [`❌ ${label} — Invalid payload`],
        };
    }
    try {
        const signal = (0, toWorldLoopsSignal_1.toWorldLoopsSignal)(validation.signal);
        const result = await (0, brief_1.callWorldLoopsBrief)({ signals: [signal], mode: 'reconciliation' });
        let candidates = result.proposalCandidates ?? [];
        if (candidates.length === 0) {
            const localCandidate = detectLocalCandidate(sourceId, evidence);
            if (localCandidate)
                candidates = [localCandidate];
        }
        // Gmail: suppress false positives for negative-intent and promotional content
        if (sourceId === 'gmail' && candidates.length > 0) {
            const suppressText = [
                evidence.subject ?? '',
                evidence.snippet ?? '',
                ...(evidence.sampleMessages ?? []).map(m => `${m.subject ?? ''} ${m.from ?? ''}`),
            ].join(' ');
            if (hasNegativeIntent(suppressText) || isPromotionalText(suppressText)) {
                candidates = [];
            }
        }
        return {
            id: sourceId, label, emoji, file, found: true, ok: result.ok, candidates,
            summaryLines: buildSummaryLines(sourceId, label, emoji, candidates, evidence, details),
        };
    }
    catch {
        return {
            id: sourceId, label, emoji, file, found: true, ok: false, candidates: [],
            summaryLines: [`⚠️ ${label} — Guard check unavailable`],
        };
    }
}
async function processAllSources(inboxDir, details = false) {
    const results = [];
    for (const src of exports.SOURCES) {
        results.push(await processSource(src.id, src.file, src.label, src.emoji, inboxDir, details));
    }
    return results;
}
function buildBriefLines(results) {
    const lines = [];
    const foundResults = results.filter(r => r.found);
    if (foundResults.length === 0) {
        lines.push('No local handoff payloads found yet.');
        lines.push('');
        lines.push('Add payloads here:');
        for (const src of exports.SOURCES) {
            lines.push(`- ${src.label}: ${exports.DEFAULT_INBOX_DIR}/${src.file}`);
        }
        lines.push('');
        lines.push('Then run:');
        lines.push('npm run guard:daily');
        lines.push('');
        lines.push('Source systems stay untouched.');
        lines.push('externalWrite:false');
        return lines;
    }
    lines.push('Sources:');
    for (const r of results) {
        lines.push(r.found ? `✅ ${r.label}` : `⬜ ${r.label} — missing`);
    }
    lines.push('');
    lines.push('Open loops:');
    for (const r of results) {
        if (r.summaryLines.length > 0) {
            lines.push('');
            for (const line of r.summaryLines) {
                lines.push(line);
            }
        }
    }
    return lines;
}
//# sourceMappingURL=dailyBriefRunner.js.map