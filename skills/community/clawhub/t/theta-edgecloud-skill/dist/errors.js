import { redact } from './redaction.js';
const MAX_MESSAGE_LEN = 280;
export function thetaError(input) {
    return input;
}
export function sanitizeHttpErrorMessage(message) {
    if (!message)
        return 'HTTP request failed';
    let out = message
        .replace(/\s+/g, ' ')
        .replace(/\b(Bearer|Basic)\s+([A-Za-z0-9\-._~+/]+=*)/gi, (_m, scheme, token) => `${scheme} ${redact(token)}`)
        .replace(/\b(x-api-key|api[-_]?key|token|secret|password)=([^\s&]+)/gi, (_m, key, value) => `${key}=${redact(value)}`)
        .replace(/\b(authorization|x-api-key|x-tva-sa-secret|api[-_]?key|token|secret|password)\s*:\s*([^\s,;]+)/gi, (_m, key, value) => `${key}: ${redact(value)}`)
        .trim();
    if (out.length > MAX_MESSAGE_LEN) {
        out = `${out.slice(0, MAX_MESSAGE_LEN - 3)}...`;
    }
    return out || 'HTTP request failed';
}
export function isThetaOnDemandCapacityError(status, message) {
    return status === 409 && /no\s+instances\s+available/i.test(message);
}
export function isRetriableHttpError(status, message) {
    return status >= 500 || status === 429 || status === 408 || isThetaOnDemandCapacityError(status, message);
}
export function fromHttpError(service, endpoint, status, message) {
    const sanitized = sanitizeHttpErrorMessage(message);
    const capacityExhausted = isThetaOnDemandCapacityError(status, message);
    return {
        code: capacityExhausted ? 'THETA_ONDEMAND_CAPACITY_EXHAUSTED' : `HTTP_${status}`,
        message: capacityExhausted
            ? `Temporary Theta on-demand capacity exhaustion: ${sanitized}`
            : sanitized,
        retriable: isRetriableHttpError(status, message),
        service,
        endpoint,
        status
    };
}
export function isStructuredError(value) {
    if (!value || typeof value !== 'object')
        return false;
    const candidate = value;
    return typeof candidate.code === 'string' && typeof candidate.message === 'string' && typeof candidate.retriable === 'boolean';
}
export function fromTransportError(service, endpoint, error) {
    const asAny = error;
    const isTimeout = asAny?.name === 'AbortError';
    const message = sanitizeHttpErrorMessage(asAny?.message ?? String(error ?? 'Network request failed'));
    return {
        code: isTimeout ? 'HTTP_408' : 'NETWORK_ERROR',
        message,
        retriable: true,
        service,
        endpoint,
        status: isTimeout ? 408 : undefined
    };
}
