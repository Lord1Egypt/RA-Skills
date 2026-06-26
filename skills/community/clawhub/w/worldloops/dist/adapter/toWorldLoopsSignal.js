"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.toWorldLoopsSignal = toWorldLoopsSignal;
const KNOWN_SOURCES = ['slack', 'gmail', 'calendar', 'github', 'manual'];
function toWorldLoopsSignal(adapter) {
    const source = KNOWN_SOURCES.includes(adapter.source)
        ? adapter.source
        : 'manual';
    const signal = {
        source,
        text: adapter.text,
    };
    if (adapter.observedAt)
        signal.createdAt = adapter.observedAt;
    if (adapter.url)
        signal.url = adapter.url;
    return signal;
}
//# sourceMappingURL=toWorldLoopsSignal.js.map