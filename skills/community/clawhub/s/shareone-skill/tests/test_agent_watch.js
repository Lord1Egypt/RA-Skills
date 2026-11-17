const assert = require('node:assert/strict');
const { test } = require('node:test');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const http = require('node:http');
const { execFile } = require('node:child_process');
const { promisify } = require('node:util');
const { parseArgs, runHandler } = require('../scripts/agent_watch');
const exec = promisify(execFile);
const script = path.resolve(__dirname, '../scripts/agent_watch.js');

test('handler failure preserves the cursor and a fresh process replays before acknowledging', async () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'shareone-watch-'));
    const handler = path.join(dir, 'receiver.js');
    fs.writeFileSync(handler, `const fs=require('node:fs');let input='';process.stdin.on('data',x=>input+=x);process.stdin.on('end',()=>{const batch=JSON.parse(input);fs.appendFileSync('received.jsonl',JSON.stringify(batch)+'\\n');if(!fs.existsSync('attempted')){fs.writeFileSync('attempted','1');process.exitCode=7;}});`);
    const event = { id: 'stable-event-id', actor_role: 'visitor', share_id: 'page', comment_id: 'comment', sequence: 1 };
    let cursor = 0, leased = false, polls = 0, releases = 0;
    const server = http.createServer(async (req, res) => {
        let raw = ''; for await (const chunk of req) raw += chunk;
        const body = JSON.parse(raw);
        assert.equal(req.headers['x-api-key'], 'test-key');
        let answer;
        if (req.method === 'PUT') answer = { name: 'tester', cursor };
        else if (req.url.endsWith('/poll')) {
            assert.equal(leased, false); polls++;
            leased = cursor === 0;
            answer = leased ? { events: [event], lease_token: 'hidden-lease', lease_seconds: 300, through: 1 } : { events: [], lease_token: null };
        } else if (req.url.endsWith('/release')) {
            assert.equal(body.lease_token, 'hidden-lease'); releases++; leased = false; answer = { released: true };
        } else if (req.url.endsWith('/ack')) {
            assert.equal(body.lease_token, 'hidden-lease'); cursor = 1; leased = false; answer = { cursor };
        } else { res.writeHead(404); res.end('{}'); return; }
        res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(answer));
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    try {
        const args = [script, '--consumer', 'tester', '--once', '--cwd', dir, '--command-json', JSON.stringify([process.execPath, handler])];
        const env = { ...process.env, SHAREONE_BASE_URL: `http://127.0.0.1:${server.address().port}`, SHAREONE_API_KEY: 'test-key', SUDOWORK_AUTH_PROXY_URL: '', SUDOWORK_AUTH_PROXY_TOKEN: '' };
        await assert.rejects(exec(process.execPath, args, { env, timeout: 15000 }), error => error.code === 1);
        assert.equal(cursor, 0); assert.equal(releases, 1);
        const { stdout } = await exec(process.execPath, args, { env, timeout: 15000 });
        assert.equal(cursor, 1);
        assert.match(stdout, /"acknowledged_through":1/);
        const received = fs.readFileSync(path.join(dir, 'received.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
        assert.equal(received.length, 2);
        assert.deepEqual(received[0], received[1]);
        assert.deepEqual(received[1].events, [event]);
        assert.ok(!JSON.stringify(received).includes('hidden-lease'));
        await exec(process.execPath, args, { env, timeout: 15000 });
        assert.equal(polls, 3);
        assert.equal(fs.readFileSync(path.join(dir, 'received.jsonl'), 'utf8').trim().split('\n').length, 2);
    } finally {
        await new Promise(resolve => server.close(resolve));
        fs.rmSync(dir, { recursive: true, force: true });
    }
});

test('long handler renews its lease; failed renewal stops it without acknowledging', async () => {
    const opts = { command: [process.execPath, '-e', 'process.stdin.resume();setTimeout(()=>{},30000)'], cwd: process.cwd(), timeoutSeconds: 10 };
    let renewals = 0;
    await assert.rejects(runHandler(opts, { lease_seconds: 3, events: [] }, async () => { renewals++; throw new Error('offline'); }), /Lease renewal failed/);
    assert.equal(renewals, 1);
});

test('timed out handlers fail delivery; scode routing requires an explicit session', async () => {
    const opts = { command: [process.execPath, '-e', 'process.stdin.resume();setTimeout(()=>{},30000)'], cwd: process.cwd(), timeoutSeconds: 1 };
    await assert.rejects(runHandler(opts, { lease_seconds: 300, events: [] }, async () => {}), /timed out/);
    const parsed = parseArgs(['--consumer', 'review', '--cwd', '/workspace', '--scode-session', 'review.jsonl']);
    assert.deepEqual(parsed.command, [process.execPath, path.resolve(__dirname, '../scripts/scode_receive.js'), path.resolve('/workspace', 'review.jsonl')]);
    assert.ok(!parsed.command.some(x => x.includes('skip-permissions')));
    const configured = parseArgs(['--consumer', 'review', '--scode-session', 'review.jsonl', '--scode-args-json', '["--auth","api-key"]']);
    assert.deepEqual(configured.command.slice(-2), ['--auth', 'api-key']);
    assert.throws(() => parseArgs(['--consumer', 'review']), /Choose/);
    assert.throws(() => parseArgs(['--consumer', '../review']), /consumer/);
});
