#!/usr/bin/env node
const { extractShareRef, emitError, parseScriptArgs, printShareOneScriptError, requestShareOneJson } = require('./shareone_client');
const { comment_filters: filters } = require('./api_contract.json');
const usage = 'node comment_list.js <share_link_or_ref> [--status ' + filters.join('|') +
    '] [--json compact|pretty] [--api-key <key>] [--base-url <url>]';
const { values, positionals: [ref] } = parseScriptArgs(['--status', '--json', '--api-key', '--base-url'], 1, usage);
const status = values.status || 'all';
const jsonMode = values.json || 'pretty';
if (!filters.includes(status)) emitError('BAD_STATUS', status, {hint: usage});
if (!['compact', 'pretty'].includes(jsonMode)) emitError('BAD_JSON_MODE', jsonMode, {hint: usage});

// Triage omits only bulky selection coordinates; reply trees retain decision facts.
function project(comment) {
    const { highlighter_data, replies, ...facts } = comment;
    const children = (replies || []).map(project);
    return { ...facts, reply_count: children.length, replies: children };
}
(async () => {
    const rows = await requestShareOneJson(`/api/v1/shares/${encodeURIComponent(extractShareRef(ref))}/comments?status=${status}`,
        {method: 'GET', apiKey: values['api-key']});
    if (!Array.isArray(rows)) emitError('INVALID_RESPONSE', 'Expected a comment array.');
    const result = {share: extractShareRef(ref), status, count: rows.length, comments: rows.map(project)};
    process.stdout.write(JSON.stringify(result, null, jsonMode === 'pretty' ? 2 : undefined) + '\n');
})().catch(error => process.exit(printShareOneScriptError(error)));
