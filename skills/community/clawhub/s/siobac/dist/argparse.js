// Tiny no-dep argv parser. Handles:
//   --flag value
//   --flag=value
//   --boolean (when next token is missing or another flag)
//   positional args (any token not preceded by an unconsumed --flag)
//
// A "real flag" is `--` followed by a LETTER (e.g. --message). A token that
// starts with dashes but NOT a letter (e.g. a markdown list "- item", or a PEM
// block "-----BEGIN …") is a VALUE, not a flag — so a value beginning with a
// dash is accepted after a value-flag. For the rare value that genuinely looks
// like a flag (`--word …`), use the `--flag=value` form.
const REAL_FLAG = /^--[A-Za-z]/;
export function parseArgs(argv) {
    const positional = [];
    const flags = {};
    for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (!arg.startsWith('--')) {
            positional.push(arg);
            continue;
        }
        const body = arg.slice(2);
        const eq = body.indexOf('=');
        if (eq >= 0) {
            flags[body.slice(0, eq)] = body.slice(eq + 1);
            continue;
        }
        const next = argv[i + 1];
        if (next !== undefined && !REAL_FLAG.test(next)) {
            flags[body] = next;
            i++;
        }
        else {
            flags[body] = true;
        }
    }
    return { positional, flags };
}
export function requireString(flags, key, cmd) {
    const v = flags[key];
    if (v === undefined)
        throw new CliError(`${cmd}: missing required --${key}`);
    if (v === true)
        throw new CliError(`${cmd}: --${key} requires a value`);
    return v;
}
export function optionalString(flags, key) {
    const v = flags[key];
    if (v === undefined)
        return undefined;
    if (v === true)
        return undefined;
    return v;
}
// A non-negative integer flag (e.g. --since <seq>). Absent → undefined. A malformed
// value (non-numeric, negative, or fractional) THROWS rather than silently coercing to
// 0 — a typo'd `--since` used to re-read the whole conversation from the start, which
// reads as "it ignored me".
export function optionalNonNegInt(flags, key) {
    const v = flags[key];
    if (v === undefined || v === true)
        return undefined;
    const n = Number(v);
    if (!Number.isInteger(n) || n < 0) {
        throw new CliError(`--${key} must be a non-negative whole number (a message seq); got "${v}". Omit it to read the most recent window.`);
    }
    return n;
}
export function optionalBoolean(flags, key) {
    return flags[key] === true;
}
export class CliError extends Error {
    constructor(message) {
        super(message);
        this.name = 'CliError';
    }
}
