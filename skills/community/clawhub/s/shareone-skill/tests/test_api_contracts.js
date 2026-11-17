const { test } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

async function fixture(t, handler, {anonymous = false} = {}) {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'shareone-contract-'));
    const requests = [];
    const server = http.createServer(async (req, res) => {
        let body = '';
        for await (const chunk of req) body += chunk;
        requests.push({method: req.method, path: req.url, headers: req.headers, body});
        await handler(requests.at(-1), res);
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    t.after(async () => {
        await new Promise(resolve => server.close(resolve));
        fs.rmSync(dir, {recursive: true, force: true});
    });
    const sourceScripts = path.join(__dirname, '../scripts');
    const scriptsDir = anonymous ? path.join(dir, 'scripts') : sourceScripts;
    if (anonymous) fs.cpSync(sourceScripts, scriptsDir, {recursive: true});
    const env = {...process.env, SHAREONE_API_KEY: anonymous ? '' : 'isolated-owner-key', SHAREONE_BASE_URL: `http://127.0.0.1:${server.address().port}`};
    for (const name of Object.keys(env)) if (name.startsWith('SUDOWORK_') || /^(http|https|all)_proxy$/i.test(name)) delete env[name];
    const run = (script, args = []) => new Promise(resolve => {
        const child = spawn(process.execPath, [path.join(scriptsDir, script + '.js'), ...args], {cwd: dir, env, windowsHide: true});
        let stdout = '', stderr = '';
        child.stdout.on('data', data => stdout += data);
        child.stderr.on('data', data => stderr += data);
        child.on('close', status => resolve({status, stdout, stderr}));
    });
    return {run, requests, dir};
}
function json(res, value, status = 200, headers = {}) {
    res.writeHead(status, {'Content-Type': 'application/json', ...headers});
    res.end(JSON.stringify(value));
}
function error(result) {
    assert.equal(result.stdout, '');
    const line = result.stderr.split('\n').find(line => line.startsWith('ERROR_JSON:'));
    assert.ok(line, result.stderr);
    return JSON.parse(line.slice('ERROR_JSON:'.length));
}

test('review wait reads one request to approval without publishing', async t => {
    let count = 0;
    const f = await fixture(t, (req, res) => {
        assert.equal(req.method, 'GET');
        assert.equal(req.path, '/api/v1/content-reviews/test-review');
        assert.equal(req.headers['x-api-key'], 'isolated-owner-key');
        const approved = ++count === 3;
        json(res, {id:'test-review', approved: approved ? true : null, status: approved ? 'approved' : 'automatic_pending', decision_source: approved ? 'automatic' : null});
    });
    const result = await f.run('wait_content_review', ['test-review', '--poll-seconds', '0.01']);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(result.stdout).approved, true);
    assert.equal(count, 3);
});

test('review wait stops on manual review and final denial', async t => {
    let response;
    const f = await fixture(t, (_, res) => json(res, response));
    for (const [approved, status, code] of [[null, 'manual_required', 'CONTENT_REVIEW_REQUIRED'], [false, 'rejected', 'CONTENT_REVIEW_DENIED']]) {
        response = {id:'test-review', approved, status, source_agent:'test-agent'};
        const before = f.requests.length;
        const result = await f.run('wait_content_review', ['test-review']);
        assert.equal(result.status, 6, result.stderr);
        assert.equal(error(result).error_code, code);
        assert.equal(error(result).detail.source_agent, 'test-agent');
        assert.equal(f.requests.length, before + 1);
    }
});

test('changed review candidate steers the owner to resubmit current facts without administrator approval', async t => {
    const f = await fixture(t, (_, res) => json(res, {id:'test-review', approved:null, status:'resubmission_required'}));
    const result = await f.run('wait_content_review', ['test-review']);
    assert.equal(result.status, 6);
    assert.match(error(result).hint, /current source bytes and access scope/);
    assert.doesNotMatch(error(result).hint, /Root|administrator/);
    assert.equal(f.requests.length, 1);
});

