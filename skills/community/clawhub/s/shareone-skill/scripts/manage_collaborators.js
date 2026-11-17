#!/usr/bin/env node

const {
    emitError,
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    getBaseUrl,
    printShareOneScriptError,
    requestShareOneBuffer,
    requestShareOneJson,
    resolveDirectApiKey,
} = require('./shareone_client');

const args = process.argv.slice(2);
let ref = null;
let apiKey = null;
let action = null;
let usernames = [];
let explicitBaseUrl = null;

function usage() {
    console.error('Usage: node manage_collaborators.js <share_link_or_id> --action <add|remove|list> [--usernames <name1,name2>] [--api-key <owner_key>] [--base-url <url>]');
    console.error('  协作者按 ShareOne 用户名标识（不是 API Key）。');
}

function nextValue(index, flag) {
    const value = args[index + 1];
    if (value === undefined) {
        emitError(`ERROR:MISSING_VALUE:${flag}`);
    }
    return value;
}

for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--api-key') {
        apiKey = nextValue(i, arg);
        i += 1;
    } else if (arg === '--base-url') {
        explicitBaseUrl = nextValue(i, arg);
        process.env.SHAREONE_BASE_URL = explicitBaseUrl;
        i += 1;
    } else if (arg === '--action') {
        action = nextValue(i, arg);
        i += 1;
    } else if (arg === '--usernames') {
        usernames = nextValue(i, arg).split(',').map(k => k.trim()).filter(Boolean);
        i += 1;
    } else if (!arg.startsWith('--') && !ref) {
        ref = arg;
    } else {
        emitError(`ERROR:UNKNOWN_ARGUMENT:${arg}`);
    }
}

if (!ref) {
    emitError('ERROR:MISSING_SHARE_REF');
}

if (!action) {
    emitError('ERROR:MISSING_ACTION', ['Provide --action add, --action remove, or --action list.'].join('\n'));
}

const validActions = new Set(['add', 'remove', 'list']);
if (!validActions.has(action)) {
    emitError(`ERROR:INVALID_ACTION:${action}`, ['--action must be one of: add, remove, list.'].join('\n'));
}

if ((action === 'add' || action === 'remove') && usernames.length === 0) {
    emitError(`ERROR:MISSING_USERNAMES`, [`--usernames is required for --action ${action}.`].join('\n'));
}

function parseRef(input) {
    const raw = String(input || '').trim();
    let path = raw.split('?')[0].split('#')[0];

    try {
        if (raw.includes('://')) {
            const parsed = new URL(raw);
            if (!explicitBaseUrl) {
                process.env.SHAREONE_BASE_URL = `${parsed.protocol}//${parsed.host}`;
            }
            path = parsed.pathname;
        }
    } catch (_) {
        path = raw.split('?')[0].split('#')[0];
    }

    const parts = path.split('/').filter(Boolean);
    const knownPrefixes = new Set(['s', 'md', 'pdf', 'ppt', 'word']);

    if (parts.length >= 2 && knownPrefixes.has(parts[0])) {
        return parts[1];
    }

    return parts[parts.length - 1] || raw;
}

(async () => {
    const credentialMode = await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey) {
        emitError('ERROR:SUDOWORK_MANAGED_KEY', ['Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。'].join('\n'));
    }

    if (credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(apiKey)) {
        emitError('ERROR:KEY_NOT_FOUND');
    }

    const shareRef = parseRef(ref);
    const apiPath = `/api/v1/shares/${encodeURIComponent(shareRef)}/collaborators`;

    if (action === 'list') {
        const res = await requestShareOneBuffer(apiPath, {
            method: 'GET',
            apiKey,
        });
        process.stdout.write(res.data);
        return;
    }

    const payload = action === 'add'
        ? { add_collaborators: usernames }
        : { remove_collaborators: usernames };

    const result = await requestShareOneJson(apiPath, {
        method: 'POST',
        apiKey,
    }, payload);

    console.log(JSON.stringify(result, null, 2));
})().catch((error) => {
    process.exit(printShareOneScriptError(error));
});
