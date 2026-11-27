// Shared HTTPS transport. It refuses any non-https:// URL; which Theta host a request goes to is
// chosen and validated by each provider client. Callers pass credentials as headers; redirects are
// refused so credentials are never forwarded to another host, and only GET requests are retried.
import { fromHttpError, fromTransportError, isRetriableHttpError, isStructuredError } from '../errors.js';
import { BasicAuth } from '../types.js';

type HttpOpts = {
  headers?: HeadersInit;
  auth?: BasicAuth;
  service?: string;
  timeoutMs?: number;
  maxRetries?: number;
  retryBackoffMs?: number;
};

const RETRIABLE_STATUS = new Set([408, 425, 429, 500, 502, 503, 504]);

function withAuth(headers: HeadersInit = {}, auth?: BasicAuth): HeadersInit {
  if (!auth) return headers;
  const token = Buffer.from(('' + String(auth.user) + ':' + String(auth.pass))).toString('base64');
  return { ...headers, Authorization: ('Basic ' + String(token)) };
}

function toPositiveInt(value: number | undefined, fallback: number, opts?: { min?: number; max?: number }): number {
  if (!Number.isFinite(value)) return fallback;
  const asInt = Math.trunc(value as number);
  const min = opts?.min ?? Number.MIN_SAFE_INTEGER;
  const max = opts?.max ?? Number.MAX_SAFE_INTEGER;
  return Math.min(Math.max(asInt, min), max);
}

function backoffDelayMs(attempt: number, baseMs: number): number {
  return baseMs * Math.max(1, 2 ** (attempt - 1));
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function request(url: string, method: string, body: BodyInit | undefined, opts?: HttpOpts): Promise<Response> {
  if (!/^https:\/\//i.test(url)) throw new Error('Only https:// URLs are allowed');
  const timeoutMs = toPositiveInt(opts?.timeoutMs, 20000, { min: 1000, max: 300000 });
  // No idempotency contract exists for mutations/inference: never replay them.
  const maxRetries = method === 'GET' ? toPositiveInt(opts?.maxRetries, 2, { min: 0, max: 6 }) : 0;
  const retryBackoffMs = toPositiveInt(opts?.retryBackoffMs, 250, { min: 25, max: 10000 });

  for (let attempt = 0; attempt <= maxRetries; attempt += 1) {
    const canRetry = attempt < maxRetries;

    try {
      const signal = AbortSignal.timeout(timeoutMs);
      const res = await fetch(url, {
        redirect: 'error',
        method,
        headers: withAuth(opts?.headers, opts?.auth),
        body,
        signal
      });

      if (res.ok) return res;

      const errorBody = await res.text();
      if (canRetry && (RETRIABLE_STATUS.has(res.status) || isRetriableHttpError(res.status, errorBody))) {
        await sleep(backoffDelayMs(attempt + 1, retryBackoffMs));
        continue;
      }

      throw fromHttpError(opts?.service ?? 'unknown', url, res.status, errorBody);
    } catch (error) {
      if (isStructuredError(error)) {
        throw error;
      }

      if (canRetry) {
        await sleep(backoffDelayMs(attempt + 1, retryBackoffMs));
        continue;
      }

      // A failure after a write was sent is never reported as retriable (it may have been received).
      throw fromTransportError(opts?.service ?? 'unknown', url, error, method !== 'GET');
    }
  }

  throw fromTransportError(opts?.service ?? 'unknown', url, new Error('HTTP request failed after retries'), method !== 'GET');
}

// Reads the body of an accepted (2xx) response. For writes, a failure here (dropped connection,
// timeout, invalid JSON) is reported as non-retriable, because the provider already accepted it.
async function acceptedJson<T>(res: Response, url: string, method: string, opts?: HttpOpts): Promise<T> {
  try {
    return (await res.json()) as T;
  } catch (error) {
    throw fromTransportError(opts?.service ?? 'unknown', url, error, method !== 'GET');
  }
}

export async function getJson<T>(url: string, opts?: HttpOpts): Promise<T> {
  const res = await request(url, 'GET', undefined, opts);
  return acceptedJson<T>(res, url, 'GET', opts);
}

export async function postJson<T>(url: string, body: unknown, opts?: HttpOpts): Promise<T> {
  const res = await request(url, 'POST', JSON.stringify(body), {
    ...opts,
    headers: withAuth({ 'content-type': 'application/json', ...(opts?.headers ?? {}) }, opts?.auth),
    auth: undefined
  });
  return acceptedJson<T>(res, url, 'POST', opts);
}

export async function putEmpty(url: string, opts?: HttpOpts): Promise<void> {
  await request(url, 'PUT', undefined, opts);
}

export async function putJson<T>(url: string, body: unknown, opts?: HttpOpts): Promise<T> {
  const res = await request(url, 'PUT', JSON.stringify(body), {
    ...opts,
    headers: { 'content-type': 'application/json', ...(opts?.headers ?? {}) }
  });
  return acceptedJson<T>(res, url, 'PUT', opts);
}

export async function deleteEmpty(url: string, opts?: HttpOpts): Promise<void> {
  await request(url, 'DELETE', undefined, opts);
  // Theta's delete endpoints take no body. Like every non-GET request, it is never retried.
}
