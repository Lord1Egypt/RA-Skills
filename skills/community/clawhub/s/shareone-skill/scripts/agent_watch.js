#!/usr/bin/env node
// Durable ShareOne delivery. A handler receives JSON on stdin and returns zero
// only after completing the work (or durably accepting it into its own inbox).
const { spawn } = require('node:child_process');
const { setTimeout: delay } = require('node:timers/promises');
const path = require('node:path');
const { requestShareOneJson, extractShareRef, printShareOneScriptError } = require('./shareone_client');

function parseArgs(argv) {
    const opts = { start: 'beginning', once: false, allActors: false, timeoutSeconds: 1800, cwd: process.cwd() };
    for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--once') opts.once = true;
        else if (arg === '--all-actors') opts.allActors = true;
        else if (arg === '--help') opts.help = true;
        else if (['--consumer', '--share', '--start', '--command-json', '--scode-session', '--scode-args-json', '--cwd', '--timeout-seconds'].includes(arg)) {
            const value = argv[++i];
            if (!value || value.startsWith('--')) throw new Error(`Missing value for ${arg}`);
            opts[arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = value;
        } else throw new Error(`Unknown option: ${arg}`);
    }
    if (opts.help) return opts;
    if (!/^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,79}$/.test(opts.consumer || '')) throw new Error('--consumer is required (letters, numbers, _, ., -; up to 80 characters)');
    if (!['beginning', 'now'].includes(opts.start)) throw new Error('--start must be beginning or now');
    if (Boolean(opts.commandJson) === Boolean(opts.scodeSession)) throw new Error('Choose --command-json or --scode-session');
    opts.timeoutSeconds = Number(opts.timeoutSeconds);
    if (!Number.isInteger(opts.timeoutSeconds) || opts.timeoutSeconds < 1 || opts.timeoutSeconds > 86400) throw new Error('--timeout-seconds must be 1..86400');
    opts.cwd = path.resolve(opts.cwd);
    if (opts.scodeSession) {
        // Explicit session avoids accidentally resuming another project's chat.
        let extra = [];
        try { extra = JSON.parse(opts.scodeArgsJson || '[]'); } catch { throw new Error('--scode-args-json must be a string array'); }
        if (!Array.isArray(extra) || extra.some(v => typeof v !== 'string')) throw new Error('--scode-args-json must be a string array');
        opts.command = [process.execPath, path.join(__dirname, 'scode_receive.js'), path.resolve(opts.cwd, opts.scodeSession), ...extra];
    } else {
        try { opts.command = JSON.parse(opts.commandJson); } catch { throw new Error('--command-json must be a JSON array of executable and arguments'); }
        if (!Array.isArray(opts.command) || !opts.command.length || opts.command.some(v => typeof v !== 'string') || !opts.command[0]) throw new Error('--command-json must be a nonempty string array');
        if (opts.scodeArgsJson) throw new Error('--scode-args-json requires --scode-session');
    }
    return opts;
}

function terminate(child) {
    if (child.exitCode !== null || child.signalCode !== null) return;
    // Only terminate the handler tree this watcher started.
    if (process.platform === 'win32') {
        const killer = spawn('taskkill', ['/PID', String(child.pid), '/T', '/F'], { windowsHide: true, stdio: 'ignore' });
        killer.on('error', () => child.kill());
    } else {
        try { process.kill(-child.pid, 'SIGKILL'); } catch { child.kill('SIGKILL'); }
    }
}

