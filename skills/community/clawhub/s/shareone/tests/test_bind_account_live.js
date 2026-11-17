#!/usr/bin/env node

/**
 * Live integration tests for bind_account.js
 *
 * Requires a running ShareOne server. Set environment variables:
 *   SHAREONE_API_KEY   — a valid API key (guest key is fine)
 *   SHAREONE_BASE_URL  — (optional, default: https://shareone.app)
 *
 * Run:
 *   SHAREONE_API_KEY=<key> node tests/test_bind_account_live.js
 *
 * Tests cover:
 *   1. CLI argument validation (no network needed)
 *   2. --send with a real guest key → CODE_SENT
 *   3. --verify with wrong code → error token
 *   4. --verify with bad format → error token
 *   5. Full workflow: create guest key → send code → verify wrong code → correct error tokens
 */

const { execFileSync, execFile } = require('child_process');
const path = require('path');

const SCRIPT = path.join(__dirname, '..', 'scripts', 'bind_account.js');
const CREATE_GUEST = path.join(__dirname, '..', 'scripts', 'create_guest_key.js');
const TEST_EMAIL = `test-bind-${Date.now()}@shareone-test.example.com`;

let passed = 0;
let failed = 0;
let skipped = 0;
const results = [];

function run(args, opts = {}) {
    const env = { ...process.env, ...(opts.env || {}) };
    try {
        const output = execFileSync('node', [SCRIPT, ...args], {
            encoding: 'utf8',
            env,
            timeout: 15000,
        });
        return { stdout: output, stderr: '', exitCode: 0 };
    } catch (error) {
        return {
            stdout: error.stdout || '',
            stderr: error.stderr || '',
            exitCode: error.status || 1,
        };
    }
}

function assert(condition, message) {
    if (!condition) throw new Error(`Assertion failed: ${message}`);
}

function test(name, fn) {
    try {
        fn();
        passed++;
        results.push({ name, status: 'PASS' });
        console.log(`  ✓ ${name}`);
    } catch (error) {
        failed++;
        results.push({ name, status: 'FAIL', error: error.message });
        console.log(`  ✗ ${name}`);
        console.log(`    ${error.message}`);
    }
}

function skip(name, reason) {
    skipped++;
    results.push({ name, status: 'SKIP', reason });
    console.log(`  - ${name} (skipped: ${reason})`);
}

// --- CLI argument validation tests (no network) ---

console.log('\n== CLI Argument Validation ==');

test('no arguments → ERROR:NO_ACTION', () => {
    const r = run([], { env: { SHAREONE_API_KEY: 'sk-fake' } });
    assert(r.exitCode !== 0, 'should exit non-zero');
    assert(r.stderr.includes('ERROR:NO_ACTION'), `expected ERROR:NO_ACTION, got: ${r.stderr}`);
});

test('--send without --email → ERROR:MISSING_EMAIL', () => {
    const r = run(['--send'], { env: { SHAREONE_API_KEY: 'sk-fake' } });
    assert(r.exitCode !== 0, 'should exit non-zero');
    assert(r.stderr.includes('ERROR:MISSING_EMAIL'), `expected ERROR:MISSING_EMAIL, got: ${r.stderr}`);
});

test('--verify without --email → ERROR:MISSING_EMAIL', () => {
    const r = run(['--verify'], { env: { SHAREONE_API_KEY: 'sk-fake' } });
    assert(r.exitCode !== 0, 'should exit non-zero');
    assert(r.stderr.includes('ERROR:MISSING_EMAIL'), `expected ERROR:MISSING_EMAIL, got: ${r.stderr}`);
});

test('--verify without --code → ERROR:MISSING_CODE', () => {
    const r = run(['--verify', '--email', 'a@b.com'], { env: { SHAREONE_API_KEY: 'sk-fake' } });
    assert(r.exitCode !== 0, 'should exit non-zero');
    assert(r.stderr.includes('ERROR:MISSING_CODE'), `expected ERROR:MISSING_CODE, got: ${r.stderr}`);
});

test('--verify with non-6-digit code → ERROR:INVALID_CODE_FORMAT', () => {
    const r = run(['--verify', '--email', 'a@b.com', '--code', 'abc'], { env: { SHAREONE_API_KEY: 'sk-fake' } });
    assert(r.exitCode !== 0, 'should exit non-zero');
    assert(r.stderr.includes('ERROR:INVALID_CODE_FORMAT'), `expected ERROR:INVALID_CODE_FORMAT, got: ${r.stderr}`);
});

test('unknown argument → ERROR:UNKNOWN_ARGUMENT', () => {
    const r = run(['--send', '--email', 'a@b.com', '--bogus'], { env: { SHAREONE_API_KEY: 'sk-fake' } });
    assert(r.exitCode !== 0, 'should exit non-zero');
    assert(r.stderr.includes('ERROR:UNKNOWN_ARGUMENT'), `expected ERROR:UNKNOWN_ARGUMENT, got: ${r.stderr}`);
});

