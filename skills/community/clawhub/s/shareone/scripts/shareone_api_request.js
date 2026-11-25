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

const {commandLine} = require('./cli_args');
const {values, positional: apiPath} = commandLine({
    summary: 'invoke a documented HTTP operation directly. Paths are relative to the configured API deployment; --public omits account credentials.',
    result: 'exact response bytes on stdout, or {saved_to,bytes} with --output. HTTP 200 may contain a failed remote refresh: inspect its domain state. Writes may commit before a lost response; replay only safe operations with the same supported intent key.',
    positional: 'api_path', options: {
        '--method': {value: 'method', normalize: value => value.toUpperCase(), choices: ['GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS'], description: 'HTTP method; defaults to GET.'},
        '--data': {value: 'json', description: 'JSON request body; use instead of --data-file.'},
        '--data-file': {value: 'path|-', description: 'Read exact UTF-8 JSON from a file or stdin; preferred for nested or non-ASCII bodies.'},
        '--api-key': true, '--public': {description: 'Omit account authentication; share viewer gates still apply.'},
        '--idempotency-key': true, '--output': {value: 'path', description: 'Save exact response bytes to this file.'}},
});
const method = values.method || 'GET', dataFile = values['data-file'] ?? null;
let data = values.data ?? null;
const apiKey = values['api-key'], publicRequest = values.public;
const idempotencyKey = values['idempotency-key'], outputPath = values.output ?? null;

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
