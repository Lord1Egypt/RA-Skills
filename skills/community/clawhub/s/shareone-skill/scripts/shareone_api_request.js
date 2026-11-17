#!/usr/bin/env node

const { emitError } = require('./shareone_client');
const fs = require('fs');
const {
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    printShareOneScriptError,
    requestShareOneBuffer,
    resolveDirectApiKey,
} = require('./shareone_client');

const args = process.argv.slice(2);
let method = 'GET';
let apiPath = null;
let data = null;
let dataFile = null;
let apiKey = null;
let publicRequest = false;
let idempotencyKey = null;
let outputPath = null;

function usage() {
    console.error("Usage: node shareone_api_request.js <api_path> [--method GET|POST|PUT|DELETE] [--data '<json>' | --data-file <path|-> ] [--api-key <key>] [--public] [--idempotency-key <key>] [--output <path>]");
    console.error("  --data-file <path>  read the request body from a file ('-' for stdin); preferred for non-ASCII or nested-JSON bodies to avoid shell quoting issues.");
}

function nextValue(index, flag) {
    const value = args[index + 1];
    if (value === undefined || value.startsWith('--')) {
        emitError(`ERROR:MISSING_VALUE:${flag}`);
    }
    return value;
}

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--method') {
        method = String(nextValue(i, args[i])).toUpperCase();
        i += 1;
    } else if (args[i] === '--data') {
        data = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--data-file') {
        dataFile = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--api-key') {
        apiKey = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--idempotency-key') {
        idempotencyKey = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--public') {
        publicRequest = true;
    } else if (args[i] === '--output') {
        outputPath = nextValue(i, args[i]);
        i += 1;
    } else if (!args[i].startsWith('--') && !apiPath) {
        apiPath = args[i];
    } else {
        emitError(`ERROR:UNKNOWN_ARGUMENT:${args[i]}`);
    }
}

if (!apiPath) {
    usage();
    emitError('BAD_ARGS', 'Required arguments are missing.');
}

// Prefer --data-file for bodies that are awkward to pass inline (CJK text,
// nested/escaped JSON): file/stdin bytes reach the request verbatim, free of
// shell quoting.
if (dataFile !== null) {
    if (data !== null) {
        emitError("ERROR:BAD_ARGS", ["Pass either --data or --data-file, not both."].join('\n'));
    }
    try {
        data = fs.readFileSync(dataFile === '-' ? 0 : dataFile, 'utf8');
    } catch (error) {
        emitError(`ERROR:DATA_FILE_UNREADABLE: ${error.message}`);
    }
}

const headers = {};
if (idempotencyKey) headers['Idempotency-Key'] = idempotencyKey;
let body = null;
if (data !== null) {
    body = data;
    headers['Content-Type'] = 'application/json';
    headers['Content-Length'] = Buffer.byteLength(body);
}

(async () => {
    const credentialMode = await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey && !publicRequest) {
        emitError("ERROR:SUDOWORK_MANAGED_KEY", ["Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。"].join('\n'));
    }

    if (!publicRequest && credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(apiKey)) {
        emitError("ERROR:KEY_NOT_FOUND");
    }

    return requestShareOneBuffer(apiPath, {
        method,
        apiKey,
        authRequired: !publicRequest,
        headers,
    }, body);
})().then((res) => {
    if (outputPath !== null) {
        fs.writeFileSync(outputPath, res.data);
        process.stdout.write(JSON.stringify({ saved_to: outputPath, bytes: res.data.length }) + '\n');
    } else {
        process.stdout.write(res.data);
    }
}).catch((error) => {
    process.exit(printShareOneScriptError(error));
});
