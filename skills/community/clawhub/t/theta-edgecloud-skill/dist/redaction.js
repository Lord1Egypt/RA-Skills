const SECRET_KEYS = ['api-key', 'api_key', 'authorization', 'secret', 'password', 'token', 'credential'];
function isSecretKey(key) {
    const normalized = key.toLowerCase();
    return SECRET_KEYS.some((needle) => normalized.includes(needle));
}
export function redact(value) {
    if (!value)
        return '';
    if (value.length <= 8)
        return '********';
    return `${value.slice(0, 3)}***${value.slice(-3)}`;
}
function redactAny(value, parentKey, seen = new WeakSet()) {
    if (value === null || value === undefined)
        return value;
    if (typeof value === 'string') {
        return parentKey && isSecretKey(parentKey) ? redact(value) : value;
    }
    if (typeof value !== 'object')
        return value;
    if (seen.has(value))
        return '[circular]';
    seen.add(value);
    if (Array.isArray(value)) {
        return value.map((entry) => redactAny(entry, parentKey, seen));
    }
    const out = {};
    for (const [k, v] of Object.entries(value)) {
        if (isSecretKey(k)) {
            out[k] = typeof v === 'string' ? redact(v) : '[redacted]';
            continue;
        }
        out[k] = redactAny(v, k, seen);
    }
    return out;
}
export function redactObject(obj) {
    return redactAny(obj);
}