test('review wait timeout returns pending record, and invalid input makes no request', async t => {
    const f = await fixture(t, (_, res) => json(res, {id:'test-review', approved:null, status:'automatic_pending'}));
    const result = await f.run('wait_content_review', ['test-review', '--timeout-seconds', '0.3', '--poll-seconds', '0.01']);
    assert.equal(result.status, 3, result.stderr);
    assert.equal(JSON.parse(result.stdout).wait_timed_out, true);
    const before = f.requests.length;
    const invalid = await f.run('wait_content_review', ['test-review', '--timeout-seconds', 'NaN']);
    assert.equal(invalid.status, 2);
    assert.equal(f.requests.length, before);
});

test('review wait returns known pending state when its final GET consumes the remaining budget', async t => {
    let calls = 0;
    const f = await fixture(t, (_, res) => {
        if (++calls === 1) json(res, {id:'test-review', approved:null, status:'automatic_pending'});
        // The second read stays open until the client cancels it at its deadline.
    });
    const result = await f.run('wait_content_review', ['test-review', '--timeout-seconds', '1', '--poll-seconds', '0.01']);
    assert.equal(result.status, 3, result.stderr);
    assert.equal(JSON.parse(result.stdout).wait_timed_out, true);
    assert.equal(JSON.parse(result.stdout).approved, null);
    assert.equal(calls, 2);
});

test('API errors steer by domain code and preserve detail and Retry-After', async t => {
    let response;
    const f = await fixture(t, (_, res) => json(res, response.body, response.status, response.headers));
    for (const [status, code, exit, retryable] of [
        [401, 'PASSWORD_REQUIRED', 6, false], [401, 'EMAIL_GATE_REQUIRED', 6, false],
        [401, 'INVALID_API_KEY', 7, false], [403, 'AGENT_OWNER_REQUIRED', 6, false],
        [400, 'BAD_REQUEST', 2, false], [404, 'NOT_FOUND', 4, false], [422, 'VALIDATION_ERROR', 2, false],
        [409, 'IDEMPOTENCY_CONFLICT', 5, false], [409, 'CONSUMER_LEASE_BUSY', 5, true], [429, 'RATE_LIMIT_EXCEEDED', 8, true],
        [409, 'CONTENT_REVIEW_REQUIRED', 6, false], [403, 'CONTENT_REVIEW_DENIED', 6, false],
    ]) {
        const detail = status === 422 ? [{loc: ['body', 'state'], type: 'missing'}] : {code, message: 'Decision detail'};
        response = {status, body: {error_code: code, detail, retryable}, headers: {'Retry-After': '2'}};
        const result = await f.run('shareone_api_request', ['/api/v1/me']);
        const parsed = error(result);
        assert.equal(result.status, exit, result.stderr);
        assert.equal(parsed.error_code, code);
        assert.deepEqual(parsed.detail, detail);
        assert.equal(parsed.retryable, retryable);
        assert.equal(parsed.retry_after, '2');
        assert.doesNotMatch(parsed.hint, /create_guest/);
    }
});

test('API response output preserves exact bytes without shell redirection', async t => {
    const body = Buffer.concat([Buffer.from('<p>你好</p>\r\n'), Buffer.from([0, 255])]);
    const f = await fixture(t, (req, res) => {
        assert.equal(req.method, 'GET');
        assert.equal(req.headers['x-api-key'], 'isolated-owner-key');
        res.writeHead(200, {'Content-Type': 'application/octet-stream'});
        res.end(body);
    });
    const file = path.join(f.dir, 'review-content.html');
    const result = await f.run('shareone_api_request', ['/api/v1/content-reviews/review/content', '--output', file]);
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(fs.readFileSync(file), body);
    assert.deepEqual(JSON.parse(result.stdout), {saved_to:file, bytes:body.length});
});

