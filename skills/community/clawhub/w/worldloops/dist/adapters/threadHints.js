"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.isReplyOrForward = isReplyOrForward;
exports.hasRequestIntent = hasRequestIntent;
exports.classifyThreadHint = classifyThreadHint;
const REPLY_FORWARD_PREFIX_RE = /^(re|fwd|fw):\s*/i;
const REQUEST_PHRASES_KO = [
    '요청드립니다',
    '확인 부탁드립니다',
    '회신 부탁드립니다',
    '가능하실까요',
    '검토 부탁드립니다',
    '답변 부탁드립니다',
];
const REQUEST_PHRASES_EN = [
    'please review',
    'can you confirm',
    'following up',
    'request',
    'could you',
    'please send',
];
function isReplyOrForward(subject) {
    return REPLY_FORWARD_PREFIX_RE.test(subject);
}
function hasRequestIntent(text) {
    if (REQUEST_PHRASES_KO.some((p) => text.includes(p)))
        return true;
    const lower = text.toLowerCase();
    if (REQUEST_PHRASES_EN.some((p) => lower.includes(p)))
        return true;
    return false;
}
/**
 * Returns a classification hint for Re:/Fwd: threads so the API can avoid
 * suppressing them as already-handled. Does not write externally.
 */
function classifyThreadHint(opts) {
    const subject = opts.subject ?? '';
    const snippet = opts.snippet ?? '';
    if (!subject || !isReplyOrForward(subject))
        return null;
    if (hasRequestIntent(`${subject} ${snippet}`)) {
        return 'potential_open_loop';
    }
    // Re:/Fwd: thread without clear request intent still deserves inspection
    return 'needs_inspection';
}
//# sourceMappingURL=threadHints.js.map