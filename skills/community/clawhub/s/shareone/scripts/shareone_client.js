const http = require('http');
const https = require('https');
const net = require('net');
const tls = require('tls');
const fs = require('fs');
const path = require('path');
const API_CONTRACT = require('./api_contract.json');

const DEFAULT_BASE_URL = 'https://shareone.app';
const CREDENTIALS_FILENAME = '.shareone_credentials';
const SUDOWORK_SECRET_NAMESPACE = 'service:shareone';
const SUDOWORK_SECRET_KEY = 'X-API-Key';
const CREDENTIAL_MODE_DIRECT = 'direct';
const CREDENTIAL_MODE_SUDOWORK_PROXY = 'sudowork_proxy';
const CREDENTIAL_MODE_DIRECT_FALLBACK = 'direct_fallback';

let credentialModePromise = null;

function isSudowork() {
    return Boolean(process.env.SUDOWORK_AUTH_PROXY_URL && process.env.SUDOWORK_AUTH_PROXY_TOKEN);
}

function getSudoworkBaseUrl() {
    return process.env.SUDOWORK_AUTH_PROXY_BASE_URL || String(process.env.SUDOWORK_AUTH_PROXY_URL || '').replace(/\/proxy\/?$/, '');
}

function getBaseUrl() {
    return process.env.SHAREONE_BASE_URL || DEFAULT_BASE_URL;
}

function getSkillCredentialsPath() {
    return path.join(path.resolve(__dirname, '..'), CREDENTIALS_FILENAME);
}

function getCredentialPathCandidates() {
    return [getSkillCredentialsPath()];
}

function canWriteCredentialsPath(credentialsPath) {
    try {
        if (fs.existsSync(credentialsPath)) {
            fs.accessSync(credentialsPath, fs.constants.W_OK);
            return true;
        }

        const raw = String(credentialsPath);
        const lastSlash = Math.max(raw.lastIndexOf('/'), raw.lastIndexOf('\\'));
        const parent = lastSlash > 0 ? raw.slice(0, lastSlash) : path.dirname(raw);
        fs.accessSync(parent, fs.constants.W_OK);
        return true;
    } catch (_) {
        return false;
    }
}

function getCredentialsPath() {
    return getSkillCredentialsPath();
}

function readLocalApiKey() {
    for (const credentialsPath of getCredentialPathCandidates()) {
        if (!fs.existsSync(credentialsPath)) continue;
        try {
            const data = JSON.parse(fs.readFileSync(credentialsPath, 'utf8'));
            if (data && data.api_key) return data.api_key;
        } catch (_) {
            // Try the next candidate.
        }
    }
    return null;
}

function resolveDirectApiKey(explicitApiKey) {
    return explicitApiKey || process.env.SHAREONE_API_KEY || readLocalApiKey();
}

/**
 * Save an API key to local credentials file.
 *
 * By default, refuses to overwrite an existing key with a *different* key.
 * Pass `{ force: true }` to allow overwriting (e.g. when the user explicitly
 * provides a new key via `--key`).
 *
 * Returns the path where the key was saved.
 * Throws if overwrite is blocked.
 */
function saveLocalApiKey(apiKey, { force = false } = {}) {
    if (!force) {
        const existing = readLocalApiKey();
        if (existing && existing !== apiKey) {
            const error = new Error(
                'EXISTING_KEY_CONFLICT: A different API Key is already saved. '
                + 'Use --key to explicitly replace it, or delete the existing key first.'
            );
            error.code = 'EXISTING_KEY_CONFLICT';
            error.existingKeyHint = existing.slice(0, 4) + '...' + existing.slice(-4);
            throw error;
        }
    }
    const candidates = getCredentialPathCandidates();
    const credentialsPath = candidates.find(canWriteCredentialsPath) || candidates[candidates.length - 1] || getCredentialsPath();
    fs.writeFileSync(credentialsPath, JSON.stringify({ api_key: apiKey }), { mode: 0o600 });
    try {
        fs.chmodSync(credentialsPath, 0o600);
    } catch (_) {
        // Best-effort on filesystems that do not support POSIX permissions.
    }
    return credentialsPath;
}