test('ambiguous POST failures require supported replay protection', async t => {
    const f = await fixture(t, (_, res) => json(res, {detail: 'Unavailable', error_code: 'SERVER_ERROR', retryable: true}, 503));
    for (const [apiPath, key, expected] of [
        ['/api/v1/pages', null, false], ['/api/v1/pages', 'same-intent', true],
        ['/api/v1/agent-guest-key', 'unsupported', false],
    ]) {
        const result = await f.run('shareone_api_request', [apiPath, '--method', 'POST', '--data', '{}', ...(key ? ['--idempotency-key', key] : [])]);
        assert.equal(result.status, 9);
        assert.equal(error(result).retryable, expected);
    }
});

test('agent reply uses one POST and outputs observed parent state', async t => {
    const observed = {id: 'reply', author_role: 'agent', status: 'open', parent_status: 'open', parent_agent_stance: 'need-input'};
    const f = await fixture(t, (req, res) => {
        assert.equal(req.method, 'POST');
        assert.deepEqual(JSON.parse(req.body), {parent_id: 'root', content: 'Reviewed', author_role: 'agent', state: 'resolved-agree'});
        assert.equal(req.headers['idempotency-key'], 'event-123.reply');
        json(res, observed, 201);
    });
    const result = await f.run('comment_reply', ['http://example.test/s/review', 'root', '--content', 'Reviewed', '--state', 'resolved-agree', '--idempotency-key', 'event-123.reply']);
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(JSON.parse(result.stdout), observed);
    assert.equal(f.requests.length, 1);
    const missing = await f.run('comment_reply', ['review', 'root', '--content', 'Reviewed']);
    assert.equal(missing.status, 2);
    assert.equal(error(missing).error_code, 'STATE_REQUIRED');
    assert.equal(f.requests.length, 1);
});

test('comment triage retains screenshots, stance and deep replies', async t => {
    const comment = {id: 'root', highlighter_data: 'bulky', screenshot_url: '/comment-screenshots/review/root.png',
        viewer_can_reattach: true, anchor_binding: {revision: 2, quote: 'Current target', highlighter_data: '{"anchor_type":"app_declared"}', actor_id: 'author', reason: 'Explicit selection'},
        agent_stance: 'need-input', updated_at: '2026-10-08T00:00:00Z', viewer_can_manage: true,
        replies: [{id: 'reply', highlighter_data: '{}', parent_status: 'open', agent_stance: 'disagree', replies: [{id: 'nested', replies: []}]}]};
    const f = await fixture(t, (req, res) => {assert.equal(req.headers['x-api-key'], 'isolated-owner-key'); json(res, [comment]);});
    const result = await f.run('comment_list', ['review', '--json', 'compact']);
    assert.equal(result.status, 0, result.stderr);
    const actual = JSON.parse(result.stdout).comments[0];
    assert.equal(actual.screenshot_url, comment.screenshot_url);
    assert.equal(actual.agent_stance, comment.agent_stance);
    assert.equal(actual.updated_at, comment.updated_at);
    assert.deepEqual(actual.anchor_binding, comment.anchor_binding);
    assert.equal(actual.viewer_can_reattach, true);
    assert.equal(actual.replies[0].replies[0].id, 'nested');
    assert.ok(!('highlighter_data' in actual));
    const invalid = await f.run('comment_list', ['review', '--status', 'unresovled']);
    assert.equal(invalid.status, 2);
    assert.equal(error(invalid).error_code, 'BAD_STATUS');
});

test('local and remote publication default comments off and honor explicit settings', async t => {
    const f = await fixture(t, (_, res) => json(res, {share_id: 'review', share_url: 'http://example.test/s/review'}, 201));
    for (const channel of ['local', 'remote']) {
        for (const value of [undefined, true, false]) {
            const file = path.join(f.dir, `${channel}-${value}.html`);
            fs.writeFileSync(file, '<p>Review</p>');
            const args = channel === 'local' ? [file] : ['--remote-url', 'https://example.test/review.html'];
            if (value !== undefined) args.push('--allow-comments', String(value));
            const result = await f.run(channel === 'local' ? 'publish' : 'upload_page', args);
            assert.equal(result.status, 0, result.stderr);
            const request = f.requests.at(-1);
            assert.equal(request.method, 'POST');
            assert.equal(JSON.parse(request.body).allow_comments, value ?? false);
        }
    }
});

