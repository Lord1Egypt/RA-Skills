#!/usr/bin/env node
const { AGENT_REPLY_STATES, CREDENTIAL_MODE_SUDOWORK_PROXY, detectCredentialMode, extractShareRef,
    emitError, parseScriptArgs, printShareOneScriptError, requestShareOneJson, resolveDirectApiKey } = require('./shareone_client');

const usage = 'node comment_reply.js <share_link_or_ref> <root_comment_id> --content <text> --state <' +
    Object.keys(AGENT_REPLY_STATES).join('|') + '> [--api-key <key>] [--base-url <url>] [--idempotency-key <key>]';
const { values, positionals: [ref, parentId] } = parseScriptArgs(
    ['--content', '--state', '--api-key', '--base-url', '--idempotency-key'], 2, usage);
if (!values.content) emitError('CONTENT_REQUIRED', 'Provide reply content.', {hint: usage});
if (!values.state) emitError('STATE_REQUIRED', 'Declare the reply state.', {hint: usage});
if (!Object.hasOwn(AGENT_REPLY_STATES, values.state)) emitError('INVALID_STATE', values.state, {hint: usage});

(async () => {
    const mode = await detectCredentialMode();
    if (mode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && values['api-key']) emitError('SUDOWORK_MANAGED_KEY');
    if (mode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(values['api-key'])) emitError('KEY_NOT_FOUND');
    const result = await requestShareOneJson(`/api/v1/shares/${encodeURIComponent(extractShareRef(ref))}/comments`, {
        method: 'POST', apiKey: values['api-key'],
        headers: values['idempotency-key'] ? {'Idempotency-Key': values['idempotency-key']} : {},
    }, { parent_id: parentId, content: values.content, author_role: 'agent', state: values.state });
    process.stdout.write(JSON.stringify(result) + '\n');
})().catch(error => process.exit(printShareOneScriptError(error)));
