const assert = require('node:assert/strict');
const http = require('node:http');
const {spawn} = require('node:child_process');
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
        assert.equal(path.dirname(path.resolve(dir)), path.resolve(os.tmpdir()));
        assert.ok(path.basename(dir).startsWith('shareone-contract-'));
        fs.rmSync(dir, {recursive: true, force: true});
    });
    const sourceScripts = path.join(__dirname, '../scripts');
    const scriptsDir = anonymous ? path.join(dir, 'scripts') : sourceScripts;
    if (anonymous) fs.cpSync(sourceScripts, scriptsDir, {recursive: true});
    const base = `http://127.0.0.1:${server.address().port}`;
    const env = {...process.env, SHAREONE_API_KEY: anonymous ? '' : 'isolated-owner-key', SHAREONE_BASE_URL: base};
    for (const name of Object.keys(env)) if (name.startsWith('SUDOWORK_') || /^(http|https|all)_proxy$/i.test(name)) delete env[name];
    const run = (script, args = [], overrides = {}) => new Promise(resolve => {
        const child = spawn(process.execPath, [path.join(scriptsDir, script + '.js'), ...args], {cwd: dir, env: {...env, ...overrides}, windowsHide: true});
        let stdout = '', stderr = '';
        child.stdout.on('data', data => stdout += data);
        child.stderr.on('data', data => stderr += data);
        child.on('close', status => resolve({status, stdout, stderr}));
    });
    return {run, requests, dir, base};
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

module.exports = {fixture, json, error};
