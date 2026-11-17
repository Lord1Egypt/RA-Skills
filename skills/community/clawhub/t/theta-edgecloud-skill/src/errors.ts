import { redact, redactObject } from './redaction.js';
import { StructuredError } from './types.js';

const MAX_MESSAGE_LEN = 280;

export function thetaError(input: StructuredError): StructuredError {
  return input;
}

export function sanitizeHttpErrorMessage(message: string): string {
  if (!message) return 'HTTP request failed';
  try {
    const parsed = JSON.parse(message);
    if (parsed && typeof parsed === 'object') message = JSON.stringify(redactObject(parsed));
  } catch { /* Plain error text is sanitized below. */ }

  let out = message
    .replace(/\s+/g, ' ')
    .replace(/\b(Bearer|Basic)\s+([A-Za-z0-9\-._~+/]+=*)/gi, (_m, scheme: string, token: string) => `${scheme} ${redact(token)}`)
    .replace(/\b(x-api-key|api[-_]?key|token|secret|password)=([^\s&]+)/gi, (_m, key: string, value: string) => `${key}=${redact(value)}`)
    .replace(/\b(authorization|x-api-key|x-tva-sa-secret|api[-_]?key|token|secret|password)\s*:\s*([^\s,;]+)/gi, (_m, key: string, value: string) => `${key}: ${redact(value)}`)
    .trim();

  if (out.length > MAX_MESSAGE_LEN) {
    out = `${out.slice(0, MAX_MESSAGE_LEN - 3)}...`;
  }

  return out || 'HTTP request failed';
}

export function isThetaOnDemandCapacityError(status: number, message: string): boolean {
  return status === 409 && /no\s+instances\s+available/i.test(message);
}

export function isRetriableHttpError(status: number, message: string): boolean {
  return status >= 500 || status === 429 || status === 408 || isThetaOnDemandCapacityError(status, message);
}

export function fromHttpError(service: string, endpoint: string, status: number, message: string): StructuredError {
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

export function isStructuredError(value: unknown): value is StructuredError {
  if (!value || typeof value !== 'object') return false;
  const candidate = value as Partial<StructuredError>;
  return typeof candidate.code === 'string' && typeof candidate.message === 'string' && typeof candidate.retriable === 'boolean';
}

export function fromTransportError(service: string, endpoint: string, error: unknown): StructuredError {
  const asAny = error as { name?: string; message?: string } | undefined;
  const isTimeout = asAny?.name === 'AbortError' || asAny?.name === 'TimeoutError';
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
