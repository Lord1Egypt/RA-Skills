#!/usr/bin/env node

const {
    emitError,
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    getBaseUrl,
    parseShareReference,
    printShareOneScriptError,
    requestShareOneBuffer,
    resolveDirectApiKey,
} = require('./shareone_client');

const {commandLine} = require('./cli_args');
const {values, positional: ref} = commandLine({
    summary: 'change an existing owner-managed share password, watermark, slug or feature settings, without replacing content. Share URLs identify the resource; --base-url or SHAREONE_BASE_URL selects another API deployment.',
    result: 'the committed server JSON/settings, or a request preview with --dry-run. Omitted settings remain unchanged; no source download is needed.',
    positional: 'share_link_or_id', options: {'--api-key': true, '--base-url': true, '--watermark': true,
        '--password': true, '--slug': true, '--allow-comments': true, '--allow-data': true,
        '--dry-run': {description: 'Print the intended request without credentials or network access.'}},
});
const apiKey = values['api-key'], dryRun = values['dry-run'];
const payload = {};
for (const [flag, field] of Object.entries({watermark: 'watermark', password: 'password', slug: 'custom_slug',
    'allow-comments': 'allow_comments', 'allow-data': 'allow_data'})) {
    if (values[flag] !== undefined) payload[field] = values[flag];
}

if (Object.keys(payload).length === 0) {
    emitError('ERROR:NO_SETTINGS_PROVIDED', ['Provide at least one of --watermark, --password, --slug, --allow-comments, or --allow-data.'].join('\n'));
}

function endpointForPrefix(prefix, shareRef) {
    const encodedRef = encodeURIComponent(shareRef);
    if (prefix === 's' || prefix === 'md') {
        return `/api/v1/pages/${encodedRef}`;
    }
    if (prefix === 'pdf' || prefix === 'ppt' || prefix === 'word') {
        return `/api/v1/files/${encodedRef}`;
    }
    return null;
}

function buildRequestBody() {
    const body = JSON.stringify(payload);
    return {
        body,
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body),
        },
    };
}

function shouldRetryAsFile(error) {
    const text = `${error && error.message ? error.message : ''}\n${error && error.responseText ? error.responseText : ''}`;
    return error && error.statusCode === 400 && /only for HTML\/Markdown|Use \/api\/v1\/files|HTML\/Markdown pages/i.test(text);
}

async function putSettings(apiPath) {
    const { body, headers } = buildRequestBody();
    return requestShareOneBuffer(apiPath, {
        method: 'PUT',
        apiKey,
        headers,
    }, body);
}

(async () => {
    const parsed = parseShareReference(ref);
    if (!parsed.shareRef) emitError('MISSING_SHARE_REF');
    const credentialMode = dryRun ? {mode: 'direct'} : await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey && !dryRun) {
        emitError('ERROR:SUDOWORK_MANAGED_KEY', ['Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。'].join('\n'));
    }

    if (!dryRun && credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(apiKey)) {
        emitError('ERROR:KEY_NOT_FOUND');
    }

    const explicitApiPath = endpointForPrefix(parsed.prefix, parsed.shareRef);
    const pageApiPath = `/api/v1/pages/${encodeURIComponent(parsed.shareRef)}`;
    const fileApiPath = `/api/v1/files/${encodeURIComponent(parsed.shareRef)}`;

    if (dryRun) {
        const result = {
            method: 'PUT',
            api_path: explicitApiPath || pageApiPath,
            payload,
            base_url: getBaseUrl(),
        };
        if (!explicitApiPath) {
            result.fallback_api_path = fileApiPath;
        }
        console.log(JSON.stringify(result, null, 2));
        return;
    }

    if (explicitApiPath) {
        const res = await putSettings(explicitApiPath);
        process.stdout.write(res.data);
        return;
    }

    try {
        const res = await putSettings(pageApiPath);
        process.stdout.write(res.data);
    } catch (error) {
        if (!shouldRetryAsFile(error)) {
            throw error;
        }
        const res = await putSettings(fileApiPath);
        process.stdout.write(res.data);
    }
})().catch((error) => {
    process.exit(printShareOneScriptError(error));
});
