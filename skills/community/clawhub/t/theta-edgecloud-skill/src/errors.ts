import { isSecretLabel, redact, redactObject } from './redaction.js';
import { StructuredError } from './types.js';

const MAX_MESSAGE_LEN = 280;
// Only this much provider error text is scanned (the result is cut to MAX_MESSAGE_LEN anyway);
// bounding it keeps redaction linear and fast on very large error bodies.
const MAX_SCAN_LEN = 8192;

export function thetaError(input: StructuredError): StructuredError {
  return input;
}

// A plaintext `label<sep>value` pair: the label is one or two word tokens (so `stream key` and
// `x-api-key` both parse), optionally quoted with straight, typographic or back quotes; the
// separator is `=`, `:`, `:=` or `=>` with optional whitespace. Whether the label marks a
// credential is decided by isSecretLabel (the same substring rule as structured redaction).
// Labels are bounded (64 characters per word) so matching stays linear; an optional backslash
// before a quote covers escaped JSON inside error text (`{\"api_key\":\"...\"}`).
// Quote set: straight, back, and typographic quotes (U+2018/2019/201C/201D); separators include
// the full-width colon and equals sign (U+FF1A/FF1D). Written as escapes to keep the source ASCII.
const LABEL_PAIR = /(\\?["'`\u2018\u2019\u201c\u201d]?)([A-Za-z][\w.-]{0,63}(?: [A-Za-z][\w.-]{0,63})?)\\?["'`\u2018\u2019\u201c\u201d]?(\s*(?::=|=>|=|:|\uff1a|\uff1d)\s*)/g;
// Values that are naturally several words (wallet phrases, private keys) are redacted through to
// the end of the message when they are not quoted or bracketed.
const MULTI_WORD_SECRETS = ['mnemonic', 'phrase', 'seedword', 'privatekey'];
const PEM_BLOCK = /-----BEGIN [A-Z0-9 ]{1,40}-----[\s\S]*?(?:-----END [A-Z0-9 ]{1,40}-----|$)/gi;
const QUOTE_CLOSE: Record<string, string> = { '"': '"', "'": "'", '`': '`', '\u201c': '\u201d', '\u2018': '\u2019', '\u201d': '\u201d', '\u2019': '\u2019' };

// End index of the value starting at `start`: a whole quoted string, a whole bracketed list or
// object (quote-aware), or an unquoted run (optionally `Bearer|Basic|Token <value>`).
// Unterminated quotes/brackets run to the end of the message (fail toward redacting more).
function labelledValueEnd(text: string, start: number, multiWord = false): number {
  const first = text[start];
  const skipQuoted = (i: number): number => {
    const close = QUOTE_CLOSE[text[i]];
    for (let j = i + 1; j < text.length; j++) {
      if (text[j] === '\\') { j++; continue; }
      if (text[j] === close) return j + 1;
    }
    return text.length;
  };
  if (first === '\\' && text[start + 1] in QUOTE_CLOSE) {
    // Escaped quoted value: runs to the next escaped matching quote.
    const close = `\\${QUOTE_CLOSE[text[start + 1]]}`;
    const end = text.indexOf(close, start + 2);
    return end === -1 ? text.length : end + close.length;
  }
  if (first in QUOTE_CLOSE) return skipQuoted(start);
  if (first === '[' || first === '{') {
    let depth = 0;
    for (let i = start; i < text.length; ) {
      const ch = text[i];
      if (ch in QUOTE_CLOSE) { i = skipQuoted(i); continue; }
      if (ch === '[' || ch === '{') depth++;
      else if (ch === ']' || ch === '}') { depth--; if (depth === 0) return i + 1; }
      i++;
    }
    return text.length;
  }
  if (multiWord) return text.length;
  // Unquoted run: ends only at whitespace; commas, semicolons, `&` and closing brackets stay
  // inside the value (fail toward redacting more).
  const match = /^(?:(?:Bearer|Basic|Token) )?\S+/i.exec(text.slice(start, start + MAX_SCAN_LEN));
  return start + (match ? match[0].length : 0);
}

function redactLabelledSecrets(text: string): string {
  const label = new RegExp(LABEL_PAIR.source, 'g');
  let out = '';
  let last = 0;
  let match: RegExpExecArray | null;
  while ((match = label.exec(text))) {
    const name = match[2];
    const valueStart = match.index + match[0].length;
    if (!isSecretLabel(name)) {
      // Re-scan from just after the label so a credential label inside a two-word match
      // (`error token=X`) or right after the separator is still found.
      label.lastIndex = match.index + match[1].length + name.split(' ')[0].length;
      continue;
    }
    const normalized = name.toLowerCase().replace(/[^a-z]/g, '');
    const valueEnd = labelledValueEnd(text, valueStart, MULTI_WORD_SECRETS.some((n) => normalized.includes(n)));
    if (valueEnd === valueStart) continue;
    const value = text.slice(valueStart, valueEnd);
    // Numeric usage counts (prompt_tokens: 12) are not secrets, as in structured redaction.
    if (/tokens$/i.test(name.replace(/[^A-Za-z]/g, '')) && /^\d+[,;]?$/.test(value)) continue;
    const scheme = /^(Bearer|Basic|Token)\s+/i.exec(value);
    out += `${text.slice(last, valueStart)}${scheme ? `${scheme[1]} ` : ''}[redacted]`;
    last = valueEnd;
    label.lastIndex = valueEnd;
  }
  return out + text.slice(last);
}

export function sanitizeHttpErrorMessage(message: string): string {
  if (!message) return 'HTTP request failed';
  // Only the first MAX_SCAN_LEN characters are ever examined. A JSON body that fits is parsed and
  // redacted by name; a longer (cut) body fails to parse and gets the plaintext rules below.
  message = message.slice(0, MAX_SCAN_LEN);
  try {
    const parsed = JSON.parse(message);
    if (parsed && typeof parsed === 'object') message = JSON.stringify(redactObject(parsed));
  } catch { /* Plain error text is sanitized below. */ }

  // Bound the scanned text, remove PEM key blocks, then labelled values (whole quoted/list
  // values), then any remaining bare Bearer/Basic tokens.
  const scanned = message.slice(0, MAX_SCAN_LEN).replace(/\s+/g, ' ').replace(PEM_BLOCK, '[redacted]');
  let out = redactLabelledSecrets(scanned)
    .replace(/\b(Bearer|Basic)\s+(?!\[redacted\])([A-Za-z0-9\-._~+/]+=*)/gi, (_m, scheme: string, token: string) => `${scheme} ${redact(token)}`)
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
