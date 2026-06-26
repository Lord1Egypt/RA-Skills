"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateAdapterSignal = validateAdapterSignal;
function isRecord(value) {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
}
function isValidISODate(value) {
    if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(value))
        return false;
    return !isNaN(new Date(value).getTime());
}
function validateAdapterSignal(input) {
    if (!isRecord(input)) {
        return { ok: false, errors: ['Input must be a JSON object'] };
    }
    const errors = [];
    if (typeof input.source !== 'string' || input.source.trim() === '') {
        errors.push('source: required, must be a non-empty string');
    }
    if (typeof input.sourceType !== 'string' || input.sourceType.trim() === '') {
        errors.push('sourceType: required, must be a non-empty string');
    }
    if (input.externalWrite !== false) {
        errors.push('externalWrite: must be false — AdapterSignal does not permit external writes');
    }
    if (typeof input.text !== 'string' || input.text.trim() === '') {
        errors.push('text: required, must be a non-empty string');
    }
    if (typeof input.observedAt !== 'string') {
        errors.push('observedAt: required, must be an ISO 8601 timestamp string');
    }
    else if (!isValidISODate(input.observedAt)) {
        errors.push('observedAt: must be a valid ISO 8601 timestamp (e.g. 2026-05-19T10:30:00.000Z)');
    }
    if (input.url !== undefined && typeof input.url !== 'string') {
        errors.push('url: if provided, must be a string');
    }
    if (input.summary !== undefined && typeof input.summary !== 'string') {
        errors.push('summary: if provided, must be a string');
    }
    if (input.metadata !== undefined && !isRecord(input.metadata)) {
        errors.push('metadata: if provided, must be an object');
    }
    if (errors.length > 0) {
        return { ok: false, errors };
    }
    const signal = {
        source: input.source.trim(),
        sourceType: input.sourceType.trim(),
        externalWrite: false,
        text: input.text.trim(),
        observedAt: input.observedAt,
    };
    if (input.url !== undefined)
        signal.url = input.url;
    if (input.summary !== undefined)
        signal.summary = input.summary;
    if (input.metadata !== undefined)
        signal.metadata = input.metadata;
    return { ok: true, signal };
}
//# sourceMappingURL=validateAdapterSignal.js.map