(() => {
    // This test only works when no local .shareone_credentials exists and
    // SHAREONE_API_KEY is not set, because readLocalApiKey reads from the
    // skill directory which we cannot override via env vars.
    const fs = require('fs');
    const credPath = path.join(__dirname, '..', '.shareone_credentials');
    if (process.env.SHAREONE_API_KEY || fs.existsSync(credPath)) {
        skip('--send without API key → ERROR:KEY_NOT_FOUND', 'API key available via env or local credentials');
    } else {
        test('--send without API key → ERROR:KEY_NOT_FOUND', () => {
            const r = run(['--send', '--email', 'a@b.com'], {
                env: { SHAREONE_API_KEY: '' },
            });
            assert(r.exitCode !== 0, 'should exit non-zero');
            assert(r.stderr.includes('ERROR:KEY_NOT_FOUND'), `expected ERROR:KEY_NOT_FOUND, got: ${r.stderr}`);
        });
    }
})();

// --- Live API tests (require SHAREONE_API_KEY) ---

const API_KEY = process.env.SHAREONE_API_KEY;

if (!API_KEY) {
    console.log('\n== Live API Tests ==');
    skip('send code with real key', 'SHAREONE_API_KEY not set');
    skip('verify with wrong code', 'SHAREONE_API_KEY not set');
    skip('guest key workflow: create → send → verify wrong', 'SHAREONE_API_KEY not set');
} else {
    console.log('\n== Live API Tests ==');

    test('--send with real key → CODE_SENT', () => {
        const r = run(['--send', '--email', TEST_EMAIL, '--api-key', API_KEY]);
        assert(r.exitCode === 0, `expected exit 0, got ${r.exitCode}. stderr: ${r.stderr}`);
        assert(r.stdout.includes('CODE_SENT'), `expected CODE_SENT in stdout, got: ${r.stdout}`);
        assert(r.stdout.includes(TEST_EMAIL), `expected email in output, got: ${r.stdout}`);
    });

    test('--verify with wrong code → error token (CODE_EXPIRED or INVALID_CODE)', () => {
        const r = run(['--verify', '--email', TEST_EMAIL, '--code', '000000', '--api-key', API_KEY]);
        assert(r.exitCode !== 0, 'should exit non-zero for wrong code');
        const out = r.stdout + r.stderr;
        const hasExpectedError = out.includes('ERROR:INVALID_CODE') ||
            out.includes('ERROR:CODE_EXPIRED') ||
            out.includes('ERROR:VERIFY_FAILED');
        assert(hasExpectedError, `expected an error token, got: ${out}`);
    });

    // Full workflow: create a fresh guest key → send code → verify with wrong code
    test('guest key workflow: create → send → verify wrong code', () => {
        // Step 1: Create a fresh guest key
        let guestKey;
        try {
            const createOut = execFileSync('node', [CREATE_GUEST], {
                encoding: 'utf8',
                timeout: 15000,
            });
            const match = createOut.match(/GUEST_KEY_CREATED:(\S+)/);
            assert(match, `expected GUEST_KEY_CREATED token, got: ${createOut}`);
            guestKey = match[1];
        } catch (error) {
            const out = (error.stdout || '') + (error.stderr || '');
            if (out.includes('RATE_LIMIT')) {
                throw new Error('SKIP: guest key creation rate limited');
            }
            throw new Error(`Failed to create guest key: ${out}`);
        }

        // Step 2: Send code to a unique email
        const uniqueEmail = `test-wf-${Date.now()}@shareone-test.example.com`;
        const sendResult = run(['--send', '--email', uniqueEmail, '--api-key', guestKey]);
        assert(sendResult.exitCode === 0, `send failed: ${sendResult.stdout} ${sendResult.stderr}`);
        assert(sendResult.stdout.includes('CODE_SENT'), `expected CODE_SENT, got: ${sendResult.stdout}`);

        // Step 3: Verify with wrong code → should get error
        const verifyResult = run(['--verify', '--email', uniqueEmail, '--code', '999999', '--api-key', guestKey]);
        assert(verifyResult.exitCode !== 0, 'wrong code should fail');
        const verifyOut = verifyResult.stdout + verifyResult.stderr;
        const hasError = verifyOut.includes('ERROR:INVALID_CODE') ||
            verifyOut.includes('ERROR:CODE_EXPIRED') ||
            verifyOut.includes('ERROR:VERIFY_FAILED');
        assert(hasError, `expected error token for wrong code, got: ${verifyOut}`);
    });
}

// --- Summary ---

console.log(`\n== Summary: ${passed} passed, ${failed} failed, ${skipped} skipped ==\n`);
process.exit(failed > 0 ? 1 : 0);