function deleteLocalApiKey() {
    let deleted = false;
    for (const credentialsPath of getCredentialPathCandidates()) {
        try {
            if (!fs.existsSync(credentialsPath)) continue;
            fs.unlinkSync(credentialsPath);
            deleted = true;
        } catch (_) {
            // Try deleting the next candidate.
        }
    }
    return deleted;
}

function appendPath(baseUrl, apiPath) {
    const trimmedBase = String(baseUrl).replace(/\/+$/, '');
    const normalizedPath = apiPath.startsWith('/') ? apiPath : `/${apiPath}`;
    return `${trimmedBase}${normalizedPath}`;
}

const MAX_REDIRECTS = 5;

// Header names that carry credentials; stripped when a redirect crosses hosts
// so we never hand the API key to a different origin.
const AUTH_HEADER_NAMES = ['x-api-key', 'authorization', 'cookie'];

function stripAuthHeaders(headers) {
    const next = {};
    for (const key of Object.keys(headers || {})) {
        if (!AUTH_HEADER_NAMES.includes(key.toLowerCase())) next[key] = headers[key];
    }
    return next;
}

// --- Proxy support -------------------------------------------------------
// Node's built-in http/https clients ignore HTTPS_PROXY/HTTP_PROXY/NO_PROXY
// (unlike curl/git/python-requests). In proxy-only-egress environments
// (corporate VPN + Clash/Verge system proxy) direct DNS is blocked, so every
// command fails with ENOTFOUND even though the proxy is reachable. Honor the
// standard env vars: tunnel HTTPS via CONNECT, proxy plain HTTP via absolute
// URI. localhost and NO_PROXY hosts stay DIRECT — so the local Sudowork auth
// proxy (127.0.0.1) is never itself re-proxied.

function shouldBypassProxy(host) {
    const h = String(host || '').toLowerCase().replace(/^\[|\]$/g, '');
    if (h === 'localhost' || h === '127.0.0.1' || h === '::1') return true;
    const noProxy = (process.env.NO_PROXY || process.env.no_proxy || '')
        .split(',').map(s => s.trim().toLowerCase().replace(/^\[|\]$/g, '')).filter(Boolean);
    return noProxy.some(entry => entry === '*' || h === entry ||
        h.endsWith('.' + entry.replace(/^\./, '')) || (entry.startsWith('.') && h.endsWith(entry)));
}

function resolveProxyUrl(target) {
    const raw = target.protocol === 'https:'
        ? (process.env.HTTPS_PROXY || process.env.https_proxy || process.env.HTTP_PROXY || process.env.http_proxy)
        : (process.env.HTTP_PROXY || process.env.http_proxy);
    if (!raw || shouldBypassProxy(target.hostname)) return null;
    try { return new URL(raw); } catch (_) { return null; }
}

function proxyAuthHeader(proxyUrl) {
    if (!proxyUrl.username) return null;
    const creds = decodeURIComponent(proxyUrl.username) + ':' + decodeURIComponent(proxyUrl.password || '');
    return 'Basic ' + Buffer.from(creds).toString('base64');
}

