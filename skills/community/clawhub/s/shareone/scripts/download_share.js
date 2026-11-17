#!/usr/bin/env node

const { emitError } = require('./shareone_client');
const fs = require('fs');
const path = require('path');
const {
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    extractShareRef,
    printShareOneScriptError,
    requestShareOneBuffer,
    resolveDirectApiKey,
} = require('./shareone_client');

const ACTIVE_TASK_FILENAME = '.shareone_active_task';

const args = process.argv.slice(2);
let ref = null;
let password = null;
let apiKey = null;
let publicOnly = false;
let save = false;
let taskAnchor = false;

function usage() {
    console.error("Usage: node download_share.js <ref> [--password <password>] [--api-key <key>] [--public-only] [--save] [--task-anchor]");
}

function nextValue(index, flag) {
    const value = args[index + 1];
    if (value === undefined || value.startsWith('--')) {
        emitError(`ERROR:MISSING_VALUE:${flag}`);
    }
    return value;
}

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--ref') {
        ref = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--password') {
        password = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--api-key') {
        apiKey = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--public-only') {
        publicOnly = true;
    } else if (args[i] === '--save') {
        save = true;
    } else if (args[i] === '--task-anchor') {
        taskAnchor = true;
        save = true;
    } else if (!args[i].startsWith('--') && !ref) {
        ref = args[i];
    } else {
        emitError(`ERROR:UNKNOWN_ARGUMENT:${args[i]}`);
    }
}

if (!ref) {
    usage();
    emitError('BAD_ARGS', 'Required arguments are missing.');
}

async function tryOwnerDownload(credentialMode) {
    if (publicOnly) return null;
    const hasKey = credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY
        ? credentialMode.hasSudoworkKey
        : Boolean(resolveDirectApiKey(apiKey));
    if (!hasKey) return null;
    const shareRef = extractShareRef(ref);
    if (!shareRef) return null;
    try {
        return await requestShareOneBuffer(`/api/v1/shares/${encodeURIComponent(shareRef)}/download`, {
            method: 'GET',
            apiKey,
            authRequired: true,
        });
    } catch (error) {
        if ([401, 403, 404].includes(error.statusCode)) return null;
        throw error;
    }
}

async function publicDownload() {
    if (password !== null) {
        const body = JSON.stringify({ ref, password });
        return requestShareOneBuffer('/api/v1/public-download', {
            method: 'POST',
            authRequired: false,
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(body),
            },
        }, body);
    }
    return requestShareOneBuffer(`/api/v1/public-download?ref=${encodeURIComponent(ref)}`, {
        method: 'GET',
        authRequired: false,
    });
}

function parseFilenameFromDisposition(disposition) {
    if (!disposition) return null;
    const utf8Match = /filename\*=utf-8''([^;]+)/i.exec(disposition);
    if (utf8Match) {
        try {
            return decodeURIComponent(utf8Match[1].trim());
        } catch (_) {
            // Fall through to the plain filename form.
        }
    }
    const plainMatch = /filename="?([^";]+)"?/i.exec(disposition);
    return plainMatch ? plainMatch[1].trim() : null;
}

function emitDownloadInfo(headers) {
    const filename = parseFilenameFromDisposition(headers['content-disposition']);
    if (filename) console.error(`INFO:FILENAME:${filename}`);
    // Downloads of HTML are served as octet-stream so no HTML-rewriting proxy
    // edits the bytes in transit; the real type travels in its own header.
    const contentType = headers['x-shareone-content-type'] || headers['content-type'];
    if (contentType) console.error(`INFO:CONTENT_TYPE:${contentType}`);
    const remoteSource = headers['x-remote-source-url'];
    if (remoteSource) {
        console.error(`INFO:REMOTE_SOURCE:${remoteSource}`);
        console.error('HINT:EDIT_AT_SOURCE');
    }
}

function sanitizeFilename(name) {
    const base = path.basename(String(name || '').trim());
    const cleaned = base.replace(/[\\/:*?"<>|]/g, '_');
    return cleaned && cleaned !== '.' && cleaned !== '..' ? cleaned : null;
}

function uniqueFilename(name) {
    if (!fs.existsSync(name)) return name;
    const ext = path.extname(name);
    const stem = ext ? name.slice(0, -ext.length) : name;
    for (let i = 1; i < 1000; i++) {
        const candidate = `${stem}-${i}${ext}`;
        if (!fs.existsSync(candidate)) return candidate;
    }
    throw new Error(`Could not choose a non-conflicting filename for ${name}`);
}

function saveDownload(result) {
    const serverName = sanitizeFilename(parseFilenameFromDisposition((result.headers || {})['content-disposition']));
    const shareRef = sanitizeFilename(extractShareRef(ref)) || 'share';

    if (taskAnchor) {
        fs.writeFileSync(ACTIVE_TASK_FILENAME, `${extractShareRef(ref)}\n`);
        console.error(`ANCHOR_WRITTEN:${ACTIVE_TASK_FILENAME}`);
    }

    const preferredName = taskAnchor
        ? `shareone_${shareRef}_source${serverName ? path.extname(serverName) || '.html' : '.html'}`
        : (serverName || `shareone_${shareRef}_download`);
    const outputName = uniqueFilename(preferredName);

    fs.writeFileSync(outputName, result.data);
    console.log(`SAVED:${outputName}`);
}

(async () => {
    const credentialMode = await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey && !publicOnly) {
        emitError("ERROR:SUDOWORK_MANAGED_KEY", ["Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。"].join('\n'));
    }

    const ownerResult = await tryOwnerDownload(credentialMode);
    const result = ownerResult || await publicDownload();
    emitDownloadInfo(result.headers || {});
    if (save) {
        saveDownload(result);
    } else {
        process.stdout.write(result.data);
    }
})().catch((error) => {
    process.exit(printShareOneScriptError(error));
});