async function runHandler(opts, batch, renew, signal) {
    const child = spawn(opts.command[0], opts.command.slice(1), {
        cwd: opts.cwd, shell: false, windowsHide: true, detached: process.platform !== 'win32',
        stdio: ['pipe', 'inherit', 'inherit'],
    });
    let failure;
    let renewing = false;
    const fail = error => { failure ||= error; terminate(child); };
    const abort = () => fail(new Error('Watcher stopping; batch remains unacknowledged'));
    signal?.addEventListener('abort', abort, { once: true });
    const timeout = setTimeout(() => fail(new Error('Handler timed out; batch remains unacknowledged')), opts.timeoutSeconds * 1000);
    const heartbeat = setInterval(async () => {
        if (renewing || failure) return;
        renewing = true;
        try { await renew(); } catch { fail(new Error('Lease renewal failed; stopping handler for redelivery')); }
        finally { renewing = false; }
    }, Math.max(1000, batch.lease_seconds * 1000 / 3));
    try {
        await new Promise((resolve, reject) => {
            child.once('error', reject);
            child.once('close', (code, sig) => {
                if (failure) reject(failure);
                else if (code === 0) resolve();
                else reject(new Error(`Handler exited ${code === null ? sig : code}; batch remains unacknowledged`));
            });
            child.stdin.on('error', error => { if (error.code !== 'EPIPE') fail(error); });
            // Never pass the lease token or API key in the payload or argv.
            child.stdin.end(JSON.stringify({ source: 'shareone', consumer: opts.consumer, events: batch.events }) + '\n');
            if (signal?.aborted) abort();
        });
    } finally {
        clearTimeout(timeout);
        clearInterval(heartbeat);
        signal?.removeEventListener('abort', abort);
    }
}

async function watch(opts, signal) {
    const root = `/api/v1/agent-consumers/${encodeURIComponent(opts.consumer)}`;
    const request = (suffix, payload, method = 'POST') => requestShareOneJson(root + suffix, { method, timeoutMs: 35000 }, payload);
    let registered = false;
    let failures = 0;
    while (!signal?.aborted) {
        let batch;
        let acknowledged = false;
        try {
            if (!registered) {
                await request('', { share_id: opts.share ? extractShareRef(opts.share) : null, start: opts.start }, 'PUT');
                registered = true;
            }
            batch = await request('/poll', { wait_seconds: opts.once ? 0 : 20, limit: 50 });
            if (!batch.lease_token) {
                if (opts.once) return;
                continue;
            }
            const events = opts.allActors ? batch.events : batch.events.filter(e => e.actor_role === 'visitor');
            if (events.length) await runHandler(opts, { ...batch, events }, () => request('/renew', { lease_token: batch.lease_token }), signal);
            if (signal?.aborted) throw new Error('Watcher stopping before acknowledgment');
            const result = await request('/ack', { lease_token: batch.lease_token });
            acknowledged = true;
            console.log(JSON.stringify({ consumer: opts.consumer, acknowledged_through: result.cursor, handled: events.length }));
            failures = 0;
            if (opts.once) return;
        } catch (error) {
            if (opts.once || (!registered && error.statusCode === 409) || [400, 401, 403, 404, 422].includes(error.statusCode)) throw error;
            // No response bodies, credentials, or comment text in watcher errors.
            console.error(`ShareOne delivery failed (${error.statusCode || error.code || 'handler/transport'}); retrying without advancing the cursor`);
            failures++;
        } finally {
            if (batch?.lease_token && !acknowledged) {
                try { await request('/release', { lease_token: batch.lease_token }); } catch { /* Expiration also releases it after a crash/network outage. */ }
            }
        }
        if (failures) {
            try { await delay(Math.min(60000, 1000 * 2 ** Math.min(failures - 1, 6)), undefined, { signal }); }
            catch { return; }
        }
    }
}

if (require.main === module) {
    const controller = new AbortController();
    process.once('SIGINT', () => controller.abort());
    process.once('SIGTERM', () => controller.abort());
    (async () => {
        const opts = parseArgs(process.argv.slice(2));
        if (opts.help) {
            console.log('Usage: node agent_watch.js --consumer NAME [--share URL_OR_REF] [--start beginning|now] [--once] [--all-actors] [--cwd PATH] [--timeout-seconds 1800] (--command-json [EXECUTABLE,ARGS...] | --scode-session PATH [--scode-args-json [ARGS...]])\nReceives durable comment events; handler gets JSON on stdin. Only exit 0 acknowledges. Keep this process supervised for automatic wakeups.');
            return;
        }
        await watch(opts, controller.signal);
    })().catch(error => {
        process.exitCode = printShareOneScriptError(error);
    });
}

module.exports = { parseArgs, runHandler, watch };