// https.Agent that reaches the origin through an HTTP CONNECT tunnel.
function connectTunnelAgent(proxyUrl) {
    const auth = proxyAuthHeader(proxyUrl);
    return new (class extends https.Agent {
        createConnection(opts, cb) {
            const host = opts.host || opts.hostname;
            const port = Number(opts.port) || 443;
            const sock = net.connect(Number(proxyUrl.port) || 80, proxyUrl.hostname);
            let settled = false;
            const fail = (err) => { if (!settled) { settled = true; sock.destroy(); cb(err); } };
            sock.once('error', fail);
            sock.once('connect', () => {
                let line = `CONNECT ${host}:${port} HTTP/1.1\r\nHost: ${host}:${port}\r\n`;
                if (auth) line += `Proxy-Authorization: ${auth}\r\n`;
                sock.write(line + '\r\n');
            });
            let buf = Buffer.alloc(0);
            const onData = (chunk) => {
                buf = Buffer.concat([buf, chunk]);
                if (buf.indexOf('\r\n\r\n') === -1) return;
                sock.removeListener('data', onData);
                const statusLine = buf.slice(0, buf.indexOf('\r\n')).toString();
                if (!/^HTTP\/\d(?:\.\d)? 200/.test(statusLine)) {
                    return fail(new Error(`Proxy CONNECT failed: ${statusLine}`));
                }
                // Verify the origin cert by default (secure), but don't hardcode
                // rejectUnauthorized — leaving it to the TLS default lets standard
                // env vars work: NODE_EXTRA_CA_CERTS for a corporate MITM-proxy CA
                // (common in these environments), and forward an explicit ca/flag
                // if the caller set one.
                const tlsOpts = { socket: sock, servername: host };
                if (opts.ca) tlsOpts.ca = opts.ca;
                if (opts.rejectUnauthorized !== undefined) tlsOpts.rejectUnauthorized = opts.rejectUnauthorized;
                const tlsSock = tls.connect(tlsOpts, () => { settled = true; cb(null, tlsSock); });
                tlsSock.once('error', fail);
            };
            sock.on('data', onData);
        }
    })();
}

function requestBuffer(url, options = {}, body = null, redirectsLeft = MAX_REDIRECTS) {
    return new Promise((resolve, reject) => {
        const target = new URL(url);
        const isHttps = target.protocol === 'https:';
        const client = isHttps ? https : http;
        const proxyUrl = resolveProxyUrl(target);

        const handleResponse = (res) => {
            // Follow redirects — Node's http client does not auto-follow, so a
            // bare `curl` would succeed where this used to surface the 3xx as an
            // error (e.g. an infra http->https / trailing-slash 301 on a DELETE).
            // Preserve the method and body (API redirects are transport-level,
            // not a POST->GET downgrade); drop the API key on a cross-host hop.
            if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location && redirectsLeft > 0) {
                res.resume(); // drain so the socket can be reused
                let nextUrl;
                try {
                    nextUrl = new URL(res.headers.location, target);
                } catch (_) {
                    nextUrl = null;
                }
                if (nextUrl) {
                    const sameHost = nextUrl.host === target.host;
                    const headers = sameHost ? (options.headers || {}) : stripAuthHeaders(options.headers || {});
                    resolve(requestBuffer(nextUrl.toString(), { ...options, headers }, body, redirectsLeft - 1));
                    return;
                }
            }
            const chunks = [];
            res.on('data', chunk => chunks.push(Buffer.from(chunk)));
            res.on('end', () => {
                const data = Buffer.concat(chunks);
                const text = data.toString('utf8');
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve({ statusCode: res.statusCode, headers: res.headers, data, text });
                    return;
                }
                const error = new Error(`HTTP ${res.statusCode}: ${text}`);
                error.statusCode = res.statusCode;
                error.responseText = text;
                error.responseHeaders = res.headers;
                error.requestMethod = options.method || 'GET';
                error.requestUrl = url;
                error.replaySafe = ['GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE'].includes(String(error.requestMethod).toUpperCase());
                reject(error);
            });
        };

        const reqOptions = {
            method: options.method || 'GET',
            headers: { ...(options.headers || {}) },
        };
        let req;
        if (proxyUrl && !isHttps) {
            // Plain-HTTP target: ask the proxy for the absolute URL.
            const auth = proxyAuthHeader(proxyUrl);
            req = client.request({
                hostname: proxyUrl.hostname,
                port: Number(proxyUrl.port) || 80,
                path: target.href,
                method: reqOptions.method,
                headers: { ...reqOptions.headers, host: target.host, ...(auth ? { 'proxy-authorization': auth } : {}) },
            }, handleResponse);
        } else {
            // HTTPS (tunnelled via CONNECT when proxied) or direct.
            if (proxyUrl) reqOptions.agent = connectTunnelAgent(proxyUrl);
            req = client.request(target, reqOptions, handleResponse);
        }

        req.on('error', error => {
            error.requestMethod = options.method || 'GET';
            error.requestUrl = url;
            error.replaySafe = ['GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE'].includes(String(error.requestMethod).toUpperCase());
            reject(error);
        });
        if (options.timeoutMs) {
            req.setTimeout(options.timeoutMs, () => {
                const error = new Error('Request timed out');
                error.code = 'ETIMEDOUT';
                req.destroy(error);
            });
        }
        if (body) req.write(body);
        req.end();
    });
}

