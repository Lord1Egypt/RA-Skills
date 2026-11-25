// Share references identify a resource; API deployment configuration owns routing.
const PUBLIC_ORIGINS = new Set(['https://shareone.app', 'https://shareone.vip', 'https://s.shareone.vip']);
const VIEW_PREFIXES = new Set(['s', 'md', 'pdf', 'ppt', 'word', 'file']);

function parseShareReference(value, apiBaseUrl) {
    const raw = String(value || '').trim();
    let pathname = raw.split('?')[0].split('#')[0];
    if (raw.includes('://') || raw.startsWith('//')) {
        let parsed;
        try { parsed = new URL(raw); } catch (_) { throw referenceError(); }
        if (!['http:', 'https:'].includes(parsed.protocol) || parsed.username || parsed.password ||
            (!PUBLIC_ORIGINS.has(parsed.origin) && parsed.origin !== new URL(apiBaseUrl).origin)) throw referenceError();
        pathname = parsed.pathname;
    }
    const parts = pathname.split('/').filter(Boolean);
    if (VIEW_PREFIXES.has(parts[0])) return {prefix: parts[0], shareRef: parts[1] || null};
    if (parts[0] === 'api' && parts.includes('shares')) return {prefix: null, shareRef: parts[parts.indexOf('shares') + 1] || null};
    return {prefix: null, shareRef: parts.at(-1) || null};
}

function referenceError() {
    const error = new Error('The share URL does not belong to a trusted service origin.');
    error.code = 'UNTRUSTED_SHARE_ORIGIN';
    error.hint = 'Configure another deployment explicitly with --base-url or SHAREONE_BASE_URL; the share link cannot change credential routing.';
    return error;
}

module.exports = {parseShareReference};