test('local and remote updates omit unspecified comment settings', async t => {
    const content = '<p>Updated review</p>';
    const f = await fixture(t, (request, res) => {
        if (request.method === 'GET') {
            assert.equal(request.path, '/api/v1/shares/review/download');
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.end(content);
        } else {
            json(res, {share_id: 'review', share_url: 'http://example.test/s/review'});
        }
    });
    const file = path.join(f.dir, 'review.html');
    fs.writeFileSync(file, content);
    for (const channel of ['local', 'remote']) {
        for (const value of [undefined, true, false]) {
            const args = channel === 'local' ? [file] : ['--remote-url', 'https://example.test/review.html'];
            args.push('--share-id', 'review');
            if (value !== undefined) args.push('--allow-comments', String(value));
            const result = await f.run(channel === 'local' ? 'publish' : 'upload_page', args);
            assert.equal(result.status, 0, result.stderr);
            const request = f.requests.filter(r => r.method === 'PUT').at(-1);
            const body = JSON.parse(request.body);
            assert.equal(body.allow_comments, value);
            assert.equal(Object.hasOwn(body, 'allow_comments'), value !== undefined);
        }
    }
});

test('anonymous comment reads preserve COMMENTS_DISABLED without credential advice', async t => {
    const response = {error_code: 'COMMENTS_DISABLED', detail: 'Comments are disabled for this page',
        hint: 'The owner must enable comments before this action is available.', retryable: false};
    const f = await fixture(t, (request, res) => {
        assert.equal(request.headers['x-api-key'], undefined);
        json(res, response, 403);
    }, {anonymous: true});
    const result = await f.run('comment_list', ['review']);
    assert.equal(result.status, 6, result.stderr);
    const actual = error(result);
    assert.equal(actual.error_code, 'COMMENTS_DISABLED');
    assert.equal(actual.category, 'permission');
    assert.equal(actual.retryable, false);
    assert.equal(actual.detail, response.detail);
    assert.equal(actual.hint, response.hint);
    assert.doesNotMatch(result.stderr, /AUTH_FAILED|INVALID_API_KEY|create_guest/);
});

test('keyed binary publication stays one replayable creation operation', async t => {
    const f = await fixture(t, (req, res) => {
        assert.equal(req.path, '/api/v1/files');
        assert.equal(req.headers['idempotency-key'], 'binary-intent');
        json(res, {share_id: 'pdf', share_url: 'http://example.test/pdf/pdf'}, 201);
    });
    const file = path.join(f.dir, 'review.pdf');
    fs.writeFileSync(file, '%PDF-isolated');
    const result = await f.run('publish', [file, '--idempotency-key', 'binary-intent']);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(result.stdout).share_id, 'pdf');
    assert.equal(f.requests.length, 1);
});

test('keyed text publication can replay after a recorded success', async t => {
    const f = await fixture(t, (req, res) => {
        assert.equal(req.headers['idempotency-key'], 'text-intent');
        assert.equal(req.method, 'POST');
        json(res, {share_id: 'review', share_url: 'http://example.test/s/review'}, 201);
    });
    const file = path.join(f.dir, 'review.html');
    fs.writeFileSync(file, '<p>Review</p>');
    for (let n = 0; n < 2; n++) {
        const result = await f.run('publish', [file, '--idempotency-key', 'text-intent']);
        assert.equal(result.status, 0, result.stderr);
        assert.equal(JSON.parse(result.stdout).share_id, 'review');
    }
    const newIntent = await f.run('publish', [file, '--idempotency-key', 'new-text-intent']);
    assert.equal(newIntent.status, 5);
    assert.equal(error(newIntent).error_code, 'FILE_PREVIOUSLY_PUBLISHED');
    assert.equal(f.requests.length, 2);
});