function buildJsonRequestBody(payload) {
    const body = payload === null ? null : JSON.stringify(payload);
    const headers = { 'Content-Type': 'application/json' };
    if (body !== null) headers['Content-Length'] = Buffer.byteLength(body);
    return { body, headers };
}

async function requestJsonUrl(url, options = {}, payload = null) {
    const { body, headers } = buildJsonRequestBody(payload);
    const res = await requestBuffer(url, {
        ...options,
        headers: {
            ...headers,
            ...(options.headers || {}),
        },
    }, body);
    return JSON.parse(res.text);
}

async function requestPublicShareOneJson(apiPath, options = {}, payload = null) {
    return requestJsonUrl(appendPath(getBaseUrl(), apiPath), options, payload);
}

function buildSudoworkSecretsUrl(pathSuffix = '') {
    const baseUrl = getSudoworkBaseUrl();
    if (!baseUrl) {
        throw new Error('SUDOWORK_AUTH_PROXY_BASE_URL is not available');
    }
    return appendPath(baseUrl, `/secrets${pathSuffix}`);
}

async function requestSudoworkSecrets(pathSuffix = '', options = {}, payload = null) {
    if (!isSudowork()) {
        throw new Error('Sudowork environment is not available');
    }
    const { body, headers } = buildJsonRequestBody(payload);
    const res = await requestBuffer(buildSudoworkSecretsUrl(pathSuffix), {
        ...options,
        headers: {
            ...headers,
            ...(options.headers || {}),
            Authorization: `Bearer ${process.env.SUDOWORK_AUTH_PROXY_TOKEN}`,
        },
    }, body);
    return JSON.parse(res.text);
}

async function listSudoworkSecrets(namespace = SUDOWORK_SECRET_NAMESPACE) {
    const query = `?namespace=${encodeURIComponent(namespace)}`;
    const result = await requestSudoworkSecrets(query, { method: 'GET' }, null);
    return Array.isArray(result.data) ? result.data : [];
}

function hasShareOneSecret(secrets) {
    return secrets.some(secret => secret && secret.namespace === SUDOWORK_SECRET_NAMESPACE && secret.key === SUDOWORK_SECRET_KEY);
}

async function hasSudoworkApiKey() {
    const mode = await detectCredentialMode();
    return mode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && mode.hasSudoworkKey;
}

async function detectCredentialMode({ refresh = false } = {}) {
    if (!refresh && credentialModePromise) return credentialModePromise;

    credentialModePromise = (async () => {
        if (!isSudowork()) {
            return {
                mode: CREDENTIAL_MODE_DIRECT,
                isSudowork: false,
                sudoworkAvailable: false,
                hasSudoworkKey: false,
                secrets: [],
                error: null,
            };
        }

        try {
            const secrets = await listSudoworkSecrets(SUDOWORK_SECRET_NAMESPACE);
            return {
                mode: CREDENTIAL_MODE_SUDOWORK_PROXY,
                isSudowork: true,
                sudoworkAvailable: true,
                hasSudoworkKey: hasShareOneSecret(secrets),
                secrets,
                error: null,
            };
        } catch (error) {
            return {
                mode: CREDENTIAL_MODE_DIRECT_FALLBACK,
                isSudowork: true,
                sudoworkAvailable: false,
                hasSudoworkKey: false,
                secrets: [],
                error,
            };
        }
    })();

    return credentialModePromise;
}

