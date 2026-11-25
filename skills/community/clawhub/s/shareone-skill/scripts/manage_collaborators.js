#!/usr/bin/env node

const {
    emitError,
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    parseShareReference,
    printShareOneScriptError,
    requestShareOneBuffer,
    requestShareOneJson,
    resolveDirectApiKey,
} = require('./shareone_client');

const {commandLine} = require('./cli_args');
const {values, positional: ref} = commandLine({
    summary: 'list or change collaborators as the share owner. Identify collaborators by ShareOne username. Another deployment requires explicit --base-url or SHAREONE_BASE_URL configuration.',
    result: 'the observed collaborators list or per-username add/remove results. Check each result; not_found is not a successful grant.',
    positional: 'share_link_or_id', options: {
        '--action': {value: 'action', choices: ['add','remove','list'], description: 'Required collaboration operation.'},
        '--usernames': {value: 'name1,name2', description: 'ShareOne usernames, required for add/remove; not API keys.'},
        '--api-key': true, '--base-url': true},
});
const apiKey = values['api-key'], action = values.action;
const usernames = (values.usernames || '').split(',').map(name => name.trim()).filter(Boolean);

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

(async () => {
    const {shareRef} = parseShareReference(ref);
    if (!shareRef) emitError('MISSING_SHARE_REF');
    const credentialMode = await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey) {
        emitError('ERROR:SUDOWORK_MANAGED_KEY', ['Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。'].join('\n'));
    }

    if (credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(apiKey)) {
        emitError('ERROR:KEY_NOT_FOUND');
    }

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
