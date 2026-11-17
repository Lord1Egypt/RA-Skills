const SECRET_KEYS = ['apikey', 'authorization', 'secret', 'password', 'token', 'credential', 'privatekey', 'mnemonic'];

// Numeric usage/limit counts (prompt_tokens, max_tokens, reasoning_tokens...) are not secrets.
// Any string, array or object under a secret-looking name, including *_tokens, is redacted.
function isSecretKey(key: string, value?: unknown): boolean {
  const normalized = key.toLowerCase().replace(/[^a-z]/g, '');
  if (typeof value === 'number' && normalized.endsWith('tokens')) return false;
  return SECRET_KEYS.some((needle) => normalized.includes(needle));
}

export function redact(value?: string): string {
  if (!value) return '';
  return '[redacted]';
}

function redactAny(value: unknown, parentKey?: string, seen: WeakSet<object> = new WeakSet()): unknown {
  if (value === null || value === undefined) return value;

  if (typeof value === 'string') {
    return parentKey && isSecretKey(parentKey) ? redact(value) : value;
  }

  if (typeof value !== 'object') return value;

  // Only a true cycle (object already on the current path) is collapsed; shared references are kept.
  if (seen.has(value)) return '[circular]';
  seen.add(value);
  try {
    return redactContainer(value, parentKey, seen);
  } finally {
    seen.delete(value);
  }
}

function redactContainer(value: object, parentKey: string | undefined, seen: WeakSet<object>): unknown {
  if (Array.isArray(value)) {
    return value.map((entry) => redactAny(entry, parentKey, seen));
  }

  const out: Record<string, unknown> = {};
  const namedSecret = Object.entries(value).some(([k,v]) => ['name','key'].includes(k) && typeof v === 'string' && isSecretKey(v));
  for (const [k, v] of Object.entries(value)) {
    if (['__proto__','constructor','prototype'].includes(k)) continue;
    if (isSecretKey(k, v) || (namedSecret && k === 'value')) {
      out[k] = typeof v === 'string' ? redact(v) : '[redacted]';
      continue;
    }
    out[k] = redactAny(v, k, seen);
  }
  return out;
}

export function redactObject<T extends Record<string, unknown>>(obj: T): T {
  return redactAny(obj) as T;
}