function resetCredentialModeCache() {
    credentialModePromise = null;
}

async function saveSudoworkApiKey(apiKey) {
    const pathSuffix = `/${encodeURIComponent(SUDOWORK_SECRET_NAMESPACE)}/${encodeURIComponent(SUDOWORK_SECRET_KEY)}`;
    return requestSudoworkSecrets(pathSuffix, { method: 'PUT' }, {
        value: apiKey,
        description: 'ShareOne API Key',
    });
}

async function deleteSudoworkApiKey() {
    const pathSuffix = `/${encodeURIComponent(SUDOWORK_SECRET_NAMESPACE)}/${encodeURIComponent(SUDOWORK_SECRET_KEY)}`;
    return requestSudoworkSecrets(pathSuffix, { method: 'DELETE' }, null);
}

async function buildShareOneRequest(apiPath, options = {}) {
    const targetUrl = appendPath(getBaseUrl(), apiPath);
    const headers = { ...(options.headers || {}) };
    const credentialMode = await detectCredentialMode();

    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && options.authRequired !== false) {
        delete headers['X-API-Key'];
        delete headers['x-api-key'];
        return {
            url: process.env.SUDOWORK_AUTH_PROXY_URL,
            options: {
                ...options,
                headers: {
                    ...headers,
                    Authorization: `Bearer ${process.env.SUDOWORK_AUTH_PROXY_TOKEN}`,
                    'X-Secret-Namespace': 'service:shareone',
                    'X-Remote-URL': targetUrl,
                    'X-Auth-Scheme': 'header',
                    'X-Auth-Header': 'X-API-Key',
                    'X-Secret-Key': 'X-API-Key'
                },
            },
        };
    }

    if (options.authRequired !== false) {
        const apiKey = resolveDirectApiKey(options.apiKey);
        if (apiKey) headers['X-API-Key'] = apiKey;
    }

    return {
        url: targetUrl,
        options: {
            ...options,
            headers,
        },
    };
}

async function requestShareOneBuffer(apiPath, options = {}, body = null) {
    const built = await buildShareOneRequest(apiPath, options);
    try {
        return await requestBuffer(built.url, built.options, body);
    } catch (error) {
        const method = String(options.method || 'GET').toUpperCase();
        const key = Object.entries(options.headers || {}).find(([name]) => name.toLowerCase() === 'idempotency-key');
        const pathName = new URL(appendPath(getBaseUrl(), apiPath)).pathname;
        const supported = API_CONTRACT.idempotency_operations.some(op => op.method === method &&
            new RegExp('^' + op.path.replace(/\{[^}]+\}/g, '[^/]+') + '$').test(pathName));
        error.replaySafe = ['GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE'].includes(method) || Boolean(key && supported);
        throw error;
    }
}

async function requestShareOneJson(apiPath, options = {}, payload = null) {
    const { body, headers } = buildJsonRequestBody(payload);

    const res = await requestShareOneBuffer(apiPath, {
        ...options,
        headers: {
            ...headers,
            ...(options.headers || {}),
        },
    }, body);
    return JSON.parse(res.text);
}

function getErrorDetail(error) {
    const text = String(error && error.responseText ? error.responseText : '');
    if (!text) return '';
    try {
        const parsed = JSON.parse(text);
        if (!parsed || typeof parsed !== 'object') {
            return text;
        }
        const detail = parsed.detail;
        if (detail && typeof detail === 'object') {
            return String(detail.message || detail.code || parsed.message || text);
        }
        return String(detail || parsed.message || text);
    } catch (_) {
        return text;
    }
}

function isSudoworkMissingKeyError(error) {
    if (!error) return false;
    const detail = getErrorDetail(error);

    if (error.statusCode === 502) {
        return /secret|key|credential|not found|missing|未配置|不存在|缺少/i.test(detail || error.message || '');
    }

    if (error.statusCode !== 401) return false;
    return /Missing API Key/i.test(detail);
}

