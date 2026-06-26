import { fromHttpError, fromTransportError, isRetriableHttpError, isStructuredError } from '../errors.js';
const RETRIABLE_STATUS = new Set([408, 425, 429, 500, 502, 503, 504]);
function withAuth(headers = {}, auth) {
    if (!auth)
        return headers;
    const token = Buffer.from(`${auth.user}:${auth.pass}`).toString('base64');
    return { ...headers, Authorization: `Basic ${token}` };
}
function toPositiveInt(value, fallback, opts) {
    if (!Number.isFinite(value))
        return fallback;
    const asInt = Math.trunc(value);
    const min = opts?.min ?? Number.MIN_SAFE_INTEGER;
    const max = opts?.max ?? Number.MAX_SAFE_INTEGER;
    return Math.min(Math.max(asInt, min), max);
}
function backoffDelayMs(attempt, baseMs) {
    return baseMs * Math.max(1, 2 ** (attempt - 1));
}
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function request(url, method, body, opts) {
    const timeoutMs = toPositiveInt(opts?.timeoutMs, 20000, { min: 1000, max: 300000 });
    const maxRetries = toPositiveInt(opts?.maxRetries, 2, { min: 0, max: 6 });
    const retryBackoffMs = toPositiveInt(opts?.retryBackoffMs, 250, { min: 25, max: 10000 });
    for (let attempt = 0; attempt <= maxRetries; attempt += 1) {
        const canRetry = attempt < maxRetries;
        try {
            const signal = AbortSignal.timeout(timeoutMs);
            const res = await fetch(url, {
                method,
                headers: withAuth(opts?.headers, opts?.auth),
                body,
                signal
            });
            if (res.ok)
                return res;
            const errorBody = await res.text();
            if (canRetry && (RETRIABLE_STATUS.has(res.status) || isRetriableHttpError(res.status, errorBody))) {
                await sleep(backoffDelayMs(attempt + 1, retryBackoffMs));
                continue;
            }
            throw fromHttpError(opts?.service ?? 'unknown', url, res.status, errorBody);
        }
        catch (error) {
            if (isStructuredError(error)) {
                throw error;
            }
            if (canRetry) {
                await sleep(backoffDelayMs(attempt + 1, retryBackoffMs));
                continue;
            }
            throw fromTransportError(opts?.service ?? 'unknown', url, error);
        }
    }
    throw fromTransportError(opts?.service ?? 'unknown', url, new Error('HTTP request failed after retries'));
}
export async function getJson(url, opts) {
    const res = await request(url, 'GET', undefined, opts);
    return res.json();
}
export async function postJson(url, body, opts) {
    const res = await request(url, 'POST', JSON.stringify(body), {
        ...opts,
        headers: withAuth({ 'content-type': 'application/json', ...(opts?.headers ?? {}) }, opts?.auth),
        auth: undefined
    });
    return res.json();
}
export async function putEmpty(url, opts) {
    await request(url, 'PUT', undefined, opts);
}
export async function putJson(url, body, opts) {
    const res = await request(url, 'PUT', JSON.stringify(body), {
        ...opts,
        headers: { 'content-type': 'application/json', ...(opts?.headers ?? {}) }
    });
    return res.json();
}
export async function deleteEmpty(url, opts) {
    await request(url, 'DELETE', undefined, opts);
}
