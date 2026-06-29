// Resolve an invite (raw slug or a share/manifest/connect URL) to { slug, host }.
// A bare slug uses this skill's API base (the production server); a full URL
// keeps its own host + any reverse-proxy prefix (e.g. /external) so reach-out
// works against whatever server the invite came from. Ported from ovoclaw-connect
// when the two skills merged.
import { getApiBase } from './api.js';
const ROUTE_SEGMENTS = new Set(['share', 'manifest', 'connect']);
function inviteError(message) {
    const err = new Error(message);
    err.code = 'invalid_request';
    return err;
}
// A connect code is shown to humans as `<code>@siobac` (email-like). Strip that
// suffix and lowercase, since codes are case-insensitive. Leaves real URLs and
// bare slugs untouched aside from the suffix.
function stripSiobacSuffix(s) {
    return s.replace(/@siobac(\.com)?$/i, '');
}
export function parseInvite(input) {
    const trimmed = input.trim();
    if (!trimmed)
        throw inviteError('invite is empty');
    // No "/" → a bare connect code (possibly `alex@siobac`). Use our configured
    // base. (Checked before URL parsing so the `@` in a code isn't mistaken for a
    // userinfo URL.)
    if (!trimmed.includes('/') && !trimmed.includes(':')) {
        const code = stripSiobacSuffix(trimmed).toLowerCase();
        if (!code)
            throw inviteError(`No connect code found in: ${input}`);
        return { slug: code, host: getApiBase() };
    }
    let url;
    try {
        url = new URL(trimmed);
    }
    catch {
        throw inviteError(`Could not parse invite: ${input}`);
    }
    if (url.protocol !== 'http:' && url.protocol !== 'https:') {
        throw inviteError(`Invite must be http(s); got "${url.protocol}" in ${input}`);
    }
    const segments = url.pathname.split('/').filter(Boolean);
    if (segments.length === 0)
        throw inviteError(`No slug found in URL: ${input}`);
    // Find the route marker ("share"/"manifest"/"connect"); the segment after it
    // is the slug, anything before it is the host prefix.
    let routeIdx = -1;
    for (let i = segments.length - 1; i >= 0; i--) {
        if (ROUTE_SEGMENTS.has(segments[i])) {
            routeIdx = i;
            break;
        }
    }
    let slug;
    let basePath;
    if (routeIdx >= 0 && routeIdx < segments.length - 1) {
        slug = segments[routeIdx + 1];
        basePath = segments.slice(0, routeIdx).join('/');
    }
    else {
        slug = segments[segments.length - 1];
        basePath = segments.slice(0, -1).join('/');
    }
    if (!slug)
        throw inviteError(`No slug found in URL: ${input}`);
    const host = basePath ? `${url.protocol}//${url.host}/${basePath}` : `${url.protocol}//${url.host}`;
    return { slug, host };
}