function isAuthFailedError(error) {
    if (!error) return false;
    const body = parseErrorBody(error);
    const code = body.error_code || (body.detail && body.detail.code);
    if (code && API_CONTRACT.errors[code]) return API_CONTRACT.errors[code].category === 'auth_failed';
    const detail = getErrorDetail(error);
    if (/password|login required|email.gate/i.test(detail)) return false;
    return error.statusCode === 401 || /Invalid API Key|Inactive user/i.test(detail);
}

function parseErrorBody(error) {
    try { return JSON.parse(error.responseText || '{}'); } catch (_) { return {}; }
}

// --- Error steering (cli-steering rules 7 + 5b) --------------------------
// Every failure carries a stable ERROR:<CODE> token, a semantic exit code, and a
// RETRYABLE flag (+ optional HINT) so the LLM/shell can branch on "retry vs
// re-auth vs fix-the-call" without parsing prose. One mapping, one emitter — SSOT.
const ERROR_CATEGORY_META = {
    validation: { exit: 2, retryable: false },  // bad/missing args — fix the call
    not_found: { exit: 4, retryable: false },
    conflict: { exit: 5, retryable: false },     // already exists / precondition
    permission: { exit: 6, retryable: false },
    access_gate: { exit: 6, retryable: false },
    auth_failed: { exit: 7, retryable: false },  // re-auth, don't retry blindly
    rate_limited: { exit: 8, retryable: true },  // back off and retry
    transient: { exit: 9, retryable: true },     // 5xx / network — retry
    error: { exit: 1, retryable: false },        // uncategorized catch-all
};

const ERROR_CODE_CATEGORY = {
    UNKNOWN_ARGUMENT: 'validation', MISSING_VALUE: 'validation', INVALID_BOOLEAN: 'validation',
    BAD_ARGS: 'validation', BAD_STATUS: 'validation', BAD_JSON_MODE: 'validation',
    MISSING_EMAIL: 'validation', MISSING_CODE: 'validation', INVALID_CODE_FORMAT: 'validation', NO_ACTION: 'validation',
    ACTIVE_SHARE_TASK: 'conflict', FILE_PREVIOUSLY_PUBLISHED: 'conflict', EXISTING_KEY_CONFLICT: 'conflict',
    DATA_FILE_UNREADABLE: 'not_found', UPDATE_VERIFY_FAILED: 'conflict',
    INVALID_STATE: 'validation', STATE_REQUIRED: 'validation', CONTENT_REQUIRED: 'validation',
    NO_SETTINGS_PROVIDED: 'validation', OPTION_NOT_SUPPORTED: 'validation',
    MISSING_SHARE_REF: 'validation', MISSING_ACTION: 'validation', INVALID_ACTION: 'validation', MISSING_USERNAMES: 'validation',
    LOOKS_LIKE_SHARE_LINK: 'validation', IS_REPLY: 'validation', INVALID_RESPONSE: 'validation',
    BINARY_NO_ALLOW_COMMENTS: 'validation', BINARY_NO_ALLOW_DATA: 'validation',
    BINARY_NO_SHARE_ID: 'validation', DOWNLOAD_NOT_ALLOWED: 'validation',
    FILE_NOT_FOUND: 'not_found', COMMENT_NOT_FOUND: 'not_found',
    CUSTOM_SLUG_TAKEN: 'conflict',
    KEY_NOT_FOUND: 'auth_failed', AUTH_FAILED: 'auth_failed', SUDOWORK_MANAGED_KEY: 'auth_failed',
    SUDOWORK_ENV_OK_KEY_NOT_FOUND: 'auth_failed', SUDOWORK_WRITE_BROKEN: 'auth_failed',
    RATE_LIMIT_EXCEEDED: 'rate_limited',
};

const ERROR_HINTS = {
    STATE_REQUIRED: '重跑并加 --state：resolved-agree | open-disagree | open-need-input。',
    INVALID_STATE: '--state 只能是 resolved-agree | open-disagree | open-need-input。',
    KEY_NOT_FOUND: '先运行 ensure_credentials.js 配置/创建 API Key，再重试。',
    AUTH_FAILED: 'Check or update the existing account key; preserve the identity that owns the share.',
    SUDOWORK_ENV_OK_KEY_NOT_FOUND: '先运行 check_api_key.js，再用 save_api_key.js / create_guest_key.js 设置 Key。',
    RATE_LIMIT_EXCEEDED: '触发限流：退避几秒后重试。',
    CUSTOM_SLUG_TAKEN: '换一个 --slug；若这是你自己删掉的旧链接，直接重发同名 slug 即可复用。',
    SUDOWORK_MANAGED_KEY: 'Sudowork 环境下 Key 由平台托管，勿手动传 --api-key。',
};

// Print the ERROR/message/HINT/RETRYABLE envelope for `code`; return the semantic
// exit code (does not exit — caller decides). `hint`/`retryable` override the map.
function _emitErrorEnvelope(code, message, opts = {}) {
    const parts = String(code).replace(/^ERROR:/, '').split(':');
    code = parts.shift();
    if (!message && parts.length) message = parts.join(':');
    const spec = API_CONTRACT.errors[code] || {};
    const category = opts.category || spec.category || ERROR_CODE_CATEGORY[code] || 'error';
    const meta = ERROR_CATEGORY_META[category] || ERROR_CATEGORY_META.error;
    console.error(`ERROR:${code}`);
    if (message) console.error(message);
    const hint = opts.hint != null ? opts.hint : (spec.hint || ERROR_HINTS[code]);
    if (hint) console.error(`HINT:${hint}`);
    const retryable = opts.retryable != null ? opts.retryable : (spec.retryable ?? meta.retryable);
    const exit = opts.exit != null ? opts.exit : meta.exit;
    console.error(`RETRYABLE:${retryable}`);
    if (opts.retryAfter != null) console.error(`RETRY_AFTER:${opts.retryAfter}`);
    console.error('ERROR_JSON:' + JSON.stringify({ error_code: code, category, message: message || '',
        hint: hint || '', retryable, exit_code: exit, ...(opts.status ? { status: opts.status } : {}),
        ...(opts.detail != null ? { detail: opts.detail } : {}), ...(opts.retryAfter != null ? { retry_after: opts.retryAfter } : {}) }));
    return exit;
}

// Terminal emitter for inline (validation/precondition) failure sites: emit the
// envelope and exit with the semantic code. Replaces `console.error('ERROR:X')`
// + `process.exit(1)`.
function emitError(code, message, opts = {}) {
    process.exit(_emitErrorEnvelope(code, message, opts));
}

// For runtime/API errors caught in a script's main(): emit the envelope and
// RETURN the semantic exit code so the caller can `process.exit(...)`.
function printShareOneScriptError(error) {
    if (isSudowork() && isSudoworkMissingKeyError(error)) {
        return _emitErrorEnvelope('SUDOWORK_ENV_OK_KEY_NOT_FOUND',
            '请先运行 check_api_key.js，并按提示通过 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。');
    }
    const status = error && error.statusCode;
    const body = parseErrorBody(error || {});
    const detail = body.detail;
    const fallback = {400: 'BAD_REQUEST', 401: 'AUTH_REQUIRED', 403: 'FORBIDDEN', 404: 'NOT_FOUND',
        405: 'METHOD_NOT_ALLOWED', 413: 'PAYLOAD_TOO_LARGE', 415: 'UNSUPPORTED_MEDIA_TYPE',
        409: 'CONFLICT', 410: 'OPERATION_RESOURCE_GONE', 422: 'VALIDATION_ERROR', 429: 'RATE_LIMIT_EXCEEDED'};
    let code = body.error_code || (detail && detail.code) || fallback[status];
    if (!code && status >= 500) code = 'SERVER_ERROR';
    if (!code && error && error.code) code = error.code;
    if (!code) {
        const match = String(error && error.message || '').match(/^([A-Z][A-Z0-9_]+):/);
        code = match ? match[1] : 'UNKNOWN_ERROR';
    }
    const transport = ['ECONNRESET', 'ECONNREFUSED', 'ETIMEDOUT', 'ENOTFOUND', 'EAI_AGAIN', 'EPIPE'].includes(code);
    const spec = API_CONTRACT.errors[code];
    const category = spec?.category || API_CONTRACT.errors[fallback[status]]?.category;
    const retryable = Boolean(body.retryable ?? (spec ? spec.retryable : transport)) &&
        (!(transport || status >= 500 || status === 429) || error.replaySafe !== false);
    return _emitErrorEnvelope(code, getErrorDetail(error) || String(error && error.message || ''), {
        ...(category ? {category} : {}),
        ...(transport ? {category: 'transient', hint: 'Check connectivity and back off; retry writes only when replay is safe.'} : {}),
        hint: body.hint || (transport ? 'Check connectivity and back off; retry writes only when replay is safe.' : undefined),
        retryable, status, detail, retryAfter: error && error.responseHeaders && error.responseHeaders['retry-after'],
    });
}

// Generated from the server's authoritative lifecycle contract.
const AGENT_REPLY_STATES = API_CONTRACT.agent_reply_states;

function parseScriptArgs(options, positionalCount, usage) {
    const args = process.argv.slice(2);
    const values = {};
    const positionals = [];
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--help') { console.log(usage); process.exit(0); }
        if (arg.startsWith('--')) {
            if (!options.includes(arg)) emitError('UNKNOWN_ARGUMENT', arg, {hint: usage});
            const value = args[++i];
            if (value === undefined || value.startsWith('--')) emitError('MISSING_VALUE', arg, {hint: usage});
            values[arg.slice(2)] = value;
        } else positionals.push(arg);
    }
    if (positionals.length !== positionalCount) emitError('BAD_ARGS', 'Incorrect positional arguments.', {hint: usage});
    if (values['base-url']) process.env.SHAREONE_BASE_URL = values['base-url'];
    return { values, positionals };
}

// Extract the trailing share ref (slug or 16-char share_id) from a full URL, a
// `/s/<ref>` path, a raw-file `/file/<ref>` path, an API `/api/.../shares/<ref>`
// path, or a bare ref. Shared by every script that accepts a
// `<share_link_or_ref>` positional arg.
function extractShareRef(value) {
    const raw = String(value || '').trim();
    if (!raw) return null;
    try {
        const parsed = raw.includes('://') ? new URL(raw) : null;
        const path = parsed ? parsed.pathname : raw.split('?')[0].split('#')[0];
        const parts = path.split('/').filter(Boolean);
        if (parts.length === 0) return raw;
        if (parts[0] === 'file' && parts.length >= 2) return parts[1];
        if (parts[0] === 'api' && parts.includes('shares')) {
            const index = parts.indexOf('shares');
            return parts[index + 1] || raw;
        }
        return parts[parts.length - 1] || raw;
    } catch (_) {
        return raw;
    }
}

module.exports = {
    AGENT_REPLY_STATES,
    CREDENTIAL_MODE_DIRECT,
    CREDENTIAL_MODE_DIRECT_FALLBACK,
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    DEFAULT_BASE_URL,
    SUDOWORK_SECRET_KEY,
    SUDOWORK_SECRET_NAMESPACE,
    appendPath,
    deleteLocalApiKey,
    deleteSudoworkApiKey,
    detectCredentialMode,
    extractShareRef,
    getBaseUrl,
    getCredentialPathCandidates,
    getCredentialsPath,
    getSkillCredentialsPath,
    hasSudoworkApiKey,
    isSudowork,
    isAuthFailedError,
    isSudoworkMissingKeyError,
    listSudoworkSecrets,
    emitError,
    parseScriptArgs,
    printShareOneScriptError,
    readLocalApiKey,
    requestBuffer,
    requestPublicShareOneJson,
    requestShareOneBuffer,
    requestShareOneJson,
    resetCredentialModeCache,
    resolveDirectApiKey,
    saveLocalApiKey,
    saveSudoworkApiKey,
};
